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

def set_process(process, name, ds, num=-1):
    fns = _d[(name, ds)][1]
    if num > 0:
        fns = fns[:num]
    fns = [('root://cmseos.fnal.gov/' + fn) if fn.startswith('/store/user') else fn for fn in fns]
    process.source.fileNames = fns

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

_add_ds("main", {
'mfv_neu_tau000100um_M0400_2017': _fromnum1("/store/user/tucker/mfv_neu_cp2_tau000100um_M0400/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_053632", 100, fnbase="reco"),
'mfv_neu_tau000100um_M0600_2017': _fromnum1("/store/user/tucker/mfv_neu_cp2_tau000100um_M0600/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_053653", 100, fnbase="reco"),
'mfv_neu_tau000100um_M0800_2017': _fromnum1("/store/user/tucker/mfv_neu_cp2_tau000100um_M0800/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_053713", 100, fnbase="reco"),
'mfv_neu_tau000100um_M1200_2017': _fromnum1("/store/user/tucker/mfv_neu_cp2_tau000100um_M1200/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_053737", 100, fnbase="reco"),
'mfv_neu_tau000100um_M1600_2017': _fromnum1("/store/user/tucker/mfv_neu_cp2_tau000100um_M1600/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_053805", 100, fnbase="reco"),
'mfv_neu_tau000100um_M3000_2017': _fromnum1("/store/user/tucker/mfv_neu_cp2_tau000100um_M3000/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_053825", 100, fnbase="reco"),
'mfv_neu_tau000300um_M0400_2017': _fromnum1("/store/user/tucker/mfv_neu_cp2_tau000300um_M0400/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_053847", 100, fnbase="reco"),
'mfv_neu_tau000300um_M0600_2017': _fromnum1("/store/user/tucker/mfv_neu_cp2_tau000300um_M0600/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_053908", 100, fnbase="reco"),
'mfv_neu_tau000300um_M0800_2017': _fromnum1("/store/user/tucker/mfv_neu_cp2_tau000300um_M0800/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_053929", 100, fnbase="reco"),
'mfv_neu_tau000300um_M1200_2017': _fromnum1("/store/user/tucker/mfv_neu_cp2_tau000300um_M1200/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_053953", 100, fnbase="reco"),
'mfv_neu_tau000300um_M1600_2017': _fromnum1("/store/user/tucker/mfv_neu_cp2_tau000300um_M1600/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_054019", 100, fnbase="reco"),
'mfv_neu_tau000300um_M3000_2017': _fromnum1("/store/user/tucker/mfv_neu_cp2_tau000300um_M3000/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_054045", 100, fnbase="reco"),
'mfv_neu_tau001000um_M0400_2017': _fromnum1("/store/user/tucker/mfv_neu_cp2_tau001000um_M0400/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_054108", 100, fnbase="reco"),
'mfv_neu_tau001000um_M0600_2017': _fromnum1("/store/user/tucker/mfv_neu_cp2_tau001000um_M0600/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_054132", 100, fnbase="reco"),
'mfv_neu_tau001000um_M0800_2017': _fromnum1("/store/user/tucker/mfv_neu_cp2_tau001000um_M0800/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_054154", 100, fnbase="reco"),
'mfv_neu_tau001000um_M1200_2017': _fromnum1("/store/user/tucker/mfv_neu_cp2_tau001000um_M1200/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_054216", 100, fnbase="reco"),
'mfv_neu_tau001000um_M1600_2017': _fromnum1("/store/user/tucker/mfv_neu_cp2_tau001000um_M1600/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_054235", 100, fnbase="reco"),
'mfv_neu_tau001000um_M3000_2017': _fromnum1("/store/user/tucker/mfv_neu_cp2_tau001000um_M3000/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_054256", 100, fnbase="reco"),
'mfv_neu_tau010000um_M0400_2017': _fromnum1("/store/user/tucker/mfv_neu_cp2_tau010000um_M0400/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_054321", 100, fnbase="reco"),
'mfv_neu_tau010000um_M0600_2017': _fromnum1("/store/user/tucker/mfv_neu_cp2_tau010000um_M0600/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_054342", 100, fnbase="reco"),
'mfv_neu_tau010000um_M0800_2017': _fromnum1("/store/user/tucker/mfv_neu_cp2_tau010000um_M0800/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_054406", 100, fnbase="reco"),
'mfv_neu_tau010000um_M1200_2017': _fromnum1("/store/user/tucker/mfv_neu_cp2_tau010000um_M1200/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_054427", 100, fnbase="reco"),
'mfv_neu_tau010000um_M1600_2017': _fromnum1("/store/user/tucker/mfv_neu_cp2_tau010000um_M1600/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_054448", 100, fnbase="reco"),
'mfv_neu_tau010000um_M3000_2017': _fromnum1("/store/user/tucker/mfv_neu_cp2_tau010000um_M3000/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_054509", 100, fnbase="reco"),
'mfv_neu_tau030000um_M0400_2017': _fromnum1("/store/user/tucker/mfv_neu_cp2_tau030000um_M0400/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_054532", 100, fnbase="reco"),
'mfv_neu_tau030000um_M0600_2017': _fromnum1("/store/user/tucker/mfv_neu_cp2_tau030000um_M0600/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_054551", 100, fnbase="reco"),
'mfv_neu_tau030000um_M0800_2017': _fromnum1("/store/user/tucker/mfv_neu_cp2_tau030000um_M0800/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_054616", 100, fnbase="reco"),
'mfv_neu_tau030000um_M1200_2017': _fromnum1("/store/user/tucker/mfv_neu_cp2_tau030000um_M1200/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_054637", 100, fnbase="reco"),
'mfv_neu_tau030000um_M1600_2017': _fromnum1("/store/user/tucker/mfv_neu_cp2_tau030000um_M1600/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_054659", 100, fnbase="reco"),
'mfv_neu_tau030000um_M3000_2017': _fromnum1("/store/user/tucker/mfv_neu_cp2_tau030000um_M3000/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_054722", 100, fnbase="reco"),
'mfv_neu_tau100000um_M0400_2017': _fromnum1("/store/user/tucker/mfv_neu_cp2_tau100000um_M0400/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_054744", 100, fnbase="reco"),
'mfv_neu_tau100000um_M0600_2017': _fromnum1("/store/user/tucker/mfv_neu_cp2_tau100000um_M0600/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_054806", 100, fnbase="reco"),
'mfv_neu_tau100000um_M0800_2017': _fromnum1("/store/user/tucker/mfv_neu_cp2_tau100000um_M0800/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_054830", 100, fnbase="reco"),
'mfv_neu_tau100000um_M1200_2017': _fromnum1("/store/user/tucker/mfv_neu_cp2_tau100000um_M1200/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_054851", 100, fnbase="reco"),
'mfv_neu_tau100000um_M1600_2017': _fromnum1("/store/user/tucker/mfv_neu_cp2_tau100000um_M1600/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_054916", 100, fnbase="reco"),
'mfv_neu_tau100000um_M3000_2017': _fromnum1("/store/user/tucker/mfv_neu_cp2_tau100000um_M3000/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_054937", 100, fnbase="reco"),
'mfv_stopdbardbar_tau000100um_M0400_2017': _fromnum1("/store/user/tucker/mfv_stopdbardbar_cp2_tau000100um_M0400/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_050346", 100, fnbase="reco"),
'mfv_stopdbardbar_tau000100um_M0600_2017': _fromnum1("/store/user/tucker/mfv_stopdbardbar_cp2_tau000100um_M0600/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_050416", 100, fnbase="reco"),
'mfv_stopdbardbar_tau000100um_M0800_2017': _fromnum1("/store/user/tucker/mfv_stopdbardbar_cp2_tau000100um_M0800/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_050436", 100, fnbase="reco"),
'mfv_stopdbardbar_tau000100um_M1200_2017': _fromnum1("/store/user/tucker/mfv_stopdbardbar_cp2_tau000100um_M1200/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_050457", 100, fnbase="reco"),
'mfv_stopdbardbar_tau000100um_M1600_2017': _fromnum1("/store/user/tucker/mfv_stopdbardbar_cp2_tau000100um_M1600/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_050522", 100, fnbase="reco"),
'mfv_stopdbardbar_tau000100um_M3000_2017': _fromnum1("/store/user/tucker/mfv_stopdbardbar_cp2_tau000100um_M3000/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_050553", 100, fnbase="reco"),
'mfv_stopdbardbar_tau000300um_M0400_2017': _fromnum1("/store/user/tucker/mfv_stopdbardbar_cp2_tau000300um_M0400/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_050621", 100, fnbase="reco"),
'mfv_stopdbardbar_tau000300um_M0600_2017': _fromnum1("/store/user/tucker/mfv_stopdbardbar_cp2_tau000300um_M0600/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_050644", 100, fnbase="reco"),
'mfv_stopdbardbar_tau000300um_M0800_2017': _fromnum1("/store/user/tucker/mfv_stopdbardbar_cp2_tau000300um_M0800/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_050707", 100, fnbase="reco"),
'mfv_stopdbardbar_tau000300um_M1200_2017': _fromnum1("/store/user/tucker/mfv_stopdbardbar_cp2_tau000300um_M1200/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_050729", 100, fnbase="reco"),
'mfv_stopdbardbar_tau000300um_M1600_2017': _fromnum1("/store/user/tucker/mfv_stopdbardbar_cp2_tau000300um_M1600/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_050750", 100, fnbase="reco"),
'mfv_stopdbardbar_tau000300um_M3000_2017': _fromnum1("/store/user/tucker/mfv_stopdbardbar_cp2_tau000300um_M3000/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_050815", 100, fnbase="reco"),
'mfv_stopdbardbar_tau001000um_M0400_2017': _fromnum1("/store/user/tucker/mfv_stopdbardbar_cp2_tau001000um_M0400/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_050856", 100, fnbase="reco"),
'mfv_stopdbardbar_tau001000um_M0600_2017': _fromnum1("/store/user/tucker/mfv_stopdbardbar_cp2_tau001000um_M0600/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_050920", 100, fnbase="reco"),
'mfv_stopdbardbar_tau001000um_M0800_2017': _fromnum1("/store/user/tucker/mfv_stopdbardbar_cp2_tau001000um_M0800/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_050941", 100, fnbase="reco"),
'mfv_stopdbardbar_tau001000um_M1200_2017': _fromnum1("/store/user/tucker/mfv_stopdbardbar_cp2_tau001000um_M1200/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_051007", 100, fnbase="reco"),
'mfv_stopdbardbar_tau001000um_M1600_2017': _fromnum1("/store/user/tucker/mfv_stopdbardbar_cp2_tau001000um_M1600/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_051027", 100, fnbase="reco"),
'mfv_stopdbardbar_tau001000um_M3000_2017': _fromnum1("/store/user/tucker/mfv_stopdbardbar_cp2_tau001000um_M3000/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_051047", 100, fnbase="reco"),
'mfv_stopdbardbar_tau010000um_M0400_2017': _fromnum1("/store/user/tucker/mfv_stopdbardbar_cp2_tau010000um_M0400/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_051109", 100, fnbase="reco"),
'mfv_stopdbardbar_tau010000um_M0600_2017': _fromnum1("/store/user/tucker/mfv_stopdbardbar_cp2_tau010000um_M0600/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_051130", 100, fnbase="reco"),
'mfv_stopdbardbar_tau010000um_M0800_2017': _fromnum1("/store/user/tucker/mfv_stopdbardbar_cp2_tau010000um_M0800/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_051150", 100, fnbase="reco"),
'mfv_stopdbardbar_tau010000um_M1200_2017': _fromnum1("/store/user/tucker/mfv_stopdbardbar_cp2_tau010000um_M1200/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_051213", 100, fnbase="reco"),
'mfv_stopdbardbar_tau010000um_M1600_2017': _fromnum1("/store/user/tucker/mfv_stopdbardbar_cp2_tau010000um_M1600/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_051234", 100, fnbase="reco"),
'mfv_stopdbardbar_tau010000um_M3000_2017': _fromnum1("/store/user/tucker/mfv_stopdbardbar_cp2_tau010000um_M3000/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_051257", 100, fnbase="reco"),
'mfv_stopdbardbar_tau030000um_M0400_2017': _fromnum1("/store/user/tucker/mfv_stopdbardbar_cp2_tau030000um_M0400/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_051325", 100, fnbase="reco"),
'mfv_stopdbardbar_tau030000um_M0600_2017': _fromnum1("/store/user/tucker/mfv_stopdbardbar_cp2_tau030000um_M0600/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_051346", 100, fnbase="reco"),
'mfv_stopdbardbar_tau030000um_M0800_2017': _fromnum1("/store/user/tucker/mfv_stopdbardbar_cp2_tau030000um_M0800/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_051408", 100, fnbase="reco"),
'mfv_stopdbardbar_tau030000um_M1200_2017': _fromnum1("/store/user/tucker/mfv_stopdbardbar_cp2_tau030000um_M1200/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_051431", 100, fnbase="reco"),
'mfv_stopdbardbar_tau030000um_M1600_2017': _fromnum1("/store/user/tucker/mfv_stopdbardbar_cp2_tau030000um_M1600/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_051454", 100, fnbase="reco"),
'mfv_stopdbardbar_tau030000um_M3000_2017': _fromnum1("/store/user/tucker/mfv_stopdbardbar_cp2_tau030000um_M3000/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_051514", 100, fnbase="reco"),
'mfv_stopdbardbar_tau100000um_M0400_2017': _fromnum1("/store/user/tucker/mfv_stopdbardbar_cp2_tau100000um_M0400/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_051539", 100, fnbase="reco"),
'mfv_stopdbardbar_tau100000um_M0600_2017': _fromnum1("/store/user/tucker/mfv_stopdbardbar_cp2_tau100000um_M0600/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_051615", 100, fnbase="reco"),
'mfv_stopdbardbar_tau100000um_M0800_2017': _fromnum1("/store/user/tucker/mfv_stopdbardbar_cp2_tau100000um_M0800/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_051638", 100, fnbase="reco"),
'mfv_stopdbardbar_tau100000um_M1200_2017': _fromnum1("/store/user/tucker/mfv_stopdbardbar_cp2_tau100000um_M1200/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_051659", 100, fnbase="reco"),
'mfv_stopdbardbar_tau100000um_M1600_2017': _fromnum1("/store/user/tucker/mfv_stopdbardbar_cp2_tau100000um_M1600/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_051722", 100, fnbase="reco"),
'mfv_stopdbardbar_tau100000um_M3000_2017': _fromnum1("/store/user/tucker/mfv_stopdbardbar_cp2_tau100000um_M3000/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/181027_051745", 100, fnbase="reco"),
})


