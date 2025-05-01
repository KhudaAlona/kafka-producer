from kafka import KafkaConsumer

consumer = KafkaConsumer('Topic2', bootstrap_servers='kafka1:9092')

for msg in consumer:
    print(f"Consumer 2 received: {msg.value.decode('utf-8')}")
