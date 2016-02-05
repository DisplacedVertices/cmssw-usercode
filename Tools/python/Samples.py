#!/usr/bin/env python

from functools import partial
from JMTucker.Tools.Sample import *

########################################################################

qcd_samples_not_used = [
    MCSample('qcdht0100', '/QCD_HT100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/AODSIM',   81719052, nice='QCD, 100 < H_{T} < 200 GeV',   color=801, syst_frac=0.20, xsec=2.785e7),
    MCSample('qcdht0200', '/QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/AODSIM',   18718905, nice='QCD, 200 < H_{T} < 300 GeV',   color=802, syst_frac=0.20, xsec=1.717e6),
    MCSample('qcdht0300', '/QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/AODSIM',   20278243, nice='QCD, 300 < H_{T} < 500 GeV',   color=803, syst_frac=0.20, xsec=3.513e5),
    ]

qcd_samples = [
    MCSample('qcdht0500', '/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',  19701790, nice='QCD, 500 < H_{T} < 700 GeV',   color=804, syst_frac=0.20, xsec=3.163e4),
    MCSample('qcdht0700', '/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/',                                                                           -1, nice='QCD, 700 < H_{T} < 1000 GeV',  color=805, syst_frac=0.20, xsec=6.802e3),
    MCSample('qcdht1000', '/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM', 5085104, nice='QCD, 1000 < H_{T} < 1500 GeV', color=806, syst_frac=0.20, xsec=1.206e3),
    MCSample('qcdht1500', '/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM', 3952170, nice='QCD, 1500 < H_{T} < 2000 GeV', color=807, syst_frac=0.20, xsec=120),
    MCSample('qcdht2000', '/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',  1981228, nice='QCD, H_{T} > 2000',            color=808, syst_frac=0.20, xsec=25.3),
    ]

ttbar_samples = [
    MCSample('ttbar', '/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM', 38493485, nice='t#bar{t}', color=4, syst_frac=0.15, xsec=832.),
    ]

leptonic_background_samples = [
    MCSample('wjetstolnu',     '/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/AODSIM',          24184766, nice='W + jets #rightarrow l#nu',                  color=  9, syst_frac=0.10, xsec=6.153e4), 
    MCSample('dyjetstollM10',  '/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/AODSIM', 30663441, nice='DY + jets #rightarrow ll, 10 < M < 50 GeV',  color= 29, syst_frac=0.10, xsec=1.861e4),
    MCSample('dyjetstollM50',  '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v3/AODSIM',     28827486, nice='DY + jets #rightarrow ll, M > 50 GeV',       color= 32, syst_frac=0.10, xsec=6.025e3),
    MCSample('qcdmupt15',      '/QCD_Pt-20toInf_MuEnrichedPt15_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/AODSIM',    13247363, nice='QCD, #hat{p}_{T} > 20 GeV, #mu p_{T} > 15 GeV', color=801, syst_frac=0.20, xsec=7.21e8 * 4.2e-4),
    ]

