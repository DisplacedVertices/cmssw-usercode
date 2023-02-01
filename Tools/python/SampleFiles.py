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
'qcdht0200_2017': _fromnum1("/store/user/shogan/QCD_HT200to300_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleUL17V1Bm_2017/230111_190109", 96),
'qcdht0300_2017': (215, ['/store/user/shogan/QCD_HT300to500_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleUL17V1Bm_2017/230112_140319/0000/ntuple_%i.root' % i for i in chain(xrange(1,10), xrange(12,18), xrange(19,23), xrange(24,27), xrange(29,41), xrange(43,47), xrange(49,61), xrange(62,65), xrange(66,87), xrange(89,92), xrange(93,113), xrange(114,130), xrange(131,184), xrange(185,234))]),
'qcdht0500_2017': _fromnum1("/store/user/shogan/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleUL17V1Bm_2017/230111_190135", 82),
'qcdht0700_2017': (213, ['/store/user/shogan/QCD_HT700to1000_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleUL17V1Bm_2017/230112_211812/0000/ntuple_%i.root' % i for i in chain(xrange(1,39), xrange(40,75), xrange(76,82), xrange(83,86), xrange(87,89), xrange(90,92), xrange(95,134), xrange(135,140), xrange(141,150), xrange(151,157), xrange(160,165), xrange(166,215), xrange(216,221), xrange(222,230), [158])]),
'qcdht1000_2017': _fromnum1("/store/user/shogan/QCD_HT1000to1500_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleUL17V1Bm_2017/230111_190200", 135),
'qcdht1500_2017': (223, ['/store/user/shogan/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraph-pythia8/NtupleUL17V1Bm_2017/230111_190214/0000/ntuple_%i.root' % i for i in chain(xrange(1,85), xrange(91,228), [87, 89])]),
'qcdht2000_2017': _fromnum1("/store/user/shogan/QCD_HT2000toInf_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleUL17V1Bm_2017/230111_190227", 186),
'ttbar_2017': _fromnum1("/store/user/shogan/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleUL17V1Bm_2017/230111_190243", 1019),

# 2018 QCD and inclusive ttbar
'qcdht0200_2018': _fromnum1("/store/user/shogan/QCD_HT200to300_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleUL18V1Bm_2018/230111_185454", 49),
'qcdht0200ext_2018': _fromnum1("/store/user/shogan/QCD_HT200to300_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleUL18V1Bm_2018/230111_185507", 83),
'qcdht0300_2018': (21, ['/store/user/shogan/QCD_HT300to500_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleUL18V1Bm_2018/230111_192227/0000/ntuple_%i.root' % i for i in chain(xrange(1,4), xrange(5,16), xrange(19,21), xrange(22,24), xrange(25,27), [17])]),
'qcdht0500_2018': _fromnum1("/store/user/shogan/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleUL18V1Bm_2018/230111_185536", 27),
'qcdht0700_2018': _fromnum1("/store/user/shogan/QCD_HT700to1000_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleUL18V1Bm_2018/230111_185550", 23),
'qcdht1000_2018': (25, ['/store/user/shogan/QCD_HT1000to1500_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleUL18V1Bm_2018/230111_185603/0000/ntuple_%i.root' % i for i in chain(xrange(2,7), xrange(8,11), xrange(15,17), xrange(18,24), xrange(25,27), xrange(33,35), [12, 31, 36, 38, 41])]),
'qcdht1500_2018': _fromnum1("/store/user/shogan/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleUL18V1Bm_2018/230112_154422", 57),
'qcdht2000_2018': _fromnum1("/store/user/shogan/QCD_HT2000toInf_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleUL18V1Bm_2018/230112_154435", 22),
'ttbar_2018': (157, ['/store/user/shogan/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleUL18V1Bm_2018/230111_185645/0000/ntuple_%i.root' % i for i in chain(xrange(1,5), xrange(6,10), xrange(12,161))]),


# 2016 RPV Signal Samples

