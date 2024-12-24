from typing import Dict, Optional
from models import Email
from services import EmailService, TicketService, FeedbackService
from exceptions import HandlerError


class EmailHandler:
    def __init__(self, email_service: EmailService, ticket_service: TicketService, 
                 feedback_service: FeedbackService):
        self.email_service = email_service
        self.ticket_service = ticket_service
        self.feedback_service = feedback_service

    def handle_complaint(self, email: Email, response: str) -> Dict[str, str]:
        """Handle complaint emails"""
        try:
            self.email_service.send_complaint_response(email.id, response)
            ticket_id = self.ticket_service.create_urgent_ticket(email.id, "complaint", response)
            return {
                "status": "success",
                "ticket_id": ticket_id,
                "actions": ["sent_complaint_response", "created_urgent_ticket"]
            }
        except Exception as e:
            raise HandlerError(f"Error handling complaint: {str(e)}", email.id)

    def handle_inquiry(self, email: Email, response: str) -> Dict[str, str]:
        """Handle inquiry emails"""
        try:
            self.email_service.send_standard_response(email.id, response)
            ticket_id = self.ticket_service.create_support_ticket(email.id, response)
            return {
                "status": "success",
                "ticket_id": ticket_id,
                "actions": ["sent_standard_response", "created_support_ticket"]
            }
        except Exception as e:
            raise HandlerError(f"Error handling inquiry: {str(e)}", email.id)

    def handle_feedback(self, email: Email, response: str) -> Dict[str, str]:
        """Handle feedback emails"""
        try:
            self.email_service.send_standard_response(email.id, response)
            self.feedback_service.log_feedback(email.id, response)
            return {
                "status": "success",
                "actions": ["sent_standard_response", "logged_feedback"]
            }
        except Exception as e:
            raise HandlerError(f"Error handling feedback: {str(e)}", email.id)

    def handle_support_request(self, email: Email, response: str) -> Dict[str, str]:
        """Handle support request emails"""
        try:
            self.email_service.send_standard_response(email.id, response)
            ticket_id = self.ticket_service.create_support_ticket(email.id, response)
            return {
                "status": "success",
                "ticket_id": ticket_id,
                "actions": ["sent_standard_response", "created_support_ticket"]
            }
        except Exception as e:
            raise HandlerError(f"Error handling support request: {str(e)}", email.id)

    def handle_other(self, email: Email, response: str) -> Dict[str, str]:
        """Handle other category emails"""
        try:
            self.email_service.send_standard_response(email.id, response)
            return {
                "status": "success",
                "actions": ["sent_standard_response"]
            }
        except Exception as e:
            raise HandlerError(f"Error handling other email: {str(e)}", email.id) 