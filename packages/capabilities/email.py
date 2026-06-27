from pydantic import BaseModel, Field, EmailStr
from packages.capabilities.base import BaseCapability, CapabilityDefinition
from packages.capabilities.registry import CapabilityRegistry
from packages.skills.email import SendEmailSkill


class EmailInput(BaseModel):
    recipient: EmailStr = Field(description="Recipient email address")
    subject: str = Field(description="Subject line")
    body: str = Field(description="Email body text")


class EmailOutput(BaseModel):
    message_id: str = Field(description="Email message identifier")
    sent_status: bool = Field(description="Success confirmation status")


class EmailCapability(BaseCapability):
    def __init__(self):
        self.definition = CapabilityDefinition(
            id="email_v1",
            name="Email Communication Capability",
            description="Composes skills to validate inputs and deliver notifications.",
            supported_actions=["send_email", "draft_reply"],
            required_tools=["GmailTool"],
            required_permissions=["email:send"],
            input_schema=EmailInput,
            output_schema=EmailOutput,
            evaluation_metrics=["delivery_rate"],
        )

    def _execute(self, validated_inputs: EmailInput, context: dict = None) -> dict:
        # Composes SendEmailSkill
        skill = SendEmailSkill()
        result = skill.execute(
            {
                "recipient": validated_inputs.recipient,
                "subject": validated_inputs.subject,
                "body": validated_inputs.body,
            },
            credentials=context.get("credentials") if context else None,
        )

        if not result["sent"]:
            raise RuntimeError(f"Email sending skill failed: {result['log']}")

        return {"message_id": "msg-xyz-777", "sent_status": True}


# Register capability dynamically
CapabilityRegistry.register(EmailCapability())
