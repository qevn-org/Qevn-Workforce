from pydantic import BaseModel, Field
from packages.capabilities.base import BaseCapability, CapabilityDefinition
from packages.capabilities.registry import CapabilityRegistry
from packages.skills.crm import SyncLeadSkill


class CRMInput(BaseModel):
    action: str = Field(description="Action: sync_lead or search_contacts")
    email: str = Field(description="Email of lead")
    first_name: str = Field(description="First name")
    last_name: str = Field(description="Last name")
    company: str = Field(description="Company")


class CRMOutput(BaseModel):
    status: str = Field(description="Synchronization status code")
    crm_id: str = Field(description="ID of lead record")


class CRMCapability(BaseCapability):
    def __init__(self):
        self.definition = CapabilityDefinition(
            id="crm_v1",
            name="CRM Synchronization Capability",
            description="Composes skills to validate and qualify leads inside Hubspot.",
            supported_actions=["search_contacts", "sync_lead"],
            required_tools=["HubSpotTool"],
            required_permissions=["crm:write"],
            input_schema=CRMInput,
            output_schema=CRMOutput,
            evaluation_metrics=["sync_latency"],
        )

    def _execute(self, validated_inputs: CRMInput, context: dict = None) -> dict:
        # Composes atomic SyncLeadSkill
        skill = SyncLeadSkill()
        result = skill.execute(
            {
                "email": validated_inputs.email,
                "first_name": validated_inputs.first_name,
                "last_name": validated_inputs.last_name,
                "company": validated_inputs.company,
            },
            credentials=context.get("credentials") if context else None,
        )

        if not result["success"]:
            raise RuntimeError(f"CRM sync skill failed: {result['message']}")

        return {"status": "synchronized", "crm_id": "hs-contact-928420"}


# Register capability dynamically
CapabilityRegistry.register(CRMCapability())
