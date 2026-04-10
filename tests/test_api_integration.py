"""
Integration tests for HTTP API (H1-H4).

Tests hit real TikTok endpoints. All tests are skipped unless the
appropriate environment variable is set — default ``pytest`` stays green.

Environment variables:
  PIRATETOK_LIVE_TEST_USER         — live TikTok username (for H1, H4)
  PIRATETOK_LIVE_TEST_OFFLINE_USER — offline TikTok username (for H2)
  PIRATETOK_LIVE_TEST_COOKIES      — browser cookie header for 18+ (optional, H4)
  PIRATETOK_LIVE_TEST_HTTP         — set to 1/true/yes to enable H3 (nonexistent probe)
"""

import os

import pytest

from piratetok_live.errors import HostNotOnlineError, UserNotFoundError
from piratetok_live.http.api import RoomInfo, RoomIdResult, check_online, fetch_room_info

pytestmark = pytest.mark.integration

_SYNTHETIC_NONEXISTENT_USER = "piratetok_py_nf_7a3c9e2f1b8d4a6c0e5f3a2b1d9c8e7"
_HTTP_TIMEOUT = 25.0

_HAVE_TEST_USER = bool(os.environ.get("PIRATETOK_LIVE_TEST_USER", "").strip())
_HAVE_OFFLINE_USER = bool(os.environ.get("PIRATETOK_LIVE_TEST_OFFLINE_USER", "").strip())
_HAVE_HTTP = os.environ.get("PIRATETOK_LIVE_TEST_HTTP", "").strip().lower() in ("1", "true", "yes")


@pytest.mark.skipif(
    not _HAVE_TEST_USER,
    reason="set PIRATETOK_LIVE_TEST_USER to a live TikTok username",
)
def test_check_online_live_user() -> None:
    """H1 — check_online on a live user returns a valid room ID."""
    user = os.environ["PIRATETOK_LIVE_TEST_USER"].strip()
    result = check_online(user, _HTTP_TIMEOUT)
    assert isinstance(result, RoomIdResult)
    assert result.room_id, "room_id must not be empty"
    assert result.room_id != "0", "room_id must not be '0'"


@pytest.mark.skipif(
    not _HAVE_OFFLINE_USER,
    reason="set PIRATETOK_LIVE_TEST_OFFLINE_USER to an offline TikTok username",
)
def test_check_online_offline_user() -> None:
    """H2 — check_online on an offline user raises HostNotOnlineError (not blocked/not found)."""
    user = os.environ["PIRATETOK_LIVE_TEST_OFFLINE_USER"].strip()
    with pytest.raises(HostNotOnlineError) as exc_info:
        check_online(user, _HTTP_TIMEOUT)
    err = exc_info.value
    assert user in str(err) or hasattr(err, "username"), (
        "HostNotOnlineError must reference the username"
    )
    assert "not" in str(err).lower() or "offline" in str(err).lower(), (
        f"error message should say 'not online' or 'offline', got: {err}"
    )


@pytest.mark.skipif(
    not _HAVE_HTTP,
    reason="set PIRATETOK_LIVE_TEST_HTTP=1 to enable the nonexistent-user probe (safe, fixed synthetic username)",
)
def test_check_online_nonexistent_user() -> None:
    """H3 — check_online on a nonexistent username raises UserNotFoundError."""
    with pytest.raises(UserNotFoundError) as exc_info:
        check_online(_SYNTHETIC_NONEXISTENT_USER, _HTTP_TIMEOUT)
    err = exc_info.value
    assert err.username == _SYNTHETIC_NONEXISTENT_USER, (
        f"UserNotFoundError.username must match the queried username, got: {err.username!r}"
    )


@pytest.mark.skipif(
    not _HAVE_TEST_USER,
    reason="set PIRATETOK_LIVE_TEST_USER to a live TikTok username",
)
def test_fetch_room_info_live_room() -> None:
    """H4 — fetch_room_info on a live room returns room metadata with non-negative viewer count."""
    user = os.environ["PIRATETOK_LIVE_TEST_USER"].strip()
    cookies = os.environ.get("PIRATETOK_LIVE_TEST_COOKIES", "")

    room = check_online(user, _HTTP_TIMEOUT)
    assert room.room_id and room.room_id != "0"

    info = fetch_room_info(room.room_id, _HTTP_TIMEOUT, cookies)
    assert isinstance(info, RoomInfo)
    assert info.viewers >= 0, f"viewers must be >= 0, got {info.viewers}"
