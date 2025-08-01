from flask import Flask, request, jsonify

app = Flask(__name__)

# Sample in-memory data
patients = {
    1: {
        "name": "Juan Perez",
        "medical_history": [
            {"date": "2024-01-10", "notes": "Consulta general"}
        ],
        "authorized_family": [2]
    }
}

family_members = {
    2: {
        "name": "Maria Perez",
        "relation": "Madre",
        "authorized_patients": [1]
    }
}

doctors = {
    1: {
        "name": "Dr. Gomez",
        "patients": [1]
    }
}

appointments = []

@app.route("/patients/<int:patient_id>")
def get_patient(patient_id):
    patient = patients.get(patient_id)
    if not patient:
        return jsonify({"error": "Paciente no encontrado"}), 404
    return jsonify(patient)

@app.route("/doctors/<int:doctor_id>")
def get_doctor(doctor_id):
    doctor = doctors.get(doctor_id)
    if not doctor:
        return jsonify({"error": "Medico no encontrado"}), 404
    # Include patient details
    patient_details = {pid: patients.get(pid) for pid in doctor["patients"]}
    return jsonify({"doctor": doctor, "patients": patient_details})

@app.route("/appointments", methods=["GET", "POST"])
def manage_appointments():
    if request.method == "POST":
        data = request.json
        appointments.append(data)
        return jsonify({"message": "Reserva creada"}), 201
    return jsonify(appointments)

@app.route("/records/<int:patient_id>", methods=["GET", "POST"])
def patient_records(patient_id):
    patient = patients.get(patient_id)
    if not patient:
        return jsonify({"error": "Paciente no encontrado"}), 404
    if request.method == "POST":
        record = request.json
        patient["medical_history"].append(record)
        return jsonify({"message": "Registro agregado"}), 201
    return jsonify(patient["medical_history"])

if __name__ == "__main__":
    app.run(debug=True)
