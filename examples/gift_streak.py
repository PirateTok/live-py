#!/usr/bin/env python3
"""Track gifts with proper streak delta handling.

Uses GiftStreakTracker to compute per-event deltas instead of
raw running totals. Game developers: use event_gift_count and
event_diamond_count for game logic, not the totals.
"""

import signal
import sys
from piratetok_live import TikTokLiveClient, EventType, GiftStreakTracker

if len(sys.argv) < 2:
    print(f"usage: {sys.argv[0]} <username>")
    sys.exit(1)

client = TikTokLiveClient(sys.argv[1]).cdn_eu()
tracker = GiftStreakTracker()
total_diamonds = 0


@client.on(EventType.connected)
def on_connected(evt):
    print(f"tracking gifts in room {evt.data['room_id']}")


@client.on(EventType.gift)
def on_gift(evt):
    global total_diamonds
    enriched = tracker.process(evt.data)

    user = evt.data.get("user", {})
    nick = user.get("uniqueId") or user.get("nickname", "?")
    gift = evt.data.get("gift", {})
    name = gift.get("name", "unknown")

    if enriched.is_final:
        total_diamonds += enriched.total_diamond_count
        print(f"  {nick} -> {name} x{enriched.total_gift_count} "
              f"— {enriched.total_diamond_count} diamonds (streak ended)")
        print(f"       running total: {total_diamonds} diamonds")
    elif enriched.event_gift_count > 0:
        print(f"  {nick} -> {name} +{enriched.event_gift_count} "
              f"(+{enriched.event_diamond_count} diamonds, streak ongoing)")


@client.on(EventType.disconnected)
def on_disconnected(evt):
    print(f"\nfinal total: {total_diamonds} diamonds")
    print(f"active streaks at disconnect: {tracker.active_streaks}")


signal.signal(signal.SIGINT, lambda *_: client.disconnect())
client.run()
