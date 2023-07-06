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
        #test: trying [15:num+15] because having issues only at a particular ntuple; want to investigate PLEASE CHANGE back to [:num]
        #fns = fns[15:num+15]
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

# _add_ds("miniaod", {
#     'mfv_stoplb_tau010000um_M0800_2018' : (1, ['/store/mc/RunIISummer20UL18MiniAODv2/DisplacedSUSY_stopToLBottom_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/40000/278F6548-7D8A-B14A-858A-83B19898CC09.root'])
# })

# _add_ds("miniaod", {
#     'mfv_stoplb_tau000300um_M0800_2018' : (1, ['/store/mc/RunIISummer20UL18MiniAODv2/DisplacedSUSY_stopToLBottom_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/30000/1140EC5A-A7C4-794C-9557-D64D8D5AFFC1.root'])
# })

_add_ds("miniaod", {
    'mfv_stopld_tau010000um_M0800_2018' : (3, ['/store/mc/RunIISummer20UL18MiniAODv2/DisplacedSUSY_stopToLD_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/40000/181536B9-11E5-2344-9E8E-BACCD7482A0A.root', '/store/mc/RunIISummer20UL18MiniAODv2/DisplacedSUSY_stopToLD_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/40000/21602664-E4E1-3E48-A244-2D131F063685.root', '/store/mc/RunIISummer20UL18MiniAODv2/DisplacedSUSY_stopToLD_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/40000/27A92C07-345E-1B48-98D9-F1C966151362.root'])
})

# _add_ds("miniaod", {
#     'mfv_stopld_tau000300um_M0800_2018' : (1, ['/store/mc/RunIISummer20UL18MiniAODv2/DisplacedSUSY_stopToLD_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/40000/274E0D1F-BA99-6F4A-AC01-12A9D425B07B.root'])
# })

_add_ds("miniaod", {
    'mfv_neu_tau010000um_M0800_2018' : (1, ['/store/mc/RunIIAutumn18MiniAOD/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-10mm_TuneCP2_13TeV_2018-pythia8/MINIAODSIM/102X_upgrade2018_realistic_v15-v1/20000/3B3E7C27-6D86-0E41-8473-041DF57E92C0.root'])
})

_add_ds("miniaod", {
    'ttbar_2018' : (1, ['/store/mc/RunIISummer20UL18MiniAODv2/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/110000/EB3E0EF8-A62F-C341-99F3-7374A6058231.root'])
})

# _add_ds("ntupleulv1lepm", {
#     'test' : (1, ['file:/afs/hep.wisc.edu/home/acwarden/work/llp/mfv_1068p1/src/JMTucker/MFVNeutralino/test/ntuple.root'])
# })

