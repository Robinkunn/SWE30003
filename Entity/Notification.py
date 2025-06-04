from Entity.Message import Message
from datetime import datetime

class Notification(Message):
    def __init__(self, sender_id, receiver_id, subject, content, notification_type):
        super().__init__(sender_id, subject, content)
        self.receiver_id = receiver_id
        self.notification_type = notification_type  
        self.is_read = False
        self.is_removed = False
    
    @classmethod
    def from_dict(cls, data):
        notif = cls(
            sender_id=data.get("sender_id"),
            receiver_id=data.get("receiver_id"),
            subject=data.get("subject"),
            content=data.get("content"),
            notification_type=data.get("notification_type")
        )
        notif.is_read = data.get("is_read", False)
        notif.is_removed = data.get("is_removed", False)
        notif.message_id = data.get("message_id")
        notif.timestamp = data.get("timestamp")
        return notif

    def to_dict(self):
        return {
            "message_id": getattr(self, "message_id", None),
            "sender_id": self.sender_id,
            "receiver_id": self.receiver_id,
            "timestamp": getattr(self, "timestamp", None),
            "subject": self.subject,
            "content": self.content,
            "notification_type": self.notification_type,
            "is_read": self.is_read,
            "is_removed": self.is_removed
        }

    def display(self, idx=None):
        read_status = "✓" if self.is_read else "●"
        prefix = f"{idx}. " if idx is not None else ""
        print(f"\n{prefix}{read_status} [{getattr(self, 'timestamp', 'N/A')}]")
        print(f"   Subject : {self.subject}")
        print(f"   Type    : {self.notification_type}")
        print(f"   Content : {self.content}")
        
    def mark_as_read(self):
        self.is_read = True

    def remove(self):
        self.is_removed = True

    def send(self, recipient_id=None):
        # recipient_id optional, default to receiver_id
        if recipient_id:
            self.receiver_id = recipient_id
        # Simulate sending notification (e.g., print or store)
        print(f"Notification sent to {self.receiver_id}: {self.subject}")
    
    @staticmethod
    def handle_notification_actions(customer_id, customer_notifications, notification_center):
        print("\nOptions:")
        print("1. Mark a notification as read")
        print("2. Remove a notification")
        print("3. View notification count")
        print("4. Mark all as read")
        print("5. Remove all notifications")
        print("0. Back to main menu")

        try:
            action = int(input("Select an action: "))

            if action == 1:
                notif_num = int(input("Enter notification number to mark as read: "))
                if 1 <= notif_num <= len(customer_notifications):
                    selected_notif = customer_notifications[notif_num - 1]
                    if notification_center.mark_notification_as_read(customer_id, selected_notif['message_id']):
                        print("Notification marked as read.")
                    else:
                        print("Failed to mark notification as read.")
                else:
                    print("Invalid notification number.")

            elif action == 2:
                notif_num = int(input("Enter notification number to remove: "))
                if 1 <= notif_num <= len(customer_notifications):
                    selected_notif = customer_notifications[notif_num - 1]
                    # Only call with customer_id and message_id
                    if notification_center.remove_notification(customer_id, selected_notif['message_id']):
                        print("Notification removed (marked as removed).")
                    else:
                        print("Failed to remove notification.")
                else:
                    print("Invalid notification number.")

            elif action == 3:
                total_count = notification_center.get_notification_count(customer_id, unread_only=False)
                unread_count = notification_center.get_notification_count(customer_id, unread_only=True)
                print(f"Total notifications: {total_count}")
                print(f"Unread notifications: {unread_count}")

            elif action == 4:
                # Mark all as read
                success = True
                for notif in customer_notifications:
                    if not notif.get('is_read', False):
                        if not notification_center.mark_notification_as_read(customer_id, notif['message_id']):
                            success = False
                if success:
                    print("All notifications marked as read.")
                else:
                    print("Some notifications could not be marked as read.")

            elif action == 5:
                 # Mark all notifications as removed (soft delete)
                success = notification_center.remove_all_notifications(customer_id)
                if success:
                    print("All notifications marked as removed.")
                else:
                    print("Some notifications could not be marked as removed.")

            elif action == 0:
                return
            else:
                print("Invalid action.")

        except ValueError:
            print("Please enter a valid number.")

    def write_content(self, content):
        """Implements abstract method to write or update notification content."""
        self.content = content
        self.timestamp = datetime.now()