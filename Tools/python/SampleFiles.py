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
    print(_d.keys())
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

_add_ds("ntupleulv1am", {
'mfv_neu_tau000100um_M0200_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-200_CTau-100um_TuneCP5_13TeV-pythia8/NtupleULV1Am_NoEF_2017/220418_171141", 33),
'mfv_neu_tau000300um_M0200_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-200_CTau-300um_TuneCP5_13TeV-pythia8/NtupleULV1Am_NoEF_2017/220418_171158", 28),
'mfv_neu_tau010000um_M0200_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-200_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleULV1Am_NoEF_2017/220418_171213", 7),
'mfv_neu_tau030000um_M0200_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-200_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleULV1Am_NoEF_2017/220418_171227", 9),
'mfv_neu_tau000100um_M0300_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-100um_TuneCP5_13TeV-pythia8/NtupleULV1Am_NoEF_2017/220418_171242", 37),
'mfv_neu_tau000300um_M0300_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-300um_TuneCP5_13TeV-pythia8/NtupleULV1Am_NoEF_2017/220418_171256", 27),
'mfv_neu_tau001000um_M0300_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleULV1Am_NoEF_2017/220418_171310", 11),
'mfv_neu_tau010000um_M0300_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleULV1Am_NoEF_2017/220418_171328", 5),
'mfv_neu_tau030000um_M0300_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleULV1Am_NoEF_2017/220418_171349", 12),
'mfv_neu_tau000100um_M0400_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-100um_TuneCP5_13TeV-pythia8/NtupleULV1Am_NoEF_2017/220418_171410", 36),
'mfv_neu_tau001000um_M0400_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleULV1Am_NoEF_2017/220418_171433", 9),
'mfv_neu_tau010000um_M0400_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleULV1Am_NoEF_2017/220418_171508", 5),
'mfv_neu_tau030000um_M0400_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleULV1Am_NoEF_2017/220418_171528", 9),
'mfv_neu_tau000100um_M0600_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-100um_TuneCP5_13TeV-pythia8/NtupleULV1Am_NoEF_2017/220418_171548", 34),
'mfv_neu_tau000300um_M0600_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-300um_TuneCP5_13TeV-pythia8/NtupleULV1Am_NoEF_2017/220418_171618", 18),
'mfv_neu_tau001000um_M0600_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleULV1Am_NoEF_2017/220418_171644", 7),
'mfv_neu_tau010000um_M0600_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleULV1Am_NoEF_2017/220418_171658", 3),
'mfv_neu_tau030000um_M0600_2017': _fromnum0("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleULV1Am_NoEF_2017/220418_171714", 5),
'mfv_neu_tau000300um_M0800_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-300um_TuneCP5_13TeV-pythia8/NtupleULV1Am_NoEF_2017/220418_171731", 18),
'mfv_neu_tau001000um_M0800_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleULV1Am_NoEF_2017/220418_171745", 4),
'mfv_neu_tau010000um_M0800_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleULV1Am_NoEF_2017/220418_171759", 4),
'mfv_neu_tau030000um_M0800_2017': (4, ['/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleULV1Am_NoEF_2017/220418_171814/0000/ntuple_%i.root' % i for i in chain(xrange(1,3), xrange(4,6))]),
'mfv_neu_tau000100um_M1200_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-100um_TuneCP5_13TeV-pythia8/NtupleULV1Am_NoEF_2017/220418_171828", 39),
'mfv_neu_tau000300um_M1200_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-300um_TuneCP5_13TeV-pythia8/NtupleULV1Am_NoEF_2017/220418_171842", 13),
'mfv_neu_tau001000um_M1200_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleULV1Am_NoEF_2017/220418_171856", 4),
'mfv_neu_tau010000um_M1200_2017': (1, ['/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleULV1Am_NoEF_2017/220418_171910/0000/ntuple_1.root']),
'mfv_neu_tau030000um_M1200_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleULV1Am_NoEF_2017/220418_171925", 3),
'mfv_neu_tau000100um_M1600_2017': (35, ['/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-100um_TuneCP5_13TeV-pythia8/NtupleULV1Am_NoEF_2017/220418_171941/0000/ntuple_%i.root' % i for i in chain(xrange(2,26), xrange(27,38))]),
'mfv_neu_tau000300um_M1600_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-300um_TuneCP5_13TeV-pythia8/NtupleULV1Am_NoEF_2017/220418_171955", 14),
'mfv_neu_tau001000um_M1600_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleULV1Am_NoEF_2017/220418_172008", 3),
'mfv_neu_tau010000um_M1600_2017': (2, ['/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleULV1Am_NoEF_2017/220418_172022/0000/ntuple_%i.root' % i for i in [1, 3]]),
'mfv_neu_tau030000um_M1600_2017': (3, ['/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleULV1Am_NoEF_2017/220418_172038/0000/ntuple_%i.root' % i for i in [1, 3, 5]]),
'mfv_neu_tau000100um_M3000_2017': (34, ['/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-100um_TuneCP5_13TeV-pythia8/NtupleULV1Am_NoEF_2017/220418_172052/0000/ntuple_%i.root' % i for i in chain(xrange(1,11), xrange(12,36))]),
'mfv_neu_tau000300um_M3000_2017': (13, ['/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-300um_TuneCP5_13TeV-pythia8/NtupleULV1Am_NoEF_2017/220418_172106/0000/ntuple_%i.root' % i for i in chain(xrange(1,13), [14])]),
'mfv_neu_tau030000um_M3000_2017': (1, ['/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleULV1Am_NoEF_2017/220418_172149/0000/ntuple_2.root']),
'mfv_stopdbardbar_tau000300um_M0300_2017': _fromnum0("/store/user/shogan/StopStopbarTo2Dbar2D_M-300_CTau-300um_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_2017/211208_143918", 40),
'mfv_stopdbardbar_tau001000um_M0300_2017': _fromnum0("/store/user/shogan/StopStopbarTo2Dbar2D_M-300_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_2017/211208_143921", 32),
'mfv_stopdbardbar_tau000300um_M0600_2017': _fromnum0("/store/user/shogan/StopStopbarTo2Dbar2D_M-600_CTau-300um_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_2017/211208_143919", 24),
'mfv_stopdbardbar_tau000300um_M0800_2017': _fromnum0("/store/user/shogan/StopStopbarTo2Dbar2D_M-800_CTau-300um_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_2017/211208_143920", 24),
'mfv_stopdbardbar_tau001000um_M0800_2017': _fromnum0("/store/user/shogan/StopStopbarTo2Dbar2D_M-800_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_2017/211208_143923", 40),
'mfv_stopbbarbbar_tau001000um_M0300_2017': _fromnum0("/store/user/shogan/StopStopbarTo2Bbar2B_M-300_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_2017/211208_143927", 40),
'mfv_stopbbarbbar_tau000300um_M0600_2017': _fromnum0("/store/user/shogan/StopStopbarTo2Bbar2B_M-600_CTau-300um_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_2017/211208_143925", 32),
'mfv_stopbbarbbar_tau001000um_M0600_2017': _fromnum0("/store/user/shogan/StopStopbarTo2Bbar2B_M-600_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_2017/211208_143928", 24),
'mfv_stopbbarbbar_tau000300um_M0800_2017': _fromnum0("/store/user/shogan/StopStopbarTo2Bbar2B_M-800_CTau-300um_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_2017/211208_143926", 24),
'mfv_stopbbarbbar_tau001000um_M0800_2017': _fromnum0("/store/user/shogan/StopStopbarTo2Bbar2B_M-800_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_2017/211208_143929", 32),
})

