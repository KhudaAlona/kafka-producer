from minio import Minio
from minio.error import S3Error
import os
import csv
from datetime import datetime, timedelta
import random

MINIO_URL = "minio:9000"  
MINIO_ACCESS_KEY = "admin"
MINIO_SECRET_KEY = "adminadmin!!"
BUCKET_NAME = "default"  

client = Minio(
    MINIO_URL,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False
)

def upload_to_minio(file_path):
    try:
        file_name = os.path.basename(file_path)
        with open(file_path, 'rb') as file_data:
            if not client.bucket_exists(BUCKET_NAME):
                client.make_bucket(BUCKET_NAME)
                print(f"Bucket '{BUCKET_NAME}' created.")
            
            print(f"Uploading {file_name} to MinIO...")
            client.put_object(BUCKET_NAME, file_name, file_data, os.stat(file_path).st_size)
            print(f"File '{file_name}' uploaded successfully.")

            os.remove(file_path)
            print(f"File '{file_name}' deleted from local storage.")
    except S3Error as e:
        print(f"Error occurred while uploading file to MinIO: {e}")

def get_previous_month_filename(current_filename):
    base_name = current_filename.split("_")
    month = int(base_name[0])
    year = int(base_name[1].split(".")[0])

    prev_month_date = datetime(year, month, 1) - timedelta(days=1)
    prev_month_filename = f"{prev_month_date.strftime('%b').lower()}_{prev_month_date.year}.csv"
    return prev_month_filename

def generate_message_data(num_records):
    message_types = ['Info', 'Warning', 'Error']
    authors = ['Alice', 'Bob', 'Charlie', 'Dave']
    sources = ['System', 'User', 'Network', 'API']

    messages = []
    for i in range(num_records):
        message = {
            'id': i + 1,
            'message': f"This is a {random.choice(message_types)} message.",
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'consumer_id': random.randint(1, 10),
            'message_type': random.choice(message_types),
            'author': random.choice(authors),
            'subject': f"Subject {random.randint(1, 100)}",
            'source': random.choice(sources),
            'received_timestamp': (datetime.now() - timedelta(minutes=random.randint(1, 60))).strftime('%Y-%m-%d %H:%M:%S'),
            'processing_time': f"{random.randint(1, 10)}ms"
        }
        messages.append(message)
    
    return messages

def write_and_upload_csv(messages, csv_filename):
    print(f"Writing data to {csv_filename}")
    with open(csv_filename, mode='w', newline='') as csv_file:
        fieldnames = messages[0].keys()
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(messages)

    upload_to_minio(csv_filename)

    prev_month_filename = get_previous_month_filename(csv_filename)
    if os.path.exists(prev_month_filename):
        upload_to_minio(prev_month_filename)

messages = generate_message_data(50)

csv_filename = 'may_2020.csv' 
write_and_upload_csv(messages, csv_filename)
