from Entity.SaleLine import SaleLine
from typing import List
from datetime import datetime
import json

class Sale:
    def __init__(self, sale_id: str, customer_id: str):
        self.sale_id = sale_id
        self.customer_id = customer_id
        self.sale_datetime = datetime.now()
        self.sale_lines: List[SaleLine] = []
        self.payment_status = "Pending"
        self.total_amount = 0.0

    def add_sale_line(self, sale_line: SaleLine):
        self.sale_lines.append(sale_line)
        self.calculate_total()

    def remove_sale_line(self, sale_line_id: str):
        self.sale_lines = [line for line in self.sale_lines if line.sale_line_id != sale_line_id]
        self.calculate_total()

    def calculate_total(self):
        self.total_amount = sum(line.calculate_subtotal() for line in self.sale_lines)

    def record_payment(self, customer_payment_methods, sale_service, trip_catalogue=None, merchandise_catalogue=None):
        if not self.sale_lines:
            print("\nNo items were purchased. Sale not recorded.")
            return False

        print("\n--- Payment Method ---")
        payment_methods = customer_payment_methods

        if not payment_methods:
            print("No saved payment methods found. Please add a payment method before proceeding.")
            return False

        for idx, method in enumerate(payment_methods, start=1):
            print(f"{idx}. {method['Payment Type']} - {method['Masked Number']} (Expiry: {method['Expiry Date']}, Provider: {method['Provider Name']})")

        while True:
            try:
                selection = int(input("Select a payment method: "))
                if 1 <= selection <= len(payment_methods):
                    selected_payment = payment_methods[selection - 1]
                    break
                else:
                    print("Please select a valid number from the list.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        # NOW update availability after payment method is selected
        self._update_item_availability(trip_catalogue, merchandise_catalogue)

        # Proceed to record the sale
        sale_service.add_sale(self)
        all_sales = sale_service.get_all_sales()  # Use SaleService to load sales

        summary = self.generate_summary()
        summary["Payment Method"] = {
            "Payment Type": selected_payment["Payment Type"],
            "Masked Number": selected_payment["Masked Number"],
            "Expiry Date": selected_payment["Expiry Date"],
            "Provider Name": selected_payment["Provider Name"]
        }

        all_sales.append(summary)

        sale_service.save_all_sales(all_sales)  # Use SaleService to save sales

        print("\nSale recorded successfully with selected payment method.")
        self.print_receipt(selected_payment)
        
        # After printing the receipt, ask if the user wants to continue shopping
        print("\n--- Thank you for your purchase! ---")
        print("Starting a new shopping session...")
        
        return True

    def _update_item_availability(self, trip_catalogue, merchandise_catalogue):
        for sale_line in self.sale_lines:
            # Check if it's a trip or merchandise based on catalogues
            if trip_catalogue:
                trip_items = trip_catalogue.trip_list if hasattr(trip_catalogue, 'trip_list') else []
                for item in trip_items:
                    if item.item_id == sale_line.item_id:
                        item.availability -= sale_line.quantity
                        item.updated_at = datetime.now()
                        trip_catalogue.update_trip_availability(item.item_id, item.availability)
                        break
            
            if merchandise_catalogue:
                merchandise_items = merchandise_catalogue.merchandise_list if hasattr(merchandise_catalogue, 'merchandise_list') else []
                for item in merchandise_items:
                    if item.item_id == sale_line.item_id:
                        item.availability -= sale_line.quantity
                        item.updated_at = datetime.now()
                        merchandise_catalogue.update_merchandise_availability(item.item_id, item.availability)
                        break

    def print_receipt(self, payment_method):
        print("\n--- Sale Receipt ---")
        print(f"Sale ID: {self.sale_id}")
        print(f"Customer ID: {self.customer_id}")
        print(f"Date: {self.sale_datetime.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Payment Method: {payment_method['Payment Type']} - {payment_method['Masked Number']}")
        print("\nItems Purchased:")

        total_amount = 0
        for i, line in enumerate(self.sale_lines, 1):
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

    def generate_summary(self):
        return {
            "Sale ID": self.sale_id,
            "Customer ID": self.customer_id,
            "Date": self.sale_datetime.isoformat(),
            "Total": self.total_amount,
            "Payment Status": self.payment_status,
            "Items": [line.generate_summary() for line in self.sale_lines]
        }