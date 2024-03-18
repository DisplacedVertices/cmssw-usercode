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
})

################################################################################

_add_ds("nr_trackingtreer_ul17", {
'qcdht0200_2017': _fromnum1("/store/user/shogan/QCD_HT200to300_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/TrackingTreerUL17_2017/230329_140552", 48, fnbase="trackingtreer"),
'qcdht0300_2017': (3, ['/store/user/shogan/QCD_HT300to500_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/TrackingTreerUL17_2017/230329_140603/0000/trackingtreer_%i.root' % i for i in chain(xrange(3,5), [1])]),
'qcdht0500_2017': _fromnum1("/store/user/shogan/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/TrackingTreerUL17_2017/230329_140614", 13, fnbase="trackingtreer"),
'qcdht0700_2017': _fromnum1("/store/user/shogan/QCD_HT700to1000_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/TrackingTreerUL17_2017/230329_140625", 55, fnbase="trackingtreer"),
'qcdht1000_2017': _fromnum1("/store/user/shogan/QCD_HT1000to1500_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/TrackingTreerUL17_2017/230329_140636", 21, fnbase="trackingtreer"),
'qcdht1500_2017': _fromnum1("/store/user/shogan/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraph-pythia8/TrackingTreerUL17_2017/230329_140648", 21, fnbase="trackingtreer"),
'qcdht2000_2017': (6, ['/store/user/shogan/QCD_HT2000toInf_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/TrackingTreerUL17_2017/230329_140659/0000/trackingtreer_%i.root' % i for i in chain(xrange(1,3), xrange(8,11), [4])]),
'ttbar_2017': _fromnum1("/store/user/shogan/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/TrackingTreerUL17_2017/230329_140540", 255, fnbase="trackingtreer"),
'BTagCSV2017B': _fromnum1("/store/user/shogan/BTagCSV/TrackingTreerUL17_2017/230329_140354", 4, fnbase="trackingtreer"),
'BTagCSV2017C': _fromnum1("/store/user/shogan/BTagCSV/TrackingTreerUL17_2017/230329_140406", 24, fnbase="trackingtreer"),
'BTagCSV2017D': _fromnum1("/store/user/shogan/BTagCSV/TrackingTreerUL17_2017/230329_140419", 15, fnbase="trackingtreer"),
'BTagCSV2017E': _fromnum1("/store/user/shogan/BTagCSV/TrackingTreerUL17_2017/230329_140431", 61, fnbase="trackingtreer"),
'BTagCSV2017F': _fromnum1("/store/user/shogan/BTagCSV/TrackingTreerUL17_2017/230329_140442", 188, fnbase="trackingtreer"),
'DisplacedJet2017C': _fromnum1("/store/user/shogan/DisplacedJet/TrackingTreerUL17_2017/230329_140454", 14, fnbase="trackingtreer"),
'DisplacedJet2017D': _fromnum1("/store/user/shogan/DisplacedJet/TrackingTreerUL17_2017/230329_140506", 5, fnbase="trackingtreer"),
'DisplacedJet2017E': (10, ['/store/user/shogan/DisplacedJet/TrackingTreerUL17_2017/230329_140517/0000/trackingtreer_%i.root' % i for i in chain(xrange(1,3), xrange(4,12))]),
'DisplacedJet2017F': (17, ['/store/user/shogan/DisplacedJet/TrackingTreerUL17_2017/230329_140528/0000/trackingtreer_%i.root' % i for i in chain(xrange(3,13), xrange(14,16), xrange(30,32), [1, 17, 19])]),
})


_add_ds("trackmovermctruthonnormdzulv30bmv6", {
'mfv_stopdbardbar_tau001000um_M0800_2017': (4, ['/store/group/lpclonglived/pkotamni/StopStopbarTo2Dbar2D_M-800_CTau-1mm_TuneCP5_13TeV-pythia8/TrackMoverMCTruthOnnormdzULV30Bmv6_2017/240229_091116/0000/mctruth_%i.root' % i for i in [0, 0, 4, 4]]),
'ggHToSSTo4l_tau1mm_M350_2017': (14, ['/store/group/lpclonglived/pkotamni/ggH_HToSSTo4l_lowctau_MH-800_MS-350_ctauS-1_TuneCP5_13TeV-powheg-pythia8/TrackMoverMCTruthOnnormdzULV30Bmv6_2017/240229_093612/0000/mctruth_%i.root' % i for i in chain(xrange(2), xrange(1,3), xrange(2,4), xrange(3,5), xrange(4,6), xrange(5,7), [0, 6])]),
})

_add_ds("trackmoveronnormdzulv30bmv6", {
'qcdht0300_2017': (510, ['/store/group/lpclonglived/pkotamni/QCD_HT300to500_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverOnnormdzULV30Bmv6_2017/240302_150829/0000/movedtree_%i.root' % i for i in chain(xrange(6,12), xrange(14,16), xrange(17,30), xrange(31,33), xrange(34,43), xrange(45,47), xrange(55,59), xrange(60,80), xrange(81,97), xrange(98,103), xrange(104,109), xrange(110,114), xrange(115,118), xrange(119,124), xrange(127,131), xrange(132,140), xrange(148,166), xrange(167,178), xrange(179,189), xrange(190,212), xrange(213,215), xrange(216,241), xrange(242,249), xrange(250,253), xrange(254,261), xrange(262,279), xrange(280,301), xrange(302,349), xrange(356,371), xrange(376,408), xrange(409,453), xrange(471,476), xrange(489,548), xrange(549,552), xrange(564,572), xrange(575,577), xrange(580,584), xrange(585,587), xrange(588,591), xrange(593,595), xrange(596,625), [0, 48, 50, 146])]),
'qcdht0500_2017': (1330, ['/store/group/lpclonglived/pkotamni/QCD_HT500to700_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverOnnormdzULV30Bmv6_2017/240302_150830' + '/%04i/movedtree_%i.root' % (i/1000,i) for i in chain(xrange(34,61), xrange(62,67), xrange(68,75), xrange(76,108), xrange(110,143), xrange(144,163), xrange(164,178), xrange(180,211), xrange(214,237), xrange(238,240), xrange(245,248), xrange(251,253), xrange(255,270), xrange(271,336), xrange(337,352), xrange(355,362), xrange(364,389), xrange(392,412), xrange(413,416), xrange(418,425), xrange(426,432), xrange(436,443), xrange(444,451), xrange(452,492), xrange(493,530), xrange(531,550), xrange(557,574), xrange(576,585), xrange(586,592), xrange(593,596), xrange(603,630), xrange(631,636), xrange(644,712), xrange(713,717), xrange(718,721), xrange(722,731), xrange(732,760), xrange(761,770), xrange(771,796), xrange(797,799), xrange(800,850), xrange(851,860), xrange(861,910), xrange(914,916), xrange(917,933), xrange(934,955), xrange(956,958), xrange(959,994), xrange(998,1001), xrange(1014,1061), xrange(1066,1095), xrange(1096,1115), xrange(1117,1130), xrange(1132,1138), xrange(1139,1176), xrange(1177,1187), xrange(1188,1210), xrange(1212,1219), xrange(1222,1242), xrange(1244,1259), xrange(1260,1266), xrange(1267,1287), xrange(1289,1304), xrange(1308,1315), xrange(1317,1319), xrange(1321,1329), xrange(1332,1340), xrange(1341,1346), xrange(1347,1370), xrange(1371,1382), xrange(1383,1431), xrange(1432,1458), xrange(1459,1469), xrange(1470,1501), xrange(1502,1505), [212, 241, 243, 390, 553, 911, 1064, 1305, 1330])]),
'qcdht0700_2017': (666, ['/store/group/lpclonglived/pkotamni/QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverOnnormdzULV30Bmv6_2017/240302_150831/0000/movedtree_%i.root' % i for i in chain(xrange(2,31), xrange(32,48), xrange(49,67), xrange(68,96), xrange(97,109), xrange(110,231), xrange(232,254), xrange(255,265), xrange(266,291), xrange(294,300), xrange(301,321), xrange(322,333), xrange(335,340), xrange(341,368), xrange(369,378), xrange(379,405), xrange(409,417), xrange(418,424), xrange(425,427), xrange(428,437), xrange(438,440), xrange(441,450), xrange(451,478), xrange(479,483), xrange(486,494), xrange(495,499), xrange(500,537), xrange(538,554), xrange(555,591), xrange(592,649), xrange(652,666), xrange(669,690), xrange(691,695), xrange(697,709), [0, 292, 406, 484, 667])]),
'qcdht1000_2017': (442, ['/store/group/lpclonglived/pkotamni/QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8/TrackMoverOnnormdzULV30Bmv6_2017/240302_150832/0000/movedtree_%i.root' % i for i in chain(xrange(4,11), xrange(14,34), xrange(35,37), xrange(48,59), xrange(60,70), xrange(71,87), xrange(88,128), xrange(130,132), xrange(133,147), xrange(148,154), xrange(155,185), xrange(186,192), xrange(193,213), xrange(214,218), xrange(219,253), xrange(256,271), xrange(272,279), xrange(280,324), xrange(325,332), xrange(333,350), xrange(351,379), xrange(391,393), xrange(397,399), xrange(400,426), xrange(427,429), xrange(431,438), xrange(439,449), xrange(450,477), xrange(478,486), xrange(487,489), xrange(491,494), xrange(495,505), [1, 12, 394])]),
'ttbar_2017': _fromnum0("/store/group/lpclonglived/pkotamni/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/TrackMoverOnnormdzULV30Bmv6_2017/240301_074805", 175, fnbase="movedtree"),
'BTagCSV2017B': _fromnum0("/store/group/lpclonglived/pkotamni/BTagCSV/TrackMoverOnnormdzULV30Bmv6_2017/240302_150824", 8, fnbase="movedtree"),
'BTagCSV2017C': (106, ['/store/group/lpclonglived/pkotamni/BTagCSV/TrackMoverOnnormdzULV30Bmv6_2017/240302_150825/0000/movedtree_%i.root' % i for i in chain(xrange(8), xrange(9,15), xrange(16,25), xrange(26,50), xrange(51,54), xrange(57,85), xrange(86,95), xrange(96,110), xrange(111,115), [55])]),
'BTagCSV2017D': _fromnum0("/store/group/lpclonglived/pkotamni/BTagCSV/TrackMoverOnnormdzULV30Bmv6_2017/240302_150826", 28, fnbase="movedtree"),
'BTagCSV2017E': (71, ['/store/group/lpclonglived/pkotamni/BTagCSV/TrackMoverOnnormdzULV30Bmv6_2017/240302_150827/0000/movedtree_%i.root' % i for i in chain(xrange(48), xrange(49,51), xrange(55,59), xrange(63,73), xrange(74,81))]),
'BTagCSV2017F': (327, ['/store/group/lpclonglived/pkotamni/BTagCSV/TrackMoverOnnormdzULV30Bmv6_2017/240302_150828/0000/movedtree_%i.root' % i for i in chain(xrange(3), xrange(4,8), xrange(9,13), xrange(14,31), xrange(33,51), xrange(53,57), xrange(58,75), xrange(77,80), xrange(81,90), xrange(94,98), xrange(101,106), xrange(107,110), xrange(114,139), xrange(140,142), xrange(144,181), xrange(182,187), xrange(189,191), xrange(199,204), xrange(205,213), xrange(221,228), xrange(229,234), xrange(236,257), xrange(258,266), xrange(267,271), xrange(272,274), xrange(275,282), xrange(285,309), xrange(310,321), xrange(324,329), xrange(330,333), xrange(343,346), xrange(347,356), xrange(361,365), xrange(366,371), xrange(372,374), xrange(375,378), xrange(383,390), xrange(393,395), xrange(400,404), xrange(405,407), xrange(408,414), xrange(416,418), [91, 334, 338, 359, 381, 398])]),
'DisplacedJet2017C': (18, ['/store/group/lpclonglived/pkotamni/DisplacedJet/TrackMoverOnnormdzULV30Bmv6_2017/240302_150820/0000/movedtree_%i.root' % i for i in chain(xrange(2), xrange(3,19))]),
'DisplacedJet2017D': (10, ['/store/group/lpclonglived/pkotamni/DisplacedJet/TrackMoverOnnormdzULV30Bmv6_2017/240302_150821/0000/movedtree_%i.root' % i for i in chain(xrange(3), xrange(4,8), xrange(9,12))]),
'DisplacedJet2017E': _fromnum0("/store/group/lpclonglived/pkotamni/DisplacedJet/TrackMoverOnnormdzULV30Bmv6_2017/240302_150822", 21, fnbase="movedtree"),
'DisplacedJet2017F': (58, ['/store/group/lpclonglived/pkotamni/DisplacedJet/TrackMoverOnnormdzULV30Bmv6_2017/240302_150823/0000/movedtree_%i.root' % i for i in chain(xrange(4), xrange(5,14), xrange(15,27), xrange(28,33), xrange(34,38), xrange(39,45), xrange(46,51), xrange(52,63), xrange(66,68))]),
})

