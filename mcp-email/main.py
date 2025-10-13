import os
import requests
import msal
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("cloudaeon-outlook-mcp")

# Constants
SENDER_EMAIL_ID = os.environ.get("SENDER_EMAIL_ID")
TENANT_ID = os.environ.get("TENANT_ID")
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")

GET_TOKEN_SCOPE = "https://graph.microsoft.com/.default"
EMAIL_API_ENDPOINT = f"https://graph.microsoft.com/v1.0/users/{SENDER_EMAIL_ID}/sendMail"

def get_access_token() -> str:
    """Fetch a new access token using MSAL."""
    get_token_app = msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{TENANT_ID}",
        client_credential=CLIENT_SECRET
    )
    token_response = get_token_app.acquire_token_for_client(scopes=[GET_TOKEN_SCOPE])
    if "access_token" in token_response:
        return token_response["access_token"]
    else:
        raise Exception("Could not obtain access token")

@mcp.tool()
async def send_email(email_recipient: str, email_subject: str, email_body: str) -> str:
    """Send an email using the Outlook API.

    Args:
        email_recipient: The recipient's email address.
        email_subject: The subject of the email.
        email_body: The body content of the email.
    """
    headers = {
        "Authorization": f"Bearer {get_access_token()}",
        "Content-Type": "application/json"
    }
    email_data = {
        "message": {
            "subject": email_subject,
            "body": {
                "contentType": "Text",
                "content": email_body
            },
            "toRecipients": [
                {
                    "emailAddress": {
                        "address": email_recipient
                    }
                }
            ]
        },
        "saveToSentItems": "true"
    }

    response = requests.post(EMAIL_API_ENDPOINT, headers=headers, json=email_data)
    if response.status_code == 202:
        return f"Email sent successfully to {email_recipient}."
    else:
        return f"Failed to send email: {response.content}"

def main():
    # Initialize and run the server
    mcp.run(transport='stdio')    

if __name__ == "__main__":
    main()