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

_removed = [
    (('qcdht0700_2017', 'miniaod'), '/store/mc/RunIIFall17MiniAODv2/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/10000/767F174C-3343-E811-A5F5-0025905A60A6.root'),
    (('qcdht0700_2017', 'miniaod'), '/store/mc/RunIIFall17MiniAODv2/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/40000/8E6AE107-6A42-E811-8422-0CC47A4C8E0E.root'),
    (('qcdht1500_2017', 'miniaod'), '/store/mc/RunIIFall17MiniAODv2/QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/10000/58077132-935C-E811-85A0-0CC47A4D7666.root'),
    (('qcdht0700_2018', 'miniaod'), '/store/mc/RunIIAutumn18MiniAOD/QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/102X_upgrade2018_realistic_v15-v1/60000/5AC8C151-EDC5-424C-ADA1-34CCAF24428E.root'),
    (('qcdht0700_2018', 'miniaod'), '/store/mc/RunIIAutumn18MiniAOD/QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/102X_upgrade2018_realistic_v15-v1/270000/ECBC623B-15F9-FF41-94D2-1673DF22A595.root'),
    (('qcdht0700_2018', 'miniaod'), '/store/mc/RunIIAutumn18MiniAOD/QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/102X_upgrade2018_realistic_v15-v1/20000/F23C4EF6-BC50-9748-B132-523B7F19F5E1.root'),
    (('qcdht1000_2018', 'miniaod'), '/store/mc/RunIIAutumn18MiniAOD/QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/102X_upgrade2018_realistic_v15-v1/120000/8F138429-3D58-5440-9FBE-4E4ABAF5A6A7.root'),
    (('qcdht1000_2018', 'miniaod'), '/store/mc/RunIIAutumn18MiniAOD/QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/102X_upgrade2018_realistic_v15-v1/120000/BAA789CF-E98B-9744-842C-C34D221F58C4.root'),
    (('qcdht1000_2018', 'miniaod'), '/store/mc/RunIIAutumn18MiniAOD/QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/102X_upgrade2018_realistic_v15-v1/120000/D2359D81-EB07-8A46-8DBA-7D4DCA14F6F4.root'),
    (('qcdht1000_2018', 'miniaod'), '/store/mc/RunIIAutumn18MiniAOD/QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/102X_upgrade2018_realistic_v15-v1/80000/643EC53B-D428-FB4B-A932-B199085745A7.root'),
    ]
for (name,ds),fn in _removed:
    _remove_file(name, ds, fn)

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


