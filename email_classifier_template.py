# Configuration and imports
import os
import json
import pandas as pd
from typing import Dict, List, Optional, Tuple
from dotenv import load_dotenv
from openai import OpenAI
from datetime import datetime
import logging
from langchain_openai import ChatOpenAI


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()



# Sample email dataset
sample_emails = [
    {
        "id": "001",
        "from": "angry.customer@example.com",
        "subject": "Broken product received",
        "body": "I received my order #12345 yesterday but it arrived completely damaged. This is unacceptable and I demand a refund immediately. This is the worst customer service I've experienced.",
        "timestamp": "2024-03-15T10:30:00Z"
    },
    {
        "id": "002",
        "from": "curious.shopper@example.com",
        "subject": "Question about product specifications",
        "body": "Hi, I'm interested in buying your premium package but I couldn't find information about whether it's compatible with Mac OS. Could you please clarify this? Thanks!",
        "timestamp": "2024-03-15T11:45:00Z"
    },
    {
        "id": "003",
        "from": "happy.user@example.com",
        "subject": "Amazing customer support",
        "body": "I just wanted to say thank you for the excellent support I received from Sarah on your team. She went above and beyond to help resolve my issue. Keep up the great work!",
        "timestamp": "2024-03-15T13:15:00Z"
    },
    {
        "id": "004",
        "from": "tech.user@example.com",
        "subject": "Need help with installation",
        "body": "I've been trying to install the software for the past hour but keep getting error code 5123. I've already tried restarting my computer and clearing the cache. Please help!",
        "timestamp": "2024-03-15T14:20:00Z"
    },
    {
        "id": "005",
        "from": "business.client@example.com",
        "subject": "Partnership opportunity",
        "body": "Our company is interested in exploring potential partnership opportunities with your organization. Would it be possible to schedule a call next week to discuss this further?",
        "timestamp": "2024-03-15T15:00:00Z"
    }
]


class EmailProcessor:
    def __init__(self):

        self.llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0,
            max_tokens=None,
            timeout=None,
        )

        # Define valid categories
        self.valid_categories = {
            "complaint", "inquiry", "feedback",
            "support_request", "other"
        }
        
    def classify_email(self, email: Dict) -> Optional[str]:
        try:
            messages = [
                (
                    "system",
                    "You are a helpful assistant that classifies emails into one of the following categories: complaint, inquiry, feedback, support_request, other. "
                    "The categories are defined as follows: "
                    "complaint: emails that are complaints about the product or service. "
                    "inquiry: emails that are inquiries about the product or service. "
                    "feedback: emails that are feedback about the product or service. "
                    "support_request: emails that are support requests for the product or service. "
                    "other: emails that are not classified into the other categories. "
                    "Please return the category in the following format: <category_name>"
                    "",
                ),
                ("human", json.dumps(email)),
            ]
             
            ai_msg = self.llm.invoke(messages)
            return ai_msg.content
        except Exception as e:
            logger.error(f"Error classifying email {email['id']}: {e}")
            return None

    def generate_response(self, email: Dict, classification: str) -> Optional[str]:

        if classification not in self.valid_categories:
            logger.error(f"Invalid classification {classification} for email {email['id']}")
            return None

        try:
            messages = [
                (
                    "system",
                    f"""You are a customer service assistant. Generate a professional and empathetic response 
                    to the email based on its classification: {classification}.
                    
                    Guidelines:
                    - For complaints: Acknowledge the issue, apologize, and provide next steps
                    - For inquiries: Provide clear and concise information
                    - For feedback: Thank them and acknowledge their input
                    - For support requests: Provide troubleshooting steps or escalation path
                    - For others: Respond appropriately to the context
                    
                    Respond in a professional tone and end with a call to action when appropriate."""
                ),
                ("human", json.dumps(email)),
            ]

            ai_msg = self.llm.invoke(messages)
            return ai_msg.content
        except Exception as e:
            logger.error(f"Error generating response for email {email['id']}: {e}")
            return None