_add_ds("miniaod", {
'mfv_neu_tau000100um_M0400_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau000100um_M0400/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_081953", 5, fnbase="miniaod"),
'mfv_neu_tau000100um_M0600_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau000100um_M0600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_081954", 5, fnbase="miniaod"),
'mfv_neu_tau000100um_M0800_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau000100um_M0800/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_081955", 5, fnbase="miniaod"),
'mfv_neu_tau000100um_M1200_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau000100um_M1200/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_081956", 5, fnbase="miniaod"),
'mfv_neu_tau000100um_M1600_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau000100um_M1600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_081957", 5, fnbase="miniaod"),
'mfv_neu_tau000100um_M3000_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau000100um_M3000/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_081958", 5, fnbase="miniaod"),
'mfv_neu_tau000300um_M0400_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau000300um_M0400/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_081959", 5, fnbase="miniaod"),
'mfv_neu_tau000300um_M0600_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau000300um_M0600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082000", 5, fnbase="miniaod"),
'mfv_neu_tau000300um_M0800_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau000300um_M0800/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082001", 5, fnbase="miniaod"),
'mfv_neu_tau000300um_M1200_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau000300um_M1200/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082002", 5, fnbase="miniaod"),
'mfv_neu_tau000300um_M1600_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau000300um_M1600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082003", 5, fnbase="miniaod"),
'mfv_neu_tau000300um_M3000_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau000300um_M3000/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082004", 5, fnbase="miniaod"),
'mfv_neu_tau001000um_M0400_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau001000um_M0400/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082005", 5, fnbase="miniaod"),
'mfv_neu_tau001000um_M0600_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau001000um_M0600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082006", 5, fnbase="miniaod"),
'mfv_neu_tau001000um_M0800_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau001000um_M0800/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082007", 5, fnbase="miniaod"),
'mfv_neu_tau001000um_M1200_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau001000um_M1200/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082008", 5, fnbase="miniaod"),
'mfv_neu_tau001000um_M1600_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau001000um_M1600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082009", 5, fnbase="miniaod"),
'mfv_neu_tau001000um_M3000_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau001000um_M3000/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082010", 5, fnbase="miniaod"),
'mfv_neu_tau010000um_M0400_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau010000um_M0400/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082011", 5, fnbase="miniaod"),
'mfv_neu_tau010000um_M0600_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau010000um_M0600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082012", 5, fnbase="miniaod"),
'mfv_neu_tau010000um_M0800_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau010000um_M0800/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082013", 5, fnbase="miniaod"),
'mfv_neu_tau010000um_M1200_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau010000um_M1200/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082014", 5, fnbase="miniaod"),
'mfv_neu_tau010000um_M1600_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau010000um_M1600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082015", 5, fnbase="miniaod"),
'mfv_neu_tau010000um_M3000_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau010000um_M3000/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082016", 5, fnbase="miniaod"),
'mfv_neu_tau030000um_M0400_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau030000um_M0400/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082017", 5, fnbase="miniaod"),
'mfv_neu_tau030000um_M0600_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau030000um_M0600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082018", 5, fnbase="miniaod"),
'mfv_neu_tau030000um_M0800_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau030000um_M0800/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082019", 5, fnbase="miniaod"),
'mfv_neu_tau030000um_M1200_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau030000um_M1200/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082020", 5, fnbase="miniaod"),
'mfv_neu_tau030000um_M1600_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau030000um_M1600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082021", 5, fnbase="miniaod"),
'mfv_neu_tau030000um_M3000_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau030000um_M3000/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082022", 5, fnbase="miniaod"),
'mfv_neu_tau100000um_M0400_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau100000um_M0400/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082023", 5, fnbase="miniaod"),
'mfv_neu_tau100000um_M0600_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau100000um_M0600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082024", 5, fnbase="miniaod"),
'mfv_neu_tau100000um_M0800_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau100000um_M0800/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082025", 5, fnbase="miniaod"),
'mfv_neu_tau100000um_M1200_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau100000um_M1200/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082026", 5, fnbase="miniaod"),
'mfv_neu_tau100000um_M1600_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau100000um_M1600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082027", 5, fnbase="miniaod"),
'mfv_neu_tau100000um_M3000_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau100000um_M3000/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082028", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau000100um_M0400_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau000100um_M0400/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082029", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau000100um_M0600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau000100um_M0600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082030", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau000100um_M0800_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau000100um_M0800/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082031", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau000100um_M1200_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau000100um_M1200/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082032", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau000100um_M1600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau000100um_M1600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082033", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau000100um_M3000_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau000100um_M3000/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082034", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau000300um_M0400_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau000300um_M0400/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082035", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau000300um_M0600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau000300um_M0600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082036", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau000300um_M0800_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau000300um_M0800/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082037", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau000300um_M1200_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau000300um_M1200/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082038", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau000300um_M1600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau000300um_M1600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082039", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau000300um_M3000_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau000300um_M3000/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082040", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau001000um_M0400_2017': (5, ['/store/user/tucker/mfv_stopdbardbar_cp2_tau001000um_M0400/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082041/0000/miniaod_%i.root' % i for i in chain(xrange(2), xrange(3,5))] + ['/store/user/tucker/mfv_stopdbardbar_cp2_tau001000um_M0400/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_095042/0000/miniaod_2.root']),
'mfv_stopdbardbar_tau001000um_M0600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau001000um_M0600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082042", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau001000um_M0800_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau001000um_M0800/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082043", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau001000um_M1200_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau001000um_M1200/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082044", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau001000um_M1600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau001000um_M1600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082045", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau001000um_M3000_2017': (5, ['/store/user/tucker/mfv_stopdbardbar_cp2_tau001000um_M3000/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082046/0000/miniaod_%i.root' % i for i in xrange(4)] + ['/store/user/tucker/mfv_stopdbardbar_cp2_tau001000um_M3000/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_145804/0000/miniaod_4.root']),
'mfv_stopdbardbar_tau010000um_M0400_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau010000um_M0400/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082047", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau010000um_M0600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau010000um_M0600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082048", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau010000um_M0800_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau010000um_M0800/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082049", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau010000um_M1200_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau010000um_M1200/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082050", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau010000um_M1600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau010000um_M1600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082051", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau010000um_M3000_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau010000um_M3000/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082052", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau030000um_M0400_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau030000um_M0400/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082053", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau030000um_M0600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau030000um_M0600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082054", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau030000um_M0800_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau030000um_M0800/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082055", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau030000um_M1200_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau030000um_M1200/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082056", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau030000um_M1600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau030000um_M1600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082057", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau030000um_M3000_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau030000um_M3000/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082058", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau100000um_M0400_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau100000um_M0400/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082059", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau100000um_M0600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau100000um_M0600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082100", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau100000um_M0800_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau100000um_M0800/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082101", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau100000um_M1200_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau100000um_M1200/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082102", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau100000um_M1600_2017': (5, ['/store/user/tucker/mfv_stopdbardbar_cp2_tau100000um_M1600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_105124/0000/miniaod_0.root'] + ['/store/user/tucker/mfv_stopdbardbar_cp2_tau100000um_M1600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082103/0000/miniaod_%i.root' % i for i in xrange(1,5)]),
'mfv_stopdbardbar_tau100000um_M3000_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau100000um_M3000/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/181029_082104", 5, fnbase="miniaod"),
})


