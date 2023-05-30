from hospital_api_client import HospitalAPIClient
import unittest
import unittest.mock as mock



def test_connect():
    client = HospitalAPIClient()
    client.connect()
    assert client.session is not None


@mock.patch('requests.get')
def test_get_patient_ids(mock_get):
    mock_response = mock.Mock()
    mock_response.json.return_value = ['patient_1', 'patient_2']
    mock_get.return_value = mock_response

    client = HospitalAPIClient()
    patient_ids = client.get_patient_ids()

    assert patient_ids == ['patient_1', 'patient_2']


@mock.patch('requests.get')
def test_read(mock_get):
    mock_response = mock.Mock()
    mock_response.json.return_value = {
        "body_temperature": 37
    }
    mock_get.return_value = mock_response

    client = HospitalAPIClient()
    data = client.read('patient_1')

    assert data['body_temperature'] == 37


def test_read_all_skips_invalid():
    client = HospitalAPIClient()
    client.connect()

    def get_patient_ids():
        return ['patient_1', 'patient_2']

    client.get_patient_ids = get_patient_ids

    def read(patient_id):
        if patient_id == 'patient_1':
            return {"body_temperature": 37}
        elif patient_id == 'patient_2':
            return {"body_temperature": 36}
        if patient_id == 'invalid':
            return 'invalid'

    client.read = read

    patients = [data for data in client.read_all()]

    # assert len(patients) == 1
    assert patients[0] == {'body_temperature': 37}


def test_read_all():
    client = HospitalAPIClient()
    client.connect()

    patient_data = {
        "patient_id": "drfXA8g1cyIJv69kiWYS",
        "vital_signs": "body_temperature -> 37.07 ; blood_pressure_systolic -> 123.96 ; blood_pressure_diastolic -> 82.21 ; heart_rate -> 69.86 ; respiratory_rate -> 14.77 ; timestamp -> 1632401883.512034"
    }

    def read():
        return patient_data

    client.read = read
    result = client.read_all()

    expected = "{\n\"drfXA8g1cyIJv69kiWYS\": {\n\"body_temperature\": 37.07,\n\"blood_pressure_systolic\": 123.96,\n\"blood_pressure_diastolic\": 82.21,\n\"heart_rate\": 69.86,\n\"respiratory_rate\": 14.77,\n\"timestamp\": 1632401883.512034\n}\n}"

    print("result:", result, "\n expected", expected)


def test_parse_vital_signs():
    client = HospitalAPIClient()
    client.connect()
    text = "body_temperature -> 37.07 ; blood_pressure_systolic -> 123.96 ; blood_pressure_diastolic -> 82.21 ; heart_rate -> 69.86 ; respiratory_rate -> 14.77 ; timestamp -> 1632401883.512034"

    vital_signs = client.parse_vital_signs(text)

    assert vital_signs['body_temperature'] == 37.07
    assert vital_signs['blood_pressure_systolic'] == 123.96
    assert vital_signs['heart_rate'] == 69.86

def test_invalid_data():
    client = HospitalAPIClient()
    client.connect()
    text = "invalid -> data"

    vital_signs = client.parse_vital_signs(text)
    assert vital_signs == {}
