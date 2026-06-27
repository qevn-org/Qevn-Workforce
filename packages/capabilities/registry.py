import logging
from typing import Dict, Type, List, Optional
from packages.capabilities.base import BaseCapability, CapabilityDefinition

logger = logging.getLogger("CapabilityRegistry")

class CapabilityRegistry:
    """
    Registry of all dynamic capability plugins installed on the platform.
    Allows dynamic lookup of plugins matching Planner action requests.
    """
    _registry: Dict[str, BaseCapability] = {}

    @classmethod
    def register(cls, capability: BaseCapability):
        """Registers a capability instance into the platform runtime registry."""
        cap_id = capability.definition.id
        cls._registry[cap_id] = capability
        logger.info(f"Successfully registered capability: {capability.definition.name} ({cap_id})")

    @classmethod
    def get_capability(cls, capability_id: str) -> Optional[BaseCapability]:
        return cls._registry.get(capability_id)

    @classmethod
    def resolve_by_action(cls, action_name: str) -> Optional[BaseCapability]:
        """
        Dynamically locates a capability containing the desired action signature.
        Used by the Planner to resolve capabilities at runtime.
        """
        for capability in cls._registry.values():
            if action_name in capability.definition.supported_actions:
                return capability
        return None

    @classmethod
    def list_capabilities(cls) -> List[CapabilityDefinition]:
        return [cap.definition for cap in cls._registry.values()]

    @classmethod
    def load_builtin_capabilities(cls):
        """Forces imports of built-in capability modules to trigger registration."""
        from packages.capabilities import research
        from packages.capabilities import crm
        from packages.capabilities import email
        from packages.capabilities import sdr
