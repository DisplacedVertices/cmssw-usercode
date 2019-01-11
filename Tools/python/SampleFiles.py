import os, base64, zlib, cPickle as pickle
from collections import defaultdict
from fnmatch import fnmatch
from itertools import chain
from pprint import pprint
from JMTucker.Tools.CRAB3ToolsBase import decrabify_list
from JMTucker.Tools.CMSSWTools import cmssw_base

_d = {}
_added_from_enc = {}

def _enc(d):
    return base64.b64encode(zlib.compress(pickle.dumps(d)))

def _denc(encd):
    return pickle.loads(zlib.decompress(base64.b64decode(encd)))

def _add(d, allow_overwrite=False, _enced_call=[0]):
    global _d
    enced = type(d) == str
    if enced:
        d = _denc(d)
        _enced_call[0] += 1
    if not allow_overwrite:
        for k in d:
            if _d.has_key(k):
                raise ValueError('already have key %s' % repr(k))
            if len(d[k][1]) != d[k][0]:
                raise ValueError('length check problem: %s %s supposed to be %i but is %i' % (k[0], k[1], d[k][0], len(d[k][1])))
    _d.update(d)
    if enced:
        for k in d.keys():
            _added_from_enc[k] = _enced_call[0]

def _remove_file(sample, ds, fn):
    n, fns = _d[(sample,ds)]
    fns.remove(fn)
    _d[(sample,ds)] = (n-1, fns)

def _replace_file(sample, ds, fn, fn2):
    n, fns = _d[(sample,ds)]
    fns.remove(fn)
    fns.append(fn2)
    _d[(sample,ds)] = (n, fns)

def _add_ds(ds, d, allow_overwrite=False):
    d2 = {}
    for k in d:
        d2[(k,ds)] = d[k]
    _add(d2, allow_overwrite)

def _fromnumlist(path, numlist, but=[], fnbase='ntuple', add=[], numbereddirs=True):
    return add + [path + ('/%04i' % (i/1000) if numbereddirs else '') + '/%s_%i.root' % (fnbase, i) for i in numlist if i not in but]

def _fromnum1(path, n, but=[], fnbase='ntuple', add=[], numbereddirs=True): # crab starts job numbering at 1
    l = _fromnumlist(path, xrange(1,n+1), but, fnbase, add, numbereddirs)
    return (len(l), l)

def _fromnum0(path, n, but=[], fnbase='ntuple', add=[], numbereddirs=True): # condorsubmitter starts at 0
    l = _fromnumlist(path, xrange(n), but, fnbase, add, numbereddirs)
    return (len(l), l)

def _frommerge(path, n):
    assert path.endswith('/merge') and path.count('/merge') == 1
    return (n, [path.replace('/merge', '/merge%s_0.root') % s for s in [''] + ['%03i' % x for x in xrange(1,n)]])

def _join(*l):
    ns, ls = zip(*l)
    return (sum(ns), sum(ls, []))

def keys():
    return _d.keys()

def dump():
    pprint(_d)

def allfiles():
    return (fn for (sample, ds), (n, fns) in _d.iteritems() for fn in fns)

def summary():
    d = defaultdict(list)
    for k in _d.iterkeys():
        a,b = k
        d[a].append((b, _d[k][0]))
    for a in sorted(d.keys()):
        for b,n in d[a]:
            print a.ljust(40), b.ljust(20), '%5i' % n

def has(name, ds):
    return _d.has_key((name, ds))

def get(name, ds):
    return _d.get((name, ds), None)

def get_fns(name, ds):
    return _d[(name,ds)][1]

def get_local_fns(name, ds, num=-1):
    fns = _d[(name, ds)][1]
    if num > 0:
        fns = fns[:num]
    return [('root://cmseos.fnal.gov/' + fn) if fn.startswith('/store/user') else fn for fn in fns]

def set_process(process, name, ds, num=-1):
    process.source.fileNames = get_local_fns(name, ds, num)

def who(name, ds):
    nfns, fns = _d[(name,ds)]
    users = set()
    for fn in fns:
        assert fn.startswith('/store')
        if fn.startswith('/store/user'):
            users.add(fn.split('/')[3])
    return tuple(sorted(users))

__all__ = [
    'dump',
    'get',
    'summary',
    ]

################################################################################

execfile(cmssw_base('src/JMTucker/Tools/python/enc_SampleFiles.py'))

_remove_file('ttbarht0800_2017', 'miniaod', '/store/mc/RunIIFall17MiniAODv2/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/40000/225CD078-B3A4-E811-AA74-001E67DDC254.root')
_remove_file('ttbarht0800_2017', 'miniaod', '/store/mc/RunIIFall17MiniAODv2/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/60000/BC22A92A-7BBA-E811-8A2B-0242AC1C0501.root')
_remove_file('ttbarht1200_2017', 'miniaod', '/store/mc/RunIIFall17MiniAODv2/TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/90000/6E6C0DD6-349B-E811-A4E1-0CC47A6C063E.root')
_remove_file('qcdht0700_2018', 'miniaod', '/store/mc/RunIIAutumn18MiniAOD/QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/102X_upgrade2018_realistic_v15-v1/020000/582A14C2-1BD1-6848-AE57-C110F6E929A0.root')

