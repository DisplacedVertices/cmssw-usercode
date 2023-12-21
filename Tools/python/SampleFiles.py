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
    return [('root://cmseos.fnal.gov/' + fn) if (fn.startswith('/store/user') or fn.startswith('/store/group')) else fn for fn in fns]
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
'ttbar_2017': _fromnum0("/store/user/pkotamni/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleULV29Lepm_2017/230318_083846", 1019),
'ww_2017': _fromnum1("/store/user/pekotamn/WW_TuneCP5_13TeV-pythia8/NtupleULV29Lepm_2017/230318_133820", 30),
'zz_2017': _fromnum1("/store/user/pekotamn/WZ_TuneCP5_13TeV-pythia8/NtupleULV29Lepm_2017/230318_133833", 17),
'wz_2017': _fromnum1("/store/user/pekotamn/ZZ_TuneCP5_13TeV-pythia8/NtupleULV29Lepm_2017/230318_133845", 12),
'ZHToSSTodddd_tau1mm_M55_2017': _fromnum1("/store/user/pekotamn/ZH_HToSSTodddd_ZToLL_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/NtupleULV29Lepm_2017/230317_190651", 58),
'WplusHToSSTodddd_tau1mm_M55_2017': _fromnum1("/store/user/pekotamn/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/NtupleULV29Lepm_2017/230317_190756", 50),
'WminusHToSSTodddd_tau1mm_M55_2017': _fromnum1("/store/user/pekotamn/WminusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/NtupleULV29Lepm_2017/230317_190727", 50),
})


