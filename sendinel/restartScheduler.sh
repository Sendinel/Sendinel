#!/bin/bash

# This script needs write permissions to the sendinel directory.

sendinelPath="$(dirname $0)"
pidFile="$sendinelPath/scheduler.pid"


if [ -f "$pidFile" ]; then
    pid=$(cat $pidFile)
    kill $pid
else
    echo "Warning: Scheduler not running - no PID file found."
fi

python "$sendinelPath/backend/scheduler.py" >> /tmp/sendinelScheduler.log 2>&1 &

newPid=$!
echo -n $newPid > $pidFile

