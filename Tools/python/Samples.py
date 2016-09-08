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
    MCSample('qcdht0700', '/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM', 15547962, nice='QCD, 700 < H_{T} < 1000 GeV',  color=805, syst_frac=0.20, xsec=6.802e3),
    MCSample('qcdht1000', '/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM', 5085104, nice='QCD, 1000 < H_{T} < 1500 GeV', color=806, syst_frac=0.20, xsec=1.206e3),
    MCSample('qcdht1500', '/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM', 3952170, nice='QCD, 1500 < H_{T} < 2000 GeV', color=807, syst_frac=0.20, xsec=120),
    MCSample('qcdht2000', '/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',  1981228, nice='QCD, H_{T} > 2000',            color=808, syst_frac=0.20, xsec=25.3),
    ]

qcd_samples_ext = [
    MCSample('qcdht0500ext', '/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/AODSIM',   43242884, nice='QCD, 500 < H_{T} < 700 GeV',   color=804, syst_frac=0.20, xsec=3.163e4),
    MCSample('qcdht0700ext', '/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/AODSIM',  29569683, nice='QCD, 700 < H_{T} < 1000 GeV',  color=805, syst_frac=0.20, xsec=6.802e3),
    MCSample('qcdht1000ext', '/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/AODSIM', 10246203, nice='QCD, 1000 < H_{T} < 1500 GeV', color=806, syst_frac=0.20, xsec=1.206e3),
    MCSample('qcdht1500ext', '/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/AODSIM',  7815090, nice='QCD, 1500 < H_{T} < 2000 GeV', color=807, syst_frac=0.20, xsec=120),
    MCSample('qcdht2000ext', '/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/AODSIM',   4016332, nice='QCD, H_{T} > 2000',            color=808, syst_frac=0.20, xsec=25.3),
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
    MCSample('mfv_neu_tau00100um_M0300', '/mfv_neu_tau00100um_M0300/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-05e8cfd69022b6357c491ecab3cf47fb/USER', 10000),
    MCSample('mfv_neu_tau00100um_M0400', '/mfv_neu_tau00100um_M0400/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-05e8cfd69022b6357c491ecab3cf47fb/USER', 10000),
    MCSample('mfv_neu_tau00100um_M0800', '/mfv_neu_tau00100um_M0800/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-05e8cfd69022b6357c491ecab3cf47fb/USER', 10000),
    MCSample('mfv_neu_tau00100um_M1200', '/mfv_neu_tau00100um_M1200/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-05e8cfd69022b6357c491ecab3cf47fb/USER', 10000),
    MCSample('mfv_neu_tau00100um_M1600', '/mfv_neu_tau00100um_M1600/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-05e8cfd69022b6357c491ecab3cf47fb/USER', 10000),
    MCSample('mfv_neu_tau00300um_M0300', '/mfv_neu_tau00300um_M0300/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-05e8cfd69022b6357c491ecab3cf47fb/USER', 10000),
    MCSample('mfv_neu_tau00300um_M0400', '/mfv_neu_tau00300um_M0400/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-05e8cfd69022b6357c491ecab3cf47fb/USER', 10000),
    MCSample('mfv_neu_tau00300um_M0800', '/mfv_neu_tau00300um_M0800/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-05e8cfd69022b6357c491ecab3cf47fb/USER', 10000),
    MCSample('mfv_neu_tau00300um_M1200', '/mfv_neu_tau00300um_M1200/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-05e8cfd69022b6357c491ecab3cf47fb/USER', 10000),
    MCSample('mfv_neu_tau00300um_M1600', '/mfv_neu_tau00300um_M1600/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-05e8cfd69022b6357c491ecab3cf47fb/USER', 10000),
    MCSample('mfv_neu_tau01000um_M0300', '/mfv_neu_tau01000um_M0300/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-05e8cfd69022b6357c491ecab3cf47fb/USER', 10000),
    MCSample('mfv_neu_tau01000um_M0400', '/mfv_neu_tau01000um_M0400/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-05e8cfd69022b6357c491ecab3cf47fb/USER', 10000),
    MCSample('mfv_neu_tau01000um_M0800', '/mfv_neu_tau01000um_M0800/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-05e8cfd69022b6357c491ecab3cf47fb/USER', 10000),
    MCSample('mfv_neu_tau01000um_M1200', '/mfv_neu_tau01000um_M1200/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-05e8cfd69022b6357c491ecab3cf47fb/USER', 10000),
    MCSample('mfv_neu_tau01000um_M1600', '/mfv_neu_tau01000um_M1600/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-05e8cfd69022b6357c491ecab3cf47fb/USER', 10000),
    MCSample('mfv_neu_tau10000um_M0300', '/mfv_neu_tau10000um_M0300/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-05e8cfd69022b6357c491ecab3cf47fb/USER', 10000),
    MCSample('mfv_neu_tau10000um_M0400', '/mfv_neu_tau10000um_M0400/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-05e8cfd69022b6357c491ecab3cf47fb/USER', 10000),
    MCSample('mfv_neu_tau10000um_M0800', '/mfv_neu_tau10000um_M0800/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-05e8cfd69022b6357c491ecab3cf47fb/USER', 10000),
    MCSample('mfv_neu_tau10000um_M1200', '/mfv_neu_tau10000um_M1200/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-05e8cfd69022b6357c491ecab3cf47fb/USER', 10000),
    MCSample('mfv_neu_tau10000um_M1600', '/mfv_neu_tau10000um_M1600/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-05e8cfd69022b6357c491ecab3cf47fb/USER', 10000),
    ]

mfv_signal_samples_glu = [
    MCSample('mfv_glu_tau00100um_M0300', '/mfv_glu_tau00100um_M0300/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-074834c564f4d17ad146136690d1a903/USER', 10000),
    MCSample('mfv_glu_tau00100um_M0400', '/mfv_glu_tau00100um_M0400/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-074834c564f4d17ad146136690d1a903/USER', 10000),
    MCSample('mfv_glu_tau00100um_M0800', '/mfv_glu_tau00100um_M0800/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-074834c564f4d17ad146136690d1a903/USER', 10000),
    MCSample('mfv_glu_tau00100um_M1200', '/mfv_glu_tau00100um_M1200/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-074834c564f4d17ad146136690d1a903/USER', 10000),
    MCSample('mfv_glu_tau00100um_M1600', '/mfv_glu_tau00100um_M1600/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-074834c564f4d17ad146136690d1a903/USER', 10000),
    MCSample('mfv_glu_tau00300um_M0300', '/mfv_glu_tau00300um_M0300/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-074834c564f4d17ad146136690d1a903/USER', 10000),
    MCSample('mfv_glu_tau00300um_M0400', '/mfv_glu_tau00300um_M0400/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-074834c564f4d17ad146136690d1a903/USER', 10000),
    MCSample('mfv_glu_tau00300um_M0800', '/mfv_glu_tau00300um_M0800/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-074834c564f4d17ad146136690d1a903/USER', 10000),
    MCSample('mfv_glu_tau00300um_M1200', '/mfv_glu_tau00300um_M1200/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-074834c564f4d17ad146136690d1a903/USER', 10000),
    MCSample('mfv_glu_tau00300um_M1600', '/mfv_glu_tau00300um_M1600/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-074834c564f4d17ad146136690d1a903/USER', 10000),
    MCSample('mfv_glu_tau01000um_M0300', '/mfv_glu_tau01000um_M0300/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-074834c564f4d17ad146136690d1a903/USER', 10000),
    MCSample('mfv_glu_tau01000um_M0400', '/mfv_glu_tau01000um_M0400/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-074834c564f4d17ad146136690d1a903/USER', 10000),
    MCSample('mfv_glu_tau01000um_M0800', '/mfv_glu_tau01000um_M0800/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-074834c564f4d17ad146136690d1a903/USER', 10000),
    MCSample('mfv_glu_tau01000um_M1200', '/mfv_glu_tau01000um_M1200/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-074834c564f4d17ad146136690d1a903/USER', 10000),
    MCSample('mfv_glu_tau01000um_M1600', '/mfv_glu_tau01000um_M1600/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-074834c564f4d17ad146136690d1a903/USER', 10000),
    MCSample('mfv_glu_tau10000um_M0300', '/mfv_glu_tau10000um_M0300/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-074834c564f4d17ad146136690d1a903/USER', 10000),
    MCSample('mfv_glu_tau10000um_M0400', '/mfv_glu_tau10000um_M0400/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-074834c564f4d17ad146136690d1a903/USER', 10000),
    MCSample('mfv_glu_tau10000um_M0800', '/mfv_glu_tau10000um_M0800/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-074834c564f4d17ad146136690d1a903/USER', 10000),
    MCSample('mfv_glu_tau10000um_M1200', '/mfv_glu_tau10000um_M1200/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-074834c564f4d17ad146136690d1a903/USER', 10000),
    MCSample('mfv_glu_tau10000um_M1600', '/mfv_glu_tau10000um_M1600/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-074834c564f4d17ad146136690d1a903/USER', 10000),
    ]

