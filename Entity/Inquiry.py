from Entity.Message import Message
from datetime import datetime

class Inquiry(Message):
    def __init__(self, sender_id, subject, content, category):
        super().__init__(sender_id, subject, content)
        self.category = category
        self.resolved = False
        self.response = None
        self.responder_id = None

    def send(self, recipient_id=None):
        pass  

    def respond(self, responder_id, response_content):
        self.responder_id = responder_id
        self.response = response_content
        self.resolved = True

    def edit_response(self, new_content):
        self.response = new_content

    def mark_as_closed(self):
        self.resolved = True

    def to_dict(self):
        return {
            "message_id": self.message_id,
            "sender_id": self.sender_id,
            "subject": self.subject,
            "content": self.content,
            "category": self.category,
            "response": self.response,
            "responder_id": self.responder_id,
            "resolved": self.resolved
        }

    @classmethod
    def from_dict(cls, data):
        inquiry = cls(
            sender_id=data["sender_id"],
            subject=data["subject"],
            content=data["content"],
            category=data["category"]
        )
        inquiry.message_id = data.get("message_id")
        inquiry.resolved = data.get("resolved", False)
        inquiry.response = data.get("response", None)
        inquiry.responder_id = data.get("responder_id", None)
        return inquiry

    def write_content(self, content):
        """Implements abstract method to write or update inquiry content."""
        self.content = content
        self.timestamp = datetime.now()

