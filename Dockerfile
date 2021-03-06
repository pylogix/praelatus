FROM python:3

WORKDIR /opt/praelatus
COPY requirements.txt requirements.txt

RUN pip install -r /opt/praelatus/requirements.txt

COPY . .

ENV PYTHONPATH /opt/praelatus

EXPOSE 8000


CMD ["gunicorn", "-k", "gevent", "--config", "/opt/praelatus/docker/gunicorn.conf", "praelatus.app"]
