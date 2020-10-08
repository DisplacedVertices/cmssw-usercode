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

_add_ds("ntuplev27bm", {
'qcdht0700_2017': _fromnum0("/store/user/joeyr/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/NtupleV27Bm_2017/191104_110502", 16),
'qcdht1000_2017': _fromnum0("/store/user/joeyr/QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8/NtupleV27Bm_2017/191104_110503", 31),
'qcdht1500_2017': _fromnum0("/store/user/joeyr/QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8/NtupleV27Bm_2017/191104_110504", 63),
'qcdht2000_2017': _fromnum0("/store/user/joeyr/QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/NtupleV27Bm_2017/191104_110505", 30),
'qcdht0300_2017': _fromnum0("/store/user/joeyr/QCD_HT300to500_TuneCP5_13TeV-madgraph-pythia8/NtupleV27Bm_2017/191104_110606", 19),
'qcdht0500_2017': (21, ['/store/user/joeyr/QCD_HT500to700_TuneCP5_13TeV-madgraph-pythia8/NtupleV27Bm_2017/191105_104225/0000/ntuple_%i.root' % i for i in [8, 10]] + ['/store/user/joeyr/QCD_HT500to700_TuneCP5_13TeV-madgraph-pythia8/NtupleV27Bm_2017/191104_110607/0000/ntuple_%i.root' % i for i in chain(xrange(8), xrange(11,17), xrange(18,21), [9])] + ['/store/user/joeyr/QCD_HT500to700_TuneCP5_13TeV-madgraph-pythia8/NtupleV27Bm_2017/191106_113753/0000/ntuple_17.root']),
'ttbar_2017': (51, ['/store/user/joeyr/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleV27Bm_2017/191106_100709/0000/ntuple_26.root'] + ['/store/user/joeyr/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleV27Bm_2017/191105_103920/0000/ntuple_%i.root' % i for i in chain(xrange(10,12), [5, 17, 40])] + ['/store/user/joeyr/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleV27Bm_2017/191104_110608/0000/ntuple_%i.root' % i for i in chain(xrange(5), xrange(6,10), xrange(12,17), xrange(18,26), xrange(27,40), xrange(41,51))]),
'mfv_neu_tau000100um_M0400_2017': (480, ['/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV27Bm_2017/191104_120357/0000/ntuple_%i.root' % i for i in chain(xrange(103,105), xrange(109,112), [85, 90, 94, 408, 415, 425])] + ['/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV27Bm_2017/191104_110506/0000/ntuple_%i.root' % i for i in chain(xrange(85), xrange(86,90), xrange(91,94), xrange(95,103), xrange(105,109), xrange(112,408), xrange(409,415), xrange(416,425), xrange(426,480))]),
'mfv_neu_tau000100um_M0600_2017': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV27Bm_2017/191104_110507", 500),
'mfv_neu_tau000100um_M0800_2017': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV27Bm_2017/191104_110508", 500),
'mfv_neu_tau000100um_M1200_2017': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV27Bm_2017/191104_110509", 500),
'mfv_neu_tau000100um_M1600_2017': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV27Bm_2017/191104_110510", 500),
'mfv_neu_tau000100um_M3000_2017': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV27Bm_2017/191104_110511", 500),
'mfv_neu_tau000300um_M0400_2017': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV27Bm_2017/191104_110512", 500),
'mfv_neu_tau000300um_M0600_2017': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV27Bm_2017/191104_110513", 490),
'mfv_neu_tau000300um_M0800_2017': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV27Bm_2017/191104_110514", 500),
'mfv_neu_tau000300um_M1200_2017': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV27Bm_2017/191104_110515", 500),
'mfv_neu_tau000300um_M1600_2017': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV27Bm_2017/191104_110516", 500),
'mfv_neu_tau000300um_M3000_2017': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV27Bm_2017/191104_110517", 490),
'mfv_neu_tau001000um_M0400_2017': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV27Bm_2017/191104_110518", 500),
'mfv_neu_tau001000um_M0600_2017': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV27Bm_2017/191104_110519", 500),
'mfv_neu_tau001000um_M0800_2017': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV27Bm_2017/191104_110520", 500),
'mfv_neu_tau001000um_M1200_2017': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV27Bm_2017/191104_110521", 480),
'mfv_neu_tau001000um_M1600_2017': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV27Bm_2017/191104_110522", 500),
'mfv_neu_tau001000um_M3000_2017': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV27Bm_2017/191104_110523", 490),
'mfv_neu_tau010000um_M0400_2017': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV27Bm_2017/191104_110524", 500),
'mfv_neu_tau010000um_M0600_2017': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV27Bm_2017/191104_110525", 500),
'mfv_neu_tau010000um_M0800_2017': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV27Bm_2017/191104_110526", 500),
'mfv_neu_tau010000um_M1200_2017': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV27Bm_2017/191104_110527", 500),
'mfv_neu_tau010000um_M1600_2017': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV27Bm_2017/191104_110528", 500),
'mfv_neu_tau010000um_M3000_2017': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV27Bm_2017/191104_110529", 490),
'mfv_neu_tau030000um_M0400_2017': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV27Bm_2017/191104_110530", 500),
'mfv_neu_tau030000um_M0600_2017': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV27Bm_2017/191104_110531", 500),
'mfv_neu_tau030000um_M0800_2017': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV27Bm_2017/191104_110532", 500),
'mfv_neu_tau030000um_M1200_2017': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV27Bm_2017/191104_110533", 500),
'mfv_neu_tau030000um_M1600_2017': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV27Bm_2017/191104_110534", 500),
'mfv_neu_tau030000um_M3000_2017': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV27Bm_2017/191104_110535", 500),
'mfv_stopdbardbar_tau000100um_M0400_2017': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-400_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV27Bm_2017/191104_110536", 500),
'mfv_stopdbardbar_tau000100um_M0600_2017': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-600_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV27Bm_2017/191104_110537", 480),
'mfv_stopdbardbar_tau000100um_M0800_2017': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-800_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV27Bm_2017/191104_110538", 500),
'mfv_stopdbardbar_tau000100um_M1200_2017': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-1200_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV27Bm_2017/191104_110539", 500),
'mfv_stopdbardbar_tau000100um_M1600_2017': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-1600_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV27Bm_2017/191104_110540", 500),
'mfv_stopdbardbar_tau000100um_M3000_2017': (475, ['/store/user/joeyr/StopStopbarTo2Dbar2D_M-3000_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV27Bm_2017/191104_110541/0000/ntuple_%i.root' % i for i in chain(xrange(147), xrange(148,475))] + ['/store/user/joeyr/StopStopbarTo2Dbar2D_M-3000_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV27Bm_2017/191105_103912/0000/ntuple_147.root']),
'mfv_stopdbardbar_tau000300um_M0400_2017': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-400_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV27Bm_2017/191104_110542", 500),
'mfv_stopdbardbar_tau000300um_M0600_2017': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-600_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV27Bm_2017/191104_110543", 500),
'mfv_stopdbardbar_tau000300um_M0800_2017': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-800_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV27Bm_2017/191104_110544", 500),
'mfv_stopdbardbar_tau000300um_M1200_2017': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-1200_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV27Bm_2017/191104_110545", 500),
'mfv_stopdbardbar_tau000300um_M1600_2017': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-1600_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV27Bm_2017/191104_110546", 500),
'mfv_stopdbardbar_tau000300um_M3000_2017': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-3000_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV27Bm_2017/191104_110547", 500),
'mfv_stopdbardbar_tau001000um_M0400_2017': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-400_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV27Bm_2017/191104_110548", 500),
'mfv_stopdbardbar_tau001000um_M0600_2017': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-600_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV27Bm_2017/191110_223404", 485),
'mfv_stopdbardbar_tau001000um_M0800_2017': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-800_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV27Bm_2017/191104_110550", 500),
'mfv_stopdbardbar_tau001000um_M1200_2017': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-1200_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV27Bm_2017/191104_110551", 495),
'mfv_stopdbardbar_tau001000um_M1600_2017': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-1600_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV27Bm_2017/191104_110552", 500),
'mfv_stopdbardbar_tau001000um_M3000_2017': (500, ['/store/user/joeyr/StopStopbarTo2Dbar2D_M-3000_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV27Bm_2017/191105_104126/0000/ntuple_%i.root' % i for i in chain(xrange(288,291), xrange(292,296), [284, 409, 412])] + ['/store/user/joeyr/StopStopbarTo2Dbar2D_M-3000_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV27Bm_2017/191104_110553/0000/ntuple_%i.root' % i for i in chain(xrange(66), xrange(68,284), xrange(285,288), xrange(296,336), xrange(337,409), xrange(410,412), xrange(413,500), [291])] + ['/store/user/joeyr/StopStopbarTo2Dbar2D_M-3000_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV27Bm_2017/191106_100710/0000/ntuple_%i.root' % i for i in chain(xrange(66,68), [336])]),
'mfv_stopdbardbar_tau010000um_M0400_2017': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-400_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV27Bm_2017/191104_110554", 500),
'mfv_stopdbardbar_tau010000um_M0600_2017': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-600_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV27Bm_2017/191104_110555", 500),
'mfv_stopdbardbar_tau010000um_M0800_2017': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-800_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV27Bm_2017/191104_110556", 490),
'mfv_stopdbardbar_tau010000um_M1200_2017': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-1200_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV27Bm_2017/191104_110557", 500),
'mfv_stopdbardbar_tau010000um_M1600_2017': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-1600_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV27Bm_2017/191104_110558", 500),
'mfv_stopdbardbar_tau010000um_M3000_2017': (500, ['/store/user/joeyr/StopStopbarTo2Dbar2D_M-3000_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV27Bm_2017/191106_100642/0000/ntuple_%i.root' % i for i in [12, 78, 80, 387, 466]] + ['/store/user/joeyr/StopStopbarTo2Dbar2D_M-3000_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV27Bm_2017/191104_110559/0000/ntuple_%i.root' % i for i in chain(xrange(12), xrange(13,78), xrange(81,387), xrange(388,466), xrange(467,500), [79])]),
'mfv_stopdbardbar_tau030000um_M0400_2017': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-400_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV27Bm_2017/191104_110600", 500),
'mfv_stopdbardbar_tau030000um_M0600_2017': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-600_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV27Bm_2017/191104_110601", 500),
'mfv_stopdbardbar_tau030000um_M0800_2017': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-800_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV27Bm_2017/191104_110602", 500),
'mfv_stopdbardbar_tau030000um_M1200_2017': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-1200_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV27Bm_2017/191104_110603", 490),
'mfv_stopdbardbar_tau030000um_M1600_2017': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-1600_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV27Bm_2017/191104_110604", 500),
'mfv_stopdbardbar_tau030000um_M3000_2017': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-3000_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV27Bm_2017/191104_110605", 500),
'qcdht0700_2018': (23, ['/store/user/joeyr/QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV27Bm_2018/191105_103930/0000/ntuple_%i.root' % i for i in [11, 17]] + ['/store/user/joeyr/QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV27Bm_2018/191104_110835/0000/ntuple_%i.root' % i for i in chain(xrange(1,9), xrange(12,17), xrange(18,23), [10])] + ['/store/user/joeyr/QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV27Bm_2018/191106_100603/0000/ntuple_%i.root' % i for i in [0, 9]]),
'qcdht1000_2018': _fromnum1("/store/user/jreicher/QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV27Bm_2018/191104_160834", 39),
'qcdht1500_2018': _fromnum0("/store/user/joeyr/QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV27Bm_2018/191104_110836", 76),
'qcdht2000_2018': _fromnum0("/store/user/joeyr/QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV27Bm_2018/191104_110837", 34),
'qcdht0300_2018': _fromnum0("/store/user/joeyr/QCD_HT300to500_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV27Bm_2018/191104_110938", 17),
'qcdht0500_2018': _fromnum0("/store/user/joeyr/QCD_HT500to700_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV27Bm_2018/191104_110939", 28),
'ttbar_2018': (70, ['/store/user/joeyr/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleV27Bm_2018/191104_110940/0000/ntuple_%i.root' % i for i in chain(xrange(4), xrange(6,70))] + ['/store/user/joeyr/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleV27Bm_2018/191108_095754/0000/ntuple_%i.root' % i for i in xrange(4,6)]),
'mfv_neu_tau000100um_M0400_2018': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27Bm_2018/191104_110838", 500),
'mfv_neu_tau000100um_M0600_2018': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27Bm_2018/191104_110839", 500),
'mfv_neu_tau000100um_M0800_2018': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27Bm_2018/191104_110840", 500),
'mfv_neu_tau000100um_M1200_2018': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27Bm_2018/191104_110841", 480),
'mfv_neu_tau000100um_M1600_2018': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27Bm_2018/191104_110842", 480),
'mfv_neu_tau000100um_M3000_2018': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27Bm_2018/191104_110843", 500),
'mfv_neu_tau000300um_M0400_2018': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27Bm_2018/191104_110844", 500),
'mfv_neu_tau000300um_M0600_2018': (500, ['/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27Bm_2018/191105_104132/0000/ntuple_%i.root' % i for i in chain(xrange(344,346), xrange(352,354), xrange(355,357), xrange(360,367), xrange(368,373), xrange(374,378), xrange(379,382), xrange(383,385), xrange(386,388), [332, 338, 348, 358])] + ['/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27Bm_2018/191104_110845/0000/ntuple_%i.root' % i for i in chain(xrange(332), xrange(333,338), xrange(339,344), xrange(346,348), xrange(349,352), xrange(388,500), [354, 357, 359, 367, 373, 378, 382, 385])]),
'mfv_neu_tau000300um_M0800_2018': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27Bm_2018/191104_110846", 500),
'mfv_neu_tau000300um_M1200_2018': (500, ['/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27Bm_2018/191104_110847/0000/ntuple_%i.root' % i for i in chain(xrange(380), xrange(381,384), xrange(385,389), xrange(390,403), xrange(404,406), xrange(409,411), xrange(422,500), [416, 420])] + ['/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27Bm_2018/191105_103925/0000/ntuple_%i.root' % i for i in chain(xrange(406,409), xrange(411,416), xrange(417,420), [380, 384, 389, 403, 421])]),
'mfv_neu_tau000300um_M1600_2018': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27Bm_2018/191104_110848", 500),
'mfv_neu_tau000300um_M3000_2018': (500, ['/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27Bm_2018/191105_104206/0000/ntuple_%i.root' % i for i in chain(xrange(63,65), xrange(67,73), xrange(77,87), xrange(88,90), xrange(405,409), [74, 91, 97, 100, 103, 160, 162, 171])] + ['/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27Bm_2018/191104_110849/0000/ntuple_%i.root' % i for i in chain(xrange(63), xrange(65,67), xrange(75,77), xrange(92,97), xrange(98,100), xrange(101,103), xrange(104,160), xrange(163,171), xrange(172,405), xrange(409,500), [73, 87, 90, 161])]),
'mfv_neu_tau001000um_M0400_2018': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27Bm_2018/191104_110850", 485),
'mfv_neu_tau001000um_M0600_2018': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27Bm_2018/191104_110851", 500),
'mfv_neu_tau001000um_M0800_2018': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27Bm_2018/191104_110852", 500),
'mfv_neu_tau001000um_M1200_2018': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27Bm_2018/191104_110853", 500),
'mfv_neu_tau001000um_M1600_2018': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27Bm_2018/191104_110854", 500),
'mfv_neu_tau001000um_M3000_2018': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27Bm_2018/191104_110855", 500),
'mfv_neu_tau010000um_M0400_2018': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27Bm_2018/191104_110856", 500),
'mfv_neu_tau010000um_M0600_2018': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27Bm_2018/191104_110857", 490),
'mfv_neu_tau010000um_M0800_2018': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27Bm_2018/191104_110858", 500),
'mfv_neu_tau010000um_M1200_2018': (500, ['/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27Bm_2018/191104_110859/0000/ntuple_%i.root' % i for i in chain(xrange(5), xrange(6,35), xrange(36,38), xrange(39,57), xrange(58,68), xrange(69,82), xrange(83,86), xrange(87,95), xrange(96,106), xrange(107,113), xrange(116,119), xrange(120,170), xrange(171,177), xrange(178,186), xrange(187,205), xrange(208,211), xrange(212,216), xrange(218,230), xrange(231,247), xrange(248,251), xrange(252,305), xrange(306,328), xrange(330,346), xrange(347,354), xrange(355,358), xrange(359,385), xrange(386,398), xrange(399,408), xrange(409,411), xrange(412,417), xrange(418,422), xrange(427,433), xrange(437,455), xrange(456,472), xrange(473,500), [114, 206, 423, 434])] + ['/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27Bm_2018/191106_100638/0000/ntuple_%i.root' % i for i in chain(xrange(216,218), xrange(328,330), xrange(424,427), xrange(435,437), [5, 35, 38, 57, 68, 82, 86, 95, 106, 113, 115, 119, 170, 177, 186, 205, 207, 211, 230, 247, 251, 305, 346, 354, 358, 385, 398, 408, 411, 417, 422, 433, 455, 472])]),
'mfv_neu_tau010000um_M1600_2018': (500, ['/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27Bm_2018/191106_100643/0000/ntuple_%i.root' % i for i in chain(xrange(4), xrange(10,14), xrange(15,18), xrange(21,23), xrange(26,34), xrange(40,42), xrange(43,46), xrange(47,53), xrange(54,56), xrange(62,66), xrange(67,71), xrange(74,82), xrange(83,86), xrange(87,90), xrange(91,93), xrange(95,100), xrange(104,106), xrange(107,110), xrange(111,115), xrange(116,119), xrange(121,125), xrange(126,128), xrange(138,143), xrange(146,148), xrange(149,159), xrange(161,163), xrange(170,172), xrange(175,178), xrange(194,198), xrange(202,204), xrange(211,214), xrange(219,221), xrange(222,227), xrange(232,237), xrange(238,243), xrange(245,249), xrange(257,260), xrange(265,269), xrange(271,275), xrange(282,284), xrange(285,290), xrange(291,294), xrange(296,298), xrange(299,301), xrange(307,310), xrange(314,319), xrange(327,331), xrange(332,334), xrange(335,342), xrange(347,351), xrange(359,363), xrange(366,370), xrange(372,375), xrange(388,392), xrange(397,400), xrange(401,403), xrange(406,410), xrange(411,414), xrange(415,419), xrange(434,436), xrange(438,440), xrange(441,443), xrange(445,447), xrange(463,465), xrange(467,470), xrange(484,486), xrange(497,500), [7, 24, 57, 72, 102, 129, 133, 144, 164, 168, 179, 181, 186, 189, 200, 207, 209, 217, 229, 250, 252, 255, 263, 277, 279, 320, 322, 325, 344, 353, 356, 376, 378, 381, 385, 393, 395, 421, 424, 426, 448, 450, 452, 455, 457, 460, 471, 476, 481, 488, 493, 495])] + ['/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27Bm_2018/191104_110900/0000/ntuple_%i.root' % i for i in chain(xrange(4,7), xrange(8,10), xrange(18,21), xrange(34,40), xrange(58,62), xrange(93,95), xrange(100,102), xrange(119,121), xrange(130,133), xrange(134,138), xrange(159,161), xrange(165,168), xrange(172,175), xrange(182,186), xrange(187,189), xrange(190,194), xrange(198,200), xrange(204,207), xrange(214,217), xrange(227,229), xrange(230,232), xrange(243,245), xrange(253,255), xrange(260,263), xrange(269,271), xrange(275,277), xrange(280,282), xrange(294,296), xrange(301,307), xrange(310,314), xrange(323,325), xrange(342,344), xrange(345,347), xrange(351,353), xrange(354,356), xrange(357,359), xrange(363,366), xrange(370,372), xrange(379,381), xrange(382,385), xrange(386,388), xrange(403,406), xrange(419,421), xrange(422,424), xrange(427,434), xrange(436,438), xrange(443,445), xrange(453,455), xrange(458,460), xrange(461,463), xrange(465,467), xrange(472,476), xrange(477,481), xrange(482,484), xrange(486,488), xrange(489,493), [14, 23, 25, 42, 46, 53, 56, 66, 71, 73, 82, 86, 90, 103, 106, 110, 115, 125, 128, 143, 145, 148, 163, 169, 178, 180, 201, 208, 210, 218, 221, 237, 249, 251, 256, 264, 278, 284, 290, 298, 319, 321, 326, 331, 334, 375, 377, 392, 394, 396, 400, 410, 414, 425, 440, 447, 449, 451, 456, 470, 494, 496])]),
'mfv_neu_tau010000um_M3000_2018': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27Bm_2018/191104_110901", 500),
'mfv_neu_tau030000um_M0400_2018': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27Bm_2018/191104_110902", 500),
'mfv_neu_tau030000um_M0600_2018': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27Bm_2018/191104_110903", 500),
'mfv_neu_tau030000um_M0800_2018': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27Bm_2018/191104_110904", 500),
'mfv_neu_tau030000um_M1200_2018': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27Bm_2018/191104_110905", 500),
'mfv_neu_tau030000um_M1600_2018': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27Bm_2018/191104_110906", 500),
'mfv_neu_tau030000um_M3000_2018': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27Bm_2018/191104_110907", 500),
'mfv_stopdbardbar_tau000100um_M0400_2018': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-400_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27Bm_2018/191104_110908", 500),
'mfv_stopdbardbar_tau000100um_M0600_2018': (500, ['/store/user/joeyr/StopStopbarTo2Dbar2D_M-600_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27Bm_2018/191104_110909/0000/ntuple_%i.root' % i for i in chain(xrange(51), xrange(54,57), xrange(58,60), xrange(62,67), xrange(70,78), xrange(80,83), xrange(164,167), xrange(178,180), xrange(212,214), xrange(215,500), [68, 86, 91, 169, 176, 183, 185, 210])] + ['/store/user/joeyr/StopStopbarTo2Dbar2D_M-600_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27Bm_2018/191106_100536/0000/ntuple_%i.root' % i for i in chain(xrange(51,54), xrange(60,62), xrange(78,80), xrange(83,86), xrange(87,91), xrange(92,164), xrange(167,169), xrange(170,176), xrange(180,183), xrange(186,210), [57, 67, 69, 177, 184, 211, 214])]),
'mfv_stopdbardbar_tau000100um_M0800_2018': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-800_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27Bm_2018/191104_110910", 500),
'mfv_stopdbardbar_tau000100um_M1200_2018': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-1200_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27Bm_2018/191104_110911", 500),
'mfv_stopdbardbar_tau000100um_M1600_2018': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-1600_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27Bm_2018/191104_110912", 500),
'mfv_stopdbardbar_tau000100um_M3000_2018': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-3000_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27Bm_2018/191104_110913", 500),
'mfv_stopdbardbar_tau000300um_M0400_2018': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-400_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27Bm_2018/191104_110914", 500),
'mfv_stopdbardbar_tau000300um_M0600_2018': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-600_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27Bm_2018/191104_110915", 500),
'mfv_stopdbardbar_tau000300um_M0800_2018': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-800_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27Bm_2018/191104_110916", 440),
'mfv_stopdbardbar_tau000300um_M1200_2018': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-1200_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27Bm_2018/191104_110917", 500),
'mfv_stopdbardbar_tau000300um_M1600_2018': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-1600_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27Bm_2018/191104_110918", 480),
'mfv_stopdbardbar_tau000300um_M3000_2018': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-3000_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27Bm_2018/191104_110919", 500),
'mfv_stopdbardbar_tau001000um_M0400_2018': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-400_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27Bm_2018/191104_110920", 500),
'mfv_stopdbardbar_tau001000um_M0600_2018': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-600_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27Bm_2018/191104_110921", 500),
'mfv_stopdbardbar_tau001000um_M0800_2018': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-800_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27Bm_2018/191104_110922", 485),
'mfv_stopdbardbar_tau001000um_M1200_2018': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-1200_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27Bm_2018/191104_110923", 500),
'mfv_stopdbardbar_tau001000um_M1600_2018': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-1600_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27Bm_2018/191104_110924", 480),
'mfv_stopdbardbar_tau001000um_M3000_2018': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-3000_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27Bm_2018/191104_110925", 500),
'mfv_stopdbardbar_tau010000um_M0400_2018': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-400_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27Bm_2018/191104_110926", 500),
'mfv_stopdbardbar_tau010000um_M0600_2018': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-600_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27Bm_2018/191104_110927", 500),
'mfv_stopdbardbar_tau010000um_M0800_2018': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-800_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27Bm_2018/191104_110928", 500),
'mfv_stopdbardbar_tau010000um_M1200_2018': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-1200_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27Bm_2018/191104_110929", 500),
'mfv_stopdbardbar_tau010000um_M1600_2018': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-1600_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27Bm_2018/191104_110930", 500),
'mfv_stopdbardbar_tau010000um_M3000_2018': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-3000_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27Bm_2018/191104_110931", 500),
'mfv_stopdbardbar_tau030000um_M0400_2018': _fromnum1("/store/user/jreicher/StopStopbarTo2Dbar2D_M-400_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27Bm_2018/191111_033328", 49),
'mfv_stopdbardbar_tau030000um_M0600_2018': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-600_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27Bm_2018/191110_223427", 495),
'mfv_stopdbardbar_tau030000um_M0800_2018': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-800_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27Bm_2018/191104_110934", 500),
'mfv_stopdbardbar_tau030000um_M1200_2018': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-1200_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27Bm_2018/191104_110935", 500),
'mfv_stopdbardbar_tau030000um_M1600_2018': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-1600_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27Bm_2018/191104_110936", 500),
'mfv_stopdbardbar_tau030000um_M3000_2018': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-3000_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27Bm_2018/191104_110937", 500),
})

