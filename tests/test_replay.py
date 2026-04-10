"""Replay test — reads a binary WSS capture, processes it through the full
decode pipeline, and asserts every value matches the manifest JSON.

Skips if testdata is not available. Set PIRATETOK_TESTDATA env var or
place captures in ../live-testdata/ or ../../live-rs/captures/.
"""

import gzip
import json
import os
import struct
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import pytest

from piratetok_live.connection.frames import decompress_if_gzipped
from piratetok_live.events.router import decode
from piratetok_live.events.types import EventType
from piratetok_live.helpers.gift_streak import GiftStreakTracker
from piratetok_live.helpers.like_accumulator import LikeAccumulator
from piratetok_live.proto.schema import (
    WebcastGiftMessage,
    WebcastLikeMessage,
    WebcastPushFrame,
    WebcastResponse,
)

# -- event type name mapping (Python lowercase -> manifest PascalCase) --

_EVENT_NAME_MAP: Dict[str, str] = {
    EventType.connected: "Connected",
    EventType.disconnected: "Disconnected",
    EventType.reconnecting: "Reconnecting",
    EventType.chat: "Chat",
    EventType.gift: "Gift",
    EventType.like: "Like",
    EventType.member: "Member",
    EventType.social: "Social",
    EventType.follow: "Follow",
    EventType.share: "Share",
    EventType.join: "Join",
    EventType.room_user_seq: "RoomUserSeq",
    EventType.control: "Control",
    EventType.live_ended: "LiveEnded",
    EventType.live_intro: "LiveIntro",
    EventType.room_message: "RoomMessage",
    EventType.caption: "Caption",
    EventType.goal_update: "GoalUpdate",
    EventType.im_delete: "ImDelete",
    EventType.rank_update: "RankUpdate",
    EventType.poll: "Poll",
    EventType.envelope: "Envelope",
    EventType.room_pin: "RoomPin",
    EventType.unauthorized_member: "UnauthorizedMember",
    EventType.link_mic_method: "LinkMicMethod",
    EventType.link_mic_battle: "LinkMicBattle",
    EventType.link_mic_armies: "LinkMicArmies",
    EventType.link_message: "LinkMessage",
    EventType.link_layer: "LinkLayer",
    EventType.link_mic_layout_state: "LinkMicLayoutState",
    EventType.gift_panel_update: "GiftPanelUpdate",
    EventType.in_room_banner: "InRoomBanner",
    EventType.guide: "Guide",
    EventType.emote_chat: "EmoteChat",
    EventType.question_new: "QuestionNew",
    EventType.sub_notify: "SubNotify",
    EventType.barrage: "Barrage",
    EventType.hourly_rank: "HourlyRank",
    EventType.msg_detect: "MsgDetect",
    EventType.link_mic_fan_ticket: "LinkMicFanTicket",
    EventType.room_verify: "RoomVerify",
    EventType.oec_live_shopping: "OecLiveShopping",
    EventType.gift_broadcast: "GiftBroadcast",
    EventType.rank_text: "RankText",
    EventType.gift_dynamic_restriction: "GiftDynamicRestriction",
    EventType.viewer_picks_update: "ViewerPicksUpdate",
    EventType.access_control: "AccessControl",
    EventType.access_recall: "AccessRecall",
    EventType.alert_box_audit_result: "AlertBoxAuditResult",
    EventType.binding_gift: "BindingGift",
    EventType.boost_card: "BoostCard",
    EventType.bottom: "BottomMessage",
    EventType.game_rank_notify: "GameRankNotify",
    EventType.gift_prompt: "GiftPrompt",
    EventType.link_state: "LinkState",
    EventType.link_mic_battle_punish_finish: "LinkMicBattlePunishFinish",
    EventType.linkmic_battle_task: "LinkmicBattleTask",
    EventType.marquee_announcement: "MarqueeAnnouncement",
    EventType.notice: "Notice",
    EventType.notify: "Notify",
    EventType.partnership_drops_update: "PartnershipDropsUpdate",
    EventType.partnership_game_offline: "PartnershipGameOffline",
    EventType.partnership_punish: "PartnershipPunish",
    EventType.perception: "Perception",
    EventType.speaker: "Speaker",
    EventType.sub_capsule: "SubCapsule",
    EventType.sub_pin_event: "SubPinEvent",
    EventType.subscription_notify: "SubscriptionNotify",
    EventType.toast: "Toast",
    EventType.system: "SystemMessage",
    EventType.live_game_intro: "LiveGameIntro",
    EventType.unknown: "Unknown",
}


def _manifest_event_name(py_type: str) -> str:
    return _EVENT_NAME_MAP.get(py_type, py_type)


# -- testdata location --

def _find_testdata() -> Optional[Path]:
    env = os.environ.get("PIRATETOK_TESTDATA")
    if env:
        p = Path(env)
        if p.exists():
            return p

    # testdata/ in repo root
    local = Path(__file__).resolve().parent.parent / "testdata"
    if (local / "captures").exists():
        return local

    return None


def _capture_path(testdata: Path, name: str) -> Path:
    return testdata / "captures" / f"{name}.bin"