mfv_signal_samples_gluddbar = [
    MCSample('mfv_gluddbar_tau00100um_M0300', '/mfv_gluddbar_tau00100um_M0300/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-5fd65809e6fdab1d9fe9d428b2335332/USER', 10000),
    MCSample('mfv_gluddbar_tau00100um_M0400', '/mfv_gluddbar_tau00100um_M0400/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-5fd65809e6fdab1d9fe9d428b2335332/USER', 10000),
    MCSample('mfv_gluddbar_tau00100um_M0800', '/mfv_gluddbar_tau00100um_M0800/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-5fd65809e6fdab1d9fe9d428b2335332/USER', 10000),
    MCSample('mfv_gluddbar_tau00100um_M1200', '/mfv_gluddbar_tau00100um_M1200/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-5fd65809e6fdab1d9fe9d428b2335332/USER', 10000),
    MCSample('mfv_gluddbar_tau00100um_M1600', '/mfv_gluddbar_tau00100um_M1600/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-5fd65809e6fdab1d9fe9d428b2335332/USER', 10000),
    MCSample('mfv_gluddbar_tau00300um_M0300', '/mfv_gluddbar_tau00300um_M0300/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-5fd65809e6fdab1d9fe9d428b2335332/USER', 10000),
    MCSample('mfv_gluddbar_tau00300um_M0400', '/mfv_gluddbar_tau00300um_M0400/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-5fd65809e6fdab1d9fe9d428b2335332/USER', 10000),
    MCSample('mfv_gluddbar_tau00300um_M0800', '/mfv_gluddbar_tau00300um_M0800/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-5fd65809e6fdab1d9fe9d428b2335332/USER', 10000),
    MCSample('mfv_gluddbar_tau00300um_M1200', '/mfv_gluddbar_tau00300um_M1200/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-5fd65809e6fdab1d9fe9d428b2335332/USER', 10000),
    MCSample('mfv_gluddbar_tau00300um_M1600', '/mfv_gluddbar_tau00300um_M1600/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-5fd65809e6fdab1d9fe9d428b2335332/USER', 10000),
    MCSample('mfv_gluddbar_tau01000um_M0300', '/mfv_gluddbar_tau01000um_M0300/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-5fd65809e6fdab1d9fe9d428b2335332/USER', 10000),
    MCSample('mfv_gluddbar_tau01000um_M0400', '/mfv_gluddbar_tau01000um_M0400/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-5fd65809e6fdab1d9fe9d428b2335332/USER', 10000),
    MCSample('mfv_gluddbar_tau01000um_M0800', '/mfv_gluddbar_tau01000um_M0800/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-5fd65809e6fdab1d9fe9d428b2335332/USER', 10000),
    MCSample('mfv_gluddbar_tau01000um_M1200', '/mfv_gluddbar_tau01000um_M1200/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-5fd65809e6fdab1d9fe9d428b2335332/USER', 10000),
    MCSample('mfv_gluddbar_tau01000um_M1600', '/mfv_gluddbar_tau01000um_M1600/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-5fd65809e6fdab1d9fe9d428b2335332/USER', 10000),
    MCSample('mfv_gluddbar_tau10000um_M0300', '/mfv_gluddbar_tau10000um_M0300/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-5fd65809e6fdab1d9fe9d428b2335332/USER', 10000),
    MCSample('mfv_gluddbar_tau10000um_M0400', '/mfv_gluddbar_tau10000um_M0400/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-5fd65809e6fdab1d9fe9d428b2335332/USER', 10000),
    MCSample('mfv_gluddbar_tau10000um_M0800', '/mfv_gluddbar_tau10000um_M0800/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-5fd65809e6fdab1d9fe9d428b2335332/USER', 10000),
    MCSample('mfv_gluddbar_tau10000um_M1200', '/mfv_gluddbar_tau10000um_M1200/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-5fd65809e6fdab1d9fe9d428b2335332/USER', 10000),
    MCSample('mfv_gluddbar_tau10000um_M1600', '/mfv_gluddbar_tau10000um_M1600/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-5fd65809e6fdab1d9fe9d428b2335332/USER', 10000),
    ]

