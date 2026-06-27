import json
import logging
from typing import Callable, Dict, List, Any
from packages.shared.src.db.client import get_redis_session

logger = logging.getLogger("QevnEventBus")

class EventBus:
    """
    Decoupled Event Bus broker.
    Publishes workflow logs, capability starts, and approvals using Redis Pub/Sub channels.
    """
    _subscribers: Dict[str, List[Callable[[Dict[str, Any]], None]]] = {}

    @classmethod
    def publish(cls, event_name: str, payload: Dict[str, Any]):
        """Publishes an event to the Redis pubsub channel and triggers local subscribers."""
        payload_data = {
            "event": event_name,
            "data": payload
        }
        
        # 1. Publish via Redis if active
        try:
            redis = get_redis_session()
            redis.publish("qevn_events", json.dumps(payload_data))
            
            # Pipe logs specifically to conversation channel if key is present
            conv_id = payload.get("conversation_id")
            if conv_id:
                redis.publish(f"conversation:{conv_id}:logs", json.dumps(payload_data))
                
        except Exception as e:
            logger.debug(f"Redis publish failed or connection skipped: {str(e)}")

        # 2. Trigger local callbacks (useful for unit tests and local runs)
        subscribers = cls._subscribers.get(event_name, [])
        for callback in subscribers:
            try:
                callback(payload)
            except Exception as ex:
                logger.error(f"Callback error for event {event_name}: {str(ex)}")

    @classmethod
    def subscribe(cls, event_name: str, callback: Callable[[Dict[str, Any]], None]):
        """Registers a callback for a specific event type."""
        if event_name not in cls._subscribers:
            cls._subscribers[event_name] = []
        cls._subscribers[event_name].append(callback)
        logger.info(f"Subscribed callback to event: {event_name}")
