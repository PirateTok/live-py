<p align="center">
  <img src="https://raw.githubusercontent.com/PirateTok/.github/main/profile/assets/og-banner-v2.png" alt="PirateTok" width="640" />
</p>

# piratetok-live-py

Connect to any TikTok Live stream and receive real-time events in Python. No signing server, no API keys, no authentication required.

```python
import asyncio
from piratetok_live import TikTokLiveClient, EventType

async def main():
    # Create client — no API key, no signing server, just a username
    client = TikTokLiveClient("username_here")

    # Register handlers with decorators — events carry decoded protobuf data
    @client.on(EventType.chat)
    def on_chat(evt):
        nick = evt.data.get("user", {}).get("nickname", "?")
        print(f"[chat] {nick}: {evt.data.get('content')}")

    @client.on(EventType.gift)
    def on_gift(evt):
        nick = evt.data.get("user", {}).get("nickname", "?")
        gift = evt.data.get("gift", {})
        print(f"[gift] {nick} sent {gift.get('name')} x{evt.data.get('repeatCount')} ({gift.get('diamondCount', 0)} diamonds)")

    @client.on(EventType.like)
    def on_like(evt):
        nick = evt.data.get("user", {}).get("nickname", "?")
        print(f"[like] {nick} ({evt.data.get('total')} total)")

    # Connect — handles auth, room resolution, WSS, heartbeat, and reconnection
    await client.connect()

asyncio.run(main())
```

## Install

```
pip install piratetok-live-py
```

Requires Python >= 3.11.

## Other languages

| Language | Install | Repo |
|:---------|:--------|:-----|
| **Rust** | `cargo add piratetok-live-rs` | [live-rs](https://github.com/PirateTok/live-rs) |
| **Go** | `go get github.com/PirateTok/live-go` | [live-go](https://github.com/PirateTok/live-go) |
| **JavaScript** | `npm install piratetok-live-js` | [live-js](https://github.com/PirateTok/live-js) |
| **C#** | `dotnet add package PirateTok.Live` | [live-cs](https://github.com/PirateTok/live-cs) |
| **Java** | `com.piratetok:live` | [live-java](https://github.com/PirateTok/live-java) |
| **Lua** | `luarocks install piratetok-live-lua` | [live-lua](https://github.com/PirateTok/live-lua) |
| **Elixir** | `{:piratetok_live, "~> 0.1"}` | [live-ex](https://github.com/PirateTok/live-ex) |
| **Dart** | `dart pub add piratetok_live` | [live-dart](https://github.com/PirateTok/live-dart) |
| **C** | `#include "piratetok.h"` | [live-c](https://github.com/PirateTok/live-c) |
| **PowerShell** | `Install-Module PirateTok.Live` | [live-ps1](https://github.com/PirateTok/live-ps1) |
| **Shell** | `bpkg install PirateTok/live-sh` | [live-sh](https://github.com/PirateTok/live-sh) |

## Features

- **Zero signing dependency** — no API keys, no signing server, no external auth
- **64 decoded event types** — hand-written betterproto dataclasses, no codegen
- **Auto-reconnection** — stale detection, exponential backoff, self-healing auth
- **Proxy support** — `.proxy(url)` builder, applies to HTTP + WSS
- **Enriched User data** — badges, gifter level, moderator status, follow info, fan club
- **Sub-routed convenience events** — `follow`, `share`, `join`, `live_ended`
- **2 runtime deps** — `betterproto` + `websockets`

## Configuration

```python
client = (TikTokLiveClient("username_here")
    .cdn_eu()
    .timeout(15)
    .max_retries(10)
    .stale_timeout(90)
    .proxy("socks5://127.0.0.1:1080")
    .user_agent("Mozilla/5.0 ...")
    .cookies("sessionid=abc; sid_tt=abc")
    .language("pt")
    .region("BR")
    .compress(False))
```

| Method | Default | Description |
|:-------|:--------|:------------|
| `.cdn_eu()` / `.cdn_us()` / `.cdn(host)` | Global CDN | WebSocket CDN endpoint |
| `.timeout(seconds)` | `10` | HTTP request timeout in seconds |
| `.max_retries(n)` | `5` | Maximum reconnection attempts before giving up |
| `.stale_timeout(seconds)` | `60` | Seconds without data before triggering a reconnect |
| `.proxy(url)` | None | HTTP/HTTPS/SOCKS5 proxy for all HTTP + WSS traffic |
| `.user_agent(ua)` | Random from pool | Override the user agent (rotated automatically on reconnect by default) |
| `.cookies(cookies)` | None | Append session cookies alongside ttwid in the WSS cookie header |
| `.language(lang)` | System detected | Override the language sent in WSS params (e.g. `"pt"`, `"ro"`) |
| `.region(reg)` | System detected | Override the region sent in WSS params (e.g. `"BR"`, `"RO"`) |
| `.compress(enabled)` | `True` | Disable gzip compression for WSS payloads (trades bandwidth for CPU) |

## Room info (optional, separate call)

```python
from piratetok_live import check_online, fetch_room_info

result = check_online("username_here")
info = fetch_room_info(result.room_id)

# 18+ rooms
info = fetch_room_info(result.room_id, cookies="sessionid=abc; sid_tt=abc")
```

## Examples

```bash
python examples/basic_chat.py <username>       # connect + print chat events
python examples/online_check.py <username>     # check if user is live
python examples/stream_info.py <username>      # fetch room metadata + stream URLs
python examples/gift_tracker.py <username>     # track gifts with diamond totals
python examples/gift_streak.py <username>      # track gifts with GiftStreakTracker deltas
python examples/profile_lookup.py [username]   # fetch profile via SIGI scrape with caching
```

## Replay testing

Deterministic cross-lib validation against binary WSS captures. Requires testdata from a separate repo:

```bash
git clone https://github.com/PirateTok/live-testdata testdata
pip install -e ".[test]"
pytest tests/test_replay.py -v
```

Tests skip gracefully if testdata is not found. You can also set `PIRATETOK_TESTDATA` to point to a custom location.

## License

0BSD
