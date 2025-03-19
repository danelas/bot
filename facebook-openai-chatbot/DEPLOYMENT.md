# Deployment Guide: Facebook Messenger Chatbot with OpenAI Assistant

This guide will help you deploy your Facebook Messenger chatbot to a server where it can be accessible via the Internet, allowing Facebook to send webhook events to it.

## Prerequisites

- A VPS or cloud server (AWS, DigitalOcean, GCP, Azure, etc.)
- A domain name pointed to your server (optional but recommended)
- Basic knowledge of server administration and command line

## Deployment Options

### Option 1: Deploying with Gunicorn and Nginx

1. **Set up your server**:
   - Install Python 3.8+ and pip
   - Install Nginx: `sudo apt-get install nginx`
   - Set up a virtual environment: `python -m venv venv`
   - Activate it: `source venv/bin/activate`
   - Install dependencies: `pip install -r requirements.txt`
   - Install Gunicorn: `pip install gunicorn`

2. **Create a Gunicorn service file**:
   Create a file at `/etc/systemd/system/facebook-chatbot.service`:

   ```
   [Unit]
   Description=Facebook Chatbot Gunicorn Service
   After=network.target

   [Service]
   User=<your-username>
   Group=<your-group>
   WorkingDirectory=/path/to/facebook-openai-chatbot
   Environment="PATH=/path/to/facebook-openai-chatbot/venv/bin"
   ExecStart=/path/to/facebook-openai-chatbot/venv/bin/gunicorn --workers 3 --bind unix:facebook-chatbot.sock -m 007 app:app

   [Install]
   WantedBy=multi-user.target
   ```

3. **Configure Nginx**:
   Create a file at `/etc/nginx/sites-available/facebook-chatbot`:

   ```
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           include proxy_params;
           proxy_pass http://unix:/path/to/facebook-openai-chatbot/facebook-chatbot.sock;
       }
   }
   ```

   Enable the site:
   ```
   sudo ln -s /etc/nginx/sites-available/facebook-chatbot /etc/nginx/sites-enabled
   ```

4. **Set up SSL with Let's Encrypt**:
   ```
   sudo apt-get install certbot python3-certbot-nginx
   sudo certbot --nginx -d your-domain.com
   ```

5. **Start and enable services**:
   ```
   sudo systemctl start facebook-chatbot
   sudo systemctl enable facebook-chatbot
   sudo systemctl restart nginx
   ```

### Option 2: Using a Serverless Solution (AWS Lambda, Vercel, etc.)

For serverless deployments, here's how to set up on Vercel with Serverless Functions:

1. **Install Vercel CLI**:
   ```
   npm install -g vercel
   ```

2. **Create a `vercel.json` configuration file**:
   ```json
   {
     "version": 2,
     "builds": [
       { "src": "app.py", "use": "@vercel/python" }
     ],
     "routes": [
       { "src": "/(.*)", "dest": "app.py" }
     ]
   }
   ```

3. **Create a `requirements.txt` file** with your dependencies

4. **Deploy to Vercel**:
   ```
   vercel
   ```

### Option 3: Using a PaaS (Heroku, PythonAnywhere, etc.)

For Heroku deployment:

1. **Create a `Procfile`**:
   ```
   web: gunicorn app:app
   ```

2. **Install Heroku CLI and deploy**:
   ```
   heroku login
   heroku create your-app-name
   git push heroku main
   ```

3. **Set environment variables**:
   ```
   heroku config:set OPENAI_API_KEY=your_key
   heroku config:set ASSISTANT_ID=your_assistant_id
   heroku config:set FACEBOOK_PAGE_ACCESS_TOKEN=your_token
   heroku config:set FACEBOOK_VERIFY_TOKEN=your_verify_token
   ```

## Setting Up Secure Environment Variables

1. **Create a `.env` file** in your project root (never commit this to version control)
2. **Add all your sensitive values** as shown in `.env.example`
3. For Google Sheets, store the `google_credentials.json` file in your project directory

## Configuring Facebook Webhook

1. Go to the Facebook Developer Portal > Your App > Messenger > Settings
2. Under "Webhooks", click "Add Callback URL"
3. Enter your webhook URL (e.g., `https://your-domain.com/webhook`)
4. Enter your verify token (the one you set in your `.env` file)
5. Subscribe to the following webhook events:
   - messages
   - messaging_postbacks
   - messaging_optins

## Testing Your Deployment

1. Send a message to your Facebook Page
2. Check your server logs for any errors:
   ```
   sudo journalctl -u facebook-chatbot.service
   ```
3. Test your webhook endpoint using curl:
   ```
   curl -X GET "https://your-domain.com/webhook?hub.verify_token=YOUR_VERIFY_TOKEN&hub.challenge=CHALLENGE_ACCEPTED&hub.mode=subscribe"
   ```

## Monitoring and Maintenance

1. Set up logging to a file:
   ```python
   import logging
   logging.basicConfig(filename='chatbot.log', level=logging.INFO)
   ```

2. Consider using a monitoring service like UptimeRobot to ensure your webhook is always accessible

3. Regularly check your Google Sheets to ensure conversations are being logged properly
