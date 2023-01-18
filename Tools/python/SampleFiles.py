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

  'mfv_neu_tau000300um_M0300_2017':_fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL17_MiniAOD/211207_194735/0000", 4, fnbase="MiniAOD", numbereddirs=False),
  'mfv_neu_tau000300um_M0600_2017':_fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL17_MiniAOD/211207_194759/0000", 4, fnbase="MiniAOD", numbereddirs=False),
  'mfv_neu_tau000300um_M0800_2017':_fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL17_MiniAOD/211207_194824/0000", 2, fnbase="MiniAOD", numbereddirs=False),
  'mfv_neu_tau001000um_M0300_2017':_fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL17_MiniAOD/211207_194849/0000", 5, fnbase="MiniAOD", numbereddirs=False),
  'mfv_neu_tau001000um_M0600_2017':_fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL17_MiniAOD/211207_194911/0000", 2, fnbase="MiniAOD", numbereddirs=False),
  'mfv_neu_tau001000um_M0800_2017':_fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL17_MiniAOD/211207_194934/0000", 3, fnbase="MiniAOD", numbereddirs=False),
#  'mfv_stopdbardbar_tau000300um_M0300_2017':_fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-300_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL17_MiniAOD/211207_195420/0000", 5, fnbase="MiniAOD", numbereddirs=False),
#  'mfv_stopdbardbar_tau000300um_M0600_2017':_fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-600_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL17_MiniAOD/211207_195446/0000", 3, fnbase="MiniAOD", numbereddirs=False),
#  'mfv_stopdbardbar_tau000300um_M0800_2017':_fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-800_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL17_MiniAOD/211207_195509/0000", 3, fnbase="MiniAOD", numbereddirs=False),
#  'mfv_stopdbardbar_tau001000um_M0300_2017':_fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-300_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL17_MiniAOD/211207_195532/0000", 4, fnbase="MiniAOD", numbereddirs=False),
#  'mfv_stopdbardbar_tau001000um_M0600_2017':_fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-600_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL17_MiniAOD/211207_195557/0000", 4, fnbase="MiniAOD", numbereddirs=False),
#  'mfv_stopdbardbar_tau001000um_M0800_2017':_fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-800_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL17_MiniAOD/211207_195620/0000", 5, fnbase="MiniAOD", numbereddirs=False),
#  'mfv_stopbbarbbar_tau000300um_M0300_2017':_fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-300_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL17_MiniAOD/211207_194958/0000", 3, fnbase="MiniAOD", numbereddirs=False),
#  'mfv_stopbbarbbar_tau000300um_M0600_2017':_fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-600_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL17_MiniAOD/211207_195021/0000", 4, fnbase="MiniAOD", numbereddirs=False),
#  'mfv_stopbbarbbar_tau000300um_M0800_2017':_fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-800_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL17_MiniAOD/211207_195045/0000", 3, fnbase="MiniAOD", numbereddirs=False),
#  'mfv_stopbbarbbar_tau001000um_M0300_2017':_fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-300_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL17_MiniAOD/211207_195111/0000", 5, fnbase="MiniAOD", numbereddirs=False),
#  'mfv_stopbbarbbar_tau001000um_M0600_2017':_fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-600_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL17_MiniAOD/211207_195334/0000", 3, fnbase="MiniAOD", numbereddirs=False),
#  'mfv_stopbbarbbar_tau001000um_M0800_2017':_fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-800_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL17_MiniAOD/211207_195357/0000", 4, fnbase="MiniAOD", numbereddirs=False),

})

################################################################################

