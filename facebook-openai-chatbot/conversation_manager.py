import json
import os
import time
from sheets_handler import GoogleSheetsHandler

class ConversationState:
    """
    Class to manage conversation state for multi-step flows
    """
    def __init__(self, user_id):
        self.user_id = user_id
        self.state_data = {
            "current_flow": None,  # e.g., "find_home_buy", "find_home_rent"
            "step": None,  # Current step in the flow
            "data": {},  # User's answers to questions
            "timestamp": time.time()
        }
    
    def set_flow(self, flow_name, step=1):
        """Set the active conversation flow"""
        self.state_data["current_flow"] = flow_name
        self.state_data["step"] = step
        self.state_data["timestamp"] = time.time()
        return self
    
    def next_step(self):
        """Move to the next step in the flow"""
        if self.state_data["step"] is not None:
            self.state_data["step"] += 1
        return self
    
    def get_step(self):
        """Get the current step number"""
        return self.state_data["step"]
    
    def get_flow(self):
        """Get the current flow name"""
        return self.state_data["current_flow"]
    
    def store_answer(self, key, value):
        """Store a user's answer"""
        self.state_data["data"][key] = value
        return self
    
    def get_answer(self, key, default=None):
        """Get a stored answer"""
        return self.state_data["data"].get(key, default)
    
    def get_all_data(self):
        """Get all stored answers"""
        return self.state_data["data"]
    
    def reset(self):
        """Reset the conversation state"""
        self.state_data = {
            "current_flow": None,
            "step": None,
            "data": {},
            "timestamp": time.time()
        }
        return self

