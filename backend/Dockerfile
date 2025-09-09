FROM python:3.11-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Add git to install some requirements
# Add curl to use for container healthcheck
RUN apk add --no-cache git curl

# Set up directories
RUN mkdir -p /var/www/backend-static/
WORKDIR /usr/src/app/backend
COPY . .

# Install requirements
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -U pip pip-tools gunicorn && \
    pip install -r requirements.txt && \
    pip install gunicorn