_add_ds("ntupleulv1bm", {

# 2017 QCD and inclusive ttbar
'qcdht0200_2017': _fromnum1("/store/user/shogan/QCD_HT200to300_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleUL17V1Bm_2017/221104_204302", 96),
'qcdht0300_2017': (151, ['/store/user/shogan/QCD_HT300to500_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleUL17V1Bm_2017/221104_204315/0000/ntuple_%i.root' % i for i in chain(xrange(2,6), xrange(7,9), xrange(10,17), xrange(19,21), xrange(24,35), xrange(36,42), xrange(45,50), xrange(51,54), xrange(56,62), xrange(63,65), xrange(66,68), xrange(75,80), xrange(81,84), xrange(86,89), xrange(90,92), xrange(93,98), xrange(99,102), xrange(104,106), xrange(107,112), xrange(124,126), xrange(134,137), xrange(138,141), xrange(142,148), xrange(157,159), xrange(160,163), xrange(164,166), xrange(167,173), xrange(179,181), xrange(183,188), xrange(191,196), xrange(202,208), xrange(209,212), xrange(213,215), xrange(220,222), xrange(227,231), [69, 113, 115, 117, 122, 127, 130, 149, 151, 154, 177, 189, 200, 216, 218, 225, 233])]),
'qcdht0500_2017': _fromnum1("/store/user/shogan/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleUL17V1Bm_2017/221104_204328", 82),
'qcdht0700_2017': _fromnum1("/store/user/shogan/QCD_HT700to1000_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleUL17V1Bm_2017/221104_204341", 229),
'qcdht1000_2017': _fromnum1("/store/user/shogan/QCD_HT1000to1500_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleUL17V1Bm_2017/221104_204354", 135),
'qcdht1500_2017': _fromnum1("/store/user/shogan/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraph-pythia8/NtupleUL17V1Bm_2017/221104_204408", 240),
'qcdht2000_2017': _fromnum1("/store/user/shogan/QCD_HT2000toInf_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleUL17V1Bm_2017/221104_204421", 186),
'ttbar_2017': _fromnum1("/store/user/shogan/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleUL17V1Bm_2017/221104_204249", 1019),

# 2018 QCD and inclusive ttbar


# 2017 RPV Signal Samples
'mfv_neu_tau000100um_M0200_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-200_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_204557", 31),
'mfv_neu_tau000300um_M0200_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-200_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_204611", 26),
'mfv_neu_tau010000um_M0200_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-200_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_204626", 7),
'mfv_neu_tau030000um_M0200_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-200_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_204639", 9),
'mfv_neu_tau000100um_M0300_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_204654", 35),
'mfv_neu_tau000300um_M0300_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_204709", 26),
'mfv_neu_tau001000um_M0300_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_204723", 11),
'mfv_neu_tau010000um_M0300_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_204737", 5),
'mfv_neu_tau030000um_M0300_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_204751", 11),
'mfv_neu_tau000100um_M0400_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_204805", 35),
'mfv_neu_tau001000um_M0400_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_204819", 9),
'mfv_neu_tau010000um_M0400_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_204833", 5),
'mfv_neu_tau030000um_M0400_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_204847", 9),
'mfv_neu_tau000100um_M0600_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_204901", 32),
'mfv_neu_tau000300um_M0600_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_204915", 18),
'mfv_neu_tau001000um_M0600_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_204929", 7),
'mfv_neu_tau010000um_M0600_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_204944", 3),
'mfv_neu_tau030000um_M0600_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_205003", 6),
'mfv_neu_tau000300um_M0800_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_205019", 17),
'mfv_neu_tau001000um_M0800_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_205036", 4),
'mfv_neu_tau010000um_M0800_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_205052", 3),
'mfv_neu_tau030000um_M0800_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_205106", 4),
'mfv_neu_tau000100um_M1200_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_205120", 36),
'mfv_neu_tau000300um_M1200_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_205134", 12),
'mfv_neu_tau001000um_M1200_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_205149", 4),
'mfv_neu_tau010000um_M1200_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_205204", 2),
'mfv_neu_tau030000um_M1200_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_205217", 3),
'mfv_neu_tau000100um_M1600_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_205232", 36),
'mfv_neu_tau000300um_M1600_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_205245", 14),
'mfv_neu_tau001000um_M1600_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_205259", 3),
'mfv_neu_tau010000um_M1600_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_205313", 3),
'mfv_neu_tau030000um_M1600_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_205327", 3),
'mfv_neu_tau000100um_M3000_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_205342", 33),
'mfv_neu_tau000300um_M3000_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_205355", 13),
'mfv_neu_tau030000um_M3000_2017': (1, ['/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_205437/0000/ntuple_3.root']),
'mfv_stopdbardbar_tau000100um_M0200_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-200_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_205452", 34),
'mfv_stopdbardbar_tau000300um_M0200_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-200_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_205505", 33),
'mfv_stopdbardbar_tau001000um_M0200_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-200_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_205519", 12),
'mfv_stopdbardbar_tau010000um_M0200_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-200_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_205534", 5),
'mfv_stopdbardbar_tau030000um_M0200_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-200_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_205547", 7),
'mfv_stopdbardbar_tau000100um_M0300_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-300_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_205602", 32),
'mfv_stopdbardbar_tau000300um_M0300_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-300_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_205616", 35),
'mfv_stopdbardbar_tau001000um_M0300_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-300_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_205630", 11),
'mfv_stopdbardbar_tau010000um_M0300_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-300_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_205644", 5),
'mfv_stopdbardbar_tau030000um_M0300_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-300_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_205658", 7),
'mfv_stopdbardbar_tau000100um_M0400_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-400_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_205715", 33),
'mfv_stopdbardbar_tau000300um_M0400_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-400_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_205729", 33),
'mfv_stopdbardbar_tau001000um_M0400_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-400_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_205743", 10),
'mfv_stopdbardbar_tau010000um_M0400_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-400_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_205757", 5),
'mfv_stopdbardbar_tau030000um_M0400_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-400_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_205810", 7),
'mfv_stopdbardbar_tau000100um_M0600_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-600_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_205825", 35),
'mfv_stopdbardbar_tau000300um_M0600_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-600_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_205838", 29),
'mfv_stopdbardbar_tau010000um_M0600_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-600_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_205852", 5),
'mfv_stopdbardbar_tau030000um_M0600_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-600_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_205906", 5),
'mfv_stopdbardbar_tau000100um_M0800_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-800_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_205924", 35),
'mfv_stopdbardbar_tau000300um_M0800_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-800_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_205938", 19),
'mfv_stopdbardbar_tau001000um_M0800_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-800_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_205952", 5),
'mfv_stopdbardbar_tau010000um_M0800_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-800_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_210006", 5),
'mfv_stopdbardbar_tau030000um_M0800_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-800_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_210021", 6),
'mfv_stopdbardbar_tau000100um_M1200_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-1200_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_210035", 36),
'mfv_stopdbardbar_tau000300um_M1200_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-1200_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_210053", 21),
'mfv_stopdbardbar_tau001000um_M1200_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-1200_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_210107", 8),
'mfv_stopdbardbar_tau010000um_M1200_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-1200_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_210121", 3),
'mfv_stopdbardbar_tau030000um_M1200_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-1200_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_210135", 4),
'mfv_stopdbardbar_tau000100um_M1600_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-1600_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_210148", 35),
'mfv_stopdbardbar_tau001000um_M1600_2017': (2, ['/store/user/shogan/StopStopbarTo2Dbar2D_M-1600_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_210203/0000/ntuple_%i.root' % i for i in [1, 4]]),
'mfv_stopdbardbar_tau010000um_M1600_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-1600_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_210217", 4),
'mfv_stopdbardbar_tau030000um_M1600_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-1600_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_210235", 5),
'mfv_stopdbardbar_tau000100um_M3000_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-3000_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_210249", 38),
'mfv_stopdbardbar_tau000300um_M3000_2017': (22, ['/store/user/shogan/StopStopbarTo2Dbar2D_M-3000_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_210303/0000/ntuple_%i.root' % i for i in chain(xrange(3,21), xrange(22,25), [1])]),
'mfv_stopdbardbar_tau010000um_M3000_2017': (1, ['/store/user/shogan/StopStopbarTo2Dbar2D_M-3000_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_210333/0000/ntuple_5.root']),
'mfv_stopbbarbbar_tau000100um_M0200_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-200_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_210402", 33),
'mfv_stopbbarbbar_tau000300um_M0200_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-200_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_210417", 33),
'mfv_stopbbarbbar_tau001000um_M0200_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-200_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_210438", 11),
'mfv_stopbbarbbar_tau010000um_M0200_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-200_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_210456", 5),
'mfv_stopbbarbbar_tau030000um_M0200_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-200_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_210509", 8),
'mfv_stopbbarbbar_tau000100um_M0300_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-300_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_210524", 34),
'mfv_stopbbarbbar_tau000300um_M0300_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-300_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_210539", 32),
'mfv_stopbbarbbar_tau001000um_M0300_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-300_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_210552", 11),
'mfv_stopbbarbbar_tau010000um_M0300_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-300_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_210606", 5),
'mfv_stopbbarbbar_tau030000um_M0300_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-300_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_210620", 7),
'mfv_stopbbarbbar_tau000100um_M0400_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-400_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_210634", 33),
'mfv_stopbbarbbar_tau000300um_M0400_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-400_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_210648", 34),
'mfv_stopbbarbbar_tau001000um_M0400_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-400_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_210726", 9),
'mfv_stopbbarbbar_tau010000um_M0400_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-400_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_210740", 5),
'mfv_stopbbarbbar_tau030000um_M0400_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-400_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_210755", 7),
'mfv_stopbbarbbar_tau000100um_M0600_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-600_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_210809", 32),
'mfv_stopbbarbbar_tau000300um_M0600_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-600_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_210823", 26),
'mfv_stopbbarbbar_tau001000um_M0600_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-600_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_210837", 7),
'mfv_stopbbarbbar_tau010000um_M0600_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-600_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_210852", 3),
'mfv_stopbbarbbar_tau030000um_M0600_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-600_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_210906", 7),
'mfv_stopbbarbbar_tau000100um_M0800_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-800_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_210920", 36),
'mfv_stopbbarbbar_tau000300um_M0800_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-800_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_210934", 19),
'mfv_stopbbarbbar_tau001000um_M0800_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-800_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_210948", 9),
'mfv_stopbbarbbar_tau010000um_M0800_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-800_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_211003", 3),
'mfv_stopbbarbbar_tau030000um_M0800_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-800_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_211018", 6),
'mfv_stopbbarbbar_tau000100um_M1200_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-1200_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_211032", 35),
'mfv_stopbbarbbar_tau000300um_M1200_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-1200_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_211046", 19),
'mfv_stopbbarbbar_tau001000um_M1200_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-1200_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_211100", 5),
'mfv_stopbbarbbar_tau010000um_M1200_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-1200_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_211115", 3),
'mfv_stopbbarbbar_tau030000um_M1200_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-1200_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_211130", 4),
'mfv_stopbbarbbar_tau000300um_M1600_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-1600_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_211144", 16),
'mfv_stopbbarbbar_tau001000um_M1600_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-1600_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_211158", 3),
'mfv_stopbbarbbar_tau030000um_M1600_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-1600_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_211212", 5),
'mfv_stopbbarbbar_tau000100um_M3000_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-3000_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_211227", 42),
'mfv_stopbbarbbar_tau000300um_M3000_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-3000_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_211241", 21),
'mfv_stopbbarbbar_tau001000um_M3000_2017': (1, ['/store/user/shogan/StopStopbarTo2Bbar2B_M-3000_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_211255/0000/ntuple_3.root']),
'mfv_stopbbarbbar_tau030000um_M3000_2017': (2, ['/store/user/shogan/StopStopbarTo2Bbar2B_M-3000_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/221104_211323/0000/ntuple_%i.root' % i for i in [1, 3]]),
})

