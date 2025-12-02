from typing import Optional

from pydantic import BaseModel


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None

class ResetTokenResponse(BaseModel):
    reset_token: str