# As of late November '23, this ntuple version will be used to study trigger behaviors
# and includes a pretty comprehensive amount of HLT jet information for trigger studies.
# Different background sources use different triggering schemes:
# ttbar_2018:       IsoMu27 OR HT425
# ttbar_ll_2018:    Dilepton triggers
# qcd sim:          HT425
# DisplacedJet2018: HT425
# SingleMuon2018:   IsoMu27
# MuonEG2018:       Dilepton triggers
_add_ds("ntupleulv9_trigstudy_bm", {
'ttbar_2018': (129, ['/store/user/shogan/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleUL18V9Bm_2018/240112_192936/0000/ntuple_%i.root' % i for i in chain(xrange(1,110), xrange(111,113), xrange(118,124), xrange(125,127), xrange(128,137), [116])]),
'ttbar_ll_2018': _fromnum1("/store/user/lpclonglived/shogan/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/NtupleUL18V9Bm_2018/240118_170231", 310),
'DisplacedJet2018A': _fromnum1("/store/user/lpclonglived/shogan/DisplacedJet/NtupleUL18V9Bm_2018/240112_190855", 14),
'DisplacedJet2018B': _fromnum1("/store/user/lpclonglived/shogan/DisplacedJet/NtupleUL18V9Bm_2018/240112_190917", 5),
'DisplacedJet2018C': _fromnum1("/store/user/lpclonglived/shogan/DisplacedJet/NtupleUL18V9Bm_2018/240112_190939", 4),
'DisplacedJet2018D': _fromnum1("/store/user/lpclonglived/shogan/DisplacedJet/NtupleUL18V9Bm_2018/240112_191002", 21),
'MuonEG2018A': _fromnum1("/store/user/lpclonglived/shogan/MuonEG/NtupleUL18V9Bm_2018/240118_170253", 57),
'MuonEG2018B': _fromnum1("/store/user/lpclonglived/shogan/MuonEG/NtupleUL18V9Bm_2018/240118_170318", 24),
'MuonEG2018C': _fromnum1("/store/user/lpclonglived/shogan/MuonEG/NtupleUL18V9Bm_2018/240118_170340", 26),
'MuonEG2018D': _fromnum1("/store/user/lpclonglived/shogan/MuonEG/NtupleUL18V9Bm_2018/240118_170402", 112),
'SingleMuon2018A': _fromnum1("/store/user/lpclonglived/shogan/SingleMuon/NtupleUL18V9Bm_2018/240112_191958", 276),
'SingleMuon2018B': _fromnum1("/store/user/lpclonglived/shogan/SingleMuon/NtupleUL18V9Bm_2018/240112_192020", 133),
'SingleMuon2018C': _fromnum1("/store/user/lpclonglived/shogan/SingleMuon/NtupleUL18V9Bm_2018/240112_192042", 131),
'SingleMuon2018D': _fromnum1("/store/user/lpclonglived/shogan/SingleMuon/NtupleUL18V9Bm_2018/240112_192105", 532),
'qcdht0100_2018': _fromnum1("/store/user/lpclonglived/shogan/QCD_HT100to200_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV9_trigstudy_Bm_2018/240117_220131", 196),
'qcdht0200_2018': _fromnum1("/store/user/lpclonglived/shogan/QCD_HT200to300_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV9_trigstudy_Bm_2018/240117_220153", 225),
'qcdht0300_2018': _fromnum1("/store/user/lpclonglived/shogan/QCD_HT300to500_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV9_trigstudy_Bm_2018/240117_220218", 77),
'qcdht0500_2018': (21, ['/store/user/lpclonglived/shogan/QCD_HT500to700_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV9_trigstudy_Bm_2018/240117_220245/0000/ntuple_%i.root' % i for i in chain(xrange(3,6), xrange(7,9), xrange(11,14), xrange(17,21), xrange(39,41), xrange(42,45), [1, 15, 33, 46])]),
'qcdht0700_2018': (20, ['/store/user/lpclonglived/shogan/QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV9_trigstudy_Bm_2018/240117_220327/0000/ntuple_%i.root' % i for i in chain(xrange(1,6), xrange(12,14), xrange(22,24), xrange(26,28), xrange(30,34), xrange(35,37), xrange(38,40), [16])]),
'qcdht1000_2018': _fromnum1("/store/user/lpclonglived/shogan/QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV9_trigstudy_Bm_2018/240117_220349", 65),
'qcdht1500_2018': _fromnum1("/store/user/lpclonglived/shogan/QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV9_trigstudy_Bm_2018/240117_220417", 141),
'qcdht2000_2018': _fromnum1("/store/user/lpclonglived/shogan/QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV9_trigstudy_Bm_2018/240117_220440", 64),

'ttbar_2016': _fromnum1("/store/user/lpclonglived/shogan/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleUL16V9_trigstudy_Bm_20162/240124_203533", 201),
'ttbar_ll_2016': _fromnum1("/store/user/lpclonglived/shogan/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/NtupleUL16V9_trigstudy_Bm_20162/240124_202149", 107),
'DisplacedJet2016F': _fromnum1("/store/user/lpclonglived/shogan/DisplacedJet/NtupleUL16V9_trigstudy_Bm_20162/240125_150727", 3),
'DisplacedJet2016G': _fromnum1("/store/user/lpclonglived/shogan/DisplacedJet/NtupleUL16V9_trigstudy_Bm_20162/240125_150751", 23),
'DisplacedJet2016H': _fromnum1("/store/user/lpclonglived/shogan/DisplacedJet/NtupleUL16V9_trigstudy_Bm_20162/240125_150814", 22),
'MuonEG2016F': _fromnum1("/store/user/lpclonglived/shogan/MuonEG/NtupleUL16V9_trigstudy_Bm_20162/240125_145248", 4),
'MuonEG2016G': _fromnum1("/store/user/lpclonglived/shogan/MuonEG/NtupleUL16V9_trigstudy_Bm_20162/240125_145311", 37),
'MuonEG2016H': _fromnum1("/store/user/lpclonglived/shogan/MuonEG/NtupleUL16V9_trigstudy_Bm_20162/240125_145332", 33),
'SingleMuon2016F': _fromnum1("/store/user/lpclonglived/shogan/SingleMuon/NtupleUL16V9_trigstudy_Bm_20162/240125_144827", 8),
'SingleMuon2016G': (149, ['/store/user/lpclonglived/shogan/SingleMuon/NtupleUL16V9_trigstudy_Bm_20162/240125_144849/0000/ntuple_%i.root' % i for i in chain(xrange(1,16), xrange(17,60), xrange(61,152))]),
'SingleMuon2016H': _fromnum1("/store/user/lpclonglived/shogan/SingleMuon/NtupleUL16V9_trigstudy_Bm_20162/240125_144911", 177),
'qcdht0100_2016': _fromnum1("/store/user/lpclonglived/shogan/QCD_HT100to200_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleUL16V9_trigstudy_Bm_20162/240214_182236", 89),
'qcdht0200_2016': _fromnum1("/store/user/lpclonglived/shogan/QCD_HT200to300_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleUL16V9_trigstudy_Bm_20162/240214_182258", 54),
'qcdht0300_2016': _fromnum1("/store/user/lpclonglived/shogan/QCD_HT300to500_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleUL16V9_trigstudy_Bm_20162/240214_182320", 61),
'qcdht0500_2016': (117, ['/store/user/lpclonglived/shogan/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleUL16V9_trigstudy_Bm_20162/240214_182343/0000/ntuple_%i.root' % i for i in chain(xrange(1,70), 
xrange(71,119))]),
'qcdht0700_2016': (98, ['/store/user/lpclonglived/shogan/QCD_HT700to1000_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleUL16V9_trigstudy_Bm_20162/240214_182405/0000/ntuple_%i.root' % i for i in chain(xrange(1,37), 
xrange(38,100))]),
'qcdht1000_2016': _fromnum1("/store/user/lpclonglived/shogan/QCD_HT1000to1500_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleUL16V9_trigstudy_Bm_20162/240214_182428", 28),
'qcdht1500_2016': _fromnum1("/store/user/lpclonglived/shogan/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleUL16V9_trigstudy_Bm_20162/240214_182451", 26),
'qcdht2000_2016': _fromnum1("/store/user/lpclonglived/shogan/QCD_HT2000toInf_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleUL16V9_trigstudy_Bm_20162/240214_182513", 23),

'qcdht0100_2016APV': _fromnum1("/store/user/lpclonglived/shogan/QCD_HT100to200_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleUL16APVV9_trigstudy_Bm_20161/240215_195154", 81),
'qcdht0200_2016APV': _fromnum1("/store/user/lpclonglived/shogan/QCD_HT200to300_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleUL16APVV9_trigstudy_Bm_20161/240215_195216", 68),
'qcdht0300_2016APV': _fromnum1("/store/user/lpclonglived/shogan/QCD_HT300to500_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleUL16APVV9_trigstudy_Bm_20161/240215_195239", 64),
'qcdht0500_2016APV': _fromnum1("/store/user/lpclonglived/shogan/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleUL16APVV9_trigstudy_Bm_20161/240215_195301", 93),
'qcdht0700_2016APV': _fromnum1("/store/user/lpclonglived/shogan/QCD_HT700to1000_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleUL16APVV9_trigstudy_Bm_20161/240215_195323", 68),
'qcdht1000_2016APV': _fromnum1("/store/user/lpclonglived/shogan/QCD_HT1000to1500_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleUL16APVV9_trigstudy_Bm_20161/240215_195345", 30),
'qcdht1500_2016APV': _fromnum1("/store/user/lpclonglived/shogan/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleUL16APVV9_trigstudy_Bm_20161/240215_195407", 36),
'qcdht2000_2016APV': _fromnum1("/store/user/lpclonglived/shogan/QCD_HT2000toInf_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleUL16APVV9_trigstudy_Bm_20161/240215_195429", 21),
'ttbar_2016APV': _fromnum1("/store/user/lpclonglived/shogan/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleUL16APVV9_trigstudy_Bm_20161/240215_215940", 141),
'ttbar_ll_2016APV': _fromnum1("/store/user/lpclonglived/shogan/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/NtupleUL16APVV9_trigstudy_Bm_20161/240215_200637", 66),
'DisplacedJet2016APVB': _fromnum1("/store/user/lpclonglived/shogan/DisplacedJet/NtupleUL16APVV9_trigstudy_Bm_20161/240216_195659", 47),
'DisplacedJet2016APVC': _fromnum1("/store/user/lpclonglived/shogan/DisplacedJet/NtupleUL16APVV9_trigstudy_Bm_20161/240216_195720", 21),
'DisplacedJet2016APVD': _fromnum1("/store/user/lpclonglived/shogan/DisplacedJet/NtupleUL16APVV9_trigstudy_Bm_20161/240216_195741", 24),
'DisplacedJet2016APVE': _fromnum1("/store/user/lpclonglived/shogan/DisplacedJet/NtupleUL16APVV9_trigstudy_Bm_20161/240216_195802", 19),
'DisplacedJet2016APVF': _fromnum1("/store/user/lpclonglived/shogan/DisplacedJet/NtupleUL16APVV9_trigstudy_Bm_20161/240216_195823", 13),
'MuonEG2016APVBv2': _fromnum1("/store/user/lpclonglived/shogan/MuonEG/NtupleUL16APVV9_trigstudy_Bm_20161/240216_210657", 29),
'MuonEG2016APVC': _fromnum1("/store/user/lpclonglived/shogan/MuonEG/NtupleUL16APVV9_trigstudy_Bm_20161/240216_210718", 17),
'MuonEG2016APVD': _fromnum1("/store/user/lpclonglived/shogan/MuonEG/NtupleUL16APVV9_trigstudy_Bm_20161/240215_215356", 27),
'MuonEG2016APVE': _fromnum1("/store/user/lpclonglived/shogan/MuonEG/NtupleUL16APVV9_trigstudy_Bm_20161/240215_215418", 24),
'MuonEG2016APVF': _fromnum1("/store/user/lpclonglived/shogan/MuonEG/NtupleUL16APVV9_trigstudy_Bm_20161/240215_215439", 17),
'SingleMuon2016APVBv2': (128, ['/store/user/lpclonglived/shogan/SingleMuon/NtupleUL16APVV9_trigstudy_Bm_20161/240216_210534/0000/ntuple_%i.root' % i for i in chain(xrange(1,79), xrange(80,91), xrange(92,131))]),
'SingleMuon2016APVC': _fromnum1("/store/user/lpclonglived/shogan/SingleMuon/NtupleUL16APVV9_trigstudy_Bm_20161/240216_210556", 62),
'SingleMuon2016APVD': _fromnum1("/store/user/lpclonglived/shogan/SingleMuon/NtupleUL16APVV9_trigstudy_Bm_20161/240215_215659", 63),
'SingleMuon2016APVE': _fromnum1("/store/user/lpclonglived/shogan/SingleMuon/NtupleUL16APVV9_trigstudy_Bm_20161/240215_215721", 87),
'SingleMuon2016APVF': _fromnum1("/store/user/lpclonglived/shogan/SingleMuon/NtupleUL16APVV9_trigstudy_Bm_20161/240215_215742", 83),

})

