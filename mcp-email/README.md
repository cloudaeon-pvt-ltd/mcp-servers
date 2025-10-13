# MCP Email Server

A Model Context Protocol (MCP) server that enables sending emails through Microsoft Outlook/Office 365 using the Microsoft Graph API.

## Overview

This MCP server provides a simple interface for sending emails using Microsoft's Graph API with Azure AD authentication. It's designed to work with any MCP-compatible client and uses service principal (client credentials) authentication for secure, automated email sending.

## Features

- ✉️ Send emails via Microsoft Graph API
- 🔐 Secure authentication using Azure AD service principal
- 📝 Support for text-based email content
- 💾 Automatic saving to sent items
- 🚀 Built with FastMCP for easy integration

## Prerequisites

Before using this MCP server, you need:

1. **Microsoft 365/Azure AD tenant**
2. **Azure App Registration** with appropriate permissions
3. **Python 3.12+**

## Azure Setup

### 1. Create an App Registration

1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to **Azure Active Directory** > **App registrations**
3. Click **New registration**
4. Fill in the details:
   - Name: `MCP Email Server`
   - Supported account types: Choose based on your needs
   - Redirect URI: Not required for this application

### 2. Configure API Permissions

1. In your app registration, go to **API permissions**
2. Click **Add a permission**
3. Select **Microsoft Graph**
4. Choose **Application permissions**
5. Add the following permissions:
   - `Mail.Send` - Send mail as any user
6. Click **Grant admin consent** for your tenant

### 3. Create Client Secret

1. Go to **Certificates & secrets**
2. Click **New client secret**
3. Add a description and set expiration
4. Copy the **Value** (this is your CLIENT_SECRET)

### 4. Get Required IDs

- **Tenant ID**: Found in Azure AD overview page
- **Client ID**: Found in your app registration overview page
- **Sender Email ID**: The email address that will send the emails

## Installation

### Clone and Install Dependencies

```bash
git clone <repository-url>
cd mcp-email
pip install -e .
```

### Environment Variables

Create a `.env` file or set the following environment variables:

```bash
SENDER_EMAIL_ID=sender@yourdomain.com
TENANT_ID=your-tenant-id
CLIENT_ID=your-client-id
CLIENT_SECRET=your-client-secret
```

**Security Note**: Never commit secrets to version control. Use environment variables or secure secret management.

## Usage

### Running the Server

```bash
python main.py
```

The server runs using stdio transport, making it compatible with MCP clients.

### Available Tools

#### `send_email`

Sends an email using the configured sender account.

**Parameters:**
- `email_recipient` (string): Recipient's email address
- `email_subject` (string): Email subject line  
- `email_body` (string): Email body content (plain text)

**Returns:**
- Success message if email is sent (HTTP 202)
- Error message if sending fails

**Example:**
```python
# This would be called by an MCP client
await send_email(
    email_recipient="recipient@example.com",
    email_subject="Hello from MCP",
    email_body="This email was sent via the MCP Email Server!"
)
```

## Configuration with MCP Clients

### Claude Desktop

Add this to your Claude Desktop configuration:

```json
{
  "mcpServers": {
    "email": {
      "command": "python",
      "args": ["path/to/mcp-email/main.py"],
      "env": {
        "SENDER_EMAIL_ID": "sender@yourdomain.com",
        "TENANT_ID": "your-tenant-id", 
        "CLIENT_ID": "your-client-id",
        "CLIENT_SECRET": "your-client-secret"
      }
    }
  }
}
```

### Other MCP Clients

The server uses stdio transport and follows MCP protocol standards, making it compatible with any MCP client.

## Authentication Flow

1. Server loads credentials from environment variables
2. Uses MSAL (Microsoft Authentication Library) to authenticate with Azure AD
3. Obtains access token using client credentials flow
4. Uses token to authenticate with Microsoft Graph API
5. Sends email via Graph API endpoint

## Error Handling

The server includes basic error handling for:
- Missing environment variables
- Authentication failures
- API request failures
- Network connectivity issues

Check the console output for detailed error messages.

## Security Considerations

- **Principle of Least Privilege**: Grant only necessary permissions
- **Secret Management**: Use secure methods to store CLIENT_SECRET
- **Token Refresh**: Tokens are obtained fresh for each request
- **Audit Logging**: Monitor sent emails through Microsoft 365 admin center

## Troubleshooting

### Common Issues

1. **"Could not obtain access token"**
   - Verify environment variables are set correctly
   - Check if client secret has expired
   - Ensure app has proper permissions and admin consent

2. **"Failed to send email"**
   - Verify sender email address exists in your tenant
   - Check if Mail.Send permission is granted
   - Ensure recipient email address is valid

3. **Permission Errors**
   - Verify admin consent was granted for the application
   - Check if the sender account has necessary mailbox permissions

### Debug Mode

To enable more detailed logging, you can modify the code to include debug information:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Dependencies

- `mcp>=1.17.0` - Model Context Protocol library
- `msal>=1.34.0` - Microsoft Authentication Library
- `requests` - HTTP requests (included with msal)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

[Add your license information here]

## Support

For issues and questions:
- Check the troubleshooting section above
- Review Microsoft Graph API documentation
- Open an issue in this repository

---

**Note**: This server uses application permissions and can send emails on behalf of any user in the tenant. Use responsibly and in accordance with your organization's policies.