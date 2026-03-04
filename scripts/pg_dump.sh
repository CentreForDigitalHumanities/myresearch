#!/bin/bash


if [[ -z $1 ]]; then
    name=$(date -Iminutes)
else
    name=$1
fi

filename=$name.sql
filepath=/mnt/dumps/$filename
   
echo Dumping to dumps/$filename

if docker compose --profile dev exec mr-postgres sh -c \
	  "pg_dumpall -U postgres > $filepath"; then
    echo Success!
else
    echo Something went wrong.
    echo This script must be run as root with the mr-postgres container running.
fi
