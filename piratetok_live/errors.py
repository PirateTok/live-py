class PirateTokError(Exception):
    pass


class UserNotFoundError(PirateTokError):
    def __init__(self, username: str) -> None:
        self.username = username
        super().__init__(f'user "{username}" does not exist')


class HostNotOnlineError(PirateTokError):
    def __init__(self, username: str) -> None:
        self.username = username
        super().__init__(f'user "{username}" is not currently live')


class TikTokBlockedError(PirateTokError):
    def __init__(self, status_code: int) -> None:
        self.status_code = status_code
        super().__init__(f"tiktok blocked (HTTP {status_code})")


class TikTokApiError(PirateTokError):
    def __init__(self, code: int) -> None:
        self.code = code
        super().__init__(f"tiktok API error: statusCode={code}")


class DeviceBlockedError(PirateTokError):
    """TikTok flagged this ttwid as DEVICE_BLOCKED. Fetch a fresh one."""

    def __init__(self) -> None:
        super().__init__("device blocked — ttwid was flagged, fetch a fresh one")


class AgeRestrictedError(PirateTokError):
    def __init__(self) -> None:
        super().__init__(
            "age-restricted stream: 18+ room — pass session cookies to fetch_room_info()"
        )


class ProfilePrivateError(PirateTokError):
    def __init__(self, username: str) -> None:
        self.username = username
        super().__init__(f"profile is private: @{username}")


class ProfileNotFoundError(PirateTokError):
    def __init__(self, username: str) -> None:
        self.username = username
        super().__init__(f"profile not found: @{username}")


class ProfileScrapeError(PirateTokError):
    def __init__(self, reason: str) -> None:
        self.reason = reason
        super().__init__(f"failed to scrape profile: {reason}")


class ProfileError(PirateTokError):
    def __init__(self, code: int) -> None:
        self.code = code
        super().__init__(f"profile fetch error: statusCode={code}")
