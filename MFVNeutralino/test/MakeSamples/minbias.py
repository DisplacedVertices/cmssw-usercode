import os

try:
    print 'getting minbias file list from cache'
    from minbias_files import files
except ImportError:
    print 'getting minbias file list from DBS and caching'
    from JMTucker.Tools.DBS import files_in_dataset
    files = files_in_dataset('/MinBias_TuneZ2star_8TeV-pythia6/Summer12-START50_V13-v3/GEN-SIM')
    open('minbias_files.py', 'wt').write('files = %r\n' % files)
