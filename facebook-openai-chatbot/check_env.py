import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Required environment variables
required_vars = [
    "OPENAI_API_KEY",
    "FACEBOOK_PAGE_ACCESS_TOKEN",
    "FACEBOOK_VERIFY_TOKEN",
    "FACEBOOK_APP_ID",
    "FACEBOOK_APP_SECRET",
    "GOOGLE_SHEETS_CREDENTIALS_FILE",
    "GOOGLE_SHEETS_ID"
]

# Check if all required variables are set
missing_vars = []
for var in required_vars:
    if not os.getenv(var):
        missing_vars.append(var)

if missing_vars:
    print("ERROR: The following required environment variables are missing:")
    for var in missing_vars:
        print(f"  - {var}")
    
    # Create a template .env file
    template_content = """# OpenAI credentials
OPENAI_API_KEY=your_openai_api_key

# Facebook Messenger credentials
FACEBOOK_APP_ID=your_facebook_app_id
FACEBOOK_APP_SECRET=your_facebook_app_secret
FACEBOOK_PAGE_ACCESS_TOKEN=your_page_access_token
FACEBOOK_VERIFY_TOKEN=your_verify_token

# Google Sheets credentials
GOOGLE_SHEETS_CREDENTIALS_FILE=path_to_credentials.json
GOOGLE_SHEETS_ID=your_sheet_id
"""
    
    print("\nHere's a template .env file you can use:")
    print("=" * 50)
    print(template_content)
    print("=" * 50)
    
    print("\nPlease create a .env file with these variables and try again.")
    sys.exit(1)
else:
    print("All required environment variables are set!")
    print("Your application is ready to run.")
    sys.exit(0)
