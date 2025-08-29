FROM python:3.11-alpine

# Add git to install some requirements
# Add curl to use for container healthcheck
RUN apk add --no-cache git curl

WORKDIR /usr/src/app/backend
COPY requirements.txt .
RUN pip install -U pip pip-tools && pip install -r requirements.txt

COPY . .