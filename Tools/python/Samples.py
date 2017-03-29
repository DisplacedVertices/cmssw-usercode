#!/usr/bin/env python

from itertools import chain
from JMTucker.Tools.Sample import *

########################################################################

########
# 2015 MC
########

qcd_samples_2015 = [
    MCSample('qcdht0500_2015', '/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',  19701790, nice='QCD, 500 < H_{T} < 700 GeV',   color=804, syst_frac=0.20, xsec=3.163e4),
    MCSample('qcdht0700_2015', '/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM', 15547962, nice='QCD, 700 < H_{T} < 1000 GeV',  color=805, syst_frac=0.20, xsec=6.802e3),
    MCSample('qcdht1000_2015', '/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM', 5085104, nice='QCD, 1000 < H_{T} < 1500 GeV', color=806, syst_frac=0.20, xsec=1.206e3),
    MCSample('qcdht1500_2015', '/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM', 3952170, nice='QCD, 1500 < H_{T} < 2000 GeV', color=807, syst_frac=0.20, xsec=120),
    MCSample('qcdht2000_2015', '/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',  1981228, nice='QCD, H_{T} > 2000',            color=808, syst_frac=0.20, xsec=25.3),
    ]

qcd_samples_ext_2015 = [
    MCSample('qcdht0500ext_2015', '/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/AODSIM',   43242884, nice='QCD, 500 < H_{T} < 700 GeV',   color=804, syst_frac=0.20, xsec=3.163e4),
    MCSample('qcdht0700ext_2015', '/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/AODSIM',  29569683, nice='QCD, 700 < H_{T} < 1000 GeV',  color=805, syst_frac=0.20, xsec=6.802e3),
    MCSample('qcdht1000ext_2015', '/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/AODSIM', 10246203, nice='QCD, 1000 < H_{T} < 1500 GeV', color=806, syst_frac=0.20, xsec=1.206e3),
    MCSample('qcdht1500ext_2015', '/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/AODSIM',  7815090, nice='QCD, 1500 < H_{T} < 2000 GeV', color=807, syst_frac=0.20, xsec=120),
    MCSample('qcdht2000ext_2015', '/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/AODSIM',   4016332, nice='QCD, H_{T} > 2000',            color=808, syst_frac=0.20, xsec=25.3),
    ]

qcd_samples_sum_2015 = [ MCSample(x.name.replace('_2015', '') + 'sum_2015', '/None/', x.nevents_orig + y.nevents_orig, nice=x.nice, color=x.color, syst_frac=x.syst_frac, xsec=x.xsec) for x,y in zip(qcd_samples_2015, qcd_samples_ext_2015) ]

ttbar_samples_2015 = [
    MCSample('ttbar_2015', '/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM', 38493485, nice='t#bar{t}', color=4, syst_frac=0.15, xsec=832.),
    ]

x = leptonic_background_samples_2015 = [
    MCSample('wjetstolnu1_2015', '/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',       24156124, nice='W + jets #rightarrow l#nu', color=  9, syst_frac=0.10, xsec=6.153e4), 
    MCSample('wjetstolnu2_2015', '/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext2-v1/AODSIM', 240721767, nice='W + jets #rightarrow l#nu', color=  9, syst_frac=0.10, xsec=6.153e4), 
    MCSample('wjetstolnu3_2015', '/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext4-v1/AODSIM', 199037280, nice='W + jets #rightarrow l#nu', color=  9, syst_frac=0.10, xsec=6.153e4), 
    MCSample('dyjetstollM101_2015', '/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',      30899063, nice='DY + jets #rightarrow ll, 10 < M < 50 GeV', color= 29, syst_frac=0.10, xsec=1.861e4),
    MCSample('dyjetstollM102_2015', '/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/AODSIM', 62169181, nice='DY + jets #rightarrow ll, 10 < M < 50 GeV', color= 29, syst_frac=0.10, xsec=1.861e4),
    MCSample('dyjetstollM103_2015', '/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext3-v1/AODSIM', 76558711, nice='DY + jets #rightarrow ll, 10 < M < 50 GeV', color= 29, syst_frac=0.10, xsec=1.861e4),
    MCSample('dyjetstollM501_2015', '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',       28751199, nice='DY + jets #rightarrow ll, M > 50 GeV', color= 32, syst_frac=0.10, xsec=6.025e3),
    MCSample('dyjetstollM502_2015', '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v2/AODSIM', 164439857, nice='DY + jets #rightarrow ll, M > 50 GeV', color= 32, syst_frac=0.10, xsec=6.025e3),
    MCSample('dyjetstollM503_2015', '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext4-v1/AODSIM', 121231446, nice='DY + jets #rightarrow ll, M > 50 GeV', color= 32, syst_frac=0.10, xsec=6.025e3),
    MCSample('qcdmupt15_2015', '/QCD_Pt-20toInf_MuEnrichedPt15_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM', 21966678, nice='QCD, #hat{p}_{T} > 20 GeV, #mu p_{T} > 15 GeV', color=801, syst_frac=0.20, xsec=7.21e8 * 4.2e-4),
    ]

leptonic_background_samples_sum_2015 = [
    MCSample('wjetstolnusum_2015',    '/None/', sum(y.nevents_orig for y in x[:3] ), nice=x[0].nice, color=x[0].color, syst_frac=x[0].syst_frac, xsec=x[0].xsec),
    MCSample('dyjetstollM10sum_2015', '/None/', sum(y.nevents_orig for y in x[3:6]), nice=x[3].nice, color=x[3].color, syst_frac=x[3].syst_frac, xsec=x[3].xsec),
    MCSample('dyjetstollM50sum_2015', '/None/', sum(y.nevents_orig for y in x[6:9]), nice=x[6].nice, color=x[6].color, syst_frac=x[6].syst_frac, xsec=x[6].xsec),
    ]
del x

mfv_signal_samples_2015 = [
    MCSample('mfv_neu_tau00100um_M0300_2015', '/mfv_neu_tau00100um_M0300/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-05e8cfd69022b6357c491ecab3cf47fb/USER', 10000),
    MCSample('mfv_neu_tau00100um_M0400_2015', '/mfv_neu_tau00100um_M0400/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-05e8cfd69022b6357c491ecab3cf47fb/USER', 10000),
    MCSample('mfv_neu_tau00100um_M0800_2015', '/mfv_neu_tau00100um_M0800/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-05e8cfd69022b6357c491ecab3cf47fb/USER', 10000),
    MCSample('mfv_neu_tau00100um_M1200_2015', '/mfv_neu_tau00100um_M1200/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-05e8cfd69022b6357c491ecab3cf47fb/USER', 10000),
    MCSample('mfv_neu_tau00100um_M1600_2015', '/mfv_neu_tau00100um_M1600/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-05e8cfd69022b6357c491ecab3cf47fb/USER', 10000),
    MCSample('mfv_neu_tau00300um_M0300_2015', '/mfv_neu_tau00300um_M0300/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-05e8cfd69022b6357c491ecab3cf47fb/USER', 10000),
    MCSample('mfv_neu_tau00300um_M0400_2015', '/mfv_neu_tau00300um_M0400/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-05e8cfd69022b6357c491ecab3cf47fb/USER', 10000),
    MCSample('mfv_neu_tau00300um_M0800_2015', '/mfv_neu_tau00300um_M0800/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-05e8cfd69022b6357c491ecab3cf47fb/USER', 10000),
    MCSample('mfv_neu_tau00300um_M1200_2015', '/mfv_neu_tau00300um_M1200/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-05e8cfd69022b6357c491ecab3cf47fb/USER', 10000),
    MCSample('mfv_neu_tau00300um_M1600_2015', '/mfv_neu_tau00300um_M1600/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-05e8cfd69022b6357c491ecab3cf47fb/USER', 10000),
    MCSample('mfv_neu_tau01000um_M0300_2015', '/mfv_neu_tau01000um_M0300/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-05e8cfd69022b6357c491ecab3cf47fb/USER', 10000),
    MCSample('mfv_neu_tau01000um_M0400_2015', '/mfv_neu_tau01000um_M0400/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-05e8cfd69022b6357c491ecab3cf47fb/USER', 10000),
    MCSample('mfv_neu_tau01000um_M0800_2015', '/mfv_neu_tau01000um_M0800/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-05e8cfd69022b6357c491ecab3cf47fb/USER', 10000),
    MCSample('mfv_neu_tau01000um_M1200_2015', '/mfv_neu_tau01000um_M1200/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-05e8cfd69022b6357c491ecab3cf47fb/USER', 10000),
    MCSample('mfv_neu_tau01000um_M1600_2015', '/mfv_neu_tau01000um_M1600/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-05e8cfd69022b6357c491ecab3cf47fb/USER', 10000),
    MCSample('mfv_neu_tau10000um_M0300_2015', '/mfv_neu_tau10000um_M0300/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-05e8cfd69022b6357c491ecab3cf47fb/USER', 10000),
    MCSample('mfv_neu_tau10000um_M0400_2015', '/mfv_neu_tau10000um_M0400/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-05e8cfd69022b6357c491ecab3cf47fb/USER', 10000),
    MCSample('mfv_neu_tau10000um_M0800_2015', '/mfv_neu_tau10000um_M0800/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-05e8cfd69022b6357c491ecab3cf47fb/USER', 10000),
    MCSample('mfv_neu_tau10000um_M1200_2015', '/mfv_neu_tau10000um_M1200/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-05e8cfd69022b6357c491ecab3cf47fb/USER', 10000),
    MCSample('mfv_neu_tau10000um_M1600_2015', '/mfv_neu_tau10000um_M1600/tucker-RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-05e8cfd69022b6357c491ecab3cf47fb/USER', 10000),
    ]

