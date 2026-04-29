from typing import Optional

from curl_cffi import requests as cffi_requests


def fetch_ttwid(
    timeout: float = 10.0,
    proxy: str = "",
    user_agent: Optional[str] = None,
    username: Optional[str] = None,
) -> str:
    """Fetch a fresh ttwid cookie via anonymous GET to a TikTok profile page.

    Uses ``curl_cffi`` to impersonate Chrome's TLS/HTTP fingerprint. Plain
    ``urllib`` and ``requests`` get fingerprinted (JA3/JA4) by TikTok's edge
    on Windows and served a challenge page (200 OK with no cookies and
    ``X-TT-System-Error: 3`` header) — Linux happens to slip through but
    Windows consistently hits the filter.

    The homepage (``/``) stopped reliably minting ttwid in late 2026; profile
    pages still mint it. We try the target user's profile first (warms the
    edge for the upcoming WSS connect), then fall back to ``/@tiktok``.

    Args:
        timeout: HTTP request timeout in seconds.
        proxy: Optional proxy URL (HTTP/HTTPS/SOCKS5).
        user_agent: Custom user agent. When None, ``curl_cffi`` uses the UA
            matching its impersonated browser (recommended — overriding the
            UA breaks fingerprint consistency and may re-trigger anti-bot).
        username: Target streamer's username. When given, ttwid is fetched
            from their profile page.
    """
    candidates = []
    if username:
        candidates.append(f"https://www.tiktok.com/@{username}")
    candidates.append("https://www.tiktok.com/@tiktok")

    proxies = {"http": proxy, "https": proxy} if proxy else None
    headers = {"User-Agent": user_agent} if user_agent else None

    last_error: Optional[Exception] = None
    for url in candidates:
        try:
            value = _try_fetch(url, timeout, proxies, headers)
            if value:
                return value
        except Exception as e:  # noqa: BLE001 — re-raised after exhausting candidates
            last_error = e
            continue

    if last_error is not None:
        raise RuntimeError(
            f"ttwid: all bootstrap URLs failed (last error: {last_error}). "
            "TikTok may be blocking your IP/region or your proxy is broken."
        ) from last_error
    raise RuntimeError(
        "ttwid: no bootstrap URL returned a ttwid cookie. "
        "TikTok served a challenge page despite TLS impersonation — "
        "your IP is likely flagged."
    )


def _try_fetch(
    url: str,
    timeout: float,
    proxies: Optional[dict],
    headers: Optional[dict],
) -> Optional[str]:
    resp = cffi_requests.get(
        url,
        impersonate="chrome",
        timeout=timeout,
        proxies=proxies,
        headers=headers,
        allow_redirects=True,
    )
    return resp.cookies.get("ttwid")
