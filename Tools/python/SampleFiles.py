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
'mfv_neu_tau000100um_M0200_2017': _fromnum1("/store/user/tucker/mfv_neu_tau000100um_M0200/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180613_182147", 100, fnbase="reco"),
'mfv_neu_tau000100um_M0300_2017': _fromnum1("/store/user/tucker/mfv_neu_tau000100um_M0300/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180613_182212", 100, fnbase="reco"),
'mfv_neu_tau000100um_M0400_2017': _fromnum1("/store/user/tucker/mfv_neu_tau000100um_M0400/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180430_161307", 100, fnbase="reco"),
'mfv_neu_tau000100um_M0600_2017': _fromnum1("/store/user/tucker/mfv_neu_tau000100um_M0600/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180430_161327", 100, fnbase="reco"),
'mfv_neu_tau000100um_M0800_2017': _fromnum1("/store/user/tucker/mfv_neu_tau000100um_M0800/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180430_161348", 100, fnbase="reco"),
'mfv_neu_tau000100um_M1200_2017': _fromnum1("/store/user/tucker/mfv_neu_tau000100um_M1200/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180430_161409", 100, fnbase="reco"),
'mfv_neu_tau000100um_M1600_2017': _fromnum1("/store/user/tucker/mfv_neu_tau000100um_M1600/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180430_161429", 100, fnbase="reco"),
'mfv_neu_tau000100um_M3000_2017': _fromnum1("/store/user/tucker/mfv_neu_tau000100um_M3000/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180430_161449", 100, fnbase="reco"),
'mfv_neu_tau000300um_M0200_2017': _fromnum1("/store/user/tucker/mfv_neu_tau000300um_M0200/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180613_182236", 100, fnbase="reco"),
'mfv_neu_tau000300um_M0300_2017': _fromnum1("/store/user/tucker/mfv_neu_tau000300um_M0300/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180613_182258", 100, fnbase="reco"),
'mfv_neu_tau000300um_M0400_2017': _fromnum1("/store/user/tucker/mfv_neu_tau000300um_M0400/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180430_161508", 100, fnbase="reco"),
'mfv_neu_tau000300um_M0600_2017': _fromnum1("/store/user/tucker/mfv_neu_tau000300um_M0600/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180430_161528", 100, fnbase="reco"),
'mfv_neu_tau000300um_M0800_2017': _fromnum1("/store/user/tucker/mfv_neu_tau000300um_M0800/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180430_161548", 100, fnbase="reco"),
'mfv_neu_tau000300um_M1200_2017': _fromnum1("/store/user/tucker/mfv_neu_tau000300um_M1200/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180430_161608", 100, fnbase="reco"),
'mfv_neu_tau000300um_M1600_2017': _fromnum1("/store/user/tucker/mfv_neu_tau000300um_M1600/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180430_161629", 100, fnbase="reco"),
'mfv_neu_tau000300um_M3000_2017': _fromnum1("/store/user/tucker/mfv_neu_tau000300um_M3000/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180430_161650", 100, fnbase="reco"),
'mfv_neu_tau001000um_M0200_2017': _fromnum1("/store/user/tucker/mfv_neu_tau001000um_M0200/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180613_182328", 100, fnbase="reco"),
'mfv_neu_tau001000um_M0300_2017': _fromnum1("/store/user/tucker/mfv_neu_tau001000um_M0300/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180613_182351", 100, fnbase="reco"),
'mfv_neu_tau001000um_M0400_2017': _fromnum1("/store/user/tucker/mfv_neu_tau001000um_M0400/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180430_161710", 100, fnbase="reco"),
'mfv_neu_tau001000um_M0600_2017': _fromnum1("/store/user/tucker/mfv_neu_tau001000um_M0600/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180430_161733", 100, fnbase="reco"),
'mfv_neu_tau001000um_M0800_2017': _fromnum1("/store/user/tucker/mfv_neu_tau001000um_M0800/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180425_114726", 100, fnbase="reco"),
'mfv_neu_tau001000um_M1200_2017': _fromnum1("/store/user/tucker/mfv_neu_tau001000um_M1200/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180430_161754", 100, fnbase="reco"),
'mfv_neu_tau001000um_M1600_2017': _fromnum1("/store/user/tucker/mfv_neu_tau001000um_M1600/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180430_161815", 100, fnbase="reco", but=[48]),
'mfv_neu_tau001000um_M3000_2017': _fromnum1("/store/user/tucker/mfv_neu_tau001000um_M3000/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180430_161837", 100, fnbase="reco"),
'mfv_neu_tau010000um_M0200_2017': _fromnum1("/store/user/tucker/mfv_neu_tau010000um_M0200/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180613_182411", 100, fnbase="reco"),
'mfv_neu_tau010000um_M0300_2017': _fromnum1("/store/user/tucker/mfv_neu_tau010000um_M0300/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180613_182433", 100, fnbase="reco"),
'mfv_neu_tau010000um_M0400_2017': _fromnum1("/store/user/tucker/mfv_neu_tau010000um_M0400/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180430_161856", 100, fnbase="reco"),
'mfv_neu_tau010000um_M0600_2017': _fromnum1("/store/user/tucker/mfv_neu_tau010000um_M0600/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180430_161915", 100, fnbase="reco"),
'mfv_neu_tau010000um_M0800_2017': _fromnum1("/store/user/tucker/mfv_neu_tau010000um_M0800/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180430_161934", 100, fnbase="reco"),
'mfv_neu_tau010000um_M1200_2017': _fromnum1("/store/user/tucker/mfv_neu_tau010000um_M1200/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180430_161954", 100, fnbase="reco"),
'mfv_neu_tau010000um_M1600_2017': _fromnum1("/store/user/tucker/mfv_neu_tau010000um_M1600/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180430_162014", 100, fnbase="reco"),
'mfv_neu_tau010000um_M3000_2017': _fromnum1("/store/user/tucker/mfv_neu_tau010000um_M3000/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180430_162042", 100, fnbase="reco"),
'mfv_neu_tau030000um_M0200_2017': _fromnum1("/store/user/tucker/mfv_neu_tau030000um_M0200/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180613_182453", 100, fnbase="reco"),
'mfv_neu_tau030000um_M0300_2017': _fromnum1("/store/user/tucker/mfv_neu_tau030000um_M0300/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180613_182514", 100, fnbase="reco"),
'mfv_neu_tau030000um_M0400_2017': _fromnum1("/store/user/tucker/mfv_neu_tau030000um_M0400/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180430_162103", 100, fnbase="reco"),
'mfv_neu_tau030000um_M0600_2017': _fromnum1("/store/user/tucker/mfv_neu_tau030000um_M0600/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180430_162123", 100, fnbase="reco"),
'mfv_neu_tau030000um_M0800_2017': _fromnum1("/store/user/tucker/mfv_neu_tau030000um_M0800/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180430_162143", 100, fnbase="reco"),
'mfv_neu_tau030000um_M1200_2017': _fromnum1("/store/user/tucker/mfv_neu_tau030000um_M1200/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180430_162207", 100, fnbase="reco"),
'mfv_neu_tau030000um_M1600_2017': _fromnum1("/store/user/tucker/mfv_neu_tau030000um_M1600/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180430_162226", 100, fnbase="reco"),
'mfv_neu_tau030000um_M3000_2017': _fromnum1("/store/user/tucker/mfv_neu_tau030000um_M3000/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180430_162245", 100, fnbase="reco"),
'mfv_neu_tau100000um_M0200_2017': _fromnum1("/store/user/tucker/mfv_neu_tau100000um_M0200/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180613_182534", 100, fnbase="reco"),
'mfv_neu_tau100000um_M0300_2017': _fromnum1("/store/user/tucker/mfv_neu_tau100000um_M0300/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180613_182555", 100, fnbase="reco"),
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
'mfv_neu_tau000100um_M0200_2017': _fromnum0("/store/user/tucker/mfv_neu_tau000100um_M0200/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180615_124133", 5, fnbase="miniaod"),
'mfv_neu_tau000100um_M0300_2017': _fromnum0("/store/user/tucker/mfv_neu_tau000100um_M0300/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180615_124139", 5, fnbase="miniaod"),
'mfv_neu_tau000100um_M0400_2017': _fromnum0("/store/user/tucker/mfv_neu_tau000100um_M0400/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180504_131526", 5, fnbase="miniaod"),
'mfv_neu_tau000100um_M0600_2017': _fromnum0("/store/user/tucker/mfv_neu_tau000100um_M0600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180504_131527", 5, fnbase="miniaod"),
'mfv_neu_tau000100um_M0800_2017': _fromnum0("/store/user/tucker/mfv_neu_tau000100um_M0800/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180504_131528", 5, fnbase="miniaod"),
'mfv_neu_tau000100um_M1200_2017': _fromnum0("/store/user/tucker/mfv_neu_tau000100um_M1200/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180504_131529", 5, fnbase="miniaod"),
'mfv_neu_tau000100um_M1600_2017': _fromnum0("/store/user/tucker/mfv_neu_tau000100um_M1600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180504_131530", 5, fnbase="miniaod"),
'mfv_neu_tau000100um_M3000_2017': _fromnum0("/store/user/tucker/mfv_neu_tau000100um_M3000/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180504_131531", 5, fnbase="miniaod"),
'mfv_neu_tau000300um_M0200_2017': _fromnum0("/store/user/tucker/mfv_neu_tau000300um_M0200/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180615_124134", 5, fnbase="miniaod"),
'mfv_neu_tau000300um_M0300_2017': _fromnum0("/store/user/tucker/mfv_neu_tau000300um_M0300/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180615_124140", 5, fnbase="miniaod"),
'mfv_neu_tau000300um_M0400_2017': _fromnum0("/store/user/tucker/mfv_neu_tau000300um_M0400/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180504_131532", 5, fnbase="miniaod"),
'mfv_neu_tau000300um_M0600_2017': _fromnum0("/store/user/tucker/mfv_neu_tau000300um_M0600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180504_131533", 5, fnbase="miniaod"),
'mfv_neu_tau000300um_M0800_2017': _fromnum0("/store/user/tucker/mfv_neu_tau000300um_M0800/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180504_131534", 5, fnbase="miniaod"),
'mfv_neu_tau000300um_M1200_2017': _fromnum0("/store/user/tucker/mfv_neu_tau000300um_M1200/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180504_131535", 5, fnbase="miniaod"),
'mfv_neu_tau000300um_M1600_2017': _fromnum0("/store/user/tucker/mfv_neu_tau000300um_M1600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180504_131536", 5, fnbase="miniaod"),
'mfv_neu_tau000300um_M3000_2017': _fromnum0("/store/user/tucker/mfv_neu_tau000300um_M3000/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180504_131537", 5, fnbase="miniaod"),
'mfv_neu_tau001000um_M0200_2017': _fromnum0("/store/user/tucker/mfv_neu_tau001000um_M0200/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180615_124135", 5, fnbase="miniaod"),
'mfv_neu_tau001000um_M0300_2017': _fromnum0("/store/user/tucker/mfv_neu_tau001000um_M0300/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180615_124141", 5, fnbase="miniaod"),
'mfv_neu_tau001000um_M0400_2017': _fromnum0("/store/user/tucker/mfv_neu_tau001000um_M0400/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180504_131538", 5, fnbase="miniaod"),
'mfv_neu_tau001000um_M0600_2017': _fromnum0("/store/user/tucker/mfv_neu_tau001000um_M0600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180504_131539", 5, fnbase="miniaod"),
'mfv_neu_tau001000um_M0800_2017': _fromnum0("/store/user/tucker/mfv_neu_tau001000um_M0800/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180426_134902", 5, fnbase="miniaod"),
'mfv_neu_tau001000um_M1200_2017': _fromnum0("/store/user/tucker/mfv_neu_tau001000um_M1200/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180504_131540", 5, fnbase="miniaod"),
'mfv_neu_tau001000um_M1600_2017': (5, ['/store/user/tucker/mfv_neu_tau001000um_M1600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180507_182404/0000/miniaod_%i.root' % i for i in [1, 3]] + ['/store/user/tucker/mfv_neu_tau001000um_M1600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180507_111934/0000/miniaod_%i.root' % i for i in [0, 2, 4]]),
'mfv_neu_tau001000um_M3000_2017': _fromnum0("/store/user/tucker/mfv_neu_tau001000um_M3000/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180504_131542", 5, fnbase="miniaod"),
'mfv_neu_tau010000um_M0200_2017': _fromnum0("/store/user/tucker/mfv_neu_tau010000um_M0200/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180615_124136", 5, fnbase="miniaod"),
'mfv_neu_tau010000um_M0300_2017': _fromnum0("/store/user/tucker/mfv_neu_tau010000um_M0300/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180615_124142", 5, fnbase="miniaod"),
'mfv_neu_tau010000um_M0400_2017': _fromnum0("/store/user/tucker/mfv_neu_tau010000um_M0400/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180504_131543", 5, fnbase="miniaod"),
'mfv_neu_tau010000um_M0600_2017': _fromnum0("/store/user/tucker/mfv_neu_tau010000um_M0600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180504_131544", 5, fnbase="miniaod"),
'mfv_neu_tau010000um_M0800_2017': _fromnum0("/store/user/tucker/mfv_neu_tau010000um_M0800/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180504_131545", 5, fnbase="miniaod"),
'mfv_neu_tau010000um_M1200_2017': _fromnum0("/store/user/tucker/mfv_neu_tau010000um_M1200/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180504_131546", 5, fnbase="miniaod"),
'mfv_neu_tau010000um_M1600_2017': _fromnum0("/store/user/tucker/mfv_neu_tau010000um_M1600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180504_131547", 5, fnbase="miniaod"),
'mfv_neu_tau010000um_M3000_2017': _fromnum0("/store/user/tucker/mfv_neu_tau010000um_M3000/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180504_131548", 5, fnbase="miniaod"),
'mfv_neu_tau030000um_M0200_2017': _fromnum0("/store/user/tucker/mfv_neu_tau030000um_M0200/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180615_124137", 5, fnbase="miniaod"),
'mfv_neu_tau030000um_M0300_2017': _fromnum0("/store/user/tucker/mfv_neu_tau030000um_M0300/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180615_124143", 5, fnbase="miniaod"),
'mfv_neu_tau030000um_M0400_2017': _fromnum0("/store/user/tucker/mfv_neu_tau030000um_M0400/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180504_131549", 5, fnbase="miniaod"),
'mfv_neu_tau030000um_M0600_2017': _fromnum0("/store/user/tucker/mfv_neu_tau030000um_M0600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180504_131550", 5, fnbase="miniaod"),
'mfv_neu_tau030000um_M0800_2017': _fromnum0("/store/user/tucker/mfv_neu_tau030000um_M0800/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180504_131551", 5, fnbase="miniaod"),
'mfv_neu_tau030000um_M1200_2017': _fromnum0("/store/user/tucker/mfv_neu_tau030000um_M1200/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180504_131552", 5, fnbase="miniaod"),
'mfv_neu_tau030000um_M1600_2017': _fromnum0("/store/user/tucker/mfv_neu_tau030000um_M1600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180504_131553", 5, fnbase="miniaod"),
'mfv_neu_tau030000um_M3000_2017': _fromnum0("/store/user/tucker/mfv_neu_tau030000um_M3000/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180504_131554", 5, fnbase="miniaod"),
'mfv_neu_tau100000um_M0200_2017': _fromnum0("/store/user/tucker/mfv_neu_tau100000um_M0200/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180615_124138", 5, fnbase="miniaod"),
'mfv_neu_tau100000um_M0300_2017': _fromnum0("/store/user/tucker/mfv_neu_tau100000um_M0300/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180615_124144", 5, fnbase="miniaod"),
'mfv_neu_tau100000um_M0400_2017': _fromnum0("/store/user/tucker/mfv_neu_tau100000um_M0400/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180504_131555", 5, fnbase="miniaod"),
'mfv_neu_tau100000um_M0600_2017': _fromnum0("/store/user/tucker/mfv_neu_tau100000um_M0600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180504_131556", 5, fnbase="miniaod"),
'mfv_neu_tau100000um_M0800_2017': _fromnum0("/store/user/tucker/mfv_neu_tau100000um_M0800/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180504_131557", 5, fnbase="miniaod"),
'mfv_neu_tau100000um_M1200_2017': _fromnum0("/store/user/tucker/mfv_neu_tau100000um_M1200/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180504_131558", 5, fnbase="miniaod"),
'mfv_neu_tau100000um_M1600_2017': _fromnum0("/store/user/tucker/mfv_neu_tau100000um_M1600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180504_131559", 5, fnbase="miniaod"),
'mfv_neu_tau100000um_M3000_2017': _fromnum0("/store/user/tucker/mfv_neu_tau100000um_M3000/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180504_131600", 5, fnbase="miniaod"),

