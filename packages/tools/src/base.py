import logging
import time
from abc import ABC, abstractmethod
from typing import Any, Dict, Type
from pydantic import BaseModel, ValidationError
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)

logger = logging.getLogger("QevnToolRegistry")


class ToolException(Exception):
    """Base exception for all execution failures inside tool integrations."""

    pass


class ToolRateLimitException(ToolException):
    """Raised when the external system rate limits the tool call."""

    pass


class ToolAuthException(ToolException):
    """Raised when authentication credentials are invalid or expired."""

    pass


class BaseTool(ABC):
    """
    Abstract Base Class for all integrations inside QEVN Workforce.
    Enforces authorization, argument validation, retries, rate limiting, and audit logging.
    """

    name: str
    description: str
    args_schema: Type[BaseModel]

    # Rate Limiting
    rate_limit_per_minute: int = 60
    _last_calls: list = []

    def __init__(self, credentials: Dict[str, Any] = None):
        self.credentials = credentials or {}

    def _check_rate_limit(self):
        """Enforces sliding-window rate limit checks."""
        now = time.time()
        # Clean older entries
        self._last_calls = [t for t in self._last_calls if now - t < 60]
        if len(self._last_calls) >= self.rate_limit_per_minute:
            raise ToolRateLimitException(
                f"Rate limit exceeded for tool {self.name}. Max {self.rate_limit_per_minute}/min."
            )
        self._last_calls.append(now)

    def _validate_auth(self):
        """Checks if auth parameters exist in credentials."""
        if not self.credentials:
            raise ToolAuthException(
                f"No authentication parameters provided for {self.name}."
            )

    def _validate_arguments(self, args: Dict[str, Any]) -> BaseModel:
        """Validates arguments against the args_schema."""
        try:
            return self.args_schema(**args)
        except ValidationError as e:
            raise ToolException(f"Invalid parameters for {self.name}: {str(e)}")

    @abstractmethod
    def _execute(self, validated_args: BaseModel) -> Any:
        """Integration execution logic, to be overridden by subclasses."""
        pass

    def run(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes the tool with built-in validation, audit logs, rate-limiters, and error routing.
        """
        logger.info(f"Tool {self.name} started execution with args: {args}")
        start_time = time.time()

        try:
            self._validate_auth()
            self._check_rate_limit()
            validated = self._validate_arguments(args)

            # Execute with tenacity retries
            result = self._run_with_retry(validated)

            duration = int((time.time() - start_time) * 1000)
            logger.info(f"Tool {self.name} completed successfully in {duration}ms")

            return {"status": "success", "result": result, "duration_ms": duration}

        except Exception as e:
            duration = int((time.time() - start_time) * 1000)
            logger.error(f"Tool {self.name} failed after {duration}ms: {str(e)}")
            return {"status": "failed", "error": str(e), "duration_ms": duration}

    @retry(
        retry=retry_if_exception_type((ToolRateLimitException, ConnectionError)),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        stop=stop_after_attempt(3),
        reraise=True,
    )
    def _run_with_retry(self, validated: BaseModel) -> Any:
        """Internal execution wrapper executing retry rules."""
        return self._execute(validated)
