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
    #print(_d.keys())
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

#execfile(cmssw_base('src/JMTucker/Tools/python/enc_SampleFiles.py'))

_removed = [
    ]

for name, ds, fns in _removed:
    for fn in fns:
        _remove_file(name, ds, fn)

################################################################################

_add_ds("miniaod", {
  'mfv_splitSUSY_tau000001000um_M1200_1100_2017':_fromnum1("/store/user/ali/splitSUSY_M1200_1100_ctau1p0_TuneCP2_13TeV_pythia8/RunIISummer20UL17_MiniAOD/210813_015111/0000/", 50, fnbase="MiniAOD", numbereddirs=False),
  'mfv_splitSUSY_tau000010000um_M1200_1100_2017':_fromnum1("/store/user/ali/splitSUSY_M1200_1100_ctau10p0_TuneCP2_13TeV_pythia8/RunIISummer20UL17_MiniAOD/210813_015035/0000/", 50, fnbase="MiniAOD", numbereddirs=False),
  'mfv_splitSUSY_tau000001000um_M1400_1200_2017':_fromnum1("/store/user/ali/splitSUSY_M1400_1200_ctau1p0_TuneCP2_13TeV_pythia8/RunIISummer20UL17_MiniAOD/210813_015224/0000/", 50, fnbase="MiniAOD", numbereddirs=False),
  'mfv_splitSUSY_tau000010000um_M1400_1200_2017':_fromnum1("/store/user/ali/splitSUSY_M1400_1200_ctau10p0_TuneCP2_13TeV_pythia8/RunIISummer20UL17_MiniAOD/210813_015149/0000/", 50, fnbase="MiniAOD", numbereddirs=False),
  'mfv_splitSUSY_tau000000100um_M2000_1800_2017':_fromnum1("/store/user/ali/splitSUSY_M2000_1800_ctau0p1_TuneCP2_13TeV_pythia8/RunIISummer20UL17_MiniAOD/210813_015301/0000/", 50, fnbase="MiniAOD", numbereddirs=False),
  'mfv_splitSUSY_tau000000300um_M2000_1800_2017':_fromnum1("/store/user/ali/splitSUSY_M2000_1800_ctau0p3_TuneCP2_13TeV_pythia8/RunIISummer20UL17_MiniAOD/210813_015338/0000/", 50, fnbase="MiniAOD", numbereddirs=False),
  'mfv_splitSUSY_tau000010000um_M2000_1800_2017':_fromnum1("/store/user/ali/splitSUSY_M2000_1800_ctau10p0_TuneCP2_13TeV_pythia8/RunIISummer20UL17_MiniAOD/210813_015414/0000/", 50, fnbase="MiniAOD", numbereddirs=False),
  'mfv_splitSUSY_tau000001000um_M2000_1800_2017':_fromnum1("/store/user/ali/splitSUSY_M2000_1800_ctau1p0_TuneCP2_13TeV_pythia8/RunIISummer20UL17_MiniAOD/210813_015449/0000", 50, fnbase="MiniAOD", numbereddirs=False),
  'mfv_splitSUSY_tau000000100um_M2000_1900_2017':_fromnum1("/store/user/ali/splitSUSY_M2000_1900_ctau0p1_TuneCP2_13TeV_pythia8/RunIISummer20UL17_MiniAOD/210813_015526/0000/", 50, fnbase="MiniAOD", numbereddirs=False),
  'mfv_splitSUSY_tau000000300um_M2000_1900_2017':_fromnum1("/store/user/ali/splitSUSY_M2000_1900_ctau0p3_TuneCP2_13TeV_pythia8/RunIISummer20UL17_MiniAOD/210813_015602/0000/", 50, fnbase="MiniAOD", numbereddirs=False),
  'mfv_splitSUSY_tau000010000um_M2000_1900_2017':_fromnum1("/store/user/ali/splitSUSY_M2000_1900_ctau10p0_TuneCP2_13TeV_pythia8/RunIISummer20UL17_MiniAOD/210813_015650/0000/", 50, fnbase="MiniAOD", numbereddirs=False),
  'mfv_splitSUSY_tau000001000um_M2000_1900_2017':_fromnum1("/store/user/ali/splitSUSY_M2000_1900_ctau1p0_TuneCP2_13TeV_pythia8/RunIISummer20UL17_MiniAOD/210813_015725/0000/", 50, fnbase="MiniAOD", numbereddirs=False),
  'mfv_splitSUSY_tau000000100um_M2400_100_2017':_fromnum1("/store/user/ali/splitSUSY_M2400_100_ctau0p1_TuneCP2_13TeV_pythia8/RunIISummer20UL17_MiniAOD/210813_015802/0000/", 50, fnbase="MiniAOD", numbereddirs=False),
  'mfv_splitSUSY_tau000000300um_M2400_100_2017':_fromnum1("/store/user/ali/splitSUSY_M2400_100_ctau0p3_TuneCP2_13TeV_pythia8/RunIISummer20UL17_MiniAOD/210813_015837/0000/", 50, fnbase="MiniAOD", numbereddirs=False),
  'mfv_splitSUSY_tau000010000um_M2400_100_2017':_fromnum1("/store/user/ali/splitSUSY_M2400_100_ctau10p0_TuneCP2_13TeV_pythia8/RunIISummer20UL17_MiniAOD/210813_015914/0000/", 50, fnbase="MiniAOD", numbereddirs=False),
  'mfv_splitSUSY_tau000001000um_M2400_100_2017':_fromnum1("/store/user/ali/splitSUSY_M2400_100_ctau1p0_TuneCP2_13TeV_pythia8/RunIISummer20UL17_MiniAOD/210813_015949/0000/", 50, fnbase="MiniAOD", numbereddirs=False),
  'mfv_splitSUSY_tau000000100um_M2400_2300_2017':_fromnum1("/store/user/ali/splitSUSY_M2400_2300_ctau0p1_TuneCP2_13TeV_pythia8/RunIISummer20UL17_MiniAOD/210813_020027/0000/", 50, fnbase="MiniAOD", numbereddirs=False),
  'mfv_splitSUSY_tau000000300um_M2400_2300_2017':_fromnum1("/store/user/ali/splitSUSY_M2400_2300_ctau0p3_TuneCP2_13TeV_pythia8/RunIISummer20UL17_MiniAOD/210813_020104/0000/", 50, fnbase="MiniAOD", numbereddirs=False),
  'mfv_splitSUSY_tau000010000um_M2400_2300_2017':_fromnum1("/store/user/ali/splitSUSY_M2400_2300_ctau10p0_TuneCP2_13TeV_pythia8/RunIISummer20UL17_MiniAOD/210813_020142/0000/", 50, fnbase="MiniAOD", numbereddirs=False),
  'mfv_splitSUSY_tau000001000um_M2400_2300_2017':_fromnum1("/store/user/ali/splitSUSY_M2400_2300_ctau1p0_TuneCP2_13TeV_pythia8/RunIISummer20UL17_MiniAOD/210813_020218/0000/", 50, fnbase="MiniAOD", numbereddirs=False),
})

