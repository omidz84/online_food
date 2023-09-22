#!/bin/bash 

cd /app

python3 manage.py collectstatic --noinput && \
python3 manage.py migrate && \
python3 manage.py checksysteminit && \
python3 manage.py compilemessages && \
gunicorn -w $GUNICORN_WORKER_NO --bind :$GUNICORN_LISTENINIG_PORT --timeout $GUNICORN_TIMEOUT kh8-api.wsgi
python3 manage.py runserver 0.0.0.0:$GUNICORN_LISTENINIG_PORT
