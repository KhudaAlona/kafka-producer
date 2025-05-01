FROM python:3.9-slim
WORKDIR /app
COPY consumer1.py .
RUN pip install kafka-python minio
CMD ["python", "consumer1.py"]