_add_ds("ntupleulv0metm", {
'qcdht0200_2017': (96, ['/store/user/ali/QCD_HT200to300_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleULV0METm_2017/210823_083216/0000/ntuple_%i.root' % i for i in [31, 79]] + ['/store/user/ali/QCD_HT200to300_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleULV0METm_2017/210822_201038/0000/ntuple_%i.root' % i for i in chain(xrange(31), xrange(32,79), xrange(80,96))]),
'qcdht0300_2017': (233, ['/store/user/ali/QCD_HT300to500_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleULV0METm_2017/210823_083227/0000/ntuple_%i.root' % i for i in [142, 177, 200, 223]] + ['/store/user/ali/QCD_HT300to500_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleULV0METm_2017/210822_201039/0000/ntuple_%i.root' % i for i in chain(xrange(142), xrange(143,177), xrange(178,200), xrange(201,223), xrange(224,233))]),
'qcdht0500_2017': _fromnum0("/store/user/ali/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleULV0METm_2017/210822_201040", 82),
'qcdht0500ext_2017': (85, ['/store/user/ali/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleULV0METm_2017/210822_201041/0000/ntuple_%i.root' % i for i in chain(xrange(66), xrange(67,85))] + ['/store/user/ali/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleULV0METm_2017/210823_083224/0000/ntuple_66.root']),
'qcdht0700_2017': _fromnum0("/store/user/ali/QCD_HT700to1000_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleULV0METm_2017/210822_201042", 229),
'qcdht1000_2017': _fromnum0("/store/user/ali/QCD_HT1000to1500_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleULV0METm_2017/210822_201043", 135),
'qcdht1500_2017': (240, ['/store/user/ali/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraph-pythia8/NtupleULV0METm_2017/210823_083218/0000/ntuple_%i.root' % i for i in [23, 39]] + ['/store/user/ali/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraph-pythia8/NtupleULV0METm_2017/210822_201044/0000/ntuple_%i.root' % i for i in chain(xrange(23), xrange(24,39), xrange(40,240))]),
'qcdht2000_2017': (186, ['/store/user/ali/QCD_HT2000toInf_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleULV0METm_2017/210823_083228/0000/ntuple_%i.root' % i for i in [14, 90]] + ['/store/user/ali/QCD_HT2000toInf_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleULV0METm_2017/210822_201045/0000/ntuple_%i.root' % i for i in chain(xrange(14), xrange(15,90), xrange(91,186))]),
'wjetstolnu_2017': (118, ['/store/user/ali/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV0METm_2017/210823_083215/0000/ntuple_%i.root' % i for i in [30, 47]] + ['/store/user/ali/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV0METm_2017/210822_201046/0000/ntuple_%i.root' % i for i in chain(xrange(27), xrange(28,30), xrange(31,46), xrange(48,120))]),
'dyjetstollM10_2017': (115, ['/store/user/ali/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV0METm_2017/210822_201047/0000/ntuple_%i.root' % i for i in chain(xrange(2), xrange(3,9), xrange(10,42), xrange(43,50), xrange(51,59), xrange(60,65), xrange(66,84), xrange(85,94), xrange(95,117))] + ['/store/user/ali/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV0METm_2017/210823_153536/0000/ntuple_42.root'] + ['/store/user/ali/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV0METm_2017/210823_083219/0000/ntuple_%i.root' % i for i in [2, 59, 65, 84, 94]]),
'dyjetstollM50_2017': (131, ['/store/user/ali/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV0METm_2017/210822_201048/0000/ntuple_%i.root' % i for i in chain(xrange(115), xrange(116,131))] + ['/store/user/ali/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV0METm_2017/210823_083215/0000/ntuple_115.root']),
'ttbar_2017': (932, ['/store/user/ali/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleULV0METm_2017/210824_085650/0000/ntuple_%i.root' % i for i in [963, 965]] + ['/store/user/ali/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleULV0METm_2017/210823_153537/0000/ntuple_%i.root' % i for i in [317, 388]] + ['/store/user/ali/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleULV0METm_2017/210822_203734' + '/%04i/ntuple_%i.root' % (i/1000,i) for i in chain(xrange(90), xrange(96,223), xrange(229,241), xrange(244,274), xrange(276,282), xrange(290,294), xrange(299,301), xrange(309,311), xrange(321,352), xrange(361,366), xrange(370,386), xrange(391,410), xrange(413,420), xrange(430,434), xrange(435,437), xrange(438,440), xrange(441,747), xrange(751,753), xrange(757,784), xrange(785,947), xrange(959,961), xrange(971,974), xrange(975,977), xrange(978,1019), [91, 94, 225, 286, 313, 316, 356, 359, 411, 423, 427, 748, 952, 957])] + ['/store/user/ali/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleULV0METm_2017/210823_083222/0000/ntuple_%i.root' % i for i in [288, 354, 429, 434, 437, 440, 754, 784, 962, 967]]),
'zjetstonunuht0100_2017': (37, ['/store/user/ali/ZJetsToNuNu_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV0METm_2017/210822_203727/0000/ntuple_%i.root' % i for i in chain(xrange(11), xrange(12,20), xrange(21,37))] + ['/store/user/ali/ZJetsToNuNu_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV0METm_2017/210823_083226/0000/ntuple_%i.root' % i for i in [11, 20]]),
'zjetstonunuht0200_2017': _fromnum0("/store/user/ali/ZJetsToNuNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV0METm_2017/210822_203728", 37),
'zjetstonunuht0400_2017': (29, ['/store/user/ali/ZJetsToNuNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV0METm_2017/210822_203729/0000/ntuple_%i.root' % i for i in chain(xrange(14), xrange(15,29))] + ['/store/user/ali/ZJetsToNuNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV0METm_2017/210823_083219/0000/ntuple_14.root']),
'zjetstonunuht0600_2017': _fromnum0("/store/user/ali/ZJetsToNuNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV0METm_2017/210822_203730", 11),
'zjetstonunuht0800_2017': _fromnum0("/store/user/ali/ZJetsToNuNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV0METm_2017/210822_203731", 5),
'zjetstonunuht1200_2017': _fromnum0("/store/user/ali/ZJetsToNuNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV0METm_2017/210822_203732", 15),
'zjetstonunuht2500_2017': _fromnum0("/store/user/ali/ZJetsToNuNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV0METm_2017/210822_203733", 23),
'mfv_splitSUSY_tau000001000um_M1400_1200_2017': _fromnum0("/store/user/ali/splitSUSY_M1400_1200_ctau1p0_TuneCP2_13TeV_pythia8/NtupleULV0METm_2017/210823_154736", 50),
'mfv_splitSUSY_tau000010000um_M1400_1200_2017': _fromnum0("/store/user/ali/splitSUSY_M1400_1200_ctau10p0_TuneCP2_13TeV_pythia8/NtupleULV0METm_2017/210823_154737", 50),
'mfv_splitSUSY_tau000001000um_M1200_1100_2017': _fromnum0("/store/user/ali/splitSUSY_M1200_1100_ctau1p0_TuneCP2_13TeV_pythia8/NtupleULV0METm_2017/210823_154738", 50),
'mfv_splitSUSY_tau000010000um_M1200_1100_2017': _fromnum0("/store/user/ali/splitSUSY_M1200_1100_ctau10p0_TuneCP2_13TeV_pythia8/NtupleULV0METm_2017/210823_154739", 50),
'mfv_splitSUSY_tau000000100um_M2000_1800_2017': _fromnum0("/store/user/ali/splitSUSY_M2000_1800_ctau0p1_TuneCP2_13TeV_pythia8/NtupleULV0METm_2017/210823_154740", 50),
'mfv_splitSUSY_tau000000300um_M2000_1800_2017': _fromnum0("/store/user/ali/splitSUSY_M2000_1800_ctau0p3_TuneCP2_13TeV_pythia8/NtupleULV0METm_2017/210823_154741", 50),
'mfv_splitSUSY_tau000010000um_M2000_1800_2017': _fromnum0("/store/user/ali/splitSUSY_M2000_1800_ctau10p0_TuneCP2_13TeV_pythia8/NtupleULV0METm_2017/210823_154742", 50),
'mfv_splitSUSY_tau000001000um_M2000_1800_2017': _fromnum0("/store/user/ali/splitSUSY_M2000_1800_ctau1p0_TuneCP2_13TeV_pythia8/NtupleULV0METm_2017/210823_154743", 50),
'mfv_splitSUSY_tau000000100um_M2000_1900_2017': _fromnum0("/store/user/ali/splitSUSY_M2000_1900_ctau0p1_TuneCP2_13TeV_pythia8/NtupleULV0METm_2017/210823_154744", 50),
'mfv_splitSUSY_tau000000300um_M2000_1900_2017': _fromnum0("/store/user/ali/splitSUSY_M2000_1900_ctau0p3_TuneCP2_13TeV_pythia8/NtupleULV0METm_2017/210823_154745", 50),
'mfv_splitSUSY_tau000010000um_M2000_1900_2017': _fromnum0("/store/user/ali/splitSUSY_M2000_1900_ctau10p0_TuneCP2_13TeV_pythia8/NtupleULV0METm_2017/210823_154746", 50),
'mfv_splitSUSY_tau000001000um_M2000_1900_2017': _fromnum0("/store/user/ali/splitSUSY_M2000_1900_ctau1p0_TuneCP2_13TeV_pythia8/NtupleULV0METm_2017/210823_154747", 50),
'mfv_splitSUSY_tau000000100um_M2400_100_2017': _fromnum0("/store/user/ali/splitSUSY_M2400_100_ctau0p1_TuneCP2_13TeV_pythia8/NtupleULV0METm_2017/210823_154748", 50),
'mfv_splitSUSY_tau000000300um_M2400_100_2017': _fromnum0("/store/user/ali/splitSUSY_M2400_100_ctau0p3_TuneCP2_13TeV_pythia8/NtupleULV0METm_2017/210823_154749", 50),
'mfv_splitSUSY_tau000010000um_M2400_100_2017': _fromnum0("/store/user/ali/splitSUSY_M2400_100_ctau10p0_TuneCP2_13TeV_pythia8/NtupleULV0METm_2017/210823_154750", 50),
'mfv_splitSUSY_tau000001000um_M2400_100_2017': _fromnum0("/store/user/ali/splitSUSY_M2400_100_ctau1p0_TuneCP2_13TeV_pythia8/NtupleULV0METm_2017/210823_154751", 50),
'mfv_splitSUSY_tau000000100um_M2400_2300_2017': _fromnum0("/store/user/ali/splitSUSY_M2400_2300_ctau0p1_TuneCP2_13TeV_pythia8/NtupleULV0METm_2017/210823_154752", 50),
'mfv_splitSUSY_tau000000300um_M2400_2300_2017': _fromnum0("/store/user/ali/splitSUSY_M2400_2300_ctau0p3_TuneCP2_13TeV_pythia8/NtupleULV0METm_2017/210823_154753", 50),
'mfv_splitSUSY_tau000010000um_M2400_2300_2017': _fromnum0("/store/user/ali/splitSUSY_M2400_2300_ctau10p0_TuneCP2_13TeV_pythia8/NtupleULV0METm_2017/210823_154754", 50),
'mfv_splitSUSY_tau000001000um_M2400_2300_2017': _fromnum0("/store/user/ali/splitSUSY_M2400_2300_ctau1p0_TuneCP2_13TeV_pythia8/NtupleULV0METm_2017/210823_154755", 50),
})

