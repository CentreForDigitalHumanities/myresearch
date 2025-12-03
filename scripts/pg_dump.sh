#!/bin/bash


if [[ -z $1 ]]; then
    filepath=/mnt/dumps/$(date -Iminutes).sql
    mkdir -p dumps
else
   filepath=$1
fi
   
echo Dumping to $filepath

if docker compose --profile dev exec mr-postgres sh -c \
	  "pg_dumpall -U postgres > $filepath"; then
    echo Success!
else
    echo Something went wrong.
    echo This script must be run as root with the mr-postgres container running.
fi
