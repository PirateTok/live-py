import os
import random
from datetime import datetime, timezone

_USER_AGENTS = (
    "Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:138.0) Gecko/20100101 Firefox/138.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14.7; rv:139.0) Gecko/20100101 Firefox/139.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
)

_FALLBACK_TZ = "UTC"
_FALLBACK_LANG = "en"
_FALLBACK_REGION = "US"
_SKIP_LOCALES = {"C", "POSIX", ""}


def random_ua() -> str:
    """Pick a random user agent from the built-in pool."""
    return random.choice(_USER_AGENTS)


def system_timezone() -> str:
    """Detect the system's IANA timezone name.

    Tries (in order):
    1. Python's zoneinfo tzinfo.key (3.9+)
    2. /etc/timezone file
    3. /etc/localtime symlink
    Falls back to "UTC" when detection fails.
    """
    tz = _tz_from_python()
    if tz is not None:
        return tz

    tz = _tz_from_etc_timezone()
    if tz is not None:
        return tz

    tz = _tz_from_localtime_link()
    if tz is not None:
        return tz

    return _FALLBACK_TZ


def system_locale() -> tuple:
    """Detect system language and region from POSIX locale.

    Tries LC_ALL, then LANG env var. Falls back to ("en", "US").
    Returns (language, region) tuple.
    """
    for var in ("LC_ALL", "LANG"):
        val = os.environ.get(var, "").strip()
        if val in _SKIP_LOCALES:
            continue
        parsed = _parse_posix_locale(val)
        if parsed is not None:
            return parsed
    return (_FALLBACK_LANG, _FALLBACK_REGION)


def system_language() -> str:
    """Detect system language code (e.g. "en", "ro", "pt")."""
    return system_locale()[0]


def system_region() -> str:
    """Detect system region/country code (e.g. "US", "RO", "BR")."""
    return system_locale()[1]


def _parse_posix_locale(s: str) -> "tuple | None":
    """Parse 'll_CC.encoding' / 'll_CC' / 'll-CC' into (lang, region)."""
    base = s.split(".")[0]
    parts = base.replace("-", "_").split("_", 1)
    lang = parts[0].lower()
    if len(lang) < 2:
        return None
    region = parts[1].upper() if len(parts) > 1 else _FALLBACK_REGION
    return (lang, region)


def _tz_from_python() -> "str | None":
    """Try to get IANA name via Python's datetime/zoneinfo."""
    try:
        tzinfo = datetime.now(timezone.utc).astimezone().tzinfo
        if tzinfo is not None:
            key = getattr(tzinfo, "key", None)
            if isinstance(key, str) and "/" in key and key.strip():
                return key.strip()
    except (AttributeError, OSError):
        pass
    return None


def _tz_from_etc_timezone() -> "str | None":
    """Read /etc/timezone (Debian/Ubuntu)."""
    try:
        with open("/etc/timezone", "r", encoding="utf-8") as f:
            tz = f.read().strip()
        if tz and "/" in tz:
            return tz
    except OSError:
        pass
    return None


def _tz_from_localtime_link() -> "str | None":
    """Parse /etc/localtime symlink target."""
    try:
        target = os.readlink("/etc/localtime")
        parts = target.split("/zoneinfo/")
        if len(parts) >= 2 and parts[1]:
            return parts[1]
    except OSError:
        pass
    return None
