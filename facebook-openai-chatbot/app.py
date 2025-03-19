import os
import json
from flask import Flask, request, Response
from dotenv import load_dotenv
from openai_helper import OpenAIHelper
from facebook_handler import FacebookHandler
from sheets_handler import GoogleSheetsHandler
from conversation_manager import ConversationManager

# Load environment variables
load_dotenv()

# Handle Google Sheets credentials for Replit environment
if os.getenv('REPL_ID'):
    from replit_sheets_handler import setup_google_credentials
    setup_google_credentials()

# Initialize Flask application
app = Flask(__name__)

# Initialize helpers
openai_helper = OpenAIHelper()
facebook_handler = FacebookHandler()
sheets_handler = GoogleSheetsHandler()
conversation_manager = ConversationManager()

# Welcome message for new conversations
WELCOME_MESSAGE = "Welcome to Swift Showings! 🎉 We make finding your next home easier and more affordable—without extra fees or hassles."

# Quick reply options for welcome
WELCOME_QUICK_REPLIES = ["Find Home", "Get Help", "Save Money", "Learn More"]

@app.route("/", methods=["GET"])
def verify():
    """
    Handle webhook verification from Facebook
    """
    # Parse the query params
    mode = request.args.get("hub.mode", "")
    token = request.args.get("hub.verify_token", "")
    challenge = request.args.get("hub.challenge", "")
    
    # Check if token and mode are in the query string
    if mode and token:
        # Check if the mode and token sent match verification
        if mode == "subscribe" and token == os.getenv("FACEBOOK_VERIFY_TOKEN"):
            # Respond with the challenge token
            print("WEBHOOK_VERIFIED")
            return challenge
        else:
            # Respond with '403 Forbidden' if verify tokens do not match
            return Response(status=403)
    
    return "Hello, this is the Swift Showings webhook server."

@app.route("/", methods=["POST"])
def webhook():
    """
    Handle webhook callbacks from Facebook
    """
    # Get the request body
    data = request.get_json()
    
    if data["object"] == "page":
        for entry in data["entry"]:
            # Iterate over webhook events
            for event in entry.get("messaging", []):
                # Get the sender's ID
                sender_id = event.get("sender", {}).get("id")
                
                if sender_id:
                    # Get user info
                    user_info = facebook_handler.get_user_profile(sender_id)
                    user_name = f"{user_info.get('first_name', '')} {user_info.get('last_name', '')}"
                    
                    # Handle different event types
                    if event.get("message"):
                        # Check if this is a quick reply
                        if event.get("message").get("quick_reply"):
                            handle_quick_reply(sender_id, user_name, event["message"]["quick_reply"]["payload"])
                        # Regular text message
                        elif event.get("message").get("text"):
                            handle_message(sender_id, user_name, event["message"]["text"])
                    # Postback (button click)
                    elif event.get("postback"):
                        handle_postback(sender_id, user_name, event["postback"]["payload"])
    
    return "EVENT_RECEIVED"

def handle_message(sender_id, user_name, message_text):
    """
    Handle incoming text messages
    """
    # Check if user is in an active conversation flow
    flow_response = conversation_manager.process_message(sender_id, user_name, message_text)
    
    if flow_response:
        # User is in an active flow - handle with conversation manager
        response_text, quick_replies = flow_response
        
        # Send response
        if quick_replies:
            facebook_handler.send_quick_replies(sender_id, response_text, quick_replies)
        else:
            facebook_handler.send_text_message(sender_id, response_text)
        
        # Log the conversation
        thread_id = openai_helper.get_or_create_conversation(sender_id)
        sheets_handler.save_conversation(
            sender_id,
            user_name,
            message_text,
            response_text,
            "Facebook",
            thread_id
        )
    else:
        # User is not in an active flow - use OpenAI
        response = openai_helper.process_message(sender_id, message_text)
        
        # Get the response text, preferring facebook-specific content if available
        response_text = response.get("facebook_content", response.get("text"))
        
        # Send response
        facebook_handler.send_text_message(sender_id, response_text)
        
        # Log the conversation
        thread_id = openai_helper.get_or_create_conversation(sender_id)
        sheets_handler.save_conversation(
            sender_id,
            user_name,
            message_text,
            response_text,
            "Facebook",
            thread_id
        )

