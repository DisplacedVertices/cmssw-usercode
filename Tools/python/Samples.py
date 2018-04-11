#!/usr/bin/env python

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

all_signal_samples_2015 = mfv_signal_samples_2015 # don't use xx4j

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

# dbs is broken for neuuds, neuudmu, bbbar, uds

mfv_neuuds_samples = [
    MCSample('mfv_neuuds_tau00100um_M0300', '/mfv_neuuds_tau00100um_M0300/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-7f45ada5c6d257f35e0d6633216dc5db/USER', 10000),
    MCSample('mfv_neuuds_tau00100um_M0400', '/mfv_neuuds_tau00100um_M0400/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-c5ebd81d56588ad1c8d57b8c52aa2073/USER', 10000),
    MCSample('mfv_neuuds_tau00100um_M0500', '/mfv_neuuds_tau00100um_M0500/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-f3008c7a3a2014a63ef2256ccc27220d/USER', 10000),
    MCSample('mfv_neuuds_tau00100um_M0600', '/mfv_neuuds_tau00100um_M0600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-d918a0c482492b778579f09d284f66f0/USER', 9900),
    MCSample('mfv_neuuds_tau00100um_M0800', '/mfv_neuuds_tau00100um_M0800/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-fdc427c7e6aaa75a1b481c95ea7c9ec0/USER', 9900),
    MCSample('mfv_neuuds_tau00100um_M1200', '/mfv_neuuds_tau00100um_M1200/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-4c904855a8c5d6899473f607ee889c15/USER', 10000),
    MCSample('mfv_neuuds_tau00100um_M1600', '/mfv_neuuds_tau00100um_M1600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-5008b5e05bf0d8ca7dd63a2621862dd0/USER', 9800),
    MCSample('mfv_neuuds_tau00100um_M3000', '/mfv_neuuds_tau00100um_M3000/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-dc55b40002d7f6f4cf68260841bc7f7b/USER', 9900),
    MCSample('mfv_neuuds_tau00300um_M0300', '/mfv_neuuds_tau00300um_M0300/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-990ccf1ff2c22b389cf0a3262a93978a/USER', 10000),
    MCSample('mfv_neuuds_tau00300um_M0400', '/mfv_neuuds_tau00300um_M0400/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-135f8a84faf9ddf34e1846429dc68cbd/USER', 10000),
    MCSample('mfv_neuuds_tau00300um_M0500', '/mfv_neuuds_tau00300um_M0500/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-dc4f47ed7ecb84f48f119407f835fa93/USER', 10000),
    MCSample('mfv_neuuds_tau00300um_M0600', '/mfv_neuuds_tau00300um_M0600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-4253316dacecac4fec2f799380aaaae8/USER', 10000),
    MCSample('mfv_neuuds_tau00300um_M0800', '/mfv_neuuds_tau00300um_M0800/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-62b30cbe9e0849f7eaee4bc1ab7aad9a/USER', 10000),
    MCSample('mfv_neuuds_tau00300um_M1200', '/mfv_neuuds_tau00300um_M1200/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-fbd6334fe08d4dc2c08d9fec02295e78/USER', 10000),
    MCSample('mfv_neuuds_tau00300um_M1600', '/mfv_neuuds_tau00300um_M1600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-efc7d87ac4d5d1fc54822f47119cd302/USER', 10000),
    MCSample('mfv_neuuds_tau00300um_M3000', '/mfv_neuuds_tau00300um_M3000/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-6a87a8405d8c4ca88af816eb6beb8120/USER', 9700),
    MCSample('mfv_neuuds_tau01000um_M0300', '/mfv_neuuds_tau01000um_M0300/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-4310c996e89cd3abdc785efe036e2f5a/USER', 10000),
    MCSample('mfv_neuuds_tau01000um_M0400', '/mfv_neuuds_tau01000um_M0400/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-5c172dbc64c52d3f0e74b370c125e2f3/USER', 10000),
    MCSample('mfv_neuuds_tau01000um_M0500', '/mfv_neuuds_tau01000um_M0500/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-76e45140919559d4058d42fbeb47e390/USER', 10000),
    MCSample('mfv_neuuds_tau01000um_M0600', '/mfv_neuuds_tau01000um_M0600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-d33c5e5985f6614d8e55deec5339809c/USER', 10000),
    MCSample('mfv_neuuds_tau01000um_M0800', '/mfv_neuuds_tau01000um_M0800/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-7c24c1e11ee17eece141e90c36f8f222/USER', 10000),
    MCSample('mfv_neuuds_tau01000um_M1200', '/mfv_neuuds_tau01000um_M1200/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-4661932641c4506f7cf876a9d4422d90/USER', 10000),
    MCSample('mfv_neuuds_tau01000um_M1600', '/mfv_neuuds_tau01000um_M1600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-f48b9ca5a13623e7c20f4d948d776ed2/USER', 9800),
    MCSample('mfv_neuuds_tau01000um_M3000', '/mfv_neuuds_tau01000um_M3000/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-fc4fd786dc709903030dd46c1b3d59a0/USER', 9900),
    MCSample('mfv_neuuds_tau10000um_M0300', '/mfv_neuuds_tau10000um_M0300/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-b927599309b646fdeb340a3bddee39d9/USER', 10000),
    MCSample('mfv_neuuds_tau10000um_M0400', '/mfv_neuuds_tau10000um_M0400/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-14e70c271d96921b04cfc57bbd4b8afd/USER', 10000),
    MCSample('mfv_neuuds_tau10000um_M0500', '/mfv_neuuds_tau10000um_M0500/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-93fdc40fbe1cc4266fad1fd62f9fd15d/USER', 10000),
    MCSample('mfv_neuuds_tau10000um_M0600', '/mfv_neuuds_tau10000um_M0600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-f5b95880445f49065019a2cec3fe68f8/USER', 10000),
    MCSample('mfv_neuuds_tau10000um_M0800', '/mfv_neuuds_tau10000um_M0800/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-cc60671cae54d915960fca71f8b1f063/USER', 10000),
    MCSample('mfv_neuuds_tau10000um_M1200', '/mfv_neuuds_tau10000um_M1200/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-3d0a01a35d59def88f9ad8352a8943b2/USER', 9900),
    MCSample('mfv_neuuds_tau10000um_M1600', '/mfv_neuuds_tau10000um_M1600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-27babd583813bde45111f4d27ffccc8b/USER', 10000),
    MCSample('mfv_neuuds_tau10000um_M3000', '/mfv_neuuds_tau10000um_M3000/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-5c80f7c7ec4ea5b595a89cf4d52b83e3/USER', 9800),
    MCSample('mfv_neuuds_tau30000um_M0300', '/mfv_neuuds_tau30000um_M0300/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-49b5e24834a44c30c393626a458d1830/USER', 9900),
    MCSample('mfv_neuuds_tau30000um_M0400', '/mfv_neuuds_tau30000um_M0400/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-3f424f5f5e51ba8156605ba0886a8c95/USER', 10000),
    MCSample('mfv_neuuds_tau30000um_M0500', '/mfv_neuuds_tau30000um_M0500/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-651f0a5257bbd19d28dfefa2b7be799f/USER', 10000),
    MCSample('mfv_neuuds_tau30000um_M0600', '/mfv_neuuds_tau30000um_M0600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-0bfd741881d9d6c1cb85ccd4f0bd9783/USER', 10000),
    MCSample('mfv_neuuds_tau30000um_M0800', '/mfv_neuuds_tau30000um_M0800/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-f3bd1782f7c362b6176001385b405e58/USER', 10000),
    MCSample('mfv_neuuds_tau30000um_M1200', '/mfv_neuuds_tau30000um_M1200/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-35a07395e11b18fa2bfb2f691cb568f5/USER', 10000),
    MCSample('mfv_neuuds_tau30000um_M1600', '/mfv_neuuds_tau30000um_M1600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-e22fdd611b4f9f7c818e6eb903d3f055/USER', 9900),
    MCSample('mfv_neuuds_tau30000um_M3000', '/mfv_neuuds_tau30000um_M3000/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-86e48bcf590e9867799fd94b7acab0a5/USER', 9800),
    ]

