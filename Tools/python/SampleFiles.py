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




_add_ds("trackmoverulv30lepelemv6", {
  #'example_zz_2017': (23, ['/store/user/pkotamni/ZZ_TuneCP5_13TeV-pythia8/TrackMoverULV30LepElemv6_2017/230718_134941/0000/movedtree_%i.root' % i for i in [12, 17]] + ['/store/user/pkotamni/ZZ_TuneCP5_13TeV-pythia8/TrackMoverULV30LepElemv6_2017/230717_221823/0000/movedtree_%i.root' % i for i in chain(xrange(12), xrange(13,17), xrange(18,23))]),
  'example_zz_2017': (23, ['/store/user/pkotamni/ZZ_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv6_2017/230718_065706/0000/movedtree_%i.root' % i for i in [2, 10]] + ['/store/user/pkotamni/ZZ_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv6_2017/230717_222209/0000/movedtree_%i.root' % i for i in chain(xrange(2), xrange(3,10), xrange(11,23))]),
  'example_ttbar_2017': (1, ['/store/user/pkotamni/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/TrackMoverULV30LepElemv6_2017/movedtree_0.root']),
  })


_add_ds("trackmoverulv30lepelemv6", {
'qcdempt015_2017': (38, ['/store/user/pkotamni/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepElemv6_2017/230717_221758/0000/movedtree_%i.root' % i for i in chain(xrange(4), xrange(5,34), xrange(36,41))]),
'qcdmupt15_2017': (1, ['/store/user/pkotamni/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/TrackMoverULV30LepElemv6_2017/230717_221759/0000/movedtree_0.root']),
'qcdempt020_2017': _fromnum0("/store/user/pkotamni/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepElemv6_2017/230717_221800", 96, fnbase="movedtree"),
'qcdempt030_2017': _fromnum0("/store/user/pkotamni/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepElemv6_2017/230717_221801", 67, fnbase="movedtree"),
'qcdempt050_2017': (68, ['/store/user/pkotamni/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepElemv6_2017/230718_065459/0000/movedtree_%i.root' % i for i in [5, 16, 63, 73]] + ['/store/user/pkotamni/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepElemv6_2017/230718_202010/0000/movedtree_15.root'] + ['/store/user/pkotamni/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepElemv6_2017/230719_080519/0000/movedtree_19.root'] + ['/store/user/pkotamni/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepElemv6_2017/230719_092102/0000/movedtree_%i.root' % i for i in [21, 31]] + ['/store/user/pkotamni/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepElemv6_2017/230717_221802/0000/movedtree_%i.root' % i for i in chain(xrange(5), xrange(6,9), xrange(10,12), xrange(17,19), xrange(22,30), xrange(32,52), xrange(53,63), xrange(64,73), [20])]),
'qcdempt080_2017': (67, ['/store/user/pkotamni/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepElemv6_2017/230718_134906/0000/movedtree_%i.root' % i for i in [21, 39, 51, 62, 64]] + ['/store/user/pkotamni/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepElemv6_2017/230718_183643/0000/movedtree_%i.root' % i for i in chain(xrange(11,13), xrange(52,54), [6, 16, 48, 56])] + ['/store/user/pkotamni/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepElemv6_2017/230718_065434/0000/movedtree_%i.root' % i for i in [1, 10, 60]] + ['/store/user/pkotamni/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepElemv6_2017/230717_221803/0000/movedtree_%i.root' % i for i in chain(xrange(2,6), xrange(7,10), xrange(13,15), xrange(17,21), xrange(22,31), xrange(34,39), xrange(40,48), xrange(57,60), xrange(65,68), [0, 49, 54, 61, 63])] + ['/store/user/pkotamni/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepElemv6_2017/230718_224906/0000/movedtree_%i.root' % i for i in chain(xrange(31,33), [15])] + ['/store/user/pkotamni/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepElemv6_2017/230718_202003/0000/movedtree_%i.root' % i for i in [33, 55]]),
'qcdempt120_2017': (85, ['/store/user/pkotamni/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepElemv6_2017/230718_065456/0000/movedtree_76.root'] + ['/store/user/pkotamni/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepElemv6_2017/230717_221804/0000/movedtree_%i.root' % i for i in chain(xrange(76), xrange(77,85))]),
'qcdempt170_2017': (36, ['/store/user/pkotamni/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepElemv6_2017/230717_221805/0000/movedtree_%i.root' % i for i in chain(xrange(2), xrange(3,7), xrange(8,10), xrange(11,16), xrange(17,22), xrange(24,32), [33, 35])] + ['/store/user/pkotamni/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepElemv6_2017/230718_065441/0000/movedtree_%i.root' % i for i in chain(xrange(22,24), [2, 7, 10, 16, 32, 34])]),
'qcdempt300_2017': (21, ['/store/user/pkotamni/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepElemv6_2017/230717_221806/0000/movedtree_%i.root' % i for i in chain(xrange(7), xrange(8,14), xrange(15,19), [20])] + ['/store/user/pkotamni/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepElemv6_2017/230718_183713/0000/movedtree_7.root'] + ['/store/user/pkotamni/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepElemv6_2017/230718_065455/0000/movedtree_%i.root' % i for i in [14, 19]]),
'qcdbctoept020_2017': _fromnum0("/store/user/pkotamni/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/TrackMoverULV30LepElemv6_2017/230717_221807", 89, fnbase="movedtree"),
'qcdbctoept030_2017': (77, ['/store/user/pkotamni/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/TrackMoverULV30LepElemv6_2017/230718_134921/0000/movedtree_%i.root' % i for i in chain(xrange(42,44), xrange(66,68), [4, 22, 27, 29, 35, 40, 48, 73, 77, 79])] + ['/store/user/pkotamni/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/TrackMoverULV30LepElemv6_2017/230719_092106/0000/movedtree_23.root'] + ['/store/user/pkotamni/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/TrackMoverULV30LepElemv6_2017/230718_224911/0000/movedtree_%i.root' % i for i in [17, 21, 49]] + ['/store/user/pkotamni/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/TrackMoverULV30LepElemv6_2017/230718_183659/0000/movedtree_%i.root' % i for i in chain(xrange(15,17), xrange(25,27), xrange(33,35), xrange(45,47), [1, 12, 19, 28, 36, 38, 41, 51, 53])] + ['/store/user/pkotamni/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/TrackMoverULV30LepElemv6_2017/230717_221808/0000/movedtree_%i.root' % i for i in chain(xrange(5,9), xrange(54,62), xrange(63,66), xrange(68,73), xrange(74,77), xrange(80,87), [37, 39, 44, 47, 52, 78])] + ['/store/user/pkotamni/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/TrackMoverULV30LepElemv6_2017/230718_065452/0000/movedtree_%i.root' % i for i in chain(xrange(9,11), [3, 32, 62])] + ['/store/user/pkotamni/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/TrackMoverULV30LepElemv6_2017/230718_202007/0000/movedtree_11.root']),
'qcdbctoept080_2017': (82, ['/store/user/pkotamni/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/TrackMoverULV30LepElemv6_2017/230718_134940/0000/movedtree_19.root'] + ['/store/user/pkotamni/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/TrackMoverULV30LepElemv6_2017/230717_221809/0000/movedtree_%i.root' % i for i in chain(xrange(19), xrange(20,82))]),
'qcdbctoept170_2017': _fromnum0("/store/user/pkotamni/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/TrackMoverULV30LepElemv6_2017/230717_221810", 90, fnbase="movedtree"),
'qcdbctoept250_2017': _fromnum0("/store/user/pkotamni/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/TrackMoverULV30LepElemv6_2017/230717_221811", 76, fnbase="movedtree"),
'wjetstolnu_2017': (399, ['/store/user/pkotamni/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverULV30LepElemv6_2017/230717_221817/0000/movedtree_%i.root' % i for i in chain(xrange(201), xrange(202,239), xrange(240,399))] + ['/store/user/pkotamni/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverULV30LepElemv6_2017/230718_065502/0000/movedtree_239.root'] + ['/store/user/pkotamni/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverULV30LepElemv6_2017/230718_183721/0000/movedtree_201.root']),
'wjetstolnu_amcatnlo_2017': _fromnum0("/store/user/pkotamni/WJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-pythia8/TrackMoverULV30LepElemv6_2017/230717_221818", 155, fnbase="movedtree"),
'dyjetstollM10_2017': (379, ['/store/user/pkotamni/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverULV30LepElemv6_2017/230717_221819/0000/movedtree_%i.root' % i for i in chain(xrange(12,257), xrange(258,390))] + ['/store/user/pkotamni/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverULV30LepElemv6_2017/230718_065457/0000/movedtree_257.root'] + ['/store/user/pkotamni/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverULV30LepElemv6_2017/230719_092100/0000/movedtree_11.root']),
'dyjetstollM50_2017': (433, ['/store/user/pkotamni/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverULV30LepElemv6_2017/230718_134931/0000/movedtree_%i.root' % i for i in chain(xrange(58,60), xrange(216,218), xrange(223,225), xrange(238,241), xrange(326,328), xrange(344,349), xrange(355,362), xrange(364,366), xrange(367,373), xrange(386,436), [52, 61, 68, 72, 74, 76, 93, 96, 101, 107, 112, 114, 119, 165, 173, 176, 184, 190, 195, 197, 205, 208, 212, 228, 242, 266, 280, 282, 286, 291, 295, 306, 313, 321, 334, 339, 341, 353, 375, 379])] + ['/store/user/pkotamni/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverULV30LepElemv6_2017/230717_221820/0000/movedtree_%i.root' % i for i in chain(xrange(52), xrange(53,58), xrange(62,68), xrange(69,72), xrange(77,93), xrange(94,96), xrange(97,101), xrange(102,107), xrange(108,112), xrange(115,119), xrange(120,165), xrange(166,173), xrange(174,176), xrange(177,184), xrange(185,190), xrange(191,195), xrange(198,205), xrange(206,208), xrange(209,212), xrange(213,216), xrange(218,223), xrange(225,228), xrange(229,238), xrange(243,266), xrange(267,280), xrange(283,286), xrange(287,291), xrange(292,295), xrange(296,306), xrange(307,313), xrange(314,321), xrange(322,326), xrange(328,334), xrange(335,339), xrange(342,344), xrange(362,364), xrange(373,375), xrange(376,379), xrange(380,386), [60, 73, 75, 113, 196, 241, 281, 340, 349, 354, 366])]),
'ttbar_2017': (1480, ['/store/user/pkotamni/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/TrackMoverULV30LepElemv6_2017/230718_183655/0001/movedtree_1352.root'] + ['/store/user/pkotamni/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/TrackMoverULV30LepElemv6_2017/230717_221821' + '/%04i/movedtree_%i.root' % (i/1000,i) for i in chain(xrange(69), xrange(70,230), xrange(231,253), xrange(254,347), xrange(348,460), xrange(461,581), xrange(582,869), xrange(870,1013), xrange(1014,1335), xrange(1336,1345), xrange(1346,1352), xrange(1353,1482))] + ['/store/user/pkotamni/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/TrackMoverULV30LepElemv6_2017/230718_065438' + '/%04i/movedtree_%i.root' % (i/1000,i) for i in [869, 1013]] + ['/store/user/pkotamni/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/TrackMoverULV30LepElemv6_2017/230719_080501/0000/movedtree_%i.root' % i for i in [230, 347, 581]] + ['/store/user/pkotamni/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/TrackMoverULV30LepElemv6_2017/230718_134910/0000/movedtree_253.root'] + ['/store/user/pkotamni/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/TrackMoverULV30LepElemv6_2017/230718_202004/0001/movedtree_1335.root'] + ['/store/user/pkotamni/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/TrackMoverULV30LepElemv6_2017/230718_224907/0000/movedtree_460.root']),
'ww_2017': (70, ['/store/user/pkotamni/WW_TuneCP5_13TeV-pythia8/TrackMoverULV30LepElemv6_2017/230718_134914/0000/movedtree_%i.root' % i for i in chain(xrange(2,4), xrange(17,19), xrange(66,68), xrange(75,77), xrange(81,83), [5, 9, 15, 26, 30, 45, 49, 53, 56, 64, 73, 84, 88])] + ['/store/user/pkotamni/WW_TuneCP5_13TeV-pythia8/TrackMoverULV30LepElemv6_2017/230717_221822/0000/movedtree_%i.root' % i for i in chain(xrange(7,9), xrange(10,15), xrange(19,26), xrange(28,30), xrange(33,35), xrange(37,40), xrange(41,43), xrange(50,53), xrange(60,64), xrange(68,73), xrange(86,88), xrange(89,91), [4, 16, 31, 48, 58, 74, 78, 83])]),
'zz_2017': (23, ['/store/user/pkotamni/ZZ_TuneCP5_13TeV-pythia8/TrackMoverULV30LepElemv6_2017/230718_134941/0000/movedtree_%i.root' % i for i in [12, 17]] + ['/store/user/pkotamni/ZZ_TuneCP5_13TeV-pythia8/TrackMoverULV30LepElemv6_2017/230717_221823/0000/movedtree_%i.root' % i for i in chain(xrange(12), xrange(13,17), xrange(18,23))]),
'wz_2017': _fromnum0("/store/user/pkotamni/WZ_TuneCP5_13TeV-pythia8/TrackMoverULV30LepElemv6_2017/230717_221824", 42, fnbase="movedtree"),
'SingleMuon2017B': _fromnum0("/store/user/pkotamni/SingleMuon/TrackMoverULV30LepElemv6_2017/230717_221812", 397, fnbase="movedtree"),
'SingleMuon2017C': (555, ['/store/user/pkotamni/SingleMuon/TrackMoverULV30LepElemv6_2017/230717_221813/0000/movedtree_%i.root' % i for i in chain(xrange(162), xrange(163,294), xrange(295,501), xrange(502,555))] + ['/store/user/pkotamni/SingleMuon/TrackMoverULV30LepElemv6_2017/230718_065436/0000/movedtree_%i.root' % i for i in [162, 294, 501]]),
'SingleMuon2017D': _fromnum0("/store/user/pkotamni/SingleMuon/TrackMoverULV30LepElemv6_2017/230717_221814", 227, fnbase="movedtree"),
'SingleMuon2017E': (570, ['/store/user/pkotamni/SingleMuon/TrackMoverULV30LepElemv6_2017/230719_080502/0000/movedtree_%i.root' % i for i in [461, 551]] + ['/store/user/pkotamni/SingleMuon/TrackMoverULV30LepElemv6_2017/230717_221815/0000/movedtree_%i.root' % i for i in chain(xrange(124), xrange(125,325), xrange(326,461), xrange(462,534), xrange(535,549), xrange(552,570), [550])] + ['/store/user/pkotamni/SingleMuon/TrackMoverULV30LepElemv6_2017/230718_183656/0000/movedtree_124.root'] + ['/store/user/pkotamni/SingleMuon/TrackMoverULV30LepElemv6_2017/230718_202005/0000/movedtree_549.root'] + ['/store/user/pkotamni/SingleMuon/TrackMoverULV30LepElemv6_2017/230718_065439/0000/movedtree_%i.root' % i for i in [325, 534]]),
'SingleMuon2017F': _fromnum0("/store/user/pkotamni/SingleMuon/TrackMoverULV30LepElemv6_2017/230717_221816", 854, fnbase="movedtree"),
'SingleElectron2017B': _fromnum1("/store/user/pekotamn/SingleElectron/TrackMoverULV30LepElemv6_2017/230718_031652", 200, fnbase="movedtree"),
'SingleElectron2017C': _fromnum1("/store/user/pekotamn/SingleElectron/TrackMoverULV30LepElemv6_2017/230718_031708", 408, fnbase="movedtree"),
'SingleElectron2017D': (166, ['/store/user/pkotamni/SingleElectron/TrackMoverULV30LepElemv6_2017/230719_092108/0000/movedtree_%i.root' % i for i in chain(xrange(124,126), [69, 109, 114, 117, 127, 145])] + ['/store/user/pkotamni/SingleElectron/TrackMoverULV30LepElemv6_2017/230719_080404/0000/movedtree_%i.root' % i for i in chain(xrange(69), xrange(70,109), xrange(110,114), xrange(115,117), xrange(118,124), xrange(128,145), xrange(146,166), [126])]),
'SingleElectron2017E': _fromnum1("/store/user/pekotamn/SingleElectron/TrackMoverULV30LepElemv6_2017/230718_031740", 374, fnbase="movedtree"),
'SingleElectron2017F': _fromnum1("/store/user/pekotamn/SingleElectron/TrackMoverULV30LepElemv6_2017/230718_031757", 576, fnbase="movedtree"),
})


