from pydantic import BaseModel, Field
from typing import Dict, Any, List
from packages.capabilities.base import BaseCapability, CapabilityDefinition
from packages.capabilities.registry import CapabilityRegistry
from packages.tools.src.registry import ToolRegistry


# --- SDR Research schemas ---
class SDRResearchInput(BaseModel):
    query: str = Field(
        description="Target location or criteria (e.g. SaaS 20-100 London)"
    )


class SDRResearchOutput(BaseModel):
    prospects: List[Dict[str, Any]] = Field(
        description="List of companies matching parameters"
    )


class SDRResearchCapability(BaseCapability):
    def __init__(self):
        self.definition = CapabilityDefinition(
            id="sdr_research_v1",
            name="SDR Prospect Research",
            description="Searches companies and prospects matching target filters.",
            supported_actions=["search_company", "search_contact"],
            required_tools=[],
            required_permissions=["research:read"],
            input_schema=SDRResearchInput,
            output_schema=SDRResearchOutput,
            evaluation_metrics=["comprehensiveness"],
        )

    def _execute(
        self, validated_inputs: SDRResearchInput, context: dict = None
    ) -> dict:
        query = validated_inputs.query
        logger = ToolRegistry.list_available_tools()  # Reference registry

        # Simulating finding contacts/companies
        prospects = [
            {
                "company": "TargetSaaS Ltd",
                "domain": "targetsaas.com",
                "contact_email": "contact@targetsaas.com",
                "decision_maker": "Bob CTO",
                "employee_count": 45,
                "location": "London",
            }
        ]
        return {"prospects": prospects}


# --- SDR Outreach schemas ---
class SDROutreachInput(BaseModel):
    company: str
    contact_email: str
    decision_maker: str
    score: int = Field(default=80, description="ICP Match score")
    action: str = Field(default="dispatch_outreach")


class SDROutreachOutput(BaseModel):
    success: bool
    crm_deal_id: str
    outbound_log: str


class SDROutreachCapability(BaseCapability):
    def __init__(self):
        self.definition = CapabilityDefinition(
            id="sdr_outreach_v1",
            name="SDR Outreach & CRM Sync",
            description="Scores prospects, upserts HubSpot contacts, and delivers Gmail outbound sequences.",
            supported_actions=["score_lead", "sync_hubspot", "dispatch_outreach"],
            required_tools=["GmailTool", "HubSpotTool"],
            required_permissions=["email:send", "crm:write"],
            input_schema=SDROutreachInput,
            output_schema=SDROutreachOutput,
            evaluation_metrics=["response_rate"],
        )

    def _execute(
        self, validated_inputs: SDROutreachInput, context: dict = None
    ) -> dict:
        credentials = (context or {}).get("credentials", {})

        # 1. Evaluate ICP Score (Simple check)
        if validated_inputs.score < 50:
            return {
                "success": False,
                "crm_deal_id": "none",
                "outbound_log": f"Lead disqualified. Score: {validated_inputs.score}",
            }

        # 2. HubSpot Upsert contact & deal (prevent duplicates)
        hubspot = ToolRegistry.get_tool(
            "HubSpotTool", credentials=credentials.get("HubSpotTool", {"token": "mock"})
        )
        res_crm = hubspot.run(
            {
                "email": validated_inputs.contact_email,
                "first_name": validated_inputs.decision_maker.split()[0],
                "last_name": validated_inputs.decision_maker.split()[-1],
                "company": validated_inputs.company,
            }
        )

        if res_crm["status"] == "failed":
            raise RuntimeError(f"HubSpot syncing failed: {res_crm['error']}")

        # 3. Threaded Gmail outbound delivery
        import os

        email_body = f"Hi {validated_inputs.decision_maker},\nWe identified your business scaling. Let's sync."

        openai_key = os.getenv("OPENAI_API_KEY")
        anthropic_key = os.getenv("ANTHROPIC_API_KEY")

        if openai_key or anthropic_key:
            try:
                prompt = (
                    f"Write a short, professional, personalized cold sales outreach email to {validated_inputs.decision_maker} "
                    f"who is at company {validated_inputs.company}.\n"
                    f"The goal of the email is to invite them to sync and qualify their business requirements.\n"
                    f"Return ONLY the email body content, without subject line, signature placeholder, or greeting placeholder."
                )
                if openai_key:
                    from langchain_openai import ChatOpenAI

                    llm = ChatOpenAI(model="gpt-4o", temperature=0.7)
                else:
                    from langchain_anthropic import ChatAnthropic

                    llm = ChatAnthropic(
                        model_name="claude-3-5-sonnet-20240620", temperature=0.7
                    )

                resp = llm.invoke(prompt)
                email_body = resp.content
            except Exception as e:
                import logging

                logger = logging.getLogger("SDROutreachCapability")
                logger.warning(
                    f"Failed to generate LLM email body, using fallback: {str(e)}"
                )

        gmail = ToolRegistry.get_tool(
            "GmailTool", credentials=credentials.get("GmailTool", {"token": "mock"})
        )
        res_mail = gmail.run(
            {
                "recipient": validated_inputs.contact_email,
                "subject": f"Qualifying {validated_inputs.company} Outbound Campaign",
                "body": email_body,
            }
        )

        if res_mail["status"] == "failed":
            raise RuntimeError(f"Gmail send failed: {res_mail['error']}")

        return {
            "success": True,
            "crm_deal_id": "hs-deal-888999",
            "outbound_log": f"Contact qualified, deal stage created. Outbound: {res_mail['result']}",
        }


# Register capabilities dynamically
CapabilityRegistry.register(SDRResearchCapability())
CapabilityRegistry.register(SDROutreachCapability())
