from typing import Dict, Any
from pydantic import BaseModel, Field


class NormalizedEvent(BaseModel):
    """
    Standardized payload schema for all incoming webhooks across QEVN Integration Hub.
    Ensures that downstream workflow runtimes receive uniform event shapes regardless of source.
    """

    event_id: str = Field(description="Unique identifier for the normalization event")
    event_type: str = Field(
        description="Normalized type classification e.g. email.received"
    )
    connector_id: str = Field(
        description="Identifier of the source connector e.g. gmail"
    )
    organization_id: str = Field(description="Context tenant organization ID")
    timestamp: str = Field(description="ISO event creation time")
    actor: str = Field(description="Entity triggering the event")
    payload: Dict[str, Any] = Field(
        default_factory=dict, description="Normalized context metadata payload details"
    )
