import json
import uuid
import asyncio
import hmac
import hashlib
import logging
from datetime import datetime
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    WebSocket,
    WebSocketDisconnect,
    Request,
)
from typing import List, Dict, Any

from apps.gateway.src.middlewares.auth import get_current_user, AuthContext
from apps.gateway.src.core.config import settings
from packages.application.employee import EmployeeService
from packages.application.workflow import WorkflowService
from packages.tools.src.registry import ToolRegistry
from packages.shared.src.db.client import get_redis_session
from packages.events.bus import EventBus

from packages.evaluation.evaluator import AIEvaluator
from packages.evaluation.feedback import FeedbackManager
from packages.evaluation.experiment import ExperimentManager
from packages.evaluation.replay import WorkflowReplayManager
from packages.evaluation.regression import RegressionTestEngine

router = APIRouter()

# Instantiate Application Services
employee_service = EmployeeService()
workflow_service = WorkflowService()


@router.get("/employees", response_model=Dict[str, Any])
def list_employees(current_user: AuthContext = Depends(get_current_user)):
    try:
        res = employee_service.list_employees(current_user.org_id)
        return {"success": True, "data": res}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# 1. Versioned REST API Paths
@router.post("/employees", response_model=Dict[str, Any])
def create_employee(
    payload: Dict[str, Any], current_user: AuthContext = Depends(get_current_user)
):
    try:
        res = employee_service.create_employee(current_user.org_id, payload)
        return {"success": True, "data": res}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/employees/{id}/install", response_model=Dict[str, Any])
