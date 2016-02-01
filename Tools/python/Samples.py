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
    MCSample('qcdht0500', '/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/AODSIM',   19664159, nice='QCD, 500 < H_{T} < 700 GeV',   color=804, syst_frac=0.20, xsec=3.163e4),
    MCSample('qcdht0700', '/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/AODSIM',  15356448, nice='QCD, 700 < H_{T} < 1000 GeV',  color=805, syst_frac=0.20, xsec=6.802e3), 
    MCSample('qcdht1000', '/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/AODSIM',  4963895, nice='QCD, 1000 < H_{T} < 1500 GeV', color=806, syst_frac=0.20, xsec=1.206e3),
    MCSample('qcdht1500', '/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/AODSIM',  3868886, nice='QCD, 1500 < H_{T} < 2000 GeV', color=807, syst_frac=0.20, xsec=120),
    MCSample('qcdht2000', '/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/AODSIM',   1961774, nice='QCD, H_{T} > 2000',            color=808, syst_frac=0.20, xsec=25.3),
    ]

ttbar_samples = [
    MCSample('ttbar', '/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/AODSIM', 42784971, nice='t#bar{t}', color=4, syst_frac=0.15, xsec=832.),
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

auxiliary_background_samples = [
    MCSample('ttbarincl',         '', 999, nice='t#bar{t}',                                                  color=  4, syst_frac=0.15, xsec=888.),
    MCSample('tttt',              '', 999, nice='t#bar{t}t#bar{t}',                                          color= -1, syst_frac=0.20, xsec=888.),
    MCSample('tthbb',             '', 999, nice='ttH, H #rightarrow bb',                                     color= -1, syst_frac=0.13, xsec=888.),
    MCSample('zjetstonunuHT050',  '', 999, nice='Z #rightarrow #nu#nu + jets, 50 < H_{T} < 100 GeV',         color= -1, syst_frac=0.10, xsec=888.),
    MCSample('zjetstonunuHT100',  '', 999, nice='Z #rightarrow #nu#nu + jets, 100 < H_{T} < 200 GeV',        color= -1, syst_frac=0.10, xsec=888.),
    MCSample('zjetstonunuHT200',  '', 999, nice='Z #rightarrow #nu#nu + jets, 200 < H_{T} < 400 GeV',        color= -1, syst_frac=0.10, xsec=888.),
    MCSample('zjetstonunuHT400',  '', 999, nice='Z #rightarrow #nu#nu + jets, H_{T} > 400 GeV',              color= -1, syst_frac=0.10, xsec=888.),
    MCSample('bjetsht0100',       '', 999, nice='b jets, 100 < H_{T} < 250 GeV',                             color=801, syst_frac=0.10, xsec=888.),
    MCSample('bjetsht0250',       '', 999, nice='b jets, 250 < H_{T} < 500 GeV',                             color=802, syst_frac=0.10, xsec=888.),
    MCSample('bjetsht0500',       '', 999, nice='b jets, 500 < H_{T} < 1000 GeV',                            color=803, syst_frac=0.10, xsec=888.),
    MCSample('bjetsht1000',       '', 999, nice='b jets, H_{T} > 1000 GeV',                                  color=804, syst_frac=0.10, xsec=888.),
    MCSample('qcdpt0000',         '', 999, nice='QCD, #hat{p}_{T} < 5 GeV',                                  color=801, syst_frac=0.10, xsec=888.),
    MCSample('qcdpt0005',         '', 999, nice='QCD, 5 < #hat{p}_{T} < 15 GeV',                             color=802, syst_frac=0.10, xsec=888.),
    MCSample('qcdpt0015',         '', 999, nice='QCD, 15 < #hat{p}_{T} < 30 GeV',                            color=803, syst_frac=0.10, xsec=888.),
    MCSample('qcdpt0030',         '', 999, nice='QCD, 30 < #hat{p}_{T} < 50 GeV',                            color=804, syst_frac=0.10, xsec=888.),
    MCSample('qcdpt0050',         '', 999, nice='QCD, 50 < #hat{p}_{T} < 80 GeV',                            color=805, syst_frac=0.10, xsec=888.),
    MCSample('qcdpt0080',         '', 999, nice='QCD, 80 < #hat{p}_{T} < 120 GeV',                           color=806, syst_frac=0.10, xsec=888.),
    MCSample('qcdpt0120',         '', 999, nice='QCD, 120 < #hat{p}_{T} < 170 GeV',                          color=807, syst_frac=0.10, xsec=888.),
    MCSample('qcdpt0170',         '', 999, nice='QCD, 170 < #hat{p}_{T} < 300 GeV',                          color=808, syst_frac=0.10, xsec=888.),
    MCSample('qcdpt0300',         '', 999, nice='QCD, 300 < #hat{p}_{T} < 470 GeV',                          color=809, syst_frac=0.10, xsec=888.),
    MCSample('qcdpt0470',         '', 999, nice='QCD, 470 < #hat{p}_{T} < 600 GeV',                          color=810, syst_frac=0.10, xsec=888.),
    MCSample('qcdpt0600',         '', 999, nice='QCD, 600 < #hat{p}_{T} < 800 GeV',                          color=811, syst_frac=0.10, xsec=888.),
    MCSample('qcdpt0800',         '', 999, nice='QCD, 800 < #hat{p}_{T} < 1000 GeV',                         color=812, syst_frac=0.10, xsec=888.),
    MCSample('qcdpt1000',         '', 999, nice='QCD, 1000 < #hat{p}_{T} < 1400 GeV',                        color=813, syst_frac=0.10, xsec=888.),
    MCSample('qcdpt1400',         '', 999, nice='QCD, 1400 < #hat{p}_{T} < 1800 GeV',                        color=814, syst_frac=0.10, xsec=888.),
    MCSample('qcdpt1800',         '', 999, nice='QCD, #hat{p}_{T} > 1800 GeV',                               color=815, syst_frac=0.10, xsec=888.),
    MCSample('qcdmu0015',         '', 999, nice='QCDmu5, 15 < #hat{p}_{T} < 20 GeV',                         color=801, syst_frac=0.10, xsec=888.),
    MCSample('qcdmu0020',         '', 999, nice='QCDmu5, 20 < #hat{p}_{T} < 30 GeV',                         color=801, syst_frac=0.10, xsec=888.),
    MCSample('qcdmu0030',         '', 999, nice='QCDmu5, 30 < #hat{p}_{T} < 50 GeV',                         color=801, syst_frac=0.10, xsec=888.),
    MCSample('qcdmu0050',         '', 999, nice='QCDmu5, 50 < #hat{p}_{T} < 80 GeV',                         color=801, syst_frac=0.10, xsec=888.),
    MCSample('qcdmu0080',         '', 999, nice='QCDmu5, 80 < #hat{p}_{T} < 120 GeV',                        color=801, syst_frac=0.10, xsec=888.),
    MCSample('qcdmu0120',         '', 999, nice='QCDmu5, 120 < #hat{p}_{T} < 170 GeV',                       color=801, syst_frac=0.10, xsec=888.),
    MCSample('qcdmu0170',         '', 999, nice='QCDmu5, 170 < #hat{p}_{T} < 300 GeV',                       color=801, syst_frac=0.10, xsec=888.),
    MCSample('qcdmu0300',         '', 999, nice='QCDmu5, 300 < #hat{p}_{T} < 470 GeV',                       color=801, syst_frac=0.10, xsec=888.),
    MCSample('qcdmu0470',         '', 999, nice='QCDmu5, 470 < #hat{p}_{T} < 600 GeV',                       color=801, syst_frac=0.10, xsec=888.),
    MCSample('qcdmu0600',         '', 999, nice='QCDmu5, 600 < #hat{p}_{T} < 800 GeV',                       color=801, syst_frac=0.10, xsec=888.),
    MCSample('qcdmu0800',         '', 999, nice='QCDmu5, 800 < #hat{p}_{T} < 1000 GeV',                      color=801, syst_frac=0.10, xsec=888.),
    MCSample('qcdmu1000',         '', 999, nice='QCDmu5, #hat{p}_{T} > 1000 GeV',                            color=801, syst_frac=0.10, xsec=888.),
    MCSample('qcdem020',          '', 999, nice='QCDem, < #hat{p}_{T} < GeV',                                color=801, syst_frac=0.10, xsec=888.),
    MCSample('qcdem030',          '', 999, nice='QCDem, < #hat{p}_{T} < GeV',                                color=801, syst_frac=0.10, xsec=888.),
    MCSample('qcdem080',          '', 999, nice='QCDem, < #hat{p}_{T} < GeV',                                color=801, syst_frac=0.10, xsec=888.),
    MCSample('qcdem170',          '', 999, nice='QCDem, < #hat{p}_{T} < GeV',                                color=801, syst_frac=0.10, xsec=888.),
    MCSample('qcdem250',          '', 999, nice='QCDem, < #hat{p}_{T} < GeV',                                color=801, syst_frac=0.10, xsec=888.),
    MCSample('qcdem350',          '', 999, nice='QCDem, < #hat{p}_{T} < GeV',                                color=801, syst_frac=0.10, xsec=888.),
    MCSample('qcdbce020',         '', 999, nice='QCDbce, < #hat{p}_{T} < GeV',                               color=801, syst_frac=0.10, xsec=888.),
    MCSample('qcdbce030',         '', 999, nice='QCDbce, < #hat{p}_{T} < GeV',                               color=801, syst_frac=0.10, xsec=888.),
    MCSample('qcdbce080',         '', 999, nice='QCDbce, < #hat{p}_{T} < GeV',                               color=801, syst_frac=0.10, xsec=888.),
    MCSample('qcdbce170',         '', 999, nice='QCDbce, < #hat{p}_{T} < GeV',                               color=801, syst_frac=0.10, xsec=888.),
    MCSample('qcdbce250',         '', 999, nice='QCDbce, < #hat{p}_{T} < GeV',                               color=801, syst_frac=0.10, xsec=888.),
    MCSample('qcdbce350',         '', 999, nice='QCDbce, < #hat{p}_{T} < GeV',                               color=801, syst_frac=0.10, xsec=888.),
    MCSample('qcdb150',           '', 999, nice='QCDb, #hat{p}_{T} > 150 GeV',                               color=801, syst_frac=0.10, xsec=888.),
    ]
'''

########################################################################

data_samples = [
    DataSample('JetHT2015Dv3', '/JetHT/Run2015D-PromptReco-v3/AOD'), # 256584-258158
    DataSample('JetHT2015Dv4', '/JetHT/Run2015D-PromptReco-v4/AOD'), # 258159-260727
    ]

auxiliary_data_samples = [
    DataSample('SingleMuon2015Dv3', '/SingleMuon/Run2015D-PromptReco-v3/AOD'),
    DataSample('SingleMuon2015Dv4', '/SingleMuon/Run2015D-PromptReco-v4/AOD'),
    ]

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
#    'auxiliary_background_samples',
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

JetHT2015Dv3.add_dataset('ntuplev5', '/JetHT/tucker-ntuplev5-77b89976378048ac64891f2e506e498f/USER', dbs_inst='phys03')
JetHT2015Dv4.add_dataset('ntuplev5', '/JetHT/tucker-ntuplev5-a43ce49cdf92a8b591fb7f3e283b5747/USER', dbs_inst='phys03')

JetHT2015Dv3.add_dataset('ntuplev6p1', '/JetHT/tucker-ntuplev6p1-d25c0abed1a78f992654e25a5f177c58/USER', dbs_inst='phys03')
JetHT2015Dv4.add_dataset('ntuplev6p1', '/JetHT/tucker-ntuplev6p1-96d392bb474bf0763c3141f66527b228/USER', dbs_inst='phys03')

def add_dataset_by_primary(ds_name, dataset, nevents_orig, **kwargs):
    x = registry.by_primary_dataset(dataset.split('/')[1])
    if len(x) != 1:
        raise ValueError('could not find sample for %s by primary dataset: %r' % (dataset, x))
    sample = x[0]
    sample.add_dataset(ds_name, dataset, nevents_orig, **kwargs)

_adbp = add_dataset_by_primary
_adbp3 = partial(_adbp, dbs_inst='phys03')

_adbp('miniaod', '/QCD_HT100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/MINIAODSIM',       80093092)
_adbp('miniaod', '/QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/MINIAODSIM',       18717349)
_adbp('miniaod', '/QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/MINIAODSIM',       20086103)
_adbp('miniaod', '/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM',       19542847)
_adbp('miniaod', '/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM',      15011016)
_adbp('miniaod', '/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/MINIAODSIM',      4963895)
_adbp('miniaod', '/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM',      3848411)
_adbp('miniaod', '/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM',       1961774)
_adbp('miniaod', '/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM',              42730273)
_adbp('miniaod', '/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM',          24151270)
_adbp('miniaod', '/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM', 30535559)
_adbp('miniaod', '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v3/MINIAODSIM',     28825132)
_adbp('miniaod', '/QCD_Pt-20toInf_MuEnrichedPt15_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM',    13201693)

_adbp3('ntuplev5', '/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/tucker-ntuplev5-cd64d4d38dd6409d4ca234e4609d3c77/USER',     2232)
_adbp3('ntuplev5', '/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/tucker-ntuplev5-93677ca5776b654c8963938d330eb240/USER',  167601)
_adbp3('ntuplev5', '/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/tucker-ntuplev5-73708112df0cc5590c697e9b2eae9a19/USER', 217664)
_adbp3('ntuplev5', '/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/tucker-ntuplev5-e8b651745d4ad004f6212ea64808b55e/USER', 242956)
_adbp3('ntuplev5', '/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/tucker-ntuplev5-f255d1905ae5ab5e7f8225d5fd33347e/USER',  156091)
_adbp3('ntuplev5', '/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/tucker-ntuplev5-865013272748526966cf501a48a930c5/USER',          181145)
_adbp3('ntuplev5', '/mfv_neu_tau00100um_M0800/tucker-ntuplev5-e95b53ac10e314a1c23b8f6bd769105a/USER',                                  5479)
_adbp3('ntuplev5', '/mfv_neu_tau00300um_M0800/tucker-ntuplev5-8f83f112f3ab7411e44d3d49b945c276/USER',                                  8064)
_adbp3('ntuplev5', '/mfv_neu_tau01000um_M0800/tucker-ntuplev5-5e8fc450c573586178f258b85d94a0e3/USER',                                  9452)
_adbp3('ntuplev5', '/mfv_neu_tau10000um_M0800/tucker-ntuplev5-8734c1a46e9ff969cef40e567e4f7ff9/USER',                                  9823)
_adbp3('ntuplev5', '/XXTo4J_M-700_CTau-1mm_TuneCUETP8M1_13TeV_pythia8/tucker-ntuplev5-1078893a9eadd8996cf0ad6bf4759d4d/USER',          9578)
_adbp3('ntuplev5', '/XXTo4J_M-700_CTau-10mm_TuneCUETP8M1_13TeV_pythia8/tucker-ntuplev5-ad44f2874d508bc75b868fe9a50955b6/USER',         9779)

_adbp3('ntuplev6p1', '/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/tucker-ntuplev6p1-67e3d7f98974d11c1564bb7c2db00e1e/USER',     57153)
_adbp3('ntuplev6p1', '/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/tucker-ntuplev6p1-c9a10c18be0a73e5a52a3cdba00902d1/USER',  4959219)
_adbp3('ntuplev6p1', '/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/tucker-ntuplev6p1-e1c240be688be7cab34a2542584578d3/USER', 4936847)
_adbp3('ntuplev6p1', '/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/tucker-ntuplev6p1-6fb96be24b04736bc637c8fc2ee98e12/USER', 3868877)
_adbp3('ntuplev6p1', '/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/tucker-ntuplev6p1-7a16a7a644097b240677f9ca8ee3dee8/USER',  1961774)
_adbp3('ntuplev6p1', '/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/tucker-ntuplev6p1-e00e92510b9a3019aac785fe26a5ec0a/USER',          1543009)
_adbp3('ntuplev6p1', '/mfv_neu_tau00100um_M0800/tucker-ntuplev6p1-39cdb84772bce34cf067b2373733078c/USER',                                   9890)
_adbp3('ntuplev6p1', '/mfv_neu_tau00300um_M0800/tucker-ntuplev6p1-352074efc31c1f68ad0131463d6ad96a/USER',                                   9891)
_adbp3('ntuplev6p1', '/mfv_neu_tau01000um_M0800/tucker-ntuplev6p1-db76f9f06698e0f8a17b0324599153f4/USER',                                   9898)
_adbp3('ntuplev6p1', '/mfv_neu_tau10000um_M0800/tucker-ntuplev6p1-c6109cb67442c3d45ff9280b602a28af/USER',                                   9850)
_adbp3('ntuplev6p1', '/XXTo4J_M-700_CTau-1mm_TuneCUETP8M1_13TeV_pythia8/tucker-ntuplev6p1-cdf92c2c6785dbea85f17c3463e50253/USER',           9920)
_adbp3('ntuplev6p1', '/XXTo4J_M-700_CTau-10mm_TuneCUETP8M1_13TeV_pythia8/tucker-ntuplev6p1-69285a53bb344009125bfec0704acd1b/USER',          9875)

_adbp3('ntuplev6p1_run1', '/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/jchu-ntuplev6p1_run1-fe2bf0e03312d6d703f8bf44ce679fd1/USER',     57153)
_adbp3('ntuplev6p1_run1', '/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/jchu-ntuplev6p1_run1-b1cd4b4740c8ca6524d11dc967bac4dc/USER',  4959219)
_adbp3('ntuplev6p1_run1', '/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/jchu-ntuplev6p1_run1-ddee14736343ba07b05db307c94c9d28/USER', 4936847)
_adbp3('ntuplev6p1_run1', '/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/jchu-ntuplev6p1_run1-f17ad16d1b5ce854bd2804fa3b6b39b3/USER', 3868877)
_adbp3('ntuplev6p1_run1', '/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/jchu-ntuplev6p1_run1-19ffa5ef5f7969e7589737cb186f585e/USER',  1961774)
_adbp3('ntuplev6p1_run1', '/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/jchu-ntuplev6p1_run1-cb52242aabfec8a312dae8e5c4a58f6d/USER',          1543009)

_adbp3('ntuplev6p1_2px8st', '/mfv_neu_tau00100um_M0800/tucker-ntuplev6p1_2px8st-5419a85b9694f5b9766e31273ae03ac0/USER', 9890) # 1 files
_adbp3('ntuplev6p1_2px8st', '/mfv_neu_tau00300um_M0800/tucker-ntuplev6p1_2px8st-104721a7c3d49e8958e075bbc0f82dd8/USER', 9891) # 1 files
_adbp3('ntuplev6p1_2px8st', '/mfv_neu_tau01000um_M0800/tucker-ntuplev6p1_2px8st-7b2462f75901743b51dc5a156a1c1414/USER', 9898) # 1 files
_adbp3('ntuplev6p1_2px8st', '/mfv_neu_tau10000um_M0800/tucker-ntuplev6p1_2px8st-d6dc678113d4eacc05ef859334d7b279/USER', 9850) # 1 files
_adbp3('ntuplev6p1_2px8st', '/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/tucker-ntuplev6p1_2px8st-44c98668603f41acd8df2c97baceffb7/USER', 57153) # 792 files
_adbp3('ntuplev6p1_2px8st', '/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/tucker-ntuplev6p1_2px8st-2ced5f0f460ad76282aafbd2182447d9/USER', 4959219) # 612 files
_adbp3('ntuplev6p1_2px8st', '/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/tucker-ntuplev6p1_2px8st-2e5decf9946cdcbd4ec398e85a130d13/USER', 4936847) # 202 files
_adbp3('ntuplev6p1_2px8st', '/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/tucker-ntuplev6p1_2px8st-e5a8decd62588e659854cf98be63711f/USER', 3868877) # 157 files
_adbp3('ntuplev6p1_2px8st', '/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/tucker-ntuplev6p1_2px8st-1754936f7ba29ae78387b8974936e161/USER', 1862060) # 75 files
_adbp3('ntuplev6p1_2px8st', '/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/tucker-ntuplev6p1_2px8st-34fa38c4d69f3aa7f301268841ddb427/USER', 1543009) # 1715 files
_adbp3('ntuplev6p1_2px8st', '/XXTo4J_M-700_CTau-1mm_TuneCUETP8M1_13TeV_pythia8/tucker-ntuplev6p1_2px8st-60455ee0f977ebc42c383fe60feb788e/USER', 9920) # 1 files
_adbp3('ntuplev6p1_2px8st', '/XXTo4J_M-700_CTau-10mm_TuneCUETP8M1_13TeV_pythia8/tucker-ntuplev6p1_2px8st-0cc6776f247803d487299598023b7949/USER', 9875) # 1 files

_adbp3('ntuplev6p1_2pxlay8st', '/mfv_neu_tau00100um_M0800/tucker-ntuplev6p1_2pxlay8st-9fd9c122b88d8afef63ada254da69e5f/USER', 9890) # 1 files
_adbp3('ntuplev6p1_2pxlay8st', '/mfv_neu_tau00300um_M0800/tucker-ntuplev6p1_2pxlay8st-004d1154c69761bf41acb77e9423bc38/USER', 9891) # 1 files
_adbp3('ntuplev6p1_2pxlay8st', '/mfv_neu_tau01000um_M0800/tucker-ntuplev6p1_2pxlay8st-8c1ed6ff65fae801e8160064765c19f1/USER', 9898) # 1 files
_adbp3('ntuplev6p1_2pxlay8st', '/mfv_neu_tau10000um_M0800/tucker-ntuplev6p1_2pxlay8st-3ec6c7523c4504968f5798f366d9e27f/USER', 9850) # 1 files
_adbp3('ntuplev6p1_2pxlay8st', '/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/tucker-ntuplev6p1_2pxlay8st-bcee0a156a80f338d2fbdf2bfcd5c2ef/USER', 57153) # 792 files
_adbp3('ntuplev6p1_2pxlay8st', '/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/tucker-ntuplev6p1_2pxlay8st-1ab04998e62ade352be18fe1954e0c9e/USER', 4959219) # 612 files
_adbp3('ntuplev6p1_2pxlay8st', '/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/tucker-ntuplev6p1_2pxlay8st-4f614163bc3145d8d326daa626913706/USER', 4936847) # 202 files
_adbp3('ntuplev6p1_2pxlay8st', '/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/tucker-ntuplev6p1_2pxlay8st-3bc3c5e190ea0e1e5000aafb3363ffc1/USER', 3868877) # 157 files
_adbp3('ntuplev6p1_2pxlay8st', '/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/tucker-ntuplev6p1_2pxlay8st-afbf0bab212797f67b9d5bb5632eb527/USER', 1837210) # 74 files
_adbp3('ntuplev6p1_2pxlay8st', '/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/tucker-ntuplev6p1_2pxlay8st-7a314667465b3c3e11c665c7c4a07498/USER', 1543009) # 1715 files
_adbp3('ntuplev6p1_2pxlay8st', '/XXTo4J_M-700_CTau-1mm_TuneCUETP8M1_13TeV_pythia8/tucker-ntuplev6p1_2pxlay8st-1804ca703e1d317d74776ac8d22c80aa/USER', 9920) # 1 files
_adbp3('ntuplev6p1_2pxlay8st', '/XXTo4J_M-700_CTau-10mm_TuneCUETP8M1_13TeV_pythia8/tucker-ntuplev6p1_2pxlay8st-d12cd34a24143f49dd45fa243f099d7d/USER', 9875) # 1 files

_adbp3('ntuplev6p1_3pxlay8st', '/mfv_neu_tau00100um_M0800/tucker-ntuplev6p1_3pxlay8st-a56e705e161ca1cc546ec2de5e4bc7e5/USER', 9890) # 1 files
_adbp3('ntuplev6p1_3pxlay8st', '/mfv_neu_tau00300um_M0800/tucker-ntuplev6p1_3pxlay8st-741265543f05120d7c547a8af4788fb3/USER', 9891) # 1 files
_adbp3('ntuplev6p1_3pxlay8st', '/mfv_neu_tau01000um_M0800/tucker-ntuplev6p1_3pxlay8st-757a9076a1c9e191ae43e4cb96a326c8/USER', 9898) # 1 files
_adbp3('ntuplev6p1_3pxlay8st', '/mfv_neu_tau10000um_M0800/tucker-ntuplev6p1_3pxlay8st-5f2475e5cdc6facc72fcea85fddf018f/USER', 9850) # 1 files
_adbp3('ntuplev6p1_3pxlay8st', '/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/tucker-ntuplev6p1_3pxlay8st-4f787a160a581bd6d7422172e58ea3e5/USER', 57153) # 792 files
_adbp3('ntuplev6p1_3pxlay8st', '/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/tucker-ntuplev6p1_3pxlay8st-9a5a7853a08bab6dfbe4ef22f0afccce/USER', 4748341) # 586 files
_adbp3('ntuplev6p1_3pxlay8st', '/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/tucker-ntuplev6p1_3pxlay8st-76040ca59d66c6a8aa3ae6438d442230/USER', 4936847) # 202 files
_adbp3('ntuplev6p1_3pxlay8st', '/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/tucker-ntuplev6p1_3pxlay8st-a34d8084dca7f6d3e0d333a5434eda9f/USER', 3868877) # 157 files
_adbp3('ntuplev6p1_3pxlay8st', '/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/tucker-ntuplev6p1_3pxlay8st-8bb627af6096343168e2713a0769d18e/USER', 1862215) # 75 files
_adbp3('ntuplev6p1_3pxlay8st', '/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/tucker-ntuplev6p1_3pxlay8st-fa6ff58078da3dea631e63ec4f8caea6/USER', 1543009) # 1715 files
_adbp3('ntuplev6p1_3pxlay8st', '/XXTo4J_M-700_CTau-1mm_TuneCUETP8M1_13TeV_pythia8/tucker-ntuplev6p1_3pxlay8st-25bdaac843819e947987b6d291f40452/USER', 9920) # 1 files
_adbp3('ntuplev6p1_3pxlay8st', '/XXTo4J_M-700_CTau-10mm_TuneCUETP8M1_13TeV_pythia8/tucker-ntuplev6p1_3pxlay8st-fe8fa09e436a54e0adb1006ba96aae74/USER', 9875) # 1 files

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
