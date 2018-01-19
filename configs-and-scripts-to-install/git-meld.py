#!/usr/bin/python

import sys
import os

os.system('meld "{left_window}" "{right_window}"'.format(left_window=sys.argv[2], right_window=sys.argv[5]))
