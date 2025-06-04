import uuid
from datetime import datetime
from Entity.SaleLine import SaleLine
from Entity.Sale import Sale
from Manager.SaleService import SaleService
from Entity.Trip import Trip
from Entity.UserAccount import UserAccount
from Entity.Inquiry import Inquiry
from Manager.InquiryManager import InquiryManager
from Manager.NotificationCenter import NotificationCenter
from Entity.Notification import Notification

class Customer(UserAccount):
    def __init__(self, sarawak_id, password_hash, full_name, email, phone, nric,
                 gender, age, nationality, occupation, dob, address):
        super().__init__(sarawak_id, password_hash, full_name, email, phone, nric)
        self.gender = gender
        self.age = age
        self.nationality = nationality
        self.occupation = occupation
        self.dob = dob
        self.address = address
        self.loyalty_points = 0
        self.payment_methods = []
        self.notification_center = NotificationCenter()

    @classmethod
    def register(cls):
        """
        Override the abstract register method from UserAccount.
        Collects all UserAccount and Customer-specific details.
        """
        print("\n--- Register as Customer ---")
        # Get base info using UserAccount's static method
        base_info = UserAccount.register(user_type="1")
        # Only proceed if registering as customer
        if base_info.get("user_type") != "1":
            print("This registration is for customers only.")
            return None

        gender = input("Gender: ").strip().capitalize()
        while gender not in ["Male", "Female"]:
            print("Invalid gender. Please enter Male or Female.")
            gender = input("Gender: ").strip().capitalize()

        age = int(input("Age: "))
        nationality = input("Nationality: ")
        occupation = input("Occupation: ")

        while True:
            dob = input("Date of Birth (YYYY-MM-DD): ").strip()
            try:
                dob_date = datetime.strptime(dob, "%Y-%m-%d")
                if dob_date > datetime.now():
                    print("Date of birth cannot be in the future.")
                else:
                    break
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD.")
                
        address = input("Address: ")

        return cls(
            base_info["sarawak_id"], base_info["password_hash"],
            base_info["full_name"], base_info["email"],
            base_info["phone"], base_info["nric"],
            gender, age, nationality, occupation, dob, address
        )
    

    def get_payment_methods(self):
        print("Not covered in the scenarios.")

    def place_order(self):
        print("Not covered in the scenarios.")


    def save_transaction(self, sale_line):
        print("Not covered in the scenarios.")


    def manage_payment_methods(self):
        print("Not covered in the scenarios.")
            
    def get_notifications(self):
        """Get and display notifications for this customer using NotificationCenter"""
        customer_notifications = self.notification_center.get_customer_notifications(self.sarawak_id)

        if not customer_notifications:
            print("No new notifications.")
            return []

        # Display notifications
        for notif in customer_notifications:
            print("\n--- Notification ---")
            print(f"Subject: {notif.get('subject')}")
            print(f"From: {notif.get('sender_id')}")
            print(f"Date: {notif.get('timestamp')}")
            print(f"Message: {notif.get('content')}")
            print(f"Type: {notif.get('notification_type')}")
            print(f"Read: {'Yes' if notif.get('is_read') else 'No'}")

        return customer_notifications

    def browse_and_purchase_items(self, catalogue, sale, item_type="merchandise"):
        """Browse and purchase items from catalog"""
        if item_type == "trip":
            departure = Trip.select_station("Select Departure Station:")
            arrival = Trip.select_station("Select Arrival Station:")
            results = catalogue.browse_by_location(departure, arrival)
        else:
            results = catalogue.merchandise_list

        available_items = [item for item in results if item.check_availability()]

        if not available_items:
            print(f"No *available* {item_type}s found.")
            return

        for i, item in enumerate(available_items, start=1):
            print(f"\n{item_type.capitalize()} {i}:")
            print(f"Name: {item.name}")
            print(f"Price: RM{item.price:.2f}")
            if item_type == "trip":
                print(f"Capacity: {getattr(item, 'capacity', 'N/A')} (Total seats)")
                print(f"Availability: {item.availability} (Seats left)")
                print(f"Rating: {getattr(item, 'rating', 'N/A')}")
                print(f"Departure Time: {getattr(item, 'departure_time', 'N/A')}")
                print(f"Arrival Time: {getattr(item, 'arrival_time', 'N/A')}")
            else:
                print(f"Availability: {item.availability}")
                print(f"Rating: {getattr(item, 'rating', 'N/A')}")
                print(f"Description: {item.description}")

        while True:
            try:
                selection = int(input(f"\nSelect {item_type.capitalize()} (0 for back): "))
                if selection == 0:
                    return
                elif 1 <= selection <= len(available_items):
                    selected_item = available_items[selection - 1]
                    quantity = int(input(f"Enter quantity to purchase (Available: {selected_item.availability}): "))
                    if quantity <= 0:
                        print("Quantity must be greater than zero.")
                    elif quantity > selected_item.availability:
                        print("Not enough availability.")
                    else:
                        sale_line = SaleLine(
                            sale_line_id=str(uuid.uuid4()),
                            item_id=selected_item.item_id,
                            item_name=selected_item.name,
                            quantity=quantity,
                            unit_price=selected_item.price
                        )
                        sale.add_sale_line(sale_line)

                        # Don't update availability here - will be updated after payment confirmation
                        print(f"Added {quantity} unit(s) of '{selected_item.name}' to cart.")
                    return
                else:
                    print(f"Invalid {item_type} number.")
            except ValueError:
                print("Please enter a valid number.")

    def ask_for_inquiry(self):
        inquiry_manager = InquiryManager()

        print("Select an inquiry category:")
        print("1. Technical Support")
        print("2. Billing")
        print("3. General")
        category_map = {
            "1": "Technical Support",
            "2": "Billing",
            "3": "General"
        }
        category_choice = input("Enter your choice: ")

        category = category_map.get(category_choice)
        if not category:
            print("Invalid category selected.")
            return

        subject = input("Enter a subject for your inquiry: ")
        content = input("Enter your inquiry message: ")

        inquiry = Inquiry(sender_id=self.sarawak_id, subject=subject, content="", category=category)
        inquiry.write_content(content)  # Use write_content to set the inquiry content
        inquiry_manager.add_inquiry(inquiry)

        print("\nYour inquiry has been submitted and saved.")

    def show_customer_menu(self, trip_catalogue, merchandise_catalogue):
        """Main customer menu interface"""
        sale_service = SaleService()
        
        while True:
            # Create a new sale object for each new purchase session
            sale_id = str(uuid.uuid4())
            sale = Sale(sale_id=sale_id, customer_id=self.sarawak_id)
            
            while True:
                print("\n--- Customer Menu ---")
                if not sale.sale_lines:
                    print("1. Browse Trips")
                    print("2. Browse Merchandise")
                    print("3. View Notifications")
                    print("4. View Purchase History")
                    print("5. Ask for Inquiry")
                    print("6. Sign Out")
                    customer_choice = input("Enter your choice: ")

                    if customer_choice == "1":
                        print("\n--- Browse Trips ---")
                        self.browse_and_purchase_items(trip_catalogue, sale, item_type="trip")

                    elif customer_choice == "2":
                        print("\n--- Browse Merchandise ---")
                        self.browse_and_purchase_items(merchandise_catalogue, sale, item_type="merchandise")
                    
                    elif customer_choice == "3":
                        print("\n--- Your Notifications ---")
                        self.display_notifications()

                    elif customer_choice == "4":
                        # Use SaleService to handle purchase history
                        customer_sales = sale_service.display_customer_purchase_history(self.sarawak_id)
                        if customer_sales:
                            self.handle_trip_actions(customer_sales, sale_service, trip_catalogue)
                    
                    elif customer_choice == "5":
                        print("\n--- Submit an Enquiry ---")
                        self.ask_for_inquiry()

                    elif customer_choice == "6":
                        print("Returning to previous menu.")
                        return
                    else:
                        print("Invalid choice.")
                else:
                    print("1. Browse Trips")
                    print("2. Browse Merchandise")
                    print("3. Proceed to Payment")
                    print("4. Empty Cart and Return to Main Menu")
                    customer_choice = input("Enter your choice: ")

                    if customer_choice == "1":
                        print("\n--- Browse Trips ---")
                        self.browse_and_purchase_items(trip_catalogue, sale, item_type="trip")
                    elif customer_choice == "2":
                        print("\n--- Browse Merchandise ---")
                        self.browse_and_purchase_items(merchandise_catalogue, sale, item_type="merchandise")
                    elif customer_choice == "3":
                        # Updated to call the Sale class method with catalogues
                        if sale.record_payment(self.payment_methods, sale_service, trip_catalogue, merchandise_catalogue):
                            break  # Break out of the inner loop to create a new sale
                    elif customer_choice == "4":
                        print("\nCart emptied. Returning to main menu.")
                        break  # Break out of the inner loop to create a new sale
                    else:
                        print("Invalid choice.")

    def display_notifications(self):
        """Display notifications with interactive actions using Notification class"""
        customer_notifications = self.notification_center.get_customer_notifications(self.sarawak_id)

        if not customer_notifications:
            print("You have no new notifications.")
            return

        # Display notifications with numbering
        for idx, notif in enumerate(customer_notifications, 1):
            read_status = "✓" if notif.get('is_read') else "●"
            print(f"\n{idx}. {read_status} [{notif.get('timestamp', 'N/A')}]")
            print(f"   Subject : {notif.get('subject', 'No Subject')}")
            print(f"   Type    : {notif.get('notification_type', 'N/A')}")
            print(f"   Content : {notif.get('content', '')}")

        # Delegate actions to Notification class
        Notification.handle_notification_actions(self.sarawak_id, customer_notifications, self.notification_center)

    def handle_trip_actions(self, customer_sales, sale_service, trip_catalogue):
        """Handle trip rescheduling and refund actions"""
        while True:
            try:
                choice = int(input("\nSelect a trip for actions (0 to go back): "))
                if choice == 0:
                    break
                elif 1 <= choice <= len(customer_sales):
                    selected_sale = customer_sales[choice - 1]
                    print(f"\n--- Action Menu for Sale ID: {selected_sale['Sale ID']} ---")
                    print("1. Reschedule Trip")
                    print("2. Request Refund")
                    print("0. Back")

                    action = input("Enter your choice: ")
                    if action == "1":
                        self.handle_reschedule(selected_sale, trip_catalogue, sale_service)
                    elif action == "2":
                        self.handle_refund(selected_sale, sale_service)
                    elif action == "0":
                        continue
                    else:
                        print("Invalid action.")
                else:
                    print("Invalid selection.")
            except ValueError:
                print("Please enter a valid number.")

    def handle_reschedule(self, selected_sale, trip_catalogue, sale_service):
        """Handle trip rescheduling using Trip class methods"""
        
        print(f"\n--- Rescheduling for Sale ID: {selected_sale['Sale ID']} ---")
        
        # Get trip lines using Trip class method
        trip_lines = Trip.get_trip_lines_from_sale(selected_sale)
        
        if not trip_lines:
            print("No trip sale lines found in this sale.")
            return
        
        # Display trip lines using Trip class method
        Trip.display_trip_lines(trip_lines)
        
        try:
            trip_choice = int(input("Select a trip to reschedule (0 to cancel): "))
            if trip_choice == 0:
                return
            
            # Use Trip class static method for rescheduling
            success = Trip.reschedule_trip(self.sarawak_id, selected_sale, trip_choice, trip_catalogue, sale_service)
            
            if success:
                print("Trip rescheduled successfully!")
            else:
                print("Failed to reschedule trip.")
                
        except ValueError:
            print("Invalid input. Please enter a number.")

    def handle_refund(self, selected_sale, sale_service):
        from Entity.Trip import Trip
        
        print(f"\n--- Refund for Sale ID: {selected_sale['Sale ID']} ---")
        
        # Get refundable trip lines using Trip class method
        refundable_lines = Trip.get_trip_lines_from_sale(selected_sale)
        
        if not refundable_lines:
            print("No refundable trips found in this sale.")
            return
        
        # Display refundable trip lines using Trip class method
        Trip.display_refundable_trip_lines(refundable_lines)
        
        try:
            refund_choice = int(input("Select a trip to request refund (0 to cancel): "))
            if refund_choice == 0:
                return
            
            # Use Trip class static method for refund processing
            success = Trip.process_refund(self.sarawak_id, selected_sale, refund_choice, sale_service)
            
            if success:
                print("Refund processed successfully!")
            else:
                print("Failed to process refund.")
                
        except ValueError:
            print("Invalid input. Please enter a number.")

    @staticmethod
    def from_dict(data: dict):
        customer = Customer(
            sarawak_id=data.get("sarawak_id"),
            password_hash=data.get("password_hash"),
            full_name=data.get("full_name"),
            email=data.get("email"),
            phone=data.get("phone"),
            nric=data.get("nric"),
            gender=data.get("gender"),
            age=data.get("age"),
            nationality=data.get("nationality"),
            occupation=data.get("occupation"),
            dob=data.get("dob"),
            address=data.get("address")
        )
        # Set loyalty_points and payment_methods if they exist
        customer.loyalty_points = data.get("loyalty_points", 0)
        customer.payment_methods = data.get("payment_methods", [])

        return customer