xx4j_samples_2015 = [    # M = 50, 100 GeV also exist
    MCSample('xx4j_tau00001mm_M0300_2015', '/XXTo4J_M-300_CTau-1mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',     10000),
    MCSample('xx4j_tau00003mm_M0300_2015', '/XXTo4J_M-300_CTau-3mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',     10000),
    MCSample('xx4j_tau00010mm_M0300_2015', '/XXTo4J_M-300_CTau-10mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',    10000),
    MCSample('xx4j_tau00030mm_M0300_2015', '/XXTo4J_M-300_CTau-30mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',    10000),
    MCSample('xx4j_tau00100mm_M0300_2015', '/XXTo4J_M-300_CTau-100mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',   10000),
    MCSample('xx4j_tau00300mm_M0300_2015', '/XXTo4J_M-300_CTau-300mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',   10000),
    MCSample('xx4j_tau01000mm_M0300_2015', '/XXTo4J_M-300_CTau-1000mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',  10000),
    MCSample('xx4j_tau02000mm_M0300_2015', '/XXTo4J_M-300_CTau-2000mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',  10000),
    MCSample('xx4j_tau00003mm_M0500_2015', '/XXTo4J_M-500_CTau-3mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',     10000),
    MCSample('xx4j_tau00010mm_M0500_2015', '/XXTo4J_M-500_CTau-10mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',    10000),
    MCSample('xx4j_tau00030mm_M0500_2015', '/XXTo4J_M-500_CTau-30mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',    10000),
    #MCSample('xx4j_tau00300mm_M0500_2015', '/XXTo4J_M-500_CTau-300mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',    9295), # only at bad t2
    MCSample('xx4j_tau01000mm_M0500_2015', '/XXTo4J_M-500_CTau-1000mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',  10000),
    MCSample('xx4j_tau02000mm_M0500_2015', '/XXTo4J_M-500_CTau-2000mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',  10000),
    MCSample('xx4j_tau00001mm_M0700_2015', '/XXTo4J_M-700_CTau-1mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',     10000),
    #MCSample('xx4j_tau00003mm_M0700_2015', '/XXTo4J_M-700_CTau-3mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',     10000), # crab didn't work and so forget it
    MCSample('xx4j_tau00010mm_M0700_2015', '/XXTo4J_M-700_CTau-10mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',    10000),
    #MCSample('xx4j_tau00030mm_M0700_2015', '/XXTo4J_M-700_CTau-30mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',    10000), # only at bad t2
    MCSample('xx4j_tau00100mm_M0700_2015', '/XXTo4J_M-700_CTau-100mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',   10000),
    MCSample('xx4j_tau00300mm_M0700_2015', '/XXTo4J_M-700_CTau-300mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',   10000),
    MCSample('xx4j_tau01000mm_M0700_2015', '/XXTo4J_M-700_CTau-1000mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',  10000),
    MCSample('xx4j_tau00001mm_M1000_2015', '/XXTo4J_M-1000_CTau-1mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',    10000),
    MCSample('xx4j_tau00003mm_M1000_2015', '/XXTo4J_M-1000_CTau-3mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',    10000),
    MCSample('xx4j_tau00030mm_M1000_2015', '/XXTo4J_M-1000_CTau-30mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',   10000),
    #MCSample('xx4j_tau00300mm_M1000_2015', '/XXTo4J_M-1000_CTau-300mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',  10000), # only at bad t2
    MCSample('xx4j_tau01000mm_M1000_2015', '/XXTo4J_M-1000_CTau-1000mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM', 10000),
    MCSample('xx4j_tau02000mm_M1000_2015', '/XXTo4J_M-1000_CTau-2000mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM', 10000),
    MCSample('xx4j_tau00001mm_M1500_2015', '/XXTo4J_M-1500_CTau-1mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',     9908),
    MCSample('xx4j_tau00010mm_M1500_2015', '/XXTo4J_M-1500_CTau-10mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',   10000),
    MCSample('xx4j_tau00030mm_M1500_2015', '/XXTo4J_M-1500_CTau-30mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',   10000),
    MCSample('xx4j_tau00300mm_M1500_2015', '/XXTo4J_M-1500_CTau-300mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',  10000),
    MCSample('xx4j_tau01000mm_M1500_2015', '/XXTo4J_M-1500_CTau-1000mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',  9745),
    #MCSample('xx4j_tau00001mm_M3000_2015', '/XXTo4J_M-3000_CTau-1mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',     9882), # only on tape
    MCSample('xx4j_tau00003mm_M3000_2015', '/XXTo4J_M-3000_CTau-3mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',    10000),
    MCSample('xx4j_tau00010mm_M3000_2015', '/XXTo4J_M-3000_CTau-10mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',   10000),
    MCSample('xx4j_tau00030mm_M3000_2015', '/XXTo4J_M-3000_CTau-30mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',   10000),
    MCSample('xx4j_tau00100mm_M3000_2015', '/XXTo4J_M-3000_CTau-100mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',  10000),
    MCSample('xx4j_tau00300mm_M3000_2015', '/XXTo4J_M-3000_CTau-300mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM',   9384),
    MCSample('xx4j_tau01000mm_M3000_2015', '/XXTo4J_M-3000_CTau-1000mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM', 10000),
    MCSample('xx4j_tau02000mm_M3000_2015', '/XXTo4J_M-3000_CTau-2000mm_TuneCUETP8M1_13TeV_pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM', 10000),
    ]

for s in mfv_signal_samples_2015:
    s.dbs_inst = 'phys03'
    s.xsec = 1e-3
    s.condor = True

for s in xx4j_samples_2015:
    s.xsec = 1e-3

########
# 2016 MC = main, so no _2016 in names
########

qcd_samples = [
    MCSample('qcdht0500', '/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/AODSIM',  18929951, nice='QCD, 500 < H_{T} < 700 GeV',   color=804, syst_frac=0.20, xsec=3.163e4),
    MCSample('qcdht0700', '/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/AODSIM', 15629253, nice='QCD, 700 < H_{T} < 1000 GeV',  color=805, syst_frac=0.20, xsec=6.802e3),
    MCSample('qcdht1000', '/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/AODSIM', 4850746, nice='QCD, 1000 < H_{T} < 1500 GeV', color=806, syst_frac=0.20, xsec=1.206e3),
    MCSample('qcdht1500', '/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/AODSIM', 3970819, nice='QCD, 1500 < H_{T} < 2000 GeV', color=807, syst_frac=0.20, xsec=120),
    MCSample('qcdht2000', '/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/AODSIM',  1991645, nice='QCD, H_{T} > 2000',            color=808, syst_frac=0.20, xsec=25.3),
    ]

