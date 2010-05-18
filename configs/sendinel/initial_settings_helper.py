import sys
from os.path import abspath, dirname

from django.core.management import setup_environ

# fix paths for run from commandline
PROJECT_PATH = dirname(abspath(__file__)) + "/../../"
sys.path.insert(0, PROJECT_PATH)
from sendinel import settings
setup_environ(settings) # this must be run before any model etc imports

def usage():
    print "Usage: initial_settings_helper.py <bluetooth enabled>"
    print "  bluetooth enabled: True or False"
    exit(1)

if len(sys.argv) != 2:
    usage()



boolean_map = {'True': True,
               'False': False}
try:
    bluetooth_enabled = boolean_map[sys.argv[1]]
except KeyError:
    usage()

from sendinel.backend.models import WayOfCommunication
bluetooth = WayOfCommunication.objects.get(name = "bluetooth")
bluetooth.enabled = bluetooth_enabled
bluetooth.save()