'mfv_stopdbardbar_tau000100um_M0400_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_tau000100um_M0400/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180530_213926", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau000100um_M0600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_tau000100um_M0600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180530_213927", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau000100um_M0800_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_tau000100um_M0800/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180530_213928", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau000100um_M1200_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_tau000100um_M1200/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180530_213929", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau000100um_M1600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_tau000100um_M1600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180530_213930", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau000100um_M3000_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_tau000100um_M3000/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180530_213931", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau000300um_M0400_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_tau000300um_M0400/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180530_213932", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau000300um_M0600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_tau000300um_M0600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180530_213933", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau000300um_M0800_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_tau000300um_M0800/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180530_213934", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau000300um_M1200_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_tau000300um_M1200/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180530_213935", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau000300um_M1600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_tau000300um_M1600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180530_213936", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau000300um_M3000_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_tau000300um_M3000/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180530_213937", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau001000um_M0400_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_tau001000um_M0400/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180530_213938", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau001000um_M0600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_tau001000um_M0600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180530_213939", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau001000um_M0800_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_tau001000um_M0800/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180530_213940", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau001000um_M1200_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_tau001000um_M1200/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180530_213941", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau001000um_M1600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_tau001000um_M1600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180530_213942", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau001000um_M3000_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_tau001000um_M3000/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180530_213943", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau010000um_M0400_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_tau010000um_M0400/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180530_213944", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau010000um_M0600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_tau010000um_M0600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180530_213945", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau010000um_M0800_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_tau010000um_M0800/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180530_213946", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau010000um_M1200_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_tau010000um_M1200/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180530_213947", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau010000um_M1600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_tau010000um_M1600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180530_213948", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau010000um_M3000_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_tau010000um_M3000/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180530_213949", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau030000um_M0400_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_tau030000um_M0400/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180530_213950", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau030000um_M0600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_tau030000um_M0600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180530_213951", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau030000um_M0800_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_tau030000um_M0800/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180530_213952", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau030000um_M1200_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_tau030000um_M1200/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180530_213953", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau030000um_M1600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_tau030000um_M1600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180530_213954", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau030000um_M3000_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_tau030000um_M3000/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180530_213955", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau100000um_M0400_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_tau100000um_M0400/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180530_213956", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau100000um_M0600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_tau100000um_M0600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180530_213957", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau100000um_M0800_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_tau100000um_M0800/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180530_213958", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau100000um_M1200_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_tau100000um_M1200/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180530_213959", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau100000um_M1600_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_tau100000um_M1600/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180530_214000", 5, fnbase="miniaod"),
'mfv_stopdbardbar_tau100000um_M3000_2017': _fromnum0("/store/user/tucker/mfv_stopdbardbar_tau100000um_M3000/RunIIFall17MiniAODv2-94X_mc2017_realistic_v14/180530_214001", 5, fnbase="miniaod"),
})


