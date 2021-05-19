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


# Shaun
_add_ds("multijet_32_exstats_c0", {
'qcdht0700_2017': (45, ['/store/user/shogan/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/TrackMoverV27mv1_c0_2017/200527_103148/0000/movedtree_24.root'] + ['/store/user/shogan/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/TrackMoverV27mv1_c0_2017/200518_095254/0000/movedtree_%i.root' % i for i in chain(xrange(24), xrange(25,45))]),
'qcdht1000_2017': _fromnum0("/store/user/shogan/QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8/TrackMoverV27mv1_c0_2017/200518_095255", 85, fnbase="movedtree"),
'qcdht1500_2017': (250, ['/store/user/shogan/QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8/TrackMoverV27mv1_c0_2017/200527_103201/0000/movedtree_%i.root' % i for i in chain(xrange(107,109), xrange(117,122), xrange(124,131), xrange(135,137), [96, 110, 112, 132])] + ['/store/user/shogan/QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8/TrackMoverV27mv1_c0_2017/200518_095256/0000/movedtree_%i.root' % i for i in chain(xrange(96), xrange(97,107), xrange(113,117), xrange(122,124), xrange(133,135), xrange(137,250), [109, 111, 131])]),
'qcdht2000_2017': (74, ['/store/user/shogan/QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/TrackMoverV27mv1_c0_2017/200518_095257/0000/movedtree_%i.root' % i for i in chain(xrange(28), xrange(29,74))] + ['/store/user/shogan/QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/TrackMoverV27mv1_c0_2017/200527_103149/0000/movedtree_28.root']),
'ttbarht0600_2017': _fromnum0("/store/user/shogan/TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mv1_c0_2017/200518_095258", 20, fnbase="movedtree"),
'ttbarht0800_2017': (8, ['/store/user/shogan/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mv1_c0_2017/200518_095259/0000/movedtree_%i.root' % i for i in [1, 7]] + ['/store/user/shogan/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mv1_c0_2017/200529_074930/0000/movedtree_%i.root' % i for i in [4, 6]] + ['/store/user/shogan/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mv1_c0_2017/200527_103152/0000/movedtree_%i.root' % i for i in chain(xrange(2,4), [0, 5])]),
'ttbarht1200_2017': _fromnum0("/store/user/shogan/TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mv1_c0_2017/200527_103151", 2, fnbase="movedtree"),
'ttbarht2500_2017': (1, ['/store/user/shogan/TTJets_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mv1_c0_2017/200518_095301/0000/movedtree_0.root']),
'qcdht0700_2018': _fromnum0("/store/user/shogan/QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mv1_c0_2018/200518_094617", 68, fnbase="movedtree"),
'qcdht1000_2018': _fromnum0("/store/user/shogan/QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mv1_c0_2018/200518_094618", 102, fnbase="movedtree"),
'qcdht1500_2018': _fromnum0("/store/user/shogan/QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mv1_c0_2018/200518_094619", 302, fnbase="movedtree"),
'qcdht2000_2018': _fromnum0("/store/user/shogan/QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mv1_c0_2018/200518_094620", 83, fnbase="movedtree"),
'ttbarht0600_2018': _fromnum0("/store/user/shogan/TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mv1_c0_2018/200518_094621", 25, fnbase="movedtree"),
'ttbarht0800_2018': _fromnum0("/store/user/shogan/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mv1_c0_2018/200518_094622", 11, fnbase="movedtree"),
'ttbarht1200_2018': _fromnum0("/store/user/shogan/TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mv1_c0_2018/200518_094623", 2, fnbase="movedtree"),
'ttbarht2500_2018': (1, ['/store/user/shogan/TTJets_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mv1_c0_2018/200518_094624/0000/movedtree_0.root']),
'JetHT2017B': (123, ['/store/user/shogan/JetHT/TrackMoverV27mv1_c0_2017/200527_103153/0000/movedtree_%i.root' % i for i in chain(xrange(80,82), xrange(101,103), xrange(105,116), xrange(117,123), [11, 21, 25, 29, 31, 33, 77, 84, 86, 88, 94])] + ['/store/user/shogan/JetHT/TrackMoverV27mv1_c0_2017/200518_095302/0000/movedtree_%i.root' % i for i in chain(xrange(11), xrange(12,21), xrange(22,25), xrange(26,29), xrange(34,77), xrange(78,80), xrange(82,84), xrange(89,94), xrange(95,101), xrange(103,105), [30, 32, 85, 87, 116])]),
'JetHT2017C': (189, ['/store/user/shogan/JetHT/TrackMoverV27mv1_c0_2017/200527_103156/0000/movedtree_%i.root' % i for i in [29, 42, 152, 177]] + ['/store/user/shogan/JetHT/TrackMoverV27mv1_c0_2017/200518_095303/0000/movedtree_%i.root' % i for i in chain(xrange(29), xrange(30,42), xrange(43,152), xrange(153,177), xrange(178,189))]),
'JetHT2017D': (88, ['/store/user/shogan/JetHT/TrackMoverV27mv1_c0_2017/200518_095304/0000/movedtree_%i.root' % i for i in chain(xrange(4), xrange(6,14), xrange(15,20), xrange(21,41), xrange(45,73), xrange(76,81), xrange(82,88), [42, 74])] + ['/store/user/shogan/JetHT/TrackMoverV27mv1_c0_2017/200527_103157/0000/movedtree_%i.root' % i for i in chain(xrange(4,6), xrange(43,45), [14, 20, 41, 73, 75, 81])]),
'JetHT2017E': (206, ['/store/user/shogan/JetHT/TrackMoverV27mv1_c0_2017/200601_080807/0000/movedtree_0.root'] + ['/store/user/shogan/JetHT/TrackMoverV27mv1_c0_2017/200527_103200/0000/movedtree_%i.root' % i for i in chain(xrange(69,71), [24, 38, 45, 48, 57, 63, 72, 83, 109])] + ['/store/user/shogan/JetHT/TrackMoverV27mv1_c0_2017/200518_095305/0000/movedtree_%i.root' % i for i in chain(xrange(1,24), xrange(25,38), xrange(39,45), xrange(46,48), xrange(49,57), xrange(58,63), xrange(64,69), xrange(73,83), xrange(84,109), xrange(110,206), [71])]),
'JetHT2017F': (254, ['/store/user/shogan/JetHT/TrackMoverV27mv1_c0_2017/200518_095306/0000/movedtree_%i.root' % i for i in chain(xrange(113), xrange(114,136), xrange(137,150), xrange(151,165), xrange(166,183), xrange(184,254))] + ['/store/user/shogan/JetHT/TrackMoverV27mv1_c0_2017/200529_074931/0000/movedtree_%i.root' % i for i in [113, 136, 150, 165, 183]]),
'JetHT2018A': _fromnum0("/store/user/shogan/JetHT/TrackMoverV27mv1_c0_2018/200518_094625", 571, fnbase="movedtree"),
'JetHT2018B': _fromnum0("/store/user/shogan/JetHT/TrackMoverV27mv1_c0_2018/200518_094626", 290, fnbase="movedtree"),
'JetHT2018C': _fromnum0("/store/user/shogan/JetHT/TrackMoverV27mv1_c0_2018/200518_094627", 214, fnbase="movedtree"),
'JetHT2018D': _fromnum0("/store/user/shogan/JetHT/TrackMoverV27mv1_c0_2018/200518_094628", 1032, fnbase="movedtree"),
})