qcd_samples_ext = [
    MCSample('qcdht0500ext', '/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v2/AODSIM',   44061488, nice='QCD, 500 < H_{T} < 700 GeV',   color=804, syst_frac=0.20, xsec=3.163e4),
    MCSample('qcdht0700ext', '/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/AODSIM',  29808140, nice='QCD, 700 < H_{T} < 1000 GeV',  color=805, syst_frac=0.20, xsec=6.802e3),
    MCSample('qcdht1000ext', '/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/AODSIM', 10360193, nice='QCD, 1000 < H_{T} < 1500 GeV', color=806, syst_frac=0.20, xsec=1.206e3),
    MCSample('qcdht1500ext', '/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/AODSIM',  7868538, nice='QCD, 1500 < H_{T} < 2000 GeV', color=807, syst_frac=0.20, xsec=120),
    MCSample('qcdht2000ext', '/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/AODSIM',   4047360, nice='QCD, H_{T} > 2000',            color=808, syst_frac=0.20, xsec=25.3),
    ]

qcd_samples_sum = [ MCSample(x.name.replace('', '') + 'sum', '/None/', x.nevents_orig + y.nevents_orig, nice=x.nice, color=x.color, syst_frac=x.syst_frac, xsec=x.xsec) for x,y in zip(qcd_samples, qcd_samples_ext) ] # for scripts downstream

ttbar_samples = [
    MCSample('ttbar', '/TTJets_TuneCUETP8M2T4_13TeV-amcatnloFXFX-pythia8/RunIISummer16DR80Premix-PUMoriond17_backup_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/AODSIM', 43662343, nice='t#bar{t}', color=4, syst_frac=0.15, xsec=832.),
    ]

leptonic_background_samples = [
    MCSample('wjetstolnu',    '/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/AODSIM',                24120319, nice='W + jets #rightarrow l#nu', color=  9, syst_frac=0.10, xsec=6.153e4), 
    MCSample('dyjetstollM10', '/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/AODSIM',  40509291, nice='DY + jets #rightarrow ll, 10 < M < 50 GeV', color= 29, syst_frac=0.10, xsec=1.861e4),
    MCSample('dyjetstollM50', '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16DR80Premix-PUMoriond17_HCALDebug_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/AODSIM', 29082237, nice='DY + jets #rightarrow ll, M > 50 GeV', color= 32, syst_frac=0.10, xsec=6.025e3),
    MCSample('qcdmupt15',     '/QCD_Pt-20toInf_MuEnrichedPt15_TuneCUETP8M1_13TeV_pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/AODSIM',          22094081, nice='QCD, #hat{p}_{T} > 20 GeV, #mu p_{T} > 15 GeV', color=801, syst_frac=0.20, xsec=7.21e8 * 4.2e-4),
    ]

mfv_ddbar_samples = [
    MCSample('mfv_ddbar_tau00100um_M0300', '/mfv_ddbar_tau00100um_M0300/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-7baaad836cd91d62036ec27bee801843/USER', 10000),
    MCSample('mfv_ddbar_tau00100um_M0400', '/mfv_ddbar_tau00100um_M0400/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-7baaad836cd91d62036ec27bee801843/USER', 10000),
    MCSample('mfv_ddbar_tau00100um_M0500', '/mfv_ddbar_tau00100um_M0500/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-7baaad836cd91d62036ec27bee801843/USER', 9999),
    MCSample('mfv_ddbar_tau00100um_M0600', '/mfv_ddbar_tau00100um_M0600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-7baaad836cd91d62036ec27bee801843/USER', 10000),
    MCSample('mfv_ddbar_tau00100um_M0800', '/mfv_ddbar_tau00100um_M0800/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-7baaad836cd91d62036ec27bee801843/USER', 10000),
    MCSample('mfv_ddbar_tau00100um_M1200', '/mfv_ddbar_tau00100um_M1200/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-7baaad836cd91d62036ec27bee801843/USER', 10000),
    MCSample('mfv_ddbar_tau00100um_M1600', '/mfv_ddbar_tau00100um_M1600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-7baaad836cd91d62036ec27bee801843/USER', 10000),
    MCSample('mfv_ddbar_tau00300um_M0300', '/mfv_ddbar_tau00300um_M0300/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-7baaad836cd91d62036ec27bee801843/USER', 9999),
    MCSample('mfv_ddbar_tau00300um_M0400', '/mfv_ddbar_tau00300um_M0400/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-7baaad836cd91d62036ec27bee801843/USER', 10000),
    MCSample('mfv_ddbar_tau00300um_M0500', '/mfv_ddbar_tau00300um_M0500/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-7baaad836cd91d62036ec27bee801843/USER', 9999),
    MCSample('mfv_ddbar_tau00300um_M0600', '/mfv_ddbar_tau00300um_M0600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-7baaad836cd91d62036ec27bee801843/USER', 9999),
    MCSample('mfv_ddbar_tau00300um_M0800', '/mfv_ddbar_tau00300um_M0800/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-7baaad836cd91d62036ec27bee801843/USER', 10000),
    MCSample('mfv_ddbar_tau00300um_M1200', '/mfv_ddbar_tau00300um_M1200/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-7baaad836cd91d62036ec27bee801843/USER', 10000),
    MCSample('mfv_ddbar_tau00300um_M1600', '/mfv_ddbar_tau00300um_M1600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-7baaad836cd91d62036ec27bee801843/USER', 10000),
    MCSample('mfv_ddbar_tau01000um_M0300', '/mfv_ddbar_tau01000um_M0300/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-7baaad836cd91d62036ec27bee801843/USER', 9999),
    MCSample('mfv_ddbar_tau01000um_M0400', '/mfv_ddbar_tau01000um_M0400/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-7baaad836cd91d62036ec27bee801843/USER', 10000),
    MCSample('mfv_ddbar_tau01000um_M0500', '/mfv_ddbar_tau01000um_M0500/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-7baaad836cd91d62036ec27bee801843/USER', 9999),
    MCSample('mfv_ddbar_tau01000um_M0600', '/mfv_ddbar_tau01000um_M0600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-7baaad836cd91d62036ec27bee801843/USER', 9999),
    MCSample('mfv_ddbar_tau01000um_M0800', '/mfv_ddbar_tau01000um_M0800/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-7baaad836cd91d62036ec27bee801843/USER', 10000),
    MCSample('mfv_ddbar_tau01000um_M1200', '/mfv_ddbar_tau01000um_M1200/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-7baaad836cd91d62036ec27bee801843/USER', 10000),
    MCSample('mfv_ddbar_tau01000um_M1600', '/mfv_ddbar_tau01000um_M1600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-7baaad836cd91d62036ec27bee801843/USER', 10000),
    MCSample('mfv_ddbar_tau10000um_M0300', '/mfv_ddbar_tau10000um_M0300/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-7baaad836cd91d62036ec27bee801843/USER', 9999),
    MCSample('mfv_ddbar_tau10000um_M0400', '/mfv_ddbar_tau10000um_M0400/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-7baaad836cd91d62036ec27bee801843/USER', 10000),
    MCSample('mfv_ddbar_tau10000um_M0500', '/mfv_ddbar_tau10000um_M0500/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-7baaad836cd91d62036ec27bee801843/USER', 10000),
    MCSample('mfv_ddbar_tau10000um_M0600', '/mfv_ddbar_tau10000um_M0600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-7baaad836cd91d62036ec27bee801843/USER', 10000),
    MCSample('mfv_ddbar_tau10000um_M0800', '/mfv_ddbar_tau10000um_M0800/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-7baaad836cd91d62036ec27bee801843/USER', 10000),
    MCSample('mfv_ddbar_tau10000um_M1200', '/mfv_ddbar_tau10000um_M1200/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-7baaad836cd91d62036ec27bee801843/USER', 10000),
    MCSample('mfv_ddbar_tau10000um_M1600', '/mfv_ddbar_tau10000um_M1600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-7baaad836cd91d62036ec27bee801843/USER', 9999),
    MCSample('mfv_ddbar_tau30000um_M0300', '/mfv_ddbar_tau30000um_M0300/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-7baaad836cd91d62036ec27bee801843/USER', 9998),
    MCSample('mfv_ddbar_tau30000um_M0400', '/mfv_ddbar_tau30000um_M0400/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-7baaad836cd91d62036ec27bee801843/USER', 10000),
    MCSample('mfv_ddbar_tau30000um_M0500', '/mfv_ddbar_tau30000um_M0500/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-7baaad836cd91d62036ec27bee801843/USER', 10000),
    MCSample('mfv_ddbar_tau30000um_M0600', '/mfv_ddbar_tau30000um_M0600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-7baaad836cd91d62036ec27bee801843/USER', 10000),
    MCSample('mfv_ddbar_tau30000um_M0800', '/mfv_ddbar_tau30000um_M0800/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-7baaad836cd91d62036ec27bee801843/USER', 9999),
    MCSample('mfv_ddbar_tau30000um_M1200', '/mfv_ddbar_tau30000um_M1200/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-7baaad836cd91d62036ec27bee801843/USER', 10000),
    MCSample('mfv_ddbar_tau30000um_M1600', '/mfv_ddbar_tau30000um_M1600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-7baaad836cd91d62036ec27bee801843/USER', 10000),
    ]

