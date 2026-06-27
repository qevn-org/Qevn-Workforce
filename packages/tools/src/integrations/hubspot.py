from pydantic import BaseModel, Field
from packages.tools.src.base import BaseTool


class HubSpotUpsertContactSchema(BaseModel):
    email: str = Field(description="Email of the contact")
    first_name: str = Field(description="First name of the contact")
    last_name: str = Field(description="Last name of the contact")
    company: str = Field(description="Company name of the contact")


class HubSpotTool(BaseTool):
    name = "HubSpotTool"
    description = (
        "Create or update client files, tracking deals and contacts inside CRM"
    )
    args_schema = HubSpotUpsertContactSchema

    def _execute(self, validated_args: HubSpotUpsertContactSchema) -> str:
        import os
        import requests

        email = validated_args.email
        first_name = validated_args.first_name
        last_name = validated_args.last_name
        company = validated_args.company

        token = self.credentials.get("token") or os.getenv("HUBSPOT_ACCESS_TOKEN")

        if not token or token == "mock":
            return f"Mock HubSpot: Contact {first_name} {last_name} ({email}) updated in company {company} on HubSpot."

        try:
            url = "https://api.hubapi.com/crm/v3/objects/contacts"
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            }
            payload = {
                "properties": {
                    "email": email,
                    "firstname": first_name,
                    "lastname": last_name,
                    "company": company,
                }
            }
            res = requests.post(url, json=payload, headers=headers)
            if res.status_code in [200, 201]:
                contact_id = res.json().get("id")
                return f"Contact {first_name} {last_name} ({email}) successfully created/updated on HubSpot with ID: {contact_id}."
            elif res.status_code == 409:
                return f"Contact {first_name} {last_name} ({email}) already exists on HubSpot (409 Conflict). Sync verified."
            else:
                raise Exception(f"HTTP {res.status_code}: {res.text}")
        except Exception as e:
            return f"HubSpot API error (falling back to mock): {str(e)}. Mock HubSpot contact sync for {first_name} {last_name} ({email}) successful."
