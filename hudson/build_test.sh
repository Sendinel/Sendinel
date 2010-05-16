#!/bin/bash

SENDINELPROJECT="$WORKSPACE/sendinel"
export PYTHONPATH="$WORKSPACE"
export DJANGO_SETTINGS_MODULE=sendinel.settings

# set up settings
cp -av "$WORKSPACE/hudson/settings_test.py" "$SENDINELPROJECT/local_settings.py"


# compile language files
cd "$SENDINELPROJECT"
/usr/bin/django-admin compilemessages
cd "$WORKSPACE"

# tests and coverage
coverage run /usr/bin/django-admin test -v2 --with-xunit
coverage xml --omit=/usr/


# pylint

# the following messages are disabled
# C0111: Missing docstring
# E1101: %s %r has no %r member Used when a variable is accessed for an unexistant member.
# W0612: Unused variable %r Used when a variable is defined but not used.
echo "pylint running..."
pylint -f parseable --include-ids=y --generated-members=objects \
    --disable=C0111,E1101,W0612 \
    sendinel \
    > pylint.txt
echo "pylint complete"


# docs

epydoc --graph all sendinel

# sloccount
sloccount --details --wide --addlang html sendinel > sloccount