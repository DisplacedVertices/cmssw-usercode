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
    #return [('root://cmsxrootd.fnal.gov/' + fn) if fn.startswith('/store/user') else fn for fn in fns]
    return [('root://cmsxrootd.hep.wisc.edu/' + fn) if fn.startswith('/store/user') else fn for fn in fns]

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

# _add_ds("miniaod",{
#     'qcdmupt15_2017': (1, ['/store/mc/RunIISummer20UL17MiniAOD/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/100000/034AE4F2-7180-7F40-81D6-740D15738CBA.root'])
# })

# _add_ds("miniaod",{
#     'wjetstolnu_2017': (1, ['/store/mc/RunIISummer20UL17MiniAODv2/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v1/00000/0434B82A-0702-3645-9019-624DBC8A79E6.root'])
# })

# _add_ds("miniaod", {
#     'qcdht0200_2017': (1, ['/store/mc/RunIISummer19UL18MiniAODv2/QCD_HT200to300_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1/270000/007919B8-D4A9-0D45-A55A-172C009CFB81.root'])
# })


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


_add_ds("ntupleulv1lepm", {
'mfv_stopld_tau000100um_M0200_2018': _fromnum0("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_0p1mm_TuneCP5_13TeV-pythia8/NtupleULV1Lepm_2018/220523_063334", 21),
'mfv_stopld_tau000300um_M0200_2018': _fromnum0("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_0p3mm_TuneCP5_13TeV-pythia8/NtupleULV1Lepm_2018/220523_063335", 21),
'mfv_stopld_tau000100um_M0600_2018': _fromnum0("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_0p1mm_TuneCP5_13TeV-pythia8/NtupleULV1Lepm_2018/220523_063336", 15),
'mfv_stopld_tau000300um_M0600_2018': _fromnum0("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_0p3mm_TuneCP5_13TeV-pythia8/NtupleULV1Lepm_2018/220523_063337", 15),
'mfv_stopld_tau000100um_M1000_2018': _fromnum0("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_0p1mm_TuneCP5_13TeV-pythia8/NtupleULV1Lepm_2018/220523_093252", 11),
'mfv_stopld_tau000300um_M1000_2018': _fromnum0("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_0p3mm_TuneCP5_13TeV-pythia8/NtupleULV1Lepm_2018/220523_063339", 14),
'mfv_stopld_tau001000um_M1000_2018': _fromnum0("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_0p1mm_TuneCP5_13TeV-pythia8/NtupleULV1Lepm_2018/220523_063340", 13),
'mfv_stopld_tau000100um_M1600_2018': _fromnum0("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_0p1mm_TuneCP5_13TeV-pythia8/NtupleULV1Lepm_2018/220523_063341", 12),
'mfv_stopld_tau000300um_M1600_2018': _fromnum0("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_0p3mm_TuneCP5_13TeV-pythia8/NtupleULV1Lepm_2018/220523_093256", 10),
})

