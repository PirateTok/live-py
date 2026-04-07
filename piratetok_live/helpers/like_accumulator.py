"""Like accumulator — monotonizes TikTok's inconsistent total_like_count.

TikTok's ``total`` field on like events arrives from different server shards
with stale values, causing the counter to jump backwards. The ``count`` field
(per-event delta) is reliable.

This helper tracks ``max(total)`` and accumulates deltas so users get a
monotonic counter.

    acc = LikeAccumulator()

    @client.on(EventType.like)
    def on_like(evt):
        stats = acc.process(evt.data)
        print(f"+{stats.event_like_count} likes, total={stats.total_like_count}")
"""

from __future__ import annotations

from typing import Any, Dict, NamedTuple


class LikeStats(NamedTuple):
    event_like_count: int
    total_like_count: int
    accumulated_count: int
    went_backwards: bool


class LikeAccumulator:
    __slots__ = ("_max_total", "_accumulated")

    def __init__(self) -> None:
        self._max_total: int = 0
        self._accumulated: int = 0

    def process(self, data: Dict[str, Any]) -> LikeStats:
        delta = int(data.get("count", 0))
        wire_total = int(data.get("total", 0))

        self._accumulated += delta
        went_backwards = wire_total < self._max_total
        if wire_total > self._max_total:
            self._max_total = wire_total

        return LikeStats(
            event_like_count=delta,
            total_like_count=self._max_total,
            accumulated_count=self._accumulated,
            went_backwards=went_backwards,
        )

    def reset(self) -> None:
        self._max_total = 0
        self._accumulated = 0
