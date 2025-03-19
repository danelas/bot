import os
import time
from dotenv import load_dotenv
from conversation_manager import ConversationManager
from sheets_handler import GoogleSheetsHandler

# Load environment variables
load_dotenv()

def test_real_estate_flow():
    """Test the Get Help > Real Estate Questions flow"""
    print("\n" + "="*60)
    print("TESTING GET HELP > REAL ESTATE QUESTIONS FLOW")
    print("="*60)
    
    # Initialize the conversation manager
    manager = ConversationManager()
    
    # Create a test user
    user_id = "test_user_cli_real_estate"
    user_name = "Test User (Real Estate)"
    
    # Start the Get Help flow
    response, quick_replies = manager.start_get_help_flow(user_id)
    print(f"\nBot: {response}")
    print(f"Quick Replies: {quick_replies}")
    
    # Select Real Estate Questions
    selection = "Real Estate Questions"
    print(f"\nUser: {selection}")
    response, quick_replies = manager.handle_help_category(user_id, user_name, selection)
    print(f"\nBot: {response}")
    print(f"Quick Replies: {quick_replies}")
    
    # Step 1: Select question topic
    selection = "Buying"
    print(f"\nUser: {selection}")
    response, quick_replies = manager.handle_real_estate_flow(user_id, user_name, selection)
    print(f"\nBot: {response}")
    print(f"Quick Replies: {quick_replies}")
    
    # Step 2: Select whether to connect with expert
    selection = "Yes, connect me"
    print(f"\nUser: {selection}")
    response, quick_replies = manager.handle_real_estate_flow(user_id, user_name, selection)
    print(f"\nBot: {response}")
    print(f"Quick Replies: {quick_replies if quick_replies else 'None'}")
    
    print("\nReal Estate Questions flow test completed successfully!\n")

def test_maintenance_flow():
    """Test the Get Help > Maintenance & Repairs flow"""
    print("\n" + "="*60)
    print("TESTING GET HELP > MAINTENANCE & REPAIRS FLOW")
    print("="*60)
    
    # Initialize the conversation manager
    manager = ConversationManager()
    
    # Create a test user
    user_id = "test_user_cli_maintenance"
    user_name = "Test User (Maintenance)"
    
    # Start the Get Help flow
    response, quick_replies = manager.start_get_help_flow(user_id)
    print(f"\nBot: {response}")
    print(f"Quick Replies: {quick_replies}")
    
    # Select Maintenance & Repairs
    selection = "Maintenance & Repairs"
    print(f"\nUser: {selection}")
    response, quick_replies = manager.handle_help_category(user_id, user_name, selection)
    print(f"\nBot: {response}")
    print(f"Quick Replies: {quick_replies}")
    
    # Step 1: Select DIY or Professional
    selection = "DIY"
    print(f"\nUser: {selection}")
    response, quick_replies = manager.handle_maintenance_flow(user_id, user_name, selection)
    print(f"\nBot: {response}")
    print(f"Quick Replies: {quick_replies}")
    
    # Step 2: Select maintenance issue
    selection = "Plumbing"
    print(f"\nUser: {selection}")
    response, quick_replies = manager.handle_maintenance_flow(user_id, user_name, selection)
    print(f"\nBot: {response}")
    print(f"Quick Replies: {quick_replies}")
    
    # Step 3: Select whether to receive guide
    selection = "Yes, send guide"
    print(f"\nUser: {selection}")
    response, quick_replies = manager.handle_maintenance_flow(user_id, user_name, selection)
    print(f"\nBot: {response}")
    print(f"Quick Replies: {quick_replies if quick_replies else 'None'}")
    
    print("\nMaintenance & Repairs flow test completed successfully!\n")

def test_legal_flow():
    """Test the Get Help > Legal Help flow"""
    print("\n" + "="*60)
    print("TESTING GET HELP > LEGAL HELP FLOW")
    print("="*60)
    
    # Initialize the conversation manager
    manager = ConversationManager()
    
    # Create a test user
    user_id = "test_user_cli_legal"
    user_name = "Test User (Legal)"
    
    # Start the Get Help flow
    response, quick_replies = manager.start_get_help_flow(user_id)
    print(f"\nBot: {response}")
    print(f"Quick Replies: {quick_replies}")
    
    # Select Legal Help
    selection = "Legal Help"
    print(f"\nUser: {selection}")
    response, quick_replies = manager.handle_help_category(user_id, user_name, selection)
    print(f"\nBot: {response}")
    print(f"Quick Replies: {quick_replies}")
    
    # Step 1: Select legal topic
    selection = "Tenant Rights"
    print(f"\nUser: {selection}")
    response, quick_replies = manager.handle_legal_flow(user_id, user_name, selection)
    print(f"\nBot: {response}")
    print(f"Quick Replies: {quick_replies}")
    
    # Step 2: Select whether to connect with specialist
    selection = "Just general info"
    print(f"\nUser: {selection}")
    response, quick_replies = manager.handle_legal_flow(user_id, user_name, selection)
    print(f"\nBot: {response}")
    print(f"Quick Replies: {quick_replies if quick_replies else 'None'}")
    
    print("\nLegal Help flow test completed successfully!\n")

def test_other_help_flow():
    """Test the Get Help > Other flow"""
    print("\n" + "="*60)
    print("TESTING GET HELP > OTHER FLOW")
    print("="*60)
    
    # Initialize the conversation manager
    manager = ConversationManager()
    
    # Create a test user
    user_id = "test_user_cli_other"
    user_name = "Test User (Other)"
    
    # Start the Get Help flow
    response, quick_replies = manager.start_get_help_flow(user_id)
    print(f"\nBot: {response}")
    print(f"Quick Replies: {quick_replies}")
    
    # Select Other
    selection = "Other"
    print(f"\nUser: {selection}")
    response, quick_replies = manager.handle_help_category(user_id, user_name, selection)
    print(f"\nBot: {response}")
    print(f"Quick Replies: {quick_replies if quick_replies else 'None'}")
    
    # Step 1: Enter a custom question
    selection = "I'm interested in investment properties. Can you tell me about the ROI for different property types in Chicago?"
    print(f"\nUser: {selection}")
    response, quick_replies = manager.handle_other_help_flow(user_id, user_name, selection)
    print(f"\nBot: {response}")
    print(f"Quick Replies: {quick_replies if quick_replies else 'None'}")
    
    print("\nOther Help flow test completed successfully!\n")

def test_interactive_flow():
    """Interactive test of the Get Help conversation flow"""
    print("\n" + "="*60)
    print("INTERACTIVE GET HELP FLOW TEST")
    print("="*60)
    
    # Initialize the conversation manager
    manager = ConversationManager()
    
    # Create a test user
    user_id = "test_user_interactive_help"
    user_name = "Interactive Help User"
    
    # Start the Get Help flow
    response, quick_replies = manager.start_get_help_flow(user_id)
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
    print("Swift Showings Get Help Flow Test")
    print("=================================")
    print("This tool tests the Get Help conversation flows")
    print()
    
    while True:
        print("\nSelect a test to run:")
        print("1. Test Real Estate Questions Flow")
        print("2. Test Maintenance & Repairs Flow")
        print("3. Test Legal Help Flow")
        print("4. Test Other Help Flow")
        print("5. Interactive Test")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ")
        
        if choice == "1":
            test_real_estate_flow()
        elif choice == "2":
            test_maintenance_flow()
        elif choice == "3":
            test_legal_flow()
        elif choice == "4":
            test_other_help_flow()
        elif choice == "5":
            test_interactive_flow()
        elif choice == "6":
            print("\nExiting...")
            break
        else:
            print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    main()
