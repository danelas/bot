import os
import time
from dotenv import load_dotenv
from conversation_manager import ConversationManager
from sheets_handler import GoogleSheetsHandler

# Load environment variables
load_dotenv()

def test_mortgage_flow():
    """Test the Save Money > Lower Mortgage Payments flow"""
    print("\n" + "="*60)
    print("TESTING SAVE MONEY > LOWER MORTGAGE PAYMENTS FLOW")
    print("="*60)
    
    # Initialize the conversation manager
    manager = ConversationManager()
    
    # Create a test user
    user_id = "test_user_cli_mortgage"
    user_name = "Test User (Mortgage)"
    
    # Start the Save Money flow
    response, quick_replies = manager.start_save_money_flow(user_id)
    print(f"\nBot: {response}")
    print(f"Quick Replies: {quick_replies}")
    
    # Select Lower Mortgage Payments
    selection = "Lower Mortgage Payments"
    print(f"\nUser: {selection}")
    response, quick_replies = manager.handle_save_money_category(user_id, user_name, selection)
    print(f"\nBot: {response}")
    print(f"Quick Replies: {quick_replies}")
    
    # Step 1: Select refinance or new loan
    selection = "Refinance"
    print(f"\nUser: {selection}")
    response, quick_replies = manager.handle_mortgage_flow(user_id, user_name, selection)
    print(f"\nBot: {response}")
    print(f"Quick Replies: {quick_replies}")
    
    # Step 2: Select whether to connect with expert
    selection = "Yes, connect me"
    print(f"\nUser: {selection}")
    response, quick_replies = manager.handle_mortgage_flow(user_id, user_name, selection)
    print(f"\nBot: {response}")
    print(f"Quick Replies: {quick_replies if quick_replies else 'None'}")
    
    print("\nLower Mortgage Payments flow test completed successfully!\n")

def test_utility_flow():
    """Test the Save Money > Reduce Utility Bills flow"""
    print("\n" + "="*60)
    print("TESTING SAVE MONEY > REDUCE UTILITY BILLS FLOW")
    print("="*60)
    
    # Initialize the conversation manager
    manager = ConversationManager()
    
    # Create a test user
    user_id = "test_user_cli_utility"
    user_name = "Test User (Utility)"
    
    # Start the Save Money flow
    response, quick_replies = manager.start_save_money_flow(user_id)
    print(f"\nBot: {response}")
    print(f"Quick Replies: {quick_replies}")
    
    # Select Reduce Utility Bills
    selection = "Reduce Utility Bills"
    print(f"\nUser: {selection}")
    response, quick_replies = manager.handle_save_money_category(user_id, user_name, selection)
    print(f"\nBot: {response}")
    print(f"Quick Replies: {quick_replies}")
    
    # Step 1: Select smart home or appliances
    selection = "Smart Home"
    print(f"\nUser: {selection}")
    response, quick_replies = manager.handle_utility_flow(user_id, user_name, selection)
    print(f"\nBot: {response}")
    print(f"Quick Replies: {quick_replies}")
    
    # Step 2: Select whether to receive guide
    selection = "Yes, send guide"
    print(f"\nUser: {selection}")
    response, quick_replies = manager.handle_utility_flow(user_id, user_name, selection)
    print(f"\nBot: {response}")
    print(f"Quick Replies: {quick_replies if quick_replies else 'None'}")
    
    print("\nReduce Utility Bills flow test completed successfully!\n")

def test_insurance_flow():
    """Test the Save Money > Home Insurance Discounts flow"""
    print("\n" + "="*60)
    print("TESTING SAVE MONEY > HOME INSURANCE DISCOUNTS FLOW")
    print("="*60)
    
    # Initialize the conversation manager
    manager = ConversationManager()
    
    # Create a test user
    user_id = "test_user_cli_insurance"
    user_name = "Test User (Insurance)"
    
    # Start the Save Money flow
    response, quick_replies = manager.start_save_money_flow(user_id)
    print(f"\nBot: {response}")
    print(f"Quick Replies: {quick_replies}")
    
    # Select Home Insurance Discounts
    selection = "Home Insurance Discounts"
    print(f"\nUser: {selection}")
    response, quick_replies = manager.handle_save_money_category(user_id, user_name, selection)
    print(f"\nBot: {response}")
    print(f"Quick Replies: {quick_replies}")
    
    # Step 1: Select if they have insurance
    selection = "Yes"
    print(f"\nUser: {selection}")
    response, quick_replies = manager.handle_insurance_flow(user_id, user_name, selection)
    print(f"\nBot: {response}")
    print(f"Quick Replies: {quick_replies}")
    
    # Step 2: Select whether to connect with advisor
    selection = "No thanks"
    print(f"\nUser: {selection}")
    response, quick_replies = manager.handle_insurance_flow(user_id, user_name, selection)
    print(f"\nBot: {response}")
    print(f"Quick Replies: {quick_replies if quick_replies else 'None'}")
    
    print("\nHome Insurance Discounts flow test completed successfully!\n")

def test_tax_flow():
    """Test the Save Money > Tax Benefits flow"""
    print("\n" + "="*60)
    print("TESTING SAVE MONEY > TAX BENEFITS FLOW")
    print("="*60)
    
    # Initialize the conversation manager
    manager = ConversationManager()
    
    # Create a test user
    user_id = "test_user_cli_tax"
    user_name = "Test User (Tax)"
    
    # Start the Save Money flow
    response, quick_replies = manager.start_save_money_flow(user_id)
    print(f"\nBot: {response}")
    print(f"Quick Replies: {quick_replies}")
    
    # Select Tax Benefits
    selection = "Tax Benefits"
    print(f"\nUser: {selection}")
    response, quick_replies = manager.handle_save_money_category(user_id, user_name, selection)
    print(f"\nBot: {response}")
    print(f"Quick Replies: {quick_replies}")
    
    # Select whether to connect with tax consultant
    selection = "Yes, connect me"
    print(f"\nUser: {selection}")
    response, quick_replies = manager.handle_tax_flow(user_id, user_name, selection)
    print(f"\nBot: {response}")
    print(f"Quick Replies: {quick_replies if quick_replies else 'None'}")
    
    print("\nTax Benefits flow test completed successfully!\n")

def test_interactive_flow():
    """Interactive test of the Save Money conversation flow"""
    print("\n" + "="*60)
    print("INTERACTIVE SAVE MONEY FLOW TEST")
    print("="*60)
    
    # Initialize the conversation manager
    manager = ConversationManager()
    
    # Create a test user
    user_id = "test_user_interactive_save_money"
    user_name = "Interactive Save Money User"
    
    # Start the Save Money flow
    response, quick_replies = manager.start_save_money_flow(user_id)
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
    print("Swift Showings Save Money Flow Test")
    print("===================================")
    print("This tool tests the Save Money conversation flows")
    print()
    
    while True:
        print("\nSelect a test to run:")
        print("1. Test Lower Mortgage Payments Flow")
        print("2. Test Reduce Utility Bills Flow")
        print("3. Test Home Insurance Discounts Flow")
        print("4. Test Tax Benefits Flow")
        print("5. Interactive Test")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ")
        
        if choice == "1":
            test_mortgage_flow()
        elif choice == "2":
            test_utility_flow()
        elif choice == "3":
            test_insurance_flow()
        elif choice == "4":
            test_tax_flow()
        elif choice == "5":
            test_interactive_flow()
        elif choice == "6":
            print("\nExiting...")
            break
        else:
            print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    main()