_add_ds("main", {
'mfv_neu_tau000100um_M0400_2017': _fromnum1("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau000100um_M0400/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_053632", 100, fnbase="reco"),
'mfv_neu_tau000100um_M0600_2017': _fromnum1("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau000100um_M0600/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_053653", 100, fnbase="reco"),
'mfv_neu_tau000100um_M0800_2017': _fromnum1("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau000100um_M0800/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_053713", 100, fnbase="reco"),
'mfv_neu_tau000100um_M1200_2017': _fromnum1("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau000100um_M1200/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_053737", 100, fnbase="reco"),
'mfv_neu_tau000100um_M1600_2017': _fromnum1("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau000100um_M1600/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_053805", 100, fnbase="reco"),
'mfv_neu_tau000100um_M3000_2017': _fromnum1("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau000100um_M3000/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_053825", 100, fnbase="reco"),
'mfv_neu_tau000300um_M0400_2017': _fromnum1("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau000300um_M0400/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_053847", 100, fnbase="reco"),
'mfv_neu_tau000300um_M0600_2017': _fromnum1("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau000300um_M0600/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_053908", 100, fnbase="reco"),
'mfv_neu_tau000300um_M0800_2017': _fromnum1("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau000300um_M0800/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_053929", 100, fnbase="reco"),
'mfv_neu_tau000300um_M1200_2017': _fromnum1("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau000300um_M1200/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_053953", 100, fnbase="reco"),
'mfv_neu_tau000300um_M1600_2017': _fromnum1("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau000300um_M1600/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_054019", 100, fnbase="reco"),
'mfv_neu_tau000300um_M3000_2017': _fromnum1("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau000300um_M3000/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_054045", 100, fnbase="reco"),
'mfv_neu_tau001000um_M0400_2017': _fromnum1("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau001000um_M0400/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_054108", 100, fnbase="reco"),
'mfv_neu_tau001000um_M0600_2017': _fromnum1("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau001000um_M0600/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_054132", 100, fnbase="reco"),
'mfv_neu_tau001000um_M0800_2017': _fromnum1("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau001000um_M0800/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_054154", 100, fnbase="reco"),
'mfv_neu_tau001000um_M1200_2017': _fromnum1("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau001000um_M1200/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_054216", 100, fnbase="reco"),
'mfv_neu_tau001000um_M1600_2017': _fromnum1("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau001000um_M1600/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_054235", 100, fnbase="reco"),
'mfv_neu_tau001000um_M3000_2017': _fromnum1("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau001000um_M3000/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_054256", 100, fnbase="reco"),
'mfv_neu_tau010000um_M0400_2017': _fromnum1("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau010000um_M0400/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_054321", 100, fnbase="reco"),
'mfv_neu_tau010000um_M0600_2017': _fromnum1("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau010000um_M0600/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_054342", 100, fnbase="reco"),
'mfv_neu_tau010000um_M0800_2017': _fromnum1("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau010000um_M0800/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_054406", 100, fnbase="reco"),
'mfv_neu_tau010000um_M1200_2017': _fromnum1("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau010000um_M1200/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_054427", 100, fnbase="reco"),
'mfv_neu_tau010000um_M1600_2017': _fromnum1("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau010000um_M1600/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_054448", 100, fnbase="reco"),
'mfv_neu_tau010000um_M3000_2017': _fromnum1("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau010000um_M3000/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_054509", 100, fnbase="reco"),
'mfv_neu_tau030000um_M0400_2017': _fromnum1("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau030000um_M0400/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_054532", 100, fnbase="reco"),
'mfv_neu_tau030000um_M0600_2017': _fromnum1("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau030000um_M0600/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_054551", 100, fnbase="reco"),
'mfv_neu_tau030000um_M0800_2017': _fromnum1("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau030000um_M0800/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_054616", 100, fnbase="reco"),
'mfv_neu_tau030000um_M1200_2017': _fromnum1("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau030000um_M1200/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_054637", 100, fnbase="reco"),
'mfv_neu_tau030000um_M1600_2017': _fromnum1("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau030000um_M1600/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_054659", 100, fnbase="reco"),
'mfv_neu_tau030000um_M3000_2017': _fromnum1("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau030000um_M3000/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_054722", 100, fnbase="reco"),
'mfv_neu_tau100000um_M0400_2017': _fromnum1("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau100000um_M0400/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_054744", 100, fnbase="reco"),
'mfv_neu_tau100000um_M0600_2017': _fromnum1("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau100000um_M0600/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_054806", 100, fnbase="reco"),
'mfv_neu_tau100000um_M0800_2017': _fromnum1("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau100000um_M0800/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_054830", 100, fnbase="reco"),
'mfv_neu_tau100000um_M1200_2017': _fromnum1("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau100000um_M1200/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_054851", 100, fnbase="reco"),
'mfv_neu_tau100000um_M1600_2017': _fromnum1("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau100000um_M1600/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_054916", 100, fnbase="reco"),
'mfv_neu_tau100000um_M3000_2017': _fromnum1("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau100000um_M3000/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_054937", 100, fnbase="reco"),
'mfv_stopdbardbar_tau000100um_M0400_2017': _fromnum1("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau000100um_M0400/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_050346", 100, fnbase="reco"),
'mfv_stopdbardbar_tau000100um_M0600_2017': _fromnum1("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau000100um_M0600/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_050416", 100, fnbase="reco"),
'mfv_stopdbardbar_tau000100um_M0800_2017': _fromnum1("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau000100um_M0800/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_050436", 100, fnbase="reco"),
'mfv_stopdbardbar_tau000100um_M1200_2017': _fromnum1("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau000100um_M1200/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_050457", 100, fnbase="reco"),
'mfv_stopdbardbar_tau000100um_M1600_2017': _fromnum1("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau000100um_M1600/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_050522", 100, fnbase="reco"),
'mfv_stopdbardbar_tau000100um_M3000_2017': _fromnum1("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau000100um_M3000/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_050553", 100, fnbase="reco"),
'mfv_stopdbardbar_tau000300um_M0400_2017': _fromnum1("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau000300um_M0400/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_050621", 100, fnbase="reco"),
'mfv_stopdbardbar_tau000300um_M0600_2017': _fromnum1("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau000300um_M0600/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_050644", 100, fnbase="reco"),
'mfv_stopdbardbar_tau000300um_M0800_2017': _fromnum1("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau000300um_M0800/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_050707", 100, fnbase="reco"),
'mfv_stopdbardbar_tau000300um_M1200_2017': _fromnum1("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau000300um_M1200/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_050729", 100, fnbase="reco"),
'mfv_stopdbardbar_tau000300um_M1600_2017': _fromnum1("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau000300um_M1600/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_050750", 100, fnbase="reco"),
'mfv_stopdbardbar_tau000300um_M3000_2017': _fromnum1("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau000300um_M3000/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_050815", 100, fnbase="reco"),
'mfv_stopdbardbar_tau001000um_M0400_2017': _fromnum1("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau001000um_M0400/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_050856", 100, fnbase="reco"),
'mfv_stopdbardbar_tau001000um_M0600_2017': _fromnum1("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau001000um_M0600/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_050920", 100, fnbase="reco"),
'mfv_stopdbardbar_tau001000um_M0800_2017': _fromnum1("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau001000um_M0800/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_050941", 100, fnbase="reco"),
'mfv_stopdbardbar_tau001000um_M1200_2017': _fromnum1("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau001000um_M1200/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_051007", 100, fnbase="reco"),
'mfv_stopdbardbar_tau001000um_M1600_2017': _fromnum1("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau001000um_M1600/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_051027", 100, fnbase="reco"),
'mfv_stopdbardbar_tau001000um_M3000_2017': _fromnum1("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau001000um_M3000/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_051047", 100, fnbase="reco"),
'mfv_stopdbardbar_tau010000um_M0400_2017': _fromnum1("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau010000um_M0400/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_051109", 100, fnbase="reco"),
'mfv_stopdbardbar_tau010000um_M0600_2017': _fromnum1("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau010000um_M0600/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_051130", 100, fnbase="reco"),
'mfv_stopdbardbar_tau010000um_M0800_2017': _fromnum1("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau010000um_M0800/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_051150", 100, fnbase="reco"),
'mfv_stopdbardbar_tau010000um_M1200_2017': _fromnum1("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau010000um_M1200/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_051213", 100, fnbase="reco"),
'mfv_stopdbardbar_tau010000um_M1600_2017': _fromnum1("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau010000um_M1600/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_051234", 100, fnbase="reco"),
'mfv_stopdbardbar_tau010000um_M3000_2017': _fromnum1("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau010000um_M3000/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_051257", 100, fnbase="reco"),
'mfv_stopdbardbar_tau030000um_M0400_2017': _fromnum1("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau030000um_M0400/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_051325", 100, fnbase="reco"),
'mfv_stopdbardbar_tau030000um_M0600_2017': _fromnum1("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau030000um_M0600/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_051346", 100, fnbase="reco"),
'mfv_stopdbardbar_tau030000um_M0800_2017': _fromnum1("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau030000um_M0800/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_051408", 100, fnbase="reco"),
'mfv_stopdbardbar_tau030000um_M1200_2017': _fromnum1("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau030000um_M1200/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_051431", 100, fnbase="reco"),
'mfv_stopdbardbar_tau030000um_M1600_2017': _fromnum1("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau030000um_M1600/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_051454", 100, fnbase="reco"),
'mfv_stopdbardbar_tau030000um_M3000_2017': _fromnum1("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau030000um_M3000/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_051514", 100, fnbase="reco"),
'mfv_stopdbardbar_tau100000um_M0400_2017': _fromnum1("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau100000um_M0400/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_051539", 100, fnbase="reco"),
'mfv_stopdbardbar_tau100000um_M0600_2017': _fromnum1("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau100000um_M0600/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_051615", 100, fnbase="reco"),
'mfv_stopdbardbar_tau100000um_M0800_2017': _fromnum1("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau100000um_M0800/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_051638", 100, fnbase="reco"),
'mfv_stopdbardbar_tau100000um_M1200_2017': _fromnum1("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau100000um_M1200/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_051659", 100, fnbase="reco"),
'mfv_stopdbardbar_tau100000um_M1600_2017': _fromnum1("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau100000um_M1600/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_051722", 100, fnbase="reco"),
'mfv_stopdbardbar_tau100000um_M3000_2017': _fromnum1("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau100000um_M3000/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_051745", 100, fnbase="reco"),
})


