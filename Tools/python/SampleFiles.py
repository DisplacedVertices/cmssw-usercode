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

def _add_single_files(ds, path, l, allow_overwrite=False):
    d = {}
    for sample in l:
        d[(sample,ds)] = (1, [os.path.join(path, sample + '.root')])
    _add(d, allow_overwrite)

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
    ('ttbarht0800_2017', 'miniaod', ['/store/mc/RunIIFall17MiniAODv2/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/40000/225CD078-B3A4-E811-AA74-001E67DDC254.root',
                                     '/store/mc/RunIIFall17MiniAODv2/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/60000/BC22A92A-7BBA-E811-8A2B-0242AC1C0501.root',]),
    ]

for name, ds, fns in _removed:
    for fn in fns:
        _remove_file(name, ds, fn)

################################################################################

_add_ds("nr_trackingtreerv23mv3", {
'qcdht0700_2017': (48, ['/store/user/wsun/croncopyeos/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/TrackingTreerV23mv3_2017/190329_154545/0000/trackingtreer_%i.root' % i for i in [25, 46]] + ['/store/user/wsun/croncopyeos/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/TrackingTreerV23mv3_2017/190329_150253/0000/trackingtreer_%i.root' % i for i in chain(xrange(22), xrange(23,25), xrange(26,46), [47])] + ['/store/user/wsun/croncopyeos/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/TrackingTreerV23mv3_2017/190401_120003/0000/trackingtreer_22.root']),
'qcdht1000_2017': _fromnum1("/store/user/wsun/croncopyeos/QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8/TrackingTreerV23mv3_2017/190329_200142", 22, fnbase="trackingtreer"),
'qcdht1500_2017': (11, ['/store/user/wsun/croncopyeos/QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8/TrackingTreerV23mv3_2017/190329_150254/0000/trackingtreer_%i.root' % i for i in chain(xrange(7), xrange(13,16), [11])]),
'qcdht2000_2017': _fromnum0("/store/user/wsun/croncopyeos/QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/TrackingTreerV23mv3_2017/190329_150255", 10, fnbase="trackingtreer"),
'qcdht0700_2018': (72, ['/store/user/wsun/croncopyeos/QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8/TrackingTreerV23mv3_2018/190329_153344/0000/trackingtreer_%i.root' % i for i in chain(xrange(3), xrange(4,72))] + ['/store/user/wsun/croncopyeos/QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8/TrackingTreerV23mv3_2018/190329_154546/0000/trackingtreer_3.root']),
'qcdht1000_2018': (26, ['/store/user/wsun/croncopyeos/QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8/TrackingTreerV23mv3_2018/190402_070940/0000/trackingtreer_%i.root' % i for i in [2, 13]] + ['/store/user/wsun/croncopyeos/QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8/TrackingTreerV23mv3_2018/190329_153345/0000/trackingtreer_%i.root' % i for i in chain(xrange(2), xrange(3,13), xrange(14,16), xrange(17,22), xrange(23,26))] + ['/store/user/wsun/croncopyeos/QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8/TrackingTreerV23mv3_2018/190401_120016/0000/trackingtreer_%i.root' % i for i in [16, 22]]),
'qcdht1500_2018': (1, ['/store/user/wsun/croncopyeos/QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8/TrackingTreerV23mv3_2018/190329_203300/0000/trackingtreer_18.root']),
'qcdht2000_2018': (9, ['/store/user/wsun/croncopyeos/QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8/TrackingTreerV23mv3_2018/190401_120017/0000/trackingtreer_0.root'] + ['/store/user/wsun/croncopyeos/QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8/TrackingTreerV23mv3_2018/190329_153346/0000/trackingtreer_%i.root' % i for i in chain(xrange(1,4), xrange(7,11), [5])]),
'JetHT2017B': _fromnum1("/store/user/wsun/croncopyeos/JetHT/TrackingTreerV23mv3_2017/190329_200156", 12, fnbase="trackingtreer"),
'JetHT2017C': _fromnum1("/store/user/wsun/croncopyeos/JetHT/TrackingTreerV23mv3_2017/190329_200207", 26, fnbase="trackingtreer"),
'JetHT2017D': _fromnum1("/store/user/wsun/croncopyeos/JetHT/TrackingTreerV23mv3_2017/190329_200224", 12, fnbase="trackingtreer"),
'JetHT2017E': _fromnum1("/store/user/wsun/croncopyeos/JetHT/TrackingTreerV23mv3_2017/190329_200239", 22, fnbase="trackingtreer"),
'JetHT2017F': _fromnum1("/store/user/wsun/croncopyeos/JetHT/TrackingTreerV23mv3_2017/190329_200252", 29, fnbase="trackingtreer"),
'JetHT2018A': _fromnum1("/store/user/wsun/croncopyeos/JetHT/TrackingTreerV23mv3_2018/190329_203312", 30, fnbase="trackingtreer"),
'JetHT2018B': _fromnum1("/store/user/wsun/croncopyeos/JetHT/TrackingTreerV23mv3_2018/190329_203322", 24, fnbase="trackingtreer"),
'JetHT2018C': _fromnum1("/store/user/wsun/croncopyeos/JetHT/TrackingTreerV23mv3_2018/190329_203332", 14, fnbase="trackingtreer"),
'JetHT2018D': _fromnum1("/store/user/wsun/croncopyeos/JetHT/TrackingTreerV23mv3_2018/190329_203343", 64, fnbase="trackingtreer"),
})


