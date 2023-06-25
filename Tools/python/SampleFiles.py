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

def _fromnum2(path, n, but=[], fnbase='ntuple', add=[], numbereddirs=True): # messed up crab job 
    l = _fromnumlist(path, xrange(2,n+1), but, fnbase, add, numbereddirs)
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
    return [('root://cmsxrootd.fnal.gov/' + fn) if fn.startswith('/store/user') else fn for fn in fns]
    #return [('root://cmsxrootd.hep.wisc.edu/' + fn) if fn.startswith('/store/user') else fn for fn in fns]

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

_add_ds("miniaod",{
    'qcdmupt15_2017': (1, ['/store/mc/RunIISummer20UL17MiniAOD/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/100000/034AE4F2-7180-7F40-81D6-740D15738CBA.root'])
})

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
  'mfv_stopdbardbar_tau000300um_M0300_2017':_fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-300_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL17_MiniAOD/211207_195420/0000", 5, fnbase="MiniAOD", numbereddirs=False),
  'mfv_stopdbardbar_tau000300um_M0600_2017':_fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-600_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL17_MiniAOD/211207_195446/0000", 3, fnbase="MiniAOD", numbereddirs=False),
  'mfv_stopdbardbar_tau000300um_M0800_2017':_fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-800_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL17_MiniAOD/211207_195509/0000", 3, fnbase="MiniAOD", numbereddirs=False),
  'mfv_stopdbardbar_tau001000um_M0300_2017':_fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-300_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL17_MiniAOD/211207_195532/0000", 4, fnbase="MiniAOD", numbereddirs=False),
  'mfv_stopdbardbar_tau001000um_M0600_2017':_fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-600_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL17_MiniAOD/211207_195557/0000", 4, fnbase="MiniAOD", numbereddirs=False),
  'mfv_stopdbardbar_tau001000um_M0800_2017':_fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-800_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL17_MiniAOD/211207_195620/0000", 5, fnbase="MiniAOD", numbereddirs=False),
  'mfv_stopbbarbbar_tau000300um_M0300_2017':_fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-300_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL17_MiniAOD/211207_194958/0000", 3, fnbase="MiniAOD", numbereddirs=False),
  'mfv_stopbbarbbar_tau000300um_M0600_2017':_fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-600_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL17_MiniAOD/211207_195021/0000", 4, fnbase="MiniAOD", numbereddirs=False),
  'mfv_stopbbarbbar_tau000300um_M0800_2017':_fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-800_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL17_MiniAOD/211207_195045/0000", 3, fnbase="MiniAOD", numbereddirs=False),
  'mfv_stopbbarbbar_tau001000um_M0300_2017':_fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-300_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL17_MiniAOD/211207_195111/0000", 5, fnbase="MiniAOD", numbereddirs=False),
  'mfv_stopbbarbbar_tau001000um_M0600_2017':_fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-600_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL17_MiniAOD/211207_195334/0000", 3, fnbase="MiniAOD", numbereddirs=False),
  'mfv_stopbbarbbar_tau001000um_M0800_2017':_fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-800_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL17_MiniAOD/211207_195357/0000", 4, fnbase="MiniAOD", numbereddirs=False),

})

_add_ds("miniaod", {
    'mfv_stopld_tau000100um_M0200_2018':_fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_0p1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18_MiniAOD/220518_074408/0000", 5, fnbase="MiniAOD", numbereddirs=False),
    'mfv_stopld_tau000300um_M0200_2018':_fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_0p3mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18_MiniAOD/220518_074523/0000", 10, fnbase="MiniAOD", numbereddirs=False),
    'mfv_stopld_tau000100um_M0600_2018':_fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_0p1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18_MiniAOD/220518_074432/0000", 5, fnbase="MiniAOD", numbereddirs=False),
    'mfv_stopld_tau000300um_M0600_2018':_fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_0p3mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18_MiniAOD/220518_074542/0000", 5, fnbase="MiniAOD", numbereddirs=False),
    'mfv_stopld_tau000100um_M1000_2018':_fromnum2("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_0p1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18_MiniAOD/220518_074449/0000", 5, fnbase="MiniAOD", numbereddirs=False),
    'mfv_stopld_tau000300um_M1000_2018':_fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_0p3mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18_MiniAOD/220518_074558/0000", 5, fnbase="MiniAOD", numbereddirs=False),
    'mfv_stopld_tau001000um_M1000_2018':_fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18_MiniAOD/220518_073950/0000", 5, fnbase="MiniAOD", numbereddirs=False),
    'mfv_stopld_tau000100um_M1600_2018':_fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_0p1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18_MiniAOD/220518_074506/0000", 5, fnbase="MiniAOD", numbereddirs=False),
    'mfv_stopld_tau000300um_M1600_2018':_fromnum2("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_0p3mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18_MiniAOD/220518_074615/0000", 5, fnbase="MiniAOD", numbereddirs=False),
})

# private samples 
# _add_ds("ntupleulv1lepm", {
# 'mfv_stopld_tau000100um_M0200_2018': _fromnum0("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_0p1mm_TuneCP5_13TeV-pythia8/NtupleULV1Lepm_2018/220523_063334", 21),
# 'mfv_stopld_tau000300um_M0200_2018': _fromnum0("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_0p3mm_TuneCP5_13TeV-pythia8/NtupleULV1Lepm_2018/220523_063335", 21),
# 'mfv_stopld_tau000100um_M0600_2018': _fromnum0("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_0p1mm_TuneCP5_13TeV-pythia8/NtupleULV1Lepm_2018/220523_063336", 15),
# 'mfv_stopld_tau000300um_M0600_2018': _fromnum0("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_0p3mm_TuneCP5_13TeV-pythia8/NtupleULV1Lepm_2018/220523_063337", 15),
# 'mfv_stopld_tau000100um_M1000_2018': _fromnum0("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_0p1mm_TuneCP5_13TeV-pythia8/NtupleULV1Lepm_2018/220523_093252", 11),
# 'mfv_stopld_tau000300um_M1000_2018': _fromnum0("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_0p3mm_TuneCP5_13TeV-pythia8/NtupleULV1Lepm_2018/220523_063339", 14),
# 'mfv_stopld_tau001000um_M1000_2018': _fromnum0("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_0p1mm_TuneCP5_13TeV-pythia8/NtupleULV1Lepm_2018/220523_063340", 13),
# 'mfv_stopld_tau000100um_M1600_2018': _fromnum0("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_0p1mm_TuneCP5_13TeV-pythia8/NtupleULV1Lepm_2018/220523_063341", 12),
# 'mfv_stopld_tau000300um_M1600_2018': _fromnum0("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_0p3mm_TuneCP5_13TeV-pythia8/NtupleULV1Lepm_2018/220523_093256", 10),
# })


_add_ds("ntupleulv27lepm", {
'qcdempt015_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV27Lepm_2017/230320_183558", 24),
'qcdmupt15_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/NtupleULV27Lepm_2017/230320_183614", 77),
'qcdempt020_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV27Lepm_2017/230320_183627", 61),
'qcdempt030_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV27Lepm_2017/230320_183639", 26),
'qcdempt050_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV27Lepm_2017/230320_183652", 29),
'qcdempt080_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV27Lepm_2017/230320_183705", 23),
'qcdempt120_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV27Lepm_2017/230320_183718", 31),
'qcdempt170_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV27Lepm_2017/230320_183730", 16),
'qcdempt300_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV27Lepm_2017/230320_183744", 13),
'qcdbctoept020_2017': _fromnum1("/store/user/pekotamn/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/NtupleULV27Lepm_2017/230320_183759", 37),
'qcdbctoept030_2017': _fromnum1("/store/user/pekotamn/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/NtupleULV27Lepm_2017/230320_183813", 34),
'qcdbctoept080_2017': _fromnum1("/store/user/pekotamn/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/NtupleULV27Lepm_2017/230320_183826", 32),
'qcdbctoept170_2017': _fromnum1("/store/user/pekotamn/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/NtupleULV27Lepm_2017/230320_183842", 35),
'qcdbctoept250_2017': _fromnum1("/store/user/pekotamn/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/NtupleULV27Lepm_2017/230320_183856", 30),
#'wjetstolnu_2017': _fromnum1("/store/user/pekotamn/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV27Lepm_2017/230320_183912", 132),
#'dyjetstollM10_2017': _fromnum1("/store/user/pekotamn/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV27Lepm_2017/230320_183924", 125),
'wjetstolnu_2017': (130, ['/store/user/pekotamn/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV27Lepm_2017/230320_183912/0000/ntuple_%i.root' % i for i in chain(xrange(1,45), xrange(47,133))]),
'dyjetstollM10_2017': (124, ['/store/user/pekotamn/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV27Lepm_2017/230320_183924/0000/ntuple_%i.root' % i for i in chain(xrange(1,45), xrange(46,126))]),
'dyjetstollM50_2017': _fromnum1("/store/user/pekotamn/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV27Lepm_2017/230320_183938", 137),
'ttbar_2017': (1015, ['/store/user/pkotamni/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleULV27Lepm_2017/230320_134018' + '/%04i/ntuple_%i.root' % (i/1000,i) for i in chain(xrange(37), xrange(40,49), xrange(52,55), xrange(57,62), xrange(64,67), xrange(68,70), xrange(71,76), xrange(80,82), xrange(89,92), xrange(93,99), xrange(117,119), xrange(129,134), xrange(195,199), xrange(210,218), xrange(235,240), xrange(254,258), xrange(265,268), xrange(281,283), xrange(292,296), xrange(305,307), xrange(326,328), xrange(339,343), xrange(364,366), xrange(396,401), xrange(423,431), xrange(439,443), xrange(455,457), xrange(541,543), xrange(583,585), xrange(703,721), xrange(731,751), xrange(763,820), xrange(830,835), xrange(845,849), xrange(868,932), xrange(942,946), xrange(969,974), xrange(984,986), xrange(997,1000), xrange(1009,1012), [38, 50, 78, 86, 100, 103, 105, 110, 120, 126, 136, 373, 476, 487, 501, 521, 552, 571, 626, 680, 752, 958])] + ['/store/user/pkotamni/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleULV27Lepm_2017/230320_144528' + '/%04i/ntuple_%i.root' % (i/1000,i) for i in chain(xrange(55,57), xrange(62,64), xrange(76,78), xrange(82,86), xrange(87,89), xrange(101,103), xrange(106,110), xrange(111,117), xrange(121,126), xrange(127,129), xrange(134,136), xrange(137,195), xrange(199,210), xrange(218,235), xrange(240,254), xrange(258,265), xrange(268,281), xrange(283,292), xrange(296,305), xrange(307,326), xrange(328,339), xrange(343,364), xrange(366,373), xrange(374,396), xrange(401,423), xrange(431,439), xrange(443,455), xrange(457,476), xrange(477,487), xrange(488,501), xrange(502,521), xrange(522,541), xrange(543,552), xrange(553,571), xrange(572,583), xrange(585,594), xrange(656,666), xrange(675,677), xrange(681,687), xrange(693,698), xrange(724,726), xrange(729,731), xrange(823,825), xrange(828,830), xrange(835,845), xrange(860,868), xrange(932,937), xrange(950,952), xrange(959,963), xrange(967,969), xrange(986,988), xrange(1002,1004), [37, 39, 49, 51, 67, 70, 79, 92, 99, 104, 119, 595, 607, 629, 649, 671, 673, 679, 691, 702, 721, 757, 761, 820, 849, 855, 947, 977, 981, 993, 1000, 1017])] + ['/store/user/pkotamni/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleULV27Lepm_2017/230320_211919' + '/%04i/ntuple_%i.root' % (i/1000,i) for i in chain(xrange(596,604), xrange(605,607), xrange(608,626), xrange(627,629), xrange(630,649), xrange(650,656), xrange(666,671), xrange(677,679), xrange(687,691), xrange(698,702), xrange(722,724), xrange(726,729), xrange(753,757), xrange(758,761), xrange(821,823), xrange(825,828), xrange(850,855), xrange(857,860), xrange(937,942), xrange(948,950), xrange(952,958), xrange(963,967), xrange(978,981), xrange(982,984), xrange(988,993), xrange(1004,1009), xrange(1012,1017), [594, 672, 674, 692, 751, 762, 946, 974, 976, 994, 996, 1001, 1018])]),
'ww_2017': _fromnum1("/store/user/pekotamn/WW_TuneCP5_13TeV-pythia8/NtupleULV27Lepm_2017/230320_183950", 30),
'zz_2017': _fromnum1("/store/user/pekotamn/WZ_TuneCP5_13TeV-pythia8/NtupleULV27Lepm_2017/230320_184003", 17),
'wz_2017': _fromnum1("/store/user/pekotamn/ZZ_TuneCP5_13TeV-pythia8/NtupleULV27Lepm_2017/230320_184017", 12),
'ZHToSSTodddd_tau1mm_M55_2017': _fromnum1("/store/user/pekotamn/ZH_HToSSTodddd_ZToLL_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/NtupleULV27Lepm_2017/230317_190147", 58),
'WplusHToSSTodddd_tau1mm_M55_2017': _fromnum1("/store/user/pekotamn/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/NtupleULV27Lepm_2017/230317_190242", 50),
'WminusHToSSTodddd_tau1mm_M55_2017': _fromnum1("/store/user/pekotamn/WminusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/NtupleULV27Lepm_2017/230317_190311", 50),
})

