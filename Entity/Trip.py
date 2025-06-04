from Entity.SellableItem import SellableItem
from Entity.Transaction import Transaction
from Manager.NotificationCenter import NotificationCenter


class Trip(SellableItem):
    def __init__(self, item_id, name, price, description, availability, capacity, route_code,
                 departure_station, arrival_station, departure_time, arrival_time, feeder_bus, rating=0.0):
        super().__init__(item_id, name, price, description, availability, rating=rating)
        self.trip_id = item_id  
        self.route_code = route_code
        self.departure_station = departure_station
        self.arrival_station = arrival_station
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.feeder_bus = feeder_bus
        self.capacity = capacity  # total seats, never changes

    def create_item(self):
        # This would typically store the trip in a database or system
        return f"Trip '{self.name}' created successfully."

    def view_trip_details(self):
        details = self.view_item_details()
        details.update({
            "Trip ID": self.trip_id,
            "Route Code": self.route_code,
            "Departure Station": self.departure_station,
            "Arrival Station": self.arrival_station,
            "Departure Time": self.departure_time,
            "Arrival Time": self.arrival_time,
            "Feeder Bus": self.feeder_bus,
            "Capacity": self.capacity
        })
        return details

    def check_seat_availability(self):
        return self.check_availability()

    def reserve_seat(self):
        print("Not covered in the scenarios.")

    def update_trip_info(self, **kwargs):
        self.update_item_info(**kwargs)

    @staticmethod
    def reschedule_trip(customer_id, selected_sale, trip_choice, trip_catalogue, sale_service):
        notification_center = NotificationCenter()
        
        # Step 1: Show sale lines that are of type 'trip'
        trip_lines = [
            (idx, item) for idx, item in enumerate(selected_sale['Items'])
            if "T" in item['Item ID']
        ]

        if not trip_lines:
            print("No trip sale lines found in this sale.")
            return False

        if trip_choice < 1 or trip_choice > len(trip_lines):
            print("Invalid trip selection.")
            return False

        try:
            original_index, selected_line = trip_lines[trip_choice - 1]

            # Step 2: Extract search criteria
            original_price = selected_line['Unit Price']
            original_name = selected_line['Item Name']

            # Step 3: Use TripCatalogue to get all trips
            matching_trips = []
            for trip in trip_catalogue.trips:
                if trip.name == original_name and trip.price == original_price and trip.check_seat_availability():
                    matching_trips.append(trip)

            if not matching_trips:
                print("No matching trips found for rescheduling.")
                return False

            print("\nAvailable Trips for Rescheduling:")
            for i, t in enumerate(matching_trips, 1):
                print(f"{i}. {t.name} - Departure: {t.departure_time}")

            new_trip_choice = int(input("Select a new trip: "))
            if 1 <= new_trip_choice <= len(matching_trips):
                new_trip = matching_trips[new_trip_choice - 1]

                # Step 4: Update the selected Sale Line
                selected_line['Item ID'] = new_trip.trip_id
                selected_line['Item Name'] = new_trip.name
                selected_line['Unit Price'] = new_trip.price

                # Update nested transaction type too
                if 'Transaction' in selected_line:
                    selected_line['Transaction']['Type'] = "Reschedule"

                print(f"Trip rescheduled to: {new_trip.name}")

                # Step 5: Create notification using NotificationCenter
                success = notification_center.create_reschedule_notification(
                    customer_id=customer_id,
                    trip_name=selected_line['Item Name'],
                    trip_id=selected_line['Item ID'],
                )

                if success:
                    print("Reschedule notification created successfully!")
                else:
                    print("Warning: Failed to create notification, but trip was rescheduled.")

                # Step 6: Save back the updated sales list using SaleService
                try:
                    all_sales = sale_service.get_all_sales()  # You need to implement this method in SaleService
                    # Find and update the correct sale
                    for i, sale in enumerate(all_sales):
                        if sale['Sale ID'] == selected_sale['Sale ID']:
                            all_sales[i] = selected_sale
                            break
                    sale_service.save_all_sales(all_sales)  # You need to implement this method in SaleService
                    print("Sale updated successfully!")
                    return True
                except Exception as e:
                    print(f"Error saving sale: {e}")
                    return False
            else:
                print("Invalid selection.")
                return False
                
        except ValueError:
            print("Invalid input. Please enter a number.")
            return False
        except Exception as e:
            print(f"An error occurred during rescheduling: {e}")
            return False

    @staticmethod
    def process_refund(customer_id, selected_sale, refund_choice, sale_service):
        notification_center = NotificationCenter()

        # Step 1: Identify refundable trip lines
        refundable_lines = [
            (idx, item) for idx, item in enumerate(selected_sale['Items'])
            if "T" in item['Item ID']
        ]

        if not refundable_lines:
            print("No refundable trips found in this sale.")
            return False

        if refund_choice < 1 or refund_choice > len(refundable_lines):
            print("Invalid refund selection.")
            return False

        try:
            _, selected_line = refundable_lines[refund_choice - 1]

            # Step 2: Process refund
            transaction = Transaction.get_transaction_by_transaction_id(
                selected_line.get("Transaction", {}).get("Transaction ID")
            )

            if transaction is None:
                print("No transaction found for this trip.")
                return False

            if transaction.process_refund(sale_service):
                print("Refund processed successfully.")
                refund_amount = selected_line['Unit Price'] * selected_line['Quantity']

                # Step 3: Create notification using NotificationCenter
                success = notification_center.create_refund_notification(
                    customer_id=customer_id,
                    trip_name=selected_line['Item Name'],
                    trip_id=selected_line['Item ID'],
                    refund_amount=refund_amount
                )

                if success:
                    print("Refund notification created successfully!")
                else:
                    print("Warning: Failed to create notification, but refund was processed.")
                
                return True
            else:
                print("Refund not allowed. Trip may have already departed.")
                return False
                
        except Exception as e:
            print(f"An error occurred during refund processing: {e}")
            return False

    @staticmethod
    def select_station(prompt: str) -> str:
        """Helper method to select station from available options"""
        from Entity.Enum.Station import Station  # Local import to avoid circular dependency
        print(f"\n{prompt}")
        stations = Station.list_stations()
        for idx, station in enumerate(stations, start=1):
            print(f"{idx}. {station.value}")

        while True:
            try:
                choice = int(input("Enter the number of your choice: "))
                if 1 <= choice <= len(stations):
                    return stations[choice - 1].value
                else:
                    print("Please choose a valid number from the list.")
            except ValueError:
                print("Invalid input. Please enter a number.")
                
    @staticmethod
    def get_trip_lines_from_sale(sale):
        return [(idx, item) for idx, item in enumerate(sale['Items']) if "T" in item['Item ID']]

    @staticmethod
    def display_trip_lines(trip_lines):
        if not trip_lines:
            print("No trip lines found.")
            return
            
        print("\nTrip Lines:")
        for i, (idx, line) in enumerate(trip_lines, 1):
            print(f"{i}. {line['Item Name']} (x{line['Quantity']}) @ RM{line['Unit Price']:.2f}")

    @staticmethod
    def display_refundable_trip_lines(refundable_lines):
        """
        Display refundable trip lines in a formatted way
        
        Args:
            refundable_lines (list): List of tuples containing (index, trip_item)
        """
        if not refundable_lines:
            print("No refundable trip lines found.")
            return
            
        print("\nRefundable Trip Lines:")
        for i, (idx, line) in enumerate(refundable_lines, 1):
            print(f"{i}. {line['Item Name']} (x{line['Quantity']}) @ RM{line['Unit Price']:.2f}")