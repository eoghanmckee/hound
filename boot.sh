#!/bin/sh
# this script is used to boot a Docker container

POSTGRES_USER=$(cat /home/hound/config/config.json | python -c 'import sys, json; print(json.load(sys.stdin)["POSTGRES_USER"])')
POSTGRES_PASSWORD=$(cat /home/hound/config/config.json | python -c 'import sys, json; print(json.load(sys.stdin)["POSTGRES_PASSWORD"])')
POSTGRES_HOST=$(cat /home/hound/config/config.json | python -c 'import sys, json; print(json.load(sys.stdin)["POSTGRES_HOST"])')
POSTGRES_DB=$(cat /home/hound/config/config.json | python -c 'import sys, json; print(json.load(sys.stdin)["POSTGRES_DB"])')
until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$POSTGRES_HOST" -d "$POSTGRES_DB" -U "$POSTGRES_USER" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping..."
  sleep 3
done

>&2 echo "Postgres is up - Starting."
sleep 3

while true; do
	flask db upgrade
    if [[ "$?" == "0" ]]; then
        break
    fi
    echo Deploy command failed, retrying in 5 secs...
    sleep 5
done
exec gunicorn -b :5000 --access-logfile - --error-logfile - hound:app

# start cron
/usr/sbin/crond -f -l 8