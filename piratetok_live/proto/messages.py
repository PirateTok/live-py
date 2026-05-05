from dataclasses import dataclass
from typing import List

import betterproto

from .schema import Common, EmoteData, MsgFilter, Text, User, UserIdentity


# === Niche / extended events ===


@dataclass(eq=False, repr=False)
class WebcastRankUpdate(betterproto.Message):
    rank_type: int = betterproto.int64_field(1)
    owner_rank: int = betterproto.int64_field(2)
    show_entrance_animation: bool = betterproto.bool_field(5)
    countdown: int = betterproto.int64_field(6)
    related_tab_rank_type: int = betterproto.int64_field(8)
    request_first_show_type: int = betterproto.int64_field(9)
    supported_version: int = betterproto.int64_field(10)
    owner_on_rank: bool = betterproto.bool_field(11)


@dataclass(eq=False, repr=False)
class WebcastRankTabInfo(betterproto.Message):
    rank_type: int = betterproto.int64_field(1)
    title: str = betterproto.string_field(2)
    list_lynx_type: int = betterproto.int64_field(4)


@dataclass(eq=False, repr=False)
class WebcastRankUpdateMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    updates_list: List["WebcastRankUpdate"] = betterproto.message_field(2)
    group_type: int = betterproto.int64_field(3)
    priority: int = betterproto.int64_field(5)
    tabs_list: List["WebcastRankTabInfo"] = betterproto.message_field(6)
    is_animation_loop_play: bool = betterproto.bool_field(7)
    animation_loop_for_off: bool = betterproto.bool_field(8)


@dataclass(eq=False, repr=False)
class WebcastPollMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    message_type: int = betterproto.int32_field(2)
    poll_id: int = betterproto.int64_field(3)
    start_content_blob: bytes = betterproto.bytes_field(4)
    end_content_blob: bytes = betterproto.bytes_field(5)
    update_content_blob: bytes = betterproto.bytes_field(6)
    poll_kind: int = betterproto.int32_field(7)


@dataclass(eq=False, repr=False)
class EnvelopeInfo(betterproto.Message):
    envelope_id: str = betterproto.string_field(1)
    business_type: int = betterproto.int32_field(2)
    envelope_idc: str = betterproto.string_field(3)
    send_user_name: str = betterproto.string_field(4)
    diamond_count: int = betterproto.int32_field(5)
    people_count: int = betterproto.int32_field(6)
    unpack_at: int = betterproto.int32_field(7)
    send_user_id: str = betterproto.string_field(8)
    create_at: str = betterproto.string_field(10)
    follow_show_status: int = betterproto.int32_field(12)
    skin_id: int = betterproto.int32_field(13)


@dataclass(eq=False, repr=False)
class WebcastEnvelopeMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    envelope_info: "EnvelopeInfo" = betterproto.message_field(2)
    display: int = betterproto.int32_field(3)


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
    nick_name_prefix: "Text" = betterproto.message_field(3)
    nick_name: str = betterproto.string_field(4)
    enter_text: "Text" = betterproto.message_field(5)