_add_ds("trackmoverulv30lepmumv4", {
'qcdmupt15_2017': (1, ['/store/user/pkotamni/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv4_2017/231120_124729/0000/movedtree_0.root']),
'qcdpt15mupt5_2017': (29, ['/store/user/pkotamni/QCD_Pt-15To20_MuEnrichedPt5_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv4_2017/231120_124730/0000/movedtree_%i.root' % i for i in chain(xrange(11), xrange(12,16), xrange(17,31))]),
'qcdpt20mupt5_2017': (194, ['/store/user/pkotamni/QCD_Pt-20To30_MuEnrichedPt5_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv4_2017/231129_100032/0000/movedtree_%i.root' % i for i in chain(xrange(47), xrange(48,53), xrange(54,63), xrange(64,72), xrange(74,80), xrange(82,89), xrange(99,102), xrange(107,113), xrange(116,121), xrange(135,143), xrange(146,150), xrange(151,158), xrange(159,165), xrange(168,177), xrange(178,197), xrange(203,212), [95, 97, 103, 105, 114, 122, 129, 213])] + ['/store/user/pkotamni/QCD_Pt-20To30_MuEnrichedPt5_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv4_2017/231130_121428/0000/movedtree_%i.root' % i for i in chain(xrange(72,74), xrange(80,82), xrange(89,95), xrange(143,145), xrange(165,167), [47, 53, 63, 96, 98, 102, 104, 106, 113, 115, 121, 150, 202, 212])]),
'qcdpt30mupt5_2017': (291, ['/store/user/pkotamni/QCD_Pt-30To50_MuEnrichedPt5_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv4_2017/231120_124732/0000/movedtree_%i.root' % i for i in chain(xrange(5), xrange(6,46), xrange(48,70), xrange(76,117), xrange(118,139), xrange(140,162), xrange(163,177), xrange(178,181), xrange(182,184), xrange(185,239), xrange(240,259), xrange(260,265), xrange(272,293), xrange(334,338), xrange(339,345), xrange(346,357), [74])]),
'qcdpt50mupt5_2017': (220, ['/store/user/pkotamni/QCD_Pt-50To80_MuEnrichedPt5_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv4_2017/231120_124733/0000/movedtree_%i.root' % i for i in chain(xrange(21), xrange(22,44), xrange(45,57), xrange(58,61), xrange(62,81), xrange(82,84), xrange(87,92), xrange(95,132), xrange(133,138), xrange(139,162), xrange(163,172), xrange(173,175), xrange(177,179), xrange(180,182), xrange(183,185), xrange(186,191), xrange(192,201), xrange(202,240), [85, 93])]),
'qcdpt80mupt5_2017': (270, ['/store/user/pkotamni/QCD_Pt-80To120_MuEnrichedPt5_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv4_2017/231120_124734/0000/movedtree_%i.root' % i for i in chain(xrange(1,105), xrange(107,147), xrange(151,277))]),
'qcdpt120mupt5_2017': (207, ['/store/user/pkotamni/QCD_Pt-120To170_MuEnrichedPt5_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv4_2017/231120_124735/0000/movedtree_%i.root' % i for i in chain(xrange(17), xrange(18,97), xrange(104,127), xrange(128,138), xrange(154,196), xrange(204,238), [146, 243])]),
'qcdpt170mupt5_2017': (431, ['/store/user/pkotamni/QCD_Pt-170To300_MuEnrichedPt5_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv4_2017/231120_124736/0000/movedtree_%i.root' % i for i in chain(xrange(2), xrange(3,156), xrange(157,161), xrange(162,210), xrange(213,272), xrange(282,447))]),
'qcdpt300mupt5_2017': _fromnum0("/store/user/pkotamni/QCD_Pt-300To470_MuEnrichedPt5_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv4_2017/231120_124737", 360, fnbase="movedtree"),
'qcdpt470mupt5_2017': _fromnum0("/store/user/pkotamni/QCD_Pt-470To600_MuEnrichedPt5_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv4_2017/231120_124738", 242, fnbase="movedtree"),
'qcdpt600mupt5_2017': (232, ['/store/user/pkotamni/QCD_Pt-600To800_MuEnrichedPt5_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv4_2017/231120_124739/0000/movedtree_%i.root' % i for i in chain(xrange(120), xrange(121,165), xrange(173,209), xrange(210,242))]),
'qcdpt800mupt5_2017': _fromnum0("/store/user/pkotamni/QCD_Pt-800To1000_MuEnrichedPt5_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv4_2017/231120_124740", 484, fnbase="movedtree"),
'qcdpt1000mupt5_2017': _fromnum0("/store/user/pkotamni/QCD_Pt-1000_MuEnrichedPt5_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv4_2017/231120_124741", 172, fnbase="movedtree"),
'qcdempt015_2017': (37, ['/store/user/pkotamni/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv4_2017/231120_124742/0000/movedtree_%i.root' % i for i in chain(xrange(4), xrange(6,35), xrange(38,41), [36])]),
'qcdempt020_2017': _fromnum0("/store/user/pkotamni/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv4_2017/231120_124743", 96, fnbase="movedtree"),
'qcdempt030_2017': _fromnum0("/store/user/pkotamni/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv4_2017/231120_124744", 67, fnbase="movedtree"),
'qcdempt050_2017': (49, ['/store/user/pkotamni/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv4_2017/231130_121543/0000/movedtree_%i.root' % i for i in [23, 33, 41, 43]] + ['/store/user/pkotamni/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv4_2017/231129_120148/0000/movedtree_%i.root' % i for i in chain(xrange(2,6), xrange(24,27), xrange(29,33), xrange(34,41), xrange(46,56), xrange(59,61), xrange(62,65), xrange(66,69), xrange(70,74), [0, 10, 42, 44, 57])]),
'qcdempt080_2017': (67, ['/store/user/pkotamni/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv4_2017/231120_124746/0000/movedtree_%i.root' % i for i in chain(xrange(44), xrange(45,68))]),
'qcdempt120_2017': (66, ['/store/user/pkotamni/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv4_2017/231130_121430/0000/movedtree_%i.root' % i for i in chain(xrange(21,23), xrange(27,29), xrange(30,32), [10, 12, 19, 40, 45, 50, 62, 75])] + ['/store/user/pkotamni/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv4_2017/231129_120150/0000/movedtree_%i.root' % i for i in chain(xrange(2), xrange(3,6), xrange(7,10), xrange(23,27), xrange(32,37), xrange(38,40), xrange(43,45), xrange(46,50), xrange(52,54), xrange(63,65), xrange(67,75), xrange(76,85), [11, 18, 20, 29, 41, 61])]),
'qcdempt170_2017': (27, ['/store/user/pkotamni/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv4_2017/231120_124748/0000/movedtree_%i.root' % i for i in chain(xrange(1,3), xrange(4,17), xrange(18,23), xrange(29,33), [24, 27, 34])]),
'qcdempt300_2017': (17, ['/store/user/pkotamni/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv4_2017/231120_124749/0000/movedtree_%i.root' % i for i in chain(xrange(2), xrange(5,9), xrange(12,21), [3, 10])]),
'qcdbctoept020_2017': (89, ['/store/user/pkotamni/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/TrackMoverULV30LepMumv4_2017/231130_121427/0000/movedtree_%i.root' % i for i in chain(xrange(72,76), xrange(80,83), xrange(84,89), [36, 77])] + ['/store/user/pkotamni/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/TrackMoverULV30LepMumv4_2017/231129_120153/0000/movedtree_%i.root' % i for i in chain(xrange(36), xrange(37,72), xrange(78,80), [76, 83])]),
'qcdbctoept030_2017': (78, ['/store/user/pkotamni/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/TrackMoverULV30LepMumv4_2017/231129_120154/0000/movedtree_%i.root' % i for i in chain(xrange(85,87), [59, 63])] + ['/store/user/pkotamni/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/TrackMoverULV30LepMumv4_2017/231130_121424/0000/movedtree_%i.root' % i for i in chain(xrange(5), xrange(6,8), xrange(9,17), xrange(19,49), xrange(50,57), xrange(60,63), xrange(64,75), xrange(76,78), xrange(79,84), [58])]),
'qcdbctoept080_2017': (50, ['/store/user/pkotamni/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/TrackMoverULV30LepMumv4_2017/231120_124752/0000/movedtree_%i.root' % i for i in chain(xrange(2), xrange(10,37), xrange(39,42), xrange(45,50), xrange(52,54), xrange(55,58), xrange(67,72), [5, 74, 77])]),
'qcdbctoept170_2017': _fromnum0("/store/user/pkotamni/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/TrackMoverULV30LepMumv4_2017/231120_124753", 90, fnbase="movedtree"),
'qcdbctoept250_2017': (70, ['/store/user/pkotamni/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/TrackMoverULV30LepMumv4_2017/231120_124754/0000/movedtree_%i.root' % i for i in chain(xrange(7), xrange(8,10), xrange(11,31), xrange(32,38), xrange(39,61), xrange(62,71), xrange(72,76))]),
'wjetstolnu_amcatnlo_2017': _fromnum1("/store/user/pekotamn/WJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-pythia8/TrackMoverULV30LepMumv4_2017/231129_173237", 158, fnbase="movedtree"),
'dyjetstollM10_2017': (98, ['/store/user/pekotamn/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverULV30LepMumv4_2017/231129_173259/0000/movedtree_%i.root' % i for i in chain(xrange(1,8), xrange(17,19), xrange(21,23), xrange(31,33), xrange(36,38), xrange(90,92), xrange(106,108), xrange(123,125), xrange(150,152), xrange(174,177), xrange(213,215), xrange(238,240), xrange(260,263), xrange(266,268), xrange(286,288), xrange(337,339), xrange(353,355), xrange(373,375), [9, 11, 24, 26, 29, 39, 41, 59, 67, 71, 74, 81, 85, 119, 121, 127, 131, 136, 138, 142, 146, 156, 158, 180, 194, 198, 203, 207, 219, 221, 224, 233, 246, 248, 271, 289, 291, 296, 298, 306, 308, 310, 314, 318, 330, 333, 335, 340, 344, 348, 360, 363, 368, 380, 386])]),
'wjetstolnu_0j_2017': (372, ['/store/group/lpclonglived/pkotamni/WJetsToLNu_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8/TrackMoverULV30LepMumv4_2017/231211_113727/0000/movedtree_%i.root' % i for i in chain(xrange(2), xrange(3,6), xrange(7,18), xrange(19,36), xrange(37,39), xrange(41,64), xrange(65,89), xrange(90,114), xrange(115,119), xrange(120,154), xrange(155,157), xrange(173,175), xrange(176,182), xrange(187,189), xrange(220,223), xrange(224,239), xrange(243,250), xrange(255,303), xrange(309,331), xrange(332,339), xrange(340,364), xrange(366,389), xrange(395,397), xrange(400,402), xrange(403,408), xrange(409,412), xrange(415,420), xrange(422,427), xrange(431,437), xrange(444,446), xrange(449,454), xrange(456,465), xrange(466,468), xrange(477,482), xrange(496,498), xrange(509,511), xrange(517,519), [393, 486, 488, 490, 492, 503, 522, 529, 536, 599])]),
#'wjetstolnu_1j_2017': (450, ['/store/group/lpclonglived/pkotamni/WJetsToLNu_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8/TrackMoverULV30LepMumv4_2017/231208_152201/0000/movedtree_%i.root' % i for i in chain(xrange(1,3), xrange(4,6), xrange(7,16), xrange(17,25), xrange(26,28), xrange(29,32), xrange(33,44), xrange(45,49), xrange(50,62), xrange(64,75), xrange(76,80), xrange(81,83), xrange(84,87), xrange(88,91), xrange(94,96), xrange(98,101), xrange(102,105), xrange(107,117), xrange(118,123), xrange(126,129), xrange(130,132), xrange(133,142), xrange(143,145), xrange(147,155), xrange(158,163), xrange(164,166), xrange(167,173), xrange(175,182), xrange(198,220), xrange(222,228), xrange(229,240), xrange(244,247), xrange(250,252), xrange(258,260), xrange(277,279), xrange(300,302), xrange(306,308), xrange(310,313), xrange(314,317), xrange(318,320), xrange(321,327), xrange(328,339), xrange(340,348), xrange(353,355), xrange(367,369), xrange(374,376), xrange(385,387), xrange(467,473), xrange(477,480), xrange(481,484), xrange(485,488), xrange(489,496), xrange(497,505), xrange(506,510), xrange(511,514), xrange(517,519), xrange(522,528), xrange(530,533), xrange(536,542), xrange(543,545), xrange(547,550), xrange(559,564), xrange(566,569), xrange(572,576), xrange(581,584), xrange(587,590), xrange(593,597), xrange(598,601), xrange(602,605), xrange(606,610), xrange(617,622), xrange(623,628), xrange(629,631), xrange(632,634), xrange(635,637), xrange(639,644), xrange(645,648), xrange(651,653), xrange(654,657), xrange(660,666), xrange(667,669), xrange(670,672), xrange(673,676), xrange(677,679), xrange(680,682), xrange(683,686), xrange(689,692), xrange(693,695), xrange(696,698), xrange(699,701), xrange(707,709), xrange(720,724), xrange(726,729), xrange(731,733), xrange(741,745), [92, 124, 185, 188, 196, 242, 248, 253, 255, 283, 289, 291, 350, 356, 358, 361, 363, 365, 370, 372, 378, 383, 389, 414, 429, 434, 439, 446, 475, 520, 534, 552, 554, 557, 570, 585, 591, 612, 614, 649, 687, 702, 704, 711, 713, 715, 717, 735, 737, 748])]),
'wjetstolnu_1j_2017': (2, ['/store/group/lpclonglived/pkotamni/WJetsToLNu_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8/TrackMoverULV30LepMumv4_2017/231208_152201/0000/movedtree_%i.root' % i for i in chain(xrange(1,3))]),
'wjetstolnu_2j_2017': (89, ['/store/group/lpclonglived/pkotamni/WJetsToLNu_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8/TrackMoverULV30LepMumv4_2017/231208_152317/0000/movedtree_%i.root' % i for i in chain(xrange(16,18), xrange(35,37), xrange(67,69), xrange(101,103), xrange(133,135), xrange(145,147), xrange(157,160), xrange(161,165), xrange(204,206), xrange(208,210), xrange(211,215), xrange(241,243), xrange(261,263), xrange(266,268), xrange(276,278), xrange(296,298), xrange(313,317), [5, 10, 20, 25, 31, 44, 46, 48, 50, 59, 71, 73, 78, 85, 96, 109, 117, 121, 150, 154, 168, 179, 181, 185, 201, 217, 226, 229, 233, 236, 238, 251, 270, 291, 301, 307, 322, 327, 334, 338, 347, 352, 354, 368, 377, 384, 388, 392])]),
'dyjetstollM50_2017': _fromnum1("/store/user/pekotamn/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverULV30LepMumv4_2017/231129_173322", 436, fnbase="movedtree"),
'ttbar_2017': (240, ['/store/user/pekotamn/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/TrackMoverULV30LepMumv4_2017/231130_165233/0000/movedtree_%i.root' % i for i in chain(xrange(12,15), xrange(29,32), xrange(46,48), xrange(52,54), xrange(78,80), xrange(112,114), xrange(133,135), xrange(136,138), xrange(163,165), xrange(166,170), xrange(182,184), xrange(204,206), xrange(213,215), xrange(229,231), xrange(238,240), xrange(246,248), xrange(280,282), xrange(286,289), xrange(308,310), xrange(313,316), xrange(343,345), xrange(350,353), xrange(356,358), xrange(381,383), xrange(403,405), xrange(410,413), xrange(417,419), xrange(434,437), xrange(480,483), xrange(559,561), xrange(573,575), xrange(576,579), xrange(583,585), xrange(587,590), xrange(591,594), xrange(596,598), xrange(619,621), xrange(639,643), xrange(680,682), xrange(699,701), xrange(739,741), xrange(767,769), xrange(772,776), xrange(778,780), xrange(794,796), xrange(814,816), [7, 9, 23, 25, 34, 37, 39, 50, 61, 66, 71, 75, 81, 83, 91, 94, 100, 120, 123, 126, 131, 142, 149, 154, 161, 171, 177, 185, 187, 191, 194, 199, 202, 211, 217, 232, 242, 250, 252, 258, 269, 276, 293, 305, 322, 325, 327, 334, 336, 354, 359, 364, 366, 370, 373, 377, 379, 384, 390, 392, 394, 396, 398, 400, 407, 415, 422, 424, 427, 430, 438, 440, 444, 456, 461, 463, 466, 478, 485, 489, 492, 495, 497, 507, 510, 513, 516, 519, 528, 532, 536, 541, 544, 553, 555, 600, 603, 605, 608, 622, 630, 633, 646, 648, 655, 661, 663, 668, 673, 675, 677, 688, 690, 692, 694, 696, 712, 714, 718, 736, 742, 747, 758, 765, 770, 790, 798, 801, 803, 811, 818])]),
'ww_2017': (19, ['/store/user/pkotamni/WW_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv4_2017/231130_120548/0000/movedtree_%i.root' % i for i in chain(xrange(24,26), xrange(35,37), xrange(49,53), xrange(67,70), [3, 8, 20, 28, 42, 59, 61, 87])]),
'zz_2017': _fromnum1("/store/user/pekotamn/ZZ_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv4_2017/231129_173407", 24, fnbase="movedtree"),
'wz_2017': (41, ['/store/user/pekotamn/WZ_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv4_2017/231129_173429/0000/movedtree_%i.root' % i for i in chain(xrange(1,18), xrange(19,25), xrange(26,44))]),
'SingleMuon2017B': (319, ['/store/user/pekotamn/SingleMuon/TrackMoverULV30LepMumv4_2017/231129_173012/0000/movedtree_%i.root' % i for i in chain(xrange(1,23), xrange(24,95), xrange(96,215), xrange(216,231), xrange(232,266), xrange(267,325))]),
'SingleMuon2017C': (520, ['/store/user/pkotamni/SingleMuon/TrackMoverULV30LepMumv4_2017/231120_124756/0000/movedtree_%i.root' % i for i in chain(xrange(14), xrange(15,57), xrange(58,64), xrange(65,99), xrange(100,113), xrange(114,122), xrange(123,190), xrange(191,216), xrange(217,263), xrange(264,292), xrange(293,326), xrange(327,342), xrange(343,403), xrange(404,406), xrange(407,409), xrange(410,418), xrange(419,427), xrange(428,435), xrange(436,440), xrange(441,444), xrange(446,448), xrange(451,453), xrange(454,457), xrange(458,463), xrange(464,475), xrange(476,478), xrange(481,486), xrange(490,492), xrange(493,516), xrange(517,521), xrange(522,555), [449, 479, 487])]),
'SingleMuon2017D': (200, ['/store/user/pekotamn/SingleMuon/TrackMoverULV30LepMumv4_2017/231129_173101/0000/movedtree_%i.root' % i for i in chain(xrange(1,10), xrange(11,38), xrange(39,48), xrange(49,64), xrange(65,82), xrange(83,100), xrange(103,136), xrange(137,151), xrange(152,157), xrange(158,176), xrange(177,185), xrange(186,191), xrange(192,214), [101])]),
'SingleMuon2017E': (495, ['/store/user/pekotamn/SingleMuon/TrackMoverULV30LepMumv4_2017/231129_173124/0000/movedtree_%i.root' % i for i in chain(xrange(1,40), xrange(41,154), xrange(155,498))]),
'SingleMuon2017F': (724, ['/store/user/pekotamn/SingleMuon/TrackMoverULV30LepMumv4_2017/231129_173148/0000/movedtree_%i.root' % i for i in chain(xrange(1,44), xrange(45,726))]),
'SingleElectron2017B': _fromnum1("/store/user/pekotamn/SingleElectron/TrackMoverULV30LepMumv4_2017/231120_184618", 200, fnbase="movedtree"),
'SingleElectron2017C': _fromnum1("/store/user/pekotamn/SingleElectron/TrackMoverULV30LepMumv4_2017/231120_184641", 408, fnbase="movedtree"),
'SingleElectron2017E': _fromnum1("/store/user/pekotamn/SingleElectron/TrackMoverULV30LepMumv4_2017/231120_184704", 374, fnbase="movedtree"),
'SingleElectron2017F': _fromnum1("/store/user/pekotamn/SingleElectron/TrackMoverULV30LepMumv4_2017/231120_184728", 576, fnbase="movedtree"),
})