class EmailAutomationSystem:
    def __init__(self, processor: EmailProcessor):
        """Initialize the automation system with an EmailProcessor."""
        self.processor = processor

        self.response_handlers = {
            "complaint": self._handle_complaint,
            "inquiry": self._handle_inquiry,
            "feedback": self._handle_feedback,
            "support_request": self._handle_support_request,
            "other": self._handle_other
        }

    def process_email(self, email: Dict) -> Dict:
        """Process a single email through the complete pipeline."""
        result = {
            "email_id": email["id"],
            "success": False,
            "classification": None,
            "response_sent": False,
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            classification = self.processor.classify_email(email)
            result["classification"] = classification
            
            if classification in self.response_handlers:
                handler = self.response_handlers[classification]
                handler(email, classification)
                result["success"] = True
                result["response_sent"] = True
            else:
                logger.warning(f"No handler found for classification: {classification}")
                
            return result
        except Exception as e:
            logger.error(f"Error processing email {email['id']}: {e}")
            return result

    def _handle_complaint(self, email: Dict, classification: str):
        """Handle complaint emails."""
        try:
            response = self.processor.generate_response(email, classification)
            if response:
                send_complaint_response(email["id"], response)
                create_urgent_ticket(email["id"], "complaint", response)
        except Exception as e:
            logger.error(f"Error handling complaint {email['id']}: {e}")
            return None

    def _handle_inquiry(self, email: Dict, classification: str):
        """Handle inquiry emails."""
        try:
            response = self.processor.generate_response(email, classification)
            if response:
                send_standard_response(email["id"], response)
                create_support_ticket(email["id"], response)
        except Exception as e:
            logger.error(f"Error handling inquiry {email['id']}: {e}")
            return None

    def _handle_feedback(self, email: Dict, classification: str):
        """Handle feedback emails."""
        try:
            response = self.processor.generate_response(email, classification)
            if response:
                send_standard_response(email["id"], response)
                log_customer_feedback(email["id"], response)
        except Exception as e:
            logger.error(f"Error handling feedback {email['id']}: {e}")
            return None

    def _handle_support_request(self, email: Dict, classification: str):
        """Handle support request emails."""
        try:
            response = self.processor.generate_response(email, classification)
            if response:
                send_standard_response(email["id"], response)
                create_support_ticket(email["id"], response)
        except Exception as e:
            logger.error(f"Error handling support request {email['id']}: {e}")
            return None

    def _handle_other(self, email: Dict, classification: str):
        """Handle other category emails."""
        try:
            response = self.processor.generate_response(email, classification)
            if response:
                send_standard_response(email["id"], response)
        except Exception as e:
            logger.error(f"Error handling other email {email['id']}: {e}")
            return None


# Mock service functions
def send_complaint_response(email_id: str, response: str):
    """Mock function to simulate sending a response to a complaint"""
    logger.info(f"Sending complaint response for email {email_id} with response: {response}")
    # In real implementation: integrate with email service


def send_standard_response(email_id: str, response: str):
    """Mock function to simulate sending a standard response"""
    logger.info(f"Sending standard response for email {email_id} with response: {response}")
    # In real implementation: integrate with email service


def create_urgent_ticket(email_id: str, category: str, context: str):
    """Mock function to simulate creating an urgent ticket"""
    logger.info(f"Creating urgent ticket for email {email_id} with category: {category} and context: {context}")
    # In real implementation: integrate with ticket system


def create_support_ticket(email_id: str, context: str):
    """Mock function to simulate creating a support ticket"""
    logger.info(f"Creating support ticket for email {email_id} with context: {context}")
    # In real implementation: integrate with ticket system


def log_customer_feedback(email_id: str, feedback: str):
    """Mock function to simulate logging customer feedback"""
    logger.info(f"Logging feedback for email {email_id} with feedback: {feedback}")
    # In real implementation: integrate with feedback system


def run_demonstration():
    """Run a demonstration of the complete system."""
    # Initialize the system
    processor = EmailProcessor()
    automation_system = EmailAutomationSystem(processor)

    # Process all sample emails
    results = []
    for email in sample_emails:
        logger.info(f"\nProcessing email {email['id']}...")
        result = automation_system.process_email(email)
        results.append(result)

    # Create a summary DataFrame
    df = pd.DataFrame(results)
    print("\nProcessing Summary:")
    print(df[["email_id", "success", "classification", "response_sent"]])

    return df


# Example usage:
if __name__ == "__main__":
    run_demonstration()