_add_ds("ntupleulv28lepm", {
'ZHToSSTodddd_tau1mm_M55_2017': _fromnum1("/store/user/pekotamn/ZH_HToSSTodddd_ZToLL_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/NtupleULV28Lepm_2017/230317_190548", 58),
'WplusHToSSTodddd_tau1mm_M55_2017': _fromnum1("/store/user/pekotamn/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/NtupleULV28Lepm_2017/230317_190521", 50),
'WminusHToSSTodddd_tau1mm_M55_2017': _fromnum1("/store/user/pekotamn/WminusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/NtupleULV28Lepm_2017/230317_190450", 50),
})

_add_ds("ntupleulsed2ndxyv29lepm", {
'qcdempt015_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULsed2ndxyV29Lepm_2017/230329_162640", 24),
'qcdmupt15_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/NtupleULsed2ndxyV29Lepm_2017/230329_162654", 69),
'qcdempt020_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULsed2ndxyV29Lepm_2017/230329_162707", 61),
'qcdempt030_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULsed2ndxyV29Lepm_2017/230329_162721", 26),
'qcdempt050_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULsed2ndxyV29Lepm_2017/230329_162734", 29),
'qcdempt080_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULsed2ndxyV29Lepm_2017/230329_162747", 23),
'qcdempt120_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULsed2ndxyV29Lepm_2017/230329_162800", 30),
'qcdempt170_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULsed2ndxyV29Lepm_2017/230329_162812", 16),
'qcdempt300_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULsed2ndxyV29Lepm_2017/230329_162826", 13),
'qcdbctoept020_2017': _fromnum1("/store/user/pekotamn/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/NtupleULsed2ndxyV29Lepm_2017/230329_162839", 37),
'qcdbctoept030_2017': _fromnum1("/store/user/pekotamn/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/NtupleULsed2ndxyV29Lepm_2017/230327_180203", 32),
'qcdbctoept080_2017': _fromnum1("/store/user/pekotamn/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/NtupleULsed2ndxyV29Lepm_2017/230329_162854", 32),
'qcdbctoept170_2017': _fromnum1("/store/user/pekotamn/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/NtupleULsed2ndxyV29Lepm_2017/230329_162906", 35),
'qcdbctoept250_2017': _fromnum1("/store/user/pekotamn/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/NtupleULsed2ndxyV29Lepm_2017/230327_180241", 30),
#'wjetstolnu_2017': _fromnum1("/store/user/pekotamn/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULsed2ndxyV29Lepm_2017/230327_180254", 132),
'wjetstolnu_2017': (129, ['/store/user/pekotamn/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULsed2ndxyV29Lepm_2017/230327_180254/0000/ntuple_%i.root' % i for i in chain(xrange(1,45), xrange(47,50), xrange(51, 133))]),
'dyjetstollM10_2017': (123, ['/store/user/pekotamn/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULsed2ndxyV29Lepm_2017/230327_180307/0000/ntuple_%i.root' % i for i in chain(xrange(1,45), xrange(46,56), xrange(57,126))]),
'dyjetstollM50_2017': _fromnum1("/store/user/pekotamn/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULsed2ndxyV29Lepm_2017/230327_180320", 137),
'ttbar_2017': _fromnum0("/store/user/pkotamni/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleULsed2ndxyV29Lepm_2017/230327_130401", 1019),
'ww_2017': _fromnum1("/store/user/pekotamn/WW_TuneCP5_13TeV-pythia8/NtupleULsed2ndxyV29Lepm_2017/230327_180332", 30),
'zz_2017': _fromnum1("/store/user/pekotamn/WZ_TuneCP5_13TeV-pythia8/NtupleULsed2ndxyV29Lepm_2017/230327_180345", 17),
'wz_2017': _fromnum1("/store/user/pekotamn/ZZ_TuneCP5_13TeV-pythia8/NtupleULsed2ndxyV29Lepm_2017/230327_180359", 12),
'mfv_stoplb_tau010000um_M0400_2017': _fromnum1("/store/user/pekotamn/DisplacedSUSY_stopToLBottom_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULsed2ndxyV29Lepm_2017/230406_032300", 201),
'mfv_stoplb_tau001000um_M0400_2017': _fromnum1("/store/user/pekotamn/DisplacedSUSY_stopToLBottom_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULsed2ndxyV29Lepm_2017/230406_032229", 201),
'mfv_stopld_tau010000um_M0400_2017': _fromnum1("/store/user/pekotamn/DisplacedSUSY_stopToLD_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULsed2ndxyV29Lepm_2017/230405_153917", 201),
'mfv_stopld_tau001000um_M0400_2017': _fromnum1("/store/user/pekotamn/DisplacedSUSY_stopToLD_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULsed2ndxyV29Lepm_2017/230406_032000", 199),
'ZHToSSTodddd_tau300um_M55_2017': _fromnum1("/store/user/pekotamn/ZH_HToSSTodddd_ZToLL_MH-125_MS-55_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/NtupleULsed2ndxyV29Lepm_2017/230330_184302", 50),
'WplusHToSSTodddd_tau30mm_M55_2017': _fromnum1("/store/user/pekotamn/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-30_TuneCP5_13TeV-powheg-pythia8/NtupleULsed2ndxyV29Lepm_2017/230405_153108", 48),
'WplusHToSSTodddd_tau1mm_M55_2017': _fromnum1("/store/user/pekotamn/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/NtupleULsed2ndxyV29Lepm_2017/230326_221217", 50),
'WplusHToSSTodddd_tau300um_M55_2017': _fromnum1("/store/user/pekotamn/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/NtupleULsed2ndxyV29Lepm_2017/230330_184208", 50),
'WminusHToSSTodddd_tau300um_M55_2017': _fromnum1("/store/user/pekotamn/WminusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/NtupleULsed2ndxyV29Lepm_2017/230330_184236", 48),
})


_add_ds("ntupleulsed4ndxyv29lepm", {
'mfv_stoplb_tau010000um_M0400_2017': _fromnum1("/store/user/pekotamn/DisplacedSUSY_stopToLBottom_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULsed4ndxyV29Lepm_2017/230407_145009", 201),
'mfv_stoplb_tau001000um_M0400_2017': _fromnum1("/store/user/pekotamn/DisplacedSUSY_stopToLBottom_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULsed4ndxyV29Lepm_2017/230407_144940", 201),
'mfv_stopld_tau010000um_M0400_2017': _fromnum1("/store/user/pekotamn/DisplacedSUSY_stopToLD_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULsed4ndxyV29Lepm_2017/230407_145033", 201),
'mfv_stopld_tau001000um_M0400_2017': _fromnum1("/store/user/pekotamn/DisplacedSUSY_stopToLD_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULsed4ndxyV29Lepm_2017/230407_145055", 199),
'ZHToSSTodddd_tau300um_M55_2017': _fromnum1("/store/user/pekotamn/ZH_HToSSTodddd_ZToLL_MH-125_MS-55_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/NtupleULsed4ndxyV29Lepm_2017/230407_144906", 50),
'WplusHToSSTodddd_tau30mm_M55_2017': _fromnum1("/store/user/pekotamn/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-30_TuneCP5_13TeV-powheg-pythia8/NtupleULsed4ndxyV29Lepm_2017/230407_144746", 48),
'WplusHToSSTodddd_tau1mm_M55_2017': _fromnum1("/store/user/pekotamn/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/NtupleULsed4ndxyV29Lepm_2017/230407_144814", 50),
'WplusHToSSTodddd_tau300um_M55_2017': _fromnum1("/store/user/pekotamn/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/NtupleULsed4ndxyV29Lepm_2017/230407_144839", 50),
})


