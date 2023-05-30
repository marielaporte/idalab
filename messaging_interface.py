import csv
import json
import numpy as np

from kafka import KafkaProducer
from nltk import app
from flask import Flask, request, jsonify

from model import ICUZen

producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

@app.route('/v1/predictions', methods=['POST'])
def predict_alarm():
    data = request.get_json()
    patient_id = np.array(data['patient_id'])
    vitals = np.array(data['vitals'])

    alarm = ICUZen.predict(vitals)

    # Publish alarm to Kafka
    producer.send('alarms', json.dumps({
        'patient_id': patient_id,
        'alarm': alarm[0]
    }).encode('utf-8'))

    return 'Alarm published!'


@app.route('/v1/patients')
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

    # Publish patients to Kafka
    for patient in patients:
        producer.send('patients', json.dumps({
            'patient_id': patient
        }).encode('utf-8'))

    return 'Patients published!'


if __name__ == '__main__':
    # Start API
    app.run(debug=True)

    # Consume messages from MQTT queue
    consume()

# consume.py

import paho.mqtt.client as mqtt


def on_message(client, userdata, msg):
    data = json.loads(msg.payload)
    patient_id = data['patient_id']
    alarm = data['alarm']

    # Process alarm here
    process_alarm(patient_id, alarm)


def consume():
    client = mqtt.Client()
    client.on_message = on_message
    client.connect('localhost')
    client.subscribe('alarms')
    client.loop_forever()