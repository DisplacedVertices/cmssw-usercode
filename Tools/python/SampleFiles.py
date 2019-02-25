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

for x,y in [
    ('qcdht0700_2017', '/store/mc/RunIIFall17MiniAODv2/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/90000/B234A578-B844-E811-BB35-0025905B85D8.root'),
    ('qcdht0700_2017', '/store/mc/RunIIFall17MiniAODv2/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/40000/2A23B4F0-3F43-E811-B600-0CC47A7C34E6.root'),
    ('qcdht0700_2017', '/store/mc/RunIIFall17MiniAODv2/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/40000/964601B9-4F43-E811-9557-0025905A611E.root'),
    ('qcdht0700_2017', '/store/mc/RunIIFall17MiniAODv2/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/70000/4AD19A1D-F443-E811-B7FE-0025905B85D8.root'),
    ('qcdht0700_2017', '/store/mc/RunIIFall17MiniAODv2/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/20000/9CD54B20-9642-E811-9189-0CC47A78A340.root'),
    ('qcdht1500_2017', '/store/mc/RunIIFall17MiniAODv2/QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/10000/AC4239D2-5A5C-E811-A0F6-0025905B857C.root'),
    ('qcdht2000_2017', '/store/mc/RunIIFall17MiniAODv2/QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/100000/3C55942E-FB66-E811-8781-00000086FE80.root'),
    ('qcdht0700_2018', '/store/mc/RunIIAutumn18MiniAOD/QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/102X_upgrade2018_realistic_v15-v1/020000/582A14C2-1BD1-6848-AE57-C110F6E929A0.root'),
    ('qcdht0700_2018', '/store/mc/RunIIAutumn18MiniAOD/QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/102X_upgrade2018_realistic_v15-v1/20000/20DB6628-3A60-3245-A133-F831ED22EFE4.root'),
    ('qcdht0700_2018', '/store/mc/RunIIAutumn18MiniAOD/QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/102X_upgrade2018_realistic_v15-v1/210000/0F36F5C9-DEE9-DD47-B1CB-54593A37E62E.root'),
    ('qcdht0700_2018', '/store/mc/RunIIAutumn18MiniAOD/QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/102X_upgrade2018_realistic_v15-v1/110000/D68ADEFB-1AFC-B74B-B887-FA6A270E93D3.root'),
    ('qcdht0700_2018', '/store/mc/RunIIAutumn18MiniAOD/QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/102X_upgrade2018_realistic_v15-v1/60000/818480BB-489C-AE4F-AE90-15E4F609DFF5.root'),
    ('qcdht1000_2018', '/store/mc/RunIIAutumn18MiniAOD/QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/102X_upgrade2018_realistic_v15-v1/80000/65289A90-B55E-7846-8657-4A9E1D72D8DE.root'),
    ('qcdht1000_2018', '/store/mc/RunIIAutumn18MiniAOD/QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/102X_upgrade2018_realistic_v15-v1/80000/81B07983-AA32-D94C-98C5-7D9D5C357D05.root'),
    ('qcdht1000_2018', '/store/mc/RunIIAutumn18MiniAOD/QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/102X_upgrade2018_realistic_v15-v1/120000/C32DE14A-0192-E74E-AB88-E9D3CD16435F.root'),
    ('ttbarht0800_2017', '/store/mc/RunIIFall17MiniAODv2/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/40000/225CD078-B3A4-E811-AA74-001E67DDC254.root'),
    ('ttbarht0800_2017', '/store/mc/RunIIFall17MiniAODv2/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/60000/BC22A92A-7BBA-E811-8A2B-0242AC1C0501.root'),
    ('ttbarht1200_2017', '/store/mc/RunIIFall17MiniAODv2/TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/90000/6E6C0DD6-349B-E811-A4E1-0CC47A6C063E.root'),
    ]:
    _remove_file(x, 'miniaod', y)

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
'qcdht0700_2018': (23, ['/store/user/tucker/QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV22m_2018/190111_120316/0000/ntuple_22.root'] + ['/store/user/tucker/QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV22m_2018/190110_114432/0000/ntuple_%i.root' % i for i in xrange(22)]),
'qcdht1000_2018': _fromnum0("/store/user/tucker/QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV22m_2018/190110_114433", 37),
'qcdht1500_2018': (76, ['/store/user/tucker/QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV22m_2018/190110_163535/0000/ntuple_%i.root' % i for i in xrange(42,44)] + ['/store/user/tucker/QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV22m_2018/190110_114434/0000/ntuple_%i.root' % i for i in chain(xrange(42), xrange(44,76))]),
'qcdht2000_2018': _fromnum0("/store/user/tucker/QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV22m_2018/190110_114435", 34),
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


