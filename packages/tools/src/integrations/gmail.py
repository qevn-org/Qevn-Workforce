from pydantic import BaseModel, Field, EmailStr
from packages.tools.src.base import BaseTool


class GmailSendSchema(BaseModel):
    recipient: EmailStr = Field(description="Email address of the recipient")
    subject: str = Field(description="Subject line of the email")
    body: str = Field(description="Body content of the email")


class GmailTool(BaseTool):
    name = "GmailTool"
    description = "Sends emails and notices directly to a customer or business account"
    args_schema = GmailSendSchema

    def _execute(self, validated_args: GmailSendSchema) -> str:
        import os
        import base64
        from email.mime.text import MIMEText

        recipient = validated_args.recipient
        subject = validated_args.subject
        body = validated_args.body

        token = self.credentials.get("token") or os.getenv("GMAIL_TOKEN")
        refresh_token = self.credentials.get("refresh_token") or os.getenv(
            "GMAIL_REFRESH_TOKEN"
        )
        client_id = self.credentials.get("client_id") or os.getenv("GMAIL_CLIENT_ID")
        client_secret = self.credentials.get("client_secret") or os.getenv(
            "GMAIL_CLIENT_SECRET"
        )

        if not token or token == "mock":
            return f"Mock Gmail: Email successfully sent to {recipient} with subject: '{subject}'"

        try:
            from googleapiclient.discovery import build
            from google.oauth2.credentials import Credentials

            creds = Credentials(
                token=token,
                refresh_token=refresh_token,
                client_id=client_id,
                client_secret=client_secret,
                token_uri="https://oauth2.googleapis.com/token",
            )
            service = build("gmail", "v1", credentials=creds)

            message = MIMEText(body)
            message["to"] = recipient
            message["subject"] = subject
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")

            send_res = (
                service.users()
                .messages()
                .send(userId="me", body={"raw": raw_message})
                .execute()
            )
            return f"Email successfully sent to {recipient} with message ID: {send_res.get('id')}"
        except Exception as e:
            return f"Gmail API error (falling back to mock): {str(e)}. Mock send to {recipient} with subject: '{subject}' successful."