_add_ds("trackmoverulv30lepmumv6", {
'qcdempt015_2017': (39, ['/store/user/pkotamni/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv6_2017/230717_222144/0000/movedtree_%i.root' % i for i in chain(xrange(4), xrange(5,35), xrange(36,41))]),
'qcdmupt15_2017': (1, ['/store/user/pkotamni/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv6_2017/230717_222145/0000/movedtree_0.root']),
'qcdempt020_2017': (96, ['/store/user/pkotamni/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv6_2017/230718_135049/0000/movedtree_%i.root' % i for i in chain(xrange(7,9), [21, 23, 33, 38, 68, 88])] + ['/store/user/pkotamni/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv6_2017/230717_222146/0000/movedtree_%i.root' % i for i in chain(xrange(7), xrange(9,21), xrange(24,33), xrange(34,38), xrange(39,57), xrange(58,68), xrange(69,88), xrange(89,96), [22])] + ['/store/user/pkotamni/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv6_2017/230718_225342/0000/movedtree_57.root']),
'qcdempt030_2017': (67, ['/store/user/pkotamni/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv6_2017/230718_135103/0000/movedtree_%i.root' % i for i in chain(xrange(57,59), [16, 52])] + ['/store/user/pkotamni/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv6_2017/230717_222147/0000/movedtree_%i.root' % i for i in chain(xrange(16), xrange(17,52), xrange(53,57), xrange(59,67))]),
'qcdempt050_2017': _fromnum0("/store/user/pkotamni/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv6_2017/230731_043913", 74, fnbase="movedtree"),
'qcdempt080_2017': (68, ['/store/user/pkotamni/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv6_2017/230717_222149/0000/movedtree_%i.root' % i for i in chain(xrange(2,8), xrange(21,29), xrange(33,35), xrange(51,53), [0, 9, 11, 13, 30, 36, 38, 41, 43, 45, 48, 61, 64, 67])] + ['/store/user/pkotamni/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv6_2017/230718_135056/0000/movedtree_%i.root' % i for i in chain(xrange(16,21), xrange(39,41), xrange(46,48), xrange(49,51), xrange(53,61), xrange(62,64), xrange(65,67), [1, 10, 14, 29, 35, 37, 42, 44])] + ['/store/user/pkotamni/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv6_2017/230718_183549/0000/movedtree_%i.root' % i for i in chain(xrange(31,33), [8, 12, 15])]),
'qcdempt120_2017': (85, ['/store/user/pkotamni/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv6_2017/230717_222150/0000/movedtree_%i.root' % i for i in chain(xrange(25,27), xrange(32,37), xrange(42,44), xrange(47,49), xrange(80,84), [4])] + ['/store/user/pkotamni/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv6_2017/230718_135052/0000/movedtree_%i.root' % i for i in chain(xrange(4), xrange(5,25), xrange(27,32), xrange(37,42), xrange(44,47), xrange(49,80), [84])]),
'qcdempt170_2017': (36, ['/store/user/pkotamni/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv6_2017/230717_222151/0000/movedtree_%i.root' % i for i in chain(xrange(8,11), xrange(14,19), xrange(20,22), xrange(31,33), [0, 6, 25, 27])] + ['/store/user/pkotamni/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv6_2017/230718_135107/0000/movedtree_%i.root' % i for i in chain(xrange(1,6), xrange(11,14), xrange(22,25), xrange(28,31), xrange(33,36), [7, 19, 26])]),
'qcdempt300_2017': (21, ['/store/user/pkotamni/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv6_2017/230718_135105/0000/movedtree_%i.root' % i for i in [1, 5, 10, 14, 19]] + ['/store/user/pkotamni/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv6_2017/230717_222152/0000/movedtree_%i.root' % i for i in chain(xrange(2,5), xrange(6,10), xrange(11,14), xrange(15,19), [0, 20])]),
'qcdbctoept020_2017': _fromnum0("/store/user/pkotamni/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/TrackMoverULV30LepMumv6_2017/230717_222153", 89, fnbase="movedtree"),
'qcdbctoept030_2017': (87, ['/store/user/pkotamni/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/TrackMoverULV30LepMumv6_2017/230717_222154/0000/movedtree_%i.root' % i for i in chain(xrange(9), xrange(10,13), xrange(14,19), xrange(22,36), xrange(37,87), [20])] + ['/store/user/pkotamni/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/TrackMoverULV30LepMumv6_2017/230718_135050/0000/movedtree_%i.root' % i for i in [9, 19, 21, 36]] + ['/store/user/pkotamni/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/TrackMoverULV30LepMumv6_2017/230718_183551/0000/movedtree_13.root']),
'qcdbctoept080_2017': (82, ['/store/user/pkotamni/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/TrackMoverULV30LepMumv6_2017/230718_135055/0000/movedtree_19.root'] + ['/store/user/pkotamni/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/TrackMoverULV30LepMumv6_2017/230717_222155/0000/movedtree_%i.root' % i for i in chain(xrange(19), xrange(20,82))]),
'qcdbctoept170_2017': (90, ['/store/user/pkotamni/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/TrackMoverULV30LepMumv6_2017/230718_065655/0000/movedtree_%i.root' % i for i in [1, 5, 39, 41]] + ['/store/user/pkotamni/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/TrackMoverULV30LepMumv6_2017/230717_222156/0000/movedtree_%i.root' % i for i in chain(xrange(2,5), xrange(6,39), xrange(42,90), [0, 40])]),
'qcdbctoept250_2017': _fromnum0("/store/user/pkotamni/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/TrackMoverULV30LepMumv6_2017/230717_222157", 76, fnbase="movedtree"),
'wjetstolnu_2017': _fromnum0("/store/user/pkotamni/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverULV30LepMumv6_2017/230717_222203", 399, fnbase="movedtree"),
'wjetstolnu_amcatnlo_2017': _fromnum0("/store/user/pkotamni/WJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-pythia8/TrackMoverULV30LepMumv6_2017/230717_222204", 155, fnbase="movedtree"),
'dyjetstollM10_2017': (379, ['/store/user/pkotamni/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverULV30LepMumv6_2017/230730_115645/0000/movedtree_%i.root' % i for i in chain(xrange(12,390), [6])]),
'dyjetstollM50_2017': (433, ['/store/user/pkotamni/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverULV30LepMumv6_2017/230731_043430/0000/movedtree_%i.root' % i for i in chain(xrange(97,99), xrange(123,127), xrange(133,136), xrange(156,159), xrange(186,189), xrange(295,299), xrange(324,326), xrange(341,343), xrange(364,367), [1, 14, 29, 35, 94, 101, 137, 143, 161, 199, 224, 229, 237, 241, 270, 315, 332, 334, 336, 368])] + ['/store/user/pkotamni/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverULV30LepMumv6_2017/230730_115646/0000/movedtree_%i.root' % i for i in chain(xrange(2,14), xrange(15,29), xrange(30,35), xrange(36,94), xrange(95,97), xrange(99,101), xrange(102,123), xrange(127,133), xrange(138,143), xrange(144,156), xrange(159,161), xrange(162,186), xrange(189,199), xrange(200,224), xrange(225,229), xrange(230,237), xrange(238,241), xrange(242,270), xrange(271,295), xrange(299,315), xrange(316,324), xrange(326,332), xrange(337,341), xrange(343,350), xrange(352,364), xrange(369,373), xrange(374,436), [0, 136, 333, 335, 367])]),
'ttbar_2017': (1479, ['/store/user/pkotamni/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/TrackMoverULV30LepMumv6_2017/230717_222207' + '/%04i/movedtree_%i.root' % (i/1000,i) for i in chain(xrange(68), xrange(69,232), xrange(233,253), xrange(254,347), xrange(348,647), xrange(648,655), xrange(656,668), xrange(669,679), xrange(681,687), xrange(688,693), xrange(694,703), xrange(704,709), xrange(710,717), xrange(718,721), xrange(722,726), xrange(727,735), xrange(736,738), xrange(739,742), xrange(752,755), xrange(762,764), xrange(769,772), xrange(780,783), xrange(785,787), xrange(794,796), xrange(805,807), xrange(822,825), xrange(826,830), xrange(831,834), xrange(835,869), xrange(870,1345), xrange(1346,1482), [746, 748, 766, 773, 776, 790, 792, 797, 799, 801, 809, 813, 818, 820])] + ['/store/user/pkotamni/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/TrackMoverULV30LepMumv6_2017/230719_080039/0001/movedtree_1345.root'] + ['/store/user/pkotamni/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/TrackMoverULV30LepMumv6_2017/230718_135100/0000/movedtree_%i.root' % i for i in chain(xrange(679,681), xrange(742,746), xrange(749,752), xrange(755,762), xrange(764,766), xrange(767,769), xrange(774,776), xrange(777,780), xrange(783,785), xrange(787,790), xrange(802,805), xrange(807,809), xrange(810,813), xrange(814,818), [647, 655, 668, 687, 693, 703, 709, 717, 721, 726, 735, 738, 747, 772, 791, 793, 796, 798, 800, 819, 821, 825, 830, 834])] + ['/store/user/pkotamni/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/TrackMoverULV30LepMumv6_2017/230718_183552/0000/movedtree_347.root'] + ['/store/user/pkotamni/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/TrackMoverULV30LepMumv6_2017/230718_202030/0000/movedtree_869.root']),
'ww_2017': (70, ['/store/user/pkotamni/WW_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv6_2017/230730_115648/0000/movedtree_%i.root' % i for i in chain(xrange(2,6), xrange(7,27), xrange(28,32), xrange(35,37), xrange(38,41), xrange(42,44), xrange(48,54), xrange(60,64), xrange(66,77), xrange(81,86), xrange(87,91), [33, 45, 56, 58, 78])]),
'zz_2017': (23, ['/store/user/pkotamni/ZZ_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv6_2017/230718_065706/0000/movedtree_%i.root' % i for i in [2, 10]] + ['/store/user/pkotamni/ZZ_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv6_2017/230717_222209/0000/movedtree_%i.root' % i for i in chain(xrange(2), xrange(3,10), xrange(11,23))]),
'wz_2017': _fromnum0("/store/user/pkotamni/WZ_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv6_2017/230717_222210", 42, fnbase="movedtree"),
'SingleMuon2017B': _fromnum0("/store/user/pkotamni/SingleMuon/TrackMoverULV30LepMumv6_2017/230717_222158", 397, fnbase="movedtree"),
'SingleMuon2017C': (555, ['/store/user/pkotamni/SingleMuon/TrackMoverULV30LepMumv6_2017/230718_065656/0000/movedtree_%i.root' % i for i in chain(xrange(3,5), xrange(125,127), xrange(134,136), xrange(155,158), xrange(160,162), xrange(186,189), xrange(256,258), xrange(295,298), xrange(353,355), xrange(358,360), xrange(383,385), xrange(527,529), [6, 9, 12, 35, 41, 54, 65, 82, 94, 98, 100, 105, 129, 139, 150, 164, 178, 183, 200, 206, 211, 214, 227, 232, 242, 244, 246, 248, 250, 266, 269, 280, 283, 285, 291, 301, 321, 324, 327, 332, 335, 339, 341, 344, 351, 361, 370, 372, 374, 376, 402, 408, 429, 454, 457, 474, 492, 512, 521, 525, 534, 536, 542, 552])] + ['/store/user/pkotamni/SingleMuon/TrackMoverULV30LepMumv6_2017/230718_135041/0000/movedtree_%i.root' % i for i in chain(xrange(143,145), xrange(194,197), xrange(349,351), [1, 80, 102, 108, 114, 116, 136, 148, 159, 168, 177, 182, 208, 249, 258, 265, 271, 287, 289, 316, 328, 336, 345, 382, 387, 390, 405, 416, 431, 445, 471, 478, 480, 495, 505, 516, 535, 539, 549, 553])] + ['/store/user/pkotamni/SingleMuon/TrackMoverULV30LepMumv6_2017/230718_183544/0000/movedtree_%i.root' % i for i in chain(xrange(21,24), xrange(26,28), xrange(106,108), xrange(303,305), xrange(337,339), xrange(355,358), xrange(378,380), xrange(435,437), xrange(522,525), [15, 38, 52, 71, 84, 96, 101, 119, 128, 131, 140, 142, 145, 174, 202, 220, 243, 260, 279, 299, 330, 343, 348, 352, 363, 371, 373, 393, 407, 426, 432, 444, 450, 475, 479, 481, 483, 486, 488, 491, 496, 500, 511, 518, 538, 543])] + ['/store/user/pkotamni/SingleMuon/TrackMoverULV30LepMumv6_2017/230717_222159/0000/movedtree_%i.root' % i for i in chain(xrange(7,9), xrange(10,12), xrange(13,15), xrange(16,21), xrange(24,26), xrange(28,35), xrange(36,38), xrange(39,41), xrange(42,52), xrange(55,65), xrange(66,71), xrange(72,80), xrange(85,94), xrange(103,105), xrange(109,114), xrange(117,119), xrange(120,125), xrange(132,134), xrange(137,139), xrange(146,148), xrange(151,155), xrange(162,164), xrange(165,168), xrange(169,174), xrange(175,177), xrange(179,182), xrange(184,186), xrange(189,194), xrange(197,200), xrange(203,206), xrange(209,211), xrange(212,214), xrange(215,220), xrange(221,227), xrange(228,232), xrange(233,242), xrange(251,256), xrange(261,265), xrange(267,269), xrange(272,279), xrange(281,283), xrange(292,295), xrange(305,316), xrange(317,321), xrange(322,324), xrange(325,327), xrange(333,335), xrange(346,348), xrange(364,370), xrange(380,382), xrange(385,387), xrange(388,390), xrange(391,393), xrange(394,402), xrange(403,405), xrange(409,416), xrange(417,426), xrange(427,429), xrange(433,435), xrange(437,444), xrange(446,450), xrange(451,454), xrange(455,457), xrange(458,471), xrange(472,474), xrange(476,478), xrange(484,486), xrange(489,491), xrange(493,495), xrange(497,500), xrange(501,505), xrange(506,511), xrange(513,516), xrange(519,521), xrange(529,534), xrange(540,542), xrange(544,549), xrange(550,552), [0, 2, 5, 53, 81, 83, 95, 97, 99, 115, 127, 130, 141, 149, 158, 201, 207, 245, 247, 259, 270, 284, 286, 288, 290, 298, 300, 302, 329, 331, 340, 342, 360, 362, 375, 377, 406, 430, 482, 487, 517, 526, 537, 554])]),
'SingleMuon2017D': (227, ['/store/user/pkotamni/SingleMuon/TrackMoverULV30LepMumv6_2017/230718_135048/0000/movedtree_173.root'] + ['/store/user/pkotamni/SingleMuon/TrackMoverULV30LepMumv6_2017/230717_222200/0000/movedtree_%i.root' % i for i in chain(xrange(173), xrange(174,227))]),
'SingleMuon2017E': (564, ['/store/user/pkotamni/SingleMuon/TrackMoverULV30LepMumv6_2017/230730_115543/0000/movedtree_%i.root' % i for i in chain(xrange(13), xrange(14,240), xrange(243,276), xrange(277,333), xrange(334,502), xrange(503,570), [241])]),
'SingleMuon2017F': (854, ['/store/user/pkotamni/SingleMuon/TrackMoverULV30LepMumv6_2017/230717_222202/0000/movedtree_%i.root' % i for i in chain(xrange(14), xrange(15,362), xrange(363,465), xrange(466,854))] + ['/store/user/pkotamni/SingleMuon/TrackMoverULV30LepMumv6_2017/230718_065702/0000/movedtree_%i.root' % i for i in [14, 362, 465]]),
'SingleElectron2017B': _fromnum1("/store/user/pekotamn/SingleElectron/TrackMoverULV30LepMumv6_2017/230718_032038", 200, fnbase="movedtree"),
'SingleElectron2017C': _fromnum1("/store/user/pekotamn/SingleElectron/TrackMoverULV30LepMumv6_2017/230718_032054", 408, fnbase="movedtree"),
'SingleElectron2017D': _fromnum0("/store/user/pkotamni/SingleElectron/TrackMoverULV30LepMumv6_2017/230730_115545", 166, fnbase="movedtree"),
'SingleElectron2017F': _fromnum1("/store/user/pekotamn/SingleElectron/TrackMoverULV30LepMumv6_2017/230718_032143", 576, fnbase="movedtree"),
})


