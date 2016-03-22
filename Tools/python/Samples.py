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
    'ttbar_samples',
    'mfv_signal_samples',
    'xx4j_samples',
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

JetHT2015D.add_dataset('ntuplev6p1_76x', '/JetHT/tucker-ntuplev6p1_76x-1c7d7cc72ce161506ace63027d8999cf/USER', dbs_inst='phys03') #, 7607820) # 1312 files

def add_dataset_by_primary(ds_name, dataset, nevents_orig, **kwargs):
    x = registry.by_primary_dataset(dataset.split('/')[1])
    if len(x) != 1:
        raise ValueError('could not find sample for %s by primary dataset: %r' % (dataset, x))
    sample = x[0]
    sample.add_dataset(ds_name, dataset, nevents_orig, **kwargs)

_adbp = add_dataset_by_primary
_adbp3 = partial(_adbp, dbs_inst='phys03')

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

_adbp3('ntuplev6p1_76x', '/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/tucker-ntuplev6p1_76x-e0115cf27c092c2dd18b3e7b858a8124/USER',     44386) # 99 files, 102 expected
_adbp3('ntuplev6p1_76x', '/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/tucker-ntuplev6p1_76x-0647f73cce69e58d0aef5913afbb0f3c/USER', 5022354) # 212 files, 213 expected
_adbp3('ntuplev6p1_76x', '/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/tucker-ntuplev6p1_76x-94e89177941e8a89c5cdccd7b741b65c/USER', 3952153) # 160 files
_adbp3('ntuplev6p1_76x', '/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/tucker-ntuplev6p1_76x-4b20a26f36e3365f106971e9e5d3e060/USER',  1981228) # 94 files
_adbp3('ntuplev6p1_76x', '/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/tucker-ntuplev6p1_76x-b4b7f8e9859e632440c4bc9123183328/USER',          1340337) # 200 files, 201 expected

_adbp3('ntuplev6p1_76x', '/QCD_Pt_120to170_TuneCUETP8M1_13TeV_pythia8/tucker-ntuplev6p1_76x-bf3f6923c6a1e33e227a5c6a07647fcf/USER',       204) # 35 files
_adbp3('ntuplev6p1_76x', '/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/tucker-ntuplev6p1_76x-b6026869a1234f510d99821d8da7b55b/USER',     53610) # 279 files
_adbp3('ntuplev6p1_76x', '/QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8/tucker-ntuplev6p1_76x-d894803de72f343a392766f8f329a33b/USER',   1742101) # 70 files
_adbp3('ntuplev6p1_76x', '/QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8/tucker-ntuplev6p1_76x-b284078fe3d600f740a3bb6af56f20dc/USER',   3927467) # 160 files
_adbp3('ntuplev6p1_76x', '/QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8/tucker-ntuplev6p1_76x-588c92d893fa2fa28d749325ab76bcc6/USER',   3977145) # 161 files
_adbp3('ntuplev6p1_76x', '/QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8/tucker-ntuplev6p1_76x-8658e6346d529fdf34bd17605838b711/USER',  3923304) # 158 files, 160 expected
_adbp3('ntuplev6p1_76x', '/QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8/tucker-ntuplev6p1_76x-295ade74294747edfc7070959e5d77a8/USER', 2967901) # 120 files
_adbp3('ntuplev6p1_76x', '/QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8/tucker-ntuplev6p1_76x-88521556180c8660af1db164e26afe25/USER',  395724) # 16 files
_adbp3('ntuplev6p1_76x', '/QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8/tucker-ntuplev6p1_76x-e1e737c071adad39805cb3f163d11d80/USER',  393760) # 16 files
_adbp3('ntuplev6p1_76x', '/QCD_Pt_2400to3200_TuneCUETP8M1_13TeV_pythia8/tucker-ntuplev6p1_76x-0cc79cc1e23b35a8c9c6b6251a8a2faa/USER',  398452) # 16 files
_adbp3('ntuplev6p1_76x', '/QCD_Pt_3200toInf_TuneCUETP8M1_13TeV_pythia8/tucker-ntuplev6p1_76x-ae2b65845f48e117e8b46ae58aaf58f7/USER',   391108) # 16 files
_adbp3('ntuplev6p1_76x', '/TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/tucker-ntuplev6p1_76x-0b35bc583e60a30fc1c2ec30c0581edb/USER', 268572) # 52 files

