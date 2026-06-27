import logging
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from packages.capabilities.registry import CapabilityRegistry

logger = logging.getLogger("EmployeeLoader")


class EmployeeConfig(BaseModel):
    id: str
    organization_id: str
    name: str
    department: str
    role: str
    description: str
    avatar_url: Optional[str] = None
    system_prompt: str
    default_model: str = "claude-3-5-sonnet"
    temperature: float = 0.2
    capabilities: list[Dict[str, Any]] = Field(default_factory=list)
    tool_permissions: list[str] = Field(default_factory=list)
    working_hours: Dict[str, Any] = Field(default_factory=dict)
    approval_rules: Dict[str, Any] = Field(default_factory=dict)


class EmployeeLoader:
    """
    Retrieves configuration-driven Employee Definitions from database / repository layers
    and instantiates capability bindings dynamically.
    """

    @classmethod
    def load_from_db(
        cls, employee_id: str, organization_id: str
    ) -> Optional[EmployeeConfig]:
        # Force load capabilities registry mapping
        CapabilityRegistry.load_builtin_capabilities()

        # Simulating loading configuration from PostgreSQL (matching schemas.py and RLS rules)
        # In production, this executes: SELECT * FROM employees WHERE id = :id AND organization_id = :org_id;

        # Mock configuration for testing
        mock_configs = {
            "employee-sdr-001": EmployeeConfig(
                id="employee-sdr-001",
                organization_id=organization_id,
                name="Alex",
                department="Sales",
                role="Outbound SDR",
                description="Qualifies inbound prospects and syncs contacts.",
                system_prompt="You qualify prospective clients and record their data in CRM.",
                capabilities=[
                    {"capability_id": "research_v1", "config": {}},
                    {"capability_id": "crm_v1", "config": {}},
                    {"capability_id": "email_v1", "config": {}},
                ],
                tool_permissions=["gmail:send", "hubspot:write"],
            )
        }

        config = mock_configs.get(employee_id)
        if not config:
            logger.warning(f"Employee {employee_id} not found in database.")
            return None

        logger.info(f"Successfully loaded configuration for Employee {config.name}")
        return config