_add_ds("trackmovermctruthulv30mv7", {
'WplusHToSSTodddd_tau1mm_M55_2017': _fromnum1("/store/user/pekotamn/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/TrackMoverMCTruthULV30LepMumv7_2017/230901_162445", 50, fnbase="mctruth"),
'WplusHToSSTodddd_tau1mm_M15_2017': _fromnum1("/store/user/pekotamn/WplusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-1_TuneCP5_13TeV-powheg-pythia8/TrackMoverMCTruthULV30LepMumv7_2017/230901_162407", 50, fnbase="mctruth"),
})


_add_ds("trackmovermctruthulv30lepmumv7", {
'WplusHToSSTodddd_tau1mm_M55_2017': _fromnum1("/store/user/pekotamn/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/TrackMoverMCTruthULV30LepMumv7_2017/230901_193542", 50, fnbase="mctruth"),
'WplusHToSSTodddd_tau1mm_M15_2017': _fromnum1("/store/user/pekotamn/WplusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-1_TuneCP5_13TeV-powheg-pythia8/TrackMoverMCTruthULV30LepMumv7_2017/230901_193632", 50, fnbase="mctruth"),
})


_add_ds("trackmovermctruthulv30lepelemv7", {
'WplusHToSSTodddd_tau1mm_M55_2017': _fromnum1("/store/user/pekotamn/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/TrackMoverMCTruthULV30LepElemv7_2017/230902_151317", 50, fnbase="mctruth"),
'WplusHToSSTodddd_tau1mm_M15_2017': _fromnum1("/store/user/pekotamn/WplusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-1_TuneCP5_13TeV-powheg-pythia8/TrackMoverMCTruthULV30LepElemv7_2017/230902_151234", 50, fnbase="mctruth"),
})