_add_ds("ntupleulsed3p5ndxyv29lepm", {
'qcdempt015_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULsed3p5ndxyV29Lepm_2017/230428_010618", 16),
'qcdmupt15_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/NtupleULsed3p5ndxyV29Lepm_2017/230428_010635", 66),
'qcdempt020_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULsed3p5ndxyV29Lepm_2017/230428_010651", 49),
'qcdempt030_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULsed3p5ndxyV29Lepm_2017/230428_010708", 24),
'qcdempt050_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULsed3p5ndxyV29Lepm_2017/230428_010724", 27),
'qcdempt080_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULsed3p5ndxyV29Lepm_2017/230428_010742", 23),
'qcdempt120_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULsed3p5ndxyV29Lepm_2017/230428_010759", 29),
'qcdempt170_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULsed3p5ndxyV29Lepm_2017/230428_010816", 16),
'qcdempt300_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULsed3p5ndxyV29Lepm_2017/230428_010833", 12),
'qcdbctoept020_2017': _fromnum1("/store/user/pekotamn/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/NtupleULsed3p5ndxyV29Lepm_2017/230428_010850", 34),
'qcdbctoept030_2017': _fromnum1("/store/user/pekotamn/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/NtupleULsed3p5ndxyV29Lepm_2017/230428_010906", 33),
'qcdbctoept080_2017': _fromnum1("/store/user/pekotamn/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/NtupleULsed3p5ndxyV29Lepm_2017/230428_010922", 30),
'qcdbctoept170_2017': _fromnum1("/store/user/pekotamn/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/NtupleULsed3p5ndxyV29Lepm_2017/230428_010939", 31),
'qcdbctoept250_2017': _fromnum1("/store/user/pekotamn/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/NtupleULsed3p5ndxyV29Lepm_2017/230428_010958", 29),
'wjetstolnu_2017': _fromnum1("/store/user/pekotamn/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULsed3p5ndxyV29Lepm_2017/230428_011015", 129),
'dyjetstollM10_2017': _fromnum1("/store/user/pekotamn/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULsed3p5ndxyV29Lepm_2017/230428_011031", 123),
'dyjetstollM50_2017': _fromnum1("/store/user/pekotamn/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULsed3p5ndxyV29Lepm_2017/230428_011048", 136),
'ww_2017': _fromnum1("/store/user/pekotamn/WW_TuneCP5_13TeV-pythia8/NtupleULsed3p5ndxyV29Lepm_2017/230428_011107", 30),
'zz_2017': _fromnum1("/store/user/pekotamn/WZ_TuneCP5_13TeV-pythia8/NtupleULsed3p5ndxyV29Lepm_2017/230428_011123", 16),
'wz_2017': _fromnum1("/store/user/pekotamn/ZZ_TuneCP5_13TeV-pythia8/NtupleULsed3p5ndxyV29Lepm_2017/230428_011140", 11),
'WplusHToSSTodddd_tau30mm_M55_2017': _fromnum1("/store/user/pekotamn/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-30_TuneCP5_13TeV-powheg-pythia8/NtupleULsed3p5ndxyV29Lepm_2017/230428_010536", 48),
'WplusHToSSTodddd_tau300um_M55_2017': _fromnum1("/store/user/pekotamn/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/NtupleULsed3p5ndxyV29Lepm_2017/230428_010353", 50),
'ttbar_2017': _fromnum0("/store/user/pkotamni/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleULsed3p5ndxyLepm_2017/230502_193852", 593),
})


_add_ds("ntupleultrkattchsed4ndxyv29lepm", {
'qcdempt015_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULtrkattchsed4ndxyV29Lepm_2017/230428_030939", 16),
'qcdmupt15_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/NtupleULtrkattchsed4ndxyV29Lepm_2017/230428_030959", 65),
'qcdempt020_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULtrkattchsed4ndxyV29Lepm_2017/230428_031021", 49),
'qcdempt030_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULtrkattchsed4ndxyV29Lepm_2017/230428_031043", 24),
'qcdempt050_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULtrkattchsed4ndxyV29Lepm_2017/230428_031104", 27),
'qcdempt080_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULtrkattchsed4ndxyV29Lepm_2017/230428_031126", 23),
'qcdempt120_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULtrkattchsed4ndxyV29Lepm_2017/230428_031147", 29),
'qcdempt170_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULtrkattchsed4ndxyV29Lepm_2017/230428_031208", 16),
'qcdempt300_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULtrkattchsed4ndxyV29Lepm_2017/230428_031229", 12),
'qcdbctoept020_2017': _fromnum1("/store/user/pekotamn/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/NtupleULtrkattchsed4ndxyV29Lepm_2017/230428_031250", 34),
'qcdbctoept030_2017': _fromnum1("/store/user/pekotamn/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/NtupleULtrkattchsed4ndxyV29Lepm_2017/230428_031311", 33),
'qcdbctoept080_2017': _fromnum1("/store/user/pekotamn/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/NtupleULtrkattchsed4ndxyV29Lepm_2017/230428_031331", 30),
'qcdbctoept170_2017': _fromnum1("/store/user/pekotamn/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/NtupleULtrkattchsed4ndxyV29Lepm_2017/230428_031353", 31),
'qcdbctoept250_2017': _fromnum1("/store/user/pekotamn/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/NtupleULtrkattchsed4ndxyV29Lepm_2017/230428_031413", 29),
'wjetstolnu_2017': _fromnum1("/store/user/pekotamn/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULtrkattchsed4ndxyV29Lepm_2017/230428_031433", 129),
'dyjetstollM10_2017': _fromnum1("/store/user/pekotamn/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULtrkattchsed4ndxyV29Lepm_2017/230428_031455", 123),
'dyjetstollM50_2017': _fromnum1("/store/user/pekotamn/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULtrkattchsed4ndxyV29Lepm_2017/230428_031515", 136),
'ww_2017': _fromnum1("/store/user/pekotamn/WW_TuneCP5_13TeV-pythia8/NtupleULtrkattchsed4ndxyV29Lepm_2017/230428_031535", 30),
'zz_2017': _fromnum1("/store/user/pekotamn/WZ_TuneCP5_13TeV-pythia8/NtupleULtrkattchsed4ndxyV29Lepm_2017/230428_031557", 16),
'wz_2017': _fromnum1("/store/user/pekotamn/ZZ_TuneCP5_13TeV-pythia8/NtupleULtrkattchsed4ndxyV29Lepm_2017/230428_031617", 11),
'WplusHToSSTodddd_tau30mm_M55_2017': _fromnum1("/store/user/pekotamn/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-30_TuneCP5_13TeV-powheg-pythia8/NtupleULtrkattchsed4ndxyV29Lepm_2017/230428_031723", 48),
'WplusHToSSTodddd_tau300um_M55_2017': _fromnum1("/store/user/pekotamn/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/NtupleULtrkattchsed4ndxyV29Lepm_2017/230428_031800", 50),
'ttbar_2017': _fromnum0("/store/user/pkotamni/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleULtrkattchsed4ndxyLepm_2017/230502_193426", 593),
})

_add_ds("ntupleulv29lepm", {
'qcdempt015_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV29Lepm_2017/230318_133442", 24),
'qcdmupt15_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/NtupleULV29Lepm_2017/230318_133455", 77),
'qcdempt020_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV29Lepm_2017/230318_133508", 61),
'qcdempt030_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV29Lepm_2017/230318_133521", 26),
'qcdempt050_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV29Lepm_2017/230318_133533", 29),
'qcdempt080_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV29Lepm_2017/230318_133547", 23),
'qcdempt120_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV29Lepm_2017/230318_133559", 31),
'qcdempt170_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV29Lepm_2017/230318_133613", 16),
'qcdempt300_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV29Lepm_2017/230318_133626", 13),
'qcdbctoept020_2017': _fromnum1("/store/user/pekotamn/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/NtupleULV29Lepm_2017/230318_133638", 37),
'qcdbctoept030_2017': _fromnum1("/store/user/pekotamn/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/NtupleULV29Lepm_2017/230318_133652", 34),
'qcdbctoept080_2017': _fromnum1("/store/user/pekotamn/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/NtupleULV29Lepm_2017/230318_133704", 32),
'qcdbctoept170_2017': _fromnum1("/store/user/pekotamn/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/NtupleULV29Lepm_2017/230318_133717", 35),
'qcdbctoept250_2017': _fromnum1("/store/user/pekotamn/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/NtupleULV29Lepm_2017/230318_133730", 30),
'wjetstolnu_2017': (129, ['/store/user/pekotamn/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV29Lepm_2017/230318_133742/0000/ntuple_%i.root' % i for i in chain(xrange(1,45), xrange(47,50), xrange(51, 133))]),
'dyjetstollM10_2017': (123, ['/store/user/pekotamn/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV29Lepm_2017/230318_133755/0000/ntuple_%i.root' % i for i in chain(xrange(1,45), xrange(46,56), xrange(57,126))]),
'dyjetstollM50_2017': _fromnum1("/store/user/pekotamn/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV29Lepm_2017/230318_133808", 137),
#'ttbar_2017': _fromnum0("/store/user/pkotamni/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleULV29Lepm_2017/230318_083846", 1019),
'ttbar_2017': _fromnum0("/store/user/pkotamni/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleULmissedV29Lepm_2017/230502_193157", 593),
'ww_2017': _fromnum1("/store/user/pekotamn/WW_TuneCP5_13TeV-pythia8/NtupleULV29Lepm_2017/230318_133820", 30),
'zz_2017': _fromnum1("/store/user/pekotamn/WZ_TuneCP5_13TeV-pythia8/NtupleULV29Lepm_2017/230318_133833", 17),
'wz_2017': _fromnum1("/store/user/pekotamn/ZZ_TuneCP5_13TeV-pythia8/NtupleULV29Lepm_2017/230318_133845", 12),
'ZHToSSTodddd_tau1mm_M55_2017': _fromnum1("/store/user/pekotamn/ZH_HToSSTodddd_ZToLL_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/NtupleULV29Lepm_2017/230317_190651", 58),
'WplusHToSSTodddd_tau1mm_M55_2017': _fromnum1("/store/user/pekotamn/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/NtupleULV29Lepm_2017/230317_190756", 50),
'WminusHToSSTodddd_tau1mm_M55_2017': _fromnum1("/store/user/pekotamn/WminusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/NtupleULV29Lepm_2017/230317_190727", 50),
})