_add_ds("multijet_32_exstats_c1", {
'qcdht0700_2017': _fromnum0("/store/user/shogan/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/TrackMoverV27mv1_c1_2017/200518_095351", 45, fnbase="movedtree"),
'qcdht1000_2017': (85, ['/store/user/shogan/QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8/TrackMoverV27mv1_c1_2017/200527_103351/0000/movedtree_%i.root' % i for i in chain(xrange(73,75), [0, 6, 10, 12, 15, 27, 29, 44, 51, 69, 84])] + ['/store/user/shogan/QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8/TrackMoverV27mv1_c1_2017/200529_075025/0000/movedtree_%i.root' % i for i in [3, 13, 19, 36, 38, 50, 53, 60]] + ['/store/user/shogan/QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8/TrackMoverV27mv1_c1_2017/200518_095352/0000/movedtree_%i.root' % i for i in chain(xrange(1,3), xrange(4,6), xrange(7,10), xrange(16,19), xrange(20,27), xrange(30,36), xrange(39,44), xrange(45,50), xrange(54,60), xrange(61,69), xrange(70,73), xrange(75,84), [11, 14, 28, 37, 52])]),
'qcdht1500_2017': _fromnum0("/store/user/shogan/QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8/TrackMoverV27mv1_c1_2017/200518_095353", 250, fnbase="movedtree"),
'qcdht2000_2017': (74, ['/store/user/shogan/QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/TrackMoverV27mv1_c1_2017/200527_103356/0000/movedtree_%i.root' % i for i in chain(xrange(5,7), [21, 31, 34, 49])] + ['/store/user/shogan/QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/TrackMoverV27mv1_c1_2017/200518_095354/0000/movedtree_%i.root' % i for i in chain(xrange(5), xrange(7,21), xrange(22,31), xrange(32,34), xrange(35,49), xrange(50,74))]),
'ttbarht0600_2017': (20, ['/store/user/shogan/TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mv1_c1_2017/200527_103354/0000/movedtree_%i.root' % i for i in [5, 13]] + ['/store/user/shogan/TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mv1_c1_2017/200518_095355/0000/movedtree_%i.root' % i for i in chain(xrange(5), xrange(6,13), xrange(14,20))]),
'ttbarht0800_2017': (8, ['/store/user/shogan/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mv1_c1_2017/200527_103355/0000/movedtree_%i.root' % i for i in xrange(2)] + ['/store/user/shogan/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mv1_c1_2017/200518_095356/0000/movedtree_%i.root' % i for i in xrange(2,8)]),
'ttbarht1200_2017': (2, ['/store/user/shogan/TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mv1_c1_2017/200527_103353/0000/movedtree_0.root'] + ['/store/user/shogan/TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mv1_c1_2017/200518_095357/0000/movedtree_1.root']),
'ttbarht2500_2017': (1, ['/store/user/shogan/TTJets_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mv1_c1_2017/200518_095358/0000/movedtree_0.root']),
'qcdht0700_2018': _fromnum0("/store/user/shogan/QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mv1_c1_2018/200518_094808", 68, fnbase="movedtree"),
'qcdht1000_2018': _fromnum0("/store/user/shogan/QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mv1_c1_2018/200518_094809", 102, fnbase="movedtree"),
'qcdht1500_2018': (302, ['/store/user/shogan/QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mv1_c1_2018/200519_091209/0000/movedtree_%i.root' % i for i in [118, 142]] + ['/store/user/shogan/QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mv1_c1_2018/200518_094810/0000/movedtree_%i.root' % i for i in chain(xrange(118), xrange(119,142), xrange(143,302))]),
'qcdht2000_2018': _fromnum0("/store/user/shogan/QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mv1_c1_2018/200518_094811", 83, fnbase="movedtree"),
'ttbarht0600_2018': _fromnum0("/store/user/shogan/TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mv1_c1_2018/200518_094812", 25, fnbase="movedtree"),
'ttbarht0800_2018': _fromnum0("/store/user/shogan/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mv1_c1_2018/200518_094813", 11, fnbase="movedtree"),
'ttbarht1200_2018': _fromnum0("/store/user/shogan/TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mv1_c1_2018/200518_094814", 2, fnbase="movedtree"),
'ttbarht2500_2018': (1, ['/store/user/shogan/TTJets_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mv1_c1_2018/200518_094815/0000/movedtree_0.root']),
'JetHT2017B': _fromnum0("/store/user/shogan/JetHT/TrackMoverV27mv1_c1_2017/200518_095359", 123, fnbase="movedtree"),
'JetHT2017C': (189, ['/store/user/shogan/JetHT/TrackMoverV27mv1_c1_2017/200529_075026/0000/movedtree_%i.root' % i for i in chain(xrange(146,148), xrange(151,155), xrange(170,175), xrange(176,181), xrange(186,188), [124, 126, 129, 131, 136, 156, 159, 182, 184])] + ['/store/user/shogan/JetHT/TrackMoverV27mv1_c1_2017/200518_095400/0000/movedtree_%i.root' % i for i in chain(xrange(124), xrange(127,129), xrange(132,136), xrange(137,146), xrange(148,151), xrange(157,159), xrange(160,164), xrange(165,170), [125, 130, 155, 175, 181, 185, 188])] + ['/store/user/shogan/JetHT/TrackMoverV27mv1_c1_2017/200601_080836/0000/movedtree_%i.root' % i for i in [164, 183]]),
'JetHT2017D': (88, ['/store/user/shogan/JetHT/TrackMoverV27mv1_c1_2017/200518_095401/0000/movedtree_%i.root' % i for i in chain(xrange(3,5), xrange(11,14), xrange(35,38), xrange(43,88), [0, 6, 18, 21, 26, 30, 32, 39])] + ['/store/user/shogan/JetHT/TrackMoverV27mv1_c1_2017/200529_075029/0000/movedtree_%i.root' % i for i in chain(xrange(1,3), xrange(7,11), xrange(14,18), xrange(19,21), xrange(22,26), xrange(27,30), xrange(33,35), xrange(40,43), [5, 31, 38])]),
'JetHT2017E': (206, ['/store/user/shogan/JetHT/TrackMoverV27mv1_c1_2017/200601_080839/0000/movedtree_%i.root' % i for i in [36, 62, 114, 144]] + ['/store/user/shogan/JetHT/TrackMoverV27mv1_c1_2017/200518_095402/0000/movedtree_%i.root' % i for i in chain(xrange(12,14), xrange(18,22), xrange(23,25), xrange(29,32), xrange(37,39), xrange(44,46), xrange(51,53), xrange(67,72), xrange(74,77), xrange(79,81), xrange(90,92), xrange(95,97), xrange(123,126), xrange(133,135), xrange(142,144), xrange(145,147), xrange(157,159), xrange(166,168), xrange(171,206), [2, 4, 10, 27, 35, 47, 55, 57, 60, 64, 82, 85, 93, 100, 104, 106, 108, 115, 129, 131, 138, 140, 151, 161, 169])] + ['/store/user/shogan/JetHT/TrackMoverV27mv1_c1_2017/200529_075031/0000/movedtree_%i.root' % i for i in chain(xrange(2), xrange(5,10), xrange(14,18), xrange(25,27), xrange(32,35), xrange(39,44), xrange(48,51), xrange(53,55), xrange(58,60), xrange(65,67), xrange(72,74), xrange(77,79), xrange(83,85), xrange(86,90), xrange(97,100), xrange(101,104), xrange(109,114), xrange(116,123), xrange(126,129), xrange(135,138), xrange(147,151), xrange(152,157), xrange(159,161), xrange(162,166), [3, 11, 22, 28, 46, 56, 61, 63, 81, 92, 94, 105, 107, 130, 132, 139, 141, 168, 170])]),
'JetHT2017F': (254, ['/store/user/shogan/JetHT/TrackMoverV27mv1_c1_2017/200601_080838/0000/movedtree_142.root'] + ['/store/user/shogan/JetHT/TrackMoverV27mv1_c1_2017/200518_095403/0000/movedtree_%i.root' % i for i in chain(xrange(142), xrange(143,254))]),
'JetHT2018A': _fromnum0("/store/user/shogan/JetHT/TrackMoverV27mv1_c1_2018/200518_094816", 571, fnbase="movedtree"),
'JetHT2018B': _fromnum0("/store/user/shogan/JetHT/TrackMoverV27mv1_c1_2018/200518_094817", 290, fnbase="movedtree"),
'JetHT2018C': (214, ['/store/user/shogan/JetHT/TrackMoverV27mv1_c1_2018/200526_113502/0000/movedtree_189.root'] + ['/store/user/shogan/JetHT/TrackMoverV27mv1_c1_2018/200518_094818/0000/movedtree_%i.root' % i for i in chain(xrange(189), xrange(190,214))]),
'JetHT2018D': (1032, ['/store/user/shogan/JetHT/TrackMoverV27mv1_c1_2018/200518_094819' + '/%04i/movedtree_%i.root' % (i/1000,i) for i in chain(xrange(10), xrange(11,236), xrange(237,1032))] + ['/store/user/shogan/JetHT/TrackMoverV27mv1_c1_2018/200520_145015/0000/movedtree_%i.root' % i for i in [10, 236]]),
})

_add_ds("multijet_32_exstats_c2", {
'qcdht0700_2017': (45, ['/store/user/shogan/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/TrackMoverV27mv1_c2_2017/200518_095430/0000/movedtree_%i.root' % i for i in chain(xrange(38), xrange(39,45))] + ['/store/user/shogan/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/TrackMoverV27mv1_c2_2017/200529_075058/0000/movedtree_38.root']),
'qcdht1000_2017': (85, ['/store/user/shogan/QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8/TrackMoverV27mv1_c2_2017/200529_075100/0000/movedtree_%i.root' % i for i in [50, 60]] + ['/store/user/shogan/QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8/TrackMoverV27mv1_c2_2017/200518_095431/0000/movedtree_%i.root' % i for i in chain(xrange(50), xrange(51,60), xrange(61,85))]),
'qcdht1500_2017': _fromnum0("/store/user/shogan/QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8/TrackMoverV27mv1_c2_2017/200518_095432", 250, fnbase="movedtree"),
'qcdht2000_2017': _fromnum0("/store/user/shogan/QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/TrackMoverV27mv1_c2_2017/200518_095433", 74, fnbase="movedtree"),
'ttbarht0600_2017': _fromnum0("/store/user/shogan/TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mv1_c2_2017/200518_095434", 20, fnbase="movedtree"),
'ttbarht0800_2017': _fromnum0("/store/user/shogan/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mv1_c2_2017/200518_095435", 8, fnbase="movedtree"),
'ttbarht1200_2017': _fromnum0("/store/user/shogan/TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mv1_c2_2017/200518_095436", 2, fnbase="movedtree"),
'ttbarht2500_2017': (1, ['/store/user/shogan/TTJets_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mv1_c2_2017/200518_095437/0000/movedtree_0.root']),
'qcdht0700_2018': _fromnum0("/store/user/shogan/QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mv1_c2_2018/200518_094852", 68, fnbase="movedtree"),
'qcdht1000_2018': _fromnum0("/store/user/shogan/QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mv1_c2_2018/200518_094853", 102, fnbase="movedtree"),
'qcdht1500_2018': _fromnum0("/store/user/shogan/QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mv1_c2_2018/200518_094854", 302, fnbase="movedtree"),
'qcdht2000_2018': _fromnum0("/store/user/shogan/QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mv1_c2_2018/200518_094855", 83, fnbase="movedtree"),
'ttbarht0600_2018': _fromnum0("/store/user/shogan/TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mv1_c2_2018/200518_094856", 25, fnbase="movedtree"),
'ttbarht0800_2018': _fromnum0("/store/user/shogan/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mv1_c2_2018/200518_094857", 11, fnbase="movedtree"),
'ttbarht1200_2018': _fromnum0("/store/user/shogan/TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mv1_c2_2018/200518_094858", 2, fnbase="movedtree"),
'ttbarht2500_2018': (1, ['/store/user/shogan/TTJets_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mv1_c2_2018/200518_094859/0000/movedtree_0.root']),
'JetHT2017B': (123, ['/store/user/shogan/JetHT/TrackMoverV27mv1_c2_2017/200529_075102/0000/movedtree_%i.root' % i for i in [26, 81]] + ['/store/user/shogan/JetHT/TrackMoverV27mv1_c2_2017/200601_080902/0000/movedtree_120.root'] + ['/store/user/shogan/JetHT/TrackMoverV27mv1_c2_2017/200518_095438/0000/movedtree_%i.root' % i for i in chain(xrange(26), xrange(27,81), xrange(82,120), xrange(121,123))]),
'JetHT2017C': (189, ['/store/user/shogan/JetHT/TrackMoverV27mv1_c2_2017/200518_095439/0000/movedtree_%i.root' % i for i in chain(xrange(3,5), xrange(11,15), xrange(19,21), xrange(38,42), xrange(43,46), xrange(47,50), xrange(51,53), xrange(55,57), xrange(65,89), xrange(90,189), [0, 6, 8, 16, 24, 33, 61])] + ['/store/user/shogan/JetHT/TrackMoverV27mv1_c2_2017/200529_075103/0000/movedtree_%i.root' % i for i in chain(xrange(1,3), xrange(9,11), xrange(17,19), xrange(21,24), xrange(25,33), xrange(34,38), xrange(53,55), xrange(57,61), xrange(62,65), [5, 7, 15, 42, 46, 50, 89])]), 
'JetHT2017D': (88, ['/store/user/shogan/JetHT/TrackMoverV27mv1_c2_2017/200529_075106/0000/movedtree_24.root'] + ['/store/user/shogan/JetHT/TrackMoverV27mv1_c2_2017/200518_095440/0000/movedtree_%i.root' % i for i in chain(xrange(24), xrange(25,88))]),
'JetHT2017E': (206, ['/store/user/shogan/JetHT/TrackMoverV27mv1_c2_2017/200518_095441/0000/movedtree_%i.root' % i for i in chain(xrange(179), xrange(180,206))] + ['/store/user/shogan/JetHT/TrackMoverV27mv1_c2_2017/200529_075108/0000/movedtree_179.root']),
'JetHT2017F': _fromnum0("/store/user/shogan/JetHT/TrackMoverV27mv1_c2_2017/200518_095442", 254, fnbase="movedtree"),
'JetHT2018A': _fromnum0("/store/user/shogan/JetHT/TrackMoverV27mv1_c2_2018/200518_094900", 571, fnbase="movedtree"),
'JetHT2018B': _fromnum0("/store/user/shogan/JetHT/TrackMoverV27mv1_c2_2018/200518_094901", 290, fnbase="movedtree"),
'JetHT2018C': _fromnum0("/store/user/shogan/JetHT/TrackMoverV27mv1_c2_2018/200518_094902", 214, fnbase="movedtree"),
'JetHT2018D': _fromnum0("/store/user/shogan/JetHT/TrackMoverV27mv1_c2_2018/200518_094903", 1032, fnbase="movedtree"),
})



