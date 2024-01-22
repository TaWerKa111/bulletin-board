#!/bin/bash

set -e

upgrade_db(){
  /usr/local/bin/python3.11 -m alembic -c database/alembic.ini upgrade head
}

upgrade_db
echo "Complete create_admin"

create_admin() {
  /usr/local/bin/python3.11 /app/manage.py create-superuser -l admin -pw admin
}

create_admin
echo "Complete create_admin"

echo "$@"

exec "$@"
