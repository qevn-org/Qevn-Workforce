import logging
from enum import Enum
from typing import Dict, Any, List, Optional
from pydantic import BaseModel


class PolicyDecision(str, Enum):
    ALLOW = "allow"
    REJECT = "reject"
    REQUIRE_APPROVAL = "require_approval"


class PolicyContext(BaseModel):
    organization_id: str
    employee_id: str
    user_role: str = "member"
    action: str  # e.g., 'send_email', 'sync_lead'
    budget_used: float = 0.0
    budget_limit: float = 10.0
    working_hour: int = 12  # Hour representation (0-23)
    working_days: List[int] = [1, 2, 3, 4, 5]  # Mon-Fri
    current_day: int = 1  # Monday


logger = logging.getLogger("PolicyEngine")


class PolicyEngine:
    """
    Unified Policy Engine.
    Intercepts proposed actions and evaluates security, permission scopes,
    budget constraints, and working-hours limits.
    """

    @classmethod
    def evaluate(cls, context: PolicyContext) -> Dict[str, Any]:
        logger.info(
            f"Evaluating action '{context.action}' for Employee {context.employee_id}..."
        )

        # 1. Check Permissions
        action_permissions = {
            "send_email": "email:send",
            "sync_lead": "crm:write",
            "search_web": "research:read",
        }

        required_perm = action_permissions.get(context.action)
        if required_perm and context.user_role == "restricted":
            logger.warning(
                f"Action '{context.action}' rejected due to insufficient role permissions."
            )
            return {
                "decision": PolicyDecision.REJECT,
                "reason": f"Role '{context.user_role}' lacks permission: {required_perm}",
            }

        # 2. Check Working Hours Constraints
        if context.current_day not in context.working_days:
            logger.warning("Action rejected: Out of office working days.")
            return {
                "decision": PolicyDecision.REJECT,
                "reason": "Execution attempted outside active working days schedule.",
            }

        # 3. Check Budgets Limits
        if context.budget_used >= context.budget_limit:
            logger.warning("Action rejected: Budget limit exceeded.")
            return {
                "decision": PolicyDecision.REJECT,
                "reason": f"Budget limit reached: {context.budget_used}/{context.budget_limit}",
            }

        # 4. Check Human Approval Requirements (Gated actions)
        gated_actions = ["send_email"]
        if context.action in gated_actions:
            logger.info(f"Action '{context.action}' requires human confirmation.")
            return {
                "decision": PolicyDecision.REQUIRE_APPROVAL,
                "reason": f"Action '{context.action}' is flagged as high-risk.",
            }

        logger.info(f"Action '{context.action}' successfully allowed.")
        return {
            "decision": PolicyDecision.ALLOW,
            "reason": "Passed all baseline permission checks.",
        }
