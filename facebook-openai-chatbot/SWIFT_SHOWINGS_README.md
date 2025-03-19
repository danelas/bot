# Swift Showings Facebook Messenger Chatbot

This application provides a complete Facebook Messenger chatbot solution for Swift Showings, integrating with OpenAI's Assistant API and Google Sheets.

## Features

- **Welcome Flow**: Presents users with a friendly welcome message and quick reply options
- **Quick Reply Options**: Find Home, Get Help, Save Money, Learn More
- **OpenAI Assistant Integration**: Handles complex queries using OpenAI's powerful AI
- **Google Sheets Integration**: Records all conversations for review and analysis
- **Platform-Specific Content**: Supports special formatting for Facebook content

## Quick Start

Follow these steps to get up and running:

1. Copy `.env.example` to `.env` and fill in your API keys:
   ```
   cp .env.example .env
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your Facebook Page (see `FACEBOOK_SETUP.md`)

4. Set up your OpenAI Assistant (see `ASSISTANT_SETUP.md`)
   - Make sure to format responses with `#facebook` tags as shown in the setup guide

5. Set up Google Sheets for logging (see `GOOGLE_SHEETS_SETUP.md`)

6. Initialize the Messenger experience:
   ```
   python setup_messenger.py
   ```

7. Run the application locally for testing:
   ```
   python app.py
   ```

8. Use `test_assistant.py` to test the chatbot flow without Facebook:
   ```
   python test_assistant.py
   ```

## Swift Showings Conversation Flow

### Initial Welcome

When a user first messages the page, they receive:
1. Welcome message: "Welcome to Swift Showings! 🎉 We make finding your next home easier and more affordable—without extra fees or hassles."
2. Options prompt: "Choose an option below to get started:"
3. Quick reply options: Find Home, Get Help, Save Money, Learn More

### Quick Reply Responses

#### Find Home
Response: "Great! Let's find you a home. What city or neighborhood are you interested in?"
- Followed by conversation about user's home preferences

#### Get Help
Response: "I'm here to help! What specifically do you need assistance with?"
- Followed by support conversation

#### Save Money
Response: "We love saving you money! Swift Showings helps you save on fees that traditional agents charge. Would you like to learn more about our fee structure?"
- Followed by information about cost savings

#### Learn More
Response: "Swift Showings makes house hunting simple and affordable. We connect you directly with sellers and provide tools to streamline your search. What would you like to know more about?"
- Followed by general information

## Deployment

For production deployment instructions, see `DEPLOYMENT.md`.

## Important Notes

- The OpenAI Assistant should be configured to provide specific content for Facebook using the `#facebook` tag
- All conversations are saved to Google Sheets including user information
- The persistent menu provides quick access to the main options
- Users can type natural language queries at any time to interact with the OpenAI-powered assistant
