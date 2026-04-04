from dataclasses import dataclass
from typing import List

import betterproto

from .schema import Common, Emote, Text, User


# === Niche + extended events ===


@dataclass(eq=False, repr=False)
class WebcastRankUpdateMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    group_type: int = betterproto.int64_field(3)


@dataclass(eq=False, repr=False)
class WebcastPollMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    poll_id: int = betterproto.int64_field(3)
    poll_kind: int = betterproto.int32_field(7)


@dataclass(eq=False, repr=False)
class WebcastEnvelopeMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)


@dataclass(eq=False, repr=False)
class WebcastRoomPinMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    pinned_message: bytes = betterproto.bytes_field(2)
    original_msg_type: str = betterproto.string_field(30)
    timestamp: int = betterproto.uint64_field(31)


@dataclass(eq=False, repr=False)
class WebcastUnauthorizedMemberMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    action: int = betterproto.int32_field(2)
    nick_name: str = betterproto.string_field(4)


@dataclass(eq=False, repr=False)
class WebcastLinkMicMethod(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    access_key: str = betterproto.string_field(3)
    anchor_linkmic_id: int = betterproto.int64_field(4)
    channel_id: int = betterproto.int64_field(8)


@dataclass(eq=False, repr=False)
class WebcastLinkMicBattle(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    id: int = betterproto.uint64_field(2)


@dataclass(eq=False, repr=False)
class WebcastLinkMicArmies(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    id: int = betterproto.uint64_field(2)
    time_stamp_1: int = betterproto.uint64_field(5)
    time_stamp_2: int = betterproto.uint64_field(6)


@dataclass(eq=False, repr=False)
class WebcastLinkMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    linker_id: int = betterproto.int64_field(3)


@dataclass(eq=False, repr=False)
class WebcastLinkLayerMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    channel_id: int = betterproto.int64_field(3)


@dataclass(eq=False, repr=False)
class WebcastLinkMicLayoutStateMessage(betterproto.Message):
    common_raw: bytes = betterproto.bytes_field(1)
    room_id: int = betterproto.int64_field(2)
    layout_state: int = betterproto.int32_field(3)
    layout_key: str = betterproto.string_field(6)


@dataclass(eq=False, repr=False)
class WebcastGiftPanelUpdateMessage(betterproto.Message):
    common_raw: bytes = betterproto.bytes_field(1)
    room_id: int = betterproto.int64_field(2)
    panel_ts_or_version: int = betterproto.int64_field(3)


@dataclass(eq=False, repr=False)
class WebcastInRoomBannerMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    json: str = betterproto.string_field(2)


@dataclass(eq=False, repr=False)
class WebcastGuideMessage(betterproto.Message):
    common_raw: bytes = betterproto.bytes_field(1)
    guide_type: int = betterproto.int32_field(2)
    duration_ms: int = betterproto.int64_field(5)
    scene: str = betterproto.string_field(7)


@dataclass(eq=False, repr=False)
class WebcastEmoteChatMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    user: "User" = betterproto.message_field(2)
    emote_list: List["Emote"] = betterproto.message_field(3)


@dataclass(eq=False, repr=False)
class WebcastQuestionNewMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)


@dataclass(eq=False, repr=False)
class WebcastSubNotifyMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    user: "User" = betterproto.message_field(2)
    sub_month: int = betterproto.int64_field(4)


@dataclass(eq=False, repr=False)
class WebcastBarrageMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    content: "Text" = betterproto.message_field(5)
    duration: int = betterproto.int32_field(6)


@dataclass(eq=False, repr=False)
class WebcastHourlyRankMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)


@dataclass(eq=False, repr=False)
class WebcastMsgDetectMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    detect_type: int = betterproto.int32_field(2)
    from_region: str = betterproto.string_field(6)


@dataclass(eq=False, repr=False)
class WebcastLinkMicFanTicketMethod(betterproto.Message):
    common: "Common" = betterproto.message_field(1)


@dataclass(eq=False, repr=False)
class RoomVerifyMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    action: int = betterproto.int32_field(2)
    content: str = betterproto.string_field(3)
    close_room: bool = betterproto.bool_field(5)


@dataclass(eq=False, repr=False)
class WebcastOecLiveShoppingMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)


@dataclass(eq=False, repr=False)
class WebcastGiftBroadcastMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    broadcast_data_blob: bytes = betterproto.bytes_field(2)


@dataclass(eq=False, repr=False)
class WebcastRankTextMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    scene: int = betterproto.int32_field(2)