_add_ds("ntuplev23m", {
'qcdht0700_2017': (16, ['/store/user/wsun/croncopyeos/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/NtupleV23m_2017/190218_014828/0000/ntuple_%i.root' % i for i in chain(xrange(4,8), [14])] + ['/store/user/wsun/croncopyeos/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/NtupleV23m_2017/190217_090223/0000/ntuple_%i.root' % i for i in chain(xrange(4), xrange(8,14), [15])]),
'qcdht1000_2017': _fromnum1("/store/user/wsun/croncopyeos/QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8/NtupleV23m_2017/190218_155129", 31),
'qcdht1500_2017': (63, ['/store/user/wsun/croncopyeos/QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8/NtupleV23m_2017/190217_090224/0000/ntuple_%i.root' % i for i in chain(xrange(40), xrange(41,63))] + ['/store/user/wsun/croncopyeos/QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8/NtupleV23m_2017/190218_014829/0000/ntuple_40.root']),
'qcdht2000_2017': (30, ['/store/user/wsun/croncopyeos/QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/NtupleV23m_2017/190218_014831/0000/ntuple_29.root'] + ['/store/user/wsun/croncopyeos/QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/NtupleV23m_2017/190217_090225/0000/ntuple_%i.root' % i for i in xrange(29)]),
'ttbarht0600_2017': _fromnum0("/store/user/wsun/croncopyeos/TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV23m_2017/190217_090219", 468),
'ttbarht0800_2017': _fromnum0("/store/user/wsun/croncopyeos/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV23m_2017/190217_090220", 388),
'ttbarht1200_2017': _fromnum0("/store/user/wsun/croncopyeos/TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV23m_2017/190217_090221", 180),
'ttbarht2500_2017': _fromnum0("/store/user/wsun/croncopyeos/TTJets_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV23m_2017/190217_090222", 95),
'mfv_neu_tau000100um_M0400_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau000100um_M0400/NtupleV23m_2017/190217_090226", 50),
'mfv_neu_tau000100um_M0600_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau000100um_M0600/NtupleV23m_2017/190217_090227", 50),
'mfv_neu_tau000100um_M0800_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau000100um_M0800/NtupleV23m_2017/190217_090228", 50),
'mfv_neu_tau000100um_M1200_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau000100um_M1200/NtupleV23m_2017/190217_090229", 50),
'mfv_neu_tau000100um_M1600_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau000100um_M1600/NtupleV23m_2017/190217_090230", 50),
'mfv_neu_tau000100um_M3000_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau000100um_M3000/NtupleV23m_2017/190217_090231", 50),
'mfv_neu_tau000300um_M0400_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau000300um_M0400/NtupleV23m_2017/190217_090232", 50),
'mfv_neu_tau000300um_M0600_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau000300um_M0600/NtupleV23m_2017/190217_090233", 50),
'mfv_neu_tau000300um_M0800_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau000300um_M0800/NtupleV23m_2017/190217_090234", 50),
'mfv_neu_tau000300um_M1200_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau000300um_M1200/NtupleV23m_2017/190217_090235", 50),
'mfv_neu_tau000300um_M1600_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau000300um_M1600/NtupleV23m_2017/190217_090236", 50),
'mfv_neu_tau000300um_M3000_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau000300um_M3000/NtupleV23m_2017/190217_090237", 50),
'mfv_neu_tau001000um_M0400_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau001000um_M0400/NtupleV23m_2017/190217_090238", 50),
'mfv_neu_tau001000um_M0600_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau001000um_M0600/NtupleV23m_2017/190217_090239", 50),
'mfv_neu_tau001000um_M0800_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau001000um_M0800/NtupleV23m_2017/190217_090240", 50),
'mfv_neu_tau001000um_M1200_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau001000um_M1200/NtupleV23m_2017/190217_090241", 50),
'mfv_neu_tau001000um_M1600_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau001000um_M1600/NtupleV23m_2017/190217_090242", 50),
'mfv_neu_tau001000um_M3000_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau001000um_M3000/NtupleV23m_2017/190217_090243", 50),
'mfv_neu_tau010000um_M0400_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau010000um_M0400/NtupleV23m_2017/190217_090244", 50),
'mfv_neu_tau010000um_M0600_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau010000um_M0600/NtupleV23m_2017/190217_090245", 50),
'mfv_neu_tau010000um_M0800_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau010000um_M0800/NtupleV23m_2017/190217_090246", 50),
'mfv_neu_tau010000um_M1200_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau010000um_M1200/NtupleV23m_2017/190217_090247", 50),
'mfv_neu_tau010000um_M1600_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau010000um_M1600/NtupleV23m_2017/190217_090248", 50),
'mfv_neu_tau010000um_M3000_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau010000um_M3000/NtupleV23m_2017/190217_090249", 50),
'mfv_neu_tau030000um_M0400_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau030000um_M0400/NtupleV23m_2017/190217_090250", 50),
'mfv_neu_tau030000um_M0600_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau030000um_M0600/NtupleV23m_2017/190217_090251", 50),
'mfv_neu_tau030000um_M0800_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau030000um_M0800/NtupleV23m_2017/190217_090252", 50),
'mfv_neu_tau030000um_M1200_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau030000um_M1200/NtupleV23m_2017/190217_090253", 50),
'mfv_neu_tau030000um_M1600_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau030000um_M1600/NtupleV23m_2017/190217_090254", 50),
'mfv_neu_tau030000um_M3000_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau030000um_M3000/NtupleV23m_2017/190217_090255", 50),
'mfv_neu_tau100000um_M0400_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau100000um_M0400/NtupleV23m_2017/190217_090256", 50),
'mfv_neu_tau100000um_M0600_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau100000um_M0600/NtupleV23m_2017/190217_090257", 50),
'mfv_neu_tau100000um_M0800_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau100000um_M0800/NtupleV23m_2017/190217_090258", 50),
'mfv_neu_tau100000um_M1200_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau100000um_M1200/NtupleV23m_2017/190217_090259", 50),
'mfv_neu_tau100000um_M1600_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau100000um_M1600/NtupleV23m_2017/190217_090300", 50),
'mfv_neu_tau100000um_M3000_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_neu_cp2_tau100000um_M3000/NtupleV23m_2017/190217_090301", 50),
'mfv_stopdbardbar_tau000100um_M0400_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau000100um_M0400/NtupleV23m_2017/190217_090302", 50),
'mfv_stopdbardbar_tau000100um_M0600_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau000100um_M0600/NtupleV23m_2017/190217_090303", 50),
'mfv_stopdbardbar_tau000100um_M0800_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau000100um_M0800/NtupleV23m_2017/190217_090304", 50),
'mfv_stopdbardbar_tau000100um_M1200_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau000100um_M1200/NtupleV23m_2017/190217_090305", 50),
'mfv_stopdbardbar_tau000100um_M1600_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau000100um_M1600/NtupleV23m_2017/190217_090306", 50),
'mfv_stopdbardbar_tau000100um_M3000_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau000100um_M3000/NtupleV23m_2017/190217_090307", 50),
'mfv_stopdbardbar_tau000300um_M0400_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau000300um_M0400/NtupleV23m_2017/190217_090308", 50),
'mfv_stopdbardbar_tau000300um_M0600_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau000300um_M0600/NtupleV23m_2017/190217_090309", 50),
'mfv_stopdbardbar_tau000300um_M0800_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau000300um_M0800/NtupleV23m_2017/190217_090310", 50),
'mfv_stopdbardbar_tau000300um_M1200_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau000300um_M1200/NtupleV23m_2017/190217_090311", 50),
'mfv_stopdbardbar_tau000300um_M1600_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau000300um_M1600/NtupleV23m_2017/190217_090312", 50),
'mfv_stopdbardbar_tau000300um_M3000_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau000300um_M3000/NtupleV23m_2017/190217_090313", 50),
'mfv_stopdbardbar_tau001000um_M0400_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau001000um_M0400/NtupleV23m_2017/190217_090314", 50),
'mfv_stopdbardbar_tau001000um_M0600_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau001000um_M0600/NtupleV23m_2017/190217_090315", 50),
'mfv_stopdbardbar_tau001000um_M0800_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau001000um_M0800/NtupleV23m_2017/190217_090316", 50),
'mfv_stopdbardbar_tau001000um_M1200_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau001000um_M1200/NtupleV23m_2017/190217_090317", 50),
'mfv_stopdbardbar_tau001000um_M1600_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau001000um_M1600/NtupleV23m_2017/190217_090318", 50),
'mfv_stopdbardbar_tau001000um_M3000_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau001000um_M3000/NtupleV23m_2017/190217_090319", 50),
'mfv_stopdbardbar_tau010000um_M0400_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau010000um_M0400/NtupleV23m_2017/190217_090320", 50),
'mfv_stopdbardbar_tau010000um_M0600_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau010000um_M0600/NtupleV23m_2017/190217_090321", 50),
'mfv_stopdbardbar_tau010000um_M0800_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau010000um_M0800/NtupleV23m_2017/190217_090322", 50),
'mfv_stopdbardbar_tau010000um_M1200_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau010000um_M1200/NtupleV23m_2017/190217_090323", 50),
'mfv_stopdbardbar_tau010000um_M1600_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau010000um_M1600/NtupleV23m_2017/190217_090324", 50),
'mfv_stopdbardbar_tau010000um_M3000_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau010000um_M3000/NtupleV23m_2017/190217_090325", 50),
'mfv_stopdbardbar_tau030000um_M0400_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau030000um_M0400/NtupleV23m_2017/190217_090326", 50),
'mfv_stopdbardbar_tau030000um_M0600_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau030000um_M0600/NtupleV23m_2017/190217_090327", 50),
'mfv_stopdbardbar_tau030000um_M0800_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau030000um_M0800/NtupleV23m_2017/190217_090328", 50),
'mfv_stopdbardbar_tau030000um_M1200_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau030000um_M1200/NtupleV23m_2017/190217_090329", 50),
'mfv_stopdbardbar_tau030000um_M1600_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau030000um_M1600/NtupleV23m_2017/190217_090330", 50),
'mfv_stopdbardbar_tau030000um_M3000_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau030000um_M3000/NtupleV23m_2017/190217_090331", 50),
'mfv_stopdbardbar_tau100000um_M0400_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau100000um_M0400/NtupleV23m_2017/190217_090332", 50),
'mfv_stopdbardbar_tau100000um_M0600_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau100000um_M0600/NtupleV23m_2017/190217_090333", 50),
'mfv_stopdbardbar_tau100000um_M0800_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau100000um_M0800/NtupleV23m_2017/190217_090334", 50),
'mfv_stopdbardbar_tau100000um_M1200_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau100000um_M1200/NtupleV23m_2017/190217_090335", 50),
'mfv_stopdbardbar_tau100000um_M1600_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau100000um_M1600/NtupleV23m_2017/190217_090336", 50),
'mfv_stopdbardbar_tau100000um_M3000_2017': _fromnum0("/store/user/wsun/croncopyeos/mfv_stopdbardbar_cp2_tau100000um_M3000/NtupleV23m_2017/190217_090337", 50),
'qcdht0700_2018': (23, ['/store/user/wsun/croncopyeos/QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV23m_2018/190217_090944/0000/ntuple_%i.root' % i for i in chain(xrange(4), xrange(6,18), xrange(19,21), [22])] + ['/store/user/wsun/croncopyeos/QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV23m_2018/190218_014832/0000/ntuple_%i.root' % i for i in chain(xrange(4,6), [18, 21])]),
'qcdht1000_2018': (37, ['/store/user/wsun/croncopyeos/QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV23m_2018/190218_014834/0000/ntuple_%i.root' % i for i in [8, 28, 32]] + ['/store/user/wsun/croncopyeos/QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV23m_2018/190217_090945/0000/ntuple_%i.root' % i for i in chain(xrange(8), xrange(9,28), xrange(29,32), xrange(33,37))]),
'qcdht1500_2018': _fromnum1("/store/user/wsun/croncopyeos/QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV23m_2018/190218_155138", 76),
'qcdht2000_2018': _fromnum0("/store/user/wsun/croncopyeos/QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV23m_2018/190217_090946", 34),
'JetHT2017B': _fromnum1("/store/user/wsun/croncopyeos/JetHT/NtupleV23m_2017/190218_155143", 25),
'JetHT2017C': _fromnum1("/store/user/wsun/croncopyeos/JetHT/NtupleV23m_2017/190218_155156", 38),
'JetHT2017D': _fromnum1("/store/user/wsun/croncopyeos/JetHT/NtupleV23m_2017/190218_155209", 18),
'JetHT2017E': _fromnum1("/store/user/wsun/croncopyeos/JetHT/NtupleV23m_2017/190218_155227", 41),
'JetHT2017F': _fromnum1("/store/user/wsun/croncopyeos/JetHT/NtupleV23m_2017/190218_155242", 51),
'JetHT2018A': _fromnum1("/store/user/wsun/croncopyeos/JetHT/NtupleV23m_2018/190218_155149", 114),
'JetHT2018B': _fromnum1("/store/user/wsun/croncopyeos/JetHT/NtupleV23m_2018/190218_155201", 64),
'JetHT2018C': _fromnum1("/store/user/wsun/croncopyeos/JetHT/NtupleV23m_2018/190218_155213", 43),
'JetHT2018D': _fromnum1("/store/user/wsun/croncopyeos/JetHT/NtupleV23m_2018/190218_155227", 189),
})

