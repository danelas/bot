import os
import json

def setup_google_credentials():
    """Create a credentials file from environment variable on Replit"""
    # Check if we're on Replit (if REPL_ID exists)
    if os.getenv('REPL_ID'):
        # Get credentials content from secrets
        creds_content = os.getenv('GOOGLE_SHEETS_CREDENTIALS_CONTENT')
        
        if creds_content:
            # Create a credentials file
            with open('google_credentials.json', 'w') as f:
                f.write(creds_content)
            
            # Set the environment variable to point to this file
            os.environ['GOOGLE_SHEETS_CREDENTIALS_FILE'] = 'google_credentials.json'
            
            print("Google credentials set up for Replit environment")
            return True
        else:
            print("ERROR: GOOGLE_SHEETS_CREDENTIALS_CONTENT not found in secrets")
            return False
    else:
        # Not on Replit, assume credentials file is set in .env
        print("Not running on Replit, using credentials file from .env")
        return True

# Add this at the top of your app.py to call this function
# from replit_sheets_handler import setup_google_credentials
# setup_google_credentials()
