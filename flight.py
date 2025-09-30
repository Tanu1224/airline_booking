from datetime import datetime

class Flight:
    def __init__(self, flight_id, source, destination, date, price=None, available_seats=None):
        self.flight_id = flight_id
        self.source = source
        self.destination = destination
        self.date = date # datetime object or string, depending on your preference
        self.price = price
        self.available_seats = available_seats

    def __repr__(self):
        return f"Flight({self.flight_id}: {self.source} to {self.destination} on {self.date})"

    # You might add methods here later, e.g., for booking a seat
    def book_seat(self, num_seats=1):
        if self.available_seats and self.available_seats >= num_seats:
            self.available_seats -= num_seats
            return True
        return False

class FlightManager:
    def __init__(self):
        # In a real application, this would interact with a database
        self.flights = self._load_initial_flights()

    def _load_initial_flights(self):
        # Placeholder for demonstration. In production, load from DB.
        return [
            Flight(1, "New York", "London", datetime(2023, 12, 20), 500, 150),
            Flight(2, "London", "Paris", datetime(2023, 12, 22), 120, 80),
            Flight(3, "New York", "Los Angeles", datetime(2023, 12, 25), 300, 200),
            Flight(4, "Paris", "Rome", datetime(2023, 12, 28), 90, 50),
            Flight(5, "New York", "London", datetime(2024, 1, 5), 550, 100),

        ]

    def get_all_flights(self):
        return self.flights

    def search_flights(self, source=None, destination=None, date=None, sort_by=None):
        results = self.flights

        if source:
            results = [f for f in results if f.source.lower() == source.lower()]
        if destination:
            results = [f for f in results if f.destination.lower() == destination.lower()]
        if date:
            # Assuming date is a datetime object or can be parsed
            search_date_str = date.strftime('%Y-%m-%d') if isinstance(date, datetime) else date
            results = [f for f in results if (f.date.strftime('%Y-%m-%d') == search_date_str)]

        if sort_by == 'price_asc':
            results.sort(key=lambda f: f.price if f.price else float('inf'))
        elif sort_by == 'price_desc':
            results.sort(key=lambda f: f.price if f.price else float('-inf'), reverse=True)
        elif sort_by == 'date_asc':
            results.sort(key=lambda f: f.date)
        elif sort_by == 'date_desc':
            results.sort(key=lambda f: f.date, reverse=True)

        return results

    # Add methods for adding, updating, deleting flights if needed
    def add_flight(self, flight):
        self.flights.append(flight)
        # In a real app, this would save to the database

    def get_flight_by_id(self, flight_id):
        return next((f for f in self.flights if f.flight_id == flight_id), None)