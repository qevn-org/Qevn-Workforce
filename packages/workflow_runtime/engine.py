import uuid
import asyncio
import logging
from typing import Dict, Any, Optional
from packages.events.bus import EventBus

logger = logging.getLogger("WorkflowRuntime")


class WorkflowStatus:
    PENDING = "pending"
    PLANNING = "planning"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"


class WorkflowInstance:
    def __init__(self, run_id: uuid.UUID, goal: str, employee_id: str):
        self.run_id = run_id
        self.goal = goal
        self.employee_id = employee_id
        self.status = WorkflowStatus.PENDING
        self.state_snapshot: Dict[str, Any] = {}
        self.checkpoint_id: Optional[uuid.UUID] = None
        self.retry_count = 0


class WorkflowRuntimeEngine:
    """
    Dedicated enterprise workflow execution engine (Asynchronous).
    Manages execution instances, checkpointing state records, retry limits, and pauses.
    """

    _active_runs: Dict[uuid.UUID, WorkflowInstance] = {}

    @classmethod
    async def start_workflow(cls, employee_id: str, goal: str) -> uuid.UUID:
        run_id = uuid.uuid4()
        instance = WorkflowInstance(run_id=run_id, goal=goal, employee_id=employee_id)
        instance.status = WorkflowStatus.PLANNING

        cls._active_runs[run_id] = instance

        # 1. Enqueue job to ARQ background worker
        try:
            from arq.connections import RedisSettings, create_pool
            from packages.shared.src.db.client import REDIS_URL

            settings = RedisSettings.from_dsn(REDIS_URL)
            redis_pool = await create_pool(settings)

            payload = {
                "task_id": str(run_id),
                "organization_id": "00000000-0000-0000-0000-000000000000",
                "employee_id": employee_id,
                "conversation_id": "default-session",
                "goal": goal,
            }

            await redis_pool.enqueue_job("run_orchestration_job", payload)
            logger.info(f"Workflow enqueued to ARQ background worker. Job ID: {run_id}")
        except Exception as err:
            logger.error(f"Failed to enqueue workflow job to ARQ: {str(err)}")

        # Publish event
        EventBus.publish(
            "WorkflowStarted",
            {
                "workflow_instance_id": str(run_id),
                "employee_id": employee_id,
                "goal": goal,
            },
        )
        logger.info(f"Workflow {run_id} started with goal: '{goal}'")
        return run_id

    @classmethod
    async def save_checkpoint(
        cls,
        run_id: uuid.UUID,
        capability_id: str,
        inputs: Dict[str, Any],
        outputs: Optional[Dict[str, Any]],
        state_snapshot: Dict[str, Any],
    ):
        """Durable checkpoint recorder (Asynchronous)."""
        instance = cls._active_runs.get(run_id)
        if not instance:
            return

        checkpoint_id = uuid.uuid4()
        instance.checkpoint_id = checkpoint_id
        instance.state_snapshot = state_snapshot

        # In production this writes to workflow_checkpoints table
        EventBus.publish(
            "CheckpointCreated",
            {
                "checkpoint_id": str(checkpoint_id),
                "workflow_instance_id": str(run_id),
                "capability_id": capability_id,
                "inputs": inputs,
                "outputs": outputs,
            },
        )
        logger.info(f"Durable checkpoint {checkpoint_id} saved for Workflow {run_id}.")

    @classmethod
    async def execute_with_retry(
        cls,
        run_id: uuid.UUID,
        operation_callable: callable,
        max_retries: int = 3,
        backoff_base: float = 2.0,
    ) -> Any:
        """Executes a capability operation implementing non-blocking exponential backoff retries."""
        instance = cls._active_runs.get(run_id)
        attempt = 0

        while attempt < max_retries:
            try:
                attempt += 1
                if asyncio.iscoroutinefunction(operation_callable):
                    result = await operation_callable()
                else:
                    result = operation_callable()
                return result
            except Exception as e:
                logger.warning(f"Attempt {attempt}/{max_retries} failed: {str(e)}")
                if instance:
                    instance.retry_count += 1

                EventBus.publish(
                    "RetryTriggered",
                    {
                        "workflow_instance_id": str(run_id),
                        "attempt": attempt,
                        "error": str(e),
                    },
                )

                if attempt == max_retries:
                    if instance:
                        instance.status = WorkflowStatus.FAILED
                    EventBus.publish(
                        "WorkflowFailed",
                        {"workflow_instance_id": str(run_id), "error": str(e)},
                    )
                    raise e

                sleep_time = backoff_base**attempt
                logger.info(f"Waiting {sleep_time}s before next retry (async)...")
                await asyncio.sleep(sleep_time)

    @classmethod
    async def pause_for_approval(
        cls,
        run_id: uuid.UUID,
        checkpoint_id: uuid.UUID,
        action_type: str,
        payload: Dict[str, Any],
    ):
        instance = cls._active_runs.get(run_id)
        if instance:
            instance.status = WorkflowStatus.PAUSED

        EventBus.publish(
            "ApprovalRequested",
            {
                "workflow_instance_id": str(run_id),
                "checkpoint_id": str(checkpoint_id),
                "action_type": action_type,
                "payload": payload,
            },
        )
        logger.info(
            f"Workflow {run_id} execution paused awaiting human approval for {action_type}."
        )

    @classmethod
    async def resume_workflow(
        cls, run_id: uuid.UUID, approval_decision: str
    ) -> Optional[WorkflowInstance]:
        instance = cls._active_runs.get(run_id)
        if not instance:
            return None

        instance.status = WorkflowStatus.RUNNING

        EventBus.publish(
            (
                "ApprovalGranted"
                if approval_decision == "approved"
                else "ApprovalRejected"
            ),
            {"workflow_instance_id": str(run_id)},
        )

        logger.info(f"Workflow {run_id} resumed with decision: '{approval_decision}'")
        return instance

    @classmethod
    async def complete_workflow(cls, run_id: uuid.UUID):
        instance = cls._active_runs.get(run_id)
        if instance:
            instance.status = WorkflowStatus.COMPLETED

        EventBus.publish("WorkflowCompleted", {"workflow_instance_id": str(run_id)})
        logger.info(f"Workflow {run_id} completed successfully.")
