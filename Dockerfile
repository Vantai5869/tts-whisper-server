FROM python:3.9-slim

RUN apt-get update && apt-get install -y ffmpeg

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

# Chạy main.py, để nó tự xử lý $PORT
CMD ["python", "main.py"]