_add_ds("ntupleulv1lepm", {
'qcdmupt15_2017': (172, ['/store/user/awarden/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/NtupleULV1Lepm_2017/220701_133510/0000/ntuple_%i.root' % i for i in chain(xrange(1,24), xrange(25,27), xrange(28,30), xrange(31,176))]),
'qcdempt020_2017': (125, ['/store/user/awarden/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV1Lepm_2017/220701_133526/0000/ntuple_%i.root' % i for i in chain(xrange(1,118), xrange(119,127))]),
'qcdempt030_2017': (50, ['/store/user/awarden/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV1Lepm_2017/220701_133542/0000/ntuple_%i.root' % i for i in chain(xrange(1,50), [51])]),
'qcdempt050_2017': _fromnum1("/store/user/awarden/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV1Lepm_2017/220701_133559", 48),
'qcdempt080_2017': _fromnum1("/store/user/awarden/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV1Lepm_2017/220701_133615", 48),
'qcdempt120_2017': (61, ['/store/user/awarden/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV1Lepm_2017/220701_133631/0000/ntuple_%i.root' % i for i in chain(xrange(1,7), xrange(8,63))]),
'qcdempt170_2017': (27, ['/store/user/awarden/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV1Lepm_2017/220701_133648/0000/ntuple_%i.root' % i for i in chain(xrange(1,6), xrange(7,29))]),
'qcdbctoept020_2017': (66, ['/store/user/awarden/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/NtupleULV1Lepm_2017/220701_133706/0000/ntuple_%i.root' % i for i in chain(xrange(1,6), xrange(7,31), xrange(32,69))]),
'qcdbctoept030_2017': (72, ['/store/user/awarden/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/NtupleULV1Lepm_2017/220701_133724/0000/ntuple_%i.root' % i for i in chain(xrange(1,20), xrange(21,39), xrange(40,42), xrange(45,77), [43])]),
'qcdbctoept080_2017': (52, ['/store/user/awarden/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/NtupleULV1Lepm_2017/220701_133741/0000/ntuple_%i.root' % i for i in chain(xrange(1,8), xrange(9,54))]),
'qcdbctoept170_2017': (66, ['/store/user/awarden/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/NtupleULV1Lepm_2017/220701_133758/0000/ntuple_%i.root' % i for i in chain(xrange(1,12), xrange(15,70))]),
'qcdbctoept250_2017': (37, ['/store/user/awarden/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/NtupleULV1Lepm_2017/220701_133816/0000/ntuple_%i.root' % i for i in chain(xrange(1,5), xrange(6,8), xrange(15,44), [10, 12])]),
'wjetstolnu_2017': (174, ['/store/user/awarden/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV1Lepm_2017/220701_133833/0000/ntuple_%i.root' % i for i in chain(xrange(1,21), xrange(22,103), xrange(105,178))]),
'dyjetstollM10_2017': (151, ['/store/user/awarden/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV1Lepm_2017/220701_133852/0000/ntuple_%i.root' % i for i in chain(xrange(1,16), xrange(17,44), xrange(45,96), xrange(97,155))]),
'dyjetstollM50_2017': _fromnum1("/store/user/awarden/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV1Lepm_2017/220701_133909", 127),
'ttbar_2017': _fromnum0("/store/user/awarden/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleULV1Lepm_2017/220701_084008", 1019),
'ww_2017': _fromnum1("/store/user/awarden/WW_TuneCP5_13TeV-pythia8/NtupleULV1Lepm_2017/220701_133927", 34),
'zz_2017': _fromnum1("/store/user/awarden/WZ_TuneCP5_13TeV-pythia8/NtupleULV1Lepm_2017/220701_133949", 18),
'wz_2017': _fromnum1("/store/user/awarden/ZZ_TuneCP5_13TeV-pythia8/NtupleULV1Lepm_2017/220701_134007", 20),
'SingleMuon2017B': (116, ['/store/user/awarden/SingleMuon/NtupleULV1Lepm_2017/220704_050430/0000/ntuple_%i.root' % i for i in chain(xrange(25), xrange(26,80), xrange(81,96), xrange(97,119))]),
'SingleMuon2017C': (150, ['/store/user/awarden/SingleMuon/NtupleULV1Lepm_2017/220705_164022/0000/ntuple_%i.root' % i for i in chain(xrange(1,19), xrange(20,84), xrange(85,94), xrange(95,154))]),
'SingleMuon2017D': (67, ['/store/user/awarden/SingleMuon/NtupleULV1Lepm_2017/220704_050431/0000/ntuple_%i.root' % i for i in chain(xrange(30), xrange(31,68))]),
'SingleMuon2017E': (153, ['/store/user/awarden/SingleMuon/NtupleULV1Lepm_2017/220704_100333/0000/ntuple_%i.root' % i for i in chain(xrange(1,77), xrange(78,98), xrange(99,103), xrange(104,126), xrange(127,158))]),
'SingleMuon2017F': (213, ['/store/user/awarden/SingleMuon/NtupleULV1Lepm_2017/220704_100352/0000/ntuple_%i.root' % i for i in chain(xrange(1,4), xrange(5,37), xrange(38,62), xrange(63,89), xrange(90,133), xrange(134,143), xrange(144,220))]),
'SingleElectron2017B': (63, ['/store/user/awarden/SingleElectron/NtupleULV1Lepm_2017/220704_050432/0000/ntuple_%i.root' % i for i in chain(xrange(24), xrange(25,64))]),
'SingleElectron2017C': (121, ['/store/user/awarden/SingleElectron/NtupleULV1Lepm_2017/220704_100410/0000/ntuple_%i.root' % i for i in chain(xrange(1,31), xrange(32,71), xrange(72,88), xrange(89,125))]),
'SingleElectron2017D': (49, ['/store/user/awarden/SingleElectron/NtupleULV1Lepm_2017/220704_050433/0000/ntuple_%i.root' % i for i in chain(xrange(14), xrange(15,50))]),
'SingleElectron2017E': (114, ['/store/user/awarden/SingleElectron/NtupleULV1Lepm_2017/220704_050434/0000/ntuple_%i.root' % i for i in chain(xrange(16), xrange(17,24), xrange(25,60), xrange(61,69), xrange(70,73), xrange(74,92), xrange(93,120))]),
'SingleElectron2017F': (165, ['/store/user/awarden/SingleElectron/NtupleULV1Lepm_2017/220704_100428/0000/ntuple_%i.root' % i for i in chain(xrange(1,7), xrange(9,17), xrange(18,25), xrange(26,37), xrange(38,41), xrange(42,103), xrange(104,110), xrange(111,118), xrange(119,135), xrange(136,140), xrange(141,154), xrange(155,178))]),
})

