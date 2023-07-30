FROM python:3.10

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

COPY ./src .

CMD gunicorn main:app -w ${UVICORN_WORKERS} --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8001
