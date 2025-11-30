import httpx
import base64
from typing import Dict, Any, Optional
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.exceptions import InvalidSignature
from loguru import logger

from src.core.domain.service.ad_mob_verification_service import AdMobVerificationService

from ..external_service.in_memory_cache import InMemoryCache


class AdMobVerificationServiceImpl(AdMobVerificationService):
    def __init__(
            self,
            cache: InMemoryCache,
            public_key_url: str
    ):
        self._cache = cache
        self._public_key_url = public_key_url

    async def _fetch_keys_from_google(self) -> dict:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(self._public_key_url)
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Failed to fetch AdMob public keys: {e}")
            return {}

    async def _get_public_key(self, key_id: str) -> Optional[ec.EllipticCurvePublicKey]:
        keys_data = await self._cache.get_or_set_atomic(
            key="admob_all_keys",
            async_factory_func=self._fetch_keys_from_google
        )

        if not keys_data:
            return None

        try:
            for key_entry in keys_data.get("keys", []):
                if str(key_entry.get("keyId")) == str(key_id):
                    pem_key = key_entry.get("pem")
                    return load_pem_public_key(pem_key.encode())
        except Exception as e:
            logger.error(f"Failed to load AdMob public key from cached data: {e}")

        return None

    @staticmethod
    def _get_message_to_verify(query_params: Dict[str, Any]) -> bytes:
        params_to_sign = [
            (k, v) for k, v in query_params.items()
            if k not in ["signature", "key_id"]
        ]
        params_to_sign.sort(key=lambda x: x[0])

        message_str = "&".join(f"{k}={v}" for k, v in params_to_sign)
        return message_str.encode()

    async def verify_reward_webhook(self, query_params: Dict[str, Any]) -> bool:
        try:
            signature_b64 = query_params.get("signature")
            key_id = query_params.get("key_id")

            if not signature_b64 or not key_id:
                logger.warning("AdMob SSV: Missing signature or key_id")
                return False

            public_key = await self._get_public_key(str(key_id))
            if not public_key:
                logger.error(f"AdMob SSV: Could not find public key for key_id {key_id}")
                return False

            message = self._get_message_to_verify(query_params)

            signature_bytes = signature_b64.replace('-', '+').replace('_', '/').encode()
            signature_bytes += b'=' * (-len(signature_bytes) % 4)
            signature_der = base64.urlsafe_b64decode(signature_bytes)

            public_key.verify(
                signature_der,
                message,
                ec.ECDSA(hashes.SHA256())
            )

            logger.info(f"AdMob SSV: Successfully verified reward for user {query_params.get('user_id')}")
            return True

        except InvalidSignature:
            logger.warning(f"AdMob SSV: INVALID SIGNATURE. Possible fraud attempt.")
            return False
        except Exception as e:
            logger.error(f"AdMob SSV: Verification process failed: {e}")
            return False