def _manifest_path(testdata: Path, name: str) -> Path:
    return testdata / "manifests" / f"{name}.json"


# -- frame reader --

def _read_capture(path: Path) -> List[bytes]:
    data = path.read_bytes()
    frames: List[bytes] = []
    pos = 0
    while pos + 4 <= len(data):
        (length,) = struct.unpack_from("<I", data, pos)
        pos += 4
        if pos + length > len(data):
            raise ValueError(f"truncated frame at offset {pos - 4}")
        frames.append(data[pos:pos + length])
        pos += length
    return frames


# -- replay engine --

class ReplayResult:
    __slots__ = (
        "frame_count", "message_count", "event_count",
        "decode_failures", "decompress_failures",
        "payload_types", "message_types", "event_types",
        "follow_count", "share_count", "join_count", "live_ended_count",
        "unknown_types",
        "like_events", "gift_groups",
        "combo_count", "non_combo_count", "streak_finals", "negative_deltas",
    )

    def __init__(self) -> None:
        self.frame_count: int = 0
        self.message_count: int = 0
        self.event_count: int = 0
        self.decode_failures: int = 0
        self.decompress_failures: int = 0
        self.payload_types: Dict[str, int] = defaultdict(int)
        self.message_types: Dict[str, int] = defaultdict(int)
        self.event_types: Dict[str, int] = defaultdict(int)
        self.follow_count: int = 0
        self.share_count: int = 0
        self.join_count: int = 0
        self.live_ended_count: int = 0
        self.unknown_types: Dict[str, int] = defaultdict(int)
        # (wire_count, wire_total, acc_total, accumulated, went_backwards)
        self.like_events: List[Tuple[int, int, int, int, bool]] = []
        # group_id -> [(gift_id, repeat_count, delta, is_final, diamond_total)]
        self.gift_groups: Dict[str, List[Tuple[int, int, int, bool, int]]] = defaultdict(list)
        self.combo_count: int = 0
        self.non_combo_count: int = 0
        self.streak_finals: int = 0
        self.negative_deltas: int = 0


def _replay(frames: List[bytes]) -> ReplayResult:
    r = ReplayResult()
    r.frame_count = len(frames)

    like_acc = LikeAccumulator()
    gift_tracker = GiftStreakTracker()

    for raw in frames:
        try:
            frame = WebcastPushFrame().parse(raw)
        except Exception:
            r.decode_failures += 1
            continue

        r.payload_types[frame.payload_type] += 1

        if frame.payload_type != "msg":
            continue

        try:
            decompressed = decompress_if_gzipped(frame.payload)
        except Exception:
            r.decompress_failures += 1
            continue

        try:
            response = WebcastResponse().parse(decompressed)
        except Exception:
            r.decode_failures += 1
            continue

        for msg in response.messages:
            r.message_count += 1
            r.message_types[msg.method] += 1

            # Route through the same decode pipeline as the live connection
            events = decode(msg.method, msg.payload)
            for evt in events:
                r.event_count += 1
                manifest_name = _manifest_event_name(evt.type)
                r.event_types[manifest_name] += 1

                if evt.type == EventType.follow:
                    r.follow_count += 1
                elif evt.type == EventType.share:
                    r.share_count += 1
                elif evt.type == EventType.join:
                    r.join_count += 1
                elif evt.type == EventType.live_ended:
                    r.live_ended_count += 1
                elif evt.type == EventType.unknown:
                    method = evt.data.get("method", "")
                    r.unknown_types[method] += 1

            # Like accumulator
            if msg.method == "WebcastLikeMessage":
                try:
                    like_msg = WebcastLikeMessage().parse(msg.payload)
                    like_data = like_msg.to_dict()
                    stats = like_acc.process(like_data)
                    r.like_events.append((
                        like_msg.count,
                        like_msg.total,
                        stats.total_like_count,
                        stats.accumulated_count,
                        stats.went_backwards,
                    ))
                except Exception:
                    pass

            # Gift streak tracker
            if msg.method == "WebcastGiftMessage":
                try:
                    gift_msg = WebcastGiftMessage().parse(msg.payload)
                    gift_data = gift_msg.to_dict()

                    if gift_msg.is_combo_gift():
                        r.combo_count += 1
                    else:
                        r.non_combo_count += 1

                    streak = gift_tracker.process(gift_data)
                    if streak.is_final:
                        r.streak_finals += 1
                    if streak.event_gift_count < 0:
                        r.negative_deltas += 1

                    key = str(gift_msg.group_id)
                    r.gift_groups[key].append((
                        gift_msg.gift_id,
                        gift_msg.repeat_count,
                        streak.event_gift_count,
                        streak.is_final,
                        streak.total_diamond_count,
                    ))
                except Exception:
                    pass

    return r


# -- assertion helpers --

