"""
WSS smoke tests (W1-W7) and disconnect lifecycle test (D1).

All tests require PIRATETOK_LIVE_TEST_USER (a live TikTok username).
They connect over real WebSocket and wait for specific event types.

These tests are inherently flaky on quiet streams — a stream that produces
no gifts within 180s would cause W3 to fail. That is expected. The tests
prove the pipeline works end-to-end; intermittent failures on quiet streams
are acceptable.

Client config used in every test:
  CDN:           EU  (webcast-ws.eu.tiktok.com)
  HTTP timeout:  15s
  Max retries:   5
  Stale timeout: 45s
"""

import asyncio
import os
import time
from typing import Callable

import pytest

from piratetok_live.client import TikTokLiveClient
from piratetok_live.events.types import EventType, TikTokEvent

pytestmark = pytest.mark.integration

_HAVE_TEST_USER = bool(os.environ.get("PIRATETOK_LIVE_TEST_USER", "").strip())

_SKIP = pytest.mark.skipif(
    not _HAVE_TEST_USER,
    reason="set PIRATETOK_LIVE_TEST_USER to a live TikTok username",
)

_AWAIT_TRAFFIC = 90
_AWAIT_CHAT = 120
_AWAIT_GIFT = 180
_AWAIT_LIKE = 120
_AWAIT_JOIN = 150
_AWAIT_FOLLOW = 180
_AWAIT_SUBSCRIPTION = 240


def _make_client(user: str) -> TikTokLiveClient:
    return (
        TikTokLiveClient(user)
        .cdn_eu()
        .timeout(15.0)
        .max_retries(5)
        .stale_timeout(45.0)
    )


async def _await_wss_event(
    user: str,
    await_timeout: int,
    register: Callable[[TikTokLiveClient, asyncio.Event], None],
    failure_message: str,
) -> None:
    """
    Core smoke test pattern:
    1. Build client with test config.
    2. Register listeners that set the hit event.
    3. Run connect() as a background task.
    4. Wait for hit event with timeout.
    5. Assert no task exception.
    6. Disconnect and await task cleanup.
    7. Assert task exited cleanly.
    """
    hit = asyncio.Event()
    client = _make_client(user)
    register(client, hit)

    connect_task: asyncio.Task = asyncio.create_task(client.connect())

    try:
        try:
            await asyncio.wait_for(asyncio.shield(hit.wait()), timeout=await_timeout)
        except TimeoutError:
            pass

        if connect_task.done() and connect_task.exception() is not None:
            raise AssertionError(
                f"connect task failed: {connect_task.exception()}"
            ) from connect_task.exception()

        assert hit.is_set(), failure_message
    finally:
        client.disconnect()
        try:
            await asyncio.wait_for(connect_task, timeout=30)
        except TimeoutError:
            connect_task.cancel()
            raise AssertionError("connect task did not exit within 30s after disconnect()")
        if connect_task.exception() is not None:
            raise AssertionError(
                f"connect task raised after disconnect: {connect_task.exception()}"
            ) from connect_task.exception()


@_SKIP
def test_connect_receives_traffic_before_timeout() -> None:
    """W1 — Any event (room_user_seq, member, chat, like, control) within 90s."""
    user = os.environ["PIRATETOK_LIVE_TEST_USER"].strip()

    def register(client: TikTokLiveClient, hit: asyncio.Event) -> None:
        client.on(EventType.room_user_seq)(lambda _e: hit.set())
        client.on(EventType.member)(lambda _e: hit.set())
        client.on(EventType.chat)(lambda _e: hit.set())
        client.on(EventType.like)(lambda _e: hit.set())
        client.on(EventType.control)(lambda _e: hit.set())

    asyncio.run(_await_wss_event(
        user,
        _AWAIT_TRAFFIC,
        register,
        f"no room traffic within {_AWAIT_TRAFFIC}s (quiet stream or block)",
    ))


@_SKIP
def test_connect_receives_chat_before_timeout() -> None:
    """W2 — Chat event with user + content within 120s."""
    user = os.environ["PIRATETOK_LIVE_TEST_USER"].strip()

    def register(client: TikTokLiveClient, hit: asyncio.Event) -> None:
        def on_chat(event: TikTokEvent) -> None:
            data = event.data or {}
            user_info = data.get("user", {}) or {}
            content = data.get("content", "")
            print(
                f"[integration test chat] "
                f"{user_info.get('unique_id', '?')}: {content}"
            )
            hit.set()

        client.on(EventType.chat)(on_chat)

    asyncio.run(_await_wss_event(
        user,
        _AWAIT_CHAT,
        register,
        f"no chat message within {_AWAIT_CHAT}s (quiet stream or block)",
    ))


@_SKIP
def test_connect_receives_gift_before_timeout() -> None:
    """W3 — Gift event with user + gift info within 180s."""
    user = os.environ["PIRATETOK_LIVE_TEST_USER"].strip()

    def register(client: TikTokLiveClient, hit: asyncio.Event) -> None:
        def on_gift(event: TikTokEvent) -> None:
            data = event.data or {}
            user_info = data.get("user", {}) or {}
            gift = data.get("gift", {}) or {}
            diamond_count = gift.get("diamond_count", 0)
            repeat_count = data.get("repeat_count", 1)
            print(
                f"[integration test gift] "
                f"{user_info.get('unique_id', '?')} -> "
                f"{gift.get('name', '?')} x{repeat_count} "
                f"({diamond_count} diamonds each)"
            )
            hit.set()

        client.on(EventType.gift)(on_gift)

    asyncio.run(_await_wss_event(
        user,
        _AWAIT_GIFT,
        register,
        f"no gift within {_AWAIT_GIFT}s (quiet stream or no gifts — try a busier stream)",
    ))