_adbp3('ntuplev6p1_76x', '/XXTo4J_M-50_CTau-1mm_TuneCUETP8M1_13TeV_pythia8/tucker-ntuplev6p1_76x-f9b4097bb7a54c8103604b804ce7cdb7/USER',         92) # 6 files
_adbp3('ntuplev6p1_76x', '/XXTo4J_M-50_CTau-10mm_TuneCUETP8M1_13TeV_pythia8/tucker-ntuplev6p1_76x-c90e1465c2b623fea09aecc3af07704a/USER',        85) # 2 files
_adbp3('ntuplev6p1_76x', '/XXTo4J_M-50_CTau-100mm_TuneCUETP8M1_13TeV_pythia8/tucker-ntuplev6p1_76x-c47a6ac26369ccb51d8b8d71050fa2e3/USER',       78) # 7 files
_adbp3('ntuplev6p1_76x', '/XXTo4J_M-50_CTau-1000mm_TuneCUETP8M1_13TeV_pythia8/tucker-ntuplev6p1_76x-e89528c1dc3cb30ccfcc31b7c438f2e2/USER',      16) # 4 files
_adbp3('ntuplev6p1_76x', '/XXTo4J_M-50_CTau-2000mm_TuneCUETP8M1_13TeV_pythia8/tucker-ntuplev6p1_76x-e08ef8f6ecfb588fe6286cbdc0e827d7/USER',       7) # 7 files
_adbp3('ntuplev6p1_76x', '/XXTo4J_M-100_CTau-1mm_TuneCUETP8M1_13TeV_pythia8/tucker-ntuplev6p1_76x-9157dc87b1a724debba43eac81186a47/USER',       681) # 6 files
_adbp3('ntuplev6p1_76x', '/XXTo4J_M-100_CTau-3mm_TuneCUETP8M1_13TeV_pythia8/tucker-ntuplev6p1_76x-292c88bd1c25addecb0760bfb1376ac0/USER',       640) # 8 files
_adbp3('ntuplev6p1_76x', '/XXTo4J_M-100_CTau-10mm_TuneCUETP8M1_13TeV_pythia8/tucker-ntuplev6p1_76x-e0b8b66f7cde4f3058871d5ef96b9b63/USER',      569) # 10 files
_adbp3('ntuplev6p1_76x', '/XXTo4J_M-100_CTau-30mm_TuneCUETP8M1_13TeV_pythia8/tucker-ntuplev6p1_76x-063efd08b119ec4267c4041d759c0209/USER',      532) # 2 files
_adbp3('ntuplev6p1_76x', '/XXTo4J_M-100_CTau-100mm_TuneCUETP8M1_13TeV_pythia8/tucker-ntuplev6p1_76x-3143493defa88888681ee19445b6626f/USER',     533) # 8 files
_adbp3('ntuplev6p1_76x', '/XXTo4J_M-100_CTau-300mm_TuneCUETP8M1_13TeV_pythia8/tucker-ntuplev6p1_76x-28d95fbc8d3b69856cc25cff9babdc31/USER',     422) # 2 files
_adbp3('ntuplev6p1_76x', '/XXTo4J_M-100_CTau-1000mm_TuneCUETP8M1_13TeV_pythia8/tucker-ntuplev6p1_76x-4e6637a2a154a5754b64dfe5f04cf2b2/USER',    191) # 2 files
_adbp3('ntuplev6p1_76x', '/XXTo4J_M-100_CTau-2000mm_TuneCUETP8M1_13TeV_pythia8/tucker-ntuplev6p1_76x-797a6c6d7297c5e40a866a897b67ef2c/USER',    101) # 10 files
_adbp3('ntuplev6p1_76x', '/XXTo4J_M-300_CTau-1mm_TuneCUETP8M1_13TeV_pythia8/tucker-ntuplev6p1_76x-88ee13f995994e95586c99f2ef94b617/USER',      4058) # 3 files
_adbp3('ntuplev6p1_76x', '/XXTo4J_M-300_CTau-3mm_TuneCUETP8M1_13TeV_pythia8/tucker-ntuplev6p1_76x-35e4002f5fab3f14ccc4761f5b730858/USER',      3860) # 5 files
_adbp3('ntuplev6p1_76x', '/XXTo4J_M-300_CTau-10mm_TuneCUETP8M1_13TeV_pythia8/tucker-ntuplev6p1_76x-226b6399318d2517cb4cb5e41898ce16/USER',     3518) # 8 files
_adbp3('ntuplev6p1_76x', '/XXTo4J_M-300_CTau-30mm_TuneCUETP8M1_13TeV_pythia8/tucker-ntuplev6p1_76x-8e437a419002d7f956a1963a48db70eb/USER',     3406) # 1 files
_adbp3('ntuplev6p1_76x', '/XXTo4J_M-300_CTau-100mm_TuneCUETP8M1_13TeV_pythia8/tucker-ntuplev6p1_76x-d8b46478627cc2b54a917e34682f1293/USER',    3308) # 1 files
_adbp3('ntuplev6p1_76x', '/XXTo4J_M-300_CTau-300mm_TuneCUETP8M1_13TeV_pythia8/tucker-ntuplev6p1_76x-96df4f9e07803cc3e5639b9597b2174a/USER',    3318) # 3 files
_adbp3('ntuplev6p1_76x', '/XXTo4J_M-300_CTau-1000mm_TuneCUETP8M1_13TeV_pythia8/tucker-ntuplev6p1_76x-114eacd3d7f068bfa8868ef35784c47a/USER',   2290) # 4 files
_adbp3('ntuplev6p1_76x', '/XXTo4J_M-300_CTau-2000mm_TuneCUETP8M1_13TeV_pythia8/tucker-ntuplev6p1_76x-2e1a7c77524291d7d2dc2755c6ce2dc7/USER',   1250) # 1 files
_adbp3('ntuplev6p1_76x', '/XXTo4J_M-500_CTau-3mm_TuneCUETP8M1_13TeV_pythia8/tucker-ntuplev6p1_76x-82f966b78896869b623b89e4bf444372/USER',      9023) # 1 files
_adbp3('ntuplev6p1_76x', '/XXTo4J_M-500_CTau-10mm_TuneCUETP8M1_13TeV_pythia8/tucker-ntuplev6p1_76x-015b3bd7a1a2458f7d7adc755d8844e4/USER',     8755) # 14 files
_adbp3('ntuplev6p1_76x', '/XXTo4J_M-500_CTau-30mm_TuneCUETP8M1_13TeV_pythia8/tucker-ntuplev6p1_76x-42361dfcd6bfb1501ffd747583679f1a/USER',     8603) # 2 files
_adbp3('ntuplev6p1_76x', '/XXTo4J_M-500_CTau-300mm_TuneCUETP8M1_13TeV_pythia8/tucker-ntuplev6p1_76x-045654b38968f2f7633d58b3819ae252/USER',    7627) # 5 files
_adbp3('ntuplev6p1_76x', '/XXTo4J_M-500_CTau-1000mm_TuneCUETP8M1_13TeV_pythia8/tucker-ntuplev6p1_76x-9acceed2713d606588845640006bc620/USER',   6916) # 3 files
_adbp3('ntuplev6p1_76x', '/XXTo4J_M-500_CTau-2000mm_TuneCUETP8M1_13TeV_pythia8/tucker-ntuplev6p1_76x-b77d643a180853a59636d0f432dbec1c/USER',   4747) # 8 files
_adbp3('ntuplev6p1_76x', '/XXTo4J_M-700_CTau-1mm_TuneCUETP8M1_13TeV_pythia8/tucker-ntuplev6p1_76x-6bb5005fa7371e0479756687fa2ba839/USER',      9898) # 14 files
_adbp3('ntuplev6p1_76x', '/XXTo4J_M-700_CTau-3mm_TuneCUETP8M1_13TeV_pythia8/tucker-ntuplev6p1_76x-ab7499eaa1318f349931b6b3efb8ff0a/USER',      9898) # 7 files
_adbp3('ntuplev6p1_76x', '/XXTo4J_M-700_CTau-10mm_TuneCUETP8M1_13TeV_pythia8/tucker-ntuplev6p1_76x-62f1c6014997a1d25139bce0dc169918/USER',     9867) # 6 files
_adbp3('ntuplev6p1_76x', '/XXTo4J_M-700_CTau-30mm_TuneCUETP8M1_13TeV_pythia8/tucker-ntuplev6p1_76x-628393f9c8214a2457375a0a4000d98c/USER',     9836) # 8 files
_adbp3('ntuplev6p1_76x', '/XXTo4J_M-700_CTau-100mm_TuneCUETP8M1_13TeV_pythia8/tucker-ntuplev6p1_76x-5af6790c611b5e745cfb142bc5aad43c/USER',    9797) # 2 files
_adbp3('ntuplev6p1_76x', '/XXTo4J_M-700_CTau-300mm_TuneCUETP8M1_13TeV_pythia8/tucker-ntuplev6p1_76x-fca2539bceaf3acecd70fb2486237502/USER',    9778) # 8 files
_adbp3('ntuplev6p1_76x', '/XXTo4J_M-700_CTau-1000mm_TuneCUETP8M1_13TeV_pythia8/tucker-ntuplev6p1_76x-5dae55451c61561ee9acc07c3d5a23b7/USER',   9191) # 2 files
_adbp3('ntuplev6p1_76x', '/XXTo4J_M-1000_CTau-1mm_TuneCUETP8M1_13TeV_pythia8/tucker-ntuplev6p1_76x-917611d01ef163148948e92829d3cffa/USER',     9992) # 6 files
_adbp3('ntuplev6p1_76x', '/XXTo4J_M-1000_CTau-3mm_TuneCUETP8M1_13TeV_pythia8/tucker-ntuplev6p1_76x-b78195926141042444493e66a0be508a/USER',     9996) # 6 files
_adbp3('ntuplev6p1_76x', '/XXTo4J_M-1000_CTau-30mm_TuneCUETP8M1_13TeV_pythia8/tucker-ntuplev6p1_76x-79d79b82b9656b42b3e578c170a3ebc4/USER',    9985) # 1 files
_adbp3('ntuplev6p1_76x', '/XXTo4J_M-1000_CTau-300mm_TuneCUETP8M1_13TeV_pythia8/tucker-ntuplev6p1_76x-15792144f60fa89556c06541c7a6119a/USER',   9989) # 5 files
_adbp3('ntuplev6p1_76x', '/XXTo4J_M-1000_CTau-1000mm_TuneCUETP8M1_13TeV_pythia8/tucker-ntuplev6p1_76x-569866f20b843a8df81cf8d073c69d37/USER',  9874) # 2 files
_adbp3('ntuplev6p1_76x', '/XXTo4J_M-1000_CTau-2000mm_TuneCUETP8M1_13TeV_pythia8/tucker-ntuplev6p1_76x-ecf0abbf20485f7b560e58116555b1eb/USER',  9057) # 4 files
_adbp3('ntuplev6p1_76x', '/XXTo4J_M-1500_CTau-1mm_TuneCUETP8M1_13TeV_pythia8/tucker-ntuplev6p1_76x-afac74b301c6731dfb724c051c044be0/USER',     9908) # 10 files
_adbp3('ntuplev6p1_76x', '/XXTo4J_M-1500_CTau-10mm_TuneCUETP8M1_13TeV_pythia8/tucker-ntuplev6p1_76x-9e2923665f84b6d07f0d38efa31d19c8/USER',   10000) # 2 files
_adbp3('ntuplev6p1_76x', '/XXTo4J_M-1500_CTau-30mm_TuneCUETP8M1_13TeV_pythia8/tucker-ntuplev6p1_76x-94cfb85c8ab3834139b9f6bff70e033a/USER',   10000) # 1 files
_adbp3('ntuplev6p1_76x', '/XXTo4J_M-1500_CTau-300mm_TuneCUETP8M1_13TeV_pythia8/tucker-ntuplev6p1_76x-ef73e504f043c5648b6eac1b5729f4dd/USER',  10000) # 11 files
_adbp3('ntuplev6p1_76x', '/XXTo4J_M-1500_CTau-1000mm_TuneCUETP8M1_13TeV_pythia8/tucker-ntuplev6p1_76x-5935238b7a22aa241c0ccffc39a563fd/USER',  9706) # 2 files
_adbp3('ntuplev6p1_76x', '/XXTo4J_M-3000_CTau-3mm_TuneCUETP8M1_13TeV_pythia8/tucker-ntuplev6p1_76x-cb727d92bcf1631b75f95e9b112e97df/USER',    10000) # 5 files
_adbp3('ntuplev6p1_76x', '/XXTo4J_M-3000_CTau-10mm_TuneCUETP8M1_13TeV_pythia8/tucker-ntuplev6p1_76x-b021ce889e311932af3cf23c67b0a641/USER',   10000) # 10 files
_adbp3('ntuplev6p1_76x', '/XXTo4J_M-3000_CTau-30mm_TuneCUETP8M1_13TeV_pythia8/tucker-ntuplev6p1_76x-a85a233660c807856cd919d47faa3bad/USER',   10000) # 2 files
_adbp3('ntuplev6p1_76x', '/XXTo4J_M-3000_CTau-100mm_TuneCUETP8M1_13TeV_pythia8/tucker-ntuplev6p1_76x-f2bbd6d5257377b5064e3ca401aabefa/USER',  10000) # 1 files
_adbp3('ntuplev6p1_76x', '/XXTo4J_M-3000_CTau-300mm_TuneCUETP8M1_13TeV_pythia8/tucker-ntuplev6p1_76x-1e4e4d0d01b21b245dfee3a408aa06dd/USER',   9384) # 10 files
_adbp3('ntuplev6p1_76x', '/XXTo4J_M-3000_CTau-1000mm_TuneCUETP8M1_13TeV_pythia8/tucker-ntuplev6p1_76x-607df008a4269dd1ee84ea880fc4a85b/USER',  9994) # 6 files
_adbp3('ntuplev6p1_76x', '/XXTo4J_M-3000_CTau-2000mm_TuneCUETP8M1_13TeV_pythia8/tucker-ntuplev6p1_76x-8af4542fc829253f3ed7e24687ddeb1a/USER',  9916) # 1 files