_add_ds("multijet_32_exstats_c3", {
'qcdht0700_2017': (45, ['/store/user/shogan/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/TrackMoverV27mv1_c3_2017/200529_075138/0000/movedtree_%i.root' % i for i in chain(xrange(9,12), xrange(15,17), [3, 19, 26, 28, 32])] + ['/store/user/shogan/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/TrackMoverV27mv1_c3_2017/200518_095506/0000/movedtree_%i.root' % i for i in chain(xrange(3), xrange(4,9), xrange(12,15), xrange(17,19), xrange(20,26), xrange(29,32), xrange(33,45), [27])]),
'qcdht1000_2017': (85, ['/store/user/shogan/QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8/TrackMoverV27mv1_c3_2017/200518_095507/0000/movedtree_%i.root' % i for i in chain(xrange(50), xrange(51,60), xrange(61,85))] + ['/store/user/shogan/QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8/TrackMoverV27mv1_c3_2017/200601_080929/0000/movedtree_%i.root' % i for i in [50, 60]]),
'qcdht1500_2017': (250, ['/store/user/shogan/QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8/TrackMoverV27mv1_c3_2017/200518_095508/0000/movedtree_%i.root' % i for i in chain(xrange(24), xrange(25,35), xrange(36,38), xrange(48,250), [41])] + ['/store/user/shogan/QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8/TrackMoverV27mv1_c3_2017/200529_075147/0000/movedtree_%i.root' % i for i in chain(xrange(38,41), xrange(42,48), [24, 35])]), 
'qcdht2000_2017': _fromnum0("/store/user/shogan/QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/TrackMoverV27mv1_c3_2017/200518_095509", 74, fnbase="movedtree"),
'ttbarht0600_2017': (20, ['/store/user/shogan/TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mv1_c3_2017/200518_095510/0000/movedtree_%i.root' % i for i in chain(xrange(6), xrange(7,9), xrange(10,18), [19])] + ['/store/user/shogan/TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mv1_c3_2017/200529_075138/0000/movedtree_%i.root' % i for i in [6, 9, 18]]),
'ttbarht0800_2017': (8, ['/store/user/shogan/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mv1_c3_2017/200518_095511/0000/movedtree_%i.root' % i for i in chain(xrange(4), [5, 7])] + ['/store/user/shogan/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mv1_c3_2017/200529_075140/0000/movedtree_%i.root' % i for i in [4, 6]]),
'ttbarht1200_2017': _fromnum0("/store/user/shogan/TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mv1_c3_2017/200518_095512", 2, fnbase="movedtree"),
'ttbarht2500_2017': (1, ['/store/user/shogan/TTJets_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mv1_c3_2017/200518_095513/0000/movedtree_0.root']),
'qcdht0700_2018': _fromnum0("/store/user/shogan/QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mv1_c3_2018/200518_094939", 68, fnbase="movedtree"),
'qcdht1000_2018': _fromnum0("/store/user/shogan/QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mv1_c3_2018/200518_094940", 102, fnbase="movedtree"),
'qcdht1500_2018': (302, ['/store/user/shogan/QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mv1_c3_2018/200518_094941/0000/movedtree_%i.root' % i for i in chain(xrange(21), xrange(22,41), xrange(42,133), xrange(134,190), xrange(191,212), xrange(213,289), xrange(290,302))] + ['/store/user/shogan/QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mv1_c3_2018/200529_075145/0000/movedtree_%i.root' % i for i in [21, 41, 133, 190, 212, 289]]), 
'qcdht2000_2018': (83, ['/store/user/shogan/QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mv1_c3_2018/200518_094942/0000/movedtree_%i.root' % i for i in chain(xrange(37), xrange(38,55), xrange(56,59), xrange(60,65), xrange(66,83))] + ['/store/user/shogan/QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mv1_c3_2018/200529_075136/0000/movedtree_%i.root' % i for i in [37, 55, 59, 65]]),
'ttbarht0600_2018': _fromnum0("/store/user/shogan/TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mv1_c3_2018/200518_094943", 25, fnbase="movedtree"),
'ttbarht0800_2018': _fromnum0("/store/user/shogan/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mv1_c3_2018/200518_094944", 11, fnbase="movedtree"),
'ttbarht1200_2018': _fromnum0("/store/user/shogan/TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mv1_c3_2018/200518_094945", 2, fnbase="movedtree"),
'ttbarht2500_2018': (1, ['/store/user/shogan/TTJets_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mv1_c3_2018/200518_094946/0000/movedtree_0.root']),
'JetHT2017B': (123, ['/store/user/shogan/JetHT/TrackMoverV27mv1_c3_2017/200529_075141/0000/movedtree_%i.root' % i for i in [29, 119]] + ['/store/user/shogan/JetHT/TrackMoverV27mv1_c3_2017/200518_095514/0000/movedtree_%i.root' % i for i in chain(xrange(29), xrange(30,119), xrange(121,123))] + ['/store/user/shogan/JetHT/TrackMoverV27mv1_c3_2017/200601_080930/0000/movedtree_120.root']),
'JetHT2017C': (189, ['/store/user/shogan/JetHT/TrackMoverV27mv1_c3_2017/200529_075143/0000/movedtree_%i.root' % i for i in chain(xrange(30,32), [10, 26, 35, 126, 154])] + ['/store/user/shogan/JetHT/TrackMoverV27mv1_c3_2017/200518_095515/0000/movedtree_%i.root' % i for i in chain(xrange(10), xrange(11,26), xrange(27,30), xrange(32,35), xrange(36,126), xrange(127,154), xrange(155,189))]),
'JetHT2017D': (88, ['/store/user/shogan/JetHT/TrackMoverV27mv1_c3_2017/200529_075144/0000/movedtree_%i.root' % i for i in chain(xrange(26,31), xrange(44,47), [32, 35, 40, 51])] + ['/store/user/shogan/JetHT/TrackMoverV27mv1_c3_2017/200518_095516/0000/movedtree_%i.root' % i for i in chain(xrange(26), xrange(33,35), xrange(36,40), xrange(41,44), xrange(47,51), xrange(52,88), [31])]),
'JetHT2017E': _fromnum0("/store/user/shogan/JetHT/TrackMoverV27mv1_c3_2017/200518_095517", 206, fnbase="movedtree"),
'JetHT2017F': _fromnum0("/store/user/shogan/JetHT/TrackMoverV27mv1_c3_2017/200518_095518", 254, fnbase="movedtree"),
'JetHT2018A': (571, ['/store/user/shogan/JetHT/TrackMoverV27mv1_c3_2018/200518_094947/0000/movedtree_%i.root' % i for i in chain(xrange(223), xrange(224,283), xrange(284,365), xrange(366,461), xrange(462,493), xrange(494,547), xrange(548,569), [570])] + ['/store/user/shogan/JetHT/TrackMoverV27mv1_c3_2018/200526_113423/0000/movedtree_%i.root' % i for i in [283, 461, 493, 547]] + ['/store/user/shogan/JetHT/TrackMoverV27mv1_c3_2018/200601_080932/0000/movedtree_%i.root' % i for i in [223, 365, 569]]),
'JetHT2018B': (290, ['/store/user/shogan/JetHT/TrackMoverV27mv1_c3_2018/200529_075149/0000/movedtree_%i.root' % i for i in [191, 238]] + ['/store/user/shogan/JetHT/TrackMoverV27mv1_c3_2018/200526_113421/0000/movedtree_%i.root' % i for i in [70, 135, 155, 204, 214, 218, 264, 274]] + ['/store/user/shogan/JetHT/TrackMoverV27mv1_c3_2018/200518_094948/0000/movedtree_%i.root' % i for i in chain(xrange(70), xrange(71,135), xrange(136,155), xrange(156,191), xrange(192,204), xrange(205,214), xrange(215,218), xrange(219,238), xrange(239,264), xrange(265,274), xrange(275,290))]),
'JetHT2018C': _fromnum0("/store/user/shogan/JetHT/TrackMoverV27mv1_c3_2018/200518_094949", 214, fnbase="movedtree"),
'JetHT2018D': (1032, ['/store/user/shogan/JetHT/TrackMoverV27mv1_c3_2018/200526_113424/0000/movedtree_697.root'] + ['/store/user/shogan/JetHT/TrackMoverV27mv1_c3_2018/200518_094950' + '/%04i/movedtree_%i.root' % (i/1000,i) for i in chain(xrange(697), xrange(698,1017), xrange(1018,1032))] + ['/store/user/shogan/JetHT/TrackMoverV27mv1_c3_2018/200527_103505/0001/movedtree_1017.root']),
})