# 2017 RPV Signal Samples
'mfv_neu_tau000100um_M0200_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-200_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/230110_181407", 29),
'mfv_neu_tau000300um_M0200_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-200_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/230110_181421", 25),
'mfv_neu_tau010000um_M0200_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-200_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/230110_181435", 5),
'mfv_neu_tau030000um_M0200_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-200_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/230110_181449", 9),
'mfv_neu_tau000100um_M0300_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/230110_181504", 31),
'mfv_neu_tau000300um_M0300_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/230110_181518", 25),
'mfv_neu_tau001000um_M0300_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/230110_181531", 9),
'mfv_neu_tau010000um_M0300_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/230110_181546", 5),
'mfv_neu_tau030000um_M0300_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/230110_181600", 7),
'mfv_neu_tau000100um_M0400_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/230110_181615", 33),
'mfv_neu_tau001000um_M0400_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/230110_181629", 9),
'mfv_neu_tau010000um_M0400_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/230110_181643", 5),
'mfv_neu_tau030000um_M0400_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/230110_181657", 9),
'mfv_neu_tau000100um_M0600_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/230110_181712", 18),
'mfv_neu_tau000300um_M0600_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/230110_181727", 14),
'mfv_neu_tau001000um_M0600_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/230110_181741", 6),
'mfv_neu_tau030000um_M0600_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/230110_181809", 6),
'mfv_neu_tau000300um_M0800_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/230110_181823", 11),
'mfv_neu_tau001000um_M0800_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/230110_181839", 4),
'mfv_neu_tau010000um_M0800_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/230110_181853", 3),
'mfv_neu_tau030000um_M0800_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/230110_181907", 3),
'mfv_neu_tau000100um_M1200_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/230110_181921", 28),
'mfv_neu_tau000300um_M1200_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/230110_181934", 10),
'mfv_neu_tau001000um_M1200_2017': (3, ['/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/230110_181949/0000/ntuple_%i.root' % i for i in chain(xrange(3,5), [1])]),
'mfv_neu_tau010000um_M1200_2017': (1, ['/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/230110_182003/0000/ntuple_2.root']),
'mfv_neu_tau030000um_M1200_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/230110_182017", 3),
'mfv_neu_tau000100um_M1600_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/230110_182031", 29),
'mfv_neu_tau000300um_M1600_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/230110_182045", 11),
'mfv_neu_tau001000um_M1600_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/230110_182102", 3),
'mfv_neu_tau010000um_M1600_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/230110_182116", 2),
'mfv_neu_tau030000um_M1600_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/230110_182130", 3),
'mfv_neu_tau000100um_M3000_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/230110_182144", 17),
'mfv_neu_tau000300um_M3000_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/230110_182158", 9),
'mfv_neu_tau030000um_M3000_2017': (1, ['/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/230110_182241/0000/ntuple_3.root']),
'mfv_stopdbardbar_tau000100um_M0200_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-200_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/230113_184547", 34),
'mfv_stopdbardbar_tau000300um_M0200_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-200_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/230113_184601", 33),
'mfv_stopdbardbar_tau001000um_M0200_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-200_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/230113_184615", 10),
'mfv_stopdbardbar_tau010000um_M0200_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-200_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/230113_184628", 5),
'mfv_stopdbardbar_tau000100um_M0300_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-300_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/230113_184656", 32),
'mfv_stopdbardbar_tau000300um_M0300_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-300_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/230113_184710", 34),
'mfv_stopdbardbar_tau001000um_M0300_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-300_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/230113_184726", 10),
'mfv_stopdbardbar_tau010000um_M0300_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-300_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/230113_184740", 5),
'mfv_stopdbardbar_tau030000um_M0300_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-300_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/230113_184754", 7),
'mfv_stopdbardbar_tau000100um_M0400_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-400_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/230113_184808", 31),
'mfv_stopdbardbar_tau000300um_M0400_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-400_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/230113_184822", 34),
'mfv_stopdbardbar_tau001000um_M0400_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-400_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/230113_184836", 10),
'mfv_stopdbardbar_tau010000um_M0400_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-400_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/230113_184850", 5),
'mfv_stopdbardbar_tau030000um_M0400_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-400_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/230113_184904", 7),
'mfv_stopdbardbar_tau000100um_M0600_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-600_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/230113_184918", 34),
'mfv_stopdbardbar_tau000300um_M0600_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-600_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/230113_184932", 27),
'mfv_stopdbardbar_tau010000um_M0600_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-600_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/230113_184946", 4),
'mfv_stopdbardbar_tau000100um_M0800_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-800_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/230113_185014", 35),
'mfv_stopdbardbar_tau000300um_M0800_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-800_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/230113_185027", 19),
'mfv_stopdbardbar_tau010000um_M0800_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-800_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/230113_185054", 5),
'mfv_stopdbardbar_tau030000um_M0800_2017': (5, ['/store/user/shogan/StopStopbarTo2Dbar2D_M-800_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/230113_185108/0000/ntuple_%i.root' % i for i in chain(xrange(3,7), [1])]),
'mfv_stopdbardbar_tau000100um_M1200_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-1200_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/230113_185123", 36),
'mfv_stopdbardbar_tau000300um_M1200_2017': (19, ['/store/user/shogan/StopStopbarTo2Dbar2D_M-1200_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/230113_185137/0000/ntuple_%i.root' % i for i in chain(xrange(1,17), xrange(18,21))]
),
'mfv_stopdbardbar_tau001000um_M1200_2017': (7, ['/store/user/shogan/StopStopbarTo2Dbar2D_M-1200_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/230113_185151/0000/ntuple_%i.root' % i for i in chain(xrange(3,9), [1])]),
'mfv_stopdbardbar_tau010000um_M1200_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-1200_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/230113_185205", 3),
'mfv_stopdbardbar_tau030000um_M1200_2017': _fromnum0("/store/user/shogan/StopStopbarTo2Dbar2D_M-1200_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/230113_185220", 3),
'mfv_stopdbardbar_tau000100um_M1600_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-1600_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/230113_185235", 33),
'mfv_stopdbardbar_tau001000um_M1600_2017': (2, ['/store/user/shogan/StopStopbarTo2Dbar2D_M-1600_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/230113_185249/0000/ntuple_%i.root' % i for i in [1, 3]]),
'mfv_stopdbardbar_tau030000um_M1600_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-1600_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/230113_185318", 5),
'mfv_stopdbardbar_tau000100um_M3000_2017': (32, ['/store/user/shogan/StopStopbarTo2Dbar2D_M-3000_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/230113_185332/0000/ntuple_%i.root' % i for i in chain(xrange(1,9), xrange(10,24), xrange(25,31), xrange(32,34), xrange(35,37))]),
'mfv_stopdbardbar_tau000300um_M3000_2017': (22, ['/store/user/shogan/StopStopbarTo2Dbar2D_M-3000_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/230113_185352/0000/ntuple_%i.root' % i for i in chain(xrange(1,3), xrange(4,24))]),
'mfv_stopdbardbar_tau010000um_M3000_2017': (1, ['/store/user/shogan/StopStopbarTo2Dbar2D_M-3000_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/230113_185424/0000/ntuple_5.root']),
'mfv_stopdbardbar_tau030000um_M3000_2017': (1, ['/store/user/shogan/StopStopbarTo2Dbar2D_M-3000_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL17V1Bm_NoEF_2017/230113_185439/0000/ntuple_3.root']),

