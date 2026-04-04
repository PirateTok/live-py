from dataclasses import dataclass
from typing import Dict, List

import betterproto


# === Frame types ===


@dataclass(eq=False, repr=False)
class WebcastPushFrame(betterproto.Message):
    seq_id: int = betterproto.uint64_field(1)
    log_id: int = betterproto.uint64_field(2)
    service: int = betterproto.uint64_field(3)
    method: int = betterproto.uint64_field(4)
    headers: Dict[str, str] = betterproto.map_field(
        5, betterproto.TYPE_STRING, betterproto.TYPE_STRING
    )
    payload_encoding: str = betterproto.string_field(6)
    payload_type: str = betterproto.string_field(7)
    payload: bytes = betterproto.bytes_field(8)


@dataclass(eq=False, repr=False)
class ResponseMessage(betterproto.Message):
    method: str = betterproto.string_field(1)
    payload: bytes = betterproto.bytes_field(2)
    msg_id: int = betterproto.int64_field(3)
    msg_type: int = betterproto.int32_field(4)
    offset: int = betterproto.int64_field(5)
    is_history: bool = betterproto.bool_field(6)


@dataclass(eq=False, repr=False)
class WebcastResponse(betterproto.Message):
    messages: List["ResponseMessage"] = betterproto.message_field(1)
    cursor: str = betterproto.string_field(2)
    fetch_interval: int = betterproto.int64_field(3)
    now: int = betterproto.int64_field(4)
    internal_ext: bytes = betterproto.bytes_field(5)
    fetch_type: int = betterproto.int32_field(6)
    route_params_map: Dict[str, str] = betterproto.map_field(
        7, betterproto.TYPE_STRING, betterproto.TYPE_STRING
    )
    heart_beat_duration: int = betterproto.int64_field(8)
    needs_ack: bool = betterproto.bool_field(9)
    push_server: str = betterproto.string_field(10)
    is_first: bool = betterproto.bool_field(11)


@dataclass(eq=False, repr=False)
class HeartbeatMessage(betterproto.Message):
    room_id: int = betterproto.uint64_field(1)


@dataclass(eq=False, repr=False)
class WebcastImEnterRoomMessage(betterproto.Message):
    room_id: int = betterproto.int64_field(1)
    room_tag: str = betterproto.string_field(2)
    live_region: str = betterproto.string_field(3)
    live_id: int = betterproto.int64_field(4)
    identity: str = betterproto.string_field(5)
    cursor: str = betterproto.string_field(6)
    account_type: int = betterproto.int64_field(7)
    enter_unique_id: int = betterproto.int64_field(8)
    filter_welcome_msg: str = betterproto.string_field(9)


# === Common types ===


@dataclass(eq=False, repr=False)
class Image(betterproto.Message):
    url_list: List[str] = betterproto.string_field(1)
    uri: str = betterproto.string_field(2)
    width: int = betterproto.int32_field(3)
    height: int = betterproto.int32_field(4)


@dataclass(eq=False, repr=False)
class Text(betterproto.Message):
    key: str = betterproto.string_field(1)
    default_pattern: str = betterproto.string_field(2)


@dataclass(eq=False, repr=False)
class Common(betterproto.Message):
    method: str = betterproto.string_field(1)
    msg_id: int = betterproto.int64_field(2)
    room_id: int = betterproto.int64_field(3)
    create_time: int = betterproto.int64_field(4)
    describe: str = betterproto.string_field(7)


@dataclass(eq=False, repr=False)
class User(betterproto.Message):
    id: int = betterproto.int64_field(1)
    nickname: str = betterproto.string_field(3)
    bio_description: str = betterproto.string_field(5)
    avatar_thumb: "Image" = betterproto.message_field(9)
    avatar_medium: "Image" = betterproto.message_field(10)
    avatar_large: "Image" = betterproto.message_field(11)
    verified: bool = betterproto.bool_field(12)
    follow_info: "FollowInfo" = betterproto.message_field(22)
    fans_club: "FansClubMember" = betterproto.message_field(24)
    top_vip_no: int = betterproto.int32_field(31)
    pay_score: int = betterproto.int64_field(34)
    fan_ticket_count: int = betterproto.int64_field(35)
    unique_id: str = betterproto.string_field(38)
    display_id: str = betterproto.string_field(46)
    badge_list: List["BadgeStruct"] = betterproto.message_field(64)
    follow_status: int = betterproto.int64_field(1024)
    is_follower: bool = betterproto.bool_field(1029)
    is_following: bool = betterproto.bool_field(1030)
    is_subscribe: bool = betterproto.bool_field(1090)


@dataclass(eq=False, repr=False)
class GiftStruct(betterproto.Message):
    image: "Image" = betterproto.message_field(1)
    describe: str = betterproto.string_field(2)
    duration: int = betterproto.int64_field(4)
    id: int = betterproto.int64_field(5)
    combo: bool = betterproto.bool_field(10)
    type: int = betterproto.int32_field(11)
    diamond_count: int = betterproto.int32_field(12)
    name: str = betterproto.string_field(16)


@dataclass(eq=False, repr=False)
class Emote(betterproto.Message):
    emote_id: str = betterproto.string_field(1)
    image: "Image" = betterproto.message_field(2)


@dataclass(eq=False, repr=False)
class UserIdentity(betterproto.Message):
    is_gift_giver_of_anchor: bool = betterproto.bool_field(1)
    is_subscriber_of_anchor: bool = betterproto.bool_field(2)
    is_mutual_following_with_anchor: bool = betterproto.bool_field(3)
    is_follower_of_anchor: bool = betterproto.bool_field(4)
    is_moderator_of_anchor: bool = betterproto.bool_field(5)
    is_anchor: bool = betterproto.bool_field(6)