_add_ds("multijet_32_exstats_c4", {
'qcdht0700_2017': (45, ['/store/user/shogan/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/TrackMoverV27mv1_c4_2017/200601_081005/0000/movedtree_%i.root' % i for i in xrange(8,10)] + ['/store/user/shogan/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/TrackMoverV27mv1_c4_2017/200518_095554/0000/movedtree_%i.root' % i for i in chain(xrange(8), xrange(10,45))]),
'qcdht1000_2017': (85, ['/store/user/shogan/QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8/TrackMoverV27mv1_c4_2017/200518_095555/0000/movedtree_%i.root' % i for i in chain(xrange(50), xrange(51,60), xrange(61,85))] + ['/store/user/shogan/QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8/TrackMoverV27mv1_c4_2017/200529_075226/0000/movedtree_%i.root' % i for i in [50, 60]]),
'qcdht1500_2017': _fromnum0("/store/user/shogan/QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8/TrackMoverV27mv1_c4_2017/200518_095556", 250, fnbase="movedtree"),
'qcdht2000_2017': _fromnum0("/store/user/shogan/QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/TrackMoverV27mv1_c4_2017/200518_095557", 74, fnbase="movedtree"),
'ttbarht0600_2017': _fromnum0("/store/user/shogan/TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mv1_c4_2017/200518_095558", 20, fnbase="movedtree"),
'ttbarht0800_2017': _fromnum0("/store/user/shogan/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mv1_c4_2017/200518_095559", 8, fnbase="movedtree"),
'ttbarht1200_2017': _fromnum0("/store/user/shogan/TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mv1_c4_2017/200518_095600", 2, fnbase="movedtree"),
'ttbarht2500_2017': (1, ['/store/user/shogan/TTJets_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mv1_c4_2017/200518_095601/0000/movedtree_0.root']),
'qcdht0700_2018': _fromnum0("/store/user/shogan/QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mv1_c4_2018/200518_095019", 68, fnbase="movedtree"),
'qcdht1000_2018': _fromnum0("/store/user/shogan/QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mv1_c4_2018/200518_095020", 102, fnbase="movedtree"),
'qcdht1500_2018': _fromnum0("/store/user/shogan/QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mv1_c4_2018/200518_095021", 302, fnbase="movedtree"),
'qcdht2000_2018': _fromnum0("/store/user/shogan/QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mv1_c4_2018/200518_095022", 83, fnbase="movedtree"),
'ttbarht0600_2018': _fromnum0("/store/user/shogan/TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mv1_c4_2018/200518_095023", 25, fnbase="movedtree"),
'ttbarht0800_2018': _fromnum0("/store/user/shogan/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mv1_c4_2018/200518_095024", 11, fnbase="movedtree"),
'ttbarht1200_2018': _fromnum0("/store/user/shogan/TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mv1_c4_2018/200518_095025", 2, fnbase="movedtree"),
'ttbarht2500_2018': (1, ['/store/user/shogan/TTJets_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mv1_c4_2018/200518_095026/0000/movedtree_0.root']),
'JetHT2017B': (123, ['/store/user/shogan/JetHT/TrackMoverV27mv1_c4_2017/200601_081006/0000/movedtree_120.root'] + ['/store/user/shogan/JetHT/TrackMoverV27mv1_c4_2017/200529_075233/0000/movedtree_%i.root' % i for i in [29, 121]] + ['/store/user/shogan/JetHT/TrackMoverV27mv1_c4_2017/200518_095602/0000/movedtree_%i.root' % i for i in chain(xrange(29), xrange(30,120), [122])]),
'JetHT2017C': (189, ['/store/user/shogan/JetHT/TrackMoverV27mv1_c4_2017/200529_075242/0000/movedtree_%i.root' % i for i in [10, 27]] + ['/store/user/shogan/JetHT/TrackMoverV27mv1_c4_2017/200518_095603/0000/movedtree_%i.root' % i for i in chain(xrange(10), xrange(11,27), xrange(28,189))]),
'JetHT2017D': (88, ['/store/user/shogan/JetHT/TrackMoverV27mv1_c4_2017/200518_095604/0000/movedtree_%i.root' % i for i in chain(xrange(34), xrange(35,88))] + ['/store/user/shogan/JetHT/TrackMoverV27mv1_c4_2017/200529_075248/0000/movedtree_34.root']),
'JetHT2017E': _fromnum0("/store/user/shogan/JetHT/TrackMoverV27mv1_c4_2017/200518_095605", 206, fnbase="movedtree"),
'JetHT2017F': (254, ['/store/user/shogan/JetHT/TrackMoverV27mv1_c4_2017/200601_081007/0000/movedtree_168.root'] + ['/store/user/shogan/JetHT/TrackMoverV27mv1_c4_2017/200518_095606/0000/movedtree_%i.root' % i for i in chain(xrange(168), xrange(169,254))]),
'JetHT2018A': _fromnum0("/store/user/shogan/JetHT/TrackMoverV27mv1_c4_2018/200518_095027", 571, fnbase="movedtree"),
'JetHT2018B': _fromnum0("/store/user/shogan/JetHT/TrackMoverV27mv1_c4_2018/200518_095028", 290, fnbase="movedtree"),
'JetHT2018C': _fromnum0("/store/user/shogan/JetHT/TrackMoverV27mv1_c4_2018/200518_095029", 214, fnbase="movedtree"),
'JetHT2018D': (1032, ['/store/user/shogan/JetHT/TrackMoverV27mv1_c4_2018/200527_103529/0000/movedtree_%i.root' % i for i in chain(xrange(838,840), [764, 805, 813, 815, 825, 832, 834, 858, 920, 922])] + ['/store/user/shogan/JetHT/TrackMoverV27mv1_c4_2018/200526_113536/0000/movedtree_416.root'] + ['/store/user/shogan/JetHT/TrackMoverV27mv1_c4_2018/200518_095030' + '/%04i/movedtree_%i.root' % (i/1000,i) for i in chain(xrange(416), xrange(417,764), xrange(765,805), xrange(806,813), xrange(816,825), xrange(826,832), xrange(835,838), xrange(840,858), xrange(859,920), xrange(923,1032), [814, 833, 921])]),
})


_add_ds("multijet_32_exstats_j0", {
'qcdht0700_2017': (45, ['/store/user/joeyr/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/TrackMoverV27mext1_2017/200516_111036/0000/movedtree_28.root'] + ['/store/user/joeyr/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/TrackMoverV27mext1_2017/200515_150737/0000/movedtree_%i.root' % i for i in chain(xrange(28), xrange(29,45))]),
'qcdht1000_2017': _fromnum0("/store/user/joeyr/QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8/TrackMoverV27mext1_2017/200515_144237", 85, fnbase="movedtree"),
'qcdht1500_2017': _fromnum0("/store/user/joeyr/QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8/TrackMoverV27mext1_2017/200515_144238", 250, fnbase="movedtree"),
'qcdht2000_2017': _fromnum0("/store/user/joeyr/QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/TrackMoverV27mext1_2017/200515_144239", 74, fnbase="movedtree"),
'ttbarht0600_2017': _fromnum0("/store/user/joeyr/TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mext1_2017/200515_144240", 20, fnbase="movedtree"),
'ttbarht0800_2017': _fromnum0("/store/user/joeyr/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mext1_2017/200515_144241", 8, fnbase="movedtree"),
'ttbarht1200_2017': _fromnum0("/store/user/joeyr/TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mext1_2017/200515_144242", 2, fnbase="movedtree"),
'ttbarht2500_2017': (1, ['/store/user/joeyr/TTJets_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mext1_2017/200515_144243/0000/movedtree_0.root']),
'qcdht1000_2018': _fromnum0("/store/user/joeyr/QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mext1_2018/200515_155025", 102, fnbase="movedtree"),
'qcdht1500_2018': _fromnum0("/store/user/joeyr/QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mext1_2018/200515_154655", 302, fnbase="movedtree"),
'qcdht2000_2018': _fromnum0("/store/user/joeyr/QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mext1_2018/200515_154656", 83, fnbase="movedtree"),
'ttbarht0600_2018': _fromnum0("/store/user/joeyr/TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mext1_2018/200515_154657", 25, fnbase="movedtree"),
'ttbarht0800_2018': _fromnum0("/store/user/joeyr/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mext1_2018/200515_154658", 11, fnbase="movedtree"),
'ttbarht1200_2018': _fromnum0("/store/user/joeyr/TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mext1_2018/200515_154659", 2, fnbase="movedtree"),
'ttbarht2500_2018': (1, ['/store/user/joeyr/TTJets_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mext1_2018/200515_154700/0000/movedtree_0.root']),
'JetHT2017B': _fromnum0("/store/user/joeyr/JetHT/TrackMoverV27mext1_2017/200515_144244", 123, fnbase="movedtree"),
'JetHT2017C': _fromnum0("/store/user/joeyr/JetHT/TrackMoverV27mext1_2017/200515_144245", 189, fnbase="movedtree"),
'JetHT2017D': (88, ['/store/user/joeyr/JetHT/TrackMoverV27mext1_2017/200515_150624/0000/movedtree_%i.root' % i for i in chain(xrange(53), xrange(54,88))] + ['/store/user/joeyr/JetHT/TrackMoverV27mext1_2017/200516_111037/0000/movedtree_53.root']),
'JetHT2017E': (206, ['/store/user/joeyr/JetHT/TrackMoverV27mext1_2017/200516_111038/0000/movedtree_9.root'] + ['/store/user/joeyr/JetHT/TrackMoverV27mext1_2017/200515_144247/0000/movedtree_%i.root' % i for i in chain(xrange(9), xrange(10,206))]),
'JetHT2017F': _fromnum0("/store/user/joeyr/JetHT/TrackMoverV27mext1_2017/200516_110804", 254, fnbase="movedtree"),
'JetHT2018A': _fromnum0("/store/user/joeyr/JetHT/TrackMoverV27mext1_2018/200515_154701", 571, fnbase="movedtree"),
'JetHT2018B': (290, ['/store/user/joeyr/JetHT/TrackMoverV27mext1_2018/200515_154702/0000/movedtree_%i.root' % i for i in chain(xrange(139), xrange(140,159), xrange(160,202), xrange(206,210), xrange(211,220), xrange(225,227), xrange(234,248), xrange(249,256), xrange(261,265), xrange(267,271), xrange(275,288), [221, 223, 229, 257, 259, 273, 289])] + ['/store/user/joeyr/JetHT/TrackMoverV27mext1_2018/200516_111034/0000/movedtree_%i.root' % i for i in chain(xrange(202,206), xrange(227,229), xrange(230,234), xrange(265,267), xrange(271,273), [139, 159, 210, 220, 222, 224, 248, 256, 258, 260, 274, 288])]),
'JetHT2018C': (214, ['/store/user/joeyr/JetHT/TrackMoverV27mext1_2018/200515_154703/0000/movedtree_%i.root' % i for i in chain(xrange(128), xrange(129,147), xrange(148,168), xrange(169,214))] + ['/store/user/joeyr/JetHT/TrackMoverV27mext1_2018/200516_111033/0000/movedtree_%i.root' % i for i in [128, 147, 168]]),
'JetHT2018D': (1032, ['/store/user/joeyr/JetHT/TrackMoverV27mext1_2018/200517_033638/0000/movedtree_%i.root' % i for i in [151, 184]] + ['/store/user/joeyr/JetHT/TrackMoverV27mext1_2018/200516_110947' + '/%04i/movedtree_%i.root' % (i/1000,i) for i in chain(xrange(151), xrange(152,184), xrange(185,219), xrange(220,236), xrange(237,1032))] + ['/store/user/joeyr/JetHT/TrackMoverV27mext1_2018/200517_033120/0000/movedtree_%i.root' % i for i in [219, 236]]),
})


