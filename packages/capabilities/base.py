import logging
from abc import ABC, abstractmethod
from typing import Any, Dict
from pydantic import BaseModel, ValidationError


class CapabilityDefinition(BaseModel):
    id: str
    name: str
    description: str
    version: str = "1.0.0"
    supported_actions: list[str]
    required_tools: list[str]
    required_permissions: list[str]
    input_schema: Any
    output_schema: Any
    retry_policy: Dict[str, Any] = {"max_attempts": 3, "backoff": "exponential"}
    timeout_seconds: int = 120
    evaluation_metrics: list[str] = []


logger = logging.getLogger("CapabilityBase")


class BaseCapability(ABC):
    """
    Base Capability Interface.
    Composes prompts, tools, and execution policies.
    """

    definition: CapabilityDefinition

    def validate_inputs(self, inputs: Dict[str, Any]) -> BaseModel:
        """Validates input payload against the capability input schema."""
        try:
            return self.definition.input_schema(**inputs)
        except ValidationError as e:
            raise ValueError(
                f"Input validation failed for capability {self.definition.name}: {str(e)}"
            )

    @abstractmethod
    def _execute(
        self, validated_inputs: BaseModel, context: Dict[str, Any] = None
    ) -> Any:
        """Core execution logic defined by each capability module."""
        pass

    def execute(
        self, inputs: Dict[str, Any], context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Public execution wrapper with validation, logging, and metrics hooks.
        """
        logger.info(
            f"Capability {self.definition.name} execution started with inputs: {inputs}"
        )
        try:
            validated = self.validate_inputs(inputs)
            result = self._execute(validated, context)

            # Post-execution validation
            output_model = (
                self.definition.output_schema(**result)
                if isinstance(result, dict)
                else result
            )

            return {
                "success": True,
                "output": (
                    output_model.model_dump()
                    if isinstance(output_model, BaseModel)
                    else output_model
                ),
                "error": None,
            }
        except Exception as e:
            logger.error(
                f"Capability {self.definition.name} execution failed: {str(e)}"
            )
            return {"success": False, "output": None, "error": str(e)}