_add_ds("ntupleulgvtxbjetv29bm", {                                                                                                                                                  'ttbar_2017': _fromnum0("/store/user/pkotamni/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleULGvtxBjetV29Bm_2017/230117_115144", 1019),                                           }) 
_add_ds("ntupleulgvtxbjet17v43bm", {                                                                                                                                                'ttbar_2017': _fromnum0("/store/user/pkotamni/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleULGvtxBjet17V43Bm_2017/230117_121141", 1019),                                         })
_add_ds("ntupleulgvtxbjetv43bm", {                                                                                                                                                  'ttbar_2017': _fromnum1("/store/user/pekotamn/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleULGvtxBjetV43Bm_20162/230106_212717", 1019),                                          })
_add_ds("ntupleulgvtxbjetv41bm", {                                                                                                                                                  'ttbar_2017': _fromnum0("/store/user/pkotamni/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleULGvtxBjetV41Bm_2017/230112_132624", 1019),                                           })

_add_ds("ntupleulgvtxbjetv29bm", {                                                                                                                                                  'ggHToSSTobbbb_tau10mm_M55_2017': _fromnum1("/store/user/pekotamn/ggH_HToSSTobbbb_MH-125_MS-55_ctauS-10_TuneCP5_13TeV-powheg-pythia8/NtupleULGvtxBjetV29Bm_NoEF_2017/230117_175300", 86),                                                                                                                                                                               })
_add_ds("ntupleulgvtxbjet17v43bm", {                                                                                                                                                'ggHToSSTobbbb_tau10mm_M55_2017': _fromnum1("/store/user/pekotamn/ggH_HToSSTobbbb_MH-125_MS-55_ctauS-10_TuneCP5_13TeV-powheg-pythia8/NtupleULGvtxBjet17V43Bm_NoEF_2017/230117_181042", 86),                                                                                                                                                                             })
_add_ds("ntupleulgvtxbjetv43bm", {                                                                                                                                                  'ggHToSSTobbbb_tau10mm_M55_2017': _fromnum1("/store/user/pekotamn/ggH_HToSSTobbbb_MH-125_MS-55_ctauS-10_TuneCP5_13TeV-powheg-pythia8/NtupleULGvtxBjetV43Bm_NoEF_20162/230107_223805", 89),                                                                                                                                                                              'ggHToSSTobbbb_tau100mm_M55_2017': _fromnum1("/store/user/pekotamn/ggH_HToSSTobbbb_MH-125_MS-55_ctauS-100_TuneCP5_13TeV-powheg-pythia8/NtupleULGvtxBjetV43Bm_NoEF_20162/230107_223817", 87),                                                                                                                                                                            }) 
_add_ds("ntupleulgvtxbjetv41bm", {                                                                                                                                                    'ggHToSSTobbbb_tau10mm_M55_2017': _fromnum1("/store/user/pekotamn/ggH_HToSSTobbbb_MH-125_MS-55_ctauS-10_TuneCP5_13TeV-powheg-pythia8/NtupleULGvtxBjetV41Bm_NoEF_2017/230112_192546", 88),                                                                                                                                                                               })


# 2018 RPV Signal Samples

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