_adbp3('ntuplev6p1_76x_errdxy40um', '/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy40um-4da1d8540d4ceb2e0540f019c2f73ab2/USER', 53610)
_adbp3('ntuplev6p1_76x_errdxy40um', '/QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy40um-ceb5b86b1f65795fc17f14c6e4af8269/USER', 1742101)
_adbp3('ntuplev6p1_76x_errdxy40um', '/QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy40um-dfe88c023f77b94b4006c7d37b0e7079/USER', 3927467)
_adbp3('ntuplev6p1_76x_errdxy40um', '/QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy40um-ccdf5da9331e9d81b86d4afa8a0c7533/USER', 3977145)
_adbp3('ntuplev6p1_76x_errdxy40um', '/QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy40um-4371d7f6187339295145946d6328aad4/USER', 3972910)
_adbp3('ntuplev6p1_76x_errdxy40um', '/QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy40um-e25df1220a62e94aa1ca01f6ccdf2491/USER', 2967901)
_adbp3('ntuplev6p1_76x_errdxy40um', '/QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy40um-e2045f192f4f2224924dc2fafb65a279/USER', 395724)
_adbp3('ntuplev6p1_76x_errdxy40um', '/QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy40um-f0392668ac399a6e3eb1135dd3fce3f1/USER', 393760)
_adbp3('ntuplev6p1_76x_errdxy40um', '/QCD_Pt_2400to3200_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy40um-d62a6986d23f8d0d633ad4e36a61ed57/USER', 398452)
_adbp3('ntuplev6p1_76x_errdxy40um', '/QCD_Pt_3200toInf_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy40um-e66a33c4ec45334c8f2616b957ebccc9/USER', 391108)
_adbp3('ntuplev6p1_76x_errdxy40um', '/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/dquach-ntuplev6p1_76x_errdxy40um-1d817e9fc44c5e503b10502d4393e734/USER', 1340337)
_adbp3('ntuplev6p1_76x_errdxy40um', '/mfv_neu_tau00100um_M0800/dquach-ntuplev6p1_76x_errdxy40um-88c3a23e8c85cfe0e0f86912abaf938c/USER', 9890)
_adbp3('ntuplev6p1_76x_errdxy40um', '/mfv_neu_tau00300um_M0800/dquach-ntuplev6p1_76x_errdxy40um-666665b8e6f40626bb5b8db2ea904cf7/USER', 9891)
_adbp3('ntuplev6p1_76x_errdxy40um', '/mfv_neu_tau01000um_M0800/dquach-ntuplev6p1_76x_errdxy40um-05b4a9678d8777331b8a0c5520cf852d/USER', 9898)
_adbp3('ntuplev6p1_76x_errdxy40um', '/mfv_neu_tau10000um_M0800/dquach-ntuplev6p1_76x_errdxy40um-53d78ec2c86c4daa7d929ad467778f45/USER', 9850)
_adbp3('ntuplev6p1_76x_errdxy40um', '/XXTo4J_M-700_CTau-1mm_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy40um-f13e18c9a9a22b907e1243cef11ae437/USER', 9898)
_adbp3('ntuplev6p1_76x_errdxy40um', '/XXTo4J_M-700_CTau-10mm_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy40um-b74a4f4279ececa08cc9fb10b62aee0a/USER', 9867)
_adbp3('ntuplev6p1_76x_errdxy40um', '/XXTo4J_M-700_CTau-30mm_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy40um-aa4a31c5e4bf3001eae9ca01194bc626/USER', 9836)

