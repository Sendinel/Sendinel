import logging
import logging.handlers
import sys
from settings import LOGGING_LEVEL, LOGGING_LEVEL_TEST

logger = logging.getLogger('sendinel')
LOG_MSG_FORMAT = '%(asctime)s %(levelname)s %(filename)s#%(lineno)d %(message)s'

if 'test' in sys.argv:
  # set logging level for tests
  logger.setLevel(LOGGING_LEVEL_TEST)
else:
  # set logging level for anything else
  if len(logger.handlers) < 1:
    logger.setLevel(LOGGING_LEVEL)    
    handler = logging.StreamHandler()
    formatter = logging.Formatter(LOG_MSG_FORMAT)
    handler.setFormatter(formatter)
    logger.addHandler(handler)