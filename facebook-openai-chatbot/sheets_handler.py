import os
import time
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class GoogleSheetsHandler:
    def __init__(self):
        # Get configuration from environment variables
        credentials_file = os.getenv("GOOGLE_SHEETS_CREDENTIALS_FILE")
        self.sheet_id = os.getenv("GOOGLE_SHEETS_ID")
        
        # Verify credentials are available
        if not credentials_file or not os.path.exists(credentials_file):
            raise Exception(f"Google Sheets credentials file not found: {credentials_file}")
        
        if not self.sheet_id:
            raise Exception("GOOGLE_SHEETS_ID environment variable is not set")
        
        # Set up credentials
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)
        
        # Create client
        self.client = gspread.authorize(credentials)
        
        # Open the spreadsheet
        self.spreadsheet = self.client.open_by_key(self.sheet_id)
        
        # Initialize sheets
        self._init_conversation_sheet()
        self._init_home_preferences_sheet()
        self._init_help_requests_sheet()
    
    def _init_conversation_sheet(self):
        """Initialize or get the conversation worksheet"""
        try:
            self.conversation_sheet = self.spreadsheet.worksheet("Conversations")
        except gspread.exceptions.WorksheetNotFound:
            # Create sheet with headers
            self.conversation_sheet = self.spreadsheet.add_worksheet(
                title="Conversations", rows="1000", cols="7"
            )
            self.conversation_sheet.append_row([
                "Timestamp", "User ID", "User Name", "Message", 
                "Response", "Platform", "Thread ID"
            ])
    
    def _init_home_preferences_sheet(self):
        """Initialize or get the home preferences worksheet"""
        try:
            self.home_preferences_sheet = self.spreadsheet.worksheet("Home Preferences")
        except gspread.exceptions.WorksheetNotFound:
            # Create sheet with headers
            self.home_preferences_sheet = self.spreadsheet.add_worksheet(
                title="Home Preferences", rows="1000", cols="9"
            )
            self.home_preferences_sheet.append_row([
                "Timestamp", "User ID", "User Name", "Type", 
                "Property Type", "Budget", "Location", 
                "Financing/Roommate", "Notes"
            ])
    
    def _init_help_requests_sheet(self):
        """Initialize or get the help requests worksheet"""
        try:
            self.help_requests_sheet = self.spreadsheet.worksheet("Help Requests")
        except gspread.exceptions.WorksheetNotFound:
            # Create sheet with headers
            self.help_requests_sheet = self.spreadsheet.add_worksheet(
                title="Help Requests", rows="1000", cols="9"
            )
            self.help_requests_sheet.append_row([
                "Timestamp", "User ID", "User Name", "Type", 
                "Category", "Details", "Status", "Follow-up", "Notes"
            ])
    
    def save_conversation(self, user_id, user_name, message, response, platform, thread_id=None):
        """
        Save a conversation to Google Sheets
        """
        try:
            now = time.strftime("%Y-%m-%d %H:%M:%S")
            
            # Append the conversation
            self.conversation_sheet.append_row([
                now, user_id, user_name, message, response, platform, thread_id or ""
            ])
            
            return True
        except Exception as e:
            print(f"Error saving conversation to Google Sheets: {e}")
            return False
    
    def save_home_preferences(self, row_data):
        """
        Save home preferences to Google Sheets
        
        row_data should be an array with:
        [timestamp, user_id, user_name, type, property_type, budget, location, financing/roommate, notes]
        """
        try:
            # Append the preferences
            self.home_preferences_sheet.append_row(row_data)
            return True
        except Exception as e:
            print(f"Error saving home preferences to Google Sheets: {e}")
            return False
    
    def save_help_request(self, row_data):
        """
        Save a help request to the Help Requests worksheet
        """
        try:
            # Get Help Requests worksheet, create if doesn't exist
            help_worksheet = self._get_or_create_worksheet("Help Requests", [
                "Timestamp", "User ID", "User Name", "Type",
                "Help Category", "Details", "Status", "Follow-up", "Notes"
            ])
            
            # Append data
            help_worksheet.append_row(row_data)
            return True
        except Exception as e:
            print(f"Error saving help request to Google Sheets: {e}")
            return False
    
    def save_money_request(self, row_data):
        """
        Save a money-saving request to the Money Requests worksheet
        """
        try:
            # Get Money Requests worksheet, create if doesn't exist
            money_worksheet = self._get_or_create_worksheet("Money Requests", [
                "Timestamp", "User ID", "User Name", "Type",
                "Savings Category", "Details", "Status", "Follow-up", "Notes"
            ])
            
            # Append data
            money_worksheet.append_row(row_data)
            return True
        except Exception as e:
            print(f"Error saving money request to Google Sheets: {e}")
            return False
    
    def _get_or_create_worksheet(self, worksheet_name, headers=None):
        """
        Get or create a worksheet in the Google Sheet
        """
        try:
            # Try to get the worksheet
            worksheet = self.spreadsheet.worksheet(worksheet_name)
            return worksheet
        except gspread.exceptions.WorksheetNotFound:
            # Create the worksheet if it doesn't exist
            worksheet = self.spreadsheet.add_worksheet(title=worksheet_name, rows=1000, cols=20)
            
            # Add headers if provided
            if headers:
                worksheet.append_row(headers)
                
            return worksheet
    
    def get_conversation_history(self, user_id, limit=10):
        """
        Get conversation history for a specific user
        """
        try:
            all_records = self.conversation_sheet.get_all_records()
            
            # Filter for the specific user
            user_records = [
                record for record in all_records 
                if record.get("User ID") == user_id
            ]
            
            # Sort by timestamp (newest first)
            user_records.sort(
                key=lambda x: datetime.strptime(x.get("Timestamp"), "%Y-%m-%d %H:%M:%S"), 
                reverse=True
            )
            
            # Limit the number of records
            limited_records = user_records[:limit]
            
            return limited_records
        except Exception as e:
            print(f"Error getting conversation history: {e}")
            return []