_adbp3('ntuplev6p1_76x_errdxy60um', '/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy60um-91b3de7777a20a116991d7c846a7737c/USER', 52045)
_adbp3('ntuplev6p1_76x_errdxy60um', '/QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy60um-22deb0b605992cbf3a557ee4da07a79f/USER', 1742101)
_adbp3('ntuplev6p1_76x_errdxy60um', '/QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy60um-20e5a0ae8ad9a8ab3810bcf1bab8f28c/USER', 3927467)
_adbp3('ntuplev6p1_76x_errdxy60um', '/QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy60um-ea9eddf2e8a7b74af5d7c02683925eb7/USER', 3977145)
_adbp3('ntuplev6p1_76x_errdxy60um', '/QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy60um-2e1375c3088973e170440f83e1ba45d1/USER', 3972910)
_adbp3('ntuplev6p1_76x_errdxy60um', '/QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy60um-38e1d304909a69e5a09596e32e045a8f/USER', 2967901)
_adbp3('ntuplev6p1_76x_errdxy60um', '/QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy60um-05dcc6174012ffc553b300a272b3f6e7/USER', 395724)
_adbp3('ntuplev6p1_76x_errdxy60um', '/QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy60um-958bfd68a4f9eb59648049020cbadacb/USER', 393760)
_adbp3('ntuplev6p1_76x_errdxy60um', '/QCD_Pt_2400to3200_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy60um-2ae2a15f056add18cc650686cf2b8ca2/USER', 398452)
_adbp3('ntuplev6p1_76x_errdxy60um', '/QCD_Pt_3200toInf_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy60um-48b620e4d09a5ca33f0bae5389b7b63d/USER', 391108)
_adbp3('ntuplev6p1_76x_errdxy60um', '/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/dquach-ntuplev6p1_76x_errdxy60um-7812398103dcff8dbb4ce893f00c7d06/USER', 1340337)
_adbp3('ntuplev6p1_76x_errdxy60um', '/mfv_neu_tau00100um_M0800/dquach-ntuplev6p1_76x_errdxy60um-c67cb707c78f4a10b0c53e88deedf1a0/USER', 9890)
_adbp3('ntuplev6p1_76x_errdxy60um', '/mfv_neu_tau00300um_M0800/dquach-ntuplev6p1_76x_errdxy60um-491405975aee5daaefc3b0bcd44a436e/USER', 9891)
_adbp3('ntuplev6p1_76x_errdxy60um', '/mfv_neu_tau01000um_M0800/dquach-ntuplev6p1_76x_errdxy60um-6f7f74c240d56c0cd30cf9014acf50c6/USER', 9898)
_adbp3('ntuplev6p1_76x_errdxy60um', '/mfv_neu_tau10000um_M0800/dquach-ntuplev6p1_76x_errdxy60um-2b9afd24bc1e0a05e5b142f761add582/USER', 9850)
_adbp3('ntuplev6p1_76x_errdxy60um', '/XXTo4J_M-700_CTau-1mm_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy60um-3d40bf4d695fa22fb1416c87780214e4/USER', 9898)
_adbp3('ntuplev6p1_76x_errdxy60um', '/XXTo4J_M-700_CTau-10mm_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy60um-9c8c52f2a8b5478e6a1bde8b46ce75f0/USER', 9867)
_adbp3('ntuplev6p1_76x_errdxy60um', '/XXTo4J_M-700_CTau-30mm_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy60um-a6f46afddd4427aa0a050bbb88100268/USER', 9836)

_adbp3('ntuplev6p1_76x_errdxy80um', '/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy80um-fba1e294e34860fd7087bf7b34ee33a2/USER', 53610)
_adbp3('ntuplev6p1_76x_errdxy80um', '/QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy80um-6c65808b2dc01c0a96d9002bcb69581d/USER', 1742101)
_adbp3('ntuplev6p1_76x_errdxy80um', '/QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy80um-95642f5b3777eb128b637e88973dbe96/USER', 3927467)
_adbp3('ntuplev6p1_76x_errdxy80um', '/QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy80um-9e30edf0aaedec05930d7c9c73edd7d7/USER', 3977145)
_adbp3('ntuplev6p1_76x_errdxy80um', '/QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy80um-7a3fa103f3a89b4a3526857744ffccc3/USER', 3972910)
_adbp3('ntuplev6p1_76x_errdxy80um', '/QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy80um-4c1848eac810163191d33b3ed7159596/USER', 2967901)
_adbp3('ntuplev6p1_76x_errdxy80um', '/QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy80um-9b75dc17463a5e540e622fce11b5b6f6/USER', 395724)
_adbp3('ntuplev6p1_76x_errdxy80um', '/QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy80um-ecca9f3ad07f110517e51470a71fa26f/USER', 393760)
_adbp3('ntuplev6p1_76x_errdxy80um', '/QCD_Pt_2400to3200_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy80um-6858c517c2e9dd040c26ad3f77843694/USER', 398452)
_adbp3('ntuplev6p1_76x_errdxy80um', '/QCD_Pt_3200toInf_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy80um-bc234359077b5e115c16b265c68a5727/USER', 391108)
_adbp3('ntuplev6p1_76x_errdxy80um', '/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/dquach-ntuplev6p1_76x_errdxy80um-2a09a0e9ae359650984c486345200e31/USER', 1340337)
_adbp3('ntuplev6p1_76x_errdxy80um', '/mfv_neu_tau00100um_M0800/dquach-ntuplev6p1_76x_errdxy80um-c0e400c1c0021bc5280bd2b894ebb57f/USER', 9890)
_adbp3('ntuplev6p1_76x_errdxy80um', '/mfv_neu_tau00300um_M0800/dquach-ntuplev6p1_76x_errdxy80um-98636f407dd5f8bdf1716cf127a861f3/USER', 9891)
_adbp3('ntuplev6p1_76x_errdxy80um', '/mfv_neu_tau01000um_M0800/dquach-ntuplev6p1_76x_errdxy80um-49759d56106f4b9a786e0c9aa0633266/USER', 9898)
_adbp3('ntuplev6p1_76x_errdxy80um', '/mfv_neu_tau10000um_M0800/dquach-ntuplev6p1_76x_errdxy80um-4f514c5203e4449c26a169043ce152fb/USER', 9850)
_adbp3('ntuplev6p1_76x_errdxy80um', '/XXTo4J_M-700_CTau-1mm_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy80um-5eb42a7a46211c6c0fca8fcf216caafc/USER', 9898)
_adbp3('ntuplev6p1_76x_errdxy80um', '/XXTo4J_M-700_CTau-10mm_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy80um-a30d114a8c311a2ec489cc8f2f1a330b/USER', 9867)
_adbp3('ntuplev6p1_76x_errdxy80um', '/XXTo4J_M-700_CTau-30mm_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy80um-a9c18c86b0f9bf265ee58aa3ec8c6ac3/USER', 9836)

