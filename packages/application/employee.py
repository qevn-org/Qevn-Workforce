import logging
from typing import Dict, Any, List
from packages.events.bus import EventBus
from packages.capabilities.registry import CapabilityRegistry

logger = logging.getLogger("EmployeeService")

class EmployeeService:
    """
    Coordinates AI Employee administration.
    Publishes domain events and validates integrity schemas.
    """
    
    def create_employee(self, organization_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        # 1. Validation Logic
        required = ["name", "system_prompt"]
        for field in required:
            if field not in payload:
                raise ValueError(f"Validation failed: Field '{field}' is required.")
                
        employee_id = payload.get("id", "emp-sdr-001")
        
        # Save to DB logic...
        
        # 2. Publish Domain Event
        EventBus.publish("EmployeeInstalled", {
            "organization_id": organization_id,
            "employee_id": employee_id,
            "name": payload["name"]
        })
        logger.info(f"Employee {payload['name']} registered in org {organization_id}.")
        return payload

    def install_capabilities(self, organization_id: str, employee_id: str, capability_ids: List[str]) -> bool:
        # Load registry checks
        CapabilityRegistry.load_builtin_capabilities()
        
        # Verify capability existences
        for cap_id in capability_ids:
            cap = CapabilityRegistry.get_capability(cap_id)
            if not cap:
                raise ValueError(f"Capability '{cap_id}' is not registered.")
                
        # Update bindings...
        
        EventBus.publish("EmployeeUpdated", {
            "organization_id": organization_id,
            "employee_id": employee_id,
            "installed_capabilities": capability_ids
        })
        logger.info(f"Capabilities {capability_ids} bound to Employee {employee_id}.")
        return True