# _add_ds("trackingtreerulv1_lepm_cut0", {
# 'ttbar_2017': (143, ['/store/user/awarden/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/TrackingTreerULV1_Lepm_cut0_2017/220715_042306/0000/trackingtreer_%i.root' % i for i in chain(xrange(110), xrange(113,115), xrange(118,120), xrange(125,127), xrange(129,132), xrange(213,215), xrange(240,242), xrange(250,253), [111, 116, 123, 135, 143, 151, 153, 165, 202, 204, 206, 219, 223, 227, 233, 235, 254])]),
# })
_add_ds("trackingtreerulv1_lepm_cut0", {
'qcdempt015_2017': _fromnum1("/store/user/awarden/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/TrackingTreerULV1_Lepm_cut0_2017/220721_155305", 39, fnbase="trackingtreer"),
'qcdmupt15_2017': (171, ['/store/user/awarden/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/TrackingTreerULV1_Lepm_cut0_2017/220721_155320/0000/trackingtreer_%i.root' % i for i in chain(xrange(1,15), xrange(16,25), xrange(26,51), xrange(52,156), xrange(157,176))]),
'qcdempt020_2017': _fromnum1("/store/user/awarden/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/TrackingTreerULV1_Lepm_cut0_2017/220721_155334", 123, fnbase="trackingtreer"),
'qcdempt030_2017': (46, ['/store/user/awarden/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/TrackingTreerULV1_Lepm_cut0_2017/220721_155347/0000/trackingtreer_%i.root' % i for i in chain(xrange(1,46), [47])]),
'qcdempt050_2017': (41, ['/store/user/awarden/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/TrackingTreerULV1_Lepm_cut0_2017/220721_155401/0000/trackingtreer_%i.root' % i for i in chain(xrange(1,41), [42])]),
'qcdempt080_2017': _fromnum0("/store/user/awarden/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/TrackingTreerULV1_Lepm_cut0_2017/220721_155415", 41, fnbase="trackingtreer"),
'qcdempt120_2017': (55, ['/store/user/awarden/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/TrackingTreerULV1_Lepm_cut0_2017/220721_155429/0000/trackingtreer_%i.root' % i for i in chain(xrange(1,5), xrange(6,57))]),
'qcdempt170_2017': _fromnum1("/store/user/awarden/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/TrackingTreerULV1_Lepm_cut0_2017/220721_155444", 27, fnbase="trackingtreer"),
'qcdempt300_2017': _fromnum1("/store/user/awarden/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/TrackingTreerULV1_Lepm_cut0_2017/220721_155458", 19, fnbase="trackingtreer"),
'qcdbctoept020_2017': (64, ['/store/user/awarden/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/TrackingTreerULV1_Lepm_cut0_2017/220721_155512/0000/trackingtreer_%i.root' % i for i in chain(xrange(1,10), xrange(11,66))]),
'qcdbctoept030_2017': _fromnum1("/store/user/awarden/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/TrackingTreerULV1_Lepm_cut0_2017/220721_155526", 69, fnbase="trackingtreer"),
'qcdbctoept080_2017': (50, ['/store/user/awarden/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/TrackingTreerULV1_Lepm_cut0_2017/220721_155540/0000/trackingtreer_%i.root' % i for i in chain(xrange(1,50), [51])]),
'qcdbctoept170_2017': (60, ['/store/user/awarden/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/TrackingTreerULV1_Lepm_cut0_2017/220721_155556/0000/trackingtreer_%i.root' % i for i in chain(xrange(1,14), xrange(15,62))]),
'qcdbctoept250_2017': (32, ['/store/user/awarden/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/TrackingTreerULV1_Lepm_cut0_2017/220721_155609/0000/trackingtreer_%i.root' % i for i in chain(xrange(1,9), xrange(15,38), [13])]),
'wjetstolnu_2017': (125, ['/store/user/awarden/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/TrackingTreerULV1_Lepm_cut0_2017/220715_092212/0000/trackingtreer_%i.root' % i for i in chain(xrange(1,26), xrange(28,121), xrange(122,129))]),
'dyjetstollM10_2017': (106, ['/store/user/awarden/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/TrackingTreerULV1_Lepm_cut0_2017/220715_092234/0000/trackingtreer_%i.root' % i for i in chain(xrange(1,20), xrange(21,108))]),
'dyjetstollM50_2017': (57, ['/store/user/awarden/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/TrackingTreerULV1_Lepm_cut0_2017/220715_092259/0000/trackingtreer_%i.root' % i for i in chain(xrange(1,7), xrange(10,15), xrange(19,23), xrange(24,27), xrange(35,43), xrange(45,50), xrange(51,55), xrange(56,70), xrange(71,75), [8, 17, 29, 32])]),
'ttbar_2017': (143, ['/store/user/awarden/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/TrackingTreerULV1_Lepm_cut0_2017/220715_042306/0000/trackingtreer_%i.root' % i for i in chain(xrange(110), xrange(113,115), xrange(118,120), xrange(125,127), xrange(129,132), xrange(213,215), xrange(240,242), xrange(250,253), [111, 116, 123, 135, 143, 151, 153, 165, 202, 204, 206, 219, 223, 227, 233, 235, 254])]),
'ww_2017': (19, ['/store/user/awarden/WW_TuneCP5_13TeV-pythia8/TrackingTreerULV1_Lepm_cut0_2017/220721_155627/0000/trackingtreer_%i.root' % i for i in chain(xrange(1,3), xrange(4,17), xrange(18,21), [22])]),
'zz_2017': _fromnum1("/store/user/awarden/WZ_TuneCP5_13TeV-pythia8/TrackingTreerULV1_Lepm_cut0_2017/220721_155641", 13, fnbase="trackingtreer"),
'wz_2017': _fromnum1("/store/user/awarden/ZZ_TuneCP5_13TeV-pythia8/TrackingTreerULV1_Lepm_cut0_2017/220721_155655", 19, fnbase="trackingtreer"),
'SingleMuon2017B': _fromnum0("/store/user/awarden/SingleMuon/TrackingTreerULV1_Lepm_cut0_2017/220721_105656", 60, fnbase="trackingtreer"),
'SingleMuon2017C': (72, ['/store/user/awarden/SingleMuon/TrackingTreerULV1_Lepm_cut0_2017/220722_122209/0000/trackingtreer_%i.root' % i for i in chain(xrange(1,62), xrange(66,68), xrange(71,79), [64])]),
'SingleMuon2017D': _fromnum0("/store/user/awarden/SingleMuon/TrackingTreerULV1_Lepm_cut0_2017/220721_105658", 34, fnbase="trackingtreer"),
'SingleMuon2017E': (84, ['/store/user/awarden/SingleMuon/TrackingTreerULV1_Lepm_cut0_2017/220721_105659/0000/trackingtreer_%i.root' % i for i in chain(xrange(5), xrange(6,33), xrange(34,86))]),
'SingleMuon2017F': (104, ['/store/user/awarden/SingleMuon/TrackingTreerULV1_Lepm_cut0_2017/220722_122223/0000/trackingtreer_%i.root' % i for i in chain(xrange(1,3), xrange(4,14), xrange(15,33), xrange(34,59), xrange(60,91), xrange(92,98), xrange(99,111))]),
'SingleElectron2017B': _fromnum0("/store/user/awarden/SingleElectron/TrackingTreerULV1_Lepm_cut0_2017/220721_105701", 32, fnbase="trackingtreer"),
'SingleElectron2017C': (62, ['/store/user/awarden/SingleElectron/TrackingTreerULV1_Lepm_cut0_2017/220721_105702/0000/trackingtreer_%i.root' % i for i in chain(xrange(2), xrange(3,51), xrange(52,64))]),
'SingleElectron2017D': _fromnum0("/store/user/awarden/SingleElectron/TrackingTreerULV1_Lepm_cut0_2017/220721_105703", 25, fnbase="trackingtreer"),
'SingleElectron2017E': _fromnum0("/store/user/awarden/SingleElectron/TrackingTreerULV1_Lepm_cut0_2017/220721_105704", 60, fnbase="trackingtreer"),
'SingleElectron2017F': (87, ['/store/user/awarden/SingleElectron/TrackingTreerULV1_Lepm_cut0_2017/220722_122238/0000/trackingtreer_%i.root' % i for i in chain(xrange(1,11), xrange(12,20), xrange(21,40), xrange(41,49), xrange(50,92))]),
})