_add_ds("ntupleulv5lepm", {
    'test' : (1, ['file:/afs/hep.wisc.edu/home/acwarden/work/llp/mfv_1068p1/src/JMTucker/MFVNeutralino/test/ntuple.root'])
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
    #'mfv_stopld_tau000100um_M0600_2018':_fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_0p1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18_MiniAOD/220518_074432/0000", 5, fnbase="MiniAOD", numbereddirs=False),
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


_add_ds("trackmoverulv30lepmumv5", {
'qcdempt015_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv5_2017/230626_221505", 47, fnbase="movedtree"),
'qcdmupt15_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv5_2017/230626_221525", 154, fnbase="movedtree"),
'qcdempt020_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv5_2017/230626_221545", 103, fnbase="movedtree"),
'qcdempt030_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv5_2017/230626_221605", 69, fnbase="movedtree"),
'qcdempt050_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv5_2017/230626_221624", 76, fnbase="movedtree"),
'qcdempt080_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv5_2017/230626_221644", 69, fnbase="movedtree"),
'qcdempt120_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv5_2017/230626_221704", 87, fnbase="movedtree"),
'qcdempt170_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv5_2017/230626_221724", 37, fnbase="movedtree"),
'qcdempt300_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv5_2017/230626_221743", 24, fnbase="movedtree"),
'qcdbctoept020_2017': (92, ['/store/user/pekotamn/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/TrackMoverULV30LepMumv5_2017/230626_221803/0000/movedtree_%i.root' % i for i in chain(xrange(1,46), xrange(47,94))]),
'qcdbctoept030_2017': (86, ['/store/user/pekotamn/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/TrackMoverULV30LepMumv5_2017/230626_221822/0000/movedtree_%i.root' % i for i in chain(xrange(1,55), xrange(57,89))]),
'qcdbctoept080_2017': (83, ['/store/user/pekotamn/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/TrackMoverULV30LepMumv5_2017/230626_221842/0000/movedtree_%i.root' % i for i in chain(xrange(1,46), xrange(47,85))]),
'qcdbctoept170_2017': _fromnum1("/store/user/pekotamn/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/TrackMoverULV30LepMumv5_2017/230626_221902", 91, fnbase="movedtree"),
'qcdbctoept250_2017': _fromnum1("/store/user/pekotamn/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/TrackMoverULV30LepMumv5_2017/230626_221921", 79, fnbase="movedtree"),
'wjetstolnu_2017': (403, ['/store/user/pekotamn/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverULV30LepMumv5_2017/230626_222302/0000/movedtree_%i.root' % i for i in chain(xrange(1,212), xrange(213,405))]),
'wjetstolnu_amcatnlo_2017': _fromnum1("/store/user/pekotamn/WJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-pythia8/TrackMoverULV30LepMumv5_2017/230626_222321", 159, fnbase="movedtree"),
'dyjetstollM10_2017': _fromnum1("/store/user/pekotamn/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverULV30LepMumv5_2017/230626_222342", 393, fnbase="movedtree"),
'dyjetstollM50_2017': (437, ['/store/user/pekotamn/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverULV30LepMumv5_2017/230627_164104/0000/movedtree_%i.root' % i for i in chain(xrange(1,94), xrange(95,336), xrange(337,440))]),
'ttbar_2017': (1468, ['/store/user/pkotamni/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/TrackMoverULV30LepMumv5_2017/230626_172505' + '/%04i/movedtree_%i.root' % (i/1000,i) for i in chain(xrange(68), xrange(69,160), xrange(161,219), xrange(220,343), xrange(344,365), xrange(366,537), xrange(538,645), xrange(646,677), xrange(678,861), xrange(862,1167), xrange(1168,1250), xrange(1251,1269), xrange(1270,1449), xrange(1450,1472), xrange(1473,1482))]),
'ww_2017': (92, ['/store/user/pekotamn/WW_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv5_2017/230626_222421/0000/movedtree_%i.root' % i for i in chain(xrange(1,45), xrange(46,94))]),
'zz_2017': _fromnum1("/store/user/pekotamn/ZZ_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv5_2017/230626_222444", 25, fnbase="movedtree"),
'wz_2017': (42, ['/store/user/pekotamn/WZ_TuneCP5_13TeV-pythia8/TrackMoverULV30LepMumv5_2017/230626_222504/0000/movedtree_%i.root' % i for i in chain(xrange(1,35), xrange(36,44))]),
'SingleMuon2017B': _fromnum1("/store/user/pekotamn/SingleMuon/TrackMoverULV30LepMumv5_2017/230626_221942", 325, fnbase="movedtree"),
'SingleMuon2017C': _fromnum1("/store/user/pekotamn/SingleMuon/TrackMoverULV30LepMumv5_2017/230626_222002", 505, fnbase="movedtree"),
'SingleMuon2017D': (206, ['/store/user/pekotamn/SingleMuon/TrackMoverULV30LepMumv5_2017/230626_222022/0000/movedtree_%i.root' % i for i in chain(xrange(1,34), xrange(35,66), xrange(67,121), xrange(122,159), xrange(160,162), xrange(163,182), xrange(183,190), xrange(191,214))]),
'SingleMuon2017E': (495, ['/store/user/pekotamn/SingleMuon/TrackMoverULV30LepMumv5_2017/230626_222042/0000/movedtree_%i.root' % i for i in chain(xrange(1,341), xrange(342,491), xrange(492,498))]),
'SingleMuon2017F': _fromnum1("/store/user/pekotamn/SingleMuon/TrackMoverULV30LepMumv5_2017/230626_222101", 725, fnbase="movedtree"),
'SingleElectron2017B': _fromnum1("/store/user/pekotamn/SingleElectron/TrackMoverULV30LepMumv5_2017/230626_222121", 200, fnbase="movedtree"),
'SingleElectron2017C': _fromnum1("/store/user/pekotamn/SingleElectron/TrackMoverULV30LepMumv5_2017/230626_222141", 408, fnbase="movedtree"),
'SingleElectron2017D': _fromnum1("/store/user/pekotamn/SingleElectron/TrackMoverULV30LepMumv5_2017/230626_222202", 163, fnbase="movedtree"),
'SingleElectron2017E': (358, ['/store/user/pekotamn/SingleElectron/TrackMoverULV30LepMumv5_2017/230626_222222/0000/movedtree_%i.root' % i for i in chain(xrange(1,43), xrange(48,117), xrange(118,144), xrange(145,154), xrange(157,182), xrange(183,233), xrange(234,238), xrange(239,270), xrange(271,277), xrange(278,280), xrange(281,293), xrange(294,305), xrange(306,343), xrange(344,355), xrange(356,376), [44, 46, 155])]),
'SingleElectron2017F': _fromnum1("/store/user/pekotamn/SingleElectron/TrackMoverULV30LepMumv5_2017/230626_222242", 576, fnbase="movedtree"),
})


_add_ds("trackmoverulv30lepelemv5", {
'qcdempt015_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepElemv5_2017/230626_222621", 47, fnbase="movedtree"),
'qcdmupt15_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/TrackMoverULV30LepElemv5_2017/230626_222643", 154, fnbase="movedtree"),
'qcdempt020_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepElemv5_2017/230626_222702", 103, fnbase="movedtree"),
'qcdempt030_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepElemv5_2017/230626_222722", 69, fnbase="movedtree"),
'qcdempt050_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepElemv5_2017/230626_222742", 76, fnbase="movedtree"),
'qcdempt080_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepElemv5_2017/230626_222801", 69, fnbase="movedtree"),
'qcdempt120_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepElemv5_2017/230626_222820", 87, fnbase="movedtree"),
'qcdempt170_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepElemv5_2017/230626_222840", 37, fnbase="movedtree"),
'qcdempt300_2017': _fromnum1("/store/user/pekotamn/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/TrackMoverULV30LepElemv5_2017/230626_222901", 24, fnbase="movedtree"),
'qcdbctoept020_2017': (92, ['/store/user/pekotamn/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/TrackMoverULV30LepElemv5_2017/230626_222920/0000/movedtree_%i.root' % i for i in chain(xrange(1,46), xrange(47,94))]),
'qcdbctoept030_2017': (86, ['/store/user/pekotamn/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/TrackMoverULV30LepElemv5_2017/230626_222941/0000/movedtree_%i.root' % i for i in chain(xrange(1,55), xrange(57,89))]),
'qcdbctoept080_2017': (83, ['/store/user/pekotamn/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/TrackMoverULV30LepElemv5_2017/230626_223000/0000/movedtree_%i.root' % i for i in chain(xrange(1,46), xrange(47,85))]),
'qcdbctoept170_2017': _fromnum1("/store/user/pekotamn/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/TrackMoverULV30LepElemv5_2017/230626_223020", 91, fnbase="movedtree"),
'qcdbctoept250_2017': _fromnum1("/store/user/pekotamn/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/TrackMoverULV30LepElemv5_2017/230626_223039", 79, fnbase="movedtree"),
'wjetstolnu_2017': (403, ['/store/user/pekotamn/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverULV30LepElemv5_2017/230626_223426/0000/movedtree_%i.root' % i for i in chain(xrange(1,212), xrange(213,405))]),
'wjetstolnu_amcatnlo_2017': _fromnum1("/store/user/pekotamn/WJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-pythia8/TrackMoverULV30LepElemv5_2017/230626_223445", 159, fnbase="movedtree"),
'dyjetstollM10_2017': _fromnum1("/store/user/pekotamn/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverULV30LepElemv5_2017/230626_223504", 393, fnbase="movedtree"),
#'dyjetstollM50_2017': (432, ['/store/user/pekotamn/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverULV30LepElemv5_2017/230626_223525/0000/movedtree_%i.root' % i for i in chain(xrange(1,308), xrange(309,317), xrange(318,326), xrange(331,407), xrange(408,429), xrange(430,440), [327, 329])]),
'ttbar_2017': (1468, ['/store/user/pkotamni/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/TrackMoverULV30LepElemv5_2017/230626_173623' + '/%04i/movedtree_%i.root' % (i/1000,i) for i in chain(xrange(68), xrange(69,160), xrange(161,219), xrange(220,343), xrange(344,365), xrange(366,537), xrange(538,645), xrange(646,677), xrange(678,861), xrange(862,1167), xrange(1168,1250), xrange(1251,1269), xrange(1270,1449), xrange(1450,1472), xrange(1473,1482))]),
'ww_2017': (92, ['/store/user/pekotamn/WW_TuneCP5_13TeV-pythia8/TrackMoverULV30LepElemv5_2017/230626_223544/0000/movedtree_%i.root' % i for i in chain(xrange(1,45), xrange(46,94))]),
'zz_2017': _fromnum1("/store/user/pekotamn/ZZ_TuneCP5_13TeV-pythia8/TrackMoverULV30LepElemv5_2017/230626_223603", 25, fnbase="movedtree"),
'wz_2017': (42, ['/store/user/pekotamn/WZ_TuneCP5_13TeV-pythia8/TrackMoverULV30LepElemv5_2017/230626_223622/0000/movedtree_%i.root' % i for i in chain(xrange(1,35), xrange(36,44))]),
'SingleMuon2017B': _fromnum1("/store/user/pekotamn/SingleMuon/TrackMoverULV30LepElemv5_2017/230626_223059", 325, fnbase="movedtree"),
'SingleMuon2017C': _fromnum1("/store/user/pekotamn/SingleMuon/TrackMoverULV30LepElemv5_2017/230626_223119", 505, fnbase="movedtree"),
'SingleMuon2017D': (206, ['/store/user/pekotamn/SingleMuon/TrackMoverULV30LepElemv5_2017/230626_223140/0000/movedtree_%i.root' % i for i in chain(xrange(1,34), xrange(35,66), xrange(67,121), xrange(122,159), xrange(160,162), xrange(163,182), xrange(183,190), xrange(191,214))]),
'SingleMuon2017E': (495, ['/store/user/pekotamn/SingleMuon/TrackMoverULV30LepElemv5_2017/230626_223200/0000/movedtree_%i.root' % i for i in chain(xrange(1,341), xrange(342,491), xrange(492,498))]),
'SingleMuon2017F': _fromnum1("/store/user/pekotamn/SingleMuon/TrackMoverULV30LepElemv5_2017/230626_223221", 725, fnbase="movedtree"),
'SingleElectron2017B': _fromnum1("/store/user/pekotamn/SingleElectron/TrackMoverULV30LepElemv5_2017/230626_223242", 200, fnbase="movedtree"),
'SingleElectron2017C': _fromnum1("/store/user/pekotamn/SingleElectron/TrackMoverULV30LepElemv5_2017/230626_223303", 408, fnbase="movedtree"),
'SingleElectron2017D': (5, ['/store/user/pekotamn/SingleElectron/TrackMoverULV30LepElemv5_2017/230626_223323/0000/movedtree_%i.root' % i for i in [1, 10, 59, 71, 81]]),
'SingleElectron2017E': (358, ['/store/user/pekotamn/SingleElectron/TrackMoverULV30LepElemv5_2017/230626_223345/0000/movedtree_%i.root' % i for i in chain(xrange(1,43), xrange(48,117), xrange(118,144), xrange(145,154), xrange(157,182), xrange(183,233), xrange(234,238), xrange(239,270), xrange(271,277), xrange(278,280), xrange(281,293), xrange(294,305), xrange(306,343), xrange(344,355), xrange(356,376), [44, 46, 155])]),
'SingleElectron2017F': _fromnum1("/store/user/pekotamn/SingleElectron/TrackMoverULV30LepElemv5_2017/230626_223406", 576, fnbase="movedtree"),
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

#2017
"""
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
"""
#2018
_add_ds("ntupleulv1lepm", {
'qcdmupt15_2018': _fromnum1("/store/user/awarden/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/NtupleULV1Lepm_2018/230323_152047", 29),
'qcdempt015_2018': _fromnum1("/store/user/awarden/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV1Lepm_2018/230323_152105", 23),
'qcdempt020_2018': _fromnum1("/store/user/awarden/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV1Lepm_2018/230323_152124", 17),
'qcdempt030_2018': _fromnum1("/store/user/awarden/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV1Lepm_2018/230323_152141", 15),
'qcdempt050_2018': _fromnum1("/store/user/awarden/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV1Lepm_2018/230323_152158", 14),
'qcdempt080_2018': _fromnum1("/store/user/awarden/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV1Lepm_2018/230323_152216", 12),
'qcdempt120_2018': _fromnum1("/store/user/awarden/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV1Lepm_2018/230323_152234", 14),
'qcdempt170_2018': _fromnum1("/store/user/awarden/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV1Lepm_2018/230323_152251", 5),
'qcdempt300_2018': _fromnum1("/store/user/awarden/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV1Lepm_2018/230323_152310", 4),
'qcdbctoept015_2018': _fromnum1("/store/user/awarden/QCD_Pt_15to20_bcToE_TuneCP5_13TeV_pythia8/NtupleULV1Lepm_2018/230323_152327", 28),
'qcdbctoept020_2018': _fromnum1("/store/user/awarden/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/NtupleULV1Lepm_2018/230323_152346", 48),
'qcdbctoept030_2018': _fromnum1("/store/user/awarden/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/NtupleULV1Lepm_2018/230323_152403", 32),
'qcdbctoept080_2018': _fromnum1("/store/user/awarden/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/NtupleULV1Lepm_2018/230323_152421", 44),
'qcdbctoept170_2018': _fromnum1("/store/user/awarden/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/NtupleULV1Lepm_2018/230323_152439", 46),
'qcdbctoept250_2018': _fromnum1("/store/user/awarden/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/NtupleULV1Lepm_2018/230323_152458", 44),
'dyjetstollM10_2018': _fromnum1("/store/user/awarden/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV1Lepm_2018/230323_152516", 115),
'dyjetstollM50_2018': (91, ['/store/user/awarden/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV1Lepm_2018/230323_152535/0000/ntuple_%i.root' % i for i in chain(xrange(1,48), xrange(49,56), xrange(58,62), xrange(65,67), xrange(68,71), xrange(72,74), xrange(75,77), xrange(81,83), xrange(86,88), xrange(92,95), xrange(96,104), xrange(107,110), [63, 78, 84, 90, 105, 111])]),
'wjetstolnu_2018': _fromnum1("/store/user/awarden/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV1Lepm_2018/230323_152552", 101),
'ttbar_2018': (129, ['/store/user/awarden/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleULV1Lepm_2018/230302_035020/0000/ntuple_%i.root' % i for i in chain(xrange(13), xrange(14,130))]),
'ww_2018': _fromnum1("/store/user/awarden/WW_TuneCP5_13TeV-pythia8/NtupleULV1Lepm_2018/230323_152610", 23),
'wz_2018': (15, ['/store/user/awarden/WZ_TuneCP5_13TeV-pythia8/NtupleULV1Lepm_2018/230323_152628/0000/ntuple_%i.root' % i for i in chain(xrange(1,8), xrange(9,17))]),
'zz_2018': _fromnum1("/store/user/awarden/ZZ_TuneCP5_13TeV-pythia8/NtupleULV1Lepm_2018/230323_152645", 6),
'mfv_stoplb_tau000100um_M1000_2018': (199, ['/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_120811/0000/ntuple_%i.root' % i for i in chain(xrange(1,118), xrange(120,202))]),
'mfv_stoplb_tau000300um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_120829", 201),
'mfv_stoplb_tau010000um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_120847", 101),
'mfv_stoplb_tau001000um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_120905", 201),
'mfv_stoplb_tau030000um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_120924", 201),
'mfv_stoplb_tau000100um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_120942", 201),
'mfv_stoplb_tau000300um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_121000", 201),
'mfv_stoplb_tau010000um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_121018", 101),
'mfv_stoplb_tau001000um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_121039", 201),
'mfv_stoplb_tau030000um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_121056", 201),
'mfv_stoplb_tau000100um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_121114", 201),
'mfv_stoplb_tau000300um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_121133", 201),
'mfv_stoplb_tau010000um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_121153", 101),
'mfv_stoplb_tau001000um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_121211", 201),
'mfv_stoplb_tau030000um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_121229", 200),
'mfv_stoplb_tau000100um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_121247", 201),
'mfv_stoplb_tau000300um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_121307", 201),
'mfv_stoplb_tau010000um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_121325", 101),
'mfv_stoplb_tau001000um_M1600_2018': (100, ['/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_121342/0000/ntuple_%i.root' % i for i in chain(xrange(1,37), xrange(38,102))]),
'mfv_stoplb_tau030000um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_121359", 101),
'mfv_stoplb_tau000100um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_121417", 200),
'mfv_stoplb_tau000300um_M1800_2018': (199, ['/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_121435/0000/ntuple_%i.root' % i for i in chain(xrange(1,32), xrange(34,202))]),
'mfv_stoplb_tau010000um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_121453", 101),
'mfv_stoplb_tau001000um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_121510", 101),
'mfv_stoplb_tau030000um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_121531", 101),
'mfv_stoplb_tau000100um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_121550", 201),
'mfv_stoplb_tau000300um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_121607", 201),
'mfv_stoplb_tau010000um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_121625", 201),
'mfv_stoplb_tau001000um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_121644", 201),
'mfv_stoplb_tau030000um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_121702", 201),
'mfv_stoplb_tau000100um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_121719", 201),
'mfv_stoplb_tau000300um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_121736", 201),
'mfv_stoplb_tau010000um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_121755", 201),
'mfv_stoplb_tau030000um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_121816", 201),
'mfv_stoplb_tau000100um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_121834", 201),
'mfv_stoplb_tau000300um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_121852", 201),
'mfv_stoplb_tau010000um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_121911", 201),
'mfv_stoplb_tau030000um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_121931", 200),
'mfv_stoplb_tau000100um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_121948", 201),
'mfv_stoplb_tau000300um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_122006", 200),
'mfv_stoplb_tau010000um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_122025", 201),
'mfv_stoplb_tau001000um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_122042", 200),
'mfv_stoplb_tau030000um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_122059", 200),
'mfv_stoplb_tau000100um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_122117", 200),
'mfv_stoplb_tau000300um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_122137", 200),
'mfv_stoplb_tau010000um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_122155", 100),
'mfv_stoplb_tau001000um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_122212", 201),
'mfv_stoplb_tau030000um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_122230", 201),
'mfv_stopld_tau000100um_M1000_2018': (200, ['/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_122249/0000/ntuple_%i.root' % i for i in chain(xrange(1,85), xrange(86,202))]),
'mfv_stopld_tau000300um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_122306", 201),
'mfv_stopld_tau010000um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_122323", 101),
'mfv_stopld_tau001000um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_122341", 201),
'mfv_stopld_tau030000um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_122401", 201),
'mfv_stopld_tau000100um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_122420", 201),
'mfv_stopld_tau000300um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_122439", 201),
'mfv_stopld_tau010000um_M1200_2018': (99, ['/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_122459/0000/ntuple_%i.root' % i for i in chain(xrange(1,66), xrange(68,102))]),
'mfv_stopld_tau001000um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_122520", 201),
'mfv_stopld_tau030000um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_122538", 201),
'mfv_stopld_tau000100um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_122556", 201),
'mfv_stopld_tau000300um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_122613", 200),
'mfv_stopld_tau010000um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_122632", 101),
'mfv_stopld_tau001000um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_122650", 201),
'mfv_stopld_tau030000um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_122707", 201),
'mfv_stopld_tau000100um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_122725", 201),
'mfv_stopld_tau000300um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_122744", 201),
'mfv_stopld_tau010000um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_122803", 101),
'mfv_stopld_tau001000um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_122821", 101),
'mfv_stopld_tau030000um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_122839", 100),
'mfv_stopld_tau000100um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_122857", 201),
'mfv_stopld_tau000300um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_122914", 201),
'mfv_stopld_tau010000um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_122932", 101),
'mfv_stopld_tau001000um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_122950", 101),
'mfv_stopld_tau030000um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_123008", 101),
'mfv_stopld_tau000100um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_123025", 201),
'mfv_stopld_tau000300um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_123043", 201),
'mfv_stopld_tau010000um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_123101", 201),
'mfv_stopld_tau001000um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_123120", 201),
'mfv_stopld_tau030000um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_123138", 201),
'mfv_stopld_tau000100um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_123156", 201),
'mfv_stopld_tau000300um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_123215", 201),
'mfv_stopld_tau010000um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_123236", 201),
'mfv_stopld_tau001000um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_123255", 201),
'mfv_stopld_tau030000um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_123313", 201),
'mfv_stopld_tau000100um_M0400_2018': (198, ['/store/user/awarden/DisplacedSUSY_stopToLD_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_123334/0000/ntuple_%i.root' % i for i in chain(xrange(1,82), xrange(83,88), xrange(89,114), xrange(115,202))]),
'mfv_stopld_tau000300um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_123356", 201),
'mfv_stopld_tau010000um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_123415", 201),
'mfv_stopld_tau001000um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_123433", 201),
'mfv_stopld_tau030000um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_123450", 201),
'mfv_stopld_tau000100um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_123509", 201),
'mfv_stopld_tau000300um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_123528", 201),
'mfv_stopld_tau010000um_M0600_2018': (200, ['/store/user/awarden/DisplacedSUSY_stopToLD_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_123547/0000/ntuple_%i.root' % i for i in chain(xrange(1,70), xrange(71,202))]),
'mfv_stopld_tau001000um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_123605", 200),
'mfv_stopld_tau030000um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_123629", 201),
'mfv_stopld_tau000100um_M0800_2018': (198, ['/store/user/awarden/DisplacedSUSY_stopToLD_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_123650/0000/ntuple_%i.root' % i for i in chain(xrange(1,102), xrange(103,106), xrange(107,201))]),
'mfv_stopld_tau000300um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_123709", 201),
'mfv_stopld_tau010000um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_123729", 101),
'mfv_stopld_tau001000um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_123747", 201),
'mfv_stopld_tau030000um_M0800_2018': (200, ['/store/user/awarden/DisplacedSUSY_stopToLD_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV1Lepm_2018/230404_123807/0000/ntuple_%i.root' % i for i in chain(xrange(1,53), xrange(54,202))]),
})

#updated lepton track requirements (relaxed nsigma > 3, min r = 2 && lostinnerhits = 0 OR min r = 1) only for pt >= 20GeV leptons 
_add_ds("ntupleulv2lepm", {
'qcdmupt15_2018': _fromnum1("/store/user/awarden/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/NtupleULV2Lepm_2018/230518_093727", 29),
'qcdempt015_2018': _fromnum1("/store/user/awarden/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV2Lepm_2018/230518_093808", 19),
'qcdempt020_2018': (15, ['/store/user/awarden/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV2Lepm_2018/230518_093850/0000/ntuple_%i.root' % i for i in chain(xrange(1,5), xrange(6,13), xrange(14,18))]),
'qcdempt030_2018': _fromnum1("/store/user/awarden/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV2Lepm_2018/230518_093932", 15),
'qcdempt050_2018': _fromnum1("/store/user/awarden/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV2Lepm_2018/230518_094013", 14),
'qcdempt080_2018': (11, ['/store/user/awarden/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV2Lepm_2018/230518_094055/0000/ntuple_%i.root' % i for i in chain(xrange(1,3), xrange(4,13))]),
'qcdempt120_2018': _fromnum1("/store/user/awarden/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV2Lepm_2018/230518_094137", 14),
'qcdempt170_2018': (4, ['/store/user/awarden/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV2Lepm_2018/230518_094219/0000/ntuple_%i.root' % i for i in chain(xrange(1,3), xrange(4,6))]),
'qcdempt300_2018': _fromnum1("/store/user/awarden/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV2Lepm_2018/230518_094300", 4),
'qcdbctoept015_2018': _fromnum1("/store/user/awarden/QCD_Pt_15to20_bcToE_TuneCP5_13TeV_pythia8/NtupleULV2Lepm_2018/230518_094342", 27),
'qcdbctoept020_2018': (41, ['/store/user/awarden/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/NtupleULV2Lepm_2018/230518_094423/0000/ntuple_%i.root' % i for i in chain(xrange(1,36), xrange(38,44))]),
'qcdbctoept030_2018': _fromnum1("/store/user/awarden/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/NtupleULV2Lepm_2018/230518_094505", 30),
'qcdbctoept080_2018': (41, ['/store/user/awarden/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/NtupleULV2Lepm_2018/230518_094550/0000/ntuple_%i.root' % i for i in chain(xrange(1,38), xrange(39,43))]),
'qcdbctoept170_2018': (45, ['/store/user/awarden/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/NtupleULV2Lepm_2018/230518_094631/0000/ntuple_%i.root' % i for i in chain(xrange(1,44), xrange(45,47))]),
'qcdbctoept250_2018': (42, ['/store/user/awarden/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/NtupleULV2Lepm_2018/230518_094713/0000/ntuple_%i.root' % i for i in chain(xrange(1,20), xrange(21,44))]),
'wjetstolnu_2018': (98, ['/store/user/awarden/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV2Lepm_2018/230518_094756/0000/ntuple_%i.root' % i for i in chain(xrange(1,54), xrange(55,77), xrange(78,101))]),
'dyjetstollM10_2018': (114, ['/store/user/awarden/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV2Lepm_2018/230518_094849/0000/ntuple_%i.root' % i for i in chain(xrange(1,66), xrange(67,116))]),
'dyjetstollM50_2018': (104, ['/store/user/awarden/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV2Lepm_2018/230518_094938/0000/ntuple_%i.root' % i for i in chain(xrange(1,13), xrange(14,32), xrange(33,48), xrange(49,55), xrange(56,60), xrange(61,94), xrange(95,111))]),
'ttbar_2018': (116, ['/store/user/awarden/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleULV2Lepm_2018/230518_045156/0000/ntuple_%i.root' % i for i in chain(xrange(17), xrange(18,27), xrange(29,34), xrange(35,37), xrange(38,42), xrange(43,66), xrange(69,91), xrange(92,94), xrange(95,97), xrange(98,110), xrange(113,115), xrange(116,130), [67, 111])]),
'ww_2018': (22, ['/store/user/awarden/WW_TuneCP5_13TeV-pythia8/NtupleULV2Lepm_2018/230518_095020/0000/ntuple_%i.root' % i for i in chain(xrange(1,17), xrange(18,24))]),
'wz_2018': _fromnum1("/store/user/awarden/WZ_TuneCP5_13TeV-pythia8/NtupleULV2Lepm_2018/230518_095112", 16),
'zz_2018': _fromnum1("/store/user/awarden/ZZ_TuneCP5_13TeV-pythia8/NtupleULV2Lepm_2018/230518_095154", 6),
'mfv_stoplb_tau000100um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_152615", 201),
'mfv_stoplb_tau000300um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_152659", 201),
'mfv_stoplb_tau010000um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_152753", 101),
'mfv_stoplb_tau001000um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_152838", 201),
'mfv_stoplb_tau030000um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_152920", 201),
'mfv_stoplb_tau000100um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_153001", 201),
'mfv_stoplb_tau000300um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_153044", 201),
'mfv_stoplb_tau010000um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_153130", 101),
'mfv_stoplb_tau001000um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_153212", 201),
'mfv_stoplb_tau030000um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_153253", 201),
'mfv_stoplb_tau000100um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_153338", 201),
'mfv_stoplb_tau000300um_M1400_2018': (199, ['/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_153421/0000/ntuple_%i.root' % i for i in chain(xrange(1,10), xrange(11,22), xrange(23,202))]),
'mfv_stoplb_tau010000um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_153503", 101),
'mfv_stoplb_tau001000um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_153546", 201),
'mfv_stoplb_tau030000um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_153630", 200),
'mfv_stoplb_tau000100um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_153711", 201),
'mfv_stoplb_tau000300um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_153753", 201),
'mfv_stoplb_tau010000um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_153837", 101),
'mfv_stoplb_tau001000um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_153918", 101),
'mfv_stoplb_tau030000um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_153958", 101),
'mfv_stoplb_tau000100um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_154041", 200),
'mfv_stoplb_tau000300um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_154123", 201),
'mfv_stoplb_tau010000um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_154205", 101),
'mfv_stoplb_tau001000um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_154248", 101),
'mfv_stoplb_tau030000um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_154332", 101),
'mfv_stoplb_tau000100um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_154414", 201),
'mfv_stoplb_tau000300um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_154458", 201),
'mfv_stoplb_tau010000um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_154541", 201),
'mfv_stoplb_tau001000um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_154623", 201),
'mfv_stoplb_tau030000um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_154704", 201),
'mfv_stoplb_tau000100um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_154748", 201),
'mfv_stoplb_tau000300um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_154829", 201),
'mfv_stoplb_tau010000um_M0300_2018': (200, ['/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_154916/0000/ntuple_%i.root' % i for i in chain(xrange(1,91), xrange(92,202))]),
'mfv_stoplb_tau001000um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_154958", 200),
'mfv_stoplb_tau030000um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_155040", 201),
'mfv_stoplb_tau000100um_M0400_2018': (200, ['/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_155122/0000/ntuple_%i.root' % i for i in chain(xrange(1,101), xrange(102,202))]),
'mfv_stoplb_tau000300um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_155206", 201),
'mfv_stoplb_tau010000um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_155248", 201),
'mfv_stoplb_tau001000um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_155334", 201),
'mfv_stoplb_tau030000um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_155416", 200),
'mfv_stoplb_tau000100um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_155459", 201),
'mfv_stoplb_tau000300um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_155544", 200),
'mfv_stoplb_tau010000um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_155628", 201),
'mfv_stoplb_tau001000um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_155710", 200),
'mfv_stoplb_tau030000um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_155754", 200),
'mfv_stoplb_tau000100um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_155837", 200),
'mfv_stoplb_tau000300um_M0800_2018': (199, ['/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_155922/0000/ntuple_%i.root' % i for i in chain(xrange(1,157), xrange(158,201))]),
'mfv_stoplb_tau010000um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_160004", 100),
'mfv_stoplb_tau001000um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_160045", 201),
'mfv_stoplb_tau030000um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_160129", 201),
'mfv_stopld_tau000100um_M1000_2018': (200, ['/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_160211/0000/ntuple_%i.root' % i for i in chain(xrange(1,123), xrange(124,202))]),
'mfv_stopld_tau000300um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_160254", 201),
'mfv_stopld_tau010000um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_160337", 101),
'mfv_stopld_tau001000um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_160417", 201),
'mfv_stopld_tau030000um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_160500", 201),
'mfv_stopld_tau000100um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_160548", 201),
'mfv_stopld_tau000300um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_160632", 201),
'mfv_stopld_tau010000um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_160714", 101),
'mfv_stopld_tau001000um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_160801", 201),
'mfv_stopld_tau030000um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_160845", 201),
'mfv_stopld_tau000100um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_160932", 201),
'mfv_stopld_tau000300um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_161014", 200),
'mfv_stopld_tau010000um_M1400_2018': (100, ['/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_161056/0000/ntuple_%i.root' % i for i in chain(xrange(1,17), xrange(18,102))]),
'mfv_stopld_tau001000um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_161138", 201),
'mfv_stopld_tau030000um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_161223", 201),
'mfv_stopld_tau000100um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_161306", 201),
'mfv_stopld_tau000300um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_161347", 201),
'mfv_stopld_tau010000um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_161428", 101),
'mfv_stopld_tau001000um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_161511", 101),
'mfv_stopld_tau030000um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_161554", 100),
'mfv_stopld_tau000100um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_161638", 201),
'mfv_stopld_tau000300um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_161719", 201),
'mfv_stopld_tau010000um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_161803", 101),
'mfv_stopld_tau001000um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_161846", 101),
'mfv_stopld_tau030000um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_161933", 101),
'mfv_stopld_tau000100um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_162017", 201),
'mfv_stopld_tau000300um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_162100", 201),
'mfv_stopld_tau010000um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_162143", 201),
'mfv_stopld_tau001000um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_162226", 201),
'mfv_stopld_tau030000um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_162309", 201),
'mfv_stopld_tau000100um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_162350", 201),
'mfv_stopld_tau000300um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_162432", 201),
'mfv_stopld_tau010000um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_162514", 201),
'mfv_stopld_tau001000um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_162556", 201),
'mfv_stopld_tau030000um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_162639", 201),
'mfv_stopld_tau000100um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_162719", 201),
'mfv_stopld_tau000300um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_162808", 201),
'mfv_stopld_tau010000um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_162850", 201),
'mfv_stopld_tau001000um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_162938", 201),
'mfv_stopld_tau030000um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_163020", 201),
'mfv_stopld_tau000100um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_163103", 201),
'mfv_stopld_tau000300um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_163144", 201),
'mfv_stopld_tau010000um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_163227", 201),
'mfv_stopld_tau001000um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_163309", 200),
'mfv_stopld_tau030000um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_163352", 201),
'mfv_stopld_tau000100um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_163435", 200),
'mfv_stopld_tau000300um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_163519", 201),
'mfv_stopld_tau010000um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_163601", 101),
'mfv_stopld_tau001000um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_163644", 201),
'mfv_stopld_tau030000um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV2Lepm_2018/230505_163725", 201),
})

#DO NOT DROP Lepton Tracks when doing the dz refit in the vertexing 
#this version used to be 3 -- but replaced with v5 because triggers were messed up 
_add_ds("ntupleulv5lepm", {
'qcdmupt15_2018': (25, ['/store/user/awarden/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/NtupleULV5Lepm_2018/230704_102750/0000/ntuple_%i.root' % i for i in chain(xrange(1,20), xrange(22,26), xrange(27,29))]),
'qcdempt015_2018': _fromnum1("/store/user/awarden/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV5Lepm_2018/230704_102831", 19),
'qcdempt020_2018': _fromnum1("/store/user/awarden/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV5Lepm_2018/230704_102912", 17),
'qcdempt030_2018': _fromnum1("/store/user/awarden/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV5Lepm_2018/230704_102952", 12),
'qcdempt050_2018': (12, ['/store/user/awarden/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV5Lepm_2018/230704_103034/0000/ntuple_%i.root' % i for i in chain(xrange(1,10), xrange(13,15), [11])]),
'qcdempt080_2018': _fromnum1("/store/user/awarden/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV5Lepm_2018/230704_103115", 12),
'qcdempt120_2018': _fromnum1("/store/user/awarden/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV5Lepm_2018/230704_103156", 14),
'qcdempt170_2018': _fromnum1("/store/user/awarden/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV5Lepm_2018/230704_103237", 5),
'qcdempt300_2018': _fromnum0("/store/user/awarden/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV5Lepm_2018/230704_103319", 3),
'qcdbctoept015_2018': _fromnum1("/store/user/awarden/QCD_Pt_15to20_bcToE_TuneCP5_13TeV_pythia8/NtupleULV5Lepm_2018/230704_103400", 25),
'qcdbctoept020_2018': _fromnum1("/store/user/awarden/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/NtupleULV5Lepm_2018/230704_103442", 38),
'qcdbctoept030_2018': _fromnum1("/store/user/awarden/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/NtupleULV5Lepm_2018/230704_103522", 28),
'qcdbctoept080_2018': _fromnum1("/store/user/awarden/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/NtupleULV5Lepm_2018/230704_103604", 41),
'qcdbctoept170_2018': (42, ['/store/user/awarden/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/NtupleULV5Lepm_2018/230704_103644/0000/ntuple_%i.root' % i for i in chain(xrange(1,39), xrange(40,44))]),
'qcdbctoept250_2018': _fromnum1("/store/user/awarden/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/NtupleULV5Lepm_2018/230704_103726", 42),
'wjetstolnu_2018': _fromnum1("/store/user/awarden/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV5Lepm_2018/230704_114655", 99),
'dyjetstollM10_2018': (107, ['/store/user/awarden/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV5Lepm_2018/230704_114738/0000/ntuple_%i.root' % i for i in chain(xrange(1,15), xrange(17,78), xrange(79,96), xrange(98,113))]),
'dyjetstollM50_2018': _fromnum1("/store/user/awarden/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV5Lepm_2018/230704_114819", 110),
'ttbar_2018': (1, ['/store/user/awarden/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleULV5Lepm_2018/230704_065026/0000/ntuple_0.root']),
'ww_2018': (21, ['/store/user/awarden/WW_TuneCP5_13TeV-pythia8/NtupleULV5Lepm_2018/230704_114902/0000/ntuple_%i.root' % i for i in chain(xrange(1,13), xrange(14,23))]),
'wz_2018': _fromnum1("/store/user/awarden/WZ_TuneCP5_13TeV-pythia8/NtupleULV5Lepm_2018/230704_114943", 16),
'zz_2018': _fromnum1("/store/user/awarden/ZZ_TuneCP5_13TeV-pythia8/NtupleULV5Lepm_2018/230704_115025", 6),
'mfv_stoplb_tau000100um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_103806", 201),
'mfv_stoplb_tau000300um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_103847", 201),
'mfv_stoplb_tau010000um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_103927", 84),
'mfv_stoplb_tau001000um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_104008", 199),
'mfv_stoplb_tau030000um_M1000_2018': (198, ['/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_104049/0000/ntuple_%i.root' % i for i in chain(xrange(1,150), xrange(154,202), [151])]),
'mfv_stoplb_tau000100um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_104131", 201),
'mfv_stoplb_tau000300um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_104211", 201),
'mfv_stoplb_tau010000um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_104253", 88),
'mfv_stoplb_tau001000um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_104333", 201),
'mfv_stoplb_tau030000um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_104415", 170),
'mfv_stoplb_tau000100um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_104455", 192),
'mfv_stoplb_tau000300um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_104538", 201),
'mfv_stoplb_tau010000um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_104619", 101),
'mfv_stoplb_tau001000um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_104704", 201),
'mfv_stoplb_tau030000um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_104744", 191),
'mfv_stoplb_tau000100um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_104825", 201),
'mfv_stoplb_tau000300um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_104905", 160),
'mfv_stoplb_tau010000um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_104946", 101),
'mfv_stoplb_tau001000um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_105027", 101),
'mfv_stoplb_tau030000um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_105109", 95),
'mfv_stoplb_tau000100um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_105149", 200),
'mfv_stoplb_tau000300um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_105230", 201),
'mfv_stoplb_tau010000um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_105312", 101),
'mfv_stoplb_tau001000um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_105355", 91),
'mfv_stoplb_tau030000um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_105436", 94),
'mfv_stoplb_tau000100um_M0200_2018': (190, ['/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_105518/0000/ntuple_%i.root' % i for i in chain(xrange(1,126), xrange(131,194), [127, 129])]),
'mfv_stoplb_tau000300um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_105558", 198),
'mfv_stoplb_tau010000um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_105639", 201),
'mfv_stoplb_tau001000um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_105719", 196),
'mfv_stoplb_tau030000um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_105801", 201),
'mfv_stoplb_tau000100um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_105841", 185),
'mfv_stoplb_tau000300um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_105925", 156),
'mfv_stoplb_tau010000um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_110005", 194),
'mfv_stoplb_tau001000um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_110047", 200),
'mfv_stoplb_tau030000um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_110126", 201),
'mfv_stoplb_tau000100um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_110208", 201),
'mfv_stoplb_tau000300um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_110248", 201),
'mfv_stoplb_tau010000um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_110332", 184),
'mfv_stoplb_tau001000um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_110413", 195),
'mfv_stoplb_tau030000um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_110457", 187),
'mfv_stoplb_tau000100um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_110536", 198),
'mfv_stoplb_tau000300um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_110618", 178),
'mfv_stoplb_tau010000um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_110658", 201),
'mfv_stoplb_tau001000um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_110740", 200),
'mfv_stoplb_tau030000um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_110821", 200),
'mfv_stoplb_tau000100um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_110902", 184),
'mfv_stoplb_tau000300um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_110942", 190),
'mfv_stoplb_tau010000um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_111023", 97),
'mfv_stoplb_tau001000um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_111103", 167),
'mfv_stoplb_tau030000um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_111146", 183),
'mfv_stopld_tau000100um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_111227", 201),
'mfv_stopld_tau000300um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_111308", 183),
'mfv_stopld_tau010000um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_111348", 101),
'mfv_stopld_tau001000um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_111430", 201),
'mfv_stopld_tau030000um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_111509", 178),
'mfv_stopld_tau000100um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_111551", 201),
'mfv_stopld_tau000300um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_111633", 196),
'mfv_stopld_tau010000um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_111714", 99),
'mfv_stopld_tau001000um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_111754", 201),
'mfv_stopld_tau030000um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_111837", 201),
'mfv_stopld_tau000100um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_111919", 201),
'mfv_stopld_tau000300um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_112001", 200),
'mfv_stopld_tau010000um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_112042", 101),
'mfv_stopld_tau001000um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_112123", 188),
'mfv_stopld_tau030000um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_112203", 168),
'mfv_stopld_tau000100um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_112250", 183),
'mfv_stopld_tau000300um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_112331", 201),
'mfv_stopld_tau010000um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_112413", 101),
'mfv_stopld_tau001000um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_112454", 101),
'mfv_stopld_tau030000um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_112536", 100),
'mfv_stopld_tau000100um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_112619", 201),
'mfv_stopld_tau000300um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_112701", 193),
'mfv_stopld_tau010000um_M1800_2018': (91, ['/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_112742/0000/ntuple_%i.root' % i for i in chain(xrange(1,5), xrange(15,102))]),
'mfv_stopld_tau001000um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_112823", 99),
'mfv_stopld_tau030000um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_112902", 91),
'mfv_stopld_tau000100um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_112945", 181),
'mfv_stopld_tau000300um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_113026", 182),
'mfv_stopld_tau010000um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_113108", 180),
'mfv_stopld_tau001000um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_113149", 185),
'mfv_stopld_tau030000um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_113230", 201),
'mfv_stopld_tau000100um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_113310", 192),
'mfv_stopld_tau000300um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_113353", 201),
'mfv_stopld_tau010000um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_113432", 179),
'mfv_stopld_tau001000um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_113515", 188),
'mfv_stopld_tau030000um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_113555", 176),
'mfv_stopld_tau000100um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_113637", 201),
'mfv_stopld_tau000300um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_113718", 196),
'mfv_stopld_tau010000um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_113800", 201),
'mfv_stopld_tau001000um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_113841", 201),
'mfv_stopld_tau030000um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_113923", 201),
'mfv_stopld_tau000100um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_114004", 180),
'mfv_stopld_tau000300um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_114046", 189),
'mfv_stopld_tau010000um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_114126", 181),
'mfv_stopld_tau001000um_M0600_2018': (193, ['/store/user/awarden/DisplacedSUSY_stopToLD_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_114208/0000/ntuple_%i.root' % i for i in chain(xrange(1,9), xrange(10,195))]),
'mfv_stopld_tau030000um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_114248", 201),
'mfv_stopld_tau000100um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_114330", 200),
'mfv_stopld_tau000300um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_114410", 189),
'mfv_stopld_tau010000um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_114453", 100),
'mfv_stopld_tau001000um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_114534", 180),
'mfv_stopld_tau030000um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV5Lepm_2018/230704_114615", 201),
})

##this ntuple version places more requirements on the lepton tracks  (namely, to be defined as a muon/electron track -- must pass cutbasedID && iso)
## warning : the triggers are messed up 
_add_ds("ntupleulv3lepm_wgen", {
'mfv_stoplb_tau010000um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_112011", 101),
'mfv_stoplb_tau001000um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_112059", 201),
'mfv_stoplb_tau030000um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_112143", 201),
'mfv_stoplb_tau000100um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_112230", 201),
'mfv_stoplb_tau000300um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_112314", 201),
'mfv_stoplb_tau010000um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_112400", 101),
'mfv_stoplb_tau001000um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_112445", 201),
'mfv_stoplb_tau030000um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_112531", 201),
'mfv_stoplb_tau000100um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_112616", 201),
'mfv_stoplb_tau000300um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_112700", 201),
'mfv_stoplb_tau010000um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_112744", 101),
'mfv_stoplb_tau001000um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_112829", 201),
'mfv_stoplb_tau030000um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_112913", 200),
'mfv_stoplb_tau000100um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_112956", 201),
'mfv_stoplb_tau000300um_M1600_2018': (182, ['/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_113040/0000/ntuple_%i.root' % i for i in chain(xrange(1,146), xrange(165,202))]),
'mfv_stoplb_tau010000um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_113124", 92),
'mfv_stoplb_tau001000um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_113210", 101),
'mfv_stoplb_tau030000um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_113254", 101),
'mfv_stoplb_tau000100um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_113339", 200),
'mfv_stoplb_tau000300um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_113424", 201),
'mfv_stoplb_tau010000um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_113506", 101),
'mfv_stoplb_tau001000um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_113551", 101),
'mfv_stoplb_tau030000um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_113634", 101),
'mfv_stoplb_tau000100um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_113717", 201),
'mfv_stoplb_tau000300um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_113801", 201),
'mfv_stoplb_tau010000um_M0200_2018': (169, ['/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_113852/0000/ntuple_%i.root' % i for i in chain(xrange(1,111), xrange(143,202))]),
'mfv_stoplb_tau001000um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_113935", 201),
'mfv_stoplb_tau030000um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_114020", 201),
'mfv_stoplb_tau000100um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_114104", 201),
'mfv_stoplb_tau000300um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_114151", 201),
'mfv_stoplb_tau010000um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_114236", 201),
'mfv_stoplb_tau001000um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_114320", 200),
'mfv_stoplb_tau030000um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_114403", 201),
'mfv_stoplb_tau000100um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_114448", 201),
'mfv_stoplb_tau000300um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_114532", 201),
'mfv_stoplb_tau010000um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_114621", 201),
'mfv_stoplb_tau001000um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_114705", 201),
'mfv_stoplb_tau030000um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_114751", 200),
'mfv_stoplb_tau000100um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_114837", 201),
'mfv_stoplb_tau000300um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_114922", 200),
'mfv_stoplb_tau010000um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_115005", 201),
'mfv_stoplb_tau001000um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_115058", 200),
'mfv_stoplb_tau030000um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_115144", 200),
'mfv_stoplb_tau000100um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_115232", 200),
'mfv_stoplb_tau000300um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_115318", 200),
'mfv_stoplb_tau010000um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_115406", 100),
'mfv_stoplb_tau001000um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_115451", 201),
'mfv_stoplb_tau030000um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_115536", 201),
'mfv_stopld_tau000100um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_115621", 201),
'mfv_stopld_tau000300um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_115708", 201),
'mfv_stopld_tau010000um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_115755", 101),
'mfv_stopld_tau001000um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_115839", 201),
'mfv_stopld_tau030000um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_115922", 201),
'mfv_stopld_tau000100um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_120007", 201),
'mfv_stopld_tau000300um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_120050", 201),
'mfv_stopld_tau010000um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_120140", 101),
'mfv_stopld_tau001000um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_120226", 201),
'mfv_stopld_tau030000um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_120312", 201),
'mfv_stopld_tau000100um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_120358", 201),
'mfv_stopld_tau000300um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_120444", 200),
'mfv_stopld_tau010000um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_120530", 101),
'mfv_stopld_tau001000um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_120616", 201),
'mfv_stopld_tau030000um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_120659", 201),
'mfv_stopld_tau000100um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_120743", 201),
'mfv_stopld_tau000300um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_120826", 201),
'mfv_stopld_tau010000um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_120914", 101),
'mfv_stopld_tau001000um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_120958", 101),
'mfv_stopld_tau030000um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_121042", 100),
'mfv_stopld_tau000100um_M1800_2018': (197, ['/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_121125/0000/ntuple_%i.root' % i for i in chain(xrange(1,32), xrange(36,202))]),
'mfv_stopld_tau000300um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_121209", 201),
'mfv_stopld_tau010000um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_121251", 101),
'mfv_stopld_tau001000um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_121334", 101),
'mfv_stopld_tau030000um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_121416", 101),
'mfv_stopld_tau000100um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_121500", 201),
'mfv_stopld_tau000300um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_121544", 201),
'mfv_stopld_tau010000um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_121627", 201),
'mfv_stopld_tau001000um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_121711", 201),
'mfv_stopld_tau030000um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_121756", 201),
'mfv_stopld_tau000100um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_121839", 201),
'mfv_stopld_tau000300um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_121924", 201),
'mfv_stopld_tau010000um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_122006", 201),
'mfv_stopld_tau001000um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_122053", 201),
'mfv_stopld_tau030000um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_122135", 201),
'mfv_stopld_tau000100um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_122222", 201),
'mfv_stopld_tau000300um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_122306", 201),
'mfv_stopld_tau010000um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_122352", 201),
'mfv_stopld_tau001000um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_122435", 201),
'mfv_stopld_tau030000um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_122521", 201),
'mfv_stopld_tau000100um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_122608", 201),
'mfv_stopld_tau000300um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_122652", 201),
'mfv_stopld_tau010000um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_122737", 201),
'mfv_stopld_tau001000um_M0600_2018': (195, ['/store/user/awarden/DisplacedSUSY_stopToLD_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_122823/0000/ntuple_%i.root' % i for i in chain(xrange(1,163), xrange(164,167), xrange(168,176), xrange(180,201), [178])]),
'mfv_stopld_tau030000um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_122907", 201),
'mfv_stopld_tau000100um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_122953", 200),
'mfv_stopld_tau000300um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_123034", 201),
'mfv_stopld_tau010000um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_123119", 101),
'mfv_stopld_tau001000um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_123202", 201),
'mfv_stopld_tau030000um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV3Lepm_WGen_2018/230629_123248", 201),
})


##adding lost tracks 
## triggers are messed up 
_add_ds("ntupleulv4lepm", {
'mfv_stoplb_tau000300um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_220412", 201),
'mfv_stoplb_tau010000um_M1000_2018': (100, ['/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_220452/0000/ntuple_%i.root' % i for i in chain(xrange(1,5), xrange(6,102))]),
'mfv_stoplb_tau001000um_M1000_2018': (200, ['/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_220534/0000/ntuple_%i.root' % i for i in chain(xrange(1,187), xrange(188,202))]),
'mfv_stoplb_tau030000um_M1000_2018': (189, ['/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_220614/0000/ntuple_%i.root' % i for i in chain(xrange(1,61), xrange(64,66), xrange(71,73), xrange(75,134), xrange(136,139), xrange(140,202), [69])]),
'mfv_stoplb_tau000100um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_220659", 201),
'mfv_stoplb_tau000300um_M1200_2018': (199, ['/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_220740/0000/ntuple_%i.root' % i for i in chain(xrange(1,40), xrange(43,202), [41])]),
'mfv_stoplb_tau010000um_M1200_2018': (97, ['/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_220822/0000/ntuple_%i.root' % i for i in chain(xrange(1,28), xrange(30,33), xrange(34,37), xrange(38,102))]),
'mfv_stoplb_tau001000um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_220903", 201),
'mfv_stoplb_tau030000um_M1200_2018': (193, ['/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_220948/0000/ntuple_%i.root' % i for i in chain(xrange(1,18), xrange(24,31), xrange(37,202), [19, 22, 33, 35])]),
'mfv_stoplb_tau000100um_M1400_2018': (192, ['/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_221029/0000/ntuple_%i.root' % i for i in chain(xrange(1,34), xrange(35,37), xrange(38,52), xrange(53,55), xrange(56,58), xrange(59,62), xrange(65,121), xrange(122,202))]),
'mfv_stoplb_tau000300um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_221111", 201),
'mfv_stoplb_tau010000um_M1400_2018': (83, ['/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_221152/0000/ntuple_%i.root' % i for i in chain(xrange(1,38), xrange(39,44), xrange(50,54), xrange(55,57), xrange(62,66), xrange(68,70), xrange(71,73), xrange(74,81), xrange(82,84), xrange(85,87), xrange(88,92), xrange(93,96), xrange(97,102), [45, 47, 58, 60])]),
'mfv_stoplb_tau001000um_M1400_2018': (200, ['/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_221235/0000/ntuple_%i.root' % i for i in chain(xrange(1,98), xrange(99,202))]),
'mfv_stoplb_tau030000um_M1400_2018': (196, ['/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_221315/0000/ntuple_%i.root' % i for i in chain(xrange(3,168), xrange(169,175), xrange(176,184), xrange(185,201), [1])]),
'mfv_stoplb_tau000100um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_221358", 201),
'mfv_stoplb_tau000300um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_221438", 201),
'mfv_stoplb_tau010000um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_221521", 101),
'mfv_stoplb_tau001000um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_221601", 101),
'mfv_stoplb_tau030000um_M1600_2018': (100, ['/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_221643/0000/ntuple_%i.root' % i for i in chain(xrange(1,29), xrange(30,102))]),
'mfv_stoplb_tau000100um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_221724", 200),
'mfv_stoplb_tau000300um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_221807", 201),
'mfv_stoplb_tau010000um_M1800_2018': (100, ['/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_221847/0000/ntuple_%i.root' % i for i in chain(xrange(1,17), xrange(18,102))]),
'mfv_stoplb_tau001000um_M1800_2018': (98, ['/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_221929/0000/ntuple_%i.root' % i for i in chain(xrange(5,41), xrange(42,102), [1, 3])]),
'mfv_stoplb_tau030000um_M1800_2018': (100, ['/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_222012/0000/ntuple_%i.root' % i for i in chain(xrange(1,8), xrange(9,102))]),
'mfv_stoplb_tau000100um_M0200_2018': (199, ['/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_222055/0000/ntuple_%i.root' % i for i in chain(xrange(1,11), xrange(12,16), xrange(17,202))]),
'mfv_stoplb_tau000300um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_222134", 201),
'mfv_stoplb_tau010000um_M0200_2018': (188, ['/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_222217/0000/ntuple_%i.root' % i for i in chain(xrange(1,132), xrange(133,135), xrange(138,146), xrange(156,202), [148])]),
'mfv_stoplb_tau001000um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_222259", 201),
'mfv_stoplb_tau030000um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_222341", 201),
'mfv_stoplb_tau000100um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_222424", 201),
'mfv_stoplb_tau000300um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_222505", 201),
'mfv_stoplb_tau010000um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_222548", 201),
'mfv_stoplb_tau001000um_M0300_2018': (199, ['/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_222629/0000/ntuple_%i.root' % i for i in chain(xrange(1,13), xrange(14,201))]),
'mfv_stoplb_tau030000um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_222711", 201),
'mfv_stoplb_tau000100um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_222752", 201),
'mfv_stoplb_tau000300um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_222834", 201),
'mfv_stoplb_tau010000um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_222920", 201),
'mfv_stoplb_tau001000um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_223010", 201),
'mfv_stoplb_tau030000um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_223050", 200),
'mfv_stoplb_tau000100um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_223132", 201),
'mfv_stoplb_tau000300um_M0600_2018': (180, ['/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_223215/0000/ntuple_%i.root' % i for i in chain(xrange(1,11), xrange(32,201), [19])]),
'mfv_stoplb_tau010000um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_223257", 201),
'mfv_stoplb_tau001000um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_223338", 200),
'mfv_stoplb_tau030000um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_223419", 200),
'mfv_stoplb_tau000100um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_223500", 200),
'mfv_stoplb_tau000300um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_223543", 200),
'mfv_stoplb_tau010000um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_223624", 100),
'mfv_stoplb_tau001000um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_223706", 201),
'mfv_stoplb_tau030000um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_223747", 201),
'mfv_stopld_tau000100um_M1000_2018': (189, ['/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_223828/0000/ntuple_%i.root' % i for i in chain(xrange(1,155), xrange(165,170), xrange(176,202), [158, 160, 162, 172])]),
'mfv_stopld_tau000300um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_223910", 201),
'mfv_stopld_tau010000um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_223956", 101),
'mfv_stopld_tau001000um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_224038", 201),
'mfv_stopld_tau030000um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_224121", 201),
'mfv_stopld_tau000100um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_224202", 201),
'mfv_stopld_tau000300um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_224244", 201),
'mfv_stopld_tau010000um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_224326", 101),
'mfv_stopld_tau001000um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_224407", 201),
'mfv_stopld_tau030000um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_224448", 201),
'mfv_stopld_tau000100um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_224530", 201),
'mfv_stopld_tau000300um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_224612", 200),
'mfv_stopld_tau010000um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_224656", 101),
'mfv_stopld_tau001000um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_224736", 201),
'mfv_stopld_tau030000um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_224819", 201),
'mfv_stopld_tau000100um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_224900", 201),
'mfv_stopld_tau000300um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_224941", 201),
'mfv_stopld_tau010000um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_225025", 101),
'mfv_stopld_tau001000um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_225108", 101),
'mfv_stopld_tau030000um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_225152", 100),
'mfv_stopld_tau000100um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_225234", 201),
'mfv_stopld_tau000300um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_225315", 201),
'mfv_stopld_tau010000um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_225358", 101),
'mfv_stopld_tau001000um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_225439", 101),
'mfv_stopld_tau030000um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_225521", 101),
'mfv_stopld_tau000100um_M0200_2018': (200, ['/store/user/awarden/DisplacedSUSY_stopToLD_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_225602/0000/ntuple_%i.root' % i for i in chain(xrange(3,202), [1])]),
'mfv_stopld_tau000300um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_225645", 201),
'mfv_stopld_tau010000um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_225726", 201),
'mfv_stopld_tau001000um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_225808", 201),
'mfv_stopld_tau030000um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_225849", 201),
'mfv_stopld_tau000100um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_225931", 201),
'mfv_stopld_tau000300um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_230017", 201),
'mfv_stopld_tau010000um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_230058", 201),
'mfv_stopld_tau001000um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_230140", 201),
'mfv_stopld_tau030000um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_230222", 201),
'mfv_stopld_tau000100um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_230306", 201),
'mfv_stopld_tau000300um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_230347", 201),
'mfv_stopld_tau010000um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_230428", 201),
'mfv_stopld_tau001000um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_230509", 201),
'mfv_stopld_tau030000um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_230553", 201),
'mfv_stopld_tau000100um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_230636", 201),
'mfv_stopld_tau000300um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_230724", 201),
'mfv_stopld_tau010000um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_230809", 201),
'mfv_stopld_tau001000um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_230857", 200),
'mfv_stopld_tau030000um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_230942", 201),
'mfv_stopld_tau000100um_M0800_2018': (198, ['/store/user/awarden/DisplacedSUSY_stopToLD_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_231035/0000/ntuple_%i.root' % i for i in chain(xrange(2,22), xrange(23,201))]),
'mfv_stopld_tau000300um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_231122", 201),
'mfv_stopld_tau010000um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_231205", 101),
'mfv_stopld_tau001000um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_231248", 201),
'mfv_stopld_tau030000um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV4Lepm_2018/230602_231330", 201),
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

#TrackingTreer 2018 
_add_ds("trackingtreerulv1_lepm", {
'qcdmupt15_2018': _fromnum1("/store/user/awarden/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/TrackingTreerULV1_Lepm_2018/230228_100230", 17, fnbase="trackingtreer"),
'qcdempt015_2018': _fromnum1("/store/user/awarden/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/TrackingTreerULV1_Lepm_2018/230228_100246", 21, fnbase="trackingtreer"),
'qcdempt020_2018': _fromnum1("/store/user/awarden/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/TrackingTreerULV1_Lepm_2018/230228_100302", 9, fnbase="trackingtreer"),
'qcdempt030_2018': _fromnum1("/store/user/awarden/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/TrackingTreerULV1_Lepm_2018/230228_100318", 13, fnbase="trackingtreer"),
'qcdempt050_2018': _fromnum1("/store/user/awarden/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/TrackingTreerULV1_Lepm_2018/230228_100336", 7, fnbase="trackingtreer"),
'qcdempt080_2018': _fromnum1("/store/user/awarden/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/TrackingTreerULV1_Lepm_2018/230228_100353", 6, fnbase="trackingtreer"),
'qcdempt120_2018': _fromnum1("/store/user/awarden/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/TrackingTreerULV1_Lepm_2018/230228_100409", 7, fnbase="trackingtreer"),
'qcdempt170_2018': _fromnum1("/store/user/awarden/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/TrackingTreerULV1_Lepm_2018/230228_100425", 3, fnbase="trackingtreer"),
'qcdempt300_2018': _fromnum1("/store/user/awarden/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/TrackingTreerULV1_Lepm_2018/230228_100443", 2, fnbase="trackingtreer"),
'qcdbctoept015_2018': _fromnum1("/store/user/awarden/QCD_Pt_15to20_bcToE_TuneCP5_13TeV_pythia8/TrackingTreerULV1_Lepm_2018/230228_100458", 21, fnbase="trackingtreer"),
'qcdbctoept020_2018': _fromnum1("/store/user/awarden/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/TrackingTreerULV1_Lepm_2018/230228_100515", 40, fnbase="trackingtreer"),
'qcdbctoept030_2018': _fromnum1("/store/user/awarden/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/TrackingTreerULV1_Lepm_2018/230228_100531", 22, fnbase="trackingtreer"),
'qcdbctoept080_2018': (26, ['/store/user/awarden/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/TrackingTreerULV1_Lepm_2018/230228_100549/0000/trackingtreer_%i.root' % i for i in chain(xrange(1,8), xrange(9,28))]),
'qcdbctoept170_2018': _fromnum1("/store/user/awarden/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/TrackingTreerULV1_Lepm_2018/230228_100605", 30, fnbase="trackingtreer"),
'qcdbctoept250_2018': _fromnum1("/store/user/awarden/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/TrackingTreerULV1_Lepm_2018/230228_100620", 30, fnbase="trackingtreer"),
'dyjetstollM10_2018': _fromnum1("/store/user/awarden/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/TrackingTreerULV1_Lepm_2018/230228_100837", 60, fnbase="trackingtreer"),
'dyjetstollM50_2018': _fromnum1("/store/user/awarden/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/TrackingTreerULV1_Lepm_2018/230228_100853", 60, fnbase="trackingtreer"),
'wjetstolnu_2018': _fromnum1("/store/user/awarden/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/TrackingTreerULV1_Lepm_2018/230228_100911", 55, fnbase="trackingtreer"),
'ttbar_2018': (322, ['/store/user/awarden/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/TrackingTreerULV1_Lepm_2018/230127_084741/0000/trackingtreer_%i.root' % i for i in chain(xrange(47), xrange(50,325))]),
'ww_2018': _fromnum1("/store/user/awarden/WW_TuneCP5_13TeV-pythia8/TrackingTreerULV1_Lepm_2018/230228_100927", 16, fnbase="trackingtreer"),
'wz_2018': _fromnum1("/store/user/awarden/WZ_TuneCP5_13TeV-pythia8/TrackingTreerULV1_Lepm_2018/230228_100943", 12, fnbase="trackingtreer"),
'zz_2018': _fromnum1("/store/user/awarden/ZZ_TuneCP5_13TeV-pythia8/TrackingTreerULV1_Lepm_2018/230228_101005", 4, fnbase="trackingtreer"),
'SingleMuon2018A': (102, ['/store/user/awarden/SingleMuon/TrackingTreerULV1_Lepm_2018/230228_100636/0000/trackingtreer_%i.root' % i for i in chain(xrange(1,3), xrange(4,14), xrange(15,17), xrange(20,26), xrange(27,37), xrange(38,43), xrange(44,57), xrange(58,86), xrange(90,94), xrange(95,115), [18, 88])]),
'SingleMuon2018B': _fromnum1("/store/user/awarden/SingleMuon/TrackingTreerULV1_Lepm_2018/230228_100654", 51, fnbase="trackingtreer"),
'SingleMuon2018C': _fromnum1("/store/user/awarden/SingleMuon/TrackingTreerULV1_Lepm_2018/230228_100710", 53, fnbase="trackingtreer"),
'SingleMuon2018D': (218, ['/store/user/awarden/SingleMuon/TrackingTreerULV1_Lepm_2018/230228_100729/0000/trackingtreer_%i.root' % i for i in chain(xrange(1,20), xrange(21,82), xrange(83,158), xrange(159,179), xrange(181,196), xrange(197,225))]),
'EGamma2018A': (159, ['/store/user/awarden/EGamma/TrackingTreerULV1_Lepm_2018/230228_100746/0000/trackingtreer_%i.root' % i for i in chain(xrange(1,5), xrange(6,161))]),
'EGamma2018B': _fromnum1("/store/user/awarden/EGamma/TrackingTreerULV1_Lepm_2018/230228_100804", 72, fnbase="trackingtreer"),
'EGamma2018C': _fromnum1("/store/user/awarden/EGamma/TrackingTreerULV1_Lepm_2018/230228_100821", 71, fnbase="trackingtreer"),
'EGamma2018D': (322, ['/store/user/awarden/EGamma/TrackingTreerULV1_Lepm_2018/230228_183805/0000/trackingtreer_%i.root' % i for i in chain(xrange(1,6), xrange(7,117), xrange(118,325))]),
})

_add_ds("trackingtreerulv2_lepm", {
'ttbar_2018': (300, ['/store/user/awarden/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/TrackingTreerULV2_Lepm_2018/230518_063044/0000/trackingtreer_%i.root' % i for i in chain(xrange(15), xrange(20,24), xrange(25,47), xrange(52,58), xrange(59,65), xrange(66,71), xrange(72,86), xrange(87,110), xrange(111,116), xrange(117,138), xrange(139,154), xrange(155,195), xrange(196,227), xrange(228,232), xrange(233,236), xrange(237,281), xrange(282,302), xrange(303,325))]),
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
