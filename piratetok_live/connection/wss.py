import asyncio
import logging
from typing import Callable, Optional

import websockets.asyncio.client as ws_client
import websockets.exceptions as ws_exc

from ..errors import DeviceBlockedError
from ..events.router import decode
from ..events.types import TikTokEvent
from ..http.ua import random_ua, system_locale
from ..proto.schema import WebcastPushFrame, WebcastResponse
from .frames import build_ack, build_enter_room, build_heartbeat, decompress_if_gzipped

_HEARTBEAT_S = 10
_STALE_TIMEOUT_S = 60
_log = logging.getLogger("piratetok_live.wss")


async def connect_wss(
    wss_url: str,
    ttwid: str,
    room_id: str,
    on_event: Callable[[TikTokEvent], None],
    on_error: Callable[[Exception], None],
    stop_event: asyncio.Event,
    stale_timeout: float = _STALE_TIMEOUT_S,
    proxy: str = "",
    user_agent: Optional[str] = None,
    cookies: Optional[str] = None,
    accept_language: Optional[str] = None,
) -> None:
    """Connect to TikTok WSS, stream events until stop_event or connection drops.

    Returns normally on clean exit, stop, stale timeout, or connection close.
    Raises DeviceBlockedError when handshake returns DEVICE_BLOCKED.
    Caller decides whether to reconnect.
    """
    ua = user_agent if user_agent else random_ua()
    cookie_header = f"ttwid={ttwid}; {cookies}" if cookies else f"ttwid={ttwid}"
    if not accept_language:
        lang, reg = system_locale()
        accept_language = f"{lang}-{reg},{lang};q=0.9"
    headers = {
        "User-Agent": ua,
        "Cookie": cookie_header,
        "Origin": "https://www.tiktok.com",
        "Referer": "https://www.tiktok.com/",
        "Accept-Language": accept_language,
        "Cache-Control": "no-cache",
    }
    ws_proxy = proxy if proxy else True  # True = auto-detect from env

    try:
        async with ws_client.connect(
            wss_url, additional_headers=headers, proxy=ws_proxy,
        ) as ws:
            await ws.send(build_heartbeat(room_id))
            await ws.send(build_enter_room(room_id))

            hb_task = asyncio.create_task(_heartbeat_loop(ws, room_id, stop_event))
            try:
                while not stop_event.is_set():
                    try:
                        raw = await asyncio.wait_for(ws.recv(), timeout=stale_timeout)
                    except TimeoutError:
                        _log.info("stale: no data for %.0fs, closing", stale_timeout)
                        break
                    try:
                        await _process_frame(raw, ws, room_id, on_event)
                    except Exception as err:
                        on_error(err)
            finally:
                hb_task.cancel()
                try:
                    await hb_task
                except asyncio.CancelledError:
                    pass
    except ws_exc.InvalidStatusCode as err:
        if _is_device_blocked(err):
            raise DeviceBlockedError() from err
        _log.info("wss rejected: status %s", err.status_code)
    except (OSError, ws_exc.WebSocketException) as err:
        _log.info("wss connection error: %s", err)


def _is_device_blocked(err: ws_exc.InvalidStatusCode) -> bool:
    """Check if a rejected handshake carries the DEVICE_BLOCKED header."""
    # websockets stores the response object; check for Handshake-Msg header
    response = getattr(err, "response", None)
    if response is not None:
        headers = getattr(response, "headers", None)
        if headers is not None:
            msg = headers.get("Handshake-Msg", "")
            if msg == "DEVICE_BLOCKED":
                return True
    # Also check status code 415 which TikTok uses for device blocks
    if hasattr(err, "status_code") and err.status_code == 415:
        return True
    return False


async def _heartbeat_loop(
    ws: ws_client.ClientConnection,
    room_id: str,
    stop_event: asyncio.Event,
) -> None:
    while not stop_event.is_set():
        await asyncio.sleep(_HEARTBEAT_S)
        try:
            await ws.send(build_heartbeat(room_id))
        except Exception as err:
            _log.debug("heartbeat send failed: %s", err)
            return


async def _process_frame(
    raw: bytes | str,
    ws: ws_client.ClientConnection,
    room_id: str,
    on_event: Callable[[TikTokEvent], None],
) -> None:
    if isinstance(raw, str):
        return

    frame = WebcastPushFrame().parse(raw)

    if frame.payload_type == "msg":
        decompressed = decompress_if_gzipped(frame.payload)
        response = WebcastResponse().parse(decompressed)

        if response.needs_ack and response.internal_ext:
            ack_data = build_ack(frame.log_id, response.internal_ext)
            try:
                await ws.send(ack_data)
            except Exception as err:
                _log.debug("ack send failed: %s", err)

        for msg in response.messages:
            events = decode(msg.method, msg.payload, room_id)
            for evt in events:
                on_event(evt)
