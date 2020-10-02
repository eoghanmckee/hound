FROM python:3.6-alpine

RUN adduser -D hound

WORKDIR /home/hound

COPY requirements.txt requirements.txt

RUN apk -U upgrade && \
    apk add --no-cache postgresql-libs postgresql-client && \
    apk add --virtual build-deps postgresql-dev gcc musl-dev tzdata && \
    pip install --upgrade --no-cache-dir pip && \
    pip install --no-cache-dir -r requirements.txt && \
    cp -f /usr/share/zoneinfo/UTC /etc/localtime && \
    echo 'UTC' >/etc/timezone && \
    apk --purge del build-deps

COPY --chown=hound:hound app app
COPY --chown=hound:hound config config
COPY --chown=hound:hound migrations migrations
COPY --chown=hound:hound integrations integrations
COPY --chown=hound:hound *.py *.sh ./

RUN mkdir -p db && \
    chmod a+x boot.sh && \
    chown -R hound:hound ./

ENV FLASK_APP hound.py

USER hound

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
