import asyncio
import logging
from typing import Callable, Dict, List, Optional

from .auth.ttwid import fetch_ttwid
from .connection.url import build_wss_url
from .connection.wss import connect_wss
from .errors import DeviceBlockedError
from .events.types import EventType, TikTokEvent
from .http.api import RoomIdResult, RoomInfo, check_online, fetch_room_info
from .http.ua import system_language, system_region

_DEFAULT_CDN = "webcast-ws.tiktok.com"
_log = logging.getLogger("piratetok_live.client")


class TikTokLiveClient:
    def __init__(self, username: str) -> None:
        self._username = username
        self._cdn_host = _DEFAULT_CDN
        self._timeout = 10.0
        self._max_retries = 5
        self._stale_timeout = 60.0
        self._proxy = ""
        self._user_agent: Optional[str] = None
        self._cookies: Optional[str] = None
        self._language: Optional[str] = None
        self._region: Optional[str] = None
        self._stop: Optional[asyncio.Event] = None
        self._listeners: Dict[str, List[Callable]] = {}

    def cdn_eu(self) -> "TikTokLiveClient":
        self._cdn_host = "webcast-ws.eu.tiktok.com"
        return self

    def cdn_us(self) -> "TikTokLiveClient":
        self._cdn_host = "webcast-ws.us.tiktok.com"
        return self

    def cdn(self, host: str) -> "TikTokLiveClient":
        self._cdn_host = host
        return self

    def timeout(self, seconds: float) -> "TikTokLiveClient":
        self._timeout = seconds
        return self

    def max_retries(self, n: int) -> "TikTokLiveClient":
        self._max_retries = n
        return self

    def stale_timeout(self, seconds: float) -> "TikTokLiveClient":
        self._stale_timeout = seconds
        return self

    def proxy(self, url: str) -> "TikTokLiveClient":
        self._proxy = url
        return self

    def user_agent(self, ua: str) -> "TikTokLiveClient":
        """Override the user agent for all requests (HTTP + WSS).

        When not set, a random UA from the built-in pool is picked on each
        reconnect attempt. This is recommended for reducing DEVICE_BLOCKED risk.
        Only set this if you have a specific UA you want to use.
        """
        self._user_agent = ua
        return self

    def language(self, lang: str) -> "TikTokLiveClient":
        """Override detected language (e.g. "pt", "ro")."""
        self._language = lang
        return self

    def region(self, reg: str) -> "TikTokLiveClient":
        """Override detected region (e.g. "BR", "RO")."""
        self._region = reg
        return self

    def cookies(self, cookies: str) -> "TikTokLiveClient":
        """Set session cookies for the WSS connection.

        These are appended alongside the ttwid cookie. Only needed if you have
        a specific reason to pass session cookies to the WebSocket handshake.

        For fetching room info on 18+ rooms, pass cookies directly to
        ``fetch_room_info()`` instead.
        """
        self._cookies = cookies
        return self

    def on(self, event_type: str) -> Callable:
        """Decorator to register an event listener."""
        def decorator(fn: Callable) -> Callable:
            self._listeners.setdefault(event_type, []).append(fn)
            return fn
        return decorator

    def _emit(self, event: TikTokEvent) -> None:
        for fn in self._listeners.get(event.type, []):
            fn(event)

    async def connect(self) -> str:
        """Connect to TikTok Live with auto-reconnection. Returns room_id."""
        room = check_online(
            self._username, self._timeout,
            proxy=self._proxy, user_agent=self._user_agent,
        )
        self._stop = asyncio.Event()
        self._emit(TikTokEvent(EventType.connected, {"room_id": room.room_id}, room.room_id))

        attempt = 0
        while not self._stop.is_set():
            ttwid = fetch_ttwid(
                self._timeout, proxy=self._proxy, user_agent=self._user_agent,
            )
            lang = self._language if self._language else system_language()
            reg = self._region if self._region else system_region()
            wss_url = build_wss_url(self._cdn_host, room.room_id, lang, reg)

            is_device_blocked = False
            try:
                await connect_wss(
                    wss_url, ttwid, room.room_id,
                    on_event=self._emit,
                    on_error=lambda e: self._emit(TikTokEvent("error", e)),
                    stop_event=self._stop,
                    stale_timeout=self._stale_timeout,
                    proxy=self._proxy,
                    user_agent=self._user_agent,
                    cookies=self._cookies,
                )
            except DeviceBlockedError:
                is_device_blocked = True
                _log.warning("DEVICE_BLOCKED — rotating ttwid + UA")

            if self._stop.is_set():
                break

            attempt += 1
            if attempt > self._max_retries:
                _log.info("max retries (%d) exceeded", self._max_retries)
                break

            # On DEVICE_BLOCKED: short delay (2s) since we're getting a fresh
            # ttwid + UA anyway. On other errors: exponential backoff.
            if is_device_blocked:
                delay = 2
            else:
                delay = min(2 ** attempt, 30)
            self._emit(TikTokEvent(
                EventType.reconnecting,
                {"attempt": attempt, "max_retries": self._max_retries, "delay": delay},
                room.room_id,
            ))
            _log.info("reconnecting in %ds (attempt %d/%d)", delay, attempt, self._max_retries)
            await asyncio.sleep(delay)

        self._emit(TikTokEvent(EventType.disconnected, None, room.room_id))
        return room.room_id

    def run(self) -> str:
        """Blocking connect — runs the asyncio event loop."""
        return asyncio.run(self.connect())

    def disconnect(self) -> None:
        if self._stop is not None:
            self._stop.set()

    @staticmethod
    def check_online(username: str, timeout: float = 10.0) -> RoomIdResult:
        return check_online(username, timeout)

    @staticmethod
    def fetch_room_info(
        room_id: str, timeout: float = 10.0, cookies: str = ""
    ) -> RoomInfo:
        return fetch_room_info(room_id, timeout, cookies)
