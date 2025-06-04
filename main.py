from Entity.Customer import Customer
from Entity.Staff import Staff
from Entity.UserAccount import UserAccount 
from Manager.TripCatalogue import TripCatalogue  
from Manager.MerchandiseCatalogue import MerchandiseCatalogue
from Manager.CustomerBase import CustomerBase
from Manager.StaffBase import StaffBase
import os

current_customer = None

def main():
    global current_customer  # Declare global inside function

    while True:
        print("\n=== Welcome to the Kuching ART System ===")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            user_type = input("Register as (1 for Customer, 2 for Staff): ").strip()
            if user_type == "1":
                customer = Customer.register()
                customer_base = CustomerBase()
                customer_base.add_customer(customer)
            elif user_type == "2":
                staff = Staff.register()
                staff_base = StaffBase()
                staff_base.add_staff(staff)

            else:
                print("Invalid registration type.")
            
        elif choice == "2":
            user, login_type = UserAccount.login()

            if user and login_type == "1":
                current_customer = Customer.from_dict(user)

                trip_catalogue = TripCatalogue()
                trip_catalogue.load_trips_from_json()
                merchandise_catalogue = MerchandiseCatalogue()
                merchandise_catalogue.load_merchandise_from_json()

                current_customer.show_customer_menu(trip_catalogue, merchandise_catalogue)


            elif user and login_type == "2":
                current_staff = Staff.from_dict(user)
                current_staff.show_staff_menu()  

                

        elif choice == "3":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
