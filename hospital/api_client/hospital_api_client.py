import requests


class HospitalAPIClient:
    """Handles the client functionality for communicating with the Hospital API"""

    BASE_URL = "https://idalab-icu.ew.r.appspot.com"

    def __init__(self):
        # Initializes the client object
        self.session = None

    def connect(self):
        # Initializes a session with the Hospital API
        self.session = requests.Session()

    def get_history_vital_signs(self):
        # Makes a GET request to retrieve the historical vital sign data from the Hospital API
        url = f"{self.BASE_URL}/history_vital_signs"
        response = requests.get(url)
        data = response.json()
        return data

    def get_patient_ids(self):
        # Makes a GET request to retrieve the list of patient IDs from the Hospital API
        response = requests.get(f"{self.BASE_URL}/patient_ids")
        patient_ids = response.json()
        return patient_ids

    def read_history(self):
        # Makes a GET request to retrieve the historical vital sign data from the Hospital API
        url = f"{self.BASE_URL}/history_vital_signs"
        response = requests.get(url)
        data = response.json()
        return data

    def convert_patient_list_to_dict(self, patient_list):
        # Converts a list of patients to a dictionary of vital sign data
        output = {}

        for patients in self.read_history().values():
            for patient in patients:
                patient_id = patient['patient_id']
                vital_signs = dict(tuple(vital.split(" -> ")) for vital in patient['vital_signs'].split("; "))
                output[patient_id] = vital_signs
        return output

    def read(self, patient_id):
        # Makes a GET request to retrieve the vital sign data for a specific patient from the Hospital API
        url = f"{self.BASE_URL}/patient_vital_signs/{patient_id}"
        response = requests.get(url)
        data = response.json()
        return data

    def read_all(self):
        # Reads vital sign data for all patients and returns it in a dictionary
        patient_ids = self.get_patient_ids()
        data = {}
        for patient_id in patient_ids['patient_id_list']:
            try:
                patient_data = self.read(patient_id)

            except Exception as e:
                # Log error
                patient_data = ""

            vital_signs = self.parse_vital_signs(patient_data)
            data[patient_id] = vital_signs
        return data

    def parse_vital_signs(self, data):
        # Parses the vital sign data from a JSON response and returns it as a dictionary
        vital_signs = {}
        for item in data['vital_signs'].split(";"):
            key, value = item.split("->")
            key = key.strip()
            value = value.strip()
            vital_signs[key] = value
        return vital_signs

