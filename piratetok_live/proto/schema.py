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


# === Common types (Image / Text / Format) ===


@dataclass(eq=False, repr=False)
class ImageContent(betterproto.Message):
    name: str = betterproto.string_field(1)
    font_color: str = betterproto.string_field(2)
    level: int = betterproto.int64_field(3)


@dataclass(eq=False, repr=False)
class Image(betterproto.Message):
    url_list: List[str] = betterproto.string_field(1)
    uri: str = betterproto.string_field(2)
    height: int = betterproto.int32_field(3)
    width: int = betterproto.int32_field(4)
    avg_color: str = betterproto.string_field(5)
    image_type: int = betterproto.int32_field(6)
    schema: str = betterproto.string_field(7)
    content: "ImageContent" = betterproto.message_field(8)
    is_animated: bool = betterproto.bool_field(9)


@dataclass(eq=False, repr=False)
class TextFormat(betterproto.Message):
    color: str = betterproto.string_field(1)
    bold: bool = betterproto.bool_field(2)
    italic: bool = betterproto.bool_field(3)
    weight: int = betterproto.int32_field(4)
    italic_angle: int = betterproto.int32_field(5)
    font_size: int = betterproto.int32_field(6)
    use_high_light_color: bool = betterproto.bool_field(7)
    use_remote_color: bool = betterproto.bool_field(8)


@dataclass(eq=False, repr=False)
class PatternRef(betterproto.Message):
    key: str = betterproto.string_field(1)
    default_pattern: str = betterproto.string_field(2)


@dataclass(eq=False, repr=False)
class TextPieceUser(betterproto.Message):
    user: "User" = betterproto.message_field(1)
    with_colon: bool = betterproto.bool_field(2)


@dataclass(eq=False, repr=False)
class TextPieceGift(betterproto.Message):
    gift_id: int = betterproto.int32_field(1)
    name_ref: "PatternRef" = betterproto.message_field(2)
    show_type: int = betterproto.int32_field(3)
    color_id: int = betterproto.int64_field(4)


@dataclass(eq=False, repr=False)
class TextPiece(betterproto.Message):
    type: int = betterproto.int32_field(1)
    format: "TextFormat" = betterproto.message_field(2)
    string_value: str = betterproto.string_field(11)
    user_value: "TextPieceUser" = betterproto.message_field(21)
    gift_value: "TextPieceGift" = betterproto.message_field(22)
    pattern_ref_value: "PatternRef" = betterproto.message_field(24)


@dataclass(eq=False, repr=False)
class Text(betterproto.Message):
    key: str = betterproto.string_field(1)
    default_pattern: str = betterproto.string_field(2)
    default_format: "TextFormat" = betterproto.message_field(3)
    pieces: List["TextPiece"] = betterproto.message_field(4)


# === Common message header (full schema) ===


@dataclass(eq=False, repr=False)
class Common(betterproto.Message):
    method: str = betterproto.string_field(1)
    msg_id: int = betterproto.int64_field(2)
    room_id: int = betterproto.int64_field(3)
    create_time: int = betterproto.int64_field(4)
    monitor: int = betterproto.int32_field(5)
    is_show_msg: bool = betterproto.bool_field(6)
    describe: str = betterproto.string_field(7)
    display_text: "Text" = betterproto.message_field(8)
    fold_type: int = betterproto.int64_field(9)
    anchor_fold_type: int = betterproto.int64_field(10)
    priority_score: int = betterproto.int64_field(11)
    log_id: str = betterproto.string_field(12)
    msg_process_filter_k: str = betterproto.string_field(13)
    msg_process_filter_v: str = betterproto.string_field(14)
    from_idc: str = betterproto.string_field(15)
    to_idc: str = betterproto.string_field(16)
    filter_msg_tags: List[str] = betterproto.string_field(17)
    anchor_priority_score: int = betterproto.int64_field(21)
    room_message_heat_level: int = betterproto.int64_field(22)
    fold_type_for_web: int = betterproto.int64_field(23)
    anchor_fold_type_for_web: int = betterproto.int64_field(24)
    client_send_time: int = betterproto.int64_field(25)
    dispatch_strategy: int = betterproto.int32_field(26)


# === User context (sub-routed to events that carry it) ===


@dataclass(eq=False, repr=False)
class UserIdentity(betterproto.Message):
    is_gift_giver_of_anchor: bool = betterproto.bool_field(1)
    is_subscriber_of_anchor: bool = betterproto.bool_field(2)
    is_mutual_following_with_anchor: bool = betterproto.bool_field(3)
    is_follower_of_anchor: bool = betterproto.bool_field(4)
    is_moderator_of_anchor: bool = betterproto.bool_field(5)
    is_anchor: bool = betterproto.bool_field(6)


# === Badge sub-types ===


@dataclass(eq=False, repr=False)
class PrivilegeLogExtra(betterproto.Message):
    data_version: str = betterproto.string_field(1)
    privilege_id: str = betterproto.string_field(2)
    privilege_version: str = betterproto.string_field(3)
    privilege_order_id: str = betterproto.string_field(4)
    level: str = betterproto.string_field(5)


