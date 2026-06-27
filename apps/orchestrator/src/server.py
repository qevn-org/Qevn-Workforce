import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List
import uuid

from apps.orchestrator.src.graphs.supervisor import orchestrator_graph
from packages.shared.src.db.client import get_redis_session

app = FastAPI(title="QEVN Workforce Agent Orchestrator Host", version="1.0.0")

# Active execution states (simulating persistent checkpoint storage)
graph_store: Dict[str, Dict[str, Any]] = {}


class RunPayload(BaseModel):
    task_id: str
    organization_id: str
    employee_id: str
    goal: str


class ApprovePayload(BaseModel):
    workflow_run_id: str
    approved: bool
    feedback: str = ""


@app.post("/run")
async def run_orchestrator(payload: RunPayload):
    # Initialize state
    conversation_id = str(uuid.uuid4())
    initial_state = {
        "organization_id": payload.organization_id,
        "employee_id": payload.employee_id,
        "conversation_id": conversation_id,
        "original_goal": payload.goal,
        "current_plan": [],
        "completed_steps": [],
        "messages": [{"role": "user", "content": payload.goal}],
        "next_node": "planner",
        "context_data": {},
        "approval_required": False,
        "approval_payload": None,
        "human_response": None,
        "loop_count": 0,
        "max_loops": 15,
        "cost_budget": 5.0,
        "accumulated_cost": 0.0,
    }

    # Execute graph iteration asynchronously
    result = await orchestrator_graph.ainvoke(initial_state)

    # Save current state checkpoint
    graph_store[payload.task_id] = result

    return {
        "task_id": payload.task_id,
        "conversation_id": conversation_id,
        "status": "active",
        "checkpoint": {
            "approval_required": result.get("approval_required"),
            "next_node": result.get("next_node"),
        },
    }


@app.post("/approve")
async def approve_action(payload: ApprovePayload):
    task_state = graph_store.get(payload.workflow_run_id)
    if not task_state:
        raise HTTPException(status_code=404, detail="Task state session not found.")

    if not task_state.get("approval_required"):
        raise HTTPException(
            status_code=400, detail="This task does not require approval."
        )

    # Inject approval response and resume execution flow
    task_state["human_response"] = "approved" if payload.approved else "rejected"
    task_state["approval_required"] = False
    task_state["next_node"] = "capability_executor"  # Route back to execution node

    # Resume graph execution asynchronously
    result = await orchestrator_graph.ainvoke(task_state)
    graph_store[payload.workflow_run_id] = result

    return {
        "task_id": payload.workflow_run_id,
        "status": "completed" if not result.get("approval_required") else "paused",
        "checkpoint": {"approval_required": result.get("approval_required")},
    }


@app.get("/health")
def health():
    return {"status": "healthy", "service": "Agent Orchestrator"}


if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8001, reload=True)