# 2018 RPV Signal Samples
'mfv_neu_tau000100um_M0200_2018': (28, ['/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-200_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL18V1Bm_NoEF_2018/230110_175941/0000/ntuple_%i.root' % i for i in chain(xrange(1,6), xrange(7,30))]),
'mfv_neu_tau000300um_M0200_2018': (13, ['/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-200_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL18V1Bm_NoEF_2018/230110_175957/0000/ntuple_%i.root' % i for i in chain(xrange(1,6), xrange(7,15))]),
'mfv_neu_tau010000um_M0200_2018': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-200_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL18V1Bm_NoEF_2018/230110_180020", 6),
'mfv_neu_tau030000um_M0200_2018': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-200_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL18V1Bm_NoEF_2018/230110_180034", 11),
'mfv_neu_tau000100um_M0300_2018': (21, ['/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL18V1Bm_NoEF_2018/230110_180048/0000/ntuple_%i.root' % i for i in chain(xrange(1,4), xrange(5,23))]),
'mfv_neu_tau000300um_M0300_2018': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL18V1Bm_NoEF_2018/230110_180102", 23),
'mfv_neu_tau001000um_M0300_2018': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL18V1Bm_NoEF_2018/230110_180116", 8),
'mfv_neu_tau010000um_M0300_2018': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL18V1Bm_NoEF_2018/230110_180130", 4),
'mfv_neu_tau030000um_M0300_2018': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL18V1Bm_NoEF_2018/230110_180144", 6),
'mfv_neu_tau000100um_M0400_2018': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL18V1Bm_NoEF_2018/230110_180159", 34),
'mfv_neu_tau000300um_M0400_2018': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL18V1Bm_NoEF_2018/230110_180215", 28),
'mfv_neu_tau001000um_M0400_2018': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL18V1Bm_NoEF_2018/230110_180229", 7),
'mfv_neu_tau010000um_M0400_2018': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL18V1Bm_NoEF_2018/230110_180243", 6),
'mfv_neu_tau030000um_M0400_2018': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL18V1Bm_NoEF_2018/230110_180259", 14),
'mfv_neu_tau000100um_M0600_2018': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL18V1Bm_NoEF_2018/230110_180313", 24),
'mfv_neu_tau001000um_M0600_2018': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL18V1Bm_NoEF_2018/230110_180328", 4),
'mfv_neu_tau010000um_M0600_2018': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL18V1Bm_NoEF_2018/230110_180341", 4),
'mfv_neu_tau030000um_M0600_2018': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL18V1Bm_NoEF_2018/230110_180355", 6),
'mfv_neu_tau000100um_M0800_2018': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL18V1Bm_NoEF_2018/230110_180409", 34),
'mfv_neu_tau000300um_M0800_2018': _fromnum0("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL18V1Bm_NoEF_2018/230110_180423", 13),
'mfv_neu_tau001000um_M0800_2018': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL18V1Bm_NoEF_2018/230110_180438", 3),
'mfv_neu_tau010000um_M0800_2018': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL18V1Bm_NoEF_2018/230110_180452", 3),
'mfv_neu_tau030000um_M0800_2018': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL18V1Bm_NoEF_2018/230110_180506", 3),
'mfv_neu_tau000100um_M1200_2018': (25, ['/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL18V1Bm_NoEF_2018/230110_180521/0000/ntuple_%i.root' % i for i in chain(xrange(1,12), xrange(13,27))]),
'mfv_neu_tau000300um_M1200_2018': (9, ['/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL18V1Bm_NoEF_2018/230110_180535/0000/ntuple_%i.root' % i for i in chain(xrange(1,4), xrange(5,11))]),
'mfv_neu_tau001000um_M1200_2018': (4, ['/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL18V1Bm_NoEF_2018/230110_180550/0000/ntuple_%i.root' % i for i in chain(xrange(3,6), [1])]),
'mfv_neu_tau010000um_M1200_2018': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL18V1Bm_NoEF_2018/230110_180604", 2),
'mfv_neu_tau030000um_M1200_2018': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL18V1Bm_NoEF_2018/230110_180618", 3),
'mfv_neu_tau000100um_M1600_2018': (31, ['/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL18V1Bm_NoEF_2018/230110_180632/0000/ntuple_%i.root' % i for i in chain(xrange(3,33), [1])]),
'mfv_neu_tau000300um_M1600_2018': (9, ['/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL18V1Bm_NoEF_2018/230110_180646/0000/ntuple_%i.root' % i for i in chain(xrange(3,11), [1])]),
'mfv_neu_tau001000um_M1600_2018': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL18V1Bm_NoEF_2018/230110_180701", 4),
'mfv_neu_tau010000um_M1600_2018': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL18V1Bm_NoEF_2018/230110_180716", 2),
'mfv_neu_tau030000um_M1600_2018': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL18V1Bm_NoEF_2018/230110_180730", 2),
'mfv_neu_tau000100um_M3000_2018': (29, ['/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL18V1Bm_NoEF_2018/230110_180743/0000/ntuple_%i.root' % i for i in chain(xrange(1,8), xrange(9,31))]),
'mfv_neu_tau000300um_M3000_2018': (9, ['/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL18V1Bm_NoEF_2018/230110_180757/0000/ntuple_%i.root' % i for i in chain(xrange(1,4), xrange(8,13), [6])]),
'mfv_stopdbardbar_tau000100um_M0200_2018': (32, ['/store/user/shogan/StopStopbarTo2Dbar2D_M-200_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL18V1Bm_NoEF_2018/230110_175338/0000/ntuple_%i.root' % i for i in chain(xrange(1,5), xrange(7,35))]),
'mfv_stopdbardbar_tau000300um_M0200_2018': (31, ['/store/user/shogan/StopStopbarTo2Dbar2D_M-200_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL18V1Bm_NoEF_2018/230110_175352/0000/ntuple_%i.root' % i for i in chain(xrange(1,3), xrange(4,33))]),
'mfv_stopdbardbar_tau001000um_M0200_2018': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-200_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL18V1Bm_NoEF_2018/230110_175406", 9),
'mfv_stopdbardbar_tau030000um_M0200_2018': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-200_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL18V1Bm_NoEF_2018/230110_175421", 7),
'mfv_stopdbardbar_tau000300um_M0300_2018': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-300_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL18V1Bm_NoEF_2018/230110_175438", 13),
'mfv_stopdbardbar_tau001000um_M0300_2018': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-300_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL18V1Bm_NoEF_2018/230110_175452", 8),
'mfv_stopdbardbar_tau010000um_M0300_2018': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-300_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL18V1Bm_NoEF_2018/230110_175507", 5),
'mfv_stopdbardbar_tau030000um_M0300_2018': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-300_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL18V1Bm_NoEF_2018/230110_175521", 7),
'mfv_stopdbardbar_tau001000um_M0400_2018': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-400_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL18V1Bm_NoEF_2018/230110_175535", 9),
'mfv_stopdbardbar_tau001000um_M0600_2018': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-600_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL18V1Bm_NoEF_2018/230110_175549", 7),
'mfv_stopdbardbar_tau030000um_M0600_2018': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-600_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL18V1Bm_NoEF_2018/230110_175618", 7),
'mfv_stopdbardbar_tau000100um_M0800_2018': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-800_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL18V1Bm_NoEF_2018/230110_175633", 32),
'mfv_stopdbardbar_tau000300um_M0800_2018': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-800_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL18V1Bm_NoEF_2018/230110_175647", 17),
'mfv_stopdbardbar_tau030000um_M0800_2018': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-800_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL18V1Bm_NoEF_2018/230110_175701", 5),
'mfv_stopdbardbar_tau000100um_M1200_2018': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-1200_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL18V1Bm_NoEF_2018/230110_175715", 31),
'mfv_stopdbardbar_tau000300um_M1200_2018': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-1200_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL18V1Bm_NoEF_2018/230110_175729", 15),
'mfv_stopdbardbar_tau010000um_M1200_2018': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-1200_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL18V1Bm_NoEF_2018/230110_175744", 3),
'mfv_stopdbardbar_tau030000um_M1200_2018': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-1200_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL18V1Bm_NoEF_2018/230110_175758", 4),
'mfv_stopdbardbar_tau000100um_M1600_2018': _fromnum0("/store/user/shogan/StopStopbarTo2Dbar2D_M-1600_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL18V1Bm_NoEF_2018/230110_175813", 31),
'mfv_stopdbardbar_tau000300um_M1600_2018': (10, ['/store/user/shogan/StopStopbarTo2Dbar2D_M-1600_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL18V1Bm_NoEF_2018/230110_175827/0000/ntuple_%i.root' % i for i in chain(xrange(2,4), xrange(5,7), xrange(8,12), xrange(13,15))]),
'mfv_stopdbardbar_tau010000um_M1600_2018': _fromnum0("/store/user/shogan/StopStopbarTo2Dbar2D_M-1600_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL18V1Bm_NoEF_2018/230110_175842", 2),
'mfv_stopdbardbar_tau030000um_M1600_2018': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-1600_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL18V1Bm_NoEF_2018/230110_175856", 4),
'mfv_stopdbardbar_tau000100um_M3000_2018': (16, ['/store/user/shogan/StopStopbarTo2Dbar2D_M-3000_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL18V1Bm_NoEF_2018/230110_175911/0000/ntuple_%i.root' % i for i in chain(xrange(9,24), [1])]),




