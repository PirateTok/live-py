import random
import urllib.parse

from ..http.ua import system_timezone


def build_wss_url(
    cdn_host: str,
    room_id: str,
    language: str = "en",
    region: str = "US",
    compress: bool = True,
) -> str:
    last_rtt = f"{100 + random.random() * 100:.3f}"
    tz = system_timezone()
    browser_language = f"{language}-{region}"

    params = urllib.parse.urlencode({
        "version_code": "180800",
        "device_platform": "web",
        "cookie_enabled": "true",
        "screen_width": "1920",
        "screen_height": "1080",
        "browser_language": browser_language,
        "browser_platform": "Linux x86_64",
        "browser_name": "Mozilla",
        "browser_version": "5.0 (X11)",
        "browser_online": "true",
        "tz_name": tz,
        "app_name": "tiktok_web",
        "sup_ws_ds_opt": "1",
        "update_version_code": "2.0.0",
        "compress": "gzip" if compress else "",
        "webcast_language": language,
        "ws_direct": "1",
        "aid": "1988",
        "live_id": "12",
        "app_language": language,
        "client_enter": "1",
        "room_id": room_id,
        "identity": "audience",
        "history_comment_count": "6",
        "last_rtt": last_rtt,
        "heartbeat_duration": "10000",
        "resp_content_type": "protobuf",
        "did_rule": "3",
    })

    return f"wss://{cdn_host}/webcast/im/ws_proxy/ws_reuse_supplement/?{params}"
