#!/usr/bin/env python3
"""
One-time Google OAuth setup.
Run this LOCALLY (not in GitHub Actions) to get your refresh token.

Usage:
  pip install google-auth-oauthlib
  python execution/setup_google_auth.py

Then copy the printed GOOGLE_REFRESH_TOKEN into your GitHub repo secrets.
"""

import json
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/gmail.compose",
]

# You'll be prompted to paste your client_secrets.json content
print("=== Google OAuth Setup ===")
print()
print("Step 1: Go to https://console.cloud.google.com")
print("Step 2: Create a project → Enable 'Google Calendar API' and 'Gmail API'")
print("Step 3: APIs & Services → Credentials → Create OAuth 2.0 Client ID")
print("         Application type: Desktop app")
print("Step 4: Download the JSON → paste the path below")
print()

client_secrets_path = input("Path to your client_secrets.json: ").strip()

flow = InstalledAppFlow.from_client_secrets_file(client_secrets_path, SCOPES)
creds = flow.run_local_server(port=0)

print()
print("=" * 60)
print("Add these to your GitHub repo → Settings → Secrets → Actions:")
print()
print(f"GOOGLE_CLIENT_ID     = {creds.client_id}")
print(f"GOOGLE_CLIENT_SECRET = {creds.client_secret}")
print(f"GOOGLE_REFRESH_TOKEN = {creds.refresh_token}")
print("=" * 60)
