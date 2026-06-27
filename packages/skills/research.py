from pydantic import BaseModel, Field
from packages.skills.base import BaseSkill


class SearchWebInput(BaseModel):
    query: str = Field(description="Search terms query")


class SearchWebOutput(BaseModel):
    results: str = Field(description="Raw search matches summary text")


class SearchWebSkill(BaseSkill):
    name = "SearchWebSkill"
    description = "Atomic skill to search public websites."
    input_schema = SearchWebInput
    output_schema = SearchWebOutput

    def _execute(
        self, validated_inputs: SearchWebInput, credentials: dict = None
    ) -> dict:
        query = validated_inputs.query
        # Simulating external search API call
        return {
            "results": f"Found 3 prospect articles matching '{query}'. General sentiment is highly positive."
        }