_add_ds("miniaod", {
'mfv_neu_tau000100um_M0400_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau000100um_M0400/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_081953", 5, fnbase="miniaod"),
'mfv_neu_tau000100um_M0600_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau000100um_M0600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_081954", 5, fnbase="miniaod"),
'mfv_neu_tau000100um_M0800_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau000100um_M0800/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_081955", 5, fnbase="miniaod"),
'mfv_neu_tau000100um_M1200_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau000100um_M1200/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_081956", 5, fnbase="miniaod"),
'mfv_neu_tau000100um_M1600_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau000100um_M1600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_081957", 5, fnbase="miniaod"),
'mfv_neu_tau000100um_M3000_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau000100um_M3000/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_081958", 5, fnbase="miniaod"),
'mfv_neu_tau000300um_M0400_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau000300um_M0400/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_081959", 5, fnbase="miniaod"),
'mfv_neu_tau000300um_M0600_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau000300um_M0600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082000", 5, fnbase="miniaod"),
'mfv_neu_tau000300um_M0800_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau000300um_M0800/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082001", 5, fnbase="miniaod"),
'mfv_neu_tau000300um_M1200_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau000300um_M1200/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082002", 5, fnbase="miniaod"),
'mfv_neu_tau000300um_M1600_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau000300um_M1600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082003", 5, fnbase="miniaod"),
'mfv_neu_tau000300um_M3000_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau000300um_M3000/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082004", 5, fnbase="miniaod"),
'mfv_neu_tau001000um_M0400_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau001000um_M0400/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082005", 5, fnbase="miniaod"),
'mfv_neu_tau001000um_M0600_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau001000um_M0600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082006", 5, fnbase="miniaod"),
'mfv_neu_tau001000um_M0800_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau001000um_M0800/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082007", 5, fnbase="miniaod"),
'mfv_neu_tau001000um_M1200_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau001000um_M1200/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082008", 5, fnbase="miniaod"),
'mfv_neu_tau001000um_M1600_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau001000um_M1600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082009", 5, fnbase="miniaod"),
'mfv_neu_tau001000um_M3000_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau001000um_M3000/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082010", 5, fnbase="miniaod"),
'mfv_neu_tau010000um_M0400_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau010000um_M0400/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082011", 5, fnbase="miniaod"),
'mfv_neu_tau010000um_M0600_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau010000um_M0600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082012", 5, fnbase="miniaod"),
'mfv_neu_tau010000um_M0800_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau010000um_M0800/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082013", 5, fnbase="miniaod"),
'mfv_neu_tau010000um_M1200_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau010000um_M1200/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082014", 5, fnbase="miniaod"),
'mfv_neu_tau010000um_M1600_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau010000um_M1600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082015", 5, fnbase="miniaod"),
'mfv_neu_tau010000um_M3000_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau010000um_M3000/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082016", 5, fnbase="miniaod"),
'mfv_neu_tau030000um_M0400_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau030000um_M0400/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082017", 5, fnbase="miniaod"),
'mfv_neu_tau030000um_M0600_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau030000um_M0600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082018", 5, fnbase="miniaod"),
'mfv_neu_tau030000um_M0800_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau030000um_M0800/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082019", 5, fnbase="miniaod"),
'mfv_neu_tau030000um_M1200_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau030000um_M1200/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082020", 5, fnbase="miniaod"),
'mfv_neu_tau030000um_M1600_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau030000um_M1600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082021", 5, fnbase="miniaod"),
'mfv_neu_tau030000um_M3000_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau030000um_M3000/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082022", 5, fnbase="miniaod"),
'mfv_neu_tau100000um_M0400_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau100000um_M0400/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082023", 5, fnbase="miniaod"),
'mfv_neu_tau100000um_M0600_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau100000um_M0600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082024", 5, fnbase="miniaod"),
'mfv_neu_tau100000um_M0800_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau100000um_M0800/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082025", 5, fnbase="miniaod"),
'mfv_neu_tau100000um_M1200_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau100000um_M1200/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082026", 5, fnbase="miniaod"),
'mfv_neu_tau100000um_M1600_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau100000um_M1600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082027", 5, fnbase="miniaod"),
'mfv_neu_tau100000um_M3000_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau100000um_M3000/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082028", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau000100um_M0400_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau000100um_M0400/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082029", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau000100um_M0600_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau000100um_M0600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082030", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau000100um_M0800_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau000100um_M0800/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082031", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau000100um_M1200_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau000100um_M1200/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082032", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau000100um_M1600_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau000100um_M1600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082033", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau000100um_M3000_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau000100um_M3000/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082034", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau000300um_M0400_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau000300um_M0400/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082035", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau000300um_M0600_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau000300um_M0600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082036", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau000300um_M0800_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau000300um_M0800/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082037", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau000300um_M1200_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau000300um_M1200/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082038", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau000300um_M1600_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau000300um_M1600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082039", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau000300um_M3000_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau000300um_M3000/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082040", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau001000um_M0400_2017': (5, ['/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau001000um_M0400/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082041/0000/miniaod_%i.root' % i for i in chain(xrange(2), xrange(3,5))] + ['/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau001000um_M0400/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_095042/0000/miniaod_2.root']),
'mfv_stopdbardbar_tau001000um_M0600_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau001000um_M0600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082042", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau001000um_M0800_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau001000um_M0800/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082043", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau001000um_M1200_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau001000um_M1200/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082044", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau001000um_M1600_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau001000um_M1600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082045", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau001000um_M3000_2017': (5, ['/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau001000um_M3000/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082046/0000/miniaod_%i.root' % i for i in xrange(4)] + ['/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau001000um_M3000/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_145804/0000/miniaod_4.root']),
'mfv_stopdbardbar_tau010000um_M0400_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau010000um_M0400/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082047", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau010000um_M0600_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau010000um_M0600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082048", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau010000um_M0800_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau010000um_M0800/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082049", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau010000um_M1200_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau010000um_M1200/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082050", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau010000um_M1600_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau010000um_M1600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082051", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau010000um_M3000_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau010000um_M3000/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082052", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau030000um_M0400_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau030000um_M0400/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082053", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau030000um_M0600_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau030000um_M0600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082054", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau030000um_M0800_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau030000um_M0800/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082055", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau030000um_M1200_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau030000um_M1200/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082056", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau030000um_M1600_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau030000um_M1600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082057", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau030000um_M3000_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau030000um_M3000/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082058", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau100000um_M0400_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau100000um_M0400/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082059", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau100000um_M0600_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau100000um_M0600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082100", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau100000um_M0800_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau100000um_M0800/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082101", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau100000um_M1200_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau100000um_M1200/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082102", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau100000um_M1600_2017': (5, ['/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau100000um_M1600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_105124/0000/miniaod_0.root'] + ['/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau100000um_M1600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082103/0000/miniaod_%i.root' % i for i in xrange(1,5)]),
'mfv_stopdbardbar_tau100000um_M3000_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau100000um_M3000/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082104", 5, fnbase="miniaod"),
})