mfv_signal_samples = [
    MCSample('mfv_neu_tau00100um_M0400', '/mfv_neu_tau00100um_M0400/tucker-reco25ns_10k-affbb539eabf650318e2abc876f6a96a/USER', 10000),
    MCSample('mfv_neu_tau00100um_M0800', '/mfv_neu_tau00100um_M0800/tucker-reco25ns_10k-affbb539eabf650318e2abc876f6a96a/USER', 10000),
    MCSample('mfv_neu_tau00100um_M1200', '/mfv_neu_tau00100um_M1200/tucker-reco25ns_10k-affbb539eabf650318e2abc876f6a96a/USER',  9800),
    MCSample('mfv_neu_tau00100um_M1600', '/mfv_neu_tau00100um_M1600/tucker-reco25ns_10k-affbb539eabf650318e2abc876f6a96a/USER', 10000),
    MCSample('mfv_neu_tau00300um_M0400', '/mfv_neu_tau00300um_M0400/tucker-reco25ns_10k-affbb539eabf650318e2abc876f6a96a/USER', 10000),
    MCSample('mfv_neu_tau00300um_M0800', '/mfv_neu_tau00300um_M0800/tucker-reco25ns_10k-affbb539eabf650318e2abc876f6a96a/USER', 10000),
    MCSample('mfv_neu_tau00300um_M1200', '/mfv_neu_tau00300um_M1200/tucker-reco25ns_10k-affbb539eabf650318e2abc876f6a96a/USER', 10000),
    MCSample('mfv_neu_tau00300um_M1600', '/mfv_neu_tau00300um_M1600/tucker-reco25ns_10k-affbb539eabf650318e2abc876f6a96a/USER',  9400),
    MCSample('mfv_neu_tau01000um_M0400', '/mfv_neu_tau01000um_M0400/tucker-reco25ns_10k-affbb539eabf650318e2abc876f6a96a/USER',  9800),
    MCSample('mfv_neu_tau01000um_M0800', '/mfv_neu_tau01000um_M0800/tucker-reco25ns_10k-affbb539eabf650318e2abc876f6a96a/USER', 10000),
    MCSample('mfv_neu_tau01000um_M1200', '/mfv_neu_tau01000um_M1200/tucker-reco25ns_10k-affbb539eabf650318e2abc876f6a96a/USER', 10000),
    MCSample('mfv_neu_tau01000um_M1600', '/mfv_neu_tau01000um_M1600/tucker-reco25ns_10k-affbb539eabf650318e2abc876f6a96a/USER', 10000),
    MCSample('mfv_neu_tau10000um_M0400', '/mfv_neu_tau10000um_M0400/tucker-reco25ns_10k-affbb539eabf650318e2abc876f6a96a/USER',  9600),
    MCSample('mfv_neu_tau10000um_M0800', '/mfv_neu_tau10000um_M0800/tucker-reco25ns_10k-affbb539eabf650318e2abc876f6a96a/USER', 10000),
    MCSample('mfv_neu_tau10000um_M1200', '/mfv_neu_tau10000um_M1200/tucker-reco25ns_10k-affbb539eabf650318e2abc876f6a96a/USER',  9600),
    MCSample('mfv_neu_tau10000um_M1600', '/mfv_neu_tau10000um_M1600/tucker-reco25ns_10k-affbb539eabf650318e2abc876f6a96a/USER',  9600),
    ]

for s in mfv_signal_samples:
    s.dbs_inst = 'phys03'
    s.xsec = 1e-3
    s.aaa = us_aaa

xx4j_samples = [
    MCSample('xx4j_tau01000um_M0700', '/XXTo4J_M-700_CTau-1mm_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/AODSIM', 10000),
    MCSample('xx4j_tau10000um_M0700', '/XXTo4J_M-700_CTau-10mm_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/AODSIM', 10000),
    ]

for s in xx4j_samples:
    s.xsec = 1e-3

