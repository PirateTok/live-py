from typing import Dict, List, Type

import betterproto

from .types import EventType, TikTokEvent
from ..proto import schema, messages

_METHOD_MAP: Dict[str, str] = {
    "WebcastChatMessage": EventType.chat,
    "WebcastGiftMessage": EventType.gift,
    "WebcastLikeMessage": EventType.like,
    "WebcastMemberMessage": EventType.member,
    "WebcastSocialMessage": EventType.social,
    "WebcastRoomUserSeqMessage": EventType.room_user_seq,
    "WebcastControlMessage": EventType.control,
    "WebcastLiveIntroMessage": EventType.live_intro,
    "WebcastRoomMessage": EventType.room_message,
    "WebcastCaptionMessage": EventType.caption,
    "WebcastGoalUpdateMessage": EventType.goal_update,
    "WebcastImDeleteMessage": EventType.im_delete,
    "WebcastRankUpdateMessage": EventType.rank_update,
    "WebcastPollMessage": EventType.poll,
    "WebcastEnvelopeMessage": EventType.envelope,
    "WebcastRoomPinMessage": EventType.room_pin,
    "WebcastUnauthorizedMemberMessage": EventType.unauthorized_member,
    "WebcastLinkMicMethod": EventType.link_mic_method,
    "WebcastLinkMicBattle": EventType.link_mic_battle,
    "WebcastLinkMicArmies": EventType.link_mic_armies,
    "WebcastLinkMessage": EventType.link_message,
    "WebcastLinkLayerMessage": EventType.link_layer,
    "WebcastLinkMicLayoutStateMessage": EventType.link_mic_layout_state,
    "WebcastGiftPanelUpdateMessage": EventType.gift_panel_update,
    "WebcastInRoomBannerMessage": EventType.in_room_banner,
    "WebcastGuideMessage": EventType.guide,
    "WebcastEmoteChatMessage": EventType.emote_chat,
    "WebcastQuestionNewMessage": EventType.question_new,
    "WebcastSubNotifyMessage": EventType.sub_notify,
    "WebcastBarrageMessage": EventType.barrage,
    "WebcastHourlyRankMessage": EventType.hourly_rank,
    "WebcastMsgDetectMessage": EventType.msg_detect,
    "WebcastLinkMicFanTicketMethod": EventType.link_mic_fan_ticket,
    "RoomVerifyMessage": EventType.room_verify,
    "WebcastOecLiveShoppingMessage": EventType.oec_live_shopping,
    "WebcastGiftBroadcastMessage": EventType.gift_broadcast,
    "WebcastRankTextMessage": EventType.rank_text,
    "WebcastGiftDynamicRestrictionMessage": EventType.gift_dynamic_restriction,
    "WebcastViewerPicksUpdateMessage": EventType.viewer_picks_update,
    "WebcastAccessControlMessage": EventType.access_control,
    "WebcastAccessRecallMessage": EventType.access_recall,
    "WebcastAlertBoxAuditResultMessage": EventType.alert_box_audit_result,
    "WebcastBindingGiftMessage": EventType.binding_gift,
    "WebcastBoostCardMessage": EventType.boost_card,
    "WebcastBottomMessage": EventType.bottom,
    "WebcastGameRankNotifyMessage": EventType.game_rank_notify,
    "WebcastGiftPromptMessage": EventType.gift_prompt,
    "WebcastLinkStateMessage": EventType.link_state,
    "WebcastLinkMicBattlePunishFinish": EventType.link_mic_battle_punish_finish,
    "WebcastLinkmicBattleTaskMessage": EventType.linkmic_battle_task,
    "WebcastMarqueeAnnouncementMessage": EventType.marquee_announcement,
    "WebcastNoticeMessage": EventType.notice,
    "WebcastNotifyMessage": EventType.notify,
    "WebcastPartnershipDropsUpdateMessage": EventType.partnership_drops_update,
    "WebcastPartnershipGameOfflineMessage": EventType.partnership_game_offline,
    "WebcastPartnershipPunishMessage": EventType.partnership_punish,
    "WebcastPerceptionMessage": EventType.perception,
    "WebcastSpeakerMessage": EventType.speaker,
    "WebcastSubCapsuleMessage": EventType.sub_capsule,
    "WebcastSubPinEventMessage": EventType.sub_pin_event,
    "WebcastSubscriptionNotifyMessage": EventType.subscription_notify,
    "WebcastToastMessage": EventType.toast,
    "WebcastSystemMessage": EventType.system,
    "WebcastLiveGameIntroMessage": EventType.live_game_intro,
}

# Proto class lookup — maps method name → betterproto.Message subclass
_PROTO_CLASSES: Dict[str, Type[betterproto.Message]] = {}

def _register_protos() -> None:
    for mod in (schema, messages):
        for name in dir(mod):
            obj = getattr(mod, name)
            if (
                isinstance(obj, type)
                and issubclass(obj, betterproto.Message)
                and name in _METHOD_MAP
            ):
                _PROTO_CLASSES[name] = obj

_register_protos()


def decode(method: str, payload: bytes, room_id: str = "") -> List[TikTokEvent]:
    event_name = _METHOD_MAP.get(method)
    if event_name is None:
        return [TikTokEvent(EventType.unknown, {"method": method, "payload": payload}, room_id)]

    proto_cls = _PROTO_CLASSES.get(method)
    if proto_cls is None:
        return [TikTokEvent(EventType.unknown, {"method": method, "payload": payload}, room_id)]

    try:
        msg = proto_cls().parse(payload)
        data = msg.to_dict()
    except (ValueError, KeyError, IndexError, TypeError):
        return [TikTokEvent(EventType.unknown, {"method": method, "payload": payload}, room_id)]

    events: List[TikTokEvent] = [TikTokEvent(event_name, data, room_id)]

    # Sub-routing (int() cast: betterproto to_dict returns int64 as str)
    if method == "WebcastSocialMessage":
        action = int(data.get("action", 0))
        if action == 1:
            events.append(TikTokEvent(EventType.follow, data, room_id))
        elif 2 <= action <= 5:
            events.append(TikTokEvent(EventType.share, data, room_id))
    elif method == "WebcastMemberMessage":
        action = int(data.get("action", 0))
        if action == 1:
            events.append(TikTokEvent(EventType.join, data, room_id))
    elif method == "WebcastControlMessage":
        action = int(data.get("action", 0))
        if action == 3:
            events.append(TikTokEvent(EventType.live_ended, data, room_id))

    return events