@dataclass(eq=False, repr=False)
class ImageBadge(betterproto.Message):
    badge_display_type: int = betterproto.int32_field(1)
    image: "Image" = betterproto.message_field(2)


@dataclass(eq=False, repr=False)
class TextBadge(betterproto.Message):
    badge_display_type: int = betterproto.int32_field(1)
    key: str = betterproto.string_field(2)
    default_pattern: str = betterproto.string_field(3)
    pieces: List[str] = betterproto.string_field(4)


@dataclass(eq=False, repr=False)
class StringBadge(betterproto.Message):
    badge_display_type: int = betterproto.int32_field(1)
    str_value: str = betterproto.string_field(2)


@dataclass(eq=False, repr=False)
class CombineBadgeBackground(betterproto.Message):
    image: "Image" = betterproto.message_field(1)
    background_color_code: str = betterproto.string_field(2)
    border_color_code: str = betterproto.string_field(3)


@dataclass(eq=False, repr=False)
class FontStyle(betterproto.Message):
    font_size: int = betterproto.int32_field(1)
    font_width: int = betterproto.int32_field(2)
    font_color: str = betterproto.string_field(3)
    border_color: str = betterproto.string_field(4)


@dataclass(eq=False, repr=False)
class BadgeText(betterproto.Message):
    """Used inside CombineBadge.text. Distinct from TextBadge — no leading enum."""
    key: str = betterproto.string_field(1)
    default_pattern: str = betterproto.string_field(2)
    pieces: List[str] = betterproto.string_field(3)


@dataclass(eq=False, repr=False)
class CombineBadge(betterproto.Message):
    badge_display_type: int = betterproto.int32_field(1)
    icon: "Image" = betterproto.message_field(2)
    text: "BadgeText" = betterproto.message_field(3)
    str_value: str = betterproto.string_field(4)
    font_style: "FontStyle" = betterproto.message_field(6)
    background: "CombineBadgeBackground" = betterproto.message_field(11)
    background_dark_mode: "CombineBadgeBackground" = betterproto.message_field(12)
    icon_auto_mirrored: bool = betterproto.bool_field(13)
    bg_auto_mirrored: bool = betterproto.bool_field(14)
    public_screen_show_style: int = betterproto.int32_field(15)
    personal_card_show_style: int = betterproto.int32_field(16)
    rank_list_online_audience_show_style: int = betterproto.int32_field(17)
    multi_guest_show_style: int = betterproto.int32_field(18)


@dataclass(eq=False, repr=False)
class BadgeStruct(betterproto.Message):
    """badge_scene: ADMIN=1, SUBSCRIBER=4, RANK_LIST=6, USER_GRADE=8, FANS=10"""
    display_type: int = betterproto.int32_field(1)
    priority_type: int = betterproto.int32_field(2)
    badge_scene: int = betterproto.int32_field(3)
    position: int = betterproto.int32_field(4)
    display_status: int = betterproto.int32_field(5)
    greyed_by_client: int = betterproto.int64_field(6)
    exhibition_type: int = betterproto.int32_field(7)
    schema_url: str = betterproto.string_field(10)
    display: bool = betterproto.bool_field(11)
    log_extra: "PrivilegeLogExtra" = betterproto.message_field(12)
    image_badge: "ImageBadge" = betterproto.message_field(20)
    text_badge: "TextBadge" = betterproto.message_field(21)
    string_badge: "StringBadge" = betterproto.message_field(22)
    combine_badge: "CombineBadge" = betterproto.message_field(23)
    is_customized: bool = betterproto.bool_field(24)


# === FollowInfo / FansClub / Subscribe ===


@dataclass(eq=False, repr=False)
class FollowInfo(betterproto.Message):
    following_count: int = betterproto.int64_field(1)
    follower_count: int = betterproto.int64_field(2)
    follow_status: int = betterproto.int64_field(3)
    push_status: int = betterproto.int64_field(4)


@dataclass(eq=False, repr=False)
class UserBadge(betterproto.Message):
    icons: Dict[str, "Image"] = betterproto.map_field(
        1, betterproto.TYPE_STRING, betterproto.TYPE_MESSAGE
    )
    title: str = betterproto.string_field(2)


@dataclass(eq=False, repr=False)
class FansClubData(betterproto.Message):
    club_name: str = betterproto.string_field(1)
    level: int = betterproto.int32_field(2)
    user_fans_club_status: int = betterproto.int32_field(3)
    badge: "UserBadge" = betterproto.message_field(4)
    available_gift_ids: List[int] = betterproto.int64_field(5)
    anchor_id: int = betterproto.int64_field(6)


@dataclass(eq=False, repr=False)
class FansClubMember(betterproto.Message):
    data: "FansClubData" = betterproto.message_field(1)
    prefer_data: Dict[str, "FansClubData"] = betterproto.map_field(
        2, betterproto.TYPE_STRING, betterproto.TYPE_MESSAGE
    )


@dataclass(eq=False, repr=False)
class FansClubInfo(betterproto.Message):
    fans_level: int = betterproto.int64_field(2)
    fans_score: int = betterproto.int64_field(3)
    fans_count: int = betterproto.int64_field(5)
    fans_club_name: str = betterproto.string_field(6)