auxiliary_background_samples = [
    MCSample('ttbaraux',  '/TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/AODSIM', 11344206, nice='t#bar{t}', color=4, syst_frac=0.15, xsec=832.),
    MCSample('qcdpt0005', '/QCD_Pt_5to10_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',      6991536, nice='QCD, 5 < #hat{p}_{T} < 10 GeV',      color=808, syst_frac=0.10, xsec=6.10183e+10),
    MCSample('qcdpt0010', '/QCD_Pt_10to15_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v2/AODSIM',     6842800, nice='QCD, 10 < #hat{p}_{T} < 15 GeV',     color=808, syst_frac=0.10, xsec=5.88758e+09),
    MCSample('qcdpt0015', '/QCD_Pt_15to30_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',    38425945, nice='QCD, 15 < #hat{p}_{T} < 30 GeV',     color=808, syst_frac=0.10, xsec=1.83741e+09),
    MCSample('qcdpt0030', '/QCD_Pt_30to50_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',     9808025, nice='QCD, 30 < #hat{p}_{T} < 50 GeV',     color=808, syst_frac=0.10, xsec=1.40932e+08),
    MCSample('qcdpt0050', '/QCD_Pt_50to80_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',     9775360, nice='QCD, 50 < #hat{p}_{T} < 80 GeV',     color=808, syst_frac=0.10, xsec=1.92043e+07),
    MCSample('qcdpt0080', '/QCD_Pt_80to120_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',    6953590, nice='QCD, 80 < #hat{p}_{T} < 120 GeV',    color=808, syst_frac=0.10, xsec=2.76253e+06),
    MCSample('qcdpt0120', '/QCD_Pt_120to170_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',   6848223, nice='QCD, 120 < #hat{p}_{T} < 300 GeV',   color=808, syst_frac=0.10, xsec=4.711e+05),
    MCSample('qcdpt0170', '/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',   6918748, nice='QCD, 170 < #hat{p}_{T} < 300 GeV',   color=808, syst_frac=0.10, xsec=117276),
    MCSample('qcdpt0300', '/QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',   5968960, nice='QCD, 300 < #hat{p}_{T} < 470 GeV',   color=809, syst_frac=0.10, xsec=7823.28),
    MCSample('qcdpt0470', '/QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',   3977770, nice='QCD, 470 < #hat{p}_{T} < 600 GeV',   color=810, syst_frac=0.10, xsec=648.174),
    MCSample('qcdpt0600', '/QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',   3979884, nice='QCD, 600 < #hat{p}_{T} < 800 GeV',   color=811, syst_frac=0.10, xsec=186.946),
    MCSample('qcdpt0800', '/QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',  3973224, nice='QCD, 800 < #hat{p}_{T} < 1000 GeV',  color=812, syst_frac=0.10, xsec=32.2928),
    MCSample('qcdpt1000', '/QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM', 2967947, nice='QCD, 1000 < #hat{p}_{T} < 1400 GeV', color=813, syst_frac=0.10, xsec=9.41832),
    MCSample('qcdpt1400', '/QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',  395725, nice='QCD, 1400 < #hat{p}_{T} < 1800 GeV', color=814, syst_frac=0.10, xsec=0.84265),
    MCSample('qcdpt1800', '/QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',  393760, nice='QCD, 1800 < #hat{p}_{T} < 2400 GeV', color=815, syst_frac=0.10, xsec=0.114943),
    MCSample('qcdpt2400', '/QCD_Pt_2400to3200_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',  398452, nice='QCD, 2400 < #hat{p}_{T} < 3200 GeV', color=815, syst_frac=0.10, xsec=0.00682981),
    MCSample('qcdpt3200', '/QCD_Pt_3200toInf_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',   391108, nice='QCD, #hat{p}_{T} > 3200 GeV',        color=815, syst_frac=0.10, xsec=0.000165445),
    ]

'''
These not updated for run2.

ttbar_systematics_samples = [
    MCSample('ttbarsystMSDecays', '', 999, nice='t#bar{t} (MSDecays)',                                       color=  4, syst_frac=0.15, xsec=888.),
    MCSample('ttbarsystM166p5',   '', 999, nice='t#bar{t} (M=166.5 GeV)',                                    color=  4, syst_frac=0.15, xsec=888.),
    MCSample('ttbarsystM178p5',   '', 999, nice='t#bar{t} (M=178.5 GeV)',                                    color=  4, syst_frac=0.15, xsec=888.),
    MCSample('ttbarsystMatchDn',  '', 999, nice='t#bar{t} (match down)',                                     color=  4, syst_frac=0.15, xsec=888.),
    MCSample('ttbarsystMatchUp',  '', 999, nice='t#bar{t} (match up)',                                       color=  4, syst_frac=0.15, xsec=888.),
    MCSample('ttbarsystScaleDn',  '', 999, nice='t#bar{t} (Q^2 down)',                                       color=  4, syst_frac=0.15, xsec=888.),
    MCSample('ttbarsystScaleUp',  '', 999, nice='t#bar{t} (Q^2 up)',                                         color=  4, syst_frac=0.15, xsec=888.),
    ]
'''

