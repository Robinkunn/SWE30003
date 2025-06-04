from datetime import datetime
import uuid
from Entity.UserAccount import UserAccount
from Manager.InquiryManager import InquiryManager  
from Entity.Notification import Notification
from Manager.NotificationCenter import NotificationCenter  



class Staff(UserAccount):
    def __init__(self, sarawak_id, password_hash, full_name, email_address, phone_number, nric,
                 role, department):
        super().__init__(sarawak_id, password_hash, full_name, email_address, phone_number, nric)
        self.role = role
        self.department = department

    @classmethod
    def register(cls):
        print("\n--- Register as Staff ---")
        # Pass user_type directly
        base_info = UserAccount.register(user_type="2")
        # Only proceed if registering as staff
        if base_info.get("user_type") != "2":
            print("This registration is for staff only.")
            return None

        role = input("Role: ").strip()
        department = input("Department: ").strip()

        return cls(
            base_info["sarawak_id"], base_info["password_hash"],
            base_info["full_name"], base_info["email"],
            base_info["phone"], base_info["nric"],
            role, department
        )

    @classmethod
    def from_dict(cls, data):
        return cls(
            sarawak_id=data["sarawak_id"],
            password_hash=data["password_hash"],
            full_name=data["full_name"],
            email_address=data["email"],
            phone_number=data["phone"],
            nric=data["nric"],
            role=data["role"],
            department=data["department"]
        )

    def check_inquiries(self):
        manager = InquiryManager()
        open_inquiries = manager.get_open_inquiries()

        if not open_inquiries:
            print("\nNo open inquiries at the moment.\n")
            return

        print("\n=== Open Inquiries ===")
        for i, inquiry in enumerate(open_inquiries, start=1):
            print(f"{i}. ID: {inquiry.message_id} | Subject: {inquiry.subject} | Category: {inquiry.category} | From: {inquiry.sender_id}")

        try:
            choice = int(input("Select an inquiry to respond to (enter number, or 0 to cancel): "))
            if choice == 0:
                print("Returning to menu...\n")
                return
            selected_inquiry = open_inquiries[choice - 1]
        except (ValueError, IndexError):
            print("Invalid selection. Returning to menu.\n")
            return

        print(f"\n--- Inquiry Content ---\n{selected_inquiry.content}\n")
        response = input("Enter your response: ").strip()

        selected_inquiry.respond(self.sarawak_id, response)
        manager.save_inquiries()

        # Create and send notification
        subject = f"Response to Your Inquiry: {selected_inquiry.subject}"
        content = f"Dear Customer,\n\nYour inquiry has been addressed by our staff.\n\nResponse:\n{response}\n\nRegards,\nCustomer Support"
        notification = Notification(
            sender_id=self.sarawak_id,
            receiver_id=selected_inquiry.sender_id,  # customer id
            subject=subject,
            content=content,
            notification_type="inquiry_response"
        )
        notification.send()

        # Save to Notification.json
        center = NotificationCenter()
        existing_notifications = center.load_notifications_from_file()
        notification_data = {
            "message_id": notification.message_id if hasattr(notification, "message_id") else str(uuid.uuid4()),
            "sender_id": notification.sender_id,
            "receiver_id": notification.receiver_id,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "subject": notification.subject,
            "content": notification.content,
            "notification_type": notification.notification_type,
            "is_read": False,
            "is_removed": False
        }
        existing_notifications.append(notification_data)
        center.save_notifications_to_file(existing_notifications)

        print("Inquiry has been marked as resolved and response saved.")
        print("A notification has been sent to the customer.\n")
        


    def show_staff_menu(self):
        while True:
            print(f"\nWelcome, {self.full_name} ({self.role})")
            print("1. View Dashboard")
            print("2. Check Inquiries")
            print("3. Manage Transactions")
            print("4. Handle Feedback")
            print("5. Manage Merchandise")
            print("6. Sign Out")

            choice = input("Enter your choice (1-6): ").strip()

            if choice == '1':
                print("Not covered in the scenarios.")
            elif choice == '2':
                self.check_inquiries()
            elif choice == '3':
                print("Not covered in the scenarios.")
            elif choice == '4':
                print("Not covered in the scenarios.")
            elif choice == '5':
                print("Not covered in the scenarios.")
            elif choice == '6':
                print("Logging out...\n")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 6.\n")