# 2016 Exotic Higgs Samples

# 2017 Exotic Higgs Samples
'ggHToSSTodddd_tau1mm_M55_2017': _fromnum1("/store/user/shogan/ggH_HToSSTodddd_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/NtupleUL17V1Bm_NoEF_2017/230113_184504", 88),
'ggHToSSTodddd_tau10mm_M55_2017': _fromnum1("/store/user/shogan/ggH_HToSSTodddd_MH-125_MS-55_ctauS-10_TuneCP5_13TeV-powheg-pythia8/NtupleUL17V1Bm_NoEF_2017/230113_184519", 84),
'ggHToSSTodddd_tau100mm_M55_2017': _fromnum1("/store/user/shogan/ggH_HToSSTodddd_MH-125_MS-55_ctauS-100_TuneCP5_13TeV-powheg-pythia8/NtupleUL17V1Bm_NoEF_2017/230113_184533", 89),

# 2018 Exotic Higgs Samples

})

# These ntuples have extra track info, but also have an HT425 trigger applied. Used for studying displaced dijet track filters
_add_ds("ntupleul17v1bm", {
'ggHToSSTodddd_tau1mm_M55_2017': _fromnum1("/store/user/shogan/ggH_HToSSTodddd_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/NtupleUL17V2Bm_NoEF_2017/230105_171550", 89),
'ggHToSSTodddd_tau10mm_M55_2017': _fromnum1("/store/user/shogan/ggH_HToSSTodddd_MH-125_MS-55_ctauS-10_TuneCP5_13TeV-powheg-pythia8/NtupleUL17V2Bm_NoEF_2017/230105_171605", 84),
'ggHToSSTodddd_tau100mm_M55_2017': _fromnum1("/store/user/shogan/ggH_HToSSTodddd_MH-125_MS-55_ctauS-100_TuneCP5_13TeV-powheg-pythia8/NtupleUL17V2Bm_NoEF_2017/230105_171621", 90),
'qcdht0500_2017': _fromnum1("/store/user/shogan/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleUL17V2Bm_2017/230127_151653", 82),
'qcdht0700_2017': (216, ['/store/user/shogan/QCD_HT700to1000_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleUL17V2Bm_2017/230127_151705/0000/ntuple_%i.root' % i for i in chain(xrange(1,14), xrange(15,57), xrange(60,90), xrange(93,105), xrange(106,153), xrange(154,157), xrange(158,163), xrange(164,166), xrange(168,170), xrange(171,230), [91])]),
'qcdht1000_2017': _fromnum1("/store/user/shogan/QCD_HT1000to1500_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleUL17V2Bm_2017/230127_151719", 135),
'ttbar_2017': _fromnum1("/store/user/shogan/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleUL17V2Bm_2017/230126_154142", 1019),
})

