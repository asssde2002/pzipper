#!/bin/sh

DB_NAME=pzipper_db

echo "###";
echo "# Create DB";
echo "###";
createdb -U postgres ${DB_NAME}


echo "###";
echo "# Refeed Data";
echo "###";
psql -U postgres --dbname=${DB_NAME} < /db/dumps/maindb.sql

