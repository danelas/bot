import os
import socket
import webbrowser
import subprocess
import sys
from dotenv import load_dotenv

load_dotenv()

def get_local_ip():
    """Get the local IP address of the machine"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def check_ngrok_installed():
    """Check if ngrok is installed"""
    try:
        subprocess.run(["ngrok", "--version"], 
                      stdout=subprocess.PIPE, 
                      stderr=subprocess.PIPE, 
                      check=True)
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        return False

def generate_verify_token():
    """Generate a random verify token if not already set"""
    import secrets
    return secrets.token_hex(16)

def main():
    print("=" * 50)
    print("Facebook Messenger Webhook Setup Guide")
    print("=" * 50)
    
    # Check verify token
    verify_token = os.getenv("FACEBOOK_VERIFY_TOKEN")
    if not verify_token:
        verify_token = generate_verify_token()
        print(f"\n⚠️ No FACEBOOK_VERIFY_TOKEN found in your .env file.")
        print(f"Generated random token: {verify_token}")
        print(f"Please add this to your .env file:")
        print(f"FACEBOOK_VERIFY_TOKEN={verify_token}")
    else:
        print(f"\n✅ FACEBOOK_VERIFY_TOKEN is configured: {verify_token}")
    
    # Check Facebook Page Access Token
    page_token = os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN")
    if not page_token:
        print("\n❌ FACEBOOK_PAGE_ACCESS_TOKEN is missing in your .env file.")
        print("You need this to send messages from your chatbot.")
        print("Get it from: https://developers.facebook.com/tools/explorer/")
    else:
        print("\n✅ FACEBOOK_PAGE_ACCESS_TOKEN is configured")
    
    # Local URL
    local_ip = get_local_ip()
    local_url = f"http://{local_ip}:5000"
    print(f"\n📡 Your local server address: {local_url}")
    
    # Check Ngrok
    if check_ngrok_installed():
        print("\n✅ Ngrok is installed and available")
        print("To expose your local server, run in a separate terminal:")
        print("    ngrok http 5000")
        print("\nThis will give you a URL like: https://abc123.ngrok.io")
    else:
        print("\n❌ Ngrok is not installed or not in your PATH")
        print("For local testing, download Ngrok from: https://ngrok.com/download")
    
    print("\n" + "=" * 50)
    print("Webhook Configuration Steps:")
    print("=" * 50)
    print("1. Start your Flask application with:")
    print("    flask run --host=0.0.0.0 --port=5000")
    
    print("\n2. Expose your application with Ngrok:")
    print("    ngrok http 5000")
    
    print("\n3. In Facebook Developer Dashboard:")
    print("   a. Go to: https://developers.facebook.com/apps/")
    print("   b. Select your app")
    print("   c. Navigate to Messenger → Settings")
    print("   d. In the 'Webhooks' section, click 'Add Callback URL'")
    print("   e. Enter your Ngrok URL + '/' as the Callback URL")
    print(f"      (e.g., https://abc123.ngrok.io/)")
    print(f"   f. Enter your Verify Token: {verify_token}")
    print("   g. Click 'Verify and Save'")
    
    print("\n4. Subscribe to events:")
    print("   a. In the 'Webhooks' section, click 'Add Subscriptions'")
    print("   b. Select your Facebook Page")
    print("   c. Select at minimum: 'messages' and 'messaging_postbacks'")
    print("   d. Click 'Save'")
    
    print("\n5. Test your webhook by sending a message to your Facebook Page")
    
    print("\n" + "=" * 50)
    print("Want to open the Facebook Developer Dashboard?")
    open_dashboard = input("Type 'yes' to open in your browser: ")
    if open_dashboard.lower() in ['yes', 'y']:
        webbrowser.open('https://developers.facebook.com/apps/')
    
    print("\nGood luck with your chatbot setup!")

if __name__ == "__main__":
    main()
