import os, base64, zlib, cPickle as pickle
from collections import defaultdict
from itertools import chain
from pprint import pprint
from JMTucker.Tools.CRAB3ToolsBase import decrabify_list

_d = {}

def _enc(d):
    return base64.b64encode(zlib.compress(pickle.dumps(d)))

def _denc(encd):
    return pickle.loads(zlib.decompress(base64.b64decode(encd)))

def _add(d, allow_overwrite=False):
    global _d
    if type(d) == str:
        d = _denc(d)
    if not allow_overwrite:
        for k in d:
            if _d.has_key(k):
                raise ValueError('already have key %s' % repr(k))
            assert len(d[k][1]) == d[k][0]
    _d.update(d)

def _add_ds(ds, d, allow_overwrite=False):
    d2 = {}
    for k in d:
        d2[(k,ds)] = d[k]
    _add(d2, allow_overwrite)

def _fromnumlist(path, numlist, but=[], fnbase='ntuple', add=[], numbereddirs=True):
    return add + [path + ('/%04i' % (i/1000) if numbereddirs else '') + '/%s_%i.root' % (fnbase, i) for i in numlist if i not in but]

def _fromnum1(path, n, but=[], fnbase='ntuple', add=[], numbereddirs=True): # crab starts job numbering at 1
    l = _fromnumlist(path, xrange(1,n+1), but, fnbase, add, numbereddirs)
    return (len(l), l)

def _fromnum0(path, n, but=[], fnbase='ntuple', add=[], numbereddirs=True): # condorsubmitter starts at 0
    l = _fromnumlist(path, xrange(n), but, fnbase, add, numbereddirs)
    return (len(l), l)

def dump():
    pprint(_d)

def summary():
    d = defaultdict(list)
    for k in _d.iterkeys():
        a,b = k
        d[a].append((b, _d[k][0]))
    for a in sorted(d.keys()):
        for b,n in d[a]:
            print a.ljust(40), b.ljust(20), '%5i' % n

def get(name, ds):
    return _d.get((name, ds), None)

def set_process(process, name, ds, num=-1):
    fns = get(name, ds)[1]
    if num > 0:
        fns = fns[:num]
    process.source.fileNames = fns

################################################################################

_add({('testqcdht2000', 'gensim') : (60 + 263,
                                     ['/store/user/tucker/qcdht2000_gensim/RunIISummer15GS-MCRUN2_71_V1/170224_171809/0000/gensim_%i.root' % i for i in chain(xrange(1,5), xrange(6,8), xrange(11,16), xrange(17,40), xrange(41,67))] +
                                     ['/store/user/tucker/qcdht2000_gensim_ext1/RunIISummer15GS-MCRUN2_71_V1/170224_210305/0000/gensim_%i.root' % i for i in chain(xrange(1,255), xrange(256,265))]
                                     )})

_add_ds('main', {
'testqcdht2000':      _fromnum0('/store/user/tucker/qcdht2000_80',      323, fnbase='reco', numbereddirs=False),
'testqcdht2000_noPU': _fromnum0('/store/user/tucker/qcdht2000_80_noPU', 323, fnbase='reco', numbereddirs=False),
})