_add_ds("trackmoverulv30lepmv2", {
  'example_ttbar_2017': (69, ['/store/user/pkotamni/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/TrackMoverULV30LepMumv4_2017/230606_222604' + '/%04i/movedtree_%i.root' % (i/1000,i) for i in xrange(69)]),
})

_add_ds("trackmovermctruthulv30lepmumv3", {
'WplusHToSSTodddd_tau30mm_M55_2017': _fromnum1("/store/user/pekotamn/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-30_TuneCP5_13TeV-powheg-pythia8/TrackMoverMCTruthULV30LepMumv3_2017/230602_151351", 48, fnbase="mctruth"),
'WplusHToSSTodddd_tau1mm_M55_2017': _fromnum0("/store/user/pkotamni/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/TrackMoverMCTruthULV30LepMumv3/230601_201335", 250, fnbase="mctruth"),
'WplusHToSSTodddd_tau300um_M55_2017': _fromnum0("/store/user/pkotamni/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/TrackMoverMCTruthULV30LepMumv3/230601_201420", 250, fnbase="mctruth"),
})



_add_ds("trackmoverulv30lepmumv4", {
'qcdempt015_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv4_2017/230607_031929", 48, fnbase="movedtree"),
'qcdmupt15_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv4_2017/230607_031949", 156, fnbase="movedtree"),
'qcdempt020_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv4_2017/230607_032009", 103, fnbase="movedtree"),
'qcdempt030_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv4_2017/230607_032031", 69, fnbase="movedtree"),
'qcdempt050_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv4_2017/230607_032052", 76, fnbase="movedtree"),
'qcdempt080_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv4_2017/230607_032112", 69, fnbase="movedtree"),
'qcdempt120_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv4_2017/230607_032133", 87, fnbase="movedtree"),
'qcdempt170_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv4_2017/230607_032153", 37, fnbase="movedtree"),
'qcdempt300_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv4_2017/230607_032213", 24, fnbase="movedtree"),
'qcdbctoept020_2017': (92, ['/store/user/pekotamn/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/TrackMoverULV30LepMumv4_2017/230607_032233/0000/movedtree_%i.root' % i for i in chain(xrange(1,46), xrange(47,94))]),
'qcdbctoept030_2017': _fromnum1("/store/user/pekotamn/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/TrackMoverULV30LepMumv4_2017/230607_032253", 89, fnbase="movedtree"),
'qcdbctoept080_2017': (84, ['/store/user/pekotamn/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/TrackMoverULV30LepMumv4_2017/230607_032313/0000/movedtree_%i.root' % i for i in chain(xrange(1,47), xrange(48,86))]),
'qcdbctoept170_2017': _fromnum1("/store/user/pekotamn/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/TrackMoverULV30LepMumv4_2017/230607_032333", 91, fnbase="movedtree"),
'qcdbctoept250_2017': _fromnum1("/store/user/pekotamn/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/TrackMoverULV30LepMumv4_2017/230607_032353", 79, fnbase="movedtree"),
'wjetstolnu_2017': (403, ['/store/user/pekotamn/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverULV30LepMumv4_2017/230607_032421/0000/movedtree_%i.root' % i for i in chain(xrange(1,212), xrange(213,405))]),
'wjetstolnu_amcatnlo_2017': _fromnum1("/store/user/pekotamn/WJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-pythia8/TrackMoverULV30LepMumv4_2017/230623_191725", 159, fnbase="movedtree"),
'dyjetstollM10_2017': _fromnum1("/store/user/pekotamn/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverULV30LepMumv4_2017/230607_032441", 393, fnbase="movedtree"),
'dyjetstollM50_2017': (434, ['/store/user/pekotamn/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverULV30LepMumv4_2017/230607_032501/0000/movedtree_%i.root' % i for i in chain(xrange(1,290), xrange(291,311), xrange(314,316), xrange(317,411), xrange(412,440), [312])]),
'ttbar_2017': (1466, ['/store/user/pkotamni/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/TrackMoverULV30LepMumv4_2017/230606_222604' + '/%04i/movedtree_%i.root' % (i/1000,i) for i in chain(xrange(69), xrange(70,160), xrange(163,219), xrange(220,343), xrange(344,365), xrange(366,537), xrange(538,645), xrange(646,677), xrange(678,861), xrange(862,1140), xrange(1141,1165), xrange(1166,1250), xrange(1251,1269), xrange(1270,1449), xrange(1450,1472), xrange(1473,1482), [161])]),
'ww_2017': _fromnum1("/store/user/pekotamn/WW_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv4_2017/230607_032521", 94, fnbase="movedtree"),
'zz_2017': _fromnum1("/store/user/pekotamn/ZZ_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv4_2017/230607_032541", 25, fnbase="movedtree"),
'wz_2017': (42, ['/store/user/pekotamn/WZ_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv4_2017/230607_032602/0000/movedtree_%i.root' % i for i in chain(xrange(1,35), xrange(36,44))]),
'SingleMuon2017B': _fromnum1("/store/user/pekotamn/SingleMuon/TrackMoverULV30LepMumv4_2017/230607_031535", 325, fnbase="movedtree"),
'SingleMuon2017C': _fromnum1("/store/user/pekotamn/SingleMuon/TrackMoverULV30LepMumv4_2017/230607_031557", 505, fnbase="movedtree"),
#'SingleMuon2017D': (207, ['/store/user/pekotamn/SingleMuon/TrackMoverULV30LepMumv4_2017/230607_031618/0000/movedtree_%i.root' % i for i in chain(xrange(1,34), xrange(35,66), xrange(67,121), xrange(122,159), xrange(160,182), xrange(183,190), xrange(191,214))]),
'SingleMuon2017E': (495, ['/store/user/pekotamn/SingleMuon/TrackMoverULV30LepMumv4_2017/230607_031639/0000/movedtree_%i.root' % i for i in chain(xrange(1,341), xrange(342,491), xrange(492,498))]),
'SingleMuon2017F': _fromnum1("/store/user/pekotamn/SingleMuon/TrackMoverULV30LepMumv4_2017/230607_031659", 725, fnbase="movedtree"),
'SingleElectron2017B': _fromnum1("/store/user/pekotamn/SingleElectron/TrackMoverULV30LepMumv4_2017/230607_031720", 200, fnbase="movedtree"),
'SingleElectron2017C': _fromnum1("/store/user/pekotamn/SingleElectron/TrackMoverULV30LepMumv4_2017/230607_160643", 408, fnbase="movedtree"),
#'SingleElectron2017D': _fromnum1("/store/user/pekotamn/SingleElectron/TrackMoverULV30LepMumv4_2017/230607_031741", 163, fnbase="movedtree"),
'SingleElectron2017E': (358, ['/store/user/pekotamn/SingleElectron/TrackMoverULV30LepMumv4_2017/230607_031803/0000/movedtree_%i.root' % i for i in chain(xrange(1,43), xrange(48,117), xrange(118,144), xrange(145,154), xrange(157,182), xrange(183,233), xrange(234,238), xrange(239,270), xrange(271,277), xrange(278,280), xrange(281,293), xrange(294,305), xrange(306,343), xrange(344,355), xrange(356,376), [44, 46, 155])]),
'SingleElectron2017F': _fromnum1("/store/user/pekotamn/SingleElectron/TrackMoverULV30LepMumv4_2017/230607_031823", 576, fnbase="movedtree"),
})