_add_ds("ntuplev21m", {
'qcdht0700_2017': _fromnum1("/store/user/tucker/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/NtupleV21m_2017/181031_190446", 16),
'qcdht1000_2017': _fromnum1("/store/user/tucker/QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8/NtupleV21m_2017/181031_190510", 31),
'qcdht1500_2017': _fromnum0("/store/user/tucker/QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8/NtupleV21m_2017/181031_143853", 63),
'qcdht2000_2017': _fromnum0("/store/user/tucker/QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/NtupleV21m_2017/181031_143854", 30),
'ttbar_2017': _fromnum0("/store/user/tucker/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleV21m_2017/181101_153920", 51),
'ttbarht0600_2017': (15+57, ["/store/user/tucker/TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV21m_recover_2017/181111_020458/0000/ntuple_%i.root" % i for i in xrange(1,16)] + ['/store/user/tucker/TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV21m_2017/181107_012022/0000/ntuple_%i.root' % i for i in chain(xrange(1,7), xrange(10,14), xrange(15,61), [8])]),
'ttbarht0800_2017': (42+37, ['/store/user/tucker/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV21m_recover_2017/181111_020531/0000/ntuple_%i.root' % i for i in chain(xrange(1,13), xrange(14,44))] + ['/store/user/tucker/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV21m_2017/181107_012041/0000/ntuple_%i.root' % i for i in chain(xrange(1,20), xrange(25,31), xrange(32,43), [21])]),
'ttbarht1200_2017': ( 9+31, ["/store/user/tucker/TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV21m_recover_2017/181111_020554/0000/ntuple_%i.root" % i for i in xrange(1,10)] + ['/store/user/tucker/TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV21m_2017/181107_012100/0000/ntuple_%i.root' % i for i in chain(xrange(1,10), xrange(11,33))]),
'ttbarht2500_2017': _fromnum1("/store/user/tucker/TTJets_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV21m_2017/181107_005843", 29),
'mfv_neu_tau000100um_M0400_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau000100um_M0400/NtupleV21m_RedoSigsWOEF_2017/181107_153848", 50),
'mfv_neu_tau000100um_M0600_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau000100um_M0600/NtupleV21m_RedoSigsWOEF_2017/181107_153849", 50),
'mfv_neu_tau000100um_M0800_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau000100um_M0800/NtupleV21m_RedoSigsWOEF_2017/181107_153850", 50),
'mfv_neu_tau000100um_M1200_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau000100um_M1200/NtupleV21m_RedoSigsWOEF_2017/181107_153851", 50),
'mfv_neu_tau000100um_M1600_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau000100um_M1600/NtupleV21m_RedoSigsWOEF_2017/181107_153852", 50),
'mfv_neu_tau000100um_M3000_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau000100um_M3000/NtupleV21m_RedoSigsWOEF_2017/181107_153853", 50),
'mfv_neu_tau000300um_M0400_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau000300um_M0400/NtupleV21m_RedoSigsWOEF_2017/181107_153854", 50),
'mfv_neu_tau000300um_M0600_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau000300um_M0600/NtupleV21m_RedoSigsWOEF_2017/181107_153855", 50),
'mfv_neu_tau000300um_M0800_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau000300um_M0800/NtupleV21m_RedoSigsWOEF_2017/181107_153856", 50),
'mfv_neu_tau000300um_M1200_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau000300um_M1200/NtupleV21m_RedoSigsWOEF_2017/181107_153857", 50),
'mfv_neu_tau000300um_M1600_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau000300um_M1600/NtupleV21m_RedoSigsWOEF_2017/181107_153858", 50),
'mfv_neu_tau000300um_M3000_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau000300um_M3000/NtupleV21m_RedoSigsWOEF_2017/181107_153859", 50),
'mfv_neu_tau001000um_M0400_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau001000um_M0400/NtupleV21m_RedoSigsWOEF_2017/181107_153900", 50),
'mfv_neu_tau001000um_M0600_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau001000um_M0600/NtupleV21m_RedoSigsWOEF_2017/181107_153901", 50),
'mfv_neu_tau001000um_M0800_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau001000um_M0800/NtupleV21m_RedoSigsWOEF_2017/181107_153902", 50),
'mfv_neu_tau001000um_M1200_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau001000um_M1200/NtupleV21m_RedoSigsWOEF_2017/181107_153903", 50),
'mfv_neu_tau001000um_M1600_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau001000um_M1600/NtupleV21m_RedoSigsWOEF_2017/181107_153904", 50),
'mfv_neu_tau001000um_M3000_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau001000um_M3000/NtupleV21m_RedoSigsWOEF_2017/181107_153905", 50),
'mfv_neu_tau010000um_M0400_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau010000um_M0400/NtupleV21m_RedoSigsWOEF_2017/181107_153906", 50),
'mfv_neu_tau010000um_M0600_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau010000um_M0600/NtupleV21m_RedoSigsWOEF_2017/181107_153907", 50),
'mfv_neu_tau010000um_M0800_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau010000um_M0800/NtupleV21m_RedoSigsWOEF_2017/181107_153908", 50),
'mfv_neu_tau010000um_M1200_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau010000um_M1200/NtupleV21m_RedoSigsWOEF_2017/181107_153909", 50),
'mfv_neu_tau010000um_M1600_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau010000um_M1600/NtupleV21m_RedoSigsWOEF_2017/181107_153910", 50),
'mfv_neu_tau010000um_M3000_2017': (50, ['/store/user/tucker/mfv_neu_cp2_tau010000um_M3000/NtupleV21m_RedoSigsWOEF_2017/181107_153911/0000/ntuple_%i.root' % i for i in chain(xrange(39), xrange(40,50))] + ['/store/user/tucker/mfv_neu_cp2_tau010000um_M3000/NtupleV21m_RedoSigsWOEF_2017/181108_074454/0000/ntuple_39.root']),
'mfv_neu_tau030000um_M0400_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau030000um_M0400/NtupleV21m_RedoSigsWOEF_2017/181107_153912", 50),
'mfv_neu_tau030000um_M0600_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau030000um_M0600/NtupleV21m_RedoSigsWOEF_2017/181107_153913", 50),
'mfv_neu_tau030000um_M0800_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau030000um_M0800/NtupleV21m_RedoSigsWOEF_2017/181107_153914", 50),
'mfv_neu_tau030000um_M1200_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau030000um_M1200/NtupleV21m_RedoSigsWOEF_2017/181107_153915", 50),
'mfv_neu_tau030000um_M1600_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau030000um_M1600/NtupleV21m_RedoSigsWOEF_2017/181107_153916", 50),
'mfv_neu_tau030000um_M3000_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau030000um_M3000/NtupleV21m_RedoSigsWOEF_2017/181107_153917", 50),
'mfv_neu_tau100000um_M0400_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau100000um_M0400/NtupleV21m_RedoSigsWOEF_2017/181107_153918", 50),
'mfv_neu_tau100000um_M0600_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau100000um_M0600/NtupleV21m_RedoSigsWOEF_2017/181107_153919", 50),
'mfv_neu_tau100000um_M0800_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau100000um_M0800/NtupleV21m_RedoSigsWOEF_2017/181107_153920", 50),
'mfv_neu_tau100000um_M1200_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau100000um_M1200/NtupleV21m_RedoSigsWOEF_2017/181107_153921", 50),
'mfv_neu_tau100000um_M1600_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau100000um_M1600/NtupleV21m_RedoSigsWOEF_2017/181107_153922", 50),
'mfv_neu_tau100000um_M3000_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau100000um_M3000/NtupleV21m_RedoSigsWOEF_2017/181107_153923", 50),
'mfv_stopdbardbar_tau000100um_M0400_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau000100um_M0400/NtupleV21m_RedoSigsWOEF_2017/181107_153924", 50),
'mfv_stopdbardbar_tau000100um_M0600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau000100um_M0600/NtupleV21m_RedoSigsWOEF_2017/181107_153925", 50),
'mfv_stopdbardbar_tau000100um_M0800_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau000100um_M0800/NtupleV21m_RedoSigsWOEF_2017/181107_153926", 50),
'mfv_stopdbardbar_tau000100um_M1200_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau000100um_M1200/NtupleV21m_RedoSigsWOEF_2017/181107_153927", 50),
'mfv_stopdbardbar_tau000100um_M1600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau000100um_M1600/NtupleV21m_RedoSigsWOEF_2017/181107_153928", 50),
'mfv_stopdbardbar_tau000100um_M3000_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau000100um_M3000/NtupleV21m_RedoSigsWOEF_2017/181107_153929", 50),
'mfv_stopdbardbar_tau000300um_M0400_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau000300um_M0400/NtupleV21m_RedoSigsWOEF_2017/181107_153930", 50),
'mfv_stopdbardbar_tau000300um_M0600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau000300um_M0600/NtupleV21m_RedoSigsWOEF_2017/181107_153931", 50),
'mfv_stopdbardbar_tau000300um_M0800_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau000300um_M0800/NtupleV21m_RedoSigsWOEF_2017/181107_153932", 50),
'mfv_stopdbardbar_tau000300um_M1200_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau000300um_M1200/NtupleV21m_RedoSigsWOEF_2017/181107_153933", 50),
'mfv_stopdbardbar_tau000300um_M1600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau000300um_M1600/NtupleV21m_RedoSigsWOEF_2017/181107_153934", 50),
'mfv_stopdbardbar_tau000300um_M3000_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau000300um_M3000/NtupleV21m_RedoSigsWOEF_2017/181107_153935", 50),
'mfv_stopdbardbar_tau001000um_M0400_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau001000um_M0400/NtupleV21m_RedoSigsWOEF_2017/181107_153936", 50),
'mfv_stopdbardbar_tau001000um_M0600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau001000um_M0600/NtupleV21m_RedoSigsWOEF_2017/181107_153937", 50),
'mfv_stopdbardbar_tau001000um_M0800_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau001000um_M0800/NtupleV21m_RedoSigsWOEF_2017/181107_153938", 50),
'mfv_stopdbardbar_tau001000um_M1200_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau001000um_M1200/NtupleV21m_RedoSigsWOEF_2017/181107_153939", 50),
'mfv_stopdbardbar_tau001000um_M1600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau001000um_M1600/NtupleV21m_RedoSigsWOEF_2017/181107_153940", 50),
'mfv_stopdbardbar_tau001000um_M3000_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau001000um_M3000/NtupleV21m_RedoSigsWOEF_2017/181107_153941", 50),
'mfv_stopdbardbar_tau010000um_M0400_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau010000um_M0400/NtupleV21m_RedoSigsWOEF_2017/181107_153942", 50),
'mfv_stopdbardbar_tau010000um_M0600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau010000um_M0600/NtupleV21m_RedoSigsWOEF_2017/181107_153943", 50),
'mfv_stopdbardbar_tau010000um_M0800_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau010000um_M0800/NtupleV21m_RedoSigsWOEF_2017/181107_153944", 50),
'mfv_stopdbardbar_tau010000um_M1200_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau010000um_M1200/NtupleV21m_RedoSigsWOEF_2017/181107_153945", 50),
'mfv_stopdbardbar_tau010000um_M1600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau010000um_M1600/NtupleV21m_RedoSigsWOEF_2017/181107_153946", 50),
'mfv_stopdbardbar_tau010000um_M3000_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau010000um_M3000/NtupleV21m_RedoSigsWOEF_2017/181107_153947", 50),
'mfv_stopdbardbar_tau030000um_M0400_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau030000um_M0400/NtupleV21m_RedoSigsWOEF_2017/181107_153948", 50),
'mfv_stopdbardbar_tau030000um_M0600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau030000um_M0600/NtupleV21m_RedoSigsWOEF_2017/181107_153949", 50),
'mfv_stopdbardbar_tau030000um_M0800_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau030000um_M0800/NtupleV21m_RedoSigsWOEF_2017/181107_153950", 50),
'mfv_stopdbardbar_tau030000um_M1200_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau030000um_M1200/NtupleV21m_RedoSigsWOEF_2017/181107_153951", 50),
'mfv_stopdbardbar_tau030000um_M1600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau030000um_M1600/NtupleV21m_RedoSigsWOEF_2017/181107_153952", 50),
'mfv_stopdbardbar_tau030000um_M3000_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau030000um_M3000/NtupleV21m_RedoSigsWOEF_2017/181107_153953", 50),
'mfv_stopdbardbar_tau100000um_M0400_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau100000um_M0400/NtupleV21m_RedoSigsWOEF_2017/181107_153954", 50),
'mfv_stopdbardbar_tau100000um_M0600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau100000um_M0600/NtupleV21m_RedoSigsWOEF_2017/181107_153955", 50),
'mfv_stopdbardbar_tau100000um_M0800_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau100000um_M0800/NtupleV21m_RedoSigsWOEF_2017/181107_153956", 50),
'mfv_stopdbardbar_tau100000um_M1200_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau100000um_M1200/NtupleV21m_RedoSigsWOEF_2017/181107_153957", 50),
'mfv_stopdbardbar_tau100000um_M1600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau100000um_M1600/NtupleV21m_RedoSigsWOEF_2017/181107_153958", 50),
'mfv_stopdbardbar_tau100000um_M3000_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau100000um_M3000/NtupleV21m_RedoSigsWOEF_2017/181107_153959", 50),
'JetHT2017B': _fromnum1("/store/user/tucker/JetHT/NtupleV21m_2017/181031_190619", 25),
'JetHT2017C': _fromnum1("/store/user/tucker/JetHT/NtupleV21m_2017/181031_190639", 38),
'JetHT2017D': _fromnum1("/store/user/tucker/JetHT/NtupleV21m_2017/181031_190658", 18),
'JetHT2017E': _fromnum1("/store/user/tucker/JetHT/NtupleV21m_2017/181031_190719", 42),
'JetHT2017F': _fromnum1("/store/user/tucker/JetHT/NtupleV21m_2017/181031_190738", 51),
'JetHT2018A': _fromnum1("/store/user/tucker/JetHT/NtupleV21m_ReReco_2018/181110_151715", 122),
'JetHT2018B': _fromnum1("/store/user/tucker/JetHT/NtupleV21m_ReReco_2018/181110_151729", 66),
'JetHT2018C': _fromnum1("/store/user/tucker/JetHT/NtupleV21m_2018/181128_173541", 55),
'JetHT2018D': _fromnum1("/store/user/tucker/JetHT/NtupleV21m_2018/181031_192438", 206),
})