mfv_signal_samples_lq2 = [
    MCSample('mfv_lq2_tau00100um_M0300', '/mfv_lq2_tau00100um_M0300/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-db077d30b173c09abb0cf952345ec8ee/USER', 10000),
    MCSample('mfv_lq2_tau00100um_M0400', '/mfv_lq2_tau00100um_M0400/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-db077d30b173c09abb0cf952345ec8ee/USER', 10000),
    MCSample('mfv_lq2_tau00100um_M0800', '/mfv_lq2_tau00100um_M0800/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-db077d30b173c09abb0cf952345ec8ee/USER', 10000),
    MCSample('mfv_lq2_tau00100um_M1200', '/mfv_lq2_tau00100um_M1200/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-db077d30b173c09abb0cf952345ec8ee/USER', 10000),
    MCSample('mfv_lq2_tau00100um_M1600', '/mfv_lq2_tau00100um_M1600/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-db077d30b173c09abb0cf952345ec8ee/USER', 10000),
    MCSample('mfv_lq2_tau00300um_M0300', '/mfv_lq2_tau00300um_M0300/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-db077d30b173c09abb0cf952345ec8ee/USER', 10000),
    MCSample('mfv_lq2_tau00300um_M0400', '/mfv_lq2_tau00300um_M0400/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-db077d30b173c09abb0cf952345ec8ee/USER', 10000),
    MCSample('mfv_lq2_tau00300um_M0800', '/mfv_lq2_tau00300um_M0800/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-db077d30b173c09abb0cf952345ec8ee/USER', 10000),
    MCSample('mfv_lq2_tau00300um_M1200', '/mfv_lq2_tau00300um_M1200/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-db077d30b173c09abb0cf952345ec8ee/USER', 10000),
    MCSample('mfv_lq2_tau00300um_M1600', '/mfv_lq2_tau00300um_M1600/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-db077d30b173c09abb0cf952345ec8ee/USER', 10000),
    MCSample('mfv_lq2_tau01000um_M0300', '/mfv_lq2_tau01000um_M0300/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-db077d30b173c09abb0cf952345ec8ee/USER', 10000),
    MCSample('mfv_lq2_tau01000um_M0400', '/mfv_lq2_tau01000um_M0400/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-db077d30b173c09abb0cf952345ec8ee/USER', 10000),
    MCSample('mfv_lq2_tau01000um_M0800', '/mfv_lq2_tau01000um_M0800/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-db077d30b173c09abb0cf952345ec8ee/USER', 10000),
    MCSample('mfv_lq2_tau01000um_M1200', '/mfv_lq2_tau01000um_M1200/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-db077d30b173c09abb0cf952345ec8ee/USER', 10000),
    MCSample('mfv_lq2_tau01000um_M1600', '/mfv_lq2_tau01000um_M1600/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-db077d30b173c09abb0cf952345ec8ee/USER', 10000),
    MCSample('mfv_lq2_tau10000um_M0300', '/mfv_lq2_tau10000um_M0300/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-db077d30b173c09abb0cf952345ec8ee/USER', 10000),
    MCSample('mfv_lq2_tau10000um_M0400', '/mfv_lq2_tau10000um_M0400/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-db077d30b173c09abb0cf952345ec8ee/USER', 10000),
    MCSample('mfv_lq2_tau10000um_M0800', '/mfv_lq2_tau10000um_M0800/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-db077d30b173c09abb0cf952345ec8ee/USER', 10000),
    MCSample('mfv_lq2_tau10000um_M1200', '/mfv_lq2_tau10000um_M1200/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-db077d30b173c09abb0cf952345ec8ee/USER', 10000),
    MCSample('mfv_lq2_tau10000um_M1600', '/mfv_lq2_tau10000um_M1600/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-db077d30b173c09abb0cf952345ec8ee/USER', 10000),
    ]

for s in mfv_signal_samples + mfv_signal_samples_glu + mfv_signal_samples_gluddbar + mfv_signal_samples_lq2:
    s.dbs_inst = 'phys03'
    s.xsec = 1e-3
    s.aaa = us_aaa

xx4j_samples = [
    MCSample('xx4j_tau00001mm_M0050', '/XXTo4J_M-50_CTau-1mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',      30000),
    MCSample('xx4j_tau00003mm_M0050', '/XXTo4J_M-50_CTau-3mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',      29218),
    MCSample('xx4j_tau00010mm_M0050', '/XXTo4J_M-50_CTau-10mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',     30000),
    MCSample('xx4j_tau00100mm_M0050', '/XXTo4J_M-50_CTau-100mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',    29788),
    MCSample('xx4j_tau01000mm_M0050', '/XXTo4J_M-50_CTau-1000mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',   29316),
    MCSample('xx4j_tau02000mm_M0050', '/XXTo4J_M-50_CTau-2000mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',   30000),
    MCSample('xx4j_tau00001mm_M0100', '/XXTo4J_M-100_CTau-1mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',     30000),
    MCSample('xx4j_tau00003mm_M0100', '/XXTo4J_M-100_CTau-3mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',     30000),
    MCSample('xx4j_tau00010mm_M0100', '/XXTo4J_M-100_CTau-10mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',    30000),
    MCSample('xx4j_tau00030mm_M0100', '/XXTo4J_M-100_CTau-30mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',    30000),
    MCSample('xx4j_tau00100mm_M0100', '/XXTo4J_M-100_CTau-100mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',   30000),
    MCSample('xx4j_tau00300mm_M0100', '/XXTo4J_M-100_CTau-300mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',   30000),
    MCSample('xx4j_tau01000mm_M0100', '/XXTo4J_M-100_CTau-1000mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',  30000),
    MCSample('xx4j_tau02000mm_M0100', '/XXTo4J_M-100_CTau-2000mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',  30000),
    MCSample('xx4j_tau00001mm_M0300', '/XXTo4J_M-300_CTau-1mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',     10000),
    MCSample('xx4j_tau00003mm_M0300', '/XXTo4J_M-300_CTau-3mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',     10000),
    MCSample('xx4j_tau00010mm_M0300', '/XXTo4J_M-300_CTau-10mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',    10000),
    MCSample('xx4j_tau00030mm_M0300', '/XXTo4J_M-300_CTau-30mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',    10000),
    MCSample('xx4j_tau00100mm_M0300', '/XXTo4J_M-300_CTau-100mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',   10000),
    MCSample('xx4j_tau00300mm_M0300', '/XXTo4J_M-300_CTau-300mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',   10000),
    MCSample('xx4j_tau01000mm_M0300', '/XXTo4J_M-300_CTau-1000mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',  10000),
    MCSample('xx4j_tau02000mm_M0300', '/XXTo4J_M-300_CTau-2000mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',  10000),
    MCSample('xx4j_tau00003mm_M0500', '/XXTo4J_M-500_CTau-3mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',     10000),
    MCSample('xx4j_tau00010mm_M0500', '/XXTo4J_M-500_CTau-10mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',    10000),
    MCSample('xx4j_tau00030mm_M0500', '/XXTo4J_M-500_CTau-30mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',    10000),
    MCSample('xx4j_tau00300mm_M0500', '/XXTo4J_M-500_CTau-300mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',    9295),
    MCSample('xx4j_tau01000mm_M0500', '/XXTo4J_M-500_CTau-1000mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',  10000),
    MCSample('xx4j_tau02000mm_M0500', '/XXTo4J_M-500_CTau-2000mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',  10000),
    MCSample('xx4j_tau00001mm_M0700', '/XXTo4J_M-700_CTau-1mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',     10000),
    MCSample('xx4j_tau00003mm_M0700', '/XXTo4J_M-700_CTau-3mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',     10000),
    MCSample('xx4j_tau00010mm_M0700', '/XXTo4J_M-700_CTau-10mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',    10000),
    MCSample('xx4j_tau00030mm_M0700', '/XXTo4J_M-700_CTau-30mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',    10000),
    MCSample('xx4j_tau00100mm_M0700', '/XXTo4J_M-700_CTau-100mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',   10000),
    MCSample('xx4j_tau00300mm_M0700', '/XXTo4J_M-700_CTau-300mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',   10000),
    MCSample('xx4j_tau01000mm_M0700', '/XXTo4J_M-700_CTau-1000mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',  10000),
    MCSample('xx4j_tau00001mm_M1000', '/XXTo4J_M-1000_CTau-1mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',    10000),
    MCSample('xx4j_tau00003mm_M1000', '/XXTo4J_M-1000_CTau-3mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',    10000),
    MCSample('xx4j_tau00030mm_M1000', '/XXTo4J_M-1000_CTau-30mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',   10000),
    MCSample('xx4j_tau00300mm_M1000', '/XXTo4J_M-1000_CTau-300mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',  10000),
    MCSample('xx4j_tau01000mm_M1000', '/XXTo4J_M-1000_CTau-1000mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM', 10000),
    MCSample('xx4j_tau02000mm_M1000', '/XXTo4J_M-1000_CTau-2000mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM', 10000),
    MCSample('xx4j_tau00001mm_M1500', '/XXTo4J_M-1500_CTau-1mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',     9908),
    MCSample('xx4j_tau00010mm_M1500', '/XXTo4J_M-1500_CTau-10mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',   10000),
    MCSample('xx4j_tau00030mm_M1500', '/XXTo4J_M-1500_CTau-30mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',   10000),
    MCSample('xx4j_tau00300mm_M1500', '/XXTo4J_M-1500_CTau-300mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',  10000),
    MCSample('xx4j_tau01000mm_M1500', '/XXTo4J_M-1500_CTau-1000mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',  9745),
    MCSample('xx4j_tau00001mm_M3000', '/XXTo4J_M-3000_CTau-1mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',     9882),
    MCSample('xx4j_tau00003mm_M3000', '/XXTo4J_M-3000_CTau-3mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',    10000),
    MCSample('xx4j_tau00010mm_M3000', '/XXTo4J_M-3000_CTau-10mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',   10000),
    MCSample('xx4j_tau00030mm_M3000', '/XXTo4J_M-3000_CTau-30mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',   10000),
    MCSample('xx4j_tau00100mm_M3000', '/XXTo4J_M-3000_CTau-100mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',  10000),
    MCSample('xx4j_tau00300mm_M3000', '/XXTo4J_M-3000_CTau-300mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',   9384),
    MCSample('xx4j_tau01000mm_M3000', '/XXTo4J_M-3000_CTau-1000mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM', 10000),
    MCSample('xx4j_tau02000mm_M3000', '/XXTo4J_M-3000_CTau-2000mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM', 10000),
    ]

