FROM python:3.11-alpine

# Add git to install some requirements
RUN apk add --no-cache git

# Set up directories
RUN mkdir -p /var/www/backend-static/
WORKDIR /usr/src/app/backend
COPY . .

# Install requirements
RUN pip install -U pip pip-tools && pip install -r requirements.txt
RUN pip install gunicorn