_add_ds("trackmoverulv30lepelemv4", {
'qcdempt015_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepElemv4_2017/230607_033610", 48, fnbase="movedtree"),
'qcdmupt15_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/TrackMoverULV30LepElemv4_2017/230607_033630", 156, fnbase="movedtree"),
'qcdempt020_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepElemv4_2017/230607_033653", 103, fnbase="movedtree"),
'qcdempt030_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepElemv4_2017/230607_033715", 69, fnbase="movedtree"),
'qcdempt050_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepElemv4_2017/230607_033736", 76, fnbase="movedtree"),
'qcdempt080_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepElemv4_2017/230607_033756", 69, fnbase="movedtree"),
'qcdempt120_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepElemv4_2017/230607_033816", 87, fnbase="movedtree"),
'qcdempt170_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepElemv4_2017/230607_033836", 37, fnbase="movedtree"),
'qcdempt300_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepElemv4_2017/230607_033856", 24, fnbase="movedtree"),
'qcdbctoept020_2017': (92, ['/store/user/pekotamn/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/TrackMoverULV30LepElemv4_2017/230607_033916/0000/movedtree_%i.root' % i for i in chain(xrange(1,46), xrange(47,94))]),
'qcdbctoept030_2017': _fromnum1("/store/user/pekotamn/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/TrackMoverULV30LepElemv4_2017/230607_033936", 89, fnbase="movedtree"),
'qcdbctoept080_2017': (84, ['/store/user/pekotamn/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/TrackMoverULV30LepElemv4_2017/230607_033956/0000/movedtree_%i.root' % i for i in chain(xrange(1,47), xrange(48,86))]),
'qcdbctoept170_2017': _fromnum1("/store/user/pekotamn/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/TrackMoverULV30LepElemv4_2017/230607_034016", 91, fnbase="movedtree"),
'qcdbctoept250_2017': _fromnum1("/store/user/pekotamn/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/TrackMoverULV30LepElemv4_2017/230607_034037", 79, fnbase="movedtree"),
'wjetstolnu_2017': (403, ['/store/user/pekotamn/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverULV30LepElemv4_2017/230607_034406/0000/movedtree_%i.root' % i for i in chain(xrange(1,212), xrange(213,405))]),
'wjetstolnu_amcatnlo_2017': _fromnum1("/store/user/pekotamn/WJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-pythia8/TrackMoverULV30LepElemv4_2017/230623_191857", 159, fnbase="movedtree"),
'dyjetstollM10_2017': _fromnum1("/store/user/pekotamn/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverULV30LepElemv4_2017/230607_034426", 393, fnbase="movedtree"),
'dyjetstollM50_2017': (434, ['/store/user/pekotamn/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverULV30LepElemv4_2017/230607_034446/0000/movedtree_%i.root' % i for i in chain(xrange(1,290), xrange(291,311), xrange(314,316), xrange(317,411), xrange(412,440), [312])]),
#'ttbar_2017': (1467, ['/store/user/pkotamni/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/TrackMoverULV30LepElemv4_2017/230606_224548' + '/%04i/movedtree_%i.root' % (i/1000,i) for i in chain(xrange(68), xrange(69,160), xrange(163,219), xrange(220,343), xrange(344,365), xrange(366,537), xrange(538,645), xrange(646,677), xrange(678,861), xrange(862,1167), xrange(1168,1250), xrange(1251,1269), xrange(1270,1449), xrange(1450,1472), xrange(1473,1482), [161])]),
'ttbar_2017': (1466, ['/store/user/pkotamni/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/TrackMoverULV30LepElemv4_2017/230606_224548' + '/%04i/movedtree_%i.root' % (i/1000,i) for i in chain(xrange(69), xrange(70,160), xrange(163,219), xrange(220,343), xrange(344,365), xrange(366,537), xrange(538,645), xrange(646,677), xrange(678,861), xrange(862,1140), xrange(1141,1165), xrange(1166,1250), xrange(1251,1269), xrange(1270,1449), xrange(1450,1472), xrange(1473,1482), [161])]),
'ww_2017': _fromnum1("/store/user/pekotamn/WW_TuneCP5_13TeV-pythia8/TrackMoverULV30LepElemv4_2017/230607_034506", 94, fnbase="movedtree"),
'zz_2017': _fromnum1("/store/user/pekotamn/ZZ_TuneCP5_13TeV-pythia8/TrackMoverULV30LepElemv4_2017/230607_034525", 25, fnbase="movedtree"),
'wz_2017': (42, ['/store/user/pekotamn/WZ_TuneCP5_13TeV-pythia8/TrackMoverULV30LepElemv4_2017/230607_034546/0000/movedtree_%i.root' % i for i in chain(xrange(1,35), xrange(36,44))]),
'SingleMuon2017B': _fromnum1("/store/user/pekotamn/SingleMuon/TrackMoverULV30LepElemv4_2017/230607_034058", 325, fnbase="movedtree"),
'SingleMuon2017C': _fromnum1("/store/user/pekotamn/SingleMuon/TrackMoverULV30LepElemv4_2017/230607_034118", 505, fnbase="movedtree"),
#'SingleMuon2017D': (206, ['/store/user/pekotamn/SingleMuon/TrackMoverULV30LepElemv4_2017/230607_034138/0000/movedtree_%i.root' % i for i in chain(xrange(1,34), xrange(35,66), xrange(67,121), xrange(122,159), xrange(160,162), xrange(163,182), xrange(183,190), xrange(191,214))]),
'SingleMuon2017E': (495, ['/store/user/pekotamn/SingleMuon/TrackMoverULV30LepElemv4_2017/230607_034159/0000/movedtree_%i.root' % i for i in chain(xrange(1,341), xrange(342,491), xrange(492,498))]),
'SingleMuon2017F': _fromnum1("/store/user/pekotamn/SingleMuon/TrackMoverULV30LepElemv4_2017/230607_034220", 725, fnbase="movedtree"),
'SingleElectron2017B': _fromnum1("/store/user/pekotamn/SingleElectron/TrackMoverULV30LepElemv4_2017/230607_034241", 200, fnbase="movedtree"),
'SingleElectron2017C': _fromnum1("/store/user/pekotamn/SingleElectron/TrackMoverULV30LepElemv4_2017/230607_160525", 408, fnbase="movedtree"),
#'SingleElectron2017D': (27, ['/store/user/pekotamn/SingleElectron/TrackMoverULV30LepElemv4_2017/230607_034303/0000/movedtree_%i.root' % i for i in chain(xrange(27,30), xrange(35,37), xrange(50,52), [1, 8, 18, 24, 31, 38, 40, 54, 56, 71, 80, 96, 101, 115, 119, 126, 132, 134, 139, 147])]),
'SingleElectron2017E': (358, ['/store/user/pekotamn/SingleElectron/TrackMoverULV30LepElemv4_2017/230607_034323/0000/movedtree_%i.root' % i for i in chain(xrange(1,43), xrange(48,117), xrange(118,144), xrange(145,154), xrange(157,182), xrange(183,233), xrange(234,238), xrange(239,270), xrange(271,277), xrange(278,280), xrange(281,293), xrange(294,305), xrange(306,343), xrange(344,355), xrange(356,376), [44, 46, 155])]),
'SingleElectron2017F': _fromnum1("/store/user/pekotamn/SingleElectron/TrackMoverULV30LepElemv4_2017/230607_034345", 576, fnbase="movedtree"),
})


_add_ds("trackmovermctruthulv30lepmv2", {
'WplusHToSSTodddd_tau30mm_M55_2017': _fromnum0("/store/user/pkotamni/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-30_TuneCP5_13TeV-powheg-pythia8/TrackMoverMCTruthULV30Lepmv2/230528_172352", 240, fnbase="mctruth"),
'WplusHToSSTodddd_tau1mm_M55_2017': _fromnum0("/store/user/pkotamni/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/TrackMoverMCTruthULV30Lepmv2/230528_172412", 250, fnbase="mctruth"),
'WplusHToSSTodddd_tau300um_M55_2017': _fromnum0("/store/user/pkotamni/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/TrackMoverMCTruthULV30Lepmv2/230528_172435", 250, fnbase="mctruth"),
})


_add_ds("ntupleuloffshjv30lepm", {
'qcdempt015_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULoffshjV30Lepm_2017/230522_180008", 21),
'qcdmupt15_2017': (60, ['/store/user/pekotamn/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/NtupleULoffshjV30Lepm_2017/230522_182408/0000/ntuple_%i.root' % i for i in chain(xrange(1,55), xrange(56,62))]),
'qcdempt020_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULoffshjV30Lepm_2017/230522_183546", 44),
'qcdempt030_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULoffshjV30Lepm_2017/230522_185004", 24),
'qcdempt050_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULoffshjV30Lepm_2017/230522_185944", 26),
'qcdempt080_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULoffshjV30Lepm_2017/230522_191131", 22),
'qcdempt120_2017': (28, ['/store/user/pekotamn/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULoffshjV30Lepm_2017/230522_191250/0000/ntuple_%i.root' % i for i in chain(xrange(1,12), xrange(13,30))]),
'qcdbctoept020_2017': _fromnum1("/store/user/pekotamn/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/NtupleULoffshjV30Lepm_2017/230522_202302", 33),
'qcdbctoept030_2017': _fromnum1("/store/user/pekotamn/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/NtupleULoffshjV30Lepm_2017/230522_202319", 32),
'qcdbctoept080_2017': _fromnum1("/store/user/pekotamn/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/NtupleULoffshjV30Lepm_2017/230522_202336", 28),
'qcdbctoept170_2017': _fromnum1("/store/user/pekotamn/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/NtupleULoffshjV30Lepm_2017/230522_202353", 31),
'qcdbctoept250_2017': _fromnum1("/store/user/pekotamn/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/NtupleULoffshjV30Lepm_2017/230522_202410", 27),
'wjetstolnu_2017': _fromnum1("/store/user/pekotamn/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULoffshjV30Lepm_2017/230522_202427", 127),
'dyjetstollM10_2017': _fromnum1("/store/user/pekotamn/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULoffshjV30Lepm_2017/230522_202444", 123),
'dyjetstollM50_2017': (135, ['/store/user/pekotamn/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULoffshjV30Lepm_2017/230522_202501/0000/ntuple_%i.root' % i for i in chain(xrange(1,104), xrange(105,137))]),
'ttbar_2017': (590, ['/store/user/pkotamni/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleULoffshjV30Lepm_2017/230524_105513/0000/ntuple_%i.root' % i for i in chain(xrange(67,69), [12, 33, 62, 72, 82, 84, 87, 98, 100, 108, 184, 256, 416])] + ['/store/user/pkotamni/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleULoffshjV30Lepm_2017/230522_152552/0000/ntuple_%i.root' % i for i in chain(xrange(12), xrange(13,27), xrange(28,33), xrange(34,62), xrange(65,67), xrange(69,72), xrange(73,82), xrange(85,87), xrange(88,98), xrange(101,108), xrange(109,184), xrange(185,256), xrange(257,296), xrange(297,416), xrange(417,593), [63, 83, 99])]),
'ww_2017': _fromnum1("/store/user/pekotamn/WW_TuneCP5_13TeV-pythia8/NtupleULoffshjV30Lepm_2017/230522_202518", 29),
'zz_2017': _fromnum1("/store/user/pekotamn/WZ_TuneCP5_13TeV-pythia8/NtupleULoffshjV30Lepm_2017/230522_202535", 16),
'wz_2017': _fromnum1("/store/user/pekotamn/ZZ_TuneCP5_13TeV-pythia8/NtupleULoffshjV30Lepm_2017/230522_202551", 10),
})


