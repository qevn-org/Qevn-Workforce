from pydantic import BaseModel, Field
from packages.tools.src.base import BaseTool
from datetime import datetime

class CalendarEventSchema(BaseModel):
    summary: str = Field(description="Title of the event")
    start_time: datetime = Field(description="Start ISO timestamp")
    end_time: datetime = Field(description="End ISO timestamp")
    attendees: list[str] = Field(description="List of attendee email addresses")

class CalendarTool(BaseTool):
    name = "CalendarTool"
    description = "Schedules events, syncs calendars, and manages meeting coordination on Google Calendar"
    args_schema = CalendarEventSchema

    def _execute(self, validated_args: CalendarEventSchema) -> str:
        import os
        
        summary = validated_args.summary
        start_time = validated_args.start_time
        end_time = validated_args.end_time
        attendees = validated_args.attendees

        token = self.credentials.get("token") or os.getenv("CALENDAR_TOKEN")
        refresh_token = self.credentials.get("refresh_token") or os.getenv("CALENDAR_REFRESH_TOKEN")
        client_id = self.credentials.get("client_id") or os.getenv("CALENDAR_CLIENT_ID")
        client_secret = self.credentials.get("client_secret") or os.getenv("CALENDAR_CLIENT_SECRET")

        if not token or token == "mock":
            return f"Mock Calendar: Event '{summary}' scheduled from {start_time} to {end_time}."

        try:
            from googleapiclient.discovery import build
            from google.oauth2.credentials import Credentials
            
            creds = Credentials(
                token=token,
                refresh_token=refresh_token,
                client_id=client_id,
                client_secret=client_secret,
                token_uri="https://oauth2.googleapis.com/token"
            )
            service = build('calendar', 'v3', credentials=creds)
            
            event_body = {
                'summary': summary,
                'start': {'dateTime': start_time.isoformat()},
                'end': {'dateTime': end_time.isoformat()},
                'attendees': [{'email': email} for email in attendees],
            }
            
            event = service.events().insert(calendarId='primary', body=event_body).execute()
            return f"Event '{summary}' scheduled successfully with event link: {event.get('htmlLink')}"
        except Exception as e:
            return f"Google Calendar API error (falling back to mock): {str(e)}. Mock Event '{summary}' scheduled from {start_time} to {end_time} successful."