_adbp3('ntuplev6p1_76x_errdxy100um', '/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy100um-3f898ecc72b529af310864836a820094/USER', 53610)
_adbp3('ntuplev6p1_76x_errdxy100um', '/QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy100um-d3d0bcf04b9526b865407d16a3b97c7c/USER', 1742101)
_adbp3('ntuplev6p1_76x_errdxy100um', '/QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy100um-5cc3b3a52760c0c6f255ab90def06bbd/USER', 3927467)
_adbp3('ntuplev6p1_76x_errdxy100um', '/QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy100um-589f83ba34683c5e13e3c615a0ccc277/USER', 3977145)
_adbp3('ntuplev6p1_76x_errdxy100um', '/QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy100um-e0c7f88220a92d9f621dbef8125f224e/USER', 3972910)
_adbp3('ntuplev6p1_76x_errdxy100um', '/QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy100um-edec7d14ac01f5ef9d842c89a459031f/USER', 2967901)
_adbp3('ntuplev6p1_76x_errdxy100um', '/QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy100um-c33d7ecb126bf00e3a8fd5a9ad3ee06e/USER', 395724)
_adbp3('ntuplev6p1_76x_errdxy100um', '/QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy100um-bfc417815999ea26c7e91436bfd2aac3/USER', 393760)
_adbp3('ntuplev6p1_76x_errdxy100um', '/QCD_Pt_2400to3200_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy100um-370c082e337b0055a4bd71900e39ecba/USER', 398452)
_adbp3('ntuplev6p1_76x_errdxy100um', '/QCD_Pt_3200toInf_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy100um-f8fd46b7cb4bbd5ec8728744fd303617/USER', 391108)
_adbp3('ntuplev6p1_76x_errdxy100um', '/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/dquach-ntuplev6p1_76x_errdxy100um-fc43db46a4dbf8e5819bd7c499bb4283/USER', 1340337)
_adbp3('ntuplev6p1_76x_errdxy100um', '/mfv_neu_tau00100um_M0800/dquach-ntuplev6p1_76x_errdxy100um-cbab1fa86861dbf307b5291a7cb00bcd/USER', 9890)
_adbp3('ntuplev6p1_76x_errdxy100um', '/mfv_neu_tau00300um_M0800/dquach-ntuplev6p1_76x_errdxy100um-0e9cedaff16e60ff0dcbb07bc71ba145/USER', 9891)
_adbp3('ntuplev6p1_76x_errdxy100um', '/mfv_neu_tau01000um_M0800/dquach-ntuplev6p1_76x_errdxy100um-d000bbab7bcb56abaab12d950956e546/USER', 9898)
_adbp3('ntuplev6p1_76x_errdxy100um', '/mfv_neu_tau10000um_M0800/dquach-ntuplev6p1_76x_errdxy100um-516e6cda5ed05f37cc0f6a818d74ed5c/USER', 9850)
_adbp3('ntuplev6p1_76x_errdxy100um', '/XXTo4J_M-700_CTau-1mm_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy100um-86d1178fccb1810db981d4151dde3011/USER', 9898)
_adbp3('ntuplev6p1_76x_errdxy100um', '/XXTo4J_M-700_CTau-10mm_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy100um-564b64cea90c301317a73c7145eae454/USER', 9867)
_adbp3('ntuplev6p1_76x_errdxy100um', '/XXTo4J_M-700_CTau-30mm_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy100um-b4539c7d764d188e92ecc291fd6cbf99/USER', 9836)

_adbp3('ntuplev6p1_76x_errdxy40um_proper', '/mfv_neu_tau00100um_M0800/dquach-ntuplev6p1_76x_errdxy40um_proper-0decc501db2e77a586e0fbc0a12e7257/USER', 9890) # 1 files
_adbp3('ntuplev6p1_76x_errdxy40um_proper', '/mfv_neu_tau00300um_M0800/dquach-ntuplev6p1_76x_errdxy40um_proper-321a336061b5e64cd76814b3fe95caf4/USER', 9891) # 1 files
_adbp3('ntuplev6p1_76x_errdxy40um_proper', '/mfv_neu_tau01000um_M0800/dquach-ntuplev6p1_76x_errdxy40um_proper-9b3605bbf72585751655b11b9d4d3d28/USER', 9898) # 1 files
_adbp3('ntuplev6p1_76x_errdxy40um_proper', '/mfv_neu_tau10000um_M0800/dquach-ntuplev6p1_76x_errdxy40um_proper-53ff186630063bb26ac3f741910844de/USER', 9850) # 1 files
_adbp3('ntuplev6p1_76x_errdxy40um_proper', '/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy40um_proper-edc858263040b10ce95600e555818ed7/USER', 53610) # 35 files
_adbp3('ntuplev6p1_76x_errdxy40um_proper', '/QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy40um_proper-80dda0a6729819143fc9034dd6045823/USER', 1742101) # 70 files
_adbp3('ntuplev6p1_76x_errdxy40um_proper', '/QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy40um_proper-c374a4e078e3d4a45c73f28b867d2646/USER', 3927467) # 160 files
_adbp3('ntuplev6p1_76x_errdxy40um_proper', '/QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy40um_proper-c08ac263747c8069d9afd097d4bd82fb/USER', 3977145) # 161 files
_adbp3('ntuplev6p1_76x_errdxy40um_proper', '/QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy40um_proper-8a756470e7761f8906a44fdc9e2f35f2/USER', 3972910) # 160 files
_adbp3('ntuplev6p1_76x_errdxy40um_proper', '/QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy40um_proper-71f488b55d48ef7ad8494b9ada29ba83/USER', 2967901) # 120 files
_adbp3('ntuplev6p1_76x_errdxy40um_proper', '/QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy40um_proper-8982d468e3bd1a3f83dcc210b4c9f84a/USER', 395724) # 16 files
_adbp3('ntuplev6p1_76x_errdxy40um_proper', '/QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy40um_proper-c95894e84fb5c7f2dfb8a5575877de1f/USER', 393760) # 16 files
_adbp3('ntuplev6p1_76x_errdxy40um_proper', '/QCD_Pt_2400to3200_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy40um_proper-f58f9ee9e40610eb6f8c1d0a04ac4e47/USER', 398452) # 16 files
_adbp3('ntuplev6p1_76x_errdxy40um_proper', '/QCD_Pt_3200toInf_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy40um_proper-676f099424ed5d83644a72ba23705aa6/USER', 391108) # 16 files
_adbp3('ntuplev6p1_76x_errdxy40um_proper', '/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/dquach-ntuplev6p1_76x_errdxy40um_proper-18de3319a1579a77cdc7f1dac0518f07/USER', 1326361) # 198 files
_adbp3('ntuplev6p1_76x_errdxy40um_proper', '/XXTo4J_M-700_CTau-1mm_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy40um_proper-6f08d734d4fbdbdf7113e838a6b38064/USER', 9898) # 3 files
_adbp3('ntuplev6p1_76x_errdxy40um_proper', '/XXTo4J_M-700_CTau-10mm_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy40um_proper-22599c40f3c8862439cc39e5b7f53157/USER', 9867) # 2 files
_adbp3('ntuplev6p1_76x_errdxy40um_proper', '/XXTo4J_M-700_CTau-30mm_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy40um_proper-7ed8bc8fcb7bbf47cea1609196e5d0fe/USER', 9836) # 2 files

