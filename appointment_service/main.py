from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from prometheus_client import Counter, generate_latest
import requests
import sqlite3
import os

app = Flask(__name__)
CORS(app)
DB_FILE = "appointments.db"

USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "http://localhost:8000")
BILLING_SERVICE_URL = os.getenv("BILLING_SERVICE_URL", "http://billing-service:8002")
NOTIFICATION_SERVICE_URL = os.getenv("NOTIFICATION_SERVICE_URL", "http://notification-service:8003")

APPOINTMENT_COUNTER = Counter('appointments_total', 'Total appointments booked')

#for DB
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT,
            date TEXT,
            time TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return {"message": "Appointment Service is running"}

@app.route('/book', methods=['POST'])
def book():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    date = data.get('date')
    time = data.get('time')

    if not all([name, email, date, time]):
        return {"error": "All fields are required"}, 400

    # Save to DB
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO appointments (name, email, date, time) VALUES (?, ?, ?, ?)",
              (name, email, date, time))
    conn.commit()
    conn.close()


    APPOINTMENT_COUNTER.inc()

    # Call billing-service
    try:
        requests.get(f"{BILLING_SERVICE_URL}/")
    except Exception as e:
        print("Billing service failed: {e}")

    # Call notification-service
    try:
        requests.get(f"{NOTIFICATION_SERVICE_URL}/")
    except Exception as e:
        print("Notification service failed: {e}")

    return {"message": f"Appointment booked for {name}"}

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype='text/plain')

@app.route('/appointments', methods=['GET'])
def get_appointments():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, date, time FROM appointments")
    rows = cursor.fetchall()
    conn.close()
    return jsonify([{"id": r[0], "name": r[1], "email": r[2], "date": r[3], "time": r[4]} for r in rows])

@app.route('/delete/<int:appointment_id>', methods=['DELETE'])
def delete_appointment(appointment_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM appointments WHERE id = ?", (appointment_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": f"Appointment {appointment_id} deleted successfully"}), 200

@app.route('/update/<int:appointment_id>', methods=['PUT'])
def update_appointment(appointment_id):
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    date = data.get('date')
    time = data.get('time')

    if not all([name, email, date, time]):
        return {"error": "All fields are required"}, 400

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        UPDATE appointments 
        SET name = ?, email = ?, date = ?, time = ? 
        WHERE id = ?
    """, (name, email, date, time, appointment_id))
    conn.commit()
    conn.close()

    return {"message": f"Appointment ID {appointment_id} updated successfully"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)