_add_ds("ntuplev23m_ntkseeds", {
'qcdht0700_2017': _fromnum0("/store/user/wsun/croncopyeos/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/NtupleV23m_NTkSeeds_2017/190218_102925", 16, fnbase="ntkseeds"),
'qcdht1000_2017': _fromnum1("/store/user/wsun/croncopyeos/QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8/NtupleV23m_NTkSeeds_2017/190218_162806", 31, fnbase="ntkseeds"),
'qcdht1500_2017': _fromnum0("/store/user/wsun/croncopyeos/QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8/NtupleV23m_NTkSeeds_2017/190218_102926", 63, fnbase="ntkseeds"),
'qcdht2000_2017': _fromnum0("/store/user/wsun/croncopyeos/QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/NtupleV23m_NTkSeeds_2017/190218_102927", 30, fnbase="ntkseeds"),
'ttbarht0600_2017': (467, ['/store/user/wsun/croncopyeos/TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV23m_NTkSeeds_2017/190218_102921/0000/ntkseeds_%i.root' % i for i in chain(xrange(375), xrange(376,468))]),
'ttbarht0800_2017': (388, ['/store/user/wsun/croncopyeos/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV23m_NTkSeeds_2017/190218_102922/0000/ntkseeds_%i.root' % i for i in chain(xrange(253), xrange(254,388))] + ['/store/user/wsun/croncopyeos/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV23m_NTkSeeds_2017/190220_132152/0000/ntkseeds_253.root']),
'ttbarht1200_2017': _fromnum0("/store/user/wsun/croncopyeos/TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV23m_NTkSeeds_2017/190218_102923", 180, fnbase="ntkseeds"),
'ttbarht2500_2017': _fromnum0("/store/user/wsun/croncopyeos/TTJets_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV23m_NTkSeeds_2017/190218_102924", 95, fnbase="ntkseeds"),
'qcdht0700_2018': _fromnum0("/store/user/wsun/croncopyeos/QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV23m_NTkSeeds_2018/190218_103158", 23, fnbase="ntkseeds"),
'qcdht1000_2018': _fromnum0("/store/user/wsun/croncopyeos/QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV23m_NTkSeeds_2018/190218_103159", 37, fnbase="ntkseeds"),
'qcdht1500_2018': _fromnum1("/store/user/wsun/croncopyeos/QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV23m_NTkSeeds_2018/190218_163108", 76, fnbase="ntkseeds"),
'qcdht2000_2018': _fromnum0("/store/user/wsun/croncopyeos/QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV23m_NTkSeeds_2018/190218_103200", 34, fnbase="ntkseeds"),
'JetHT2017B': _fromnum1("/store/user/wsun/croncopyeos/JetHT/NtupleV23m_NTkSeeds_2017/190218_162819", 25, fnbase="ntkseeds"),
'JetHT2017C': _fromnum1("/store/user/wsun/croncopyeos/JetHT/NtupleV23m_NTkSeeds_2017/190218_162834", 38, fnbase="ntkseeds"),
'JetHT2017D': _fromnum1("/store/user/wsun/croncopyeos/JetHT/NtupleV23m_NTkSeeds_2017/190218_162849", 18, fnbase="ntkseeds"),
'JetHT2017E': _fromnum1("/store/user/wsun/croncopyeos/JetHT/NtupleV23m_NTkSeeds_2017/190218_162907", 41, fnbase="ntkseeds"),
'JetHT2017F': _fromnum1("/store/user/wsun/croncopyeos/JetHT/NtupleV23m_NTkSeeds_2017/190218_162919", 51, fnbase="ntkseeds"),
'JetHT2018A': _fromnum1("/store/user/wsun/croncopyeos/JetHT/NtupleV23m_NTkSeeds_2018/190218_163120", 114, fnbase="ntkseeds"),
'JetHT2018B': _fromnum1("/store/user/wsun/croncopyeos/JetHT/NtupleV23m_NTkSeeds_2018/190218_163132", 64, fnbase="ntkseeds"),
'JetHT2018C': _fromnum1("/store/user/wsun/croncopyeos/JetHT/NtupleV23m_NTkSeeds_2018/190218_163145", 43, fnbase="ntkseeds"),
'JetHT2018D': _fromnum1("/store/user/wsun/croncopyeos/JetHT/NtupleV23m_NTkSeeds_2018/190218_163157", 189, fnbase="ntkseeds"),
})