_add_ds("ntuplev20m", {
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
'mfv_neu_tau000100um_M0200_2017': _frommerge("/store/user/tucker/mfv_neu_tau000100um_M0200/NtupleV20m_merge_2017/180810_090222/0000/merge", 1),
'mfv_neu_tau000100um_M0300_2017': _frommerge("/store/user/tucker/mfv_neu_tau000100um_M0300/NtupleV20m_merge_2017/180810_090223/0000/merge", 1),
'mfv_neu_tau000100um_M0400_2017': _frommerge("/store/user/tucker/mfv_neu_tau00100um_M0400/NtupleV20m_merge_2017/180810_090224/0000/merge", 1),
'mfv_neu_tau000100um_M0600_2017': _frommerge("/store/user/tucker/mfv_neu_tau00100um_M0600/NtupleV20m_merge_2017/180810_090225/0000/merge", 1),
'mfv_neu_tau000100um_M0800_2017': _frommerge("/store/user/tucker/mfv_neu_tau00100um_M0800/NtupleV20m_merge_2017/180810_090226/0000/merge", 1),
'mfv_neu_tau000100um_M1200_2017': _frommerge("/store/user/tucker/mfv_neu_tau00100um_M1200/NtupleV20m_merge_2017/180810_090227/0000/merge", 1),
'mfv_neu_tau000100um_M1600_2017': _frommerge("/store/user/tucker/mfv_neu_tau00100um_M1600/NtupleV20m_merge_2017/180810_090228/0000/merge", 1),
'mfv_neu_tau000100um_M3000_2017': _frommerge("/store/user/tucker/mfv_neu_tau00100um_M3000/NtupleV20m_merge_2017/180810_090229/0000/merge", 1),
'mfv_neu_tau000300um_M0200_2017': _frommerge("/store/user/tucker/mfv_neu_tau000300um_M0200/NtupleV20m_merge_2017/180810_090230/0000/merge", 1),
'mfv_neu_tau000300um_M0300_2017': _frommerge("/store/user/tucker/mfv_neu_tau000300um_M0300/NtupleV20m_merge_2017/180810_090231/0000/merge", 1),
'mfv_neu_tau000300um_M0400_2017': _frommerge("/store/user/tucker/mfv_neu_tau00300um_M0400/NtupleV20m_merge_2017/180810_090232/0000/merge", 1),
'mfv_neu_tau000300um_M0600_2017': _frommerge("/store/user/tucker/mfv_neu_tau00300um_M0600/NtupleV20m_merge_2017/180810_090233/0000/merge", 1),
'mfv_neu_tau000300um_M0800_2017': _frommerge("/store/user/tucker/mfv_neu_tau00300um_M0800/NtupleV20m_merge_2017/180810_090234/0000/merge", 1),
'mfv_neu_tau000300um_M1200_2017': _frommerge("/store/user/tucker/mfv_neu_tau00300um_M1200/NtupleV20m_merge_2017/180810_090235/0000/merge", 1),
'mfv_neu_tau000300um_M1600_2017': _frommerge("/store/user/tucker/mfv_neu_tau00300um_M1600/NtupleV20m_merge_2017/180810_090236/0000/merge", 1),
'mfv_neu_tau000300um_M3000_2017': _frommerge("/store/user/tucker/mfv_neu_tau00300um_M3000/NtupleV20m_merge_2017/180810_090237/0000/merge", 1),
'mfv_neu_tau001000um_M0200_2017': _frommerge("/store/user/tucker/mfv_neu_tau001000um_M0200/NtupleV20m_merge_2017/180810_090238/0000/merge", 1),
'mfv_neu_tau001000um_M0300_2017': _frommerge("/store/user/tucker/mfv_neu_tau001000um_M0300/NtupleV20m_merge_2017/180810_090239/0000/merge", 1),
'mfv_neu_tau001000um_M0400_2017': _frommerge("/store/user/tucker/mfv_neu_tau01000um_M0400/NtupleV20m_merge_2017/180810_090240/0000/merge", 1),
'mfv_neu_tau001000um_M0600_2017': _frommerge("/store/user/tucker/mfv_neu_tau01000um_M0600/NtupleV20m_merge_2017/180810_090241/0000/merge", 1),
'mfv_neu_tau001000um_M0800_2017': _frommerge("/store/user/tucker/mfv_neu_tau01000um_M0800/NtupleV20m_merge_2017/180810_090242/0000/merge", 1),
'mfv_neu_tau001000um_M1200_2017': _frommerge("/store/user/tucker/mfv_neu_tau01000um_M1200/NtupleV20m_merge_2017/180810_090243/0000/merge", 1),
'mfv_neu_tau001000um_M1600_2017': _frommerge("/store/user/tucker/mfv_neu_tau01000um_M1600/NtupleV20m_merge_2017/180810_090244/0000/merge", 1),
'mfv_neu_tau001000um_M3000_2017': _frommerge("/store/user/tucker/mfv_neu_tau01000um_M3000/NtupleV20m_merge_2017/180810_090245/0000/merge", 1),
'mfv_neu_tau010000um_M0200_2017': _frommerge("/store/user/tucker/mfv_neu_tau010000um_M0200/NtupleV20m_merge_2017/180810_090246/0000/merge", 1),
'mfv_neu_tau010000um_M0300_2017': _frommerge("/store/user/tucker/mfv_neu_tau010000um_M0300/NtupleV20m_merge_2017/180810_090247/0000/merge", 1),
'mfv_neu_tau010000um_M0400_2017': _frommerge("/store/user/tucker/mfv_neu_tau10000um_M0400/NtupleV20m_merge_2017/180810_090248/0000/merge", 1),
'mfv_neu_tau010000um_M0600_2017': _frommerge("/store/user/tucker/mfv_neu_tau10000um_M0600/NtupleV20m_merge_2017/180810_090249/0000/merge", 1),
'mfv_neu_tau010000um_M0800_2017': _frommerge("/store/user/tucker/mfv_neu_tau10000um_M0800/NtupleV20m_merge_2017/180810_090250/0000/merge", 1),
'mfv_neu_tau010000um_M1200_2017': _frommerge("/store/user/tucker/mfv_neu_tau10000um_M1200/NtupleV20m_merge_2017/180810_090251/0000/merge", 1),
'mfv_neu_tau010000um_M1600_2017': _frommerge("/store/user/tucker/mfv_neu_tau10000um_M1600/NtupleV20m_merge_2017/180810_090252/0000/merge", 1),
'mfv_neu_tau010000um_M3000_2017': _frommerge("/store/user/tucker/mfv_neu_tau10000um_M3000/NtupleV20m_merge_2017/180810_090253/0000/merge", 1),
'mfv_neu_tau030000um_M0200_2017': _frommerge("/store/user/tucker/mfv_neu_tau030000um_M0200/NtupleV20m_merge_2017/180810_090254/0000/merge", 1),
'mfv_neu_tau030000um_M0300_2017': _frommerge("/store/user/tucker/mfv_neu_tau030000um_M0300/NtupleV20m_merge_2017/180810_090255/0000/merge", 1),
'mfv_neu_tau030000um_M0400_2017': _frommerge("/store/user/tucker/mfv_neu_tau30000um_M0400/NtupleV20m_merge_2017/180810_090256/0000/merge", 1),
'mfv_neu_tau030000um_M0600_2017': _frommerge("/store/user/tucker/mfv_neu_tau30000um_M0600/NtupleV20m_merge_2017/180810_090257/0000/merge", 1),
'mfv_neu_tau030000um_M0800_2017': _frommerge("/store/user/tucker/mfv_neu_tau30000um_M0800/NtupleV20m_merge_2017/180810_090258/0000/merge", 1),
'mfv_neu_tau030000um_M1200_2017': _frommerge("/store/user/tucker/mfv_neu_tau30000um_M1200/NtupleV20m_merge_2017/180810_090259/0000/merge", 1),
'mfv_neu_tau030000um_M1600_2017': _frommerge("/store/user/tucker/mfv_neu_tau30000um_M1600/NtupleV20m_merge_2017/180810_090300/0000/merge", 1),
'mfv_neu_tau030000um_M3000_2017': _frommerge("/store/user/tucker/mfv_neu_tau30000um_M3000/NtupleV20m_merge_2017/180810_090301/0000/merge", 1),
'mfv_neu_tau100000um_M0200_2017': _frommerge("/store/user/tucker/mfv_neu_tau100000um_M0200/NtupleV20m_merge_2017/180810_090302/0000/merge", 1),
'mfv_neu_tau100000um_M0300_2017': _frommerge("/store/user/tucker/mfv_neu_tau100000um_M0300/NtupleV20m_merge_2017/180810_090303/0000/merge", 1),
'mfv_neu_tau100000um_M0400_2017': _frommerge("/store/user/tucker/mfv_neu_tau100000um_M0400/NtupleV20m_merge_2017/180810_090304/0000/merge", 1),
'mfv_neu_tau100000um_M0600_2017': _frommerge("/store/user/tucker/mfv_neu_tau100000um_M0600/NtupleV20m_merge_2017/180810_090305/0000/merge", 1),
'mfv_neu_tau100000um_M0800_2017': _frommerge("/store/user/tucker/mfv_neu_tau100000um_M0800/NtupleV20m_merge_2017/180810_090306/0000/merge", 1),
'mfv_neu_tau100000um_M1200_2017': _frommerge("/store/user/tucker/mfv_neu_tau100000um_M1200/NtupleV20m_merge_2017/180810_090307/0000/merge", 1),
'mfv_neu_tau100000um_M1600_2017': _frommerge("/store/user/tucker/mfv_neu_tau100000um_M1600/NtupleV20m_merge_2017/180810_090308/0000/merge", 1),
'mfv_neu_tau100000um_M3000_2017': _frommerge("/store/user/tucker/mfv_neu_tau100000um_M3000/NtupleV20m_merge_2017/180810_090309/0000/merge", 1),
'mfv_stopdbardbar_tau000100um_M0400_2017': _frommerge("/store/user/tucker/mfv_stopdbardbar_tau000100um_M0400/NtupleV20m_merge_2017/180810_090310/0000/merge", 1),
'mfv_stopdbardbar_tau000100um_M0600_2017': _frommerge("/store/user/tucker/mfv_stopdbardbar_tau000100um_M0600/NtupleV20m_merge_2017/180810_090311/0000/merge", 1),
'mfv_stopdbardbar_tau000100um_M0800_2017': _frommerge("/store/user/tucker/mfv_stopdbardbar_tau000100um_M0800/NtupleV20m_merge_2017/180810_090312/0000/merge", 1),
'mfv_stopdbardbar_tau000100um_M1200_2017': _frommerge("/store/user/tucker/mfv_stopdbardbar_tau000100um_M1200/NtupleV20m_merge_2017/180810_090313/0000/merge", 1),
'mfv_stopdbardbar_tau000100um_M1600_2017': _frommerge("/store/user/tucker/mfv_stopdbardbar_tau000100um_M1600/NtupleV20m_merge_2017/180810_090314/0000/merge", 1),
'mfv_stopdbardbar_tau000100um_M3000_2017': _frommerge("/store/user/tucker/mfv_stopdbardbar_tau000100um_M3000/NtupleV20m_merge_2017/180810_090315/0000/merge", 1),
'mfv_stopdbardbar_tau000300um_M0400_2017': _frommerge("/store/user/tucker/mfv_stopdbardbar_tau000300um_M0400/NtupleV20m_merge_2017/180810_090316/0000/merge", 1),
'mfv_stopdbardbar_tau000300um_M0600_2017': _frommerge("/store/user/tucker/mfv_stopdbardbar_tau000300um_M0600/NtupleV20m_merge_2017/180810_090317/0000/merge", 1),
'mfv_stopdbardbar_tau000300um_M0800_2017': _frommerge("/store/user/tucker/mfv_stopdbardbar_tau000300um_M0800/NtupleV20m_merge_2017/180810_090318/0000/merge", 1),
'mfv_stopdbardbar_tau000300um_M1200_2017': _frommerge("/store/user/tucker/mfv_stopdbardbar_tau000300um_M1200/NtupleV20m_merge_2017/180810_090319/0000/merge", 1),
'mfv_stopdbardbar_tau000300um_M1600_2017': _frommerge("/store/user/tucker/mfv_stopdbardbar_tau000300um_M1600/NtupleV20m_merge_2017/180810_090320/0000/merge", 1),
'mfv_stopdbardbar_tau000300um_M3000_2017': _frommerge("/store/user/tucker/mfv_stopdbardbar_tau000300um_M3000/NtupleV20m_merge_2017/180810_090321/0000/merge", 1),
'mfv_stopdbardbar_tau001000um_M0400_2017': _frommerge("/store/user/tucker/mfv_stopdbardbar_tau001000um_M0400/NtupleV20m_merge_2017/180810_090322/0000/merge", 1),
'mfv_stopdbardbar_tau001000um_M0600_2017': _frommerge("/store/user/tucker/mfv_stopdbardbar_tau001000um_M0600/NtupleV20m_merge_2017/180810_090323/0000/merge", 1),
'mfv_stopdbardbar_tau001000um_M0800_2017': _frommerge("/store/user/tucker/mfv_stopdbardbar_tau001000um_M0800/NtupleV20m_merge_2017/180810_090324/0000/merge", 1),
'mfv_stopdbardbar_tau001000um_M1200_2017': _frommerge("/store/user/tucker/mfv_stopdbardbar_tau001000um_M1200/NtupleV20m_merge_2017/180810_090325/0000/merge", 1),
'mfv_stopdbardbar_tau001000um_M1600_2017': _frommerge("/store/user/tucker/mfv_stopdbardbar_tau001000um_M1600/NtupleV20m_merge_2017/180810_090326/0000/merge", 1),
'mfv_stopdbardbar_tau001000um_M3000_2017': _frommerge("/store/user/tucker/mfv_stopdbardbar_tau001000um_M3000/NtupleV20m_merge_2017/180810_090327/0000/merge", 1),
'mfv_stopdbardbar_tau010000um_M0400_2017': _frommerge("/store/user/tucker/mfv_stopdbardbar_tau010000um_M0400/NtupleV20m_merge_2017/180810_090328/0000/merge", 1),
'mfv_stopdbardbar_tau010000um_M0600_2017': _frommerge("/store/user/tucker/mfv_stopdbardbar_tau010000um_M0600/NtupleV20m_merge_2017/180810_090329/0000/merge", 1),
'mfv_stopdbardbar_tau010000um_M0800_2017': _frommerge("/store/user/tucker/mfv_stopdbardbar_tau010000um_M0800/NtupleV20m_merge_2017/180810_090330/0000/merge", 1),
'mfv_stopdbardbar_tau010000um_M1200_2017': _frommerge("/store/user/tucker/mfv_stopdbardbar_tau010000um_M1200/NtupleV20m_merge_2017/180810_090331/0000/merge", 1),
'mfv_stopdbardbar_tau010000um_M1600_2017': _frommerge("/store/user/tucker/mfv_stopdbardbar_tau010000um_M1600/NtupleV20m_merge_2017/180810_090332/0000/merge", 1),
'mfv_stopdbardbar_tau010000um_M3000_2017': _frommerge("/store/user/tucker/mfv_stopdbardbar_tau010000um_M3000/NtupleV20m_merge_2017/180810_090333/0000/merge", 1),
'mfv_stopdbardbar_tau030000um_M0400_2017': _frommerge("/store/user/tucker/mfv_stopdbardbar_tau030000um_M0400/NtupleV20m_merge_2017/180810_090334/0000/merge", 1),
'mfv_stopdbardbar_tau030000um_M0600_2017': _frommerge("/store/user/tucker/mfv_stopdbardbar_tau030000um_M0600/NtupleV20m_merge_2017/180810_090335/0000/merge", 1),
'mfv_stopdbardbar_tau030000um_M0800_2017': _frommerge("/store/user/tucker/mfv_stopdbardbar_tau030000um_M0800/NtupleV20m_merge_2017/180810_090336/0000/merge", 1),
'mfv_stopdbardbar_tau030000um_M1200_2017': _frommerge("/store/user/tucker/mfv_stopdbardbar_tau030000um_M1200/NtupleV20m_merge_2017/180810_090337/0000/merge", 1),
'mfv_stopdbardbar_tau030000um_M1600_2017': _frommerge("/store/user/tucker/mfv_stopdbardbar_tau030000um_M1600/NtupleV20m_merge_2017/180810_090338/0000/merge", 1),
'mfv_stopdbardbar_tau030000um_M3000_2017': _frommerge("/store/user/tucker/mfv_stopdbardbar_tau030000um_M3000/NtupleV20m_merge_2017/180810_090339/0000/merge", 1),
'mfv_stopdbardbar_tau100000um_M0400_2017': _frommerge("/store/user/tucker/mfv_stopdbardbar_tau100000um_M0400/NtupleV20m_merge_2017/180810_090340/0000/merge", 1),
'mfv_stopdbardbar_tau100000um_M0600_2017': _frommerge("/store/user/tucker/mfv_stopdbardbar_tau100000um_M0600/NtupleV20m_merge_2017/180810_090341/0000/merge", 1),
'mfv_stopdbardbar_tau100000um_M0800_2017': _frommerge("/store/user/tucker/mfv_stopdbardbar_tau100000um_M0800/NtupleV20m_merge_2017/180810_090342/0000/merge", 1),
'mfv_stopdbardbar_tau100000um_M1200_2017': _frommerge("/store/user/tucker/mfv_stopdbardbar_tau100000um_M1200/NtupleV20m_merge_2017/180810_090343/0000/merge", 1),
'mfv_stopdbardbar_tau100000um_M1600_2017': _frommerge("/store/user/tucker/mfv_stopdbardbar_tau100000um_M1600/NtupleV20m_merge_2017/180810_090344/0000/merge", 1),
'mfv_stopdbardbar_tau100000um_M3000_2017': _frommerge("/store/user/tucker/mfv_stopdbardbar_tau100000um_M3000/NtupleV20m_merge_2017/180810_090345/0000/merge", 1),
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