_add_ds("ntuplev21m", {
'qcdht0700_2017': _fromnum1("/store/user/tucker/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/NtupleV21m_2017/181031_190446", 16),
'qcdht1000_2017': _fromnum1("/store/user/tucker/QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8/NtupleV21m_2017/181031_190510", 31),
'qcdht1500_2017': _fromnum0("/store/user/tucker/QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8/NtupleV21m_2017/181031_143853", 63),
'qcdht2000_2017': _fromnum0("/store/user/tucker/QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/NtupleV21m_2017/181031_143854", 30),
'ttbar_2017': _fromnum0("/store/user/tucker/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleV21m_2017/181101_153920", 51),
'mfv_neu_tau000100um_M0400_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau000100um_M0400/NtupleV21m_2017/181031_140740", 50),
'mfv_neu_tau000100um_M0600_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau000100um_M0600/NtupleV21m_2017/181031_140741", 50),
'mfv_neu_tau000100um_M0800_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau000100um_M0800/NtupleV21m_2017/181031_140742", 50),
'mfv_neu_tau000100um_M1200_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau000100um_M1200/NtupleV21m_2017/181031_140743", 50),
'mfv_neu_tau000100um_M1600_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau000100um_M1600/NtupleV21m_2017/181031_140744", 50),
'mfv_neu_tau000100um_M3000_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau000100um_M3000/NtupleV21m_2017/181031_140745", 50),
'mfv_neu_tau000300um_M0400_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau000300um_M0400/NtupleV21m_2017/181031_140746", 50),
'mfv_neu_tau000300um_M0600_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau000300um_M0600/NtupleV21m_2017/181031_140747", 50),
'mfv_neu_tau000300um_M0800_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau000300um_M0800/NtupleV21m_2017/181031_140748", 50),
'mfv_neu_tau000300um_M1200_2017': (50, ['/store/user/tucker/mfv_neu_cp2_tau000300um_M1200/NtupleV21m_2017/181031_140749/0000/ntuple_%i.root' % i for i in xrange(1,50)] + ['/store/user/tucker/mfv_neu_cp2_tau000300um_M1200/NtupleV21m_2017/181031_144925/0000/ntuple_0.root']),
'mfv_neu_tau000300um_M1600_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau000300um_M1600/NtupleV21m_2017/181031_140750", 50),
'mfv_neu_tau000300um_M3000_2017': (50, ['/store/user/tucker/mfv_neu_cp2_tau000300um_M3000/NtupleV21m_2017/181031_144926/0000/ntuple_48.root'] + ['/store/user/tucker/mfv_neu_cp2_tau000300um_M3000/NtupleV21m_2017/181031_140751/0000/ntuple_%i.root' % i for i in chain(xrange(48), [49])]),
'mfv_neu_tau001000um_M0400_2017': (50, ['/store/user/tucker/mfv_neu_cp2_tau001000um_M0400/NtupleV21m_2017/181031_144934/0000/ntuple_5.root'] + ['/store/user/tucker/mfv_neu_cp2_tau001000um_M0400/NtupleV21m_2017/181031_140752/0000/ntuple_%i.root' % i for i in chain(xrange(5), xrange(6,50))]),
'mfv_neu_tau001000um_M0600_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau001000um_M0600/NtupleV21m_2017/181031_140753", 50),
'mfv_neu_tau001000um_M0800_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau001000um_M0800/NtupleV21m_2017/181031_140754", 50),
'mfv_neu_tau001000um_M1200_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau001000um_M1200/NtupleV21m_2017/181031_140755", 50),
'mfv_neu_tau001000um_M1600_2017': (50, ['/store/user/tucker/mfv_neu_cp2_tau001000um_M1600/NtupleV21m_2017/181031_144927/0000/ntuple_38.root'] + ['/store/user/tucker/mfv_neu_cp2_tau001000um_M1600/NtupleV21m_2017/181031_140756/0000/ntuple_%i.root' % i for i in chain(xrange(38), xrange(39,50))]),
'mfv_neu_tau001000um_M3000_2017': (50, ['/store/user/tucker/mfv_neu_cp2_tau001000um_M3000/NtupleV21m_2017/181031_140757/0000/ntuple_%i.root' % i for i in chain(xrange(28), xrange(29,50))] + ['/store/user/tucker/mfv_neu_cp2_tau001000um_M3000/NtupleV21m_2017/181031_231755/0000/ntuple_28.root']),
'mfv_neu_tau010000um_M0400_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau010000um_M0400/NtupleV21m_2017/181031_140758", 50),
'mfv_neu_tau010000um_M0600_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau010000um_M0600/NtupleV21m_2017/181031_140759", 50),
'mfv_neu_tau010000um_M0800_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau010000um_M0800/NtupleV21m_2017/181031_140800", 50),
'mfv_neu_tau010000um_M1200_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau010000um_M1200/NtupleV21m_2017/181031_140801", 50),
'mfv_neu_tau010000um_M1600_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau010000um_M1600/NtupleV21m_2017/181031_140802", 50),
'mfv_neu_tau010000um_M3000_2017': (50, ['/store/user/tucker/mfv_neu_cp2_tau010000um_M3000/NtupleV21m_2017/181031_223155/0000/ntuple_%i.root' % i for i in [8, 14]] + ['/store/user/tucker/mfv_neu_cp2_tau010000um_M3000/NtupleV21m_2017/181031_140803/0000/ntuple_%i.root' % i for i in chain(xrange(8), xrange(9,14), xrange(15,50))]),
'mfv_neu_tau030000um_M0400_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau030000um_M0400/NtupleV21m_2017/181031_140804", 50),
'mfv_neu_tau030000um_M0600_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau030000um_M0600/NtupleV21m_2017/181031_140805", 50),
'mfv_neu_tau030000um_M0800_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau030000um_M0800/NtupleV21m_2017/181031_140806", 50),
'mfv_neu_tau030000um_M1200_2017': (50, ['/store/user/tucker/mfv_neu_cp2_tau030000um_M1200/NtupleV21m_2017/181031_140807/0000/ntuple_%i.root' % i for i in chain(xrange(18), xrange(19,37), xrange(38,50))] + ['/store/user/tucker/mfv_neu_cp2_tau030000um_M1200/NtupleV21m_2017/181031_144927/0000/ntuple_%i.root' % i for i in [18, 37]]),
'mfv_neu_tau030000um_M1600_2017': (50, ['/store/user/tucker/mfv_neu_cp2_tau030000um_M1600/NtupleV21m_2017/181031_140808/0000/ntuple_%i.root' % i for i in chain(xrange(25), xrange(26,28), xrange(29,50))] + ['/store/user/tucker/mfv_neu_cp2_tau030000um_M1600/NtupleV21m_2017/181031_144928/0000/ntuple_%i.root' % i for i in [25, 28]]),
'mfv_neu_tau030000um_M3000_2017': (50, ['/store/user/tucker/mfv_neu_cp2_tau030000um_M3000/NtupleV21m_2017/181031_155733/0000/ntuple_18.root'] + ['/store/user/tucker/mfv_neu_cp2_tau030000um_M3000/NtupleV21m_2017/181031_140809/0000/ntuple_%i.root' % i for i in chain(xrange(18), xrange(19,50))]),
'mfv_neu_tau100000um_M0400_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau100000um_M0400/NtupleV21m_2017/181031_140810", 50),
'mfv_neu_tau100000um_M0600_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau100000um_M0600/NtupleV21m_2017/181031_140811", 50),
'mfv_neu_tau100000um_M0800_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau100000um_M0800/NtupleV21m_2017/181031_140812", 50),
'mfv_neu_tau100000um_M1200_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau100000um_M1200/NtupleV21m_2017/181031_140813", 50),
'mfv_neu_tau100000um_M1600_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau100000um_M1600/NtupleV21m_2017/181031_140814", 50),
'mfv_neu_tau100000um_M3000_2017': _fromnum0("/store/user/tucker/mfv_neu_cp2_tau100000um_M3000/NtupleV21m_2017/181031_140815", 50),
'mfv_stopdbardbar_tau000100um_M0400_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau000100um_M0400/NtupleV21m_2017/181031_140816", 50),
'mfv_stopdbardbar_tau000100um_M0600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau000100um_M0600/NtupleV21m_2017/181031_140817", 50),
'mfv_stopdbardbar_tau000100um_M0800_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau000100um_M0800/NtupleV21m_2017/181031_140818", 50),
'mfv_stopdbardbar_tau000100um_M1200_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau000100um_M1200/NtupleV21m_2017/181031_140819", 50),
'mfv_stopdbardbar_tau000100um_M1600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau000100um_M1600/NtupleV21m_2017/181031_140820", 50),
'mfv_stopdbardbar_tau000100um_M3000_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau000100um_M3000/NtupleV21m_2017/181031_140821", 50),
'mfv_stopdbardbar_tau000300um_M0400_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau000300um_M0400/NtupleV21m_2017/181031_140822", 50),
'mfv_stopdbardbar_tau000300um_M0600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau000300um_M0600/NtupleV21m_2017/181031_140823", 50),
'mfv_stopdbardbar_tau000300um_M0800_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau000300um_M0800/NtupleV21m_2017/181031_140824", 50),
'mfv_stopdbardbar_tau000300um_M1200_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau000300um_M1200/NtupleV21m_2017/181031_140825", 50),
'mfv_stopdbardbar_tau000300um_M1600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau000300um_M1600/NtupleV21m_2017/181031_140826", 50),
'mfv_stopdbardbar_tau000300um_M3000_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau000300um_M3000/NtupleV21m_2017/181031_140827", 50),
'mfv_stopdbardbar_tau001000um_M0400_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau001000um_M0400/NtupleV21m_2017/181031_140828", 50),
'mfv_stopdbardbar_tau001000um_M0600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau001000um_M0600/NtupleV21m_2017/181031_140829", 50),
'mfv_stopdbardbar_tau001000um_M0800_2017': (50, ['/store/user/tucker/mfv_stopdbardbar_cp2_tau001000um_M0800/NtupleV21m_2017/181031_144929/0000/ntuple_37.root'] + ['/store/user/tucker/mfv_stopdbardbar_cp2_tau001000um_M0800/NtupleV21m_2017/181031_140830/0000/ntuple_%i.root' % i for i in chain(xrange(37), xrange(38,50))]),
'mfv_stopdbardbar_tau001000um_M1200_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau001000um_M1200/NtupleV21m_2017/181031_140831", 50),
'mfv_stopdbardbar_tau001000um_M1600_2017': (50, ['/store/user/tucker/mfv_stopdbardbar_cp2_tau001000um_M1600/NtupleV21m_2017/181031_140832/0000/ntuple_%i.root' % i for i in chain(xrange(37), xrange(38,50))] + ['/store/user/tucker/mfv_stopdbardbar_cp2_tau001000um_M1600/NtupleV21m_2017/181031_164954/0000/ntuple_37.root']),
'mfv_stopdbardbar_tau001000um_M3000_2017': (50, ['/store/user/tucker/mfv_stopdbardbar_cp2_tau001000um_M3000/NtupleV21m_2017/181031_163515/0000/ntuple_47.root'] + ['/store/user/tucker/mfv_stopdbardbar_cp2_tau001000um_M3000/NtupleV21m_2017/181031_191907/0000/ntuple_%i.root' % i for i in [14, 18]] + ['/store/user/tucker/mfv_stopdbardbar_cp2_tau001000um_M3000/NtupleV21m_2017/181031_140833/0000/ntuple_%i.root' % i for i in chain(xrange(8), xrange(9,14), xrange(15,18), xrange(19,31), xrange(32,47), xrange(48,50))] + ['/store/user/tucker/mfv_stopdbardbar_cp2_tau001000um_M3000/NtupleV21m_2017/181031_172516/0000/ntuple_31.root'] + ['/store/user/tucker/mfv_stopdbardbar_cp2_tau001000um_M3000/NtupleV21m_2017/181101_081912/0000/ntuple_8.root']),
'mfv_stopdbardbar_tau010000um_M0400_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau010000um_M0400/NtupleV21m_2017/181031_140834", 50),
'mfv_stopdbardbar_tau010000um_M0600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau010000um_M0600/NtupleV21m_2017/181031_140835", 50),
'mfv_stopdbardbar_tau010000um_M0800_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau010000um_M0800/NtupleV21m_2017/181031_140836", 50),
'mfv_stopdbardbar_tau010000um_M1200_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau010000um_M1200/NtupleV21m_2017/181031_140837", 50),
'mfv_stopdbardbar_tau010000um_M1600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau010000um_M1600/NtupleV21m_2017/181031_140838", 50),
'mfv_stopdbardbar_tau010000um_M3000_2017': (50, ['/store/user/tucker/mfv_stopdbardbar_cp2_tau010000um_M3000/NtupleV21m_2017/181031_140839/0000/ntuple_%i.root' % i for i in chain(xrange(29), xrange(30,44), xrange(45,50))] + ['/store/user/tucker/mfv_stopdbardbar_cp2_tau010000um_M3000/NtupleV21m_2017/181031_191908/0000/ntuple_29.root'] + ['/store/user/tucker/mfv_stopdbardbar_cp2_tau010000um_M3000/NtupleV21m_2017/181031_231756/0000/ntuple_44.root']),
'mfv_stopdbardbar_tau030000um_M0400_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau030000um_M0400/NtupleV21m_2017/181031_140840", 50),
'mfv_stopdbardbar_tau030000um_M0600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau030000um_M0600/NtupleV21m_2017/181031_140841", 50),
'mfv_stopdbardbar_tau030000um_M0800_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau030000um_M0800/NtupleV21m_2017/181031_140842", 50),
'mfv_stopdbardbar_tau030000um_M1200_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau030000um_M1200/NtupleV21m_2017/181031_140843", 50),
'mfv_stopdbardbar_tau030000um_M1600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau030000um_M1600/NtupleV21m_2017/181031_140844", 50),
'mfv_stopdbardbar_tau030000um_M3000_2017': (50, ['/store/user/tucker/mfv_stopdbardbar_cp2_tau030000um_M3000/NtupleV21m_2017/181031_151110/0000/ntuple_37.root'] + ['/store/user/tucker/mfv_stopdbardbar_cp2_tau030000um_M3000/NtupleV21m_2017/181031_191909/0000/ntuple_43.root'] + ['/store/user/tucker/mfv_stopdbardbar_cp2_tau030000um_M3000/NtupleV21m_2017/181031_140845/0000/ntuple_%i.root' % i for i in chain(xrange(37), xrange(38,43), xrange(44,50))]),
'mfv_stopdbardbar_tau100000um_M0400_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau100000um_M0400/NtupleV21m_2017/181031_140846", 50),
'mfv_stopdbardbar_tau100000um_M0600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau100000um_M0600/NtupleV21m_2017/181031_140847", 50),
'mfv_stopdbardbar_tau100000um_M0800_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau100000um_M0800/NtupleV21m_2017/181031_140848", 50),
'mfv_stopdbardbar_tau100000um_M1200_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau100000um_M1200/NtupleV21m_2017/181031_140849", 50),
'mfv_stopdbardbar_tau100000um_M1600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau100000um_M1600/NtupleV21m_2017/181031_140850", 50),
'mfv_stopdbardbar_tau100000um_M3000_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_cp2_tau100000um_M3000/NtupleV21m_2017/181031_140851", 50),
'JetHT2017B': _fromnum1("/store/user/tucker/JetHT/NtupleV21m_2017/181031_190619", 25),
'JetHT2017C': _fromnum1("/store/user/tucker/JetHT/NtupleV21m_2017/181031_190639", 38),
'JetHT2017D': _fromnum1("/store/user/tucker/JetHT/NtupleV21m_2017/181031_190658", 18),
'JetHT2017E': _fromnum1("/store/user/tucker/JetHT/NtupleV21m_2017/181031_190719", 42),
'JetHT2017F': _fromnum1("/store/user/tucker/JetHT/NtupleV21m_2017/181031_190738", 51),
'JetHT2018A1': _fromnum1("/store/user/tucker/JetHT/NtupleV21m_2018/181031_192223", 58),
'JetHT2018A2': _fromnum1("/store/user/tucker/JetHT/NtupleV21m_2018/181031_192237", 12),
'JetHT2018A3': _fromnum1("/store/user/tucker/JetHT/NtupleV21m_2018/181031_192255", 25),
'JetHT2018B1': _fromnum1("/store/user/tucker/JetHT/NtupleV21m_2018/181031_192315", 43),
'JetHT2018B2': _fromnum1("/store/user/tucker/JetHT/NtupleV21m_2018/181031_192336", 4),
'JetHT2018C1': _fromnum1("/store/user/tucker/JetHT/NtupleV21m_2018/181031_192350", 3),
'JetHT2018C2': _fromnum1("/store/user/tucker/JetHT/NtupleV21m_2018/181031_192406", 18),
'JetHT2018C3': _fromnum1("/store/user/tucker/JetHT/NtupleV21m_2018/181031_192422", 19),
'JetHT2018D2': _fromnum1("/store/user/tucker/JetHT/NtupleV21m_2018/181031_192438", 206),
})


