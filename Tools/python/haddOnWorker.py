#!/usr/bin/env python

'''
Very simple script which basically acts like:
hadd [output] [in1 in2 ...]
This solely exists for use as a simple condor executable.

USAGE:
python haddOnWorker.py [output] [in1 in2 ...]
'''

import sys, os
import socket

hostname = socket.gethostname()
print "Host name: ", hostname
print sys.argv

target = sys.argv[1]
flist = sys.argv[2:]

fstr = ' '.join(flist)

cmd = 'hadd ' + target + ' ' + fstr
print cmd
os.system(cmd)
