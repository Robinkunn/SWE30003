from abc import ABC, abstractmethod
from datetime import datetime



class SellableItem(ABC):
    def __init__(self, item_id: str, name: str, price: float, description: str,
                 availability: int, rating: float = 0.0, status: str = "active"):
        self.item_id = item_id
        self.name = name
        self.price = price
        self.description = description
        self.availability = availability
        self.rating = rating
        self.status = status
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def view_item_details(self) -> dict:
        return {
            "Item ID": self.item_id,
            "Name": self.name,
            "Price": f"RM{self.price:.2f}",
            "Description": self.description,
            "Availability": self.availability,
            "Rating": self.rating,
            "Status": self.status,
            "Created At": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "Updated At": self.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        }

    def check_availability(self) -> bool:
        return self.availability > 0

    def update_item_info(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.now()

    @abstractmethod
    def create_item(self):
        pass

    @staticmethod
    def print_receipt(sale, payment_method):
        print("\n--- Sale Receipt ---")
        print(f"Sale ID: {sale.sale_id}")
        print(f"Customer ID: {sale.customer_id}")
        print(f"Date: {sale.sale_datetime.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Payment Method: {payment_method['Payment Type']} - {payment_method['Masked Number']}")
        print("\nItems Purchased:")

        total_amount = 0
        for i, line in enumerate(sale.sale_lines, 1):
            line_total = line.quantity * line.unit_price
            total_amount += line_total
            print(f"{i}. {line.item_name} (x{line.quantity}) @ RM{line.unit_price:.2f} each - RM{line_total:.2f}")
            if hasattr(line, 'transaction') and line.transaction:
                qr_code_id = getattr(line.transaction, 'qr_code_id', None)
            if qr_code_id:
                print(f"    QR Code ID: {qr_code_id}")

        print(f"\nTotal Amount: RM{total_amount:.2f}")
        print("-----------------------------")
        print("Thank you for your purchase!")