_add_ds('ntuplev10', {

'qcdht0500':    _fromnum1('/store/user/tucker/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NtupleV10/170129_025922',    762, but=[16, 37]),
'qcdht0700':    _fromnum1('/store/user/tucker/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NtupleV10/170129_025950',   628),
'qcdht1000':    _fromnum1('/store/user/tucker/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NtupleV10/170129_030019',  195),
'qcdht1500':    _fromnum1('/store/user/tucker/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NtupleV10/170129_030045',  160, but=[2,4,13,19,20,22,24,71,73,78,79]),
'qcdht2000':    _fromnum1('/store/user/tucker/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NtupleV10/170129_030115',    80),
'qcdht0500ext': _fromnum1('/store/user/tucker/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NtupleV10/170129_030402',   1770),
'qcdht0700ext': _fromnum1('/store/user/tucker/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NtupleV10/170129_030430',  1198),
'qcdht1000ext': _fromnum1('/store/user/tucker/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NtupleV10/170129_030458',  417),
'qcdht1500ext': _fromnum1('/store/user/tucker/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NtupleV10/170129_030525',  316, but=[13]),
'qcdht2000ext': _fromnum1('/store/user/tucker/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NtupleV10/170129_030553',   163),

'official_mfv_neu_tau00100um_M0300': _fromnum1('/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-100um_TuneCUETP8M1_13TeV-pythia8/NtupleV10/170127_024549',  5),
'official_mfv_neu_tau00300um_M0300': _fromnum1('/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-300um_TuneCUETP8M1_13TeV-pythia8/NtupleV10/170127_024617',  5),
'official_mfv_neu_tau10000um_M0300': _fromnum1('/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-10mm_TuneCUETP8M1_13TeV-pythia8/NtupleV10/170127_024651',   5),
'official_mfv_neu_tau00100um_M0400': _fromnum1('/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-100um_TuneCUETP8M1_13TeV-pythia8/NtupleV10/170127_024721',  5),
'official_mfv_neu_tau01000um_M0400': _fromnum1('/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-1mm_TuneCUETP8M1_13TeV-pythia8/NtupleV10/170127_024752',    5),
'official_mfv_neu_tau10000um_M0400': _fromnum1('/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-10mm_TuneCUETP8M1_13TeV-pythia8/NtupleV10/170127_024821',   4),
'official_mfv_neu_tau00100um_M0800': _fromnum1('/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-100um_TuneCUETP8M1_13TeV-pythia8/NtupleV10/170127_024850',  4),
'official_mfv_neu_tau10000um_M0800': _fromnum1('/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-10mm_TuneCUETP8M1_13TeV-pythia8/NtupleV10/170127_024949',   5),
'official_mfv_neu_tau00300um_M1200': _fromnum1('/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-300um_TuneCUETP8M1_13TeV-pythia8/NtupleV10/170127_025019', 5),
'official_mfv_neu_tau01000um_M1200': _fromnum1('/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-1mm_TuneCUETP8M1_13TeV-pythia8/NtupleV10/170127_025049',   5),
'official_mfv_neu_tau00100um_M1600': _fromnum1('/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-100um_TuneCUETP8M1_13TeV-pythia8/NtupleV10/170127_025119', 5),
'official_mfv_neu_tau00300um_M1600': _fromnum1('/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-300um_TuneCUETP8M1_13TeV-pythia8/NtupleV10/170127_025148', 5),

'JetHT2016B3': _fromnum1('/store/user/tucker/JetHT/NtupleV10/170124_035716', 1758),
'JetHT2016C' : _fromnum1('/store/user/tucker/JetHT/NtupleV10/170124_035750', 580), 
'JetHT2016D' : _fromnum1('/store/user/tucker/JetHT/NtupleV10/170124_035827', 972, but=[64]),
'JetHT2016E' : _fromnum1('/store/user/tucker/JetHT/NtupleV10/170124_035858', 826, but=[335]),
'JetHT2016F' : _fromnum1('/store/user/tucker/JetHT/NtupleV10/170124_035931', 603),
'JetHT2016G' : _fromnum1('/store/user/tucker/JetHT/NtupleV10/170124_025401', 1423, but=[790,1063,1267,1298,1339]),
'JetHT2016H2': _fromnum1('/store/user/tucker/JetHT/NtupleV10/170128_191149', 1541),
'JetHT2016H3': _fromnum1('/store/user/tucker/JetHT/NtupleV10/170128_191217', 41),
})

