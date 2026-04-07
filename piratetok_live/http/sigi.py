import json
import urllib.request
from typing import Optional

from ..errors import (
    ProfileError,
    ProfileNotFoundError,
    ProfilePrivateError,
    ProfileScrapeError,
)
from .ua import random_ua

_SIGI_MARKER = 'id="__UNIVERSAL_DATA_FOR_REHYDRATION__"'


class SigiProfile:
    """Profile data scraped from a TikTok profile page via SIGI state.

    Contains HD avatar URLs (720x720 and 1080x1080) plus basic profile
    metadata. All fields except bio_link are guaranteed present on public
    profiles.
    """

    __slots__ = (
        "user_id",
        "unique_id",
        "nickname",
        "bio",
        "avatar_thumb",
        "avatar_medium",
        "avatar_large",
        "verified",
        "private_account",
        "is_organization",
        "room_id",
        "bio_link",
        "follower_count",
        "following_count",
        "heart_count",
        "video_count",
        "friend_count",
    )

    def __init__(
        self,
        user_id: str,
        unique_id: str,
        nickname: str,
        bio: str,
        avatar_thumb: str,
        avatar_medium: str,
        avatar_large: str,
        verified: bool,
        private_account: bool,
        is_organization: bool,
        room_id: str,
        bio_link: Optional[str],
        follower_count: int,
        following_count: int,
        heart_count: int,
        video_count: int,
        friend_count: int,
    ) -> None:
        self.user_id = user_id
        self.unique_id = unique_id
        self.nickname = nickname
        self.bio = bio
        self.avatar_thumb = avatar_thumb
        self.avatar_medium = avatar_medium
        self.avatar_large = avatar_large
        self.verified = verified
        self.private_account = private_account
        self.is_organization = is_organization
        self.room_id = room_id
        self.bio_link = bio_link
        self.follower_count = follower_count
        self.following_count = following_count
        self.heart_count = heart_count
        self.video_count = video_count
        self.friend_count = friend_count


def scrape_profile(
    username: str,
    ttwid: str,
    timeout: float = 15.0,
    user_agent: Optional[str] = None,
    proxy: str = "",
    cookies: str = "",
) -> SigiProfile:
    """Scrape a TikTok profile page and extract profile data from the
    embedded SIGI JSON blob.

    This is a stateless function -- no caching. Use ProfileCache for
    cached access.
    """
    clean = username.strip().lstrip("@").lower()
    ua = user_agent if user_agent else random_ua()

    cookie_header = _build_cookie_header(ttwid, cookies)

    handlers: list = []
    if proxy:
        handlers.append(urllib.request.ProxyHandler({"https": proxy, "http": proxy}))
    opener = urllib.request.build_opener(*handlers)

    req = urllib.request.Request(
        f"https://www.tiktok.com/@{clean}",
        headers={
            "User-Agent": ua,
            "Cookie": cookie_header,
            "Accept-Language": "en-US,en;q=0.9",
        },
    )
    with opener.open(req, timeout=timeout) as resp:
        html = resp.read().decode("utf-8")

    json_str = _extract_sigi_json(html)
    blob = json.loads(json_str)

    user_detail = blob.get("__DEFAULT_SCOPE__", {}).get("webapp.user-detail")
    if user_detail is None:
        raise ProfileScrapeError("missing __DEFAULT_SCOPE__/webapp.user-detail")

    status_code = user_detail.get("statusCode", 0)
    if status_code != 0:
        if status_code == 10222:
            raise ProfilePrivateError(clean)
        if status_code in (10221, 10223):
            raise ProfileNotFoundError(clean)
        raise ProfileError(status_code)

    user_info = user_detail.get("userInfo")
    if user_info is None:
        raise ProfileScrapeError("missing userInfo")

    user = user_info.get("user", {})
    stats = user_info.get("stats", {})

    bio_link_obj = user.get("bioLink")
    bio_link = None
    if isinstance(bio_link_obj, dict):
        link_val = bio_link_obj.get("link", "")
        if link_val:
            bio_link = link_val

    return SigiProfile(
        user_id=str(user.get("id", "")),
        unique_id=str(user.get("uniqueId", "")),
        nickname=str(user.get("nickname", "")),
        bio=str(user.get("signature", "")),
        avatar_thumb=str(user.get("avatarThumb", "")),
        avatar_medium=str(user.get("avatarMedium", "")),
        avatar_large=str(user.get("avatarLarger", "")),
        verified=bool(user.get("verified", False)),
        private_account=bool(user.get("privateAccount", False)),
        is_organization=int(user.get("isOrganization", 0)) != 0,
        room_id=str(user.get("roomId", "")),
        bio_link=bio_link,
        follower_count=int(stats.get("followerCount", 0)),
        following_count=int(stats.get("followingCount", 0)),
        heart_count=int(stats.get("heartCount", 0)),
        video_count=int(stats.get("videoCount", 0)),
        friend_count=int(stats.get("friendCount", 0)),
    )


def _extract_sigi_json(html: str) -> str:
    """Extract the JSON string from the SIGI script tag via string searching.
    No regex, no HTML parser.
    """
    marker_pos = html.find(_SIGI_MARKER)
    if marker_pos == -1:
        raise ProfileScrapeError("SIGI script tag not found in HTML")

    gt_pos = html.find(">", marker_pos)
    if gt_pos == -1:
        raise ProfileScrapeError("no > after SIGI marker")

    json_start = gt_pos + 1
    script_end = html.find("</script>", json_start)
    if script_end == -1:
        raise ProfileScrapeError("no </script> after SIGI JSON")

    json_str = html[json_start:script_end]
    if not json_str:
        raise ProfileScrapeError("empty SIGI JSON blob")

    return json_str


def _build_cookie_header(ttwid: str, cookies: str) -> str:
    """Build Cookie header with ttwid, stripping any user-provided ttwid."""
    if not cookies:
        return f"ttwid={ttwid}"
    # Strip user-provided ttwid so the fresh one always wins
    filtered = "; ".join(
        pair for pair in cookies.split("; ") if not pair.startswith("ttwid=")
    )
    if not filtered:
        return f"ttwid={ttwid}"
    return f"ttwid={ttwid}; {filtered}"
