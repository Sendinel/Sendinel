#!/bin/bash

# Replace these three settings.
PROJDIR="$1"
PORT="$2"

PIDFILE="$PROJDIR/fastcgi.pid"


cd $PROJDIR
if [ -f $PIDFILE ]; then
    kill `cat -- $PIDFILE`
    rm -f -- $PIDFILE
fi

exec /usr/bin/env - \
  PYTHONPATH="../python:.." \
  sendinel/manage.py runfcgi host=127.0.0.1 port=$2  pidfile=$PIDFILE 
