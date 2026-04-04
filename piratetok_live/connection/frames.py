import gzip

from ..proto.schema import (
    HeartbeatMessage,
    WebcastImEnterRoomMessage,
    WebcastPushFrame,
)


def build_heartbeat(room_id: str) -> bytes:
    hb = bytes(HeartbeatMessage(room_id=int(room_id)))
    frame = WebcastPushFrame(
        payload_encoding="pb",
        payload_type="hb",
        payload=hb,
    )
    return bytes(frame)


def build_enter_room(room_id: str) -> bytes:
    enter = bytes(WebcastImEnterRoomMessage(
        room_id=int(room_id),
        live_id=12,
        identity="audience",
        filter_welcome_msg="0",
    ))
    frame = WebcastPushFrame(
        payload_encoding="pb",
        payload_type="im_enter_room",
        payload=enter,
    )
    return bytes(frame)


def build_ack(log_id: int, internal_ext: bytes) -> bytes:
    frame = WebcastPushFrame(
        payload_encoding="pb",
        payload_type="ack",
        log_id=log_id,
        payload=internal_ext,
    )
    return bytes(frame)


def decompress_if_gzipped(data: bytes) -> bytes:
    if len(data) >= 2 and data[0] == 0x1F and data[1] == 0x8B:
        return gzip.decompress(data)
    return data
