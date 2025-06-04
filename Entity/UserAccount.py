# UserAccount.py
from abc import ABC, abstractmethod
import hashlib
import json
import os
import re

class UserAccount(ABC):
    def __init__(self, sarawak_id, password_hash, full_name, email, phone, nric):
        self.sarawak_id = sarawak_id
        self.password_hash = password_hash
        self.full_name = full_name
        self.email = email
        self.phone = phone
        self.nric = nric
        self.is_disabled = False
        self.is_logged_in = False
        self.last_login = None
        self.linked_accounts = []

    @abstractmethod
    def register(user_type):
        # Determine the filename based on user type
        filename = 'Customer.json' if user_type == "1" else 'Staff.json'

        # Check for a unique Sarawak ID
        while True:
            sarawak_id = input("Sarawak ID: ").strip()
            if not sarawak_id:
                print("Sarawak ID cannot be empty.")
                continue
            
            users = UserAccount.load_users(filename)
            if any(user.get("sarawak_id") == sarawak_id for user in users):
                print("Sarawak ID already exists. Please enter a different ID.")
            else:
                break

        raw_password = input("Password (min 6 chars): ").strip()
        while len(raw_password) < 6:
            print("Password too short. Please enter at least 6 characters.")
            raw_password = input("Password (min 6 chars): ").strip()

        full_name = input("Full Name: ").strip()
        while not full_name:
            print("Full Name cannot be empty.")
            full_name = input("Full Name: ").strip()

        email = input("Email: ").strip()
        while not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            print("Invalid email format.")
            email = input("Email: ").strip()

        phone = input("Phone: ").strip()
        while not phone.isdigit() or len(phone) < 10:
            print("Phone must be numeric and at least 10 digits.")
            phone = input("Phone (numbers only): ").strip()

        nric = input("NRIC (12 digits): ").strip()
        while not (nric.isdigit() and len(nric) == 12):
            print("NRIC must be 12 digits.")
            nric = input("NRIC (12 digits): ").strip()

        password_hash = UserAccount.hash_password(raw_password)

        return {
            "user_type": user_type,
            "sarawak_id": sarawak_id,
            "password_hash": password_hash,
            "full_name": full_name,
            "email": email,
            "phone": phone,
            "nric": nric
        }
    
    @staticmethod
    def login():
        print("\n--- Login ---")
        print("1. Customer")
        print("2. Staff")
        login_type = input("Login as (1 for Customer, 2 for Staff): ").strip()

        if login_type not in ["1", "2"]:
            print("Invalid login type selected. Returning to main menu...")
            return None, None

        sarawak_id = input("Enter Sarawak ID: ").strip()
        password = input("Enter Password: ").strip()

        # Load user data using path directly (generic, not limited to customers)
        filename = 'Customer.json' if login_type == "1" else 'Staff.json'
        try:
            with open(filename, 'r') as f:
                user_list = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            print(f"Failed to load user data from {filename}")
            return None, None

        user = UserAccount.authenticate(user_list, sarawak_id, password)
        if user:
            print(f"{user.get('full_name')} logged in successfully!")
            return user, login_type
        else:
            print("Invalid Sarawak ID or password.")
            return None, None

    def sign_out(self):
        self.is_logged_in = False

    def reset_credentials(self, new_password=None, new_linked_accounts=None):
        print("Not covered in the scenarios.")

    @staticmethod
    def authenticate(user_list, sarawak_id, password):
        password_hash = UserAccount.hash_password(password)
        for user in user_list:
            if user.get('sarawak_id') == sarawak_id and user.get('password_hash') == password_hash:
                return user
        return None
    
    def link_auth_provider():
        pass

    def update_profile(self, full_name=None, email=None, phone=None):
        pass

    def enable_account(self):
        pass

    def disable_account(self):
        pass

    # ----------------------------------------------------
    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def load_users(filename):
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return []
        return []

    
    
    

    


    

