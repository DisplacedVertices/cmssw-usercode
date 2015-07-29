#!/usr/bin/env python

from JMTucker.Tools.Sample import *

########################################################################

print 'JMTBAD need to update samples and cross sections for run 2'

ttbar_xsec = 245.8 # for world-combination m_top = 173.3 GeV (252.9 at CMS-measured m_top = 172.5)
ttbar_xsec_had = ttbar_xsec * 0.457

# https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat8TeV or PREP for xsecs
ttbar_samples = [
    MCSample('ttbarhadronic',     '', 999, nice='t#bar{t}, hadronic',                                        color=  4, syst_frac=0.15, xsec=888.),
    MCSample('ttbarsemilep',      '', 999, nice='t#bar{t}, semileptonic',                                    color=  4, syst_frac=0.15, xsec=888.),
    MCSample('ttbardilep',        '', 999, nice='t#bar{t}, dileptonic',                                      color=  4, syst_frac=0.15, xsec=888.),
    ]

qcd_samples = [
    MCSample('qcdht0100',         '', 999, nice='QCD, 100 < H_{T} < 250 GeV',                                color=801, syst_frac=0.10, xsec=888.),
    MCSample('qcdht0250',         '', 999, nice='QCD, 250 < H_{T} < 500 GeV',                                color=802, syst_frac=0.10, xsec=888.),
    MCSample('qcdht0500',         '', 999, nice='QCD, 500 < H_{T} < 1000 GeV',                               color=803, syst_frac=0.10, xsec=888.),
    MCSample('qcdht1000',         '', 999, nice='QCD, H_{T} > 1000 GeV',                                     color=804, syst_frac=0.10, xsec=888.),
    ]

leptonic_background_samples = [
    MCSample('wjetstolnu',        '', 999, nice='W + jets #rightarrow l#nu',                                 color=  9, syst_frac=0.10, xsec=888.),
    MCSample('dyjetstollM10',     '', 999, nice='DY + jets #rightarrow ll, 10 < M < 50 GeV',                 color= 29, syst_frac=0.10, xsec=888.),
    MCSample('dyjetstollM50',     '', 999, nice='DY + jets #rightarrow ll, M > 50 GeV',                      color= 32, syst_frac=0.10, xsec=888.),
    ]

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
    MCSample('qcdmupt15',         '', 999, nice='QCD, #hat{p}_{T} > 20 GeV, #mu p_{T} > 15 GeV',             color=801, syst_frac=0.10, xsec=888.),
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

########################################################################

data_samples = [
    DataSample('JetHT2015A', '/JetHT/Run2015A-PromptReco-v1/AOD'),
    DataSample('JetHT2015B', '/JetHT/Run2015B-PromptReco-v1/AOD'),
    ]

auxiliary_data_samples = [
    DataSample('SingleMuon2015A', '/SingleMuon/Run2015A-PromptReco-v1/AOD'),
    DataSample('SingleMuon2015B', '/SingleMuon/Run2015B-PromptReco-v1/AOD'),
    ]

########################################################################

samples = SamplesRegistry()

__all__ = [
    'ttbar_samples',
    'qcd_samples',
    'leptonic_background_samples',
    'ttbar_systematics_samples',
    'auxiliary_background_samples',
    'data_samples',
    'auxiliary_data_samples',
    'samples',
    ]

for x in __all__:
    o = eval(x)
    if type(o) == list:
        samples.add_list(x,o)
        for sample in o:
            samples.add(sample)
            exec '%s = sample' % sample.name
            __all__.append(sample.name)

########################################################################

# Extra datasets, filter efficiencies, other overrides go here.

########################################################################

if __name__ == '__main__':
    pass # JMTBAD