@dataclass(eq=False, repr=False)
class SubscribeInfo(betterproto.Message):
    is_subscribe: bool = betterproto.bool_field(2)
    subscriber_count: int = betterproto.int64_field(5)


# === User mod flags / verification / extras ===


@dataclass(eq=False, repr=False)
class UserAttr(betterproto.Message):
    is_muted: bool = betterproto.bool_field(1)
    is_admin: bool = betterproto.bool_field(2)
    is_super_admin: bool = betterproto.bool_field(3)
    mute_duration: int = betterproto.int64_field(4)


@dataclass(eq=False, repr=False)
class AuthenticationInfo(betterproto.Message):
    custom_verify: str = betterproto.string_field(1)
    enterprise_verify_reason: str = betterproto.string_field(2)
    authentication_badge: "Image" = betterproto.message_field(3)


@dataclass(eq=False, repr=False)
class BorderInfo(betterproto.Message):
    icon: "Image" = betterproto.message_field(1)
    level: int = betterproto.int64_field(2)
    source: str = betterproto.string_field(3)
    profile_decoration_ribbon: "Image" = betterproto.message_field(4)
    avatar_background_color: str = betterproto.string_field(7)
    avatar_background_border_color: str = betterproto.string_field(8)


@dataclass(eq=False, repr=False)
class ComboBadgeInfo(betterproto.Message):
    icon: "Image" = betterproto.message_field(1)
    combo_count: int = betterproto.int64_field(2)


@dataclass(eq=False, repr=False)
class AnchorLevel(betterproto.Message):
    level: int = betterproto.int64_field(1)
    experience: int = betterproto.int64_field(2)
    lowest_experience_this_level: int = betterproto.int64_field(3)
    highest_experience_this_level: int = betterproto.int64_field(4)
    stage_level: "Image" = betterproto.message_field(12)
    small_icon: "Image" = betterproto.message_field(13)


@dataclass(eq=False, repr=False)
class Author(betterproto.Message):
    video_total_count: int = betterproto.int64_field(1)
    video_total_play_count: int = betterproto.int64_field(2)
    video_total_favorite_count: int = betterproto.int64_field(6)


@dataclass(eq=False, repr=False)
class UserHonor(betterproto.Message):
    total_diamond: int = betterproto.int64_field(1)
    diamond_icon: "Image" = betterproto.message_field(2)
    current_honor_name: str = betterproto.string_field(3)
    current_honor_icon: "Image" = betterproto.message_field(4)
    level: int = betterproto.int32_field(6)
    current_diamond: int = betterproto.int64_field(9)
    score: int = betterproto.int64_field(25)


@dataclass(eq=False, repr=False)
class GradeIcon(betterproto.Message):
    icon: "Image" = betterproto.message_field(1)
    icon_diamond: int = betterproto.int64_field(2)
    level: int = betterproto.int64_field(3)
    level_str: str = betterproto.string_field(4)


@dataclass(eq=False, repr=False)
class PayGrade(betterproto.Message):
    total_diamond_count: int = betterproto.int64_field(1)
    diamond_icon: "Image" = betterproto.message_field(2)
    name: str = betterproto.string_field(3)
    icon: "Image" = betterproto.message_field(4)
    next_name: str = betterproto.string_field(5)
    level: int = betterproto.int64_field(6)
    next_icon: "Image" = betterproto.message_field(7)
    next_diamond: int = betterproto.int64_field(8)
    now_diamond: int = betterproto.int64_field(9)
    this_grade_min_diamond: int = betterproto.int64_field(10)
    this_grade_max_diamond: int = betterproto.int64_field(11)
    grade_icon_list: List["GradeIcon"] = betterproto.message_field(26)
    score: int = betterproto.int64_field(25)
    grade_banner: str = betterproto.string_field(1001)


@dataclass(eq=False, repr=False)
class OwnRoom(betterproto.Message):
    room_ids: List[int] = betterproto.int64_field(1)


@dataclass(eq=False, repr=False)
class EcommerceEntrance(betterproto.Message):
    url: str = betterproto.string_field(1)
    type: int = betterproto.int32_field(2)


# === User (full proto) ===