_add_ds("ntuplev21m_ntkseeds", {
'qcdht0700_2017': _fromnum1("/store/user/tucker/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/NtupleV21m_NTkSeeds_2017/181101_203532", 16, fnbase="ntkseeds"),
'qcdht1000_2017': _fromnum1("/store/user/tucker/QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8/NtupleV21m_NTkSeeds_2017/181101_203559", 31, fnbase="ntkseeds"),
'qcdht1500_2017': _fromnum0("/store/user/tucker/QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8/NtupleV21m_NTkSeeds_2017/181101_153818", 63, fnbase="ntkseeds"),
'qcdht2000_2017': _fromnum0("/store/user/tucker/QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/NtupleV21m_NTkSeeds_2017/181101_153819", 30, fnbase="ntkseeds"),
'ttbar_2017': _fromnum0("/store/user/tucker/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleV21m_NTkSeeds_2017/181101_153817", 51, fnbase="ntkseeds"),
'ttbarht0600_2017': _join((217, ['/store/user/tucker/TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV21m_NTkSeeds_2017/181113_165019/0000/ntkseeds_%i.root' % i for i in chain(xrange(1,17), xrange(18,24), xrange(25,37), xrange(38,40), xrange(41,51), xrange(52,56), xrange(57,59), xrange(61,66), xrange(67,69), xrange(72,76), xrange(78,80), xrange(81,84), xrange(85,92), xrange(93,95), xrange(96,166), xrange(167,188), xrange(189,200), xrange(203,206), xrange(210,214), xrange(217,224), xrange(225,246), [70, 207, 215])]), (55, ['/store/user/tucker/TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV21m_NTkSeeds_recover_2017/181123_180324/0000/ntkseeds_%i.root' % i for i in chain(xrange(1,27), xrange(28,57))])),
'ttbarht0800_2017': _join((179, ['/store/user/tucker/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV21m_NTkSeeds_2017/181113_165041/0000/ntkseeds_%i.root' % i for i in chain(xrange(1,12), xrange(13,16), xrange(20,28), xrange(29,49), xrange(50,59), xrange(60,74), xrange(76,78), xrange(82,110), xrange(111,115), xrange(116,122), xrange(125,128), xrange(131,135), xrange(137,144), xrange(145,148), xrange(150,158), xrange(163,176), xrange(177,189), xrange(190,198), xrange(199,210), [17, 80, 129, 159, 161])]),(59, ['/store/user/tucker/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV21m_NTkSeeds_recover_2017/181123_180351/0000/ntkseeds_%i.root' % i for i in chain(xrange(1,4), xrange(5,61))])),
'ttbarht1200_2017': _join((96, ['/store/user/tucker/TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV21m_NTkSeeds_2017/181113_165100/0000/ntkseeds_%i.root' % i for i in chain(xrange(1,7), xrange(9,22), xrange(23,66), xrange(67,91), xrange(92,96), xrange(98,104))]),_fromnum1("/store/user/tucker/TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV21m_NTkSeeds_recover_2017/181123_180413", 14, fnbase="ntkseeds")),
'ttbarht2500_2017': _join((56, ['/store/user/tucker/TTJets_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV21m_NTkSeeds_2017/181113_165127/0000/ntkseeds_%i.root' % i for i in chain(xrange(1,6), xrange(11,62))]),(8, ['/store/user/tucker/TTJets_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV21m_NTkSeeds_recover_2017/181123_180430/0000/ntkseeds_%i.root' % i for i in chain(xrange(1,8), [9])])),
'JetHT2017B': _fromnum1("/store/user/tucker/JetHT/NtupleV21m_NTkSeeds_2017/181101_203624", 25, fnbase="ntkseeds"),
'JetHT2017C': _fromnum1("/store/user/tucker/JetHT/NtupleV21m_NTkSeeds_2017/181101_203710", 38, fnbase="ntkseeds"),
'JetHT2017D': _fromnum1("/store/user/tucker/JetHT/NtupleV21m_NTkSeeds_2017/181101_203730", 18, fnbase="ntkseeds"),
'JetHT2017E': _fromnum1("/store/user/tucker/JetHT/NtupleV21m_NTkSeeds_2017/181101_203749", 42, fnbase="ntkseeds"),
'JetHT2017F': _fromnum1("/store/user/tucker/JetHT/NtupleV21m_NTkSeeds_2017/181101_203815", 51, fnbase="ntkseeds"),
'JetHT2018A': _fromnum1("/store/user/tucker/JetHT/NtupleV21m_NTkSeeds_ReReco_2018/181110_155029", 122, fnbase="ntkseeds"),
'JetHT2018B': _fromnum1("/store/user/tucker/JetHT/NtupleV21m_NTkSeeds_ReReco_2018/181110_155044", 66, fnbase="ntkseeds"),

'JetHT2018D': _fromnum1("/store/user/tucker/JetHT/NtupleV21m_NTkSeeds_2018/181101_204401", 207, fnbase="ntkseeds"),
})


_add_ds("v0ntuplev21mv1", {
'qcdht0700_2017': _fromnum0("/store/user/tucker/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/HTFilteredV0NtupleV21mV1_2017/181123_220143", 6),
'qcdht1000_2017': _fromnum0("/store/user/tucker/QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8/HTFilteredV0NtupleV21mV1_2017/181123_220144", 11),
'qcdht1500_2017': _fromnum0("/store/user/tucker/QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8/HTFilteredV0NtupleV21mV1_2017/181123_220145", 21),
'qcdht2000_2017': _fromnum0("/store/user/tucker/QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/HTFilteredV0NtupleV21mV1_2017/181123_220146", 10),
'ttbar_2017': _fromnum0("/store/user/tucker/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/HTFilteredV0NtupleV21mV1_2017/181123_220138", 17),
'ttbarht0600_2017': _fromnum0("/store/user/tucker/TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/HTFilteredV0NtupleV21mV1_2017/181123_220139", 77),
'ttbarht0800_2017': _fromnum0("/store/user/tucker/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/HTFilteredV0NtupleV21mV1_2017/181123_220140", 65),
'ttbarht1200_2017': _fromnum0("/store/user/tucker/TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/HTFilteredV0NtupleV21mV1_2017/181123_220141", 31),
'ttbarht2500_2017': _fromnum0("/store/user/tucker/TTJets_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8/HTFilteredV0NtupleV21mV1_2017/181123_220142", 16),
'JetHT2017B': _fromnum1("/store/user/tucker/JetHT/V0NtupleV21mV1_full_2017/181124_025655", 25),
'JetHT2017C': _fromnum1("/store/user/tucker/JetHT/V0NtupleV21mV1_full_2017/181124_025711", 39),
'JetHT2017D': _fromnum1("/store/user/tucker/JetHT/V0NtupleV21mV1_full_2017/181124_025726", 18),
'JetHT2017E': _fromnum1("/store/user/tucker/JetHT/V0NtupleV21mV1_full_2017/181124_025741", 42),
'JetHT2017F': _fromnum1("/store/user/tucker/JetHT/V0NtupleV21mV1_full_2017/181124_025759", 51),
'JetHT2018A': _fromnum1("/store/user/tucker/JetHT/V0NtupleV21mV1_full_2018/181124_030337", 128),
'JetHT2018B': _fromnum1("/store/user/tucker/JetHT/V0NtupleV21mV1_full_2018/181124_030350", 70),
'JetHT2018C': _fromnum1("/store/user/tucker/JetHT/V0NtupleV21mV1_2018/181128_173812", 55),
'JetHT2018D2': _fromnum1("/store/user/tucker/JetHT/V0NtupleV21mV1_full_2018/181124_030326", 209),
})


