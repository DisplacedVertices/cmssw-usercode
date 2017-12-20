#!/usr/bin/env python

from itertools import chain
from JMTucker.Tools.Sample import *

########################################################################

def _tau(sample):
    s = sample.name
    is_um = '0um_' in s
    x = int(s[s.index('tau')+3:s.index('um_' if is_um else 'mm_')])
    if not is_um:
        x *= 1000
    return x

def _mass(sample):
    s = sample.name
    x = s.index('_M')
    y = s.find('_',x+1)
    if y == -1:
        y = len(s)
    return int(s[x+2:y])

def _set_tau_mass(sample):
    sample.is_signal = True
    sample.tau  = _tau (sample)
    sample.mass = _mass(sample)

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
    _set_tau_mass(s)
    s.is_private = True
    s.dbs_inst = 'phys03'
    s.xsec = 1e-3
    s.condor = True

for s in xx4j_samples_2015:
    _set_tau_mass(s)
    s.is_private = False
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

minbias_samples = [
    MCSample('private_minbias', '/minbias/tucker-RunIISummer15GS-MCRUN2_71_V1-79473ee9dd0d24ba1969f21e10b4fae5/USER', 996000),
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
    MCSample('mfv_ddbar_tau00100um_M3000', '/mfv_ddbar_tau00100um_M3000/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-4bd045e185937c8f9d9213d30e50042e/USER', 9600),
    MCSample('mfv_ddbar_tau00300um_M3000', '/mfv_ddbar_tau00300um_M3000/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-a989911b8307b037b70d78770376a565/USER', 9500),
    MCSample('mfv_ddbar_tau01000um_M3000', '/mfv_ddbar_tau01000um_M3000/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-00dbe3af53b86679ab81b1546f649f69/USER', 9800),
    MCSample('mfv_ddbar_tau10000um_M3000', '/mfv_ddbar_tau10000um_M3000/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-32b77a1a2701fc5408c4cb9177d94fe1/USER', 9600),
    MCSample('mfv_ddbar_tau30000um_M3000', '/mfv_ddbar_tau30000um_M3000/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-91b5c6de7bcd3318c5cf96086a5d71dd/USER', 10000),
    ]

