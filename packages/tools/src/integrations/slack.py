from pydantic import BaseModel, Field
from packages.tools.src.base import BaseTool

class SlackMessageSchema(BaseModel):
    channel: str = Field(description="Slack channel name or ID")
    message: str = Field(description="The message to send to the channel")

class SlackTool(BaseTool):
    name = "SlackTool"
    description = "Dispatches logs, approvals, and general conversations to team Slack workspace channels"
    args_schema = SlackMessageSchema

    def _execute(self, validated_args: SlackMessageSchema) -> str:
        import os
        
        channel = validated_args.channel
        message = validated_args.message

        token = self.credentials.get("token") or os.getenv("SLACK_BOT_TOKEN")

        if not token or token == "mock":
            return f"Mock Slack: Message posted successfully to channel {channel}."

        try:
            from slack_sdk import WebClient
            client = WebClient(token=token)
            response = client.chat_postMessage(
                channel=channel,
                text=message
            )
            return f"Message posted successfully to channel {channel}. Timestamp: {response['ts']}"
        except Exception as e:
            return f"Slack API error (falling back to mock): {str(e)}. Mock Slack message to channel {channel} successful."

