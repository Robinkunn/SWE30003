from datetime import datetime
import json
import uuid

class Transaction:
    def __init__(self, amount: float, transaction_type: str = "Purchase", transaction_id: str = None):
        self.transaction_id = transaction_id or self.generate_transaction_id()
        self.transaction_type = transaction_type
        self.transaction_datetime = datetime.now()
        self.transaction_status = "Pending"
        self.amount = amount
        self.qr_code_id = self.generate_qr_code_id()

    def generate_transaction_id(self):
        return f"T{uuid.uuid4().hex[:8].upper()}" 
    
    def generate_qr_code_id(self):
        return f"QR{uuid.uuid4().hex[:8].upper()}" 

    def get_summary(self):
        return {
            "Transaction ID": self.transaction_id,
            "Type": self.transaction_type,
            "Date": self.transaction_datetime.isoformat(),
            "Status": self.transaction_status,
            "Amount": self.amount,
            "QR Code ID": self.qr_code_id,

        }

    def generate_receipt(self):
        return f"Receipt: {self.transaction_id} - {self.transaction_type} - {self.amount} - {self.transaction_status}"

    def generate_qr_data(self):
        return f"{self.transaction_id}|{self.amount}|{self.transaction_status}|{self.qr_code_id}"


    def process_refund(self, sale_service) -> bool:
        """Allow refund only within 3 days after the transaction was made and update Sale.json using SaleService."""
        try:
            now = datetime.now()
            days_since_purchase = (now - self.transaction_datetime).days

            if days_since_purchase <= 3:
                self.transaction_status = "Refunded"
                self.transaction_type = "Refund"

                # Use SaleService to load and update sales
                sales = sale_service.get_all_sales()

                updated = False
                for sale in sales:
                    items = sale.get("Items", [])
                    for item in items:
                        transaction = item.get("Transaction", {})
                        if transaction.get("Transaction ID") == self.transaction_id:
                            # Update the transaction in-place
                            transaction["Status"] = self.transaction_status
                            transaction["Type"] = self.transaction_type
                            updated = True
                            break
                    if updated:
                        break

                if updated:
                    sale_service.save_all_sales(sales)
                    print("Refund approved and Sale.json updated.")
                    return True
                else:
                    print("Refund approved but transaction not found in Sale.json.")
                    return False
            else:
                print("Refund denied: more than 3 days since purchase.")
                return False

        except Exception as e:
            print(f"Error processing refund: {e}")
            return False

    @staticmethod
    def get_transaction_by_transaction_id(transaction_id): 
        try:
            with open("Sale.json", "r") as f:
                sales = json.load(f)

                for sale in sales:
                    items = sale.get("Items", [])
                    for item in items:
                        transaction = item.get("Transaction")
                        if transaction and transaction.get("Transaction ID") == transaction_id:
                            return Transaction.from_dict(transaction, item.get("Item ID"))  
        except Exception as e:
            print(f"Error reading Sale.json: {e}")
        return None
    
    @staticmethod
    def from_dict(data: dict, item_id: str = None):
        t = Transaction(
            amount=data.get("Amount", 0.0),
            transaction_type=data.get("Type", "Purchase"),
            transaction_id=data.get("Transaction ID")
        )
        t.transaction_datetime = datetime.fromisoformat(data.get("Date"))
        t.transaction_status = data.get("Status", "Pending")
        t.qr_code_id = data.get("QR Code ID")
        t.item_id = item_id  # Needed for refund logic
        return t



