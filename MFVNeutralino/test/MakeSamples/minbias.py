import os

try:
    print 'getting minbias file list from cache'
    from minbias_files import files
except ImportError:
    print 'nope, getting minbias file list from DBS and caching'
    from JMTucker.Tools.DBS import files_in_dataset
    from JMTucker.Tools.general import to_pickle
    files = files_in_dataset('/MinBias_TuneCUETP8M1_13TeV-pythia8/RunIIWinter15GS-MCRUN2_71_V1-v1/GEN-SIM')
    to_pickle(files, 'minbias_files.pkl', comp=True)
    open('minbias_files.py', 'wt').write("import cPickle, gzip; files = cPickle.load(gzip.GzipFile('minbias_files.pkl', 'rb'))\n")
