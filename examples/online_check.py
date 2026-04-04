#!/usr/bin/env python3
"""Check if a TikTok user is currently live."""

import sys
from piratetok_live import check_online, HostNotOnlineError, UserNotFoundError, TikTokBlockedError

if len(sys.argv) < 2:
    print(f"usage: {sys.argv[0]} <username>")
    sys.exit(1)

username = sys.argv[1]

try:
    result = check_online(username)
    print(f"LIVE  {username}  room_id={result.room_id}")
except HostNotOnlineError:
    print(f"OFF   {username}")
    sys.exit(1)
except UserNotFoundError:
    print(f"404   {username} does not exist")
    sys.exit(1)
except TikTokBlockedError as e:
    print(f"BLOCKED  HTTP {e.status_code}")
    sys.exit(1)