# tracking treer cut 0 but with lepton info; event filter and trigger filter were applied
_add_ds("trackingtreerulv1_lepm_wlep", {
'wjetstolnu_2017': (117, ['/store/user/awarden/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/TrackingTreerULV1_Lepm_wlep_2017/220907_100104/0000/trackingtreer_%i.root' % i for i in chain(xrange(1,26), xrange(27,119))]),
'dyjetstollM10_2017': (95, ['/store/user/awarden/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/TrackingTreerULV1_Lepm_wlep_2017/220907_100120/0000/trackingtreer_%i.root' % i for i in chain(xrange(1,20), xrange(23,28), xrange(29,33), xrange(34,101))]),
'dyjetstollM50_2017': (60, ['/store/user/awarden/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/TrackingTreerULV1_Lepm_wlep_2017/220907_100134/0000/trackingtreer_%i.root' % i for i in chain(xrange(1,7), xrange(8,19), xrange(20,23), xrange(24,27), xrange(41,67), xrange(70,75), [28, 30, 32, 37, 39, 68])]),
'SingleMuon2017B': _fromnum0("/store/user/awarden/SingleMuon/TrackingTreerULV1_Lepm_wlep_2017/220907_063427", 60, fnbase="trackingtreer"),
'SingleMuon2017C': (72, ['/store/user/awarden/SingleMuon/TrackingTreerULV1_Lepm_wlep_2017/220907_100033/0000/trackingtreer_%i.root' % i for i in chain(xrange(1,6), xrange(8,10), xrange(11,22), xrange(24,65), xrange(66,79))]),
'SingleMuon2017D': _fromnum0("/store/user/awarden/SingleMuon/TrackingTreerULV1_Lepm_wlep_2017/220907_063428", 34, fnbase="trackingtreer"),
'SingleMuon2017E': (84, ['/store/user/awarden/SingleMuon/TrackingTreerULV1_Lepm_wlep_2017/220907_063429/0000/trackingtreer_%i.root' % i for i in chain(xrange(5), xrange(6,82), xrange(83,86))]),
'SingleMuon2017F': (90, ['/store/user/awarden/SingleMuon/TrackingTreerULV1_Lepm_wlep_2017/220907_100048/0000/trackingtreer_%i.root' % i for i in chain(xrange(1,16), xrange(17,21), xrange(22,44), xrange(45,50), xrange(51,54), xrange(58,63), xrange(71,77), xrange(78,80), xrange(83,89), xrange(90,96), xrange(97,105), xrange(108,110), [55, 64, 66, 69, 81, 106])]),
'SingleElectron2017B': _fromnum0("/store/user/awarden/SingleElectron/TrackingTreerULV1_Lepm_wlep_2017/220907_063430", 32, fnbase="trackingtreer"),
'SingleElectron2017C': (63, ['/store/user/awarden/SingleElectron/TrackingTreerULV1_Lepm_wlep_2017/220907_063431/0000/trackingtreer_%i.root' % i for i in chain(xrange(46), xrange(47,64))]),
'SingleElectron2017D': _fromnum0("/store/user/awarden/SingleElectron/TrackingTreerULV1_Lepm_wlep_2017/220907_063432", 25, fnbase="trackingtreer"),
'SingleElectron2017E': _fromnum0("/store/user/awarden/SingleElectron/TrackingTreerULV1_Lepm_wlep_2017/220907_063433", 60, fnbase="trackingtreer"),
'SingleElectron2017F': (81, ['/store/user/awarden/SingleElectron/TrackingTreerULV1_Lepm_wlep_2017/220907_090445/0000/trackingtreer_%i.root' % i for i in chain(xrange(1,10), xrange(11,14), xrange(15,17), xrange(18,23), xrange(24,34), xrange(37,54), xrange(55,62), xrange(64,91), [35])]),
})

