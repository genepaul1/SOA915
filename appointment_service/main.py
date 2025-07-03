from flask import Flask, request, jsonify
from prometheus_client import Counter, generate_latest

app = Flask(__name__)
appointments = []

APPOINTMENT_COUNTER = Counter('appointments_total', 'Total appointments booked')

@app.route('/')
def index():
    return {"message": "Appointment Service is running"}

@app.route('/book', methods=['POST'])
def book():
    data = request.get_json()
    name = data.get('name')
    if not name:
        return {"error": "Name is required"}, 400
    appointments.append({"name": name})
    APPOINTMENT_COUNTER.inc()
    return {"message": f"Appointment booked for {name}"}

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': 'text/plain'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)
