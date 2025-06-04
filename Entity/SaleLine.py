from Entity.Transaction import Transaction

class SaleLine:
    def __init__(self, sale_line_id: str, item_id: str, item_name: str, quantity: int, unit_price: float):
        self.sale_line_id = sale_line_id
        self.item_id = item_id
        self.item_name = item_name
        self.quantity = quantity
        self.unit_price = unit_price
        self.transaction: Transaction = self.create_transaction()

    def create_transaction(self):
        subtotal = self.quantity * self.unit_price
        return Transaction(amount=subtotal)

    def calculate_subtotal(self):
        return self.quantity * self.unit_price

    def generate_summary(self):
        return {
            "Sale Line ID": self.sale_line_id,
            "Item ID": self.item_id,
            "Item Name": self.item_name,
            "Quantity": self.quantity,
            "Unit Price": self.unit_price,
            "Subtotal": self.calculate_subtotal(),
            "Transaction": self.transaction.get_summary()
        }
