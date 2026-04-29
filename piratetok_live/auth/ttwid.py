import http.cookiejar
import urllib.request
from typing import Optional

from ..http.ua import random_ua

_BROWSER_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
}


def fetch_ttwid(
    timeout: float = 10.0,
    proxy: str = "",
    user_agent: Optional[str] = None,
    username: Optional[str] = None,
) -> str:
    """Fetch a fresh ttwid cookie via anonymous GET to a TikTok profile page.

    The homepage (``https://www.tiktok.com/``) stopped reliably minting ttwid
    in late 2026 — TikTok's edge returns ``X-TT-System-Error: 3`` and refuses
    to set the cookie. Profile pages (``/@{username}``) still mint it
    consistently. We try the target user's profile first, then fall back to
    ``/@tiktok`` (canonical first-party page).

    Args:
        timeout: HTTP request timeout in seconds.
        proxy: Optional proxy URL (HTTP/HTTPS/SOCKS5).
        user_agent: Custom user agent. When None, picks a random UA from pool.
        username: Target streamer's username. When given, ttwid is fetched from
            their profile page (warming the edge for the upcoming WSS connect).
    """
    ua = user_agent if user_agent else random_ua()

    candidates = []
    if username:
        candidates.append(f"https://www.tiktok.com/@{username}")
    candidates.append("https://www.tiktok.com/@tiktok")

    last_error: Optional[Exception] = None
    for url in candidates:
        try:
            value = _try_fetch(url, ua, timeout, proxy)
            if value:
                return value
        except Exception as e:  # noqa: BLE001 — we re-raise after all candidates exhausted
            last_error = e
            continue

    if last_error is not None:
        raise RuntimeError(
            f"ttwid: all bootstrap URLs failed (last error: {last_error}). "
            "TikTok may be blocking your IP/region or your proxy is broken."
        ) from last_error
    raise RuntimeError(
        "ttwid: no bootstrap URL returned a ttwid cookie. "
        "TikTok likely served a challenge page (IP/region block or fingerprint flag)."
    )


def _try_fetch(url: str, ua: str, timeout: float, proxy: str) -> Optional[str]:
    jar = http.cookiejar.CookieJar()
    handlers: list = [urllib.request.HTTPCookieProcessor(jar)]
    if proxy:
        handlers.append(urllib.request.ProxyHandler({"https": proxy, "http": proxy}))
    opener = urllib.request.build_opener(*handlers)

    headers = dict(_BROWSER_HEADERS)
    headers["User-Agent"] = ua
    req = urllib.request.Request(url, headers=headers)
    opener.open(req, timeout=timeout).close()

    for cookie in jar:
        if cookie.name == "ttwid":
            return cookie.value
    return None