# These ntuples have extra track info, more HLT calojet info, AND no HT425 trigger
_add_ds("ntupleul17v2bm", {
'ggHToSSTodddd_tau1mm_M55_2017': _fromnum1("/store/user/shogan/ggH_HToSSTodddd_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/NtupleUL17V1_extra_hltcaloBm_NoEF_2017/230120_223714", 88),
'ggHToSSTodddd_tau10mm_M55_2017': (82, ['/store/user/shogan/ggH_HToSSTodddd_MH-125_MS-55_ctauS-10_TuneCP5_13TeV-powheg-pythia8/NtupleUL17V1_extra_hltcaloBm_NoEF_2017/230120_223728/0000/ntuple_%i.root' % i for i in chain(xrange(1,15), xrange(16,69), xrange(70,85))]),
'ggHToSSTodddd_tau100mm_M55_2017': (86, ['/store/user/shogan/ggH_HToSSTodddd_MH-125_MS-55_ctauS-100_TuneCP5_13TeV-powheg-pythia8/NtupleUL17V1_extra_hltcaloBm_NoEF_2017/230120_223742/0000/ntuple_%i.root' % i for i in chain(xrange(1,58), xrange(59,62), xrange(63,67), xrange(68,90))]),
})

# Used to study some stuff for background template construction
_add_ds("ntupleulv1bm_ntkseeds", {
'qcdht0200_2017': _fromnum1("/store/user/shogan/QCD_HT200to300_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleUL17V1Bm_NTkSeeds_2017/221216_193901", 96, fnbase="ntkseeds"),
'qcdht0300_2017': (134, ['/store/user/shogan/QCD_HT300to500_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleUL17V1Bm_NTkSeeds_2017/221216_193914/0000/ntkseeds_%i.root' % i for i in chain(xrange(1,3), xrange(4,10), xrange(11,16), xrange(20,22), xrange(23,26), xrange(29,34), xrange(35,38), xrange(41,44), xrange(47,52), xrange(53,66), xrange(70,72), xrange(77,79), xrange(80,83), xrange(84,88), xrange(92,103), xrange(104,106), xrange(110,112), xrange(113,115), xrange(132,134), xrange(143,148), xrange(167,169), xrange(199,202), xrange(205,207), xrange(208,211), xrange(212,217), xrange(220,226), xrange(228,231), xrange(232,234), [17, 27, 39, 45, 67, 73, 90, 107, 122, 125, 136, 139, 141, 149, 151, 154, 159, 161, 164, 176, 179, 187, 189, 192, 194, 218])]),
'qcdht0500_2017': _fromnum1("/store/user/shogan/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleUL17V1Bm_NTkSeeds_2017/221216_193928", 82, fnbase="ntkseeds"),
'qcdht0700_2017': (225, ['/store/user/shogan/QCD_HT700to1000_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleUL17V1Bm_NTkSeeds_2017/221216_193942/0000/ntkseeds_%i.root' % i for i in chain(xrange(1,34), xrange(35,55), xrange(57,157), xrange(158,230))]),
'qcdht1000_2017': _fromnum1("/store/user/shogan/QCD_HT1000to1500_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleUL17V1Bm_NTkSeeds_2017/221216_193956", 135, fnbase="ntkseeds"),
'qcdht1500_2017': (235, ['/store/user/shogan/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraph-pythia8/NtupleUL17V1Bm_NTkSeeds_2017/221216_194009/0000/ntkseeds_%i.root' % i for i in chain(xrange(1,98), xrange(103,241))]),
'qcdht2000_2017': _fromnum1("/store/user/shogan/QCD_HT2000toInf_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleUL17V1Bm_NTkSeeds_2017/221216_194023", 186, fnbase="ntkseeds"),
'ttbar_2017': _fromnum1("/store/user/shogan/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleUL17V1Bm_NTkSeeds_2017/221216_193847", 1019, fnbase="ntkseeds"),

'qcdht0200_2018': (42, ['/store/user/shogan/QCD_HT200to300_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleUL18V1Bm_NTkSeeds_2018/230117_154236/0000/ntkseeds_%i.root' % i for i in chain(xrange(1,3), xrange(4,9), xrange(11,18), xrange(19,26), xrange(27,42), xrange(43,47), xrange(48,50))]),
'qcdht0200ext_2018': _fromnum1("/store/user/shogan/QCD_HT200to300_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleUL18V1Bm_NTkSeeds_2018/230117_154250", 83, fnbase="ntkseeds"),
'qcdht0300_2018': _fromnum1("/store/user/shogan/QCD_HT300to500_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleUL18V1Bm_NTkSeeds_2018/230117_154303", 26, fnbase="ntkseeds"),
'qcdht0500_2018': _fromnum1("/store/user/shogan/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleUL18V1Bm_NTkSeeds_2018/230117_154317", 27, fnbase="ntkseeds"),
'qcdht0700_2018': (5, ['/store/user/shogan/QCD_HT700to1000_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleUL18V1Bm_NTkSeeds_2018/230117_154330/0000/ntkseeds_%i.root' % i for i in chain(xrange(1,3), [14, 21, 23])]),
'qcdht1000_2018': (36, ['/store/user/shogan/QCD_HT1000to1500_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleUL18V1Bm_NTkSeeds_2018/230117_154343/0000/ntkseeds_%i.root' % i for i in chain(xrange(1,9), xrange(10,16), xrange(17,23), xrange(26,28), xrange(29,42), [24])]),
'qcdht1500_2018': _fromnum1("/store/user/shogan/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleUL18V1Bm_NTkSeeds_2018/230117_154356", 57, fnbase="ntkseeds"),
'qcdht2000_2018': _fromnum1("/store/user/shogan/QCD_HT2000toInf_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleUL18V1Bm_NTkSeeds_2018/230117_154410", 22, fnbase="ntkseeds"),
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