for s in xx4j_samples:
    s.xsec = 1e-3

wh_samples_4Tau = [
    MCSample('wh_4Tau_tau0000mm_M10', '/WH_HToSSTo4Tau_WToLNu_MH125_MS10_ctauS0_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',    20000),
    MCSample('wh_4Tau_tau1000mm_M10', '/WH_HToSSTo4Tau_WToLNu_MH125_MS10_ctauS1000_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER', 20000),
    MCSample('wh_4Tau_tau0100mm_M10', '/WH_HToSSTo4Tau_WToLNu_MH125_MS10_ctauS100_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',  19800),
    MCSample('wh_4Tau_tau0010mm_M10', '/WH_HToSSTo4Tau_WToLNu_MH125_MS10_ctauS10_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',   20000),
    MCSample('wh_4Tau_tau0001mm_M10', '/WH_HToSSTo4Tau_WToLNu_MH125_MS10_ctauS1_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',    19700),
    MCSample('wh_4Tau_tau0000mm_M25', '/WH_HToSSTo4Tau_WToLNu_MH125_MS25_ctauS0_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',    19900),
    MCSample('wh_4Tau_tau1000mm_M25', '/WH_HToSSTo4Tau_WToLNu_MH125_MS25_ctauS1000_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER', 19900),
    MCSample('wh_4Tau_tau0100mm_M25', '/WH_HToSSTo4Tau_WToLNu_MH125_MS25_ctauS100_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',  20000),
    MCSample('wh_4Tau_tau0010mm_M25', '/WH_HToSSTo4Tau_WToLNu_MH125_MS25_ctauS10_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',   19900),
    MCSample('wh_4Tau_tau0001mm_M25', '/WH_HToSSTo4Tau_WToLNu_MH125_MS25_ctauS1_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',    20000),
    MCSample('wh_4Tau_tau0000mm_M40', '/WH_HToSSTo4Tau_WToLNu_MH125_MS40_ctauS0_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',    20000),
    MCSample('wh_4Tau_tau1000mm_M40', '/WH_HToSSTo4Tau_WToLNu_MH125_MS40_ctauS1000_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER', 19900),
    MCSample('wh_4Tau_tau0100mm_M40', '/WH_HToSSTo4Tau_WToLNu_MH125_MS40_ctauS100_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',  19800),
    MCSample('wh_4Tau_tau0010mm_M40', '/WH_HToSSTo4Tau_WToLNu_MH125_MS40_ctauS10_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',   20000),
    MCSample('wh_4Tau_tau0001mm_M40', '/WH_HToSSTo4Tau_WToLNu_MH125_MS40_ctauS1_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',    20000)
]

wh_samples_bbbb = [
    MCSample('wh_bbbb_tau0000mm_M10', '/WH_HToSSTobbbb_WToLNu_MH125_MS10_ctauS0_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',    20000),
    MCSample('wh_bbbb_tau1000mm_M10', '/WH_HToSSTobbbb_WToLNu_MH125_MS10_ctauS1000_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER', 20000),
    MCSample('wh_bbbb_tau0100mm_M10', '/WH_HToSSTobbbb_WToLNu_MH125_MS10_ctauS100_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',  20000),
    MCSample('wh_bbbb_tau0010mm_M10', '/WH_HToSSTobbbb_WToLNu_MH125_MS10_ctauS10_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',   20000),
    MCSample('wh_bbbb_tau0001mm_M10', '/WH_HToSSTobbbb_WToLNu_MH125_MS10_ctauS1_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',    20000),
    MCSample('wh_bbbb_tau0000mm_M25', '/WH_HToSSTobbbb_WToLNu_MH125_MS25_ctauS0_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',    19800),
    MCSample('wh_bbbb_tau1000mm_M25', '/WH_HToSSTobbbb_WToLNu_MH125_MS25_ctauS1000_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER', 19900),
    MCSample('wh_bbbb_tau0100mm_M25', '/WH_HToSSTobbbb_WToLNu_MH125_MS25_ctauS100_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',  20000),
    MCSample('wh_bbbb_tau0010mm_M25', '/WH_HToSSTobbbb_WToLNu_MH125_MS25_ctauS10_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',   20000),
    MCSample('wh_bbbb_tau0001mm_M25', '/WH_HToSSTobbbb_WToLNu_MH125_MS25_ctauS1_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',    20000),
    MCSample('wh_bbbb_tau0000mm_M40', '/WH_HToSSTobbbb_WToLNu_MH125_MS40_ctauS0_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',    19800),
    MCSample('wh_bbbb_tau1000mm_M40', '/WH_HToSSTobbbb_WToLNu_MH125_MS40_ctauS1000_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER', 20000),
    MCSample('wh_bbbb_tau0100mm_M40', '/WH_HToSSTobbbb_WToLNu_MH125_MS40_ctauS100_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',  20000),
    MCSample('wh_bbbb_tau0010mm_M40', '/WH_HToSSTobbbb_WToLNu_MH125_MS40_ctauS10_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',   19900),
    MCSample('wh_bbbb_tau0001mm_M40', '/WH_HToSSTobbbb_WToLNu_MH125_MS40_ctauS1_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',    20000)
]