@dataclass(eq=False, repr=False)
class WebcastGiftDynamicRestrictionMessage(betterproto.Message):
    common_raw: bytes = betterproto.bytes_field(1)
    restriction_blob: bytes = betterproto.bytes_field(2)


@dataclass(eq=False, repr=False)
class WebcastViewerPicksUpdateMessage(betterproto.Message):
    common_raw: bytes = betterproto.bytes_field(1)
    update_type: int = betterproto.int32_field(2)


# === Secondary events ===


@dataclass(eq=False, repr=False)
class WebcastAccessControlMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    captcha_blob: bytes = betterproto.bytes_field(2)


@dataclass(eq=False, repr=False)
class WebcastAccessRecallMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    status: int = betterproto.int32_field(2)
    duration: int = betterproto.int64_field(3)
    end_time: int = betterproto.int64_field(4)


@dataclass(eq=False, repr=False)
class WebcastAlertBoxAuditResultMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    user_id: int = betterproto.int64_field(2)
    scene: int = betterproto.int32_field(5)


@dataclass(eq=False, repr=False)
class WebcastBindingGiftMessage(betterproto.Message):
    gift_message_blob: bytes = betterproto.bytes_field(1)
    common: "Common" = betterproto.message_field(2)


@dataclass(eq=False, repr=False)
class WebcastBoostCardMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    cards_blob: bytes = betterproto.bytes_field(2)


@dataclass(eq=False, repr=False)
class WebcastBottomMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    content: str = betterproto.string_field(2)
    show_type: int = betterproto.int32_field(3)
    duration: int = betterproto.int64_field(5)


@dataclass(eq=False, repr=False)
class WebcastGameRankNotifyMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    msg_type: int = betterproto.int32_field(2)
    notify_text: str = betterproto.string_field(3)


@dataclass(eq=False, repr=False)
class WebcastGiftPromptMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    title: str = betterproto.string_field(2)
    body: str = betterproto.string_field(3)


@dataclass(eq=False, repr=False)
class WebcastLinkStateMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    channel_id: int = betterproto.int64_field(2)
    scene: int = betterproto.int32_field(3)
    version: int = betterproto.int32_field(4)


@dataclass(eq=False, repr=False)
class WebcastLinkMicBattlePunishFinish(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    id1: int = betterproto.uint64_field(2)
    timestamp: int = betterproto.uint64_field(3)


@dataclass(eq=False, repr=False)
class WebcastLinkmicBattleTaskMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)


@dataclass(eq=False, repr=False)
class WebcastMarqueeAnnouncementMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    message_scene: int = betterproto.int32_field(2)


@dataclass(eq=False, repr=False)
class WebcastNoticeMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    content: str = betterproto.string_field(2)
    notice_type: int = betterproto.int32_field(3)


@dataclass(eq=False, repr=False)
class WebcastNotifyMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    schema: str = betterproto.string_field(2)
    notify_type: int = betterproto.int32_field(3)
    content_str: str = betterproto.string_field(4)


@dataclass(eq=False, repr=False)
class WebcastPartnershipDropsUpdateMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    change_mode: int = betterproto.int32_field(2)


@dataclass(eq=False, repr=False)
class WebcastPartnershipGameOfflineMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)


@dataclass(eq=False, repr=False)
class WebcastPartnershipPunishMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)


@dataclass(eq=False, repr=False)
class WebcastPerceptionMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    dialog_blob: bytes = betterproto.bytes_field(2)
    end_time: int = betterproto.int64_field(4)


@dataclass(eq=False, repr=False)
class WebcastSpeakerMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)


@dataclass(eq=False, repr=False)
class WebcastSubCapsuleMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    description: str = betterproto.string_field(2)
    btn_name: str = betterproto.string_field(3)
    btn_url: str = betterproto.string_field(4)


@dataclass(eq=False, repr=False)
class WebcastSubPinEventMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    action_type: int = betterproto.int32_field(2)
    operator_user_id: int = betterproto.int64_field(4)


@dataclass(eq=False, repr=False)
class WebcastSubscriptionNotifyMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    user: "User" = betterproto.message_field(2)
    exhibition_type: int = betterproto.int32_field(3)


@dataclass(eq=False, repr=False)
class WebcastToastMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    display_duration_ms: int = betterproto.int64_field(2)
    delay_display_duration_ms: int = betterproto.int64_field(3)


@dataclass(eq=False, repr=False)
class WebcastSystemMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    message: str = betterproto.string_field(2)


@dataclass(eq=False, repr=False)
class WebcastLiveGameIntroMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    game_text: "Text" = betterproto.message_field(2)
