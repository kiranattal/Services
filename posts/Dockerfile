# #Docker file is basically instruction to build an image, a blueprint that your container will run off of
# FROM python:3.8
# #RUN pip3 install pipenv
# ENV GOOGLE_APPLICATION_CREDENTIALS tactical-crow-340111-08a8dcc1139b.json
# WORKDIR /app
# # COPY Pipfile .
# # COPY Pipfile.lock .
# ADD . /app
# # RUN pipenv install --deploy --ignore-pipfile
# RUN pip install -r requirements.txt

# #CMD ["pipenv", "run", "python3", "app.py"]
# CMD ["uwsgi","app.ini"]

# Use the Python3.7.2 image
FROM python:3.7.2-stretch

# Set the working directory to /app
WORKDIR /posts

ENV GOOGLE_APPLICATION_CREDENTIALS tactical-crow-340111-08a8dcc1139b.json

# Copy the current directory contents into the container at /app 
ADD . /posts

# Install the dependencies
RUN pip install -r requirements.txt

# run the command to start uWSGI
CMD ["uwsgi", "app.ini"]


# FROM ubuntu:18.04
# RUN apt-get update -y && apt-get install software-properties-common -y  && apt-get upgrade -y && apt-get install curl -y
# RUN mkdir /home/flaskapp
# RUN apt install python3-pip -y
# ENV FLASK_APP app
# ENV LC_ALL C.UTF-8
# ENV LANG C.UTF-8
# ENV GOOGLE_APPLICATION_CREDENTIALS tactical-crow-340111-08a8dcc1139b.json

# WORKDIR /home/flaskapp
# COPY . /home/flaskapp
# RUN pip3 install -r requirements.txt
# CMD ["gunicorn","--bind","0.0.0.0:5000","wsgi:app"]

# FROM alpine:latest
# RUN apk update
# RUN apk add py-pip
# RUN apk add --no-cache python3-dev 
# RUN pip install --upgrade pip
# ENV PROJECT_DIR /user
# WORKDIR $(PROJECT_DIR)
# COPY . /user
# RUN pip --no-cache-dir install -r requirements.txt

# CMD ["python3", "app.py"]

# FROM alpine:latest

# RUN apk update
# RUN apk add py-pip
# RUN apk add --no-cache python3-dev 
# RUN pip install --upgrade pip

# WORKDIR /app
# COPY . /app
# RUN pip --no-cache-dir install -r requirements.txt

# CMD ["python3", "app.py"]
# ENV GOOGLE_APPLICATION_CREDENTIALS tactical-crow-340111-08a8dcc1139b.json


# FROM alpine:latest

# RUN apk update
# RUN apk add py-pip
# RUN apk add --no-cache python3-dev 
# RUN pip install --upgrade pip

# WORKDIR /app
# COPY . /app
# ENV GOOGLE_APPLICATION_CREDENTIALS tactical-crow-340111-08a8dcc1139b.json
# RUN pip --no-cache-dir install --upgrade -r requirements.txt

# CMD ["python3", "app.py"]
