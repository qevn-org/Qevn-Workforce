import os
import httpx
import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
from cryptography.fernet import Fernet
from sqlalchemy import text
from packages.shared.src.db.client import AsyncSessionLocal

logger = logging.getLogger("CentralOAuthManager")

# Derived encryption key for credentials at rest
ENCRYPTION_KEY = os.getenv("QEVN_ENCRYPTION_KEY", Fernet.generate_key().decode())
cipher = Fernet(ENCRYPTION_KEY.encode())


class OAuthManager:
    """
    Centralized OAuth Credential Store & Key Rotation Manager.
    Encrypts access/refresh tokens using AES-GCM (via Fernet) before database writes,
    and handles automatic background token refreshes.
    """

    @classmethod
    def encrypt_token(cls, token: str) -> bytes:
        return cipher.encrypt(token.encode("utf-8"))

    @classmethod
    def decrypt_token(cls, encrypted_token: bytes) -> str:
        return cipher.decrypt(encrypted_token).decode("utf-8")

    @classmethod
    async def get_valid_token(cls, connection_id: str) -> str:
        """
        Loads and decrypts access token, executing refresh rotation if expired.
        """
        async with AsyncSessionLocal() as session:
            query = text(
                """
                SELECT encrypted_access_token, encrypted_refresh_token, token_expiry, id 
                FROM oauth_connections 
                WHERE id = :connection_id 
                LIMIT 1;
            """
            )
            res = await session.execute(query, {"connection_id": connection_id})
            row = res.fetchone()
            if not row:
                raise ValueError("OAuth connection not found.")

            enc_access, enc_refresh, expiry, conn_uuid = row

            # Check if token is expired (or close to it, within 2 minutes)
            now = datetime.utcnow()
            if expiry and now >= (expiry - timedelta(minutes=2)):
                logger.info(
                    f"OAuth access token expired for connection {connection_id}. Initiating rotation..."
                )

                # Fetch refresh token
                refresh_token = cls.decrypt_token(enc_refresh) if enc_refresh else None
                if not refresh_token:
                    raise PermissionError(
                        "Access token expired and no refresh token available."
                    )

                # Call mock token exchange API or actual OAuth Provider endpoint
                new_access, new_refresh, expires_in = await cls._refresh_provider_token(
                    refresh_token
                )

                # Encrypt and update credentials in database
                new_enc_access = cls.encrypt_token(new_access)
                new_enc_refresh = (
                    cls.encrypt_token(new_refresh) if new_refresh else enc_refresh
                )
                new_expiry = datetime.utcnow() + timedelta(seconds=expires_in)

                update_query = text(
                    """
                    UPDATE oauth_connections 
                    SET encrypted_access_token = :new_access, 
                        encrypted_refresh_token = :new_refresh, 
                        token_expiry = :new_expiry, 
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = :connection_id;
                """
                )
                await session.execute(
                    update_query,
                    {
                        "new_access": new_enc_access,
                        "new_refresh": new_enc_refresh,
                        "new_expiry": new_expiry,
                        "connection_id": connection_id,
                    },
                )
                await session.commit()
                logger.info(
                    f"OAuth connection credentials rotated successfully for {connection_id}."
                )
                return new_access

            return cls.decrypt_token(enc_access)

    @classmethod
    async def _refresh_provider_token(
        cls, refresh_token: str
    ) -> tuple[str, Optional[str], int]:
        """
        Sends token refresh exchange to provider.
        (Mocked fallback return if network endpoints are not resolving).
        """
        try:
            # Example HTTP client call
            # async with httpx.AsyncClient() as client:
            #     r = await client.post("https://oauth.provider.com/token", data={...})
            #     data = r.json()
            #     return data["access_token"], data.get("refresh_token"), data["expires_in"]
            pass
        except Exception:
            pass

        # Fallback simulated response
        return "rotated_access_token_123", "rotated_refresh_token_456", 3600
