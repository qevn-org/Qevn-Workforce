from pydantic import BaseModel, Field
from packages.capabilities.base import BaseCapability, CapabilityDefinition
from packages.capabilities.registry import CapabilityRegistry
from packages.skills.research import SearchWebSkill

class ResearchInput(BaseModel):
    query: str = Field(description="Search term or topic to research")
    depth: str = Field(default="shallow", description="Depth of search")

class ResearchOutput(BaseModel):
    summary: str = Field(description="Summarized findings of the research task")

class ResearchCapability(BaseCapability):
    def __init__(self):
        self.definition = CapabilityDefinition(
            id="research_v1",
            name="Research Capability",
            description="Composes skills to run search queries and analyze documents.",
            supported_actions=["search_web", "summarize_document"],
            required_tools=[],
            required_permissions=["research:read"],
            input_schema=ResearchInput,
            output_schema=ResearchOutput,
            evaluation_metrics=["completeness"]
        )

    def _execute(self, validated_inputs: ResearchInput, context: dict = None) -> dict:
        # Composes atomic SearchWebSkill
        skill = SearchWebSkill()
        result = skill.execute({"query": validated_inputs.query})
        
        return {"summary": result["results"]}

# Register capability dynamically
CapabilityRegistry.register(ResearchCapability())
