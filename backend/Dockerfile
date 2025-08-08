FROM python:3.11-alpine

# Add git to install some requirements
RUN apk add --no-cache git

# Set up directories
RUN mkdir -p /var/www/backend-static/
WORKDIR /usr/src/app/backend
COPY . .

# Install requirements
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -U pip pip-tools gunicorn && \
    pip install -r requirements.txt && \
    pip install gunicorn
