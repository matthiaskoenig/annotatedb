FROM python:3.7
ENV PYTHONUNBUFFERED 1

# Allows docker to cache installed dependencies between builds
RUN pip install pip setuptools --upgrade
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Adds application code to the image
COPY . /code
WORKDIR /code

# install pkdb_app
RUN pip install -e .

EXPOSE 9000
CMD newrelic-admin run-program gunicorn --bind 0.0.0.0:$PORT --access-logfile - adb_app.wsgi:application