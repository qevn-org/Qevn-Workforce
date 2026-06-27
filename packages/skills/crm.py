from pydantic import BaseModel, Field
from packages.skills.base import BaseSkill
from packages.tools.src.registry import ToolRegistry

class SyncLeadInput(BaseModel):
    email: str = Field(description="Lead contact email")
    first_name: str = Field(description="First name")
    last_name: str = Field(description="Last name")
    company: str = Field(description="Company")

class SyncLeadOutput(BaseModel):
    success: bool
    message: str

class SyncLeadSkill(BaseSkill):
    name = "SyncLeadSkill"
    description = "Atomic skill to update lead record inside CRM database."
    input_schema = SyncLeadInput
    output_schema = SyncLeadOutput

    def _execute(self, validated_inputs: SyncLeadInput, credentials: dict = None) -> dict:
        hubspot = ToolRegistry.get_tool("HubSpotTool", credentials=credentials or {"token": "mock"})
        res = hubspot.run({
            "email": validated_inputs.email,
            "first_name": validated_inputs.first_name,
            "last_name": validated_inputs.last_name,
            "company": validated_inputs.company
        })
        
        if res["status"] == "failed":
            return {"success": False, "message": f"HubSpot sync failed: {res['error']}"}
            
        return {"success": True, "message": res["result"]}