_add_ds("ntuplev21m_ntkseeds", {
'qcdht0700_2017': _fromnum1("/store/user/tucker/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/NtupleV21m_NTkSeeds_2017/181101_203532", 16, fnbase="ntkseeds"),
'qcdht1000_2017': _fromnum1("/store/user/tucker/QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8/NtupleV21m_NTkSeeds_2017/181101_203559", 31, fnbase="ntkseeds"),
'qcdht1500_2017': _fromnum0("/store/user/tucker/QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8/NtupleV21m_NTkSeeds_2017/181101_153818", 63, fnbase="ntkseeds"),
'qcdht2000_2017': _fromnum0("/store/user/tucker/QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/NtupleV21m_NTkSeeds_2017/181101_153819", 30, fnbase="ntkseeds"),
'ttbar_2017': _fromnum0("/store/user/tucker/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleV21m_NTkSeeds_2017/181101_153817", 51, fnbase="ntkseeds"),
'JetHT2017B': _fromnum1("/store/user/tucker/JetHT/NtupleV21m_NTkSeeds_2017/181101_203624", 25, fnbase="ntkseeds"),
'JetHT2017C': _fromnum1("/store/user/tucker/JetHT/NtupleV21m_NTkSeeds_2017/181101_203710", 38, fnbase="ntkseeds"),
'JetHT2017D': _fromnum1("/store/user/tucker/JetHT/NtupleV21m_NTkSeeds_2017/181101_203730", 18, fnbase="ntkseeds"),
'JetHT2017E': _fromnum1("/store/user/tucker/JetHT/NtupleV21m_NTkSeeds_2017/181101_203749", 42, fnbase="ntkseeds"),
'JetHT2017F': _fromnum1("/store/user/tucker/JetHT/NtupleV21m_NTkSeeds_2017/181101_203815", 51, fnbase="ntkseeds"),
'JetHT2018A1': _fromnum1("/store/user/tucker/JetHT/NtupleV21m_NTkSeeds_2018/181101_204136", 58, fnbase="ntkseeds"),
'JetHT2018A2': _fromnum1("/store/user/tucker/JetHT/NtupleV21m_NTkSeeds_2018/181101_204154", 12, fnbase="ntkseeds"),
'JetHT2018A3': _fromnum1("/store/user/tucker/JetHT/NtupleV21m_NTkSeeds_2018/181101_204211", 25, fnbase="ntkseeds"),
'JetHT2018B1': _fromnum1("/store/user/tucker/JetHT/NtupleV21m_NTkSeeds_2018/181101_204229", 43, fnbase="ntkseeds"),
'JetHT2018B2': _fromnum1("/store/user/tucker/JetHT/NtupleV21m_NTkSeeds_2018/181101_204244", 4, fnbase="ntkseeds"),
'JetHT2018C1': _fromnum1("/store/user/tucker/JetHT/NtupleV21m_NTkSeeds_2018/181101_204311", 3, fnbase="ntkseeds"),
'JetHT2018C2': _fromnum1("/store/user/tucker/JetHT/NtupleV21m_NTkSeeds_2018/181101_204325", 18, fnbase="ntkseeds"),
'JetHT2018C3': _fromnum1("/store/user/tucker/JetHT/NtupleV21m_NTkSeeds_2018/181101_204342", 19, fnbase="ntkseeds"),
'JetHT2018D2': _fromnum1("/store/user/tucker/JetHT/NtupleV21m_NTkSeeds_2018/181101_204401", 207, fnbase="ntkseeds"),
})