# As of mid-December '23, this ntuple is identical to the one below, but fixes an issue where ~no
# HLT calojets were saved. I don't think this information will be needed in the long run (hence why
# I'm not planning on making signal ntuples for this version), but is necessary to help debug some
# filter studies.
#
# BKG has an IsoMu27 trigger applied
_add_ds("ntupleulv9_more_hltcalobm", {
'ttbar_2017': (51, ['/store/user/lpclonglived/shogan/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleULV9_more_HLTCaloBm_2017/231215_013947/0000/ntuple_%i.root' % i for i in chain(xrange(1,8), xrange(12,19), xrange(22,26), xrange(27,32), xrange(33,43), xrange(44,54), xrange(55,61), [9, 20])]),
'SingleMuon2017B': (104, ['/store/user/lpclonglived/shogan/SingleMuon/NtupleULV9_more_HLTCaloBm_2017/231215_013754/0000/ntuple_%i.root' % i for i in chain(xrange(1,76), xrange(77,88), xrange(89,107))]),
'SingleMuon2017C': (132, ['/store/user/lpclonglived/shogan/SingleMuon/NtupleULV9_more_HLTCaloBm_2017/231215_013817/0000/ntuple_%i.root' % i for i in chain(xrange(1,4), xrange(8,11), xrange(12,14), xrange(15,67), xrange(68,99), xrange(100,140), [5])]),
'SingleMuon2017D': (58, ['/store/user/lpclonglived/shogan/SingleMuon/NtupleULV9_more_HLTCaloBm_2017/231215_013839/0000/ntuple_%i.root' % i for i in chain(xrange(1,25), xrange(26,52), xrange(53,56), xrange(60,64), [57])]),
'SingleMuon2017E': (149, ['/store/user/lpclonglived/shogan/SingleMuon/NtupleULV9_more_HLTCaloBm_2017/231215_013902/0000/ntuple_%i.root' % i for i in chain(xrange(1,13), xrange(14,19), xrange(20,22), xrange(23,32), xrange(33,37), xrange(41,140), xrange(141,153), xrange(154,160))]),
'SingleMuon2017F': (240, ['/store/user/lpclonglived/shogan/SingleMuon/NtupleULV9_more_HLTCaloBm_2017/231215_013924/0000/ntuple_%i.root' % i for i in chain(xrange(1,19), xrange(20,39), xrange(40,151), xrange(152,244))]),
})

_add_ds("ntupleulv9_dileptrigbm", {
'ttbar_2017': _fromnum1("/store/user/shogan/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleUL17V9_dileptrigBm_2017/231219_191715", 60),
'ttbar_ll_2017': (113, ['/store/user/shogan/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/NtupleULV9_dileptrigBm_2017/240123_142719/0000/ntuple_%i.root' % i for i in chain(xrange(2,6), xrange(7,16), xrange(17,32), xrange(33,39), xrange(44,51), xrange(52,60), xrange(61,67), xrange(68,73), xrange(74,77), xrange(78,87), xrange(90,107), xrange(108,113), xrange(116,121), xrange(122,124), xrange(128,131), xrange(132,137), [42, 88, 114, 126])]),
'MuonEG2017B': _fromnum1("/store/user/shogan/MuonEG/NtupleUL17V9_dileptrigBm_2017/231219_191446", 5),
'MuonEG2017C': (17, ['/store/user/shogan/MuonEG/NtupleUL17V9_dileptrigBm_2017/231219_191515/0000/ntuple_%i.root' % i for i in chain(xrange(1,3), xrange(5,20))]),
'MuonEG2017D': (9, ['/store/user/shogan/MuonEG/NtupleUL17V9_dileptrigBm_2017/231219_191539/0000/ntuple_%i.root' % i for i in chain(xrange(1,7), xrange(9,12))]),
'MuonEG2017E': _fromnum1("/store/user/shogan/MuonEG/NtupleUL17V9_dileptrigBm_2017/231219_191627", 27),
'MuonEG2017F': _fromnum1("/store/user/shogan/MuonEG/NtupleUL17V9_dileptrigBm_2017/231219_191652", 36),

})

