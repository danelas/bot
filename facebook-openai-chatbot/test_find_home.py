import os
import time
from dotenv import load_dotenv
from conversation_manager import ConversationManager
from sheets_handler import GoogleSheetsHandler

# Load environment variables
load_dotenv()

def test_buy_flow():
    """Test the Find Home > Buy conversation flow"""
    print("\n" + "="*60)
    print("TESTING FIND HOME > BUY FLOW")
    print("="*60)
    
    # Initialize the conversation manager
    manager = ConversationManager()
    
    # Create a test user
    user_id = "test_user_cli_buy"
    user_name = "Test User (Buy)"
    
    # Start the Find Home flow
    response, quick_replies = manager.start_find_home_flow(user_id)
    print(f"\nBot: {response}")
    print(f"Quick Replies: {quick_replies}")
    
    # Select Buy
    selection = "Buy"
    print(f"\nUser: {selection}")
    response, quick_replies = manager.handle_buy_or_rent(user_id, selection)
    print(f"\nBot: {response}")
    print(f"Quick Replies: {quick_replies}")
    
    # Step 1: Select home type
    selection = "House"
    print(f"\nUser: {selection}")
    response, quick_replies = manager.handle_buy_flow(user_id, user_name, selection)
    print(f"\nBot: {response}")
    print(f"Quick Replies: {quick_replies}")
    
    # Step 2: Select budget
    selection = "$300k-$400k"
    print(f"\nUser: {selection}")
    response, quick_replies = manager.handle_buy_flow(user_id, user_name, selection)
    print(f"\nBot: {response}")
    print(f"Quick Replies: {quick_replies if quick_replies else 'None'}")
    
    # Step 3: Enter location
    selection = "Chicago, IL"
    print(f"\nUser: {selection}")
    response, quick_replies = manager.handle_buy_flow(user_id, user_name, selection)
    print(f"\nBot: {response}")
    print(f"Quick Replies: {quick_replies}")
    
    # Step 4: Select financing option
    selection = "Yes, I'm pre-approved"
    print(f"\nUser: {selection}")
    response, quick_replies = manager.handle_buy_flow(user_id, user_name, selection)
    print(f"\nBot: {response}")
    print(f"Quick Replies: {quick_replies if quick_replies else 'None'}")
    
    print("\nBuy flow test completed successfully!\n")

def test_rent_flow():
    """Test the Find Home > Rent conversation flow"""
    print("\n" + "="*60)
    print("TESTING FIND HOME > RENT FLOW")
    print("="*60)
    
    # Initialize the conversation manager
    manager = ConversationManager()
    
    # Create a test user
    user_id = "test_user_cli_rent"
    user_name = "Test User (Rent)"
    
    # Start the Find Home flow
    response, quick_replies = manager.start_find_home_flow(user_id)
    print(f"\nBot: {response}")
    print(f"Quick Replies: {quick_replies}")
    
    # Select Rent
    selection = "Rent"
    print(f"\nUser: {selection}")
    response, quick_replies = manager.handle_buy_or_rent(user_id, selection)
    print(f"\nBot: {response}")
    print(f"Quick Replies: {quick_replies}")
    
    # Step 1: Select property type
    selection = "Apartment"
    print(f"\nUser: {selection}")
    response, quick_replies = manager.handle_rent_flow(user_id, user_name, selection)
    print(f"\nBot: {response}")
    print(f"Quick Replies: {quick_replies}")
    
    # Step 2: Select budget
    selection = "$1500-$2000"
    print(f"\nUser: {selection}")
    response, quick_replies = manager.handle_rent_flow(user_id, user_name, selection)
    print(f"\nBot: {response}")
    print(f"Quick Replies: {quick_replies if quick_replies else 'None'}")
    
    # Step 3: Enter location
    selection = "Boston, MA"
    print(f"\nUser: {selection}")
    response, quick_replies = manager.handle_rent_flow(user_id, user_name, selection)
    print(f"\nBot: {response}")
    print(f"Quick Replies: {quick_replies}")
    
    # Step 4: Select roommate option
    selection = "No"
    print(f"\nUser: {selection}")
    response, quick_replies = manager.handle_rent_flow(user_id, user_name, selection)
    print(f"\nBot: {response}")
    print(f"Quick Replies: {quick_replies if quick_replies else 'None'}")
    
    print("\nRent flow test completed successfully!\n")

def test_interactive_flow():
    """Interactive test of the Find Home conversation flow"""
    print("\n" + "="*60)
    print("INTERACTIVE FIND HOME FLOW TEST")
    print("="*60)
    
    # Initialize the conversation manager
    manager = ConversationManager()
    
    # Create a test user
    user_id = "test_user_interactive"
    user_name = "Interactive User"
    
    # Start the Find Home flow
    response, quick_replies = manager.start_find_home_flow(user_id)
    print(f"\nBot: {response}")
    if quick_replies:
        print(f"Quick Replies: {quick_replies}")
    
    # Interactive conversation
    while True:
        user_input = input("\nYour response (or 'exit' to quit): ")
        if user_input.lower() == 'exit':
            break
        
        # Process the user's message
        flow_response = manager.process_message(user_id, user_name, user_input)
        
        if flow_response:
            response_text, quick_replies = flow_response
            print(f"\nBot: {response_text}")
            if quick_replies:
                print(f"Quick Replies: {quick_replies}")
        else:
            print("\nBot: Sorry, I didn't understand that. Please try again.")

def main():
    print("Swift Showings Find Home Flow Test")
    print("=================================")
    print("This tool tests the Find Home conversation flows")
    print()
    
    while True:
        print("\nSelect a test to run:")
        print("1. Test Buy Flow")
        print("2. Test Rent Flow")
        print("3. Interactive Test")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ")
        
        if choice == "1":
            test_buy_flow()
        elif choice == "2":
            test_rent_flow()
        elif choice == "3":
            test_interactive_flow()
        elif choice == "4":
            print("\nExiting...")
            break
        else:
            print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    main()