_add_ds("ntuplev27p1bm", {   
'qcdht0300_2017': _fromnum0("/store/user/joeyr/QCD_HT300to500_TuneCP5_13TeV-madgraph-pythia8/NtupleV27p1Bm_2017/200130_104322", 19),
'qcdht0500_2017': _fromnum0("/store/user/joeyr/QCD_HT500to700_TuneCP5_13TeV-madgraph-pythia8/NtupleV27p1Bm_2017/200130_104323", 21),
'qcdht0700_2017': _fromnum0("/store/user/joeyr/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/NtupleV27p1Bm_2017/200129_170358", 16),
'qcdht1000_2017': _fromnum0("/store/user/joeyr/QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8/NtupleV27p1Bm_2017/200129_170359", 31),
'qcdht1500_2017': _fromnum0("/store/user/joeyr/QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8/NtupleV27p1Bm_2017/200129_170400", 63),
'qcdht2000_2017': _fromnum0("/store/user/joeyr/QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/NtupleV27p1Bm_2017/200129_170401", 30),
'qcdbenrichedht0300_2017': _fromnum0("/store/user/joeyr/QCD_bEnriched_HT300to500_TuneCP5_13TeV-madgraph-pythia8/NtupleV27p1Bm_2017/200427_193432", 2),
'qcdbenrichedht0300ext_2017': (1, ['/store/user/joeyr/QCD_bEnriched_HT300to500_TuneCP5_13TeV-madgraph-pythia8/NtupleV27p1Bm_2017/200427_193433/0000/ntuple_0.root']),
'qcdbenrichedht0500_2017': _fromnum0("/store/user/joeyr/QCD_bEnriched_HT500to700_TuneCP5_13TeV-madgraph-pythia8/NtupleV27p1Bm_2017/200427_193434", 2),
'qcdbenrichedht0500ext_2017': (1, ['/store/user/joeyr/QCD_bEnriched_HT500to700_TuneCP5_13TeV-madgraph-pythia8/NtupleV27p1Bm_2017/200427_193435/0000/ntuple_0.root']),
'qcdbenrichedht0700_2017': (1, ['/store/user/joeyr/QCD_bEnriched_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/NtupleV27p1Bm_2017/200427_193436/0000/ntuple_0.root']),
'qcdbenrichedht0700ext_2017': (1, ['/store/user/joeyr/QCD_bEnriched_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/NtupleV27p1Bm_2017/200427_193437/0000/ntuple_0.root']),
'qcdbenrichedht1000_2017': (1, ['/store/user/joeyr/QCD_bEnriched_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8/NtupleV27p1Bm_2017/200427_193438/0000/ntuple_0.root']),
'qcdbenrichedht1000ext_2017': (1, ['/store/user/joeyr/QCD_bEnriched_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8/NtupleV27p1Bm_2017/200427_193439/0000/ntuple_0.root']),
'qcdbgenfilterht0300_2017': _fromnum0("/store/user/joeyr/QCD_HT300to500_BGenFilter_TuneCP5_13TeV-madgraph-pythia8/NtupleV27p1Bm_2017/200428_155854", 9),
'qcdbgenfilterht0500_2017': _fromnum0("/store/user/joeyr/QCD_HT500to700_BGenFilter_TuneCP5_13TeV-madgraph-pythia8/NtupleV27p1Bm_2017/200428_155855", 12),
'qcdbgenfilterht0700_2017': _fromnum0("/store/user/joeyr/QCD_HT700to1000_BGenFilter_TuneCP5_13TeV-madgraph-pythia8/NtupleV27p1Bm_2017/200428_155856", 3),
'qcdbgenfilterht0700ext_2017': _fromnum0("/store/user/joeyr/QCD_HT700to1000_BGenFilter_TuneCP5_13TeV-madgraph-pythia8/NtupleV27p1Bm_2017/200428_155857", 15),
'qcdbgenfilterht1000_2017': _fromnum0("/store/user/joeyr/QCD_HT1000to1500_BGenFilter_TuneCP5_13TeV-madgraph-pythia8/NtupleV27p1Bm_2017/200428_155858", 4),
'ttbar_2017': _fromnum0("/store/user/joeyr/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleV27p1Bm_2017/200129_170504", 51),
'mfv_neu_tau000100um_M0400_2017': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV27p1Bm_2017/200129_170402", 480),
'mfv_neu_tau000100um_M0600_2017': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV27p1Bm_2017/200130_104223", 500),
'mfv_neu_tau000100um_M0800_2017': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV27p1Bm_2017/200129_170404", 500),
'mfv_neu_tau000100um_M1200_2017': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV27p1Bm_2017/200129_170405", 500),
'mfv_neu_tau000100um_M1600_2017': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV27p1Bm_2017/200129_170406", 500),
'mfv_neu_tau000100um_M3000_2017': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV27p1Bm_2017/200129_170407", 500),
'mfv_neu_tau000300um_M0400_2017': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV27p1Bm_2017/200129_170408", 500),
'mfv_neu_tau000300um_M0600_2017': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV27p1Bm_2017/200129_170409", 490),
'mfv_neu_tau000300um_M0800_2017': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV27p1Bm_2017/200129_170410", 500),
'mfv_neu_tau000300um_M1200_2017': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV27p1Bm_2017/200129_170411", 500),
'mfv_neu_tau000300um_M1600_2017': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV27p1Bm_2017/200129_170412", 500),
'mfv_neu_tau000300um_M3000_2017': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV27p1Bm_2017/200129_170413", 490),
'mfv_neu_tau001000um_M0400_2017': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV27p1Bm_2017/200129_170414", 500),
'mfv_neu_tau001000um_M0600_2017': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV27p1Bm_2017/200129_170415", 500),
'mfv_neu_tau001000um_M0800_2017': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV27p1Bm_2017/200129_170416", 500),
'mfv_neu_tau001000um_M1200_2017': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV27p1Bm_2017/200129_170417", 480),
'mfv_neu_tau001000um_M1600_2017': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV27p1Bm_2017/200129_170418", 500),
'mfv_neu_tau001000um_M3000_2017': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV27p1Bm_2017/200129_170419", 490),
'mfv_neu_tau010000um_M0400_2017': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV27p1Bm_2017/200129_170420", 500),
'mfv_neu_tau010000um_M0600_2017': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV27p1Bm_2017/200129_170421", 500),
'mfv_neu_tau010000um_M0800_2017': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV27p1Bm_2017/200129_170422", 500),
'mfv_neu_tau010000um_M1200_2017': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV27p1Bm_2017/200129_170423", 500),
'mfv_neu_tau010000um_M1600_2017': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV27p1Bm_2017/200129_170424", 500),
'mfv_neu_tau010000um_M3000_2017': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV27p1Bm_2017/200129_170425", 490),
'mfv_neu_tau030000um_M0400_2017': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV27p1Bm_2017/200129_170426", 500),
'mfv_neu_tau030000um_M0600_2017': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV27p1Bm_2017/200129_170427", 500),
'mfv_neu_tau030000um_M0800_2017': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV27p1Bm_2017/200129_170428", 500),
'mfv_neu_tau030000um_M1200_2017': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV27p1Bm_2017/200129_170429", 500),
'mfv_neu_tau030000um_M1600_2017': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV27p1Bm_2017/200129_170430", 500),
'mfv_neu_tau030000um_M3000_2017': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV27p1Bm_2017/200129_170431", 500),
'mfv_stopdbardbar_tau000100um_M0400_2017': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-400_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV27p1Bm_2017/200129_170432", 500),
'mfv_stopdbardbar_tau000100um_M0600_2017': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-600_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV27p1Bm_2017/200129_170433", 480),
'mfv_stopdbardbar_tau000100um_M0800_2017': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-800_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV27p1Bm_2017/200129_170434", 500),
'mfv_stopdbardbar_tau000100um_M1200_2017': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-1200_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV27p1Bm_2017/200129_170435", 500),
'mfv_stopdbardbar_tau000100um_M1600_2017': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-1600_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV27p1Bm_2017/200130_104256", 500),
'mfv_stopdbardbar_tau000100um_M3000_2017': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-3000_CTau-100um_TuneCP2_13TeV-pythia8/NtupleV27p1Bm_2017/200129_170437", 475),
'mfv_stopdbardbar_tau000300um_M0400_2017': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-400_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV27p1Bm_2017/200129_170438", 500),
'mfv_stopdbardbar_tau000300um_M0600_2017': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-600_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV27p1Bm_2017/200129_170439", 500),
'mfv_stopdbardbar_tau000300um_M0800_2017': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-800_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV27p1Bm_2017/200129_170440", 500),
'mfv_stopdbardbar_tau000300um_M1200_2017': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-1200_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV27p1Bm_2017/200129_170441", 500),
'mfv_stopdbardbar_tau000300um_M1600_2017': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-1600_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV27p1Bm_2017/200129_170442", 500),
'mfv_stopdbardbar_tau000300um_M3000_2017': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-3000_CTau-300um_TuneCP2_13TeV-pythia8/NtupleV27p1Bm_2017/200129_170443", 500),
'mfv_stopdbardbar_tau001000um_M0400_2017': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-400_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV27p1Bm_2017/200129_170444", 500),
'mfv_stopdbardbar_tau001000um_M0600_2017': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-600_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV27p1Bm_2017/200130_104305", 485),
'mfv_stopdbardbar_tau001000um_M0800_2017': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-800_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV27p1Bm_2017/200129_170446", 500),
'mfv_stopdbardbar_tau001000um_M1200_2017': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-1200_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV27p1Bm_2017/200129_170447", 495),
'mfv_stopdbardbar_tau001000um_M1600_2017': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-1600_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV27p1Bm_2017/200129_170448", 500),
'mfv_stopdbardbar_tau001000um_M3000_2017': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-3000_CTau-1mm_TuneCP2_13TeV-pythia8/NtupleV27p1Bm_2017/200129_170449", 500),
'mfv_stopdbardbar_tau010000um_M0400_2017': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-400_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV27p1Bm_2017/200129_170450", 500),
'mfv_stopdbardbar_tau010000um_M0600_2017': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-600_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV27p1Bm_2017/200129_170451", 500),
'mfv_stopdbardbar_tau010000um_M0800_2017': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-800_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV27p1Bm_2017/200129_170452", 490),
'mfv_stopdbardbar_tau010000um_M1200_2017': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-1200_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV27p1Bm_2017/200129_170453", 500),
'mfv_stopdbardbar_tau010000um_M1600_2017': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-1600_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV27p1Bm_2017/200129_170454", 500),
'mfv_stopdbardbar_tau010000um_M3000_2017': (500, ['/store/user/joeyr/StopStopbarTo2Dbar2D_M-3000_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV27p1Bm_2017/200129_170455/0000/ntuple_%i.root' % i for i in chain(xrange(86), xrange(87,500))] + ['/store/user/joeyr/StopStopbarTo2Dbar2D_M-3000_CTau-10mm_TuneCP2_13TeV-pythia8/NtupleV27p1Bm_2017/200130_130630/0000/ntuple_86.root']),
'mfv_stopdbardbar_tau030000um_M0400_2017': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-400_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV27p1Bm_2017/200129_170456", 500),
'mfv_stopdbardbar_tau030000um_M0600_2017': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-600_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV27p1Bm_2017/200129_170457", 500),
'mfv_stopdbardbar_tau030000um_M0800_2017': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-800_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV27p1Bm_2017/200129_170458", 500),
'mfv_stopdbardbar_tau030000um_M1200_2017': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-1200_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV27p1Bm_2017/200129_170459", 490),
'mfv_stopdbardbar_tau030000um_M1600_2017': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-1600_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV27p1Bm_2017/200129_170500", 500),
'mfv_stopdbardbar_tau030000um_M3000_2017': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-3000_CTau-30mm_TuneCP2_13TeV-pythia8/NtupleV27p1Bm_2017/200129_170501", 500),
'qcdht0700_2018': _fromnum0("/store/user/joeyr/QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV27p1Bm_2018/200130_104301", 23),
'qcdht1000_2018': _fromnum1("/store/user/jreicher/QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV27p1Bm_2018/200129_220451", 39),
'qcdht1500_2018': _fromnum0("/store/user/joeyr/QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV27p1Bm_2018/200129_170907", 76),
'qcdht2000_2018': _fromnum0("/store/user/joeyr/QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV27p1Bm_2018/200129_170908", 34),
'qcdht0300_2018': _fromnum0("/store/user/joeyr/QCD_HT300to500_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV27p1Bm_2018/200130_180445", 17),
'qcdht0500_2018': (28, ['/store/user/joeyr/QCD_HT500to700_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV27p1Bm_2018/200131_100651/0000/ntuple_%i.root' % i for i in [3, 20]] + ['/store/user/joeyr/QCD_HT500to700_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV27p1Bm_2018/200130_180436/0000/ntuple_12.root'] + ['/store/user/joeyr/QCD_HT500to700_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleV27p1Bm_2018/200129_171009/0000/ntuple_%i.root' % i for i in chain(xrange(3), xrange(4,12), xrange(13,20), xrange(21,28))]),
'ttbar_2018': _fromnum0("/store/user/joeyr/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleV27p1Bm_2018/200129_171010", 70),
'mfv_neu_tau000100um_M0400_2018': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27p1Bm_2018/200129_170909", 500),
'mfv_neu_tau000100um_M0600_2018': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27p1Bm_2018/200129_170910", 500),
'mfv_neu_tau000100um_M0800_2018': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27p1Bm_2018/200129_170911", 500),
'mfv_neu_tau000100um_M1200_2018': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27p1Bm_2018/200129_170912", 480),
'mfv_neu_tau000100um_M1600_2018': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27p1Bm_2018/200129_170913", 480),
'mfv_neu_tau000100um_M3000_2018': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27p1Bm_2018/200129_170914", 500),
'mfv_neu_tau000300um_M0400_2018': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27p1Bm_2018/200129_170915", 500),
'mfv_neu_tau000300um_M0600_2018': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27p1Bm_2018/200130_104311", 500),
'mfv_neu_tau000300um_M0800_2018': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27p1Bm_2018/200129_170917", 500),
'mfv_neu_tau000300um_M1200_2018': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27p1Bm_2018/200129_170918", 500),
'mfv_neu_tau000300um_M1600_2018': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27p1Bm_2018/200129_170919", 500),
'mfv_neu_tau000300um_M3000_2018': (500, ['/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27p1Bm_2018/200130_104315/0000/ntuple_%i.root' % i for i in chain(xrange(97), xrange(98,171), xrange(172,237), xrange(238,241), xrange(242,277), xrange(278,500))] + ['/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27p1Bm_2018/200130_161831/0000/ntuple_%i.root' % i for i in [97, 171, 237, 241, 277]]),
'mfv_neu_tau001000um_M0400_2018': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27p1Bm_2018/200129_170921", 485),
'mfv_neu_tau001000um_M0600_2018': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27p1Bm_2018/200129_170922", 500),
'mfv_neu_tau001000um_M0800_2018': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27p1Bm_2018/200129_170923", 500),
'mfv_neu_tau001000um_M1200_2018': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27p1Bm_2018/200129_170924", 500),
'mfv_neu_tau001000um_M1600_2018': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27p1Bm_2018/200129_170925", 500),
'mfv_neu_tau001000um_M3000_2018': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27p1Bm_2018/200129_170926", 500),
'mfv_neu_tau010000um_M0400_2018': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27p1Bm_2018/200129_170927", 500),
'mfv_neu_tau010000um_M0600_2018': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27p1Bm_2018/200129_170928", 490),
'mfv_neu_tau010000um_M0800_2018': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27p1Bm_2018/200129_170929", 500),
'mfv_neu_tau010000um_M1200_2018': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27p1Bm_2018/200129_170930", 500),
'mfv_neu_tau010000um_M1600_2018': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27p1Bm_2018/200129_170931", 500),
'mfv_neu_tau010000um_M3000_2018': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27p1Bm_2018/200129_170932", 500),
'mfv_neu_tau030000um_M0400_2018': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27p1Bm_2018/200129_170933", 500),
'mfv_neu_tau030000um_M0600_2018': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27p1Bm_2018/200129_170934", 500),
'mfv_neu_tau030000um_M0800_2018': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27p1Bm_2018/200129_170935", 500),
'mfv_neu_tau030000um_M1200_2018': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27p1Bm_2018/200129_170936", 500),
'mfv_neu_tau030000um_M1600_2018': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27p1Bm_2018/200129_170937", 500),
'mfv_neu_tau030000um_M3000_2018': _fromnum0("/store/user/joeyr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27p1Bm_2018/200129_170938", 500),
'mfv_stopdbardbar_tau000100um_M0400_2018': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-400_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27p1Bm_2018/200129_170939", 500),
'mfv_stopdbardbar_tau000100um_M0600_2018': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-600_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27p1Bm_2018/200129_170940", 500),
'mfv_stopdbardbar_tau000100um_M0800_2018': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-800_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27p1Bm_2018/200129_170941", 500),
'mfv_stopdbardbar_tau000100um_M1200_2018': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-1200_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27p1Bm_2018/200129_170942", 500),
'mfv_stopdbardbar_tau000100um_M1600_2018': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-1600_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27p1Bm_2018/200129_170943", 500),
'mfv_stopdbardbar_tau000100um_M3000_2018': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-3000_CTau-100um_TuneCP2_13TeV_2018-pythia8/NtupleV27p1Bm_2018/200129_170944", 500),
'mfv_stopdbardbar_tau000300um_M0400_2018': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-400_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27p1Bm_2018/200129_170945", 500),
'mfv_stopdbardbar_tau000300um_M0600_2018': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-600_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27p1Bm_2018/200131_100124", 500),
'mfv_stopdbardbar_tau000300um_M0800_2018': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-800_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27p1Bm_2018/200129_170947", 440),
'mfv_stopdbardbar_tau000300um_M1200_2018': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-1200_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27p1Bm_2018/200129_170948", 500),
'mfv_stopdbardbar_tau000300um_M1600_2018': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-1600_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27p1Bm_2018/200129_170949", 480),
'mfv_stopdbardbar_tau000300um_M3000_2018': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-3000_CTau-300um_TuneCP2_13TeV_2018-pythia8/NtupleV27p1Bm_2018/200130_104345", 500),
'mfv_stopdbardbar_tau001000um_M0400_2018': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-400_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27p1Bm_2018/200129_170951", 500),
'mfv_stopdbardbar_tau001000um_M0600_2018': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-600_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27p1Bm_2018/200129_170952", 500),
'mfv_stopdbardbar_tau001000um_M0800_2018': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-800_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27p1Bm_2018/200129_170953", 485),
'mfv_stopdbardbar_tau001000um_M1200_2018': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-1200_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27p1Bm_2018/200129_170954", 500),
'mfv_stopdbardbar_tau001000um_M1600_2018': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-1600_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27p1Bm_2018/200129_170955", 480),
'mfv_stopdbardbar_tau001000um_M3000_2018': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-3000_CTau-1mm_TuneCP2_13TeV_2018-pythia8/NtupleV27p1Bm_2018/200129_170956", 500),
'mfv_stopdbardbar_tau010000um_M0400_2018': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-400_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27p1Bm_2018/200129_170957", 500),
'mfv_stopdbardbar_tau010000um_M0600_2018': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-600_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27p1Bm_2018/200129_170958", 500),
'mfv_stopdbardbar_tau010000um_M0800_2018': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-800_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27p1Bm_2018/200129_170959", 500),
'mfv_stopdbardbar_tau010000um_M1200_2018': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-1200_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27p1Bm_2018/200129_171000", 500),
'mfv_stopdbardbar_tau010000um_M1600_2018': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-1600_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27p1Bm_2018/200129_171001", 500),
'mfv_stopdbardbar_tau010000um_M3000_2018': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-3000_CTau-10mm_TuneCP2_13TeV_2018-pythia8/NtupleV27p1Bm_2018/200131_100140", 500),
'mfv_stopdbardbar_tau030000um_M0400_2018': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-400_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27p1Bm_2018/200130_104358", 490),
'mfv_stopdbardbar_tau030000um_M0600_2018': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-600_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27p1Bm_2018/200129_171003", 495),
'mfv_stopdbardbar_tau030000um_M0800_2018': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-800_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27p1Bm_2018/200129_171004", 500),
'mfv_stopdbardbar_tau030000um_M1200_2018': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-1200_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27p1Bm_2018/200129_171005", 500),
'mfv_stopdbardbar_tau030000um_M1600_2018': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-1600_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27p1Bm_2018/200129_171006", 500),
'mfv_stopdbardbar_tau030000um_M3000_2018': _fromnum0("/store/user/joeyr/StopStopbarTo2Dbar2D_M-3000_CTau-30mm_TuneCP2_13TeV_2018-pythia8/NtupleV27p1Bm_2018/200129_171007", 500),
})