_add_ds("trackmoverulv30lepelemv7", {
'qcdmupt15_2017': (1, ['/store/user/pkotamni/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/TrackMoverULV30LepElemv7_2017/230816_084846/0000/movedtree_0.root']),
'qcdempt015_2017': (38, ['/store/user/pkotamni/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepElemv7_2017/230816_084859/0000/movedtree_%i.root' % i for i in chain(xrange(4), xrange(5,28), xrange(29,35), xrange(36,38), [39])] + ['/store/user/pkotamni/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepElemv7_2017/230817_134440/0000/movedtree_28.root'] + ['/store/user/pkotamni/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepElemv7_2017/230817_154006/0000/movedtree_38.root']),
'qcdempt020_2017': (96, ['/store/user/pkotamni/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepElemv7_2017/230816_084900/0000/movedtree_%i.root' % i for i in chain(xrange(1,5), xrange(6,19), xrange(20,44), xrange(45,83), xrange(85,96))] + ['/store/user/pkotamni/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepElemv7_2017/230817_134406/0000/movedtree_%i.root' % i for i in chain(xrange(83,85), [0, 5, 44])] + ['/store/user/pkotamni/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepElemv7_2017/230817_154005/0000/movedtree_19.root']),
'qcdempt030_2017': (67, ['/store/user/pkotamni/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepElemv7_2017/230816_084901/0000/movedtree_%i.root' % i for i in chain(xrange(28), xrange(29,67))] + ['/store/user/pkotamni/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepElemv7_2017/230817_134405/0000/movedtree_28.root']),
'qcdempt050_2017': (74, ['/store/user/pkotamni/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepElemv7_2017/230816_084902/0000/movedtree_%i.root' % i for i in chain(xrange(25), xrange(26,46), xrange(47,50), xrange(51,59), xrange(60,74))] + ['/store/user/pkotamni/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepElemv7_2017/230817_134430/0000/movedtree_%i.root' % i for i in [25, 46, 50, 59]]),
'qcdempt080_2017': (68, ['/store/user/pkotamni/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepElemv7_2017/230817_134443/0000/movedtree_14.root'] + ['/store/user/pkotamni/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepElemv7_2017/230816_084903/0000/movedtree_%i.root' % i for i in chain(xrange(14), xrange(15,68))]),
'qcdempt120_2017': (85, ['/store/user/pkotamni/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepElemv7_2017/230817_154004/0000/movedtree_1.root'] + ['/store/user/pkotamni/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepElemv7_2017/230817_134431/0000/movedtree_10.root'] + ['/store/user/pkotamni/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepElemv7_2017/230816_084904/0000/movedtree_%i.root' % i for i in chain(xrange(2,10), xrange(11,85), [0])]),
'qcdempt170_2017': (32, ['/store/user/pkotamni/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepElemv7_2017/230817_134449/0000/movedtree_7.root'] + ['/store/user/pkotamni/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepElemv7_2017/230816_084905/0000/movedtree_%i.root' % i for i in chain(xrange(3), xrange(4,7), xrange(8,26), xrange(29,35), [27])]),
'qcdempt300_2017': (20, ['/store/user/pkotamni/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepElemv7_2017/230816_084906/0000/movedtree_%i.root' % i for i in chain(xrange(2,5), xrange(6,10), xrange(12,21), [0])] + ['/store/user/pkotamni/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepElemv7_2017/230817_154000/0000/movedtree_5.root'] + ['/store/user/pkotamni/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepElemv7_2017/230817_134404/0000/movedtree_%i.root' % i for i in xrange(10,12)]),
'qcdbctoept020_2017': _fromnum0("/store/user/pkotamni/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/TrackMoverULV30LepElemv7_2017/230816_084907", 89, fnbase="movedtree"),
'qcdbctoept030_2017': (87, ['/store/user/pkotamni/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/TrackMoverULV30LepElemv7_2017/230816_084908/0000/movedtree_%i.root' % i for i in chain(xrange(2,5), xrange(6,87), [0])] + ['/store/user/pkotamni/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/TrackMoverULV30LepElemv7_2017/230817_134452/0000/movedtree_%i.root' % i for i in [1, 5]]),
'qcdbctoept080_2017': (82, ['/store/user/pkotamni/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/TrackMoverULV30LepElemv7_2017/230816_084909/0000/movedtree_%i.root' % i for i in chain(xrange(2,30), xrange(31,72), xrange(73,82), [0])] + ['/store/user/pkotamni/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/TrackMoverULV30LepElemv7_2017/230817_134444/0000/movedtree_%i.root' % i for i in [1, 30, 72]]),
'qcdbctoept170_2017': (90, ['/store/user/pkotamni/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/TrackMoverULV30LepElemv7_2017/230817_134441/0000/movedtree_33.root'] + ['/store/user/pkotamni/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/TrackMoverULV30LepElemv7_2017/230816_084910/0000/movedtree_%i.root' % i for i in chain(xrange(33), xrange(34,90))]),
'qcdbctoept250_2017': (76, ['/store/user/pkotamni/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/TrackMoverULV30LepElemv7_2017/230816_084911/0000/movedtree_%i.root' % i for i in chain(xrange(2,6), xrange(7,14), xrange(15,76), [0])] + ['/store/user/pkotamni/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/TrackMoverULV30LepElemv7_2017/230817_134448/0000/movedtree_%i.root' % i for i in [1, 6, 14]]),
'wjetstolnu_2017': (399, ['/store/user/pkotamni/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverULV30LepElemv7_2017/230817_134451/0000/movedtree_%i.root' % i for i in chain(xrange(297,299), [71, 117, 260, 331, 375])] + ['/store/user/pkotamni/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverULV30LepElemv7_2017/230816_084918/0000/movedtree_%i.root' % i for i in chain(xrange(71), xrange(72,117), xrange(118,260), xrange(261,297), xrange(299,331), xrange(332,375), xrange(376,399))]),
'wjetstolnu_amcatnlo_2017': (146, ['/store/user/pkotamni/WJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-pythia8/TrackMoverULV30LepElemv7_2017/230816_084919/0000/movedtree_%i.root' % i for i in chain(xrange(9,12), xrange(21,25), xrange(30,38), xrange(76,78), xrange(101,130), xrange(131,133), xrange(134,148), [67, 84, 151])] + ['/store/user/pkotamni/WJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-pythia8/TrackMoverULV30LepElemv7_2017/230817_134445/0000/movedtree_%i.root' % i for i in chain(xrange(9), xrange(13,21), xrange(38,53), xrange(54,59), xrange(62,67), xrange(68,76), xrange(78,82), xrange(85,95), xrange(96,101), xrange(148,151), [60, 83, 133])] + ['/store/user/pkotamni/WJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-pythia8/TrackMoverULV30LepElemv7_2017/230817_154011/0000/movedtree_%i.root' % i for i in [12, 53, 59, 61, 82, 95]]),
'dyjetstollM10_2017': (376, ['/store/user/pkotamni/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverULV30LepElemv7_2017/230816_084920/0000/movedtree_%i.root' % i for i in chain(xrange(13,22), xrange(23,26), xrange(27,44), xrange(45,70), xrange(71,110), xrange(111,165), xrange(166,175), xrange(178,185), xrange(186,206), xrange(207,213), xrange(214,218), xrange(219,223), xrange(224,234), xrange(235,389), [176])] + ['/store/user/pkotamni/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverULV30LepElemv7_2017/230817_154009/0000/movedtree_%i.root' % i for i in [26, 70]] + ['/store/user/pkotamni/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverULV30LepElemv7_2017/230817_134428/0000/movedtree_%i.root' % i for i in [12, 22, 44, 110, 165, 175, 185, 206, 213, 218, 223, 234]]),
'dyjetstollM50_2017': (432, ['/store/user/pkotamni/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverULV30LepElemv7_2017/230816_084921/0000/movedtree_%i.root' % i for i in chain(xrange(5), xrange(6,9), xrange(10,29), xrange(30,78), xrange(79,91), xrange(92,94), xrange(95,108), xrange(109,126), xrange(127,165), xrange(166,168), xrange(169,173), xrange(174,182), xrange(183,189), xrange(190,203), xrange(204,210), xrange(211,229), xrange(231,298), xrange(300,350), xrange(355,369), xrange(370,372), xrange(374,386), xrange(387,399), xrange(400,415), xrange(416,421), xrange(422,436), [353])] + ['/store/user/pkotamni/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverULV30LepElemv7_2017/230817_154007/0000/movedtree_91.root'] + ['/store/user/pkotamni/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverULV30LepElemv7_2017/230817_134453/0000/movedtree_%i.root' % i for i in chain(xrange(229,231), [5, 9, 29, 78, 94, 108, 126, 165, 168, 173, 182, 189, 203, 210, 298, 352, 354, 369, 372, 386, 399, 415, 421])]),
'ttbar_2017': (1481, ['/store/user/pkotamni/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/TrackMoverULV30LepElemv7_2017/230817_134433' + '/%04i/movedtree_%i.root' % (i/1000,i) for i in chain(xrange(753,755), [13, 28, 84, 87, 112, 160, 204, 226, 276, 339, 429, 500, 504, 514, 543, 571, 626, 656, 677, 695, 751, 762, 792, 820, 828, 836, 865, 869, 895, 910, 931, 936, 940, 959, 967, 1002, 1009, 1033, 1045, 1088, 1091, 1192, 1248, 1250, 1271, 1281, 1350, 1385, 1411, 1437])] + ['/store/user/pkotamni/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/TrackMoverULV30LepElemv7_2017/230816_084922' + '/%04i/movedtree_%i.root' % (i/1000,i) for i in chain(xrange(13), xrange(14,28), xrange(29,68), xrange(69,84), xrange(85,87), xrange(88,112), xrange(113,160), xrange(161,204), xrange(205,226), xrange(227,276), xrange(277,339), xrange(340,429), xrange(430,491), xrange(492,500), xrange(501,504), xrange(505,514), xrange(515,543), xrange(544,551), xrange(552,571), xrange(572,626), xrange(627,656), xrange(657,677), xrange(678,695), xrange(696,751), xrange(755,762), xrange(763,792), xrange(793,820), xrange(821,828), xrange(829,836), xrange(837,865), xrange(866,869), xrange(870,895), xrange(896,910), xrange(911,931), xrange(932,936), xrange(937,940), xrange(941,959), xrange(960,967), xrange(968,1002), xrange(1003,1009), xrange(1010,1033), xrange(1034,1045), xrange(1046,1088), xrange(1089,1091), xrange(1092,1192), xrange(1193,1248), xrange(1251,1271), xrange(1272,1281), xrange(1282,1350), xrange(1351,1385), xrange(1386,1411), xrange(1412,1437), xrange(1438,1482), [752, 1249])] + ['/store/user/pkotamni/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/TrackMoverULV30LepElemv7_2017/230817_154008/0000/movedtree_%i.root' % i for i in [491, 551]]),
'ww_2017': (70, ['/store/user/pkotamni/WW_TuneCP5_13TeV-pythia8/TrackMoverULV30LepElemv7_2017/230817_134437/0000/movedtree_%i.root' % i for i in [24, 31, 37, 51, 90]] + ['/store/user/pkotamni/WW_TuneCP5_13TeV-pythia8/TrackMoverULV30LepElemv7_2017/230816_084923/0000/movedtree_%i.root' % i for i in chain(xrange(2,6), xrange(7,24), xrange(25,27), xrange(28,31), xrange(33,35), xrange(41,44), xrange(48,51), xrange(52,54), xrange(60,64), xrange(66,77), xrange(81,86), xrange(87,90), [36, 39, 45, 56, 58, 78])]),
'zz_2017': _fromnum0("/store/user/pkotamni/ZZ_TuneCP5_13TeV-pythia8/TrackMoverULV30LepElemv7_2017/230816_084924", 23, fnbase="movedtree"),
'wz_2017': (42, ['/store/user/pkotamni/WZ_TuneCP5_13TeV-pythia8/TrackMoverULV30LepElemv7_2017/230816_084925/0000/movedtree_%i.root' % i for i in chain(xrange(1,16), xrange(17,19), xrange(20,29), xrange(30,42))] + ['/store/user/pkotamni/WZ_TuneCP5_13TeV-pythia8/TrackMoverULV30LepElemv7_2017/230817_134436/0000/movedtree_%i.root' % i for i in [0, 16, 19, 29]]),
'SingleElectron2017B': _fromnum1("/store/user/pekotamn/SingleElectron/TrackMoverULV30LepElemv7_2017/230816_134738", 200, fnbase="movedtree"),
'SingleElectron2017C': _fromnum1("/store/user/pekotamn/SingleElectron/TrackMoverULV30LepElemv7_2017/230816_134800", 408, fnbase="movedtree"),
'SingleElectron2017D': (166, ['/store/user/pkotamni/SingleElectron/TrackMoverULV30LepElemv7_2017/230817_134439/0000/movedtree_%i.root' % i for i in [41, 103, 139]] + ['/store/user/pkotamni/SingleElectron/TrackMoverULV30LepElemv7_2017/230816_084917/0000/movedtree_%i.root' % i for i in chain(xrange(41), xrange(42,103), xrange(104,139), xrange(140,166))]),
'SingleElectron2017E': _fromnum1("/store/user/pekotamn/SingleElectron/TrackMoverULV30LepElemv7_2017/230816_134823", 374, fnbase="movedtree"),
'SingleElectron2017F': _fromnum1("/store/user/pekotamn/SingleElectron/TrackMoverULV30LepElemv7_2017/230816_134845", 576, fnbase="movedtree"),
})


