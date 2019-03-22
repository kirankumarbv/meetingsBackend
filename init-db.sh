#!/bin/bash

rm -rf app.db
rm -rf migrations

python migrate.py db init
python migrate.py db migrate
python migrate.py db upgrade