_add_ds("multijet_32_exstats_j1", {
'qcdht0700_2017': (45, ['/store/user/joeyr/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/TrackMoverV27mext2_2017/200516_112408/0000/movedtree_%i.root' % i for i in xrange(1,45)] + ['/store/user/joeyr/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/TrackMoverV27mext2_2017/200517_033115/0000/movedtree_0.root']),
'qcdht1000_2017': _fromnum0("/store/user/joeyr/QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8/TrackMoverV27mext2_2017/200516_112409", 85, fnbase="movedtree"),
'qcdht1500_2017': _fromnum0("/store/user/joeyr/QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8/TrackMoverV27mext2_2017/200516_112410", 250, fnbase="movedtree"),
'qcdht2000_2017': (74, ['/store/user/joeyr/QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/TrackMoverV27mext2_2017/200517_034216/0000/movedtree_%i.root' % i for i in chain(xrange(18,21), [1, 30])] + ['/store/user/joeyr/QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/TrackMoverV27mext2_2017/200517_042931/0000/movedtree_69.root'] + ['/store/user/joeyr/QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/TrackMoverV27mext2_2017/200517_033636/0000/movedtree_%i.root' % i for i in [5, 7]] + ['/store/user/joeyr/QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/TrackMoverV27mext2_2017/200517_034731/0000/movedtree_%i.root' % i for i in chain(xrange(27,29), [32])] + ['/store/user/joeyr/QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/TrackMoverV27mext2_2017/200517_033119/0000/movedtree_%i.root' % i for i in [12, 14]] + ['/store/user/joeyr/QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/TrackMoverV27mext2_2017/200517_020817/0000/movedtree_10.root'] + ['/store/user/joeyr/QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/TrackMoverV27mext2_2017/200516_112411/0000/movedtree_%i.root' % i for i in chain(xrange(2,5), xrange(8,10), xrange(15,18), xrange(21,27), xrange(33,69), xrange(70,74), [0, 6, 11, 13, 29, 31])]),
'ttbarht0600_2017': _fromnum0("/store/user/joeyr/TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mext2_2017/200516_112412", 20, fnbase="movedtree"),
'ttbarht0800_2017': _fromnum0("/store/user/joeyr/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mext2_2017/200516_112413", 8, fnbase="movedtree"),
'ttbarht1200_2017': _fromnum0("/store/user/joeyr/TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mext2_2017/200516_112414", 2, fnbase="movedtree"),
'ttbarht2500_2017': (1, ['/store/user/joeyr/TTJets_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mext2_2017/200516_112415/0000/movedtree_0.root']),
'qcdht0700_2018': _fromnum0("/store/user/joeyr/QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mext2_2018/200516_112422", 68, fnbase="movedtree"),
'qcdht1000_2018': _fromnum0("/store/user/joeyr/QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mext2_2018/200516_112423", 102, fnbase="movedtree"),
'qcdht1500_2018': _fromnum0("/store/user/joeyr/QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mext2_2018/200516_112424", 302, fnbase="movedtree"),
'qcdht2000_2018': _fromnum0("/store/user/joeyr/QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mext2_2018/200516_112425", 83, fnbase="movedtree"),
'ttbarht0600_2018': _fromnum0("/store/user/joeyr/TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mext2_2018/200516_112426", 25, fnbase="movedtree"),
'ttbarht0800_2018': (11, ['/store/user/joeyr/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mext2_2018/200517_034211/0000/movedtree_8.root'] + ['/store/user/joeyr/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mext2_2018/200517_033632/0000/movedtree_0.root'] + ['/store/user/joeyr/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mext2_2018/200516_112427/0000/movedtree_%i.root' % i for i in chain(xrange(1,8), xrange(9,11))]),
'ttbarht1200_2018': _fromnum0("/store/user/joeyr/TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mext2_2018/200516_112428", 2, fnbase="movedtree"),
'ttbarht2500_2018': (1, ['/store/user/joeyr/TTJets_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mext2_2018/200516_112429/0000/movedtree_0.root']),
'JetHT2017B': _fromnum0("/store/user/joeyr/JetHT/TrackMoverV27mext2_2017/200516_112416", 123, fnbase="movedtree"),
'JetHT2017C': (189, ['/store/user/joeyr/JetHT/TrackMoverV27mext2_2017/200516_112417/0000/movedtree_%i.root' % i for i in chain(xrange(152), xrange(153,189))] + ['/store/user/joeyr/JetHT/TrackMoverV27mext2_2017/200517_033659/0000/movedtree_152.root']),
'JetHT2017D': _fromnum0("/store/user/joeyr/JetHT/TrackMoverV27mext2_2017/200516_112418", 88, fnbase="movedtree"),
'JetHT2017E': (206, ['/store/user/joeyr/JetHT/TrackMoverV27mext2_2017/200528_114740/0000/movedtree_10.root'] + ['/store/user/joeyr/JetHT/TrackMoverV27mext2_2017/200516_112419/0000/movedtree_%i.root' % i for i in chain(xrange(10), xrange(11,206))]),
'JetHT2017F': (254, ['/store/user/joeyr/JetHT/TrackMoverV27mext2_2017/200528_114739/0000/movedtree_13.root'] + ['/store/user/joeyr/JetHT/TrackMoverV27mext2_2017/200528_175054/0000/movedtree_87.root'] + ['/store/user/joeyr/JetHT/TrackMoverV27mext2_2017/200516_112420/0000/movedtree_%i.root' % i for i in chain(xrange(13), xrange(14,87), xrange(88,254))]),
'JetHT2018A': (571, ['/store/user/joeyr/JetHT/TrackMoverV27mext2_2018/200517_021843/0000/movedtree_32.root'] + ['/store/user/joeyr/JetHT/TrackMoverV27mext2_2018/200517_042907/0000/movedtree_222.root'] + ['/store/user/joeyr/JetHT/TrackMoverV27mext2_2018/200517_033634/0000/movedtree_%i.root' % i for i in chain(xrange(105,108), [101, 110])] + ['/store/user/joeyr/JetHT/TrackMoverV27mext2_2018/200517_074242/0000/movedtree_457.root'] + ['/store/user/joeyr/JetHT/TrackMoverV27mext2_2018/200517_034214/0000/movedtree_%i.root' % i for i in chain(xrange(116,118), [97, 108])] + ['/store/user/joeyr/JetHT/TrackMoverV27mext2_2018/200601_074945/0000/movedtree_563.root'] + ['/store/user/joeyr/JetHT/TrackMoverV27mext2_2018/200517_042352/0000/movedtree_227.root'] + ['/store/user/joeyr/JetHT/TrackMoverV27mext2_2018/200516_112430/0000/movedtree_%i.root' % i for i in chain(xrange(24), xrange(25,32), xrange(33,97), xrange(120,143), xrange(144,166), xrange(167,214), xrange(216,222), xrange(223,227), xrange(228,278), xrange(279,321), xrange(322,340), xrange(341,349), xrange(350,389), xrange(390,421), xrange(422,431), xrange(432,454), xrange(455,457), xrange(458,464), xrange(465,523), xrange(524,540), xrange(541,563), xrange(564,571), [99, 102, 109, 111, 113, 115, 118])] + ['/store/user/joeyr/JetHT/TrackMoverV27mext2_2018/200517_013708/0000/movedtree_24.root'] + ['/store/user/joeyr/JetHT/TrackMoverV27mext2_2018/200517_034729/0000/movedtree_%i.root' % i for i in [112, 114]] + ['/store/user/joeyr/JetHT/TrackMoverV27mext2_2018/200529_140016/0000/movedtree_119.root'] + ['/store/user/joeyr/JetHT/TrackMoverV27mext2_2018/200517_072701/0000/movedtree_431.root'] + ['/store/user/joeyr/JetHT/TrackMoverV27mext2_2018/200517_070106/0000/movedtree_421.root'] + ['/store/user/joeyr/JetHT/TrackMoverV27mext2_2018/200517_041837/0000/movedtree_%i.root' % i for i in [143, 166]] + ['/store/user/joeyr/JetHT/TrackMoverV27mext2_2018/200517_051717/0000/movedtree_%i.root' % i for i in [340, 349]] + ['/store/user/joeyr/JetHT/TrackMoverV27mext2_2018/200517_043458/0000/movedtree_214.root'] + ['/store/user/joeyr/JetHT/TrackMoverV27mext2_2018/200517_073726/0000/movedtree_464.root'] + ['/store/user/joeyr/JetHT/TrackMoverV27mext2_2018/200517_050622/0000/movedtree_215.root'] + ['/store/user/joeyr/JetHT/TrackMoverV27mext2_2018/200517_050104/0000/movedtree_278.root'] + ['/store/user/joeyr/JetHT/TrackMoverV27mext2_2018/200528_231258/0000/movedtree_%i.root' % i for i in [100, 389, 454, 523, 540]] + ['/store/user/joeyr/JetHT/TrackMoverV27mext2_2018/200517_033117/0000/movedtree_%i.root' % i for i in chain(xrange(103,105), [98])] + ['/store/user/joeyr/JetHT/TrackMoverV27mext2_2018/200517_051141/0000/movedtree_321.root']),
'JetHT2018B': (290, ['/store/user/joeyr/JetHT/TrackMoverV27mext2_2018/200517_050618/0000/movedtree_99.root'] + ['/store/user/joeyr/JetHT/TrackMoverV27mext2_2018/200517_080331/0000/movedtree_281.root'] + ['/store/user/joeyr/JetHT/TrackMoverV27mext2_2018/200517_045546/0000/movedtree_86.root'] + ['/store/user/joeyr/JetHT/TrackMoverV27mext2_2018/200517_042904/0000/movedtree_24.root'] + ['/store/user/joeyr/JetHT/TrackMoverV27mext2_2018/200517_051136/0000/movedtree_62.root'] + ['/store/user/joeyr/JetHT/TrackMoverV27mext2_2018/200516_112431/0000/movedtree_%i.root' % i for i in chain(xrange(4), xrange(5,24), xrange(25,29), xrange(30,53), xrange(54,62), xrange(63,86), xrange(88,91), xrange(92,99), xrange(100,281), xrange(282,290))] + ['/store/user/joeyr/JetHT/TrackMoverV27mext2_2018/200517_042349/0000/movedtree_4.root'] + ['/store/user/joeyr/JetHT/TrackMoverV27mext2_2018/200517_050100/0000/movedtree_87.root'] + ['/store/user/joeyr/JetHT/TrackMoverV27mext2_2018/200517_044522/0000/movedtree_53.root'] + ['/store/user/joeyr/JetHT/TrackMoverV27mext2_2018/200517_043455/0000/movedtree_29.root'] + ['/store/user/joeyr/JetHT/TrackMoverV27mext2_2018/200517_051712/0000/movedtree_91.root']),
'JetHT2018C': _fromnum0("/store/user/joeyr/JetHT/TrackMoverV27mext2_2018/200516_112432", 214, fnbase="movedtree"),
'JetHT2018D': _fromnum0("/store/user/joeyr/JetHT/TrackMoverV27mext2_2018/200516_112433", 1032, fnbase="movedtree"),
})


