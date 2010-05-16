# allow wildcard import - explicitly listing all options here again doesn't
#   seem to make sense
# pylint: disable=W0614,W0401
from sendinel.settings import * # Properly namespaced as needed.

# ROOT_URLCONF = 'yourapp.settings.test.urls'

# fix for Django test client not finding urls module
import sys
sys.path.insert(0, PROJECT_PATH)


DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = ':memory:'
 
INSTALLED_APPS += ('django_nose', )
TEST_RUNNER = 'django_nose.run_tests'
