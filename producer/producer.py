# producer/producer.py
from kafka import KafkaProducer
import csv
import time

producer = KafkaProducer(bootstrap_servers='kafka1:9092')

with open('data.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        message = str(row).encode('utf-8')
        producer.send('Topic1', message)
        producer.send('Topic2', message)
        print(f"Sent: {row}")
        time.sleep(1)

producer.flush()
