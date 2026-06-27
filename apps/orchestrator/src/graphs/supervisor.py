import json
import logging
import uuid
import asyncio
from typing import Dict, Any
from langgraph.graph import StateGraph, END
from apps.orchestrator.src.state import AgentState
from packages.capabilities.registry import CapabilityRegistry
from packages.employees.loader import EmployeeLoader
from packages.shared.src.db.client import get_redis_session
from packages.events.bus import EventBus
from packages.policy_engine.rules import PolicyEngine, PolicyContext, PolicyDecision
from packages.workflow_runtime.engine import WorkflowRuntimeEngine

logger = logging.getLogger("QevnOrchestrator")


async def planner_node(state: AgentState) -> Dict[str, Any]:
    """
    Dynamic Planner Node (Asynchronous).
    Analyzes goal and steps to decide next action with safety boundaries.
    """
    goal = state["original_goal"]
    completed = state.get("completed_steps", [])
    messages = state.get("messages", [])

    # 1. Initialize budget/loop variables if not present
    loop_count = state.get("loop_count", 0) + 1
    max_loops = state.get("max_loops", 15)
    cost_budget = state.get("cost_budget", 5.0)
    accumulated_cost = state.get("accumulated_cost", 0.0)

    logger.info(
        f"Dynamic Planner analyzing goal: '{goal}' (Loop {loop_count}/{max_loops})"
    )

    # Check if a workflow instance has been initialized
    run_id_str = state.get("context_data", {}).get("workflow_instance_id")
    if not run_id_str:
        # Step 0: Initialize Workflow Runtime run
        run_id = await WorkflowRuntimeEngine.start_workflow(state["employee_id"], goal)
        run_id_str = str(run_id)
        state["context_data"]["workflow_instance_id"] = run_id_str

    # 2. Enforce safety thresholds
    if loop_count > max_loops:
        logger.error(
            f"Planner loop limit exceeded ({loop_count}/{max_loops}). Suspending workflow."
        )
        EventBus.publish(
            "IncidentTriggered",
            {
                "workflow_instance_id": run_id_str,
                "severity": "Critical",
                "message": f"Orchestration suspended: Exceeded max loop limit of {max_loops} iterations.",
            },
        )
        # Force graph transition to suspension node
        return {
            "loop_count": loop_count,
            "approval_required": True,
            "next_node": "human_approval_gate",
            "context_data": {
                "workflow_instance_id": run_id_str,
                "next_action": "suspend_loop_limit",
                "action_inputs": {
                    "reason": f"Loop iteration count {loop_count} exceeds threshold."
                },
            },
        }

    if accumulated_cost >= cost_budget:
        logger.error(
            f"Planner cost budget exceeded (${accumulated_cost}/${cost_budget}). Suspending workflow."
        )
        EventBus.publish(
            "IncidentTriggered",
            {
                "workflow_instance_id": run_id_str,
                "severity": "Critical",
                "message": f"Orchestration suspended: Exceeded budget cap of ${cost_budget}.",
            },
        )
        return {
            "approval_required": True,
            "next_node": "human_approval_gate",
            "context_data": {
                "workflow_instance_id": run_id_str,
                "next_action": "suspend_budget_limit",
                "action_inputs": {
                    "reason": f"Accumulated cost ${accumulated_cost} exceeds budget ${cost_budget}."
                },
            },
        }

    # Try to execute with real LLM if keys are present
    import os

    openai_key = os.getenv("OPENAI_API_KEY")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")

    if openai_key or anthropic_key:
        try:
            from pydantic import BaseModel, Field
            from typing import List, Dict, Any

            class PlannerDecision(BaseModel):
                reasoning: str = Field(
                    description="Explanation of the planning decision and why this step was chosen."
                )
                next_action: str = Field(
                    description="Name of the action to execute (e.g., 'search_web', 'sync_lead', 'send_email'), or 'finalize' if the goal is fully accomplished."
                )
                action_inputs: Dict[str, Any] = Field(
                    default_factory=dict,
                    description="The input parameters matching the action's schema. Leave empty if next_action is 'finalize'.",
                )
                current_plan: List[str] = Field(
                    default_factory=list,
                    description="An updated list of steps to achieve the user's goal.",
                )

            # Load employee configurations for prompts
            emp_config = EmployeeLoader.load_from_db(
                state["employee_id"], state["organization_id"]
            )

            # Retrieve capability schemas
            capabilities_info = []
            for cap in CapabilityRegistry.list_capabilities():
                schema_dict = {}
                if hasattr(cap.input_schema, "model_json_schema"):
                    schema_dict = cap.input_schema.model_json_schema()
                elif hasattr(cap.input_schema, "schema"):
                    schema_dict = cap.input_schema.schema()

                capabilities_info.append(
                    {
                        "capability_id": cap.id,
                        "name": cap.name,
                        "description": cap.description,
                        "supported_actions": cap.supported_actions,
                        "input_schema": schema_dict,
                    }
                )

            system_prompt = (
                f"You are the Supervisor Agent for an AI Employee.\n"
                f"Employee Name: {emp_config.name if emp_config else 'Agent'}\n"
                f"Role Prompt: {emp_config.system_prompt if emp_config else 'Execute workflows and record results.'}\n\n"
                f"Available Actions & Input Schemas:\n"
                f"{json.dumps(capabilities_info, indent=2)}\n\n"
                f"Your task is to analyze the original goal, the completed steps, and history logs, and decide the next action.\n"
                f"If the goal has been successfully completed, return 'finalize' as the next_action.\n"
                f"You must strictly return a structured response matching the PlannerDecision schema."
            )

            history_text = "\n".join(
                [f"{m['role'].upper()}: {m['content']}" for m in messages]
            )

            model = None
            if openai_key:
                from langchain_openai import ChatOpenAI

                model = ChatOpenAI(
                    model=os.getenv("OPENAI_MODEL", "gpt-4o"), temperature=0
                )
            else:
                from langchain_anthropic import ChatAnthropic

                model = ChatAnthropic(
                    model_name=os.getenv(
                        "ANTHROPIC_MODEL", "claude-3-5-sonnet-20240620"
                    ),
                    temperature=0,
                )

            structured_model = model.with_structured_output(PlannerDecision)

            from langchain_core.messages import SystemMessage, HumanMessage

            messages_payload = [
                SystemMessage(content=system_prompt),
                HumanMessage(
                    content=(
                        f"Original Goal: {goal}\n"
                        f"Completed Steps: {completed}\n"
                        f"Execution History Logs:\n{history_text}"
                    )
                ),
            ]

            decision = structured_model.invoke(messages_payload)
            logger.info(f"Supervisor LLM decision: {decision}")

            if decision.next_action == "finalize":
                run_id = uuid.UUID(run_id_str)
                await WorkflowRuntimeEngine.complete_workflow(run_id)
                messages.append(
                    {
                        "role": "assistant",
                        "content": f"Supervisor decided to finalize. Reasoning: {decision.reasoning}",
                    }
                )
                return {
                    "messages": messages,
                    "next_node": "finalize",
                    "context_data": {"workflow_instance_id": run_id_str},
                }
            else:
                messages.append(
                    {
                        "role": "system",
                        "content": f"Planner decided to run action: {decision.next_action}. Reasoning: {decision.reasoning}",
                    }
                )
                return {
                    "loop_count": loop_count,
                    "accumulated_cost": accumulated_cost + 0.05,
                    "current_plan": decision.current_plan,
                    "messages": messages,
                    "next_node": "evaluate_policy",
                    "context_data": {
                        "workflow_instance_id": run_id_str,
                        "next_action": decision.next_action,
                        "action_inputs": decision.action_inputs,
                    },
                }
        except Exception as e:
            logger.error(
                f"Error in Supervisor LLM reasoning (falling back to mock): {str(e)}"
            )

    # Fallback / Mock Planning transitions
    if not completed:
        next_action = "search_web"
        action_inputs = {"query": goal}
        messages.append(
            {
                "role": "system",
                "content": f"Planner (Mock) decided to run action: {next_action}",
            }
        )
        return {
            "loop_count": loop_count,
            "accumulated_cost": accumulated_cost + 0.04,
            "current_plan": ["Run research query"],
            "messages": messages,
            "next_node": "evaluate_policy",
            "context_data": {
                "workflow_instance_id": run_id_str,
                "next_action": next_action,
                "action_inputs": action_inputs,
            },
        }

    elif len(completed) == 1:
        next_action = "sync_lead"
        action_inputs = {
            "action": "sync_lead",
            "email": "lead@company.com",
            "first_name": "Alice",
            "last_name": "Smith",
            "company": "Enterprise Inc",
        }
        messages.append(
            {
                "role": "system",
                "content": f"Planner (Mock) decided to run action: {next_action}",
            }
        )
        return {
            "loop_count": loop_count,
            "accumulated_cost": accumulated_cost + 0.06,
            "current_plan": ["Sync prospect to HubSpot"],
            "messages": messages,
            "next_node": "evaluate_policy",
            "context_data": {
                "workflow_instance_id": run_id_str,
                "next_action": next_action,
                "action_inputs": action_inputs,
            },
        }

    elif len(completed) == 2:
        next_action = "send_email"
        action_inputs = {
            "recipient": "client@example.com",
            "subject": "Qualification Setup",
            "body": "Your prospect files have been qualified and synchronized.",
        }
        messages.append(
            {
                "role": "system",
                "content": f"Planner (Mock) decided to run action: {next_action}",
            }
        )
        return {
            "loop_count": loop_count,
            "accumulated_cost": accumulated_cost + 0.02,
            "current_plan": ["Send confirmation email"],
            "messages": messages,
            "next_node": "evaluate_policy",
            "context_data": {
                "workflow_instance_id": run_id_str,
                "next_action": next_action,
                "action_inputs": action_inputs,
            },
        }

    # Workflow completed successfully
    run_id = uuid.UUID(run_id_str)
    await WorkflowRuntimeEngine.complete_workflow(run_id)

    messages.append({"role": "assistant", "content": "Goal accomplished successfully."})
    return {
        "messages": messages,
        "next_node": "finalize",
        "context_data": {"workflow_instance_id": run_id_str},
    }


