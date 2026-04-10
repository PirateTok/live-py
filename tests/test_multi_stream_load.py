"""
Multi-stream concurrent load test (M1).

Requires PIRATETOK_LIVE_TEST_USERS — comma-separated list of live TikTok
usernames. All must be live simultaneously for the full 60-second window.

What this tests:
  - N concurrent WSS connections from a single process
  - All clients reach CONNECTED state within 120s
  - All clients receive events during the 60s live window
  - All session tasks complete cleanly after disconnect
"""

import asyncio
import os
from typing import Dict, List

import pytest

from piratetok_live.client import TikTokLiveClient
from piratetok_live.events.types import EventType, TikTokEvent

pytestmark = pytest.mark.integration

_HAVE_TEST_USERS = bool(os.environ.get("PIRATETOK_LIVE_TEST_USERS", "").strip())

_SKIP = pytest.mark.skipif(
    not _HAVE_TEST_USERS,
    reason="set PIRATETOK_LIVE_TEST_USERS to a comma-separated list of live TikTok usernames",
)

_CONNECT_TIMEOUT = 120
_LIVE_WINDOW = 60
_SESSION_JOIN_TIMEOUT = 120


def _make_client(user: str) -> TikTokLiveClient:
    return (
        TikTokLiveClient(user)
        .cdn_eu()
        .timeout(15.0)
        .max_retries(5)
        .stale_timeout(120.0)
    )


@_SKIP
def test_multiple_live_clients_track_chat_for_one_minute() -> None:
    """M1 — N concurrent clients all connect and receive events for 60s."""
    raw = os.environ["PIRATETOK_LIVE_TEST_USERS"].strip()
    usernames = [u.strip() for u in raw.split(",") if u.strip()]
    assert usernames, "PIRATETOK_LIVE_TEST_USERS must contain at least one username"

    asyncio.run(_run_multi_stream(usernames))


async def _run_multi_stream(usernames: List[str]) -> None:
    n = len(usernames)
    clients: List[TikTokLiveClient] = [_make_client(u) for u in usernames]
    connect_events: List[asyncio.Event] = [asyncio.Event() for _ in range(n)]
    chat_counts: Dict[str, int] = {u: 0 for u in usernames}

    for i, (client, user) in enumerate(zip(clients, usernames)):
        idx = i

        def make_on_connected(ev: asyncio.Event) -> object:
            def on_connected(_event: TikTokEvent) -> None:
                ev.set()
            return on_connected

        def make_on_chat(uname: str) -> object:
            def on_chat(_event: TikTokEvent) -> None:
                chat_counts[uname] += 1
            return on_chat

        client.on(EventType.connected)(make_on_connected(connect_events[idx]))
        client.on(EventType.chat)(make_on_chat(user))

    tasks: List[asyncio.Task] = [
        asyncio.create_task(client.connect(), name=f"wss-{user}")
        for client, user in zip(clients, usernames)
    ]

    try:
        wait_all_connected = asyncio.gather(*(ev.wait() for ev in connect_events))
        try:
            await asyncio.wait_for(wait_all_connected, timeout=_CONNECT_TIMEOUT)
        except TimeoutError:
            not_connected = [
                usernames[i]
                for i, ev in enumerate(connect_events)
                if not ev.is_set()
            ]
            raise AssertionError(
                f"clients did not reach CONNECTED within {_CONNECT_TIMEOUT}s: "
                f"{not_connected}"
            )

        for task in tasks:
            if task.done() and task.exception() is not None:
                raise AssertionError(
                    f"a connect task failed before live window: {task.exception()}"
                ) from task.exception()

        await asyncio.sleep(_LIVE_WINDOW)

        for user, count in chat_counts.items():
            print(f"[integration test multi-stream] {user}: {count} chat events in {_LIVE_WINDOW}s")

    finally:
        for client in clients:
            client.disconnect()

        try:
            done, pending = await asyncio.wait(tasks, timeout=_SESSION_JOIN_TIMEOUT)
        except Exception:
            done = set()
            pending = set(tasks)

        if pending:
            for task in pending:
                task.cancel()
            raise AssertionError(
                f"{len(pending)} session task(s) did not complete within "
                f"{_SESSION_JOIN_TIMEOUT}s after disconnect"
            )

        for task in done:
            exc = task.exception()
            if exc is not None:
                raise AssertionError(
                    f"a session task raised after disconnect: {exc}"
                ) from exc