_add_ds("multijet_32_exstats_j2", {
'qcdht0700_2017': _fromnum0("/store/user/joeyr/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/TrackMoverV27mext3_2017/200516_112442", 45, fnbase="movedtree"),
'qcdht1000_2017': _fromnum0("/store/user/joeyr/QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8/TrackMoverV27mext3_2017/200516_112443", 85, fnbase="movedtree"),
'qcdht1500_2017': _fromnum0("/store/user/joeyr/QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8/TrackMoverV27mext3_2017/200516_112444", 250, fnbase="movedtree"),
'qcdht2000_2017': _fromnum0("/store/user/joeyr/QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/TrackMoverV27mext3_2017/200516_112445", 74, fnbase="movedtree"),
'ttbarht0600_2017': _fromnum0("/store/user/joeyr/TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mext3_2017/200516_112446", 20, fnbase="movedtree"),
'ttbarht0800_2017': _fromnum0("/store/user/joeyr/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mext3_2017/200516_112447", 8, fnbase="movedtree"),
'ttbarht1200_2017': _fromnum0("/store/user/joeyr/TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mext3_2017/200516_112448", 2, fnbase="movedtree"),
'ttbarht2500_2017': (1, ['/store/user/joeyr/TTJets_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mext3_2017/200516_112449/0000/movedtree_0.root']),
'qcdht0700_2018': _fromnum0("/store/user/joeyr/QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mext3_2018/200516_112519", 68, fnbase="movedtree"),
'qcdht1000_2018': _fromnum0("/store/user/joeyr/QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mext3_2018/200516_112520", 102, fnbase="movedtree"),
'qcdht1500_2018': _fromnum0("/store/user/joeyr/QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mext3_2018/200516_112521", 302, fnbase="movedtree"),
'qcdht2000_2018': _fromnum0("/store/user/joeyr/QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mext3_2018/200516_112522", 83, fnbase="movedtree"),
'ttbarht0600_2018': _fromnum0("/store/user/joeyr/TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mext3_2018/200516_112523", 25, fnbase="movedtree"),
'ttbarht0800_2018': _fromnum0("/store/user/joeyr/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mext3_2018/200516_112524", 11, fnbase="movedtree"),
'ttbarht1200_2018': _fromnum0("/store/user/joeyr/TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mext3_2018/200516_112525", 2, fnbase="movedtree"),
'ttbarht2500_2018': (1, ['/store/user/joeyr/TTJets_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mext3_2018/200516_112526/0000/movedtree_0.root']),
'JetHT2017B': _fromnum0("/store/user/joeyr/JetHT/TrackMoverV27mext3_2017/200516_112450", 123, fnbase="movedtree"),
'JetHT2017C': _fromnum0("/store/user/joeyr/JetHT/TrackMoverV27mext3_2017/200516_112451", 189, fnbase="movedtree"),
'JetHT2017D': _fromnum0("/store/user/joeyr/JetHT/TrackMoverV27mext3_2017/200516_112452", 88, fnbase="movedtree"),
'JetHT2017E': _fromnum0("/store/user/joeyr/JetHT/TrackMoverV27mext3_2017/200516_112453", 206, fnbase="movedtree"),
'JetHT2017F': (254, ['/store/user/joeyr/JetHT/TrackMoverV27mext3_2017/200516_112454/0000/movedtree_%i.root' % i for i in chain(xrange(147), xrange(148,254))] + ['/store/user/joeyr/JetHT/TrackMoverV27mext3_2017/200528_114738/0000/movedtree_147.root']),
'JetHT2018A': _fromnum0("/store/user/joeyr/JetHT/TrackMoverV27mext3_2018/200516_112527", 571, fnbase="movedtree"),
'JetHT2018B': _fromnum0("/store/user/joeyr/JetHT/TrackMoverV27mext3_2018/200516_112528", 290, fnbase="movedtree"),
'JetHT2018C': _fromnum0("/store/user/joeyr/JetHT/TrackMoverV27mext3_2018/200516_112529", 214, fnbase="movedtree"),
'JetHT2018D': _fromnum0("/store/user/joeyr/JetHT/TrackMoverV27mext3_2018/200516_112530", 1032, fnbase="movedtree"),
})