def capability_router(state: AgentState) -> str:
    """
    Routes execution dynamically by evaluating Policy Engine decisions.
    """
    next_node = state.get("next_node")
    if next_node == "finalize":
        return "finalize"
    if next_node == "human_approval_gate":
        return "human_approval_gate"

    context_data = state.get("context_data", {})
    action = context_data.get("next_action")
    employee_id = state["employee_id"]
    org_id = state["organization_id"]

    # 1. Build Policy Context
    policy_ctx = PolicyContext(
        organization_id=org_id,
        employee_id=employee_id,
        action=action,
        user_role=state.get("context_data", {}).get("user_role", "member"),
    )

    # 2. Evaluate Policy
    decision_res = PolicyEngine.evaluate(policy_ctx)
    decision = decision_res["decision"]

    # Save policy decisions event
    EventBus.publish(
        "PolicyDecisionLogged",
        {
            "workflow_instance_id": context_data.get("workflow_instance_id"),
            "action": action,
            "decision": decision,
            "reason": decision_res["reason"],
        },
    )

    if decision == PolicyDecision.REJECT:
        raise PermissionError(
            f"Policy Engine rejected execution of '{action}': {decision_res['reason']}"
        )

    if decision == PolicyDecision.REQUIRE_APPROVAL and not state.get("human_response"):
        return "human_approval_gate"

    return "capability_executor"