_add_ds("nr_trackingtreerv23mv3", {
'qcdht0700_2017': (48, ['/store/user/tucker/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/TrackingTreerV23mv3_2017/190329_154545/0000/trackingtreer_%i.root' % i for i in [25, 46]] + ['/store/user/tucker/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/TrackingTreerV23mv3_2017/190329_150253/0000/trackingtreer_%i.root' % i for i in chain(xrange(22), xrange(23,25), xrange(26,46), [47])] + ['/store/user/tucker/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/TrackingTreerV23mv3_2017/190401_120003/0000/trackingtreer_22.root']),
'qcdht1000_2017': _fromnum1("/store/user/tucker/QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8/TrackingTreerV23mv3_2017/190329_200142", 22, fnbase="trackingtreer"),
'qcdht1500_2017': (11, ['/store/user/tucker/QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8/TrackingTreerV23mv3_2017/190329_150254/0000/trackingtreer_%i.root' % i for i in chain(xrange(7), xrange(13,16), [11])]),
'qcdht2000_2017': _fromnum0("/store/user/tucker/QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/TrackingTreerV23mv3_2017/190329_150255", 10, fnbase="trackingtreer"),
'qcdht0700_2018': (72, ['/store/user/tucker/QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8/TrackingTreerV23mv3_2018/190329_153344/0000/trackingtreer_%i.root' % i for i in chain(xrange(3), xrange(4,72))] + ['/store/user/tucker/QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8/TrackingTreerV23mv3_2018/190329_154546/0000/trackingtreer_3.root']),
'qcdht1000_2018': (26, ['/store/user/tucker/QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8/TrackingTreerV23mv3_2018/190402_070940/0000/trackingtreer_%i.root' % i for i in [2, 13]] + ['/store/user/tucker/QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8/TrackingTreerV23mv3_2018/190329_153345/0000/trackingtreer_%i.root' % i for i in chain(xrange(2), xrange(3,13), xrange(14,16), xrange(17,22), xrange(23,26))] + ['/store/user/tucker/QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8/TrackingTreerV23mv3_2018/190401_120016/0000/trackingtreer_%i.root' % i for i in [16, 22]]),
'qcdht1500_2018': (1, ['/store/user/tucker/QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8/TrackingTreerV23mv3_2018/190329_203300/0000/trackingtreer_18.root']),
'qcdht2000_2018': (9, ['/store/user/tucker/QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8/TrackingTreerV23mv3_2018/190401_120017/0000/trackingtreer_0.root'] + ['/store/user/tucker/QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8/TrackingTreerV23mv3_2018/190329_153346/0000/trackingtreer_%i.root' % i for i in chain(xrange(1,4), xrange(7,11), [5])]),
'JetHT2017B': _fromnum1("/store/user/tucker/JetHT/TrackingTreerV23mv3_2017/190329_200156", 12, fnbase="trackingtreer"),
'JetHT2017C': _fromnum1("/store/user/tucker/JetHT/TrackingTreerV23mv3_2017/190329_200207", 26, fnbase="trackingtreer"),
'JetHT2017D': _fromnum1("/store/user/tucker/JetHT/TrackingTreerV23mv3_2017/190329_200224", 12, fnbase="trackingtreer"),
'JetHT2017E': _fromnum1("/store/user/tucker/JetHT/TrackingTreerV23mv3_2017/190329_200239", 22, fnbase="trackingtreer"),
'JetHT2017F': _fromnum1("/store/user/tucker/JetHT/TrackingTreerV23mv3_2017/190329_200252", 29, fnbase="trackingtreer"),
'JetHT2018A': _fromnum1("/store/user/tucker/JetHT/TrackingTreerV23mv3_2018/190329_203312", 30, fnbase="trackingtreer"),
'JetHT2018B': _fromnum1("/store/user/tucker/JetHT/TrackingTreerV23mv3_2018/190329_203322", 24, fnbase="trackingtreer"),
'JetHT2018C': _fromnum1("/store/user/tucker/JetHT/TrackingTreerV23mv3_2018/190329_203332", 14, fnbase="trackingtreer"),
'JetHT2018D': _fromnum1("/store/user/tucker/JetHT/TrackingTreerV23mv3_2018/190329_203343", 64, fnbase="trackingtreer"),
})


