#!/bin/bash

# This script needs write permissions to the sendinel directory.

sendinelPath="$(dirname $0)"
pidFile="$sendinelPath/scheduler.pid"
logFile="/tmp/sendinelScheduler.log"

start() {
    echo -n "Starting Sendinel scheduler"
    cd $sendinelPath && \
    python "$sendinelPath/backend/scheduler.py" $pidFile
    echo "."
}

stop() {
    echo -n "Stopping sendinel scheduler"
    if [ -f "$pidFile" ]; then
        pid=$(cat $pidFile)
        kill $pid
        # pid file should be removed by python
    else
        echo "Warning: Scheduler not running - no PID file found."
    fi

    echo "."
}

case "$1" in
 start)
    start
    ;;
 stop)
    stop
    ;;
 restart)
    stop
    start
    ;;
 *)
    echo "Usage: $0 {start|stop|restart}" >&2
    exit 1
    ;;
esac

exit 0


