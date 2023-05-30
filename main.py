import ssl
from time import sleep

import psycopg2
import os
import csv
import numpy as np
from django.core.mail import send_mail

from hospital_api_client import HospitalAPIClient
from model import ICUZen


class DBHandler:
    """Handles database connections and queries"""
    def connect(self):
        conn = psycopg2.connect(host="localhost",
                                database="db",
                                user="user",
                                password="password",
                                sslmode="require")


    def create_patient_table(self):
        conn = self.connect()
        cur = conn.cursor()

        cur.execute("""
                CREATE TABLE patients (
                    patient_id VARCHAR(20) PRIMARY KEY,
                    body_temperature FLOAT,
                    blood_pressure_systolic INT,
                    blood_pressure_diastolic INT,
                    heart_rate INT,  
                    respiratory_rate INT, 
                    timestamp TIMESTAMP  
                );
                """)

        conn.commit()
        conn.close()

    def connect(self):
        client = HospitalAPIClient()
        client.connect()

    def save_data(self, data):
        conn = self.connect()
        cur = conn.cursor()

        # Insert data into DB
        cur.execute("INSERT INTO patients VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    data)

        conn.commit()
        conn.close()

        def save_vital_signs(raw_data):
            for patient_id, vital_signs in raw_data.items():
                if vital_signs:
                    # Extract values
                    temperature = vital_signs['body_temperature']
                    blood_pressure_systolic = vital_signs['blood_pressure_systolic']
                    blood_pressure_diastolic = vital_signs['blood_pressure_diastolic']
                    heart_rate = vital_signs['heart_rate']
                    respiratory_rate = vital_signs['respiratory_rate']
                    timestamp = vital_signs['timestamp']

                    # Print sample data for debugging
                    print(temperature, heart_rate)

                    # Save data to database
                    self.save_data((
                        patient_id,
                        temperature,
                        blood_pressure_systolic,
                        blood_pressure_diastolic,
                        heart_rate,
                        respiratory_rate,
                        timestamp
                    ))

class CSVHandler:
    def initialize_raw_data_csv_file(self):
        # Encrypted CSV file
        filepath = "secured/raw_data.csv.enc"

        # Create encrypted file
        os.system(f"openssl aes-256-cbc -e -in raw_data.csv -out {filepath}"
              "-k secret")

        with open(filepath, mode='w', newline='') as file:
            writer = csv.writer(file)
            # Write header row
            writer.writerow(
                ['patient_id', 'body_temperature', 'blood_pressure_systolic', 'blood_pressure_diastolic', 'heart_rate',
                'respiratory_rate', 'timestamp'])

    def initialize_predictions_csv_file(self):
        with open('secured/predictions.csv.enc', mode='w', newline='') as file:
            writer = csv.writer(file)
            # Write the header row
            writer.writerow(
                ['patient_id', 'body_temperature', 'blood_pressure_systolic', 'blood_pressure_diastolic', 'heart_rate',
                 'respiratory_rate'])

    def save_raw_data_to_csv(self, data):
        with open('secured/raw_data.csv.enc', mode='a', newline='') as file:
            writer = csv.writer(file)
            # Write the data rows
            for patient_id, vital_signs in data.items():
                writer.writerow([patient_id, vital_signs['body_temperature'], vital_signs['blood_pressure_systolic'],
                                 vital_signs['blood_pressure_diastolic'], vital_signs['heart_rate'],
                                 vital_signs['respiratory_rate'], vital_signs['timestamp']])

    # Save raw prediction
    def save_prediction(self, patient_id, should_alarm):
        with open('secured/predictions.csv.enc', 'a') as f:
            writer = csv.writer(f)
            writer.writerow([patient_id, should_alarm[0], should_alarm[1], should_alarm[2], should_alarm[3], should_alarm[4]])


class Dashboard:

    def __init__(self):
        self.data = {}

    def update_data(self, new_data):
        """Update the data from the vital signs API"""
        self.data.update(new_data)

    def check_alarms(self):
        """Check for patients that need alarms"""
        for patient_id, vital_signs in self.data.items():
            if vital_signs:
                data = np.array(list(vital_signs.values()))
                input_data = data[:-1].reshape(-1, 1).astype(float)
                should_alarm = self.model.predict(input_data)

                if should_alarm[0] == 1:
                    # Alarm detected
                    self.notify_clinicians(patient_id)
                    return patient_id
        return None
    def start(self, api):
        """Start monitoring loop"""
        while True:
            # Get new data
            if api:
                new_data = api.read_all()

            # Update data
            #self.update_data(new_data)

            # Check for alarms
            self.check_alarms()

            sleep(5)  # Wait 5 seconds
def main():
    # Connect to hospital API
    client = HospitalAPIClient()
    api = client.connect()

    db = DBHandler()
    csv = CSVHandler()
    dashboard = Dashboard()

    csv.initialize_raw_data_csv_file()
    csv.initialize_predictions_csv_file()

    # Create alarm model
    model = ICUZen()

    #dashboard.start(api)

    # Save raw data
    csv.save_raw_data_to_csv(client.convert_patient_list_to_dict(client.read_history()))
    while True:
        raw_data = client.read_all()
        csv.save_raw_data_to_csv(raw_data)
        #save_vital_signs(raw_data)

        # Predict alarm
        #dashboard.check_alarms()
        for patient_id, vital_signs in raw_data.items():
            # Only use non-empty data
            if vital_signs:
                print(vital_signs)
                data = np.array(list(vital_signs.values()))
                input_data = data[:-1].reshape(-1, 1).astype(float)
                should_alarm = model.predict(input_data)
                print(should_alarm, should_alarm.shape)

                # Save predictions
                csv.save_prediction(patient_id, should_alarm)




if __name__ == "__main__":
    main()