_add_ds("nr_k0ntuplev23mv4", {
'qcdht0700_2017': _fromnum0("/store/user/tucker/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/K0NtupleV23mv4_2017/190420_185316", 191, fnbase="k0tree"),
'qcdht1000_2017': _fromnum1("/store/user/tucker/QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8/K0NtupleV23mv4_2017/190420_235315", 85, fnbase="k0tree"),
'qcdht1500_2017': (62, ['/store/user/tucker/QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8/K0NtupleV23mv4_2017/190420_185317/0000/k0tree_%i.root' % i for i in chain(xrange(3), xrange(4,14), xrange(15,27), xrange(28,36), xrange(41,55), xrange(56,63), [37, 39])] + ['/store/user/tucker/QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8/K0NtupleV23mv4_2017/190423_094943/0000/k0tree_%i.root' % i for i in [38, 40]] + ['/store/user/tucker/QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8/K0NtupleV23mv4_2017/190423_094535/0000/k0tree_%i.root' % i for i in [3, 14, 27, 36]]),
'qcdht2000_2017': (36, ['/store/user/tucker/QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/K0NtupleV23mv4_2017/190423_094536/0000/k0tree_%i.root' % i for i in [7, 15, 26, 30, 36]] + ['/store/user/tucker/QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/K0NtupleV23mv4_2017/190423_094944/0000/k0tree_1.root'] + ['/store/user/tucker/QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/K0NtupleV23mv4_2017/190420_185318/0000/k0tree_%i.root' % i for i in chain(xrange(2,7), xrange(9,15), xrange(16,26), xrange(27,30), xrange(31,36), [0])]),
'qcdht0700_2018': (285, ['/store/user/tucker/QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8/K0NtupleV23mv4_2018/190420_185357/0000/k0tree_%i.root' % i for i in chain(xrange(251), xrange(252,286))]),
'qcdht1000_2018': (101, ['/store/user/tucker/QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8/K0NtupleV23mv4_2018/190420_185358/0000/k0tree_%i.root' % i for i in chain(xrange(66), xrange(67,71), xrange(73,79), xrange(80,90), xrange(91,101))] + ['/store/user/tucker/QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8/K0NtupleV23mv4_2018/190423_094538/0000/k0tree_%i.root' % i for i in chain(xrange(71,73), [66, 79, 90])]),
'qcdht1500_2018': _fromnum1("/store/user/tucker/QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8/K0NtupleV23mv4_2018/190420_235356", 76, fnbase="k0tree"),
'qcdht2000_2018': (42, ['/store/user/tucker/QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8/K0NtupleV23mv4_2018/190420_185359/0000/k0tree_%i.root' % i for i in chain(xrange(10), xrange(11,42))] + ['/store/user/tucker/QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8/K0NtupleV23mv4_2018/190423_094539/0000/k0tree_10.root']),
'JetHT2017B': _fromnum1("/store/user/tucker/JetHT/K0NtupleV23mv4_2017/190420_235209", 155, fnbase="k0tree"),
'JetHT2017C': _fromnum1("/store/user/tucker/JetHT/K0NtupleV23mv4_2017/190420_235224", 233, fnbase="k0tree"),
'JetHT2017D': _fromnum1("/store/user/tucker/JetHT/K0NtupleV23mv4_2017/190420_235237", 110, fnbase="k0tree"),
'JetHT2017E': _fromnum1("/store/user/tucker/JetHT/K0NtupleV23mv4_2017/190420_235249", 256, fnbase="k0tree"),
'JetHT2017F': _fromnum1("/store/user/tucker/JetHT/K0NtupleV23mv4_2017/190420_235302", 318, fnbase="k0tree"),
'JetHT2018A': _fromnum1("/store/user/tucker/JetHT/K0NtupleV23mv4_2018/190420_235311", 710, fnbase="k0tree"),
'JetHT2018B': _fromnum1("/store/user/tucker/JetHT/K0NtupleV23mv4_2018/190420_235323", 360, fnbase="k0tree"),
'JetHT2018C': _fromnum1("/store/user/tucker/JetHT/K0NtupleV23mv4_2018/190420_235334", 267, fnbase="k0tree"),
'JetHT2018D': (1139, ['/store/user/tucker/JetHT/K0NtupleV23mv4_2018/190420_235345' + '/%04i/k0tree_%i.root' % (i/1000,i) for i in chain(xrange(1,5), xrange(6,31), xrange(32,103), xrange(104,112), xrange(113,120), xrange(121,155), xrange(156,180), xrange(181,187), xrange(188,190), xrange(191,265), xrange(266,295), xrange(296,321), xrange(322,409), xrange(410,449), xrange(452,456), xrange(457,467), xrange(468,515), xrange(516,553), xrange(554,654), xrange(655,660), xrange(661,686), xrange(687,768), xrange(769,849), xrange(852,857), xrange(858,895), xrange(896,906), xrange(907,948), xrange(949,983), xrange(984,987), xrange(988,1000), xrange(1001,1008), xrange(1011,1016), xrange(1017,1042), xrange(1043,1048), xrange(1049,1069), xrange(1070,1090), xrange(1091,1159), xrange(1160,1180), [450, 850, 1009])]),
})


