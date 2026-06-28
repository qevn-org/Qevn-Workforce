import os
from dotenv import load_dotenv
from google_auth_oauthlib.flow import InstalledAppFlow

# Load environment variables
load_dotenv()

# We request permission to send emails and create calendar events
SCOPES = [
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/calendar.events",
]

client_id = os.getenv("GMAIL_CLIENT_ID")
client_secret = os.getenv("GMAIL_CLIENT_SECRET")

if not client_id or not client_secret:
    print(
        "ERROR: Please set GMAIL_CLIENT_ID and GMAIL_CLIENT_SECRET in your .env file first."
    )
    exit(1)

# Configure client info dynamically
client_config = {
    "installed": {
        "client_id": client_id,
        "client_secret": client_secret,
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "redirect_uris": ["http://localhost:8080/"],
    }
}

print("Starting Google Authentication Flow...")
print(
    "IMPORTANT: Make sure you have added 'http://localhost:8080/' as an 'Authorized redirect URI' in your Google Cloud Console under this Client ID."
)
print("Opening browser for authorization...\n")

try:
    flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
    # Start local server to receive redirection code
    creds = flow.run_local_server(port=8080, prompt="consent")

    print("\n==================================================")
    print("   GOOGLE OAUTH TOKENS GENERATED SUCCESSFULLY     ")
    print("==================================================")
    print(f"GMAIL_TOKEN={creds.token}")
    print(f"GMAIL_REFRESH_TOKEN={creds.refresh_token}")
    print("==================================================\n")

    # Append to .env file
    with open(".env", "a") as f:
        f.write(
            f"\n# --- GOOGLE OAUTH TOKENS ---\nGMAIL_TOKEN={creds.token}\nGMAIL_REFRESH_TOKEN={creds.refresh_token}\n"
        )

    print("Tokens appended successfully to your local .env file!")
    print(
        "Copy the values above and add them as environment variables on Railway to make the cloud agents live!"
    )

except Exception as e:
    print(f"ERROR: Authentication flow failed: {str(e)}")