_add_ds('ntuplev11', {

'official_mfv_neu_tau00100um_M0800': _fromnum0('/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-100um_TuneCUETP8M1_13TeV-pythia8/NtupleV11_2016/170216_225918', 2),
'official_mfv_neu_tau00300um_M0800': _fromnum1('/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-300um_TuneCUETP8M1_13TeV-pythia8/NtupleV11_2016/170217_045836', 5),
'official_mfv_neu_tau10000um_M0800': _fromnum1('/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-10mm_TuneCUETP8M1_13TeV-pythia8/NtupleV11_2016/170217_050124', 5),

'qcdht0500': _fromnum0('/store/user/tucker/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NtupleV11_2016_qcdht0500/170217_151519', 115),
'qcdht0700' : (1845, 
               ['/store/user/tucker/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NtupleV11_2016_qcdht0700/170222_134631/0000/ntuple_%i.root' % i for i in [1241, 1255]] +
               ['/store/user/tucker/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NtupleV11_2016_qcdht0700/170220_124629/0000/ntuple_%i.root' % i for i in chain(xrange(74), xrange(75,129), xrange(130,164), xrange(165,170), xrange(171,257), xrange(258,297), xrange(298,304), xrange(305,353), xrange(356,392), xrange(393,408), xrange(409,480), xrange(481,494), xrange(495,544), xrange(545,553), xrange(555,608), xrange(609,616), xrange(617,631), xrange(632,634), xrange(635,706), xrange(707,711), xrange(712,742), xrange(743,770), xrange(771,835), xrange(836,852), xrange(854,859), xrange(860,871), xrange(874,914), xrange(915,925), xrange(928,933), xrange(934,967), xrange(968,977), xrange(978,993), xrange(995,1001), xrange(1002,1029), xrange(1030,1041), xrange(1042,1046), xrange(1047,1053), xrange(1056,1075), xrange(1076,1078), xrange(1079,1086), xrange(1087,1094), xrange(1095,1098), xrange(1099,1116), xrange(1117,1123), xrange(1124,1154), xrange(1155,1173), xrange(1174,1194), xrange(1195,1200), xrange(1201,1213), xrange(1214,1223), xrange(1224,1241), xrange(1242,1244), xrange(1246,1255), xrange(1257,1267), xrange(1268,1280), xrange(1281,1315), xrange(1316,1337), xrange(1338,1347), xrange(1348,1376), xrange(1377,1382), xrange(1383,1386), xrange(1387,1401), xrange(1402,1404), xrange(1405,1413), xrange(1414,1420), xrange(1423,1431), xrange(1434,1446), xrange(1447,1452), xrange(1457,1464), xrange(1466,1471), xrange(1472,1479), xrange(1480,1490), xrange(1491,1497), xrange(1498,1525), xrange(1527,1532), xrange(1533,1583), xrange(1584,1588), xrange(1589,1684), xrange(1685,1696), xrange(1697,1711), xrange(1712,1731), xrange(1732,1739), xrange(1740,1763), xrange(1764,1781), xrange(1783,1792), xrange(1793,1845), [354, 872, 926, 1054, 1421, 1432, 1453, 1455])] +
               ['/store/user/tucker/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NtupleV11_2016_qcdht0700/170221_145150/0000/ntuple_%i.root' % i for i in chain(xrange(553,555), xrange(852,854), xrange(993,995), xrange(1244,1246), xrange(1464,1466), xrange(1525,1527), xrange(1781,1783), [74, 129, 164, 170, 257, 297, 304, 353, 355, 392, 408, 480, 494, 544, 608, 616, 631, 634, 706, 711, 742, 770, 835, 859, 871, 873, 914, 925, 927, 933, 967, 977, 1001, 1029, 1041, 1046, 1053, 1055, 1075, 1078, 1086, 1094, 1098, 1116, 1123, 1154, 1173, 1194, 1200, 1213, 1223, 1256, 1267, 1280, 1315, 1337, 1347, 1376, 1382, 1386, 1401, 1404, 1413, 1420, 1422, 1431, 1433, 1446, 1452, 1454, 1456, 1471, 1479, 1490, 1497, 1532, 1583, 1588, 1684, 1696, 1711, 1731, 1739, 1763, 1792])]
               ),
'qcdht1000': _fromnum1('/store/user/tucker/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NtupleV11_2016/170217_045658', 195),
'qcdht1500': _fromnum0('/store/user/tucker/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NtupleV11_2016_qcdht1500/170217_151519', 34),
'qcdht2000': _fromnum1('/store/user/tucker/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NtupleV11_2016/170217_045736', 80),

'qcdht0500ext': _fromnum0('/store/user/tucker/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NtupleV11_2016_qcdht0500ext/170217_151519', 269),
'qcdht0700ext': _fromnum0('/store/user/tucker/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NtupleV11_2016_qcdht0700ext/170217_151519', 176),
'qcdht1000ext': _fromnum0('/store/user/tucker/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NtupleV11_2016_qcdht1000ext/170217_151519', 73),
'qcdht1500ext': _fromnum0('/store/user/tucker/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NtupleV11_2016_qcdht1500ext/170217_151519', 64),
'qcdht2000ext': _fromnum1('/store/user/tucker/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NtupleV11_2016/170217_045806', 163),

'ttbar': (1253, ['/store/user/tucker/TTJets_TuneCUETP8M2T4_13TeV-amcatnloFXFX-pythia8/NtupleV11_2016/170222_220951' + '/%04i/ntuple_%i.root' % (i/1000,i) for i in chain(xrange(1,389), xrange(390,421), xrange(422,587), xrange(588,760), xrange(761,768), xrange(769,1259))]),

'JetHT2016B3': (1752 + 93,
                ['/store/user/tucker/JetHT/NtupleV11_2016/170218_180953' + '/%04i/ntuple_%i.root' % (i/1000,i) for i in chain(xrange(1,280), xrange(281,585), xrange(586,628), xrange(629,1473), xrange(1474,1525), xrange(1526,1724), xrange(1725,1759))] +
                ['/store/user/tucker/JetHT/NtupleV11_2016/170222_205536/0000/ntuple_%i.root' % i for i in xrange(1,94)]
                ),
'JetHT2016C':  (580, ['/store/user/tucker/JetHT/NtupleV11_2016/170217_044934/0000/ntuple_%i.root' % i for i in xrange(1,581)]),
'JetHT2016D':  (969 + 37,
                ['/store/user/tucker/JetHT/NtupleV11_2016/170217_045150/0000/ntuple_%i.root' % i for i in chain(xrange(1,54), xrange(56,64), xrange(65,973))] +
                ['/store/user/tucker/JetHT/NtupleV11_2016/170222_205605/0000/ntuple_%i.root' % i for i in chain(xrange(1,14), xrange(19,38), xrange(41,46))]
                ),
'JetHT2016E':  (826, ['/store/user/tucker/JetHT/NtupleV11_2016/170217_045229/0000/ntuple_%i.root' % i for i in xrange(1,827)]),
'JetHT2016F':  (603, ['/store/user/tucker/JetHT/NtupleV11_2016/170217_045346/0000/ntuple_%i.root' % i for i in xrange(1,604)]),
'JetHT2016G':  (1419 + 85,
                ['/store/user/tucker/JetHT/NtupleV11_2016/170218_181024' + '/%04i/ntuple_%i.root' % (i/1000,i) for i in chain(xrange(1,696), xrange(697,857), xrange(858,1149), xrange(1150,1300), xrange(1301,1424))] +
                ['/store/user/tucker/JetHT/NtupleV11_2016/170222_205637/0000/ntuple_%i.root' % i for i in xrange(1,86)]
                ),
'JetHT2016H2': (1533 + 120,
                ['/store/user/tucker/JetHT/NtupleV11_2016/170217_045421' + '/%04i/ntuple_%i.root' % (i/1000,i) for i in chain(xrange(1,659), [660], xrange(662,908), xrange(910,976), xrange(977,1062), xrange(1063,1065), xrange(1066,1405), xrange(1406,1542))] +
                ['/store/user/tucker/JetHT/NtupleV11_2016/170222_205707/0000/ntuple_%i.root' % i for i in xrange(1,121)]
                ),
'JetHT2016H3': (41 , ['/store/user/tucker/JetHT/NtupleV11_2016/170217_045451/0000/ntuple_%i.root' % i for i in xrange(1,42)]),

})