_add_ds("ntuplev27p1bm_ntkseeds", {
'qcdht0700_2017': _fromnum0("/store/user/joeyr/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/NtupleV27p1Bm_NTkSeedsRetry_2017/200413_142426", 16, fnbase="ntkseeds"),
'qcdht1000_2017': _fromnum0("/store/user/joeyr/QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8/NtupleV27p1Bm_NTkSeedsRetry_2017/200413_142427", 31, fnbase="ntkseeds"),
'qcdht1500_2017': _fromnum0("/store/user/joeyr/QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8/NtupleV27p1Bm_NTkSeedsRetry_2017/200413_142428", 63, fnbase="ntkseeds"),
'qcdht2000_2017': (30, ['/store/user/joeyr/QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/NtupleV27p1Bm_NTkSeedsRetry_2017/200414_095709/0000/ntkseeds_20.root'] + ['/store/user/joeyr/QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/NtupleV27p1Bm_NTkSeedsRetry_2017/200414_021826/0000/ntkseeds_24.root'] + ['/store/user/joeyr/QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/NtupleV27p1Bm_NTkSeedsRetry_2017/200414_074915/0000/ntkseeds_2.root'] + ['/store/user/joeyr/QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/NtupleV27p1Bm_NTkSeedsRetry_2017/200413_142429/0000/ntkseeds_%i.root' % i for i in chain(xrange(2), xrange(3,20), xrange(21,24), xrange(25,30))]),
'qcdht0300_2017': _fromnum0("/store/user/joeyr/QCD_HT300to500_TuneCP5_13TeV-madgraph-pythia8/NtupleV27p1Bm_NTkSeedsRetry_2017/200413_142430", 19, fnbase="ntkseeds"),
'qcdht0500_2017': _fromnum0("/store/user/joeyr/QCD_HT500to700_TuneCP5_13TeV-madgraph-pythia8/NtupleV27p1Bm_NTkSeedsRetry_2017/200413_142431", 21, fnbase="ntkseeds"),
'ttbar_2017': (51, ['/store/user/joeyr/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleV27p1Bm_NTkSeedsRetry_2017/200414_044846/0000/ntkseeds_5.root'] + ['/store/user/joeyr/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleV27p1Bm_NTkSeedsRetry_2017/200413_142432/0000/ntkseeds_%i.root' % i for i in chain(xrange(5), xrange(6,51))]),
'qcdbenrichedht0300_2017': _fromnum0("/store/user/joeyr/QCD_bEnriched_HT300to500_TuneCP5_13TeV-madgraph-pythia8/NtupleV27p1Bm_NTkSeeds_2017/200427_193519", 2, fnbase="ntkseeds"),
'qcdbenrichedht0300ext_2017': (1, ['/store/user/joeyr/QCD_bEnriched_HT300to500_TuneCP5_13TeV-madgraph-pythia8/NtupleV27p1Bm_NTkSeeds_2017/200427_193520/0000/ntkseeds_0.root']),
'qcdbenrichedht0500_2017': _fromnum0("/store/user/joeyr/QCD_bEnriched_HT500to700_TuneCP5_13TeV-madgraph-pythia8/NtupleV27p1Bm_NTkSeeds_2017/200427_193521", 2, fnbase="ntkseeds"),
'qcdbenrichedht0500ext_2017': (1, ['/store/user/joeyr/QCD_bEnriched_HT500to700_TuneCP5_13TeV-madgraph-pythia8/NtupleV27p1Bm_NTkSeeds_2017/200427_193522/0000/ntkseeds_0.root']),
'qcdbenrichedht0700_2017': (1, ['/store/user/joeyr/QCD_bEnriched_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/NtupleV27p1Bm_NTkSeeds_2017/200427_193523/0000/ntkseeds_0.root']),
'qcdbenrichedht0700ext_2017': (1, ['/store/user/joeyr/QCD_bEnriched_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/NtupleV27p1Bm_NTkSeeds_2017/200427_193524/0000/ntkseeds_0.root']),
'qcdbenrichedht1000_2017': (1, ['/store/user/joeyr/QCD_bEnriched_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8/NtupleV27p1Bm_NTkSeeds_2017/200427_193525/0000/ntkseeds_0.root']),
'qcdbenrichedht1000ext_2017': (1, ['/store/user/joeyr/QCD_bEnriched_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8/NtupleV27p1Bm_NTkSeeds_2017/200427_193526/0000/ntkseeds_0.root']),
'qcdbgenfilterht0300_2017': _fromnum0("/store/user/joeyr/QCD_HT300to500_BGenFilter_TuneCP5_13TeV-madgraph-pythia8/NtupleV27p1Bm_NTkSeeds_2017/200428_155945", 9, fnbase="ntkseeds"),
'qcdbgenfilterht0500_2017': _fromnum0("/store/user/joeyr/QCD_HT500to700_BGenFilter_TuneCP5_13TeV-madgraph-pythia8/NtupleV27p1Bm_NTkSeeds_2017/200428_155946", 12, fnbase="ntkseeds"),
'qcdbgenfilterht0700_2017': _fromnum0("/store/user/joeyr/QCD_HT700to1000_BGenFilter_TuneCP5_13TeV-madgraph-pythia8/NtupleV27p1Bm_NTkSeeds_2017/200428_155947", 3, fnbase="ntkseeds"),
'qcdbgenfilterht0700ext_2017': _fromnum0("/store/user/joeyr/QCD_HT700to1000_BGenFilter_TuneCP5_13TeV-madgraph-pythia8/NtupleV27p1Bm_NTkSeeds_2017/200428_155948", 15, fnbase="ntkseeds"),
'qcdbgenfilterht1000_2017': _fromnum0("/store/user/joeyr/QCD_HT1000to1500_BGenFilter_TuneCP5_13TeV-madgraph-pythia8/NtupleV27p1Bm_NTkSeeds_2017/200428_155949", 4, fnbase="ntkseeds"),
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