_add_ds("ntuplev23m", {
'qcdht0700_2017': (16, ['/store/user/tucker/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/NtupleV23m_2017/190218_014828/0000/ntuple_%i.root' % i for i in chain(xrange(4,8), [14])] + ['/store/user/tucker/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/NtupleV23m_2017/190217_090223/0000/ntuple_%i.root' % i for i in chain(xrange(4), xrange(8,14), [15])]),
'qcdht1000_2017': _fromnum1("/store/user/tucker/QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8/NtupleV23m_2017/190218_155129", 31),
'qcdht1500_2017': (63, ['/store/user/tucker/QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8/NtupleV23m_2017/190217_090224/0000/ntuple_%i.root' % i for i in chain(xrange(40), xrange(41,63))] + ['/store/user/tucker/QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8/NtupleV23m_2017/190218_014829/0000/ntuple_40.root']),
'qcdht2000_2017': (30, ['/store/user/tucker/QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/NtupleV23m_2017/190218_014831/0000/ntuple_29.root'] + ['/store/user/tucker/QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/NtupleV23m_2017/190217_090225/0000/ntuple_%i.root' % i for i in xrange(29)]),
'ttbarht0600_2017': _fromnum0("/store/user/tucker/TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV23m_2017/190217_090219", 468),
'ttbarht0800_2017': _fromnum0("/store/user/tucker/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV23m_2017/190217_090220", 388),
'ttbarht1200_2017': _fromnum0("/store/user/tucker/TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV23m_2017/190217_090221", 180),
'ttbarht2500_2017': _fromnum0("/store/user/tucker/TTJets_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV23m_2017/190217_090222", 95),
'mfv_neu_tau000100um_M0400_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau000100um_M0400/NtupleV23m_2017/190217_090226", 50),
'mfv_neu_tau000100um_M0600_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau000100um_M0600/NtupleV23m_2017/190217_090227", 50),
'mfv_neu_tau000100um_M0800_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau000100um_M0800/NtupleV23m_2017/190217_090228", 50),
'mfv_neu_tau000100um_M1200_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau000100um_M1200/NtupleV23m_2017/190217_090229", 50),
'mfv_neu_tau000100um_M1600_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau000100um_M1600/NtupleV23m_2017/190217_090230", 50),
'mfv_neu_tau000100um_M3000_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau000100um_M3000/NtupleV23m_2017/190217_090231", 50),
'mfv_neu_tau000300um_M0400_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau000300um_M0400/NtupleV23m_2017/190217_090232", 50),
'mfv_neu_tau000300um_M0600_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau000300um_M0600/NtupleV23m_2017/190217_090233", 50),
'mfv_neu_tau000300um_M0800_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau000300um_M0800/NtupleV23m_2017/190217_090234", 50),
'mfv_neu_tau000300um_M1200_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau000300um_M1200/NtupleV23m_2017/190217_090235", 50),
'mfv_neu_tau000300um_M1600_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau000300um_M1600/NtupleV23m_2017/190217_090236", 50),
'mfv_neu_tau000300um_M3000_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau000300um_M3000/NtupleV23m_2017/190217_090237", 50),
'mfv_neu_tau001000um_M0400_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau001000um_M0400/NtupleV23m_2017/190217_090238", 50),
'mfv_neu_tau001000um_M0600_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau001000um_M0600/NtupleV23m_2017/190217_090239", 50),
'mfv_neu_tau001000um_M0800_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau001000um_M0800/NtupleV23m_2017/190217_090240", 50),
'mfv_neu_tau001000um_M1200_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau001000um_M1200/NtupleV23m_2017/190217_090241", 50),
'mfv_neu_tau001000um_M1600_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau001000um_M1600/NtupleV23m_2017/190217_090242", 50),
'mfv_neu_tau001000um_M3000_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau001000um_M3000/NtupleV23m_2017/190217_090243", 50),
'mfv_neu_tau010000um_M0400_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau010000um_M0400/NtupleV23m_2017/190217_090244", 50),
'mfv_neu_tau010000um_M0600_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau010000um_M0600/NtupleV23m_2017/190217_090245", 50),
'mfv_neu_tau010000um_M0800_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau010000um_M0800/NtupleV23m_2017/190217_090246", 50),
'mfv_neu_tau010000um_M1200_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau010000um_M1200/NtupleV23m_2017/190217_090247", 50),
'mfv_neu_tau010000um_M1600_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau010000um_M1600/NtupleV23m_2017/190217_090248", 50),
'mfv_neu_tau010000um_M3000_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau010000um_M3000/NtupleV23m_2017/190217_090249", 50),
'mfv_neu_tau030000um_M0400_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau030000um_M0400/NtupleV23m_2017/190217_090250", 50),
'mfv_neu_tau030000um_M0600_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau030000um_M0600/NtupleV23m_2017/190217_090251", 50),
'mfv_neu_tau030000um_M0800_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau030000um_M0800/NtupleV23m_2017/190217_090252", 50),
'mfv_neu_tau030000um_M1200_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau030000um_M1200/NtupleV23m_2017/190217_090253", 50),
'mfv_neu_tau030000um_M1600_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau030000um_M1600/NtupleV23m_2017/190217_090254", 50),
'mfv_neu_tau030000um_M3000_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau030000um_M3000/NtupleV23m_2017/190217_090255", 50),
'mfv_neu_tau100000um_M0400_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau100000um_M0400/NtupleV23m_2017/190217_090256", 50),
'mfv_neu_tau100000um_M0600_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau100000um_M0600/NtupleV23m_2017/190217_090257", 50),
'mfv_neu_tau100000um_M0800_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau100000um_M0800/NtupleV23m_2017/190217_090258", 50),
'mfv_neu_tau100000um_M1200_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau100000um_M1200/NtupleV23m_2017/190217_090259", 50),
'mfv_neu_tau100000um_M1600_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau100000um_M1600/NtupleV23m_2017/190217_090300", 50),
'mfv_neu_tau100000um_M3000_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau100000um_M3000/NtupleV23m_2017/190217_090301", 50),
'mfv_stopdbardbar_tau000100um_M0400_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau000100um_M0400/NtupleV23m_2017/190217_090302", 50),
'mfv_stopdbardbar_tau000100um_M0600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau000100um_M0600/NtupleV23m_2017/190217_090303", 50),
'mfv_stopdbardbar_tau000100um_M0800_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau000100um_M0800/NtupleV23m_2017/190217_090304", 50),
'mfv_stopdbardbar_tau000100um_M1200_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau000100um_M1200/NtupleV23m_2017/190217_090305", 50),
'mfv_stopdbardbar_tau000100um_M1600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau000100um_M1600/NtupleV23m_2017/190217_090306", 50),
'mfv_stopdbardbar_tau000100um_M3000_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau000100um_M3000/NtupleV23m_2017/190217_090307", 50),
'mfv_stopdbardbar_tau000300um_M0400_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau000300um_M0400/NtupleV23m_2017/190217_090308", 50),
'mfv_stopdbardbar_tau000300um_M0600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau000300um_M0600/NtupleV23m_2017/190217_090309", 50),
'mfv_stopdbardbar_tau000300um_M0800_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau000300um_M0800/NtupleV23m_2017/190217_090310", 50),
'mfv_stopdbardbar_tau000300um_M1200_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau000300um_M1200/NtupleV23m_2017/190217_090311", 50),
'mfv_stopdbardbar_tau000300um_M1600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau000300um_M1600/NtupleV23m_2017/190217_090312", 50),
'mfv_stopdbardbar_tau000300um_M3000_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau000300um_M3000/NtupleV23m_2017/190217_090313", 50),
'mfv_stopdbardbar_tau001000um_M0400_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau001000um_M0400/NtupleV23m_2017/190217_090314", 50),
'mfv_stopdbardbar_tau001000um_M0600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau001000um_M0600/NtupleV23m_2017/190217_090315", 50),
'mfv_stopdbardbar_tau001000um_M0800_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau001000um_M0800/NtupleV23m_2017/190217_090316", 50),
'mfv_stopdbardbar_tau001000um_M1200_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau001000um_M1200/NtupleV23m_2017/190217_090317", 50),
'mfv_stopdbardbar_tau001000um_M1600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau001000um_M1600/NtupleV23m_2017/190217_090318", 50),
'mfv_stopdbardbar_tau001000um_M3000_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau001000um_M3000/NtupleV23m_2017/190217_090319", 50),
'mfv_stopdbardbar_tau010000um_M0400_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau010000um_M0400/NtupleV23m_2017/190217_090320", 50),
'mfv_stopdbardbar_tau010000um_M0600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau010000um_M0600/NtupleV23m_2017/190217_090321", 50),
'mfv_stopdbardbar_tau010000um_M0800_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau010000um_M0800/NtupleV23m_2017/190217_090322", 50),
'mfv_stopdbardbar_tau010000um_M1200_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau010000um_M1200/NtupleV23m_2017/190217_090323", 50),
'mfv_stopdbardbar_tau010000um_M1600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau010000um_M1600/NtupleV23m_2017/190217_090324", 50),
'mfv_stopdbardbar_tau010000um_M3000_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau010000um_M3000/NtupleV23m_2017/190217_090325", 50),
'mfv_stopdbardbar_tau030000um_M0400_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau030000um_M0400/NtupleV23m_2017/190217_090326", 50),
'mfv_stopdbardbar_tau030000um_M0600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau030000um_M0600/NtupleV23m_2017/190217_090327", 50),
'mfv_stopdbardbar_tau030000um_M0800_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau030000um_M0800/NtupleV23m_2017/190217_090328", 50),
'mfv_stopdbardbar_tau030000um_M1200_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau030000um_M1200/NtupleV23m_2017/190217_090329", 50),
'mfv_stopdbardbar_tau030000um_M1600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau030000um_M1600/NtupleV23m_2017/190217_090330", 50),
'mfv_stopdbardbar_tau030000um_M3000_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau030000um_M3000/NtupleV23m_2017/190217_090331", 50),
'mfv_stopdbardbar_tau100000um_M0400_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau100000um_M0400/NtupleV23m_2017/190217_090332", 50),
'mfv_stopdbardbar_tau100000um_M0600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau100000um_M0600/NtupleV23m_2017/190217_090333", 50),
'mfv_stopdbardbar_tau100000um_M0800_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau100000um_M0800/NtupleV23m_2017/190217_090334", 50),
'mfv_stopdbardbar_tau100000um_M1200_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau100000um_M1200/NtupleV23m_2017/190217_090335", 50),
'mfv_stopdbardbar_tau100000um_M1600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau100000um_M1600/NtupleV23m_2017/190217_090336", 50),
'mfv_stopdbardbar_tau100000um_M3000_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau100000um_M3000/NtupleV23m_2017/190217_090337", 50),
'qcdht0700_2018': (23, ['/store/user/tucker/QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV23m_2018/190217_090944/0000/ntuple_%i.root' % i for i in chain(xrange(4), xrange(6,18), xrange(19,21), [22])] + ['/store/user/tucker/QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV23m_2018/190218_014832/0000/ntuple_%i.root' % i for i in chain(xrange(4,6), [18, 21])]),
'qcdht1000_2018': (37, ['/store/user/tucker/QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV23m_2018/190218_014834/0000/ntuple_%i.root' % i for i in [8, 28, 32]] + ['/store/user/tucker/QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV23m_2018/190217_090945/0000/ntuple_%i.root' % i for i in chain(xrange(8), xrange(9,28), xrange(29,32), xrange(33,37))]),
'qcdht1500_2018': _fromnum1("/store/user/tucker/QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV23m_2018/190218_155138", 76),
'qcdht2000_2018': _fromnum0("/store/user/tucker/QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV23m_2018/190217_090946", 34),
'JetHT2017B': _fromnum1("/store/user/tucker/JetHT/NtupleV23m_2017/190218_155143", 25),
'JetHT2017C': _fromnum1("/store/user/tucker/JetHT/NtupleV23m_2017/190218_155156", 38),
'JetHT2017D': _fromnum1("/store/user/tucker/JetHT/NtupleV23m_2017/190218_155209", 18),
'JetHT2017E': _fromnum1("/store/user/tucker/JetHT/NtupleV23m_2017/190218_155227", 41),
'JetHT2017F': _fromnum1("/store/user/tucker/JetHT/NtupleV23m_2017/190218_155242", 51),
'JetHT2018A': _fromnum1("/store/user/tucker/JetHT/NtupleV23m_2018/190218_155149", 114),
'JetHT2018B': _fromnum1("/store/user/tucker/JetHT/NtupleV23m_2018/190218_155201", 64),
'JetHT2018C': _fromnum1("/store/user/tucker/JetHT/NtupleV23m_2018/190218_155213", 43),
'JetHT2018D': _fromnum1("/store/user/tucker/JetHT/NtupleV23m_2018/190218_155227", 189),
})

