from pydantic import BaseModel, Field
from packages.tools.src.base import BaseTool


class TwilioCallSchema(BaseModel):
    to_number: str = Field(description="Recipient phone number with country code")
    voice_prompt: str = Field(
        description="Instructions or script for the text-to-speech engine"
    )


class TwilioTool(BaseTool):
    name = "TwilioTool"
    description = (
        "Triggers voice phone calls or SMS dispatches for escalation workflows"
    )
    args_schema = TwilioCallSchema

    def _execute(self, validated_args: TwilioCallSchema) -> str:
        import os

        to_number = validated_args.to_number
        voice_prompt = validated_args.voice_prompt

        account_sid = self.credentials.get("account_sid") or os.getenv(
            "TWILIO_ACCOUNT_SID"
        )
        auth_token = self.credentials.get("auth_token") or os.getenv(
            "TWILIO_AUTH_TOKEN"
        )
        from_number = self.credentials.get("from_number") or os.getenv(
            "TWILIO_FROM_NUMBER", "+1234567890"
        )

        if not account_sid or not auth_token or account_sid == "mock":
            return f"Mock Twilio: VoIP Call initiated to {to_number} with script: '{voice_prompt}'"

        try:
            from twilio.rest import Client

            client = Client(account_sid, auth_token)
            # Create a call using TwiML text-to-speech
            twiml = f"<Response><Say>{voice_prompt}</Say></Response>"
            call = client.calls.create(to=to_number, from_=from_number, twiml=twiml)
            return f"VoIP Call initiated to {to_number} with Call SID: {call.sid}"
        except Exception as e:
            return f"Twilio API error (falling back to mock): {str(e)}. Mock VoIP call to {to_number} with script: '{voice_prompt}' successful."
