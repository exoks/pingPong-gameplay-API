FROM python:3.12.2-slim-bullseye

COPY    ./tools/ tools/

RUN     python -m venv venv \
        && . /venv/bin/activate \
        && pip install --no-//add  
cache-dir --upgrade pip \
        && pip install --no-cache-dir -r /tools/requirements.txt \
        && chmod +x /tools/entrypoint.sh

ENV     PATH="/venv/bin:$PATH"
COPY    ./app/ app/
WORKDIR /app

EXPOSE 6060

ENTRYPOINT ["/tools/entrypoint.sh"]
CMD ["gunicorn", "service_core.wsgi:application", "-c" , "gunicorn.conf.py"]
