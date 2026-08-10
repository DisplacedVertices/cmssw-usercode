#!/usr/bin/env python

'''
This is the driver for haddCondorSubmit. This file takes a list of filenames
from all.txt (to be refined in the future) and splits up the hadding for each sample.
Then for each sample, up to 10 files are hadded together at a given time on the
Condor nodes.

USAGE:
python haddCondorDriver.py [path to output dir] [path to input dir]
'''

import ROOT
import sys, os # glob, argparse
import subprocess
import socket
import time
#from JMTucker.Tools.CRAB3ToolsSh import is_crab_working_dir, crab_hadd_args, crab_hadd_files, crab_hadd
#from JMTucker.Tools.CondorTools import is_cs_dir, cs_hadd_args, cs_hadd_files, cs_hadd

#path = '/usatlas/u/jreic/tpframe/Run/Full2015_AFS/fetch/'
#path = '/direct/usatlas+u/jreic/condor/dir_hadd_step2/'

globalOutputPath = sys.argv[1] + '/'
globalInputPath = sys.argv[2] + '/'


iteration = 0

while True :
    outputPath = globalOutputPath + '/' + str(iteration) + '/'
    os.mkdir(outputPath)

    if iteration == 0 :
        inputPath = globalInputPath
    else :
        inputPath = globalOutputPath + '/' + str(iteration-1) + '/'

    fileOfFileNames = open('all.txt','r')
    for line in fileOfFileNames :
        line = line.strip()

        #cmd = 'haddCondorSubmit.py ' + outputPath + ' ' + line + ' ' + inputPath + line.replace('.root', '*.root')
        cmd = 'python haddCondorSubmit.py ' + outputPath + ' ' + line + ' ' + inputPath + line.replace('.root', '*.root')
        print cmd
        os.system(cmd)
        print ''

    fileOfFileNames.close()    

    
    while True :
        jobs = subprocess.Popen('condor_q ' + os.getenv('USER'), shell=True, stdout = subprocess.PIPE)
        output = jobs.communicate()[0]

        if not output.replace(' ','') :
            display = 'Condor Problem! Waiting...'
            print display
            continue

        elif os.getenv('USER') not in output :
            print 'condor finished!'
            break

        else :
           # print output
            print 'waiting...'
            #time.sleep(5)
            time.sleep(120)

    ls = subprocess.Popen('ls ' + outputPath, shell=True, stdout = subprocess.PIPE)
    ls = ls.communicate()[0]

    if '-1.root' in ls :
        print str(iteration)
        iteration += 1
    else :
        print 'done!'
        os.system('mv ' + outputPath + '*.root ' + globalOutputPath)
        os.system('rename -0.root .root ' + globalOutputPath + '/*')
        break