_add_ds("ntuplev23m_ntkseeds", {
'qcdht0700_2017': _fromnum0("/store/user/tucker/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/NtupleV23m_NTkSeeds_2017/190218_102925", 16, fnbase="ntkseeds"),
'qcdht1000_2017': _fromnum1("/store/user/tucker/QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8/NtupleV23m_NTkSeeds_2017/190218_162806", 31, fnbase="ntkseeds"),
'qcdht1500_2017': _fromnum0("/store/user/tucker/QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8/NtupleV23m_NTkSeeds_2017/190218_102926", 63, fnbase="ntkseeds"),
'qcdht2000_2017': _fromnum0("/store/user/tucker/QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/NtupleV23m_NTkSeeds_2017/190218_102927", 30, fnbase="ntkseeds"),
'ttbarht0600_2017': (467, ['/store/user/tucker/TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV23m_NTkSeeds_2017/190218_102921/0000/ntkseeds_%i.root' % i for i in chain(xrange(375), xrange(376,468))]),
'ttbarht0800_2017': (388, ['/store/user/tucker/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV23m_NTkSeeds_2017/190218_102922/0000/ntkseeds_%i.root' % i for i in chain(xrange(253), xrange(254,388))] + ['/store/user/tucker/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV23m_NTkSeeds_2017/190220_132152/0000/ntkseeds_253.root']),
'ttbarht1200_2017': _fromnum0("/store/user/tucker/TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV23m_NTkSeeds_2017/190218_102923", 180, fnbase="ntkseeds"),
'ttbarht2500_2017': _fromnum0("/store/user/tucker/TTJets_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV23m_NTkSeeds_2017/190218_102924", 95, fnbase="ntkseeds"),
'qcdht0700_2018': _fromnum0("/store/user/tucker/QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV23m_NTkSeeds_2018/190218_103158", 23, fnbase="ntkseeds"),
'qcdht1000_2018': _fromnum0("/store/user/tucker/QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV23m_NTkSeeds_2018/190218_103159", 37, fnbase="ntkseeds"),
'qcdht1500_2018': _fromnum1("/store/user/tucker/QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV23m_NTkSeeds_2018/190218_163108", 76, fnbase="ntkseeds"),
'qcdht2000_2018': _fromnum0("/store/user/tucker/QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV23m_NTkSeeds_2018/190218_103200", 34, fnbase="ntkseeds"),
'JetHT2017B': _fromnum1("/store/user/tucker/JetHT/NtupleV23m_NTkSeeds_2017/190218_162819", 25, fnbase="ntkseeds"),
'JetHT2017C': _fromnum1("/store/user/tucker/JetHT/NtupleV23m_NTkSeeds_2017/190218_162834", 38, fnbase="ntkseeds"),
'JetHT2017D': _fromnum1("/store/user/tucker/JetHT/NtupleV23m_NTkSeeds_2017/190218_162849", 18, fnbase="ntkseeds"),
'JetHT2017E': _fromnum1("/store/user/tucker/JetHT/NtupleV23m_NTkSeeds_2017/190218_162907", 41, fnbase="ntkseeds"),
'JetHT2017F': _fromnum1("/store/user/tucker/JetHT/NtupleV23m_NTkSeeds_2017/190218_162919", 51, fnbase="ntkseeds"),
'JetHT2018A': _fromnum1("/store/user/tucker/JetHT/NtupleV23m_NTkSeeds_2018/190218_163120", 114, fnbase="ntkseeds"),
'JetHT2018B': _fromnum1("/store/user/tucker/JetHT/NtupleV23m_NTkSeeds_2018/190218_163132", 64, fnbase="ntkseeds"),
'JetHT2018C': _fromnum1("/store/user/tucker/JetHT/NtupleV23m_NTkSeeds_2018/190218_163145", 43, fnbase="ntkseeds"),
'JetHT2018D': _fromnum1("/store/user/tucker/JetHT/NtupleV23m_NTkSeeds_2018/190218_163157", 189, fnbase="ntkseeds"),
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