async def human_approval_gate(state: AgentState) -> Dict[str, Any]:
    """
    Suspends execution thread and registers pause inside WorkflowRuntime (Asynchronous).
    """
    context_data = state.get("context_data", {})
    run_id = uuid.UUID(context_data["workflow_instance_id"])
    action = context_data["next_action"]
    inputs = context_data["action_inputs"]

    # Register Pause status in Runtime Engine
    checkpoint_id = uuid.uuid4()
    await WorkflowRuntimeEngine.pause_for_approval(
        run_id, checkpoint_id, action, inputs
    )

    return {
        "approval_required": True,
        "approval_payload": {"action": action, "inputs": inputs},
    }


async def capability_executor_node(state: AgentState) -> Dict[str, Any]:
    """
    Executes resolved capability through Workflow Runtime retry loops,
    logging durable checkpoints (Asynchronous).
    """
    completed = state.get("completed_steps", [])
    messages = state.get("messages", [])
    context_data = state.get("context_data", {})

    run_id = uuid.UUID(context_data["workflow_instance_id"])
    action = context_data["next_action"]
    inputs = context_data["action_inputs"]

    capability = CapabilityRegistry.resolve_by_action(action)
    if not capability:
        raise ValueError(f"No registered capability can execute action '{action}'")

    # Pre-execution Checkpoint
    await WorkflowRuntimeEngine.save_checkpoint(
        run_id=run_id,
        capability_id=capability.definition.id,
        inputs=inputs,
        outputs=None,
        state_snapshot=state,
    )

    # Execute through Runtime exponential retry loop
    EventBus.publish(
        "CapabilityStarted",
        {
            "workflow_instance_id": str(run_id),
            "capability_id": capability.definition.id,
            "action": action,
        },
    )

    async def run_op():
        if asyncio.iscoroutinefunction(capability.execute):
            return await capability.execute(inputs, context={"credentials": {}})
        return capability.execute(inputs, context={"credentials": {}})

    res = await WorkflowRuntimeEngine.execute_with_retry(run_id, run_op)

    # Post-execution Checkpoint
    await WorkflowRuntimeEngine.save_checkpoint(
        run_id=run_id,
        capability_id=capability.definition.id,
        inputs=inputs,
        outputs=res,
        state_snapshot=state,
    )

    EventBus.publish(
        "CapabilityCompleted",
        {
            "workflow_instance_id": str(run_id),
            "capability_id": capability.definition.id,
            "success": res["success"],
            "error": res["error"],
        },
    )

    if not res["success"]:
        raise RuntimeError(f"Capability execution failed: {res['error']}")

    completed.append(f"Completed action '{action}'")
    messages.append(
        {
            "role": "system",
            "content": f"Capability {capability.definition.id} output: {res['output']}",
        }
    )

    return {
        "completed_steps": completed,
        "messages": messages,
        "approval_required": False,
        "human_response": None,
        "next_node": "planner",
    }


# Assemble StateGraph
workflow = StateGraph(AgentState)

workflow.add_node("planner", planner_node)
workflow.add_node("human_approval_gate", human_approval_gate)
workflow.add_node("capability_executor", capability_executor_node)

workflow.set_entry_point("planner")

workflow.add_conditional_edges(
    "planner",
    capability_router,
    {
        "capability_executor": "capability_executor",
        "human_approval_gate": "human_approval_gate",
        "finalize": END,
    },
)

workflow.add_edge("capability_executor", "planner")
workflow.add_edge("human_approval_gate", END)

orchestrator_graph = workflow.compile()
