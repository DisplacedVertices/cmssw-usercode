#!/usr/bin/env python

import os, sys
from collections import defaultdict

# Data structure is {batch_name : {sample_name : [(file1, nevents1), ...]}}

# To find things to clean:
#   cat SampleFiles_db.py | grep "': [{\[]" > order
# then edit and pass to pprint

from SampleFiles_db import SampleFiles

def setup(process, batch, sample, nevents, file=None):
    if file is not None:
        fnnevs = SampleFiles[batch][sample]
        if file >= len(fnnevs):
            raise ValueError('file is more than available')
        process.source.fileNames = [fnnevs[file][0]]
        process.maxEvents.input = -1
        return

    ntot = 0
    files = []
    for fn, n in SampleFiles[batch][sample]:
        files.append(fn)
        ntot += n
        if nevents > 0 and ntot > nevents:
            break
    process.source.fileNames = files
    process.maxEvents.input = nevents

def sum_nevents(batch):
    sums = defaultdict(int)
    for sample, filenev in SampleFiles[batch].iteritems():
        for fn, nev in filenev:
            sums[sample] += nev
    return dict(sums)

def jobs(filenevs):
    return sorted(int(os.path.basename(file).split('_')[-3]) for file, nev in filenevs)

from pprint import pprint as _pprint

def pprint(d, batches=None):
    # Would use regular pprint, but it just doesn't look good.

    if batches is None:
        batches = d.keys()
        batches.sort()

    print 'SampleFiles = {'
    for batch in batches:
        if type(batch) == tuple:
            batch, samples = batch
        else:
            samples = sorted(d[batch].keys())

        print "    '%s': {" % batch
        d2 = d[batch]
        for sample in samples:
            filenev = d2[sample]
            print "        '%s': [" % sample
            filenev.sort()
            maxw = max(len(fn) for fn, nev in filenev)
            for fn, nev in filenev:
                w = len(fn)
                print "            ('%s',%s%7i)," % (fn, ' '*(maxw - w), nev)
            print '        ],'
        print '    },'
    print '}'

if __name__ == '__main__' and 'read' in sys.argv:
    from JMTucker.Tools.Samples import all_samples
    from collections import defaultdict
    sys.argv.append('-b')
    import ROOT
    if os.environ['CMSSW_BASE']:
        ROOT.gSystem.Load('libFWCoreFWLite')
        ROOT.AutoLibraryLoader.enable()
        ROOT.gSystem.Load('libDataFormatsFWLite.so')
        ROOT.gSystem.Load('libDataFormatsPatCandidates.so')

    # Make dict with format as above from list of filenames in argv.
    d = defaultdict(lambda: defaultdict(list))

    def fill_fn_nevents(fn, batch, sample):
        f = ROOT.TFile.Open(fn)
        nevents = f.Get('Events').GetEntriesFast()
        print fn, nevents
        d[batch][sample].append((fn, nevents))
        
    if 'store' in sys.argv:
        for x in sys.argv[1:]:
            if '/store/' in x:
                x = x.split('/store/')[1]
                fn = 'dcap://cmsdca3.fnal.gov:24145/pnfs/fnal.gov/usr/cms/WAX/11/store/' + x
                x = x.split('/')
                user = x[1]
                batch = user + '-' + x[3] + '-' + x[4]
                sample = x[2]
                fill_fn_nevents(fn, batch, sample)
    else:
        for x in sys.argv[1:]:
            if os.path.isfile(x):
                fn = os.path.realpath(os.path.expanduser(x)) # shell should expanduser ~ already but why not
                path, base_fn = os.path.split(fn)
                x, dirname = os.path.split(path)

                batch, sample = None, None
                for s in all_samples:
                    if dirname.endswith('_' + s.name):
                        batch = dirname.replace('_' + sample.name, '')
                        sample = s.name
                if batch is None:
                    batch, sample = dirname.rsplit('_', 1)

                fill_fn_nevents(fn, batch, sample)

    print repr(d)

    print '\n --- cut here ---\n'

    pprint(d)

elif __name__ == '__main__' and 'nevents' in sys.argv:
    import JMTucker.Tools.Samples as Samples
    batch = sys.argv[sys.argv.index('nevents')+1]
    sums = sum_nevents(batch)
    for sample in sorted(sums):
        filenevs = SampleFiles[batch][sample]
        jbs = jobs(filenevs)
        if len(jbs) != len(set(jbs)):
            print 'problem with jobs'
        nevents = sums[sample]
        orig = -999
        try:
            sobj = getattr(Samples, sample)
            orig = sobj.total_events if sobj.total_events > 0 else sobj.nevents_orig
        except AttributeError:
            pass
        if nevents > orig:
            print 'what the'

        if 'eff' in sys.argv:
            eff = float(nevents)/orig
            print '%s = %9.4e  # %8i / %8i' % ((sample + '.ana_filter_eff').ljust(35), eff, nevents, orig)
        else:
            print '%s = %8i' % ((sample + '.total_events').ljust(30), nevents),
            if nevents != orig:
                nfiles = len(filenevs)
                diff = sorted(set(range(1,nfiles+1)).symmetric_difference(jobs(filenevs)))
                print '  # in %i files (%i ev/file), original # events = %8i. jobs diff: %s' % (nfiles, round(nevents/nfiles), orig, diff)
            else:
                print

elif __name__ == '__main__' and 'print' in sys.argv:
    pprint(SampleFiles)
