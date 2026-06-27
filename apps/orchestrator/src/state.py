from typing import TypedDict, List, Dict, Any, Optional

class AgentState(TypedDict):
    """
    Defines the structural keys tracked inside the LangGraph state machine.
    """
    # Identifiers
    organization_id: str
    employee_id: str
    conversation_id: str
    
    # Goal planning
    original_goal: str
    current_plan: List[str]
    completed_steps: List[str]
    
    # Message logs & intermediate responses
    messages: List[Dict[str, Any]]
    next_node: str
    context_data: Dict[str, Any]
    
    # Human in the Loop validation flags
    approval_required: bool
    approval_payload: Optional[Dict[str, Any]]
    human_response: Optional[str]
    
    # Loop boundaries & budget controls (Phase 5)
    loop_count: int
    max_loops: int
    cost_budget: float
    accumulated_cost: float
