FROM python:3.13-slim

WORKDIR /app

COPY config.yaml .

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY cab.py .
COPY pro.py .
COPY utils.py .
COPY vehicle.py .

CMD ["python", "app.py"]