_add_ds("ntupleulv30lepm", {
'qcdempt015_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV30Lepm_2017/230504_170340", 21),
#'qcdmupt15_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/NtupleULV30Lepm_2017/230504_170356", 63),
'qcdmupt15_2017': (60, ['/store/user/pekotamn/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/NtupleULV30Lepm_2017/230504_170356/0000/ntuple_%i.root' % i for i in chain(xrange(1,55), xrange(56,62))]),
'qcdempt020_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV30Lepm_2017/230504_170413", 46),
'qcdempt030_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV30Lepm_2017/230504_170430", 24),
'qcdempt050_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV30Lepm_2017/230504_170447", 26),
'qcdempt080_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV30Lepm_2017/230504_170503", 22),
#'qcdempt120_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV30Lepm_2017/230504_170522", 29),
'qcdempt120_2017': (28, ['/store/user/pekotamn/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV30Lepm_2017/230504_170522/0000/ntuple_%i.root' % i for i in chain(xrange(1,12), xrange(13,30))]),
'qcdempt170_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV30Lepm_2017/230504_170539", 14),
'qcdempt300_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV30Lepm_2017/230504_170557", 12),
'qcdbctoept020_2017': _fromnum1("/store/user/pekotamn/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/NtupleULV30Lepm_2017/230504_170614", 34),
'qcdbctoept030_2017': _fromnum1("/store/user/pekotamn/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/NtupleULV30Lepm_2017/230504_170632", 33),
'qcdbctoept080_2017': _fromnum1("/store/user/pekotamn/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/NtupleULV30Lepm_2017/230504_170649", 29),
'qcdbctoept170_2017': _fromnum1("/store/user/pekotamn/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/NtupleULV30Lepm_2017/230504_170706", 31),
'qcdbctoept250_2017': _fromnum1("/store/user/pekotamn/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/NtupleULV30Lepm_2017/230504_170723", 29),
'wjetstolnu_2017': _fromnum1("/store/user/pekotamn/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV30Lepm_2017/230504_170740", 127),
'dyjetstollM10_2017': _fromnum1("/store/user/pekotamn/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV30Lepm_2017/230504_170757", 123),
#'dyjetstollM50_2017': _fromnum1("/store/user/pekotamn/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV30Lepm_2017/230504_170814", 136),
'dyjetstollM50_2017': (135, ['/store/user/pekotamn/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV30Lepm_2017/230504_170814/0000/ntuple_%i.root' % i for i in chain(xrange(1,104), xrange(105,137))]),
#'ttbar_2017': _fromnum0("/store/user/pkotamni/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleULV30Lepm_2017/230504_120905", 593),
'ttbar_2017': (590, ['/store/user/pkotamni/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleULV30Lepm_2017/230504_120905/0000/ntuple_%i.root' % i for i in chain(xrange(67,69), [12, 33, 62, 72, 82, 84, 87, 98, 100, 108, 184, 256, 416])] + ['/store/user/pkotamni/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleULoffshjV30Lepm_2017/230522_152552/0000/ntuple_%i.root' % i for i in chain(xrange(12), xrange(13,27), xrange(28,33), xrange(34,62), xrange(65,67), xrange(69,72), xrange(73,82), xrange(85,87), xrange(88,98), xrange(101,108), xrange(109,184), xrange(185,256), xrange(257,296), xrange(297,416), xrange(417,593), [63, 83, 99])]),
'ww_2017': _fromnum1("/store/user/pekotamn/WW_TuneCP5_13TeV-pythia8/NtupleULV30Lepm_2017/230504_170831", 30),
'zz_2017': _fromnum1("/store/user/pekotamn/WZ_TuneCP5_13TeV-pythia8/NtupleULV30Lepm_2017/230504_170848", 16),
'wz_2017': _fromnum1("/store/user/pekotamn/ZZ_TuneCP5_13TeV-pythia8/NtupleULV30Lepm_2017/230504_170905", 11),
'mfv_stoplb_tau010000um_M0400_2017': _fromnum1("/store/user/pekotamn/DisplacedSUSY_stopToLBottom_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV30Lepm_2017/230504_182637", 201),
'mfv_stoplb_tau001000um_M0400_2017': _fromnum1("/store/user/pekotamn/DisplacedSUSY_stopToLBottom_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV30Lepm_2017/230504_182707", 201),
'mfv_stopld_tau010000um_M0400_2017': _fromnum1("/store/user/pekotamn/DisplacedSUSY_stopToLD_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV30Lepm_2017/230504_182600", 201),
'mfv_stopld_tau001000um_M0400_2017': _fromnum1("/store/user/pekotamn/DisplacedSUSY_stopToLD_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV30Lepm_2017/230504_182525", 199),
'WplusHToSSTodddd_tau30mm_M55_2017': _fromnum1("/store/user/pekotamn/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-30_TuneCP5_13TeV-powheg-pythia8/NtupleULV30Lepm_2017/230504_182358", 48),
'WplusHToSSTodddd_tau1mm_M55_2017': _fromnum1("/store/user/pekotamn/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/NtupleULV30Lepm_2017/230504_182435", 50),
'WplusHToSSTodddd_tau300um_M55_2017': _fromnum1("/store/user/pekotamn/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/NtupleULV30Lepm_2017/230504_182323", 50),
})


_add_ds("ntupleultkrec0p9v30lepm", {
'qcdempt015_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULtkrec0p9V30Lepm_2017/230514_144341", 21),
'qcdmupt15_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/NtupleULtkrec0p9V30Lepm_2017/230514_144358", 65),
'qcdempt020_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULtkrec0p9V30Lepm_2017/230514_144415", 44),
#'qcdempt030_2017': (23, ['/store/user/pekotamn/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULtkrec0p9V30Lepm_2017/230514_144431/0000/ntuple_%i.root' % i for i in chain(xrange(1,23), [24])]),
'qcdempt050_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULtkrec0p9V30Lepm_2017/230514_144448", 26),
'qcdempt080_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULtkrec0p9V30Lepm_2017/230514_144506", 22),
#'qcdempt120_2017': (28, ['/store/user/pekotamn/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULtkrec0p9V30Lepm_2017/230514_144522/0000/ntuple_%i.root' % i for i in chain(xrange(1,12), xrange(13,30))]),
'qcdempt170_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULtkrec0p9V30Lepm_2017/230514_144539", 14),
'qcdempt300_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULtkrec0p9V30Lepm_2017/230514_144555", 12),
#'qcdbctoept020_2017': (33, ['/store/user/pekotamn/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/NtupleULtkrec0p9V30Lepm_2017/230514_144614/0000/ntuple_%i.root' % i for i in chain(xrange(1,33), [34])]),
'qcdbctoept030_2017': _fromnum1("/store/user/pekotamn/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/NtupleULtkrec0p9V30Lepm_2017/230514_144631", 32),
'qcdbctoept080_2017': _fromnum1("/store/user/pekotamn/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/NtupleULtkrec0p9V30Lepm_2017/230514_144648", 29),
#'qcdbctoept170_2017': _fromnum1("/store/user/pekotamn/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/NtupleULtkrec0p9V30Lepm_2017/230514_144705", 31),
'qcdbctoept250_2017': _fromnum1("/store/user/pekotamn/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/NtupleULtkrec0p9V30Lepm_2017/230514_144722", 28),
'wjetstolnu_2017': _fromnum1("/store/user/pekotamn/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULtkrec0p9V30Lepm_2017/230514_144738", 127),
'dyjetstollM10_2017': _fromnum1("/store/user/pekotamn/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULtkrec0p9V30Lepm_2017/230514_144755", 123),
#'dyjetstollM50_2017': (131, ['/store/user/pekotamn/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULtkrec0p9V30Lepm_2017/230514_144811/0000/ntuple_%i.root' % i for i in chain(xrange(1,18), xrange(19,101), xrange(104,130), xrange(133,137), [102, 131])]),
'ttbar_2017': (584, ['/store/user/pkotamni/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleULtkrec0p9V30Lepm_2017/230514_094902/0000/ntuple_%i.root' % i for i in chain(xrange(27), xrange(28,64), xrange(66,296), xrange(297,343), xrange(344,387), xrange(388,393), xrange(394,477), xrange(478,513), xrange(514,593))]),
'ww_2017': _fromnum1("/store/user/pekotamn/WW_TuneCP5_13TeV-pythia8/NtupleULtkrec0p9V30Lepm_2017/230514_144829", 29),
'zz_2017': _fromnum1("/store/user/pekotamn/WZ_TuneCP5_13TeV-pythia8/NtupleULtkrec0p9V30Lepm_2017/230514_144845", 16),
'wz_2017': _fromnum1("/store/user/pekotamn/ZZ_TuneCP5_13TeV-pythia8/NtupleULtkrec0p9V30Lepm_2017/230514_144902", 10),
'WplusHToSSTodddd_tau1mm_M55_2017': _fromnum1("/store/user/pekotamn/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/NtupleULtkrec0p9V30Lepm_2017/230514_144251", 50),
})


