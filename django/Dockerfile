FROM tiangolo/uwsgi-nginx:python3.6-alpine3.7

ENV LISTEN_PORT=8000
EXPOSE 8000

# Indicate where uwsgi.ini lives
ENV UWSGI_INI uwsgi.ini

# Tell nginx where static files live (as typically collected using Django's
# collectstatic command.
ENV STATIC_URL /app/static_collected

# Copy the app files to a folder and run it from there
WORKDIR /app
ADD . /app

# Make app folder writable for the sake of db.sqlite3, and make that file also writable.
RUN chmod g+w /app

# Make sure dependencies are installed
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
RUN python3 -m pip install psycopg2
RUN python3 -m pip install -r requirements.txt
