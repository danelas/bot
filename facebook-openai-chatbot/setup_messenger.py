import requests
from dotenv import load_dotenv
from facebook_handler import FacebookHandler

def main():
    """
    Set up the Facebook Messenger profile for Swift Showings
    This script configures:
    1. The Get Started button
    2. The greeting text
    3. The persistent menu
    """
    print("Setting up Swift Showings Facebook Messenger profile...")
    
    # Initialize Facebook handler
    fb_handler = FacebookHandler()
    
    # Set up the Get Started button
    print("Setting up Get Started button...")
    get_started_result = fb_handler.setup_get_started_button()
    if get_started_result.get("result") == "success":
        print("✅ Get Started button set up successfully")
    else:
        print(f"❌ Failed to set up Get Started button: {get_started_result}")
    
    # Set up greeting text
    print("Setting up greeting text...")
    greeting_result = fb_handler.setup_greeting_text()
    if greeting_result.get("result") == "success":
        print("✅ Greeting text set up successfully")
    else:
        print(f"❌ Failed to set up greeting text: {greeting_result}")
    
    # Set up persistent menu
    print("Setting up persistent menu...")
    menu_result = fb_handler.setup_persistent_menu()
    if menu_result.get("result") == "success":
        print("✅ Persistent menu set up successfully")
    else:
        print(f"❌ Failed to set up persistent menu: {menu_result}")
    
    print("\nSetup complete!")
    print("\nReminders:")
    print("1. Make sure your webhook is properly configured in Facebook Developer Portal")
    print("2. Subscribe to messaging events (messages, messaging_postbacks)")
    print("3. Your Facebook Page must be connected to your app")
    print("\nTesting Instructions:")
    print("1. Visit your Facebook Page and click 'Send Message'")
    print("2. You should see the greeting message and Get Started button")
    print("3. When you click Get Started, the welcome message with quick replies should appear")

if __name__ == "__main__":
    # Load environment variables
    load_dotenv()
    main()
