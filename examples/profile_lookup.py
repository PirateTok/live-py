#!/usr/bin/env python3
"""Fetch TikTok profiles via SIGI scrape with caching."""

import sys

from piratetok_live import ProfileCache, ProfilePrivateError, ProfileNotFoundError


def main() -> None:
    username = sys.argv[1] if len(sys.argv) > 1 else "tiktok"
    cache = ProfileCache()

    print(f"Fetching profile for @{username}...")
    try:
        profile = cache.fetch(username)
    except ProfilePrivateError:
        print(f"  @{username} is a private account")
        return
    except ProfileNotFoundError:
        print(f"  @{username} does not exist")
        return

    print(f"  User ID:    {profile.user_id}")
    print(f"  Nickname:   {profile.nickname}")
    print(f"  Verified:   {profile.verified}")
    print(f"  Followers:  {profile.follower_count}")
    print(f"  Videos:     {profile.video_count}")
    print(f"  Avatar (thumb):  {profile.avatar_thumb}")
    print(f"  Avatar (720):    {profile.avatar_medium}")
    print(f"  Avatar (1080):   {profile.avatar_large}")
    print(f"  Bio link:   {profile.bio_link or '(none)'}")
    print(f"  Room ID:    {profile.room_id or '(offline)'}")

    print(f"\nFetching @{username} again (should be cached)...")
    profile2 = cache.fetch(username)
    print(f"  [cached] {profile2.nickname} — {profile2.follower_count} followers")


if __name__ == "__main__":
    main()
