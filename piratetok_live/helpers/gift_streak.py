"""Gift streak tracker — computes per-event deltas from TikTok's running totals.

TikTok combo gifts fire multiple events during a streak, each carrying a
running total in ``repeat_count`` (2, 4, 7, 7). This helper tracks active
streaks by ``group_id`` and computes the delta per event so game developers
get the number they actually need: how many *new* gifts arrived.

This is a helper, not part of the core pipeline. Create one, call
``process()`` on each gift event dict.

    tracker = GiftStreakTracker()

    @client.on(EventType.gift)
    def on_gift(evt):
        enriched = tracker.process(evt.data)
        print(f"+{enriched.event_gift_count} gifts, +{enriched.event_diamond_count} diamonds")
"""

from __future__ import annotations

import time
from typing import Any, Dict, NamedTuple

_STALE_SECONDS = 60.0


class GiftStreakEvent(NamedTuple):
    streak_id: int
    is_active: bool
    is_final: bool
    event_gift_count: int
    total_gift_count: int
    event_diamond_count: int
    total_diamond_count: int


class GiftStreakTracker:
    __slots__ = ("_streaks",)

    def __init__(self) -> None:
        self._streaks: Dict[int, tuple[int, float]] = {}

    def process(self, data: Dict[str, Any]) -> GiftStreakEvent:
        gift = data.get("gift", {})
        gift_type = int(gift.get("type", 0))
        repeat_count = int(data.get("repeat_count", data.get("repeatCount", 1)))
        repeat_end = int(data.get("repeat_end", data.get("repeatEnd", 0)))
        group_id = int(data.get("group_id", data.get("groupId", 0)))
        diamond_per = int(gift.get("diamond_count", gift.get("diamondCount", 0)))

        is_combo = gift_type == 1
        is_final = (not is_combo) or (repeat_end == 1)

        if not is_combo:
            return GiftStreakEvent(
                streak_id=group_id,
                is_active=False,
                is_final=True,
                event_gift_count=1,
                total_gift_count=1,
                event_diamond_count=diamond_per,
                total_diamond_count=diamond_per,
            )

        now = time.monotonic()
        self._evict_stale(now)

        prev = self._streaks.get(group_id)
        prev_count = prev[0] if prev else 0
        delta = max(repeat_count - prev_count, 0)

        if is_final:
            self._streaks.pop(group_id, None)
        else:
            self._streaks[group_id] = (repeat_count, now)

        total_diamonds = diamond_per * max(repeat_count, 1)
        event_diamonds = diamond_per * delta

        return GiftStreakEvent(
            streak_id=group_id,
            is_active=not is_final,
            is_final=is_final,
            event_gift_count=delta,
            total_gift_count=repeat_count,
            event_diamond_count=event_diamonds,
            total_diamond_count=total_diamonds,
        )

    @property
    def active_streaks(self) -> int:
        return len(self._streaks)

    def reset(self) -> None:
        self._streaks.clear()

    def _evict_stale(self, now: float) -> None:
        stale = [gid for gid, (_, ts) in self._streaks.items()
                 if now - ts > _STALE_SECONDS]
        for gid in stale:
            del self._streaks[gid]
