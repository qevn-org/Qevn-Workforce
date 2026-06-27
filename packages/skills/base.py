from abc import ABC, abstractmethod
from typing import Any, Dict
from pydantic import BaseModel, ValidationError

class BaseSkill(ABC):
    """
    Abstract Base Class for atomic skills.
    Skills contain no reasoning logic; they only execute a single focused integration task.
    """
    name: str
    description: str
    input_schema: type[BaseModel]
    output_schema: type[BaseModel]

    def validate_inputs(self, inputs: Dict[str, Any]) -> BaseModel:
        try:
            return self.input_schema(**inputs)
        except ValidationError as e:
            raise ValueError(f"Skill {self.name} input validation failed: {str(e)}")

    @abstractmethod
    def _execute(self, validated_inputs: BaseModel, credentials: Dict[str, Any] = None) -> Any:
        pass

    def execute(self, inputs: Dict[str, Any], credentials: Dict[str, Any] = None) -> Dict[str, Any]:
        validated = self.validate_inputs(inputs)
        result = self._execute(validated, credentials)
        
        output_model = self.output_schema(**result) if isinstance(result, dict) else result
        return output_model.model_dump() if isinstance(output_model, BaseModel) else output_model