mfv_neuudmu_samples = [
    MCSample('mfv_neuudmu_tau00100um_M0300', '/mfv_neuudmu_tau00100um_M0300/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-6ba18ae22eb7aa76445edd226bff7911/USER', 10000),
    MCSample('mfv_neuudmu_tau00100um_M0400', '/mfv_neuudmu_tau00100um_M0400/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-8c006de9851d139bca97582899a46bdc/USER', 10000),
    MCSample('mfv_neuudmu_tau00100um_M0500', '/mfv_neuudmu_tau00100um_M0500/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-513883dfbc4dacd59e734124fc168ba6/USER', 10000),
    MCSample('mfv_neuudmu_tau00100um_M0600', '/mfv_neuudmu_tau00100um_M0600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-651ce7da6eb1407548bc572b0c56845c/USER', 10000),
    MCSample('mfv_neuudmu_tau00100um_M0800', '/mfv_neuudmu_tau00100um_M0800/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-440f2a712b4f0c109233521c8a160e7b/USER', 10000),
    MCSample('mfv_neuudmu_tau00100um_M1200', '/mfv_neuudmu_tau00100um_M1200/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-64eb2d2dd4d410ce0bd4e5015c97d8de/USER', 10000),
    MCSample('mfv_neuudmu_tau00100um_M1600', '/mfv_neuudmu_tau00100um_M1600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-e89a0b781b7b5eea6d3ba07d8bff2d6e/USER', 10000),
    MCSample('mfv_neuudmu_tau00100um_M3000', '/mfv_neuudmu_tau00100um_M3000/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-73e5e512ecd038c1af3c06d09a94ee5d/USER', 9800),
    MCSample('mfv_neuudmu_tau00300um_M0300', '/mfv_neuudmu_tau00300um_M0300/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-1ab4c867ae28872c2a6768a2071b300d/USER', 10000),
    MCSample('mfv_neuudmu_tau00300um_M0400', '/mfv_neuudmu_tau00300um_M0400/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-68e75882bd66a1f85e67b863a94cd9ff/USER', 10000),
    MCSample('mfv_neuudmu_tau00300um_M0500', '/mfv_neuudmu_tau00300um_M0500/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-b3a9b1c614634ec7c3fbc0625356b5af/USER', 10000),
    MCSample('mfv_neuudmu_tau00300um_M0600', '/mfv_neuudmu_tau00300um_M0600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-2a17f96f380c3d9bd643ece3ed14b7aa/USER', 10000),
    MCSample('mfv_neuudmu_tau00300um_M0800', '/mfv_neuudmu_tau00300um_M0800/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-d672ce19b76476a8c6e157bc38f3c9a7/USER', 10000),
    MCSample('mfv_neuudmu_tau00300um_M1200', '/mfv_neuudmu_tau00300um_M1200/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-a552933a0b19cb73227af15be4cb64fb/USER', 10000),
    MCSample('mfv_neuudmu_tau00300um_M1600', '/mfv_neuudmu_tau00300um_M1600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-eed7502c8b618134e7c4e5abe5c11c1e/USER', 10000),
    MCSample('mfv_neuudmu_tau00300um_M3000', '/mfv_neuudmu_tau00300um_M3000/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-a5f7d09906cce761edb1090ccb35a53a/USER', 9800),
    MCSample('mfv_neuudmu_tau01000um_M0300', '/mfv_neuudmu_tau01000um_M0300/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-904995eeabcfeb3b40dda74e1241238f/USER', 10000),
    MCSample('mfv_neuudmu_tau01000um_M0400', '/mfv_neuudmu_tau01000um_M0400/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-635892ebdeb197621c3aa670db9374c4/USER', 10000),
    MCSample('mfv_neuudmu_tau01000um_M0500', '/mfv_neuudmu_tau01000um_M0500/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-c1de6c58d2230a8d6aae3e5af9856702/USER', 10000),
    MCSample('mfv_neuudmu_tau01000um_M0600', '/mfv_neuudmu_tau01000um_M0600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-9fba0d6f9a5bd5381bee983671f9e341/USER', 10000),
    MCSample('mfv_neuudmu_tau01000um_M0800', '/mfv_neuudmu_tau01000um_M0800/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-272c9ed83ec3fdd4e5bb64737db10dc0/USER', 10000),
    MCSample('mfv_neuudmu_tau01000um_M1200', '/mfv_neuudmu_tau01000um_M1200/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-127f1d43043e5badcafcc094210e7b5f/USER', 10000),
    MCSample('mfv_neuudmu_tau01000um_M1600', '/mfv_neuudmu_tau01000um_M1600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-164249497272df50ee36ca55bf34b180/USER', 10000),
    MCSample('mfv_neuudmu_tau01000um_M3000', '/mfv_neuudmu_tau01000um_M3000/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-9fe22fef1e43727d089d31c350c37ad7/USER', 10000),
    MCSample('mfv_neuudmu_tau10000um_M0300', '/mfv_neuudmu_tau10000um_M0300/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-33d07809d56e643e78eb42f3a729ed68/USER', 10000),
    MCSample('mfv_neuudmu_tau10000um_M0400', '/mfv_neuudmu_tau10000um_M0400/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-0f8e41f35d18c2a5d4d38c5495edbf01/USER', 9900),
    MCSample('mfv_neuudmu_tau10000um_M0500', '/mfv_neuudmu_tau10000um_M0500/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-d7e64c94dfce2892e9b689cb5304e6ee/USER', 9800),
    MCSample('mfv_neuudmu_tau10000um_M0600', '/mfv_neuudmu_tau10000um_M0600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-e02be6e2b43be13c6d7dffa1ccb469c7/USER', 10000),
    MCSample('mfv_neuudmu_tau10000um_M0800', '/mfv_neuudmu_tau10000um_M0800/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-e4d3bb95d8512907d38adf1723f8e868/USER', 9900),
    MCSample('mfv_neuudmu_tau10000um_M1200', '/mfv_neuudmu_tau10000um_M1200/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-eec831a93ccfb5a6309cd57f1fe07253/USER', 10000),
    MCSample('mfv_neuudmu_tau10000um_M1600', '/mfv_neuudmu_tau10000um_M1600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-e80f0659248f7a8a8cec141c1ca88ae2/USER', 10000),
    MCSample('mfv_neuudmu_tau10000um_M3000', '/mfv_neuudmu_tau10000um_M3000/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-b0947c9b111cbe1b3ecc962d2711a012/USER', 10000),
    MCSample('mfv_neuudmu_tau30000um_M0300', '/mfv_neuudmu_tau30000um_M0300/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-82882806f429a8513a42219e78151621/USER', 9900),
    MCSample('mfv_neuudmu_tau30000um_M0400', '/mfv_neuudmu_tau30000um_M0400/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-3c127992814496d8af6a09c1780b2ce6/USER', 10000),
    MCSample('mfv_neuudmu_tau30000um_M0500', '/mfv_neuudmu_tau30000um_M0500/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-fb0de664656c63d00b8e5a9bceba84f2/USER', 10000),
    MCSample('mfv_neuudmu_tau30000um_M0600', '/mfv_neuudmu_tau30000um_M0600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-3a43916e1b6017bb31ed98501f684aae/USER', 10000),
    MCSample('mfv_neuudmu_tau30000um_M0800', '/mfv_neuudmu_tau30000um_M0800/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-364d4e18a68bdc7787fadafe347fe17f/USER', 10000),
    MCSample('mfv_neuudmu_tau30000um_M1200', '/mfv_neuudmu_tau30000um_M1200/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-70133e08f5e8f02764cf96a033102877/USER', 9900),
    MCSample('mfv_neuudmu_tau30000um_M1600', '/mfv_neuudmu_tau30000um_M1600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-fb4edca49c0ac8e4bb0fe2ab181505c3/USER', 10000),
    MCSample('mfv_neuudmu_tau30000um_M3000', '/mfv_neuudmu_tau30000um_M3000/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-45a96de62b563ce948bce24442620783/USER', 10000),
    ]

