import logging
import logging.handlers
import sys
from sendinel.settings import LOGGING_LEVEL, LOGGING_LEVEL_TEST

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

# logging decorator for views
def log_request(viewfunc):
    def do_log_request(*args, **kwargs):
        request = args[0]
        get_data = dict(request.GET, **request.POST) # merge both dicts
        
         # args[0] should be request
        logger.info("%s %s.%s %s %s" % (args[0].method,
                                    viewfunc.__module__,
                                    viewfunc.__name__,
                                    str(kwargs),
                                    str(get_data)))
        return viewfunc(*args, **kwargs)
    return do_log_request
