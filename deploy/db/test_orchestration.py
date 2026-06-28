import asyncio
import os
import sys
from dotenv import load_dotenv

# Load local environment
load_dotenv()

# Add root directory to python path
sys.path.append(os.getcwd())

from apps.orchestrator.src.graphs.supervisor import orchestrator_graph


async def main():
    initial_state = {
        "organization_id": "00000000-0000-0000-0000-000000000000",
        "employee_id": "e3e35e9c-f1b6-4861-9ff2-c45fb86a177d",
        "conversation_id": "default-session",
        "original_goal": "Draft a personalized sales outreach email to invite Dhruv (dhruv@qevn.in) from company Qevn to schedule a discovery call, upsert their details to HubSpot, and dispatch the email via Gmail.",
        "current_plan": [],
        "completed_steps": [],
        "messages": [
            {
                "role": "user",
                "content": "Draft a personalized sales outreach email to invite Dhruv (dhruv@qevn.in) from company Qevn to schedule a discovery call, upsert their details to HubSpot, and dispatch the email via Gmail.",
            }
        ],
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

    print("Invoking LangGraph orchestrator graph locally with current .env keys...")
    try:
        result = await orchestrator_graph.ainvoke(initial_state)
        print("\n=== EXECUTION SUCCESSFUL ===")
        print("Final State Keys:", list(result.keys()))
        print("Messages Count:", len(result.get("messages", [])))
    except Exception as e:
        print("\n=== CRITICAL EXECUTION ERROR ===")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