# Used to get sumdbv overlap correction curves. Due to how ntkseeds works, there is no event filter (and thus no trigger) applied.
_add_ds("ntupleulv9bm_ntkseeds", {
'qcdht0100_2016APV': _fromnum1("/store/user/shogan/QCD_HT100to200_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleULV9Bm_NTkSeeds_20161/240229_165651", 81, fnbase="ntkseeds"),
'qcdht0200_2016APV': _fromnum1("/store/user/shogan/QCD_HT200to300_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleULV9Bm_NTkSeeds_20161/240229_165713", 68, fnbase="ntkseeds"),
'qcdht0300_2016APV': (63, ['/store/user/shogan/QCD_HT300to500_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleULV9Bm_NTkSeeds_20161/240229_165734/0000/ntkseeds_%i.root' % i for i in chain(xrange(1,20), xrange(21,65))]),
'qcdht0500_2016APV': _fromnum1("/store/user/shogan/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleULV9Bm_NTkSeeds_20161/240229_165756", 93, fnbase="ntkseeds"),
'qcdht0700_2016APV': _fromnum1("/store/user/shogan/QCD_HT700to1000_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleULV9Bm_NTkSeeds_20161/240229_165818", 68, fnbase="ntkseeds"),
'qcdht1000_2016APV': _fromnum1("/store/user/shogan/QCD_HT1000to1500_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleULV9Bm_NTkSeeds_20161/240229_165839", 29, fnbase="ntkseeds"),
'qcdht1500_2016APV': _fromnum1("/store/user/shogan/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleULV9Bm_NTkSeeds_20161/240229_165902", 36, fnbase="ntkseeds"),
'qcdht2000_2016APV': _fromnum1("/store/user/shogan/QCD_HT2000toInf_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleULV9Bm_NTkSeeds_20161/240229_165923", 21, fnbase="ntkseeds"),
'ttbar_2016APV': _fromnum1("/store/user/shogan/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleULV9Bm_NTkSeeds_20161/240229_165945", 142, fnbase="ntkseeds"),
'qcdht0100_2016': _fromnum1("/store/user/shogan/QCD_HT100to200_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleULV9Bm_NTkSeeds_20162/240229_170317", 89, fnbase="ntkseeds"),
'qcdht0200_2016': _fromnum1("/store/user/shogan/QCD_HT200to300_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleULV9Bm_NTkSeeds_20162/240229_170339", 54, fnbase="ntkseeds"),
'qcdht0300_2016': _fromnum1("/store/user/shogan/QCD_HT300to500_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleULV9Bm_NTkSeeds_20162/240229_170400", 63, fnbase="ntkseeds"),
'qcdht0500_2016': _fromnum1("/store/user/shogan/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleULV9Bm_NTkSeeds_20162/240229_170429", 119, fnbase="ntkseeds"),
'qcdht0700_2016': _fromnum1("/store/user/shogan/QCD_HT700to1000_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleULV9Bm_NTkSeeds_20162/240229_170506", 103, fnbase="ntkseeds"),
'qcdht1000_2016': _fromnum1("/store/user/shogan/QCD_HT1000to1500_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleULV9Bm_NTkSeeds_20162/240229_170530", 28, fnbase="ntkseeds"),
'qcdht1500_2016': _fromnum1("/store/user/shogan/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleULV9Bm_NTkSeeds_20162/240229_170556", 26, fnbase="ntkseeds"),
'qcdht2000_2016': _fromnum1("/store/user/shogan/QCD_HT2000toInf_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleULV9Bm_NTkSeeds_20162/240229_170618", 24, fnbase="ntkseeds"),
'ttbar_2016': _fromnum1("/store/user/shogan/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleULV9Bm_NTkSeeds_20162/240229_170643", 201, fnbase="ntkseeds"),
'qcdht0300_2017': (259, ['/store/user/shogan/QCD_HT300to500_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV9Bm_NTkSeeds_2017/240229_171034/0000/ntkseeds_%i.root' % i for i in chain(xrange(1,93), xrange(94,261))]),
'qcdht0500_2017': _fromnum1("/store/user/shogan/QCD_HT500to700_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV9Bm_NTkSeeds_2017/240229_171057", 508, fnbase="ntkseeds"),
'qcdht0700_2017': _fromnum1("/store/user/shogan/QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV9Bm_NTkSeeds_2017/240229_171119", 286, fnbase="ntkseeds"),
'qcdht1000_2017': _fromnum1("/store/user/shogan/QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV9Bm_NTkSeeds_2017/240229_171143", 173, fnbase="ntkseeds"),
'qcdht1500_2017': _fromnum1("/store/user/shogan/QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV9Bm_NTkSeeds_2017/240229_171204", 445, fnbase="ntkseeds"),
'ttbar_2017': (58, ['/store/user/shogan/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleULV9Bm_NTkSeeds_2017/240229_171227/0000/ntkseeds_%i.root' % i for i in chain(xrange(1,13), xrange(14,25), xrange(26,61))]),
'qcdht0100_2018': _fromnum1("/store/user/shogan/QCD_HT100to200_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV9Bm_NTkSeeds_2018/240229_171438", 186, fnbase="ntkseeds"),
'qcdht0200_2018': _fromnum1("/store/user/shogan/QCD_HT200to300_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV9Bm_NTkSeeds_2018/240229_171538", 193, fnbase="ntkseeds"),
'qcdht0300_2018': _fromnum1("/store/user/shogan/QCD_HT300to500_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV9Bm_NTkSeeds_2018/240229_171601", 41, fnbase="ntkseeds"),
'qcdht0500_2018': _fromnum1("/store/user/shogan/QCD_HT500to700_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV9Bm_NTkSeeds_2018/240229_171623", 46, fnbase="ntkseeds"),
'qcdht0700_2018': _fromnum1("/store/user/shogan/QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV9Bm_NTkSeeds_2018/240229_171645", 40, fnbase="ntkseeds"),
'qcdht1000_2018': (59, ['/store/user/shogan/QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV9Bm_NTkSeeds_2018/240229_171710/0000/ntkseeds_%i.root' % i for i in chain(xrange(1,27), xrange(28,36), xrange(37,62))]),
'qcdht1500_2018': (140, ['/store/user/shogan/QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV9Bm_NTkSeeds_2018/240229_171734/0000/ntkseeds_%i.root' % i for i in chain(xrange(1,61), xrange(62,142))]),
'qcdht2000_2018': _fromnum1("/store/user/shogan/QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV9Bm_NTkSeeds_2018/240229_171757", 64, fnbase="ntkseeds"),
'ttbar_2018': (134, ['/store/user/shogan/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleULV9Bm_NTkSeeds_2018/240229_171822/0000/ntkseeds_%i.root' % i for i in chain(xrange(1,66), xrange(67,80), xrange(81,137))]),
})


