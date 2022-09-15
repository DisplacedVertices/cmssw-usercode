#!/usr/bin/env python

'''
This script creates the condor submission files
for a given input dataset. These are then submitted
to condor, where haddOnWorker.py is called
in order to do the hadding. Only 10 files are hadded
at a time, to ensure for speedy jobs.

USAGE:
python haddCondorSubmit.py [target dir] [output dataset rootfile] [in1 in2 ...]

update : to be used with mhadd, combine the target dir and output dataset rootfile 
'''

import ROOT
import sys, os
import socket

#print 'haddCondorSubmit'

hostname = socket.gethostname()
#print "Host name: ", hostname

# dir_hadd = sys.argv[1]
# target = sys.argv[2]
# flist = sys.argv[3:]
print sys.argv
dir_hadd_target = sys.argv[1]
flist = sys.argv[2:] 

#splitting up the arguments again
dir_hadd, target = dir_hadd_target.rsplit("/", 1)

target = target.replace('.root','')


nTotal = len(flist)
nLoops = 0

# Special case! Just copy the files over rather than wasting time hadding a single file
if nTotal == 1 :
    infile = flist.pop()
    outfile = dir_hadd+'/'+target+'.root'
    os.system('cp ' + infile + ' ' + outfile)
    print 'copied ' + infile + ' to ' + outfile
    print 'exiting!'
    exit()


while len(flist) > 0 :

    strNLoops = str(nLoops)

   # nItemsToPop = 10
    nItemsToPop = 200

    inputFiles = ''

    for i in xrange(nItemsToPop) :
        if len(flist) > 0 :
            fstr = flist.pop()
            inputFiles = inputFiles + ' ' + fstr

    prefixStr = dir_hadd+'/'+target+'-'+strNLoops
    
    condorFile = open(dir_hadd+'/submit_'+strNLoops, 'w')
    condorFile.write('executable       = haddOnWorker.py\n')
    condorFile.write('universe         = vanilla\n')
    condorFile.write('log              = '+prefixStr+'.log\n')
    condorFile.write('output           = '+prefixStr+'.out\n')
    condorFile.write('error            = '+prefixStr+'.err\n')
    condorFile.write('arguments        = '+prefixStr+'.root ' + inputFiles + '\n')
    condorFile.write('getenv           = True\n')

    # if 'bnl' in hostname :
    #     condorFile.write('accounting_group = group_atlas.upenn\n')

    condorFile.write('queue\n')
    condorFile.close()

    os.system('condor_submit '+dir_hadd+'/submit_'+strNLoops)
    
    nLoops += 1
