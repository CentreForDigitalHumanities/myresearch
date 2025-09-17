FROM python:3.11-alpine

# Add git to install some requirements
# Add curl to use for container healthcheck
# Add xmlsec for saml
RUN apk add --no-cache git curl xmlsec

# Set up directories
RUN mkdir -p /var/www/backend-static/
WORKDIR /usr/src/app/backend
COPY . .

# Install requirements
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -U pip pip-tools gunicorn && \
    pip install -r requirements.txt && \
    pip install gunicorn