_add_ds("ntuplev24m", {
'qcdht0700_2017': _fromnum0("/store/user/tucker/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/NtupleV24m_2017/190509_153834", 16),
'qcdht1000_2017': _fromnum0("/store/user/tucker/QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8/NtupleV24m_2017/190509_153835", 31),
'qcdht1500_2017': _fromnum0("/store/user/tucker/QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8/NtupleV24m_2017/190509_153836", 63),
'qcdht2000_2017': _fromnum0("/store/user/tucker/QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/NtupleV24m_2017/190509_153837", 30),
'ttbarht0600_2017': _fromnum0("/store/user/tucker/TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV24m_2017/190509_153830", 468),
'ttbarht0800_2017': (387, ['/store/user/tucker/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV24m_2017/190509_153831/0000/ntuple_%i.root' % i for i in chain(xrange(283), xrange(284,367), xrange(368,389))]),
'ttbarht1200_2017': (180, ['/store/user/tucker/TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV24m_2017/190509_153832/0000/ntuple_%i.root' % i for i in chain(xrange(169), xrange(170,181))]),
'ttbarht2500_2017': _fromnum0("/store/user/tucker/TTJets_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV24m_2017/190509_153833", 95),
'mfv_neu_tau000100um_M0400_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau000100um_M0400/NtupleV24m_2017/190509_153838", 50),
'mfv_neu_tau000100um_M0600_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau000100um_M0600/NtupleV24m_2017/190509_153839", 50),
'mfv_neu_tau000100um_M0800_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau000100um_M0800/NtupleV24m_2017/190509_153840", 50),
'mfv_neu_tau000100um_M1200_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau000100um_M1200/NtupleV24m_2017/190509_153841", 50),
'mfv_neu_tau000100um_M1600_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau000100um_M1600/NtupleV24m_2017/190509_153842", 50),
'mfv_neu_tau000100um_M3000_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau000100um_M3000/NtupleV24m_2017/190509_153843", 50),
'mfv_neu_tau000300um_M0400_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau000300um_M0400/NtupleV24m_2017/190509_153844", 50),
'mfv_neu_tau000300um_M0600_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau000300um_M0600/NtupleV24m_2017/190509_153845", 50),
'mfv_neu_tau000300um_M0800_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau000300um_M0800/NtupleV24m_2017/190509_153846", 50),
'mfv_neu_tau000300um_M1200_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau000300um_M1200/NtupleV24m_2017/190509_153847", 50),
'mfv_neu_tau000300um_M1600_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau000300um_M1600/NtupleV24m_2017/190509_153848", 50),
'mfv_neu_tau000300um_M3000_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau000300um_M3000/NtupleV24m_2017/190509_153849", 50),
'mfv_neu_tau001000um_M0400_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau001000um_M0400/NtupleV24m_2017/190509_153850", 50),
'mfv_neu_tau001000um_M0600_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau001000um_M0600/NtupleV24m_2017/190509_153851", 50),
'mfv_neu_tau001000um_M0800_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau001000um_M0800/NtupleV24m_2017/190509_153852", 50),
'mfv_neu_tau001000um_M1200_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau001000um_M1200/NtupleV24m_2017/190509_153853", 50),
'mfv_neu_tau001000um_M1600_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau001000um_M1600/NtupleV24m_2017/190509_153854", 50),
'mfv_neu_tau001000um_M3000_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau001000um_M3000/NtupleV24m_2017/190509_153855", 50),
'mfv_neu_tau010000um_M0400_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau010000um_M0400/NtupleV24m_2017/190509_153856", 50),
'mfv_neu_tau010000um_M0600_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau010000um_M0600/NtupleV24m_2017/190509_153857", 50),
'mfv_neu_tau010000um_M0800_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau010000um_M0800/NtupleV24m_2017/190509_153858", 50),
'mfv_neu_tau010000um_M1200_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau010000um_M1200/NtupleV24m_2017/190509_153859", 50),
'mfv_neu_tau010000um_M1600_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau010000um_M1600/NtupleV24m_2017/190509_153900", 50),
'mfv_neu_tau010000um_M3000_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau010000um_M3000/NtupleV24m_2017/190509_153901", 50),
'mfv_neu_tau030000um_M0400_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau030000um_M0400/NtupleV24m_2017/190509_153902", 50),
'mfv_neu_tau030000um_M0600_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau030000um_M0600/NtupleV24m_2017/190509_153903", 50),
'mfv_neu_tau030000um_M0800_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau030000um_M0800/NtupleV24m_2017/190509_153904", 50),
'mfv_neu_tau030000um_M1200_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau030000um_M1200/NtupleV24m_2017/190509_153905", 50),
'mfv_neu_tau030000um_M1600_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau030000um_M1600/NtupleV24m_2017/190509_153906", 50),
'mfv_neu_tau030000um_M3000_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau030000um_M3000/NtupleV24m_2017/190509_153907", 50),
'mfv_neu_tau100000um_M0400_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau100000um_M0400/NtupleV24m_2017/190509_153908", 50),
'mfv_neu_tau100000um_M0600_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau100000um_M0600/NtupleV24m_2017/190509_153909", 50),
'mfv_neu_tau100000um_M0800_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau100000um_M0800/NtupleV24m_2017/190509_153910", 50),
'mfv_neu_tau100000um_M1200_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau100000um_M1200/NtupleV24m_2017/190509_153911", 50),
'mfv_neu_tau100000um_M1600_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau100000um_M1600/NtupleV24m_2017/190509_153912", 50),
'mfv_neu_tau100000um_M3000_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau100000um_M3000/NtupleV24m_2017/190509_153913", 50),
'mfv_stopdbardbar_tau000100um_M0400_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau000100um_M0400/NtupleV24m_2017/190509_153914", 50),
'mfv_stopdbardbar_tau000100um_M0600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau000100um_M0600/NtupleV24m_2017/190509_153915", 50),
'mfv_stopdbardbar_tau000100um_M0800_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau000100um_M0800/NtupleV24m_2017/190509_153916", 50),
'mfv_stopdbardbar_tau000100um_M1200_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau000100um_M1200/NtupleV24m_2017/190509_153917", 50),
'mfv_stopdbardbar_tau000100um_M1600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau000100um_M1600/NtupleV24m_2017/190509_153918", 50),
'mfv_stopdbardbar_tau000100um_M3000_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau000100um_M3000/NtupleV24m_2017/190509_153919", 50),
'mfv_stopdbardbar_tau000300um_M0400_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau000300um_M0400/NtupleV24m_2017/190509_153920", 50),
'mfv_stopdbardbar_tau000300um_M0600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau000300um_M0600/NtupleV24m_2017/190509_153921", 50),
'mfv_stopdbardbar_tau000300um_M0800_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau000300um_M0800/NtupleV24m_2017/190509_153922", 50),
'mfv_stopdbardbar_tau000300um_M1200_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau000300um_M1200/NtupleV24m_2017/190509_153923", 50),
'mfv_stopdbardbar_tau000300um_M1600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau000300um_M1600/NtupleV24m_2017/190509_153924", 50),
'mfv_stopdbardbar_tau000300um_M3000_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau000300um_M3000/NtupleV24m_2017/190509_153925", 50),
'mfv_stopdbardbar_tau001000um_M0400_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau001000um_M0400/NtupleV24m_2017/190509_153926", 50),
'mfv_stopdbardbar_tau001000um_M0600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau001000um_M0600/NtupleV24m_2017/190509_153927", 50),
'mfv_stopdbardbar_tau001000um_M0800_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau001000um_M0800/NtupleV24m_2017/190509_153928", 50),
'mfv_stopdbardbar_tau001000um_M1200_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau001000um_M1200/NtupleV24m_2017/190509_153929", 50),
'mfv_stopdbardbar_tau001000um_M1600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau001000um_M1600/NtupleV24m_2017/190509_153930", 50),
'mfv_stopdbardbar_tau001000um_M3000_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau001000um_M3000/NtupleV24m_2017/190509_153931", 50),
'mfv_stopdbardbar_tau010000um_M0400_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau010000um_M0400/NtupleV24m_2017/190509_153932", 50),
'mfv_stopdbardbar_tau010000um_M0600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau010000um_M0600/NtupleV24m_2017/190509_153933", 50),
'mfv_stopdbardbar_tau010000um_M0800_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau010000um_M0800/NtupleV24m_2017/190509_153934", 50),
'mfv_stopdbardbar_tau010000um_M1200_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau010000um_M1200/NtupleV24m_2017/190509_153935", 50),
'mfv_stopdbardbar_tau010000um_M1600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau010000um_M1600/NtupleV24m_2017/190509_153936", 50),
'mfv_stopdbardbar_tau010000um_M3000_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau010000um_M3000/NtupleV24m_2017/190509_153937", 50),
'mfv_stopdbardbar_tau030000um_M0400_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau030000um_M0400/NtupleV24m_2017/190509_153938", 50),
'mfv_stopdbardbar_tau030000um_M0600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau030000um_M0600/NtupleV24m_2017/190509_153939", 50),
'mfv_stopdbardbar_tau030000um_M0800_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau030000um_M0800/NtupleV24m_2017/190509_153940", 50),
'mfv_stopdbardbar_tau030000um_M1200_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau030000um_M1200/NtupleV24m_2017/190509_153941", 50),
'mfv_stopdbardbar_tau030000um_M1600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau030000um_M1600/NtupleV24m_2017/190509_153942", 50),
'mfv_stopdbardbar_tau030000um_M3000_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau030000um_M3000/NtupleV24m_2017/190509_153943", 50),
'mfv_stopdbardbar_tau100000um_M0400_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau100000um_M0400/NtupleV24m_2017/190509_153944", 50),
'mfv_stopdbardbar_tau100000um_M0600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau100000um_M0600/NtupleV24m_2017/190509_153945", 50),
'mfv_stopdbardbar_tau100000um_M0800_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau100000um_M0800/NtupleV24m_2017/190509_153946", 50),
'mfv_stopdbardbar_tau100000um_M1200_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau100000um_M1200/NtupleV24m_2017/190509_153947", 50),
'mfv_stopdbardbar_tau100000um_M1600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau100000um_M1600/NtupleV24m_2017/190509_153948", 50),
'mfv_stopdbardbar_tau100000um_M3000_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau100000um_M3000/NtupleV24m_2017/190509_153949", 50),
'qcdht0700_2018': _fromnum0("/store/user/tucker/QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV24m_2018/190509_153854", 23),
'qcdht1000_2018': _fromnum0("/store/user/tucker/QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV24m_2018/190509_153855", 37),
'qcdht1500_2018': _fromnum0("/store/user/tucker/QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV24m_2018/190509_153856", 76),
'qcdht2000_2018': _fromnum0("/store/user/tucker/QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV24m_2018/190509_153857", 34),
'ttbarht0600_2018': _fromnum0("/store/user/tucker/TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV24m_2018/190509_153852", 101),
'ttbarht0800_2018': _fromnum0("/store/user/tucker/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV24m_2018/190509_153853", 133),
'ttbarht1200_2018': _fromnum1("/store/user/tucker/TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV24m_2018/190509_203750", 41),
'ttbarht2500_2018': _fromnum1("/store/user/tucker/TTJets_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV24m_2018/190509_203802", 21),
'JetHT2017B': _fromnum1("/store/user/tucker/JetHT/NtupleV24m_2017/190509_203731", 25),
'JetHT2017C': _fromnum1("/store/user/tucker/JetHT/NtupleV24m_2017/190509_203744", 38),
'JetHT2017D': (17, ['/store/user/tucker/JetHT/NtupleV24m_2017/190509_203758/0000/ntuple_%i.root' % i for i in chain(xrange(1,10), xrange(11,19))]),
'JetHT2017E': _fromnum1("/store/user/tucker/JetHT/NtupleV24m_2017/190509_203815", 41),
'JetHT2017F': _fromnum1("/store/user/tucker/JetHT/NtupleV24m_2017/190509_203829", 51),
'JetHT2018A': _fromnum1("/store/user/tucker/JetHT/NtupleV24m_2018/190509_203813", 114),
'JetHT2018B': _fromnum1("/store/user/tucker/JetHT/NtupleV24m_2018/190509_203825", 57),
'JetHT2018C': _fromnum1("/store/user/tucker/JetHT/NtupleV24m_2018/190509_203836", 43),
'JetHT2018D': _fromnum1("/store/user/tucker/JetHT/NtupleV24m_2018/190509_203851", 189),
})

