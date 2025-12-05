class StoragePath:
    """
    Định nghĩa cấu trúc thư mục lưu trữ trên S3/Local.
    Cấu trúc:
    images/
    ├── banners/
    └── users/
        └── avatars/
    """
    _IMAGES_ROOT = "images"

    BANNERS = f"{_IMAGES_ROOT}/banners"
    USER_AVATARS = f"{_IMAGES_ROOT}/users/avatars"