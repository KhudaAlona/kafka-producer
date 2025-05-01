import os
import csv
import time
from minio import Minio
from minio.error import S3Error

minio_client = Minio(
    "localhost:9000",  
    access_key="admin",  
    secret_key="adminadmin!!",  
    secure=False  
)

bucket_name = "default"

def ensure_bucket_exists():
    try:
        if not minio_client.bucket_exists(bucket_name):
            minio_client.make_bucket(bucket_name)
            print(f"Bucket '{bucket_name}' created.")
        else:
            print(f"Bucket '{bucket_name}' already exists.")
    except S3Error as e:
        print(f"Error occurred while checking/creating bucket: {e}")

def upload_to_minio(file_path):
    try:
        with open(file_path, 'rb') as file_data:
            file_name = os.path.basename(file_path)
            print(f"Uploading {file_name} to MinIO...")
            minio_client.put_object(bucket_name, file_name, file_data, os.stat(file_path).st_size)
            print(f"File '{file_name}' uploaded successfully.")
            os.remove(file_path)  
            print(f"File '{file_name}' deleted from local storage.")
    except S3Error as e:
        print(f"Error occurred while uploading file to MinIO: {e}")

def process_and_upload_files():
    ensure_bucket_exists()  
    
    file_name = "april_2020.csv"
    
    if os.path.exists(file_name):
        print(f"Processing file: {file_name}")
        upload_to_minio(file_name)
    else:
        print(f"File {file_name} does not exist in the local directory.")
        
if __name__ == "__main__":
    process_and_upload_files()