if 0:
    _add({
            ('official_mfv_neu_tau10000um_M0800', 'miniaod'): (16, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-10mm_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv2_PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/' + x for x in [
                    '08FBE8E9-BEDC-E611-AA3F-0025901AC3EE.root',
                    'FAC3790B-52DC-E611-BB40-001E67E5A39A.root',
                    'F08DE058-BFDC-E611-812C-008CFA11134C.root',
                    '0A708315-82DC-E611-9BB8-D067E5F914D3.root',
                    'A04BA2B6-BEDC-E611-909B-0090FAA57FC4.root',
                    'CA2D8F12-7EDC-E611-99F4-A4BF01013D80.root',
                    'DA564E95-80DC-E611-999A-0025905B85DA.root',
                    'E4C81247-C0DC-E611-927C-0025905B85FE.root',
                    'DE7ADA27-80DC-E611-90B1-0CC47AD98C8C.root',
                    '02A485AE-6FDC-E611-8432-24BE05CEFB41.root',
                    '185994B2-BEDC-E611-83B7-5065F3819241.root',
                    '200E5FD6-4FDC-E611-8FC2-0025901FB438.root',
                    '02EA9183-C0DC-E611-A512-02163E0140E6.root',
                    '3C1F7655-50DC-E611-AFFC-001E67586A2F.root',
                    '84A0F5B5-51DC-E611-A4DF-0025905A6118.root',
                    'DC37A0A8-51DC-E611-A4A4-0CC47A78A456.root'
                    ]])})

