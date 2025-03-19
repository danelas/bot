# Setting Up Your OpenAI Assistant for the Facebook Chatbot

This guide will help you create and configure an OpenAI Assistant that works effectively with the Facebook Messenger chatbot.

## Create the Assistant in OpenAI Platform

1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Navigate to the "Assistants" section
3. Click "Create Assistant"

## Basic Configuration

Configure your assistant with the following:

1. **Name**: Choose a name for your assistant (e.g., "Facebook Page Assistant")
2. **Model**: Select a GPT model (GPT-4o is recommended for best performance)
3. **Description**: Add a description of what your assistant does

## Instructions for the Assistant

In the "Instructions" field, provide guidance for how your assistant should behave. Here's a template you can use:

```
You are a helpful assistant for [Your Business Name]'s Facebook Page. Your role is to assist users who message the page with questions, inquiries, and support.

## Response Format

For each response, you should provide content in the following format:

General response to the user's query.

#instagram
[Instagram-optimized version of your response with relevant hashtags]

#facebook
[Facebook-optimized version of your response]

## Guidelines:

1. Be friendly, helpful, and concise.
2. Represent the brand voice of [Your Business].
3. When users ask about products or services, provide accurate information based on the available knowledge.
4. For support inquiries, gather relevant information before attempting to solve the problem.
5. If you don't know something, admit it and offer to connect the user with a human representative if needed.
6. Include appropriate hashtags in the Instagram section.
7. Keep Facebook content shorter and more conversational.
8. Never share confidential information about the business or users.
9. If users ask questions that require recent information you don't have, explain your knowledge cutoff and offer alternatives.
10. For appointment bookings or reservations, collect all necessary details: name, date, time, service requested, and contact information.
```

Customize the instructions based on your specific business and use case.

## Knowledge Base (Optional)

If you want your assistant to have specific knowledge about your business:

1. In the "Knowledge" section, click "Add"
2. Upload relevant documents such as:
   - Product catalogs
   - FAQs
   - Service descriptions
   - Company policies
   - Price lists

## Capabilities

Enable the following capabilities:

1. ✅ Code Interpreter (if you want the assistant to be able to process data)
2. ✅ Retrieval (to use the knowledge files you uploaded)
3. ✅ Function calling (if you plan to add custom functions later)

## Testing Your Assistant

Before connecting to Facebook:

1. Test your assistant directly in the OpenAI platform
2. Try various types of questions related to your business
3. Check if the responses include both the general text and the platform-specific sections

## Getting Your Assistant ID

After creating your assistant:

1. From the Assistants dashboard, click on your assistant
2. Look for the "Assistant ID" (it will look something like "asst_abc123...")
3. Copy this ID and add it to your `.env` file as the `ASSISTANT_ID` value

## Additional Tips for Improving Your Assistant

1. **Regular Updates**: Update your assistant's knowledge files regularly to keep information current
2. **Analyze Conversations**: Review the saved conversations in Google Sheets to identify common questions or issues
3. **Refine Instructions**: Based on actual conversations, refine your instructions to improve response quality
4. **Custom Functions**: For advanced use cases, consider implementing custom functions that your assistant can call
