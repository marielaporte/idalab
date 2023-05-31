import csv
import json

from flask import Flask, request, jsonify
from kafka import KafkaProducer

from model.model import ICUZen

app = Flask(__name__)
producer = KafkaProducer(bootstrap_servers=['localhost:9092'])


@app.route('/v1/predictions', methods=['POST'])
def predict_alarm():
    patient_id = request.json['patient_id']
    alarm = ICUZen.predict(request.json['vitals'])

    # Publish alarm to Kafka
    producer.send('alarms', json.dumps({
        'patient_id': patient_id,
        'alarm': alarm
    }).encode('utf-8'))

    return 'Alarm published!'


@app.route('/v1/patients')
def get_patients():
    # Read patients from file
    patients = []

    with open('../hospital/data/raw_data.csv') as f:
        reader = csv.reader(f)

        # Skip header row
        next(reader)

        for row in reader:
            patient_id = row[0]
            patients.append(patient_id)

    return jsonify(patients)


if __name__ == '__main__':
    app.run(debug=True)