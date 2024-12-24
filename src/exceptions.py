class EmailProcessingError(Exception):
    """Base exception for email processing errors"""
    def __init__(self, message: str, email_id: str = None):
        self.email_id = email_id
        self.message = message
        super().__init__(self.message)

class ClassificationError(EmailProcessingError):
    """Raised when there's an error classifying an email"""
    pass

class ResponseGenerationError(EmailProcessingError):
    """Raised when there's an error generating a response"""
    pass

class HandlerError(EmailProcessingError):
    """Raised when there's an error in email handling"""
    pass

class ValidationError(EmailProcessingError):
    """Raised when there's an error validating email data"""
    pass 