@dataclass(eq=False, repr=False)
class User(betterproto.Message):
    id: int = betterproto.int64_field(1)
    nickname: str = betterproto.string_field(3)
    bio_description: str = betterproto.string_field(5)
    avatar_thumb: "Image" = betterproto.message_field(9)
    avatar_medium: "Image" = betterproto.message_field(10)
    avatar_large: "Image" = betterproto.message_field(11)
    verified: bool = betterproto.bool_field(12)
    status: int = betterproto.int32_field(15)
    create_time: int = betterproto.int64_field(16)
    modify_time: int = betterproto.int64_field(17)
    secret: int = betterproto.int32_field(18)
    share_qrcode_uri: str = betterproto.string_field(19)
    badge_image_list: List["Image"] = betterproto.message_field(21)
    follow_info: "FollowInfo" = betterproto.message_field(22)
    user_honor: "UserHonor" = betterproto.message_field(23)
    fans_club: "FansClubMember" = betterproto.message_field(24)
    border: "BorderInfo" = betterproto.message_field(25)
    special_id: str = betterproto.string_field(26)
    avatar_border: "Image" = betterproto.message_field(27)
    medal: "Image" = betterproto.message_field(28)
    user_badges: List["Image"] = betterproto.message_field(29)
    new_user_badges: List["Image"] = betterproto.message_field(30)
    top_vip_no: int = betterproto.int32_field(31)
    user_attr: "UserAttr" = betterproto.message_field(32)
    own_room: "OwnRoom" = betterproto.message_field(33)
    pay_score: int = betterproto.int64_field(34)
    fan_ticket_count: int = betterproto.int64_field(35)
    anchor_info: "AnchorLevel" = betterproto.message_field(36)
    link_mic_stats: int = betterproto.int32_field(37)
    unique_id: str = betterproto.string_field(38)
    enable_show_commerce_sale: bool = betterproto.bool_field(39)
    with_fusion_shop_entry: bool = betterproto.bool_field(40)
    pay_scores: int = betterproto.int64_field(41)
    anchor_level: "AnchorLevel" = betterproto.message_field(42)
    verified_content: str = betterproto.string_field(43)
    author_info: "Author" = betterproto.message_field(44)
    top_fans: List["User"] = betterproto.message_field(45)
    sec_uid: str = betterproto.string_field(46)
    user_role: int = betterproto.int32_field(47)
    personal_card: "Image" = betterproto.message_field(52)
    authentication_info: "AuthenticationInfo" = betterproto.message_field(53)
    media_badge_image_list: List["Image"] = betterproto.message_field(57)
    commerce_webcast_config_ids: List[int] = betterproto.int64_field(60)
    borders: List["BorderInfo"] = betterproto.message_field(61)
    combo_badge_info: "ComboBadgeInfo" = betterproto.message_field(62)
    subscribe_info: "SubscribeInfo" = betterproto.message_field(63)
    badge_list: List["BadgeStruct"] = betterproto.message_field(64)
    mint_type_label: List[int] = betterproto.int64_field(65)
    fans_club_info: "FansClubInfo" = betterproto.message_field(66)
    pay_grade: "PayGrade" = betterproto.message_field(67)
    allow_find_by_contacts: bool = betterproto.bool_field(1002)
    allow_others_download_video: bool = betterproto.bool_field(1003)
    allow_others_download_when_sharing_video: bool = betterproto.bool_field(1004)
    allow_share_show_profile: bool = betterproto.bool_field(1005)
    allow_show_in_gossip: bool = betterproto.bool_field(1006)
    allow_show_my_action: bool = betterproto.bool_field(1007)
    allow_strange_comment: bool = betterproto.bool_field(1008)
    allow_unfollower_comment: bool = betterproto.bool_field(1009)
    allow_use_linkmic: bool = betterproto.bool_field(1010)
    avatar_jpg: "Image" = betterproto.message_field(1012)
    background_img_url: str = betterproto.string_field(1013)
    block_status: int = betterproto.int32_field(1016)
    comment_restrict: int = betterproto.int32_field(1017)
    constellation: str = betterproto.string_field(1018)
    disable_ichat: int = betterproto.int32_field(1019)
    enable_ichat_img: int = betterproto.int64_field(1020)
    exp: int = betterproto.int32_field(1021)
    fold_stranger_chat: bool = betterproto.bool_field(1023)
    follow_status: int = betterproto.int64_field(1024)
    ichat_restrict_type: int = betterproto.int32_field(1027)
    id_str: str = betterproto.string_field(1028)
    is_follower: bool = betterproto.bool_field(1029)
    is_following: bool = betterproto.bool_field(1030)
    need_profile_guide: bool = betterproto.bool_field(1031)
    push_comment_status: bool = betterproto.bool_field(1033)
    push_digg: bool = betterproto.bool_field(1034)
    push_follow: bool = betterproto.bool_field(1035)
    push_friend_action: bool = betterproto.bool_field(1036)
    push_ichat: bool = betterproto.bool_field(1037)
    push_status: bool = betterproto.bool_field(1038)
    push_video_post: bool = betterproto.bool_field(1039)
    push_video_recommend: bool = betterproto.bool_field(1040)
    verified_reason: str = betterproto.string_field(1043)
    enable_car_management_permission: bool = betterproto.bool_field(1044)
    scm_label: str = betterproto.string_field(1046)
    ecommerce_entrance: "EcommerceEntrance" = betterproto.message_field(1047)
    is_block: bool = betterproto.bool_field(1048)
    is_subscribe: bool = betterproto.bool_field(1090)
    is_anchor_marked: bool = betterproto.bool_field(1091)


# === Public area common ===


@dataclass(eq=False, repr=False)
class PublicAreaCommon(betterproto.Message):
    user_label: "Image" = betterproto.message_field(1)
    user_consume_in_room: int = betterproto.int64_field(2)


@dataclass(eq=False, repr=False)
class PortraitTagItem(betterproto.Message):
    tag_type: int = betterproto.int32_field(1)
    tag_text: "Text" = betterproto.message_field(2)