_add_ds("multijet_32_exstats_j3", {
'qcdht0700_2017': _fromnum0("/store/user/joeyr/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/TrackMoverV27mext4_2017/200516_112546", 45, fnbase="movedtree"),
'qcdht1000_2017': (85, ['/store/user/joeyr/QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8/TrackMoverV27mext4_2017/200516_112547/0000/movedtree_%i.root' % i for i in chain(xrange(18), xrange(19,28), xrange(29,32), xrange(33,85))] + ['/store/user/joeyr/QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8/TrackMoverV27mext4_2017/200528_114718/0000/movedtree_%i.root' % i for i in [18, 28, 32]]),
'qcdht1500_2017': _fromnum0("/store/user/joeyr/QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8/TrackMoverV27mext4_2017/200516_112548", 250, fnbase="movedtree"),
'qcdht2000_2017': _fromnum0("/store/user/joeyr/QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/TrackMoverV27mext4_2017/200516_112549", 74, fnbase="movedtree"),
'ttbarht0600_2017': _fromnum0("/store/user/joeyr/TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mext4_2017/200516_112550", 20, fnbase="movedtree"),
'ttbarht0800_2017': _fromnum0("/store/user/joeyr/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mext4_2017/200516_112551", 8, fnbase="movedtree"),
'ttbarht1200_2017': (2, ['/store/user/joeyr/TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mext4_2017/200516_112552/0000/movedtree_1.root'] + ['/store/user/joeyr/TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mext4_2017/200528_114737/0000/movedtree_0.root']),
'ttbarht2500_2017': (1, ['/store/user/joeyr/TTJets_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mext4_2017/200516_112553/0000/movedtree_0.root']),
'qcdht0700_2018': (68, ['/store/user/joeyr/QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mext4_2018/200516_112603/0000/movedtree_%i.root' % i for i in chain(xrange(25), xrange(26,29), xrange(30,41), xrange(43,68))] + ['/store/user/joeyr/QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mext4_2018/200528_114734/0000/movedtree_%i.root' % i for i in chain(xrange(41,43), [25, 29])]), 
'qcdht1000_2018': _fromnum0("/store/user/joeyr/QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mext4_2018/200516_112604", 102, fnbase="movedtree"),
'qcdht1500_2018': (302, ['/store/user/joeyr/QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mext4_2018/200516_112605/0000/movedtree_%i.root' % i for i in chain(xrange(21), xrange(22,41), xrange(42,133), xrange(134,190), xrange(191,212), xrange(213,302))] + ['/store/user/joeyr/QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mext4_2018/200528_114716/0000/movedtree_%i.root' % i for i in [21, 41, 133, 190, 212]]), 
'qcdht2000_2018': _fromnum0("/store/user/joeyr/QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mext4_2018/200516_112606", 83, fnbase="movedtree"),
'ttbarht0600_2018': _fromnum0("/store/user/joeyr/TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mext4_2018/200516_112607", 25, fnbase="movedtree"),
'ttbarht0800_2018': (11, ['/store/user/joeyr/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mext4_2018/200528_114736/0000/movedtree_10.root'] + ['/store/user/joeyr/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mext4_2018/200516_112608/0000/movedtree_%i.root' % i for i in xrange(10)]),
'ttbarht1200_2018': _fromnum0("/store/user/joeyr/TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mext4_2018/200516_112609", 2, fnbase="movedtree"),
'ttbarht2500_2018': (1, ['/store/user/joeyr/TTJets_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mext4_2018/200516_112610/0000/movedtree_0.root']),
'JetHT2017B': _fromnum0("/store/user/joeyr/JetHT/TrackMoverV27mext4_2017/200516_112554", 123, fnbase="movedtree"),
'JetHT2017C': _fromnum0("/store/user/joeyr/JetHT/TrackMoverV27mext4_2017/200516_112555", 189, fnbase="movedtree"),
'JetHT2017D': _fromnum0("/store/user/joeyr/JetHT/TrackMoverV27mext4_2017/200516_112556", 88, fnbase="movedtree"),
'JetHT2017E': _fromnum0("/store/user/joeyr/JetHT/TrackMoverV27mext4_2017/200516_112557", 206, fnbase="movedtree"),
'JetHT2017F': _fromnum0("/store/user/joeyr/JetHT/TrackMoverV27mext4_2017/200516_112558", 254, fnbase="movedtree"),
'JetHT2018A': (571, ['/store/user/joeyr/JetHT/TrackMoverV27mext4_2018/200516_112611/0000/movedtree_%i.root' % i for i in chain(xrange(22), xrange(23,90), xrange(91,115), xrange(116,150), xrange(151,191), xrange(194,199), xrange(200,205), xrange(206,213), xrange(216,223), xrange(224,232), xrange(233,237), xrange(238,283), xrange(284,365), xrange(366,571), [192, 214])] + ['/store/user/joeyr/JetHT/TrackMoverV27mext4_2018/200528_153918/0000/movedtree_%i.root' % i for i in [90, 215]] + ['/store/user/joeyr/JetHT/TrackMoverV27mext4_2018/200528_114723/0000/movedtree_%i.root' % i for i in [22, 115, 191, 193, 199, 223, 232, 237, 283]] + ['/store/user/joeyr/JetHT/TrackMoverV27mext4_2018/200529_140009/0000/movedtree_205.root'] + ['/store/user/joeyr/JetHT/TrackMoverV27mext4_2018/200528_230925/0000/movedtree_365.root'] + ['/store/user/joeyr/JetHT/TrackMoverV27mext4_2018/200528_175046/0000/movedtree_213.root'] + ['/store/user/joeyr/JetHT/TrackMoverV27mext4_2018/200529_092326/0000/movedtree_150.root']),
'JetHT2018B': _fromnum0("/store/user/joeyr/JetHT/TrackMoverV27mext4_2018/200516_112612", 290, fnbase="movedtree"),
'JetHT2018C': _fromnum0("/store/user/joeyr/JetHT/TrackMoverV27mext4_2018/200516_112613", 214, fnbase="movedtree"),
'JetHT2018D': (1032, ['/store/user/joeyr/JetHT/TrackMoverV27mext4_2018/200516_112614' + '/%04i/movedtree_%i.root' % (i/1000,i) for i in chain(xrange(380), xrange(381,1032))] + ['/store/user/joeyr/JetHT/TrackMoverV27mext4_2018/200528_114726/0000/movedtree_380.root']),
})


_add_ds("multijet_32_exstats_j4", {
'qcdht0700_2017': _fromnum0("/store/user/joeyr/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/TrackMoverV27mext5_2017/200516_112622", 45, fnbase="movedtree"),
'qcdht1000_2017': (85, ['/store/user/joeyr/QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8/TrackMoverV27mext5_2017/200516_112623/0000/movedtree_%i.root' % i for i in chain(xrange(78), xrange(79,85))] + ['/store/user/joeyr/QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8/TrackMoverV27mext5_2017/200528_114735/0000/movedtree_78.root']),
'qcdht1500_2017': _fromnum0("/store/user/joeyr/QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8/TrackMoverV27mext5_2017/200516_112624", 250, fnbase="movedtree"),
'qcdht2000_2017': _fromnum0("/store/user/joeyr/QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/TrackMoverV27mext5_2017/200516_112625", 74, fnbase="movedtree"),
'ttbarht0600_2017': _fromnum0("/store/user/joeyr/TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mext5_2017/200516_112626", 20, fnbase="movedtree"),
'ttbarht0800_2017': _fromnum0("/store/user/joeyr/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mext5_2017/200516_112627", 8, fnbase="movedtree"),
'ttbarht1200_2017': _fromnum0("/store/user/joeyr/TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mext5_2017/200516_112628", 2, fnbase="movedtree"),
'ttbarht2500_2017': (1, ['/store/user/joeyr/TTJets_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mext5_2017/200516_112629/0000/movedtree_0.root']),
'qcdht0700_2018': _fromnum0("/store/user/joeyr/QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mext5_2018/200516_112656", 68, fnbase="movedtree"),
'qcdht1000_2018': _fromnum0("/store/user/joeyr/QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mext5_2018/200516_112657", 102, fnbase="movedtree"),
'qcdht1500_2018': _fromnum0("/store/user/joeyr/QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mext5_2018/200516_112658", 302, fnbase="movedtree"),
'qcdht2000_2018': _fromnum0("/store/user/joeyr/QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mext5_2018/200516_112659", 83, fnbase="movedtree"),
'ttbarht0600_2018': _fromnum0("/store/user/joeyr/TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mext5_2018/200516_112700", 25, fnbase="movedtree"),
'ttbarht0800_2018': _fromnum0("/store/user/joeyr/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mext5_2018/200516_112701", 11, fnbase="movedtree"),
'ttbarht1200_2018': _fromnum0("/store/user/joeyr/TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mext5_2018/200516_112702", 2, fnbase="movedtree"),
'ttbarht2500_2018': (1, ['/store/user/joeyr/TTJets_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mext5_2018/200516_112703/0000/movedtree_0.root']),
'JetHT2017B': _fromnum0("/store/user/joeyr/JetHT/TrackMoverV27mext5_2017/200516_112630", 123, fnbase="movedtree"),
'JetHT2017C': _fromnum0("/store/user/joeyr/JetHT/TrackMoverV27mext5_2017/200516_112631", 189, fnbase="movedtree"),
'JetHT2017D': _fromnum0("/store/user/joeyr/JetHT/TrackMoverV27mext5_2017/200516_112632", 88, fnbase="movedtree"),
'JetHT2017E': _fromnum0("/store/user/joeyr/JetHT/TrackMoverV27mext5_2017/200516_112633", 206, fnbase="movedtree"),
'JetHT2017F': _fromnum0("/store/user/joeyr/JetHT/TrackMoverV27mext5_2017/200516_112634", 254, fnbase="movedtree"),
'JetHT2018A': _fromnum0("/store/user/joeyr/JetHT/TrackMoverV27mext5_2018/200516_112704", 571, fnbase="movedtree"),
'JetHT2018B': _fromnum0("/store/user/joeyr/JetHT/TrackMoverV27mext5_2018/200516_112705", 290, fnbase="movedtree"),
'JetHT2018C': _fromnum0("/store/user/joeyr/JetHT/TrackMoverV27mext5_2018/200516_112706", 214, fnbase="movedtree"),
'JetHT2018D': (1032, ['/store/user/joeyr/JetHT/TrackMoverV27mext5_2018/200528_114748' + '/%04i/movedtree_%i.root' % (i/1000,i) for i in chain(xrange(999,1001), [421, 451, 480, 492, 504, 510, 524, 529, 540, 566, 568, 595, 655, 660, 676, 691, 694, 734, 958, 962, 966, 968, 973, 975, 987, 995, 1011, 1014])] + ['/store/user/joeyr/JetHT/TrackMoverV27mext5_2018/200516_112707' + '/%04i/movedtree_%i.root' % (i/1000,i) for i in chain(xrange(421), xrange(422,451), xrange(452,480), xrange(481,492), xrange(493,504), xrange(505,510), xrange(511,524), xrange(525,529), xrange(530,540), xrange(541,566), xrange(569,590), xrange(591,595), xrange(596,604), xrange(605,619), xrange(620,635), xrange(636,655), xrange(656,660), xrange(661,676), xrange(677,691), xrange(692,694), xrange(695,705), xrange(706,718), xrange(719,734), xrange(735,773), xrange(774,958), xrange(959,962), xrange(963,966), xrange(969,973), xrange(976,987), xrange(988,995), xrange(996,999), xrange(1001,1011), xrange(1012,1014), xrange(1015,1032), [967, 974])] + ['/store/user/joeyr/JetHT/TrackMoverV27mext5_2018/200528_175047/0000/movedtree_%i.root' % i for i in [567, 590, 604, 619, 635, 705, 718, 773]]),
})


