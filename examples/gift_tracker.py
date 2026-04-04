#!/usr/bin/env python3
"""Track gifts in a TikTok live stream with summary on disconnect."""

import signal
import sys
from collections import defaultdict
from piratetok_live import TikTokLiveClient, EventType

if len(sys.argv) < 2:
    print(f"usage: {sys.argv[0]} <username>")
    sys.exit(1)

client = TikTokLiveClient(sys.argv[1]).cdn_eu()
gifts: dict = defaultdict(lambda: {"count": 0, "diamonds": 0})


@client.on(EventType.connected)
def on_connected(evt):
    print(f"tracking gifts in room {evt.data['room_id']}")


@client.on(EventType.gift)
def on_gift(evt):
    user = evt.data.get("user", {})
    nick = user.get("uniqueId") or user.get("nickname", "?")
    gift = evt.data.get("gift", {})
    name = gift.get("name", "unknown")
    diamonds = int(gift.get("diamondCount", 0))
    count = int(evt.data.get("repeatCount", 1))

    gifts[nick]["count"] += count
    gifts[nick]["diamonds"] += diamonds * count
    print(f"  {nick} → {name} x{count} ({diamonds * count} diamonds)")


def print_summary():
    if not gifts:
        print("\nno gifts received")
        return
    print(f"\n--- gift summary ({len(gifts)} gifters) ---")
    ranked = sorted(gifts.items(), key=lambda x: x[1]["diamonds"], reverse=True)
    for nick, stats in ranked:
        print(f"  {nick}: {stats['count']} gifts, {stats['diamonds']} diamonds")


@client.on(EventType.disconnected)
def on_disconnected(evt):
    print_summary()


signal.signal(signal.SIGINT, lambda *_: (print_summary(), client.disconnect()))
client.run()
