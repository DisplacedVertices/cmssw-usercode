import os
from collections import defaultdict
from FWCore.PythonUtilities.LumiList import LumiList
from JMTucker.Tools.ROOTTools import *
from JMTucker.Tools.Samples import *

def is_data_fn(fn):
    return 'JetHT' in fn

def gettree(root_fn, path):
    f = ROOT.TFile(root_fn)
    t = f.Get(path + '/t')
    return f, t

def getlist(root_fn, path):
    f, t = gettree(root_fn, path)
    is_data = is_data_fn(root_fn)
    branches = 'run:lumi:event' if is_data else 'lumi:event'
    return sorted(set(detree(t, branches)))
    
def writelist(l, out_fn, gzip):
    f = open(out_fn, 'wt')
    is_data = is_data_fn(out_fn)
    fmt = '(%i,%i,%i),\n' if is_data else '(%i,%i),\n'
    for x in l:
        f.write(fmt % x)
    f.close()
    if gzip:
        os.system('gzip %s' % out_fn)

def makelist(root_fn, out_fn, gzip):
    writelist(getlist(root_fn), out_fn, gzip)

def writejson(l, out_fn):
    is_data = is_data_fn(out_fn)
    if not is_data:
        run = 1
    rll = defaultdict(list)
    for x in l:
        if is_data:
            run, lumi = x[:2]
        else:
            lumi = x[0]
        rll[run].append(lumi)
    LumiList(runsAndLumis=rll).writeJSON(out_fn)

def printforsubmit():
    root = '/uscms_data/d2/tucker/crab_dirs/MinitreeV12'
    samples = data_samples + data_samples_2015 + ttbar_samples + ttbar_samples_2015 + qcd_samples_sum + qcd_samples_sum_2015

    for sample in samples:
        fn = os.path.join(root, '%s.root' % sample.name)
        for ntracks, path in (3,'tre33'), (4,'tre44'), (5,'mfvMiniTree'):
            if is_data_fn(sample.name) and ntracks == 5:
                continue
            f, t = gettree(fn, path)
            n = t.Draw('nvtx', 'nvtx==1')
            print "(('%s', %i), %i)," % (sample.name, ntracks, n)

def dosamples():
    root = '/uscms_data/d2/tucker/crab_dirs/MinitreeV12'
    paths = 'tre33', 'tre34', 'tre44', 'mfvMiniTree'
    samples = data_samples + data_samples_2015 + ttbar_samples + ttbar_samples_2015 + qcd_samples + qcd_samples_ext + qcd_samples_2015 + qcd_samples_ext_2015

    for sample in samples:
        print sample.name
        lists = [getlist(os.path.join(root, '%s.root' % sample.name), p) for p in paths]
        l = sorted(set(sum(lists, [])))
        writelist(l, 'vetolist.%s' % sample.name, True)
        writejson(l, 'json.%s'     % sample.name)

#writelist(sum([getlist('/uscms_data/d2/tucker/crab_dirs/MinitreeV12/qcdht1000ext.root', p) for p in 'tre33', 'tre34', 'tre44', 'mfvMiniTree'], []), 'veto_temp', True)
#makelist('/uscms_data/d2/tucker/crab_dirs/MinitreeV12/ttbar.root', 'veto_ttbar_temp', True)
#dosamples()
printforsubmit()