def handle_quick_reply(sender_id, user_name, payload):
    """
    Handle quick replies from the user
    """
    thread_id = openai_helper.get_or_create_conversation(sender_id)
    
    if payload == "FIND_HOME":
        # Start the Find Home flow
        response_text, quick_replies = conversation_manager.start_find_home_flow(sender_id)
        facebook_handler.send_quick_replies(sender_id, response_text, quick_replies)
        
        # Log the conversation
        sheets_handler.save_conversation(
            sender_id,
            user_name,
            "Quick Reply: Find Home",
            response_text,
            "Facebook",
            thread_id
        )
    elif payload == "GET_HELP":
        # Start the Get Help flow
        response_text, quick_replies = conversation_manager.start_get_help_flow(sender_id)
        facebook_handler.send_quick_replies(sender_id, response_text, quick_replies)
        
        # Log the conversation
        sheets_handler.save_conversation(
            sender_id,
            user_name,
            "Quick Reply: Get Help",
            response_text,
            "Facebook",
            thread_id
        )
    elif payload == "SAVE_MONEY":
        # Start the Save Money flow
        response_text, quick_replies = conversation_manager.start_save_money_flow(sender_id)
        facebook_handler.send_quick_replies(sender_id, response_text, quick_replies)
        
        # Log the conversation
        sheets_handler.save_conversation(
            sender_id,
            user_name,
            "Quick Reply: Save Money",
            response_text,
            "Facebook",
            thread_id
        )
    elif payload == "LEARN_MORE":
        response_text = "Swift Showings makes house hunting simple and affordable. We connect you directly with sellers and provide tools to streamline your search. What would you like to know more about?"
        facebook_handler.send_text_message(sender_id, response_text)
        
        # Log the conversation
        sheets_handler.save_conversation(
            sender_id,
            user_name,
            "Quick Reply: Learn More",
            response_text,
            "Facebook",
            thread_id
        )
    elif payload in ["BUY", "RENT"]:
        # Handle Buy/Rent selection from the Find Home flow
        if payload == "BUY":
            response = conversation_manager.handle_buy_flow(sender_id, user_name, payload, 1)
        else:
            response = conversation_manager.handle_rent_flow(sender_id, user_name, payload, 1)
        
        if response:
            response_text, quick_replies = response
            
            if quick_replies:
                facebook_handler.send_quick_replies(sender_id, response_text, quick_replies)
            else:
                facebook_handler.send_text_message(sender_id, response_text)
            
            # Log the conversation
            sheets_handler.save_conversation(
                sender_id,
                user_name,
                f"Selected: {payload}",
                response_text,
                "Facebook",
                thread_id
            )
    else:
        # Check if this is part of an ongoing conversation flow
        flow_response = conversation_manager.process_message(sender_id, user_name, payload)
        
        if flow_response:
            response_text, quick_replies = flow_response
            
            if quick_replies:
                facebook_handler.send_quick_replies(sender_id, response_text, quick_replies)
            else:
                facebook_handler.send_text_message(sender_id, response_text)
            
            # Log the conversation
            sheets_handler.save_conversation(
                sender_id,
                user_name,
                f"Quick Reply: {payload}",
                response_text,
                "Facebook",
                thread_id
            )
        else:
            # Not part of a flow, use OpenAI
            response = openai_helper.process_message(sender_id, payload)
            response_text = response.get("facebook_content", response.get("text"))
            
            facebook_handler.send_text_message(sender_id, response_text)
            
            # Log the conversation
            sheets_handler.save_conversation(
                sender_id,
                user_name,
                f"Quick Reply: {payload}",
                response_text,
                "Facebook",
                thread_id
            )

def handle_postback(sender_id, user_name, payload):
    """
    Handle postbacks from buttons
    """
    if payload == "GET_STARTED":
        # Send welcome message with quick replies
        facebook_handler.send_quick_replies(
            sender_id, 
            WELCOME_MESSAGE, 
            WELCOME_QUICK_REPLIES
        )
        
        # Log the conversation
        thread_id = openai_helper.get_or_create_conversation(sender_id)
        sheets_handler.save_conversation(
            sender_id,
            user_name,
            "Get Started",
            WELCOME_MESSAGE,
            "Facebook",
            thread_id
        )
    else:
        # Treat other postbacks like quick replies
        handle_quick_reply(sender_id, user_name, payload)

@app.route("/setup", methods=["GET"])
def setup():
    """
    Route to set up the Messenger profile
    """
    result = facebook_handler.setup_messenger_profile()
    return {"success": result}

if __name__ == "__main__":
    app.run(debug=True, port=5000)