@dataclass(eq=False, repr=False)
class PrivilegeLogExtra(betterproto.Message):
    data_version: str = betterproto.string_field(1)
    privilege_id: str = betterproto.string_field(2)
    privilege_version: str = betterproto.string_field(3)
    level: str = betterproto.string_field(5)


@dataclass(eq=False, repr=False)
class BadgeImage(betterproto.Message):
    image: "Image" = betterproto.message_field(2)


@dataclass(eq=False, repr=False)
class BadgeText(betterproto.Message):
    key: str = betterproto.string_field(2)
    default_pattern: str = betterproto.string_field(3)


@dataclass(eq=False, repr=False)
class BadgeString(betterproto.Message):
    content_str: str = betterproto.string_field(2)


@dataclass(eq=False, repr=False)
class BadgeStruct(betterproto.Message):
    """badge_scene values: ADMIN=1, SUBSCRIBER=4, RANK_LIST=6, USER_GRADE=8, FANS=10"""
    display_type: int = betterproto.int32_field(1)
    badge_scene: int = betterproto.int32_field(3)
    display: bool = betterproto.bool_field(11)
    log_extra: "PrivilegeLogExtra" = betterproto.message_field(12)
    image_badge: "BadgeImage" = betterproto.message_field(20)
    text_badge: "BadgeText" = betterproto.message_field(21)
    string_badge: "BadgeString" = betterproto.message_field(22)


@dataclass(eq=False, repr=False)
class FollowInfo(betterproto.Message):
    following_count: int = betterproto.int64_field(1)
    follower_count: int = betterproto.int64_field(2)
    follow_status: int = betterproto.int64_field(3)


@dataclass(eq=False, repr=False)
class FansClubData(betterproto.Message):
    club_name: str = betterproto.string_field(1)
    level: int = betterproto.int32_field(2)


@dataclass(eq=False, repr=False)
class FansClubMember(betterproto.Message):
    data: "FansClubData" = betterproto.message_field(1)


# === Core message types ===


@dataclass(eq=False, repr=False)
class WebcastChatMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    user: "User" = betterproto.message_field(2)
    content: str = betterproto.string_field(3)
    content_language: str = betterproto.string_field(14)


@dataclass(eq=False, repr=False)
class WebcastGiftMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    gift_id: int = betterproto.int64_field(2)
    fan_ticket_count: int = betterproto.int64_field(3)
    group_count: int = betterproto.int32_field(4)
    repeat_count: int = betterproto.int32_field(5)
    combo_count: int = betterproto.int32_field(6)
    user: "User" = betterproto.message_field(7)
    to_user: "User" = betterproto.message_field(8)
    repeat_end: int = betterproto.int32_field(9)
    group_id: int = betterproto.int64_field(11)
    room_fan_ticket_count: int = betterproto.int64_field(13)
    gift: "GiftStruct" = betterproto.message_field(15)
    send_type: int = betterproto.int64_field(17)

    def is_combo_gift(self) -> bool:
        return self.gift.type == 1 if self.gift else False

    def is_streak_over(self) -> bool:
        if not self.is_combo_gift():
            return True
        return self.repeat_end == 1

    def diamond_total(self) -> int:
        per_gift = self.gift.diamond_count if self.gift else 0
        return per_gift * max(self.repeat_count, 1)


@dataclass(eq=False, repr=False)
class WebcastLikeMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    count: int = betterproto.int32_field(2)
    total: int = betterproto.int32_field(3)
    user: "User" = betterproto.message_field(5)


@dataclass(eq=False, repr=False)
class WebcastMemberMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    user: "User" = betterproto.message_field(2)
    member_count: int = betterproto.int32_field(3)
    action: int = betterproto.int32_field(10)
    action_description: str = betterproto.string_field(11)


@dataclass(eq=False, repr=False)
class WebcastSocialMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    user: "User" = betterproto.message_field(2)
    share_type: int = betterproto.int64_field(3)
    action: int = betterproto.int64_field(4)
    share_target: str = betterproto.string_field(5)
    follow_count: int = betterproto.int32_field(6)
    share_count: int = betterproto.int32_field(8)


@dataclass(eq=False, repr=False)
class WebcastRoomUserSeqMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    total: int = betterproto.int64_field(3)
    pop_str: str = betterproto.string_field(4)
    popularity: int = betterproto.int64_field(6)
    total_user: int = betterproto.int32_field(7)


@dataclass(eq=False, repr=False)
class WebcastControlMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    action: int = betterproto.int32_field(2)
    tips: str = betterproto.string_field(3)


@dataclass(eq=False, repr=False)
class WebcastLiveIntroMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    room_id: int = betterproto.int64_field(2)
    content: str = betterproto.string_field(4)
    host: "User" = betterproto.message_field(5)
    language: str = betterproto.string_field(8)


@dataclass(eq=False, repr=False)
class WebcastRoomMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    content: str = betterproto.string_field(2)


@dataclass(eq=False, repr=False)
class WebcastCaptionMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    time_stamp: int = betterproto.uint64_field(2)


@dataclass(eq=False, repr=False)
class WebcastGoalUpdateMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    contributor_id: int = betterproto.int64_field(4)
    contribute_count: int = betterproto.int64_field(9)
    contribute_score: int = betterproto.int64_field(10)
    pin: bool = betterproto.bool_field(13)
    unpin: bool = betterproto.bool_field(14)


@dataclass(eq=False, repr=False)
class WebcastImDeleteMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    delete_msg_ids_list: List[int] = betterproto.int64_field(2)
    delete_user_ids_list: List[int] = betterproto.int64_field(3)
