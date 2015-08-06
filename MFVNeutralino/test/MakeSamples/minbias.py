import os

try:
    print 'getting minbias file list from cache'
    from minbias_files import files
except ImportError:
    print 'nope, getting minbias file list from DBS and caching'
    from JMTucker.Tools.DBS import files_in_dataset
    files = files_in_dataset('/MinBias_TuneCUETP8M1_13TeV-pythia8/RunIIWinter15GS-MCRUN2_71_V1-v1/GEN-SIM')
    open('minbias_files.py', 'wt').write('files = %r\n' % files)
