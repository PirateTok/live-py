from typing import Any, NamedTuple


class EventType:
    # Control
    connected = "connected"
    disconnected = "disconnected"
    reconnecting = "reconnecting"
    unknown = "unknown"

    # core
    chat = "chat"
    gift = "gift"
    like = "like"
    member = "member"
    social = "social"
    room_user_seq = "room_user_seq"
    control = "control"

    # Sub-routed convenience
    follow = "follow"
    share = "share"
    join = "join"
    live_ended = "live_ended"

    # useful
    live_intro = "live_intro"
    room_message = "room_message"
    caption = "caption"
    goal_update = "goal_update"
    im_delete = "im_delete"

    # niche + extended
    rank_update = "rank_update"
    poll = "poll"
    envelope = "envelope"
    room_pin = "room_pin"
    unauthorized_member = "unauthorized_member"
    link_mic_method = "link_mic_method"
    link_mic_battle = "link_mic_battle"
    link_mic_armies = "link_mic_armies"
    link_message = "link_message"
    link_layer = "link_layer"
    link_mic_layout_state = "link_mic_layout_state"
    gift_panel_update = "gift_panel_update"
    in_room_banner = "in_room_banner"
    guide = "guide"
    emote_chat = "emote_chat"
    question_new = "question_new"
    sub_notify = "sub_notify"
    barrage = "barrage"
    hourly_rank = "hourly_rank"
    msg_detect = "msg_detect"
    link_mic_fan_ticket = "link_mic_fan_ticket"
    room_verify = "room_verify"
    oec_live_shopping = "oec_live_shopping"
    gift_broadcast = "gift_broadcast"
    rank_text = "rank_text"
    gift_dynamic_restriction = "gift_dynamic_restriction"
    viewer_picks_update = "viewer_picks_update"

    # secondary
    access_control = "access_control"
    access_recall = "access_recall"
    alert_box_audit_result = "alert_box_audit_result"
    binding_gift = "binding_gift"
    boost_card = "boost_card"
    bottom = "bottom"
    game_rank_notify = "game_rank_notify"
    gift_prompt = "gift_prompt"
    link_state = "link_state"
    link_mic_battle_punish_finish = "link_mic_battle_punish_finish"
    linkmic_battle_task = "linkmic_battle_task"
    marquee_announcement = "marquee_announcement"
    notice = "notice"
    notify = "notify"
    partnership_drops_update = "partnership_drops_update"
    partnership_game_offline = "partnership_game_offline"
    partnership_punish = "partnership_punish"
    perception = "perception"
    speaker = "speaker"
    sub_capsule = "sub_capsule"
    sub_pin_event = "sub_pin_event"
    subscription_notify = "subscription_notify"
    toast = "toast"
    system = "system"
    live_game_intro = "live_game_intro"


class TikTokEvent(NamedTuple):
    type: str
    data: Any
    room_id: str = ""