mfv_signal_samples = [
    MCSample('mfv_neu_tau00100um_M0600', '/mfv_neu_tau00100um_M0600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-61de7e7798ef8f788c198c43f09ebf3d/USER', 10000),
    MCSample('mfv_neu_tau00100um_M3000', '/mfv_neu_tau00100um_M3000/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-799254d98714d4bddcfc4dddd0b67e7b/USER', 9700),
    MCSample('mfv_neu_tau00300um_M0600', '/mfv_neu_tau00300um_M0600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-36f33e35675d4fdda6e229a231c74a68/USER', 20000),
    MCSample('mfv_neu_tau00300um_M0800', '/mfv_neu_tau00300um_M0800/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-36f33e35675d4fdda6e229a231c74a68/USER', 20000),
    MCSample('mfv_neu_tau00300um_M3000', '/mfv_neu_tau00300um_M3000/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-799254d98714d4bddcfc4dddd0b67e7b/USER', 9800),
    MCSample('mfv_neu_tau01000um_M0600', '/mfv_neu_tau01000um_M0600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-36f33e35675d4fdda6e229a231c74a68/USER', 20000),
    MCSample('mfv_neu_tau01000um_M3000', '/mfv_neu_tau01000um_M3000/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-799254d98714d4bddcfc4dddd0b67e7b/USER', 9300),
    MCSample('mfv_neu_tau10000um_M0600', '/mfv_neu_tau10000um_M0600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-61de7e7798ef8f788c198c43f09ebf3d/USER', 10000),
    MCSample('mfv_neu_tau10000um_M3000', '/mfv_neu_tau10000um_M3000/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-799254d98714d4bddcfc4dddd0b67e7b/USER', 9500),
    MCSample('mfv_neu_tau30000um_M0300', '/mfv_neu_tau30000um_M0300/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-78fa28476a320b0d17459f4085218e86/USER', 10000),
    MCSample('mfv_neu_tau30000um_M0400', '/mfv_neu_tau30000um_M0400/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-78fa28476a320b0d17459f4085218e86/USER', 10000),
    MCSample('mfv_neu_tau30000um_M0600', '/mfv_neu_tau30000um_M0600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-61de7e7798ef8f788c198c43f09ebf3d/USER', 10000),
    MCSample('mfv_neu_tau30000um_M0800', '/mfv_neu_tau30000um_M0800/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-78fa28476a320b0d17459f4085218e86/USER', 10000),
    MCSample('mfv_neu_tau30000um_M1200', '/mfv_neu_tau30000um_M1200/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-78fa28476a320b0d17459f4085218e86/USER', 10000),
    MCSample('mfv_neu_tau30000um_M1600', '/mfv_neu_tau30000um_M1600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-78fa28476a320b0d17459f4085218e86/USER', 10000),
    MCSample('mfv_neu_tau30000um_M3000', '/mfv_neu_tau30000um_M3000/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-799254d98714d4bddcfc4dddd0b67e7b/USER', 9699),
    ]