_add_ds("trackmoverulv30lepmumv8", {
'qcdpt120mupt5_2017': (183, ['/store/user/pkotamni/QCD_Pt-120To170_MuEnrichedPt5_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv8_2017/230822_101818/0000/movedtree_%i.root' % i for i in chain(xrange(17), xrange(18,24), xrange(25,34), xrange(35,60), xrange(61,63), xrange(64,82), xrange(83,91), xrange(92,94), xrange(104,107), xrange(109,118), xrange(119,127), xrange(131,137), xrange(154,160), xrange(161,172), xrange(173,189), xrange(190,196), xrange(204,207), xrange(208,210), xrange(213,225), xrange(226,229), xrange(230,238), [146, 211, 243])]),
})

_add_ds("trackmoverulv30lepmumv9", {
'qcdpt120mupt5_2017': (194, ['/store/user/pkotamni/QCD_Pt-120To170_MuEnrichedPt5_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv9_2017/230822_131215/0000/movedtree_%i.root' % i for i in chain(xrange(13), xrange(14,16), xrange(19,68), xrange(69,94), xrange(104,109), xrange(110,126), xrange(128,137), xrange(154,184), xrange(185,196), xrange(204,229), xrange(230,234), xrange(235,238), [146, 243])]),
})

_add_ds("trackmoverulv30lepmumv7", {
'qcdempt015_2017': (37, ['/store/user/pkotamni/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv7_2017/230804_055324/0000/movedtree_%i.root' % i for i in chain(xrange(4), xrange(5,34), xrange(38,41), [36])]),
'qcdmupt15_2017': (1, ['/store/user/pkotamni/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv7_2017/230804_032220/0000/movedtree_0.root']),
'qcdpt15mupt5_2017': (29, ['/store/user/pkotamni/QCD_Pt-15To20_MuEnrichedPt5_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv7_2017/230813_092703/0000/movedtree_%i.root' % i for i in chain(xrange(11), xrange(12,16), xrange(17,31))]),
'qcdpt20mupt5_2017': (196, ['/store/user/pkotamni/QCD_Pt-20To30_MuEnrichedPt5_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv7_2017/230813_092704/0000/movedtree_%i.root' % i for i in chain(xrange(123), xrange(135,158), xrange(159,177), xrange(178,197), xrange(202,214), [129])]),
'qcdpt30mupt5_2017': (297, ['/store/user/pkotamni/QCD_Pt-30To50_MuEnrichedPt5_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv7_2017/230813_092705/0000/movedtree_%i.root' % i for i in chain(xrange(46), xrange(48,70), xrange(76,210), xrange(211,239), xrange(240,252), xrange(254,265), xrange(272,293), xrange(334,338), xrange(339,357), [74])]),
'qcdpt50mupt5_2017': (227, ['/store/user/pkotamni/QCD_Pt-50To80_MuEnrichedPt5_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv7_2017/230813_092706/0000/movedtree_%i.root' % i for i in chain(xrange(7), xrange(8,55), xrange(56,73), xrange(74,97), xrange(98,107), xrange(108,117), xrange(118,162), xrange(163,175), xrange(177,179), xrange(180,182), xrange(183,190), xrange(191,197), xrange(198,240))]),
'qcdpt80mupt5_2017': (270, ['/store/user/pkotamni/QCD_Pt-80To120_MuEnrichedPt5_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv7_2017/230813_092707/0000/movedtree_%i.root' % i for i in chain(xrange(1,105), xrange(107,147), xrange(151,277))]),
'qcdpt120mupt5_2017': (207, ['/store/user/pkotamni/QCD_Pt-120To170_MuEnrichedPt5_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv7_2017/230811_101041/0000/movedtree_%i.root' % i for i in chain(xrange(17), xrange(18,97), xrange(104,127), xrange(128,138), xrange(154,196), xrange(204,238), [146, 243])]),
'qcdpt170mupt5_2017': (433, ['/store/user/pkotamni/QCD_Pt-170To300_MuEnrichedPt5_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv7_2017/230811_075009/0000/movedtree_%i.root' % i for i in chain(xrange(2), xrange(3,210), xrange(213,272), xrange(282,447))]),
'qcdpt300mupt5_2017': _fromnum0("/store/user/pkotamni/QCD_Pt-300To470_MuEnrichedPt5_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv7_2017/230811_075010", 360, fnbase="movedtree"),
'qcdpt470mupt5_2017': _fromnum0("/store/user/pkotamni/QCD_Pt-470To600_MuEnrichedPt5_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv7_2017/230811_075011", 242, fnbase="movedtree"),
'qcdpt600mupt5_2017': (234, ['/store/user/pkotamni/QCD_Pt-600To800_MuEnrichedPt5_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv7_2017/230811_075012/0000/movedtree_%i.root' % i for i in chain(xrange(165), xrange(173,242))]),
'qcdpt800mupt5_2017': _fromnum0("/store/user/pkotamni/QCD_Pt-800To1000_MuEnrichedPt5_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv7_2017/230811_075013", 484, fnbase="movedtree"),
'qcdpt1000mupt5_2017': _fromnum0("/store/user/pkotamni/QCD_Pt-1000_MuEnrichedPt5_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv7_2017/230811_075014", 172, fnbase="movedtree"),
'qcdempt020_2017': (96, ['/store/user/pkotamni/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv7_2017/230804_055326/0000/movedtree_%i.root' % i for i in chain(xrange(57), xrange(58,96))] + ['/store/user/pkotamni/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv7_2017/230804_123844/0000/movedtree_57.root']),
'qcdempt030_2017': _fromnum0("/store/user/pkotamni/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv7_2017/230804_055327", 67, fnbase="movedtree"),
'qcdempt050_2017': _fromnum0("/store/user/pkotamni/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv7_2017/230804_055328", 74, fnbase="movedtree"),
'qcdempt080_2017': (68, ['/store/user/pkotamni/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv7_2017/230804_123839/0000/movedtree_%i.root' % i for i in [5, 31, 57]] + ['/store/user/pkotamni/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv7_2017/230804_055329/0000/movedtree_%i.root' % i for i in chain(xrange(5), xrange(7,13), xrange(14,17), xrange(18,21), xrange(22,29), xrange(33,49), xrange(50,55), xrange(58,68), [30, 56])] + ['/store/user/pkotamni/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv7_2017/230806_024308/0000/movedtree_%i.root' % i for i in [6, 13, 17, 21, 29, 32, 49, 55]]),
'qcdempt120_2017': (85, ['/store/user/pkotamni/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv7_2017/230804_123835/0000/movedtree_%i.root' % i for i in [46, 61, 71, 83]] + ['/store/user/pkotamni/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv7_2017/230804_055330/0000/movedtree_%i.root' % i for i in chain(xrange(46), xrange(47,61), xrange(62,71), xrange(72,83), [84])]),
'qcdempt170_2017': (34, ['/store/user/pkotamni/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv7_2017/230804_055331/0000/movedtree_%i.root' % i for i in chain(xrange(2), xrange(3,28), xrange(29,36))]),
'qcdempt300_2017': _fromnum0("/store/user/pkotamni/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv7_2017/230804_055332", 21, fnbase="movedtree"),
'qcdbctoept020_2017': _fromnum0("/store/user/pkotamni/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/TrackMoverULV30LepMumv7_2017/230804_055333", 89, fnbase="movedtree"),
'qcdbctoept030_2017': (87, ['/store/user/pkotamni/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/TrackMoverULV30LepMumv7_2017/230806_024307/0000/movedtree_%i.root' % i for i in [12, 22]] + ['/store/user/pkotamni/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/TrackMoverULV30LepMumv7_2017/230804_055334/0000/movedtree_%i.root' % i for i in chain(xrange(12), xrange(13,22), xrange(23,87))]),
'qcdbctoept080_2017': _fromnum0("/store/user/pkotamni/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/TrackMoverULV30LepMumv7_2017/230804_055335", 82, fnbase="movedtree"),
'qcdbctoept170_2017': _fromnum0("/store/user/pkotamni/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/TrackMoverULV30LepMumv7_2017/230804_055336", 90, fnbase="movedtree"),
'qcdbctoept250_2017': _fromnum1("/store/user/pekotamn/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/TrackMoverULV30LepMumv7_2017/230806_165105", 32, fnbase="movedtree"),
'wjetstolnu_2017': (399, ['/store/user/pkotamni/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverULV30LepMumv7_2017/230804_054846/0000/movedtree_%i.root' % i for i in chain(xrange(51), xrange(55,62), xrange(63,399), [52])] + ['/store/user/pkotamni/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverULV30LepMumv7_2017/230804_123838/0000/movedtree_%i.root' % i for i in chain(xrange(53,55), [51, 62])]),
'wjetstolnu_amcatnlo_2017': (146, ['/store/user/pkotamni/WJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-pythia8/TrackMoverULV30LepMumv7_2017/230804_123857/0000/movedtree_%i.root' % i for i in chain(xrange(73,75), xrange(79,82), xrange(97,99), [12, 16, 37, 39, 42, 51, 62, 89, 149])] + ['/store/user/pkotamni/WJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-pythia8/TrackMoverULV30LepMumv7_2017/230804_054847/0000/movedtree_%i.root' % i for i in chain(xrange(12), xrange(13,16), xrange(17,25), xrange(30,37), xrange(43,51), xrange(54,59), xrange(60,62), xrange(63,67), xrange(68,73), xrange(75,79), xrange(82,88), xrange(90,93), xrange(94,97), xrange(99,129), xrange(130,149), xrange(150,152), [38, 40, 52])] + ['/store/user/pkotamni/WJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-pythia8/TrackMoverULV30LepMumv7_2017/230806_024323/0000/movedtree_%i.root' % i for i in [41, 53, 59, 67, 88, 93]]),
'dyjetstollM10_2017': _fromnum1("/store/user/pekotamn/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverULV30LepMumv7_2017/230806_165246", 392, fnbase="movedtree"),
'dyjetstollM50_2017': (433, ['/store/user/pkotamni/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverULV30LepMumv7_2017/230804_123843/0000/movedtree_%i.root' % i for i in chain(xrange(320,323), xrange(341,344), xrange(361,369), xrange(428,431), [8, 10, 159, 244, 294, 308, 311, 382, 392, 394])] + ['/store/user/pkotamni/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverULV30LepMumv7_2017/230804_054849/0000/movedtree_%i.root' % i for i in chain(xrange(8), xrange(11,159), xrange(160,244), xrange(245,294), xrange(295,308), xrange(309,311), xrange(312,320), xrange(323,341), xrange(344,350), xrange(353,361), xrange(369,372), xrange(374,382), xrange(383,392), xrange(395,428), xrange(431,436), [9, 393])] + ['/store/user/pkotamni/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverULV30LepMumv7_2017/230806_024319/0000/movedtree_350.root'] + ['/store/user/pkotamni/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverULV30LepMumv7_2017/230806_040133/0000/movedtree_351.root']),
'ttbar_2017': (1481, ['/store/user/pkotamni/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/TrackMoverULV30LepMumv7_2017/230804_125236' + '/%04i/movedtree_%i.root' % (i/1000,i) for i in [855, 867, 870, 889, 893, 898, 900, 919, 937, 975, 995, 997, 1038]] + ['/store/user/pkotamni/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/TrackMoverULV30LepMumv7_2017/230804_125450' + '/%04i/movedtree_%i.root' % (i/1000,i) for i in [832, 835, 837, 861, 868, 873, 884, 888, 921, 944, 946, 971, 1037, 1048, 1065, 1082, 1113, 1152]] + ['/store/user/pkotamni/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/TrackMoverULV30LepMumv7_2017/230804_123841' + '/%04i/movedtree_%i.root' % (i/1000,i) for i in chain(xrange(697,699), xrange(753,756), xrange(821,823), xrange(847,850), xrange(862,864), [688, 707, 720, 734, 740, 765, 770, 788, 794, 808, 815, 817, 827, 842, 852, 990, 1004])] + ['/store/user/pkotamni/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/TrackMoverULV30LepMumv7_2017/230806_024312' + '/%04i/movedtree_%i.root' % (i/1000,i) for i in chain(xrange(1105,1107), xrange(1111,1113), xrange(1122,1125), xrange(1131,1133), xrange(1139,1141), xrange(1143,1145), xrange(1156,1158), xrange(1159,1161), xrange(1173,1175), xrange(1193,1195), xrange(1196,1202), xrange(1204,1207), xrange(1209,1211), xrange(1212,1214), xrange(1220,1224), xrange(1232,1234), xrange(1237,1239), xrange(1244,1246), xrange(1249,1251), xrange(1252,1254), xrange(1256,1262), xrange(1267,1270), xrange(1271,1273), xrange(1275,1278), xrange(1282,1284), xrange(1296,1298), xrange(1302,1306), xrange(1307,1310), xrange(1318,1323), xrange(1324,1329), xrange(1331,1335), xrange(1345,1347), xrange(1348,1352), xrange(1353,1355), xrange(1357,1361), xrange(1373,1375), xrange(1376,1380), xrange(1391,1394), xrange(1395,1397), xrange(1402,1404), xrange(1407,1409), xrange(1420,1423), xrange(1424,1429), xrange(1443,1445), xrange(1448,1450), xrange(1451,1453), xrange(1454,1458), xrange(1462,1464), xrange(1465,1472), xrange(1473,1476), [883, 899, 984, 1012, 1025, 1036, 1057, 1060, 1073, 1077, 1092, 1096, 1116, 1128, 1148, 1150, 1153, 1169, 1171, 1178, 1183, 1185, 1188, 1218, 1225, 1229, 1235, 1241, 1247, 1263, 1279, 1285, 1289, 1293, 1300, 1312, 1315, 1340, 1343, 1364, 1367, 1385, 1387, 1405, 1412, 1416, 1433, 1446, 1460, 1477, 1480])] + ['/store/user/pkotamni/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/TrackMoverULV30LepMumv7_2017/230804_125704' + '/%04i/movedtree_%i.root' % (i/1000,i) for i in chain(xrange(906,910), xrange(969,971), xrange(1145,1147), [891, 915, 930, 951, 965, 993, 999, 1005, 1007, 1020, 1041, 1047, 1049, 1086, 1095, 1102, 1121, 1138])] + ['/store/user/pkotamni/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/TrackMoverULV30LepMumv7_2017/230804_125022' + '/%04i/movedtree_%i.root' % (i/1000,i) for i in chain(xrange(874,876), [820, 841, 843, 860, 912, 956, 963, 994, 1023, 1040, 1044, 1046, 1089, 1091])] + ['/store/user/pkotamni/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/TrackMoverULV30LepMumv7_2017/230804_124125/0000/movedtree_%i.root' % i for i in chain(xrange(748,750), xrange(792,794), xrange(810,812), [700, 721, 737, 739, 746, 758, 763, 783, 787, 828, 840, 851, 856, 872, 976])] + ['/store/user/pkotamni/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/TrackMoverULV30LepMumv7_2017/230804_125920' + '/%04i/movedtree_%i.root' % (i/1000,i) for i in chain(xrange(931,933), [894, 929, 934, 947, 954, 972, 1035, 1042, 1053, 1059, 1103, 1110, 1133, 1137, 1180, 1191, 1479])] + ['/store/user/pkotamni/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/TrackMoverULV30LepMumv7_2017/230804_054850' + '/%04i/movedtree_%i.root' % (i/1000,i) for i in chain(xrange(68), xrange(69,688), xrange(689,697), xrange(701,707), xrange(708,720), xrange(722,728), xrange(741,746), xrange(750,753), xrange(756,758), xrange(759,761), xrange(766,770), xrange(771,783), xrange(784,787), xrange(789,792), xrange(796,798), xrange(799,804), xrange(805,808), xrange(825,827), xrange(833,835), xrange(838,840), xrange(853,855), xrange(864,866), xrange(876,880), xrange(881,883), xrange(886,888), xrange(895,898), xrange(901,906), xrange(910,912), xrange(913,915), xrange(922,925), xrange(938,940), xrange(941,944), xrange(948,951), xrange(952,954), xrange(960,963), xrange(966,969), xrange(973,975), xrange(977,981), xrange(985,988), xrange(991,993), xrange(1000,1004), xrange(1008,1012), xrange(1014,1020), xrange(1021,1023), xrange(1028,1030), xrange(1031,1033), xrange(1050,1053), xrange(1055,1057), xrange(1061,1065), xrange(1066,1073), xrange(1074,1077), xrange(1078,1082), xrange(1083,1086), xrange(1087,1089), xrange(1093,1095), xrange(1097,1102), xrange(1107,1110), xrange(1114,1116), xrange(1117,1121), xrange(1125,1128), xrange(1129,1131), xrange(1134,1137), xrange(1141,1143), xrange(1154,1156), xrange(1161,1169), xrange(1175,1178), xrange(1181,1183), xrange(1186,1188), xrange(1189,1191), xrange(1202,1204), xrange(1207,1209), xrange(1214,1218), xrange(1226,1229), xrange(1230,1232), xrange(1239,1241), xrange(1242,1244), xrange(1254,1256), xrange(1264,1267), xrange(1273,1275), xrange(1280,1282), xrange(1286,1289), xrange(1290,1293), xrange(1294,1296), xrange(1298,1300), xrange(1310,1312), xrange(1316,1318), xrange(1329,1331), xrange(1335,1340), xrange(1341,1343), xrange(1355,1357), xrange(1361,1364), xrange(1365,1367), xrange(1368,1373), xrange(1380,1385), xrange(1389,1391), xrange(1397,1402), xrange(1409,1412), xrange(1413,1416), xrange(1417,1420), xrange(1429,1433), xrange(1434,1443), xrange(1458,1460), [699, 729, 732, 735, 747, 764, 812, 814, 816, 818, 823, 829, 831, 836, 844, 846, 858, 869, 871, 890, 892, 916, 920, 926, 928, 933, 935, 945, 955, 957, 964, 982, 989, 996, 998, 1006, 1024, 1034, 1039, 1043, 1045, 1058, 1090, 1104, 1147, 1149, 1151, 1158, 1170, 1172, 1179, 1184, 1192, 1195, 1211, 1219, 1224, 1234, 1236, 1246, 1248, 1251, 1262, 1270, 1278, 1284, 1301, 1306, 1314, 1323, 1344, 1347, 1352, 1375, 1386, 1394, 1404, 1406, 1423, 1445, 1447, 1450, 1453, 1461, 1464, 1472, 1476, 1478, 1481])] + ['/store/user/pkotamni/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/TrackMoverULV30LepMumv7_2017/230804_124339' + '/%04i/movedtree_%i.root' % (i/1000,i) for i in chain(xrange(917,919), [728, 731, 733, 738, 761, 798, 819, 824, 857, 859, 866, 1013])] + ['/store/user/pkotamni/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/TrackMoverULV30LepMumv7_2017/230804_124807' + '/%04i/movedtree_%i.root' % (i/1000,i) for i in chain(xrange(958,960), [730, 804, 809, 813, 830, 845, 850, 880, 925, 927, 936, 940, 981, 983, 1026, 1030, 1054, 1313, 1388])] + ['/store/user/pkotamni/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/TrackMoverULV30LepMumv7_2017/230804_124553' + '/%04i/movedtree_%i.root' % (i/1000,i) for i in [736, 762, 795, 885, 988, 1027, 1033]]),
'ww_2017': _fromnum1("/store/user/pekotamn/WW_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv7_2017/230806_165151", 93, fnbase="movedtree"),
'zz_2017': (23, ['/store/user/pkotamni/ZZ_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv7_2017/230804_123836/0000/movedtree_19.root'] + ['/store/user/pkotamni/ZZ_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv7_2017/230804_054852/0000/movedtree_%i.root' % i for i in chain(xrange(4), xrange(6,19), xrange(20,23))] + ['/store/user/pkotamni/ZZ_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv7_2017/230806_024304/0000/movedtree_%i.root' % i for i in xrange(4,6)]),
'wz_2017': _fromnum0("/store/user/pkotamni/WZ_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv7_2017/230804_054853", 42, fnbase="movedtree"),
'SingleMuon2017B': _fromnum0("/store/user/pkotamni/SingleMuon/TrackMoverULV30LepMumv7_2017/230804_055338", 397, fnbase="movedtree"),
'SingleMuon2017C': (555, ['/store/user/pkotamni/SingleMuon/TrackMoverULV30LepMumv7_2017/230804_055339/0000/movedtree_%i.root' % i for i in chain(xrange(2,4), xrange(6,9), xrange(10,15), xrange(18,21), xrange(23,26), xrange(28,35), xrange(36,38), xrange(43,47), xrange(53,62), xrange(63,66), xrange(67,69), xrange(72,75), xrange(76,79), xrange(86,92), xrange(94,96), xrange(97,100), xrange(103,108), xrange(109,112), xrange(117,124), xrange(125,128), xrange(132,143), xrange(145,148), xrange(149,154), xrange(155,159), xrange(162,166), xrange(167,169), xrange(170,175), xrange(179,185), xrange(188,191), xrange(192,195), xrange(196,198), xrange(203,207), xrange(208,220), xrange(222,224), xrange(227,233), xrange(238,243), xrange(247,251), xrange(253,255), xrange(257,264), xrange(267,273), xrange(275,280), xrange(281,288), xrange(290,296), xrange(297,303), xrange(304,306), xrange(313,316), xrange(318,324), xrange(325,328), xrange(334,336), xrange(339,346), xrange(347,349), xrange(351,354), xrange(357,359), xrange(360,369), xrange(374,377), xrange(379,381), xrange(382,387), xrange(388,391), xrange(392,394), xrange(397,399), xrange(400,404), xrange(408,416), xrange(417,421), xrange(422,424), xrange(425,431), xrange(436,440), xrange(441,443), xrange(445,447), xrange(448,457), xrange(459,463), xrange(465,471), xrange(473,478), xrange(483,485), xrange(487,490), xrange(497,505), xrange(510,512), xrange(515,517), xrange(521,523), xrange(524,527), xrange(529,531), xrange(534,536), xrange(543,548), xrange(549,552), xrange(553,555), [0, 16, 49, 51, 83, 113, 130, 160, 186, 199, 225, 234, 236, 245, 311, 329, 331, 355, 372, 395, 406, 434, 493, 495, 506, 519, 537, 541])] + ['/store/user/pkotamni/SingleMuon/TrackMoverULV30LepMumv7_2017/230804_123859/0000/movedtree_%i.root' % i for i in chain(xrange(4,6), xrange(21,23), xrange(26,28), xrange(38,43), xrange(47,49), xrange(69,72), xrange(79,83), xrange(84,86), xrange(92,94), xrange(100,103), xrange(114,117), xrange(128,130), xrange(143,145), xrange(175,179), xrange(200,203), xrange(220,222), xrange(243,245), xrange(251,253), xrange(255,257), xrange(264,267), xrange(273,275), xrange(288,290), xrange(306,311), xrange(316,318), xrange(332,334), xrange(336,339), xrange(349,351), xrange(369,372), xrange(377,379), xrange(404,406), xrange(431,434), xrange(443,445), xrange(457,459), xrange(463,465), xrange(471,473), xrange(478,483), xrange(485,487), xrange(490,493), xrange(507,510), xrange(512,515), xrange(517,519), xrange(527,529), xrange(531,534), xrange(538,541), [1, 9, 15, 17, 35, 50, 52, 62, 66, 75, 96, 108, 112, 124, 131, 148, 154, 159, 161, 166, 169, 185, 187, 191, 195, 198, 207, 224, 226, 233, 235, 237, 246, 280, 296, 303, 312, 324, 328, 330, 346, 354, 356, 359, 373, 381, 387, 391, 394, 396, 399, 407, 421, 424, 435, 440, 447, 494, 496, 505, 520, 523, 536, 542, 548, 552])] + ['/store/user/pkotamni/SingleMuon/TrackMoverULV30LepMumv7_2017/230806_030532/0000/movedtree_416.root']),
'SingleMuon2017D': _fromnum0("/store/user/pkotamni/SingleMuon/TrackMoverULV30LepMumv7_2017/230804_055340", 227, fnbase="movedtree"),
'SingleMuon2017E': _fromnum0("/store/user/pkotamni/SingleMuon/TrackMoverULV30LepMumv7_2017/230804_055341", 570, fnbase="movedtree"),
'SingleMuon2017F': (854, ['/store/user/pkotamni/SingleMuon/TrackMoverULV30LepMumv7_2017/230804_123829/0000/movedtree_%i.root' % i for i in [427, 534, 644]] + ['/store/user/pkotamni/SingleMuon/TrackMoverULV30LepMumv7_2017/230804_055342/0000/movedtree_%i.root' % i for i in chain(xrange(427), xrange(428,534), xrange(535,644), xrange(645,854))]),
'SingleElectron2017B': _fromnum1("/store/user/pekotamn/SingleElectron/TrackMoverULV30LepMumv7_2017/230804_105230", 200, fnbase="movedtree"),
'SingleElectron2017C': _fromnum1("/store/user/pekotamn/SingleElectron/TrackMoverULV30LepMumv7_2017/230804_105248", 408, fnbase="movedtree"),
'SingleElectron2017D': (166, ['/store/user/pkotamni/SingleElectron/TrackMoverULV30LepMumv7_2017/230804_123834/0000/movedtree_%i.root' % i for i in chain(xrange(71,73), xrange(129,131), xrange(145,148), [5, 58, 77, 80, 89, 94, 111, 124, 153])] + ['/store/user/pkotamni/SingleElectron/TrackMoverULV30LepMumv7_2017/230804_124124/0000/movedtree_%i.root' % i for i in [128, 159]] + ['/store/user/pkotamni/SingleElectron/TrackMoverULV30LepMumv7_2017/230804_124337/0000/movedtree_%i.root' % i for i in [121, 162]] + ['/store/user/pkotamni/SingleElectron/TrackMoverULV30LepMumv7_2017/230804_055343/0000/movedtree_%i.root' % i for i in chain(xrange(5), xrange(6,58), xrange(59,71), xrange(73,77), xrange(78,80), xrange(81,89), xrange(90,94), xrange(95,111), xrange(112,121), xrange(122,124), xrange(125,128), xrange(131,145), xrange(148,153), xrange(154,159), xrange(160,162), xrange(163,166))]),
'SingleElectron2017E': _fromnum1("/store/user/pekotamn/SingleElectron/TrackMoverULV30LepMumv7_2017/230804_105305", 374, fnbase="movedtree"),
'SingleElectron2017F': _fromnum1("/store/user/pekotamn/SingleElectron/TrackMoverULV30LepMumv7_2017/230804_105323", 576, fnbase="movedtree"),
})



_add_ds("ntupleulv30lepm", {
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