zh_samples_4Tau = [
    MCSample('zh_4Tau_tau0000mm_M10', '/ZH_HToSSTo4Tau_ZToLL_MH125_MS10_ctauS0_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',    19900),
    MCSample('zh_4Tau_tau1000mm_M10', '/ZH_HToSSTo4Tau_ZToLL_MH125_MS10_ctauS1000_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER', 20000),
    MCSample('zh_4Tau_tau0100mm_M10', '/ZH_HToSSTo4Tau_ZToLL_MH125_MS10_ctauS100_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',  19800),
    MCSample('zh_4Tau_tau0010mm_M10', '/ZH_HToSSTo4Tau_ZToLL_MH125_MS10_ctauS10_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',   20000),
    MCSample('zh_4Tau_tau0001mm_M10', '/ZH_HToSSTo4Tau_ZToLL_MH125_MS10_ctauS1_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',    19900),
    MCSample('zh_4Tau_tau0000mm_M25', '/ZH_HToSSTo4Tau_ZToLL_MH125_MS25_ctauS0_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',    19600),
    MCSample('zh_4Tau_tau0100mm_M25', '/ZH_HToSSTo4Tau_ZToLL_MH125_MS25_ctauS100_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',  20000),
    MCSample('zh_4Tau_tau0010mm_M25', '/ZH_HToSSTo4Tau_ZToLL_MH125_MS25_ctauS10_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',   19900),
    MCSample('zh_4Tau_tau0001mm_M25', '/ZH_HToSSTo4Tau_ZToLL_MH125_MS25_ctauS1_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',    20000),
    MCSample('zh_4Tau_tau0000mm_M40', '/ZH_HToSSTo4Tau_ZToLL_MH125_MS40_ctauS0_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',    20000),
    MCSample('zh_4Tau_tau1000mm_M40', '/ZH_HToSSTo4Tau_ZToLL_MH125_MS40_ctauS1000_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER', 19700),
    MCSample('zh_4Tau_tau0100mm_M40', '/ZH_HToSSTo4Tau_ZToLL_MH125_MS40_ctauS100_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',  20000),
    MCSample('zh_4Tau_tau0010mm_M40', '/ZH_HToSSTo4Tau_ZToLL_MH125_MS40_ctauS10_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',   19900),
    MCSample('zh_4Tau_tau0001mm_M40', '/ZH_HToSSTo4Tau_ZToLL_MH125_MS40_ctauS1_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',    20000)
]

zh_samples_bbbb = [
    MCSample('zh_bbbb_tau0000mm_M10', '/ZH_HToSSTobbbb_ZToLL_MH125_MS10_ctauS0_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',    19800),
    MCSample('zh_bbbb_tau1000mm_M10', '/ZH_HToSSTobbbb_ZToLL_MH125_MS10_ctauS1000_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER', 20000),
    MCSample('zh_bbbb_tau0100mm_M10', '/ZH_HToSSTobbbb_ZToLL_MH125_MS10_ctauS100_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',  20000),
    MCSample('zh_bbbb_tau0010mm_M10', '/ZH_HToSSTobbbb_ZToLL_MH125_MS10_ctauS10_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',   20000),
    MCSample('zh_bbbb_tau0001mm_M10', '/ZH_HToSSTobbbb_ZToLL_MH125_MS10_ctauS1_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',    20000),
    MCSample('zh_bbbb_tau0000mm_M25', '/ZH_HToSSTobbbb_ZToLL_MH125_MS25_ctauS0_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',    20000),
    MCSample('zh_bbbb_tau1000mm_M25', '/ZH_HToSSTobbbb_ZToLL_MH125_MS25_ctauS1000_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER', 20000),
    MCSample('zh_bbbb_tau0100mm_M25', '/ZH_HToSSTobbbb_ZToLL_MH125_MS25_ctauS100_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',  19900),
    MCSample('zh_bbbb_tau0010mm_M25', '/ZH_HToSSTobbbb_ZToLL_MH125_MS25_ctauS10_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',   20000),
    MCSample('zh_bbbb_tau0001mm_M25', '/ZH_HToSSTobbbb_ZToLL_MH125_MS25_ctauS1_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',    19800),
    MCSample('zh_bbbb_tau0000mm_M40', '/ZH_HToSSTobbbb_ZToLL_MH125_MS40_ctauS0_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',    20000),
    MCSample('zh_bbbb_tau1000mm_M40', '/ZH_HToSSTobbbb_ZToLL_MH125_MS40_ctauS1000_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER', 20000),
    MCSample('zh_bbbb_tau0100mm_M40', '/ZH_HToSSTobbbb_ZToLL_MH125_MS40_ctauS100_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',  20000),
    MCSample('zh_bbbb_tau0010mm_M40', '/ZH_HToSSTobbbb_ZToLL_MH125_MS40_ctauS10_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',   20000),
    MCSample('zh_bbbb_tau0001mm_M40', '/ZH_HToSSTobbbb_ZToLL_MH125_MS40_ctauS1_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER',    20000)
]

zh_samples_dddd = [
    MCSample('zh_dddd_tau0010mm_M25', '/ZH_HToSSTodddd_ZToLL_MH125_MS25_ctauS10_13TeV/kreis-group-space-DIGI-RECO-2-413386f6eddb08329706f28eff10fb19/USER', 20000)
]

for s in wh_samples_4Tau + wh_samples_bbbb + zh_samples_4Tau + zh_samples_bbbb + zh_samples_dddd:
    s.dbs_inst = 'phys03'
    s.xsec = 1e-3

auxiliary_background_samples = [
    MCSample('ttbaraux',  '/TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM', 10235840, nice='t#bar{t}', color=4, syst_frac=0.15, xsec=832.),
    ]

qcdpt_samples_not_used =[
    MCSample('qcdpt0005', '/QCD_Pt_5to10_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',      6991536, nice='QCD, 5 < #hat{p}_{T} < 10 GeV',      color=808, syst_frac=0.10, xsec=6.102e+10),
    MCSample('qcdpt0010', '/QCD_Pt_10to15_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v2/AODSIM',     6842800, nice='QCD, 10 < #hat{p}_{T} < 15 GeV',     color=808, syst_frac=0.10, xsec=5.888e+09),
    MCSample('qcdpt0015', '/QCD_Pt_15to30_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',    38425945, nice='QCD, 15 < #hat{p}_{T} < 30 GeV',     color=808, syst_frac=0.10, xsec=1.837e+09),
    MCSample('qcdpt0030', '/QCD_Pt_30to50_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',     9808025, nice='QCD, 30 < #hat{p}_{T} < 50 GeV',     color=808, syst_frac=0.10, xsec=1.409e+08),
    MCSample('qcdpt0050', '/QCD_Pt_50to80_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',     9775360, nice='QCD, 50 < #hat{p}_{T} < 80 GeV',     color=808, syst_frac=0.10, xsec=1.920e+07),
    MCSample('qcdpt0080', '/QCD_Pt_80to120_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',    6953590, nice='QCD, 80 < #hat{p}_{T} < 120 GeV',    color=808, syst_frac=0.10, xsec=2.763e+06),
    MCSample('qcdpt0120', '/QCD_Pt_120to170_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',   6848223, nice='QCD, 120 < #hat{p}_{T} < 300 GeV',   color=808, syst_frac=0.10, xsec=4.711e+05),
    ]