mfv_signal_samples = [
    MCSample('mfv_neu_tau00100um_M0300', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-100um_TuneCUETP8M1_13TeV-pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/AODSIM',  100000),
    MCSample('mfv_neu_tau00300um_M0300', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-300um_TuneCUETP8M1_13TeV-pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/AODSIM',  100000),
    MCSample('mfv_neu_tau01000um_M0300', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-1mm_TuneCUETP8M1_13TeV-pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v2/AODSIM',    100000),
    MCSample('mfv_neu_tau10000um_M0300', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-10mm_TuneCUETP8M1_13TeV-pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/AODSIM',    99302),
    MCSample('mfv_neu_tau30000um_M0300', '/mfv_neu_tau30000um_M0300/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-78fa28476a320b0d17459f4085218e86/USER', 10000),
    MCSample('mfv_neu_tau00100um_M0400', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-100um_TuneCUETP8M1_13TeV-pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/AODSIM',  100000),
    MCSample('mfv_neu_tau00300um_M0400', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-300um_TuneCUETP8M1_13TeV-pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v2/AODSIM',  100000),
    MCSample('mfv_neu_tau01000um_M0400', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-1mm_TuneCUETP8M1_13TeV-pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/AODSIM',    100000),
    MCSample('mfv_neu_tau10000um_M0400', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-10mm_TuneCUETP8M1_13TeV-pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/AODSIM',    99208),
    MCSample('mfv_neu_tau30000um_M0400', '/mfv_neu_tau30000um_M0400/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-78fa28476a320b0d17459f4085218e86/USER', 10000),
    MCSample('mfv_neu_tau00100um_M0500', '/mfv_neu_tau00100um_M0500/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-fd1230a2367467346289bcbf14b059e3/USER', 9800),
    MCSample('mfv_neu_tau00300um_M0500', '/mfv_neu_tau00300um_M0500/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-f63f7e76264567a015480e166c29a3f8/USER', 10000),
    MCSample('mfv_neu_tau01000um_M0500', '/mfv_neu_tau01000um_M0500/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-e84055c983e45954618b4bfc0693909b/USER', 9600),
    MCSample('mfv_neu_tau10000um_M0500', '/mfv_neu_tau10000um_M0500/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-44225b5f655304752a0c8f79adea3b43/USER', 9800),
    MCSample('mfv_neu_tau30000um_M0500', '/mfv_neu_tau30000um_M0500/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-bc775802f93affa8e53335c8e07b53a2/USER', 9900),
    MCSample('mfv_neu_tau00100um_M0600', '/mfv_neu_tau00100um_M0600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-61de7e7798ef8f788c198c43f09ebf3d/USER', 10000),
    MCSample('mfv_neu_tau00300um_M0600', '/mfv_neu_tau00300um_M0600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-36f33e35675d4fdda6e229a231c74a68/USER', 20000),
    MCSample('mfv_neu_tau01000um_M0600', '/mfv_neu_tau01000um_M0600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-36f33e35675d4fdda6e229a231c74a68/USER', 20000),
    MCSample('mfv_neu_tau10000um_M0600', '/mfv_neu_tau10000um_M0600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-61de7e7798ef8f788c198c43f09ebf3d/USER', 10000),
    MCSample('mfv_neu_tau30000um_M0600', '/mfv_neu_tau30000um_M0600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-61de7e7798ef8f788c198c43f09ebf3d/USER', 10000),
    MCSample('mfv_neu_tau00100um_M0800', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-100um_TuneCUETP8M1_13TeV-pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/AODSIM',   98260),
#    MCSample('my_mfv_neu_tau00300um_M0800', '/mfv_neu_tau00300um_M0800/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-36f33e35675d4fdda6e229a231c74a68/USER', 20000),
    MCSample('mfv_neu_tau00300um_M0800', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-300um_TuneCUETP8M1_13TeV-pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/AODSIM',  100000),
    MCSample('mfv_neu_tau01000um_M0800', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-1mm_TuneCUETP8M1_13TeV-pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v2/AODSIM',     99672),
    MCSample('mfv_neu_tau10000um_M0800', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-10mm_TuneCUETP8M1_13TeV-pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/AODSIM',   100000),
    MCSample('mfv_neu_tau30000um_M0800', '/mfv_neu_tau30000um_M0800/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-78fa28476a320b0d17459f4085218e86/USER', 10000),
    MCSample('mfv_neu_tau00100um_M1200', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-100um_TuneCUETP8M1_13TeV-pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v2/AODSIM',  99540),
    MCSample('mfv_neu_tau00300um_M1200', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-300um_TuneCUETP8M1_13TeV-pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau01000um_M1200', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-1mm_TuneCUETP8M1_13TeV-pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/AODSIM',   100000),
    MCSample('mfv_neu_tau10000um_M1200', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-10mm_TuneCUETP8M1_13TeV-pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v2/AODSIM',   99540),
    MCSample('mfv_neu_tau30000um_M1200', '/mfv_neu_tau30000um_M1200/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-78fa28476a320b0d17459f4085218e86/USER', 10000),
    MCSample('mfv_neu_tau00100um_M1600', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-100um_TuneCUETP8M1_13TeV-pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/AODSIM',  99734),
    MCSample('mfv_neu_tau00300um_M1600', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-300um_TuneCUETP8M1_13TeV-pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/AODSIM',  99999),
    MCSample('mfv_neu_tau01000um_M1600', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-1mm_TuneCUETP8M1_13TeV-pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/AODSIM',   100000),
    MCSample('mfv_neu_tau10000um_M1600', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-10mm_TuneCUETP8M1_13TeV-pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/AODSIM',   99751),
    MCSample('mfv_neu_tau30000um_M1600', '/mfv_neu_tau30000um_M1600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-78fa28476a320b0d17459f4085218e86/USER', 10000),
    MCSample('mfv_neu_tau00100um_M3000', '/mfv_neu_tau00100um_M3000/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-799254d98714d4bddcfc4dddd0b67e7b/USER', 9700),
    MCSample('mfv_neu_tau00300um_M3000', '/mfv_neu_tau00300um_M3000/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-799254d98714d4bddcfc4dddd0b67e7b/USER', 9800),
    MCSample('mfv_neu_tau01000um_M3000', '/mfv_neu_tau01000um_M3000/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-799254d98714d4bddcfc4dddd0b67e7b/USER', 9300),
    MCSample('mfv_neu_tau10000um_M3000', '/mfv_neu_tau10000um_M3000/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-799254d98714d4bddcfc4dddd0b67e7b/USER', 9500),
    MCSample('mfv_neu_tau30000um_M3000', '/mfv_neu_tau30000um_M3000/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-799254d98714d4bddcfc4dddd0b67e7b/USER', 9699),
    ]

mfv_bbbar_samples = [
    MCSample('mfv_bbbar_tau00100um_M0300', 'mfv_bbbar_tau00100um_M0300/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-e2312696cc7ea69e809b2d8f4fd549d4/USER', 0),
    MCSample('mfv_bbbar_tau00100um_M0400', 'mfv_bbbar_tau00100um_M0400/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-572d89de06044714d27eb5a9d439ab39/USER', 0),
    MCSample('mfv_bbbar_tau00100um_M0500', 'mfv_bbbar_tau00100um_M0500/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-bf39316f7a5785a89771d7870f54e817/USER', 0),
    MCSample('mfv_bbbar_tau00100um_M0600', 'mfv_bbbar_tau00100um_M0600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-71b06ca1b1bacee63218392f3dbdcd3f/USER', 0),
    MCSample('mfv_bbbar_tau00100um_M0800', 'mfv_bbbar_tau00100um_M0800/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-a68a5b9f1c3f88cc8a8d520a35405af9/USER', 0),
    MCSample('mfv_bbbar_tau00100um_M1200', 'mfv_bbbar_tau00100um_M1200/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-4e643b011d88ed2e3714d66d38abb503/USER', 0),
    MCSample('mfv_bbbar_tau00100um_M1600', 'mfv_bbbar_tau00100um_M1600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-942e13d5f7fb55c27cf29ab3b1aca28a/USER', 0),
    MCSample('mfv_bbbar_tau00100um_M3000', 'mfv_bbbar_tau00100um_M3000/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-40b3cb94f2c68b28f3a453ccbc4f2411/USER', 0),
    MCSample('mfv_bbbar_tau00300um_M0300', 'mfv_bbbar_tau00300um_M0300/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-2e8f7f56f92270a3abb9da4f19025231/USER', 0),
    MCSample('mfv_bbbar_tau00300um_M0400', 'mfv_bbbar_tau00300um_M0400/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-a26c7f4c7b251a7c2c8f3f21766b73a3/USER', 0),
    MCSample('mfv_bbbar_tau00300um_M0500', 'mfv_bbbar_tau00300um_M0500/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-c4310b6b2f5d69d3a0b80c37ad0800e7/USER', 0),
    MCSample('mfv_bbbar_tau00300um_M0600', 'mfv_bbbar_tau00300um_M0600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-62ffea31e86b0a2c54cb1f8e96bd4225/USER', 0),
    MCSample('mfv_bbbar_tau00300um_M0800', 'mfv_bbbar_tau00300um_M0800/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-713fca92db484107816a60f399be149d/USER', 0),
    MCSample('mfv_bbbar_tau00300um_M1200', 'mfv_bbbar_tau00300um_M1200/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-6fa43d1c6a5c32d57b387745844f8f87/USER', 0),
    MCSample('mfv_bbbar_tau00300um_M1600', 'mfv_bbbar_tau00300um_M1600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-d37b0569902388d6cff7915a173566ff/USER', 0),
    MCSample('mfv_bbbar_tau00300um_M3000', 'mfv_bbbar_tau00300um_M3000/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-e4f58251fd919f3ad42d3d0d4021b943/USER', 0),
    MCSample('mfv_bbbar_tau01000um_M0300', 'mfv_bbbar_tau01000um_M0300/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-6683393a614d78df9ab20fff39f3b0bf/USER', 0),
    MCSample('mfv_bbbar_tau01000um_M0400', 'mfv_bbbar_tau01000um_M0400/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-35d29bfc38c172850023843898d60268/USER', 0),
    MCSample('mfv_bbbar_tau01000um_M0500', 'mfv_bbbar_tau01000um_M0500/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-87fd9bb4ba1470d061b0d6ee093bce26/USER', 0),
    MCSample('mfv_bbbar_tau01000um_M0600', 'mfv_bbbar_tau01000um_M0600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-446ff6747b6bda9db4bb13ffb1bed977/USER', 0),
    MCSample('mfv_bbbar_tau01000um_M0800', 'mfv_bbbar_tau01000um_M0800/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-70d39ac15ee6d32428d726caaaf6b9da/USER', 0),
    MCSample('mfv_bbbar_tau01000um_M1200', 'mfv_bbbar_tau01000um_M1200/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-cab7daddce334b12b51839222f2f8601/USER', 0),
    MCSample('mfv_bbbar_tau01000um_M1600', 'mfv_bbbar_tau01000um_M1600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-7b2f1ad8c4d0f9650cc476ece3a1af2d/USER', 0),
    MCSample('mfv_bbbar_tau01000um_M3000', 'mfv_bbbar_tau01000um_M3000/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-a6d3d3436c6f2dcbbea5e89be3f580b4/USER', 0),
    MCSample('mfv_bbbar_tau10000um_M0300', 'mfv_bbbar_tau10000um_M0300/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-3aa3e489e37573d65cfc7d57329564df/USER', 0),
    MCSample('mfv_bbbar_tau10000um_M0400', 'mfv_bbbar_tau10000um_M0400/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-f1c2e296efd2adecaf1c213a381e4694/USER', 0),
    MCSample('mfv_bbbar_tau10000um_M0500', 'mfv_bbbar_tau10000um_M0500/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-eaf33c65a9626c8c1090fe7803b29dfa/USER', 0),
    MCSample('mfv_bbbar_tau10000um_M0600', 'mfv_bbbar_tau10000um_M0600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-4f6c12a8e9f73e4f9582b05e7e1e48e4/USER', 0),
    MCSample('mfv_bbbar_tau10000um_M0800', 'mfv_bbbar_tau10000um_M0800/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-042239d4588fc13ed59ebdd8c7a70612/USER', 0),
    MCSample('mfv_bbbar_tau10000um_M1200', 'mfv_bbbar_tau10000um_M1200/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-423a7bcd0295b01c662e6467d1da342c/USER', 0),
    MCSample('mfv_bbbar_tau10000um_M1600', 'mfv_bbbar_tau10000um_M1600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-1207d449751b3a2006d3cb0a4356d396/USER', 0),
    MCSample('mfv_bbbar_tau10000um_M3000', 'mfv_bbbar_tau10000um_M3000/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-1dcf7198c93eac1198f665d227d8faf1/USER', 0),
    MCSample('mfv_bbbar_tau30000um_M0300', 'mfv_bbbar_tau30000um_M0300/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-84843b9a018c9d96d8b6bcc603094f7c/USER', 0),
    MCSample('mfv_bbbar_tau30000um_M0400', 'mfv_bbbar_tau30000um_M0400/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-840fdb5d1716c6fc67c0ed84c74cdb1e/USER', 0),
    MCSample('mfv_bbbar_tau30000um_M0500', 'mfv_bbbar_tau30000um_M0500/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-7c8c67f8e1436b75ea54966c68dafcc3/USER', 0),
    MCSample('mfv_bbbar_tau30000um_M0600', 'mfv_bbbar_tau30000um_M0600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-274ddc780f125d4e78177dead7ab80f0/USER', 0),
    MCSample('mfv_bbbar_tau30000um_M0800', 'mfv_bbbar_tau30000um_M0800/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-a959c5485db64b3b384ff33e88b86de2/USER', 0),
    MCSample('mfv_bbbar_tau30000um_M1200', 'mfv_bbbar_tau30000um_M1200/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-10d9bb63db8ce4bf35b6a2e489a20c73/USER', 0),
    MCSample('mfv_bbbar_tau30000um_M1600', 'mfv_bbbar_tau30000um_M1600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-a2cd3ccf0cf49604c12300d01674deac/USER', 0),
    MCSample('mfv_bbbar_tau30000um_M3000', 'mfv_bbbar_tau30000um_M3000/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-4e49501f099cd99476d94589e7f17a71/USER', 0),
    ]

mfv_uds_samples = [
    MCSample('mfv_uds_tau00100um_M0300', 'mfv_uds_tau00100um_M0300/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-82b16b0a89bcdbb6f997347dae987231/USER', 0),
    MCSample('mfv_uds_tau00100um_M0400', 'mfv_uds_tau00100um_M0400/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-190567b8a45d92e19b0937a1e607866f/USER', 0),
    MCSample('mfv_uds_tau00100um_M0500', 'mfv_uds_tau00100um_M0500/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-119351233a87695361937858d3ae4269/USER', 0),
    MCSample('mfv_uds_tau00100um_M0600', 'mfv_uds_tau00100um_M0600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-b690613046588e4a2d27bbe9bbb41b6a/USER', 0),
    MCSample('mfv_uds_tau00100um_M0800', 'mfv_uds_tau00100um_M0800/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-326b336b4c4010146d44b2fc0a62a91a/USER', 0),
    MCSample('mfv_uds_tau00100um_M1200', 'mfv_uds_tau00100um_M1200/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-4d69dc682d46bc0b69daeaa5fa278c88/USER', 0),
    MCSample('mfv_uds_tau00100um_M1600', 'mfv_uds_tau00100um_M1600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-984a2431ee075f1ccf1389a52fa947f1/USER', 0),
    MCSample('mfv_uds_tau00100um_M3000', 'mfv_uds_tau00100um_M3000/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-6cf2d0405f7c6c3402a63d93e8c09da4/USER', 0),
    MCSample('mfv_uds_tau00300um_M0300', 'mfv_uds_tau00300um_M0300/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-5658bf62cf01672ccfad56db65844cdb/USER', 0),
    MCSample('mfv_uds_tau00300um_M0400', 'mfv_uds_tau00300um_M0400/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-17889d5ed12adbebaa13111021423dbe/USER', 0),
    MCSample('mfv_uds_tau00300um_M0500', 'mfv_uds_tau00300um_M0500/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-3a4e3c87e2543f37833f5c50394b2a72/USER', 0),
    MCSample('mfv_uds_tau00300um_M0600', 'mfv_uds_tau00300um_M0600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-e0dda3b7ef0e879c3c25757860675905/USER', 0),
    MCSample('mfv_uds_tau00300um_M0800', 'mfv_uds_tau00300um_M0800/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-5de3e18f05640f7bd6d9c153b9c656a3/USER', 0),
    MCSample('mfv_uds_tau00300um_M1200', 'mfv_uds_tau00300um_M1200/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-1911abd2630aedb00c0e3ecb22ab35da/USER', 0),
    MCSample('mfv_uds_tau00300um_M1600', 'mfv_uds_tau00300um_M1600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-ba3a6ecfa3a95295f2bedd9bfcb8cfec/USER', 0),
    MCSample('mfv_uds_tau00300um_M3000', 'mfv_uds_tau00300um_M3000/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-ed925c26da89d1d68de78dd5021ce263/USER', 0),
    MCSample('mfv_uds_tau01000um_M0300', 'mfv_uds_tau01000um_M0300/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-707c494914e0137bc6ef157243b4fbaa/USER', 0),
    MCSample('mfv_uds_tau01000um_M0400', 'mfv_uds_tau01000um_M0400/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-dfaa9f34779648453369e7fd004af8b0/USER', 0),
    MCSample('mfv_uds_tau01000um_M0500', 'mfv_uds_tau01000um_M0500/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-59eaff2d18ee87dba804899f7447a509/USER', 0),
    MCSample('mfv_uds_tau01000um_M0600', 'mfv_uds_tau01000um_M0600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-d7d8f44e862d5a1a4bb59996e2912ca1/USER', 0),
    MCSample('mfv_uds_tau01000um_M0800', 'mfv_uds_tau01000um_M0800/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-9f5c2b13a968eec72ddbe1069f4303b5/USER', 0),
    MCSample('mfv_uds_tau01000um_M1200', 'mfv_uds_tau01000um_M1200/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-c36c884bf6b595346b6b1c706b2b4c1c/USER', 0),
    MCSample('mfv_uds_tau01000um_M1600', 'mfv_uds_tau01000um_M1600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-db64aa8640ee5ef734c5dc2329a66eb1/USER', 0),
    MCSample('mfv_uds_tau01000um_M3000', 'mfv_uds_tau01000um_M3000/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-9e42325dfc13eb57750eaaf888856c08/USER', 0),
    MCSample('mfv_uds_tau10000um_M0300', 'mfv_uds_tau10000um_M0300/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-75158039a854929659171db558e3493e/USER', 0),
    MCSample('mfv_uds_tau10000um_M0400', 'mfv_uds_tau10000um_M0400/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-379557d73872185fb6f080481c8934a5/USER', 0),
    MCSample('mfv_uds_tau10000um_M0500', 'mfv_uds_tau10000um_M0500/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-af710099247a79005b22de863d21cc70/USER', 0),
    MCSample('mfv_uds_tau10000um_M0600', 'mfv_uds_tau10000um_M0600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-707c99e0eb520bf8364663e44551332f/USER', 0),
    MCSample('mfv_uds_tau10000um_M0800', 'mfv_uds_tau10000um_M0800/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-13a9111670fd1268c1ab5b9e50d4b8ea/USER', 0),
    MCSample('mfv_uds_tau10000um_M1200', 'mfv_uds_tau10000um_M1200/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-2d104c69cd09f40f9bc9b38eb8a87e2b/USER', 0),
    MCSample('mfv_uds_tau10000um_M1600', 'mfv_uds_tau10000um_M1600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-ce602be94b95f1dcd95d47930e15becd/USER', 0),
    MCSample('mfv_uds_tau10000um_M3000', 'mfv_uds_tau10000um_M3000/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-5d0445916a3c0a3b7bb7494f547f52bf/USER', 0),
    MCSample('mfv_uds_tau30000um_M0300', 'mfv_uds_tau30000um_M0300/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-2c660b5633ac3bfc2f9892609c3b8dc4/USER', 0),
    MCSample('mfv_uds_tau30000um_M0400', 'mfv_uds_tau30000um_M0400/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-933010a987c4c220a2c2aefb8c772642/USER', 0),
    MCSample('mfv_uds_tau30000um_M0500', 'mfv_uds_tau30000um_M0500/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-53ab585fb43e19eaa9231b0b3c9611d2/USER', 0),
    MCSample('mfv_uds_tau30000um_M0600', 'mfv_uds_tau30000um_M0600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-ddd8cdfd0c7263c5289979f5fa44ad3d/USER', 0),
    MCSample('mfv_uds_tau30000um_M0800', 'mfv_uds_tau30000um_M0800/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-8b9cc8d22fc8c3d810d5f93a06d802ef/USER', 0),
    MCSample('mfv_uds_tau30000um_M1200', 'mfv_uds_tau30000um_M1200/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-92c5cff29ac328d3a3f677e4095a600c/USER', 0),
    MCSample('mfv_uds_tau30000um_M1600', 'mfv_uds_tau30000um_M1600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-95155077a2e7410db0ec624eaa523f91/USER', 0),
    MCSample('mfv_uds_tau30000um_M3000', 'mfv_uds_tau30000um_M3000/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-57e0c50e2a1f9cf1cab70beae89c5363/USER', 0),
    ]

mfv_hip_samples = [ # dbs may be screwed up for these, and the ones that say "Premix" weren't really premixed, I just forgot to change the output name
    MCSample('mfv_ddbar_tau00100um_M0300_hip1p0_mit', '/mfv_ddbar_tau00100um_M0300/tucker-RunIISummer16DR80-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-90bd64cf19795b03775f4010661fcc0d/USER', 9899),
    MCSample('mfv_ddbar_tau00100um_M0400_hip1p0_mit', '/mfv_ddbar_tau00100um_M0400/tucker-RunIISummer16DR80-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-28ff807dea20cd8e63c6a95816485dda/USER', 9900),
    MCSample('mfv_ddbar_tau00100um_M0600_hip1p0_mit', '/mfv_ddbar_tau00100um_M0600/tucker-RunIISummer16DR80-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-a925963c387a03f42f3056a7591b39f6/USER', 9099),
    MCSample('mfv_ddbar_tau00100um_M0800_hip1p0_mit', '/mfv_ddbar_tau00100um_M0800/tucker-RunIISummer16DR80-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-0c3411e26e4f92a45de29b99910e7843/USER', 10000),
    MCSample('mfv_ddbar_tau00100um_M1200_hip1p0_mit', '/mfv_ddbar_tau00100um_M1200/tucker-RunIISummer16DR80-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-94859ae26a740f43f986c78962d8aed7/USER', 9800),
    MCSample('mfv_ddbar_tau00100um_M1600_hip1p0_mit', '/mfv_ddbar_tau00100um_M1600/tucker-RunIISummer16DR80-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-cd24b7eb5a3b0d5cdaba11ebed4a8452/USER', 9999),
    MCSample('mfv_ddbar_tau00300um_M0300_hip1p0_mit', '/mfv_ddbar_tau00300um_M0300/tucker-RunIISummer16DR80-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-a5ac261cd09a5fabd742c0c424d6b605/USER', 9998),
    MCSample('mfv_ddbar_tau00300um_M0400_hip1p0_mit', '/mfv_ddbar_tau00300um_M0400/tucker-RunIISummer16DR80-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-7615d19b05d4831c5b6a5044339c8e62/USER', 9998),
    MCSample('mfv_ddbar_tau00300um_M0600_hip1p0_mit', '/mfv_ddbar_tau00300um_M0600/tucker-RunIISummer16DR80-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-1a1577d7f30ab31178a8a99d78079bb0/USER', 9999),
    MCSample('mfv_ddbar_tau00300um_M0800_hip1p0_mit', '/mfv_ddbar_tau00300um_M0800/tucker-RunIISummer16DR80-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-05ce845954d1a80667f08c12e2b25312/USER', 9999),
    MCSample('mfv_ddbar_tau00300um_M1200_hip1p0_mit', '/mfv_ddbar_tau00300um_M1200/tucker-RunIISummer16DR80-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-dbcc00efe95ed6c550904089d24d934d/USER', 10000),
    MCSample('mfv_ddbar_tau00300um_M1600_hip1p0_mit', '/mfv_ddbar_tau00300um_M1600/tucker-RunIISummer16DR80-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-913624bbc8a5fddb50c2eef71960711d/USER', 9999),
    MCSample('mfv_ddbar_tau01000um_M0300_hip1p0_mit', '/mfv_ddbar_tau01000um_M0300/tucker-RunIISummer16DR80-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-e2e7a4655524b5290ca848b5f50d53bc/USER', 9899),
    MCSample('mfv_ddbar_tau01000um_M0400_hip1p0_mit', '/mfv_ddbar_tau01000um_M0400/tucker-RunIISummer16DR80-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-32fa0dbd1edfdf55e3319dc8484ae9f8/USER', 10000),
    MCSample('mfv_ddbar_tau01000um_M0600_hip1p0_mit', '/mfv_ddbar_tau01000um_M0600/tucker-RunIISummer16DR80-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-d0fbf5a9c10ed3a6e5d0db0d3279de16/USER', 9999),
    MCSample('mfv_ddbar_tau01000um_M0800_hip1p0_mit', '/mfv_ddbar_tau01000um_M0800/tucker-RunIISummer16DR80-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-7d1a2a9dc3c6f7579b80c299719d34fc/USER', 10000),
    MCSample('mfv_ddbar_tau01000um_M1200_hip1p0_mit', '/mfv_ddbar_tau01000um_M1200/tucker-RunIISummer16DR80-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-d4e1d646c95550a6c8f6e5d035d490d2/USER', 10000),
    MCSample('mfv_ddbar_tau01000um_M1600_hip1p0_mit', '/mfv_ddbar_tau01000um_M1600/tucker-RunIISummer16DR80-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-cf3245d7e9ecdcfcf1bde1c2eec6255e/USER', 9999),
    MCSample('mfv_ddbar_tau10000um_M0300_hip1p0_mit', '/mfv_ddbar_tau10000um_M0300/tucker-RunIISummer16DR80-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-0b945a400b8aa19f375ba4d2d2316336/USER', 9999),
    MCSample('mfv_ddbar_tau10000um_M0400_hip1p0_mit', '/mfv_ddbar_tau10000um_M0400/tucker-RunIISummer16DR80-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-f83f2f49f1798bd41da30473b5274102/USER', 10000),
    MCSample('mfv_ddbar_tau10000um_M0600_hip1p0_mit', '/mfv_ddbar_tau10000um_M0600/tucker-RunIISummer16DR80-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-20c5a8c51e5a6aab25bf9dcebaca7693/USER', 9999),
    MCSample('mfv_ddbar_tau10000um_M0800_hip1p0_mit', '/mfv_ddbar_tau10000um_M0800/tucker-RunIISummer16DR80-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-32a9bc80892d1df56493e3bb0cba4912/USER', 10000),
    MCSample('mfv_ddbar_tau10000um_M1200_hip1p0_mit', '/mfv_ddbar_tau10000um_M1200/tucker-RunIISummer16DR80-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-aef71f8615f73ba5f26edb8cdf7dda9b/USER', 10000),
    MCSample('mfv_ddbar_tau10000um_M1600_hip1p0_mit', '/mfv_ddbar_tau10000um_M1600/tucker-RunIISummer16DR80-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-271af1956bd767fcfe52a2f6e9a77e14/USER', 9999),
    MCSample('mfv_ddbar_tau30000um_M0300_hip1p0_mit', '/mfv_ddbar_tau30000um_M0300/tucker-RunIISummer16DR80-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-2297d1b6761c4cd6a465ba38b0dac32b/USER', 9998),
    MCSample('mfv_ddbar_tau30000um_M0400_hip1p0_mit', '/mfv_ddbar_tau30000um_M0400/tucker-RunIISummer16DR80-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-6f45e894e5360dc0d647ee9fa7a6935e/USER', 9998),
    MCSample('mfv_ddbar_tau30000um_M0600_hip1p0_mit', '/mfv_ddbar_tau30000um_M0600/tucker-RunIISummer16DR80-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-19080caac7381b60c4e5b84985845ccf/USER', 9899),
    MCSample('mfv_ddbar_tau30000um_M0800_hip1p0_mit', '/mfv_ddbar_tau30000um_M0800/tucker-RunIISummer16DR80-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-4e69d3fb42967f75d7c7bc20745aadbb/USER', 9899),
    MCSample('mfv_ddbar_tau30000um_M1200_hip1p0_mit', '/mfv_ddbar_tau30000um_M1200/tucker-RunIISummer16DR80-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-e3b3706ef0656cf6a95cfffce6bedd85/USER', 10000),
    MCSample('mfv_ddbar_tau30000um_M1600_hip1p0_mit', '/mfv_ddbar_tau30000um_M1600/tucker-RunIISummer16DR80-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-04fbfd0e4530245774d5c7cff77a5454/USER', 9999),

    MCSample('mfv_neu_tau00100um_M0300_hip1p0_mit', '/mfv_neu_tau00100um_M0300/tucker-RunIISummer16DR80-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-5a3eecd2420295c27d0388f848249d61/USER', 10000),
    MCSample('mfv_neu_tau00100um_M0400_hip1p0_mit', '/mfv_neu_tau00100um_M0400/tucker-RunIISummer16DR80-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-1c8be84001ad3413875ff3b496f0d2eb/USER', 10000),
    MCSample('mfv_neu_tau00100um_M0600_hip1p0_mit', '/mfv_neu_tau00100um_M0600/tucker-RunIISummer16DR80-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-5036e0af297a9a2eaae95ae8ef29ddbc/USER', 10000),
    MCSample('mfv_neu_tau00100um_M0800_hip1p0_mit', '/mfv_neu_tau00100um_M0800/tucker-RunIISummer16DR80-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-c6d266562f6eaadff33e4f5f6c17bd00/USER', 10000),
    MCSample('mfv_neu_tau00100um_M1200_hip1p0_mit', '/mfv_neu_tau00100um_M1200/tucker-RunIISummer16DR80-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-3c4ab1c3ce01f3e61ab7e4be11b5d90e/USER',  9900),
    MCSample('mfv_neu_tau00100um_M1600_hip1p0_mit', '/mfv_neu_tau00100um_M1600/tucker-RunIISummer16DR80-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-de4d2dc7022f797bf09a44fd87f0e9ec/USER', 10000),
    MCSample('mfv_neu_tau00300um_M0300_hip1p0_mit', '/mfv_neu_tau00300um_M0300/tucker-RunIISummer16DR80-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-8c375f6fd1f86660f07ff7ab2cdaff23/USER', 10000),
    MCSample('mfv_neu_tau00300um_M0400_hip1p0_mit', '/mfv_neu_tau00300um_M0400/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-5f5d6ef2ffb6a650dd2c91d2feda49ce/USER', 10000),
    MCSample('mfv_neu_tau00300um_M0600_hip1p0_mit', '/mfv_neu_tau00300um_M0600/tucker-RunIISummer16DR80-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-ea3f7182fc528c697f53243a6a1651ab/USER',  9900),
    MCSample('mfv_neu_tau00300um_M0800_hip1p0_mit', '/mfv_neu_tau00300um_M0800/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-42adc6a10357c55389b6a60e7bd3274b/USER', 10000),
    MCSample('mfv_neu_tau00300um_M1200_hip1p0_mit', '/mfv_neu_tau00300um_M1200/tucker-RunIISummer16DR80-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-73661668b137dc695d6822a771b25575/USER', 10000),
    MCSample('mfv_neu_tau00300um_M1600_hip1p0_mit', '/mfv_neu_tau00300um_M1600/tucker-RunIISummer16DR80-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-a2e8ee16064263ed40bc3da661d11807/USER', 10000),
    MCSample('mfv_neu_tau01000um_M0300_hip1p0_mit', '/mfv_neu_tau01000um_M0300/tucker-RunIISummer16DR80-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-53834c01b4a118bf086ed6844fbeb601/USER', 10000),
    MCSample('mfv_neu_tau01000um_M0400_hip1p0_mit', '/mfv_neu_tau01000um_M0400/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-3824911761fa1d58c752de20493bfc44/USER', 10000),
    MCSample('mfv_neu_tau01000um_M0600_hip1p0_mit', '/mfv_neu_tau01000um_M0600/tucker-RunIISummer16DR80-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-a2b32d06ff4ad0ded0a6a7c67f98da50/USER', 10000),
    MCSample('mfv_neu_tau01000um_M0800_hip1p0_mit', '/mfv_neu_tau01000um_M0800/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-7465d401a02b15ec03cc491dd62ad01c/USER', 10000),
    MCSample('mfv_neu_tau01000um_M1200_hip1p0_mit', '/mfv_neu_tau01000um_M1200/tucker-RunIISummer16DR80-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-1be23432e9938b1c353f87865bfb7087/USER',  9800),
    MCSample('mfv_neu_tau01000um_M1600_hip1p0_mit', '/mfv_neu_tau01000um_M1600/tucker-RunIISummer16DR80-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-9cdd88a04e8a3dc235435bf2e02f1693/USER', 10000),
    MCSample('mfv_neu_tau10000um_M0300_hip1p0_mit', '/mfv_neu_tau10000um_M0300/tucker-RunIISummer16DR80-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-5a1205472e4736b56bb1ba1025953703/USER', 10000),
    MCSample('mfv_neu_tau10000um_M0400_hip1p0_mit', '/mfv_neu_tau10000um_M0400/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-49f888181b3f2e089819514e45257b78/USER', 10000),
    MCSample('mfv_neu_tau10000um_M0600_hip1p0_mit', '/mfv_neu_tau10000um_M0600/tucker-RunIISummer16DR80-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-8bc7e45b2962bc1d6c9d69860c7f9216/USER', 10000),
    MCSample('mfv_neu_tau10000um_M0800_hip1p0_mit', '/mfv_neu_tau10000um_M0800/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-aba1e2e9fe3baf3380691657497b73bd/USER', 10000),
    MCSample('mfv_neu_tau10000um_M1200_hip1p0_mit', '/mfv_neu_tau10000um_M1200/tucker-RunIISummer16DR80-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-2af3dfe5c8498bd771394a9549a5b8e1/USER', 10000),
    MCSample('mfv_neu_tau10000um_M1600_hip1p0_mit', '/mfv_neu_tau10000um_M1600/tucker-RunIISummer16DR80-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-a0618d3a7397d352513e67d3d3806277/USER', 10000),
    MCSample('mfv_neu_tau30000um_M0300_hip1p0_mit', '/mfv_neu_tau30000um_M0300/tucker-RunIISummer16DR80-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-a6e54faba20a3730605411bf507a8f24/USER', 10000),
    MCSample('mfv_neu_tau30000um_M0400_hip1p0_mit', '/mfv_neu_tau30000um_M0400/tucker-RunIISummer16DR80-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-26f985ebd88bed1aaede31ebc8d48d87/USER', 10000),
    MCSample('mfv_neu_tau30000um_M0600_hip1p0_mit', '/mfv_neu_tau30000um_M0600/tucker-RunIISummer16DR80-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-08aa1554f299a3c65ae7c273e4f9ed4b/USER', 10000),
    MCSample('mfv_neu_tau30000um_M0800_hip1p0_mit', '/mfv_neu_tau30000um_M0800/tucker-RunIISummer16DR80-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-69ec92defa19865dacb7728bcbde95da/USER', 10000),
    MCSample('mfv_neu_tau30000um_M1200_hip1p0_mit', '/mfv_neu_tau30000um_M1200/tucker-RunIISummer16DR80-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-cfc324797066dd2bb0b6e13e3dabada3/USER',  9900),
    MCSample('mfv_neu_tau30000um_M1600_hip1p0_mit', '/mfv_neu_tau30000um_M1600/tucker-RunIISummer16DR80-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-c5e763a88dabdb717409c32ce672b20d/USER', 10000),
    ]

for s in mfv_ddbar_samples + mfv_signal_samples + mfv_bbbar_samples + mfv_uds_samples + mfv_hip_samples:
    _set_tau_mass(s)
    s.xsec = 1e-3
    s.is_private = s.dataset.startswith('/mfv_')
    if s.is_private:
        s.dbs_inst = 'phys03'
        s.condor = True

qcd_hip_samples = [
    MCSample('qcdht0700_hip1p0_mit', '/qcdht0700/tucker-RunIISummer16DR80-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-de9e9f9c2951885a85d93dfb6395e7a7/USER', 25257, xsec=6.802e3),
    MCSample('qcdht1000_hip1p0_mit', '/qcdht1000/None/USER', 511738 + 447284 + 435441, xsec=1.206e3),
    MCSample('qcdht1500_hip1p0_mit', '/qcdht1500/tucker-RunIISummer16DR80-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-88f7eac3ad6536b10bb56426728dc593/USER', 446881, xsec=120),
    ]

for s in qcd_hip_samples:
    s.is_private = True
    s.dbs_inst = 'phys03'
    s.condor = True

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

    DataSample('ZeroBias2016B3', '/ZeroBias/Run2016B-23Sep2016-v3/AOD'),
    DataSample('ZeroBias2016C', '/ZeroBias/Run2016C-23Sep2016-v1/AOD'),
    DataSample('ZeroBias2016D', '/ZeroBias/Run2016D-23Sep2016-v1/AOD'),
    DataSample('ZeroBias2016E', '/ZeroBias/Run2016E-23Sep2016-v1/AOD'),
    DataSample('ZeroBias2016F', '/ZeroBias/Run2016F-23Sep2016-v1/AOD'),
    DataSample('ZeroBias2016G', '/ZeroBias/Run2016G-23Sep2016-v1/AOD'),
    DataSample('ZeroBias2016H2', '/ZeroBias/Run2016H-PromptReco-v2/AOD'),
    DataSample('ZeroBias2016H3', '/ZeroBias/Run2016H-PromptReco-v3/AOD'),

    DataSample('ReproJetHT2016B', '/JetHT/Run2016B-18Apr2017_ver2-v1/AOD'),
    DataSample('ReproJetHT2016C', '/JetHT/Run2016C-18Apr2017-v1/AOD'),
    DataSample('ReproJetHT2016D', '/JetHT/Run2016D-18Apr2017-v1/AOD'),
    DataSample('ReproJetHT2016E', '/JetHT/Run2016E-18Apr2017-v1/AOD'),
    DataSample('ReproJetHT2016F', '/JetHT/Run2016F-18Apr2017-v1/AOD'),
    DataSample('ReproJetHT2016G', '/JetHT/Run2016G-18Apr2017-v1/AOD'),
    DataSample('ReproJetHT2016H', '/JetHT/Run2016H-18Apr2017-v1/AOD'),
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
    'qcd_hip_samples',
    'ttbar_samples',
    'leptonic_background_samples',
    'minbias_samples',
    'mfv_ddbar_samples',
    'mfv_signal_samples',
    'mfv_bbbar_samples',
    'mfv_uds_samples',
    'mfv_hip_samples',
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

# none

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

for x in data_samples + [qcdht0700, qcdht2000, ttbar, mfv_neu_tau01000um_M0600, mfv_neu_tau30000um_M0800, mfv_ddbar_tau00300um_M0400, mfv_ddbar_tau00300um_M0800, mfv_ddbar_tau01000um_M0400, mfv_ddbar_tau01000um_M0800]:
    x.add_dataset('validation')
    x.datasets['validation'].condor = True

for x in (data_samples_2015 +
          ttbar_samples_2015 + qcd_samples_2015 + qcd_samples_ext_2015 +
          mfv_signal_samples_2015 +
          data_samples +
          ttbar_samples + qcd_samples + qcd_samples_ext +
          mfv_signal_samples + mfv_ddbar_samples + mfv_hip_samples + qcd_hip_samples):
    x.add_dataset('ntuplev15')
    x.add_dataset('ntuplev16')
    if not x.is_signal:
        x.add_dataset('ntuplev16_ntkseeds')

for x in data_samples + qcd_samples + qcd_samples_ext + qcd_hip_samples[-2:]:
    x.add_dataset('v0ntuplev1')
for x in data_samples + [s for s in auxiliary_data_samples if s.name.startswith('ZeroBias')] + qcd_samples[2:4] + qcd_samples_ext[2:4]:
    x.add_dataset('v0ntuplev2')

for x in mfv_signal_samples + mfv_ddbar_samples:
    for y in '3p7', '3p8', '3p9', '4p1', '4p2', '4p3':
        x.add_dataset('ntuplev15_sigmadxy%s' % y)

for x in mfv_signal_samples_2015 + mfv_signal_samples + mfv_ddbar_samples + mfv_hip_samples:
    x.add_dataset('ntuplev16_wgenv2')

for x in 'ntuplev15lep', 'ntuplev15lep_IsoMu24', 'ntuplev15lep_IsoTkMu24', 'ntuplev15lep_VVVL350', 'ntuplev15lep_VVVL400', 'ntuplev15lep_Mu50':
    mfv_neu_tau01000um_M0300.add_dataset(x)

for x in mfv_neu_tau00100um_M0300, mfv_neu_tau01000um_M0300:
    x.add_dataset('ntuplev15_leptrigs')

########
# other condor declarations
########

for x in data_samples_2015 + qcd_samples + qcd_samples_ext + [ttbar, mfv_neu_tau00300um_M1600, mfv_neu_tau10000um_M1600]:
    if x not in (qcdht0500, qcdht0700):
        x.condor = True
JetHT2015D.xrootd_url = 'root://dcache-cms-xrootd.desy.de/'
qcdht1000ext.xrootd_url = 'root://dcache-cms-xrootd.desy.de/'
for x in qcdht2000ext, ttbar, mfv_neu_tau10000um_M1600:
    x.xrootd_url = 'root://cmseos.fnal.gov/'

for x in (qcdht0500_2015, qcdht0700_2015, qcdht1000_2015, qcdht2000_2015, qcdht0500ext_2015, qcdht1500ext_2015, qcdht2000ext_2015, ttbar_2015):
    x.condor = True
    x.xrootd_url = 'root://cmseos.fnal.gov/'

for x in qcd_samples_2015:
    x.datasets['miniaod'].condor = True
    x.datasets['miniaod'].xrootd_url = 'root://cmseos.fnal.gov/'

for x in (JetHT2016B3,
          qcdht0700, qcdht1000, qcdht1500, qcdht0700ext, qcdht1500ext, qcdht2000ext, ttbar,
          mfv_neu_tau10000um_M0300, mfv_neu_tau01000um_M0400, mfv_neu_tau00100um_M0800,
          mfv_neu_tau00300um_M0800, mfv_neu_tau01000um_M1200, mfv_neu_tau00100um_M1600, mfv_neu_tau10000um_M1600):
    x.datasets['miniaod'].condor = True

ttbar_2015.datasets['miniaod'].condor = True
ttbar_2015.datasets['miniaod'].xrootd_url = 'root://dcache-cms-xrootd.desy.de/'

ds4condor = ['ntuple', 'v0ntuple', 'pick1vtx']
for s in registry.all():
    for ds in s.datasets.keys():
        for ds4 in ds4condor:
            if ds.startswith(ds4):
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
                if s.name.startswith('mfv_') or s.name.startswith('xx4j') or s.name.startswith('mfv_'): #'sum' not in s.name:
                    for ds in ('ntuplev11',): #'miniaod', 'ntuplev11':
                        if (s.name.startswith('mfv_') or s.name.startswith('xx4j')) and ds == 'miniaod':
                            continue
                        if not s.has_dataset(ds):
                            print s.name, 'no', ds
                        else:
                            if not _d.has_key((s.name, 'ntuplev11')):
                                print s.name, 'no files'

    if 0:
        for x in registry.all():
            if x.condor:
                if x.is_signal and x.is_private:
                    continue
                print x.name
        # for x in $(<curr_condor.txt); samples site $x main

    if 0:
        for l in [mfv_signal_samples]:
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
        for s in mfv_signal_samples:
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

    if 0:
        dses = set(s.dataset for s in registry.all())
        for line in open('todel.txt'):
            line = line.strip()
            if line in dses:
                print line
