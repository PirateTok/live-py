import http.cookiejar
import urllib.request
from typing import Optional

from ..http.ua import random_ua


def fetch_ttwid(
    timeout: float = 10.0, proxy: str = "", user_agent: Optional[str] = None
) -> str:
    """Fetch a fresh ttwid cookie via anonymous GET to tiktok.com.

    Args:
        timeout: HTTP request timeout in seconds.
        proxy: Optional proxy URL (HTTP/HTTPS/SOCKS5).
        user_agent: Custom user agent. When None, picks a random UA from pool.
    """
    ua = user_agent if user_agent else random_ua()
    jar = http.cookiejar.CookieJar()
    handlers: list = [urllib.request.HTTPCookieProcessor(jar)]
    if proxy:
        handlers.append(urllib.request.ProxyHandler({"https": proxy, "http": proxy}))
    opener = urllib.request.build_opener(*handlers)
    req = urllib.request.Request(
        "https://www.tiktok.com/",
        headers={"User-Agent": ua},
    )
    opener.open(req, timeout=timeout).close()

    for cookie in jar:
        if cookie.name == "ttwid":
            return cookie.value

    raise RuntimeError("ttwid: no ttwid cookie in response")