mfv_neuude_samples = [
    MCSample('mfv_neuude_tau00100um_M0300', '/mfv_neuude_tau00100um_M0300/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-aef862612edd897e282afc9d9ee72e72/USER', 10000),
    MCSample('mfv_neuude_tau00100um_M0400', '/mfv_neuude_tau00100um_M0400/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-ca2e7e3dcdcdee227c5918f43d078dee/USER', 10000),
    MCSample('mfv_neuude_tau00100um_M0500', '/mfv_neuude_tau00100um_M0500/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-3d264e06c4051c62515fb45d8dfc5948/USER', 10000),
    MCSample('mfv_neuude_tau00100um_M0600', '/mfv_neuude_tau00100um_M0600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-fde0892fbc44565d98acb13a236bfa25/USER', 10000),
    MCSample('mfv_neuude_tau00100um_M0800', '/mfv_neuude_tau00100um_M0800/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-1c085e41e01a469df5a43d2a5e9b6a97/USER', 10000),
    MCSample('mfv_neuude_tau00100um_M1200', '/mfv_neuude_tau00100um_M1200/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-511b3dc29c04737bff4a4589810af28c/USER', 10000),
    MCSample('mfv_neuude_tau00100um_M1600', '/mfv_neuude_tau00100um_M1600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-17fe12d5209e001bd9b34d621ac3629c/USER', 10000),
    MCSample('mfv_neuude_tau00100um_M3000', '/mfv_neuude_tau00100um_M3000/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-facbc4778129ee25aae06d30a7a70d56/USER', 10000),
    MCSample('mfv_neuude_tau00300um_M0300', '/mfv_neuude_tau00300um_M0300/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-2a42d5fbcaf11d32ad6448bd3448fa3c/USER', 10000),
    MCSample('mfv_neuude_tau00300um_M0400', '/mfv_neuude_tau00300um_M0400/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-df5c8147c72818fb380f142d7284ebda/USER', 10000),
    MCSample('mfv_neuude_tau00300um_M0500', '/mfv_neuude_tau00300um_M0500/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-17969e67c5cd94a4e19b0ac6069d2493/USER', 9900),
    MCSample('mfv_neuude_tau00300um_M0600', '/mfv_neuude_tau00300um_M0600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-eb40c0e70397509fa37ec16e5dc39847/USER', 10000),
    MCSample('mfv_neuude_tau00300um_M0800', '/mfv_neuude_tau00300um_M0800/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-3fdd5bc7c8cc2bc7917ce9667027e8f7/USER', 10000),
    MCSample('mfv_neuude_tau00300um_M1200', '/mfv_neuude_tau00300um_M1200/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-1952098e9e28d64e0af8a81341d49eb1/USER', 10000),
    MCSample('mfv_neuude_tau00300um_M1600', '/mfv_neuude_tau00300um_M1600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-764bef3220987400e70450ee73d484f8/USER', 9800),
    MCSample('mfv_neuude_tau00300um_M3000', '/mfv_neuude_tau00300um_M3000/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-576a3e57fe01b7044b98cda680d331da/USER', 9800),
    MCSample('mfv_neuude_tau01000um_M0300', '/mfv_neuude_tau01000um_M0300/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-73393c198dccb4cabfd759be2e94bc9c/USER', 10000),
    MCSample('mfv_neuude_tau01000um_M0400', '/mfv_neuude_tau01000um_M0400/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-14586e71d119ee676d6e5439b2ae3e12/USER', 10000),
    MCSample('mfv_neuude_tau01000um_M0500', '/mfv_neuude_tau01000um_M0500/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-0722208ac65dc44a66c6ef0531e3be9b/USER', 10000),
    MCSample('mfv_neuude_tau01000um_M0600', '/mfv_neuude_tau01000um_M0600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-6f6f911f4d43d037d8081e3370880e77/USER', 10000),
    MCSample('mfv_neuude_tau01000um_M0800', '/mfv_neuude_tau01000um_M0800/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-c5de8a482f2fccfe4861bbb8976feeb7/USER', 10000),
    MCSample('mfv_neuude_tau01000um_M1200', '/mfv_neuude_tau01000um_M1200/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-9a3e6e0dad2b1aa8b7126ffd1178ba9d/USER', 9800),
    MCSample('mfv_neuude_tau01000um_M1600', '/mfv_neuude_tau01000um_M1600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-bca84ce7425c1491758de32fd00a4d2e/USER', 9900),
    MCSample('mfv_neuude_tau01000um_M3000', '/mfv_neuude_tau01000um_M3000/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-8fa553de5a55b92e15639ee0b5e96332/USER', 9700),
    MCSample('mfv_neuude_tau10000um_M0300', '/mfv_neuude_tau10000um_M0300/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-774e773c9760d847267b2593ee3af318/USER', 10000),
    MCSample('mfv_neuude_tau10000um_M0400', '/mfv_neuude_tau10000um_M0400/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-8ba246e60bdfe8bb8caf2fc320f67093/USER', 10000),
    MCSample('mfv_neuude_tau10000um_M0500', '/mfv_neuude_tau10000um_M0500/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-f37c150bc8eb21aa2ec3783461e1591b/USER', 10000),
    MCSample('mfv_neuude_tau10000um_M0600', '/mfv_neuude_tau10000um_M0600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-b7969ccf6f039c7ebf7efb94c1c335f3/USER', 10000),
    MCSample('mfv_neuude_tau10000um_M0800', '/mfv_neuude_tau10000um_M0800/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-68a7bd5f678f9be72f765c2de6821fb0/USER', 10000),
    MCSample('mfv_neuude_tau10000um_M1200', '/mfv_neuude_tau10000um_M1200/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-d27d0bb6f6a1e3e0427e9989edaa2a0e/USER', 10000),
    MCSample('mfv_neuude_tau10000um_M1600', '/mfv_neuude_tau10000um_M1600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-d9d432704a02dc9bf840227c26b09116/USER', 9900),
    MCSample('mfv_neuude_tau10000um_M3000', '/mfv_neuude_tau10000um_M3000/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-e1fec9844bb3cac4d679f225e60eabe5/USER', 9900),
    MCSample('mfv_neuude_tau30000um_M0300', '/mfv_neuude_tau30000um_M0300/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-4ddd753686fbef0f59bef1d483e9fa04/USER', 10000),
    MCSample('mfv_neuude_tau30000um_M0400', '/mfv_neuude_tau30000um_M0400/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-0e84861090aad2bd8284283b5c5b476a/USER', 10000),
    MCSample('mfv_neuude_tau30000um_M0500', '/mfv_neuude_tau30000um_M0500/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-965ee92ecb5d3021cb645cba919d21c5/USER', 10000),
    MCSample('mfv_neuude_tau30000um_M0600', '/mfv_neuude_tau30000um_M0600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-9eb3ea30fb613d9feb3809df555db2ce/USER', 10000),
    MCSample('mfv_neuude_tau30000um_M0800', '/mfv_neuude_tau30000um_M0800/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-3f2420a4c8e0c2ecbdfde0a9c2bab985/USER', 10000),
    MCSample('mfv_neuude_tau30000um_M1200', '/mfv_neuude_tau30000um_M1200/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-010cd15f9b41da760244d38569c12ea4/USER', 10000),
    MCSample('mfv_neuude_tau30000um_M1600', '/mfv_neuude_tau30000um_M1600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-4187cac1ef1338f60d79a64951ec119d/USER', 9900),
    MCSample('mfv_neuude_tau30000um_M3000', '/mfv_neuude_tau30000um_M3000/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-3eb16698972b98821164f2f9127d5b36/USER', 10000),
    ]
 
