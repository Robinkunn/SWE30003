from Entity.Notification import Notification
from datetime import datetime
import json
import uuid

class NotificationCenter:
    def __init__(self):
        self.notifications = []
        self.json_file = "Notification.json"

    def add_notification(self, notification: Notification):
        """Add a new notification to the center."""
        self.notifications.append(notification)

    def load_notifications_from_file(self):
        """Load notifications from JSON file."""
        try:
            with open(self.json_file, "r") as f:
                notifications_data = json.load(f)
            return notifications_data
        except FileNotFoundError:
            return []
        except Exception as e:
            # For debugging purposes, you can uncomment the next line to see the error
            # print(f"Error loading notifications: {e}")
            return []

    def save_notifications_to_file(self, notifications_data):
        """Save notifications to JSON file."""
        try:
            with open(self.json_file, "w") as f:
                json.dump(notifications_data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving notifications: {e}")
            return False

    def create_reschedule_notification(self, customer_id, trip_name, trip_id):
        """Create and save a trip reschedule notification."""
        notification_data = {
            "message_id": str(uuid.uuid4()),
            "sender_id": "SYSTEM",
            "receiver_id": customer_id,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "subject": "Trip Rescheduled Successfully",
            "content": f"Your trip '{trip_name}' (ID: {trip_id}) has been successfully rescheduled.",
            "notification_type": "trip_reschedule",
            "is_read": False,
            "is_removed": False
        }
        
        # Load existing notifications
        notifications = self.load_notifications_from_file()
        
        # Add new notification
        notifications.append(notification_data)
        
        # Save updated notifications
        return self.save_notifications_to_file(notifications)

    def create_system_notification(self, customer_id, subject, content, notification_type="system"):
        """Create a general system notification."""
        notification_data = {
            "message_id": str(uuid.uuid4()),
            "sender_id": "SYSTEM",
            "receiver_id": customer_id,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "subject": subject,
            "content": content,
            "notification_type": notification_type,
            "is_read": False,
            "is_removed": False
        }
        
        # Load existing notifications
        notifications = self.load_notifications_from_file()
        
        # Add new notification
        notifications.append(notification_data)
        
        # Save updated notifications
        return self.save_notifications_to_file(notifications)

    def create_refund_notification(self, customer_id, trip_name, trip_id, refund_amount):
        """Create a trip refund notification."""
        notification_data = {
            "message_id": str(uuid.uuid4()),
            "sender_id": "SYSTEM",
            "receiver_id": customer_id,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "subject": "Refund Processed Successfully",
            "content": f"Your refund for trip '{trip_name}' (ID: {trip_id}) has been processed. Refund amount: RM{refund_amount:.2f}. The amount will be credited to your original payment method within 3-5 business days.",
            "notification_type": "trip_refund",
            "is_read": False,
            "is_removed": False
        }
        
        # Load existing notifications
        notifications = self.load_notifications_from_file()
        
        # Add new notification
        notifications.append(notification_data)
        
        # Save updated notifications
        return self.save_notifications_to_file(notifications)

    def get_customer_notifications(self, customer_id, unread_only=False):
        """Get all notifications for a specific customer."""
        notifications = self.load_notifications_from_file()
        customer_notifications = [
            n for n in notifications 
            if n["receiver_id"] == customer_id and not n.get("is_removed", False)
        ]
        
        if unread_only:
            customer_notifications = [
                n for n in customer_notifications 
                if not n.get("is_read", False)
            ]
        
        return customer_notifications

    def display_customer_notifications(self, customer_id):
        customer_notifications = self.get_customer_notifications(customer_id)
        if not customer_notifications:
            print("You have no new notifications.")
            return []
        for idx, notif_data in enumerate(customer_notifications, 1):
            notif = Notification.from_dict(notif_data)
            notif.display(idx)
        return customer_notifications

    def display_detailed_notifications(self, customer_id):
        pass

    def mark_notification_as_read(self, customer_id, message_id):
        notifications = self.load_notifications_from_file()
        updated = False
        for i, data in enumerate(notifications):
            if data["receiver_id"] == customer_id and data["message_id"] == message_id:
                notif = Notification.from_dict(data)
                notif.mark_as_read()
                notifications[i] = notif.to_dict()
                updated = True
                break
        return self.save_notifications_to_file(notifications) if updated else False

    def remove_notification(self, customer_id, message_id):
        notifications = self.load_notifications_from_file()
        updated = False
        for i, data in enumerate(notifications):
            if data["receiver_id"] == customer_id and data["message_id"] == message_id:
                notif = Notification.from_dict(data)
                notif.remove()
                notifications[i] = notif.to_dict()
                updated = True
                break
        return self.save_notifications_to_file(notifications) if updated else False

    def get_notification_count(self, customer_id, unread_only=True):
        """Get count of notifications for a customer."""
        notifications = self.get_customer_notifications(customer_id, unread_only)
        return len(notifications)

    def mark_all_as_read(self, customer_id):
        """Mark all notifications for a customer as read."""
        notifications = self.load_notifications_from_file()
        
        for notification in notifications:
            if (notification["receiver_id"] == customer_id and 
                not notification.get("is_removed", False)):
                notification["is_read"] = True
        
        return self.save_notifications_to_file(notifications)

    def remove_all_notifications(self, customer_id):
        """Soft delete all notifications for a customer."""
        notifications = self.load_notifications_from_file()
        
        for notification in notifications:
            if (notification["receiver_id"] == customer_id and 
                not notification.get("is_removed", False)):
                notification["is_removed"] = True
        
        return self.save_notifications_to_file(notifications)

    def get_notifications_by_type(self, customer_id, notification_type):
        """Get notifications of a specific type for a customer."""
        customer_notifications = self.get_customer_notifications(customer_id)
        return [
            n for n in customer_notifications 
            if n.get("notification_type") == notification_type
        ]

    def search_notifications(self, customer_id, search_term):
        """Search notifications by subject or content."""
        customer_notifications = self.get_customer_notifications(customer_id)
        search_term = search_term.lower()
        
        return [
            n for n in customer_notifications 
            if (search_term in n.get("subject", "").lower() or 
                search_term in n.get("content", "").lower())
        ]