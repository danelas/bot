import os
from dotenv import load_dotenv
from openai_helper import OpenAIAssistant
from sheets_handler import GoogleSheetsHandler

# Load environment variables
load_dotenv()

def swift_showings_welcome():
    """Display the Swift Showings welcome flow"""
    print("\n" + "="*50)
    print("SWIFT SHOWINGS MESSENGER SIMULATION")
    print("="*50)
    print("\nFacebook Messenger: Welcome to Swift Showings! 🎉 We make finding your next home easier and more affordable—without extra fees or hassles.")
    print("\nFacebook Messenger: Choose an option below to get started:")
    print("Quick Reply Options: [Find Home] [Get Help] [Save Money] [Learn More]")
    
    while True:
        choice = input("\nSelect a quick reply option (or type 'exit' to quit): ").strip()
        
        if choice.lower() == 'exit':
            return None
            
        if choice.lower() == 'find home':
            return "Great! Let's find you a home. What city or neighborhood are you interested in?"
        elif choice.lower() == 'get help':
            return "I'm here to help! What specifically do you need assistance with?"
        elif choice.lower() == 'save money':
            return "We love saving you money! Swift Showings helps you save on fees that traditional agents charge. Would you like to learn more about our fee structure?"
        elif choice.lower() == 'learn more':
            return "Swift Showings makes house hunting simple and affordable. We connect you directly with sellers and provide tools to streamline your search. What would you like to know more about?"
        else:
            print("Please select a valid option: Find Home, Get Help, Save Money, Learn More")

def main():
    print("Swift Showings Assistant Test CLI")
    print("=========================")
    print("This tool tests the Swift Showings chatbot without Facebook.")
    print("Press Ctrl+C to exit at any time.")
    print()
    
    # Show welcome flow first
    print("Starting welcome flow simulation...")
    response = swift_showings_welcome()
    if not response:
        return
        
    print(f"\nBot: {response}")
    
    # Initialize the OpenAI Assistant
    assistant = OpenAIAssistant()
    
    # Try to initialize the Google Sheets handler
    try:
        sheets = GoogleSheetsHandler()
        sheets_available = True
    except Exception as e:
        print(f"Google Sheets integration not available: {e}")
        sheets_available = False
    
    # Generate a test user ID
    user_id = "test_user_cli"
    user_name = "Test User"
    
    # Start conversation loop
    while True:
        try:
            # Get user input
            message = input("\nYou: ")
            
            if not message:
                continue
                
            if message.lower() in ["exit", "quit", "q"]:
                break
            
            print("\nProcessing...")
            
            # Process the message
            response = assistant.process_message(user_id, message)
            
            # Display the response
            print(f"\nBot: {response.get('text')}")
            
            # Check if there are platform-specific responses
            if 'instagram_content' in response and response['instagram_content'] != response['text']:
                print(f"\nInstagram Content: {response.get('instagram_content')}")
                
            if 'facebook_content' in response and response['facebook_content'] != response['text']:
                print(f"\nFacebook Content: {response.get('facebook_content')}")
            
            # Save to Google Sheets if available
            if sheets_available:
                thread_id = assistant.get_or_create_thread(user_id)
                saved = sheets.save_conversation(
                    user_id,
                    user_name,
                    message,
                    response.get('text'),
                    "CLI Test",
                    thread_id
                )
                if saved:
                    print("\n[Conversation saved to Google Sheets]")
        
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"\nError: {e}")

if __name__ == "__main__":
    main()