_add_ds("ntuplev22m", {
'qcdht0700_2017': _fromnum0("/store/user/tucker/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/NtupleV22m_2017/181218_204713", 16),
'qcdht1000_2017': _fromnum1("/store/user/tucker/QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8/NtupleV22m_2017/181219_024439", 31),
'qcdht1500_2017': _fromnum0("/store/user/tucker/QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8/NtupleV22m_2017/181218_204714", 63),
'qcdht2000_2017': _fromnum0("/store/user/tucker/QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/NtupleV22m_2017/181218_204715", 30),
'ttbarht0600_2017': (468, ['/store/user/tucker/TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV22m_2017/181218_231737/0000/ntuple_125.root'] + ['/store/user/tucker/TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV22m_2017/181218_204709/0000/ntuple_%i.root' % i for i in chain(xrange(48), xrange(49,125), xrange(126,345), xrange(346,468))] + ['/store/user/tucker/TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV22m_2017/181218_231736/0000/ntuple_345.root'] + ['/store/user/tucker/TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV22m_2017/181218_233124/0000/ntuple_48.root']),
'ttbarht0800_2017': (389, ['/store/user/tucker/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV22m_2017/181222_165526/0000/ntuple_%i.root' % i for i in [283, 367]] + ['/store/user/tucker/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV22m_2017/181222_165534/0000/ntuple_%i.root' % i for i in [89, 361]] + ['/store/user/tucker/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV22m_2017/181218_204710/0000/ntuple_%i.root' % i for i in chain(xrange(89), xrange(90,283), xrange(284,361), xrange(362,367), xrange(368,389))]),
'ttbarht1200_2017': (180, ['/store/user/tucker/TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV22m_2017/181222_165803/0000/ntuple_169.root'] + ['/store/user/tucker/TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV22m_2017/181218_231739/0000/ntuple_89.root'] + ['/store/user/tucker/TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV22m_2017/181218_204711/0000/ntuple_%i.root' % i for i in chain(xrange(89), xrange(90,106), xrange(107,169), xrange(170,181))]),
'ttbarht2500_2017': (95, ['/store/user/tucker/TTJets_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV22m_2017/181218_231740/0000/ntuple_10.root'] + ['/store/user/tucker/TTJets_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV22m_2017/181218_204712/0000/ntuple_%i.root' % i for i in chain(xrange(10), xrange(11,95))]),
'mfv_neu_tau000100um_M0400_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau000100um_M0400/NtupleV22m_2017/181218_204716", 50),
'mfv_neu_tau000100um_M0600_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau000100um_M0600/NtupleV22m_2017/181218_204717", 50),
'mfv_neu_tau000100um_M0800_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau000100um_M0800/NtupleV22m_2017/181218_204718", 50),
'mfv_neu_tau000100um_M1200_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau000100um_M1200/NtupleV22m_2017/181218_204719", 50),
'mfv_neu_tau000100um_M1600_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau000100um_M1600/NtupleV22m_2017/181218_204720", 50),
'mfv_neu_tau000100um_M3000_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau000100um_M3000/NtupleV22m_2017/181218_204721", 50),
'mfv_neu_tau000300um_M0400_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau000300um_M0400/NtupleV22m_2017/181218_204722", 50),
'mfv_neu_tau000300um_M0600_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau000300um_M0600/NtupleV22m_2017/181218_204723", 50),
'mfv_neu_tau000300um_M0800_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau000300um_M0800/NtupleV22m_2017/181218_204724", 50),
'mfv_neu_tau000300um_M1200_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau000300um_M1200/NtupleV22m_2017/181218_204725", 50),
'mfv_neu_tau000300um_M1600_2017': (50, ['/store/user/tucker/mfv_neu_cp2_tau000300um_M1600/NtupleV22m_2017/181218_231741/0000/ntuple_38.root'] + ['/store/user/tucker/mfv_neu_cp2_tau000300um_M1600/NtupleV22m_2017/181218_204726/0000/ntuple_%i.root' % i for i in chain(xrange(38), xrange(39,50))]),
'mfv_neu_tau000300um_M3000_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau000300um_M3000/NtupleV22m_2017/181218_204727", 50),
'mfv_neu_tau001000um_M0400_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau001000um_M0400/NtupleV22m_2017/181218_204728", 50),
'mfv_neu_tau001000um_M0600_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau001000um_M0600/NtupleV22m_2017/181218_204729", 50),
'mfv_neu_tau001000um_M0800_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau001000um_M0800/NtupleV22m_2017/181218_204730", 50),
'mfv_neu_tau001000um_M1200_2017': (50, ['/store/user/tucker/mfv_neu_cp2_tau001000um_M1200/NtupleV22m_2017/181218_204731/0000/ntuple_%i.root' % i for i in chain(xrange(27), xrange(28,50))] + ['/store/user/tucker/mfv_neu_cp2_tau001000um_M1200/NtupleV22m_2017/181218_231741/0000/ntuple_27.root']),
'mfv_neu_tau001000um_M1600_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau001000um_M1600/NtupleV22m_2017/181218_204732", 50),
'mfv_neu_tau001000um_M3000_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau001000um_M3000/NtupleV22m_2017/181218_204733", 50),
'mfv_neu_tau010000um_M0400_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau010000um_M0400/NtupleV22m_2017/181218_204734", 50),
'mfv_neu_tau010000um_M0600_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau010000um_M0600/NtupleV22m_2017/181218_204735", 50),
'mfv_neu_tau010000um_M0800_2017': (50, ['/store/user/tucker/mfv_neu_cp2_tau010000um_M0800/NtupleV22m_2017/181218_204736/0000/ntuple_%i.root' % i for i in chain(xrange(10), xrange(11,50))] + ['/store/user/tucker/mfv_neu_cp2_tau010000um_M0800/NtupleV22m_2017/181218_231742/0000/ntuple_10.root']),
'mfv_neu_tau010000um_M1200_2017': (50, ['/store/user/tucker/mfv_neu_cp2_tau010000um_M1200/NtupleV22m_2017/181218_231743/0000/ntuple_0.root'] + ['/store/user/tucker/mfv_neu_cp2_tau010000um_M1200/NtupleV22m_2017/181218_204737/0000/ntuple_%i.root' % i for i in xrange(1,50)]),
'mfv_neu_tau010000um_M1600_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau010000um_M1600/NtupleV22m_2017/181218_204738", 50),
'mfv_neu_tau010000um_M3000_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau010000um_M3000/NtupleV22m_2017/181218_204739", 50),
'mfv_neu_tau030000um_M0400_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau030000um_M0400/NtupleV22m_2017/181218_204740", 50),
'mfv_neu_tau030000um_M0600_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau030000um_M0600/NtupleV22m_2017/181218_204741", 50),
'mfv_neu_tau030000um_M0800_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau030000um_M0800/NtupleV22m_2017/181218_204742", 50),
'mfv_neu_tau030000um_M1200_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau030000um_M1200/NtupleV22m_2017/181218_204743", 50),
'mfv_neu_tau030000um_M1600_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau030000um_M1600/NtupleV22m_2017/181218_204744", 50),
'mfv_neu_tau030000um_M3000_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau030000um_M3000/NtupleV22m_2017/181218_204745", 50),
'mfv_neu_tau100000um_M0400_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau100000um_M0400/NtupleV22m_2017/181218_204746", 50),
'mfv_neu_tau100000um_M0600_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau100000um_M0600/NtupleV22m_2017/181218_204747", 50),
'mfv_neu_tau100000um_M0800_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau100000um_M0800/NtupleV22m_2017/181218_204748", 50),
'mfv_neu_tau100000um_M1200_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau100000um_M1200/NtupleV22m_2017/181218_204749", 50),
'mfv_neu_tau100000um_M1600_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau100000um_M1600/NtupleV22m_2017/181218_204750", 50),
'mfv_neu_tau100000um_M3000_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau100000um_M3000/NtupleV22m_2017/181218_204751", 50),
'mfv_stopdbardbar_tau000100um_M0400_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau000100um_M0400/NtupleV22m_2017/181218_204752", 50),
'mfv_stopdbardbar_tau000100um_M0600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau000100um_M0600/NtupleV22m_2017/181218_204753", 50),
'mfv_stopdbardbar_tau000100um_M0800_2017': (50, ['/store/user/tucker/mfv_stopdbardbar_cp2_tau000100um_M0800/NtupleV22m_2017/181218_204754/0000/ntuple_%i.root' % i for i in chain(xrange(10), xrange(11,14), xrange(15,50))] + ['/store/user/tucker/mfv_stopdbardbar_cp2_tau000100um_M0800/NtupleV22m_2017/181218_231745/0000/ntuple_%i.root' % i for i in [10, 14]]),
'mfv_stopdbardbar_tau000100um_M1200_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau000100um_M1200/NtupleV22m_2017/181218_204755", 50),
'mfv_stopdbardbar_tau000100um_M1600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau000100um_M1600/NtupleV22m_2017/181218_204756", 50),
'mfv_stopdbardbar_tau000100um_M3000_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau000100um_M3000/NtupleV22m_2017/181218_204757", 50),
'mfv_stopdbardbar_tau000300um_M0400_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau000300um_M0400/NtupleV22m_2017/181218_204758", 50),
'mfv_stopdbardbar_tau000300um_M0600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau000300um_M0600/NtupleV22m_2017/181218_204759", 50),
'mfv_stopdbardbar_tau000300um_M0800_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau000300um_M0800/NtupleV22m_2017/181218_204800", 50),
'mfv_stopdbardbar_tau000300um_M1200_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau000300um_M1200/NtupleV22m_2017/181218_204801", 50),
'mfv_stopdbardbar_tau000300um_M1600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau000300um_M1600/NtupleV22m_2017/181218_204802", 50),
'mfv_stopdbardbar_tau000300um_M3000_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau000300um_M3000/NtupleV22m_2017/181218_204803", 50),
'mfv_stopdbardbar_tau001000um_M0400_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau001000um_M0400/NtupleV22m_2017/181218_204804", 50),
'mfv_stopdbardbar_tau001000um_M0600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau001000um_M0600/NtupleV22m_2017/181218_204805", 50),
'mfv_stopdbardbar_tau001000um_M0800_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau001000um_M0800/NtupleV22m_2017/181218_204806", 50),
'mfv_stopdbardbar_tau001000um_M1200_2017': (50, ['/store/user/tucker/mfv_stopdbardbar_cp2_tau001000um_M1200/NtupleV22m_2017/181218_231745/0000/ntuple_38.root'] + ['/store/user/tucker/mfv_stopdbardbar_cp2_tau001000um_M1200/NtupleV22m_2017/181218_204807/0000/ntuple_%i.root' % i for i in chain(xrange(38), xrange(39,50))]),
'mfv_stopdbardbar_tau001000um_M1600_2017': (50, ['/store/user/tucker/mfv_stopdbardbar_cp2_tau001000um_M1600/NtupleV22m_2017/181218_204808/0000/ntuple_%i.root' % i for i in chain(xrange(38), xrange(39,50))] + ['/store/user/tucker/mfv_stopdbardbar_cp2_tau001000um_M1600/NtupleV22m_2017/181218_231746/0000/ntuple_38.root']),
'mfv_stopdbardbar_tau001000um_M3000_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau001000um_M3000/NtupleV22m_2017/181218_204809", 50),
'mfv_stopdbardbar_tau010000um_M0400_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau010000um_M0400/NtupleV22m_2017/181218_204810", 50),
'mfv_stopdbardbar_tau010000um_M0600_2017': (50, ['/store/user/tucker/mfv_stopdbardbar_cp2_tau010000um_M0600/NtupleV22m_2017/181218_204811/0000/ntuple_%i.root' % i for i in chain(xrange(16), xrange(17,25), xrange(26,50))] + ['/store/user/tucker/mfv_stopdbardbar_cp2_tau010000um_M0600/NtupleV22m_2017/181218_231747/0000/ntuple_%i.root' % i for i in [16, 25]]),
'mfv_stopdbardbar_tau010000um_M0800_2017': (50, ['/store/user/tucker/mfv_stopdbardbar_cp2_tau010000um_M0800/NtupleV22m_2017/181218_231748/0000/ntuple_18.root'] + ['/store/user/tucker/mfv_stopdbardbar_cp2_tau010000um_M0800/NtupleV22m_2017/181218_204812/0000/ntuple_%i.root' % i for i in chain(xrange(18), xrange(19,50))]),
'mfv_stopdbardbar_tau010000um_M1200_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau010000um_M1200/NtupleV22m_2017/181218_204813", 50),
'mfv_stopdbardbar_tau010000um_M1600_2017': (50, ['/store/user/tucker/mfv_stopdbardbar_cp2_tau010000um_M1600/NtupleV22m_2017/181218_231749/0000/ntuple_26.root'] + ['/store/user/tucker/mfv_stopdbardbar_cp2_tau010000um_M1600/NtupleV22m_2017/181218_204814/0000/ntuple_%i.root' % i for i in chain(xrange(26), xrange(27,50))]),
'mfv_stopdbardbar_tau010000um_M3000_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau010000um_M3000/NtupleV22m_2017/181218_204815", 50),
'mfv_stopdbardbar_tau030000um_M0400_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau030000um_M0400/NtupleV22m_2017/181218_204816", 50),
'mfv_stopdbardbar_tau030000um_M0600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau030000um_M0600/NtupleV22m_2017/181218_204817", 50),
'mfv_stopdbardbar_tau030000um_M0800_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau030000um_M0800/NtupleV22m_2017/181218_204818", 50),
'mfv_stopdbardbar_tau030000um_M1200_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau030000um_M1200/NtupleV22m_2017/181218_204819", 50),
'mfv_stopdbardbar_tau030000um_M1600_2017': (50, ['/store/user/tucker/mfv_stopdbardbar_cp2_tau030000um_M1600/NtupleV22m_2017/181218_204820/0000/ntuple_%i.root' % i for i in chain(xrange(37), xrange(38,50))] + ['/store/user/tucker/mfv_stopdbardbar_cp2_tau030000um_M1600/NtupleV22m_2017/181218_231749/0000/ntuple_37.root']),
'mfv_stopdbardbar_tau030000um_M3000_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau030000um_M3000/NtupleV22m_2017/181218_204821", 50),
'mfv_stopdbardbar_tau100000um_M0400_2017': (50, ['/store/user/tucker/mfv_stopdbardbar_cp2_tau100000um_M0400/NtupleV22m_2017/181218_231750/0000/ntuple_10.root'] + ['/store/user/tucker/mfv_stopdbardbar_cp2_tau100000um_M0400/NtupleV22m_2017/181218_204822/0000/ntuple_%i.root' % i for i in chain(xrange(10), xrange(11,50))]),
'mfv_stopdbardbar_tau100000um_M0600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau100000um_M0600/NtupleV22m_2017/181218_204823", 50),
'mfv_stopdbardbar_tau100000um_M0800_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau100000um_M0800/NtupleV22m_2017/181218_204824", 50),
'mfv_stopdbardbar_tau100000um_M1200_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau100000um_M1200/NtupleV22m_2017/181218_204825", 50),
'mfv_stopdbardbar_tau100000um_M1600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau100000um_M1600/NtupleV22m_2017/181218_204826", 50),
'mfv_stopdbardbar_tau100000um_M3000_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau100000um_M3000/NtupleV22m_2017/181218_204827", 50),
'JetHT2017B': _fromnum1("/store/user/tucker/JetHT/NtupleV22m_2017/181219_024457", 25),
'JetHT2017C': _fromnum1("/store/user/tucker/JetHT/NtupleV22m_2017/181219_024516", 38),
'JetHT2017D': _fromnum1("/store/user/tucker/JetHT/NtupleV22m_2017/181219_024618", 18),
'JetHT2017E': _fromnum1("/store/user/tucker/JetHT/NtupleV22m_2017/181219_024646", 41),
'JetHT2017F': _fromnum1("/store/user/tucker/JetHT/NtupleV22m_2017/181219_024707", 51),
'JetHT2018A': _fromnum1("/store/user/tucker/JetHT/NtupleV22m_2018/181219_024606", 121),
'JetHT2018B': _fromnum1("/store/user/tucker/JetHT/NtupleV22m_2018/181219_024626", 64),
'JetHT2018C': _fromnum1("/store/user/tucker/JetHT/NtupleV22m_2018/181219_024642", 50),
'JetHT2018D': _fromnum1("/store/user/tucker/JetHT/NtupleV22m_2018/181219_024658", 189),
})


