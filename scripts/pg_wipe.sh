#!/bin/bash
# Don't continue if we encounter an error
set -e

echo
echo @@@ Warning @@@
echo Do not run in production!
echo
echo This will destroy your current database. You may want to run pg_dump.sh to make a backup first.
echo Continue? [y/N]

read y
if [[ $y != y && $y != Y ]]; then
    echo Aborting
    exit 1
fi

if docker compose --profile dev run mr-postgres sh -c \
	  "rm -r /var/lib/postgresql/data/*"; then
    echo Success!
else
    echo Something went wrong.
    echo This script must be run as root.
fi
    

