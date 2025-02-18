#!/bin/sh

PGPASSWORD=postgres pg_dump -h db -U postgres -Fp -O \
  --exclude-table-data=django_admin_log \
  --exclude-table-data=django_session \
  pzipper_db > dumps/maindb.sql