FROM python:3.9-slim

# Cài FFmpeg
RUN apt-get update && apt-get install -y ffmpeg

# Sao chép code
WORKDIR /app
COPY . /app

# Cài phụ thuộc Python
RUN pip install --no-cache-dir -r requirements.txt

# Chạy server
CMD ["python", "main.py"]