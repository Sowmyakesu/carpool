from flask import Flask, render_template, request, redirect, url_for

import mysql.connector

app = Flask(__name__)

# Database configuration
db_config = {
    'user': 'root',
    'password': 'Premya@1996',
    'host': 'localhost',
    'database': 'carpooling_db'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def index():
    return render_template('index.html')



@app.route('/offer_ride', methods=['GET', 'POST'])
def offer_ride():
    message = None
    if request.method == 'POST':
        driver_name = request.form['driver_name']
        origin = request.form['origin']
        destination = request.form['destination']
        date = request.form['date']
        seats_available = request.form['seats_available']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO rides (driver_name, origin, destination, date, seats_available) VALUES (%s, %s, %s, %s, %s)",
            (driver_name, origin, destination, date, seats_available)
        )
        conn.commit()
        cursor.close()
        conn.close()

        message = 'Ride offered successfully!'  # Set a success message

    return render_template('offer_ride.html', message=message)


@app.route('/search_rides', methods=['GET', 'POST'])
def search_rides():
    if request.method == 'POST':
        origin = request.form['origin']
        destination = request.form['destination']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT * FROM rides
            WHERE origin = %s AND destination = %s AND seats_available > 0
        """, (origin, destination))
        rides = cursor.fetchall()
        cursor.close()
        conn.close()

        return render_template('search_rides.html', rides=rides)

    return render_template('search_rides.html', rides=[])

@app.route('/book_ride/<int:ride_id>', methods=['POST'])
def book_ride(ride_id):
    user_name = request.form['user_name']
    seats_booked = int(request.form['seats_booked'])
    message = None

    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if enough seats are available
    cursor.execute("""
        SELECT seats_available FROM rides WHERE id = %s
    """, (ride_id,))
    result = cursor.fetchone()
    
    if result and result[0] >= seats_booked:
        # Insert booking record
        cursor.execute("""
            INSERT INTO bookings (ride_id, user_name, seats_booked)
            VALUES (%s, %s, %s)
        """, (ride_id, user_name, seats_booked))
        conn.commit()
        
        # Update seats available
        cursor.execute("""
            UPDATE rides SET seats_available = seats_available - %s WHERE id = %s
        """, (seats_booked, ride_id))
        conn.commit()
        
        message = 'Ride booked successfully!'  # Set a success message

    cursor.close()
    conn.close()
    
    return redirect(url_for('search_rides', message=message))

if __name__ == '__main__':
    app.run(debug=True)