@dataclass(eq=False, repr=False)
class PortraitTopic(betterproto.Message):
    topic_action_type: int = betterproto.int32_field(1)
    topic_text: "Text" = betterproto.message_field(2)
    topic_tips: "Text" = betterproto.message_field(3)


@dataclass(eq=False, repr=False)
class CreatorSuccessInfo(betterproto.Message):
    tags: List["PortraitTagItem"] = betterproto.message_field(1)
    topic: "PortraitTopic" = betterproto.message_field(2)


@dataclass(eq=False, repr=False)
class UserMetricsItem(betterproto.Message):
    type: int = betterproto.int32_field(1)
    metrics_value: str = betterproto.string_field(2)


@dataclass(eq=False, repr=False)
class PortraitTag(betterproto.Message):
    tag_id: str = betterproto.string_field(1)
    priority: int = betterproto.int64_field(2)
    show_value: str = betterproto.string_field(3)
    show_args: str = betterproto.string_field(4)


@dataclass(eq=False, repr=False)
class PortraitInfo(betterproto.Message):
    user_metrics: List["UserMetricsItem"] = betterproto.message_field(1)
    portrait_tag: List["PortraitTag"] = betterproto.message_field(2)


@dataclass(eq=False, repr=False)
class UserInteractionInfo(betterproto.Message):
    like_cnt: int = betterproto.int64_field(1)
    comment_cnt: int = betterproto.int64_field(2)
    share_cnt: int = betterproto.int64_field(3)


@dataclass(eq=False, repr=False)
class PublicAreaMessageCommon(betterproto.Message):
    scroll_gap_count: int = betterproto.int64_field(1)
    anchor_scroll_gap_count: int = betterproto.int64_field(2)
    release_to_scroll_area: bool = betterproto.bool_field(3)
    anchor_release_to_scroll_area: bool = betterproto.bool_field(4)
    is_anchor_marked: bool = betterproto.bool_field(5)
    creator_success_info: "CreatorSuccessInfo" = betterproto.message_field(6)
    portrait_info: "PortraitInfo" = betterproto.message_field(7)
    user_interaction_info: "UserInteractionInfo" = betterproto.message_field(8)
    admin_fold_type: int = betterproto.int64_field(9)


# === MsgFilter / Emote ===


@dataclass(eq=False, repr=False)
class MsgFilter(betterproto.Message):
    is_gifter: bool = betterproto.bool_field(1)
    is_subscribed_to_anchor: bool = betterproto.bool_field(2)


@dataclass(eq=False, repr=False)
class Emote(betterproto.Message):
    emote_id: str = betterproto.string_field(1)
    image: "Image" = betterproto.message_field(2)


@dataclass(eq=False, repr=False)
class EmoteData(betterproto.Message):
    place_in_comment: int = betterproto.int32_field(1)
    emote: "Emote" = betterproto.message_field(2)


# === Gift sub-types ===


@dataclass(eq=False, repr=False)
class GiftBoxInfo(betterproto.Message):
    capacity: int = betterproto.int64_field(1)
    is_primary_box: bool = betterproto.bool_field(2)
    scheme_url: str = betterproto.string_field(3)


@dataclass(eq=False, repr=False)
class GiftPanelBanner(betterproto.Message):
    display_text: "Text" = betterproto.message_field(1)
    left_icon: "Image" = betterproto.message_field(2)
    schema_url: str = betterproto.string_field(3)
    bg_colors: List[str] = betterproto.string_field(5)
    banner_lynx_url: str = betterproto.string_field(6)
    banner_priority: int = betterproto.int32_field(7)
    banner_lynx_extra: str = betterproto.string_field(8)
    bg_image: "Image" = betterproto.message_field(9)


@dataclass(eq=False, repr=False)
class GiftStruct(betterproto.Message):
    image: "Image" = betterproto.message_field(1)
    describe: str = betterproto.string_field(2)
    duration: int = betterproto.int32_field(4)
    id: int = betterproto.int64_field(5)
    for_link_mic: bool = betterproto.bool_field(7)
    combo: bool = betterproto.bool_field(10)
    type: int = betterproto.int32_field(11)
    diamond_count: int = betterproto.int32_field(12)
    is_displayed_on_panel: bool = betterproto.bool_field(13)
    primary_effect_id: int = betterproto.int64_field(14)
    gift_label_icon: "Image" = betterproto.message_field(15)
    name: str = betterproto.string_field(16)
    icon: "Image" = betterproto.message_field(21)
    gold_effect: str = betterproto.string_field(24)
    preview_image: "Image" = betterproto.message_field(47)
    gift_panel_banner: "GiftPanelBanner" = betterproto.message_field(48)
    is_broadcast_gift: bool = betterproto.bool_field(49)
    is_effect_befview: bool = betterproto.bool_field(50)
    is_random_gift: bool = betterproto.bool_field(51)
    is_box_gift: bool = betterproto.bool_field(52)
    can_put_in_gift_box: bool = betterproto.bool_field(53)
    gift_box_info: "GiftBoxInfo" = betterproto.message_field(54)