_add_ds("ntuplev24m_ntkseeds", {
'qcdht0700_2017': _fromnum0("/store/user/tucker/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/NtupleV24m_NTkSeeds_2017/190509_155953", 16, fnbase="ntkseeds"),
'qcdht1000_2017': _fromnum0("/store/user/tucker/QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8/NtupleV24m_NTkSeeds_2017/190509_155954", 31, fnbase="ntkseeds"),
'qcdht1500_2017': _fromnum0("/store/user/tucker/QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8/NtupleV24m_NTkSeeds_2017/190509_155955", 63, fnbase="ntkseeds"),
'qcdht2000_2017': (30, ['/store/user/tucker/QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/NtupleV24m_NTkSeeds_2017/190509_155956/0000/ntkseeds_%i.root' % i for i in chain(xrange(24), xrange(25,30))] + ['/store/user/tucker/QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/NtupleV24m_NTkSeeds_2017/190514_130154/0000/ntkseeds_24.root']),
'ttbarht0600_2017': (467, ['/store/user/tucker/TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV24m_NTkSeeds_2017/190509_155949/0000/ntkseeds_%i.root' % i for i in chain(xrange(375), xrange(376,468))]),
'ttbarht0800_2017': (386, ['/store/user/tucker/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV24m_NTkSeeds_2017/190509_155950/0000/ntkseeds_%i.root' % i for i in chain(xrange(253), xrange(254,283), xrange(284,367), xrange(368,389))]),
'ttbarht1200_2017': (180, ['/store/user/tucker/TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV24m_NTkSeeds_2017/190509_155951/0000/ntkseeds_%i.root' % i for i in chain(xrange(169), xrange(170,181))]),
'ttbarht2500_2017': _fromnum0("/store/user/tucker/TTJets_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV24m_NTkSeeds_2017/190509_155952", 95, fnbase="ntkseeds"),
'qcdht0700_2018': (23, ['/store/user/tucker/QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV24m_NTkSeeds_2018/190514_130158/0000/ntkseeds_5.root'] + ['/store/user/tucker/QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV24m_NTkSeeds_2018/190509_181904/0000/ntkseeds_%i.root' % i for i in chain(xrange(5), xrange(6,23))]),
'qcdht1000_2018': (37, ['/store/user/tucker/QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV24m_NTkSeeds_2018/190509_181905/0000/ntkseeds_%i.root' % i for i in chain(xrange(11), xrange(12,37))] + ['/store/user/tucker/QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV24m_NTkSeeds_2018/190514_130200/0000/ntkseeds_11.root']),
'qcdht1500_2018': _fromnum0("/store/user/tucker/QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV24m_NTkSeeds_2018/190509_181906", 76, fnbase="ntkseeds"),
'qcdht2000_2018': _fromnum0("/store/user/tucker/QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV24m_NTkSeeds_2018/190509_181907", 34, fnbase="ntkseeds"),
'ttbarht0600_2018': _fromnum0("/store/user/tucker/TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV24m_NTkSeeds_2018/190509_180613", 101, fnbase="ntkseeds"),
'ttbarht0800_2018': (133, ['/store/user/tucker/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV24m_NTkSeeds_2018/190515_150620/0000/ntkseeds_74.root'] + ['/store/user/tucker/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV24m_NTkSeeds_2018/190509_181903/0000/ntkseeds_%i.root' % i for i in chain(xrange(74), xrange(75,123), xrange(124,133))] + ['/store/user/tucker/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV24m_NTkSeeds_2018/190514_130157/0000/ntkseeds_123.root']),
'ttbarht1200_2018': _fromnum1("/store/user/tucker/TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV24m_NTkSeeds_2018/190510_003124", 41, fnbase="ntkseeds"),
'ttbarht2500_2018': (20, ['/store/user/tucker/TTJets_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV24m_NTkSeeds_2018/190510_003135/0000/ntkseeds_%i.root' % i for i in chain(xrange(1,5), xrange(6,22))]),
'JetHT2017B': _fromnum1("/store/user/tucker/JetHT/NtupleV24m_NTkSeeds_2017/190509_205847", 25, fnbase="ntkseeds"),
'JetHT2017C': (34, ['/store/user/tucker/JetHT/NtupleV24m_NTkSeeds_2017/190509_205902/0000/ntkseeds_%i.root' % i for i in chain(xrange(1,8), xrange(9,17), xrange(18,29), xrange(30,32), xrange(33,39))]),
'JetHT2017D': _fromnum1("/store/user/tucker/JetHT/NtupleV24m_NTkSeeds_2017/190509_205916", 18, fnbase="ntkseeds"),
'JetHT2017E': _fromnum1("/store/user/tucker/JetHT/NtupleV24m_NTkSeeds_2017/190509_205932", 41, fnbase="ntkseeds"),
'JetHT2017F': _fromnum1("/store/user/tucker/JetHT/NtupleV24m_NTkSeeds_2017/190509_205948", 51, fnbase="ntkseeds"),
'JetHT2018A': _fromnum1("/store/user/tucker/JetHT/NtupleV24m_NTkSeeds_2018/190510_003146", 114, fnbase="ntkseeds"),
'JetHT2018B': _fromnum1("/store/user/tucker/JetHT/NtupleV24m_NTkSeeds_2018/190510_003157", 57, fnbase="ntkseeds"),
'JetHT2018C': _fromnum1("/store/user/tucker/JetHT/NtupleV24m_NTkSeeds_2018/190510_003208", 43, fnbase="ntkseeds"),
'JetHT2018D': (185, ['/store/user/tucker/JetHT/NtupleV24m_NTkSeeds_2018/190510_003220/0000/ntkseeds_%i.root' % i for i in chain(xrange(1,35), xrange(36,38), xrange(39,52), xrange(53,112), xrange(113,190))]),
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

    elif 'removed' in sys.argv:
        import colors
        def ok(fn):
            assert fn.startswith('/store') and fn.endswith('.root')
            ret = os.system('xrdcp -sf root://cmsxrootd-site.fnal.gov/%s /dev/null' % fn)
            if ret != 0:
                ret = os.system('xrdcp -sf root://cmseos.fnal.gov/%s /dev/null' % fn)
            return ret == 0
        for (name,ds), fn in _removed:
            print (colors.boldred if ok(fn) else colors.green)('%s %s %s' % (name, ds, fn))

    else:
        sys.exit('did not understand argv %r' % sys.argv)
