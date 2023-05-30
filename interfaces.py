from hospital_api_client import HospitalAPIClient
from typing import Protocol
class Alarm:
    def __init__(self, timestamp, patient_id, vital_sign, value, is_alarm):
        self.timestamp = timestamp
        self.patient_id = patient_id
        self.vital_sign = vital_sign
        self.value = value
        self.is_alarm = is_alarm

class ICUDataSource:

    def get_alarms(self, start_time, end_time):
        """defines a clear data contract for an alarm event, with all required fields."""
        pass



    def get_patient_data(self, patient_id):
        """abstracts away the specific ICU API, allowing different implementations."""
        client = HospitalAPIClient()
        client.connect()
        data = client.read(patient_id)
        return data


class ICUDataSource(Protocol):

    def get_alarms(self, start_time, end_time): ...

    def get_patient_data(patient_id): ...