qcdpt_samples = [
    MCSample('qcdpt0170', '/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',   6918748, nice='QCD, 170 < #hat{p}_{T} < 300 GeV',   color=800, syst_frac=0.10, xsec=1.173e+05),
    MCSample('qcdpt0300', '/QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',   5968960, nice='QCD, 300 < #hat{p}_{T} < 470 GeV',   color=801, syst_frac=0.10, xsec=7.823e+03),
    MCSample('qcdpt0470', '/QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',   3977770, nice='QCD, 470 < #hat{p}_{T} < 600 GeV',   color=802, syst_frac=0.10, xsec=6.482e+02),
    MCSample('qcdpt0600', '/QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',   3979884, nice='QCD, 600 < #hat{p}_{T} < 800 GeV',   color=803, syst_frac=0.10, xsec=1.869e+02),
    MCSample('qcdpt0800', '/QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',  3973224, nice='QCD, 800 < #hat{p}_{T} < 1000 GeV',  color=804, syst_frac=0.10, xsec=3.229e+01),
    MCSample('qcdpt1000', '/QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM', 2967947, nice='QCD, 1000 < #hat{p}_{T} < 1400 GeV', color=805, syst_frac=0.10, xsec=9.418e+00),
    MCSample('qcdpt1400', '/QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',  395725, nice='QCD, 1400 < #hat{p}_{T} < 1800 GeV', color=806, syst_frac=0.10, xsec=8.427e-01),
    MCSample('qcdpt1800', '/QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',  393760, nice='QCD, 1800 < #hat{p}_{T} < 2400 GeV', color=807, syst_frac=0.10, xsec=1.149e-01),
    MCSample('qcdpt2400', '/QCD_Pt_2400to3200_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',  398452, nice='QCD, 2400 < #hat{p}_{T} < 3200 GeV', color=808, syst_frac=0.10, xsec=6.830e-03),
    MCSample('qcdpt3200', '/QCD_Pt_3200toInf_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',   391108, nice='QCD, #hat{p}_{T} > 3200 GeV',        color=809, syst_frac=0.10, xsec=1.654e-04),
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
    'qcd_samples_ext',
    'ttbar_samples',
    'mfv_signal_samples',
    'mfv_signal_samples_glu',
    'mfv_signal_samples_gluddbar',
    'mfv_signal_samples_lq2',
    'xx4j_samples',
    'wh_samples_4Tau',
    'wh_samples_bbbb',
    'zh_samples_4Tau',
    'zh_samples_bbbb',
    'zh_samples_dddd',
    'leptonic_background_samples',
#    'ttbar_systematics_samples',
    'auxiliary_background_samples',
    'qcdpt_samples_not_used',
    'qcdpt_samples',
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

JetHT2015D.add_dataset('ntuplev6p1_76x_nstlays3', '/JetHT/dquach-ntuplev6p1_76x_data-1a10619cdc6042d141a5a3a54b840554/USER', dbs_inst='phys03') #, 7607820) # 1311 files

def add_dataset_by_primary(ds_name, dataset, nevents_orig, **kwargs):
    x = registry.by_primary_dataset(dataset.split('/')[1])
    if len(x) != 1:
        raise ValueError('could not find sample for %s by primary dataset: %r' % (dataset, x))
    sample = x[0]
    sample.add_dataset(ds_name, dataset, nevents_orig, **kwargs)

_adbp = add_dataset_by_primary
_adbp3 = partial(_adbp, dbs_inst='phys03')

# for x in $(<a.txt); echo _adbp3\(\'\', \'${x}\', $(dass 3 nevents $x)\) \# $(dass 3 file $x | wl) files

_adbp3('sim', '/mfv_neu_tau00100um_M0400/tucker-sim_10k-c66f4a7649a68ea5b6afdf05975ce9cf/USER', 10000) # 50 files
_adbp3('sim', '/mfv_neu_tau00100um_M0800/tucker-sim_10k-c66f4a7649a68ea5b6afdf05975ce9cf/USER', 10000) # 50 files
_adbp3('sim', '/mfv_neu_tau00100um_M1200/tucker-sim_10k-c66f4a7649a68ea5b6afdf05975ce9cf/USER',  9800) # 49 files
_adbp3('sim', '/mfv_neu_tau00100um_M1600/tucker-sim_10k-c66f4a7649a68ea5b6afdf05975ce9cf/USER', 10000) # 50 files
_adbp3('sim', '/mfv_neu_tau00300um_M0400/tucker-sim_10k-c66f4a7649a68ea5b6afdf05975ce9cf/USER', 10000) # 50 files
_adbp3('sim', '/mfv_neu_tau00300um_M0800/tucker-sim_10k-c66f4a7649a68ea5b6afdf05975ce9cf/USER', 10000) # 50 files
_adbp3('sim', '/mfv_neu_tau00300um_M1200/tucker-sim_10k-c66f4a7649a68ea5b6afdf05975ce9cf/USER', 10000) # 50 files
_adbp3('sim', '/mfv_neu_tau00300um_M1600/tucker-sim_10k-c66f4a7649a68ea5b6afdf05975ce9cf/USER',  9400) # 47 files
_adbp3('sim', '/mfv_neu_tau01000um_M0400/tucker-sim_10k-c66f4a7649a68ea5b6afdf05975ce9cf/USER',  9800) # 49 files
_adbp3('sim', '/mfv_neu_tau01000um_M0800/tucker-sim_10k-c66f4a7649a68ea5b6afdf05975ce9cf/USER', 10000) # 50 files
_adbp3('sim', '/mfv_neu_tau01000um_M1200/tucker-sim_10k-c66f4a7649a68ea5b6afdf05975ce9cf/USER', 10000) # 50 files
_adbp3('sim', '/mfv_neu_tau01000um_M1600/tucker-sim_10k-c66f4a7649a68ea5b6afdf05975ce9cf/USER', 10000) # 50 files
_adbp3('sim', '/mfv_neu_tau10000um_M0400/tucker-sim_10k-c66f4a7649a68ea5b6afdf05975ce9cf/USER',  9600) # 48 files
_adbp3('sim', '/mfv_neu_tau10000um_M0800/tucker-sim_10k-c66f4a7649a68ea5b6afdf05975ce9cf/USER', 10000) # 50 files
_adbp3('sim', '/mfv_neu_tau10000um_M1200/tucker-sim_10k-c66f4a7649a68ea5b6afdf05975ce9cf/USER',  9600) # 48 files
_adbp3('sim', '/mfv_neu_tau10000um_M1600/tucker-sim_10k-c66f4a7649a68ea5b6afdf05975ce9cf/USER',  9600) # 48 files

# can't use _adbp3 because of the -ext datasets that have same primary
qcdht0500.add_dataset('ntuplev6p1_76x_nstlays3', '/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/dquach-ntuplev6p1_76x_nstlays3_try3-0fbadeb0e2a98a2143c6c3d63c2148cf/USER',     45715) # 100 files
qcdht0700.add_dataset('ntuplev6p1_76x_nstlays3', '/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/dquach-ntuplev6p1_76x_nstlays3_try2-0563a6174ccfef7445b47a1adf52e04e/USER',  4408678) # 204 files
qcdht1000.add_dataset('ntuplev6p1_76x_nstlays3', '/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/dquach-ntuplev6p1_76x_nstlays3_try2-9c87ea2e204738f8e66398eae2e1ceea/USER', 5039738) # 206 files
qcdht1500.add_dataset('ntuplev6p1_76x_nstlays3', '/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/dquach-ntuplev6p1_76x_nstlays3_try2-0e21961f02f2bbcb31e97c1d56ed84b9/USER', 3952153) # 160 files
qcdht2000.add_dataset('ntuplev6p1_76x_nstlays3', '/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/dquach-ntuplev6p1_76x_nstlays3_try2-d07a09819adfc59c1cee757ffeb6279f/USER',  1981228) # 81 files

_adbp3('ntuplev6p1_76x_nstlays3', '/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/dquach-ntuplev6p1_76x_nstlays3_try3-a058b539af07e93a090902e6078c0efe/USER', 1333601) # 193 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_neu_tau00100um_M0300/dquach-ntuplev6p1_76x_signal-1caceb02a3d5bd67eebd50c7af8df8ef/USER', 1498) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_neu_tau00100um_M0400/dquach-ntuplev6p1_76x_signal-e5d3e1bd9d3a61a647fe70f1a1ca6c3a/USER', 3802) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_neu_tau00100um_M0800/dquach-ntuplev6p1_76x_signal-b329d925cd4c8251bb3cb039b346ca77/USER', 9900) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_neu_tau00100um_M1200/dquach-ntuplev6p1_76x_signal-5aa39285cbad602533211a7d6df1b80f/USER', 9996) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_neu_tau00100um_M1600/dquach-ntuplev6p1_76x_signal-0599f3e6321ef9d5a2d84a03640adba2/USER', 10000) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_neu_tau00300um_M0300/dquach-ntuplev6p1_76x_signal-e33ddfec4e1fd18a3bfc6a82773bc924/USER', 1492) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_neu_tau00300um_M0400/dquach-ntuplev6p1_76x_signal-9a9865053faa67854dc4a664150b6f6d/USER', 3672) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_neu_tau00300um_M0800/dquach-ntuplev6p1_76x_signal-9d427f650437d32c08db085488094ddd/USER', 9877) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_neu_tau00300um_M1200/dquach-ntuplev6p1_76x_signal-f522d03f9ec6059281e0035501845b6d/USER', 9995) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_neu_tau00300um_M1600/dquach-ntuplev6p1_76x_signal-001f599dfdcb3b68990363c74df28915/USER', 10000) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_neu_tau01000um_M0300/dquach-ntuplev6p1_76x_signal-ca77c05e10ef66beabf854ad2b028093/USER', 1463) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_neu_tau01000um_M0400/dquach-ntuplev6p1_76x_signal-cbf664a5aaf421e5d79d10014555cb3a/USER', 3635) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_neu_tau01000um_M0800/dquach-ntuplev6p1_76x_signal-3149177ec8fbf6168b030c8a999b7d3e/USER', 9883) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_neu_tau01000um_M1200/dquach-ntuplev6p1_76x_signal-e85a28b0bcf63447a9168a6e9f8db6d9/USER', 9997) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_neu_tau01000um_M1600/dquach-ntuplev6p1_76x_signal-681c54d8e6d93272dcf80b3406bf2fb8/USER', 10000) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_neu_tau10000um_M0300/dquach-ntuplev6p1_76x_signal-718936e91338fb279377dfd1442dbae9/USER', 1175) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_neu_tau10000um_M0400/dquach-ntuplev6p1_76x_signal-2016d8d097c2c236eef9b2b8fb56b2ef/USER', 2980) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_neu_tau10000um_M0800/dquach-ntuplev6p1_76x_signal-e8c19f7c227f1fc4127d581cabe8fd48/USER', 9794) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_neu_tau10000um_M1200/dquach-ntuplev6p1_76x_signal-415a49ef6dbc56dac8323b114f277dc4/USER', 9992) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_neu_tau10000um_M1600/dquach-ntuplev6p1_76x_signal-6ec162923e0141b77281b147224d5aae/USER', 10000) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_glu_tau00100um_M0300/dquach-ntuplev6p1_76x_signal-9dc542067e5b0622e19ec15eb57fc3fb/USER', 1475) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_glu_tau00100um_M0400/dquach-ntuplev6p1_76x_signal-ddeb95b46eb7cdd4c61ab23f4a9cd780/USER', 3760) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_glu_tau00100um_M0800/dquach-ntuplev6p1_76x_signal-1af329077aeaa553bd124dde75099247/USER', 9885) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_glu_tau00100um_M1200/dquach-ntuplev6p1_76x_signal-64b9754f9a3b0bb17815926089141019/USER', 9988) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_glu_tau00100um_M1600/dquach-ntuplev6p1_76x_signal-c8bff750800916e474a1dc19020367b8/USER', 9992) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_glu_tau00300um_M0300/dquach-ntuplev6p1_76x_signal-abd9f61e188d7ac92868b2417a2142c9/USER', 1435) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_glu_tau00300um_M0400/dquach-ntuplev6p1_76x_signal-93fa0c249f3b49c8dce0fed7e9d5c2f5/USER', 3721) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_glu_tau00300um_M0800/dquach-ntuplev6p1_76x_signal-e27f3400a041816e538ff9423cffbbd6/USER', 9870) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_glu_tau00300um_M1200/dquach-ntuplev6p1_76x_signal-7e1d38694734dfa6678795cb899a1d9e/USER', 9995) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_glu_tau00300um_M1600/dquach-ntuplev6p1_76x_signal-45e5b234fb6136a620bf959943ea327e/USER', 9995) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_glu_tau01000um_M0300/dquach-ntuplev6p1_76x_signal-8f27909919a6f4594e5a1460945220be/USER', 1377) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_glu_tau01000um_M0400/dquach-ntuplev6p1_76x_signal-55edba3f75d79be0e885c36145ff572c/USER', 3550) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_glu_tau01000um_M0800/dquach-ntuplev6p1_76x_signal-744d399656e7e20911d54b80e008da7d/USER', 9867) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_glu_tau01000um_M1200/dquach-ntuplev6p1_76x_signal-2fe2edfa78ceed33e0d8ab9d18573948/USER', 9995) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_glu_tau01000um_M1600/dquach-ntuplev6p1_76x_signal-a53c281ab3d0a8cfcbc153232b8c764b/USER', 9995) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_glu_tau10000um_M0300/dquach-ntuplev6p1_76x_signal-9ea8d1d34f8ca9859cce06791d460c70/USER', 1107) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_glu_tau10000um_M0400/dquach-ntuplev6p1_76x_signal-d9f78561fa591a992a568e21d189cea3/USER', 2875) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_glu_tau10000um_M0800/dquach-ntuplev6p1_76x_signal-53851d69c5566a20775234a6710cd33a/USER', 9753) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_glu_tau10000um_M1200/dquach-ntuplev6p1_76x_signal-c747e31529dce08f453e15888bdf70dc/USER', 9981) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_glu_tau10000um_M1600/dquach-ntuplev6p1_76x_signal-fa9fa26f6facf759c161b03916dce97d/USER', 9998) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_gluddbar_tau00100um_M0300/dquach-ntuplev6p1_76x_signal-e66bb9168428415fb263fca3b5fb0733/USER', 2371) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_gluddbar_tau00100um_M0400/dquach-ntuplev6p1_76x_signal-1f57dfe3d763bfea6fc428b86641f264/USER', 5652) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_gluddbar_tau00100um_M0800/dquach-ntuplev6p1_76x_signal-88fc60676aba9793b8c2566a68c27d97/USER', 9902) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_gluddbar_tau00100um_M1200/dquach-ntuplev6p1_76x_signal-6f40d8bc0992416238c33251ada4f169/USER', 9989) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_gluddbar_tau00100um_M1600/dquach-ntuplev6p1_76x_signal-df54990a9905b5521b9ee6d73302ff52/USER', 9995) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_gluddbar_tau00300um_M0300/dquach-ntuplev6p1_76x_signal-4d6298891bb43ad02b39c5ad15b5bcfe/USER', 2434) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_gluddbar_tau00300um_M0400/dquach-ntuplev6p1_76x_signal-fc08315fe7e36c83b2e1e9cc1b7150d7/USER', 5657) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_gluddbar_tau00300um_M0800/dquach-ntuplev6p1_76x_signal-dec85a8f6278ca357910c7d3df5059fa/USER', 9873) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_gluddbar_tau00300um_M1200/dquach-ntuplev6p1_76x_signal-7ce1d1bb80c0c507565df96e84118be4/USER', 9982) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_gluddbar_tau00300um_M1600/dquach-ntuplev6p1_76x_signal-37d935e03ac74d8cdaf48015d63975cf/USER', 9994) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_gluddbar_tau01000um_M0300/dquach-ntuplev6p1_76x_signal-3691658cfedeccd5f77f48989979db66/USER', 2301) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_gluddbar_tau01000um_M0400/dquach-ntuplev6p1_76x_signal-6afa5e6959a6556a4321f14d8ee9450c/USER', 5594) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_gluddbar_tau01000um_M0800/dquach-ntuplev6p1_76x_signal-186921026f83a74458d21849238da6ce/USER', 9890) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_gluddbar_tau01000um_M1200/dquach-ntuplev6p1_76x_signal-4be75f5c89af6ed93d81a76240f3fa72/USER', 9984) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_gluddbar_tau01000um_M1600/dquach-ntuplev6p1_76x_signal-bfbf86e25879769749f195b150576ae0/USER', 9991) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_gluddbar_tau10000um_M0300/dquach-ntuplev6p1_76x_signal-be63a0c4ea244b54d7056636656f7da5/USER', 1971) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_gluddbar_tau10000um_M0400/dquach-ntuplev6p1_76x_signal-6bf18d339333514e3cffd2447538b19f/USER', 4884) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_gluddbar_tau10000um_M0800/dquach-ntuplev6p1_76x_signal-c656d084133c2b54f8f31d0f6e7716cb/USER', 9871) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_gluddbar_tau10000um_M1200/dquach-ntuplev6p1_76x_signal-8769f088e8c10378c65d231b8f8048f0/USER', 9985) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_gluddbar_tau10000um_M1600/dquach-ntuplev6p1_76x_signal-139a0a8554afc40d3b5792ab909aa5f9/USER', 9995) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_lq2_tau00100um_M0300/dquach-ntuplev6p1_76x_signal-b03b5e1ecd80a295e5a4087026a83e4e/USER', 1043) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_lq2_tau00100um_M0400/dquach-ntuplev6p1_76x_signal-5d0848a4672e2f89bc7f84e2fa13e382/USER', 2243) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_lq2_tau00100um_M0800/dquach-ntuplev6p1_76x_signal-a494c952c9dd420ed62fad1ffa279357/USER', 7770) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_lq2_tau00100um_M1200/dquach-ntuplev6p1_76x_signal-6722aa3dbeda52784d90e35f690acdb6/USER', 9528) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_lq2_tau00100um_M1600/dquach-ntuplev6p1_76x_signal-cf57228c96840a239792e727215742fd/USER', 9863) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_lq2_tau00300um_M0300/dquach-ntuplev6p1_76x_signal-93b7c4c93a8163f5fa24f3bec52e5e48/USER', 1004) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_lq2_tau00300um_M0400/dquach-ntuplev6p1_76x_signal-f8cea61c9492606df578edb2789488fd/USER', 2232) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_lq2_tau00300um_M0800/dquach-ntuplev6p1_76x_signal-ecaace5a5ef9336c4a8771c449f4a4c9/USER', 7854) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_lq2_tau00300um_M1200/dquach-ntuplev6p1_76x_signal-dda29fbb337c516058f3261440324faa/USER', 9541) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_lq2_tau00300um_M1600/dquach-ntuplev6p1_76x_signal-3369d62f82751ffc681c2408dc617565/USER', 9875) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_lq2_tau01000um_M0300/dquach-ntuplev6p1_76x_signal-f045e74d4f029a0914a1d366274a8fe1/USER', 1043) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_lq2_tau01000um_M0400/dquach-ntuplev6p1_76x_signal-d314a48458c661ff344a01a0151813d6/USER', 2180) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_lq2_tau01000um_M0800/dquach-ntuplev6p1_76x_signal-dfd5ed58a9ce35293af9677f058a103f/USER', 7830) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_lq2_tau01000um_M1200/dquach-ntuplev6p1_76x_signal-12da3101816b464335eea917398e3e4a/USER', 9501) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_lq2_tau01000um_M1600/dquach-ntuplev6p1_76x_signal-8da6225b3e6f3241b59cbb041365e294/USER', 9864) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_lq2_tau10000um_M0300/dquach-ntuplev6p1_76x_signal-1e04979f18261f39fabee222e00edfa3/USER', 1001) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_lq2_tau10000um_M0400/dquach-ntuplev6p1_76x_signal-58350a6def6efdee4c5d265867a6aecd/USER', 2052) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_lq2_tau10000um_M0800/dquach-ntuplev6p1_76x_signal-4d089d5b983498a0ce4791aae351195c/USER', 7718) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_lq2_tau10000um_M1200/dquach-ntuplev6p1_76x_signal-8788be2db4c55c09cdf534113476d28d/USER', 9466) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_lq2_tau10000um_M1600/dquach-ntuplev6p1_76x_signal-80a70aac7c29b2644f0554dfb5633277/USER', 9866) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/XXTo4J_M-700_CTau-1mm_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_nstlays3_try2-e1f22acb7f159b559521cda099d97246/USER', 9898) # 3 files
_adbp3('ntuplev6p1_76x_nstlays3', '/XXTo4J_M-700_CTau-10mm_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_nstlays3_try2-1417969c55c0055e05ba27e9c016eaa8/USER', 9867) # 2 files
_adbp3('ntuplev6p1_76x_nstlays3', '/XXTo4J_M-700_CTau-30mm_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_nstlays3_try2-ce3da775da3c8fa8b287f0e82d2fe17c/USER', 9836) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/XXTo4J_M-50_CTau-1mm_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_signal-d74b051ffbfbc2f624612d79e0c38289/USER', 92) # 2 files
_adbp3('ntuplev6p1_76x_nstlays3', '/XXTo4J_M-100_CTau-1mm_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_signal-f9fdb240138288e752f8c9263be528c6/USER', 681) # 2 files
_adbp3('ntuplev6p1_76x_nstlays3', '/XXTo4J_M-300_CTau-1mm_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_signal-fef163ae8f4dfab65a01043078f3dedb/USER', 4058) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/XXTo4J_M-1500_CTau-1mm_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_signal-e801807342421d24a3e95bb1f7ad0d7d/USER', 9908) # 3 files


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

    if 0:
        from DBS import *
        for x in qcd_samples_ext:
            ds = x.dataset
            print ds
            print x.name, numevents_in_dataset(ds)

    if 1:
        for x,y in zip(qcd_samples, qcd_samples_ext):
            print x.name, x.int_lumi_orig/1000, '->', (x.int_lumi_orig + y.int_lumi_orig)/1000

