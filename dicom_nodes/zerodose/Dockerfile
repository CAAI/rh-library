#System
FROM python:3.10

#General requirements
COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /app
COPY server.py server.py

CMD ["python", "server.py"]