_add_ds("ntupleulv1bm", {
'mfv_neu_tau000100um_M0200_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-200_CTau-100um_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_195139", 32),
'mfv_neu_tau000300um_M0200_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-200_CTau-300um_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_195153", 26),
'mfv_neu_tau010000um_M0200_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-200_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_195207", 7),
'mfv_neu_tau030000um_M0200_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-200_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_195221", 9),
'mfv_neu_tau000100um_M0300_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-100um_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_195237", 35),
'mfv_neu_tau000300um_M0300_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-300um_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_195251", 26),
'mfv_neu_tau001000um_M0300_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_195306", 11),
'mfv_neu_tau010000um_M0300_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_195320", 5),
'mfv_neu_tau030000um_M0300_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_195333", 11),
'mfv_neu_tau000100um_M0400_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-100um_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_195348", 35),
'mfv_neu_tau001000um_M0400_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_195402", 9),
'mfv_neu_tau010000um_M0400_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_195416", 5),
'mfv_neu_tau030000um_M0400_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_195431", 9),
'mfv_neu_tau000100um_M0600_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-100um_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_195444", 32),
'mfv_neu_tau000300um_M0600_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-300um_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_195459", 18),
'mfv_neu_tau001000um_M0600_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_195513", 7),
'mfv_neu_tau010000um_M0600_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_195533", 3),
'mfv_neu_tau030000um_M0600_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_195547", 6),
'mfv_neu_tau000300um_M0800_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-300um_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_195606", 17),
'mfv_neu_tau001000um_M0800_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_195621", 4),
'mfv_neu_tau010000um_M0800_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_195635", 4),
'mfv_neu_tau030000um_M0800_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_195651", 5),
'mfv_neu_tau000100um_M1200_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-100um_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_195705", 38),
'mfv_neu_tau000300um_M1200_2017': (11, ['/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-300um_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_195720/0000/ntuple_%i.root' % i for i in chain(xrange(1,11), [12])]),
'mfv_neu_tau001000um_M1200_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_195734", 4),
'mfv_neu_tau010000um_M1200_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_195748", 2),
'mfv_neu_tau030000um_M1200_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_195802", 3),
'mfv_neu_tau000100um_M1600_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-100um_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_195817", 36),
'mfv_neu_tau000300um_M1600_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-300um_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_195831", 14),
'mfv_neu_tau001000um_M1600_2017': _fromnum0("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_195845", 2),
'mfv_neu_tau010000um_M1600_2017': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_195859", 2),
'mfv_neu_tau030000um_M1600_2017': (3, ['/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_195913/0000/ntuple_%i.root' % i for i in chain(xrange(1,3), [4])]),
'mfv_neu_tau000100um_M3000_2017': (28, ['/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-100um_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_195930/0000/ntuple_%i.root' % i for i in chain(xrange(3,9), xrange(13,34), [11])]),
'mfv_neu_tau000300um_M3000_2017': (12, ['/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-300um_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_195944/0000/ntuple_%i.root' % i for i in chain(xrange(1,3), xrange(4,14))]),
'mfv_neu_tau030000um_M3000_2017': (1, ['/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_200028/0000/ntuple_3.root']),
'mfv_stopdbardbar_tau000100um_M0200_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-200_CTau-100um_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_200043", 34),
'mfv_stopdbardbar_tau000300um_M0200_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-200_CTau-300um_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_200057", 33),
'mfv_stopdbardbar_tau001000um_M0200_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-200_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_200111", 13),
'mfv_stopdbardbar_tau010000um_M0200_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-200_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_200125", 5),
'mfv_stopdbardbar_tau030000um_M0200_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-200_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_200139", 7),
'mfv_stopdbardbar_tau000100um_M0300_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-300_CTau-100um_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_200154", 33),
'mfv_stopdbardbar_tau000300um_M0300_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-300_CTau-300um_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_200208", 35),
'mfv_stopdbardbar_tau001000um_M0300_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-300_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_200222", 11),
'mfv_stopdbardbar_tau010000um_M0300_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-300_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_200236", 5),
'mfv_stopdbardbar_tau030000um_M0300_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-300_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_200250", 7),
'mfv_stopdbardbar_tau000100um_M0400_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-400_CTau-100um_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_200305", 33),
'mfv_stopdbardbar_tau000300um_M0400_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-400_CTau-300um_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_200319", 35),
'mfv_stopdbardbar_tau001000um_M0400_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-400_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_200334", 10),
'mfv_stopdbardbar_tau010000um_M0400_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-400_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_200348", 5),
'mfv_stopdbardbar_tau030000um_M0400_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-400_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_200402", 7),
'mfv_stopdbardbar_tau000100um_M0600_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-600_CTau-100um_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_200417", 35),
'mfv_stopdbardbar_tau000300um_M0600_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-600_CTau-300um_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_200431", 29),
'mfv_stopdbardbar_tau010000um_M0600_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-600_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_200445", 5),
'mfv_stopdbardbar_tau030000um_M0600_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-600_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_200503", 5),
'mfv_stopdbardbar_tau000100um_M0800_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-800_CTau-100um_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_200518", 35),
'mfv_stopdbardbar_tau000300um_M0800_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-800_CTau-300um_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_200535", 19),
'mfv_stopdbardbar_tau001000um_M0800_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-800_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_200549", 5),
'mfv_stopdbardbar_tau010000um_M0800_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-800_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_200604", 5),
'mfv_stopdbardbar_tau030000um_M0800_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-800_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_200618", 6),
'mfv_stopdbardbar_tau000100um_M1200_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-1200_CTau-100um_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_200632", 37),
'mfv_stopdbardbar_tau000300um_M1200_2017': (20, ['/store/user/shogan/StopStopbarTo2Dbar2D_M-1200_CTau-300um_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_200646/0000/ntuple_%i.root' % i for i in chain(xrange(4,23), [2])]),
'mfv_stopdbardbar_tau001000um_M1200_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-1200_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_200700", 8),
'mfv_stopdbardbar_tau010000um_M1200_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-1200_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_200715", 3),
'mfv_stopdbardbar_tau030000um_M1200_2017': (1, ['/store/user/shogan/StopStopbarTo2Dbar2D_M-1200_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_200730/0000/ntuple_4.root']),
'mfv_stopdbardbar_tau000100um_M1600_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-1600_CTau-100um_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_200743", 36),
'mfv_stopdbardbar_tau001000um_M1600_2017': (1, ['/store/user/shogan/StopStopbarTo2Dbar2D_M-1600_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_200757/0000/ntuple_1.root']),
'mfv_stopdbardbar_tau010000um_M1600_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-1600_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_200812", 4),
'mfv_stopdbardbar_tau030000um_M1600_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-1600_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_200826", 5),
'mfv_stopdbardbar_tau000100um_M3000_2017': (37, ['/store/user/shogan/StopStopbarTo2Dbar2D_M-3000_CTau-100um_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_200841/0000/ntuple_%i.root' % i for i in chain(xrange(1,11), xrange(12,39))]),
'mfv_stopdbardbar_tau000300um_M3000_2017': (19, ['/store/user/shogan/StopStopbarTo2Dbar2D_M-3000_CTau-300um_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_200855/0000/ntuple_%i.root' % i for i in chain(xrange(1,8), xrange(10,17), xrange(18,22), [24])]),
'mfv_stopdbardbar_tau010000um_M3000_2017': (1, ['/store/user/shogan/StopStopbarTo2Dbar2D_M-3000_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_200923/0000/ntuple_5.root']),
'mfv_stopbbarbbar_tau000100um_M0200_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-200_CTau-100um_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_200952", 33),
'mfv_stopbbarbbar_tau000300um_M0200_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-200_CTau-300um_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_201006", 34),
'mfv_stopbbarbbar_tau001000um_M0200_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-200_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_201020", 11),
'mfv_stopbbarbbar_tau010000um_M0200_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-200_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_201034", 5),
'mfv_stopbbarbbar_tau030000um_M0200_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-200_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_201048", 8),
'mfv_stopbbarbbar_tau000100um_M0300_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-300_CTau-100um_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_201103", 34),
'mfv_stopbbarbbar_tau000300um_M0300_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-300_CTau-300um_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_201117", 32),
'mfv_stopbbarbbar_tau001000um_M0300_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-300_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_201131", 11),
'mfv_stopbbarbbar_tau010000um_M0300_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-300_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_201145", 5),
'mfv_stopbbarbbar_tau030000um_M0300_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-300_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_201200", 7),
'mfv_stopbbarbbar_tau000100um_M0400_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-400_CTau-100um_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_201215", 34),
'mfv_stopbbarbbar_tau000300um_M0400_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-400_CTau-300um_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_201232", 34),
'mfv_stopbbarbbar_tau001000um_M0400_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-400_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_201246", 10),
'mfv_stopbbarbbar_tau010000um_M0400_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-400_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_201303", 5),
'mfv_stopbbarbbar_tau030000um_M0400_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-400_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_201318", 7),
'mfv_stopbbarbbar_tau000100um_M0600_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-600_CTau-100um_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_201334", 33),
'mfv_stopbbarbbar_tau000300um_M0600_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-600_CTau-300um_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_201348", 27),
'mfv_stopbbarbbar_tau001000um_M0600_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-600_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_201403", 7),
'mfv_stopbbarbbar_tau010000um_M0600_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-600_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_201416", 3),
'mfv_stopbbarbbar_tau030000um_M0600_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-600_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_201432", 7),
'mfv_stopbbarbbar_tau000100um_M0800_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-800_CTau-100um_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_201446", 38),
'mfv_stopbbarbbar_tau000300um_M0800_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-800_CTau-300um_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_201500", 20),
'mfv_stopbbarbbar_tau001000um_M0800_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-800_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_201514", 9),
'mfv_stopbbarbbar_tau010000um_M0800_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-800_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_201528", 3),
'mfv_stopbbarbbar_tau030000um_M0800_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-800_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_201543", 6),
'mfv_stopbbarbbar_tau000100um_M1200_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-1200_CTau-100um_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_201558", 36),
'mfv_stopbbarbbar_tau000300um_M1200_2017': (18, ['/store/user/shogan/StopStopbarTo2Bbar2B_M-1200_CTau-300um_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_201614/0000/ntuple_%i.root' % i for i in chain(xrange(1,16), xrange(17,20))]),
'mfv_stopbbarbbar_tau001000um_M1200_2017': (4, ['/store/user/shogan/StopStopbarTo2Bbar2B_M-1200_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_203210/0000/ntuple_%i.root' % i for i in chain(xrange(1,3), xrange(4,6))]),
'mfv_stopbbarbbar_tau010000um_M1200_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-1200_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_204722", 3),
'mfv_stopbbarbbar_tau000300um_M1600_2017': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-1600_CTau-300um_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_211748", 16),
'mfv_stopbbarbbar_tau001000um_M1600_2017': (2, ['/store/user/shogan/StopStopbarTo2Bbar2B_M-1600_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_211803/0000/ntuple_%i.root' % i for i in [1, 4]]),
'mfv_stopbbarbbar_tau030000um_M1600_2017': (4, ['/store/user/shogan/StopStopbarTo2Bbar2B_M-1600_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_211824/0000/ntuple_%i.root' % i for i in chain(xrange(3,6), [1])]),
'mfv_stopbbarbbar_tau000100um_M3000_2017': (42, ['/store/user/shogan/StopStopbarTo2Bbar2B_M-3000_CTau-100um_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_211838/0000/ntuple_%i.root' % i for i in chain(xrange(1,21), xrange(22,44))]),
'mfv_stopbbarbbar_tau000300um_M3000_2017': (11, ['/store/user/shogan/StopStopbarTo2Bbar2B_M-3000_CTau-300um_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_211852/0000/ntuple_%i.root' % i for i in chain(xrange(2,4), xrange(6,8), xrange(14,18), xrange(19,22))]),
'mfv_stopbbarbbar_tau001000um_M3000_2017': (1, ['/store/user/shogan/StopStopbarTo2Bbar2B_M-3000_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_211910/0000/ntuple_3.root']),
'mfv_stopbbarbbar_tau030000um_M3000_2017': (1, ['/store/user/shogan/StopStopbarTo2Bbar2B_M-3000_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleULV1Bm_NoEF_2017/221003_211942/0000/ntuple_2.root']),
# 2018 UL Samples below this line
'mfv_neu_tau000100um_M0200_2018': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-200_CTau-100um_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_192949", 34),
'mfv_neu_tau000300um_M0200_2018': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-200_CTau-300um_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_193003", 26),
'mfv_neu_tau010000um_M0200_2018': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-200_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_193017", 6),
'mfv_neu_tau030000um_M0200_2018': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-200_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_193031", 11),
'mfv_neu_tau000100um_M0300_2018': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-100um_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_193045", 33),
'mfv_neu_tau000300um_M0300_2018': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-300um_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_193059", 25),
'mfv_neu_tau001000um_M0300_2018': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_193112", 11),
'mfv_neu_tau010000um_M0300_2018': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_193126", 6),
'mfv_neu_tau030000um_M0300_2018': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_193140", 13),
'mfv_neu_tau000100um_M0400_2018': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-100um_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_193155", 36),
'mfv_neu_tau000300um_M0400_2018': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-300um_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_193208", 31),
'mfv_neu_tau001000um_M0400_2018': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_193222", 7),
'mfv_neu_tau010000um_M0400_2018': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_193236", 6),
'mfv_neu_tau030000um_M0400_2018': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_193250", 14),
'mfv_neu_tau000100um_M0600_2018': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-100um_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_193304", 35),
'mfv_neu_tau001000um_M0600_2018': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_193318", 6),
'mfv_neu_tau010000um_M0600_2018': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_193331", 4),
'mfv_neu_tau030000um_M0600_2018': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_193345", 6),
'mfv_neu_tau000100um_M0800_2018': (37, ['/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-100um_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_193359/0000/ntuple_%i.root' % i for i in chain(xrange(1,25), xrange(26,39))]),
'mfv_neu_tau000300um_M0800_2018': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-300um_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_193414", 14),
'mfv_neu_tau001000um_M0800_2018': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_193427", 4),
'mfv_neu_tau010000um_M0800_2018': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_193441", 4),
'mfv_neu_tau030000um_M0800_2018': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_193455", 5),
'mfv_neu_tau000100um_M1200_2018': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-100um_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_193509", 40),
'mfv_neu_tau000300um_M1200_2018': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-300um_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_193523", 13),
'mfv_neu_tau001000um_M1200_2018': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_193537", 7),
'mfv_neu_tau010000um_M1200_2018': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_193551", 4),
'mfv_neu_tau030000um_M1200_2018': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_193604", 6),
'mfv_neu_tau000100um_M1600_2018': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-100um_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_193618", 34),
'mfv_neu_tau000300um_M1600_2018': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-300um_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_193633", 12),
'mfv_neu_tau001000um_M1600_2018': _fromnum0("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_193646", 4),
'mfv_neu_tau010000um_M1600_2018': _fromnum0("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_193700", 3),
'mfv_neu_tau030000um_M1600_2018': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_193713", 4),
'mfv_neu_tau000100um_M3000_2018': (38, ['/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-100um_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_193727/0000/ntuple_%i.root' % i for i in chain(xrange(1,18), xrange(19,40))]),
'mfv_neu_tau000300um_M3000_2018': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-300um_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_193741", 12),
'mfv_neu_tau010000um_M3000_2018': (1, ['/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_193809/0000/ntuple_2.root']),
'mfv_stopdbardbar_tau000100um_M0200_2018': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-200_CTau-100um_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_193836", 38),
'mfv_stopdbardbar_tau000300um_M0200_2018': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-200_CTau-300um_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_193851", 36),
'mfv_stopdbardbar_tau001000um_M0200_2018': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-200_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_193904", 9),
'mfv_stopdbardbar_tau030000um_M0200_2018': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-200_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_193918", 7),
'mfv_stopdbardbar_tau000300um_M0300_2018': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-300_CTau-300um_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_193931", 31),
'mfv_stopdbardbar_tau001000um_M0300_2018': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-300_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_193945", 8),
'mfv_stopdbardbar_tau010000um_M0300_2018': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-300_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_194104", 5),
'mfv_stopdbardbar_tau030000um_M0300_2018': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-300_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_194118", 7),
'mfv_stopdbardbar_tau001000um_M0400_2018': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-400_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_194132", 10),
'mfv_stopdbardbar_tau001000um_M0600_2018': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-600_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_194145", 9),
'mfv_stopdbardbar_tau010000um_M0600_2018': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-600_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_194159", 3),
'mfv_stopdbardbar_tau030000um_M0600_2018': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-600_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_194214", 8),
'mfv_stopdbardbar_tau000100um_M0800_2018': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-800_CTau-100um_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_194229", 34),
'mfv_stopdbardbar_tau000300um_M0800_2018': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-800_CTau-300um_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_194243", 17),
'mfv_stopdbardbar_tau030000um_M0800_2018': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-800_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_194257", 7),
'mfv_stopdbardbar_tau000100um_M1200_2018': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-1200_CTau-100um_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_194310", 34),
'mfv_stopdbardbar_tau000300um_M1200_2018': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-1200_CTau-300um_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_194324", 15),
'mfv_stopdbardbar_tau010000um_M1200_2018': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-1200_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_194339", 3),
'mfv_stopdbardbar_tau030000um_M1200_2018': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-1200_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_194353", 4),
'mfv_stopdbardbar_tau000100um_M1600_2018': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-1600_CTau-100um_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_194407", 35),
'mfv_stopdbardbar_tau000300um_M1600_2018': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-1600_CTau-300um_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_194421", 14),
'mfv_stopdbardbar_tau010000um_M1600_2018': _fromnum0("/store/user/shogan/StopStopbarTo2Dbar2D_M-1600_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_194435", 2),
'mfv_stopdbardbar_tau030000um_M1600_2018': _fromnum0("/store/user/shogan/StopStopbarTo2Dbar2D_M-1600_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_194450", 3),
'mfv_stopdbardbar_tau000100um_M3000_2018': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-3000_CTau-100um_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_194503", 32),
'mfv_stopbbarbbar_tau000100um_M0200_2018': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-200_CTau-100um_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_194530", 37),
'mfv_stopbbarbbar_tau000300um_M0200_2018': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-200_CTau-300um_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_194544", 36),
'mfv_stopbbarbbar_tau001000um_M0200_2018': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-200_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_194559", 11),
'mfv_stopbbarbbar_tau010000um_M0200_2018': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-200_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_194613", 6),
'mfv_stopbbarbbar_tau030000um_M0200_2018': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-200_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_194627", 9),
'mfv_stopbbarbbar_tau000100um_M0300_2018': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-300_CTau-100um_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_194641", 35),
'mfv_stopbbarbbar_tau000300um_M0300_2018': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-300_CTau-300um_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_194655", 34),
'mfv_stopbbarbbar_tau001000um_M0300_2018': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-300_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_194709", 12),
'mfv_stopbbarbbar_tau010000um_M0300_2018': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-300_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_194723", 7),
'mfv_stopbbarbbar_tau030000um_M0300_2018': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-300_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_194736", 7),
'mfv_stopbbarbbar_tau000100um_M0400_2018': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-400_CTau-100um_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_194750", 35),
'mfv_stopbbarbbar_tau000300um_M0400_2018': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-400_CTau-300um_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_194803", 32),
'mfv_stopbbarbbar_tau001000um_M0400_2018': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-400_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_194818", 11),
'mfv_stopbbarbbar_tau010000um_M0400_2018': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-400_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_194832", 5),
'mfv_stopbbarbbar_tau030000um_M0400_2018': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-400_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_194846", 8),
'mfv_stopbbarbbar_tau000100um_M0600_2018': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-600_CTau-100um_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_194859", 31),
'mfv_stopbbarbbar_tau000300um_M0600_2018': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-600_CTau-300um_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_194913", 28),
'mfv_stopbbarbbar_tau001000um_M0600_2018': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-600_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_194928", 7),
'mfv_stopbbarbbar_tau010000um_M0600_2018': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-600_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_194941", 6),
'mfv_stopbbarbbar_tau030000um_M0600_2018': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-600_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_194956", 5),
'mfv_stopbbarbbar_tau000100um_M0800_2018': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-800_CTau-100um_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_195009", 34),
'mfv_stopbbarbbar_tau000300um_M0800_2018': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-800_CTau-300um_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_195023", 22),
'mfv_stopbbarbbar_tau010000um_M0800_2018': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-800_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_195039", 3),
'mfv_stopbbarbbar_tau030000um_M0800_2018': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-800_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_195052", 5),
'mfv_stopbbarbbar_tau000100um_M1200_2018': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-1200_CTau-100um_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_195106", 35),
'mfv_stopbbarbbar_tau000300um_M1200_2018': (19, ['/store/user/shogan/StopStopbarTo2Bbar2B_M-1200_CTau-300um_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_195120/0000/ntuple_%i.root' % i for i in chain(xrange(1,8), xrange(9,21))]),
'mfv_stopbbarbbar_tau001000um_M1200_2018': (6, ['/store/user/shogan/StopStopbarTo2Bbar2B_M-1200_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_195133/0000/ntuple_%i.root' % i for i in chain(xrange(3,8), [1])]),
'mfv_stopbbarbbar_tau010000um_M1200_2018': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-1200_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_195148", 3),
'mfv_stopbbarbbar_tau030000um_M1200_2018': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-1200_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_195202", 5),
'mfv_stopbbarbbar_tau000100um_M1600_2018': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-1600_CTau-100um_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_195215", 29),
'mfv_stopbbarbbar_tau000300um_M1600_2018': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-1600_CTau-300um_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_195229", 19),
'mfv_stopbbarbbar_tau001000um_M1600_2018': _fromnum0("/store/user/shogan/StopStopbarTo2Bbar2B_M-1600_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_195242", 5),
'mfv_stopbbarbbar_tau010000um_M1600_2018': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-1600_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_195257", 3),
'mfv_stopbbarbbar_tau030000um_M1600_2018': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-1600_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_195311", 6),
'mfv_stopbbarbbar_tau000100um_M3000_2018': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-3000_CTau-100um_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_195325", 38),
'mfv_stopbbarbbar_tau000300um_M3000_2018': (12, ['/store/user/shogan/StopStopbarTo2Bbar2B_M-3000_CTau-300um_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_195338/0000/ntuple_%i.root' % i for i in chain(xrange(1,5), xrange(10,18))]),
'mfv_stopbbarbbar_tau030000um_M3000_2018': (1, ['/store/user/shogan/StopStopbarTo2Bbar2B_M-3000_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleULV1_keeptkBm_NoEF_2017/220929_195420/0000/ntuple_3.root']),
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
