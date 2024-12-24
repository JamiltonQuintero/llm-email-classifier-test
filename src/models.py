from typing import Dict, Optional, List
from datetime import datetime
from dataclasses import dataclass

@dataclass
class Email:
    id: str
    sender: str
    subject: str
    body: str
    timestamp: str
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Email':
        try:
            return cls(
                id=data['id'],
                sender=data['from'],
                subject=data['subject'],
                body=data['body'],
                timestamp=data['timestamp']
            )
        except KeyError as e:
            raise ValidationError(f"Missing required field: {e}", data.get('id'))

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "from": self.sender,
            "subject": self.subject,
            "body": self.body,
            "timestamp": self.timestamp
        }

@dataclass
class ProcessingResult:
    email_id: str
    success: bool
    classification: Optional[str]
    response_sent: bool
    timestamp: str
    error: Optional[str] = None
    actions_taken: List[str] = None

    def __post_init__(self):
        if self.actions_taken is None:
            self.actions_taken = []

    def add_action(self, action: str):
        if self.actions_taken is None:
            self.actions_taken = []
        self.actions_taken.append(action)

    def to_dict(self) -> Dict:
        return {
            "email_id": self.email_id,
            "success": self.success,
            "classification": self.classification,
            "response_sent": self.response_sent,
            "timestamp": self.timestamp,
            "error": self.error,
            "actions_taken": self.actions_taken
        } 