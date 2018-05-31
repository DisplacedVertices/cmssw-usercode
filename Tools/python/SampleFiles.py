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
'mfv_neu_tau000100um_M0400_2017': _fromnum1("/store/user/tucker/mfv_neu_tau000100um_M0400/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180430_161307", 100, fnbase="reco"),
'mfv_neu_tau000100um_M0600_2017': _fromnum1("/store/user/tucker/mfv_neu_tau000100um_M0600/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180430_161327", 100, fnbase="reco"),
'mfv_neu_tau000100um_M0800_2017': _fromnum1("/store/user/tucker/mfv_neu_tau000100um_M0800/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180430_161348", 100, fnbase="reco"),
'mfv_neu_tau000100um_M1200_2017': _fromnum1("/store/user/tucker/mfv_neu_tau000100um_M1200/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180430_161409", 100, fnbase="reco"),
'mfv_neu_tau000100um_M1600_2017': _fromnum1("/store/user/tucker/mfv_neu_tau000100um_M1600/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180430_161429", 100, fnbase="reco"),
'mfv_neu_tau000100um_M3000_2017': _fromnum1("/store/user/tucker/mfv_neu_tau000100um_M3000/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180430_161449", 100, fnbase="reco"),
'mfv_neu_tau000300um_M0400_2017': _fromnum1("/store/user/tucker/mfv_neu_tau000300um_M0400/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180430_161508", 100, fnbase="reco"),
'mfv_neu_tau000300um_M0600_2017': _fromnum1("/store/user/tucker/mfv_neu_tau000300um_M0600/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180430_161528", 100, fnbase="reco"),
'mfv_neu_tau000300um_M0800_2017': _fromnum1("/store/user/tucker/mfv_neu_tau000300um_M0800/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180430_161548", 100, fnbase="reco"),
'mfv_neu_tau000300um_M1200_2017': _fromnum1("/store/user/tucker/mfv_neu_tau000300um_M1200/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180430_161608", 100, fnbase="reco"),
'mfv_neu_tau000300um_M1600_2017': _fromnum1("/store/user/tucker/mfv_neu_tau000300um_M1600/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180430_161629", 100, fnbase="reco"),
'mfv_neu_tau000300um_M3000_2017': _fromnum1("/store/user/tucker/mfv_neu_tau000300um_M3000/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180430_161650", 100, fnbase="reco"),
'mfv_neu_tau001000um_M0400_2017': _fromnum1("/store/user/tucker/mfv_neu_tau001000um_M0400/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180430_161710", 100, fnbase="reco"),
'mfv_neu_tau001000um_M0600_2017': _fromnum1("/store/user/tucker/mfv_neu_tau001000um_M0600/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180430_161733", 100, fnbase="reco"),
'mfv_neu_tau001000um_M0800_2017': _fromnum1("/store/user/tucker/mfv_neu_tau001000um_M0800/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180425_114726", 100, fnbase="reco"),
'mfv_neu_tau001000um_M1200_2017': _fromnum1("/store/user/tucker/mfv_neu_tau001000um_M1200/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180430_161754", 100, fnbase="reco"),
'mfv_neu_tau001000um_M1600_2017': _fromnum1("/store/user/tucker/mfv_neu_tau001000um_M1600/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180430_161815", 100, fnbase="reco", but=[48]),
'mfv_neu_tau001000um_M3000_2017': _fromnum1("/store/user/tucker/mfv_neu_tau001000um_M3000/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180430_161837", 100, fnbase="reco"),
'mfv_neu_tau010000um_M0400_2017': _fromnum1("/store/user/tucker/mfv_neu_tau010000um_M0400/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180430_161856", 100, fnbase="reco"),
'mfv_neu_tau010000um_M0600_2017': _fromnum1("/store/user/tucker/mfv_neu_tau010000um_M0600/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180430_161915", 100, fnbase="reco"),
'mfv_neu_tau010000um_M0800_2017': _fromnum1("/store/user/tucker/mfv_neu_tau010000um_M0800/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180430_161934", 100, fnbase="reco"),
'mfv_neu_tau010000um_M1200_2017': _fromnum1("/store/user/tucker/mfv_neu_tau010000um_M1200/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180430_161954", 100, fnbase="reco"),
'mfv_neu_tau010000um_M1600_2017': _fromnum1("/store/user/tucker/mfv_neu_tau010000um_M1600/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180430_162014", 100, fnbase="reco"),
'mfv_neu_tau010000um_M3000_2017': _fromnum1("/store/user/tucker/mfv_neu_tau010000um_M3000/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180430_162042", 100, fnbase="reco"),
'mfv_neu_tau030000um_M0400_2017': _fromnum1("/store/user/tucker/mfv_neu_tau030000um_M0400/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180430_162103", 100, fnbase="reco"),
'mfv_neu_tau030000um_M0600_2017': _fromnum1("/store/user/tucker/mfv_neu_tau030000um_M0600/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180430_162123", 100, fnbase="reco"),
'mfv_neu_tau030000um_M0800_2017': _fromnum1("/store/user/tucker/mfv_neu_tau030000um_M0800/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180430_162143", 100, fnbase="reco"),
'mfv_neu_tau030000um_M1200_2017': _fromnum1("/store/user/tucker/mfv_neu_tau030000um_M1200/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180430_162207", 100, fnbase="reco"),
'mfv_neu_tau030000um_M1600_2017': _fromnum1("/store/user/tucker/mfv_neu_tau030000um_M1600/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180430_162226", 100, fnbase="reco"),
'mfv_neu_tau030000um_M3000_2017': _fromnum1("/store/user/tucker/mfv_neu_tau030000um_M3000/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180430_162245", 100, fnbase="reco"),
'mfv_neu_tau100000um_M0400_2017': _fromnum1("/store/user/tucker/mfv_neu_tau100000um_M0400/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180430_162304", 100, fnbase="reco"),
'mfv_neu_tau100000um_M0600_2017': _fromnum1("/store/user/tucker/mfv_neu_tau100000um_M0600/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180430_162331", 100, fnbase="reco"),
'mfv_neu_tau100000um_M0800_2017': _fromnum1("/store/user/tucker/mfv_neu_tau100000um_M0800/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180430_162350", 100, fnbase="reco"),
'mfv_neu_tau100000um_M1200_2017': _fromnum1("/store/user/tucker/mfv_neu_tau100000um_M1200/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180430_162409", 100, fnbase="reco"),
'mfv_neu_tau100000um_M1600_2017': _fromnum1("/store/user/tucker/mfv_neu_tau100000um_M1600/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180430_162429", 100, fnbase="reco"),
'mfv_neu_tau100000um_M3000_2017': _fromnum1("/store/user/tucker/mfv_neu_tau100000um_M3000/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180430_162449", 100, fnbase="reco"),

