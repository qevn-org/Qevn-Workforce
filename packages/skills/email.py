from pydantic import BaseModel, Field, EmailStr
from packages.skills.base import BaseSkill
from packages.tools.src.registry import ToolRegistry


class SendEmailInput(BaseModel):
    recipient: EmailStr = Field(description="Recipient email address")
    subject: str = Field(description="Subject line")
    body: str = Field(description="Body message text")


class SendEmailOutput(BaseModel):
    sent: bool = Field(description="Delivery confirmation status")
    log: str = Field(description="Execution result log summary")


class SendEmailSkill(BaseSkill):
    name = "SendEmailSkill"
    description = "Atomic skill to dispatch an email via Gmail API."
    input_schema = SendEmailInput
    output_schema = SendEmailOutput

    def _execute(
        self, validated_inputs: SendEmailInput, credentials: dict = None
    ) -> dict:
        # Load Tool integration
        gmail = ToolRegistry.get_tool(
            "GmailTool", credentials=credentials or {"token": "mock"}
        )
        res = gmail.run(
            {
                "recipient": validated_inputs.recipient,
                "subject": validated_inputs.subject,
                "body": validated_inputs.body,
            }
        )

        if res["status"] == "failed":
            return {"sent": False, "log": f"Failure: {res['error']}"}

        return {"sent": True, "log": f"Success: {res['result']}"}
