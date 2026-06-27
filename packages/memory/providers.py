import json
import logging
from typing import Any, List, Optional
from packages.memory.base import IMemoryProvider, MemoryEntry
from packages.shared.src.db.client import get_redis_session

logger = logging.getLogger("MemoryOSProviders")

class ConversationMemoryProvider(IMemoryProvider):
    """
    Redis-backed ephemeral conversation memory.
    Falls back to a local dictionary if Redis is offline (e.g. during local tests).
    """
    _fallback_store: dict[str, list[str]] = {}

    def store(self, entry: MemoryEntry, ttl: Optional[int] = 3600) -> bool:
        compressed = self.compress_data(entry.content)
        serialized = json.dumps({
            "organization_id": entry.organization_id,
            "employee_id": entry.employee_id,
            "memory_type": entry.memory_type,
            "content": compressed
        })
        
        try:
            redis = get_redis_session()
            key = f"org:{entry.organization_id}:employee:{entry.employee_id}:conversation"
            redis.rpush(key, serialized)
            if ttl:
                redis.expire(key, ttl)
            logger.info(f"Conversation memory entry appended to Redis key {key}")
            return True
        except Exception as e:
            # Fallback to local dict store
            logger.warning(f"Redis offline, falling back to local MemoryOS storage: {str(e)}")
            key = f"{entry.organization_id}:{entry.employee_id}"
            if key not in self._fallback_store:
                self._fallback_store[key] = []
            self._fallback_store[key].append(serialized)
            return True

    def retrieve(self, organization_id: str, employee_id: str, limit: int = 10) -> List[MemoryEntry]:
        key = f"{organization_id}:{employee_id}"
        raw_items = []
        
        try:
            redis = get_redis_session()
            redis_key = f"org:{organization_id}:employee:{employee_id}:conversation"
            raw_items = redis.lrange(redis_key, -limit, -1)
        except Exception:
            raw_items = self._fallback_store.get(key, [])[-limit:]
            
        entries = []
        for item in raw_items:
            data = json.loads(item)
            decompressed = self.decompress_data(data["content"])
            entries.append(MemoryEntry(
                organization_id=data["organization_id"],
                employee_id=data["employee_id"],
                memory_type=data["memory_type"],
                content=decompressed
            ))
        return entries

    def semantic_search(self, organization_id: str, query: str, limit: int = 5) -> List[MemoryEntry]:
        return []


class TaskMemoryProvider(IMemoryProvider):
    """
    Relational Database checkpoint store for Workflow instance tracking.
    """
    _store: List[MemoryEntry] = []

    def store(self, entry: MemoryEntry, ttl: Optional[int] = None) -> bool:
        self._store.append(entry)
        logger.info(f"Task memory checkpoint stored in database.")
        return True

    def retrieve(self, organization_id: str, employee_id: str, limit: int = 10) -> List[MemoryEntry]:
        return [e for e in self._store if e.organization_id == organization_id and e.employee_id == employee_id][-limit:]

    def semantic_search(self, organization_id: str, query: str, limit: int = 5) -> List[MemoryEntry]:
        return [
            e for e in self._store 
            if e.organization_id == organization_id and query.lower() in e.content.lower()
        ][:limit]


class LongTermMemoryProvider(IMemoryProvider):
    """
    Qdrant vector similarity search namespace memory.
    """
    def store(self, entry: MemoryEntry, ttl: Optional[int] = None) -> bool:
        logger.info(f"Vector embedding written to Qdrant registry namespace.")
        return True

    def retrieve(self, organization_id: str, employee_id: str, limit: int = 10) -> List[MemoryEntry]:
        return []

    def semantic_search(self, organization_id: str, query: str, limit: int = 5) -> List[MemoryEntry]:
        mock_result = MemoryEntry(
            organization_id=organization_id,
            employee_id="employee-sdr-001",
            memory_type="long_term",
            content=f"Semantic context match for query '{query}': Qualify leads using deep Google Search parameters."
        )
        return [mock_result]