mfv_misc_samples = [
    MCSample('mfv_neucdb_tau01000um_M0800', '/mfv_neucdb_tau01000um_M0800/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-5e8bbbfd9a85c6633a03d9b65f3d35df/USER', 10000),
    MCSample('mfv_neucdb_tau10000um_M1600', '/mfv_neucdb_tau10000um_M1600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-6bb197af22348da8d9f9b411540e61df/USER', 9900),
    MCSample('mfv_neucds_tau01000um_M0800', '/mfv_neucds_tau01000um_M0800/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-51ea4166693bfdc26862f96fbd7ec158/USER', 10000),
    MCSample('mfv_neucds_tau10000um_M1600', '/mfv_neucds_tau10000um_M1600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-1e307f99474f2a97292ca79ee65fd464/USER', 9900),
    MCSample('mfv_neutbb_tau01000um_M0800', '/mfv_neutbb_tau01000um_M0800/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-0d493cea93a430e7edbb1e567eaea25a/USER', 9900),
    MCSample('mfv_neutbb_tau10000um_M1600', '/mfv_neutbb_tau10000um_M1600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-f5195637e3c78f8327132f9f2f9cfa50/USER', 9700),
    MCSample('mfv_neutds_tau01000um_M0800', '/mfv_neutds_tau01000um_M0800/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-a8de20ac33902302c0f0aa90d286a33f/USER', 10000),
    MCSample('mfv_neutds_tau10000um_M1600', '/mfv_neutds_tau10000um_M1600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-2e8d32f5e910a3c93aa01281063c9ba9/USER', 9600),
    MCSample('mfv_neuubb_tau01000um_M0800', '/mfv_neuubb_tau01000um_M0800/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-910f21636fac69895f5d16a6d8c46f90/USER', 10000),
    MCSample('mfv_neuubb_tau10000um_M1600', '/mfv_neuubb_tau10000um_M1600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-a125894d2383dc32f0a3dfec12438cb5/USER', 9800),
    MCSample('mfv_neuudb_tau01000um_M0800', '/mfv_neuudb_tau01000um_M0800/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-71c928bf558e1132c0df375c33a21202/USER', 9900),
    MCSample('mfv_neuudb_tau10000um_M1600', '/mfv_neuudb_tau10000um_M1600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-0bac255a70a0a3afedbcb28f36c7205e/USER', 10000),
    # "tu" = tau but "tau" is a reserved string in our sample names
    MCSample('mfv_neuudtu_tau01000um_M0800', '/mfv_neuudtau_tau01000um_M0800/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-2d69f57508d44050ac2268e7a3c1c4f5/USER', 10000),
    MCSample('mfv_neuudtu_tau10000um_M1600', '/mfv_neuudtau_tau10000um_M1600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-ae17070838abfc249976d0f5220ce40e/USER', 10000),
    ]

