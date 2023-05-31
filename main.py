from time import sleep

import psycopg2
import os
import csv
import numpy as np

from hospital.api_client.hospital_api_client import HospitalAPIClient
from model.model import ICUZen


class DBHandler:
    """Handles database connections and queries
    Note: This class is currently not linked to any database, but is already implemented."""

    def connect(self):
        """Connects to a PostgreSQL database
        Returns a database connection object"""

        conn = psycopg2.connect(host="localhost",
                                database="db",
                                user="user",
                                password="password",
                                sslmode="require")

        return conn

    def create_patient_table(self):
        """Creates a 'patients' table in the database with the required columns"""

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
        """Initializes a connection to the Hospital API
        Returns a client object for making API requests"""

        client = HospitalAPIClient()
        client.connect()

    def save_data(self, data):
        """Saves patient vital sign data to the 'patients' table in the database"""

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
        """Initializes the raw data CSV file with a header row
        The file is located in the 'hospital/data' directory"""

        filepath = "hospital/data/raw_data.csv"

        with open(filepath, mode='w', newline='') as file:
            writer = csv.writer(file)
            # Write header row
            writer.writerow(
                ['patient_id', 'body_temperature', 'blood_pressure_systolic', 'blood_pressure_diastolic', 'heart_rate',
                'respiratory_rate', 'timestamp'])




    def initialize_predictions_csv_file(self):
        """Initializes the predictions CSV file with a header row
            The file is located in the 'hospital/data' directory"""

        with open('hospital/data/predictions.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            # Write the header row
            writer.writerow(
                ['patient_id', 'body_temperature', 'blood_pressure_systolic', 'blood_pressure_diastolic', 'heart_rate',
                 'respiratory_rate'])




    def save_raw_data_to_csv(self, data):
        """Saves a dictionary of patient vital sign data to a CSV file
            The data is encrypted, and the file is located in the 'hospital/data' directory

            Args:
                data (dict): A dictionary of patient vital sign data, where the keys are patient IDs and the values are dictionaries
                            containing the vital sign measurements and timestamps"""

        with open('hospital/data/raw_data.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            # Write the data rows
            for patient_id, vital_signs in data.items():
                writer.writerow([patient_id, vital_signs['body_temperature'], vital_signs['blood_pressure_systolic'],
                                 vital_signs['blood_pressure_diastolic'], vital_signs['heart_rate'],
                                 vital_signs['respiratory_rate'], vital_signs['timestamp']])

    def save_prediction(self, patient_id, should_alarm):
        """Saves the prediction results for the given patient to a CSV file
            The predictions are encrypted, and the file is located in the 'hospital/data' directory
            The function appends a new row to the end of the file, with the patient ID and the five prediction values

            Args:
               patient_id (str): The ID of the patient for whom the prediction was made
               should_alarm (list): A list of five Boolean values indicating whether an alarm should be raised for each observation"""

        with open('hospital/data/predictions.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow([patient_id, should_alarm[0], should_alarm[1], should_alarm[2], should_alarm[3], should_alarm[4]])


class Dashboard:
    """Handles the dashboard functionality for the ICUZen application"""

    def __init__(self):
        # Initializes the dashboard object
        self.data = {}

        # Creates backup CSV files
        self.csv_raw_data = CSVHandler()
        self.csv_prediction = CSVHandler()

        # Connects to hospital API
        self.client = HospitalAPIClient()

        # Creates an instance of the alarm model
        self.model = ICUZen()


    def initialize(self):
        # Initializes the backup CSV files and connects to the hospital API
        self.csv_raw_data.initialize_raw_data_csv_file()
        self.csv_prediction.initialize_predictions_csv_file()

        # Connects to the hospital API
        client = HospitalAPIClient()
        client.connect()


    def check_alarm(self, patient_id, should_alarm):
        """Checks if the given patient needs assistance based on the model's prediction"""
        if should_alarm[0] == 1:
            self.notify_clinicians(patient_id)
        return None


    def notify_clinicians(self, patient_id):
        """Notifies clinicians that the given patient needs assistance
        Note: Could be implemented in a messaging system"""

        print(f"{patient_id} needs assistance")


    def run(self):
        """Runs the dashboard loop, reading data from the Hospital API and making predictions"""

        while True:
            raw_data = self.client.read_all()
            self.csv_raw_data.save_raw_data_to_csv(raw_data)

            for patient_id, vital_signs in raw_data.items():
                if vital_signs:
                    data = np.array(list(vital_signs.values()))
                    input_data = data[:-1].reshape(-1, 1).astype(float)
                    should_alarm = self.model.predict(input_data)
                    self.check_alarm(patient_id, should_alarm)

                    # Save predictions
                    self.csv_prediction.save_prediction(patient_id, should_alarm)
            sleep(1)
def main():
    dashboard = Dashboard()
    dashboard.initialize()
    dashboard.run()


if __name__ == "__main__":
    main()