_add_ds("trackmovermctruthulv30lepmumv4", {
'WplusHToSSTodddd_tau300um_M55_2017': _fromnum1("/store/user/pekotamn/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/TrackMoverMCTruthULV30LepMumv4_2017/231120_184238", 50, fnbase="mctruth"),
'WplusHToSSTodddd_tau1mm_M55_2017': _fromnum1("/store/user/pekotamn/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/TrackMoverMCTruthULV30LepMumv4_2017/231120_184138", 50, fnbase="mctruth"),
'WplusHToSSTodddd_tau10mm_M55_2017': _fromnum1("/store/user/pekotamn/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-10_TuneCP5_13TeV-powheg-pythia8/TrackMoverMCTruthULV30LepMumv4_2017/231120_184410", 50, fnbase="mctruth"),
})



_add_ds("ntupleulv30lepmum", {
'qcdpt15mupt5_2017': (7, ['/store/group/lpclonglived/pkotamni/QCD_Pt-15To20_MuEnrichedPt5_TuneCP5_13TeV-pythia8/NtupleULV30LepMum_2017/231130_150936/0000/ntuple_%i.root' % i for i in chain(xrange(3), xrange(6,10))]),
'qcdpt20mupt5_2017': (57, ['/store/group/lpclonglived/pkotamni/QCD_Pt-20To30_MuEnrichedPt5_TuneCP5_13TeV-pythia8/NtupleULV30LepMum_2017/231130_150937/0000/ntuple_%i.root' % i for i in chain(xrange(37), xrange(41,47), xrange(48,53), xrange(54,59), xrange(61,65))]),
'qcdpt30mupt5_2017': (84, ['/store/group/lpclonglived/pkotamni/QCD_Pt-30To50_MuEnrichedPt5_TuneCP5_13TeV-pythia8/NtupleULV30LepMum_2017/231130_150938/0000/ntuple_%i.root' % i for i in chain(xrange(13), xrange(15,21), xrange(23,71), xrange(72,74), xrange(75,77), xrange(82,88), xrange(102,108), [78])]),
'qcdpt50mupt5_2017': (68, ['/store/group/lpclonglived/pkotamni/QCD_Pt-50To80_MuEnrichedPt5_TuneCP5_13TeV-pythia8/NtupleULV30LepMum_2017/231130_150939/0000/ntuple_%i.root' % i for i in chain(xrange(48), xrange(49,52), xrange(55,72))]),
'qcdpt80mupt5_2017': (79, ['/store/group/lpclonglived/pkotamni/QCD_Pt-80To120_MuEnrichedPt5_TuneCP5_13TeV-pythia8/NtupleULV30LepMum_2017/231130_150940/0000/ntuple_%i.root' % i for i in chain(xrange(1,31), xrange(32,44), xrange(46,82), [83])]),
'qcdpt120mupt5_2017': (58, ['/store/group/lpclonglived/pkotamni/QCD_Pt-120To170_MuEnrichedPt5_TuneCP5_13TeV-pythia8/NtupleULV30LepMum_2017/231130_150941/0000/ntuple_%i.root' % i for i in chain(xrange(1,5), xrange(6,29), xrange(32,38), xrange(39,41), xrange(46,59), xrange(61,71))]),
'qcdpt170mupt5_2017': (120, ['/store/group/lpclonglived/pkotamni/QCD_Pt-170To300_MuEnrichedPt5_TuneCP5_13TeV-pythia8/NtupleULV30LepMum_2017/231130_150942/0000/ntuple_%i.root' % i for i in chain(xrange(3,8), xrange(9,12), xrange(13,19), xrange(20,22), xrange(23,37), xrange(38,40), xrange(43,63), xrange(64,81), xrange(85,134), [1, 41])]),
'qcdpt300mupt5_2017': (107, ['/store/group/lpclonglived/pkotamni/QCD_Pt-300To470_MuEnrichedPt5_TuneCP5_13TeV-pythia8/NtupleULV30LepMum_2017/231130_150943/0000/ntuple_%i.root' % i for i in chain(xrange(74), xrange(75,108))]),
'qcdpt470mupt5_2017': (70, ['/store/group/lpclonglived/pkotamni/QCD_Pt-470To600_MuEnrichedPt5_TuneCP5_13TeV-pythia8/NtupleULV30LepMum_2017/231130_150944/0000/ntuple_%i.root' % i for i in chain(xrange(47), xrange(48,61), xrange(62,72))]),
'qcdpt600mupt5_2017': (60, ['/store/group/lpclonglived/pkotamni/QCD_Pt-600To800_MuEnrichedPt5_TuneCP5_13TeV-pythia8/NtupleULV30LepMum_2017/231130_150945/0000/ntuple_%i.root' % i for i in chain(xrange(2), xrange(3,5), xrange(8,12), xrange(15,40), xrange(41,43), xrange(45,49), xrange(52,58), xrange(59,67), xrange(68,73), [6, 13])]),
'qcdpt800mupt5_2017': (138, ['/store/group/lpclonglived/pkotamni/QCD_Pt-800To1000_MuEnrichedPt5_TuneCP5_13TeV-pythia8/NtupleULV30LepMum_2017/231130_150946/0000/ntuple_%i.root' % i for i in chain(xrange(127), xrange(128,133), xrange(134,140))]),
'qcdpt1000mupt5_2017': (20, ['/store/group/lpclonglived/pkotamni/QCD_Pt-1000_MuEnrichedPt5_TuneCP5_13TeV-pythia8/NtupleULV30LepMum_2017/231130_150947/0000/ntuple_%i.root' % i for i in chain(xrange(8,15), xrange(16,20), xrange(21,30))]),
'qcdempt015_2017': (10, ['/store/group/lpclonglived/pkotamni/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV30LepMum_2017/231130_150948/0000/ntuple_%i.root' % i for i in chain(xrange(2,10), [0, 12])]),
'qcdempt020_2017': _fromnum0("/store/group/lpclonglived/pkotamni/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV30LepMum_2017/231130_150949", 29),
'qcdempt030_2017': _fromnum0("/store/group/lpclonglived/pkotamni/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV30LepMum_2017/231130_150950", 20),
'qcdempt050_2017': (7, ['/store/group/lpclonglived/pkotamni/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV30LepMum_2017/231130_150951/0000/ntuple_%i.root' % i for i in chain(xrange(14,16), xrange(18,20), [0, 11, 21])]),
'qcdempt080_2017': _fromnum0("/store/group/lpclonglived/pkotamni/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV30LepMum_2017/231130_150952", 21),
'qcdempt120_2017': (9, ['/store/group/lpclonglived/pkotamni/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV30LepMum_2017/231130_150953/0000/ntuple_%i.root' % i for i in chain(xrange(9,11), xrange(23,26), [0, 12, 14, 20])]),
'qcdempt300_2017': (6, ['/store/group/lpclonglived/pkotamni/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV30LepMum_2017/231130_150955/0000/ntuple_%i.root' % i for i in chain(xrange(2,7), [0])]),
'qcdbctoept020_2017': _fromnum0("/store/group/lpclonglived/pkotamni/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/NtupleULV30LepMum_2017/231130_150956", 27),
'qcdbctoept030_2017': (18, ['/store/group/lpclonglived/pkotamni/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/NtupleULV30LepMum_2017/231130_150957/0000/ntuple_%i.root' % i for i in chain(xrange(3,5), xrange(6,14), xrange(15,17), xrange(18,22), [0, 24])]),
'qcdbctoept080_2017': _fromnum0("/store/group/lpclonglived/pkotamni/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/NtupleULV30LepMum_2017/231130_150958", 25),
'qcdbctoept170_2017': (14, ['/store/group/lpclonglived/pkotamni/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/NtupleULV30LepMum_2017/231130_150959/0000/ntuple_%i.root' % i for i in chain(xrange(5,8), xrange(14,17), xrange(19,23), xrange(25,27), [3, 12])]),
'qcdbctoept250_2017': (17, ['/store/group/lpclonglived/pkotamni/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/NtupleULV30LepMum_2017/231130_151000/0000/ntuple_%i.root' % i for i in chain(xrange(2), xrange(4,9), xrange(12,18), xrange(19,21), [10, 22])]),
'wjetstolnu_2017': _fromnum1("/store/user/pekotamn/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV30LepMum_2017/231130_210825", 120),
'wjetstolnu_amcatnlo_2017': _fromnum1("/store/user/pekotamn/WJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleULV30LepMum_2017/231130_210848", 48),
'dyjetstollM10_2017': (3, ['/store/user/pekotamn/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV30LepMum_2017/231130_210910/0000/ntuple_%i.root' % i for i in chain(xrange(1,3), [92])]),
'dyjetstollM50_2017': _fromnum1("/store/user/pekotamn/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV30LepMum_2017/231130_210932", 132),
'ww_2017': (2, ['/store/group/lpclonglived/pkotamni/WW_TuneCP5_13TeV-pythia8/NtupleULV30LepMum_2017/231130_151001/0000/ntuple_%i.root' % i for i in [15, 20]]),
'zz_2017': (6, ['/store/group/lpclonglived/pkotamni/ZZ_TuneCP5_13TeV-pythia8/NtupleULV30LepMum_2017/231130_151002/0000/ntuple_%i.root' % i for i in chain(xrange(2,7), [0])]),
'wz_2017': _fromnum0("/store/group/lpclonglived/pkotamni/WZ_TuneCP5_13TeV-pythia8/NtupleULV30LepMum_2017/231130_151003", 13),
'ZHToSSTodddd_tau100um_M15_2017': (243, ['/store/group/lpclonglived/pkotamni/ZH_HToSSTodddd_ZToLL_MH-125_MS-15_ctauS-0p1_TuneCP5_13TeV-powheg-pythia8/NtupleULV30LepMum_2017/231130_173841/0000/ntuple_%i.root' % i for i in chain(xrange(87), xrange(88,161), xrange(162,244), [245])]),
'ZHToSSTodddd_tau300um_M15_2017': _fromnum0("/store/group/lpclonglived/pkotamni/ZH_HToSSTodddd_ZToLL_MH-125_MS-15_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/NtupleULV30LepMum_2017/231130_173842", 250),
'ZHToSSTodddd_tau1mm_M15_2017': _fromnum0("/store/group/lpclonglived/pkotamni/ZH_HToSSTodddd_ZToLL_MH-125_MS-15_ctauS-1_TuneCP5_13TeV-powheg-pythia8/NtupleULV30LepMum_2017/231130_173843", 250),
'ZHToSSTodddd_tau3mm_M15_2017': (245, ['/store/group/lpclonglived/pkotamni/ZH_HToSSTodddd_ZToLL_MH-125_MS-15_ctauS-3_TuneCP5_13TeV-powheg-pythia8/NtupleULV30LepMum_2017/231130_173844/0000/ntuple_%i.root' % i for i in chain(xrange(114), xrange(115,133), xrange(134,196), xrange(197,218), xrange(219,221), xrange(222,250))]),
'ZHToSSTodddd_tau10mm_M15_2017': (241, ['/store/group/lpclonglived/pkotamni/ZH_HToSSTodddd_ZToLL_MH-125_MS-15_ctauS-10_TuneCP5_13TeV-powheg-pythia8/NtupleULV30LepMum_2017/231130_173845/0000/ntuple_%i.root' % i for i in chain(xrange(20), xrange(21,35), xrange(36,49), xrange(50,67), xrange(68,79), xrange(80,102), xrange(104,113), xrange(114,116), xrange(117,250))]),
'ZHToSSTodddd_tau30mm_M15_2017': _fromnum0("/store/group/lpclonglived/pkotamni/ZH_HToSSTodddd_ZToLL_MH-125_MS-15_ctauS-30_TuneCP5_13TeV-powheg-pythia8/NtupleULV30LepMum_2017/231130_173846", 250),
'ZHToSSTodddd_tau100um_M40_2017': (247, ['/store/group/lpclonglived/pkotamni/ZH_HToSSTodddd_ZToLL_MH-125_MS-40_ctauS-0p1_TuneCP5_13TeV-powheg-pythia8/NtupleULV30LepMum_2017/231130_173847/0000/ntuple_%i.root' % i for i in chain(xrange(25), xrange(26,174), xrange(175,202), xrange(203,250))]),
'ZHToSSTodddd_tau300um_M40_2017': (246, ['/store/group/lpclonglived/pkotamni/ZH_HToSSTodddd_ZToLL_MH-125_MS-40_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/NtupleULV30LepMum_2017/231130_173848/0000/ntuple_%i.root' % i for i in chain(xrange(67), xrange(68,76), xrange(77,140), xrange(141,243), xrange(244,250))]),
'ZHToSSTodddd_tau1mm_M40_2017': _fromnum0("/store/group/lpclonglived/pkotamni/ZH_HToSSTodddd_ZToLL_MH-125_MS-40_ctauS-1_TuneCP5_13TeV-powheg-pythia8/NtupleULV30LepMum_2017/231130_173849", 250),
'ZHToSSTodddd_tau3mm_M40_2017': (246, ['/store/group/lpclonglived/pkotamni/ZH_HToSSTodddd_ZToLL_MH-125_MS-40_ctauS-3_TuneCP5_13TeV-powheg-pythia8/NtupleULV30LepMum_2017/231130_173850/0000/ntuple_%i.root' % i for i in chain(xrange(16), xrange(17,31), xrange(32,123), xrange(124,233), xrange(234,250))]),
'ZHToSSTodddd_tau10mm_M40_2017': (248, ['/store/group/lpclonglived/pkotamni/ZH_HToSSTodddd_ZToLL_MH-125_MS-40_ctauS-10_TuneCP5_13TeV-powheg-pythia8/NtupleULV30LepMum_2017/231130_173851/0000/ntuple_%i.root' % i for i in chain(xrange(33), xrange(34,106), xrange(107,250))]),
'ZHToSSTodddd_tau30mm_M40_2017': _fromnum0("/store/group/lpclonglived/pkotamni/ZH_HToSSTodddd_ZToLL_MH-125_MS-40_ctauS-30_TuneCP5_13TeV-powheg-pythia8/NtupleULV30LepMum_2017/231130_173852", 250),
'ZHToSSTodddd_tau100um_M55_2017': (249, ['/store/group/lpclonglived/pkotamni/ZH_HToSSTodddd_ZToLL_MH-125_MS-55_ctauS-0p1_TuneCP5_13TeV-powheg-pythia8/NtupleULV30LepMum_2017/231130_173853/0000/ntuple_%i.root' % i for i in chain(xrange(176), xrange(177,250))]),
'ZHToSSTodddd_tau300um_M55_2017': (247, ['/store/group/lpclonglived/pkotamni/ZH_HToSSTodddd_ZToLL_MH-125_MS-55_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/NtupleULV30LepMum_2017/231130_173854/0000/ntuple_%i.root' % i for i in chain(xrange(29), xrange(30,46), xrange(47,101), xrange(102,250))]),
'ZHToSSTodddd_tau1mm_M55_2017': (157, ['/store/group/lpclonglived/pkotamni/ZH_HToSSTodddd_ZToLL_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/NtupleULV30LepMum_2017/231130_173855/0000/ntuple_%i.root' % i for i in chain(xrange(26), xrange(30,32), xrange(33,37), xrange(38,40), xrange(48,56), xrange(57,59), xrange(60,63), xrange(68,70), xrange(72,74), xrange(75,80), xrange(81,85), xrange(87,90), xrange(91,96), xrange(97,99), xrange(102,107), xrange(113,115), xrange(116,118), xrange(122,124), xrange(125,127), xrange(130,132), xrange(138,142), xrange(145,147), xrange(148,150), xrange(153,156), xrange(158,161), xrange(162,168), xrange(186,188), xrange(189,195), xrange(197,205), xrange(209,212), xrange(218,220), xrange(227,229), xrange(232,235), xrange(236,238), xrange(241,245), xrange(248,250), [27, 41, 43, 45, 65, 108, 111, 128, 133, 136, 143, 169, 175, 180, 182, 206, 221, 225])]),
'ZHToSSTodddd_tau3mm_M55_2017': (227, ['/store/group/lpclonglived/pkotamni/ZH_HToSSTodddd_ZToLL_MH-125_MS-55_ctauS-3_TuneCP5_13TeV-powheg-pythia8/NtupleULV30LepMum_2017/231130_173856/0000/ntuple_%i.root' % i for i in chain(xrange(2), xrange(3,99), xrange(102,108), xrange(112,114), xrange(116,138), xrange(142,147), xrange(148,150), xrange(151,154), xrange(156,158), xrange(159,169), xrange(171,186), xrange(187,190), xrange(191,241), xrange(242,250), [140])]),
'ZHToSSTodddd_tau10mm_M55_2017': (245, ['/store/group/lpclonglived/pkotamni/ZH_HToSSTodddd_ZToLL_MH-125_MS-55_ctauS-10_TuneCP5_13TeV-powheg-pythia8/NtupleULV30LepMum_2017/231130_173857/0000/ntuple_%i.root' % i for i in chain(xrange(165), xrange(166,231), xrange(232,235), xrange(236,244), xrange(245,247), xrange(248,250))]),
'ZHToSSTodddd_tau30mm_M55_2017': (166, ['/store/group/lpclonglived/pkotamni/ZH_HToSSTodddd_ZToLL_MH-125_MS-55_ctauS-30_TuneCP5_13TeV-powheg-pythia8/NtupleULV30LepMum_2017/231130_173858/0000/ntuple_%i.root' % i for i in chain(xrange(3,36), xrange(37,44), xrange(45,49), xrange(50,52), xrange(54,61), xrange(66,72), xrange(77,79), xrange(82,84), xrange(85,87), xrange(88,90), xrange(91,97), xrange(98,101), xrange(102,104), xrange(105,107), xrange(114,118), xrange(119,122), xrange(126,135), xrange(136,139), xrange(148,154), xrange(157,160), xrange(161,163), xrange(166,169), xrange(174,179), xrange(183,185), xrange(186,188), xrange(191,193), xrange(194,197), xrange(214,217), xrange(225,227), xrange(233,235), xrange(238,240), xrange(243,250), [0, 62, 75, 108, 110, 123, 142, 155, 170, 172, 180, 189, 199, 204, 206, 208, 210, 219, 223, 228, 231, 236, 241])]),
'WplusHToSSTodddd_tau100um_M15_2017': (247, ['/store/group/lpclonglived/pkotamni/WplusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-0p1_TuneCP5_13TeV-powheg-pythia8/NtupleULV30LepMum_2017/231130_173859/0000/ntuple_%i.root' % i for i in chain(xrange(102), xrange(103,235), xrange(236,248), [249])]),
'WplusHToSSTodddd_tau300um_M15_2017': (243, ['/store/group/lpclonglived/pkotamni/WplusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/NtupleULV30LepMum_2017/231130_173900/0000/ntuple_%i.root' % i for i in chain(xrange(4), xrange(5,14), xrange(15,245))]),
'WplusHToSSTodddd_tau1mm_M15_2017': _fromnum0("/store/group/lpclonglived/pkotamni/WplusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-1_TuneCP5_13TeV-powheg-pythia8/NtupleULV30LepMum_2017/231130_173901", 250),
'WplusHToSSTodddd_tau3mm_M15_2017': (245, ['/store/group/lpclonglived/pkotamni/WplusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-3_TuneCP5_13TeV-powheg-pythia8/NtupleULV30LepMum_2017/231130_173902/0000/ntuple_%i.root' % i for i in chain(xrange(44), xrange(45,82), xrange(83,90), xrange(91,129), xrange(130,225), xrange(226,250))]),
'WplusHToSSTodddd_tau30mm_M15_2017': (248, ['/store/group/lpclonglived/pkotamni/WplusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-30_TuneCP5_13TeV-powheg-pythia8/NtupleULV30LepMum_2017/231130_173903/0000/ntuple_%i.root' % i for i in chain(xrange(34), xrange(35,44), xrange(45,250))]),
'WplusHToSSTodddd_tau300um_M40_2017': (245, ['/store/group/lpclonglived/pkotamni/WplusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/NtupleULV30LepMum_2017/231130_174419/0000/ntuple_%i.root' % i for i in chain(xrange(156), xrange(157,186), xrange(187,205), xrange(206,227), xrange(228,234), xrange(235,250))]),
'WplusHToSSTodddd_tau1mm_M40_2017': (248, ['/store/group/lpclonglived/pkotamni/WplusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-1_TuneCP5_13TeV-powheg-pythia8/NtupleULV30LepMum_2017/231130_174420/0000/ntuple_%i.root' % i for i in chain(xrange(57), xrange(58,139), xrange(140,250))]),
'WplusHToSSTodddd_tau3mm_M40_2017': (238, ['/store/group/lpclonglived/pkotamni/WplusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-3_TuneCP5_13TeV-powheg-pythia8/NtupleULV30LepMum_2017/231130_174421/0000/ntuple_%i.root' % i for i in chain(xrange(109), xrange(110,222), xrange(223,240))]),
'WplusHToSSTodddd_tau30mm_M40_2017': (245, ['/store/group/lpclonglived/pkotamni/WplusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-30_TuneCP5_13TeV-powheg-pythia8/NtupleULV30LepMum_2017/231130_174422/0000/ntuple_%i.root' % i for i in chain(xrange(66), xrange(67,96), xrange(97,142), xrange(143,230), xrange(231,249))]),
'WplusHToSSTodddd_tau100um_M55_2017': _fromnum0("/store/group/lpclonglived/pkotamni/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-0p1_TuneCP5_13TeV-powheg-pythia8/NtupleULV30LepMum_2017/231130_174423", 250),
'WplusHToSSTodddd_tau300um_M55_2017': (248, ['/store/group/lpclonglived/pkotamni/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/NtupleULV30LepMum_2017/231130_174424/0000/ntuple_%i.root' % i for i in chain(xrange(178), xrange(179,241), xrange(242,250))]),
'WplusHToSSTodddd_tau1mm_M55_2017': (249, ['/store/group/lpclonglived/pkotamni/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/NtupleULV30LepMum_2017/231130_174425/0000/ntuple_%i.root' % i for i in chain(xrange(97), xrange(98,250))]),
'WplusHToSSTodddd_tau3mm_M55_2017': (249, ['/store/group/lpclonglived/pkotamni/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-3_TuneCP5_13TeV-powheg-pythia8/NtupleULV30LepMum_2017/231130_174426/0000/ntuple_%i.root' % i for i in chain(xrange(36), xrange(37,250))]),
'WplusHToSSTodddd_tau30mm_M55_2017': (233, ['/store/group/lpclonglived/pkotamni/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-30_TuneCP5_13TeV-powheg-pythia8/NtupleULV30LepMum_2017/231130_174427/0000/ntuple_%i.root' % i for i in chain(xrange(42), xrange(47,57), xrange(58,84), xrange(85,104), xrange(105,219), xrange(220,240), [43, 45])]),
'WplusHToSSTodddd_tau10mm_M55_2017': _fromnum0("/store/group/lpclonglived/pkotamni/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-10_TuneCP5_13TeV-powheg-pythia8/NtupleULV30LepMum_2017/231130_174428", 125),
'WminusHToSSTodddd_tau1mm_M15_2017': (242, ['/store/group/lpclonglived/pkotamni/WminusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-1_TuneCP5_13TeV-powheg-pythia8/NtupleULV30LepMum_2017/231130_174429/0000/ntuple_%i.root' % i for i in chain(xrange(191), xrange(192,198), xrange(199,209), xrange(210,245))]),
'WminusHToSSTodddd_tau3mm_M15_2017': (244, ['/store/group/lpclonglived/pkotamni/WminusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-3_TuneCP5_13TeV-powheg-pythia8/NtupleULV30LepMum_2017/231130_174430/0000/ntuple_%i.root' % i for i in chain(xrange(191), xrange(192,245))]),
'WminusHToSSTodddd_tau10mm_M15_2017': (247, ['/store/group/lpclonglived/pkotamni/WminusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-10_TuneCP5_13TeV-powheg-pythia8/NtupleULV30LepMum_2017/231130_174431/0000/ntuple_%i.root' % i for i in chain(xrange(98), xrange(99,104), xrange(105,196), xrange(197,250))]),
'WminusHToSSTodddd_tau30mm_M15_2017': (246, ['/store/group/lpclonglived/pkotamni/WminusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-30_TuneCP5_13TeV-powheg-pythia8/NtupleULV30LepMum_2017/231130_174432/0000/ntuple_%i.root' % i for i in chain(xrange(22), xrange(23,103), xrange(104,154), xrange(155,191), xrange(192,250))]),
'WminusHToSSTodddd_tau300um_M40_2017': (246, ['/store/group/lpclonglived/pkotamni/WminusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/NtupleULV30LepMum_2017/231130_174433/0000/ntuple_%i.root' % i for i in chain(xrange(1,24), xrange(25,45), xrange(46,141), xrange(142,250))]),
'WminusHToSSTodddd_tau1mm_M40_2017': (236, ['/store/group/lpclonglived/pkotamni/WminusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-1_TuneCP5_13TeV-powheg-pythia8/NtupleULV30LepMum_2017/231130_174434/0000/ntuple_%i.root' % i for i in chain(xrange(159), xrange(160,171), xrange(173,176), xrange(177,240))]),
'WminusHToSSTodddd_tau3mm_M40_2017': (248, ['/store/group/lpclonglived/pkotamni/WminusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-3_TuneCP5_13TeV-powheg-pythia8/NtupleULV30LepMum_2017/231130_174435/0000/ntuple_%i.root' % i for i in chain(xrange(136), xrange(137,205), xrange(206,250))]),
'WminusHToSSTodddd_tau10mm_M40_2017': (247, ['/store/group/lpclonglived/pkotamni/WminusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-10_TuneCP5_13TeV-powheg-pythia8/NtupleULV30LepMum_2017/231130_174436/0000/ntuple_%i.root' % i for i in chain(xrange(94), xrange(95,154), xrange(155,182), xrange(183,250))]),
'WminusHToSSTodddd_tau30mm_M40_2017': (248, ['/store/group/lpclonglived/pkotamni/WminusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-30_TuneCP5_13TeV-powheg-pythia8/NtupleULV30LepMum_2017/231130_174437/0000/ntuple_%i.root' % i for i in chain(xrange(87), xrange(88,123), xrange(124,250))]),
'WminusHToSSTodddd_tau300um_M55_2017': (239, ['/store/group/lpclonglived/pkotamni/WminusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/NtupleULV30LepMum_2017/231130_174438/0000/ntuple_%i.root' % i for i in chain(xrange(231), xrange(232,240))]),
'WminusHToSSTodddd_tau1mm_M55_2017': (138, ['/store/group/lpclonglived/pkotamni/WminusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/NtupleULV30LepMum_2017/231130_174439/0000/ntuple_%i.root' % i for i in chain(xrange(73), xrange(74,139))]),
'WminusHToSSTodddd_tau3mm_M55_2017': (246, ['/store/group/lpclonglived/pkotamni/WminusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-3_TuneCP5_13TeV-powheg-pythia8/NtupleULV30LepMum_2017/231130_174440/0000/ntuple_%i.root' % i for i in chain(xrange(123), xrange(124,184), xrange(185,200), xrange(201,206), xrange(207,250))]),
'WminusHToSSTodddd_tau10mm_M55_2017': _fromnum0("/store/group/lpclonglived/pkotamni/WminusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-10_TuneCP5_13TeV-powheg-pythia8/NtupleULV30LepMum_2017/231130_174441", 250),
'WminusHToSSTodddd_tau30mm_M55_2017': (229, ['/store/group/lpclonglived/pkotamni/WminusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-30_TuneCP5_13TeV-powheg-pythia8/NtupleULV30LepMum_2017/231130_174442/0000/ntuple_%i.root' % i for i in chain(xrange(15), xrange(16,141), xrange(142,148), xrange(149,153), xrange(154,165), xrange(166,171), xrange(172,176), xrange(177,188), xrange(191,196), xrange(198,212), xrange(213,226), xrange(227,229), xrange(232,235), xrange(238,240), xrange(243,249), [189, 230, 241])]),
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