mfv_xxddbar_samples = [
    MCSample("mfv_xxddbar_tau00100um_M0300", "/mfv_xxddbar_tau00100um_M0300/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-eef48cb5e07a9d98f25b10b0052a2c0a/USER", 26900),
    MCSample("mfv_xxddbar_tau00100um_M0400", "/mfv_xxddbar_tau00100um_M0400/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-f403d4c2df44ed929e4bed765c344c86/USER", 28000),
    MCSample("mfv_xxddbar_tau00100um_M0500", "/mfv_xxddbar_tau00100um_M0500/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-c9ee9f35bd55d31127bbab500eacec06/USER", 24100),
    MCSample("mfv_xxddbar_tau00100um_M0600", "/mfv_xxddbar_tau00100um_M0600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-d03da199c09d375fca46dc31216ed7ab/USER", 25500),
    MCSample("mfv_xxddbar_tau00100um_M0800", "/mfv_xxddbar_tau00100um_M0800/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-90fd2c51208418faea5a046b766d72a3/USER", 24800),
    MCSample("mfv_xxddbar_tau00100um_M1200", "/mfv_xxddbar_tau00100um_M1200/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-0739a18ffdb1e32c0f7f5833148b985e/USER", 10500),
    MCSample("mfv_xxddbar_tau00100um_M1600", "/mfv_xxddbar_tau00100um_M1600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-1634a766c0f3f83c725ed06b4da9aecb/USER", 11100),  # inc /mfv_xxddbar_tau00100um_M1600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-e2bea9000081855f3205e44ef19f9af1/USER
    MCSample("mfv_xxddbar_tau00100um_M3000", "/mfv_xxddbar_tau00100um_M3000/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-4596791259f0ff7ef6fa7383d95c0c77/USER", 10200),
    MCSample("mfv_xxddbar_tau00300um_M0300", "/mfv_xxddbar_tau00300um_M0300/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-df8d45ffe4e823a5ad6c3094c88c00e3/USER", 22200),
    MCSample("mfv_xxddbar_tau00300um_M0400", "/mfv_xxddbar_tau00300um_M0400/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-386151ff1ef88d689b44015ea7f03083/USER", 27700),
    MCSample("mfv_xxddbar_tau00300um_M0500", "/mfv_xxddbar_tau00300um_M0500/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-dd404c2ce09ac70ba64a55215d556030/USER", 25400),
    MCSample("mfv_xxddbar_tau00300um_M0600", "/mfv_xxddbar_tau00300um_M0600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-83099075458fa3068c5422378cecbedd/USER", 22700),
    MCSample("mfv_xxddbar_tau00300um_M0800", "/mfv_xxddbar_tau00300um_M0800/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-bf69218f4fc4a6505c366e053c92c38e/USER", 10400),
    MCSample("mfv_xxddbar_tau00300um_M1200", "/mfv_xxddbar_tau00300um_M1200/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-58ed24e72acf3a7f124f7f5fb9e8d5a5/USER", 10100),
    MCSample("mfv_xxddbar_tau00300um_M1600", "/mfv_xxddbar_tau00300um_M1600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-a03f6bd22fa91583d6bc77acf5437270/USER", 23600),
    MCSample("mfv_xxddbar_tau00300um_M3000", "/mfv_xxddbar_tau00300um_M3000/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-096d935dae651efb025e2d1bef08022e/USER", 7600),
    MCSample("mfv_xxddbar_tau01000um_M0300", "/mfv_xxddbar_tau01000um_M0300/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-7d4446734d2dd96ac3c619192708444f/USER", 20300),
    MCSample("mfv_xxddbar_tau01000um_M0400", "/mfv_xxddbar_tau01000um_M0400/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-59c0293874a4735637e3c571ca0c4849/USER", 13300),
    MCSample("mfv_xxddbar_tau01000um_M0500", "/mfv_xxddbar_tau01000um_M0500/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-e78a9aecde814dda4a53e39a7f1a1d3b/USER", 13400),
    MCSample("mfv_xxddbar_tau01000um_M0600", "/mfv_xxddbar_tau01000um_M0600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-2fc079b8fe254f1cbc67494566b562ca/USER", 13500),
    MCSample("mfv_xxddbar_tau01000um_M0800", "/mfv_xxddbar_tau01000um_M0800/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-667fb5ecafc03cacccb5f4fb59dddf57/USER", 13000),
    MCSample("mfv_xxddbar_tau01000um_M1200", "/mfv_xxddbar_tau01000um_M1200/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-1c23ce47d5c028cc724eddb78642578a/USER", 18300),
    MCSample("mfv_xxddbar_tau01000um_M1600", "/mfv_xxddbar_tau01000um_M1600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-66fb61193f6a52cd5fe2bb5df7f285c8/USER",  9900),
    MCSample("mfv_xxddbar_tau01000um_M3000", "/mfv_xxddbar_tau01000um_M3000/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-396a2816e0b7e5e938640b07e01bc924/USER", 19200),
    MCSample("mfv_xxddbar_tau10000um_M0300", "/mfv_xxddbar_tau10000um_M0300/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-32a8f4e1b118730572707882a271f9ba/USER", 14400),
    MCSample("mfv_xxddbar_tau10000um_M0400", "/mfv_xxddbar_tau10000um_M0400/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-66b413af075cc9e4180b279f2f0575df/USER", 27700),
    MCSample("mfv_xxddbar_tau10000um_M0500", "/mfv_xxddbar_tau10000um_M0500/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-e42b679506b54ced003473f5c5f8311d/USER", 27400),
    MCSample("mfv_xxddbar_tau10000um_M0600", "/mfv_xxddbar_tau10000um_M0600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-b4a865cfb0629f8ed98cbc4a611f9cb8/USER", 3400),
    MCSample("mfv_xxddbar_tau10000um_M0800", "/mfv_xxddbar_tau10000um_M0800/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-f92992b14ec383062827dc3878689d32/USER", 11600),
    MCSample("mfv_xxddbar_tau10000um_M1200", "/mfv_xxddbar_tau10000um_M1200/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-3014d9d383ea55237f7ebe6c49d4fd20/USER", 11900),
    MCSample("mfv_xxddbar_tau10000um_M1600", "/mfv_xxddbar_tau10000um_M1600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-d83e124ccaa75c1461b12a074b0e3cc6/USER", 26100),
    MCSample("mfv_xxddbar_tau10000um_M3000", "/mfv_xxddbar_tau10000um_M3000/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-2d54bebfd5fa871345280dcdefa916d8/USER", 9300),
    MCSample("mfv_xxddbar_tau30000um_M0300", "/mfv_xxddbar_tau30000um_M0300/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-530c7ad95a572496ca765e0c804a5274/USER", 9100),
    MCSample("mfv_xxddbar_tau30000um_M0400", "/mfv_xxddbar_tau30000um_M0400/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-43fda0b9e5d40198527306c680540bfc/USER", 13500),
    MCSample("mfv_xxddbar_tau30000um_M0500", "/mfv_xxddbar_tau30000um_M0500/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-1acb5b1563767e4798ce671400e05235/USER", 12900),
    MCSample("mfv_xxddbar_tau30000um_M0600", "/mfv_xxddbar_tau30000um_M0600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-8f8d1730405164fe0d413d85b3b9413c/USER", 11800),
    MCSample("mfv_xxddbar_tau30000um_M0800", "/mfv_xxddbar_tau30000um_M0800/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-8834db5ef6b902ab46c21b29b1ffa1b3/USER", 17900),
    MCSample("mfv_xxddbar_tau30000um_M1200", "/mfv_xxddbar_tau30000um_M1200/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-5431b3029dc9cc7418d6d42bbc48200d/USER", 8700),
    MCSample("mfv_xxddbar_tau30000um_M1600", "/mfv_xxddbar_tau30000um_M1600/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-90f9ec53aea36b2df5ad81f434af14db/USER", 11100),
    MCSample("mfv_xxddbar_tau30000um_M3000", "/mfv_xxddbar_tau30000um_M3000/tucker-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-ed4704e7ef306fce954cbe4ca16fe9a8/USER", 9600),
    ]

