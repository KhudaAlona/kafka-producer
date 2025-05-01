# producer/Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY producer.py .
COPY data.csv ./data.csv
RUN pip install kafka-python
CMD ["python", "producer.py"]