#Newest tracking treer cut 0 with sel lepton tracks & good lepton sel tracks; event filter and trigger filter were applied
_add_ds("trackingtreerulv1_lepm_wsellep", {
'wjetstolnu_2017': (114, ['/store/user/awarden/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/TrackingTreerULV1_Lepm_wsellep_2017/220913_200259/0000/trackingtreer_%i.root' % i for i in chain(xrange(1,6), xrange(7,18), xrange(19,27), xrange(28,118))]),
'dyjetstollM10_2017': (90, ['/store/user/awarden/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/TrackingTreerULV1_Lepm_wsellep_2017/220913_200316/0000/trackingtreer_%i.root' % i for i in chain(xrange(1,3), xrange(4,17), xrange(24,98), [21])]),
'dyjetstollM50_2017': (59, ['/store/user/awarden/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/TrackingTreerULV1_Lepm_wsellep_2017/220913_200331/0000/trackingtreer_%i.root' % i for i in chain(xrange(1,3), xrange(4,7), xrange(10,13), xrange(14,22), xrange(25,27), xrange(28,30), xrange(36,38), xrange(43,75), [8, 23, 32, 39, 41])]),                                                                                                                                                                                              
'SingleMuon2017B': _fromnum0("/store/user/awarden/SingleMuon/TrackingTreerULV1_Lepm_wsellep_2017/220913_150334", 60, fnbase="trackingtreer"),
'SingleMuon2017C': _fromnum1("/store/user/awarden/SingleMuon/TrackingTreerULV1_Lepm_wsellep_2017/220913_200213", 78, fnbase="trackingtreer"),
'SingleMuon2017D': _fromnum0("/store/user/awarden/SingleMuon/TrackingTreerULV1_Lepm_wsellep_2017/220913_150335", 34, fnbase="trackingtreer"),
'SingleMuon2017E': _fromnum0("/store/user/awarden/SingleMuon/TrackingTreerULV1_Lepm_wsellep_2017/220913_150336", 86, fnbase="trackingtreer"),
'SingleMuon2017F': _fromnum1("/store/user/awarden/SingleMuon/TrackingTreerULV1_Lepm_wsellep_2017/220913_200228", 109, fnbase="trackingtreer"),
'SingleElectron2017B': _fromnum0("/store/user/awarden/SingleElectron/TrackingTreerULV1_Lepm_wsellep_2017/220913_150337", 32, fnbase="trackingtreer"),
'SingleElectron2017C': (51, ['/store/user/awarden/SingleElectron/TrackingTreerULV1_Lepm_wsellep_2017/220913_150338/0000/trackingtreer_%i.root' % i for i in chain(xrange(7), xrange(9,21), xrange(22,28), xrange(30,37), xrange(38,41), xrange(44,50), xrange(51,53), xrange(54,57), xrange(58,61), [42, 63])]),                                                                                                                                                                                                                             
'SingleElectron2017D': _fromnum0("/store/user/awarden/SingleElectron/TrackingTreerULV1_Lepm_wsellep_2017/220913_150339", 25, fnbase="trackingtreer"),
'SingleElectron2017E': _fromnum0("/store/user/awarden/SingleElectron/TrackingTreerULV1_Lepm_wsellep_2017/220913_150340", 60, fnbase="trackingtreer"),
'SingleElectron2017F': _fromnum1("/store/user/awarden/SingleElectron/TrackingTreerULV1_Lepm_wsellep_2017/220913_200245", 90, fnbase="trackingtreer"),
})

_add_ds("trackingtreerulv1_lepm_cut1", {
'wjetstolnu_2017': (122, ['/store/user/awarden/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/TrackingTreerULV1_Lepm_cut1_2017/220719_120543/0000/trackingtreer_%i.root' % i for i in chain(xrange(1,15), xrange(16,26), xrange(27,31), xrange(33,107), xrange(108,116), xrange(117,129))]),
'dyjetstollM10_2017': (101, ['/store/user/awarden/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/TrackingTreerULV1_Lepm_cut1_2017/220719_120558/0000/trackingtreer_%i.root' % i for i in chain(xrange(1,5), xrange(6,20), xrange(22,24), xrange(27,69), xrange(70,108), [25])]),
'dyjetstollM50_2017': (56, ['/store/user/awarden/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/TrackingTreerULV1_Lepm_cut1_2017/220719_120612/0000/trackingtreer_%i.root' % i for i in chain(xrange(1,7), xrange(8,12), xrange(13,24), xrange(25,27), xrange(44,75), [32, 36])]),
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
