import os
import json
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Facebook Configuration
FACEBOOK_PAGE_ACCESS_TOKEN = os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN")

class FacebookHandler:
    def __init__(self):
        self.page_access_token = FACEBOOK_PAGE_ACCESS_TOKEN
        self.api_version = "v17.0"  # Using a recent API version
        self.base_url = f"https://graph.facebook.com/{self.api_version}"
    
    def send_text_message(self, recipient_id, message_text):
        """Send a text message to a recipient"""
        endpoint = f"{self.base_url}/me/messages"
        params = {"access_token": self.page_access_token}
        headers = {"Content-Type": "application/json"}
        
        data = {
            "recipient": {"id": recipient_id},
            "messaging_type": "RESPONSE",
            "message": {"text": message_text}
        }
        
        response = requests.post(
            endpoint,
            params=params,
            headers=headers,
            data=json.dumps(data)
        )
        
        return response.json()
    
    def send_quick_replies(self, recipient_id, message_text, quick_replies):
        """Send a message with quick reply buttons"""
        endpoint = f"{self.base_url}/me/messages"
        params = {"access_token": self.page_access_token}
        headers = {"Content-Type": "application/json"}
        
        # Format the quick replies
        formatted_quick_replies = []
        for reply in quick_replies:
            formatted_quick_replies.append({
                "content_type": "text",
                "title": reply,
                "payload": reply.upper().replace(" ", "_")
            })
        
        data = {
            "recipient": {"id": recipient_id},
            "messaging_type": "RESPONSE",
            "message": {
                "text": message_text,
                "quick_replies": formatted_quick_replies
            }
        }
        
        response = requests.post(
            endpoint,
            params=params,
            headers=headers,
            data=json.dumps(data)
        )
        
        return response.json()
    
    def send_image_message(self, recipient_id, image_url):
        """Send an image message to a recipient"""
        endpoint = f"{self.base_url}/me/messages"
        params = {"access_token": self.page_access_token}
        headers = {"Content-Type": "application/json"}
        
        data = {
            "recipient": {"id": recipient_id},
            "messaging_type": "RESPONSE",
            "message": {
                "attachment": {
                    "type": "image",
                    "payload": {
                        "url": image_url,
                        "is_reusable": True
                    }
                }
            }
        }
        
        response = requests.post(
            endpoint,
            params=params,
            headers=headers,
            data=json.dumps(data)
        )
        
        return response.json()
    
    def send_button_template(self, recipient_id, text, buttons):
        """Send a button template message to a recipient"""
        endpoint = f"{self.base_url}/me/messages"
        params = {"access_token": self.page_access_token}
        headers = {"Content-Type": "application/json"}
        
        data = {
            "recipient": {"id": recipient_id},
            "messaging_type": "RESPONSE",
            "message": {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "button",
                        "text": text,
                        "buttons": buttons
                    }
                }
            }
        }
        
        response = requests.post(
            endpoint,
            params=params,
            headers=headers,
            data=json.dumps(data)
        )
        
        return response.json()
    
    def get_user_profile(self, user_id):
        """Get user profile information"""
        endpoint = f"{self.base_url}/{user_id}"
        params = {
            "access_token": self.page_access_token,
            "fields": "first_name,last_name,profile_pic"
        }
        
        response = requests.get(endpoint, params=params)
        return response.json()
    
    def mark_seen(self, recipient_id):
        """Mark message as seen"""
        endpoint = f"{self.base_url}/me/messages"
        params = {"access_token": self.page_access_token}
        headers = {"Content-Type": "application/json"}
        
        data = {
            "recipient": {"id": recipient_id},
            "sender_action": "mark_seen"
        }
        
        response = requests.post(
            endpoint,
            params=params,
            headers=headers,
            data=json.dumps(data)
        )
        
        return response.json()
        
    def setup_get_started_button(self):
        """Set up the Get Started button"""
        endpoint = f"{self.base_url}/me/messenger_profile"
        params = {"access_token": self.page_access_token}
        headers = {"Content-Type": "application/json"}
        
        data = {
            "get_started": {
                "payload": "GET_STARTED"
            }
        }
        
        response = requests.post(
            endpoint,
            params=params,
            headers=headers,
            data=json.dumps(data)
        )
        
        return response.json()
        
    def setup_greeting_text(self):
        """Set up the greeting text shown on the welcome screen"""
        endpoint = f"{self.base_url}/me/messenger_profile"
        params = {"access_token": self.page_access_token}
        headers = {"Content-Type": "application/json"}
        
        data = {
            "greeting": [
                {
                    "locale": "default",
                    "text": "Welcome to Swift Showings! 🎉 We make finding your next home easier and more affordable—without extra fees or hassles."
                }
            ]
        }
        
        response = requests.post(
            endpoint,
            params=params,
            headers=headers,
            data=json.dumps(data)
        )
        
        return response.json()
        
    def setup_persistent_menu(self):
        """Set up the persistent menu"""
        endpoint = f"{self.base_url}/me/messenger_profile"
        params = {"access_token": self.page_access_token}
        headers = {"Content-Type": "application/json"}
        
        data = {
            "persistent_menu": [
                {
                    "locale": "default",
                    "composer_input_disabled": False,
                    "call_to_actions": [
                        {
                            "type": "postback",
                            "title": "Find Home",
                            "payload": "FIND_HOME"
                        },
                        {
                            "type": "postback",
                            "title": "Get Help",
                            "payload": "GET_HELP"
                        },
                        {
                            "type": "postback",
                            "title": "Save Money",
                            "payload": "SAVE_MONEY"
                        },
                        {
                            "type": "postback",
                            "title": "Learn More",
                            "payload": "LEARN_MORE"
                        }
                    ]
                }
            ]
        }
        
        response = requests.post(
            endpoint,
            params=params,
            headers=headers,
            data=json.dumps(data)
        )
        
        return response.json()
    
    def send_welcome_message(self, recipient_id):
        """Send the welcome message with quick replies"""
        # First message
        self.send_text_message(
            recipient_id, 
            "Welcome to Swift Showings! 🎉 We make finding your next home easier and more affordable—without extra fees or hassles."
        )
        
        # Second message with quick replies
        quick_replies = ["Find Home", "Get Help", "Save Money", "Learn More"]
        self.send_quick_replies(
            recipient_id,
            "Choose an option below to get started:",
            quick_replies
        )
        
        return True
