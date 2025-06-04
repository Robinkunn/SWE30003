from abc import ABC, abstractmethod
from datetime import datetime
import uuid

class Message(ABC):
    def __init__(self, sender_id, subject, content):
        self.message_id = str(uuid.uuid4())  # Unique message identifier
        self.sender_id = sender_id
        self.timestamp = datetime.now()
        self.subject = subject
        self.content = content

    @abstractmethod
    def send(self, recipient_id=None):
        pass  

    @abstractmethod
    def write_content(self, content):
        """Abstract method to write or update message content."""
        pass

    def edit_content(self, new_content):
        self.content = new_content
        self.timestamp = datetime.now()
