FROM python:3.9-alpine

# Cài FFmpeg và phụ thuộc cần thiết
RUN apk add --no-cache ffmpeg

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "$PORT"]