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
    s.dbs_inst = 'phys03'
    s.xsec = 1e-3
    s.condor = True

for s in xx4j_samples_2015:
    _set_tau_mass(s)
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
    MCSample('mfv_neu_tau00100um_M0600', '/mfv_neu_tau00100um_M0600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-61de7e7798ef8f788c198c43f09ebf3d/USER', 10000),
    MCSample('mfv_neu_tau00300um_M0600', '/mfv_neu_tau00300um_M0600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-36f33e35675d4fdda6e229a231c74a68/USER', 20000),
    MCSample('mfv_neu_tau01000um_M0600', '/mfv_neu_tau01000um_M0600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-36f33e35675d4fdda6e229a231c74a68/USER', 20000),
    MCSample('mfv_neu_tau10000um_M0600', '/mfv_neu_tau10000um_M0600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-61de7e7798ef8f788c198c43f09ebf3d/USER', 10000),
    MCSample('mfv_neu_tau30000um_M0600', '/mfv_neu_tau30000um_M0600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-61de7e7798ef8f788c198c43f09ebf3d/USER', 10000),
    MCSample('mfv_neu_tau00100um_M0800', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-100um_TuneCUETP8M1_13TeV-pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/AODSIM',   98260),
    MCSample('my_mfv_neu_tau00300um_M0800', '/mfv_neu_tau00300um_M0800/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-36f33e35675d4fdda6e229a231c74a68/USER', 20000),
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

mfv_hip_samples = [
    MCSample('mfv_ddbar_tau00300um_M0400_hip1p0', '/mfv_ddbar_tau00300um_M0400/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-99716630a6bfd21a8e13f2d8e0d595b6/USER', 10000),
    MCSample('mfv_ddbar_tau00300um_M0800_hip1p0', '/mfv_ddbar_tau00300um_M0800/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-99716630a6bfd21a8e13f2d8e0d595b6/USER', 9998),
    MCSample('mfv_ddbar_tau01000um_M0400_hip1p0', '/mfv_ddbar_tau01000um_M0400/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-99716630a6bfd21a8e13f2d8e0d595b6/USER', 9999),
    MCSample('mfv_ddbar_tau01000um_M0800_hip1p0', '/mfv_ddbar_tau01000um_M0800/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-99716630a6bfd21a8e13f2d8e0d595b6/USER', 10000),
    MCSample('mfv_ddbar_tau10000um_M0400_hip1p0', '/mfv_ddbar_tau10000um_M0400/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-99716630a6bfd21a8e13f2d8e0d595b6/USER', 10000),
    MCSample('mfv_ddbar_tau10000um_M0800_hip1p0', '/mfv_ddbar_tau10000um_M0800/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-99716630a6bfd21a8e13f2d8e0d595b6/USER', 9999),
    MCSample('mfv_neu_tau00300um_M0400_hip1p0', '/mfv_neu_tau00300um_M0400/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-977e3d201d318113a6b581d0cdd1aa65/USER', 10000),
    MCSample('mfv_neu_tau00300um_M0800_hip1p0', '/mfv_neu_tau00300um_M0800/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-977e3d201d318113a6b581d0cdd1aa65/USER', 10000),
    MCSample('mfv_neu_tau01000um_M0400_hip1p0', '/mfv_neu_tau01000um_M0400/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-977e3d201d318113a6b581d0cdd1aa65/USER', 10000),
    MCSample('mfv_neu_tau01000um_M0800_hip1p0', '/mfv_neu_tau01000um_M0800/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-2e7a8ef3d2ddf172de431b4420ab6ecf/USER', 10000),
    MCSample('mfv_neu_tau10000um_M0400_hip1p0', '/mfv_neu_tau10000um_M0400/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-977e3d201d318113a6b581d0cdd1aa65/USER', 10000),
    MCSample('mfv_neu_tau10000um_M0800_hip1p0', '/mfv_neu_tau10000um_M0800/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-2e7a8ef3d2ddf172de431b4420ab6ecf/USER', 10000),
    ]

for s in mfv_ddbar_samples + mfv_signal_samples + mfv_hip_samples:
    _set_tau_mass(s)
    s.xsec = 1e-3
    s.is_private = s.dataset.startswith('/mfv_')
    if s.is_private:
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

SingleMuon2016B3.add_dataset('trigskimv1', '/SingleMuon/tucker-TrigSkimV1-6ba5dd8c9a33aab8a6e2472789317878/USER', 35241)
SingleMuon2016C.add_dataset('trigskimv1', '/SingleMuon/tucker-TrigSkimV1-82edc478e1c389712ac7b0eb3d3b0434/USER', 18229)
SingleMuon2016D.add_dataset('trigskimv1', '/SingleMuon/tucker-TrigSkimV1-1ed6f4ab317ce7bb7309546437e1421b/USER', 31034)
SingleMuon2016E.add_dataset('trigskimv1', '/SingleMuon/tucker-TrigSkimV1-5cf9154b23f7eea54d7241d0e9a81907/USER', 29185)
SingleMuon2016F.add_dataset('trigskimv1', '/SingleMuon/tucker-TrigSkimV1-eb2acd8cc58caef922ab0468b30922df/USER', 21755)
SingleMuon2016G.add_dataset('trigskimv1', '/SingleMuon/tucker-TrigSkimV1-10a79bb3ddc729731322877ecdf5fef6/USER', 51891)
SingleMuon2016H2.add_dataset('trigskimv1', '/SingleMuon/tucker-TrigSkimV1-04ce4943aa061593fed4ddb8c85f283c/USER', 139374)
SingleMuon2016H3.add_dataset('trigskimv1', '/SingleMuon/tucker-TrigSkimV1-42f42c38f8f1c9713ac6dac6d8fe4da2/USER', 3706)

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

for x in data_samples + [qcdht0700, qcdht2000, ttbar, my_mfv_neu_tau00300um_M0800, mfv_neu_tau01000um_M0600, mfv_neu_tau30000um_M0800, mfv_ddbar_tau00300um_M0400, mfv_ddbar_tau00300um_M0800, mfv_ddbar_tau01000um_M0400, mfv_ddbar_tau01000um_M0800]:
    x.add_dataset('validation')
    x.datasets['validation'].condor = True

for x in data_samples + data_samples_2015 + \
        ttbar_samples + ttbar_samples_2015 + qcd_samples + qcd_samples_2015 + qcd_samples_ext + qcd_samples_ext_2015 + \
        mfv_signal_samples + mfv_signal_samples_2015 + mfv_ddbar_samples + mfv_hip_samples:
    x.add_dataset('ntuplev14')

for x in ttbar_samples + ttbar_samples_2015 + qcd_samples + qcd_samples_ext + qcd_samples_2015 + qcd_samples_ext_2015 + data_samples + data_samples_2015:
    if x.name != 'qcdht0700':
        x.add_dataset('pick1vtxv14')

for x in ttbar_samples + qcd_samples + qcd_samples_ext:
    x.add_dataset('ntuplev14p2')
    x.add_dataset('ntuplev14p2_3tkseeds')
    x.add_dataset('ntuplev14p2_4tkseeds')
    x.add_dataset('ntuplev14p2_5tkseeds')

########
# other condor declarations
########

JetHT2015C.condor = True
JetHT2015D.condor = True
JetHT2015D.xrootd_url = 'root://dcache-cms-xrootd.desy.de/'

for x in (qcdht2000ext,
          qcdht0500_2015, qcdht0700_2015, qcdht1000_2015, qcdht1500_2015, qcdht2000_2015,
          qcdht0500ext_2015, qcdht0700ext_2015, qcdht1000ext_2015, qcdht1500ext_2015, qcdht2000ext_2015,
          ttbar_2015, ttbar):
    x.condor = True
    x.xrootd_url = 'root://cmseos.fnal.gov/'

for x in (JetHT2016G,
          SingleMuon2016B3, SingleMuon2016C, SingleMuon2016E, SingleMuon2016H2,
          qcdht0500, qcdht1500, qcdht0500ext, qcdht0700ext, qcdht1000ext, qcdht1500ext, #qcdht2000,
          wjetstolnu, dyjetstollM50, qcdmupt15,
          mfv_neu_tau00100um_M0300, mfv_neu_tau10000um_M0300,
          mfv_neu_tau00100um_M0800, mfv_neu_tau00300um_M0800, mfv_neu_tau01000um_M0800,
          mfv_neu_tau01000um_M1200, mfv_neu_tau10000um_M1200,
          mfv_neu_tau00100um_M1600, mfv_neu_tau10000um_M1600,
          mfv_neu_tau10000um_M0800,
          xx4j_tau00001mm_M0300_2015, xx4j_tau00003mm_M0300_2015, xx4j_tau00300mm_M0300_2015, xx4j_tau01000mm_M0300_2015, xx4j_tau02000mm_M0300_2015, xx4j_tau00010mm_M0500_2015, xx4j_tau00010mm_M0700_2015, xx4j_tau00300mm_M1500_2015, xx4j_tau01000mm_M1500_2015, xx4j_tau00003mm_M3000_2015, xx4j_tau00100mm_M3000_2015, xx4j_tau00300mm_M3000_2015, xx4j_tau01000mm_M3000_2015, xx4j_tau02000mm_M3000_2015,
          ):
    x.condor = True

#qcdht2000.xrootd_url = 'root://ccmsdlf.ads.rl.ac.uk//castor/ads.rl.ac.uk/prod/cms/disk'
mfv_neu_tau10000um_M1200.xrootd_url = 'root://xrootd2.ihepa.ufl.edu/'
mfv_neu_tau00300um_M0800.xrootd_url = 'root://cmseos.fnal.gov/'

for x in qcd_samples_2015:
    x.datasets['miniaod'].condor = True
    x.datasets['miniaod'].xrootd_url = 'root://cmseos.fnal.gov/'

for x in (JetHT2016B3,
          SingleMuon2016B3, SingleMuon2016C, SingleMuon2016E,
          qcdht0700, qcdht1000, qcdht1500, qcdht0700ext, qcdht1500ext, qcdht2000ext, ttbar,
          mfv_neu_tau10000um_M0300, mfv_neu_tau01000um_M0400, mfv_neu_tau00100um_M0800,
          mfv_neu_tau00300um_M0800, mfv_neu_tau01000um_M1200, mfv_neu_tau00100um_M1600, mfv_neu_tau10000um_M1600):
    x.datasets['miniaod'].condor = True

ttbar_2015.datasets['miniaod'].condor = True
ttbar_2015.datasets['miniaod'].xrootd_url = 'root://dcache-cms-xrootd.desy.de/'

for s in registry.all():
    for ds in s.datasets.keys():
        if ds.startswith('ntuple') or ds.startswith('pick1vtx'):
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
