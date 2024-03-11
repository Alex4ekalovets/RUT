FROM python:3.10

ENV PYTHONUNBUFFERED=1

RUN mkdir /app

WORKDIR /app

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

COPY requirements.txt ./

RUN pip install --no-cache-dir --upgrade pip \
  && pip install --no-cache-dir -r requirements.txt

COPY . .

CMD gunicorn app:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000