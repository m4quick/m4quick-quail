#!/usr/bin/env python3
"""
Microsoft Graph API client for mmirzaie@msn.com
Handles device code auth and stores refresh token for automated use.
"""

import json
import os
import sys
import requests
from pathlib import Path
from datetime import datetime, timedelta

# Microsoft Graph settings for personal accounts
CLIENT_ID = "0b4231ce-b868-4aba-9c94-a4bb40cd9bcd"  # Enki-Mail-Assistant app
AUTH_URL = "https://login.microsoftonline.com/common/oauth2/v2.0"
GRAPH_URL = "https://graph.microsoft.com/v1.0"
SCOPES = [
    "openid",
    "profile",
    "offline_access",
    "https://graph.microsoft.com/Mail.Read",
    "https://graph.microsoft.com/Mail.Send",
    "https://graph.microsoft.com/Calendars.Read",
    "https://graph.microsoft.com/Calendars.Read.Shared",
]

TOKEN_FILE = Path.home() / ".config" / "enki" / "ms_graph_token.json"

def ensure_token_file():
    """Ensure token directory exists."""
    TOKEN_FILE.parent.mkdir(parents=True, exist_ok=True)

def load_token():
    """Load stored token if exists and valid."""
    if not TOKEN_FILE.exists():
        return None
    try:
        with open(TOKEN_FILE, 'r') as f:
            token = json.load(f)
        # Check if expired
        expires_at = datetime.fromisoformat(token.get('expires_at', '2000-01-01'))
        if datetime.now() < expires_at - timedelta(minutes=5):
            return token
        # Try refresh
        return refresh_token(token.get('refresh_token'))
    except Exception as e:
        print(f"Token error: {e}")
        return None

def refresh_token(refresh_token):
    """Refresh access token using refresh token."""
    if not refresh_token:
        return None
    
    response = requests.post(
        f"{AUTH_URL}/token",
        data={
            "client_id": CLIENT_ID,
            "refresh_token": refresh_token,
            "scope": " ".join(SCOPES),
            "grant_type": "refresh_token",
        }
    )
    if response.status_code == 200:
        token = response.json()
        token['expires_at'] = (datetime.now() + timedelta(seconds=token['expires_in'])).isoformat()
        save_token(token)
        return token
    return None

def device_code_auth():
    """Authenticate using device code flow."""
    print("Initiating device code authentication...")
    
    # Step 1: Request device code
    response = requests.post(
        f"{AUTH_URL}/devicecode",
        data={
            "client_id": CLIENT_ID,
            "scope": " ".join(SCOPES),
        }
    )
    
    if response.status_code != 200:
        print(f"Error getting device code: {response.text}")
        return None
    
    device_code = response.json()
    print(f"\n{'='*60}")
    print(f"To sign in, use a web browser to open:")
    print(f"  {device_code['verification_uri']}")
    print(f"\nAnd enter the code: {device_code['user_code']}")
    print(f"{'='*60}\n")
    print("Waiting for authentication... (check your phone for SMS/Authenticator prompt)")
    
    # Step 2: Poll for token
    interval = device_code.get('interval', 5)
    while True:
        import time
        time.sleep(interval)
        
        token_response = requests.post(
            f"{AUTH_URL}/token",
            data={
                "client_id": CLIENT_ID,
                "device_code": device_code['device_code'],
                "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
            }
        )
        
        if token_response.status_code == 200:
            token = token_response.json()
            token['expires_at'] = (datetime.now() + timedelta(seconds=token['expires_in'])).isoformat()
            save_token(token)
            print("✓ Authentication successful!")
            return token
        
        error = token_response.json().get('error')
        if error == 'authorization_pending':
            continue  # Still waiting
        elif error == 'expired_token':
            print("✗ Device code expired. Please try again.")
            return None
        else:
            print(f"Error: {token_response.text}")
            return None

def save_token(token):
    """Save token to file with restricted permissions."""
    ensure_token_file()
    with open(TOKEN_FILE, 'w') as f:
        json.dump(token, f)
    os.chmod(TOKEN_FILE, 0o600)  # Owner read/write only

def get_access_token():
    """Get valid access token, authenticating if necessary."""
    token = load_token()
    if token:
        return token['access_token']
    return device_code_auth()['access_token']

def get_emails(access_token, top=10):
    """Fetch recent emails."""
    response = requests.get(
        f"{GRAPH_URL}/me/messages",
        headers={"Authorization": f"Bearer {access_token}"},
        params={"$top": top, "$orderby": "receivedDateTime desc", "$select": "subject,from,receivedDateTime,isRead,importance"}
    )
    if response.status_code == 200:
        return response.json().get('value', [])
    print(f"Error fetching emails: {response.status_code}")
    return []

def get_calendar(access_token, days=1):
    """Fetch calendar events for next N days."""
    start = datetime.now().isoformat()
    end = (datetime.now() + timedelta(days=days)).isoformat()
    
    response = requests.get(
        f"{GRAPH_URL}/me/calendarview",
        headers={"Authorization": f"Bearer {access_token}"},
        params={
            "startDateTime": start,
            "endDateTime": end,
            "$select": "subject,start,end,location",
            "$orderby": "start/dateTime"
        }
    )
    if response.status_code == 200:
        return response.json().get('value', [])
    print(f"Error fetching calendar: {response.status_code}")
    return []

def send_email(access_token, to, subject, body):
    """Send an email."""
    response = requests.post(
        f"{GRAPH_URL}/me/sendMail",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        },
        json={
            "message": {
                "subject": subject,
                "body": {"contentType": "HTML", "content": body},
                "toRecipients": [{"emailAddress": {"address": to}}]
            }
        }
    )
    return response.status_code == 202

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print(f"  {sys.argv[0]} auth          - Authenticate with device code")
        print(f"  {sys.argv[0]} emails [N]    - List N recent emails (default 10)")
        print(f"  {sys.argv[0]} calendar [N]  - Show calendar for next N days (default 1)")
        print(f"  {sys.argv[0]} send TO SUBJECT BODY - Send email")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "auth":
        token = device_code_auth()
        if token:
            print(f"Token saved to: {TOKEN_FILE}")
    
    elif cmd == "emails":
        access_token = get_access_token()
        if access_token:
            emails = get_emails(access_token, int(sys.argv[2]) if len(sys.argv) > 2 else 10)
            print(json.dumps(emails, indent=2))
    
    elif cmd == "calendar":
        access_token = get_access_token()
        if access_token:
            events = get_calendar(access_token, int(sys.argv[2]) if len(sys.argv) > 2 else 1)
            print(json.dumps(events, indent=2))
    
    elif cmd == "send":
        if len(sys.argv) < 5:
            print("Usage: send TO SUBJECT BODY")
            sys.exit(1)
        access_token = get_access_token()
        if access_token:
            success = send_email(access_token, sys.argv[2], sys.argv[3], sys.argv[4])
            print("Sent!" if success else "Failed")
