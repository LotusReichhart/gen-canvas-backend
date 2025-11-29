from typing import Dict, Optional

class BusinessException(Exception):
    def __init__(
        self,
        message_key: str,
        status_code: int = 400,
        error_details: Optional[Dict[str, str]] = None
    ):
        self.message_key = message_key
        self.status_code = status_code
        self.error_details = error_details