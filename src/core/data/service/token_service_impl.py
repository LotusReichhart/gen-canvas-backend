import uuid
from loguru import logger
from datetime import datetime, timezone, timedelta
from typing import Dict, Optional, Any

from jwt import encode, decode, ExpiredSignatureError, InvalidTokenError

from src.core.domain.service.token_service import TokenService


class TokenServiceImpl(TokenService):
    def __init__(
            self,
            access_secret: str,
            refresh_secret: str,
            access_lifetime: timedelta,
            refresh_lifetime: timedelta,
            algorithm: str = "HS256"
    ):
        self._access_secret = access_secret
        self._refresh_secret = refresh_secret
        self._access_lifetime = access_lifetime
        self._refresh_lifetime = refresh_lifetime
        self._algorithm = algorithm

    def create_access_token(self,
                            user_id: int,
                            signin_count: int,
                            sign_out_count: int,
                            refresh_jti: str) -> Dict[str, str]:
        payload = {
            "id": user_id,
            "signin_count": signin_count,
            "sign_out_count": sign_out_count,
            "exp": datetime.now(timezone.utc) + self._access_lifetime,
            "iat": datetime.now(timezone.utc),
            "jti": str(uuid.uuid4()),
            "refresh_jti": refresh_jti
        }
        token = encode(payload, self._access_secret, algorithm=self._algorithm)
        return {"token": token}

    def create_refresh_token(self,
                             user_id: int,
                             signin_count: int,
                             sign_out_count: int) -> Dict[str, str]:
        device_id = str(uuid.uuid4())
        payload = {
            "id": user_id,
            "signin_count": signin_count,
            "sign_out_count": sign_out_count,
            "exp": datetime.now(timezone.utc) + self._refresh_lifetime,
            "iat": datetime.now(timezone.utc),
            "jti": device_id
        }
        token = encode(payload, self._refresh_secret, algorithm=self._algorithm)
        return {"token": token, "device_id": device_id}

    def verify_access_token(self, token: str) -> Optional[Dict[str, Any]]:
        try:
            return decode(token, self._access_secret, algorithms=[self._algorithm])
        except ExpiredSignatureError:
            logger.warning("Access Token has expired")
            return None
        except InvalidTokenError as e:
            logger.warning(f"Invalid Access Token: {e}")
            return None

    def verify_refresh_token(self, token: str) -> Optional[Dict[str, Any]]:
        try:
            return decode(token, self._refresh_secret, algorithms=[self._algorithm])
        except ExpiredSignatureError:
            logger.warning("Refresh Token has expired")
            return None
        except InvalidTokenError as e:
            logger.warning(f"Invalid Refresh Token: {e}")
            return None

    def create_reset_token(self) -> str:
        return str(uuid.uuid4())
