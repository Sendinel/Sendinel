#!/bin/bash

SENDINELPROJECT="$WORKSPACE/sendinel"
export PYTHONPATH="$WORKSPACE"

# set up settings
cp -av "$WORKSPACE/hudson/settings_test.py" "$SENDINELPROJECT/local_settings.py"
cd "$SENDINELPROJECT"

# compile language files
/usr/bin/django-admin compilemessages --settings=sendinel.settings

# tests and coverage
coverage run /usr/bin/django-admin test --settings=sendinel.settings -v2 --with-xunit
coverage xml --omit=/usr/


# pylint
echo "pylint running..."
pylint -f parseable sendinel --include-ids=y --generated-members=objects > pylint.txt
echo "pylint complete"


# docs
export DJANGO_SETTINGS_MODULE=sendinel.settings
cd "$WORKSPACE"
epydoc --graph all sendinel
unset DJANGO_SETTINGS_MODULE

# sloccount
sloccount --details --wide --addlang html sendinel > sloccount