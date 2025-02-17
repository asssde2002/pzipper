#!/bin/sh

DB_NAME=pzipper_db

echo "###";
echo "# Create Db";
echo "###";
createdb -U postgres ${DB_NAME}
