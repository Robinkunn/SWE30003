import json
import os
from Entity.Inquiry import Inquiry

class InquiryManager:
    def __init__(self, filename="Inquiry.json"):
        self.filename = filename
        self.inquiries = self.load_inquiries()

    def add_inquiry(self, inquiry):
        self.inquiries.append(inquiry)
        self.save_inquiries()

    def get_by_customer(self, customer_id):
        return [inq for inq in self.inquiries if inq.sender_id == customer_id]

    def get_by_staff(self, staff_id):
        return [inq for inq in self.inquiries if inq.responder_id == staff_id]

    def get_open_inquiries(self):
        return [inq for inq in self.inquiries if not inq.resolved]

    def link_inquiries(self, inquiry_ids):
        # Implement linking logic if needed
        pass

    def close_thread(self, inquiry_ids):
        for inq in self.inquiries:
            if inq.message_id in inquiry_ids:
                inq.mark_as_closed()
        self.save_inquiries()

    def save_inquiries(self):
        with open(self.filename, "w") as f:
            json.dump([inq.to_dict() for inq in self.inquiries], f, indent=4)

    def load_inquiries(self):
        if not os.path.exists(self.filename) or os.stat(self.filename).st_size == 0:
            return []

        with open(self.filename, "r") as f:
            try:
                data = json.load(f)
                return [Inquiry.from_dict(d) for d in data]
            except json.JSONDecodeError:
                print(f"Warning: {self.filename} is not valid JSON. Starting with an empty list.")
                return []

