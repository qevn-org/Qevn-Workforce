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

        # Connect to Postgres database to load configuration dynamically
        from packages.shared.src.db.client import SessionLocal
        from sqlalchemy import text

        db_employee_id = employee_id
        db_org_id = (
            "00000000-0000-0000-0000-000000000000"
            if organization_id == "org_mock_456"
            else organization_id
        )

        try:
            with SessionLocal() as session:
                query = text(
                    """
                    SELECT id, organization_id, name, department, role_title, description, system_prompt
                    FROM employees
                    WHERE id::text = :id AND organization_id::text = :org_id;
                """
                )
                res = session.execute(
                    query, {"id": db_employee_id, "org_id": db_org_id}
                )
                row = res.fetchone()
                if not row:
                    # Fallback to query by ID only (ignoring org ID constraints for cross-tenant resilience in dev)
                    query_fallback = text(
                        """
                        SELECT id, organization_id, name, department, role_title, description, system_prompt
                        FROM employees
                        WHERE id::text = :id;
                    """
                    )
                    res_fallback = session.execute(
                        query_fallback, {"id": db_employee_id}
                    )
                    row = res_fallback.fetchone()
                    if not row:
                        logger.warning(f"Employee {employee_id} not found in database.")
                        return None

                (
                    emp_id,
                    db_org,
                    name,
                    department,
                    role_title,
                    description,
                    system_prompt,
                ) = row

                # Load bound capabilities from employee_capabilities
                cap_query = text(
                    """
                    SELECT capability_id, config
                    FROM employee_capabilities
                    WHERE employee_id::text = :id;
                """
                )
                cap_res = session.execute(cap_query, {"id": str(emp_id)})
                capabilities = []
                for cap_row in cap_res.fetchall():
                    capabilities.append(
                        {"capability_id": cap_row[0], "config": cap_row[1] or {}}
                    )

                # Load tool permissions
                tool_query = text(
                    """
                    SELECT tool_name
                    FROM employee_tools
                    WHERE employee_id::text = :id;
                """
                )
                tool_res = session.execute(tool_query, {"id": str(emp_id)})
                tool_permissions = [tool_row[0] for tool_row in tool_res.fetchall()]

                # Fallback defaults if capabilities or tools are empty
                if not capabilities:
                    capabilities = [
                        {"capability_id": "research_v1", "config": {}},
                        {"capability_id": "crm_v1", "config": {}},
                        {"capability_id": "email_v1", "config": {}},
                    ]
                if not tool_permissions:
                    tool_permissions = ["gmail:send", "hubspot:write"]

                logger.info(
                    f"Successfully loaded configuration for Employee {name} from database."
                )
                return EmployeeConfig(
                    id=str(emp_id),
                    organization_id=str(db_org),
                    name=name,
                    department=department or "Operations",
                    role=role_title or "AI Employee",
                    description=description or "",
                    system_prompt=system_prompt,
                    capabilities=capabilities,
                    tool_permissions=tool_permissions,
                )

        except Exception as e:
            logger.error(
                f"Error loading employee {employee_id} from database: {str(e)}"
            )
            return None
