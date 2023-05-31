from kafka import KafkaConsumer
import json

consumer = KafkaConsumer('alarms',
                         bootstrap_servers=['localhost:9092'],
                         auto_offset_reset='earliest')


def process_alarm(patient_id, alarm):
    # Process alarm for patient here...
    print(f"Alarm for patient {patient_id}: {alarm}")


def consume():
    for message in consumer:
        data = json.loads(message.value.decode('utf-8'))
        patient_id = data['patient_id']
        alarm = data['alarm']

        process_alarm(patient_id, alarm)


if __name__ == '__main__':
    consume()