from abc import ABC, abstractmethod
from Entity.Sale import Sale
from typing import List, Optional
from datetime import datetime
import json
import os

class SaleService(ABC):
    def __init__(self):
        self.sales: List[Sale] = []

    def add_sale(self, sale: Sale):
        self.sales.append(sale)

    def get_sale_by_id(self, sale_id: str) -> Optional[Sale]:
        return next((s for s in self.sales if s.sale_id == sale_id), None)

    def filter_sales(self, from_date: datetime = None, to_date: datetime = None, min_amount: float = None):
        filtered = self.sales
        if from_date:
            filtered = [s for s in filtered if s.sale_datetime >= from_date]
        if to_date:
            filtered = [s for s in filtered if s.sale_datetime <= to_date]
        if min_amount:
            filtered = [s for s in filtered if s.total_amount >= min_amount]
        return filtered

    def calculate_total_revenue(self):
        return sum(s.total_amount for s in self.sales if s.payment_status == "Completed")

    def generate_report(self, summary=True):
        return [sale.generate_summary() for sale in self.sales] if summary else self.sales

    def get_customer_purchase_history(self, customer_id: str):
        """Get purchase history for a specific customer"""
        try:
            with open("Sale.json", "r") as f:
                all_sales = json.load(f)
            customer_sales = [s for s in all_sales if s["Customer ID"] == customer_id]
            return customer_sales
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def display_customer_purchase_history(self, customer_id: str):
        """Display purchase history for a specific customer"""
        customer_sales = self.get_customer_purchase_history(customer_id)
        
        if not customer_sales:
            print("No purchase history found.")
            return customer_sales
        
        print("\n--- Purchase History ---")
        for i, s in enumerate(customer_sales, 1):
            print("\n===============================")
            print(f"Purchase {i}")
            print(f"Sale ID       : {s['Sale ID']}")
            print(f"Customer ID   : {s['Customer ID']}")
            print(f"Date          : {s['Date']}")
            print(f"Payment Method: {s.get('Payment Method', 'N/A')}")
            print("\nItems Purchased:")
            print("-" * 50)
            total = 0.0
            for idx, line in enumerate(s['Items'], 1):
                name = line['Item Name']
                quantity = line['Quantity']
                unit_price = line['Unit Price']
                line_total = quantity * unit_price
                total += line_total
                print(f"{idx}. {name} (x{quantity}) @ RM{unit_price:.2f} - RM{line_total:.2f}")
                if 'QR Code ID' in line:
                    print(f"   QR Code ID: {line['QR Code ID']}")
            print("-" * 50)
            print(f"Total Amount: RM{total:.2f}")
            print("===============================\n")
        
        return customer_sales

    def get_all_sales(self):
        """Load all sales from Sale.json"""
        try:
            with open("Sale.json", "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_all_sales(self, all_sales):
        """Save all sales to Sale.json"""
        with open("Sale.json", "w") as f:
            json.dump(all_sales, f, indent=2)