mfv_stopdbardbar_samples = [
    MCSample('mfv_stopdbardbar_tau00100um_M0300', '/mfv_stopdbardbar_tau00100um_M0300/jchu-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-98f50e22f4a548ea9b384da8c5c08d55/USER', 13100),
    MCSample('mfv_stopdbardbar_tau00100um_M0400', '/mfv_stopdbardbar_tau00100um_M0400/jchu-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-863c210ddc03c09f684102e00ffd1a47/USER', 14100),
    MCSample('mfv_stopdbardbar_tau00100um_M0500', '/mfv_stopdbardbar_tau00100um_M0500/jchu-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-34d053c251cab1c70c9d7742b033998c/USER', 10200),
    MCSample('mfv_stopdbardbar_tau00100um_M0600', '/mfv_stopdbardbar_tau00100um_M0600/jchu-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-cd02b976ff3549b968e8ea333fd16fa0/USER', 12900),
    MCSample('mfv_stopdbardbar_tau00100um_M0800', '/mfv_stopdbardbar_tau00100um_M0800/jchu-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-319b9667dd30baea99e84b7b11665182/USER', 13300),
    MCSample('mfv_stopdbardbar_tau00100um_M1200', '/mfv_stopdbardbar_tau00100um_M1200/jchu-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-b57febe42c6b4a2f207ed82e0bc8595a/USER', 8500),
    MCSample('mfv_stopdbardbar_tau00100um_M1600', '/mfv_stopdbardbar_tau00100um_M1600/jchu-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-1a14b13a9efef52e898f08aebde5818a/USER', 8700),
    MCSample('mfv_stopdbardbar_tau00100um_M3000', '/mfv_stopdbardbar_tau00100um_M3000/jchu-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-ad59b8e4fe0c18b2c96ad845292cf408/USER', 7100),
    MCSample('mfv_stopdbardbar_tau00300um_M0300', '/mfv_stopdbardbar_tau00300um_M0300/jchu-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-e8e31dacd94096b956850d782329714e/USER', 13100),
    MCSample('mfv_stopdbardbar_tau00300um_M0400', '/mfv_stopdbardbar_tau00300um_M0400/jchu-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-db446d5aa34a9cd5279dc7ab4c3b797c/USER', 13900),
    MCSample('mfv_stopdbardbar_tau00300um_M0500', '/mfv_stopdbardbar_tau00300um_M0500/jchu-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-35f15d36157eb57072c8cb9faab2a279/USER', 7400),
    MCSample('mfv_stopdbardbar_tau00300um_M0600', '/mfv_stopdbardbar_tau00300um_M0600/jchu-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-8e584bdcc0499c9a99d7dd897752085a/USER', 7700),
    MCSample('mfv_stopdbardbar_tau00300um_M0800', '/mfv_stopdbardbar_tau00300um_M0800/jchu-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-6726475daac032497262dfddf13b6e9a/USER', 12500),
    MCSample('mfv_stopdbardbar_tau00300um_M1200', '/mfv_stopdbardbar_tau00300um_M1200/jchu-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-31742a2ce229bfc165b05361a0120bd3/USER', 8400),
    MCSample('mfv_stopdbardbar_tau00300um_M1600', '/mfv_stopdbardbar_tau00300um_M1600/jchu-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-f20d4f2a2cbb33baceaa0e2de74c19ea/USER', 8500),
    MCSample('mfv_stopdbardbar_tau00300um_M3000', '/mfv_stopdbardbar_tau00300um_M3000/jchu-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-2bf57502a78d4ddc919cd6ccbf4e81d7/USER', 6800),
    MCSample('mfv_stopdbardbar_tau01000um_M0300', '/mfv_stopdbardbar_tau01000um_M0300/jchu-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-aedf737601f56da7292fd98b6a798e45/USER', 14100),
    MCSample('mfv_stopdbardbar_tau01000um_M0400', '/mfv_stopdbardbar_tau01000um_M0400/jchu-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-f69d59cbab67eee455cc5c171bf66f98/USER', 12800),
    MCSample('mfv_stopdbardbar_tau01000um_M0500', '/mfv_stopdbardbar_tau01000um_M0500/jchu-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-7b305d0f35951d3ac89a6d0676915332/USER', 13400),
    MCSample('mfv_stopdbardbar_tau01000um_M0600', '/mfv_stopdbardbar_tau01000um_M0600/jchu-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-858de389bfea64b55467b12cf3620d53/USER', 11900),
    MCSample('mfv_stopdbardbar_tau01000um_M0800', '/mfv_stopdbardbar_tau01000um_M0800/jchu-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-604057663224b360e8ceec3be3d2de92/USER', 11800),
    MCSample('mfv_stopdbardbar_tau01000um_M1200', '/mfv_stopdbardbar_tau01000um_M1200/jchu-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-bb16eccdf29f6c1bbde3dccf32e21261/USER', 11300),
    MCSample('mfv_stopdbardbar_tau01000um_M1600', '/mfv_stopdbardbar_tau01000um_M1600/jchu-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-a22e0fde13ccd0d7aa4aa478da776f21/USER', 8600),
    MCSample('mfv_stopdbardbar_tau01000um_M3000', '/mfv_stopdbardbar_tau01000um_M3000/jchu-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-0d015404911c29202ea44ff433b0f347/USER', 7100),
    MCSample('mfv_stopdbardbar_tau10000um_M0300', '/mfv_stopdbardbar_tau10000um_M0300/jchu-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-375b18896f6bb9be7c88ac7eb850d6d3/USER', 13800),
    MCSample('mfv_stopdbardbar_tau10000um_M0400', '/mfv_stopdbardbar_tau10000um_M0400/jchu-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-6b9ef935279531bbdfdcb1851edda26a/USER', 13000),
    MCSample('mfv_stopdbardbar_tau10000um_M0500', '/mfv_stopdbardbar_tau10000um_M0500/jchu-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-a83304e6183caad7d3953ad53cd8a027/USER', 10500),
    MCSample('mfv_stopdbardbar_tau10000um_M0600', '/mfv_stopdbardbar_tau10000um_M0600/jchu-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-c7f00ba311307466cec294cf12e89fd5/USER', 12100),
    MCSample('mfv_stopdbardbar_tau10000um_M0800', '/mfv_stopdbardbar_tau10000um_M0800/jchu-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-9da4cdc084b8f41dc096dc04c9fbc655/USER', 11800),
    MCSample('mfv_stopdbardbar_tau10000um_M1200', '/mfv_stopdbardbar_tau10000um_M1200/jchu-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-86d95b83295efef812d81d728e11cab1/USER', 10900),
    MCSample('mfv_stopdbardbar_tau10000um_M1600', '/mfv_stopdbardbar_tau10000um_M1600/jchu-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-9c847f7143748108d3e0a79ed7649642/USER', 10000),
    MCSample('mfv_stopdbardbar_tau10000um_M3000', '/mfv_stopdbardbar_tau10000um_M3000/jchu-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-d6f5d5249e10f3714aee71416714dc7c/USER', 9200),
    MCSample('mfv_stopdbardbar_tau30000um_M0300', '/mfv_stopdbardbar_tau30000um_M0300/jchu-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-f7f10eba7c32bc0c406da6948a667085/USER', 8300),
    MCSample('mfv_stopdbardbar_tau30000um_M0400', '/mfv_stopdbardbar_tau30000um_M0400/jchu-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-9bf8cf68f755b971960d56084e42d10e/USER', 14500),
    MCSample('mfv_stopdbardbar_tau30000um_M0500', '/mfv_stopdbardbar_tau30000um_M0500/jchu-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-c3f376a0402cf7ba114f24da0c7dab17/USER', 12100),
    MCSample('mfv_stopdbardbar_tau30000um_M0600', '/mfv_stopdbardbar_tau30000um_M0600/jchu-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-7332f13395b7a5652b9dcae3ff188c80/USER', 13300),
    MCSample('mfv_stopdbardbar_tau30000um_M0800', '/mfv_stopdbardbar_tau30000um_M0800/jchu-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-764857cab3683640ac214bd1aa6a85fd/USER', 13300),
    MCSample('mfv_stopdbardbar_tau30000um_M1200', '/mfv_stopdbardbar_tau30000um_M1200/jchu-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-d9727effb7d467e51035002a850ea916/USER', 11000),
    MCSample('mfv_stopdbardbar_tau30000um_M1600', '/mfv_stopdbardbar_tau30000um_M1600/jchu-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-ec6e6b7a74a00749df770640cebfed6f/USER', 11700),
    MCSample('mfv_stopdbardbar_tau30000um_M3000', '/mfv_stopdbardbar_tau30000um_M3000/jchu-RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-f72fed6cac8a8dbdd0dd1e72ce3e6c2e/USER', 10100),
    ]