'mfv_stopdbardbar_tau000100um_M0400_2017': (100, ['/store/user/tucker/mfv_stopdbardbar_tau000100um_M0400/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180530_110343/0000/reco_96.root'] + ['/store/user/tucker/mfv_stopdbardbar_tau000100um_M0400/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180528_124501/0000/reco_%i.root' % i for i in chain(xrange(96), xrange(97,100))]),
'mfv_stopdbardbar_tau000100um_M0600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_tau000100um_M0600/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180528_124510", 100, fnbase="reco"),
'mfv_stopdbardbar_tau000100um_M0800_2017': (100, ['/store/user/tucker/mfv_stopdbardbar_tau000100um_M0800/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180528_124514/0000/reco_%i.root' % i for i in chain(xrange(47), xrange(48,61), xrange(62,100))] + ['/store/user/tucker/mfv_stopdbardbar_tau000100um_M0800/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180530_110346/0000/reco_61.root'] + ['/store/user/tucker/mfv_stopdbardbar_tau000100um_M0800/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180530_110428/0000/reco_47.root']),
'mfv_stopdbardbar_tau000100um_M1200_2017': (100, ['/store/user/tucker/mfv_stopdbardbar_tau000100um_M1200/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180528_124518/0000/reco_%i.root' % i for i in chain(xrange(23), xrange(24,53), xrange(54,63), xrange(64,87), xrange(88,100))] + ['/store/user/tucker/mfv_stopdbardbar_tau000100um_M1200/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180529_184802/0000/reco_%i.root' % i for i in [23, 53, 63, 87]]),
'mfv_stopdbardbar_tau000100um_M1600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_tau000100um_M1600/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180528_124535", 100, fnbase="reco"),
'mfv_stopdbardbar_tau000100um_M3000_2017': (100, ['/store/user/tucker/mfv_stopdbardbar_tau000100um_M3000/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180530_110347/0000/reco_60.root'] + ['/store/user/tucker/mfv_stopdbardbar_tau000100um_M3000/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180528_124540/0000/reco_%i.root' % i for i in chain(xrange(60), xrange(61,100))]),
'mfv_stopdbardbar_tau000300um_M0400_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_tau000300um_M0400/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180528_124544", 100, fnbase="reco"),
'mfv_stopdbardbar_tau000300um_M0600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_tau000300um_M0600/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180528_124549", 100, fnbase="reco"),
'mfv_stopdbardbar_tau000300um_M0800_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_tau000300um_M0800/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180528_124554", 100, fnbase="reco"),
'mfv_stopdbardbar_tau000300um_M1200_2017': (100, ['/store/user/tucker/mfv_stopdbardbar_tau000300um_M1200/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180530_110348/0000/reco_35.root'] + ['/store/user/tucker/mfv_stopdbardbar_tau000300um_M1200/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180528_124559/0000/reco_%i.root' % i for i in chain(xrange(35), xrange(36,100))]),
'mfv_stopdbardbar_tau000300um_M1600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_tau000300um_M1600/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180528_124604", 100, fnbase="reco"),
'mfv_stopdbardbar_tau000300um_M3000_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_tau000300um_M3000/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180528_124608", 100, fnbase="reco"),
'mfv_stopdbardbar_tau001000um_M0400_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_tau001000um_M0400/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180528_124614", 100, fnbase="reco"),
'mfv_stopdbardbar_tau001000um_M0600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_tau001000um_M0600/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180528_124618", 100, fnbase="reco"),
'mfv_stopdbardbar_tau001000um_M0800_2017': (100, ['/store/user/tucker/mfv_stopdbardbar_tau001000um_M0800/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180530_110350/0000/reco_44.root'] + ['/store/user/tucker/mfv_stopdbardbar_tau001000um_M0800/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180528_124623/0000/reco_%i.root' % i for i in chain(xrange(44), xrange(45,100))]),
'mfv_stopdbardbar_tau001000um_M1200_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_tau001000um_M1200/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180528_124627", 100, fnbase="reco"),
'mfv_stopdbardbar_tau001000um_M1600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_tau001000um_M1600/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180528_124632", 100, fnbase="reco"),
'mfv_stopdbardbar_tau001000um_M3000_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_tau001000um_M3000/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180528_124636", 100, fnbase="reco"),
'mfv_stopdbardbar_tau010000um_M0400_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_tau010000um_M0400/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180528_124640", 100, fnbase="reco"),
'mfv_stopdbardbar_tau010000um_M0600_2017': (100, ['/store/user/tucker/mfv_stopdbardbar_tau010000um_M0600/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180528_124644/0000/reco_%i.root' % i for i in chain(xrange(25), xrange(26,100))] + ['/store/user/tucker/mfv_stopdbardbar_tau010000um_M0600/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180530_110350/0000/reco_25.root']),
'mfv_stopdbardbar_tau010000um_M0800_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_tau010000um_M0800/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180528_124649", 100, fnbase="reco"),
'mfv_stopdbardbar_tau010000um_M1200_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_tau010000um_M1200/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180528_124658", 100, fnbase="reco"),
'mfv_stopdbardbar_tau010000um_M1600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_tau010000um_M1600/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180528_124704", 100, fnbase="reco"),
'mfv_stopdbardbar_tau010000um_M3000_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_tau010000um_M3000/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180528_124708", 100, fnbase="reco"),
'mfv_stopdbardbar_tau030000um_M0400_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_tau030000um_M0400/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180528_124712", 100, fnbase="reco"),
'mfv_stopdbardbar_tau030000um_M0600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_tau030000um_M0600/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180528_124716", 100, fnbase="reco"),
'mfv_stopdbardbar_tau030000um_M0800_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_tau030000um_M0800/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180528_124720", 100, fnbase="reco"),
'mfv_stopdbardbar_tau030000um_M1200_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_tau030000um_M1200/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180528_124724", 100, fnbase="reco"),
'mfv_stopdbardbar_tau030000um_M1600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_tau030000um_M1600/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180528_124729", 100, fnbase="reco"),
'mfv_stopdbardbar_tau030000um_M3000_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_tau030000um_M3000/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180528_124733", 100, fnbase="reco"),
'mfv_stopdbardbar_tau100000um_M0400_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_tau100000um_M0400/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180528_124738", 100, fnbase="reco"),
'mfv_stopdbardbar_tau100000um_M0600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_tau100000um_M0600/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180528_124742", 100, fnbase="reco"),
'mfv_stopdbardbar_tau100000um_M0800_2017': (100, ['/store/user/tucker/mfv_stopdbardbar_tau100000um_M0800/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180530_110352/0000/reco_63.root'] + ['/store/user/tucker/mfv_stopdbardbar_tau100000um_M0800/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180528_124746/0000/reco_%i.root' % i for i in chain(xrange(63), xrange(64,100))]),
'mfv_stopdbardbar_tau100000um_M1200_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_tau100000um_M1200/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180528_124751", 100, fnbase="reco"),
'mfv_stopdbardbar_tau100000um_M1600_2017': (100, ['/store/user/tucker/mfv_stopdbardbar_tau100000um_M1600/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180528_124754/0000/reco_%i.root' % i for i in chain(xrange(95), xrange(96,100))] + ['/store/user/tucker/mfv_stopdbardbar_tau100000um_M1600/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180530_110353/0000/reco_95.root']),
'mfv_stopdbardbar_tau100000um_M3000_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_tau100000um_M3000/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180528_124758", 100, fnbase="reco"),
})