# As of late November '23, this is the main ntuple type for the analysis. Includes a few bugfixes (e.g. electron iso)
# and includes a pretty comprehensive amount of HLT jet information for trigger studies.
# Signal will have no triggers applied.
_add_ds("ntupleulv9bm", {

# 2016APV Background
'ttbar_2016APV': _fromnum1("/store/user/shogan/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleUL16APVV9Bm_20161/240228_193436", 141),
'qcdht0100_2016APV': _fromnum1("/store/user/shogan/QCD_HT100to200_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleUL16APVV9Bm_20161/240228_193129", 81),
'qcdht0200_2016APV': _fromnum1("/store/user/shogan/QCD_HT200to300_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleUL16APVV9Bm_20161/240228_193152", 68),
'qcdht0300_2016APV': _fromnum1("/store/user/shogan/QCD_HT300to500_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleUL16APVV9Bm_20161/240228_193216", 64),
'qcdht0500_2016APV': _fromnum1("/store/user/shogan/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleUL16APVV9Bm_20161/240228_193239", 93),
'qcdht0700_2016APV': _fromnum1("/store/user/shogan/QCD_HT700to1000_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleUL16APVV9Bm_20161/240228_193301", 68),
'qcdht1000_2016APV': _fromnum1("/store/user/shogan/QCD_HT1000to1500_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleUL16APVV9Bm_20161/240228_193325", 29),
'qcdht1500_2016APV': _fromnum1("/store/user/shogan/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleUL16APVV9Bm_20161/240228_193349", 36),
'qcdht2000_2016APV': _fromnum1("/store/user/shogan/QCD_HT2000toInf_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleUL16APVV9Bm_20161/240228_193413", 21),

# 2016 Background
'ttbar_2016': _fromnum1("/store/user/shogan/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleUL16V9Bm_20162/240228_192828", 201),
'qcdht0100_2016': _fromnum1("/store/user/shogan/QCD_HT100to200_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleUL16V9Bm_20162/240228_192503", 89),
'qcdht0200_2016': _fromnum1("/store/user/shogan/QCD_HT200to300_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleUL16V9Bm_20162/240228_192529", 54),
'qcdht0300_2016': _fromnum1("/store/user/shogan/QCD_HT300to500_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleUL16V9Bm_20162/240228_192551", 63),
'qcdht0500_2016': _fromnum1("/store/user/shogan/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleUL16V9Bm_20162/240228_192614", 119),
'qcdht0700_2016': _fromnum1("/store/user/shogan/QCD_HT700to1000_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleUL16V9Bm_20162/240228_192635", 103),
'qcdht1000_2016': _fromnum1("/store/user/shogan/QCD_HT1000to1500_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleUL16V9Bm_20162/240228_192656", 28),
'qcdht1500_2016': _fromnum1("/store/user/shogan/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleUL16V9Bm_20162/240228_192722", 26),
'qcdht2000_2016': _fromnum1("/store/user/shogan/QCD_HT2000toInf_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/NtupleUL16V9Bm_20162/240228_192744", 24),

# 2017 Background
'ttbar_2017': _fromnum1("/store/user/lpclonglived/shogan/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleUL17V9Bm_2017/231201_182043", 60),
'SingleMuon2017B': _fromnum1("/store/user/lpclonglived/shogan/SingleMuon/NtupleUL17V9Bm_2017/231201_181852", 106),
'SingleMuon2017C': _fromnum1("/store/user/lpclonglived/shogan/SingleMuon/NtupleUL17V9Bm_2017/231201_181914", 139),
'SingleMuon2017D': _fromnum1("/store/user/lpclonglived/shogan/SingleMuon/NtupleUL17V9Bm_2017/231201_181936", 63),
'SingleMuon2017E': _fromnum1("/store/user/lpclonglived/shogan/SingleMuon/NtupleUL17V9Bm_2017/231201_181959", 159),
'SingleMuon2017F': _fromnum1("/store/user/lpclonglived/shogan/SingleMuon/NtupleUL17V9Bm_2017/231201_182020", 243),
'qcdht0300_2017': _fromnum1("/store/user/shogan/QCD_HT300to500_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleUL17V9Bm_2017/240228_190811", 260),
'qcdht0500_2017': _fromnum1("/store/user/shogan/QCD_HT500to700_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleUL17V9Bm_2017/240228_190833", 508),
'qcdht0700_2017': _fromnum1("/store/user/shogan/QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleUL17V9Bm_2017/240228_190855", 286),
'qcdht1000_2017': _fromnum1("/store/user/shogan/QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleUL17V9Bm_2017/240228_190917", 173),
'qcdht1500_2017': _fromnum1("/store/user/shogan/QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleUL17V9Bm_2017/240228_190942", 445),

# 2018 Background
'qcdht0100_2018': _fromnum1("/store/user/shogan/QCD_HT100to200_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleUL18V9Bm_2018/240228_191240", 186),
'qcdht0200_2018': _fromnum1("/store/user/shogan/QCD_HT200to300_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleUL18V9Bm_2018/240228_191301", 193),
'qcdht0300_2018': _fromnum1("/store/user/shogan/QCD_HT300to500_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleUL18V9Bm_2018/240228_191323", 41),
'qcdht0500_2018': (44, ['/store/user/shogan/QCD_HT500to700_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleUL18V9Bm_2018/240228_191347/0000/ntuple_%i.root' % i for i in chain(xrange(1,20), xrange(21,46))]),  # Miss: 1/45
'qcdht0700_2018': _fromnum1("/store/user/shogan/QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleUL18V9Bm_2018/240228_191411", 40),
'qcdht1000_2018': _fromnum1("/store/user/shogan/QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleUL18V9Bm_2018/240228_191434", 61),
'qcdht1500_2018': _fromnum1("/store/user/shogan/QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleUL18V9Bm_2018/240228_191459", 141),
'qcdht2000_2018': _fromnum1("/store/user/shogan/QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleUL18V9Bm_2018/240228_191525", 64),
'ttbar_2018': (129, ['/store/user/shogan/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleUL18V9Bm_2018/240228_191657/0000/ntuple_%i.root' % i for i in chain(xrange(1,3), xrange(4,6), xrange(9,20), xrange(21,23), xrange(25,56), xrange(57,137), [7])]),  # Miss: 7/136


# 2016APV Signal Samples
'mfv_neu_tau000100um_M0200_2016APV': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-200_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_200752", 17),
'mfv_neu_tau000300um_M0200_2016APV': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-200_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_200824", 14),
'mfv_neu_tau001000um_M0200_2016APV': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-200_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_200846", 4),
'mfv_neu_tau010000um_M0200_2016APV': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-200_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_200909", 3),
'mfv_neu_tau030000um_M0200_2016APV': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-200_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_200930", 5),
'mfv_neu_tau000100um_M0300_2016APV': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_200953", 16),
'mfv_neu_tau000300um_M0300_2016APV': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_201014", 13),
'mfv_neu_tau001000um_M0300_2016APV': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_201036", 5),
'mfv_neu_tau010000um_M0300_2016APV': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_201058", 3),
'mfv_neu_tau030000um_M0300_2016APV': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_201120", 5),
'mfv_neu_tau000100um_M0400_2016APV': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_201141", 17),
'mfv_neu_tau000300um_M0400_2016APV': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_201203", 14),
'mfv_neu_tau001000um_M0400_2016APV': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_201225", 5),
'mfv_neu_tau010000um_M0400_2016APV': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_201247", 3),
'mfv_neu_tau030000um_M0400_2016APV': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_201309", 5),
'mfv_neu_tau000100um_M0600_2016APV': (16, ['/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_201330/0000/ntuple_%i.root' % i for i in chain(xrange(1,5), xrange(6,18))]),
'mfv_neu_tau000300um_M0600_2016APV': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_201351", 7),
'mfv_neu_tau001000um_M0600_2016APV': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_201414", 5),
'mfv_neu_tau010000um_M0600_2016APV': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_201435", 2),
'mfv_neu_tau030000um_M0600_2016APV': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_201456", 2),
'mfv_neu_tau000100um_M0800_2016APV': (16, ['/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_201519/0000/ntuple_%i.root' % i for i in chain(xrange(1,7), xrange(8,18))]),
'mfv_neu_tau000300um_M0800_2016APV': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_201540", 7),
'mfv_neu_tau001000um_M0800_2016APV': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_201601", 2),
'mfv_neu_tau010000um_M0800_2016APV': (1, ['/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_201623/0000/ntuple_1.root']),
'mfv_neu_tau030000um_M0800_2016APV': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_201645", 4),
'mfv_neu_tau000100um_M1200_2016APV': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_201706", 15),
'mfv_neu_tau000300um_M1200_2016APV': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_201728", 7),
'mfv_neu_tau001000um_M1200_2016APV': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_201750", 2),
'mfv_neu_tau010000um_M1200_2016APV': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_201811", 2),
'mfv_neu_tau030000um_M1200_2016APV': (1, ['/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_201834/0000/ntuple_2.root']),
'mfv_neu_tau000100um_M1600_2016APV': (17, ['/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_201856/0000/ntuple_%i.root' % i for i in chain(xrange(3,19), [1])]),
'mfv_neu_tau000300um_M1600_2016APV': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_201917", 6),
'mfv_neu_tau001000um_M1600_2016APV': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_201939", 3),
'mfv_neu_tau030000um_M1600_2016APV': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_202022", 3),
'mfv_neu_tau000100um_M3000_2016APV': (4, ['/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_202045/0000/ntuple_%i.root' % i for i in chain(xrange(9,11), [7, 15])]),
'mfv_neu_tau000300um_M3000_2016APV': _fromnum1("/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_202106", 5),
'mfv_neu_tau030000um_M3000_2016APV': (1, ['/store/user/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_202214/0000/ntuple_2.root']),
'mfv_stopdbardbar_tau000100um_M0200_2016APV': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-200_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_202235", 16),
'mfv_stopdbardbar_tau000300um_M0200_2016APV': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-200_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_202258", 18),
'mfv_stopdbardbar_tau001000um_M0200_2016APV': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-200_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_202319", 6),
'mfv_stopdbardbar_tau010000um_M0200_2016APV': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-200_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_202341", 3),
'mfv_stopdbardbar_tau030000um_M0200_2016APV': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-200_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_202403", 4),
'mfv_stopdbardbar_tau000100um_M0300_2016APV': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-300_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_202425", 16),
'mfv_stopdbardbar_tau000300um_M0300_2016APV': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-300_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_202446", 16),
'mfv_stopdbardbar_tau001000um_M0300_2016APV': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-300_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_202508", 6),
'mfv_stopdbardbar_tau010000um_M0300_2016APV': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-300_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_202530", 3),
'mfv_stopdbardbar_tau030000um_M0300_2016APV': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-300_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_202551", 6),
'mfv_stopdbardbar_tau000100um_M0400_2016APV': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-400_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_202614", 18),
'mfv_stopdbardbar_tau000300um_M0400_2016APV': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-400_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_202640", 16),
'mfv_stopdbardbar_tau001000um_M0400_2016APV': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-400_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_202701", 5),
'mfv_stopdbardbar_tau010000um_M0400_2016APV': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-400_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_202723", 3),
'mfv_stopdbardbar_tau030000um_M0400_2016APV': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-400_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_202744", 4),
'mfv_stopdbardbar_tau000100um_M0600_2016APV': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-600_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_202806", 16),
'mfv_stopdbardbar_tau000300um_M0600_2016APV': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-600_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_202828", 13),
'mfv_stopdbardbar_tau001000um_M0600_2016APV': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-600_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_202849", 4),
'mfv_stopdbardbar_tau010000um_M0600_2016APV': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-600_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_202936", 2),
'mfv_stopdbardbar_tau030000um_M0600_2016APV': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-600_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_202958", 3),
'mfv_stopdbardbar_tau000100um_M0800_2016APV': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-800_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_203019", 18),
'mfv_stopdbardbar_tau000300um_M0800_2016APV': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-800_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_203040", 11),
'mfv_stopdbardbar_tau001000um_M0800_2016APV': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-800_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_203103", 3),
'mfv_stopdbardbar_tau010000um_M0800_2016APV': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-800_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_203124", 2),
'mfv_stopdbardbar_tau030000um_M0800_2016APV': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-800_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_203146", 3),
'mfv_stopdbardbar_tau000100um_M1200_2016APV': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-1200_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_203208", 15),
'mfv_stopdbardbar_tau000300um_M1200_2016APV': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-1200_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_203230", 7),
'mfv_stopdbardbar_tau001000um_M1200_2016APV': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-1200_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_203252", 2),
'mfv_stopdbardbar_tau010000um_M1200_2016APV': (1, ['/store/user/shogan/StopStopbarTo2Dbar2D_M-1200_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_203314/0000/ntuple_1.root']),
'mfv_stopdbardbar_tau030000um_M1200_2016APV': (1, ['/store/user/shogan/StopStopbarTo2Dbar2D_M-1200_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_203335/0000/ntuple_2.root']),
'mfv_stopdbardbar_tau000100um_M1600_2016APV': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-1600_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_203356", 17),
'mfv_stopdbardbar_tau000300um_M1600_2016APV': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-1600_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_203419", 9),
'mfv_stopdbardbar_tau001000um_M1600_2016APV': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-1600_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_203440", 3),
'mfv_stopdbardbar_tau010000um_M1600_2016APV': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-1600_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_203501", 2),
'mfv_stopdbardbar_tau030000um_M1600_2016APV': (1, ['/store/user/shogan/StopStopbarTo2Dbar2D_M-1600_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_203524/0000/ntuple_1.root']),
'mfv_stopdbardbar_tau000100um_M3000_2016APV': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-3000_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_203545", 16),
'mfv_stopdbardbar_tau000300um_M3000_2016APV': _fromnum1("/store/user/shogan/StopStopbarTo2Dbar2D_M-3000_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_203607", 6),
'mfv_stopdbardbar_tau030000um_M3000_2016APV': (1, ['/store/user/shogan/StopStopbarTo2Dbar2D_M-3000_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_203713/0000/ntuple_1.root']),
'mfv_stopbbarbbar_tau000100um_M0200_2016APV': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-200_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_203735", 26),
'mfv_stopbbarbbar_tau000300um_M0200_2016APV': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-200_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_203756", 23),
'mfv_stopbbarbbar_tau001000um_M0200_2016APV': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-200_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_203817", 8),
'mfv_stopbbarbbar_tau010000um_M0200_2016APV': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-200_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_203840", 3),
'mfv_stopbbarbbar_tau030000um_M0200_2016APV': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-200_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_203901", 6),
'mfv_stopbbarbbar_tau000100um_M0300_2016APV': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-300_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_203926", 25),
'mfv_stopbbarbbar_tau000300um_M0300_2016APV': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-300_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_203948", 14),
'mfv_stopbbarbbar_tau001000um_M0300_2016APV': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-300_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_204010", 4),
'mfv_stopbbarbbar_tau010000um_M0300_2016APV': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-300_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_204031", 3),
'mfv_stopbbarbbar_tau030000um_M0300_2016APV': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-300_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_204054", 4),
'mfv_stopbbarbbar_tau000100um_M0400_2016APV': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-400_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_204115", 18),
'mfv_stopbbarbbar_tau000300um_M0400_2016APV': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-400_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_204137", 17),
'mfv_stopbbarbbar_tau001000um_M0400_2016APV': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-400_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_204159", 4),
'mfv_stopbbarbbar_tau010000um_M0400_2016APV': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-400_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_204220", 3),
'mfv_stopbbarbbar_tau030000um_M0400_2016APV': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-400_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_204242", 10),
'mfv_stopbbarbbar_tau000100um_M0600_2016APV': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-600_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_204304", 21),
'mfv_stopbbarbbar_tau000300um_M0600_2016APV': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-600_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_204325", 10),
'mfv_stopbbarbbar_tau001000um_M0600_2016APV': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-600_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_204347", 3),
'mfv_stopbbarbbar_tau010000um_M0600_2016APV': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-600_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_204409", 2),
'mfv_stopbbarbbar_tau030000um_M0600_2016APV': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-600_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_204430", 4),
'mfv_stopbbarbbar_tau000100um_M0800_2016APV': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-800_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_204452", 18),
'mfv_stopbbarbbar_tau000300um_M0800_2016APV': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-800_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_204516", 11),
'mfv_stopbbarbbar_tau001000um_M0800_2016APV': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-800_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_204537", 8),
'mfv_stopbbarbbar_tau010000um_M0800_2016APV': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-800_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_204559", 3),
'mfv_stopbbarbbar_tau030000um_M0800_2016APV': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-800_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_204621", 3),
'mfv_stopbbarbbar_tau000100um_M1200_2016APV': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-1200_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_204642", 17),
'mfv_stopbbarbbar_tau000300um_M1200_2016APV': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-1200_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_204704", 12),
'mfv_stopbbarbbar_tau001000um_M1200_2016APV': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-1200_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_204726", 2),
'mfv_stopbbarbbar_tau010000um_M1200_2016APV': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-1200_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_204748", 2),
'mfv_stopbbarbbar_tau030000um_M1200_2016APV': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-1200_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_204809", 6),
'mfv_stopbbarbbar_tau000100um_M1600_2016APV': (13, ['/store/user/shogan/StopStopbarTo2Bbar2B_M-1600_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_204831/0000/ntuple_%i.root' % i for i in chain(xrange(1,8), xrange(9,15))]),
'mfv_stopbbarbbar_tau000300um_M1600_2016APV': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-1600_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_204853", 7),
'mfv_stopbbarbbar_tau001000um_M1600_2016APV': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-1600_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_204914", 2),
'mfv_stopbbarbbar_tau010000um_M1600_2016APV': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-1600_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_204937", 2),
'mfv_stopbbarbbar_tau030000um_M1600_2016APV': (1, ['/store/user/shogan/StopStopbarTo2Bbar2B_M-1600_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_204958/0000/ntuple_2.root']),
'mfv_stopbbarbbar_tau000100um_M3000_2016APV': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-3000_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_205020", 17),
'mfv_stopbbarbbar_tau000300um_M3000_2016APV': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-3000_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_205042", 20),
'mfv_stopbbarbbar_tau001000um_M3000_2016APV': (1, ['/store/user/shogan/StopStopbarTo2Bbar2B_M-3000_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_205103/0000/ntuple_3.root']),
'mfv_stopbbarbbar_tau010000um_M3000_2016APV': _fromnum1("/store/user/shogan/StopStopbarTo2Bbar2B_M-3000_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL16APVV9Bm_NoEF_20161/240219_205125", 5),

# 2016 Signal Samples
'mfv_neu_tau000100um_M0200_2016': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-200_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_193224", 17),
'mfv_neu_tau000300um_M0200_2016': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-200_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_193246", 14),
'mfv_neu_tau001000um_M0200_2016': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-200_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_193308", 4),
'mfv_neu_tau010000um_M0200_2016': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-200_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_193332", 3),
'mfv_neu_tau030000um_M0200_2016': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-200_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_193353", 5),
'mfv_neu_tau000100um_M0300_2016': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_193415", 16),
'mfv_neu_tau000300um_M0300_2016': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_193438", 11),
'mfv_neu_tau001000um_M0300_2016': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_193500", 4),
'mfv_neu_tau010000um_M0300_2016': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_193522", 3),
'mfv_neu_tau030000um_M0300_2016': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_193545", 5),
'mfv_neu_tau000100um_M0400_2016': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_193606", 20),
'mfv_neu_tau000300um_M0400_2016': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_193628", 11),
'mfv_neu_tau001000um_M0400_2016': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_193651", 3),
'mfv_neu_tau010000um_M0400_2016': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_193713", 3),
'mfv_neu_tau030000um_M0400_2016': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_193734", 5),
'mfv_neu_tau000100um_M0600_2016': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_193757", 17),
'mfv_neu_tau000300um_M0600_2016': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_193819", 7),
'mfv_neu_tau001000um_M0600_2016': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_193841", 2),
'mfv_neu_tau010000um_M0600_2016': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_193904", 3),
'mfv_neu_tau030000um_M0600_2016': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_193926", 2),
'mfv_neu_tau000100um_M0800_2016': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_193948", 16),
'mfv_neu_tau000300um_M0800_2016': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_194011", 8),
'mfv_neu_tau001000um_M0800_2016': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_194032", 3),
'mfv_neu_tau010000um_M0800_2016': (1, ['/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_194054/0000/ntuple_1.root']),
'mfv_neu_tau030000um_M0800_2016': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_194117", 2),
'mfv_neu_tau000100um_M1200_2016': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_194138", 18),
'mfv_neu_tau000300um_M1200_2016': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_194200", 6),
'mfv_neu_tau001000um_M1200_2016': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_194222", 4),
'mfv_neu_tau010000um_M1200_2016': (1, ['/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_194244/0000/ntuple_1.root']),
'mfv_neu_tau030000um_M1200_2016': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_194306", 2),
'mfv_neu_tau000100um_M1600_2016': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_194329", 17),
'mfv_neu_tau000300um_M1600_2016': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_194351", 9),
'mfv_neu_tau001000um_M1600_2016': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_194413", 3),
'mfv_neu_tau010000um_M1600_2016': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_194435", 2),
'mfv_neu_tau030000um_M1600_2016': (1, ['/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_194457/0000/ntuple_2.root']),
'mfv_neu_tau000100um_M3000_2016': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_194519", 17),
'mfv_neu_tau000300um_M3000_2016': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_194542", 7),
'mfv_neu_tau001000um_M3000_2016': (1, ['/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_194604/0000/ntuple_2.root']),
'mfv_stopdbardbar_tau000100um_M0200_2016': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-200_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_194711", 18),
'mfv_stopdbardbar_tau000300um_M0200_2016': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-200_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_194733", 17),
'mfv_stopdbardbar_tau001000um_M0200_2016': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-200_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_194755", 5),
'mfv_stopdbardbar_tau010000um_M0200_2016': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-200_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_194817", 3),
'mfv_stopdbardbar_tau030000um_M0200_2016': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-200_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_194839", 4),
'mfv_stopdbardbar_tau000100um_M0300_2016': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-300_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_194903", 19),
'mfv_stopdbardbar_tau000300um_M0300_2016': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-300_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_194925", 14),
'mfv_stopdbardbar_tau001000um_M0300_2016': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-300_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_194947", 6),
'mfv_stopdbardbar_tau010000um_M0300_2016': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-300_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_195010", 3),
'mfv_stopdbardbar_tau030000um_M0300_2016': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-300_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_195032", 7),
'mfv_stopdbardbar_tau000100um_M0400_2016': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-400_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_195054", 17),
'mfv_stopdbardbar_tau000300um_M0400_2016': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-400_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_195117", 17),
'mfv_stopdbardbar_tau001000um_M0400_2016': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-400_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_195138", 7),
'mfv_stopdbardbar_tau010000um_M0400_2016': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-400_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_195200", 3),
'mfv_stopdbardbar_tau030000um_M0400_2016': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-400_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_195224", 4),
'mfv_stopdbardbar_tau000100um_M0600_2016': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-600_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_195245", 17),
'mfv_stopdbardbar_tau000300um_M0600_2016': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-600_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_195307", 12),
'mfv_stopdbardbar_tau001000um_M0600_2016': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-600_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_195330", 6),
'mfv_stopdbardbar_tau010000um_M0600_2016': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-600_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_195352", 3),
'mfv_stopdbardbar_tau030000um_M0600_2016': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-600_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_195414", 4),
'mfv_stopdbardbar_tau000100um_M0800_2016': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-800_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_195437", 17),
'mfv_stopdbardbar_tau000300um_M0800_2016': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-800_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_195459", 9),
'mfv_stopdbardbar_tau001000um_M0800_2016': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-800_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_195521", 3),
'mfv_stopdbardbar_tau010000um_M0800_2016': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-800_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_195544", 3),
'mfv_stopdbardbar_tau030000um_M0800_2016': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-800_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_195606", 2),
'mfv_stopdbardbar_tau000100um_M1200_2016': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-1200_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_195628", 17),
'mfv_stopdbardbar_tau000300um_M1200_2016': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-1200_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_195650", 7),
'mfv_stopdbardbar_tau001000um_M1200_2016': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-1200_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_195712", 2),
'mfv_stopdbardbar_tau010000um_M1200_2016': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-1200_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_195734", 2),
'mfv_stopdbardbar_tau030000um_M1200_2016': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-1200_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_195756", 4),
'mfv_stopdbardbar_tau000100um_M1600_2016': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-1600_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_195817", 19),
'mfv_stopdbardbar_tau000300um_M1600_2016': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-1600_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_195840", 9),
'mfv_stopdbardbar_tau001000um_M1600_2016': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-1600_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_195902", 2),
'mfv_stopdbardbar_tau010000um_M1600_2016': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-1600_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_195924", 2),
'mfv_stopdbardbar_tau030000um_M1600_2016': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-1600_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_195946", 4),
'mfv_stopdbardbar_tau000100um_M3000_2016': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-3000_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_200009", 16),
'mfv_stopdbardbar_tau000300um_M3000_2016': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-3000_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_200031", 8),
'mfv_stopdbardbar_tau010000um_M3000_2016': (1, ['/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-3000_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_200117/0000/ntuple_2.root']),
'mfv_stopbbarbbar_tau000100um_M0200_2016': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-200_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_200202", 16),
'mfv_stopbbarbbar_tau000300um_M0200_2016': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-200_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_200226", 14),
'mfv_stopbbarbbar_tau001000um_M0200_2016': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-200_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_200248", 4),
'mfv_stopbbarbbar_tau010000um_M0200_2016': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-200_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_200310", 3),
'mfv_stopbbarbbar_tau030000um_M0200_2016': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-200_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_200334", 4),
'mfv_stopbbarbbar_tau000100um_M0300_2016': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-300_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_200356", 16),
'mfv_stopbbarbbar_tau000300um_M0300_2016': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-300_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_200418", 18),
'mfv_stopbbarbbar_tau001000um_M0300_2016': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-300_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_200441", 4),
'mfv_stopbbarbbar_tau010000um_M0300_2016': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-300_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_200503", 3),
'mfv_stopbbarbbar_tau030000um_M0300_2016': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-300_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_200525", 4),
'mfv_stopbbarbbar_tau000100um_M0400_2016': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-400_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_200548", 17),
'mfv_stopbbarbbar_tau000300um_M0400_2016': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-400_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_200610", 18),
'mfv_stopbbarbbar_tau001000um_M0400_2016': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-400_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_200631", 7),
'mfv_stopbbarbbar_tau010000um_M0400_2016': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-400_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_200654", 3),
'mfv_stopbbarbbar_tau030000um_M0400_2016': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-400_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_200717", 4),
'mfv_stopbbarbbar_tau000100um_M0600_2016': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-600_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_200739", 15),
'mfv_stopbbarbbar_tau000300um_M0600_2016': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-600_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_200801", 12),
'mfv_stopbbarbbar_tau001000um_M0600_2016': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-600_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_200826", 4),
'mfv_stopbbarbbar_tau010000um_M0600_2016': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-600_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_200848", 2),
'mfv_stopbbarbbar_tau030000um_M0600_2016': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-600_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_200911", 3),
'mfv_stopbbarbbar_tau000100um_M0800_2016': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-800_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_200932", 17),
'mfv_stopbbarbbar_tau000300um_M0800_2016': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-800_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_200954", 12),
'mfv_stopbbarbbar_tau001000um_M0800_2016': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-800_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_201017", 5),
'mfv_stopbbarbbar_tau010000um_M0800_2016': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-800_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_201039", 2),
'mfv_stopbbarbbar_tau030000um_M0800_2016': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-800_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_201100", 2),
'mfv_stopbbarbbar_tau000100um_M1200_2016': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-1200_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_201123", 17),
'mfv_stopbbarbbar_tau000300um_M1200_2016': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-1200_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_201145", 9),
'mfv_stopbbarbbar_tau001000um_M1200_2016': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-1200_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_201225", 3),
'mfv_stopbbarbbar_tau010000um_M1200_2016': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-1200_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_201249", 2),
'mfv_stopbbarbbar_tau030000um_M1200_2016': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-1200_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_201310", 2),
'mfv_stopbbarbbar_tau000100um_M1600_2016': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-1600_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_201332", 15),
'mfv_stopbbarbbar_tau000300um_M1600_2016': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-1600_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_201355", 9),
'mfv_stopbbarbbar_tau001000um_M1600_2016': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-1600_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_201417", 2),
'mfv_stopbbarbbar_tau010000um_M1600_2016': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-1600_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_201439", 2),
'mfv_stopbbarbbar_tau030000um_M1600_2016': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-1600_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_201502", 2),
'mfv_stopbbarbbar_tau000100um_M3000_2016': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-3000_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_201524", 18),
'mfv_stopbbarbbar_tau000300um_M3000_2016': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-3000_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_201545", 8),
'mfv_stopbbarbbar_tau010000um_M3000_2016': (1, ['/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-3000_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_201629/0000/ntuple_2.root']),
'mfv_stopbbarbbar_tau030000um_M3000_2016': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-3000_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL16V9Bm_NoEF_20162/240220_201652", 2),


# 2017 Signal Samples
'mfv_neu_tau000100um_M0200_2017': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-200_CTau-100um_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_181504", 30),
'mfv_neu_tau000300um_M0200_2017': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-200_CTau-300um_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_181527", 25),
'mfv_neu_tau010000um_M0200_2017': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-200_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_181551", 5),
'mfv_neu_tau030000um_M0200_2017': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-200_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_181615", 9),
'mfv_neu_tau000100um_M0300_2017': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-100um_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_181638", 34),
'mfv_neu_tau000300um_M0300_2017': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-300um_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_181702", 23),
'mfv_neu_tau001000um_M0300_2017': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_181725", 8),
'mfv_neu_tau010000um_M0300_2017': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_181748", 5),
'mfv_neu_tau030000um_M0300_2017': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_181812", 9),
'mfv_neu_tau000100um_M0400_2017': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-100um_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_181837", 31),
'mfv_neu_tau001000um_M0400_2017': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_181901", 8),
'mfv_neu_tau010000um_M0400_2017': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_181926", 5),
'mfv_neu_tau030000um_M0400_2017': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_181949", 9),
'mfv_neu_tau000100um_M0600_2017': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-100um_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_182012", 32),
'mfv_neu_tau000300um_M0600_2017': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-300um_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_182036", 14),
'mfv_neu_tau001000um_M0600_2017': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_182100", 5),
'mfv_neu_tau010000um_M0600_2017': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_182123", 3),
'mfv_neu_tau030000um_M0600_2017': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_182146", 6),
'mfv_neu_tau000300um_M0800_2017': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-300um_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_182210", 14),
'mfv_neu_tau001000um_M0800_2017': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_182233", 4),
'mfv_neu_tau010000um_M0800_2017': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_182257", 3),
'mfv_neu_tau030000um_M0800_2017': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_182321", 4),
'mfv_neu_tau000100um_M1200_2017': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-100um_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_182343", 31),
'mfv_neu_tau000300um_M1200_2017': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-300um_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_182406", 11),
'mfv_neu_tau001000um_M1200_2017': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_182430", 4),
'mfv_neu_tau010000um_M1200_2017': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_182453", 2),
'mfv_neu_tau030000um_M1200_2017': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_182516", 3),
'mfv_neu_tau000100um_M1600_2017': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-100um_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_182541", 32),
'mfv_neu_tau000300um_M1600_2017': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-300um_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_182603", 11),
'mfv_neu_tau000100um_M3000_2017': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-100um_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_182738", 30),
'mfv_neu_tau000300um_M3000_2017': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-300um_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_182802", 11),
'mfv_stopdbardbar_tau000100um_M0200_2017': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-200_CTau-100um_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_182941", 31),
'mfv_stopdbardbar_tau000300um_M0200_2017': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-200_CTau-300um_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_183005", 30),
'mfv_stopdbardbar_tau001000um_M0200_2017': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-200_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_183029", 9),
'mfv_stopdbardbar_tau010000um_M0200_2017': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-200_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_183053", 5),
'mfv_stopdbardbar_tau030000um_M0200_2017': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-200_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_183116", 7),
'mfv_stopdbardbar_tau000100um_M0300_2017': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-300_CTau-100um_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_183141", 29),
'mfv_stopdbardbar_tau000300um_M0300_2017': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-300_CTau-300um_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_183204", 30),
'mfv_stopdbardbar_tau001000um_M0300_2017': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-300_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_183228", 9),
'mfv_stopdbardbar_tau010000um_M0300_2017': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-300_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_183252", 5),
'mfv_stopdbardbar_tau030000um_M0300_2017': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-300_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_183316", 7),
'mfv_stopdbardbar_tau000100um_M0400_2017': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-400_CTau-100um_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_183339", 31),
'mfv_stopdbardbar_tau000300um_M0400_2017': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-400_CTau-300um_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_183402", 31),
'mfv_stopdbardbar_tau001000um_M0400_2017': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-400_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_183425", 8),
'mfv_stopdbardbar_tau010000um_M0400_2017': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-400_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_183450", 5),
'mfv_stopdbardbar_tau030000um_M0400_2017': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-400_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_183513", 7),
'mfv_stopdbardbar_tau000100um_M0600_2017': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-600_CTau-100um_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_183538", 29),
'mfv_stopdbardbar_tau000300um_M0600_2017': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-600_CTau-300um_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_183614", 23),
'mfv_stopdbardbar_tau010000um_M0600_2017': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-600_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_183639", 3),
'mfv_stopdbardbar_tau030000um_M0600_2017': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-600_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_183703", 5),
'mfv_stopdbardbar_tau000100um_M0800_2017': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-800_CTau-100um_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_183727", 33),
'mfv_stopdbardbar_tau000300um_M0800_2017': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-800_CTau-300um_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_183752", 18),
'mfv_stopdbardbar_tau001000um_M0800_2017': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-800_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_183815", 5),
'mfv_stopdbardbar_tau010000um_M0800_2017': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-800_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_183838", 5),
'mfv_stopdbardbar_tau030000um_M0800_2017': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-800_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_183902", 5),
'mfv_stopdbardbar_tau000100um_M1200_2017': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-1200_CTau-100um_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_183925", 32),
'mfv_stopdbardbar_tau000300um_M1200_2017': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-1200_CTau-300um_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_183948", 17),
'mfv_stopdbardbar_tau000100um_M1600_2017': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-1600_CTau-100um_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_184122", 30),
'mfv_stopdbardbar_tau000100um_M3000_2017': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-3000_CTau-100um_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_184258", 30),
'mfv_stopbbarbbar_tau000100um_M0200_2017': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-200_CTau-100um_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_184458", 32),
'mfv_stopbbarbbar_tau000300um_M0200_2017': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-200_CTau-300um_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_184521", 31),
'mfv_stopbbarbbar_tau001000um_M0200_2017': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-200_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_184546", 8),
'mfv_stopbbarbbar_tau010000um_M0200_2017': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-200_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_184609", 5),
'mfv_stopbbarbbar_tau030000um_M0200_2017': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-200_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_184633", 8),
'mfv_stopbbarbbar_tau000100um_M0300_2017': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-300_CTau-100um_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_184656", 30),
'mfv_stopbbarbbar_tau000300um_M0300_2017': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-300_CTau-300um_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_184720", 32),
'mfv_stopbbarbbar_tau001000um_M0300_2017': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-300_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_184744", 11),
'mfv_stopbbarbbar_tau010000um_M0300_2017': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-300_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_184807", 5),
'mfv_stopbbarbbar_tau030000um_M0300_2017': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-300_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_184830", 7),
'mfv_stopbbarbbar_tau000100um_M0400_2017': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-400_CTau-100um_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_184853", 31),
'mfv_stopbbarbbar_tau000300um_M0400_2017': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-400_CTau-300um_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_184916", 32),
'mfv_stopbbarbbar_tau001000um_M0400_2017': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-400_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_184940", 8),
'mfv_stopbbarbbar_tau010000um_M0400_2017': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-400_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_185003", 5),
'mfv_stopbbarbbar_tau030000um_M0400_2017': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-400_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_185027", 7),
'mfv_stopbbarbbar_tau000100um_M0600_2017': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-600_CTau-100um_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_185050", 32),
'mfv_stopbbarbbar_tau000300um_M0600_2017': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-600_CTau-300um_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_185113", 24),
'mfv_stopbbarbbar_tau001000um_M0600_2017': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-600_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_185137", 7),
'mfv_stopbbarbbar_tau010000um_M0600_2017': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-600_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_185200", 3),
'mfv_stopbbarbbar_tau030000um_M0600_2017': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-600_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_185223", 6),
'mfv_stopbbarbbar_tau000100um_M0800_2017': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-800_CTau-100um_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_185246", 30),
'mfv_stopbbarbbar_tau000300um_M0800_2017': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-800_CTau-300um_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_185310", 19),
'mfv_stopbbarbbar_tau001000um_M0800_2017': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-800_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_185334", 7),
'mfv_stopbbarbbar_tau010000um_M0800_2017': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-800_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_185358", 3),
'mfv_stopbbarbbar_tau030000um_M0800_2017': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-800_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_185421", 5),
'mfv_stopbbarbbar_tau000100um_M1200_2017': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-1200_CTau-100um_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_185444", 31),
'mfv_stopbbarbbar_tau000300um_M1200_2017': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-1200_CTau-300um_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_185508", 16),
'mfv_stopbbarbbar_tau001000um_M1200_2017': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-1200_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_185531", 5),
'mfv_stopbbarbbar_tau010000um_M1200_2017': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-1200_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_185557", 3),
'mfv_stopbbarbbar_tau030000um_M1200_2017': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-1200_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_185621", 4),
'mfv_stopbbarbbar_tau000300um_M1600_2017': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-1600_CTau-300um_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_185644", 14),
'mfv_stopbbarbbar_tau000100um_M3000_2017': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-3000_CTau-100um_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_185818", 30),
'ggHToSSTodddd_tau1mm_M55_2017': _fromnum1("/store/user/lpclonglived/shogan/ggH_HToSSTodddd_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_190017", 77),
'ggHToSSTodddd_tau10mm_M55_2017': _fromnum1("/store/user/lpclonglived/shogan/ggH_HToSSTodddd_MH-125_MS-55_ctauS-10_TuneCP5_13TeV-powheg-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_190042", 74),
'ggHToSSTodddd_tau100mm_M55_2017': _fromnum1("/store/user/lpclonglived/shogan/ggH_HToSSTodddd_MH-125_MS-55_ctauS-100_TuneCP5_13TeV-powheg-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_190105", 78),
'mfv_stopdbardbar_tau010000um_M1200_2017': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-1200_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_184035", 3),
'mfv_stopbbarbbar_tau001000um_M1600_2017': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-1600_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_185708", 4),
'mfv_stopbbarbbar_tau030000um_M1600_2017': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-1600_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_185754", 4),
'mfv_stopbbarbbar_tau000300um_M3000_2017': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-3000_CTau-300um_TuneCP5_13TeV-pythia8/NtupleU17LV9_redo_Bm_NoEF_2017/231120_185841", 16),

# 2018 Signal Samples
'mfv_neu_tau000100um_M0200_2018': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-200_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_212903", 33),
'mfv_neu_tau000300um_M0200_2018': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-200_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_212926", 23),
'mfv_neu_tau010000um_M0200_2018': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-200_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_212949", 5),
'mfv_neu_tau030000um_M0200_2018': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-200_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_213055", 10),
'mfv_neu_tau001000um_M0300_2018': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_213207", 9),
'mfv_neu_tau030000um_M0300_2018': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_213253", 11),
'mfv_neu_tau001000um_M0400_2018': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_213402", 7),
'mfv_neu_tau030000um_M0400_2018': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_213448", 12),
'mfv_stopdbardbar_tau000100um_M0200_2018': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-200_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_214421", 29),
'mfv_stopdbardbar_tau000300um_M0200_2018': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-200_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_214443", 30),
'mfv_stopdbardbar_tau001000um_M0200_2018': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-200_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_214507", 8),
'mfv_stopdbardbar_tau010000um_M0200_2018': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-200_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_214530", 5),
'mfv_stopdbardbar_tau030000um_M0200_2018': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-200_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_214553", 7),
'mfv_stopdbardbar_tau000100um_M0300_2018': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-300_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_214616", 31),
'mfv_stopdbardbar_tau030000um_M0300_2018': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-300_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_214747", 7),
'mfv_stopdbardbar_tau001000um_M0400_2018': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-400_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_214857", 8),
'mfv_stopdbardbar_tau010000um_M0400_2018': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-400_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_214920", 9),
'mfv_stopdbardbar_tau030000um_M0400_2018': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-400_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_214944", 11),
'mfv_stopdbardbar_tau000100um_M0800_2018': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-800_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_215203", 30),
'mfv_stopbbarbbar_tau000100um_M0200_2018': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-200_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_215943", 31),
'mfv_stopbbarbbar_tau000300um_M0200_2018': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-200_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_220006", 31),
'mfv_stopbbarbbar_tau001000um_M0200_2018': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-200_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_220030", 8),
'mfv_stopbbarbbar_tau010000um_M0200_2018': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-200_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_220053", 5),
'mfv_stopbbarbbar_tau030000um_M0200_2018': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-200_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_220116", 7),
'mfv_stopbbarbbar_tau000100um_M0300_2018': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-300_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_220139", 31),
'mfv_stopbbarbbar_tau000300um_M0300_2018': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-300_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_220202", 29),
'mfv_stopbbarbbar_tau001000um_M0300_2018': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-300_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_220226", 9),
'mfv_stopbbarbbar_tau010000um_M0300_2018': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-300_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_220249", 7),
'mfv_stopbbarbbar_tau030000um_M0300_2018': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-300_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_220312", 7),
'mfv_stopbbarbbar_tau001000um_M0400_2018': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-400_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_220420", 9),
'mfv_stopbbarbbar_tau010000um_M0400_2018': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-400_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_220443", 5),
'mfv_stopbbarbbar_tau030000um_M0400_2018': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-400_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_220506", 7),
'mfv_stopbbarbbar_tau000100um_M1600_2018': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-1600_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_221048", 29),

'mfv_neu_tau000100um_M0300_2018': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_213121", 32),
'mfv_neu_tau000300um_M0300_2018': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_213143", 24),
'mfv_neu_tau010000um_M0300_2018': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_213230", 5),
'mfv_neu_tau000100um_M0400_2018': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_213316", 29),
'mfv_neu_tau010000um_M0400_2018': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_213424", 6),
'mfv_neu_tau000100um_M0600_2018': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_213511", 29),
'mfv_neu_tau001000um_M0600_2018': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_213533", 4),
'mfv_neu_tau010000um_M0600_2018': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_213557", 4),
'mfv_neu_tau030000um_M0600_2018': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_213619", 5),
'mfv_neu_tau000100um_M0800_2018': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_213641", 31),
'mfv_neu_tau000300um_M0800_2018': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_213705", 13),
'mfv_neu_tau001000um_M0800_2018': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_213727", 4),
'mfv_neu_tau010000um_M0800_2018': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_213750", 2),
'mfv_neu_tau030000um_M0800_2018': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_213814", 4),
'mfv_neu_tau000100um_M1200_2018': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_213837", 32),
'mfv_neu_tau001000um_M1200_2018': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_213924", 4),
'mfv_neu_tau010000um_M1200_2018': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_213947", 3),
'mfv_neu_tau030000um_M1200_2018': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_214009", 5),
'mfv_neu_tau000100um_M1600_2018': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_214033", 30),
'mfv_neu_tau001000um_M1600_2018': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_214118", 5),
'mfv_neu_tau010000um_M1600_2018': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_214142", 3),
'mfv_neu_tau030000um_M1600_2018': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_214204", 4),
'mfv_neu_tau000300um_M3000_2018': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_214250", 9),
'mfv_stopdbardbar_tau000300um_M0300_2018': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-300_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_214639", 30),
'mfv_stopdbardbar_tau001000um_M0300_2018': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-300_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_214701", 8),
'mfv_stopdbardbar_tau010000um_M0300_2018': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-300_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_214725", 5),
'mfv_stopdbardbar_tau000100um_M0400_2018': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-400_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_214810", 36),
'mfv_stopdbardbar_tau000300um_M0400_2018': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-400_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_214835", 36),
'mfv_stopdbardbar_tau000100um_M0600_2018': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-600_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_215008", 37),
'mfv_stopdbardbar_tau000300um_M0600_2018': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-600_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_215031", 27),
'mfv_stopdbardbar_tau001000um_M0600_2018': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-600_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_215054", 7),
'mfv_stopdbardbar_tau010000um_M0600_2018': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-600_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_215117", 3),
'mfv_stopdbardbar_tau030000um_M0600_2018': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-600_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_215139", 6),
'mfv_stopdbardbar_tau000300um_M0800_2018': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-800_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_215225", 17),
'mfv_stopdbardbar_tau001000um_M0800_2018': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-800_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_215248", 8),
'mfv_stopdbardbar_tau010000um_M0800_2018': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-800_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_215311", 6),
'mfv_stopdbardbar_tau030000um_M0800_2018': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-800_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_215334", 4),
'mfv_stopdbardbar_tau000100um_M1200_2018': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-1200_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_215356", 31),
'mfv_stopdbardbar_tau000300um_M1200_2018': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-1200_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_215419", 15),
'mfv_stopdbardbar_tau001000um_M1200_2018': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-1200_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_215442", 6),
'mfv_stopdbardbar_tau010000um_M1200_2018': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-1200_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_215506", 3),
'mfv_stopdbardbar_tau030000um_M1200_2018': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-1200_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_215530", 4),
'mfv_stopdbardbar_tau000100um_M1600_2018': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-1600_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_215553", 30),
'mfv_stopdbardbar_tau000300um_M1600_2018': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-1600_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_215615", 14),
'mfv_stopdbardbar_tau001000um_M1600_2018': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-1600_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_215639", 9),
'mfv_stopdbardbar_tau030000um_M1600_2018': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-1600_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_215724", 4),
'mfv_stopdbardbar_tau000100um_M3000_2018': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-3000_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_215747", 29),
'mfv_stopbbarbbar_tau000100um_M0400_2018': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-400_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_220335", 31),
'mfv_stopbbarbbar_tau000300um_M0400_2018': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-400_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_220357", 28),
'mfv_stopbbarbbar_tau001000um_M0600_2018': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-600_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_220614", 6),
'mfv_stopbbarbbar_tau010000um_M0600_2018': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-600_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_220636", 4),
'mfv_stopbbarbbar_tau030000um_M0600_2018': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-600_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_220659", 5),
'mfv_stopbbarbbar_tau000100um_M0800_2018': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-800_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_220722", 32),
'mfv_stopbbarbbar_tau000300um_M0800_2018': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-800_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_220744", 20),
'mfv_stopbbarbbar_tau010000um_M0800_2018': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-800_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_220808", 3),
'mfv_stopbbarbbar_tau000100um_M1200_2018': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-1200_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_220853", 28),
'mfv_stopbbarbbar_tau010000um_M1200_2018': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-1200_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_221002", 4),
'mfv_stopbbarbbar_tau030000um_M1200_2018': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-1200_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_221025", 5),
'mfv_stopbbarbbar_tau000300um_M1600_2018': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-1600_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_221110", 13),
'mfv_stopbbarbbar_tau010000um_M1600_2018': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-1600_CTau-10mm_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_221156", 3),
'mfv_stopbbarbbar_tau030000um_M1600_2018': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-1600_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_221218", 4),
'ggHToSSTodddd_tau1mm_M55_2018': _fromnum1("/store/user/lpclonglived/shogan/ggH_HToSSTodddd_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_221435", 86),
'ggHToSSTodddd_tau10mm_M55_2018': _fromnum1("/store/user/lpclonglived/shogan/ggH_HToSSTodddd_MH-125_MS-55_ctauS-10_TuneCP5_13TeV-powheg-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_221500", 84),

'mfv_neu_tau000300um_M0400_2018': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_213339", 25),
'mfv_neu_tau000300um_M1200_2018': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_213901", 11),
'mfv_neu_tau000300um_M1600_2018': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_214055", 11),
'mfv_neu_tau000100um_M3000_2018': _fromnum1("/store/user/lpclonglived/shogan/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_214227", 29),
'mfv_stopdbardbar_tau000300um_M3000_2018': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Dbar2D_M-3000_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_215810", 20),
'mfv_stopbbarbbar_tau000100um_M0600_2018': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-600_CTau-100um_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_220528", 30),
'mfv_stopbbarbbar_tau000300um_M0600_2018': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-600_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_220551", 24),
'mfv_stopbbarbbar_tau030000um_M0800_2018': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-800_CTau-30mm_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_220831", 5),
'mfv_stopbbarbbar_tau000300um_M1200_2018': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-1200_CTau-300um_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_220917", 18),
'mfv_stopbbarbbar_tau001000um_M1200_2018': _fromnum1("/store/user/lpclonglived/shogan/StopStopbarTo2Bbar2B_M-1200_CTau-1mm_TuneCP5_13TeV-pythia8/NtupleUL18V9Bm_NoEF_2018/240119_220939", 7),


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