_adbp3('ntuplev6p1_76x_errdxy60um_proper', '/mfv_neu_tau00100um_M0800/dquach-ntuplev6p1_76x_errdxy60um_proper-b5f5ce816284d1787c8e4ad6d3cb211f/USER', 9890) # 1 files
_adbp3('ntuplev6p1_76x_errdxy60um_proper', '/mfv_neu_tau00300um_M0800/dquach-ntuplev6p1_76x_errdxy60um_proper-8f07806f381d49ceeb9c93c2f9f06c7c/USER', 9891) # 1 files
_adbp3('ntuplev6p1_76x_errdxy60um_proper', '/mfv_neu_tau01000um_M0800/dquach-ntuplev6p1_76x_errdxy60um_proper-67f817415870bf7a76d8be60619bbdb4/USER', 9898) # 1 files
_adbp3('ntuplev6p1_76x_errdxy60um_proper', '/mfv_neu_tau10000um_M0800/dquach-ntuplev6p1_76x_errdxy60um_proper-f629d72524a4b251297a1a6b6085db4f/USER', 9850) # 1 files
_adbp3('ntuplev6p1_76x_errdxy60um_proper', '/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy60um_proper-7660137cf3b4e5645338660284b28e93/USER', 53610) # 35 files
_adbp3('ntuplev6p1_76x_errdxy60um_proper', '/QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy60um_proper-67d8ab125f3e7bc80da6c063905135c5/USER', 1742101) # 70 files
_adbp3('ntuplev6p1_76x_errdxy60um_proper', '/QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy60um_proper-bb9afe14d0e193b3294fcdbb355abd98/USER', 3927467) # 160 files
_adbp3('ntuplev6p1_76x_errdxy60um_proper', '/QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy60um_proper-5343538b8d0f3b3189f904c52d44a61f/USER', 3977145) # 161 files
_adbp3('ntuplev6p1_76x_errdxy60um_proper', '/QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy60um_proper-cdfbc377e00303507d0aef17b1058c8f/USER', 3972910) # 160 files
_adbp3('ntuplev6p1_76x_errdxy60um_proper', '/QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy60um_proper-6c87ad2c36e2ee74d6c556954fe79523/USER', 2967901) # 120 files
_adbp3('ntuplev6p1_76x_errdxy60um_proper', '/QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy60um_proper-50a011639b7df66d8a447039f19d2a6c/USER', 395724) # 16 files
_adbp3('ntuplev6p1_76x_errdxy60um_proper', '/QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy60um_proper-8a15271f6fd5d83a9163d03e38700c28/USER', 393760) # 16 files
_adbp3('ntuplev6p1_76x_errdxy60um_proper', '/QCD_Pt_2400to3200_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy60um_proper-956513bf6fd18075e58929b11bab6646/USER', 398452) # 16 files
_adbp3('ntuplev6p1_76x_errdxy60um_proper', '/QCD_Pt_3200toInf_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy60um_proper-36404945e9fdcd4e01a0d68ed0d35ff1/USER', 391108) # 16 files
_adbp3('ntuplev6p1_76x_errdxy60um_proper', '/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/dquach-ntuplev6p1_76x_errdxy60um_proper-87f75ebe2f261f222a82b6cc490ee43f/USER', 1333333) # 199 files
_adbp3('ntuplev6p1_76x_errdxy60um_proper', '/XXTo4J_M-700_CTau-1mm_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy60um_proper-6723686611ecd30409f950c2c82c1ce1/USER', 9898) # 3 files
_adbp3('ntuplev6p1_76x_errdxy60um_proper', '/XXTo4J_M-700_CTau-10mm_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy60um_proper-a2d9a1a86e45ba72b7975cd5876475a1/USER', 9867) # 2 files
_adbp3('ntuplev6p1_76x_errdxy60um_proper', '/XXTo4J_M-700_CTau-30mm_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy60um_proper-7da9fdbaaa35b702e395d9e376036ef2/USER', 9836) # 2 files

_adbp3('ntuplev6p1_76x_errdxy80um_proper', '/mfv_neu_tau00100um_M0800/dquach-ntuplev6p1_76x_errdxy80um_proper-7ef0a311e6cbe3a0e8813a06fac0915a/USER', 9890) # 1 files
_adbp3('ntuplev6p1_76x_errdxy80um_proper', '/mfv_neu_tau00300um_M0800/dquach-ntuplev6p1_76x_errdxy80um_proper-cff508e043703f8130da0527c08328de/USER', 9891) # 1 files
_adbp3('ntuplev6p1_76x_errdxy80um_proper', '/mfv_neu_tau01000um_M0800/dquach-ntuplev6p1_76x_errdxy80um_proper-e278cb48f51cf8dc8ee912659b38eacd/USER', 9898) # 1 files
_adbp3('ntuplev6p1_76x_errdxy80um_proper', '/mfv_neu_tau10000um_M0800/dquach-ntuplev6p1_76x_errdxy80um_proper-86536b94a8d6582ef736e0f0d51b06ec/USER', 9850) # 1 files
_adbp3('ntuplev6p1_76x_errdxy80um_proper', '/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy80um_proper-a7400371ba4b32ff9df3ad6b37b55363/USER', 53610) # 35 files
_adbp3('ntuplev6p1_76x_errdxy80um_proper', '/QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy80um_proper-8a4e352646afaccef878443943d57a6f/USER', 1742101) # 70 files
_adbp3('ntuplev6p1_76x_errdxy80um_proper', '/QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy80um_proper-221c745a952e7b311710c311332b048a/USER', 3927467) # 160 files
_adbp3('ntuplev6p1_76x_errdxy80um_proper', '/QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy80um_proper-24cbdb57a2e902401fb25c60ff3f4889/USER', 3977145) # 161 files
_adbp3('ntuplev6p1_76x_errdxy80um_proper', '/QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy80um_proper-3a17d63913f6245d24d994f71ca94ac6/USER', 3972910) # 160 files
_adbp3('ntuplev6p1_76x_errdxy80um_proper', '/QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy80um_proper-043c9531bf71b3555c0178a1678af761/USER', 2967901) # 120 files
_adbp3('ntuplev6p1_76x_errdxy80um_proper', '/QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy80um_proper-7e0b0ca69d70747da5830b67385afff7/USER', 395724) # 16 files
_adbp3('ntuplev6p1_76x_errdxy80um_proper', '/QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy80um_proper-2b4d1099870d7ded24617046450450e7/USER', 393760) # 16 files
_adbp3('ntuplev6p1_76x_errdxy80um_proper', '/QCD_Pt_2400to3200_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy80um_proper-640d5263ec5d454dfb77a4e1cc9d549d/USER', 398452) # 16 files
_adbp3('ntuplev6p1_76x_errdxy80um_proper', '/QCD_Pt_3200toInf_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy80um_proper-fc3a649af00c608e4ad8c79d32e90e6f/USER', 391108) # 16 files
_adbp3('ntuplev6p1_76x_errdxy80um_proper', '/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/dquach-ntuplev6p1_76x_errdxy80um_proper-0d14501f0546f3f164f83ce305d81b02/USER', 1340337) # 200 files
_adbp3('ntuplev6p1_76x_errdxy80um_proper', '/XXTo4J_M-700_CTau-1mm_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy80um_proper-ada280b92f7d2c985570874b9f5d998b/USER', 9898) # 3 files
_adbp3('ntuplev6p1_76x_errdxy80um_proper', '/XXTo4J_M-700_CTau-10mm_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy80um_proper-9d7a1298762d61ea09a9d72d7604cbde/USER', 9867) # 2 files
_adbp3('ntuplev6p1_76x_errdxy80um_proper', '/XXTo4J_M-700_CTau-30mm_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy80um_proper-4f6a5b99ce1c329cd863cc9e35eeed3d/USER', 9836) # 2 files