_add_ds("ntupleultkrec1p1v30lepm", {
'qcdempt015_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULtkrec1p1V30Lepm_2017/230514_143129", 21),
'qcdmupt15_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/NtupleULtkrec1p1V30Lepm_2017/230514_143146", 65),
'qcdempt020_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULtkrec1p1V30Lepm_2017/230514_143202", 44),
#'qcdempt030_2017': (23, ['/store/user/pekotamn/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULtkrec1p1V30Lepm_2017/230514_143219/0000/ntuple_%i.root' % i for i in chain(xrange(1,23), [24])]),
'qcdempt050_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULtkrec1p1V30Lepm_2017/230514_143236", 26),
'qcdempt080_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULtkrec1p1V30Lepm_2017/230514_143252", 22),
#'qcdempt120_2017': (28, ['/store/user/pekotamn/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULtkrec1p1V30Lepm_2017/230514_143308/0000/ntuple_%i.root' % i for i in chain(xrange(1,12), xrange(13,30))]),
'qcdempt170_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULtkrec1p1V30Lepm_2017/230514_143325", 14),
'qcdempt300_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULtkrec1p1V30Lepm_2017/230514_143342", 12),
#'qcdbctoept020_2017': (33, ['/store/user/pekotamn/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/NtupleULtkrec1p1V30Lepm_2017/230514_143359/0000/ntuple_%i.root' % i for i in chain(xrange(1,33), [34])]),
'qcdbctoept030_2017': _fromnum1("/store/user/pekotamn/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/NtupleULtkrec1p1V30Lepm_2017/230514_143415", 32),
'qcdbctoept080_2017': _fromnum1("/store/user/pekotamn/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/NtupleULtkrec1p1V30Lepm_2017/230514_143431", 29),
#'qcdbctoept170_2017': (30, ['/store/user/pekotamn/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/NtupleULtkrec1p1V30Lepm_2017/230514_143448/0000/ntuple_%i.root' % i for i in chain(xrange(1,21), xrange(22,32))]),
'qcdbctoept250_2017': _fromnum1("/store/user/pekotamn/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/NtupleULtkrec1p1V30Lepm_2017/230514_143505", 28),
'wjetstolnu_2017': _fromnum1("/store/user/pekotamn/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULtkrec1p1V30Lepm_2017/230514_143521", 127),
'dyjetstollM10_2017': _fromnum1("/store/user/pekotamn/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULtkrec1p1V30Lepm_2017/230514_143538", 123),
#'dyjetstollM50_2017': (131, ['/store/user/pekotamn/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULtkrec1p1V30Lepm_2017/230514_143555/0000/ntuple_%i.root' % i for i in chain(xrange(1,101), xrange(104,113), xrange(114,130), xrange(133,137), [102, 131])]),
'ttbar_2017': (584, ['/store/user/pkotamni/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleULtkrec1p1V30Lepm_2017/230514_093645/0000/ntuple_%i.root' % i for i in chain(xrange(27), xrange(28,64), xrange(66,296), xrange(297,343), xrange(344,387), xrange(388,393), xrange(394,477), xrange(478,513), xrange(514,593))]),
'ww_2017': _fromnum1("/store/user/pekotamn/WW_TuneCP5_13TeV-pythia8/NtupleULtkrec1p1V30Lepm_2017/230514_143611", 29),
'zz_2017': _fromnum1("/store/user/pekotamn/WZ_TuneCP5_13TeV-pythia8/NtupleULtkrec1p1V30Lepm_2017/230514_143628", 16),
'wz_2017': _fromnum1("/store/user/pekotamn/ZZ_TuneCP5_13TeV-pythia8/NtupleULtkrec1p1V30Lepm_2017/230514_143644", 10),
'WplusHToSSTodddd_tau1mm_M55_2017': _fromnum1("/store/user/pekotamn/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/NtupleULtkrec1p1V30Lepm_2017/230514_142955", 50),
})


_add_ds("ntupleulv1lepm", {
'qcdempt015_2017': _fromnum1("/store/user/awarden/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV1Lepm_2017/221118_130831", 35),
'qcdmupt15_2017': _fromnum1("/store/user/awarden/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/NtupleULV1Lepm_2017/221117_163136", 120),
'qcdempt020_2017': _fromnum1("/store/user/awarden/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV1Lepm_2017/221117_163154", 96),
#'qcdempt030_2017': (36, ['/store/user/awarden/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV1Lepm_2017/221117_163213/0000/ntuple_%i.root' % i for i in chain(xrange(1,25), xrange(26,38))]),
'qcdempt050_2017': _fromnum1("/store/user/awarden/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV1Lepm_2017/221117_163232", 39),
'qcdempt080_2017': _fromnum1("/store/user/awarden/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV1Lepm_2017/221117_163255", 36),
'qcdempt120_2017': _fromnum1("/store/user/awarden/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV1Lepm_2017/221117_163313", 44),
'qcdempt170_2017': _fromnum1("/store/user/awarden/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV1Lepm_2017/221117_163333", 27),
'qcdempt300_2017': _fromnum1("/store/user/awarden/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV1Lepm_2017/221117_163356", 17),
'qcdbctoept020_2017': _fromnum1("/store/user/awarden/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/NtupleULV1Lepm_2017/221117_163540", 51),
#'qcdbctoept030_2017': (47, ['/store/user/awarden/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/NtupleULV1Lepm_2017/221117_163601/0000/ntuple_%i.root' % i for i in chain(xrange(1,26), xrange(27,49))]),
#'qcdbctoept080_2017': (37, ['/store/user/awarden/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/NtupleULV1Lepm_2017/221117_163620/0000/ntuple_%i.root' % i for i in chain(xrange(1,13), xrange(14,39))]),
'qcdbctoept170_2017': _fromnum1("/store/user/awarden/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/NtupleULV1Lepm_2017/221117_163638", 44),
'qcdbctoept250_2017': _fromnum1("/store/user/awarden/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/NtupleULV1Lepm_2017/221117_163656", 37),
#'wjetstolnu_2017': (145, ['/store/user/awarden/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV1Lepm_2017/221117_163717/0000/ntuple_%i.root' % i for i in chain(xrange(1,35), xrange(41,152))]),
#'dyjetstollM10_2017': (130, ['/store/user/awarden/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV1Lepm_2017/221117_163735/0000/ntuple_%i.root' % i for i in chain(xrange(1,26), xrange(35,41), xrange(42,139), [29, 33])]),
#'dyjetstollM50_2017': (137, ['/store/user/awarden/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV1Lepm_2017/221117_163753/0000/ntuple_%i.root' % i for i in chain(xrange(1,19), xrange(21,140))]),
'ttbar_2017': _fromnum0("/store/user/awarden/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleULV1Lepm_2017/221117_095953", 1019),
#'ww_2017': (30, ['/store/user/awarden/WW_TuneCP5_13TeV-pythia8/NtupleULV1Lepm_2017/221117_163812/0000/ntuple_%i.root' % i for i in chain(xrange(1,9), xrange(10,32))]),
'zz_2017': _fromnum1("/store/user/awarden/WZ_TuneCP5_13TeV-pythia8/NtupleULV1Lepm_2017/221117_163833", 18),
'wz_2017': _fromnum1("/store/user/awarden/ZZ_TuneCP5_13TeV-pythia8/NtupleULV1Lepm_2017/221117_163852", 14),
'mfv_stoplb_tau000100um_M1000_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_173002", 201),
'mfv_stoplb_tau000300um_M1000_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_173020", 201),
'mfv_stoplb_tau010000um_M1000_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_173041", 101),
'mfv_stoplb_tau001000um_M1000_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_173100", 201),
'mfv_stoplb_tau030000um_M1000_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_173118", 201),
'mfv_stoplb_tau000100um_M1200_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_173137", 201),
'mfv_stoplb_tau000300um_M1200_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_173156", 200),
'mfv_stoplb_tau010000um_M1200_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_173214", 101),
'mfv_stoplb_tau001000um_M1200_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_173232", 201),
'mfv_stoplb_tau030000um_M1200_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_173250", 201),
'mfv_stoplb_tau000100um_M1400_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_173311", 201),
'mfv_stoplb_tau000300um_M1400_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_173330", 201),
'mfv_stoplb_tau010000um_M1400_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_173349", 101),
'mfv_stoplb_tau001000um_M1400_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_173408", 201),
'mfv_stoplb_tau030000um_M1400_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_173433", 201),
'mfv_stoplb_tau000100um_M1600_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_173453", 201),
'mfv_stoplb_tau000300um_M1600_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_173514", 201),
'mfv_stoplb_tau010000um_M1600_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_173536", 101),
'mfv_stoplb_tau001000um_M1600_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_173555", 101),
'mfv_stoplb_tau030000um_M1600_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_173621", 101),
'mfv_stoplb_tau000100um_M1800_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_173641", 201),
'mfv_stoplb_tau000300um_M1800_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_173659", 201),
'mfv_stoplb_tau010000um_M1800_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_173717", 101),
'mfv_stoplb_tau001000um_M1800_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_173737", 101),
'mfv_stoplb_tau030000um_M1800_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_173758", 101),
'mfv_stoplb_tau000100um_M0200_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_173817", 201),
'mfv_stoplb_tau000300um_M0200_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_173835", 201),
'mfv_stoplb_tau010000um_M0200_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_173854", 201),
'mfv_stoplb_tau030000um_M0200_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_173935", 201),
'mfv_stoplb_tau000100um_M0300_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_173953", 201),
'mfv_stoplb_tau000300um_M0300_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_174011", 200),
'mfv_stoplb_tau010000um_M0300_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_174033", 201),
'mfv_stoplb_tau030000um_M0300_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_174111", 201),
'mfv_stoplb_tau000100um_M0400_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_174246", 201),
'mfv_stoplb_tau000300um_M0400_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_174306", 201),
'mfv_stoplb_tau010000um_M0400_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_174324", 201),
'mfv_stoplb_tau030000um_M0400_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_174403", 201),
'mfv_stoplb_tau000100um_M0600_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_174427", 201),
'mfv_stoplb_tau000300um_M0600_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_174445", 201),
'mfv_stoplb_tau010000um_M0600_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_174504", 201),
'mfv_stoplb_tau030000um_M0600_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_174545", 201),
'mfv_stoplb_tau000100um_M0800_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_174603", 201),
'mfv_stoplb_tau000300um_M0800_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_174621", 201),
'mfv_stoplb_tau010000um_M0800_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_174643", 101),
'mfv_stoplb_tau030000um_M0800_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_174720", 201),
'mfv_stopld_tau000100um_M1000_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_174737", 201),
'mfv_stopld_tau000300um_M1000_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_174757", 201),
'mfv_stopld_tau010000um_M1000_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_174814", 101),
'mfv_stopld_tau001000um_M1000_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_174833", 201),
'mfv_stopld_tau030000um_M1000_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221118_131235", 201),
'mfv_stopld_tau000100um_M1200_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_174909", 201),
'mfv_stopld_tau000300um_M1200_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221118_131255", 201),
'mfv_stopld_tau010000um_M1200_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_174927", 101),
'mfv_stopld_tau001000um_M1200_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221118_131320", 201),
'mfv_stopld_tau030000um_M1200_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_175002", 201),
'mfv_stopld_tau000100um_M1400_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_175023", 201),
'mfv_stopld_tau000300um_M1400_2017': (200, ['/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_175040/0000/ntuple_%i.root' % i for i in chain(xrange(1,64), xrange(65,202))]),
'mfv_stopld_tau010000um_M1400_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_175059", 101),
'mfv_stopld_tau001000um_M1400_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_175117", 201),
'mfv_stopld_tau030000um_M1400_2017': (200, ['/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_175136/0000/ntuple_%i.root' % i for i in chain(xrange(1,79), xrange(80,202))]),
'mfv_stopld_tau000100um_M1600_2017': (200, ['/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_175155/0000/ntuple_%i.root' % i for i in chain(xrange(1,189), xrange(190,202))]),
'mfv_stopld_tau000300um_M1600_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_175213", 201),
'mfv_stopld_tau010000um_M1600_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_175231", 101),
'mfv_stopld_tau001000um_M1600_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_175252", 101),
'mfv_stopld_tau030000um_M1600_2017': (100, ['/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_175310/0000/ntuple_%i.root' % i for i in chain(xrange(3,102), [1])]),
'mfv_stopld_tau000100um_M1800_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_175328", 200),
'mfv_stopld_tau000300um_M1800_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_175347", 201),
'mfv_stopld_tau010000um_M1800_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_175408", 101),
'mfv_stopld_tau001000um_M1800_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_175429", 101),
'mfv_stopld_tau030000um_M1800_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_175453", 101),
'mfv_stopld_tau000100um_M0200_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_175514", 201),
'mfv_stopld_tau000300um_M0200_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_175533", 201),
'mfv_stopld_tau010000um_M0200_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_175552", 200),
'mfv_stopld_tau030000um_M0200_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_175631", 201),
'mfv_stopld_tau000100um_M0300_2017': (199, ['/store/user/awarden/DisplacedSUSY_stopToLD_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_175649/0000/ntuple_%i.root' % i for i in chain(xrange(1,28), xrange(29,131), xrange(132,202))]),
'mfv_stopld_tau000300um_M0300_2017': (199, ['/store/user/awarden/DisplacedSUSY_stopToLD_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_175707/0000/ntuple_%i.root' % i for i in chain(xrange(1,95), xrange(96,142), xrange(143,202))]),
'mfv_stopld_tau010000um_M0300_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_175725", 201),
'mfv_stopld_tau030000um_M0300_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_175804", 201),
'mfv_stopld_tau000100um_M0400_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_175822", 201),
'mfv_stopld_tau000300um_M0400_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_175840", 201),
'mfv_stopld_tau010000um_M0400_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_175859", 201),
'mfv_stopld_tau030000um_M0400_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_175937", 201),
'mfv_stopld_tau000100um_M0600_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_175955", 201),
'mfv_stopld_tau000300um_M0600_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_180013", 200),
'mfv_stopld_tau010000um_M0600_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_180031", 196),
'mfv_stopld_tau030000um_M0600_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_180109", 201),
'mfv_stopld_tau000100um_M0800_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_180128", 201),
'mfv_stopld_tau000300um_M0800_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_180146", 201),
'mfv_stopld_tau010000um_M0800_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_180204", 101),
'mfv_stopld_tau030000um_M0800_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2017/221117_180245", 201),
})