_add_ds("ntupleulv1_keeptkmetm", {
'qcdht0200_2017': _fromnum0("/store/user/ali/QCD_HT200to300_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleULV1_keeptkMETm_2017/210917_104447", 96),
'qcdht0300_2017': _fromnum0("/store/user/ali/QCD_HT300to500_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleULV1_keeptkMETm_2017/210917_104448", 233),
'qcdht0500_2017': _fromnum0("/store/user/ali/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleULV1_keeptkMETm_2017/210917_104449", 82),
'qcdht0500ext_2017': _fromnum1("/store/user/lian/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleULV1_keeptkMETm_2017/210917_154315", 86),
'qcdht0700_2017': _fromnum0("/store/user/ali/QCD_HT700to1000_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleULV1_keeptkMETm_2017/210917_104450", 229),
'qcdht1000_2017': _fromnum1("/store/user/lian/QCD_HT1000to1500_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleULV1_keeptkMETm_2017/210917_154329", 135),
'qcdht1500_2017': _fromnum1("/store/user/lian/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraph-pythia8/NtupleULV1_keeptkMETm_2017/210918_173515", 240),
'qcdht2000_2017': _fromnum1("/store/user/lian/QCD_HT2000toInf_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleULV1_keeptkMETm_2017/210917_154343", 186),
'wjetstolnu_2017': _fromnum1("/store/user/lian/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV1_keeptkMETm_2017/210917_154358", 236),
'dyjetstollM10_2017': _fromnum1("/store/user/lian/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV1_keeptkMETm_2017/210917_154432", 206),
'dyjetstollM50_2017': _fromnum1("/store/user/lian/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV1_keeptkMETm_2017/210917_154446", 144),
'ttbar_2017': (1019, ['/store/user/ali/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleULV1_keeptkMETm_2017/210917_104519' + '/%04i/ntuple_%i.root' % (i/1000,i) for i in chain(xrange(366), xrange(367,1019))] + ['/store/user/ali/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleULV1_keeptkMETm_2017/210918_063140/0000/ntuple_366.root']),
'zjetstonunuht0100_2017': _fromnum1("/store/user/lian/ZJetsToNuNu_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV1_keeptkMETm_2017/210918_173538", 115),
'zjetstonunuht0200_2017': _fromnum1("/store/user/lian/ZJetsToNuNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV1_keeptkMETm_2017/210918_173555", 127),
'zjetstonunuht0400_2017': _fromnum1("/store/user/lian/ZJetsToNuNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV1_keeptkMETm_2017/210918_173614", 124),
'zjetstonunuht0600_2017': _fromnum1("/store/user/lian/ZJetsToNuNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV1_keeptkMETm_2017/210918_173632", 62),
'zjetstonunuht0800_2017': _fromnum1("/store/user/lian/ZJetsToNuNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV1_keeptkMETm_2017/210918_173649", 27),
'zjetstonunuht1200_2017': _fromnum1("/store/user/lian/ZJetsToNuNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV1_keeptkMETm_2017/210918_173706", 24),
'zjetstonunuht2500_2017': _fromnum1("/store/user/lian/ZJetsToNuNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV1_keeptkMETm_2017/210918_173723", 23),
'mfv_splitSUSY_tau000001000um_M1400_1200_2017': _fromnum0("/store/user/ali/splitSUSY_M1400_1200_ctau1p0_TuneCP2_13TeV_pythia8/NtupleULV1_keeptkMETm_2017/210917_104452", 50),
'mfv_splitSUSY_tau000010000um_M1400_1200_2017': _fromnum0("/store/user/ali/splitSUSY_M1400_1200_ctau10p0_TuneCP2_13TeV_pythia8/NtupleULV1_keeptkMETm_2017/210917_104453", 50),
'mfv_splitSUSY_tau000001000um_M1200_1100_2017': _fromnum0("/store/user/ali/splitSUSY_M1200_1100_ctau1p0_TuneCP2_13TeV_pythia8/NtupleULV1_keeptkMETm_2017/210917_104454", 50),
'mfv_splitSUSY_tau000010000um_M1200_1100_2017': _fromnum0("/store/user/ali/splitSUSY_M1200_1100_ctau10p0_TuneCP2_13TeV_pythia8/NtupleULV1_keeptkMETm_2017/210917_104455", 50),
'mfv_splitSUSY_tau000000100um_M2000_1800_2017': _fromnum0("/store/user/ali/splitSUSY_M2000_1800_ctau0p1_TuneCP2_13TeV_pythia8/NtupleULV1_keeptkMETm_2017/210917_104456", 50),
'mfv_splitSUSY_tau000000300um_M2000_1800_2017': _fromnum0("/store/user/ali/splitSUSY_M2000_1800_ctau0p3_TuneCP2_13TeV_pythia8/NtupleULV1_keeptkMETm_2017/210917_104457", 50),
'mfv_splitSUSY_tau000010000um_M2000_1800_2017': _fromnum0("/store/user/ali/splitSUSY_M2000_1800_ctau10p0_TuneCP2_13TeV_pythia8/NtupleULV1_keeptkMETm_2017/210917_104458", 50),
'mfv_splitSUSY_tau000001000um_M2000_1800_2017': _fromnum0("/store/user/ali/splitSUSY_M2000_1800_ctau1p0_TuneCP2_13TeV_pythia8/NtupleULV1_keeptkMETm_2017/210917_104459", 50),
'mfv_splitSUSY_tau000000100um_M2000_1900_2017': _fromnum0("/store/user/ali/splitSUSY_M2000_1900_ctau0p1_TuneCP2_13TeV_pythia8/NtupleULV1_keeptkMETm_2017/210917_104500", 50),
'mfv_splitSUSY_tau000000300um_M2000_1900_2017': _fromnum0("/store/user/ali/splitSUSY_M2000_1900_ctau0p3_TuneCP2_13TeV_pythia8/NtupleULV1_keeptkMETm_2017/210917_104501", 50),
'mfv_splitSUSY_tau000010000um_M2000_1900_2017': _fromnum0("/store/user/ali/splitSUSY_M2000_1900_ctau10p0_TuneCP2_13TeV_pythia8/NtupleULV1_keeptkMETm_2017/210917_104502", 50),
'mfv_splitSUSY_tau000001000um_M2000_1900_2017': _fromnum0("/store/user/ali/splitSUSY_M2000_1900_ctau1p0_TuneCP2_13TeV_pythia8/NtupleULV1_keeptkMETm_2017/210917_104503", 50),
'mfv_splitSUSY_tau000000100um_M2400_100_2017': _fromnum0("/store/user/ali/splitSUSY_M2400_100_ctau0p1_TuneCP2_13TeV_pythia8/NtupleULV1_keeptkMETm_2017/210917_104504", 50),
'mfv_splitSUSY_tau000000300um_M2400_100_2017': _fromnum0("/store/user/ali/splitSUSY_M2400_100_ctau0p3_TuneCP2_13TeV_pythia8/NtupleULV1_keeptkMETm_2017/210917_104505", 50),
'mfv_splitSUSY_tau000010000um_M2400_100_2017': _fromnum0("/store/user/ali/splitSUSY_M2400_100_ctau10p0_TuneCP2_13TeV_pythia8/NtupleULV1_keeptkMETm_2017/210917_104506", 50),
'mfv_splitSUSY_tau000001000um_M2400_100_2017': _fromnum0("/store/user/ali/splitSUSY_M2400_100_ctau1p0_TuneCP2_13TeV_pythia8/NtupleULV1_keeptkMETm_2017/210917_104507", 50),
'mfv_splitSUSY_tau000000100um_M2400_2300_2017': _fromnum0("/store/user/ali/splitSUSY_M2400_2300_ctau0p1_TuneCP2_13TeV_pythia8/NtupleULV1_keeptkMETm_2017/210917_104508", 50),
'mfv_splitSUSY_tau000000300um_M2400_2300_2017': _fromnum0("/store/user/ali/splitSUSY_M2400_2300_ctau0p3_TuneCP2_13TeV_pythia8/NtupleULV1_keeptkMETm_2017/210917_104509", 50),
'mfv_splitSUSY_tau000010000um_M2400_2300_2017': _fromnum0("/store/user/ali/splitSUSY_M2400_2300_ctau10p0_TuneCP2_13TeV_pythia8/NtupleULV1_keeptkMETm_2017/210917_104510", 50),
'mfv_splitSUSY_tau000001000um_M2400_2300_2017': _fromnum0("/store/user/ali/splitSUSY_M2400_2300_ctau1p0_TuneCP2_13TeV_pythia8/NtupleULV1_keeptkMETm_2017/210917_104511", 50),
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
        print colors.boldred('red means the file is OK,'), colors.green('green means it should stay in the removed list')
        for name, ds, fns in _removed:
            for fn in fns:
                print (colors.boldred if ok(fn) else colors.green)('%s %s %s' % (name, ds, fn))

    else:
        if not (len(sys.argv) == 1 and sys.argv[0].endswith('/SampleFiles.py')):
            sys.exit('did not understand argv %r' % sys.argv)
