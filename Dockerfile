FROM python:3.9-slim

copy requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

WORKDIR /app
COPY bot /app/bot
COPY main.py /app/main.py

CMD ["python", "main.py"]
