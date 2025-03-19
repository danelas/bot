import os
import time
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# OpenAI Configuration
openai.api_key = os.getenv("OPENAI_API_KEY")

class OpenAIHelper:
    def __init__(self):
        self.conversations = {}  # Store conversation history by user_id
        
        # Define the system message with Swift Showings context
        self.system_message = """You are a helpful assistant for Swift Showings, a real estate service that connects home buyers directly with sellers to save on agent fees. 
Swift Showings helps users find homes, schedule viewings, and save money during the home buying process.

When asked about real estate, provide helpful and accurate information. You should be knowledgeable about buying, selling, and renting properties.

If users ask for specific property listings or showings, guide them to use the Find Home feature available through the chat interface.

For any questions about savings, mortgage options, or financial aspects of home buying, provide general guidance and direct them to the Save Money feature.

When users need assistance with property issues, repairs, legal matters or other help topics, recommend the Get Help feature.

Be friendly, professional, and helpful at all times.

If you need to include different content for social media platforms, use hashtags like #facebook or #instagram followed by platform-specific content.
"""
    
    def get_or_create_conversation(self, user_id):
        """Get existing conversation for user or create a new one"""
        if user_id not in self.conversations:
            self.conversations[user_id] = [
                {"role": "system", "content": self.system_message}
            ]
        return self.conversations[user_id]
    
    def add_message_to_conversation(self, user_id, message_content):
        """Add a new user message to the conversation"""
        conversation = self.get_or_create_conversation(user_id)
        conversation.append({"role": "user", "content": message_content})
        return conversation
    
    def process_message(self, user_id, message_content):
        """Process a message using the OpenAI Chat Completion API"""
        # Add Swift Showings context to the message if it appears to be a real estate query
        enhanced_message = self._enhance_message_with_context(message_content)
        
        # Get the conversation history and add the new message
        conversation = self.add_message_to_conversation(user_id, enhanced_message)
        
        # Keep conversation size manageable (limit to last 10 messages)
        if len(conversation) > 11:  # system message + 10 exchange messages
            # Always keep the system message at position 0
            system_message = conversation[0]
            conversation = [system_message] + conversation[-10:]
        
        try:
            # Call the OpenAI Chat Completion API
            response = openai.ChatCompletion.create(
                model="gpt-4",  
                messages=conversation,
                max_tokens=1000,
                temperature=0.7
            )
            
            # Extract the assistant's response
            assistant_message = response.choices[0].message['content']
            
            # Add the assistant's response to the conversation history
            conversation.append({"role": "assistant", "content": assistant_message})
            
            # Process the response for platform-specific content
            return self._process_response(assistant_message)
            
        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            return {"text": "I'm sorry, but I encountered an error processing your request."}
    
    def _process_response(self, response_text):
        """Process the response to extract platform-specific content"""
        # Default values
        instagram_content = response_text
        facebook_content = response_text
        
        # Look for platform-specific tags in the response
        if "#instagram" in response_text.lower():
            parts = response_text.split("#instagram")
            if len(parts) > 1:
                instagram_content = parts[1].strip()
                # Clean up the main response text
                response_text = parts[0].strip()
                
        if "#facebook" in response_text.lower():
            parts = response_text.split("#facebook")
            if len(parts) > 1:
                facebook_content = parts[1].strip()
                # If we haven't already cleaned the response from Instagram tag
                if "#instagram" not in response_text.lower():
                    response_text = parts[0].strip()
        
        # Clean up any remaining tags in the messages
        instagram_content = self._clean_tags(instagram_content)
        facebook_content = self._clean_tags(facebook_content)
        response_text = self._clean_tags(response_text)
        
        # Format messages specifically for Swift Showings context
        facebook_content = self._format_for_swift_showings(facebook_content)
        
        return {
            "text": response_text,
            "instagram_content": instagram_content,
            "facebook_content": facebook_content
        }
    
    def _clean_tags(self, content):
        """Remove any social media tags from the content"""
        if not content:
            return content
            
        # List of tags to clean
        tags = ["#facebook", "#instagram", "#twitter", "#linkedin"]
        
        # Remove each tag
        for tag in tags:
            if tag in content.lower():
                # Split on the tag and take everything after it
                parts = content.lower().split(tag)
                if len(parts) > 1:
                    # If tag is at the start, take everything after it
                    content = content[len(parts[0]) + len(tag):].strip()
                else:
                    # If tag is at the end, remove it
                    content = content[:content.lower().find(tag)].strip()
        
        return content
    
    def _format_for_swift_showings(self, content):
        """Format content for Swift Showings real estate context"""
        if not content:
            return content
            
        # Add Swift Showings branding if not present
        if "Swift Showings" not in content and "swift showings" not in content.lower():
            # Don't add branding if content is very short (likely just a quick reply)
            if len(content) > 50:
                content += "\n\nSwift Showings - Real Estate Made Simple"
                
        return content
    
    def _enhance_message_with_context(self, message):
        """Add Swift Showings context to the message if appropriate"""
        # List of real estate related keywords
        real_estate_keywords = [
            "home", "house", "property", "real estate", "realtor", "agent", 
            "buy", "purchase", "rent", "apartment", "condo", "listing",
            "mortgage", "loan", "closing", "offer", "bid", "price", "cost",
            "fee", "bedroom", "bathroom", "square foot", "sqft", "neighborhood",
            "location", "address", "tour", "showing", "open house", "sell"
        ]
        
        # Check if message contains real estate keywords
        message_lower = message.lower()
        contains_real_estate_term = any(keyword in message_lower for keyword in real_estate_keywords)
        
        # If it contains real estate keywords, add context
        if contains_real_estate_term and len(message) > 10:
            # Don't modify very short messages or quick replies
            return f"{message}\n\n[Context: This is a user of Swift Showings, a service that connects home buyers directly with sellers to save on agent fees. Swift Showings helps users find homes, schedule viewings, and save money during the home buying process.]"
        
        return message