@dataclass(eq=False, repr=False)
class GiftIMPriority(betterproto.Message):
    queue_sizes: List[int] = betterproto.int64_field(1)
    self_queue_priority: int = betterproto.int64_field(2)
    priority: int = betterproto.int64_field(3)


@dataclass(eq=False, repr=False)
class GiftMonitorInfo(betterproto.Message):
    anchor_id: int = betterproto.int64_field(1)
    profit_api_message_dur: int = betterproto.int64_field(2)
    send_gift_profit_api_start_ms: int = betterproto.int64_field(3)
    send_gift_profit_core_start_ms: int = betterproto.int64_field(4)
    send_gift_req_start_ms: int = betterproto.int64_field(5)
    send_gift_send_message_success_ms: int = betterproto.int64_field(6)
    send_profit_api_dur: int = betterproto.int64_field(7)
    to_user_id: int = betterproto.int64_field(8)
    send_gift_start_client_local_ms: int = betterproto.int64_field(9)
    from_platform: str = betterproto.string_field(10)
    from_version: str = betterproto.string_field(11)


@dataclass(eq=False, repr=False)
class SponsorshipInfo(betterproto.Message):
    gift_id: int = betterproto.int64_field(1)
    sponsor_id: int = betterproto.int64_field(2)
    light_gift_up: bool = betterproto.bool_field(3)
    unlighted_gift_icon: str = betterproto.string_field(4)
    gift_gallery_detail_page_scheme_url: str = betterproto.string_field(5)
    gift_gallery_click_sponsor: bool = betterproto.bool_field(6)
    become_all_sponsored: bool = betterproto.bool_field(21)


@dataclass(eq=False, repr=False)
class MatchInfo(betterproto.Message):
    critical: int = betterproto.int64_field(1)
    effect_card_in_use: bool = betterproto.bool_field(2)
    multiplier_type: int = betterproto.int32_field(3)
    multiplier_value: int = betterproto.int64_field(4)


@dataclass(eq=False, repr=False)
class GiftTrayInfo(betterproto.Message):
    m_dynamic_img: "Image" = betterproto.message_field(1)
    can_mirror: bool = betterproto.bool_field(2)
    tray_normal_bg_img: "Image" = betterproto.message_field(3)
    tray_normal_bg_color: List[str] = betterproto.string_field(4)
    tray_small_bg_img: "Image" = betterproto.message_field(5)
    tray_small_bg_color: List[str] = betterproto.string_field(6)
    right_tag_text: "Text" = betterproto.message_field(7)
    right_tag_bg_img: "Image" = betterproto.message_field(8)
    right_tag_bg_color: List[str] = betterproto.string_field(9)
    tray_name_text_color: str = betterproto.string_field(10)
    tray_desc_text_color: str = betterproto.string_field(11)
    right_tag_jump_schema: str = betterproto.string_field(12)


@dataclass(eq=False, repr=False)
class InteractiveGiftInfo(betterproto.Message):
    cross_screen_delay: int = betterproto.int64_field(1)
    cross_screen_role: int = betterproto.int64_field(2)
    uniq_id: int = betterproto.int64_field(4)
    to_user_team_id: int = betterproto.int64_field(5)


@dataclass(eq=False, repr=False)
class LynxGiftExtra(betterproto.Message):
    id: int = betterproto.int64_field(1)
    code: int = betterproto.int64_field(2)
    type: int = betterproto.int64_field(3)
    params: List[str] = betterproto.string_field(4)
    extra: str = betterproto.string_field(5)


@dataclass(eq=False, repr=False)
class TextEffectDetail(betterproto.Message):
    text: "Text" = betterproto.message_field(1)
    text_font_size: int = betterproto.int32_field(2)
    background: "Image" = betterproto.message_field(3)
    start: int = betterproto.int64_field(4)
    duration: int = betterproto.int64_field(5)
    x: int = betterproto.int32_field(6)
    y: int = betterproto.int32_field(7)


@dataclass(eq=False, repr=False)
class TextEffect(betterproto.Message):
    portrait_detail: "TextEffectDetail" = betterproto.message_field(1)
    landscape_detail: "TextEffectDetail" = betterproto.message_field(2)


# === Core Webcast events ===


@dataclass(eq=False, repr=False)
class WebcastChatMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    user: "User" = betterproto.message_field(2)
    content: str = betterproto.string_field(3)
    visible_to_sender: bool = betterproto.bool_field(4)
    background: "Image" = betterproto.message_field(5)
    full_screen_text_color: str = betterproto.string_field(6)
    background_image_v2: "Image" = betterproto.message_field(7)
    public_area_common: "PublicAreaCommon" = betterproto.message_field(9)
    gift_image: "Image" = betterproto.message_field(10)
    input_type: int = betterproto.int32_field(11)
    at_user: "User" = betterproto.message_field(12)
    emotes: List["EmoteData"] = betterproto.message_field(13)
    content_language: str = betterproto.string_field(14)
    msg_filter: "MsgFilter" = betterproto.message_field(15)
    quick_chat_scene: int = betterproto.int32_field(16)
    communityflagged_status: int = betterproto.int32_field(17)
    user_identity: "UserIdentity" = betterproto.message_field(18)
    comment_tag: List[int] = betterproto.int32_field(20)
    public_area_message_common: "PublicAreaMessageCommon" = betterproto.message_field(21)
    screen_time: int = betterproto.int64_field(22)
    signature: str = betterproto.string_field(23)
    signature_version: str = betterproto.string_field(24)
    ec_streamer_key: str = betterproto.string_field(25)


