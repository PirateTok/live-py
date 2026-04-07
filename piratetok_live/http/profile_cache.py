import threading
import time
from typing import Optional, Union

from ..auth.ttwid import fetch_ttwid
from ..errors import (
    ProfileError,
    ProfileNotFoundError,
    ProfilePrivateError,
    ProfileScrapeError,
)
from .sigi import SigiProfile, scrape_profile

_DEFAULT_TTL = 300.0  # 5 minutes
_TTWID_TIMEOUT = 10.0
_SCRAPE_TIMEOUT = 15.0

_CacheValue = Union[SigiProfile, Exception]


class _CacheEntry:
    __slots__ = ("value", "inserted_at")

    def __init__(self, value: _CacheValue) -> None:
        self.value = value
        self.inserted_at = time.monotonic()


class ProfileCache:
    """Cached profile fetcher that scrapes TikTok profile pages for HD
    avatars and profile metadata.

    Thread-safe via threading.Lock.

    Example::

        cache = ProfileCache()
        profile = cache.fetch("tiktok")
        print(f"{profile.nickname} -- {profile.follower_count} followers")
        print(f"HD avatar: {profile.avatar_large}")

        # Second call is instant (cached)
        cached = cache.fetch("tiktok")
    """

    def __init__(
        self,
        ttl: float = _DEFAULT_TTL,
        proxy: str = "",
        user_agent: Optional[str] = None,
        cookies: str = "",
    ) -> None:
        self._ttl = ttl
        self._proxy = proxy
        self._user_agent = user_agent
        self._cookies = cookies
        self._ttwid: Optional[str] = None
        self._entries: dict = {}
        self._lock = threading.Lock()

    def fetch(self, username: str) -> SigiProfile:
        """Return cached profile if valid, otherwise scrape and cache."""
        key = _normalize_key(username)

        with self._lock:
            entry = self._entries.get(key)
            if entry is not None and (time.monotonic() - entry.inserted_at) < self._ttl:
                if isinstance(entry.value, Exception):
                    raise entry.value
                return entry.value

        ttwid = self._ensure_ttwid()

        try:
            profile = scrape_profile(
                key,
                ttwid,
                timeout=_SCRAPE_TIMEOUT,
                user_agent=self._user_agent,
                proxy=self._proxy,
                cookies=self._cookies,
            )
        except (ProfilePrivateError, ProfileNotFoundError, ProfileError) as err:
            # Negative cache
            with self._lock:
                self._entries[key] = _CacheEntry(err)
            raise

        with self._lock:
            self._entries[key] = _CacheEntry(profile)
        return profile

    def cached(self, username: str) -> Optional[SigiProfile]:
        """Return cached profile without fetching. None on miss or expiry."""
        key = _normalize_key(username)
        with self._lock:
            entry = self._entries.get(key)
            if entry is None:
                return None
            if (time.monotonic() - entry.inserted_at) >= self._ttl:
                return None
            if isinstance(entry.value, Exception):
                return None
            return entry.value

    def invalidate(self, username: str) -> None:
        """Remove one entry from cache."""
        key = _normalize_key(username)
        with self._lock:
            self._entries.pop(key, None)

    def invalidate_all(self) -> None:
        """Clear entire cache."""
        with self._lock:
            self._entries.clear()

    def _ensure_ttwid(self) -> str:
        with self._lock:
            if self._ttwid is not None:
                return self._ttwid

        ttwid = fetch_ttwid(
            timeout=_TTWID_TIMEOUT,
            proxy=self._proxy,
            user_agent=self._user_agent,
        )

        with self._lock:
            self._ttwid = ttwid
        return ttwid


def _normalize_key(username: str) -> str:
    return username.strip().lstrip("@").lower()
