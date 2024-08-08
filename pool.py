#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# MySQL Database configuration
db_config = {
    'user': 'root',
    'password': 'Premya@1996',
    'host': 'localhost',
    'database': 'carpooling_db'
}

# Function to connect to the database
def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Offer a ride
@app.route('/offer_ride', methods=['GET', 'POST'])
def offer_ride():
    if request.method == 'POST':
        driver_name = request.form['driver_name']
        origin = request.form['origin']
        destination = request.form['destination']
        date = request.form['date']
        seats_available = request.form['seats_available']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO rides (driver_name, origin, destination, date, seats_available)
            VALUES (%s, %s, %s, %s, %s)
        """, (driver_name, origin, destination, date, seats_available))
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('index'))
    return render_template('offer_ride.html')

# Search for rides
@app.route('/search_rides', methods=['GET', 'POST'])
def search_rides():
    rides = []
    if request.method == 'POST':
        origin = request.form['origin']
        destination = request.form['destination']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT * FROM rides WHERE origin = %s AND destination = %s
        """, (origin, destination))
        rides = cursor.fetchall()
        cursor.close()
        conn.close()
        
    return render_template('search_rides.html', rides=rides)

if __name__ == '__main__':
    app.run(debug=True)