_add_ds("ntuplev22m_ntkseeds", {
'qcdht0700_2017': _fromnum0("/store/user/tucker/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/NtupleV22m_NTkSeeds_2017/181218_205150", 16, fnbase="ntkseeds"),
'qcdht1000_2017': _fromnum1("/store/user/tucker/QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8/NtupleV22m_NTkSeeds_2017/181219_024941", 31, fnbase="ntkseeds"),
'qcdht1500_2017': _fromnum0("/store/user/tucker/QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8/NtupleV22m_NTkSeeds_2017/181218_205151", 63, fnbase="ntkseeds"),
'qcdht2000_2017': _fromnum0("/store/user/tucker/QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/NtupleV22m_NTkSeeds_2017/181218_205152", 30, fnbase="ntkseeds"),
'ttbarht0600_2017': (468, ['/store/user/tucker/TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV22m_NTkSeeds_2017/181222_105046/0000/ntkseeds_%i.root' % i for i in [78, 271]] + ['/store/user/tucker/TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV22m_NTkSeeds_2017/181218_205146/0000/ntkseeds_%i.root' % i for i in chain(xrange(27), xrange(28,78), xrange(79,141), xrange(142,152), xrange(153,191), xrange(192,271), xrange(272,277), xrange(278,468))] + ['/store/user/tucker/TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV22m_NTkSeeds_2017/181222_105047/0000/ntkseeds_%i.root' % i for i in [191, 277]] + ['/store/user/tucker/TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV22m_NTkSeeds_2017/181222_165925/0000/ntkseeds_141.root'] + ['/store/user/tucker/TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV22m_NTkSeeds_2017/181218_231752/0000/ntkseeds_%i.root' % i for i in [27, 152]]),
'ttbarht0800_2017': (388, ['/store/user/tucker/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV22m_NTkSeeds_2017/181222_170647/0000/ntkseeds_%i.root' % i for i in [283, 367]] + ['/store/user/tucker/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV22m_NTkSeeds_2017/181222_170212/0000/ntkseeds_%i.root' % i for i in [243, 282]] + ['/store/user/tucker/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV22m_NTkSeeds_2017/181218_205147/0000/ntkseeds_%i.root' % i for i in chain(xrange(88), xrange(89,243), xrange(244,253), xrange(254,256), xrange(257,282), xrange(284,316), xrange(317,367), xrange(368,389))] + ['/store/user/tucker/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV22m_NTkSeeds_2017/181218_231753/0000/ntkseeds_88.root'] + ['/store/user/tucker/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV22m_NTkSeeds_2017/181222_105051/0000/ntkseeds_256.root'] + ['/store/user/tucker/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV22m_NTkSeeds_2017/181222_105048/0000/ntkseeds_316.root']),
'ttbarht1200_2017': (181, ['/store/user/tucker/TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV22m_NTkSeeds_2017/181222_165945/0000/ntkseeds_173.root'] + ['/store/user/tucker/TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV22m_NTkSeeds_2017/181218_231754/0000/ntkseeds_76.root'] + ['/store/user/tucker/TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV22m_NTkSeeds_2017/181218_205148/0000/ntkseeds_%i.root' % i for i in chain(xrange(76), xrange(77,169), xrange(170,173), xrange(174,181))] + ['/store/user/tucker/TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV22m_NTkSeeds_2017/181222_170140/0000/ntkseeds_169.root']),
'ttbarht2500_2017': (95, ['/store/user/tucker/TTJets_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV22m_NTkSeeds_2017/181222_105054/0000/ntkseeds_75.root'] + ['/store/user/tucker/TTJets_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV22m_NTkSeeds_2017/181222_165933/0000/ntkseeds_73.root'] + ['/store/user/tucker/TTJets_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV22m_NTkSeeds_2017/181218_205149/0000/ntkseeds_%i.root' % i for i in chain(xrange(25), xrange(26,37), xrange(38,73), xrange(76,95), [74])] + ['/store/user/tucker/TTJets_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV22m_NTkSeeds_2017/181218_231755/0000/ntkseeds_%i.root' % i for i in [25, 37]]),
'JetHT2017B': _fromnum1("/store/user/tucker/JetHT/NtupleV22m_NTkSeeds_2017/181219_025001", 25, fnbase="ntkseeds"),
'JetHT2017C': _fromnum1("/store/user/tucker/JetHT/NtupleV22m_NTkSeeds_2017/181219_025025", 38, fnbase="ntkseeds"),
'JetHT2017D': _fromnum1("/store/user/tucker/JetHT/NtupleV22m_NTkSeeds_2017/181219_025054", 18, fnbase="ntkseeds"),
'JetHT2017E': _fromnum1("/store/user/tucker/JetHT/NtupleV22m_NTkSeeds_2017/181219_025120", 41, fnbase="ntkseeds"),
'JetHT2017F': (50+9, ['/store/user/tucker/JetHT/NtupleV22m_NTkSeeds_2017/181219_025144/0000/ntkseeds_%i.root' % i for i in chain(xrange(1,33), xrange(34,52))] + ["/store/user/tucker/JetHT/NtupleV22m_NTkSeeds_recover_2017/181227_165342/0000/ntkseeds_%i.root" % i for i in xrange(1,10)]),
'JetHT2018A': _fromnum1("/store/user/tucker/JetHT/NtupleV22m_NTkSeeds_2018/181219_024948", 121, fnbase="ntkseeds"),
'JetHT2018B': _fromnum1("/store/user/tucker/JetHT/NtupleV22m_NTkSeeds_2018/181219_025004", 64, fnbase="ntkseeds"),
'JetHT2018C': (49+8+2, ['/store/user/tucker/JetHT/NtupleV22m_NTkSeeds_2018/181219_025019/0000/ntkseeds_%i.root' % i for i in chain(xrange(1,25), xrange(26,51))] + ['/store/user/tucker/JetHT/NtupleV22m_NTkSeeds_recover_2018/181227_165411/0000/ntkseeds_%i.root' % i for i in chain(xrange(3,10), [1])] + ['/store/user/tucker/JetHT/NtupleV22m_NTkSeeds_recover2_2018/190102_210036/0000/ntkseeds_%i.root' % i for i in [1, 3]]),
'JetHT2018D': _fromnum1("/store/user/tucker/JetHT/NtupleV22m_NTkSeeds_2018/181219_025037", 189, fnbase="ntkseeds"),
})


