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

def _fromnumlist(path, numlist, but=[], fnbase='ntuple', add=[]):
    return add + [path + '/%04i/%s_%i.root' % (i/1000, fnbase, i) for i in numlist if i not in but]

def _fromnum1(path, n, but=[], fnbase='ntuple', add=[]): # crab starts job numbering at 1
    l = _fromnumlist(path, xrange(1,n+1), but, fnbase, add)
    return (len(l), l)

def _fromnum0(path, n, but=[], fnbase='ntuple', add=[]): # condorsubmitter starts at 0
    l = _fromnumlist(path, xrange(n), but, fnbase, add)
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

_add_ds('main', {
'testqcdht2000':      (85, ['/store/user/tucker/qcdht2000_80/reco_%i.root'      % i for i in xrange(91) if i not in [5,19,74,77,84,85]]),
'testqcdht2000_noPU': (85, ['/store/user/tucker/qcdht2000_80_noPU/reco_%i.root' % i for i in xrange(91) if i not in [5,19,74,77,84,85]]),
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

'qcdht1000': _fromnum1('/store/user/tucker/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NtupleV11_2016/170217_045658', 195),
'qcdht1500': _fromnum0('/store/user/tucker/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NtupleV11_2016_qcdht1500/170217_151519', 34),
'qcdht2000': _fromnum1('/store/user/tucker/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NtupleV11_2016/170217_045736', 80),

'qcdht0500ext': _fromnum0('/store/user/tucker/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NtupleV11_2016_qcdht0500ext/170217_151519', 269),
'qcdht0700ext': _fromnum0('/store/user/tucker/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NtupleV11_2016_qcdht0700ext/170217_151519', 176),
'qcdht1000ext': _fromnum0('/store/user/tucker/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NtupleV11_2016_qcdht1000ext/170217_151519', 73),
'qcdht1500ext': _fromnum0('/store/user/tucker/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NtupleV11_2016_qcdht1500ext/170217_151519', 64),
'qcdht2000ext': _fromnum1('/store/user/tucker/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NtupleV11_2016/170217_045806', 163),

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
