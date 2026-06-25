FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY 4d-crypto-demo.py .
CMD ["python", "4d-crypto-demo.py"]