_add_ds("ntuplev20m", {
'JetHT2017B': _fromnum1("/store/user/tucker/JetHT/NtupleV20m_2017/180925_201903", 513),
'JetHT2017C': _fromnum1("/store/user/tucker/JetHT/NtupleV20m_2017/180925_201922", 777),
'JetHT2017D': _fromnum1("/store/user/tucker/JetHT/NtupleV20m_2017/180925_201941", 372),
'JetHT2017E': _fromnum1("/store/user/tucker/JetHT/NtupleV20m_2017/180925_202003", 724),
'JetHT2017F': _fromnum1("/store/user/tucker/JetHT/NtupleV20m_2017/180925_202026", 931),
'qcdht0700_2017': _frommerge("/store/user/tucker/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/NtupleV20m_merge_2017/180810_090200/0000/merge",  3),
'qcdht1000_2017': _frommerge("/store/user/tucker/QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8/NtupleV20m_merge_2017/180810_090201/0000/merge", 12),
'qcdht1500_2017': _frommerge("/store/user/tucker/QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8/NtupleV20m_merge_2017/180810_090202/0000/merge", 25),
'qcdht2000_2017': _frommerge("/store/user/tucker/QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/NtupleV20m_merge_2017/180810_090203/0000/merge", 15),
'ttbar_2017': _fromnum1("/store/user/tucker/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleV20m_2017/180808_064546", 308),
'wjetstolnu_2017': _frommerge("/store/user/tucker/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV20m_merge_2017/180810_090204/0000/merge", 1),
'dyjetstollM10_2017': _frommerge("/store/user/tucker/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV20m_merge_2017/180810_090205/0000/merge", 1),
'dyjetstollM50_2017': _frommerge("/store/user/tucker/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleV20m_merge_2017/180810_090206/0000/merge", 2),
'qcdmupt15_2017': _frommerge("/store/user/tucker/QCD_Pt-20toInf_MuEnrichedPt15_TuneCP5_13TeV_pythia8/NtupleV20m_merge_2017/180810_090207/0000/merge", 1),
'qcdempt015_2017': _frommerge("/store/user/tucker/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV_pythia8/NtupleV20m_merge_2017/180810_090208/0000/merge", 1),
'qcdempt020_2017': _frommerge("/store/user/tucker/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV_pythia8/NtupleV20m_merge_2017/180810_090209/0000/merge", 1),
'qcdempt030_2017': _frommerge("/store/user/tucker/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV_pythia8/NtupleV20m_merge_2017/180810_090210/0000/merge", 1),
'qcdempt050_2017': _frommerge("/store/user/tucker/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV_pythia8/NtupleV20m_merge_2017/180810_090211/0000/merge", 1),
'qcdempt080_2017': _frommerge("/store/user/tucker/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV_pythia8/NtupleV20m_merge_2017/180810_090212/0000/merge", 1),
'qcdempt120_2017': _frommerge("/store/user/tucker/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV_pythia8/NtupleV20m_merge_2017/180810_090213/0000/merge", 1),
'qcdempt170_2017': _frommerge("/store/user/tucker/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV_pythia8/NtupleV20m_merge_2017/180810_090214/0000/merge", 1),
'qcdempt300_2017': _frommerge("/store/user/tucker/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV_pythia8/NtupleV20m_merge_2017/180810_090215/0000/merge", 1),
'qcdbctoept015_2017': _frommerge("/store/user/tucker/QCD_Pt_15to20_bcToE_TuneCP5_13TeV_pythia8/NtupleV20m_merge_2017/180810_090216/0000/merge", 1),
'qcdbctoept020_2017': _frommerge("/store/user/tucker/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/NtupleV20m_merge_2017/180810_090217/0000/merge", 1),
'qcdbctoept030_2017': _frommerge("/store/user/tucker/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/NtupleV20m_merge_2017/180810_090218/0000/merge", 1),
'qcdbctoept080_2017': _frommerge("/store/user/tucker/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/NtupleV20m_merge_2017/180810_090219/0000/merge", 1),
'qcdbctoept170_2017': _frommerge("/store/user/tucker/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/NtupleV20m_merge_2017/180810_090220/0000/merge", 1),
'qcdbctoept250_2017': _frommerge("/store/user/tucker/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/NtupleV20m_merge_2017/180810_090221/0000/merge", 4),
})


