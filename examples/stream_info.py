#!/usr/bin/env python3
"""Fetch room metadata and stream URLs for a live TikTok user."""

import sys
from piratetok_live import (
    check_online,
    fetch_room_info,
    AgeRestrictedError,
    HostNotOnlineError,
    UserNotFoundError,
)

if len(sys.argv) < 2:
    print(f"usage: {sys.argv[0]} <username> [cookies]")
    sys.exit(1)

username = sys.argv[1]
cookies = sys.argv[2] if len(sys.argv) > 2 else ""

try:
    room = check_online(username)
except HostNotOnlineError:
    print(f"{username} is not live")
    sys.exit(1)
except UserNotFoundError:
    print(f"{username} does not exist")
    sys.exit(1)

print(f"room_id: {room.room_id}")

try:
    info = fetch_room_info(room.room_id, cookies=cookies)
except AgeRestrictedError:
    print("18+ room — pass session cookies: sessionid=xxx;sid_tt=xxx")
    sys.exit(1)

print(f"title:      {info.title}")
print(f"viewers:    {info.viewers}")
print(f"likes:      {info.likes}")
print(f"total_user: {info.total_user}")

if info.stream_url:
    print(f"flv_origin: {info.stream_url.flv_origin or '(none)'}")
    print(f"flv_hd:     {info.stream_url.flv_hd or '(none)'}")
    print(f"flv_sd:     {info.stream_url.flv_sd or '(none)'}")
    print(f"flv_ld:     {info.stream_url.flv_ld or '(none)'}")
    print(f"flv_audio:  {info.stream_url.flv_audio or '(none)'}")
else:
    print("no stream URLs available")
