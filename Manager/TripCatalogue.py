import json
from Entity.Trip import Trip
from datetime import datetime


class TripCatalogue:
    def __init__(self):
        self.trips = []

    def load_trips_from_json(self, filename="Trip.json"):
        try:
            with open(filename, 'r') as file:
                trip_data = json.load(file)
                for data in trip_data:
                    # Example for TripCatalogue
                    trip = Trip(
                        item_id=data['item_id'],
                        name=data['name'],
                        price=data['price'],
                        description=data['description'],
                        availability=data['availability'],
                        capacity=data['capacity'],
                        route_code=data['route_code'],
                        departure_station=data['departure_station'],
                        arrival_station=data['arrival_station'],
                        departure_time=data['departure_time'],
                        arrival_time=data['arrival_time'],
                        feeder_bus=data['feeder_bus'],
                        rating=data.get('rating', 0.0)
                    )
                    self.trips.append(trip)
        except FileNotFoundError:
            print("Trip.json file not found.")
        except Exception as e:
            print(f"Error loading trips: {e}")

    def browse_trips(self):
        return [trip.view_trip_details() for trip in self.trips]

    def browse_by_location(self, departure, arrival):
        return [
            trip
            for trip in self.trips
            if trip.departure_station.lower() == departure.lower()
            and trip.arrival_station.lower() == arrival.lower()
        ]


    def add_trip(self, trip):
        self.trips.append(trip)

    def remove_trip(self, trip_id):
        self.trips = [trip for trip in self.trips if trip.trip_id != trip_id]

    def update_trip(self, trip_id, **kwargs):
        for trip in self.trips:
            if trip.trip_id == trip_id:
                trip.update_trip_info(**kwargs)
                return True
        return False

    def select_trip(self, trip_id):
        for trip in self.trips:
            if trip.trip_id == trip_id:
                return trip.view_trip_details()
        return None

    def update_trip_availability(self, item_id, new_availability):
        import json

        try:
            with open("Trip.json", "r") as file:
                trips = json.load(file)

            # Update the availability of the specific trip
            for trip in trips:
                if trip.get("item_id") == item_id:
                    trip["availability"] = new_availability
                    break

            with open("Trip.json", "w") as file:
                json.dump(trips, file, indent=4)

        except FileNotFoundError:
            print("Trip.json file not found.")
        except Exception as e:
            print(f"Error updating availability: {e}")
