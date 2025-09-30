from flask import Flask, render_template, request, redirect, url_for
from flight import Flight, FlightManager
from datetime import datetime

# ... (app setup and flight_manager initialization remain the same)
app = Flask(__name__)
flight_manager = FlightManager()


@app.route('/')
def index():
    # If the index is also a search page, you might want to show all flights initially
    # or redirect to the dashboard. For this example, let's redirect to dashboard.
    return redirect(url_for('dashboard')) 


@app.route('/dashboard')
def dashboard():
    # Show all available flights initially.
    all_flights = flight_manager.get_all_flights()
    
    # We pass the list of Flight objects to the template.
    return render_template('dashboard.html', flights=all_flights)

if __name__ == '__main__':
    app.run(debug=True)