_adbp3('ntuplev6p1_76x_errdxy100um_proper', '/mfv_neu_tau00100um_M0800/dquach-ntuplev6p1_76x_errdxy100um_proper-339b743a7d4e449f2a89a60ecf3d434a/USER', 9890) # 1 files
_adbp3('ntuplev6p1_76x_errdxy100um_proper', '/mfv_neu_tau00300um_M0800/dquach-ntuplev6p1_76x_errdxy100um_proper-bccd9140586fd9c4bbdcbd0282328ef2/USER', 9891) # 1 files
_adbp3('ntuplev6p1_76x_errdxy100um_proper', '/mfv_neu_tau01000um_M0800/dquach-ntuplev6p1_76x_errdxy100um_proper-51bd122b062c619278fba3c9929f929c/USER', 9898) # 1 files
_adbp3('ntuplev6p1_76x_errdxy100um_proper', '/mfv_neu_tau10000um_M0800/dquach-ntuplev6p1_76x_errdxy100um_proper-14b05958df35a07512ba92a983eb61c0/USER', 9850) # 1 files
_adbp3('ntuplev6p1_76x_errdxy100um_proper', '/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy100um_proper-e4104f7ce6004c4e80970be71a26fe8e/USER', 52102) # 34 files
_adbp3('ntuplev6p1_76x_errdxy100um_proper', '/QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy100um_proper-4de38b7ff89099d946f42f40fd839fa4/USER', 1742101) # 70 files
_adbp3('ntuplev6p1_76x_errdxy100um_proper', '/QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy100um_proper-103b69602f7dfe64e5cfdd0931b8724f/USER', 3927467) # 160 files
_adbp3('ntuplev6p1_76x_errdxy100um_proper', '/QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy100um_proper-12c8ac1ef64b93a9b239217c157f20b6/USER', 3977145) # 161 files
_adbp3('ntuplev6p1_76x_errdxy100um_proper', '/QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy100um_proper-39802c13093753a72c6e24530964c4e9/USER', 3948171) # 159 files
_adbp3('ntuplev6p1_76x_errdxy100um_proper', '/QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy100um_proper-4fd35c49e581e83f224e1d765f359632/USER', 2967901) # 120 files
_adbp3('ntuplev6p1_76x_errdxy100um_proper', '/QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy100um_proper-5382babf5a7907e0ddacc057ee032cc6/USER', 395724) # 16 files
_adbp3('ntuplev6p1_76x_errdxy100um_proper', '/QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy100um_proper-d7a223b64cb9d0a4e69c9378468ba466/USER', 393760) # 16 files
_adbp3('ntuplev6p1_76x_errdxy100um_proper', '/QCD_Pt_2400to3200_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy100um_proper-ea560e2e2e392efe769d8df9302c7d83/USER', 398452) # 16 files
_adbp3('ntuplev6p1_76x_errdxy100um_proper', '/QCD_Pt_3200toInf_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy100um_proper-e176e120dd6da700e19a56e1b823f1a3/USER', 391108) # 16 files
_adbp3('ntuplev6p1_76x_errdxy100um_proper', '/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/dquach-ntuplev6p1_76x_errdxy100um_proper-a6ba819eda59db5ec3b8f19113a572b4/USER', 1340337) # 200 files
_adbp3('ntuplev6p1_76x_errdxy100um_proper', '/XXTo4J_M-700_CTau-1mm_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy100um_proper-2a1dbcdbfeee766db766c135626bdf8a/USER', 9898) # 3 files
_adbp3('ntuplev6p1_76x_errdxy100um_proper', '/XXTo4J_M-700_CTau-10mm_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy100um_proper-663808ed8c1f198645b079407ff5e785/USER', 9867) # 2 files
_adbp3('ntuplev6p1_76x_errdxy100um_proper', '/XXTo4J_M-700_CTau-30mm_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_errdxy100um_proper-82b2174ee58f4471e1daeedc3f016c43/USER', 9836) # 2 files

_adbp3('ntuplev6p1_76x_newdefault', '/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/dquach-ntuplev6p1_76x_newdefault_try2-9c95ee86a30ef40901122e3c85f06b39/USER', 4408678) # 204 files
_adbp3('ntuplev6p1_76x_newdefault', '/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/dquach-ntuplev6p1_76x_newdefault_try2-1ac163ad622d6b6b00921aa191f56b92/USER', 5039738) # 206 files
_adbp3('ntuplev6p1_76x_newdefault', '/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/dquach-ntuplev6p1_76x_newdefault_try2-0c1cffb7fce277f47c95d0beb6cb247b/USER', 3952153) # 160 files
_adbp3('ntuplev6p1_76x_newdefault', '/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/dquach-ntuplev6p1_76x_newdefault_try2-3ec21486764ebbc8f73d7009341683a4/USER', 1981228) # 81 files
_adbp3('ntuplev6p1_76x_newdefault', '/XXTo4J_M-700_CTau-1mm_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_newdefault_try2-ae05a31b64deaa01f1eb1fa8dcb3a2f7/USER', 9898) # 3 files
_adbp3('ntuplev6p1_76x_newdefault', '/XXTo4J_M-700_CTau-10mm_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_newdefault_try2-f5a0d1fdce51e33aaae9026f7c82b093/USER', 9867) # 2 files
_adbp3('ntuplev6p1_76x_newdefault', '/XXTo4J_M-700_CTau-30mm_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_newdefault_try2-981747c563e0def594e6a7b573470b29/USER', 9836) # 1 files
_adbp3('ntuplev6p1_76x_newdefault', '/mfv_neu_tau00100um_M0800/dquach-ntuplev6p1_76x_newdefault_try2-69619f9f3ead8619bb138c3148be2fd4/USER', 9703) # 1 files
_adbp3('ntuplev6p1_76x_newdefault', '/mfv_neu_tau00300um_M0800/dquach-ntuplev6p1_76x_newdefault_try2-65a5c7db1dc79d34ee08a5d451f8b3e4/USER', 9877) # 1 files
_adbp3('ntuplev6p1_76x_newdefault', '/mfv_neu_tau01000um_M0800/dquach-ntuplev6p1_76x_newdefault_try2-3f7b002f3fcb02908759046481bfcc0b/USER', 9883) # 1 files
_adbp3('ntuplev6p1_76x_newdefault', '/mfv_neu_tau10000um_M0800/dquach-ntuplev6p1_76x_newdefault_try2-bc5e8ed1e5b2ee0b40191817ba7374d4/USER', 9794) # 1 files