mfv_stopbbarbbar_samples = [
    MCSample('mfv_stopbbarbbar_tau00300um_M0600', '/mfv_stopbbarbbar_tau00300um_M0600/None/None', 10000),
    MCSample('mfv_stopbbarbbar_tau00300um_M1200', '/mfv_stopbbarbbar_tau00300um_M1200/None/None',  9900),
    MCSample('mfv_stopbbarbbar_tau01000um_M0800', '/mfv_stopbbarbbar_tau01000um_M0800/None/None', 10000),
    MCSample('mfv_stopbbarbbar_tau10000um_M0600', '/mfv_stopbbarbbar_tau10000um_M0600/None/None', 10000),
    MCSample('mfv_stopbbarbbar_tau10000um_M1200', '/mfv_stopbbarbbar_tau10000um_M1200/None/None', 10000),
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

for s in mfv_ddbar_samples + mfv_signal_samples + mfv_neuuds_samples + mfv_neuudmu_samples + mfv_neuude_samples + mfv_misc_samples + mfv_xxddbar_samples + mfv_stopdbardbar_samples + mfv_stopbbarbbar_samples + mfv_hip_samples:
    _set_tau_mass(s)
    s.xsec = 1e-3
    s.is_private = s.dataset.startswith('/mfv_')
    if s.is_private:
        s.dbs_inst = 'phys03'
        s.condor = True

all_signal_samples = mfv_ddbar_samples + mfv_signal_samples + mfv_neuuds_samples + mfv_neuudmu_samples + mfv_neuude_samples + mfv_misc_samples + mfv_xxddbar_samples + mfv_stopdbardbar_samples + mfv_stopbbarbbar_samples + mfv_hip_samples

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

all_signal_samples = mfv_ddbar_samples + mfv_signal_samples + mfv_neuuds_samples + mfv_neuudmu_samples + mfv_neuude_samples + mfv_misc_samples + mfv_xxddbar_samples + mfv_stopdbardbar_samples + mfv_stopbbarbbar_samples + mfv_hip_samples

__all__ = [
    'qcd_samples',
    'qcd_samples_ext',
    'qcd_samples_sum',
    'ttbar_samples',
    'leptonic_background_samples',
    'minbias_samples',
    'mfv_ddbar_samples',
    'mfv_signal_samples',
    'mfv_neuuds_samples',
    'mfv_neuudmu_samples',
    'mfv_neuude_samples',
    'mfv_misc_samples',
    'mfv_xxddbar_samples',
    'mfv_stopdbardbar_samples',
    'mfv_stopbbarbbar_samples',
    'mfv_hip_samples',
    'qcd_hip_samples',
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

__all__ += [
    'all_signal_samples',
    'all_signal_samples_2015',
    ]

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

for x in mfv_ddbar_samples:
    x.add_dataset('miniaod', '/%s/None/USER' % x.primary_dataset, x.nevents_orig)
    x.datasets['miniaod'].condor = True

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

for x in mfv_stopdbardbar_samples:
    x.add_dataset('ntuplev16')

for x in data_samples + qcd_samples + qcd_samples_ext + qcd_hip_samples[-2:]:
    x.add_dataset('v0ntuplev1')
for x in data_samples + [s for s in auxiliary_data_samples if s.name.startswith('ZeroBias')] + qcd_samples[2:4] + qcd_samples_ext[2:4]:
    x.add_dataset('v0ntuplev2')

for x in mfv_signal_samples + mfv_ddbar_samples:
    for y in '3p7', '3p8', '3p9', '4p1', '4p2', '4p3':
        x.add_dataset('ntuplev15_sigmadxy%s' % y)

for x in mfv_signal_samples_2015 + mfv_signal_samples + mfv_ddbar_samples + mfv_hip_samples + mfv_neuuds_samples + mfv_neuudmu_samples + mfv_neuude_samples + mfv_misc_samples + mfv_xxddbar_samples + mfv_stopdbardbar_samples + mfv_stopbbarbbar_samples:
    x.add_dataset('ntuplev16_wgenv2')

for x in 'ntuplev15lep', 'ntuplev15lep_IsoMu24', 'ntuplev15lep_IsoTkMu24', 'ntuplev15lep_VVVL350', 'ntuplev15lep_VVVL400', 'ntuplev15lep_Mu50':
    mfv_neu_tau01000um_M0300.add_dataset(x)

for x in mfv_neu_tau00100um_M0300, mfv_neu_tau01000um_M0300:
    x.add_dataset('ntuplev15_leptrigs')

########
# automatic condor declarations for ntuples
########

ds4condor = ['ntuple', 'v0ntuple', 'pick1vtx']
for s in registry.all():
    for ds in s.datasets.keys():
        for ds4 in ds4condor:
            if ds.startswith(ds4):
                s.datasets[ds].condor = True

########
# other condor declarations, generate condorable dict with Shed/condor_list.py
########

# 2018-01-23 15:45:00.239927
condorable = {
    "T3_US_FNALLPC": {
        "main": [JetHT2015C, mfv_neu_tau00100um_M0300, mfv_neu_tau00300um_M0300, mfv_neu_tau10000um_M0300, mfv_neu_tau00100um_M0400, mfv_neu_tau00300um_M0400, mfv_neu_tau10000um_M0400, mfv_neu_tau00100um_M0800, mfv_neu_tau00300um_M0800, mfv_neu_tau01000um_M0800, mfv_neu_tau00100um_M1200, mfv_neu_tau00300um_M1200, mfv_neu_tau01000um_M1200, mfv_neu_tau10000um_M1200, mfv_neu_tau00100um_M1600, mfv_neu_tau00300um_M1600, mfv_neu_tau10000um_M1600, qcdht0500_2015, qcdht0700_2015, qcdht1000_2015, qcdht1500_2015, qcdht2000_2015, qcdht0500ext_2015, qcdht0700ext_2015, qcdht1000ext_2015, qcdht1500ext_2015, qcdht2000ext_2015, ttbar_2015, qcdht2000ext, ttbar],
        "miniaod": [SingleMuon2016B3, SingleMuon2016D, SingleMuon2016F, SingleMuon2016G, SingleMuon2016H2, SingleMuon2016H3, mfv_neu_tau10000um_M1600],
        },
    "T1_US_FNAL_Disk": {
        "main": [JetHT2016G, SingleMuon2016G, qcdht0500ext, qcdht0700ext, qcdht1500ext],
        "miniaod": [JetHT2016B3, SingleMuon2016C, SingleMuon2016E, ZeroBias2016B3, ZeroBias2016H3, ReproJetHT2016B, ReproJetHT2016C, ReproJetHT2016F, mfv_neu_tau00100um_M0300, mfv_neu_tau00300um_M0300, mfv_neu_tau10000um_M0300, mfv_neu_tau00100um_M0400, mfv_neu_tau10000um_M0400, mfv_neu_tau01000um_M0800, mfv_neu_tau00300um_M1200, mfv_neu_tau00300um_M1600, qcdht0700ext, ttbar, dyjetstollM10],
        },
    "T2_DE_DESY": {
        "main": [JetHT2015D, SingleMuon2016D, mfv_neu_tau01000um_M0300, wjetstolnu1_2015, qcdht2000],
        "miniaod": [JetHT2015C, JetHT2015D, SingleMuon2015D, JetHT2016C, JetHT2016D, JetHT2016E, JetHT2016F, JetHT2016G, JetHT2016H2, JetHT2016H3, ZeroBias2016C, ReproJetHT2016D, ReproJetHT2016E, ReproJetHT2016G, ReproJetHT2016H, mfv_neu_tau00100um_M0800, mfv_neu_tau00100um_M1200, mfv_neu_tau01000um_M1200, qcdht0500_2015, qcdht1500_2015, qcdht2000_2015, wjetstolnu1_2015, dyjetstollM101_2015, dyjetstollM102_2015, qcdht0500, qcdht0700, qcdht1000, qcdht1500, qcdht2000, qcdht0500ext, qcdht1000ext, qcdht1500ext, qcdht2000ext, wjetstolnu],
        },
    }

sites = {
    'T3_US_FNALLPC': 'root://cmseos.fnal.gov/',
    'T1_US_FNAL_Disk': 'root://cmsxrootd-site.fnal.gov/',
    'T2_DE_DESY': 'root://dcache-cms-xrootd.desy.de/'
    }

for site, d in condorable.iteritems():
    if sites.has_key(site):
        for ds, samples in d.iteritems():
            for s in samples:
                s.datasets[ds].condor = True
                s.datasets[ds].xrootd_url = sites[site]
                
########################################################################

if __name__ == '__main__':
    main(registry)

    import sys
    from pprint import pprint
    from JMTucker.Tools import DBS
    from JMTucker.Tools.general import popen

    if 0:
        from DBS import *
        for s in data_samples + mfv_signal_samples:
            n1, n2 = s.datasets['main'].nevents_orig, s.datasets['miniaod'].nevents_orig
            if n1 != n2:
                print s.name, n1, n2

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

    if 0:
        for ds in 'main', 'miniaod':
            for s in registry.all():
                if s.has_dataset(ds):
                    s.set_curr_dataset(ds)
                    print '%s %s %s %s' % (s.name, ds, s.condor, s.xrootd_url)
