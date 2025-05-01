# consumer1/Dockerfile (і такий самий для consumer2 з відповідним .py)
FROM python:3.9-slim
WORKDIR /app
COPY consumer1.py .
RUN pip install kafka-python
CMD ["python", "consumer1.py"]