@dataclass(eq=False, repr=False)
class WebcastGiftMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    gift_id: int = betterproto.int32_field(2)
    fan_ticket_count: int = betterproto.int64_field(3)
    group_count: int = betterproto.int32_field(4)
    repeat_count: int = betterproto.int32_field(5)
    combo_count: int = betterproto.int32_field(6)
    user: "User" = betterproto.message_field(7)
    to_user: "User" = betterproto.message_field(8)
    repeat_end: int = betterproto.int32_field(9)
    text_effect: "TextEffect" = betterproto.message_field(10)
    group_id: int = betterproto.uint64_field(11)
    income_taskgifts: int = betterproto.int64_field(12)
    room_fan_ticket_count: int = betterproto.int64_field(13)
    priority: "GiftIMPriority" = betterproto.message_field(14)
    gift: "GiftStruct" = betterproto.message_field(15)
    log_id: str = betterproto.string_field(16)
    send_type: int = betterproto.int64_field(17)
    public_area_common: "PublicAreaCommon" = betterproto.message_field(18)
    tray_display_text: "Text" = betterproto.message_field(19)
    banned_display_effects: int = betterproto.int64_field(20)
    tray_info: "GiftTrayInfo" = betterproto.message_field(21)
    monitor_extra: str = betterproto.string_field(22)
    gift_extra: "GiftMonitorInfo" = betterproto.message_field(23)
    color_id: int = betterproto.int64_field(24)
    is_first_sent: bool = betterproto.bool_field(25)
    display_text_for_anchor: "Text" = betterproto.message_field(26)
    display_text_for_audience: "Text" = betterproto.message_field(27)
    order_id: str = betterproto.string_field(28)
    gifts_in_box_blob: bytes = betterproto.bytes_field(29)
    msg_filter: "MsgFilter" = betterproto.message_field(30)
    lynx_extra: List["LynxGiftExtra"] = betterproto.message_field(31)
    user_identity: "UserIdentity" = betterproto.message_field(32)
    match_info: "MatchInfo" = betterproto.message_field(33)
    linkmic_gift_expression_strategy: int = betterproto.int32_field(34)
    flying_mic_resources_blob: bytes = betterproto.bytes_field(35)
    disable_gift_tracking: bool = betterproto.bool_field(36)
    asset_blob: bytes = betterproto.bytes_field(37)
    version: int = betterproto.int32_field(38)
    sponsorship_info: List["SponsorshipInfo"] = betterproto.message_field(39)
    flying_mic_resources_v2_blob: bytes = betterproto.bytes_field(40)
    public_area_message_common: "PublicAreaMessageCommon" = betterproto.message_field(41)
    signature: str = betterproto.string_field(42)
    signature_version: str = betterproto.string_field(43)
    multi_generate_message: bool = betterproto.bool_field(44)
    to_member_id: str = betterproto.string_field(45)
    to_member_id_int: int = betterproto.int64_field(46)
    to_member_nickname: str = betterproto.string_field(47)
    interactive_gift_info: "InteractiveGiftInfo" = betterproto.message_field(48)

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
    total: int = betterproto.int64_field(3)
    color: int = betterproto.int32_field(4)
    user: "User" = betterproto.message_field(5)
    icon: str = betterproto.string_field(6)
    icons: List["Image"] = betterproto.message_field(7)
    effect_cnt: int = betterproto.int64_field(9)
    public_area_message_common: "PublicAreaMessageCommon" = betterproto.message_field(11)
    room_message_heat_level: int = betterproto.int64_field(12)


@dataclass(eq=False, repr=False)
class WebcastMemberMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    user: "User" = betterproto.message_field(2)
    member_count: int = betterproto.int32_field(3)
    operator: "User" = betterproto.message_field(4)
    is_set_to_admin: bool = betterproto.bool_field(5)
    is_top_user: bool = betterproto.bool_field(6)
    rank_score: int = betterproto.int32_field(7)
    top_user_no: int = betterproto.int32_field(8)
    enter_type: int = betterproto.int32_field(9)
    action: int = betterproto.int32_field(10)
    action_description: str = betterproto.string_field(11)
    user_id: int = betterproto.int64_field(12)
    pop_str: str = betterproto.string_field(14)
    background: "Image" = betterproto.message_field(17)
    anchor_display_text: "Text" = betterproto.message_field(18)
    client_enter_source: str = betterproto.string_field(19)
    client_enter_type: str = betterproto.string_field(20)
    client_live_reason: str = betterproto.string_field(21)
    action_duration: int = betterproto.int64_field(22)
    user_share_type: str = betterproto.string_field(23)
    display_style: int = betterproto.int32_field(24)
    kick_source: int = betterproto.int32_field(26)
    allow_preview_time: int = betterproto.int64_field(27)
    last_subscription_action: int = betterproto.int64_field(28)
    public_area_message_common: "PublicAreaMessageCommon" = betterproto.message_field(29)
    live_sub_only_tier: int = betterproto.int64_field(30)
    live_sub_only_month: int = betterproto.int64_field(31)
    ec_streamer_key: str = betterproto.string_field(32)
    show_wave: int = betterproto.int64_field(33)
    hit_ab_status: int = betterproto.int32_field(35)