#TrackingTreer with good lepton sel tracks + tracks matched to good leptons; event filter and trigger filter were applied
_add_ds("trackingtreerulv1_lepm_wsellep", {
'qcdempt015_2017': _fromnum1("/store/user/awarden/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/TrackingTreerULV1_Lepm_wsellep_2017/221004_094341", 35, fnbase="trackingtreer"),
'qcdmupt15_2017': _fromnum1("/store/user/awarden/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/TrackingTreerULV1_Lepm_wsellep_2017/221004_094356", 142, fnbase="trackingtreer"),
'qcdempt020_2017': _fromnum1("/store/user/awarden/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/TrackingTreerULV1_Lepm_wsellep_2017/221004_094410", 103, fnbase="trackingtreer"),
'qcdempt030_2017': (33, ['/store/user/awarden/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/TrackingTreerULV1_Lepm_wsellep_2017/221004_094427/0000/trackingtreer_%i.root' % i for i in chain(xrange(3,35), [1])]),
'qcdempt050_2017': _fromnum1("/store/user/awarden/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/TrackingTreerULV1_Lepm_wsellep_2017/221004_094441", 38, fnbase="trackingtreer"),
'qcdempt080_2017': _fromnum1("/store/user/awarden/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/TrackingTreerULV1_Lepm_wsellep_2017/221004_094456", 34, fnbase="trackingtreer"),
'qcdempt120_2017': _fromnum1("/store/user/awarden/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/TrackingTreerULV1_Lepm_wsellep_2017/221004_094511", 41, fnbase="trackingtreer"),
'qcdempt170_2017': _fromnum1("/store/user/awarden/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/TrackingTreerULV1_Lepm_wsellep_2017/221004_094527", 25, fnbase="trackingtreer"),
'qcdempt300_2017': _fromnum1("/store/user/awarden/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/TrackingTreerULV1_Lepm_wsellep_2017/221004_094543", 17, fnbase="trackingtreer"),
'qcdbctoept020_2017': _fromnum1("/store/user/awarden/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/TrackingTreerULV1_Lepm_wsellep_2017/221004_094558", 51, fnbase="trackingtreer"),
'qcdbctoept030_2017': _fromnum1("/store/user/awarden/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/TrackingTreerULV1_Lepm_wsellep_2017/221004_094613", 48, fnbase="trackingtreer"),
'qcdbctoept080_2017': (33, ['/store/user/awarden/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/TrackingTreerULV1_Lepm_wsellep_2017/221004_094629/0000/trackingtreer_%i.root' % i for i in chain(xrange(1,5), xrange(6,35))]),
'qcdbctoept170_2017': _fromnum1("/store/user/awarden/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/TrackingTreerULV1_Lepm_wsellep_2017/221004_094645", 46, fnbase="trackingtreer"),
'qcdbctoept250_2017': _fromnum1("/store/user/awarden/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/TrackingTreerULV1_Lepm_wsellep_2017/221004_094700", 32, fnbase="trackingtreer"),
'wjetstolnu_2017': _fromnum1("/store/user/awarden/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/TrackingTreerULV1_Lepm_wsellep_2017/221004_094805", 106, fnbase="trackingtreer"),
'dyjetstollM10_2017': (93, ['/store/user/awarden/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/TrackingTreerULV1_Lepm_wsellep_2017/221004_094821/0000/trackingtreer_%i.root' % i for i in chain(xrange(1,10), xrange(11,63), xrange(64,96))]),
'dyjetstollM50_2017': (60, ['/store/user/awarden/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/TrackingTreerULV1_Lepm_wsellep_2017/221004_094836/0000/trackingtreer_%i.root' % i for i in chain(xrange(1,7), xrange(9,17), xrange(18,23), xrange(24,35), xrange(36,41), xrange(44,52), xrange(53,55), xrange(60,67), xrange(68,72), [42, 56, 58, 74])]),
'ttbar_2017': (254, ['/store/user/awarden/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/TrackingTreerULV1_Lepm_wsellep_2017/221004_123503/0000/trackingtreer_%i.root' % i for i in chain(xrange(106), xrange(107,255))]),
'ww_2017': _fromnum1("/store/user/awarden/WW_TuneCP5_13TeV-pythia8/TrackingTreerULV1_Lepm_wsellep_2017/221004_094852", 21, fnbase="trackingtreer"),
'zz_2017': _fromnum1("/store/user/awarden/WZ_TuneCP5_13TeV-pythia8/TrackingTreerULV1_Lepm_wsellep_2017/221004_094908", 13, fnbase="trackingtreer"),
'wz_2017': _fromnum1("/store/user/awarden/ZZ_TuneCP5_13TeV-pythia8/TrackingTreerULV1_Lepm_wsellep_2017/221004_094923", 14, fnbase="trackingtreer"),
'SingleMuon2017B': _fromnum0("/store/user/awarden/SingleMuon/TrackingTreerULV1_Lepm_wsellep_2017/221004_044926", 60, fnbase="trackingtreer"),
'SingleMuon2017C': _fromnum1("/store/user/awarden/SingleMuon/TrackingTreerULV1_Lepm_wsellep_2017/221004_094716", 78, fnbase="trackingtreer"),
'SingleMuon2017D': _fromnum0("/store/user/awarden/SingleMuon/TrackingTreerULV1_Lepm_wsellep_2017/221004_044927", 34, fnbase="trackingtreer"),
'SingleMuon2017E': _fromnum0("/store/user/awarden/SingleMuon/TrackingTreerULV1_Lepm_wsellep_2017/221004_044928", 86, fnbase="trackingtreer"),
'SingleMuon2017F': _fromnum1("/store/user/awarden/SingleMuon/TrackingTreerULV1_Lepm_wsellep_2017/221004_094732", 109, fnbase="trackingtreer"),
'SingleElectron2017B': _fromnum0("/store/user/awarden/SingleElectron/TrackingTreerULV1_Lepm_wsellep_2017/221004_044929", 32, fnbase="trackingtreer"),
'SingleElectron2017C': _fromnum0("/store/user/awarden/SingleElectron/TrackingTreerULV1_Lepm_wsellep_2017/221004_044930", 64, fnbase="trackingtreer"),
'SingleElectron2017D': _fromnum0("/store/user/awarden/SingleElectron/TrackingTreerULV1_Lepm_wsellep_2017/221004_044931", 25, fnbase="trackingtreer"),
'SingleElectron2017E': (59, ['/store/user/awarden/SingleElectron/TrackingTreerULV1_Lepm_wsellep_2017/221004_044932/0000/trackingtreer_%i.root' % i for i in chain(xrange(9), xrange(10,60))]),
'SingleElectron2017F': _fromnum1("/store/user/awarden/SingleElectron/TrackingTreerULV1_Lepm_wsellep_2017/221004_094749", 89, fnbase="trackingtreer"),
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
