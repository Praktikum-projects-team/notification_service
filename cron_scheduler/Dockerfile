FROM python:3.10

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

COPY . .

ENTRYPOINT wait-for-it -s "${POSTGRES_HOST}:${POSTGRES_PORT}" --timeout 60 \
            && wait-for-it -s "${RABBITMQ_HOST}:${RABBITMQ_PORT}" --timeout 60 \
            && python main.py