@dataclass(eq=False, repr=False)
class Contributor(betterproto.Message):
    score: int = betterproto.int64_field(1)
    user: "User" = betterproto.message_field(2)
    rank: int = betterproto.int64_field(3)
    delta: int = betterproto.int64_field(4)


@dataclass(eq=False, repr=False)
class WebcastRoomUserSeqMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    ranks_list: List["Contributor"] = betterproto.message_field(2)
    viewer_count: int = betterproto.int64_field(3)
    pop_str: str = betterproto.string_field(4)
    seats_list: List["Contributor"] = betterproto.message_field(5)
    popularity: int = betterproto.int64_field(6)
    total_user: int = betterproto.int64_field(7)
    anonymous: int = betterproto.int64_field(8)


@dataclass(eq=False, repr=False)
class WebcastSocialMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    user: "User" = betterproto.message_field(2)
    share_type: int = betterproto.int64_field(3)
    action: int = betterproto.int64_field(4)
    share_target: str = betterproto.string_field(5)
    follow_count: int = betterproto.int64_field(6)
    share_display_style: int = betterproto.int64_field(7)
    share_count: int = betterproto.int32_field(8)
    public_area_message_common: "PublicAreaMessageCommon" = betterproto.message_field(9)
    signature: str = betterproto.string_field(10)
    signature_version: str = betterproto.string_field(11)
    show_duration_ms: int = betterproto.int64_field(12)


@dataclass(eq=False, repr=False)
class WebcastControlExtra(betterproto.Message):
    reason_no: int = betterproto.int64_field(2)
    source: str = betterproto.string_field(8)


@dataclass(eq=False, repr=False)
class WebcastControlMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    action: int = betterproto.int32_field(2)
    tips: str = betterproto.string_field(3)
    extra: "WebcastControlExtra" = betterproto.message_field(4)
    float_style: int = betterproto.int32_field(9)


@dataclass(eq=False, repr=False)
class WebcastLiveIntroMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    id: int = betterproto.int64_field(2)
    audit_status: int = betterproto.int32_field(3)
    content: str = betterproto.string_field(4)
    user: "User" = betterproto.message_field(5)
    intro_mode: int = betterproto.int32_field(6)
    badges: List["BadgeStruct"] = betterproto.message_field(7)
    content_language: str = betterproto.string_field(8)


@dataclass(eq=False, repr=False)
class WebcastRoomMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    content: str = betterproto.string_field(2)
    supprot_landscape: bool = betterproto.bool_field(3)
    source: int = betterproto.int32_field(4)
    icon: "Image" = betterproto.message_field(5)
    scene: int = betterproto.int32_field(6)
    is_welcome: bool = betterproto.bool_field(7)
    public_area_common: "PublicAreaMessageCommon" = betterproto.message_field(8)
    show_duration_ms: int = betterproto.int64_field(9)
    sub_scene: str = betterproto.string_field(10)


@dataclass(eq=False, repr=False)
class CaptionContent(betterproto.Message):
    language: str = betterproto.string_field(1)
    text: str = betterproto.string_field(2)


@dataclass(eq=False, repr=False)
class WebcastCaptionMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    timestamp_ms: int = betterproto.int64_field(2)
    duration_ms: int = betterproto.int64_field(3)
    content: List["CaptionContent"] = betterproto.message_field(4)
    sentence_id: int = betterproto.int64_field(5)
    sequence_id: int = betterproto.int64_field(6)
    definite: bool = betterproto.bool_field(7)


@dataclass(eq=False, repr=False)
class WebcastGoalUpdateMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    indicator_blob: bytes = betterproto.bytes_field(2)
    goal_blob: bytes = betterproto.bytes_field(3)
    contributor_id: int = betterproto.int64_field(4)
    contributor_avatar: "Image" = betterproto.message_field(5)
    contributor_display_id: str = betterproto.string_field(6)
    contribute_subgoal_blob: bytes = betterproto.bytes_field(7)
    contribute_count: int = betterproto.int64_field(9)
    contribute_score: int = betterproto.int64_field(10)
    gift_repeat_count: int = betterproto.int64_field(11)
    contributor_id_str: str = betterproto.string_field(12)
    pin: bool = betterproto.bool_field(13)
    unpin: bool = betterproto.bool_field(14)
    pin_info_blob: bytes = betterproto.bytes_field(15)
    update_source: int = betterproto.int32_field(16)
    goal_extra: str = betterproto.string_field(17)


@dataclass(eq=False, repr=False)
class WebcastImDeleteMessage(betterproto.Message):
    common: "Common" = betterproto.message_field(1)
    delete_msg_ids_list: List[int] = betterproto.int64_field(2)
    delete_user_ids_list: List[int] = betterproto.int64_field(3)
