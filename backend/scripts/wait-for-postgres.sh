#!/bin/sh

HOST=$1
PORT=$2

while ! pg_isready -h $HOST -p $PORT
do
    echo "$(date) - waiting for database to start"
    sleep 5
done