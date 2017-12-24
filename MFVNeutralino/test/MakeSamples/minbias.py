import os
from gzip import GzipFile as gzip_open

def _read_gzip_file(fn):
    print 'getting minbias file list from cache', fn
    files = []
    with gzip_open(fn) as f:
        for line in f:
            line = line.strip()
            if line:
                files.append(line)
    return files

def _from_dbs_and_cache(fn, ds):
    print 'hitting DBS %s for %s' % (ds, fn)
    from JMTucker.Tools.DBS import files_in_dataset
    files = files_in_dataset(ds, instance='phys03' if ds.endswith('/USER') else 'global')
    with gzip_open(fn, 'w') as f:
        for file in files:
            f.write(file)
            f.write('\n')
    return files

def _from_cache_or_dbs(fn, ds):
    return _read_gzip_file(fn) if os.path.isfile(fn) else _from_dbs_and_cache(fn, ds)

def files():
    #return _from_cache_or_dbs('official_minbias.txt.gz', '/MinBias_TuneCUETP8M1_13TeV-pythia8/RunIISummer15GS-MCRUN2_71_V1-v2/GEN-SIM')
    return _from_cache_or_dbs('private_minbias.txt.gz', '/minbias/tucker-RunIISummer15GS-MCRUN2_71_V1-79473ee9dd0d24ba1969f21e10b4fae5/USER')

def premix_files():
    return _from_cache_or_dbs('minbias_premix.txt.gz', '/Neutrino_E-10_gun/RunIISpring15PrePremix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v2-v2/GEN-SIM-DIGI-RAW')