_add_ds("miniaod", {
'mfv_neu_tau000100um_M0400_2017': _fromnum0("/store/user/tucker/mfv_neu_tau000100um_M0400/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180504_131526", 5, fnbase="miniaod"),
'mfv_neu_tau000100um_M0600_2017': _fromnum0("/store/user/tucker/mfv_neu_tau000100um_M0600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180504_131527", 5, fnbase="miniaod"),
'mfv_neu_tau000100um_M0800_2017': _fromnum0("/store/user/tucker/mfv_neu_tau000100um_M0800/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180504_131528", 5, fnbase="miniaod"),
'mfv_neu_tau000100um_M1200_2017': _fromnum0("/store/user/tucker/mfv_neu_tau000100um_M1200/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180504_131529", 5, fnbase="miniaod"),
'mfv_neu_tau000100um_M1600_2017': _fromnum0("/store/user/tucker/mfv_neu_tau000100um_M1600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180504_131530", 5, fnbase="miniaod"),
'mfv_neu_tau000100um_M3000_2017': _fromnum0("/store/user/tucker/mfv_neu_tau000100um_M3000/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180504_131531", 5, fnbase="miniaod"),
'mfv_neu_tau000300um_M0400_2017': _fromnum0("/store/user/tucker/mfv_neu_tau000300um_M0400/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180504_131532", 5, fnbase="miniaod"),
'mfv_neu_tau000300um_M0600_2017': _fromnum0("/store/user/tucker/mfv_neu_tau000300um_M0600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180504_131533", 5, fnbase="miniaod"),
'mfv_neu_tau000300um_M0800_2017': _fromnum0("/store/user/tucker/mfv_neu_tau000300um_M0800/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180504_131534", 5, fnbase="miniaod"),
'mfv_neu_tau000300um_M1200_2017': _fromnum0("/store/user/tucker/mfv_neu_tau000300um_M1200/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180504_131535", 5, fnbase="miniaod"),
'mfv_neu_tau000300um_M1600_2017': _fromnum0("/store/user/tucker/mfv_neu_tau000300um_M1600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180504_131536", 5, fnbase="miniaod"),
'mfv_neu_tau000300um_M3000_2017': _fromnum0("/store/user/tucker/mfv_neu_tau000300um_M3000/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180504_131537", 5, fnbase="miniaod"),
'mfv_neu_tau001000um_M0400_2017': _fromnum0("/store/user/tucker/mfv_neu_tau001000um_M0400/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180504_131538", 5, fnbase="miniaod"),
'mfv_neu_tau001000um_M0600_2017': _fromnum0("/store/user/tucker/mfv_neu_tau001000um_M0600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180504_131539", 5, fnbase="miniaod"),
'mfv_neu_tau001000um_M0800_2017': _fromnum0("/store/user/tucker/mfv_neu_tau001000um_M0800/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180426_134902", 5, fnbase="miniaod"),
'mfv_neu_tau001000um_M1200_2017': _fromnum0("/store/user/tucker/mfv_neu_tau001000um_M1200/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180504_131540", 5, fnbase="miniaod"),
'mfv_neu_tau001000um_M1600_2017': (5, ['/store/user/tucker/mfv_neu_tau001000um_M1600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180507_182404/0000/miniaod_%i.root' % i for i in [1, 3]] + ['/store/user/tucker/mfv_neu_tau001000um_M1600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180507_111934/0000/miniaod_%i.root' % i for i in [0, 2, 4]]),
'mfv_neu_tau001000um_M3000_2017': _fromnum0("/store/user/tucker/mfv_neu_tau001000um_M3000/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180504_131542", 5, fnbase="miniaod"),
'mfv_neu_tau010000um_M0400_2017': _fromnum0("/store/user/tucker/mfv_neu_tau010000um_M0400/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180504_131543", 5, fnbase="miniaod"),
'mfv_neu_tau010000um_M0600_2017': _fromnum0("/store/user/tucker/mfv_neu_tau010000um_M0600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180504_131544", 5, fnbase="miniaod"),
'mfv_neu_tau010000um_M0800_2017': _fromnum0("/store/user/tucker/mfv_neu_tau010000um_M0800/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180504_131545", 5, fnbase="miniaod"),
'mfv_neu_tau010000um_M1200_2017': _fromnum0("/store/user/tucker/mfv_neu_tau010000um_M1200/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180504_131546", 5, fnbase="miniaod"),
'mfv_neu_tau010000um_M1600_2017': _fromnum0("/store/user/tucker/mfv_neu_tau010000um_M1600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180504_131547", 5, fnbase="miniaod"),
'mfv_neu_tau010000um_M3000_2017': _fromnum0("/store/user/tucker/mfv_neu_tau010000um_M3000/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180504_131548", 5, fnbase="miniaod"),
'mfv_neu_tau030000um_M0400_2017': _fromnum0("/store/user/tucker/mfv_neu_tau030000um_M0400/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180504_131549", 5, fnbase="miniaod"),
'mfv_neu_tau030000um_M0600_2017': _fromnum0("/store/user/tucker/mfv_neu_tau030000um_M0600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180504_131550", 5, fnbase="miniaod"),
'mfv_neu_tau030000um_M0800_2017': _fromnum0("/store/user/tucker/mfv_neu_tau030000um_M0800/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180504_131551", 5, fnbase="miniaod"),
'mfv_neu_tau030000um_M1200_2017': _fromnum0("/store/user/tucker/mfv_neu_tau030000um_M1200/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180504_131552", 5, fnbase="miniaod"),
'mfv_neu_tau030000um_M1600_2017': _fromnum0("/store/user/tucker/mfv_neu_tau030000um_M1600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180504_131553", 5, fnbase="miniaod"),
'mfv_neu_tau030000um_M3000_2017': _fromnum0("/store/user/tucker/mfv_neu_tau030000um_M3000/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180504_131554", 5, fnbase="miniaod"),
'mfv_neu_tau100000um_M0400_2017': _fromnum0("/store/user/tucker/mfv_neu_tau100000um_M0400/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180504_131555", 5, fnbase="miniaod"),
'mfv_neu_tau100000um_M0600_2017': _fromnum0("/store/user/tucker/mfv_neu_tau100000um_M0600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180504_131556", 5, fnbase="miniaod"),
'mfv_neu_tau100000um_M0800_2017': _fromnum0("/store/user/tucker/mfv_neu_tau100000um_M0800/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180504_131557", 5, fnbase="miniaod"),
'mfv_neu_tau100000um_M1200_2017': _fromnum0("/store/user/tucker/mfv_neu_tau100000um_M1200/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180504_131558", 5, fnbase="miniaod"),
'mfv_neu_tau100000um_M1600_2017': _fromnum0("/store/user/tucker/mfv_neu_tau100000um_M1600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180504_131559", 5, fnbase="miniaod"),
'mfv_neu_tau100000um_M3000_2017': _fromnum0("/store/user/tucker/mfv_neu_tau100000um_M3000/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180504_131600", 5, fnbase="miniaod"),
})

################################################################################

if __name__ == '__main__':
    import sys

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