@_SKIP
def test_connect_receives_like_before_timeout() -> None:
    """W4 — Like event with user + count within 120s."""
    user = os.environ["PIRATETOK_LIVE_TEST_USER"].strip()

    def register(client: TikTokLiveClient, hit: asyncio.Event) -> None:
        def on_like(event: TikTokEvent) -> None:
            data = event.data or {}
            user_info = data.get("user", {}) or {}
            print(
                f"[integration test like] "
                f"{user_info.get('unique_id', '?')} "
                f"count={data.get('count')} total={data.get('total')}"
            )
            hit.set()

        client.on(EventType.like)(on_like)

    asyncio.run(_await_wss_event(
        user,
        _AWAIT_LIKE,
        register,
        f"no like within {_AWAIT_LIKE}s (quiet stream or block)",
    ))


@_SKIP
def test_connect_receives_join_before_timeout() -> None:
    """W5 — Join sub-routed event with user within 150s."""
    user = os.environ["PIRATETOK_LIVE_TEST_USER"].strip()

    def register(client: TikTokLiveClient, hit: asyncio.Event) -> None:
        def on_join(event: TikTokEvent) -> None:
            data = event.data or {}
            user_info = data.get("user", {}) or {}
            print(
                f"[integration test join] "
                f"{user_info.get('unique_id', '?')}"
            )
            hit.set()

        client.on(EventType.join)(on_join)

    asyncio.run(_await_wss_event(
        user,
        _AWAIT_JOIN,
        register,
        f"no join within {_AWAIT_JOIN}s (try a busier stream)",
    ))


@_SKIP
def test_connect_receives_follow_before_timeout() -> None:
    """W6 — Follow sub-routed event with user within 180s."""
    user = os.environ["PIRATETOK_LIVE_TEST_USER"].strip()

    def register(client: TikTokLiveClient, hit: asyncio.Event) -> None:
        def on_follow(event: TikTokEvent) -> None:
            data = event.data or {}
            user_info = data.get("user", {}) or {}
            print(
                f"[integration test follow] "
                f"{user_info.get('unique_id', '?')}"
            )
            hit.set()

        client.on(EventType.follow)(on_follow)

    asyncio.run(_await_wss_event(
        user,
        _AWAIT_FOLLOW,
        register,
        f"no follow within {_AWAIT_FOLLOW}s (follows are infrequent — try a growing stream)",
    ))


@pytest.mark.skip(reason="W7 disabled by default — subscriptions are too rare on most streams")
@_SKIP
def test_connect_receives_subscription_signal_before_timeout() -> None:
    """W7 — Any subscription-related event within 240s. Disabled by default."""
    user = os.environ["PIRATETOK_LIVE_TEST_USER"].strip()

    def register(client: TikTokLiveClient, hit: asyncio.Event) -> None:
        def on_sub(_event: TikTokEvent) -> None:
            hit.set()

        client.on(EventType.sub_notify)(on_sub)
        client.on(EventType.subscription_notify)(on_sub)
        client.on(EventType.sub_capsule)(on_sub)
        client.on(EventType.sub_pin_event)(on_sub)

    asyncio.run(_await_wss_event(
        user,
        _AWAIT_SUBSCRIPTION,
        register,
        f"no subscription event within {_AWAIT_SUBSCRIPTION}s (need subs on a sub-enabled stream)",
    ))


@_SKIP
def test_disconnect_unblocks_connect_task_after_connected() -> None:
    """D1 — disconnect() causes the connect coroutine to exit within 18s."""
    user = os.environ["PIRATETOK_LIVE_TEST_USER"].strip()

    async def run() -> None:
        connected = asyncio.Event()
        client = _make_client(user)
        client.on(EventType.connected)(lambda _e: connected.set())

        connect_task: asyncio.Task = asyncio.create_task(client.connect())

        try:
            try:
                await asyncio.wait_for(asyncio.shield(connected.wait()), timeout=90)
            except TimeoutError:
                raise AssertionError(
                    "never reached connected state within 90s (offline user or network)"
                )

            if connect_task.done() and connect_task.exception() is not None:
                raise AssertionError(
                    f"connect task failed before disconnect: {connect_task.exception()}"
                ) from connect_task.exception()

            t0 = time.monotonic()
            client.disconnect()

            try:
                await asyncio.wait_for(connect_task, timeout=20)
            except TimeoutError:
                raise AssertionError(
                    "connect task did not exit within 20s after disconnect()"
                )

            elapsed = time.monotonic() - t0
            assert elapsed < 18, (
                f"worker join should finish within 18s of disconnect, took {elapsed:.1f}s"
            )

            if connect_task.exception() is not None:
                raise AssertionError(
                    f"connect task raised after disconnect: {connect_task.exception()}"
                ) from connect_task.exception()
        finally:
            client.disconnect()
            if not connect_task.done():
                connect_task.cancel()
                try:
                    await connect_task
                except (asyncio.CancelledError, Exception):
                    pass

    asyncio.run(run())
