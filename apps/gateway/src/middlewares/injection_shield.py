import re
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response
import json


class PromptInjectionPIIShieldMiddleware(BaseHTTPMiddleware):
    """
    Middleware performing input validation checks for prompt injections
    and masking sensitive PII (e.g. credit card / SSN patterns) from outgoing response payloads.
    """

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        # Prompt Injection Shield
        if request.method in ["POST", "PUT", "PATCH"]:
            try:
                body = await request.body()
                if body:
                    body_str = body.decode("utf-8")

                    # Search for standard injection heuristics (e.g. "ignore previous instructions", "system override")
                    injection_patterns = [
                        r"(?i)ignore\s+(?:all\s+)?prior\s+instructions",
                        r"(?i)system\s+override",
                        r"(?i)you\s+are\s+now\s+a\s+developer",
                        r"(?i)bypass\s+security",
                    ]

                    for pattern in injection_patterns:
                        if re.search(pattern, body_str):
                            raise HTTPException(
                                status_code=400,
                                detail="Potential system instruction override detected. Request rejected.",
                            )
            except HTTPException as he:
                raise he
            except Exception:
                # Fallback if body decoding fails
                pass

        # Execute downstream pipeline
        response = await call_next(request)

        # In-line PII Masking for Response Streams / bodies (SSN and simple credit cards)
        if response.headers.get("content-type") == "application/json":
            try:
                # Capture body
                response_body = [section async for section in response.body_iterator]
                response.body_iterator = iterate_in_memory(response_body)

                full_body = b"".join(response_body).decode("utf-8")

                # Mask SSNs: XXX-XX-XXXX
                ssn_pattern = r"\b\d{3}-\d{2}-\d{4}\b"
                masked = re.sub(ssn_pattern, "[REDACTED_SSN]", full_body)

                # Mask credit cards: XXXX-XXXX-XXXX-XXXX
                cc_pattern = r"\b(?:\d{4}-){3}\d{4}\b"
                masked = re.sub(cc_pattern, "[REDACTED_CARD]", masked)

                response.headers["content-length"] = str(len(masked.encode("utf-8")))
                return Response(
                    content=masked,
                    status_code=response.status_code,
                    headers=dict(response.headers),
                    media_type=response.media_type,
                )
            except Exception:
                # If modification fails, return raw response
                pass

        return response


async def iterate_in_memory(body_list):
    for part in body_list:
        yield part