class ConversationManager:
    """
    Manager for handling conversation state and flows
    """
    def __init__(self):
        self.conversations = {}
        self.sheets_handler = GoogleSheetsHandler()
    
    def get_state(self, user_id):
        """Get the conversation state for a user"""
        if user_id not in self.conversations:
            self.conversations[user_id] = ConversationState(user_id)
        return self.conversations[user_id]
    
    def handle_buy_flow(self, user_id, user_name, message, step=None):
        """
        Handle the "Find Home > Buy" conversation flow
        Returns (response_text, quick_replies or None)
        """
        state = self.get_state(user_id)
        
        # If step is explicitly provided, override the state
        if step is not None:
            state.set_flow("find_home_buy", step)
        
        current_step = state.get_step()
        
        # Step 1: Ask about home type
        if current_step == 1:
            state.next_step()
            return ("What type of home are you interested in?", 
                    ["House", "Condo", "Apartment", "Townhome", "Other"])
        
        # Step 2: Store home type and ask about budget
        elif current_step == 2:
            state.store_answer("home_type", message)
            state.next_step()
            return ("What is your budget range?", 
                    ["$100k-$200k", "$200k-$300k", "$300k-$400k", "$400k-$500k", "$500k+"])
        
        # Step 3: Store budget and ask about location
        elif current_step == 3:
            state.store_answer("budget", message)
            state.next_step()
            return ("What location are you considering? Please type the city and state.", None)
        
        # Step 4: Store location and ask about financing
        elif current_step == 4:
            state.store_answer("location", message)
            state.next_step()
            return ("Do you have financing or need assistance?", 
                    ["Yes, I'm pre-approved", "No, I need financing help"])
        
        # Step 5: Store financing answer and complete the flow
        elif current_step == 5:
            state.store_answer("financing", message)
            
            # Save all data to Google Sheets
            all_data = state.get_all_data()
            self.save_home_preferences(user_id, user_name, "buy", all_data)
            
            # Reset the flow for next time
            state.reset()
            
            return (f"Thank you! We've recorded your preferences for a {all_data.get('home_type')} in {all_data.get('location')} within budget {all_data.get('budget')}.\n\nOur team will review available properties and get back to you soon. Is there anything specific you're looking for in your new home?", None)
    
    def handle_rent_flow(self, user_id, user_name, message, step=None):
        """
        Handle the "Find Home > Rent" conversation flow
        Returns (response_text, quick_replies or None)
        """
        state = self.get_state(user_id)
        
        # If step is explicitly provided, override the state
        if step is not None:
            state.set_flow("find_home_rent", step)
        
        current_step = state.get_step()
        
        # Step 1: Ask about property type
        if current_step == 1:
            state.next_step()
            return ("What kind of property are you looking for?", 
                    ["Apartment", "House", "Townhome", "Other"])
        
        # Step 2: Store property type and ask about budget
        elif current_step == 2:
            state.store_answer("property_type", message)
            state.next_step()
            return ("What's your monthly budget?", 
                    ["$500-$1000", "$1000-$1500", "$1500-$2000", "$2000-$2500", "$2500+"])
        
        # Step 3: Store budget and ask about location
        elif current_step == 3:
            state.store_answer("budget", message)
            state.next_step()
            return ("What area are you interested in? Please type the city and state.", None)
        
        # Step 4: Store location and ask about roommate service
        elif current_step == 4:
            state.store_answer("location", message)
            state.next_step()
            return ("Do you need a roommate-finding service?", 
                    ["Yes", "No"])
        
        # Step 5: Store roommate answer and complete the flow
        elif current_step == 5:
            state.store_answer("roommate_service", message)
            
            # Save all data to Google Sheets
            all_data = state.get_all_data()
            self.save_home_preferences(user_id, user_name, "rent", all_data)
            
            # Reset the flow for next time
            state.reset()
            
            return (f"Thank you! We've recorded your preferences for a {all_data.get('property_type')} to rent in {all_data.get('location')} within a monthly budget of {all_data.get('budget')}.\n\nOur rental specialists will review available properties and get back to you soon. Is there anything specific you're looking for in your new home?", None)
    
    def handle_buy_or_rent(self, user_id, message):
        """Handle the buy vs rent decision and set up the next flow"""
        state = self.get_state(user_id)
        
        if message.lower() == "buy":
            state.set_flow("find_home_buy", 1)
            return self.handle_buy_flow(user_id, None, None, 1)
        elif message.lower() == "rent":
            state.set_flow("find_home_rent", 1)
            return self.handle_rent_flow(user_id, None, None, 1)
        else:
            # Invalid response
            return ("Please choose Buy or Rent to continue.", ["Buy", "Rent"])
    
    def start_get_help_flow(self, user_id):
        """Start the Get Help flow"""
        state = self.get_state(user_id)
        state.set_flow("get_help")
        return ("How can we assist you today?", 
                ["Real Estate Questions", "Maintenance & Repairs", "Legal Help", "Other"])
    
    def handle_help_category(self, user_id, user_name, message, step=None):
        """Handle the initial category selection for help"""
        state = self.get_state(user_id)
        
        # Store the help category
        state.store_answer("help_category", message)
        
        # Route to the appropriate flow based on the category
        if message == "Real Estate Questions":
            state.set_flow("help_real_estate", 1)
            return self.handle_real_estate_flow(user_id, user_name, None, 1)
        elif message == "Maintenance & Repairs":
            state.set_flow("help_maintenance", 1)
            return self.handle_maintenance_flow(user_id, user_name, None, 1)
        elif message == "Legal Help":
            state.set_flow("help_legal", 1)
            return self.handle_legal_flow(user_id, user_name, None, 1)
        elif message == "Other":
            state.set_flow("help_other", 1)
            return self.handle_other_help_flow(user_id, user_name, None, 1)
        else:
            # Invalid category
            return ("Please select one of the following help categories:", 
                    ["Real Estate Questions", "Maintenance & Repairs", "Legal Help", "Other"])
    
    def handle_real_estate_flow(self, user_id, user_name, message, step=None):
        """
        Handle the "Get Help > Real Estate Questions" flow
        Returns (response_text, quick_replies or None)
        """
        state = self.get_state(user_id)
        
        # If step is explicitly provided, override the state
        if step is not None:
            state.set_flow("help_real_estate", step)
        
        current_step = state.get_step()
        
        # Step 1: Ask about specific real estate topic
        if current_step == 1:
            state.next_step()
            return ("What's your question about?", 
                    ["Buying", "Selling", "Renting", "Financing"])
        
        # Step 2: Store topic and provide appropriate response
        elif current_step == 2:
            state.store_answer("real_estate_topic", message)
            state.next_step()
            
            # Different responses based on the topic
            responses = {
                "Buying": "Buying a home is a major decision. Swift Showings can help you navigate the process without the high fees of traditional agents. Some key things to consider are your budget, location preferences, and financing options. Would you like to speak with one of our home buying experts?",
                
                "Selling": "Swift Showings can help you sell your home with lower fees than traditional agents. We provide professional photos, listing services, and connect you directly with interested buyers. Would you like to speak with one of our home selling experts?",
                
                "Renting": "Finding the right rental property can be challenging. Swift Showings can help you find apartments, houses, or townhomes that match your budget and preferences. We also offer roommate-finding services if needed. Would you like to speak with one of our rental specialists?",
                
                "Financing": "Financing a home purchase involves understanding mortgage options, interest rates, and qualification requirements. Swift Showings partners with several lenders who can help you explore your options. Would you like to speak with one of our financing partners?"
            }
            
            topic = state.get_answer("real_estate_topic")
            response = responses.get(topic, "We'd be happy to answer your real estate questions. Would you like to speak with one of our experts?")
            
            return (response, ["Yes, connect me", "No thanks"])
        
        # Step 3: Store whether they want to connect and complete the flow
        elif current_step == 3:
            state.store_answer("wants_connection", message)
            
            # Save all data to Google Sheets
            all_data = state.get_all_data()
            self.save_help_request(user_id, user_name, all_data)
            
            # Reset the flow for next time
            state.reset()
            
            if message == "Yes, connect me":
                return ("Great! One of our experts will reach out to you shortly via Messenger. Is there anything specific you'd like them to prepare for your conversation?", None)
            else:
                return ("No problem! If you have any other questions about real estate, feel free to ask anytime. Is there something else I can help you with today?", None)
    
    def handle_maintenance_flow(self, user_id, user_name, message, step=None):
        """
        Handle the "Get Help > Maintenance & Repairs" flow
        Returns (response_text, quick_replies or None)
        """
        state = self.get_state(user_id)
        
        # If step is explicitly provided, override the state
        if step is not None:
            state.set_flow("help_maintenance", step)
        
        current_step = state.get_step()
        
        # Step 1: Ask about DIY or Professional
        if current_step == 1:
            state.next_step()
            return ("Are you looking for DIY solutions or a professional service?", 
                    ["DIY", "Professional"])
        
        # Step 2: Store preference and provide appropriate response
        elif current_step == 2:
            state.store_answer("maintenance_preference", message)
            state.next_step()
            
            if message == "DIY":
                return ("What type of maintenance issue are you trying to address?", 
                        ["Plumbing", "Electrical", "HVAC", "Structural", "Other"])
            else:  # Professional
                return ("What type of professional service do you need?", 
                        ["Plumber", "Electrician", "HVAC Technician", "Contractor", "Other"])
        
        # Step 3: Store the issue type and provide relevant information
        elif current_step == 3:
            state.store_answer("maintenance_issue", message)
            state.next_step()
            
            preference = state.get_answer("maintenance_preference")
            issue = state.get_answer("maintenance_issue")
            
            if preference == "DIY":
                # DIY guidance based on issue type
                diy_responses = {
                    "Plumbing": "For common plumbing issues, we recommend checking for leaks at pipe connections, ensuring proper water pressure, and using plungers for simple clogs. Would you like us to send you our DIY plumbing troubleshooting guide?",
                    
                    "Electrical": "For electrical issues, always prioritize safety. Check if the issue is isolated to one circuit by examining your breaker panel. For simple fixture issues, ensure the power is OFF before attempting any work. Would you like us to send you our DIY electrical safety guide?",
                    
                    "HVAC": "For HVAC maintenance, regularly replace filters, ensure vents are unblocked, and check thermostat settings. Simple issues can often be resolved by cleaning components and ensuring proper airflow. Would you like us to send you our HVAC maintenance checklist?",
                    
                    "Structural": "For minor structural issues like small cracks or loose fixtures, monitoring the problem is important. Document with photos to track any changes. Would you like us to send you our guide for identifying serious vs. minor structural concerns?",
                    
                    "Other": "We have various DIY guides for home maintenance and repairs. What specific issue are you trying to address?"
                }
                
                response = diy_responses.get(issue, "We have various DIY guides that might help. Would you like us to send you some resources?")
                return (response, ["Yes, send guide", "No thanks"])
                
            else:  # Professional
                # Professional referral based on issue type
                pro_responses = {
                    "Plumber": "We work with licensed plumbers who can handle everything from leaks to installations. Our network of professionals offers competitive rates and quality service. Would you like us to recommend a plumber in your area?",
                    
                    "Electrician": "Our network includes certified electricians who can handle repairs, installations, and inspections. They offer competitive rates and reliable service. Would you like us to recommend an electrician in your area?",
                    
                    "HVAC Technician": "We partner with HVAC specialists who can handle maintenance, repairs, and installations for heating and cooling systems. Would you like us to recommend an HVAC technician in your area?",
                    
                    "Contractor": "Our contractor network includes professionals for renovations, repairs, and custom work. They offer fair pricing and quality craftsmanship. Would you like us to recommend a contractor in your area?",
                    
                    "Other": "We have a wide network of home service professionals. What specific type of service provider do you need?"
                }
                
                response = pro_responses.get(issue, "We can recommend qualified professionals for your needs. Would you like us to connect you with a service provider?")
                return (response, ["Yes, recommend", "No thanks"])
        
        # Step 4: Store their response and finalize
        elif current_step == 4:
            state.store_answer("wants_resources", message)
            
            # Save all data to Google Sheets
            all_data = state.get_all_data()
            self.save_help_request(user_id, user_name, all_data)
            
            # Reset the flow for next time
            state.reset()
            
            preference = all_data.get("maintenance_preference")
            if message.startswith("Yes"):
                if preference == "DIY":
                    return ("We'll send you the relevant DIY guide via Messenger shortly. If you find you need professional help after trying the DIY approach, just let us know. Is there anything else you need help with today?", None)
                else:  # Professional
                    return ("We'll have one of our service partners contact you soon to provide a quote and schedule service. Is there anything specific about your maintenance needs that we should share with them?", None)
            else:
                return ("No problem! If you need maintenance or repair assistance in the future, we're here to help. Is there something else I can assist you with today?", None)
    
    def handle_legal_flow(self, user_id, user_name, message, step=None):
        """
        Handle the "Get Help > Legal Help" flow
        Returns (response_text, quick_replies or None)
        """
        state = self.get_state(user_id)
        
        # If step is explicitly provided, override the state
        if step is not None:
            state.set_flow("help_legal", step)
        
        current_step = state.get_step()
        
        # Step 1: Ask about legal topic
        if current_step == 1:
            state.next_step()
            return ("Do you need help with contracts, tenant rights, or something else?", 
                    ["Contracts", "Tenant Rights", "Other"])
        
        # Step 2: Store topic and provide appropriate response
        elif current_step == 2:
            state.store_answer("legal_topic", message)
            state.next_step()
            
            # Different responses based on the topic
            legal_responses = {
                "Contracts": "Real estate contracts can be complex legal documents. While we can provide general information, specific legal advice should come from a qualified attorney. We can offer general guidance on standard contract terms and what to look for. Would you like us to connect you with a real estate attorney?",
                
                "Tenant Rights": "Tenant rights vary by location, but generally cover issues like security deposits, maintenance responsibilities, privacy, and eviction procedures. We can provide general information, but specific legal advice requires an attorney. Would you like us to connect you with a tenant rights specialist?",
                
                "Other": "Legal matters in real estate can cover many areas. To provide the most helpful guidance, could you tell us more about your specific legal concern?"
            }
            
            topic = state.get_answer("legal_topic")
            response = legal_responses.get(topic, "For specific legal advice, we recommend consulting with a qualified attorney. Would you like us to connect you with a real estate legal specialist?")
            
            if topic == "Other":
                return (response, None)  # Free text response
            else:
                return (response, ["Yes, connect me", "Just general info"])
        
        # Step 3: Store their response or get more details for "Other"
        elif current_step == 3:
            legal_topic = state.get_answer("legal_topic")
            
            if legal_topic == "Other":
                # Store their specific legal concern
                state.store_answer("specific_legal_concern", message)
                state.next_step()
                return ("Thank you for explaining your concern. While we can provide general information, specific legal advice should come from a qualified attorney. Would you like us to connect you with a legal specialist who can help with this matter?", 
                        ["Yes, connect me", "Just general info"])
            else:
                # Store whether they want a referral
                state.store_answer("wants_legal_referral", message)
                
                # Save all data to Google Sheets
                all_data = state.get_all_data()
                self.save_help_request(user_id, user_name, all_data)
                
                # Reset the flow for next time
                state.reset()
                
                if message == "Yes, connect me":
                    return ("We'll have a legal specialist contact you soon via Messenger. They can provide more specific guidance based on your situation and location. Is there anything else about your legal concern that we should share with them?", None)
                else:
                    return ("We understand. For general information, it's important to know that real estate legal matters are governed by both state and local laws. We recommend researching the specific regulations for your location or consulting free legal resources available through housing authorities. Is there something specific you'd like to understand better?", None)
        
        # Step 4: For "Other" path, store whether they want a referral
        elif current_step == 4:
            state.store_answer("wants_legal_referral", message)
            
            # Save all data to Google Sheets
            all_data = state.get_all_data()
            self.save_help_request(user_id, user_name, all_data)
            
            # Reset the flow for next time
            state.reset()
            
            if message == "Yes, connect me":
                return ("We'll have a legal specialist contact you soon via Messenger. They can provide more specific guidance based on your situation and location. Is there anything else about your legal concern that we should share with them?", None)
            else:
                return ("We understand. For general information, it's important to know that real estate legal matters are governed by both state and local laws. We recommend researching the specific regulations for your location or consulting free legal resources available through housing authorities. Is there something specific you'd like to understand better?", None)
    
    def handle_other_help_flow(self, user_id, user_name, message, step=None):
        """
        Handle the "Get Help > Other" flow
        Returns (response_text, quick_replies or None)
        """
        state = self.get_state(user_id)
        
        # If step is explicitly provided, override the state
        if step is not None:
            state.set_flow("help_other", step)
        
        current_step = state.get_step()
        
        # Step 1: Ask about their specific question
        if current_step == 1:
            state.next_step()
            return ("Please type your question or describe what you need help with, and we'll connect you with a live agent who can assist you.", None)
        
        # Step 2: Store their question and complete
        elif current_step == 2:
            state.store_answer("other_question", message)
            
            # Save all data to Google Sheets
            all_data = state.get_all_data()
            self.save_help_request(user_id, user_name, all_data)
            
            # Reset the flow for next time
            state.reset()
            
            return ("Thank you for your question. We've recorded it and will have a live agent follow up with you as soon as possible, usually within 1 business day. Is there anything else you'd like to add to your request?", None)
    
    def save_help_request(self, user_id, user_name, data):
        """Save help request to Google Sheets"""
        try:
            # Format the data for storage
            now = time.strftime("%Y-%m-%d %H:%M:%S")
            
            # Get main category
            category = data.get("help_category", "Unknown")
            
            # Build details string based on the category
            if category == "Real Estate Questions":
                details = f"Topic: {data.get('real_estate_topic', 'N/A')}, Connect: {data.get('wants_connection', 'N/A')}"
            elif category == "Maintenance & Repairs":
                details = f"Preference: {data.get('maintenance_preference', 'N/A')}, Issue: {data.get('maintenance_issue', 'N/A')}, Resources: {data.get('wants_resources', 'N/A')}"
            elif category == "Legal Help":
                topic = data.get('legal_topic', 'N/A')
                if topic == "Other":
                    details = f"Topic: Other - {data.get('specific_legal_concern', 'N/A')}, Referral: {data.get('wants_legal_referral', 'N/A')}"
                else:
                    details = f"Topic: {topic}, Referral: {data.get('wants_legal_referral', 'N/A')}"
            elif category == "Other":
                details = f"Question: {data.get('other_question', 'N/A')}"
            else:
                details = "No specific details provided"
            
            # Format the row
            row_data = [
                now,                  # Timestamp
                user_id,              # User ID
                user_name,            # User Name
                "Help Request",       # Type
                category,             # Help Category
                details,              # Details
                "Pending",            # Status
                "",                   # Follow-up
                ""                    # Notes
            ]
            
            # Save to sheets
            if hasattr(self.sheets_handler, 'save_help_request'):
                return self.sheets_handler.save_help_request(row_data)
            else:
                # Fall back to general method if specific one doesn't exist
                return self.sheets_handler.save_home_preferences(row_data)
                
        except Exception as e:
            print(f"Error saving help request: {e}")
            return False
    
    def start_save_money_flow(self, user_id):
        """Start the Save Money flow"""
        state = self.get_state(user_id)
        state.set_flow("save_money")
        return ("What type of savings are you looking for?", 
                ["Lower Mortgage Payments", "Reduce Utility Bills", "Home Insurance Discounts", "Tax Benefits"])
    
    def handle_save_money_category(self, user_id, user_name, message, step=None):
        """Handle the initial category selection for saving money"""
        state = self.get_state(user_id)
        
        # Store the savings category
        state.store_answer("savings_category", message)
        
        # Route to the appropriate flow based on the category
        if message == "Lower Mortgage Payments":
            state.set_flow("savings_mortgage", 1)
            return self.handle_mortgage_flow(user_id, user_name, None, 1)
        elif message == "Reduce Utility Bills":
            state.set_flow("savings_utility", 1)
            return self.handle_utility_flow(user_id, user_name, None, 1)
        elif message == "Home Insurance Discounts":
            state.set_flow("savings_insurance", 1)
            return self.handle_insurance_flow(user_id, user_name, None, 1)
        elif message == "Tax Benefits":
            state.set_flow("savings_tax", 1)
            return self.handle_tax_flow(user_id, user_name, None, 1)
        else:
            # Invalid category
            return ("Please select one of the following savings categories:", 
                    ["Lower Mortgage Payments", "Reduce Utility Bills", "Home Insurance Discounts", "Tax Benefits"])
    
    def handle_mortgage_flow(self, user_id, user_name, message, step=None):
        """
        Handle the "Save Money > Lower Mortgage Payments" flow
        Returns (response_text, quick_replies or None)
        """
        state = self.get_state(user_id)
        
        # If step is explicitly provided, override the state
        if step is not None:
            state.set_flow("savings_mortgage", step)
        
        current_step = state.get_step()
        
        # Step 1: Ask if refinancing or new loan
        if current_step == 1:
            state.next_step()
            return ("Are you refinancing or looking for a new loan?", 
                    ["Refinance", "New Loan"])
        
        # Step 2: Store answer and provide lender options
        elif current_step == 2:
            state.store_answer("mortgage_type", message)
            state.next_step()
            
            response = ""
            if message == "Refinance":
                response = "Refinancing can be a great way to lower your monthly payments. Our recommended lenders for refinancing include:\n\n" + \
                           "• SwiftRate Mortgage: Specializing in quick refinancing with competitive rates\n" + \
                           "• HomeSaver Loans: Offering no-fee refinancing options\n" + \
                           "• EasyFi: Digital-first refinancing with streamlined approval process\n\n" + \
                           "Would you like to connect with a mortgage expert to discuss your refinancing options?"
            else:  # New Loan
                response = "Finding the right mortgage for a new home is crucial. Our recommended lenders include:\n\n" + \
                           "• FirstTime Mortgage: Specializing in first-time homebuyer programs\n" + \
                           "• ValueRate Home Loans: Offering competitive rates with flexible terms\n" + \
                           "• SwiftApproval: Known for their quick pre-approval process\n\n" + \
                           "Would you like to connect with a mortgage expert to discuss your options?"
            
            return (response, ["Yes, connect me", "No thanks"])
        
        # Step 3: Store if they want to connect and complete
        elif current_step == 3:
            state.store_answer("wants_mortgage_expert", message)
            
            # Save all data to Google Sheets
            all_data = state.get_all_data()
            self.save_money_request(user_id, user_name, all_data)
            
            # Reset the flow for next time
            state.reset()
            
            if message == "Yes, connect me":
                return ("Great! One of our mortgage specialists will reach out to you shortly. They'll help you explore the best options to lower your payments. Is there anything specific about your mortgage situation they should know?", None)
            else:
                return ("No problem! If you decide you'd like to speak with a mortgage expert in the future, just let us know. In the meantime, our blog has some great articles on finding the best mortgage rates. Is there anything else I can help you with today?", None)
    
    def handle_utility_flow(self, user_id, user_name, message, step=None):
        """
        Handle the "Save Money > Reduce Utility Bills" flow
        Returns (response_text, quick_replies or None)
        """
        state = self.get_state(user_id)
        
        # If step is explicitly provided, override the state
        if step is not None:
            state.set_flow("savings_utility", step)
        
        current_step = state.get_step()
        
        # Step 1: Ask about smart home or appliances
        if current_step == 1:
            state.next_step()
            return ("Are you interested in smart home solutions or energy-efficient appliances?", 
                    ["Smart Home", "Appliances", "Both"])
        
        # Step 2: Store preference and provide appropriate information
        elif current_step == 2:
            state.store_answer("utility_preference", message)
            state.next_step()
            
            response = ""
            if message == "Smart Home":
                response = "Smart home solutions can significantly reduce your utility bills. Some effective options include:\n\n" + \
                           "• Smart thermostats: Save 10-15% on heating and cooling costs\n" + \
                           "• Smart lighting: Reduce electricity usage by automatically turning off when not needed\n" + \
                           "• Smart plugs: Control energy usage of electronics and appliances\n" + \
                           "• Smart water controllers: Reduce water waste and lower water bills\n\n" + \
                           "Many utility companies offer rebates for installing these devices. Would you like us to send you our guide on smart home energy savings?"
            elif message == "Appliances":
                response = "Energy-efficient appliances can dramatically reduce your utility bills. Look for ENERGY STAR certified:\n\n" + \
                           "• Refrigerators: Can save $300+ over their lifetime\n" + \
                           "• Washing machines: Use 25% less energy and 33% less water\n" + \
                           "• HVAC systems: Can reduce energy usage by up to 20%\n" + \
                           "• Water heaters: Tankless options can save up to 30% on water heating\n\n" + \
                           "Many states offer rebates or tax incentives for energy-efficient upgrades. Would you like us to send you information about rebate programs in your area?"
            else:  # Both
                response = "Combining smart home technology with energy-efficient appliances creates the biggest impact on utility bills.\n\n" + \
                           "Smart home solutions:\n" + \
                           "• Smart thermostats: Save 10-15% on heating and cooling\n" + \
                           "• Smart lighting and plugs: Reduce electricity waste\n\n" + \
                           "Energy-efficient appliances:\n" + \
                           "• ENERGY STAR certified appliances use significantly less energy\n" + \
                           "• Modern HVAC systems paired with smart controls maximize savings\n\n" + \
                           "Would you like us to send you our comprehensive guide on reducing utility bills?"
            
            return (response, ["Yes, send guide", "No thanks"])
        
        # Step 3: Store if they want the guide and complete
        elif current_step == 3:
            state.store_answer("wants_utility_guide", message)
            
            # Save all data to Google Sheets
            all_data = state.get_all_data()
            self.save_money_request(user_id, user_name, all_data)
            
            # Reset the flow for next time
            state.reset()
            
            if message == "Yes, send guide":
                return ("Great! We'll send you our guide on reducing utility bills via Messenger. It includes links to current rebate programs and tax incentives for energy-efficient upgrades. Is there anything specific about your home's energy usage you're concerned about?", None)
            else:
                return ("No problem! If you'd like information about reducing utility bills in the future, just let us know. Is there anything else I can help you with today?", None)
    
    def handle_insurance_flow(self, user_id, user_name, message, step=None):
        """
        Handle the "Save Money > Home Insurance Discounts" flow
        Returns (response_text, quick_replies or None)
        """
        state = self.get_state(user_id)
        
        # If step is explicitly provided, override the state
        if step is not None:
            state.set_flow("savings_insurance", step)
        
        current_step = state.get_step()
        
        # Step 1: Ask if they currently have home insurance
        if current_step == 1:
            state.next_step()
            return ("Do you currently have home insurance?", 
                    ["Yes", "No", "Shopping Around"])
        
        # Step 2: Store answer and provide insurance information
        elif current_step == 2:
            state.store_answer("has_insurance", message)
            state.next_step()
            
            response = ""
            if message == "Yes":
                response = "Many homeowners don't realize they qualify for discounts on their existing policy. Common discounts include:\n\n" + \
                           "• Multi-policy (bundling with auto insurance): 5-25% savings\n" + \
                           "• Home security systems: 5-20% savings\n" + \
                           "• Impact-resistant roofing: 5-10% savings\n" + \
                           "• New home/renovation discounts: 10-15% savings\n" + \
                           "• Claims-free discount: 5-20% for no claims history\n\n" + \
                           "Would you like us to connect you with an insurance advisor who can review your current policy for potential savings?"
            elif message == "No":
                response = "When shopping for home insurance, it's important to compare offers from multiple providers. Some top-rated insurers for cost-effective coverage include:\n\n" + \
                           "• HomeGuard Insurance: Known for competitive rates and good customer service\n" + \
                           "• ValueSafe: Offers specialized packages for new homeowners\n" + \
                           "• SecureHome: Provides substantial discounts for home security features\n\n" + \
                           "Would you like us to connect you with an insurance advisor who can help you find the best rates?"
            else:  # Shopping Around
                response = "Smart move! Shopping around regularly can save you hundreds on home insurance. When comparing policies, consider these factors:\n\n" + \
                           "• Coverage limits: Make sure they match your home's actual replacement value\n" + \
                           "• Deductibles: Higher deductibles mean lower premiums\n" + \
                           "• Discount opportunities: Security systems, bundling, etc.\n" + \
                           "• Customer service ratings: Check independent reviews\n\n" + \
                           "Would you like us to connect you with an insurance advisor who can help you compare options?"
            
            return (response, ["Yes, connect me", "No thanks"])
        
        # Step 3: Store if they want to connect and complete
        elif current_step == 3:
            state.store_answer("wants_insurance_advisor", message)
            
            # Save all data to Google Sheets
            all_data = state.get_all_data()
            self.save_money_request(user_id, user_name, all_data)
            
            # Reset the flow for next time
            state.reset()
            
            if message == "Yes, connect me":
                return ("Great! One of our insurance partners will reach out to you soon to help you explore the best options for your situation. They can provide a free review of your current policy or help you find new coverage with maximum discounts. Is there anything specific about your home or insurance needs they should know?", None)
            else:
                return ("No problem! If you'd like help with home insurance in the future, just let us know. We also have a helpful guide on our website that outlines the most overlooked insurance discounts. Is there anything else I can help you with today?", None)
    
    def handle_tax_flow(self, user_id, user_name, message, step=None):
        """
        Handle the "Save Money > Tax Benefits" flow
        Returns (response_text, quick_replies or None)
        """
        state = self.get_state(user_id)
        
        # If step is explicitly provided, override the state
        if step is not None:
            state.set_flow("savings_tax", step)
        
        current_step = state.get_step()
        
        # Step 1: Provide tax information and ask if they want to connect with consultant
        if current_step == 1:
            state.next_step()
            
            response = "Homeownership comes with several valuable tax benefits. The most common include:\n\n" + \
                       "• Mortgage interest deduction: Interest paid on up to $750,000 of mortgage debt\n" + \
                       "• Property tax deduction: Up to $10,000 in state and local taxes\n" + \
                       "• Home office deduction: If you work from home\n" + \
                       "• Energy efficiency credits: For qualifying improvements\n" + \
                       "• Capital gains exclusion: When selling your primary residence\n\n" + \
                       "Tax laws change frequently and benefits vary based on your situation. Would you like to connect with a tax consultant who specializes in real estate?"
            
            return (response, ["Yes, connect me", "No thanks"])
        
        # Step 2: Store if they want to connect and complete
        elif current_step == 2:
            state.store_answer("wants_tax_consultant", message)
            
            # Save all data to Google Sheets
            all_data = state.get_all_data()
            self.save_money_request(user_id, user_name, all_data)
            
            # Reset the flow for next time
            state.reset()
            
            if message == "Yes, connect me":
                return ("Great! One of our tax consultant partners will reach out to you soon. They can provide personalized advice on maximizing your homeowner tax benefits. Is there anything specific about your tax situation they should know?", None)
            else:
                return ("No problem! If you'd like more information about homeowner tax benefits in the future, just let us know. Our blog also has seasonal tax tips that you might find helpful. Is there anything else I can help you with today?", None)
    
    def save_money_request(self, user_id, user_name, data):
        """Save money-saving request to Google Sheets"""
        try:
            # Format the data for storage
            now = time.strftime("%Y-%m-%d %H:%M:%S")
            
            # Get main category
            category = data.get("savings_category", "Unknown")
            
            # Build details string based on the category
            if category == "Lower Mortgage Payments":
                details = f"Type: {data.get('mortgage_type', 'N/A')}, Connect: {data.get('wants_mortgage_expert', 'N/A')}"
            elif category == "Reduce Utility Bills":
                details = f"Preference: {data.get('utility_preference', 'N/A')}, Guide: {data.get('wants_utility_guide', 'N/A')}"
            elif category == "Home Insurance Discounts":
                details = f"Has Insurance: {data.get('has_insurance', 'N/A')}, Connect: {data.get('wants_insurance_advisor', 'N/A')}"
            elif category == "Tax Benefits":
                details = f"Connect: {data.get('wants_tax_consultant', 'N/A')}"
            else:
                details = "No specific details provided"
            
            # Format the row
            row_data = [
                now,                  # Timestamp
                user_id,              # User ID
                user_name,            # User Name
                "Save Money Request", # Type
                category,             # Savings Category
                details,              # Details
                "Pending",            # Status
                "",                   # Follow-up
                ""                    # Notes
            ]
            
            # Save to sheets
            if hasattr(self.sheets_handler, 'save_money_request'):
                return self.sheets_handler.save_money_request(row_data)
            else:
                # Fall back to general method if specific one doesn't exist
                return self.sheets_handler.save_home_preferences(row_data)
                
        except Exception as e:
            print(f"Error saving money request: {e}")
            return False
    
    def process_message(self, user_id, user_name, message):
        """
        Process a message based on the current conversation state
        Returns (response_text, quick_replies or None)
        """
        state = self.get_state(user_id)
        current_flow = state.get_flow()
        
        # Check the current flow and route accordingly
        if current_flow == "find_home_buy":
            return self.handle_buy_flow(user_id, user_name, message)
        elif current_flow == "find_home_rent":
            return self.handle_rent_flow(user_id, user_name, message)
        elif current_flow == "find_home":
            return self.handle_buy_or_rent(user_id, message)
        elif current_flow == "get_help":
            return self.handle_help_category(user_id, user_name, message)
        elif current_flow == "help_real_estate":
            return self.handle_real_estate_flow(user_id, user_name, message)
        elif current_flow == "help_maintenance":
            return self.handle_maintenance_flow(user_id, user_name, message)
        elif current_flow == "help_legal":
            return self.handle_legal_flow(user_id, user_name, message)
        elif current_flow == "help_other":
            return self.handle_other_help_flow(user_id, user_name, message)
        elif current_flow == "save_money":
            return self.handle_save_money_category(user_id, user_name, message)
        elif current_flow == "savings_mortgage":
            return self.handle_mortgage_flow(user_id, user_name, message)
        elif current_flow == "savings_utility":
            return self.handle_utility_flow(user_id, user_name, message)
        elif current_flow == "savings_insurance":
            return self.handle_insurance_flow(user_id, user_name, message)
        elif current_flow == "savings_tax":
            return self.handle_tax_flow(user_id, user_name, message)
        
        # No active flow
        return None
    
    def start_find_home_flow(self, user_id):
        """Start the Find Home flow"""
        state = self.get_state(user_id)
        state.set_flow("find_home")
        return ("Great! Are you looking to buy or rent?", ["Buy", "Rent"])
    
    def save_home_preferences(self, user_id, user_name, type, data):
        """Save home search preferences to Google Sheets"""
        try:
            # Format the data for storage
            now = time.strftime("%Y-%m-%d %H:%M:%S")
            
            # For Buy flow
            if type == "buy":
                row_data = [
                    now,                     # Timestamp
                    user_id,                 # User ID
                    user_name,               # User Name
                    "Buy",                   # Type
                    data.get("home_type"),   # Home Type
                    data.get("budget"),      # Budget
                    data.get("location"),    # Location
                    data.get("financing"),   # Financing
                    ""                       # Additional Notes
                ]
            # For Rent flow
            elif type == "rent":
                row_data = [
                    now,                           # Timestamp
                    user_id,                       # User ID
                    user_name,                     # User Name
                    "Rent",                        # Type
                    data.get("property_type"),     # Property Type
                    data.get("budget"),            # Budget
                    data.get("location"),          # Location
                    data.get("roommate_service"),  # Roommate Service
                    ""                             # Additional Notes
                ]
            
            # Save to separate sheet for home preferences
            return self.sheets_handler.save_home_preferences(row_data)
        except Exception as e:
            print(f"Error saving home preferences: {e}")
            return False