@dataclass(eq=False, repr=False)
class WebcastLinkMicMethod(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    message_type: int = betterproto.int32_field(2)
    user_id: int = betterproto.int64_field(5)
    channel_id: int = betterproto.int64_field(8)
    to_user_id: int = betterproto.int64_field(21)
    start_time_ms: int = betterproto.int64_field(26)
    anchor_link_mic_id_str: str = betterproto.string_field(37)
    rival_anchor_id: int = betterproto.int64_field(38)
    rival_linkmic_id_str: str = betterproto.string_field(40)


@dataclass(eq=False, repr=False)
class WebcastLinkMicBattle(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    battle_id: int = betterproto.int64_field(2)
    action: int = betterproto.int32_field(4)


@dataclass(eq=False, repr=False)
class WebcastLinkMicArmies(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    battle_id: int = betterproto.int64_field(2)
    channel_id: int = betterproto.int64_field(4)
    battle_status: int = betterproto.int32_field(7)
    from_user_id: int = betterproto.int64_field(8)
    gift_id: int = betterproto.int64_field(9)
    gift_count: int = betterproto.int32_field(10)
    total_diamond_count: int = betterproto.int32_field(12)
    repeat_count: int = betterproto.int32_field(13)
    trigger_critical_strike: bool = betterproto.bool_field(15)


@dataclass(eq=False, repr=False)
class WebcastLinkMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    message_type: int = betterproto.int32_field(2)
    linker_id: int = betterproto.int64_field(3)
    scene: int = betterproto.int32_field(4)
    list_change_content_blob: bytes = betterproto.bytes_field(20)


@dataclass(eq=False, repr=False)
class WebcastLinkLayerMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    message_type: int = betterproto.int32_field(2)
    channel_id: int = betterproto.int64_field(3)
    scene: int = betterproto.int32_field(4)
    source: str = betterproto.string_field(5)
    centerized_idc: str = betterproto.string_field(6)
    rtc_room_id: int = betterproto.int64_field(7)
    group_change_blob: bytes = betterproto.bytes_field(118)
    business_blob: bytes = betterproto.bytes_field(200)


@dataclass(eq=False, repr=False)
class WebcastLinkMicLayoutStateMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    room_id: int = betterproto.int64_field(2)
    layout_state: int = betterproto.int32_field(3)
    layout_key: str = betterproto.string_field(6)


@dataclass(eq=False, repr=False)
class WebcastGiftPanelUpdateMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    room_id: int = betterproto.int64_field(2)
    panel_ts_or_version: int = betterproto.int64_field(3)
    panel_blob: bytes = betterproto.bytes_field(10)
    gift_list_blob: bytes = betterproto.bytes_field(11)
    vault_blob: bytes = betterproto.bytes_field(12)


@dataclass(eq=False, repr=False)
class WebcastInRoomBannerMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    raw_data_entries: List[bytes] = betterproto.bytes_field(2)
    position: int = betterproto.int32_field(3)
    action_type: int = betterproto.int32_field(4)


@dataclass(eq=False, repr=False)
class WebcastGuideMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    guide_type: int = betterproto.int32_field(2)
    duration_ms: int = betterproto.int64_field(5)
    scene: str = betterproto.string_field(7)


@dataclass(eq=False, repr=False)
class WebcastEmoteChatMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    user: "User" = betterproto.message_field(2)
    emote_list: List["EmoteData"] = betterproto.message_field(3)
    msg_filter: "MsgFilter" = betterproto.message_field(4)
    user_identity: "UserIdentity" = betterproto.message_field(5)


@dataclass(eq=False, repr=False)
class QuestionDetails(betterproto.Message):
    question_id: int = betterproto.int64_field(1)
    question_text: str = betterproto.string_field(2)
    answer_status: int = betterproto.int32_field(3)
    create_time: int = betterproto.int64_field(4)
    user: "User" = betterproto.message_field(5)


@dataclass(eq=False, repr=False)
class WebcastQuestionNewMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    details: "QuestionDetails" = betterproto.message_field(2)


@dataclass(eq=False, repr=False)
class WebcastSubNotifyMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    sender: "User" = betterproto.message_field(2)
    exhibition_type: int = betterproto.int32_field(3)
    sub_month: int = betterproto.int32_field(4)
    subscribe_type: int = betterproto.int32_field(5)
    old_subscribe_status: int = betterproto.int32_field(6)
    user_subscribe_status: int = betterproto.int32_field(7)
    subscribing_status: int = betterproto.int32_field(8)
    change_type: int = betterproto.int32_field(9)
    upgrade_count: int = betterproto.int64_field(10)
    user: "User" = betterproto.message_field(11)


@dataclass(eq=False, repr=False)
class WebcastBarrageMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    event_blob: bytes = betterproto.bytes_field(2)
    msg_type: int = betterproto.int32_field(3)
    duration: int = betterproto.int64_field(6)
    display_config: int = betterproto.int32_field(9)
    gallery_gift_id: int = betterproto.int64_field(10)
    schema: str = betterproto.string_field(22)
    sub_type: str = betterproto.string_field(23)


@dataclass(eq=False, repr=False)
class WebcastHourlyRankMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    rank_container_blob: bytes = betterproto.bytes_field(2)
    data2: int = betterproto.uint32_field(3)


@dataclass(eq=False, repr=False)
class MsgDetectTriggerCondition(betterproto.Message):
    uplink_detect_http: bool = betterproto.bool_field(1)
    uplink_detect_web_socket: bool = betterproto.bool_field(2)
    detect_p2p_msg: bool = betterproto.bool_field(3)
    detect_room_msg: bool = betterproto.bool_field(4)
    http_optimize: bool = betterproto.bool_field(5)


@dataclass(eq=False, repr=False)
class MsgDetectTimeInfo(betterproto.Message):
    client_start_ms: int = betterproto.int64_field(1)
    api_recv_time_ms: int = betterproto.int64_field(2)
    api_send_to_goim_ms: int = betterproto.int64_field(3)


@dataclass(eq=False, repr=False)
class WebcastMsgDetectMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    detect_type: int = betterproto.int32_field(2)
    trigger_condition: "MsgDetectTriggerCondition" = betterproto.message_field(3)
    time_info: "MsgDetectTimeInfo" = betterproto.message_field(4)
    trigger_by: int = betterproto.int32_field(5)
    from_region: str = betterproto.string_field(6)


@dataclass(eq=False, repr=False)
class WebcastLinkMicFanTicketMethod(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    fan_ticket_room_notice_blob: bytes = betterproto.bytes_field(2)


@dataclass(eq=False, repr=False)
class RoomVerifyMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    action: int = betterproto.int32_field(2)
    content: str = betterproto.string_field(3)
    notice_type: int = betterproto.int32_field(4)
    close_room: bool = betterproto.bool_field(5)


@dataclass(eq=False, repr=False)
class WebcastOecLiveShoppingMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    shopping_data_blob: bytes = betterproto.bytes_field(2)


@dataclass(eq=False, repr=False)
class WebcastGiftBroadcastMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    broadcast_data_blob: bytes = betterproto.bytes_field(2)


@dataclass(eq=False, repr=False)
class WebcastRankTextMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    scene: int = betterproto.int32_field(2)
    owner_idx_before_update: int = betterproto.int64_field(3)
    owner_idx_after_update: int = betterproto.int64_field(4)
    self_get_badge_msg: str = betterproto.string_field(5)
    other_get_badge_msg: str = betterproto.string_field(6)
    cur_user_id: int = betterproto.int64_field(7)


@dataclass(eq=False, repr=False)
class WebcastGiftDynamicRestrictionMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    restriction_blob: bytes = betterproto.bytes_field(2)


@dataclass(eq=False, repr=False)
class WebcastViewerPicksUpdateMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    update_type: int = betterproto.int32_field(2)
    picks_blob: bytes = betterproto.bytes_field(3)


# === Secondary events ===


@dataclass(eq=False, repr=False)
class WebcastSystemMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    message: str = betterproto.string_field(2)


@dataclass(eq=False, repr=False)
class WebcastLiveGameIntroMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    game_data_blob: bytes = betterproto.bytes_field(2)


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
    id1: int = betterproto.int64_field(2)
    timestamp: int = betterproto.int64_field(3)


@dataclass(eq=False, repr=False)
class WebcastLinkmicBattleTaskMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    task_data_blob: bytes = betterproto.bytes_field(2)


@dataclass(eq=False, repr=False)
class WebcastMarqueeAnnouncementMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    message_scene: int = betterproto.int32_field(2)
    entity_list_blob: bytes = betterproto.bytes_field(3)


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
    offline_game_list_blob: bytes = betterproto.bytes_field(2)


@dataclass(eq=False, repr=False)
class WebcastPartnershipPunishMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    punish_info_blob: bytes = betterproto.bytes_field(2)


@dataclass(eq=False, repr=False)
class WebcastPerceptionMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    dialog_blob: bytes = betterproto.bytes_field(2)
    end_time: int = betterproto.int64_field(4)


@dataclass(eq=False, repr=False)
class WebcastSpeakerMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    user: "User" = betterproto.message_field(2)
    display_text: "Text" = betterproto.message_field(3)
    trigger_type: int = betterproto.int32_field(4)


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
    toast_text: str = betterproto.string_field(4)
    button_text: str = betterproto.string_field(5)
    button_schema: str = betterproto.string_field(6)
