FROM python:3.10-slim

WORKDIR /app

COPY demo.py .

EXPOSE 8080

CMD ["python3", "demo.py"]