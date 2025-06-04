# StaffBase.py
import json
from Entity.Staff import Staff

STAFF_JSON_PATH = 'Staff.json'

class StaffBase:
    def __init__(self):
        self.staff_collection = {}

    def load_staff_from_file(self):
        try:
            with open(STAFF_JSON_PATH, 'r') as f:
                data = json.load(f)
                for s in data:
                    staff = Staff(
                        sarawak_id=s['sarawak_id'],
                        password_hash=s['password_hash'],
                        full_name=s['full_name'],
                        email_address=s['email'],
                        phone_number=s['phone'],
                        nric=s['nric'],
                        role=s['role'],
                        department=s['department'],
                        responsibilities=s.get('responsibilities', []),
                        assigned_modules=s.get('assigned_modules', [])
                    )
                    self.staff_collection[s['sarawak_id']] = staff
        except FileNotFoundError:
            print(f"{STAFF_JSON_PATH} not found. Starting with empty staff base.")
        except json.JSONDecodeError:
            print(f"Invalid JSON in {STAFF_JSON_PATH}.")

    def add_staff(self, staff):
        # Load existing staff data from JSON
        try:
            with open(STAFF_JSON_PATH, 'r') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []

        # Convert staff object to dict (you can add a to_dict() method to Staff for this)
        staff_data = {
            "sarawak_id": staff.sarawak_id,
            "password_hash": staff.password_hash,
            "full_name": staff.full_name,
            "email": staff.email,
            "phone": staff.phone,
            "nric": staff.nric,
            "role": staff.role,
            "department": staff.department
        }

        # Append new staff data and save back
        data.append(staff_data)
        with open(STAFF_JSON_PATH, 'w') as f:
            json.dump(data, f, indent=4)

        # Update in-memory collection
        self.staff_collection[staff.sarawak_id] = staff
        print(f"Staff {staff.full_name} added to the system and saved to {STAFF_JSON_PATH}.")
        
    def remove_staff_by_id(self, sarawak_id):
        if sarawak_id in self.staff_collection:
            removed = self.staff_collection.pop(sarawak_id)
            print(f"Staff {removed.full_name} removed from the system.")
        else:
            print(f"No staff found with Sarawak ID {sarawak_id}.")

    def search_staff_by_id(self, sarawak_id):
        return self.staff_collection.get(sarawak_id)

    def search_staff_by_role_or_department(self, role=None, department=None):
        result = []
        for staff in self.staff_collection.values():
            if (role and staff.role == role) or (department and staff.department == department):
                result.append(staff)
        return result

    def update_staff_profile(self, sarawak_id, **kwargs):
        staff = self.search_staff_by_id(sarawak_id)
        if staff:
            staff.update_profile(**kwargs)
        else:
            print(f"No staff found with Sarawak ID {sarawak_id}.")

    def list_all_staff(self):
        return list(self.staff_collection.values())
