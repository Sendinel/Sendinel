import sys, os

os.chdir(os.path.dirname(__file__))

try:
    import nose
except ImportError:
    print ('please install nose to run the tests')
    sys.exit(1)

# try:
#     import sendinel
# except ImportError:
#     print ('can not find sendinel')
#     sys.exit(1)

try:
    # make sure the current source is first on sys.path
    sys.path.insert(0, '..')
    sys.path.insert(0, '../..')
    import sendinel
except ImportError:
    print ('Cannot find Sendinel to test: %s' % sys.exc_info()[1])
    sys.exit(1)
else:
    print ('Sendinel test suite running (Python %s)...' %
           (sys.version.split()[0]))
    
nose.main()