########################################################################

data_samples = [
    DataSample('JetHT2015D', '/JetHT/Run2015D-16Dec2015-v1/AOD'), # 256630 - 260727
    ]

auxiliary_data_samples = [
    #DataSample('SingleMuon2015Dv3', '/SingleMuon/Run2015D-PromptReco-v3/AOD'),
    #DataSample('SingleMuon2015Dv4', '/SingleMuon/Run2015D-PromptReco-v4/AOD'),
    ]

for s in data_samples + auxiliary_data_samples:
    s.json = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/Reprocessing/Cert_13TeV_16Dec2015ReReco_Collisions15_25ns_JSON_Silver.txt'

########################################################################

registry = SamplesRegistry()

__all__ = [
    'qcd_samples_not_used',
    'qcd_samples',
    'ttbar_samples',
    'mfv_signal_samples',
    'xx4j_samples',
    'leptonic_background_samples',
#    'ttbar_systematics_samples',
    'auxiliary_background_samples',
    'data_samples',
    'auxiliary_data_samples',
    'registry',
    ]

for x in __all__:
    o = eval(x)
    if type(o) == list:
        registry.add_list(x,o)
        for sample in o:
            registry.add(sample)
            exec '%s = sample' % sample.name
            __all__.append(sample.name)

########################################################################

# Extra datasets and other overrides go here.

qcdht0500.aaa = eu_aaa
qcdht1000.aaa = us_aaa + eu_aaa 

# Can't add data datasets by primary (many have the same primary).
for sample in data_samples + auxiliary_data_samples:
    sample.add_dataset('miniaod', sample.dataset.replace('AOD', 'MINIAOD'))

JetHT2015D.add_dataset('ntuplev6p1_76x', '/JetHT/tucker-ntuplev6p1_76x-1c7d7cc72ce161506ace63027d8999cf/USER', dbs_inst='phys03') #, 7607820) # 1312 files

def add_dataset_by_primary(ds_name, dataset, nevents_orig, **kwargs):
    x = registry.by_primary_dataset(dataset.split('/')[1])
    if len(x) != 1:
        raise ValueError('could not find sample for %s by primary dataset: %r' % (dataset, x))
    sample = x[0]
    sample.add_dataset(ds_name, dataset, nevents_orig, **kwargs)

_adbp = add_dataset_by_primary
_adbp3 = partial(_adbp, dbs_inst='phys03')

_adbp3('ntuplev6p1_76x', '/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/tucker-ntuplev6p1_76x-e0115cf27c092c2dd18b3e7b858a8124/USER',     44386) # 99 files, 102 expected
_adbp3('ntuplev6p1_76x', '/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/tucker-ntuplev6p1_76x-0647f73cce69e58d0aef5913afbb0f3c/USER', 5022354) # 212 files, 213 expected
_adbp3('ntuplev6p1_76x', '/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/tucker-ntuplev6p1_76x-94e89177941e8a89c5cdccd7b741b65c/USER', 3952153) # 160 files
_adbp3('ntuplev6p1_76x', '/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/tucker-ntuplev6p1_76x-4b20a26f36e3365f106971e9e5d3e060/USER',  1981228) # 94 files
_adbp3('ntuplev6p1_76x', '/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/tucker-ntuplev6p1_76x-b4b7f8e9859e632440c4bc9123183328/USER',          1319314) # 197 files, 201 expected

# for x in $(cat a.txt); echo _adbp3\(\'\', \'${x}\', $(dass 3 nevents $x)\) \# $(dass 3 file $x | wl) files

########################################################################

if __name__ == '__main__':
    main(registry)

    if 0:
        from DBS import *
        for x in qcd_samples + ttbar_samples + smaller_background_samples:
            ds = x.datasets['miniaod'].dataset
            print ds
            print numevents_in_dataset(ds)

    if 0:
        for sample in qcd_samples + ttbar_samples:
            print "'%s': %.4e," % (sample.name, sample.datasets['ntuplev6p1'].nevents_orig / float(sample.nevents_orig))
