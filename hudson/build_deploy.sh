#!/bin/bash
if [ ! -n "$DEPLOY_SOURCE" ] || [ ! -n "$DEPLOY_TARGET" ] || [ ! -n "$FASTCGI_PORT" ]; then
    echo "Usage: $0"
    echo "This script needs the followingenvironment variables:"
    echo " DEPLOY_SOURCE - e.g. workspace of test job"
    echo " DEPLOY_TARGET - code will be copied there for deployment"
    echo " DEPLOY_SETTINGS - path to a django settings file that will be copied as local_settings"
    echo " FASTCGI_PORT - django will run on 127.0.0.1:FASTCGI_PORT"
    exit 1
fi

DJANGO_PROJECT="sendinel"
cd "$DEPLOY_TARGET/$DJANGO_PROJECT" || exit 1

# stop sendinel scheduler
./scheduler.sh stop || exit 1

# copy files over
rsync -av --delete "$DEPLOY_SOURCE/$DJANGO_PROJECT" "$DEPLOY_TARGET" || exit 1

# copy configuration
cp -av "$DEPLOY_SETTINGS" "$DEPLOY_TARGET/$DJANGO_PROJECT/local_settings.py" || exit 1

# restart FastCGI processes
"$DEPLOY_SOURCE/hudson/deploy_restart_fastcgi.sh" "$DEPLOY_TARGET" "$FASTCGI_PORT"|| exit 1

# copy docs over
rsync -av --delete "$DEPLOY_SOURCE/html" "$DEPLOY_TARGET"

# set up database and load fixtures
./manage.py syncdb --noinput -v2  || exit 1
./manage.py loaddata backend/fixtures/admin_auth.json || exit 1
./manage.py loaddata backend/fixtures/backend.xml || exit 1

# start scheduler
BUILD_ID=dontKillMe ./scheduler.sh start
