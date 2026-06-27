import hmac
import hashlib
import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

logger = logging.getLogger("ConnectorSDK")

class ConnectorManifest(BaseModel):
    id: str
    name: str
    version: str
    description: str
    scopes: List[str] = Field(default_factory=list)
    oauth_config: Dict[str, Any] = Field(default_factory=dict)
    webhook_supported: bool = False

class BaseConnector(ABC):
    """
    Abstract base class for all Enterprise Integration Hub connectors.
    Provides standard hooks for OAuth operations, health endpoints,
    and webhook signature verifications.
    """
    
    def __init__(self, manifest: ConnectorManifest, config: Dict[str, Any] = None):
        self.manifest = manifest
        self.config = config or {}
        
    @abstractmethod
    def health_check(self) -> bool:
        """Executes a diagnostic integration request checking API connectivity."""
        pass
        
    def verify_webhook_signature(self, headers: Dict[str, str], body: bytes, secret: str) -> bool:
        """
        Generic HMAC SHA256 signature verifier. Can be overridden by specific API requirements.
        """
        signature = headers.get("X-Qevn-Signature") or headers.get("x-hub-signature-256")
        if not signature:
            logger.warning("Webhook validation failed: Missing signature header.")
            return False
            
        # Clean prefix if GitHub format (sha256=...)
        if signature.startswith("sha256="):
            signature = signature[7:]
            
        try:
            expected = hmac.new(secret.encode("utf-8"), body, hashlib.sha256).hexdigest()
            return hmac.compare_digest(expected, signature)
        except Exception as e:
            logger.error(f"Webhook signature calculation error: {str(e)}")
            return False

    @abstractmethod
    def normalize_webhook_payload(self, raw_payload: Dict[str, Any], context: Dict[str, Any]) -> Any:
        """
        Normalizes a raw incoming API webhook payload to a standard event format.
        """
        pass
