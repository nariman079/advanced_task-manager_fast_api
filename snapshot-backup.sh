#!/bin/sh

while true; do
    cp /data/objectmanager.rdb /backup/$(date +%s).rdb
    sleep $BACKUP_PERIOD
done