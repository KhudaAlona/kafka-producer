from kafka import KafkaConsumer
import csv
import os
from minio import Minio
from minio.error import S3Error
import shutil

# Ініціалізація клієнта MinIO
client = Minio(
    "minio:9000",
    access_key="admin",
    secret_key="adminadmin!!",
    secure=False
)

bucket_name = "default"


found = client.bucket_exists(bucket_name)
if not found:
    client.make_bucket(bucket_name)
    print(f"Bucket '{bucket_name}' created.")
else:
    print(f"Bucket '{bucket_name}' already exists.")

# Підключення до Kafka
consumer = KafkaConsumer(
    'Topic1',
    bootstrap_servers='kafka1:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
)

# Функція для завантаження CSV файлу в MinIO
def upload_to_minio(file_path):
    try:
        with open(file_path, 'rb') as file_data:
            file_name = os.path.basename(file_path)
            client.put_object(bucket_name, file_name, file_data, os.stat(file_path).st_size)
            print(f"File '{file_name}' uploaded successfully.")
            os.remove(file_path)
            print(f"File '{file_name}' deleted from consumer.")
    except S3Error as e:
        print(f"Error occurred: {e}")

month_year = "april_2020"
csv_filename = f"{month_year}.csv"
header = ['id', 'name', 'age'] 
with open(csv_filename, mode='w', newline='') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=header)
    writer.writeheader()

    # Читання та записування повідомлень
    for msg in consumer:
        message = msg.value.decode('utf-8')
        row = eval(message) 
        writer.writerow(row)

        print(f"Message written to {csv_filename}: {row}")

        if month_year != "april_2020":  
            previous_file = f"{month_year}.csv"
            upload_to_minio(previous_file)