official_mfv_signal_samples = [
    MCSample('official_mfv_neu_tau00100um_M0300', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-100um_TuneCUETP8M1_13TeV-pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/AODSIM',  100000),
    MCSample('official_mfv_neu_tau00300um_M0300', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-300um_TuneCUETP8M1_13TeV-pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/AODSIM',  100000),
    MCSample('official_mfv_neu_tau01000um_M0300', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-1mm_TuneCUETP8M1_13TeV-pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v2/AODSIM',    100000),
    MCSample('official_mfv_neu_tau10000um_M0300', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-10mm_TuneCUETP8M1_13TeV-pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/AODSIM',    99302),
    MCSample('official_mfv_neu_tau00100um_M0400', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-100um_TuneCUETP8M1_13TeV-pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/AODSIM',  100000),
    MCSample('official_mfv_neu_tau00300um_M0400', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-300um_TuneCUETP8M1_13TeV-pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v2/AODSIM',  100000),
    MCSample('official_mfv_neu_tau01000um_M0400', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-1mm_TuneCUETP8M1_13TeV-pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/AODSIM',    100000),
    MCSample('official_mfv_neu_tau10000um_M0400', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-10mm_TuneCUETP8M1_13TeV-pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/AODSIM',    99208),
    MCSample('official_mfv_neu_tau00100um_M0800', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-100um_TuneCUETP8M1_13TeV-pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/AODSIM',   98260),
    MCSample('official_mfv_neu_tau00300um_M0800', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-300um_TuneCUETP8M1_13TeV-pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/AODSIM',  100000),
    MCSample('official_mfv_neu_tau01000um_M0800', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-1mm_TuneCUETP8M1_13TeV-pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v2/AODSIM',     99672),
    MCSample('official_mfv_neu_tau10000um_M0800', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-10mm_TuneCUETP8M1_13TeV-pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/AODSIM',   100000),
    MCSample('official_mfv_neu_tau00100um_M1200', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-100um_TuneCUETP8M1_13TeV-pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v2/AODSIM',  99540),
    MCSample('official_mfv_neu_tau00300um_M1200', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-300um_TuneCUETP8M1_13TeV-pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/AODSIM', 100000),
    MCSample('official_mfv_neu_tau01000um_M1200', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-1mm_TuneCUETP8M1_13TeV-pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/AODSIM',   100000),
    MCSample('official_mfv_neu_tau10000um_M1200', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-10mm_TuneCUETP8M1_13TeV-pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v2/AODSIM',   99540),
    MCSample('official_mfv_neu_tau00100um_M1600', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-100um_TuneCUETP8M1_13TeV-pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/AODSIM',  99734),
    MCSample('official_mfv_neu_tau00300um_M1600', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-300um_TuneCUETP8M1_13TeV-pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/AODSIM',  99999),
    MCSample('official_mfv_neu_tau01000um_M1600', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-1mm_TuneCUETP8M1_13TeV-pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/AODSIM',   100000),
    MCSample('official_mfv_neu_tau10000um_M1600', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-10mm_TuneCUETP8M1_13TeV-pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/AODSIM',   99751),
    ]

for s in mfv_ddbar_samples + mfv_signal_samples:
    s.dbs_inst = 'phys03'
    s.xsec = 1e-3
    s.condor = True

for s in official_mfv_signal_samples:
    s.xsec = 1e-3

########################################################################

########
# 2015 data
########

data_samples_2015 = [
    DataSample('JetHT2015C', '/JetHT/Run2015C_25ns-16Dec2015-v1/AOD'), # 254227 - 255031
    DataSample('JetHT2015D', '/JetHT/Run2015D-16Dec2015-v1/AOD'),      # 256630 - 260727
    ]

auxiliary_data_samples_2015 = [
    DataSample('SingleMuon2015C', '/SingleMuon/Run2015C_25ns-16Dec2015-v1/AOD'),
    DataSample('SingleMuon2015D', '/SingleMuon/Run2015D-16Dec2015-v1/AOD'),
    ]

for s in data_samples_2015 + auxiliary_data_samples_2015:
    s.json = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/Reprocessing/Cert_13TeV_16Dec2015ReReco_Collisions15_25ns_JSON_Silver_v2.txt'

########
# 2016 data = main so no _2016 in list names
########

data_samples = [
    DataSample('JetHT2016B3', '/JetHT/Run2016B-23Sep2016-v3/AOD'),  # 272007 - 275376
    DataSample('JetHT2016C', '/JetHT/Run2016C-23Sep2016-v1/AOD'),   # 275657 - 276283
    DataSample('JetHT2016D', '/JetHT/Run2016D-23Sep2016-v1/AOD'),   # 276315 - 276811
    DataSample('JetHT2016E', '/JetHT/Run2016E-23Sep2016-v1/AOD'),   # 276831 - 277420
    DataSample('JetHT2016F', '/JetHT/Run2016F-23Sep2016-v1/AOD'),   # 277772 - 278808
    DataSample('JetHT2016G', '/JetHT/Run2016G-23Sep2016-v1/AOD'),   # 278820 - 280385
    DataSample('JetHT2016H2', '/JetHT/Run2016H-PromptReco-v2/AOD'), # 281207 - 284035 
    DataSample('JetHT2016H3', '/JetHT/Run2016H-PromptReco-v3/AOD'), # 284036 - 284068  but json only through 284044
    ]

auxiliary_data_samples = [
    DataSample('SingleMuon2016B3', '/SingleMuon/Run2016B-23Sep2016-v3/AOD'),
    DataSample('SingleMuon2016C', '/SingleMuon/Run2016C-23Sep2016-v1/AOD'),
    DataSample('SingleMuon2016D', '/SingleMuon/Run2016D-23Sep2016-v1/AOD'),
    DataSample('SingleMuon2016E', '/SingleMuon/Run2016E-23Sep2016-v1/AOD'),
    DataSample('SingleMuon2016F', '/SingleMuon/Run2016F-23Sep2016-v1/AOD'),
    DataSample('SingleMuon2016G', '/SingleMuon/Run2016G-23Sep2016-v1/AOD'),
    DataSample('SingleMuon2016H2', '/SingleMuon/Run2016H-PromptReco-v2/AOD'),
    DataSample('SingleMuon2016H3', '/SingleMuon/Run2016H-PromptReco-v3/AOD'),
    ]

for s in data_samples + auxiliary_data_samples:
    s.json = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/ReReco/Final/Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt' # includes PromptReco for H

########################################################################

registry = SamplesRegistry()

# shortcuts, be careful:
# - 2015/6
# - can't add data, qcd datasets by primary (have the same primary for different datasets)
# basically only use them for the signal samples (until xx4j 2016 exists, grr)
from functools import partial
_adbp = registry.add_dataset_by_primary
_adbp3 = partial(_adbp, dbs_inst='phys03')

__all__ = [
    'qcd_samples',
    'qcd_samples_ext',
    'qcd_samples_sum',
    'ttbar_samples',
    'leptonic_background_samples',
    'mfv_ddbar_samples',
    'mfv_signal_samples',
    'official_mfv_signal_samples',
    'data_samples',
    'auxiliary_data_samples',

    'qcd_samples_2015',
    'qcd_samples_ext_2015',
    'qcd_samples_sum_2015',
    'ttbar_samples_2015',
    'mfv_signal_samples_2015',
    'xx4j_samples_2015',
    'leptonic_background_samples_2015',
    'leptonic_background_samples_sum_2015',
    'data_samples_2015',
    'auxiliary_data_samples_2015',

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

########
# Extra datasets and other overrides go here.
########

########
# gensims
########

# /qcdht2000_gensim/tucker-RunIISummer15GS-MCRUN2_71_V1-b23e9743a38a9c86cad94bbc723daab4/USER
# /qcdht2000_gensim_ext1/tucker-RunIISummer15GS-MCRUN2_71_V1-b23e9743a38a9c86cad94bbc723daab4/USER
#testqcdht2000.add_dataset('gensim', '/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/tucker-RunIISummer15GS-MCRUN2_71_V1/GEN-SIM', 33377, dbs_inst='phys03', condor=True)

########
# miniaod
########

for sample in data_samples + auxiliary_data_samples + data_samples_2015 + auxiliary_data_samples_2015:
    sample.add_dataset('miniaod', sample.dataset.replace('AOD', 'MINIAOD'))

qcdht0500_2015.add_dataset('miniaod', '/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM',  19665695)
qcdht0700_2015.add_dataset('miniaod', '/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM', 15547962)
qcdht1000_2015.add_dataset('miniaod', '/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM', 5049267)
qcdht1500_2015.add_dataset('miniaod', '/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM', 3939077)
qcdht2000_2015.add_dataset('miniaod', '/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM',  1981228)
qcdht0500ext_2015.add_dataset('miniaod', '/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/MINIAODSIM',   43075365)
qcdht0700ext_2015.add_dataset('miniaod', '/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/MINIAODSIM',  29552713)
qcdht1000ext_2015.add_dataset('miniaod', '/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/MINIAODSIM', 10144378)
qcdht1500ext_2015.add_dataset('miniaod', '/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/MINIAODSIM',  7813960)
qcdht2000ext_2015.add_dataset('miniaod', '/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/MINIAODSIM',   4016332)
wjetstolnu1_2015.add_dataset('miniaod', '/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM',       24156124)
wjetstolnu2_2015.add_dataset('miniaod', '/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext2-v1/MINIAODSIM', 238185234)
wjetstolnu3_2015.add_dataset('miniaod', '/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext4-v1/MINIAODSIM', 199037280)
dyjetstollM101_2015.add_dataset('miniaod', '/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM',      30899063)
dyjetstollM102_2015.add_dataset('miniaod', '/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/MINIAODSIM', 62135699)
dyjetstollM103_2015.add_dataset('miniaod', '/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext3-v1/MINIAODSIM', 76558711)
dyjetstollM501_2015.add_dataset('miniaod', '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM',       28751199)
dyjetstollM502_2015.add_dataset('miniaod', '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v2/MINIAODSIM', 163982720)
dyjetstollM503_2015.add_dataset('miniaod', '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext4-v1/MINIAODSIM', 121212419)
qcdmupt15_2015.add_dataset('miniaod', '/QCD_Pt-20toInf_MuEnrichedPt15_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM', 21948126)
ttbar_2015.add_dataset('miniaod', '/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM', 38475776)

qcdht0500.add_dataset('miniaod', '/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',  18929951)
qcdht0700.add_dataset('miniaod', '/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', 15629253)
qcdht1000.add_dataset('miniaod', '/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', 4767100)
qcdht1500.add_dataset('miniaod', '/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', 3970819)
qcdht2000.add_dataset('miniaod', '/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',  1991645)
qcdht0500ext.add_dataset('miniaod', '/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v2/MINIAODSIM',   43341392)
qcdht0700ext.add_dataset('miniaod', '/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM',  29783527)
qcdht1000ext.add_dataset('miniaod', '/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM', 10360193)
qcdht1500ext.add_dataset('miniaod', '/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM',  7855883)
qcdht2000ext.add_dataset('miniaod', '/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM',   4047360)
wjetstolnu.add_dataset('miniaod', '/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', 24120319)
dyjetstollM10.add_dataset('miniaod', '/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM', 40381391)
dyjetstollM50.add_dataset('miniaod', '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv2-PUMoriond17_HCALDebug_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', 28968252)
qcdmupt15.add_dataset('miniaod', '/QCD_Pt-20toInf_MuEnrichedPt15_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', 22094081)
ttbar.add_dataset('miniaod', '/TTJets_TuneCUETP8M2T4_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv2-PUMoriond17_backup_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', 43561608)

_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-100um_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',  100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-300um_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',  100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-1mm_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v2/MINIAODSIM',    100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-10mm_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',    99302)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-100um_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',  100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-300um_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v2/MINIAODSIM',  100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-1mm_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',    100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-10mm_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',    99208)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-100um_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',   98260)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-300um_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',  100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-1mm_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v2/MINIAODSIM',     99672)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-10mm_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',   100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-100um_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v2/MINIAODSIM',  99540)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-300um_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-1mm_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',   100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-10mm_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v2/MINIAODSIM',  100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-100um_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',  99734)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-300um_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',  99999)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-1mm_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',   100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-10mm_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',   99004)

########
# ntuples
########

_adbp3('ntuplev12', '/XXTo4J_M-700_CTau-1mm_TuneCUETP8M1_13TeV_pythia8/tucker-NtupleV12-74c4c2c4366ee21399061436d4ad2bc0/USER', 9898)
_adbp3('ntuplev12', '/XXTo4J_M-1000_CTau-1mm_TuneCUETP8M1_13TeV_pythia8/tucker-NtupleV12-03301097f209334307f9519fed01dfae/USER', 9992)
_adbp3('ntuplev12', '/XXTo4J_M-1500_CTau-1mm_TuneCUETP8M1_13TeV_pythia8/tucker-NtupleV12-a87eed61d55cdb87ba6fb1566c649455/USER', 9908)
_adbp3('ntuplev12', '/XXTo4J_M-500_CTau-3mm_TuneCUETP8M1_13TeV_pythia8/tucker-NtupleV12-39d46eccd29893bd1f03ecf3effefebd/USER', 9023)
_adbp3('ntuplev12', '/XXTo4J_M-1000_CTau-3mm_TuneCUETP8M1_13TeV_pythia8/tucker-NtupleV12-0a23d3c0d715a95b8b7ceebb01f99e3e/USER', 9996)
_adbp3('ntuplev12', '/XXTo4J_M-300_CTau-10mm_TuneCUETP8M1_13TeV_pythia8/tucker-NtupleV12-f86a81b3f00c8cd53b87fd2438bd07c3/USER', 3518)
_adbp3('ntuplev12', '/XXTo4J_M-1500_CTau-10mm_TuneCUETP8M1_13TeV_pythia8/tucker-NtupleV12-f5a6e990693195e460e51b6398d39856/USER', 10000)
_adbp3('ntuplev12', '/XXTo4J_M-3000_CTau-10mm_TuneCUETP8M1_13TeV_pythia8/tucker-NtupleV12-956e1caffa5b5c9f01fc4b39e32427a4/USER', 10000)
_adbp3('ntuplev12', '/XXTo4J_M-300_CTau-30mm_TuneCUETP8M1_13TeV_pythia8/tucker-NtupleV12-e3b8c27ef4a9a4aa7c225682718d7578/USER', 3406)
_adbp3('ntuplev12', '/XXTo4J_M-500_CTau-30mm_TuneCUETP8M1_13TeV_pythia8/tucker-NtupleV12-e02e37a2025e53aea453fe147c8d48b6/USER', 8603)
_adbp3('ntuplev12', '/XXTo4J_M-1000_CTau-30mm_TuneCUETP8M1_13TeV_pythia8/tucker-NtupleV12-76abce6e8948ed2194f75f952c9c327f/USER', 9985)
_adbp3('ntuplev12', '/XXTo4J_M-1500_CTau-30mm_TuneCUETP8M1_13TeV_pythia8/tucker-NtupleV12-61d9e23b8cdcfc409f519cc8a16ef43e/USER', 10000)
_adbp3('ntuplev12', '/XXTo4J_M-3000_CTau-30mm_TuneCUETP8M1_13TeV_pythia8/tucker-NtupleV12-a2324649b5fcf7429e1db0eb5bfb2882/USER', 10000)
_adbp3('ntuplev12', '/XXTo4J_M-300_CTau-100mm_TuneCUETP8M1_13TeV_pythia8/tucker-NtupleV12-57dc05d90339421f16a0d5e3a3566e5d/USER', 3308)
_adbp3('ntuplev12', '/XXTo4J_M-700_CTau-100mm_TuneCUETP8M1_13TeV_pythia8/tucker-NtupleV12-0f33fa9db9e1a1071c709f71c6233e33/USER', 9797)
_adbp3('ntuplev12', '/XXTo4J_M-700_CTau-300mm_TuneCUETP8M1_13TeV_pythia8/tucker-NtupleV12-14249ef0c9113f3ab1388e2993efd4db/USER', 9778)
_adbp3('ntuplev12', '/XXTo4J_M-500_CTau-1000mm_TuneCUETP8M1_13TeV_pythia8/tucker-NtupleV12-93ec491dfab870e9c437b6141fefeee0/USER', 6916)
_adbp3('ntuplev12', '/XXTo4J_M-700_CTau-1000mm_TuneCUETP8M1_13TeV_pythia8/tucker-NtupleV12-5f4870e9d95c37e884cbe70ceb72c618/USER', 9191)
_adbp3('ntuplev12', '/XXTo4J_M-1000_CTau-1000mm_TuneCUETP8M1_13TeV_pythia8/tucker-NtupleV12-e3d9619cec8d938b2ac37df44a7b6a44/USER', 9874)
_adbp3('ntuplev12', '/XXTo4J_M-500_CTau-2000mm_TuneCUETP8M1_13TeV_pythia8/tucker-NtupleV12-2f7d078a81292bc0467b5509c7d70280/USER', 4747)
_adbp3('ntuplev12', '/XXTo4J_M-1000_CTau-2000mm_TuneCUETP8M1_13TeV_pythia8/tucker-NtupleV12-4edd88dc11eb946bea6c3779cad0778a/USER', 9057)

qcdht1000.add_dataset('ntuplev12', '/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/tucker-NtupleV12-3bac46bb2586b0a97a1779f787554d15/USER', 4831702)
qcdht2000ext.add_dataset('ntuplev12', '/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/tucker-NtupleV12-afce10d34c768ff65be25a3adba6c137/USER', 4047360)

_adbp3('ntuplev12', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-300um_TuneCUETP8M1_13TeV-pythia8/tucker-NtupleV12-5032985219d91f2b94f9ab9542a5dbf1/USER', 18387)
_adbp3('ntuplev12', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-300um_TuneCUETP8M1_13TeV-pythia8/tucker-NtupleV12-231a28da67ecf51928a79a87edb89c32/USER', 44660)
_adbp3('ntuplev12', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-300um_TuneCUETP8M1_13TeV-pythia8/tucker-NtupleV12-074c32799594b8e296a80150ff51c31f/USER', 99982)
_adbp3('ntuplev12', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-300um_TuneCUETP8M1_13TeV-pythia8/tucker-NtupleV12-40ccbbcaae06cf3ab9ab85199bf142ff/USER', 99997)
_adbp3('ntuplev12', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-1mm_TuneCUETP8M1_13TeV-pythia8/tucker-NtupleV12-3ab58216ff95f0763d8d8668fed4601d/USER', 43281)
_adbp3('ntuplev12', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-1mm_TuneCUETP8M1_13TeV-pythia8/tucker-NtupleV12-6614b201ae1f1e2d032d04ac54a64c3f/USER', 100000)
_adbp3('ntuplev12', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-10mm_TuneCUETP8M1_13TeV-pythia8/tucker-NtupleV12-023000c29873201b6e9e0d593be98714/USER', 34040)
_adbp3('ntuplev12', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-10mm_TuneCUETP8M1_13TeV-pythia8/tucker-NtupleV12-1df51208804a01868becde20111f4ae7/USER', 98620)

JetHT2016B3.add_dataset('ntuplev12', '/JetHT/tucker-NtupleV12-ed09b748f6be0007d3f80d7a9c651110/USER', 20459353)
JetHT2016C.add_dataset('ntuplev12', '/JetHT/tucker-NtupleV12-4de46f5786c935edf774085b52be2cc3/USER', 9003136)
JetHT2016D.add_dataset('ntuplev12', '/JetHT/tucker-NtupleV12-c0862f82c6d9e4968498ec9a917038a7/USER', 14726858)
JetHT2016E.add_dataset('ntuplev12', '/JetHT/tucker-NtupleV12-c0c08c96cd0b60bbd85c4f0b2427e38b/USER', 13664363)
JetHT2016F.add_dataset('ntuplev12', '/JetHT/tucker-NtupleV12-0af523479fcfbed97639cbffb0aa89d8/USER', 10755341)
JetHT2016G.add_dataset('ntuplev12', '/JetHT/tucker-NtupleV12-248d7971c1c7719f6ec9ef73221e7dcf/USER', 27659741)
JetHT2016H2.add_dataset('ntuplev12', '/JetHT/tucker-NtupleV12-72bc9d6c7302b35406ec73af1e478c83/USER', 14180580)
JetHT2016H3.add_dataset('ntuplev12', '/JetHT/tucker-NtupleV12-c2c950db55264ce616ae0a4bfc441bdb/USER', 361026)

for x in (JetHT2015C, JetHT2015D, mfv_neu_tau00100um_M0300_2015, mfv_neu_tau00100um_M0400_2015, mfv_neu_tau00100um_M0800_2015, mfv_neu_tau00100um_M1200_2015, mfv_neu_tau00100um_M1600_2015, mfv_neu_tau00300um_M0300_2015, mfv_neu_tau00300um_M0400_2015, mfv_neu_tau00300um_M0800_2015, mfv_neu_tau00300um_M1200_2015, mfv_neu_tau00300um_M1600_2015, mfv_neu_tau01000um_M0300_2015, mfv_neu_tau01000um_M0400_2015, mfv_neu_tau01000um_M0800_2015, mfv_neu_tau01000um_M1200_2015, mfv_neu_tau01000um_M1600_2015, mfv_neu_tau10000um_M0300_2015, mfv_neu_tau10000um_M0400_2015, mfv_neu_tau10000um_M0800_2015, mfv_neu_tau10000um_M1200_2015, mfv_neu_tau10000um_M1600_2015, official_mfv_neu_tau00100um_M0300, official_mfv_neu_tau00100um_M0800, official_mfv_neu_tau00100um_M1200, official_mfv_neu_tau00100um_M1600, official_mfv_neu_tau00300um_M0800, official_mfv_neu_tau01000um_M0300, official_mfv_neu_tau01000um_M0800, official_mfv_neu_tau01000um_M1200, official_mfv_neu_tau10000um_M0300, official_mfv_neu_tau10000um_M1200, official_mfv_neu_tau10000um_M1600, qcdht0500, qcdht0500_2015, qcdht0500ext, qcdht0500ext_2015, qcdht0700, qcdht0700_2015, qcdht0700ext, qcdht0700ext_2015, qcdht1000_2015, qcdht1000ext, qcdht1000ext_2015, qcdht1500, qcdht1500_2015, qcdht1500ext, qcdht1500ext_2015, qcdht2000, qcdht2000_2015, qcdht2000ext_2015, ttbar, ttbar_2015, xx4j_tau00001mm_M0300_2015, xx4j_tau00003mm_M0300_2015, xx4j_tau00003mm_M3000_2015, xx4j_tau00010mm_M0500_2015, xx4j_tau00010mm_M0700_2015, xx4j_tau00100mm_M3000_2015, xx4j_tau00300mm_M0300_2015, xx4j_tau00300mm_M1500_2015, xx4j_tau00300mm_M3000_2015, xx4j_tau01000mm_M0300_2015, xx4j_tau01000mm_M1500_2015, xx4j_tau01000mm_M3000_2015, xx4j_tau02000mm_M0300_2015, xx4j_tau02000mm_M3000_2015,):
    x.add_dataset('ntuplev12')

qcdht0500.add_dataset('pick1vtxv1', '/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/tucker-Pick1VtxV1-fcc6aaec1961e7bcf17b9c0fe4107509/USER', 6)
qcdht0700.add_dataset('pick1vtxv1', '/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/tucker-Pick1VtxV1-2aea76e35d539298e18916833dbc74f1/USER', 2502)
qcdht1000.add_dataset('pick1vtxv1', '/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/tucker-Pick1VtxV1-8afc595d081ee1f94f783e1522e075c9/USER', 23215)
qcdht1500.add_dataset('pick1vtxv1', '/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/tucker-Pick1VtxV1-d4e99261570f80d2911af23da7638dca/USER', 36394)
qcdht2000.add_dataset('pick1vtxv1', '/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/tucker-Pick1VtxV1-68ed9a7d908fe44cd6d0b63faf778cf0/USER', 23593)
qcdht0500ext.add_dataset('pick1vtxv1', '/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/tucker-Pick1VtxV1-a37dfa072e5d03a021f17fce6afd2b00/USER', 24)
qcdht0700ext.add_dataset('pick1vtxv1', '/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/tucker-Pick1VtxV1-5638c525258d2251f88fd88d678c05ee/USER', 4941)
qcdht1000ext.add_dataset('pick1vtxv1', '/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/tucker-Pick1VtxV1-e2ba514394879e0966fe3e21073240c7/USER', 49350)
qcdht1500ext.add_dataset('pick1vtxv1', '/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/tucker-Pick1VtxV1-176431eb1f7b3da10a55c78c72f41e91/USER', 72588)
ttbar.add_dataset('pick1vtxv1', '/TTJets_TuneCUETP8M2T4_13TeV-amcatnloFXFX-pythia8/tucker-Pick1VtxV1-2ff5f2f92aca436adf9b213a040bf828/USER', 19603)
qcdht0500_2015.add_dataset('pick1vtxv1', '/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/tucker-Pick1VtxV1-f043e40fc32d092cdc49150b3ec811b0/USER', 12)
qcdht0700_2015.add_dataset('pick1vtxv1', '/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/tucker-Pick1VtxV1-65df0d5e5c3f76c72b74221d7b5b8700/USER', 1766)
qcdht1000_2015.add_dataset('pick1vtxv1', '/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/tucker-Pick1VtxV1-75c290893cdb61f138b4fe4eefb1c5a7/USER', 15270)
qcdht1500_2015.add_dataset('pick1vtxv1', '/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/tucker-Pick1VtxV1-7305ee7a0ef5d247f9662bf418bce9ac/USER', 23069)
qcdht2000_2015.add_dataset('pick1vtxv1', '/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/tucker-Pick1VtxV1-0be3f492b9a08c8896c4c9d8e6fd6d56/USER', 16058)
qcdht0500ext_2015.add_dataset('pick1vtxv1', '/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/tucker-Pick1VtxV1-18bed05a3c605603df624a1c8c8f09a4/USER', 17)
qcdht0700ext_2015.add_dataset('pick1vtxv1', '/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/tucker-Pick1VtxV1-fc50c7c27ee475c86efd5a7b40d64868/USER', 3429)
qcdht1000ext_2015.add_dataset('pick1vtxv1', '/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/tucker-Pick1VtxV1-94d3fdf1dac0ad1ed94a7104e68a6299/USER', 30837)
qcdht1500ext_2015.add_dataset('pick1vtxv1', '/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/tucker-Pick1VtxV1-4d1af49094452e9e05493cdcade0780e/USER', 45870)
ttbar_2015.add_dataset('pick1vtxv1', '/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/tucker-Pick1VtxV1-375a5077021b79bab6d9cc16597b393e/USER', 15381)

for x in qcdht2000ext, qcdht2000ext_2015:
    x.add_dataset('pick1vtxv1')

########
# other condor declarations
########

JetHT2015C.condor = True
JetHT2015D.condor = True
JetHT2015D.xrootd_url = 'root://dcache-cms-xrootd.desy.de/'

for x in (qcdht2000ext,
          qcdht0500_2015, qcdht0700_2015, qcdht1000_2015, qcdht1500_2015, qcdht2000_2015,
          qcdht0500ext_2015, qcdht0700ext_2015, qcdht1000ext_2015, qcdht1500ext_2015, qcdht2000ext_2015,
          ttbar_2015):
    x.condor = True
    x.xrootd_url = 'root://cmseos.fnal.gov/'

for x in (SingleMuon2016B3, SingleMuon2016C, SingleMuon2016E, SingleMuon2016H2,
          qcdht0500, qcdht1500, qcdht0500ext, qcdht0700, qcdht0700ext, qcdht1000ext, qcdht1500ext, qcdht2000,
          ttbar,
          wjetstolnu, dyjetstollM50, qcdmupt15,
          official_mfv_neu_tau00100um_M0300, official_mfv_neu_tau10000um_M0300, official_mfv_neu_tau01000um_M0300,
          official_mfv_neu_tau00100um_M0800, official_mfv_neu_tau00300um_M0800, official_mfv_neu_tau01000um_M0800,
          official_mfv_neu_tau00100um_M1200, official_mfv_neu_tau01000um_M1200, official_mfv_neu_tau10000um_M1200,
          official_mfv_neu_tau00100um_M1600, official_mfv_neu_tau10000um_M1600,
          xx4j_tau00001mm_M0300_2015, xx4j_tau00003mm_M0300_2015, xx4j_tau00300mm_M0300_2015, xx4j_tau01000mm_M0300_2015, xx4j_tau02000mm_M0300_2015, xx4j_tau00010mm_M0500_2015, xx4j_tau00010mm_M0700_2015, xx4j_tau00300mm_M1500_2015, xx4j_tau01000mm_M1500_2015, xx4j_tau00003mm_M3000_2015, xx4j_tau00100mm_M3000_2015, xx4j_tau00300mm_M3000_2015, xx4j_tau01000mm_M3000_2015, xx4j_tau02000mm_M3000_2015,
          ):
    x.condor = True

qcdht2000.xrootd_url = 'root://ccmsdlf.ads.rl.ac.uk//castor/ads.rl.ac.uk/prod/cms/disk'
official_mfv_neu_tau01000um_M0300.xrootd_url = 'root://xrootd2.ihepa.ufl.edu/'
official_mfv_neu_tau01000um_M0800.xrootd_url = 'root://xrootd2.ihepa.ufl.edu/'
official_mfv_neu_tau10000um_M1200.xrootd_url = 'root://xrootd2.ihepa.ufl.edu/'
official_mfv_neu_tau00300um_M0800.xrootd_url = 'root://cmseos.fnal.gov/'

for x in qcd_samples_2015:
    x.datasets['miniaod'].condor = True
    x.datasets['miniaod'].xrootd_url = 'root://cmseos.fnal.gov/'

for x in (JetHT2016B3,
          SingleMuon2016B3, SingleMuon2016C, SingleMuon2016E,
          qcdht0700, qcdht1000, qcdht1500, qcdht0700ext, qcdht1500ext, qcdht2000ext, ttbar,
          official_mfv_neu_tau10000um_M0300, official_mfv_neu_tau01000um_M0400, official_mfv_neu_tau00100um_M0800,
          official_mfv_neu_tau00300um_M0800, official_mfv_neu_tau01000um_M1200, official_mfv_neu_tau00100um_M1600, official_mfv_neu_tau10000um_M1600):
    x.datasets['miniaod'].condor = True

ttbar_2015.datasets['miniaod'].condor = True
ttbar_2015.datasets['miniaod'].xrootd_url = 'root://dcache-cms-xrootd.desy.de/'

for s in registry.all():
    for ds in s.datasets.keys():
        if ds.startswith('ntuple'):
            s.datasets[ds].condor = True

########################################################################

if __name__ == '__main__':
    main(registry)

    import sys
    from pprint import pprint
    from JMTucker.Tools import DBS
    from JMTucker.Tools.general import popen

    if 0:
        from JMTucker.Tools.SampleFiles import _d
        for y,l in [(2015, sum([eval(l) for l in __all__ if type(eval(l)) == list and l.endswith('2015')], [])),
                    (2016, sum([eval(l) for l in __all__ if type(eval(l)) == list and not l.endswith('2015')], []))]:
            print y
            for s in l:
                if s.name.startswith('mfv_') or s.name.startswith('xx4j') or s.name.startswith('official_mfv_'): #'sum' not in s.name:
                    for ds in ('ntuplev11',): #'miniaod', 'ntuplev11':
                        if (s.name.startswith('mfv_') or s.name.startswith('xx4j')) and ds == 'miniaod':
                            continue
                        if not s.has_dataset(ds):
                            print s.name, 'no', ds
                        else:
                            if not _d.has_key((s.name, 'ntuplev11')):
                                print s.name, 'no files'

    if 0:
        for l in [official_mfv_signal_samples]:
            for s in l:
                #s.set_curr_dataset('miniaod')
                try:
                    sites = DBS.sites_for_dataset(s.dataset)
                    #files = DBS.files_in_dataset(s.dataset)
                except RuntimeError:
                    print s.name, 'PROBLEM'
                    continue
                sites = [x for x in sites if not x.endswith('_Buffer') and not x.endswith('_MSS')]
                #print s.name.ljust(30), str(len(files)).ljust(10), ' '.join(sites)
                print s.name.ljust(50), ' '.join(sites)

    if 0:
        for s in official_mfv_signal_samples:
            n1, n2 = s.datasets['main'].nevents_orig, s.datasets['miniaod'].nevents_orig
            if n1 != n2:
                print s.name, n1, n2

    if 0:
        from DBS import *
        for s in data_samples:
            print s.name.ljust(15), '%20i %20i' % (numevents_in_dataset(s.datasets['main'].dataset), numevents_in_dataset(s.datasets['miniaod'].dataset))

    if 0:
        from JMTucker.Tools.general import popen
        for s in qcd_samples + qcd_samples_17 + qcd_samples_ext + qcd_samples_ext_17 + ttbar_samples + leptonic_background_samples:
            print s.name, popen('dasgoclient_linux -query "site dataset=%s" | sort | uniq' % s.dataset).replace('\n', ' ')

    if 0:
        aod_strings = ['RunIIFall15DR76-PU25nsData2015v1', 'RunIISummer16DR80Premix-PUMoriond17']
        miniaod_strings = ['RunIIFall15MiniAODv2-PU25nsData2015v1', 'RunIISummer16MiniAODv2-PUMoriond17']
        no = 'Trains Material ALCA Flat RunIISpring16MiniAODv1'.split()
        from JMTucker.Tools.general import popen
        for s in xx4j_samples_2015: #qcd_samples + ttbar_samples + leptonic_background_samples:
            print s.name
            #print s.primary_dataset
            output = popen('dasgoclient_linux -query "dataset=/%s/*/*AODSIM"' % s.primary_dataset).split('\n')
            for y in 'AODSIM MINIAODSIM'.split():
                for x in output:
                    ok = True
                    for n in no:
                        if n in x:
                            ok = False
                    if not ok:
                        continue
                    #print x
                    if x.endswith('/' + y):
                        nevents = None
                        for line in popen('dasgoclient_linux -query "dataset=%s | grep dataset.nevents"' % x).split('\n'):
                            try:
                                nevents = int(float(line))
                            except ValueError:
                                pass
                        assert nevents is not None and nevents > 0
                        print '"%s", %i' % (x, nevents)

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

    if 0:
        for x,y in zip(qcd_samples, qcd_samples_ext):
            print x.name, x.int_lumi_orig/1000, '->', (x.int_lumi_orig + y.int_lumi_orig)/1000

    if 0:
        from JMTucker.Tools.general import coderep_files
        f = open('a.txt', 'wt')
        for x in qcd_samples + qcd_samples_ext + ttbar_samples + data_samples:
            for y in ('ntuplev11',):
                print x.name, y
                if not x.try_curr_dataset(y):
                    continue
                code = coderep_files(x.filenames)
                f.write('(%r, %r): (%i, %s),\n' % (x.name, y, len(x.filenames), code))

    if 0:
        import os
        from JMTucker.Tools.general import coderep_files
        f = open('a.txt', 'wt')
        for s in qcd_samples + qcd_samples_ext + ttbar_samples + data_samples:
            print s.name
            fns = s.filenames
            base = os.path.commonprefix(fns)
            bns = [x.replace(base, '') for x in fns]
            code = "[%r + x for x in '''\n" % base
            for bn in bns:
                code += bn + '\n'
            code += "'''.split('\n')]"
            f.write('(%r, %r): (%i, %s),\n' % (s.name, y, len(fns), code))
