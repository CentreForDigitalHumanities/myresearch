FROM python:3.11-alpine

# Add git to install some requirements
RUN apk add --no-cache git

WORKDIR /usr/src/app/backend
COPY requirements.txt .
RUN pip install -U pip pip-tools && pip install -r requirements.txt

COPY . .