def _assert_replay(name: str, r: ReplayResult, m: Dict[str, Any]) -> None:
    assert r.frame_count == m["frame_count"], f"{name}: frame_count"
    assert r.message_count == m["message_count"], f"{name}: message_count"
    assert r.event_count == m["event_count"], f"{name}: event_count"
    assert r.decode_failures == m["decode_failures"], f"{name}: decode_failures"
    assert r.decompress_failures == m["decompress_failures"], f"{name}: decompress_failures"

    assert dict(r.payload_types) == m["payload_types"], f"{name}: payload_types"
    assert dict(r.message_types) == m["message_types"], f"{name}: message_types"
    assert dict(r.event_types) == m["event_types"], f"{name}: event_types"

    sub = m["sub_routed"]
    assert r.follow_count == sub["follow"], f"{name}: sub_routed.follow"
    assert r.share_count == sub["share"], f"{name}: sub_routed.share"
    assert r.join_count == sub["join"], f"{name}: sub_routed.join"
    assert r.live_ended_count == sub["live_ended"], f"{name}: sub_routed.live_ended"

    assert dict(r.unknown_types) == m["unknown_types"], f"{name}: unknown_types"

    # like accumulator
    ml = m["like_accumulator"]
    assert len(r.like_events) == ml["event_count"], f"{name}: like event_count"

    backwards = sum(1 for e in r.like_events if e[4])
    assert backwards == ml["backwards_jumps"], f"{name}: like backwards_jumps"

    if r.like_events:
        last = r.like_events[-1]
        assert last[2] == ml["final_max_total"], f"{name}: like final_max_total"
        assert last[3] == ml["final_accumulated"], f"{name}: like final_accumulated"

    if len(r.like_events) >= 2:
        acc_mono = all(
            r.like_events[i + 1][2] >= r.like_events[i][2]
            for i in range(len(r.like_events) - 1)
        )
        accum_mono = all(
            r.like_events[i + 1][3] >= r.like_events[i][3]
            for i in range(len(r.like_events) - 1)
        )
    else:
        acc_mono = True
        accum_mono = True
    assert acc_mono == ml["acc_total_monotonic"], f"{name}: like acc_total_monotonic"
    assert accum_mono == ml["accumulated_monotonic"], f"{name}: like accumulated_monotonic"

    # like event-by-event
    expected_likes = ml["events"]
    assert len(r.like_events) == len(expected_likes), f"{name}: like events length"
    for i, (got, exp) in enumerate(zip(r.like_events, expected_likes)):
        assert got[0] == exp["wire_count"], f"{name}: like[{i}].wire_count"
        assert got[1] == exp["wire_total"], f"{name}: like[{i}].wire_total"
        assert got[2] == exp["acc_total"], f"{name}: like[{i}].acc_total"
        assert got[3] == exp["accumulated"], f"{name}: like[{i}].accumulated"
        assert got[4] == exp["went_backwards"], f"{name}: like[{i}].went_backwards"

    # gift streaks
    mg = m["gift_streaks"]
    total_gifts = r.combo_count + r.non_combo_count
    assert total_gifts == mg["event_count"], f"{name}: gift event_count"
    assert r.combo_count == mg["combo_count"], f"{name}: gift combo_count"
    assert r.non_combo_count == mg["non_combo_count"], f"{name}: gift non_combo_count"
    assert r.streak_finals == mg["streak_finals"], f"{name}: gift streak_finals"
    assert r.negative_deltas == mg["negative_deltas"], f"{name}: gift negative_deltas"

    # gift group-by-group
    got_groups = dict(r.gift_groups)
    exp_groups = mg["groups"]
    assert len(got_groups) == len(exp_groups), f"{name}: gift groups count"
    for gid, got_evts in got_groups.items():
        assert gid in exp_groups, f"{name}: missing gift group {gid}"
        exp_evts = exp_groups[gid]
        assert len(got_evts) == len(exp_evts), f"{name}: gift group {gid} length"
        for i, (got, exp) in enumerate(zip(got_evts, exp_evts)):
            assert got[0] == exp["gift_id"], f"{name}: gift[{gid}][{i}].gift_id"
            assert got[1] == exp["repeat_count"], f"{name}: gift[{gid}][{i}].repeat_count"
            assert got[2] == exp["delta"], f"{name}: gift[{gid}][{i}].delta"
            assert got[3] == exp["is_final"], f"{name}: gift[{gid}][{i}].is_final"
            assert got[4] == exp["diamond_total"], f"{name}: gift[{gid}][{i}].diamond_total"


# -- test runner --

def _run_capture_test(name: str) -> None:
    testdata = _find_testdata()
    if testdata is None:
        pytest.skip(
            f"no testdata (set PIRATETOK_TESTDATA or clone live-testdata)"
        )

    cap = _capture_path(testdata, name)
    man = _manifest_path(testdata, name)

    if not cap.exists():
        pytest.skip(f"capture not found at {cap}")
    if not man.exists():
        pytest.skip(f"manifest not found at {man}")

    manifest = json.loads(man.read_text())
    frames = _read_capture(cap)
    result = _replay(frames)

    _assert_replay(name, result, manifest)


def test_replay_calvinterest6() -> None:
    _run_capture_test("calvinterest6")


def test_replay_happyhappygaltv() -> None:
    _run_capture_test("happyhappygaltv")


def test_replay_fox4newsdallasfortworth() -> None:
    _run_capture_test("fox4newsdallasfortworth")