################################################################################

if __name__ == '__main__':
    import sys, re

    def _printlist(l):
        for x in l:
            print x

    def _args(x, *names):
        n = len(names)
        i = sys.argv.index(x)
        if len(sys.argv) < i+n+1 or sys.argv[i+1] in ('-h','--help','help'):
            sys.exit('usage: %s %s %s' % (sys.argv[0], x, ' '.join(names)))
        return tuple(sys.argv[i+j] for j in xrange(1,n+1))
    def _arg(x,name):
        return _args(x,name)[0]

    if 'enc' in sys.argv:
        dataset, sample, listfn = _args('enc', 'dataset','sample','listfn')
        fns = [x.strip() for x in open(listfn).read().split('\n') if x.strip()]
        n = len(fns)
        print '# %s, %s, %i files' % (sample, dataset, n)
        print '_add(%r)' % _enc({(sample,dataset):(n,fns)})

    elif 'testfiles' in sys.argv:
        dataset, sample = _args('testfiles', 'dataset','sample')
        is_ntuple = dataset.startswith('ntuple')
        from JMTucker.Tools.ROOTTools import ROOT
        print sample, dataset
        nev, nev2 = 0, 0
        def get_n(f,p):
            try:
                return f.Get(p).GetEntries()
            except ReferenceError:
                return 1e99
        for fn in get(sample, dataset)[1]:
            n = get_n(ROOT.TFile.Open('root://cmseos.fnal.gov/' + fn), 'Events')
            nev += n
            if is_ntuple:
                n2 = get_n(ROOT.TFile.Open('root://cmseos.fnal.gov/' + fn.replace('ntuple', 'vertex_histos')), 'mfvVertices/h_n_all_tracks')
                nev2 += n2
                print fn, n, n2
            else:
                print fn, n
        print 'total:', nev, 'events',
        if is_ntuple:
            print nev2, 'in vertex_histos h_n_all_tracks',
        print

    elif 'forcopy' in sys.argv:
        dataset, sample = _args('forcopy', 'dataset','sample')
        if not has(sample, dataset):
            raise KeyError('no key sample = %s dataset = %s' % (sample, dataset))
        print sample, dataset
        from JMTucker.Tools import eos
        out_fn = '%s_%s' % (sample, dataset)
        out_f = open(out_fn, 'wt')
        out_f.write('copy\n')
        for fn in get(sample, dataset)[1]:
            md5sum = eos.md5sum(fn)
            x = '%s  %s\n' % (md5sum, fn)
            out_f.write(x)
            print x,
        out_f.close()

    elif 'fordelete' in sys.argv:
        dataset, sample = _args('fordelete', 'dataset','sample')
        if not has(sample, dataset):
            raise KeyError('no key sample = %s dataset = %s' % (sample, dataset))
        print sample, dataset
        from JMTucker.Tools import eos
        out_fn = '%s_%s' % (sample, dataset)
        out_f = open(out_fn, 'wt')
        out_f.write('delete\n%s\n' % '\n'.join(get(sample, dataset)[1]))
        out_f.close()

    elif 'dump' in sys.argv:
        dump()

    elif 'summary' in sys.argv:
        summary()

    elif 'datasets' in sys.argv:
        _printlist(sorted(set(ds for _, ds in _d.keys())))

    elif 'samples' in sys.argv:
        _printlist(sorted(set(name for name, ds in _d.keys() if ds == _arg('samples', 'dataset'))))

    elif 'files' in sys.argv:
        dataset, sample = _args('files', 'dataset','sample')
        _printlist(sorted(get(sample, dataset)[1]))

    elif 'allfiles' in sys.argv:
        _printlist(sorted(allfiles()))

    elif 'otherfiles' in sys.argv:
        list_fn = _arg('otherfiles', 'list_fn')
        other_fns = set()
        for line in open(list_fn):
            line = line.strip()
            if line.endswith('.root'):
                assert '/store' in line
                other_fns.add(line.replace('/eos/uscms', ''))
        all_fns = set(allfiles())
        print 'root files in %s not in SampleFiles:' % list_fn
        _printlist(sorted(other_fns - all_fns))
        print 'root files in SampleFiles not in %s:' % list_fn
        _printlist(sorted(all_fns - other_fns))

    elif 'filematch' in sys.argv:
        pattern = _arg('filematch', 'pattern')
        for (sample, dataset), (_, fns) in _d.iteritems():
            for fn in fns:
                if fnmatch(fn, pattern):
                    print sample, dataset, fn

    elif 'dirs' in sys.argv:
        dataset, sample = _args('dirs', 'dataset','sample')
        fns = get(sample, dataset)[1]
        path_re = re.compile(r'(/store.*/\d{6}_\d{6})/')
        _printlist(sorted(set(path_re.search(fn).group(1) for fn in fns)))
        # for x in ttbar qcdht0700 qcdht1000 qcdht1500 qcdht2000 wjetstolnu dyjetstollM10 dyjetstollM50 qcdmupt15 ; echo $x $(eosdu $(samplefiles dirs  ntuplev18m ${x}_2017) )

    elif 'whosummary' in sys.argv:
        whosummary = defaultdict(list)
        for k in _d:
            users = who(*k)
            if users:
                whosummary[users].append(k)
        print 'by user(s):'
        for users, dses in whosummary.iteritems():
            dses.sort()
            print ' + '.join(users)
            for ds in dses:
                print '    ', ds

    elif 'who' in sys.argv:
        dataset, sample = _args('who', 'dataset','sample')
        print ' + '.join(who(sample, dataset))

    elif 'sync' in sys.argv:
        from JMTucker.Tools import Samples
        in_sf_not_s = []
        in_s_not_sf = []

        for k in _d.iterkeys():
            name, ds = k
            if not hasattr(Samples, name) or not getattr(Samples, name).has_dataset(ds):
                in_sf_not_s.append(k)

        for s in Samples.registry.all():
            for ds in s.datasets:
                k = s.name, ds
                if not _d.has_key(k):
                    in_s_not_sf.append(k)

        print '%-45s %25s %10s' % ('in SampleFiles but not Samples:', '', 'enced?')
        for k in sorted(in_sf_not_s):
            name, ds = k
            print '%-45s %25s %10i' % (name, ds, _added_from_enc.get(k, -1))
        print
        print '%-45s %25s' % ('in Samples but not SampleFiles:', '')
        for k in sorted(in_s_not_sf):
            print '%-45s %25s' % k

    else:
        sys.exit('did not understand argv %r' % sys.argv)
