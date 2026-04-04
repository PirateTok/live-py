#!/usr/bin/env python3
"""Connect to a TikTok live stream and print chat events."""

import sys
from piratetok_live import TikTokLiveClient, EventType

if len(sys.argv) < 2:
    print(f"usage: {sys.argv[0]} <username>")
    sys.exit(1)

client = TikTokLiveClient(sys.argv[1]).cdn_eu()


@client.on(EventType.connected)
def on_connected(evt):
    print(f"connected to room {evt.data['room_id']}")


@client.on(EventType.chat)
def on_chat(evt):
    user = evt.data.get("user", {})
    nick = user.get("uniqueId") or user.get("nickname", "?")
    print(f"[chat] {nick}: {evt.data.get('content', '')}")


@client.on(EventType.gift)
def on_gift(evt):
    user = evt.data.get("user", {})
    nick = user.get("uniqueId") or user.get("nickname", "?")
    gift = evt.data.get("gift", {})
    print(f"[gift] {nick} sent {gift.get('name', '?')} x{evt.data.get('repeatCount', 1)}")


@client.on(EventType.follow)
def on_follow(evt):
    user = evt.data.get("user", {})
    nick = user.get("uniqueId") or user.get("nickname", "?")
    print(f"[follow] {nick}")


@client.on(EventType.join)
def on_join(evt):
    user = evt.data.get("user", {})
    nick = user.get("uniqueId") or user.get("nickname", "?")
    print(f"[join] {nick}")


@client.on(EventType.like)
def on_like(evt):
    user = evt.data.get("user", {})
    nick = user.get("uniqueId") or user.get("nickname", "?")
    print(f"[like] {nick} x{evt.data.get('count', 1)}")


@client.on(EventType.room_user_seq)
def on_viewers(evt):
    print(f"[viewers] {evt.data.get('totalUser', '?')}")


@client.on(EventType.live_ended)
def on_ended(evt):
    print("[stream ended]")


@client.on(EventType.disconnected)
def on_disconnected(evt):
    print("disconnected")


client.run()