_add_ds("ntuplev27m_wgen", {
'mfv_neu_tau000100um_M0400_2018': (3, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114244/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114244/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114244/0000/merge002_0.root']),
'mfv_neu_tau000100um_M0600_2018': (4, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114245/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114245/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114245/0000/merge002_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114245/0000/merge003_0.root']),
'mfv_neu_tau000100um_M0800_2018': (4, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180319/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180319/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180319/0000/merge002_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180319/0000/merge003_0.root']),
'mfv_neu_tau000100um_M1200_2018': (4, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180320/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180320/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180320/0000/merge002_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180320/0000/merge003_0.root']),
'mfv_neu_tau000100um_M1600_2018': (4, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180321/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180321/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180321/0000/merge002_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180321/0000/merge003_0.root']),
'mfv_neu_tau000100um_M3000_2018': (4, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180322/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180322/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180322/0000/merge002_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180322/0000/merge003_0.root']),
'mfv_neu_tau000300um_M0400_2018': (3, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114246/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114246/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114246/0000/merge002_0.root']),
'mfv_neu_tau000300um_M0600_2018': (4, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180323/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180323/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180323/0000/merge002_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180323/0000/merge003_0.root']),
'mfv_neu_tau000300um_M0800_2018': (4, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114247/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114247/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114247/0000/merge002_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114247/0000/merge003_0.root']),
'mfv_neu_tau000300um_M1200_2018': (4, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180324/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180324/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180324/0000/merge002_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180324/0000/merge003_0.root']),
'mfv_neu_tau000300um_M1600_2018': (4, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180325/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180325/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180325/0000/merge002_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180325/0000/merge003_0.root']),
'mfv_neu_tau000300um_M3000_2018': (4, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180326/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180326/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180326/0000/merge002_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180326/0000/merge003_0.root']),
'mfv_neu_tau001000um_M0400_2018': (4, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180327/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180327/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180327/0000/merge002_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180327/0000/merge003_0.root']),
'mfv_neu_tau001000um_M0600_2018': (4, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180328/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180328/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180328/0000/merge002_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180328/0000/merge003_0.root']),
'mfv_neu_tau001000um_M0800_2018': (4, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180329/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180329/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180329/0000/merge002_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180329/0000/merge003_0.root']),
'mfv_neu_tau001000um_M1200_2018': (4, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180330/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180330/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180330/0000/merge002_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180330/0000/merge003_0.root']),
'mfv_neu_tau001000um_M3000_2018': (5, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114248/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114248/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114248/0000/merge002_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114248/0000/merge003_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114248/0000/merge004_0.root']),
'mfv_neu_tau010000um_M0400_2018': (4, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114249/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114249/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114249/0000/merge002_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114249/0000/merge003_0.root']),
'mfv_neu_tau010000um_M0600_2018': (4, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114250/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114250/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114250/0000/merge002_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114250/0000/merge003_0.root']),
'mfv_neu_tau010000um_M0800_2018': (4, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180331/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180331/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180331/0000/merge002_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180331/0000/merge003_0.root']),
'mfv_neu_tau010000um_M1200_2018': (5, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114251/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114251/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114251/0000/merge002_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114251/0000/merge003_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114251/0000/merge004_0.root']),
'mfv_neu_tau010000um_M1600_2018': (5, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180332/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180332/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180332/0000/merge002_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180332/0000/merge003_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180332/0000/merge004_0.root']),
'mfv_neu_tau010000um_M3000_2018': (5, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_132553/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_132553/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_132553/0000/merge002_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_132553/0000/merge003_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_132553/0000/merge004_0.root']),
'mfv_neu_tau030000um_M0400_2018': (4, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114252/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114252/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114252/0000/merge002_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114252/0000/merge003_0.root']),
'mfv_neu_tau030000um_M0600_2018': (4, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114253/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114253/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114253/0000/merge002_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114253/0000/merge003_0.root']),
'mfv_neu_tau030000um_M0800_2018': (4, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114254/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114254/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114254/0000/merge002_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114254/0000/merge003_0.root']),
'mfv_neu_tau030000um_M1200_2018': (4, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114255/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114255/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114255/0000/merge002_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114255/0000/merge003_0.root']),
'mfv_neu_tau030000um_M1600_2018': (5, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114256/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114256/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114256/0000/merge002_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114256/0000/merge003_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114256/0000/merge004_0.root']),
'mfv_neu_tau030000um_M3000_2018': (5, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114257/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114257/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114257/0000/merge002_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114257/0000/merge003_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114257/0000/merge004_0.root']),
'mfv_stopdbardbar_tau000100um_M0400_2018': (3, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-400_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114258/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-400_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114258/0000/merge001_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-400_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114258/0000/merge002_0.root']),
'mfv_stopdbardbar_tau000100um_M0600_2018': (3, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-600_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114259/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-600_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114259/0000/merge001_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-600_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114259/0000/merge002_0.root']),
'mfv_stopdbardbar_tau000100um_M0800_2018': (3, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-800_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114300/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-800_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114300/0000/merge001_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-800_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114300/0000/merge002_0.root']),
'mfv_stopdbardbar_tau000100um_M1200_2018': (3, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-1200_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114301/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1200_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114301/0000/merge001_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1200_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114301/0000/merge002_0.root']),
'mfv_stopdbardbar_tau000100um_M1600_2018': (3, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-1600_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180333/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1600_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180333/0000/merge001_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1600_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180333/0000/merge002_0.root']),
'mfv_stopdbardbar_tau000100um_M3000_2018': (4, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180334/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180334/0000/merge001_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180334/0000/merge002_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180334/0000/merge003_0.root']),
'mfv_stopdbardbar_tau000300um_M0400_2018': (3, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-400_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180335/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-400_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180335/0000/merge001_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-400_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180335/0000/merge002_0.root']),
'mfv_stopdbardbar_tau000300um_M0600_2018': (3, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-600_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180336/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-600_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180336/0000/merge001_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-600_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180336/0000/merge002_0.root']),
'mfv_stopdbardbar_tau000300um_M0800_2018': (3, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-800_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114302/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-800_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114302/0000/merge001_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-800_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114302/0000/merge002_0.root']),
'mfv_stopdbardbar_tau000300um_M1200_2018': (3, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-1200_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114303/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1200_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114303/0000/merge001_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1200_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114303/0000/merge002_0.root']),
'mfv_stopdbardbar_tau000300um_M1600_2018': (3, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-1600_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180337/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1600_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180337/0000/merge001_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1600_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180337/0000/merge002_0.root']),
'mfv_stopdbardbar_tau000300um_M3000_2018': (4, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180338/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180338/0000/merge001_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180338/0000/merge002_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180338/0000/merge003_0.root']),
'mfv_stopdbardbar_tau001000um_M0400_2018': (3, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-400_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114304/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-400_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114304/0000/merge001_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-400_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114304/0000/merge002_0.root']),
'mfv_stopdbardbar_tau001000um_M0600_2018': (3, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-600_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114305/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-600_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114305/0000/merge001_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-600_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114305/0000/merge002_0.root']),
'mfv_stopdbardbar_tau001000um_M1200_2018': (4, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-1200_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114306/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1200_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114306/0000/merge001_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1200_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114306/0000/merge002_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1200_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114306/0000/merge003_0.root']),
'mfv_stopdbardbar_tau001000um_M1600_2018': (4, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-1600_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114307/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1600_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114307/0000/merge001_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1600_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114307/0000/merge002_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1600_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114307/0000/merge003_0.root']),
'mfv_stopdbardbar_tau001000um_M3000_2018': (4, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180339/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180339/0000/merge001_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180339/0000/merge002_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180339/0000/merge003_0.root']),
'mfv_stopdbardbar_tau010000um_M0400_2018': (3, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-400_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114308/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-400_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114308/0000/merge001_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-400_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114308/0000/merge002_0.root']),
'mfv_stopdbardbar_tau010000um_M0600_2018': (3, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-600_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114309/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-600_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114309/0000/merge001_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-600_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114309/0000/merge002_0.root']),
'mfv_stopdbardbar_tau010000um_M0800_2018': (4, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-800_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114310/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-800_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114310/0000/merge001_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-800_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114310/0000/merge002_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-800_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114310/0000/merge003_0.root']),
'mfv_stopdbardbar_tau010000um_M1200_2018': (4, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-1200_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180340/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1200_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180340/0000/merge001_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1200_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180340/0000/merge002_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1200_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180340/0000/merge003_0.root']),
'mfv_stopdbardbar_tau010000um_M1600_2018': (4, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-1600_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114311/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1600_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114311/0000/merge001_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1600_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114311/0000/merge002_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1600_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114311/0000/merge003_0.root']),
'mfv_stopdbardbar_tau010000um_M3000_2018': (5, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180341/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180341/0000/merge001_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180341/0000/merge002_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180341/0000/merge003_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180341/0000/merge004_0.root']),
'mfv_stopdbardbar_tau030000um_M0400_2018': (3, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-400_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180342/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-400_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180342/0000/merge001_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-400_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180342/0000/merge002_0.root']),
'mfv_stopdbardbar_tau030000um_M0600_2018': (3, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-600_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180343/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-600_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180343/0000/merge001_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-600_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180343/0000/merge002_0.root']),
'mfv_stopdbardbar_tau030000um_M0800_2018': (3, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-800_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114312/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-800_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114312/0000/merge001_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-800_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114312/0000/merge002_0.root']),
'mfv_stopdbardbar_tau030000um_M1200_2018': (4, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-1200_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114313/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1200_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114313/0000/merge001_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1200_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114313/0000/merge002_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1200_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_114313/0000/merge003_0.root']),
'mfv_stopdbardbar_tau030000um_M1600_2018': (4, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-1600_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180344/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1600_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180344/0000/merge001_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1600_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180344/0000/merge002_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1600_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200415_180344/0000/merge003_0.root']),
'mfv_stopdbardbar_tau030000um_M3000_2018': (4, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_132616/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_132616/0000/merge001_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_132616/0000/merge002_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_WGen_2018/200411_132616/0000/merge003_0.root']),
})


_add_ds("ntuplev27m", {
'qcdht0700_2017': _fromnum0("/store/user/tucker/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/NtupleV27m_2017/190802_112506", 16),
'qcdht1000_2017': _fromnum0("/store/user/tucker/QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8/NtupleV27m_2017/190802_112507", 31),
'qcdht1500_2017': _fromnum0("/store/user/tucker/QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8/NtupleV27m_2017/190802_112508", 63),
'qcdht2000_2017': _fromnum0("/store/user/tucker/QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/NtupleV27m_2017/190802_112509", 30),
'ttbarht0600_2017': _fromnum0("/store/user/tucker/TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV27m_2017/190802_112510", 4),
'ttbarht0800_2017': _fromnum0("/store/user/tucker/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV27m_2017/190802_112511", 3),
'ttbarht1200_2017': (1, ['/store/user/tucker/TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV27m_2017/190802_112512/0000/ntuple_0.root']),
'ttbarht2500_2017': (1, ['/store/user/tucker/TTJets_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV27m_2017/190802_112513/0000/ntuple_0.root']),
'qcdht0700_2018': _fromnum0("/store/user/tucker/QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV27m_2018/190802_113539", 23),
'qcdht1000_2018': _fromnum0("/store/user/tucker/QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV27m_2018/190802_113540", 37),
'qcdht1500_2018': _fromnum0("/store/user/tucker/QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV27m_2018/190802_113541", 76),
'qcdht2000_2018': _fromnum0("/store/user/tucker/QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV27m_2018/190802_113542", 34),
'ttbarht0600_2018': _fromnum0("/store/user/tucker/TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV27m_2018/190802_113543", 5),
'ttbarht0800_2018': _fromnum0("/store/user/tucker/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV27m_2018/190802_113544", 4),
'ttbarht1200_2018': (1, ['/store/user/tucker/TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV27m_2018/190802_113545/0000/ntuple_0.root']),
'ttbarht2500_2018': (1, ['/store/user/tucker/TTJets_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV27m_2018/190802_113546/0000/ntuple_0.root']),
'mfv_neu_tau000100um_M0400_2017': (2, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133743/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133743/0000/merge001_0.root']),
'mfv_neu_tau000100um_M0600_2017': (2, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133744/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133744/0000/merge001_0.root']),
'mfv_neu_tau000100um_M0800_2017': (2, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133745/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133745/0000/merge001_0.root']),
'mfv_neu_tau000100um_M1200_2017': (2, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133746/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133746/0000/merge001_0.root']),
'mfv_neu_tau000100um_M1600_2017': (2, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133747/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133747/0000/merge001_0.root']),
'mfv_neu_tau000100um_M3000_2017': (2, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133748/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133748/0000/merge001_0.root']),
'mfv_neu_tau000300um_M0400_2017': (2, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133749/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133749/0000/merge001_0.root']),
'mfv_neu_tau000300um_M0600_2017': (2, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133750/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133750/0000/merge001_0.root']),
'mfv_neu_tau000300um_M0800_2017': (2, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133751/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133751/0000/merge001_0.root']),
'mfv_neu_tau000300um_M1200_2017': (2, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133752/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133752/0000/merge001_0.root']),
'mfv_neu_tau000300um_M1600_2017': (2, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133753/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133753/0000/merge001_0.root']),
'mfv_neu_tau000300um_M3000_2017': (3, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133754/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133754/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133754/0000/merge002_0.root']),
'mfv_neu_tau001000um_M0400_2017': (2, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133755/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133755/0000/merge001_0.root']),
'mfv_neu_tau001000um_M0600_2017': (2, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133756/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133756/0000/merge001_0.root']),
'mfv_neu_tau001000um_M0800_2017': (2, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133757/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133757/0000/merge001_0.root']),
'mfv_neu_tau001000um_M1200_2017': (2, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133758/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133758/0000/merge001_0.root']),
'mfv_neu_tau001000um_M1600_2017': (3, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_150922/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_150922/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_150922/0000/merge002_0.root']),
'mfv_neu_tau001000um_M3000_2017': (3, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133800/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133800/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133800/0000/merge002_0.root']),
'mfv_neu_tau010000um_M0400_2017': (2, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133801/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133801/0000/merge001_0.root']),
'mfv_neu_tau010000um_M0600_2017': (2, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133802/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133802/0000/merge001_0.root']),
'mfv_neu_tau010000um_M0800_2017': (3, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133803/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133803/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133803/0000/merge002_0.root']),
'mfv_neu_tau010000um_M1200_2017': (3, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133804/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133804/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133804/0000/merge002_0.root']),
'mfv_neu_tau010000um_M1600_2017': (3, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133805/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133805/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133805/0000/merge002_0.root']),
'mfv_neu_tau010000um_M3000_2017': (4, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133806/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133806/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133806/0000/merge002_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133806/0000/merge003_0.root']),
'mfv_neu_tau030000um_M0400_2017': (2, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133807/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133807/0000/merge001_0.root']),
'mfv_neu_tau030000um_M0600_2017': (2, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133808/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133808/0000/merge001_0.root']),
'mfv_neu_tau030000um_M0800_2017': (2, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133809/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133809/0000/merge001_0.root']),
'mfv_neu_tau030000um_M1200_2017': (3, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133810/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133810/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133810/0000/merge002_0.root']),
'mfv_neu_tau030000um_M1600_2017': (3, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_150924/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_150924/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_150924/0000/merge002_0.root']),
'mfv_neu_tau030000um_M3000_2017': (3, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133812/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133812/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133812/0000/merge002_0.root']),
'mfv_stopdbardbar_tau000100um_M0400_2017': (1, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-400_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133813/0000/merge_0.root']),
'mfv_stopdbardbar_tau000100um_M0600_2017': (1, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-600_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133814/0000/merge_0.root']),
'mfv_stopdbardbar_tau000100um_M0800_2017': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-800_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133815/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-800_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133815/0000/merge001_0.root']),
'mfv_stopdbardbar_tau000100um_M1200_2017': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-1200_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133816/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1200_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133816/0000/merge001_0.root']),
'mfv_stopdbardbar_tau000100um_M1600_2017': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-1600_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133817/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1600_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133817/0000/merge001_0.root']),
'mfv_stopdbardbar_tau000100um_M3000_2017': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133818/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133818/0000/merge001_0.root']),
'mfv_stopdbardbar_tau000300um_M0400_2017': (1, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-400_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133819/0000/merge_0.root']),
'mfv_stopdbardbar_tau000300um_M0600_2017': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-600_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133820/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-600_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133820/0000/merge001_0.root']),
'mfv_stopdbardbar_tau000300um_M0800_2017': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-800_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133821/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-800_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133821/0000/merge001_0.root']),
'mfv_stopdbardbar_tau000300um_M1200_2017': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-1200_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133822/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1200_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133822/0000/merge001_0.root']),
'mfv_stopdbardbar_tau000300um_M1600_2017': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-1600_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_150929/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1600_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_150929/0000/merge001_0.root']),
'mfv_stopdbardbar_tau000300um_M3000_2017': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133824/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133824/0000/merge001_0.root']),
'mfv_stopdbardbar_tau001000um_M0400_2017': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-400_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_150931/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-400_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_150931/0000/merge001_0.root']),
'mfv_stopdbardbar_tau001000um_M0600_2017': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-600_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133826/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-600_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133826/0000/merge001_0.root']),
'mfv_stopdbardbar_tau001000um_M0800_2017': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-800_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133827/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-800_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133827/0000/merge001_0.root']),
'mfv_stopdbardbar_tau001000um_M1200_2017': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-1200_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133828/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1200_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133828/0000/merge001_0.root']),
'mfv_stopdbardbar_tau001000um_M1600_2017': (3, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-1600_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133829/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1600_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133829/0000/merge001_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1600_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133829/0000/merge002_0.root']),
'mfv_stopdbardbar_tau001000um_M3000_2017': (3, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133830/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133830/0000/merge001_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133830/0000/merge002_0.root']),
'mfv_stopdbardbar_tau010000um_M0400_2017': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-400_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133831/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-400_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133831/0000/merge001_0.root']),
'mfv_stopdbardbar_tau010000um_M0600_2017': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-600_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_150933/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-600_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_150933/0000/merge001_0.root']),
'mfv_stopdbardbar_tau010000um_M0800_2017': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-800_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_150934/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-800_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_150934/0000/merge001_0.root']),
'mfv_stopdbardbar_tau010000um_M1200_2017': (3, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-1200_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_150935/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1200_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_150935/0000/merge001_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1200_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_150935/0000/merge002_0.root']),
'mfv_stopdbardbar_tau010000um_M1600_2017': (3, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-1600_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133835/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1600_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133835/0000/merge001_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1600_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133835/0000/merge002_0.root']),
'mfv_stopdbardbar_tau010000um_M3000_2017': (3, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133836/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133836/0000/merge001_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133836/0000/merge002_0.root']),
'mfv_stopdbardbar_tau030000um_M0400_2017': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-400_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133837/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-400_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133837/0000/merge001_0.root']),
'mfv_stopdbardbar_tau030000um_M0600_2017': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-600_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133838/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-600_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133838/0000/merge001_0.root']),
'mfv_stopdbardbar_tau030000um_M0800_2017': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-800_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133839/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-800_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133839/0000/merge001_0.root']),
'mfv_stopdbardbar_tau030000um_M1200_2017': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-1200_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133840/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1200_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133840/0000/merge001_0.root']),
'mfv_stopdbardbar_tau030000um_M1600_2017': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-1600_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133841/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1600_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133841/0000/merge001_0.root']),
'mfv_stopdbardbar_tau030000um_M3000_2017': (3, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133842/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133842/0000/merge001_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV27m_2017/190808_133842/0000/merge002_0.root']),
'mfv_neu_tau000100um_M0400_2018': (2, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133748/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133748/0000/merge001_0.root']),
'mfv_neu_tau000100um_M0600_2018': (2, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133749/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133749/0000/merge001_0.root']),
'mfv_neu_tau000100um_M0800_2018': (2, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133750/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133750/0000/merge001_0.root']),
'mfv_neu_tau000100um_M1200_2018': (2, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133751/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133751/0000/merge001_0.root']),
'mfv_neu_tau000100um_M1600_2018': (2, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133752/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133752/0000/merge001_0.root']),
'mfv_neu_tau000100um_M3000_2018': (2, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133753/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133753/0000/merge001_0.root']),
'mfv_neu_tau000300um_M0400_2018': (2, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133754/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133754/0000/merge001_0.root']),
'mfv_neu_tau000300um_M0600_2018': (2, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133755/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133755/0000/merge001_0.root']),
'mfv_neu_tau000300um_M0800_2018': (2, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133756/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133756/0000/merge001_0.root']),
'mfv_neu_tau000300um_M1200_2018': (2, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133757/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133757/0000/merge001_0.root']),
'mfv_neu_tau000300um_M1600_2018': (2, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133758/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133758/0000/merge001_0.root']),
'mfv_neu_tau000300um_M3000_2018': (2, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133759/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133759/0000/merge001_0.root']),
'mfv_neu_tau001000um_M0400_2018': (2, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133800/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133800/0000/merge001_0.root']),
'mfv_neu_tau001000um_M0600_2018': (2, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133801/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133801/0000/merge001_0.root']),
'mfv_neu_tau001000um_M0800_2018': (2, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133802/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133802/0000/merge001_0.root']),
'mfv_neu_tau001000um_M1200_2018': (2, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133803/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133803/0000/merge001_0.root']),
'mfv_neu_tau001000um_M1600_2018': (3, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_150925/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_150925/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_150925/0000/merge002_0.root']),
'mfv_neu_tau001000um_M3000_2018': (3, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190809_094900/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190809_094900/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190809_094900/0000/merge002_0.root']),
'mfv_neu_tau010000um_M0400_2018': (2, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133805/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133805/0000/merge001_0.root']),
'mfv_neu_tau010000um_M0600_2018': (2, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133806/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133806/0000/merge001_0.root']),
'mfv_neu_tau010000um_M0800_2018': (3, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133807/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133807/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133807/0000/merge002_0.root']),
'mfv_neu_tau010000um_M1200_2018': (3, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_150926/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_150926/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_150926/0000/merge002_0.root']),
'mfv_neu_tau010000um_M1600_2018': (3, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_150927/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_150927/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_150927/0000/merge002_0.root']),
'mfv_neu_tau010000um_M3000_2018': (3, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133810/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133810/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133810/0000/merge002_0.root']),
'mfv_neu_tau030000um_M0400_2018': (2, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133811/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133811/0000/merge001_0.root']),
'mfv_neu_tau030000um_M0600_2018': (2, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133812/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133812/0000/merge001_0.root']),
'mfv_neu_tau030000um_M0800_2018': (2, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133813/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133813/0000/merge001_0.root']),
'mfv_neu_tau030000um_M1200_2018': (3, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133814/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133814/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133814/0000/merge002_0.root']),
'mfv_neu_tau030000um_M1600_2018': (3, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_150930/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_150930/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_150930/0000/merge002_0.root']),
'mfv_neu_tau030000um_M3000_2018': (3, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133816/0000/merge_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133816/0000/merge001_0.root', '/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133816/0000/merge002_0.root']),
'mfv_stopdbardbar_tau000100um_M0400_2018': (1, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-400_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133817/0000/merge_0.root']),
'mfv_stopdbardbar_tau000100um_M0600_2018': (1, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-600_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133818/0000/merge_0.root']),
'mfv_stopdbardbar_tau000100um_M0800_2018': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-800_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133819/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-800_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133819/0000/merge001_0.root']),
'mfv_stopdbardbar_tau000100um_M1200_2018': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-1200_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133820/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1200_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133820/0000/merge001_0.root']),
'mfv_stopdbardbar_tau000100um_M1600_2018': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-1600_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133821/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1600_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133821/0000/merge001_0.root']),
'mfv_stopdbardbar_tau000100um_M3000_2018': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133822/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133822/0000/merge001_0.root']),
'mfv_stopdbardbar_tau000300um_M0400_2018': (1, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-400_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_150932/0000/merge_0.root']),
'mfv_stopdbardbar_tau000300um_M0600_2018': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-600_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133824/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-600_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133824/0000/merge001_0.root']),
'mfv_stopdbardbar_tau000300um_M0800_2018': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-800_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133825/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-800_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133825/0000/merge001_0.root']),
'mfv_stopdbardbar_tau000300um_M1200_2018': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-1200_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_150936/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1200_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_150936/0000/merge001_0.root']),
'mfv_stopdbardbar_tau000300um_M1600_2018': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-1600_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_150937/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1600_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_150937/0000/merge001_0.root']),
'mfv_stopdbardbar_tau000300um_M3000_2018': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133828/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133828/0000/merge001_0.root']),
'mfv_stopdbardbar_tau001000um_M0400_2018': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-400_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133829/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-400_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133829/0000/merge001_0.root']),
'mfv_stopdbardbar_tau001000um_M0600_2018': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-600_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133830/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-600_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133830/0000/merge001_0.root']),
'mfv_stopdbardbar_tau001000um_M0800_2018': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-800_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_150938/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-800_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_150938/0000/merge001_0.root']),
'mfv_stopdbardbar_tau001000um_M1200_2018': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-1200_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133832/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1200_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133832/0000/merge001_0.root']),
'mfv_stopdbardbar_tau001000um_M1600_2018': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-1600_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190809_094929/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1600_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190809_094929/0000/merge001_0.root']),
'mfv_stopdbardbar_tau001000um_M3000_2018': (3, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190809_094930/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190809_094930/0000/merge001_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190809_094930/0000/merge002_0.root']),
'mfv_stopdbardbar_tau010000um_M0400_2018': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-400_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133833/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-400_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133833/0000/merge001_0.root']),
'mfv_stopdbardbar_tau010000um_M0600_2018': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-600_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133834/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-600_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133834/0000/merge001_0.root']),
'mfv_stopdbardbar_tau010000um_M0800_2018': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-800_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133835/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-800_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133835/0000/merge001_0.root']),
'mfv_stopdbardbar_tau010000um_M1200_2018': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-1200_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190809_033121/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1200_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190809_033121/0000/merge001_0.root']),
'mfv_stopdbardbar_tau010000um_M1600_2018': (3, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-1600_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190809_094935/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1600_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190809_094935/0000/merge001_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1600_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190809_094935/0000/merge002_0.root']),
'mfv_stopdbardbar_tau010000um_M3000_2018': (3, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190809_094936/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190809_094936/0000/merge001_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190809_094936/0000/merge002_0.root']),
'mfv_stopdbardbar_tau030000um_M0400_2018': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-400_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133837/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-400_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133837/0000/merge001_0.root']),
'mfv_stopdbardbar_tau030000um_M0600_2018': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-600_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133838/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-600_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133838/0000/merge001_0.root']),
'mfv_stopdbardbar_tau030000um_M0800_2018': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-800_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_150940/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-800_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_150940/0000/merge001_0.root']),
'mfv_stopdbardbar_tau030000um_M1200_2018': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-1200_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133840/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1200_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133840/0000/merge001_0.root']),
'mfv_stopdbardbar_tau030000um_M1600_2018': (2, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-1600_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133841/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-1600_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190808_133841/0000/merge001_0.root']),
'mfv_stopdbardbar_tau030000um_M3000_2018': (3, ['/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190809_094942/0000/merge_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190809_094942/0000/merge001_0.root', '/store/user/tucker/StopStopbarTo2Dbar2D_M-3000_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27m_2018/190809_094942/0000/merge002_0.root']),
'JetHT2017B': _fromnum0("/store/user/tucker/JetHT/NtupleV27m_2017/190802_112514", 25),
'JetHT2017C': _fromnum0("/store/user/tucker/JetHT/NtupleV27m_2017/190802_112515", 38),
'JetHT2017D': _fromnum0("/store/user/tucker/JetHT/NtupleV27m_2017/190802_112516", 18),
'JetHT2017E': (42, ['/store/user/tucker/JetHT/NtupleV27m_2017/190802_112517/0000/ntuple_%i.root' % i for i in chain(xrange(2,42), [0])] + ['/store/user/tucker/JetHT/NtupleV27m_2017/190806_004211/0000/ntuple_1.root']),
'JetHT2017F': _fromnum0("/store/user/tucker/JetHT/NtupleV27m_2017/190802_112518", 51),
'JetHT2018A': _fromnum0("/store/user/tucker/JetHT/NtupleV27m_2018/190802_113547", 115),
'JetHT2018B': _fromnum0("/store/user/tucker/JetHT/NtupleV27m_2018/190802_113548", 58),
'JetHT2018C': (107, ['/store/user/tucker/JetHT/NtupleV27m_2018/190803_214147/0000/ntuple_%i.root' % i for i in chain(xrange(68), xrange(69,107))] + ['/store/user/tucker/JetHT/NtupleV27m_2018/190805_064028/0000/ntuple_68.root']),
'JetHT2018D': _fromnum0("/store/user/tucker/JetHT/NtupleV27m_2018/190802_113550", 207),
})

_add_ds("ntuplev27m_ntkseeds", {
'qcdht0700_2017': _fromnum0("/store/user/tucker/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/NtupleV27m_NTkSeeds_2017/190802_115905", 16, fnbase="ntkseeds"),
'qcdht1000_2017': _fromnum0("/store/user/tucker/QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8/NtupleV27m_NTkSeeds_2017/190802_115906", 31, fnbase="ntkseeds"),
'qcdht1500_2017': _fromnum0("/store/user/tucker/QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8/NtupleV27m_NTkSeeds_2017/190802_115907", 63, fnbase="ntkseeds"),
'qcdht2000_2017': _fromnum0("/store/user/tucker/QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/NtupleV27m_NTkSeeds_2017/190802_115908", 30, fnbase="ntkseeds"),
'ttbarht0600_2017': _fromnum0("/store/user/tucker/TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV27m_NTkSeeds_2017/190802_115909", 4, fnbase="ntkseeds"),
'ttbarht0800_2017': _fromnum0("/store/user/tucker/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV27m_NTkSeeds_2017/190802_115910", 3, fnbase="ntkseeds"),
'ttbarht1200_2017': (1, ['/store/user/tucker/TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV27m_NTkSeeds_2017/190802_115911/0000/ntkseeds_0.root']),
'ttbarht2500_2017': (1, ['/store/user/tucker/TTJets_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV27m_NTkSeeds_2017/190802_115912/0000/ntkseeds_0.root']),
'qcdht0700_2018': _fromnum0("/store/user/tucker/QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV27m_NTkSeeds_2018/190802_115936", 23, fnbase="ntkseeds"),
'qcdht1000_2018': _fromnum0("/store/user/tucker/QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV27m_NTkSeeds_2018/190802_115937", 37, fnbase="ntkseeds"),
'qcdht1500_2018': _fromnum0("/store/user/tucker/QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV27m_NTkSeeds_2018/190802_115938", 76, fnbase="ntkseeds"),
'qcdht2000_2018': _fromnum0("/store/user/tucker/QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV27m_NTkSeeds_2018/190802_115939", 34, fnbase="ntkseeds"),
'ttbarht0600_2018': _fromnum0("/store/user/tucker/TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV27m_NTkSeeds_2018/190802_115940", 5, fnbase="ntkseeds"),
'ttbarht0800_2018': _fromnum0("/store/user/tucker/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV27m_NTkSeeds_2018/190802_115941", 4, fnbase="ntkseeds"),
'ttbarht1200_2018': (1, ['/store/user/tucker/TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV27m_NTkSeeds_2018/190802_115942/0000/ntkseeds_0.root']),
'ttbarht2500_2018': (1, ['/store/user/tucker/TTJets_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV27m_NTkSeeds_2018/190802_115943/0000/ntkseeds_0.root']),
'JetHT2017B': _fromnum0("/store/user/tucker/JetHT/NtupleV27m_NTkSeeds_2017/190802_115913", 62, fnbase="ntkseeds"),
'JetHT2017C': _fromnum0("/store/user/tucker/JetHT/NtupleV27m_NTkSeeds_2017/190802_115914", 95, fnbase="ntkseeds"),
'JetHT2017D': _fromnum0("/store/user/tucker/JetHT/NtupleV27m_NTkSeeds_2017/190802_115915", 44, fnbase="ntkseeds"),
'JetHT2017E': _fromnum0("/store/user/tucker/JetHT/NtupleV27m_NTkSeeds_2017/190802_115916", 103, fnbase="ntkseeds"),
'JetHT2017F': _fromnum0("/store/user/tucker/JetHT/NtupleV27m_NTkSeeds_2017/190802_115917", 127, fnbase="ntkseeds"),
'JetHT2018A': _fromnum0("/store/user/tucker/JetHT/NtupleV27m_NTkSeeds_2018/190802_115944", 286, fnbase="ntkseeds"),
'JetHT2018B': _fromnum0("/store/user/tucker/JetHT/NtupleV27m_NTkSeeds_2018/190802_115945", 145, fnbase="ntkseeds"),
'JetHT2018C': _fromnum0("/store/user/tucker/JetHT/NtupleV27m_NTkSeeds_2018/190802_115946", 107, fnbase="ntkseeds"),
'JetHT2018D': _fromnum0("/store/user/tucker/JetHT/NtupleV27m_NTkSeeds_2018/190802_115947", 516, fnbase="ntkseeds"),
})


_add_ds("ntuplev27m_norefitdzcut", {
'qcdht0700_2017': _fromnum0("/store/user/tucker/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/NtupleV27m_NoRefitDzCut_2017/190819_163618", 16),
'qcdht1000_2017': _fromnum0("/store/user/tucker/QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8/NtupleV27m_NoRefitDzCut_2017/190819_163619", 31),
'qcdht1500_2017': _fromnum0("/store/user/tucker/QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8/NtupleV27m_NoRefitDzCut_2017/190819_163620", 63),
'qcdht2000_2017': _fromnum0("/store/user/tucker/QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/NtupleV27m_NoRefitDzCut_2017/190819_163621", 30),
'ttbarht0600_2017': _fromnum0("/store/user/tucker/TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV27m_NoRefitDzCut_2017/190819_163622", 4),
'ttbarht0800_2017': _fromnum0("/store/user/tucker/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV27m_NoRefitDzCut_2017/190819_163623", 3),
'ttbarht1200_2017': (1, ['/store/user/tucker/TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV27m_NoRefitDzCut_2017/190819_163624/0000/ntuple_0.root']),
'ttbarht2500_2017': (1, ['/store/user/tucker/TTJets_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV27m_NoRefitDzCut_2017/190819_163625/0000/ntuple_0.root']),
'mfv_neu_tau010000um_M0800_2017': (3, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV27m_NoRefitDzCut_2017/merge/%s.root' % x for x in 'mrg', 'mrg001', 'mrg002']),
'qcdht0700_2018': _fromnum0("/store/user/tucker/QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV27m_NoRefitDzCut_2018/190819_163623", 23),
'qcdht1000_2018': _fromnum0("/store/user/tucker/QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV27m_NoRefitDzCut_2018/190819_163624", 37),
'qcdht1500_2018': _fromnum0("/store/user/tucker/QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV27m_NoRefitDzCut_2018/190819_163625", 76),
'qcdht2000_2018': _fromnum0("/store/user/tucker/QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV27m_NoRefitDzCut_2018/190819_163626", 34),
'ttbarht0600_2018': _fromnum0("/store/user/tucker/TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV27m_NoRefitDzCut_2018/190819_163627", 5),
'ttbarht0800_2018': _fromnum0("/store/user/tucker/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV27m_NoRefitDzCut_2018/190819_163628", 4),
'ttbarht1200_2018': (1, ['/store/user/tucker/TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV27m_NoRefitDzCut_2018/190819_163629/0000/ntuple_0.root']),
'ttbarht2500_2018': (1, ['/store/user/tucker/TTJets_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV27m_NoRefitDzCut_2018/190819_163630/0000/ntuple_0.root']),
'JetHT2017B': _fromnum0("/store/user/tucker/JetHT/NtupleV27m_NoRefitDzCut_2017/190819_163626", 41),
'JetHT2017C': (63, ['/store/user/tucker/JetHT/NtupleV27m_NoRefitDzCut_2017/190820_080617/0000/ntuple_%i.root' % i for i in [42, 51]] + ['/store/user/tucker/JetHT/NtupleV27m_NoRefitDzCut_2017/190819_163627/0000/ntuple_%i.root' % i for i in chain(xrange(42), xrange(43,51), xrange(52,63))]),
'JetHT2017D': _fromnum0("/store/user/tucker/JetHT/NtupleV27m_NoRefitDzCut_2017/190819_163628", 30),
'JetHT2017E': (69, ['/store/user/tucker/JetHT/NtupleV27m_NoRefitDzCut_2017/190819_163629/0000/ntuple_%i.root' % i for i in chain(xrange(3), xrange(4,53), xrange(54,69))] + ['/store/user/tucker/JetHT/NtupleV27m_NoRefitDzCut_2017/190820_080619/0000/ntuple_%i.root' % i for i in [3, 53]]),
'JetHT2017F': _fromnum0("/store/user/tucker/JetHT/NtupleV27m_NoRefitDzCut_2017/190819_163630", 85),
'JetHT2018A': _fromnum0("/store/user/tucker/JetHT/NtupleV27m_NoRefitDzCut_2018/190819_163631", 191),
'JetHT2018B': _fromnum0("/store/user/tucker/JetHT/NtupleV27m_NoRefitDzCut_2018/190819_163632", 97),
'JetHT2018C': (72, ['/store/user/tucker/JetHT/NtupleV27m_NoRefitDzCut_2018/190819_163633/0000/ntuple_%i.root' % i for i in chain(xrange(6), xrange(8,11), xrange(12,14), xrange(16,31), xrange(32,35), xrange(39,45), xrange(46,52), xrange(53,59), xrange(60,72), [37])] + ['/store/user/tucker/JetHT/NtupleV27m_NoRefitDzCut_2018/190820_080621/0000/ntuple_%i.root' % i for i in chain(xrange(6,8), xrange(14,16), xrange(35,37), [11, 31, 38, 45, 52, 59])]),
'JetHT2018D': _fromnum0("/store/user/tucker/JetHT/NtupleV27m_NoRefitDzCut_2018/190819_163634", 344),
})


_add_single_files('nr_k0ntuplev25mv1', '/store/user/wsun/croncopyeos/hadded/K0NtupleV25mv1', \
                      ['qcdht%04i_%i' % (x,y) for y in (2017,2018) for x in (700,1000,1500,2000)] + \
                      ['JetHT%i%s' % (y,x) for y in (2017,2018) for x in ('BCDEF' if y == 2017 else 'ABCD')])

for xx in '', '_NoRefitDzCut':
    _add_single_files('nr_trackmoverv27mv1' + xx.lower(), '/store/user/%s/hadded/TrackMoverV27mv1' % ('shogan/croncopyeos' if not xx else 'tucker') + xx, \
                          ['qcdht%04i_%i' % (x,y) for y in (2017,2018) for x in (700,1000,1500,2000)] + \
                          ['ttbarht%04i_%i' % (x,y) for y in (2017,2018) for x in (600,800,1200,2500)] + \
                          ['JetHT%i%s' % (y,x) for y in (2017,2018) for x in ('BCDEF' if y == 2017 else 'ABCD')])

    _add_single_files('nr_trackmovermctruthv27mv1' + xx.lower(), '/store/user/shogan/croncopyeos/hadded/TrackMoverMCTruthV27mv1' + xx, \
                          ['mfv_%s_tau%06ium_M%04i_%i' % (a,b,c,y) for y in (2017,2018) for a in ('neu','stopdbardbar') for b in (100,300,1000,10000,30000) for c in (400,600,800,1200,1600,3000)])

_add_single_files('nr_trackmovermctruthv27mv2', '/store/user/tucker/hadded/TrackMoverMCTruthV27mv2', \
                      ['mfv_%s_tau%06ium_M%04i_%i' % (a,b,c,y) for y in (2017,2018) for a in ('neu','stopdbardbar') for b in (100,300,1000,10000,30000) for c in (400,600,800,1200,1600,3000)])

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
        print colors.boldred('red means the file is OK,'), colors.green('green means it should stay in the removed list')
        for name, ds, fns in _removed:
            for fn in fns:
                print (colors.boldred if ok(fn) else colors.green)('%s %s %s' % (name, ds, fn))

    else:
        if not (len(sys.argv) == 1 and sys.argv[0].endswith('/SampleFiles.py')):
            sys.exit('did not understand argv %r' % sys.argv)
