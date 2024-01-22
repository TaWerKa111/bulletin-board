#!/bin/bash

set -e

upgrade_db(){
  /usr/local/bin/python3.11 -m alembic -c common/alembic.ini upgrade head
}

upgrade_db
echo "Complete create_admin"

create_admin() {
  /usr/local/bin/python3.11 -m alembic -c common/alembic.ini upgrade head
}

create_admin
echo "Complete create_admin"