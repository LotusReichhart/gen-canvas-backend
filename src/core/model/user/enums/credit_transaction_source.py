from enum import Enum


class CreditTransactionSource(str, Enum):
    """Nguồn gốc của giao dịch điểm (credit)"""
    DAILY_REFILL = "daily_refill"  # Được hồi hàng ngày
    AD_REWARD = "ad_reward"  # Xem quảng cáo
    AI_IMAGE_CREATE = "ai_image_create"  # Dùng tính năng tạo ảnh
    AI_IMAGE_EDIT = "ai_image_edit"  # Dùng tính năng sửa ảnh
    AI_BG_REMOVE = "ai_bg_remove"  # Dùng tính năng xóa phông
    AI_ID_PHOTO = "ai_id_photo"  # Dùng tính năng ảnh thẻ
    INITIAL_GIFT = "initial_gift"  # Quà tặng khi đăng ký