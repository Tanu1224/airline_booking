from flask import Flask, render_template, request, redirect, url_for
from flight import Flight, FlightManager, Booking, BookingManager
from datetime import datetime
from flask import flash

# ... (app setup and flight_manager initialization remain the same)
app = Flask(__name__)
app.secret_key = 'some_secret_key'
flight_manager = FlightManager()
booking_manager = BookingManager()

@app.route('/')
def index():
    # If the index is also a search page, you might want to show all flights initially
    # or redirect to the dashboard. For this example, let's redirect to dashboard.
    return redirect(url_for('dashboard')) 


@app.route('/dashboard')
def dashboard():
    # Get search parameters from the URL (e.g., /dashboard?source=London)
    source = request.args.get('source')
    destination = request.args.get('destination')
    date_str = request.args.get('date')
    sort_by = request.args.get('sort_by')

    # You would create a search_flights method in your FlightManager
    # For now, let's assume it exists and works like this:
    filtered_flights = flight_manager.search_flights(
        source=source, 
        destination=destination, 
        date_str=date_str, 
        sort_by=sort_by
    )
    
    # Pass the filtered list of flights to the template
    return render_template('dashboard.html', flights=filtered_flights)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        try:
            flight_id = request.form['flight_id']
            source = request.form['source']
            destination = request.form['destination']
            date_str = request.form['date']
            time_str = request.form['time']
            flight_datetime = datetime.strptime(f"{date_str} {time_str}", '%Y-%m-%d %H:%M')
            
            seats = int(request.form['seats'])
            price = float(request.form['price'])

            new_flight = Flight(flight_id, source, destination, flight_datetime, seats, price)
            flight_manager.add_flight(new_flight)
            
        except (ValueError, KeyError) as e:
            print(f"Error adding flight: {e}")

        return redirect(url_for('admin'))

    all_flights = flight_manager.get_all_flights()
    return render_template('admin.html', flights=all_flights)


@app.route('/delete_flight/<flight_id>')
def delete_flight(flight_id):
    flight_manager.delete_flight(flight_id)
    return redirect(url_for('admin'))


@app.route('/book_flight/<flight_id>')
def book_flight(flight_id):
    flight = flight_manager.get_flight_by_id(flight_id)
    if flight:
        # For now, we'll use a hardcoded user_id.
        # Later, this would come from a logged-in user's session.
        user_id = 'default_user' 
        
        booking = booking_manager.add_booking(user_id, flight)
        if booking:
            # Flash a success message
            flash(f"Successfully booked Flight {flight.flight_id} from {flight.source} to {flight.destination}!", 'success')
        else:
            flash(f"Sorry, Flight {flight.flight_id} is full.", 'error')
    else:
        flash("Flight not found.", 'error')
    
    return redirect(url_for('dashboard'))

@app.route('/my_bookings')
def my_bookings():
    user_id = 'default_user' # Hardcoded for now
    user_bookings = booking_manager.get_user_bookings(user_id)
    return render_template('booking.html', bookings=user_bookings)



if __name__ == '__main__':
    app.run(debug=True)