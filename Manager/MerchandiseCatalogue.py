import json
from Entity.Merchandise import Merchandise
from datetime import datetime


class MerchandiseCatalogue:
    def __init__(self):
        self.merchandise_list = [] 

    def load_merchandise_from_json(self, filename="Merchandise.json"):
        try:
            with open(filename, 'r') as file:
                data_list = json.load(file)
                for data in data_list:
                    merch = Merchandise(
                        item_id=data["item_id"],
                        name=data["name"],
                        price=data["price"],
                        description=data["description"],
                        availability=data["availability"],
                        category=data["category"],
                        image_url=data["image_url"],
                        last_restocked=datetime.fromisoformat(data["last_restocked"])
                    )
                    self.merchandise_list.append(merch)
        except FileNotFoundError:
            print("Merchandise.json file not found.")
        except Exception as e:
            print(f"Error loading merchandise: {e}")

    def browse_merchandise(self):
        return [item.view_merchandise_details() for item in self.merchandise_list]

    def add_merchandise(self, merchandise):
        self.merchandise_list.append(merchandise)

    def remove_merchandise(self, merch_id):
        self.merchandise_list = [m for m in self.merchandise_list if m.merchandise_id != merch_id]

    def update_merchandise(self, merch_id, **kwargs):
        for m in self.merchandise_list:
            if m.merchandise_id == merch_id:
                m.update_merchandise_info(**kwargs)
                return True
        return False

    def select_merchandise(self, merch_id):
        for m in self.merchandise_list:
            if m.merchandise_id == merch_id:
                return m.view_merchandise_details()
        return None

    def update_merchandise_availability(self, item_id, new_availability):
        try:
            with open("Merchandise.json", "r") as file:
                merchandise_data = json.load(file)

            for merch in merchandise_data:
                if merch.get("item_id") == item_id:
                    merch["availability"] = new_availability
                    merch["last_restocked"] = datetime.now().isoformat()
                    break

            with open("Merchandise.json", "w") as file:
                json.dump(merchandise_data, file, indent=4)

        except FileNotFoundError:
            print("Merchandise.json file not found.")
        except Exception as e:
            print(f"Error updating availability: {e}")
