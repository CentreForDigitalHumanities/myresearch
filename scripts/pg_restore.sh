#!/bin/bash
# Don't continue if we encounter an error
set -e

if [[ -z $1 ]]; then
    echo Argument required
    exit 1
fi

echo
echo @@@ Warning @@@
echo Do not run in production!
echo
echo This will destroy your current database. Continue? [y/N]
read y

if [[ $y != y && $y != Y ]]; then
    echo Aborting
    exit 1
fi

dump=$(basename $1)
echo Restoring $dump

filepath=/mnt/dumps/$dump

if docker compose --profile dev exec mr-postgres sh -c \
	  "psql -U postgres -f $filepath"; then
    echo Success!
else
    echo Something went wrong.
    echo This script must be run as root with the mr-postgres container running.
fi
    
