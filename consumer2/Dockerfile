FROM python:3.9-slim
WORKDIR /app
COPY consumer2.py .
RUN pip install kafka-python minio
CMD ["python", "consumer2.py"]
