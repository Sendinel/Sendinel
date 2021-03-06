from os.path import abspath, dirname, basename, splitext
from glob import glob
import sys
import unittest

sys.path.insert(0, abspath('../../'))

search_path = dirname(abspath(__file__))
files = glob(search_path + '/*.py')

for file in files:
    name = splitext(basename(file))[0]
    if name != "__init__":
        exec "from %s import *" % name
