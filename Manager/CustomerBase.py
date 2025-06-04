# CustomerBase.py
import json
from Entity.Customer import Customer
from Entity.UserAccount import UserAccount

CUSTOMER_JSON_PATH = 'Customer.json'

class CustomerBase:
    def __init__(self):
        self.customers = []


    def add_customer(self, customer: Customer):
        # Load existing data
        try:
            with open(CUSTOMER_JSON_PATH, 'r') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []

        # Convert Customer object to dict
        customer_data = {
            "sarawak_id": customer.sarawak_id,
            "password_hash": customer.password_hash,
            "full_name": customer.full_name,
            "email": customer.email,
            "phone": customer.phone,
            "nric": customer.nric,
            "gender": customer.gender,
            "age": customer.age,
            "nationality": customer.nationality,
            "occupation": customer.occupation,
            "dob": customer.dob,
            "address": customer.address,
            "loyalty_points": customer.loyalty_points,
            "payment_methods": customer.payment_methods
        }

        # Append and save
        data.append(customer_data)
        with open(CUSTOMER_JSON_PATH, 'w') as f:
            json.dump(data, f, indent=4)

        print(f"Customer {customer.full_name} registered and saved to {CUSTOMER_JSON_PATH}.")
        self.customers.append(customer)

    # --------------------------------------------------------------
    def load_customers_from_file(self):
        try:
            with open(CUSTOMER_JSON_PATH, 'r') as f:
                data = json.load(f)
                for c in data:
                    customer = Customer(
                        sarawak_id=c['sarawak_id'],
                        password_hash=c['password_hash'],
                        full_name=c['full_name'],
                        email=c['email'],
                        phone=c['phone'],
                        nric=c['nric'],
                        gender=c['gender'],
                        age=c['age'],
                        nationality=c['nationality'],
                        occupation=c['occupation'],
                        dob=c['dob'],
                        address=c['address']
                    )
                    customer.loyalty_points = c.get('loyalty_points', 0)
                    customer.payment_methods = c.get('payment_methods', [])
                    self.customers.append(customer)
        except FileNotFoundError:
            print(f"{CUSTOMER_JSON_PATH} not found. Starting with empty customer base.")
        except json.JSONDecodeError:
            print(f"Invalid JSON in {CUSTOMER_JSON_PATH}.")

    @staticmethod
    def load_users(filename='Customer.json'):
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []