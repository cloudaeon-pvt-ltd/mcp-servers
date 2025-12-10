import os
import requests
import msal
from mcp.server.fastmcp import FastMCP
import base64
import mimetypes

from dotenv import load_dotenv
import re
load_dotenv()

# Initialize FastMCP server
mcp = FastMCP("cloudaeon-outlook-mcp", host="0.0.0.0", port=8011)

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
async def send_email(email_recipient: str, email_subject: str, email_body: str, attachment_file_path: str = "") -> str:
    """Send an email using the Outlook API.

    Args:
        email_recipient: The recipient's email address.
        email_subject: The subject of the email.
        email_body: The body content of the email.
        attachment_file_path: Path to the attachment file (optional).
    """
    headers = {
        "Authorization": f"Bearer {get_access_token()}",
        "Content-Type": "application/json"
    }
    
    # Initialize email data structure
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
    
    # Handle attachment if provided
    if attachment_file_path and attachment_file_path.strip():
        # Clean attachment_file_path to remove excessive backslashes and normalize
        cleaned_path = attachment_file_path.strip().strip('\'"')

        # Normalize the path (collapses redundant separators, up-level references)
        cleaned_path = os.path.normpath(cleaned_path)

        # Use the cleaned path for opening the file below
        attachment_file_path = cleaned_path
            
        # Read the file and encode it as base64
        with open(attachment_file_path, "rb") as f:
            file_bytes = f.read()
        encoded_bytes = base64.b64encode(file_bytes).decode("utf-8")
        
        # Determine the MIME type of the file
        mime_type, _ = mimetypes.guess_type(attachment_file_path)
        if mime_type is None:
            mime_type = "application/octet-stream"  # Default for unknown file types

        # Add attachment to email data
        email_data["message"]["attachments"] = [
            {
                "@odata.type": "#microsoft.graph.fileAttachment",
                "name": os.path.basename(attachment_file_path),
                "contentType": mime_type,
                "contentBytes": encoded_bytes
            }
        ]

    response = requests.post(EMAIL_API_ENDPOINT, headers=headers, json=email_data)
    if response.status_code == 202:
        return f"Email sent successfully to {email_recipient}."
    else:
        return f"Failed to send email: {response.content}"

def main():
    # Initialize and run the server
    mcp.run(transport='streamable-http')    

if __name__ == "__main__":
    main()