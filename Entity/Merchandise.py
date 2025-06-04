from Entity.SellableItem import SellableItem
from datetime import datetime


class Merchandise(SellableItem):
    def __init__(self, item_id, name, price, description, availability, category, image_url, last_restocked=None):
        super().__init__(item_id, name, price, description, availability)
        self.merchandise_id = item_id  # alias
        self.category = category
        self.image_url = image_url
        self.last_restocked = last_restocked if last_restocked else datetime.now()

    def create_item(self):
        return f"Merchandise '{self.name}' created successfully."

    def view_merchandise_details(self):
        details = self.view_item_details()
        details.update({
            "Merchandise ID": self.merchandise_id,
            "Category": self.category,
            "Image URL": self.image_url,
            "Last Restocked": self.last_restocked
        })
        return details

    def check_stock_availability(self):
        return self.check_availability()

    def restock(self, quantity):
        pass

    def update_merchandise_info(self, **kwargs):
        self.update_item_info(**kwargs)
