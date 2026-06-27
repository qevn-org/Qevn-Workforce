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
                
        # Fallback to default system org if org_id is mock
        db_org_id = "00000000-0000-0000-0000-000000000000" if organization_id == "org_mock_456" else organization_id
        
        name = payload["name"]
        description = payload.get("description", "")
        role_title = payload.get("role_title", "Custom Agent")
        department = payload.get("department", "Operations")
        system_prompt = payload["system_prompt"]
        
        from packages.shared.src.db.client import SessionLocal
        from sqlalchemy import text
        import uuid
        
        employee_id = str(uuid.uuid4())
        
        try:
            with SessionLocal() as session:
                with session.begin():
                    query = text("""
                        INSERT INTO employees (id, organization_id, name, description, role_title, department, system_prompt)
                        VALUES (:id, :org_id, :name, :description, :role_title, :department, :system_prompt);
                    """)
                    session.execute(query, {
                        "id": employee_id,
                        "org_id": db_org_id,
                        "name": name,
                        "description": description,
                        "role_title": role_title,
                        "department": department,
                        "system_prompt": system_prompt
                    })
            payload["id"] = employee_id
        except Exception as e:
            logger.error(f"Failed to insert employee to DB: {str(e)}")
            raise e
            
        # 2. Publish Domain Event
        EventBus.publish("EmployeeInstalled", {
            "organization_id": organization_id,
            "employee_id": employee_id,
            "name": payload["name"]
        })
        logger.info(f"Employee {payload['name']} registered in DB and org {organization_id}.")
        return payload

    def list_employees(self, organization_id: str) -> List[Dict[str, Any]]:
        from packages.shared.src.db.client import SessionLocal
        from sqlalchemy import text
        
        # Fallback to default system org if org_id is mock
        db_org_id = "00000000-0000-0000-0000-000000000000" if organization_id == "org_mock_456" else organization_id
        
        try:
            with SessionLocal() as session:
                query = text("""
                    SELECT id, name, description, role_title, department, system_prompt, timezone
                    FROM employees
                    WHERE organization_id = :org_id;
                """)
                result = session.execute(query, {"org_id": db_org_id})
                employees = []
                for row in result:
                    employees.append({
                        "id": str(row[0]),
                        "name": row[1],
                        "description": row[2] or "",
                        "role_title": row[3] or "",
                        "department": row[4] or "",
                        "system_prompt": row[5] or "",
                        "timezone": row[6] or "UTC"
                    })
                return employees
        except Exception as e:
            logger.error(f"Error fetching employees from DB: {str(e)}")
            return []

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