_add_ds("ntuplev20m_ntkseeds", {
'qcdht0700_2017': _fromnum1("/store/user/tucker/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/NtupleV20m_NTkSeeds_2017/180919_182021", 199, fnbase="ntkseeds"),
'qcdht1000_2017': _fromnum1("/store/user/tucker/QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8/NtupleV20m_NTkSeeds_2017/180919_182039", 883, fnbase="ntkseeds"),
'qcdht1500_2017': _fromnum1("/store/user/tucker/QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8/NtupleV20m_NTkSeeds_2017/180919_182058", 780, fnbase="ntkseeds"),
'qcdht2000_2017': _fromnum1("/store/user/tucker/QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/NtupleV20m_NTkSeeds_2017/180919_182117", 361, fnbase="ntkseeds"),
'ttbar_2017': _fromnum1("/store/user/tucker/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleV20m_NTkSeeds_2017/180919_181958", 308, fnbase="ntkseeds"),
'wjetstolnu_2017': _fromnum1("/store/user/tucker/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV20m_NTkSeeds_2017/180919_182136", 197, fnbase="ntkseeds"),
'dyjetstollM10_2017': _fromnum1("/store/user/tucker/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV20m_NTkSeeds_2017/180919_182154", 312, fnbase="ntkseeds"),
'dyjetstollM50_2017': _fromnum1("/store/user/tucker/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleV20m_NTkSeeds_2017/180919_182213", 216, fnbase="ntkseeds"),
'qcdmupt15_2017': _fromnum1("/store/user/tucker/QCD_Pt-20toInf_MuEnrichedPt15_TuneCP5_13TeV_pythia8/NtupleV20m_NTkSeeds_2017/180919_182232", 137, fnbase="ntkseeds"),
'qcdempt015_2017': _fromnum1("/store/user/tucker/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV_pythia8/NtupleV20m_NTkSeeds_2017/180919_182251", 89, fnbase="ntkseeds"),
'qcdempt020_2017': _fromnum1("/store/user/tucker/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV_pythia8/NtupleV20m_NTkSeeds_2017/180919_182309", 93, fnbase="ntkseeds"),
'qcdempt030_2017': _fromnum1("/store/user/tucker/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV_pythia8/NtupleV20m_NTkSeeds_2017/180919_182328", 118, fnbase="ntkseeds"),
'qcdempt050_2017': _fromnum1("/store/user/tucker/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV_pythia8/NtupleV20m_NTkSeeds_2017/180919_182347", 86, fnbase="ntkseeds"),
'qcdempt080_2017': _fromnum1("/store/user/tucker/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV_pythia8/NtupleV20m_NTkSeeds_2017/180919_182411", 68, fnbase="ntkseeds"),
'qcdempt120_2017': _fromnum1("/store/user/tucker/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV_pythia8/NtupleV20m_NTkSeeds_2017/180919_182433", 71, fnbase="ntkseeds"),
'qcdempt170_2017': _fromnum1("/store/user/tucker/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV_pythia8/NtupleV20m_NTkSeeds_2017/180919_182451", 29, fnbase="ntkseeds"),
'qcdempt300_2017': _fromnum1("/store/user/tucker/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV_pythia8/NtupleV20m_NTkSeeds_2017/180919_182510", 24, fnbase="ntkseeds"),
'qcdbctoept015_2017': _fromnum1("/store/user/tucker/QCD_Pt_15to20_bcToE_TuneCP5_13TeV_pythia8/NtupleV20m_NTkSeeds_2017/180919_182529", 18, fnbase="ntkseeds"),
'qcdbctoept020_2017': _fromnum1("/store/user/tucker/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/NtupleV20m_NTkSeeds_2017/180919_182550", 83, fnbase="ntkseeds"),
'qcdbctoept030_2017': _fromnum1("/store/user/tucker/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/NtupleV20m_NTkSeeds_2017/180919_182609", 129, fnbase="ntkseeds"),
'qcdbctoept080_2017': _fromnum1("/store/user/tucker/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/NtupleV20m_NTkSeeds_2017/180919_182627", 129, fnbase="ntkseeds"),
'qcdbctoept170_2017': _fromnum1("/store/user/tucker/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/NtupleV20m_NTkSeeds_2017/180919_182646", 79, fnbase="ntkseeds"),
'qcdbctoept250_2017': _fromnum1("/store/user/tucker/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/NtupleV20m_NTkSeeds_2017/180919_182706", 80, fnbase="ntkseeds"),
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