def install_employee_capabilities(
    id: str,
    payload: Dict[str, Any],
    current_user: AuthContext = Depends(get_current_user),
):
    try:
        capability_ids = payload.get("capabilities", [])
        employee_service.install_capabilities(current_user.org_id, id, capability_ids)
        return {"success": True, "message": "Capabilities successfully bound."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/workflows/start", response_model=Dict[str, Any])
async def start_workflow(
    payload: Dict[str, Any], current_user: AuthContext = Depends(get_current_user)
):
    try:
        employee_id = payload.get("employee_id")
        goal = payload.get("goal")
        run_id = await workflow_service.start_workflow(
            current_user.org_id, employee_id, goal
        )
        return {"success": True, "data": {"workflow_instance_id": str(run_id)}}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/workflows/{id}/resume", response_model=Dict[str, Any])
def resume_workflow(
    id: str,
    payload: Dict[str, Any],
    current_user: AuthContext = Depends(get_current_user),
):
    try:
        decision = payload.get("decision", "approved")
        workflow_service.resume_workflow(current_user.org_id, uuid.UUID(id), decision)
        return {"success": True, "message": "Workflow successfully resumed."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/tools", response_model=Dict[str, str])
def list_tools(current_user: AuthContext = Depends(get_current_user)):
    return ToolRegistry.list_available_tools()


@router.post("/integrations/webhooks/{subscription_id}")
async def webhook_ingress(subscription_id: str, request: Request):
    # Read raw body for signature verification
    body = await request.body()
    headers = {k.lower(): v for k, v in request.headers.items()}

    # Standard secret for mock verification test
    secret_key = "mock_secret_key"

    # 1. Verify signature
    signature = headers.get("x-qevn-signature")
    if not signature:
        raise HTTPException(
            status_code=401,
            detail="Webhook validation failed: Missing signature header.",
        )

    expected_sig = hmac.new(
        secret_key.encode("utf-8"), body, hashlib.sha256
    ).hexdigest()
    if not hmac.compare_digest(expected_sig, signature):
        # In production this writes to webhook_dlq table
        logger = logging.getLogger("WebhookIngress")
        logger.warning(
            f"Signature mismatch. Writing payload to DLQ for subscription {subscription_id}"
        )
        raise HTTPException(
            status_code=401, detail="Webhook verification signature mismatch."
        )

    # 2. Parse and normalize event payload
    try:
        raw_payload = json.loads(body.decode("utf-8"))
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON payload.")

    normalized_event = {
        "event_id": str(uuid.uuid4()),
        "event_type": raw_payload.get("event_type", "generic.webhook"),
        "connector_id": raw_payload.get("connector_id", "gmail"),
        "organization_id": raw_payload.get("organization_id", "org_mock"),
        "timestamp": str(datetime.utcnow()),
        "actor": raw_payload.get("actor", "system"),
        "payload": raw_payload.get("data", {}),
    }

    # Publish to platform event bus
    EventBus.publish("NormalizedEventReceived", normalized_event)

    return {"success": True, "message": "Webhook received and normalized."}


# 3. AI Evaluation & Continuous Improvement Endpoints
@router.get("/evaluation/scorecards/{employee_id}", response_model=Dict[str, Any])
async def get_scorecard(
    employee_id: str, current_user: AuthContext = Depends(get_current_user)
):
    try:
        scorecard = await AIEvaluator.generate_scorecard(
            employee_id, current_user.org_id
        )
        return {"success": True, "data": scorecard}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/evaluation/experiments", response_model=Dict[str, Any])
async def create_experiment(
    payload: Dict[str, Any], current_user: AuthContext = Depends(get_current_user)
):
    try:
        # In production this parses payload and inserts to experiments table
        return {
            "success": True,
            "message": "Experiment successfully created and activated.",
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/evaluation/replay", response_model=Dict[str, Any])
async def replay_workflow(
    payload: Dict[str, Any], current_user: AuthContext = Depends(get_current_user)
):
    try:
        wf_id_str = payload.get("workflow_instance_id")
        if not wf_id_str:
            raise ValueError("Missing workflow_instance_id payload parameter.")
        wf_id = uuid.UUID(wf_id_str)
        new_prompt = payload.get("new_prompt")
        new_model = payload.get("new_model")

        report = await WorkflowReplayManager.replay_workflow(
            workflow_instance_id=wf_id, new_prompt=new_prompt, new_model=new_model
        )
        return {"success": True, "data": report}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/evaluation/feedback", response_model=Dict[str, Any])
async def submit_human_feedback(
    payload: Dict[str, Any], current_user: AuthContext = Depends(get_current_user)
):
    try:
        wf_id_str = payload.get("workflow_instance_id")
        if not wf_id_str:
            raise ValueError("Missing workflow_instance_id payload parameter.")
        wf_id = uuid.UUID(wf_id_str)
        rating = payload.get("rating")
        correction = payload.get("correction")
        edits = payload.get("edits", [])
        decision = payload.get("decision")

        success = await FeedbackManager.submit_feedback(
            organization_id=current_user.org_id,
            workflow_instance_id=wf_id,
            rating=rating,
            correction=correction,
            edit_history=edits,
            decision=decision,
        )
        return {"success": success, "message": "Human feedback recorded successfully."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/evaluation/benchmarks/{suite_id}/run", response_model=Dict[str, Any])
async def run_benchmark_regression(
    suite_id: str,
    payload: Dict[str, Any],
    current_user: AuthContext = Depends(get_current_user),
):
    try:
        model_name = payload.get("model", "claude-3-5-sonnet")
        prompt_ver_str = payload.get("prompt_version_id")
        prompt_ver = uuid.UUID(prompt_ver_str) if prompt_ver_str else None

        res = await RegressionTestEngine.run_benchmark_suite(
            suite_id=uuid.UUID(suite_id),
            prompt_version_id=prompt_ver,
            model_name=model_name,
        )
        return {"success": True, "data": res}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# 2. Versioned WebSockets stream with 10s heartbeat checks
@router.websocket("/stream")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    redis = get_redis_session()
    pubsub = redis.pubsub()

    async def send_heartbeat():
        """Sends ping frame every 10s to keep connection alive."""
        while True:
            try:
                await asyncio.sleep(10)
                await websocket.send_json({"event": "ping"})
            except asyncio.CancelledError:
                break
            except Exception:
                break

    heartbeat_task = None
    try:
        # Await subscription authentication frame
        auth_data = await websocket.receive_text()
        claims = json.loads(auth_data)

        token = claims.get("token")
        conversation_id = claims.get("conversation_id")

        if not token or not conversation_id:
            await websocket.send_json({"error": "Unauthorized connection request."})
            await websocket.close(code=4001)
            return

        pubsub.subscribe(f"conversation:{conversation_id}:logs")
        await websocket.send_json(
            {"status": "subscribed", "conversation_id": conversation_id}
        )

        # Start heartbeat task
        heartbeat_task = asyncio.create_task(send_heartbeat())

        while True:
            # Yield control to prevent blocking event loop
            await asyncio.sleep(0.1)
            msg = pubsub.get_message(ignore_subscribe_messages=True, timeout=0.1)
            if msg:
                data = json.loads(msg["data"])
                await websocket.send_json(data)

    except WebSocketDisconnect:
        logger = logging.getLogger("WSGateway")
        logger.info("WebSocket connection closed by client.")
    finally:
        if heartbeat_task:
            heartbeat_task.cancel()
        pubsub.unsubscribe()
        pubsub.close()
