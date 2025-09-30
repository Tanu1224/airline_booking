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

    from datetime import datetime

# Inside your FlightManager class in flight.py
    def search_flights(self, source, destination, date_str, sort_by):
        # Start with a copy of all flights
        results = self.flights[:] 

        # --- Filtering ---
        # Filter by source (if provided)
        if source:
            results = [f for f in results if source.lower() in f.source.lower()]

        # Filter by destination (if provided)
        if destination:
            results = [f for f in results if destination.lower() in f.destination.lower()]

        # Filter by date (if provided)
        if date_str:
            try:
                search_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                results = [f for f in results if f.date.date() == search_date]
            except ValueError:
                # Silently ignore invalid date formats
                pass

        # --- Sorting ---
        if sort_by == "price":
            results.sort(key=lambda f: f.price)
        elif sort_by == "time":
            results.sort(key=lambda f: f.date.time())
        elif sort_by == "seats":
            results.sort(key=lambda f: f.available_seats, reverse=True)
                
        return results

    # Add methods for adding, updating, deleting flights if needed
    def add_flight(self, flight):
        self.flights.append(flight)
        # In a real app, this would save to the database
        
    def delete_flight(self, flight_id):
        flight_to_delete = None
        for flight in self.flights:
            if flight.flight_id == flight_id:
                flight_to_delete = flight
                break
        
        if flight_to_delete:
            self.flights.remove(flight_to_delete)

    # Inside your FlightManager class
    def get_flight_by_id(self, flight_id):
        for flight in self.flights:
            if str(flight.flight_id) == str(flight_id):
                return flight
        return None
    
    def book_seat(self):
        """Decrements the seat count if seats are available."""
        if self.available_seats > 0:
            self.available_seats -= 1
            return True
        return False
    
    
class Booking:
    """Represents a single booking made by a user for a flight."""
    def __init__(self, booking_id, user_id, flight):
        self.booking_id = booking_id
        self.user_id = user_id
        self.flight = flight

class BookingManager:
    """Manages all flight bookings."""
    def __init__(self):
        self.bookings = []
        self._next_booking_id = 1

    def add_booking(self, user_id, flight):
        """Creates and adds a new booking."""
        if flight.book_seat():
            booking = Booking(self._next_booking_id, user_id, flight)
            self.bookings.append(booking)
            self._next_booking_id += 1
            return booking
        return None # No seats were available

    def get_user_bookings(self, user_id):
        """Returns all bookings for a specific user."""
        return [b for b in self.bookings if b.user_id == user_id]