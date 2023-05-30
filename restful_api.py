import numpy as np
import csv
from flask import Flask, request, jsonify
from hospital_api_client import HospitalAPIClient
from model import ICUZen

app = Flask(__name__)


@app.route('/v1/predictions', methods=['POST'])
def predict_alarm():
    data = request.get_json()
    vitals = np.array(data['vitals'])

    alarm = ICUZen.predict(vitals)

    return jsonify(alarm=alarm[0])


def get_patients():
    # Read patients from file
    patients = []

    with open('secured/raw_data.csv.enc') as f:
        reader = csv.reader(f)

        # Skip header row
        next(reader)

        for row in reader:
            patient_id = row[0]
            patients.append(patient_id)

    return jsonify(patients)


@app.route('/v1/patients/<patient_id>')
def get_patient(patient_id):
    # Read patient data from file
    data = []

    with open('predictions.csv.enc') as f:
        reader = csv.reader(f)

        # Loop through each row
        for row in reader:

            # Check if patient ID matches
            if row[0] == patient_id:
                data.append(row)

                # Keep only the last result
                if len(data) > 1:
                    data = data[-1:]

    return jsonify(data[0])


if __name__ == '__main__':
    app.run(debug=True)