import logging
import uuid
from typing import Dict, Any, List
from packages.events.bus import EventBus
from packages.workflow_runtime.engine import WorkflowRuntimeEngine

logger = logging.getLogger("WorkflowService")


class WorkflowService:
    """
    Coordinates workflow state queries, triggers executions via the WorkflowRuntime,
    and publishes domain events.
    """

    async def start_workflow(
        self, organization_id: str, employee_id: str, goal: str
    ) -> uuid.UUID:
        # 1. Validation Layer
        if not goal or len(goal) < 5:
            raise ValueError("Validation failed: Target goal description is too short.")

        # 2. Invoke Workflow Runtime
        run_id = await WorkflowRuntimeEngine.start_workflow(employee_id, goal)

        # 3. Publish domain event
        EventBus.publish(
            "WorkflowStarted",
            {
                "organization_id": organization_id,
                "employee_id": employee_id,
                "workflow_instance_id": str(run_id),
                "goal": goal,
            },
        )
        logger.info(
            f"Workflow service enqueued run {run_id} for organization {organization_id}."
        )
        return run_id

    def resume_workflow(
        self, organization_id: str, run_id: uuid.UUID, approval_decision: str
    ) -> bool:
        # Resume checkpoint using Workflow Runtime engine
        instance = WorkflowRuntimeEngine.resume_workflow(run_id, approval_decision)
        if not instance:
            raise ValueError(f"Active run {run_id} not found in execution states.")

        EventBus.publish(
            (
                "ApprovalGranted"
                if approval_decision == "approved"
                else "ApprovalRejected"
            ),
            {
                "organization_id": organization_id,
                "workflow_instance_id": str(run_id),
                "decision": approval_decision,
            },
        )
        logger.info(
            f"Workflow {run_id} approved and resumed in organization {organization_id}."
        )
        return True
