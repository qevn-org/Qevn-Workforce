import gzip
import json
import base64
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class MemoryEntry(BaseModel):
    organization_id: str
    employee_id: str
    memory_type: str  # e.g., 'conversation', 'task', 'long_term'
    content: str
    vector_id: Optional[str] = None


class IMemoryProvider(ABC):
    """
    Abstract interface for all Memory OS providers.
    Supports compression, serialization, and tenant-isolated semantic searches.
    """

    @abstractmethod
    def store(self, entry: MemoryEntry, ttl: Optional[int] = None) -> bool:
        pass

    @abstractmethod
    def retrieve(
        self, organization_id: str, employee_id: str, limit: int = 10
    ) -> List[MemoryEntry]:
        pass

    @abstractmethod
    def semantic_search(
        self, organization_id: str, query: str, limit: int = 5
    ) -> List[MemoryEntry]:
        pass

    def compress_data(self, data: str) -> str:
        """Compresses string content to Gzip Base64 representation."""
        compressed = gzip.compress(data.encode("utf-8"))
        return base64.b64encode(compressed).decode("utf-8")

    def decompress_data(self, compressed_b64: str) -> str:
        """Decompresses Gzip Base64 payload back to UTF-8 string."""
        compressed_bytes = base64.b64decode(compressed_b64.encode("utf-8"))
        return gzip.decompress(compressed_bytes).decode("utf-8")
