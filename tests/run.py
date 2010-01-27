import sys

try:
    import nose
except ImportError:
    print ('please install nose to run the tests')
    sys.exit(1)

try:
    import sendinel
except ImportError:
    print ('can not find sendinel')
    sys.exit(1)
    
nose.main()