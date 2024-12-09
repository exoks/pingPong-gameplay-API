#!/bin/sh

set -e

sleep 4
echo "===============================>>> Start Setup <<<==============================="
. /venv/bin/activate

python  /app/manage.py makemigrations
python  /app/manage.py migrate --noinput

echo "==============================>>> Start Server <<<==============================="
exec "$@"