_adbp3('ntuplev6p1_76x_nstlays3', '/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/dquach-ntuplev6p1_76x_nstlays3_try2-0563a6174ccfef7445b47a1adf52e04e/USER', 4408678) # 204 files
_adbp3('ntuplev6p1_76x_nstlays3', '/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/dquach-ntuplev6p1_76x_nstlays3_try2-9c87ea2e204738f8e66398eae2e1ceea/USER', 5039738) # 206 files
_adbp3('ntuplev6p1_76x_nstlays3', '/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/dquach-ntuplev6p1_76x_nstlays3_try2-0e21961f02f2bbcb31e97c1d56ed84b9/USER', 3952153) # 160 files
_adbp3('ntuplev6p1_76x_nstlays3', '/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/dquach-ntuplev6p1_76x_nstlays3_try2-d07a09819adfc59c1cee757ffeb6279f/USER', 1981228) # 81 files
_adbp3('ntuplev6p1_76x_nstlays3', '/XXTo4J_M-700_CTau-1mm_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_nstlays3_try2-e1f22acb7f159b559521cda099d97246/USER', 9898) # 3 files
_adbp3('ntuplev6p1_76x_nstlays3', '/XXTo4J_M-700_CTau-10mm_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_nstlays3_try2-1417969c55c0055e05ba27e9c016eaa8/USER', 9867) # 2 files
_adbp3('ntuplev6p1_76x_nstlays3', '/XXTo4J_M-700_CTau-30mm_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_nstlays3_try2-ce3da775da3c8fa8b287f0e82d2fe17c/USER', 9836) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_neu_tau00100um_M0800/dquach-ntuplev6p1_76x_nstlays3_try2-7ae9495b0be7532a9ad37380b27f5556/USER', 9703) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_neu_tau00300um_M0800/dquach-ntuplev6p1_76x_nstlays3_try2-03104c0e9eec564d64a1121d775777ff/USER', 9877) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_neu_tau01000um_M0800/dquach-ntuplev6p1_76x_nstlays3_try2-c9742dec426e9ca7fa0300d223dfc51d/USER', 9883) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_neu_tau10000um_M0800/dquach-ntuplev6p1_76x_nstlays3_try2-9d680d61eab0a536677ab255e00cb0a2/USER', 9794) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_neu_tau01000um_M0300/dquach-ntuplev6p1_76x_signal-ca77c05e10ef66beabf854ad2b028093/USER', 1463) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_neu_tau01000um_M0400/dquach-ntuplev6p1_76x_signal-cbf664a5aaf421e5d79d10014555cb3a/USER', 3635) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_neu_tau01000um_M1200/dquach-ntuplev6p1_76x_signal-e85a28b0bcf63447a9168a6e9f8db6d9/USER', 9997) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/mfv_neu_tau01000um_M1600/dquach-ntuplev6p1_76x_signal-681c54d8e6d93272dcf80b3406bf2fb8/USER', 10000) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/XXTo4J_M-50_CTau-1mm_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_signal-d74b051ffbfbc2f624612d79e0c38289/USER', 92) # 2 files
_adbp3('ntuplev6p1_76x_nstlays3', '/XXTo4J_M-100_CTau-1mm_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_signal-f9fdb240138288e752f8c9263be528c6/USER', 681) # 2 files
_adbp3('ntuplev6p1_76x_nstlays3', '/XXTo4J_M-300_CTau-1mm_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_signal-fef163ae8f4dfab65a01043078f3dedb/USER', 4058) # 1 files
_adbp3('ntuplev6p1_76x_nstlays3', '/XXTo4J_M-1500_CTau-1mm_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_signal-e801807342421d24a3e95bb1f7ad0d7d/USER', 9908) # 3 files

_adbp3('ntuplev6p1_76x_nstlays5', '/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/dquach-ntuplev6p1_76x_nstlays5_try2-b2d6e71246d10cf2d9a34b76ac72d20e/USER', 4408678) # 204 files
_adbp3('ntuplev6p1_76x_nstlays5', '/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/dquach-ntuplev6p1_76x_nstlays5_try2-a414da26c478bd22f48fb7ea24274bfa/USER', 5039738) # 206 files
_adbp3('ntuplev6p1_76x_nstlays5', '/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/dquach-ntuplev6p1_76x_nstlays5_try2-57613a87a9b6ca71e70258f9f80999e7/USER', 3952153) # 160 files
_adbp3('ntuplev6p1_76x_nstlays5', '/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/dquach-ntuplev6p1_76x_nstlays5_try2-0ccecfe2435f0e217beb69589329de50/USER', 1981228) # 81 files
_adbp3('ntuplev6p1_76x_nstlays5', '/XXTo4J_M-700_CTau-1mm_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_nstlays5_try2-9592f9f0b4b5457705991c4aac0527ae/USER', 9898) # 3 files
_adbp3('ntuplev6p1_76x_nstlays5', '/XXTo4J_M-700_CTau-10mm_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_nstlays5_try2-1e537943487f75b4a68c40bd0b9d7d65/USER', 9867) # 2 files
_adbp3('ntuplev6p1_76x_nstlays5', '/XXTo4J_M-700_CTau-30mm_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_nstlays5_try2-5d89a407d61f8d4e9557e986bb7d4e95/USER', 9836) # 1 files
_adbp3('ntuplev6p1_76x_nstlays5', '/mfv_neu_tau00100um_M0800/dquach-ntuplev6p1_76x_nstlays5_try2-0a3dfe54bdf0f225d7f709e9fe11df1c/USER', 9703) # 1 files
_adbp3('ntuplev6p1_76x_nstlays5', '/mfv_neu_tau00300um_M0800/dquach-ntuplev6p1_76x_nstlays5_try2-3eb0333d6ef3c1e7c0ebad08bd18397a/USER', 9877) # 1 files
_adbp3('ntuplev6p1_76x_nstlays5', '/mfv_neu_tau01000um_M0800/dquach-ntuplev6p1_76x_nstlays5_try2-4850c47ad0b6a2c56500280effb4c14f/USER', 9883) # 1 files
_adbp3('ntuplev6p1_76x_nstlays5', '/mfv_neu_tau10000um_M0800/dquach-ntuplev6p1_76x_nstlays5_try2-28ee4c253d04e253d1d68c7273fd6455/USER', 9595) # 1 files

_adbp3('ntuplev6p1_76x_nstlays7', '/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/dquach-ntuplev6p1_76x_nstlays7_try2-d2dae149bfe8db5d2981859b747ae467/USER', 4408678) # 204 files
_adbp3('ntuplev6p1_76x_nstlays7', '/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/dquach-ntuplev6p1_76x_nstlays7_try2-ce1edb8fbbef1596af75829e518cc34b/USER', 5039738) # 206 files
_adbp3('ntuplev6p1_76x_nstlays7', '/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/dquach-ntuplev6p1_76x_nstlays7_try2-18b620fa64e1757a590aeb5e410ab46c/USER', 3952153) # 160 files
_adbp3('ntuplev6p1_76x_nstlays7', '/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/dquach-ntuplev6p1_76x_nstlays7_try2-0b99d407cc65df155fd6148801259210/USER', 1981228) # 81 files
_adbp3('ntuplev6p1_76x_nstlays7', '/XXTo4J_M-700_CTau-1mm_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_nstlays7_try2-b2c0b59d100a9f01d5d30651990b3cd3/USER', 9898) # 3 files
_adbp3('ntuplev6p1_76x_nstlays7', '/XXTo4J_M-700_CTau-10mm_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_nstlays7_try2-54886466d3f7a6aa074c6781192b6419/USER', 9867) # 2 files
_adbp3('ntuplev6p1_76x_nstlays7', '/XXTo4J_M-700_CTau-30mm_TuneCUETP8M1_13TeV_pythia8/dquach-ntuplev6p1_76x_nstlays7_try2-d9f2640cbd7293ad1c88adba803b9fd0/USER', 9836) # 1 files
_adbp3('ntuplev6p1_76x_nstlays7', '/mfv_neu_tau00100um_M0800/dquach-ntuplev6p1_76x_nstlays7_try2-61cbf31e3173ec8794fbc8381783c30c/USER', 9703) # 1 files
_adbp3('ntuplev6p1_76x_nstlays7', '/mfv_neu_tau00300um_M0800/dquach-ntuplev6p1_76x_nstlays7_try2-5233ccb1615ab5c8223aa56336565e24/USER', 9877) # 1 files
_adbp3('ntuplev6p1_76x_nstlays7', '/mfv_neu_tau01000um_M0800/dquach-ntuplev6p1_76x_nstlays7_try2-487857b1fe09ddd3374a4bdd88564d99/USER', 9883) # 1 files
_adbp3('ntuplev6p1_76x_nstlays7', '/mfv_neu_tau10000um_M0800/dquach-ntuplev6p1_76x_nstlays7_try2-8b687cf372331ff6c19dbdafb544fd75/USER', 9595) # 1 files


# for x in $(<a.txt); echo _adbp3\(\'\', \'${x}\', $(dass 3 nevents $x)\) \# $(dass 3 file $x | wl) files

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
