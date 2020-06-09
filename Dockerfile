FROM python:3.6-alpine

RUN adduser -D hound

WORKDIR /home/hound

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn pymysql

RUN apk update && \
    apk add --virtual build-deps gcc musl-dev && \
    apk add postgresql-dev

RUN apk add --update
RUN apk --update add postgresql-client
RUN pip install psycopg2

COPY app app
COPY config config
COPY migrations migrations
COPY integrations integrations
COPY *.py ./
COPY *.sh ./
RUN mkdir -p db
RUN chmod a+x boot.sh

ENV FLASK_APP hound.py

RUN chown -R hound:hound ./
USER hound

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