_add({('JetHT2016H2', 'fortest'): (1, ['/store/user/tucker/JetHT2016H2.8AAACEA3-B786-E611-953E-02163E013547.root'])})
_add({('JetHT2016H2', 'miniaodskimtestv1'): (24, ['/store/user/tucker/JetHT/MiniAODSkimTestv1/170209_105600/0000/miniaod_%i.root' % i for i in xrange(24)])})

_add({('JetHT2016H2', 'miniaodfortest'): (1, ['/store/user/tucker/JetHT2016H2.MiniAOD.9C0A2FFD-B886-E611-BEA7-02163E011B30.root'])})
_add({('JetHT2016H2', 'ntuplev10fromminiaodtestv2'): (33, ['/store/user/tucker/JetHT/NtupleV10FromMiniAODTestv2/170209_171229/0000/ntuple_%i.root' % i for i in xrange(33)])})
_add({('JetHT2016H2', 'ntuplev10correspondingsubset'): (4, ['/store/user/tucker/JetHT/NtupleV10/170128_191149/0000/ntuple_%i.root' % i for i in [45,46,47,49]])})

_add({('official_mfv_neu_tau10000um_M0800', 'ntuplev10fromminiaodtestv2'): (16, ['/store/user/tucker/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-10mm_TuneCUETP8M1_13TeV-pythia8/NtupleV10FromMiniAODTestv2_signal/170210_135908/0000/ntuple_%i.root' % i for i in xrange(16)])})

__all__ = [
    'dump',
    'get',
    'summary',
    ]

if __name__ == '__main__':
    import sys
    if 'enc' in sys.argv:
        sample = sys.argv[sys.argv.index('enc')+1]
        dataset = sys.argv[sys.argv.index('enc')+2]
        listfn = sys.argv[sys.argv.index('enc')+3]
        fns = [x.strip() for x in open(listfn).read().split('\n') if x.strip()]
        n = len(fns)
        print '# %s, %s, %i files' % (sample, dataset, n)
        print '_add(%r)' % _enc({(sample,dataset):(n,fns)})
    elif 'testfiles' in sys.argv:
        sample = sys.argv[sys.argv.index('testfiles')+1]
        dataset = sys.argv[sys.argv.index('testfiles')+2]
        from JMTucker.Tools.ROOTTools import ROOT
        print sample, dataset
        def n(f,p):
            try:
                n = f.Get(p).GetEntries()
            except ReferenceError:
                pass
        for fn in get(sample, dataset)[1]:
            n(ROOT.TFile.Open('root://cmseos.fnal.gov/' + fn), 'Events')
            if dataset.startswith('ntuple'):
                n(ROOT.TFile.Open('root://cmseos.fnal.gov/' + fn.replace('ntuple', 'vertex_histos')), 'mfvVertices/h_n_all_tracks')
    else:
        summary()