_add_ds("multijet_32_exstats_j5", {
'qcdht0700_2017': _fromnum0("/store/user/joeyr/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/TrackMoverV27mext6_2017/200516_112704", 45, fnbase="movedtree"),
'qcdht1000_2017': _fromnum0("/store/user/joeyr/QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8/TrackMoverV27mext6_2017/200516_112705", 85, fnbase="movedtree"),
'qcdht1500_2017': _fromnum0("/store/user/joeyr/QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8/TrackMoverV27mext6_2017/200516_112706", 250, fnbase="movedtree"),
'qcdht2000_2017': _fromnum0("/store/user/joeyr/QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/TrackMoverV27mext6_2017/200516_112707", 74, fnbase="movedtree"),
'ttbarht0600_2017': _fromnum0("/store/user/joeyr/TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mext6_2017/200516_112708", 20, fnbase="movedtree"),
'ttbarht0800_2017': _fromnum0("/store/user/joeyr/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mext6_2017/200516_112709", 8, fnbase="movedtree"),
'ttbarht1200_2017': _fromnum0("/store/user/joeyr/TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mext6_2017/200516_112710", 2, fnbase="movedtree"),
'ttbarht2500_2017': (1, ['/store/user/joeyr/TTJets_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mext6_2017/200516_112711/0000/movedtree_0.root']),
'qcdht0700_2018': _fromnum0("/store/user/joeyr/QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mext6_2018/200516_112818", 68, fnbase="movedtree"),
'qcdht1000_2018': _fromnum0("/store/user/joeyr/QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mext6_2018/200516_112819", 102, fnbase="movedtree"),
'qcdht1500_2018': _fromnum0("/store/user/joeyr/QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mext6_2018/200516_112820", 302, fnbase="movedtree"),
'qcdht2000_2018': _fromnum0("/store/user/joeyr/QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mext6_2018/200516_112821", 83, fnbase="movedtree"),
'ttbarht0600_2018': _fromnum0("/store/user/joeyr/TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mext6_2018/200516_112822", 25, fnbase="movedtree"),
'ttbarht0800_2018': _fromnum0("/store/user/joeyr/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mext6_2018/200516_112823", 11, fnbase="movedtree"),
'ttbarht1200_2018': _fromnum0("/store/user/joeyr/TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mext6_2018/200516_112824", 2, fnbase="movedtree"),
'ttbarht2500_2018': (1, ['/store/user/joeyr/TTJets_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverV27mext6_2018/200516_112825/0000/movedtree_0.root']),
'JetHT2017B': (123, ['/store/user/joeyr/JetHT/TrackMoverV27mext6_2017/200528_114717/0000/movedtree_7.root'] + ['/store/user/joeyr/JetHT/TrackMoverV27mext6_2017/200516_112712/0000/movedtree_%i.root' % i for i in chain(xrange(7), xrange(8,123))]),
'JetHT2017C': _fromnum0("/store/user/joeyr/JetHT/TrackMoverV27mext6_2017/200516_112713", 189, fnbase="movedtree"),
'JetHT2017D': (88, ['/store/user/joeyr/JetHT/TrackMoverV27mext6_2017/200516_112714/0000/movedtree_%i.root' % i for i in chain(xrange(53), xrange(54,88))] + ['/store/user/joeyr/JetHT/TrackMoverV27mext6_2017/200528_114725/0000/movedtree_53.root']),
'JetHT2017E': (206, ['/store/user/joeyr/JetHT/TrackMoverV27mext6_2017/200516_112715/0000/movedtree_%i.root' % i for i in chain(xrange(21), xrange(22,39), xrange(40,46), xrange(47,51), xrange(57,59), xrange(63,70), xrange(72,74), xrange(76,109), xrange(110,112), xrange(114,150), xrange(151,206), [54, 61])] + ['/store/user/joeyr/JetHT/TrackMoverV27mext6_2017/200528_114720/0000/movedtree_%i.root' % i for i in chain(xrange(51,54), xrange(55,57), xrange(59,61), xrange(70,72), xrange(74,76), xrange(112,114), [21, 39, 46, 62, 109, 150])]),
'JetHT2017F': (254, ['/store/user/joeyr/JetHT/TrackMoverV27mext6_2017/200516_112716/0000/movedtree_%i.root' % i for i in chain(xrange(5), xrange(6,18), xrange(19,23), xrange(24,100), xrange(101,116), xrange(117,177), xrange(178,187), xrange(188,191), xrange(192,210), xrange(211,220), xrange(222,233), xrange(234,240), xrange(241,243), xrange(244,254))] + ['/store/user/joeyr/JetHT/TrackMoverV27mext6_2017/200528_114719/0000/movedtree_%i.root' % i for i in chain(xrange(220,222), [5, 18, 23, 100, 116, 177, 187, 191, 210, 233, 240, 243])]),
'JetHT2018A': _fromnum0("/store/user/joeyr/JetHT/TrackMoverV27mext6_2018/200516_112826", 571, fnbase="movedtree"),
'JetHT2018B': _fromnum0("/store/user/joeyr/JetHT/TrackMoverV27mext6_2018/200516_112827", 290, fnbase="movedtree"),
'JetHT2018C': (214, ['/store/user/joeyr/JetHT/TrackMoverV27mext6_2018/200516_112828/0000/movedtree_%i.root' % i for i in chain(xrange(204), xrange(205,214))] + ['/store/user/joeyr/JetHT/TrackMoverV27mext6_2018/200528_114722/0000/movedtree_204.root']),
'JetHT2018D': (1032, ['/store/user/joeyr/JetHT/TrackMoverV27mext6_2018/200516_112829' + '/%04i/movedtree_%i.root' % (i/1000,i) for i in chain(xrange(1,3), xrange(4,15), xrange(20,220), xrange(221,224), xrange(226,246), xrange(247,251), xrange(252,259), xrange(260,264), xrange(273,275), xrange(276,280), xrange(281,286), xrange(287,301), xrange(306,314), xrange(315,323), xrange(324,326), xrange(327,331), xrange(332,338), xrange(340,346), xrange(347,364), xrange(365,369), xrange(382,384), xrange(387,389), xrange(394,396), xrange(401,403), xrange(408,411), xrange(413,416), xrange(443,446), xrange(463,465), xrange(474,478), xrange(490,492), xrange(499,501), xrange(502,506), xrange(507,509), xrange(510,512), xrange(513,515), xrange(517,520), xrange(525,527), xrange(531,533), xrange(550,552), xrange(557,563), xrange(567,570), xrange(574,576), xrange(581,585), xrange(588,591), xrange(604,606), xrange(617,619), xrange(630,633), xrange(636,640), xrange(641,643), xrange(645,648), xrange(662,664), xrange(677,680), xrange(681,683), xrange(685,688), xrange(689,693), xrange(714,716), xrange(730,735), xrange(758,762), xrange(771,775), xrange(778,780), xrange(790,793), xrange(805,807), xrange(825,827), xrange(839,841), xrange(848,852), xrange(861,865), xrange(874,1032), [18, 265, 267, 271, 302, 304, 371, 373, 376, 392, 417, 428, 431, 434, 437, 447, 455, 457, 459, 469, 471, 480, 484, 529, 537, 544, 548, 554, 592, 598, 608, 612, 620, 625, 628, 651, 653, 665, 674, 694, 696, 700, 708, 719, 728, 736, 741, 744, 748, 753, 755, 767, 782, 784, 786, 795, 797, 811, 820, 822, 828, 830, 843, 846, 859, 868, 870, 872])] + ['/store/user/joeyr/JetHT/TrackMoverV27mext6_2018/200528_175043/0000/movedtree_%i.root' % i for i in chain(xrange(659,661), [378, 381, 405, 418, 424, 435, 440, 460, 488, 498, 501, 523, 530, 535, 545, 553, 619, 626, 643, 710, 729, 740])] + ['/store/user/joeyr/JetHT/TrackMoverV27mext6_2018/200528_114741/0000/movedtree_%i.root' % i for i in chain(xrange(15,18), xrange(224,226), xrange(268,271), xrange(338,340), xrange(369,371), xrange(374,376), xrange(379,381), xrange(384,387), xrange(389,392), xrange(396,401), xrange(403,405), xrange(406,408), xrange(411,413), xrange(419,424), xrange(425,428), xrange(429,431), xrange(432,434), xrange(438,440), xrange(441,443), xrange(448,455), xrange(461,463), xrange(465,469), xrange(472,474), xrange(478,480), xrange(481,484), xrange(485,488), xrange(492,498), xrange(515,517), xrange(520,523), xrange(527,529), xrange(533,535), xrange(538,544), xrange(546,548), xrange(555,557), xrange(563,567), xrange(570,574), xrange(576,581), xrange(585,588), xrange(593,598), xrange(599,604), xrange(606,608), xrange(609,612), xrange(613,617), xrange(621,625), xrange(633,636), xrange(648,651), xrange(654,659), xrange(666,674), xrange(675,677), xrange(683,685), xrange(697,700), xrange(701,708), xrange(711,714), xrange(716,719), xrange(720,728), xrange(737,740), xrange(742,744), xrange(745,748), xrange(749,753), xrange(756,758), xrange(762,767), xrange(768,771), xrange(775,778), xrange(780,782), xrange(787,790), xrange(793,795), xrange(798,805), xrange(807,811), xrange(812,820), xrange(823,825), xrange(831,839), xrange(841,843), xrange(844,846), xrange(852,859), xrange(865,868), [0, 3, 19, 220, 246, 251, 259, 264, 266, 272, 275, 280, 286, 301, 303, 305, 314, 323, 326, 331, 346, 364, 372, 377, 393, 416, 436, 446, 456, 458, 470, 489, 506, 509, 512, 524, 536, 549, 552, 591, 627, 629, 640, 644, 652, 661, 664, 680, 688, 693, 695, 709, 735, 754, 783, 785, 796, 821, 827, 829, 847, 860, 869, 871, 873])]),
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

# only multijet samples
_add_single_files('nr_trackmovermctruthv27mv3', '/store/user/joeyr/hadded/TrackMoverMCTruthV27mv3', \
                      ['mfv_%s_tau%06ium_M%04i_%i' % (a,b,c,y) for y in (2017,2018) for a in ('neu',) for b in (100,300,1000,10000,30000) for c in (400,600,800,1200,1600,3000)])

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
