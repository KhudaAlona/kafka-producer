# consumer1/consumer1.py
from kafka import KafkaConsumer

consumer = KafkaConsumer('Topic1', bootstrap_servers='kafka1:9092')

for msg in consumer:
    print(f"Consumer 1 received: {msg.value.decode('utf-8')}")
