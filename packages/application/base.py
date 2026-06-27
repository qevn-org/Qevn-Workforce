from typing import Protocol, List, Dict, Any, Optional
from uuid import UUID


class IEmployeeService(Protocol):
    def create_employee(
        self, organization_id: str, payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Validates payload and registers a configuration-driven employee in PostgreSQL."""
        ...

    def install_capabilities(
        self, organization_id: str, employee_id: str, capability_ids: List[str]
    ) -> bool:
        """Configures capability mappings for the specified Employee."""
        ...


class IWorkflowService(Protocol):
    def start_workflow(self, organization_id: str, employee_id: str, goal: str) -> UUID:
        """Triggers a workflow runtime instance and logs dynamic events."""
        ...

    def resume_workflow(
        self, organization_id: str, run_id: UUID, approval_decision: str
    ) -> bool:
        """Applies human approval feedback to resume a suspended run checkpoint."""
        ...
