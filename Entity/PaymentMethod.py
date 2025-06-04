class PaymentMethod:
    def __init__(self, payment_type=None, masked_number=None, expiry_date=None, provider_name=None, is_valid=True):
        self.payment_type = payment_type
        self.masked_number = masked_number
        self.expiry_date = expiry_date
        self.provider_name = provider_name
        self.is_valid = is_valid

    def store_payment_details(self, payment_type, masked_number, expiry_date, provider_name):
        print("Not convered in the scenarios")
        
    def validate_payment_information(self):
        print("Not convered in the scenarios")

    def deactivate_payment_method(self):
        print("Not convered in the scenarios")

    def display_masked_payment_info(self):
        print("Not convered in the scenarios")

    def create_method(self):
        return {
            "Payment Type": "Credit Card",
            "Masked Number": "************1111",
            "Expiry Date": "12/2026",
            "Provider Name": "Visa",
            "Is Valid": True
        }
