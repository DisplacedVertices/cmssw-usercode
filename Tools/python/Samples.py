#!/usr/bin/env python

from JMTucker.Tools.Sample import *
from JMTucker.Tools.CMSSWTools import json_path

########################################################################

def _model(sample):
    s = sample if type(sample) == str else sample.name
    return s.split('_tau')[0]

def _tau(sample):
    s = sample if type(sample) == str else sample.name
    is_um = '0um_' in s
    x = int(s[s.index('tau')+3:s.index('um_' if is_um else 'mm_')])
    if not is_um:
        x *= 1000
    return x

def _mass(sample):
    s = sample if type(sample) == str else sample.name
    x = s.index('_M')
    y = s.find('_',x+1)
    if y == -1:
        y = len(s)
    return int(s[x+2:y])

def _decay(sample):
    s = sample if type(sample) == str else sample.name
    if s.startswith('of_'):
        s = s[3:]
    decay = {
        'mfv_neu': r'\tilde{N} \rightarrow tbs',
        'xx4j': r'X \rightarrow q\bar{q}',
        'mfv_ddbar': r'\tilde{g} \rightarrow d\bar{d}',
        'mfv_neuuds': r'\tilde{N} \rightarrow uds',
        'mfv_neuudmu': r'\tilde{N} \rightarrow u\bar{d}\mu^{\minus}',
        'mfv_neuude': r'\tilde{N} \rightarrow u\bar{d}e^{\minus}',
        'mfv_neucdb': r'\tilde{N} \rightarrow cdb',
        'mfv_neucds': r'\tilde{N} \rightarrow cds',
        'mfv_neutbb': r'\tilde{N} \rightarrow tbb',
        'mfv_neutds': r'\tilde{N} \rightarrow tds',
        'mfv_neuubb': r'\tilde{N} \rightarrow ubb',
        'mfv_neuudb': r'\tilde{N} \rightarrow udb',
        'mfv_neuudtu': r'\tilde{N} \rightarrow u\bar{d}\tau^{\minus}',
        'mfv_xxddbar': r'X \rightarrow d\bar{d}',
        'mfv_stopdbardbar': r'\tilde{t} \rightarrow \bar{d}\bar{d}',
        'mfv_stopbbarbbar': r'\tilde{t} \rightarrow \bar{b}\bar{b}',
        }[_model(s)]
    year = int(s.rsplit('_')[-1])
    assert 2015 <= year <= 2018
    decay += ' (%i)' % year
    return decay

def _latex(sample):
    tau = _tau(sample)
    if tau < 1000:
        tau = '%3i\mum' % tau
    else:
        assert tau % 1000 == 0
        tau = '%4i\mm' % (tau/1000)
    return r'$%s$,   $c\tau = %s$, $M = %4s\GeV$' % (_decay(sample), tau, _mass(sample))

def _set_signal_stuff(sample):
    sample.is_signal = True
    sample.model = _model(sample)
    sample.decay = _decay(sample)
    sample.tau = _tau(sample)
    sample.mass = _mass(sample)
    sample.latex = _latex(sample)
    sample.xsec = 1e-3
    sample.is_private = sample.dataset.startswith('/mfv_')
    if sample.is_private:
        sample.dbs_inst = 'phys03'
        sample.condor = True
        sample.xrootd_url = xrootd_sites['T3_US_FNALLPC']

########################################################################

########
# 2017 MC
########

qcd_samples_2017 = [
    MCSample('qcdht0700_2017', '/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/AODSIM',                 48042655, nice='QCD, 700 < H_{T} < 1000 GeV',  color=805, syst_frac=0.20, xsec=6.351e3),
    MCSample('qcdht1000_2017', '/QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17DRPremix-PU2017_new_pmx_94X_mc2017_realistic_v11-v1/AODSIM', 16882838, nice='QCD, 1000 < H_{T} < 1500 GeV', color=806, syst_frac=0.20, xsec=1.096e3),
    MCSample('qcdht1500_2017', '/QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v2/AODSIM',         11634434, nice='QCD, 1500 < H_{T} < 2000 GeV', color=807, syst_frac=0.20, xsec=99.0),
    MCSample('qcdht2000_2017', '/QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v2/AODSIM',           5941306, nice='QCD, H_{T} > 2000',            color=808, syst_frac=0.20, xsec=20.2),
    ]

ttbar_samples_2017 = [
    MCSample('ttbarht0600_2017', '/TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM',   81565576, nice='t#bar{t}, 600 < H_{T} < 800 GeV',   color=600, syst_frac=0.15, xsec=1.817),
    MCSample('ttbarht0800_2017', '/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM',  40248127, nice='t#bar{t}, 800 < H_{T} < 1200 GeV',  color=601, syst_frac=0.15, xsec=0.7520),
    MCSample('ttbarht1200_2017', '/TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 13214871, nice='t#bar{t}, 1200 < H_{T} < 2500 GeV', color=602, syst_frac=0.15, xsec=0.1313),
    MCSample('ttbarht2500_2017', '/TTJets_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v3/AODSIM',   5155687, nice='t#bar{t}, H_{T} > 2500 GeV',        color=603, syst_frac=0.15, xsec=1.41e-3),
    ]

leptonic_samples_2017 = [
    MCSample('ttbar_2017',            '/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 155582358, nice='t#bar{t}', color=4, syst_frac=0.15, xsec=832.), # JMTBAD replace with semi/dilep samples
    MCSample('wjetstolnu_2017',       '/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v2/AODSIM',                    33073306, nice='W + jets #rightarrow l#nu', color=  9, syst_frac=0.10, xsec=5.28e4),
    MCSample('wjetstolnuext_2017',    '/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11_ext1-v2/AODSIM',               44652002, nice='W + jets #rightarrow l#nu', color=  9, syst_frac=0.10, xsec=5.28e4),
    MCSample('dyjetstollM10_2017',    '/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v2/AODSIM',                  39521230, nice='DY + jets #rightarrow ll, 10 < M < 50 GeV', color= 29, syst_frac=0.10, xsec=1.58e4),
   #MCSample('dyjetstollM10ext_2017', '/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11_ext1-v1/AODSIM',      39536839, nice='DY + jets #rightarrow ll, 10 < M < 50 GeV', color= 29, syst_frac=0.10, xsec=1.58e4),
    MCSample('dyjetstollM50_2017',    '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17DRPremix-RECOSIMstep_94X_mc2017_realistic_v10-v1/AODSIM',          48675378, nice='DY + jets #rightarrow ll, M > 50 GeV', color= 32, syst_frac=0.10, xsec=5.34e3),
    MCSample('dyjetstollM50ext_2017', '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17DRPremix-RECOSIMstep_94X_mc2017_realistic_v10_ext1-v1/AODSIM',     49313842, nice='DY + jets #rightarrow ll, M > 50 GeV', color= 32, syst_frac=0.10, xsec=5.34e3),
    MCSample('qcdmupt15_2017',        '/QCD_Pt-20toInf_MuEnrichedPt15_TuneCP5_13TeV_pythia8/RunIIFall17DRPremix-PU2017RECOSIMstep_94X_mc2017_realistic_v11-v1/AODSIM',  21833984, nice='QCD, #hat{p}_{T} > 20 GeV, #mu p_{T} > 15 GeV', color=801, syst_frac=0.20, xsec=5.23e8*4.57e-4),
   #MCSample('qcdempt015_2017',       '/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV_pythia8/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/AODSIM',                         11215220, nice='QCD,  15 < #hat{p}_{T} <  20 GeV, EM enriched', color=801, syst_frac=0.20, xsec=1.28e3*0.0018),
   #MCSample('qcdempt020_2017',       '/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV_pythia8/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/AODSIM',                         11590942, nice='QCD,  20 < #hat{p}_{T} <  30 GeV, EM enriched', color=801, syst_frac=0.20, xsec=5.58e8*0.0096),
   #MCSample('qcdempt030_2017',       '/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV_pythia8/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/AODSIM',                         14766010, nice='QCD,  30 < #hat{p}_{T} <  50 GeV, EM enriched', color=801, syst_frac=0.20, xsec=1.36e8*0.0730),
   #MCSample('qcdempt050_2017',       '/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV_pythia8/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/AODSIM',                         10689785, nice='QCD,  50 < #hat{p}_{T} <  80 GeV, EM enriched', color=801, syst_frac=0.20, xsec=1.98e7*0.1460),
   #MCSample('qcdempt080_2017',       '/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV_pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM',                  9104852, nice='QCD,  80 < #hat{p}_{T} < 120 GeV, EM enriched', color=801, syst_frac=0.20, xsec=2.80e6*0.1250),
   #MCSample('qcdempt120_2017',       '/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV_pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v2/AODSIM',                 8515107, nice='QCD, 120 < #hat{p}_{T} < 170 GeV, EM enriched', color=801, syst_frac=0.20, xsec=4.77e5*0.1320),
   #MCSample('qcdempt170_2017',                                                                                                                                                 , nice='QCD, 170 < #hat{p}_{T} < 300 GeV, EM enriched', color=801, syst_frac=0.20, xsec=1.14e5*0.1650),
   #MCSample('qcdempt300_2017',       '/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV_pythia8/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/AODSIM',                        2898084, nice='QCD, #hat{p}_{T} > 300 GeV, EM enriched',       color=801, syst_frac=0.20, xsec=9.00e3*0.1500),
   #MCSample('qcdbctoept015_2017',                                                                                                                                              , nice='QCD,  15 < #hat{p}_{T} <  20 GeV, HF electrons', color=801, syst_frac=0.20, xsec=1.27e9*0.00020),
   #MCSample('qcdbctoept020_2017',    '/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/RunIIFall17DRPremix-PU2017_new_pmx_94X_mc2017_realistic_v11-v1/AODSIM',                5831551, nice='QCD,  20 < #hat{p}_{T} <  30 GeV, HF electrons', color=801, syst_frac=0.20, xsec=5.58e8*0.00059),
   #MCSample('qcdbctoept030_2017',    '/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/AODSIM',                              16073047, nice='QCD,  30 < #hat{p}_{T} <  80 GeV, HF electrons', color=801, syst_frac=0.20, xsec=1.59e8*0.00255),
   #MCSample('qcdbctoept080_2017',    '/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/AODSIM',                             15999466, nice='QCD,  80 < #hat{p}_{T} < 170 GeV, HF electrons', color=801, syst_frac=0.20, xsec=3.22e6*0.01183),
   #MCSample('qcdbctoept170_2017',    '/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/AODSIM',                             9847660, nice='QCD, 170 < #hat{p}_{T} < 250 GeV, HF electrons', color=801, syst_frac=0.20, xsec=1.06e5*0.02492),
   #MCSample('qcdbctoept250_2017',    '/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1/AODSIM',                            10115200, nice='QCD, #hat{p}_{T} > 250 GeV, HF electrons',       color=801, syst_frac=0.20, xsec=2.11e4*0.03375),
    ]

leptonic_samples_sum_2017 = [
    SumSample('wjetstolnusum_2017',    leptonic_samples_2017[ :2]),
   #SumSample('dyjetstollM10sum_2017', leptonic_samples_2017[2:4]),
    SumSample('dyjetstollM50sum_2017', leptonic_samples_2017[3:5]),
    ]

mfv_signal_samples_2017 = [
    MCSample('mfv_neu_tau000100um_M0400_2017', '/mfv_neu_cp2_tau000100um_M0400/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1-e19c32c4f9d94e596684928085d1f2f4/USER', 10000),
    MCSample('mfv_neu_tau000100um_M0600_2017', '/mfv_neu_cp2_tau000100um_M0600/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1-98a6b130f95e6de782a84e79560989b4/USER', 10000),
    MCSample('mfv_neu_tau000100um_M0800_2017', '/mfv_neu_cp2_tau000100um_M0800/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1-f1acdde05f5ae67a63f236356d3a3929/USER', 10000),
    MCSample('mfv_neu_tau000100um_M1200_2017', '/mfv_neu_cp2_tau000100um_M1200/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1-b4c24ee44c55453e27105fbfc1a50f1e/USER', 10000),
    MCSample('mfv_neu_tau000100um_M1600_2017', '/mfv_neu_cp2_tau000100um_M1600/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1-a16fede3a15ec9e78bc60b859a96ec7d/USER', 10000),
    MCSample('mfv_neu_tau000100um_M3000_2017', '/mfv_neu_cp2_tau000100um_M3000/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1-06885863ce8a716b61297c212a1d6ccb/USER', 10000),
    MCSample('mfv_neu_tau000300um_M0400_2017', '/mfv_neu_cp2_tau000300um_M0400/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1-19b36f0dc7bf56de03ab8ea241cddbe4/USER', 10000),
    MCSample('mfv_neu_tau000300um_M0600_2017', '/mfv_neu_cp2_tau000300um_M0600/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1-6f6233dc0f004db465ed499fb0859298/USER', 10000),
    MCSample('mfv_neu_tau000300um_M0800_2017', '/mfv_neu_cp2_tau000300um_M0800/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1-446aa89128f5e93f5d7e59296f77922c/USER', 10000),
    MCSample('mfv_neu_tau000300um_M1200_2017', '/mfv_neu_cp2_tau000300um_M1200/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1-73a90851d5907c77b1d4757913ce05c7/USER', 10000),
    MCSample('mfv_neu_tau000300um_M1600_2017', '/mfv_neu_cp2_tau000300um_M1600/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1-2846a70bad54494c0dca2cf6d6846d8f/USER', 10000),
    MCSample('mfv_neu_tau000300um_M3000_2017', '/mfv_neu_cp2_tau000300um_M3000/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1-adc565be1789a5083a44b2d3645cd801/USER', 10000),
    MCSample('mfv_neu_tau001000um_M0400_2017', '/mfv_neu_cp2_tau001000um_M0400/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1-a757c4bf78c91222ead284fe74e95b67/USER', 10000),
    MCSample('mfv_neu_tau001000um_M0600_2017', '/mfv_neu_cp2_tau001000um_M0600/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1-d45245fcd1697f7c43bc03cf682944a9/USER', 10000),
    MCSample('mfv_neu_tau001000um_M0800_2017', '/mfv_neu_cp2_tau001000um_M0800/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1-6f63fc6954c100df7f3d48f533bb9743/USER', 10000),
    MCSample('mfv_neu_tau001000um_M1200_2017', '/mfv_neu_cp2_tau001000um_M1200/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1-fb45182cb8c5c0041b9b0e198aad7419/USER', 10000),
    MCSample('mfv_neu_tau001000um_M1600_2017', '/mfv_neu_cp2_tau001000um_M1600/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1-08c0f3d8fbe0068949c5db9eac4678e8/USER', 10000),
    MCSample('mfv_neu_tau001000um_M3000_2017', '/mfv_neu_cp2_tau001000um_M3000/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1-570c4a54f61953548f5f22ff0dd9d42c/USER', 10000),
    MCSample('mfv_neu_tau010000um_M0400_2017', '/mfv_neu_cp2_tau010000um_M0400/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1-bd4b3de2f988859726a7cb875f0cc840/USER', 10000),
    MCSample('mfv_neu_tau010000um_M0600_2017', '/mfv_neu_cp2_tau010000um_M0600/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1-d4f1e7ae5b0bb5de2932e0bde376e61a/USER', 10000),
    MCSample('mfv_neu_tau010000um_M0800_2017', '/mfv_neu_cp2_tau010000um_M0800/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1-7b53adcc89bbf593ed5aba60bfb3a5f5/USER', 10000),
    MCSample('mfv_neu_tau010000um_M1200_2017', '/mfv_neu_cp2_tau010000um_M1200/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1-8c12e8f45a6f0e3eecf5a4b2026e69d6/USER', 10000),
    MCSample('mfv_neu_tau010000um_M1600_2017', '/mfv_neu_cp2_tau010000um_M1600/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1-b09c8118ee7dae1892997cd84f519da4/USER', 10000),
    MCSample('mfv_neu_tau010000um_M3000_2017', '/mfv_neu_cp2_tau010000um_M3000/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1-382bee073321d400b463da9e5e04463a/USER', 10000),
    MCSample('mfv_neu_tau030000um_M0400_2017', '/mfv_neu_cp2_tau030000um_M0400/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1-b900b24766a395c6a602904beb671093/USER', 10000),
    MCSample('mfv_neu_tau030000um_M0600_2017', '/mfv_neu_cp2_tau030000um_M0600/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1-b156edd7a24c6cf97c4092bedba82cb3/USER', 10000),
    MCSample('mfv_neu_tau030000um_M0800_2017', '/mfv_neu_cp2_tau030000um_M0800/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1-9073331bdef335aaab0baac64e350432/USER', 10000),
    MCSample('mfv_neu_tau030000um_M1200_2017', '/mfv_neu_cp2_tau030000um_M1200/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1-b077b6b163bf4909a33d46c782207ec2/USER', 10000),
    MCSample('mfv_neu_tau030000um_M1600_2017', '/mfv_neu_cp2_tau030000um_M1600/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1-0d40934f09beb1cfb9c9c3d02dddd16f/USER', 10000),
    MCSample('mfv_neu_tau030000um_M3000_2017', '/mfv_neu_cp2_tau030000um_M3000/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1-a24bebdbc9f1f696346005182d2d7ea2/USER', 10000),
    MCSample('mfv_neu_tau100000um_M0400_2017', '/mfv_neu_cp2_tau100000um_M0400/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1-ac116e932f994ac79ee477bfe1229b61/USER', 10000),
    MCSample('mfv_neu_tau100000um_M0600_2017', '/mfv_neu_cp2_tau100000um_M0600/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1-4b57b0077ac36c6db262447c29e73782/USER', 10000),
    MCSample('mfv_neu_tau100000um_M0800_2017', '/mfv_neu_cp2_tau100000um_M0800/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1-570f60cad749a4699470d1a3f6aff699/USER', 10000),
    MCSample('mfv_neu_tau100000um_M1200_2017', '/mfv_neu_cp2_tau100000um_M1200/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1-4c8c238162f211a5efbbe45d1ecfca18/USER', 10000),
    MCSample('mfv_neu_tau100000um_M1600_2017', '/mfv_neu_cp2_tau100000um_M1600/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1-1af2dcc9c59a4ad598bc4a7f2db8616d/USER', 10000),
    MCSample('mfv_neu_tau100000um_M3000_2017', '/mfv_neu_cp2_tau100000um_M3000/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1-0f425094ecffff5ee7c713678fa04f5c/USER', 10000),
    ]

of_mfv_signal_samples_2017 = [
    MCSample('of_mfv_neu_tau000100um_M0400_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-100um_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 96000),
    MCSample('of_mfv_neu_tau000100um_M0600_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-100um_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('of_mfv_neu_tau000100um_M0800_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-100um_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('of_mfv_neu_tau000100um_M1200_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-100um_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('of_mfv_neu_tau000100um_M1600_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-100um_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('of_mfv_neu_tau000100um_M3000_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-100um_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 99997),
    MCSample('of_mfv_neu_tau000300um_M0400_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-300um_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('of_mfv_neu_tau000300um_M0600_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-300um_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 98000),
    MCSample('of_mfv_neu_tau000300um_M0800_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-300um_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('of_mfv_neu_tau000300um_M1200_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-300um_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('of_mfv_neu_tau000300um_M1600_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-300um_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('of_mfv_neu_tau000300um_M3000_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-300um_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 97999),
    MCSample('of_mfv_neu_tau001000um_M0400_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-1mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('of_mfv_neu_tau001000um_M0600_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-1mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('of_mfv_neu_tau001000um_M0800_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-1mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('of_mfv_neu_tau001000um_M1200_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-1mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 98000),
    MCSample('of_mfv_neu_tau001000um_M1600_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-1mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('of_mfv_neu_tau001000um_M3000_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-1mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 97999),
    MCSample('of_mfv_neu_tau010000um_M0400_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-10mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('of_mfv_neu_tau010000um_M0600_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-10mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('of_mfv_neu_tau010000um_M0800_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-10mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('of_mfv_neu_tau010000um_M1200_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-10mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('of_mfv_neu_tau010000um_M1600_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-10mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('of_mfv_neu_tau010000um_M3000_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-10mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 97999),
    MCSample('of_mfv_neu_tau030000um_M0400_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-30mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('of_mfv_neu_tau030000um_M0600_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-30mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('of_mfv_neu_tau030000um_M0800_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-30mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('of_mfv_neu_tau030000um_M1200_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-30mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('of_mfv_neu_tau030000um_M1600_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-30mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('of_mfv_neu_tau030000um_M3000_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-30mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 99999),
    ]

mfv_stopdbardbar_samples_2017 = [
    MCSample('mfv_stopdbardbar_tau000100um_M0400_2017', '/mfv_stopdbardbar_cp2_tau000100um_M0400/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1-205b3ca875fdf079d3fcbb5409038584/USER', 10000),
    MCSample('mfv_stopdbardbar_tau000100um_M0600_2017', '/mfv_stopdbardbar_cp2_tau000100um_M0600/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1-fe488ff0566ec904395d68041c25d292/USER', 10000),
    MCSample('mfv_stopdbardbar_tau000100um_M0800_2017', '/mfv_stopdbardbar_cp2_tau000100um_M0800/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1-108f49845c950ea66b573802fd76b993/USER', 10000),
    MCSample('mfv_stopdbardbar_tau000100um_M1200_2017', '/mfv_stopdbardbar_cp2_tau000100um_M1200/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1-7ce38d30d549597e5ef0980e1a77bde1/USER', 10000),
    MCSample('mfv_stopdbardbar_tau000100um_M1600_2017', '/mfv_stopdbardbar_cp2_tau000100um_M1600/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1-cb8aea1afffd09910656c276d423c1de/USER', 10000),
    MCSample('mfv_stopdbardbar_tau000100um_M3000_2017', '/mfv_stopdbardbar_cp2_tau000100um_M3000/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1-bd86962041d10293fe3955b9a2a76b49/USER', 10000),
    MCSample('mfv_stopdbardbar_tau000300um_M0400_2017', '/mfv_stopdbardbar_cp2_tau000300um_M0400/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1-51c30fc02760b805732692dd721a5cbb/USER', 10000),
    MCSample('mfv_stopdbardbar_tau000300um_M0600_2017', '/mfv_stopdbardbar_cp2_tau000300um_M0600/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1-2595a5c801f07763931a8ff6eda02a63/USER', 10000),
    MCSample('mfv_stopdbardbar_tau000300um_M0800_2017', '/mfv_stopdbardbar_cp2_tau000300um_M0800/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1-c412575ec602b0b281d9135280672f6f/USER', 10000),
    MCSample('mfv_stopdbardbar_tau000300um_M1200_2017', '/mfv_stopdbardbar_cp2_tau000300um_M1200/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1-9b69b6acaf1b70dec6c84b2c9b483e15/USER', 10000),
    MCSample('mfv_stopdbardbar_tau000300um_M1600_2017', '/mfv_stopdbardbar_cp2_tau000300um_M1600/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1-6f4ec8de19007716424c533ff7fcbad9/USER', 10000),
    MCSample('mfv_stopdbardbar_tau000300um_M3000_2017', '/mfv_stopdbardbar_cp2_tau000300um_M3000/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1-37bfabf9a21402171345e243e2425fce/USER', 10000),
    MCSample('mfv_stopdbardbar_tau001000um_M0400_2017', '/mfv_stopdbardbar_cp2_tau001000um_M0400/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1-3bd71289304d7951247b24b5853da07d/USER', 10000),
    MCSample('mfv_stopdbardbar_tau001000um_M0600_2017', '/mfv_stopdbardbar_cp2_tau001000um_M0600/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1-bf170f8b92d3c7d880869aad6980545c/USER', 10000),
    MCSample('mfv_stopdbardbar_tau001000um_M0800_2017', '/mfv_stopdbardbar_cp2_tau001000um_M0800/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1-041e733a7f4ff104f7dd4f67dbf58be5/USER', 10000),
    MCSample('mfv_stopdbardbar_tau001000um_M1200_2017', '/mfv_stopdbardbar_cp2_tau001000um_M1200/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1-fab8472ef16e983f555223fdb1db93fb/USER', 10000),
    MCSample('mfv_stopdbardbar_tau001000um_M1600_2017', '/mfv_stopdbardbar_cp2_tau001000um_M1600/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1-edf30737fc1be198c48ee3d323ebeb87/USER', 10000),
    MCSample('mfv_stopdbardbar_tau001000um_M3000_2017', '/mfv_stopdbardbar_cp2_tau001000um_M3000/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1-f919e91dd53b0c14e11792ef139c06d8/USER', 10000),
    MCSample('mfv_stopdbardbar_tau010000um_M0400_2017', '/mfv_stopdbardbar_cp2_tau010000um_M0400/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1-1b2d6ee167e76719cb00d4d783998e2e/USER', 10000),
    MCSample('mfv_stopdbardbar_tau010000um_M0600_2017', '/mfv_stopdbardbar_cp2_tau010000um_M0600/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1-25b738ea3ef1af921967b4546f75f92f/USER', 10000),
    MCSample('mfv_stopdbardbar_tau010000um_M0800_2017', '/mfv_stopdbardbar_cp2_tau010000um_M0800/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1-2f966991153a44d60e05d8544a913c1b/USER', 10000),
    MCSample('mfv_stopdbardbar_tau010000um_M1200_2017', '/mfv_stopdbardbar_cp2_tau010000um_M1200/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1-4110b6bd0bc3083e5e4cf8e57f4f4079/USER', 10000),
    MCSample('mfv_stopdbardbar_tau010000um_M1600_2017', '/mfv_stopdbardbar_cp2_tau010000um_M1600/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1-dd199e2242766a01e02398b2ce7f126c/USER', 10000),
    MCSample('mfv_stopdbardbar_tau010000um_M3000_2017', '/mfv_stopdbardbar_cp2_tau010000um_M3000/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1-8477664b65144f1bb1994d6b7f7d3f28/USER', 10000),
    MCSample('mfv_stopdbardbar_tau030000um_M0400_2017', '/mfv_stopdbardbar_cp2_tau030000um_M0400/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1-25b46c716765e8645a4500f5e175acb8/USER', 10000),
    MCSample('mfv_stopdbardbar_tau030000um_M0600_2017', '/mfv_stopdbardbar_cp2_tau030000um_M0600/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1-27cbbb98a47b45a5289409b2d7bc84d0/USER', 10000),
    MCSample('mfv_stopdbardbar_tau030000um_M0800_2017', '/mfv_stopdbardbar_cp2_tau030000um_M0800/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1-08160c924bc4aa73adb4fbd1f3bf2607/USER', 10000),
    MCSample('mfv_stopdbardbar_tau030000um_M1200_2017', '/mfv_stopdbardbar_cp2_tau030000um_M1200/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1-d15231bf5cd7993b220b8ce189a2f4a7/USER', 10000),
    MCSample('mfv_stopdbardbar_tau030000um_M1600_2017', '/mfv_stopdbardbar_cp2_tau030000um_M1600/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1-136b1c100c9499d6b2ba33a57064fce5/USER', 10000),
    MCSample('mfv_stopdbardbar_tau030000um_M3000_2017', '/mfv_stopdbardbar_cp2_tau030000um_M3000/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1-8ccf3900ed71f208132799cc91baa8aa/USER', 10000),
    MCSample('mfv_stopdbardbar_tau100000um_M0400_2017', '/mfv_stopdbardbar_cp2_tau100000um_M0400/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1-92309752170a5d0cea009fdf5e6bcf87/USER', 10000),
    MCSample('mfv_stopdbardbar_tau100000um_M0600_2017', '/mfv_stopdbardbar_cp2_tau100000um_M0600/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1-1930c786a83a564f929f2436120e9f11/USER', 10000),
    MCSample('mfv_stopdbardbar_tau100000um_M0800_2017', '/mfv_stopdbardbar_cp2_tau100000um_M0800/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1-317019a7fc3cefbbd0893f4f46014422/USER', 10000),
    MCSample('mfv_stopdbardbar_tau100000um_M1200_2017', '/mfv_stopdbardbar_cp2_tau100000um_M1200/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1-98039a8a53a0af9912eb3505baf842b9/USER', 10000),
    MCSample('mfv_stopdbardbar_tau100000um_M1600_2017', '/mfv_stopdbardbar_cp2_tau100000um_M1600/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1-0fc64622f57632cfb8f0e54327a4be9a/USER', 10000),
    MCSample('mfv_stopdbardbar_tau100000um_M3000_2017', '/mfv_stopdbardbar_cp2_tau100000um_M3000/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v11-v1-5ccf703e67d55a4cf75fc47cfbde08aa/USER', 10000),
    ]

of_mfv_stopdbardbar_samples_2017 = [
    MCSample('of_mfv_stopdbardbar_tau000100um_M0400_2017', '/StopStopbarTo2Dbar2D_M-400_CTau-100um_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('of_mfv_stopdbardbar_tau000100um_M0600_2017', '/StopStopbarTo2Dbar2D_M-600_CTau-100um_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 96000),
    MCSample('of_mfv_stopdbardbar_tau000100um_M0800_2017', '/StopStopbarTo2Dbar2D_M-800_CTau-100um_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('of_mfv_stopdbardbar_tau000100um_M1200_2017', '/StopStopbarTo2Dbar2D_M-1200_CTau-100um_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('of_mfv_stopdbardbar_tau000100um_M1600_2017', '/StopStopbarTo2Dbar2D_M-1600_CTau-100um_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('of_mfv_stopdbardbar_tau000100um_M3000_2017', '/StopStopbarTo2Dbar2D_M-3000_CTau-100um_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 95000),
    MCSample('of_mfv_stopdbardbar_tau000300um_M0400_2017', '/StopStopbarTo2Dbar2D_M-400_CTau-300um_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('of_mfv_stopdbardbar_tau000300um_M0600_2017', '/StopStopbarTo2Dbar2D_M-600_CTau-300um_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('of_mfv_stopdbardbar_tau000300um_M0800_2017', '/StopStopbarTo2Dbar2D_M-800_CTau-300um_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('of_mfv_stopdbardbar_tau000300um_M1200_2017', '/StopStopbarTo2Dbar2D_M-1200_CTau-300um_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('of_mfv_stopdbardbar_tau000300um_M1600_2017', '/StopStopbarTo2Dbar2D_M-1600_CTau-300um_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('of_mfv_stopdbardbar_tau000300um_M3000_2017', '/StopStopbarTo2Dbar2D_M-3000_CTau-300um_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('of_mfv_stopdbardbar_tau001000um_M0400_2017', '/StopStopbarTo2Dbar2D_M-400_CTau-1mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('of_mfv_stopdbardbar_tau001000um_M0600_2017', '/StopStopbarTo2Dbar2D_M-600_CTau-1mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 97000),
    MCSample('of_mfv_stopdbardbar_tau001000um_M0800_2017', '/StopStopbarTo2Dbar2D_M-800_CTau-1mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('of_mfv_stopdbardbar_tau001000um_M1200_2017', '/StopStopbarTo2Dbar2D_M-1200_CTau-1mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 99000),
    MCSample('of_mfv_stopdbardbar_tau001000um_M1600_2017', '/StopStopbarTo2Dbar2D_M-1600_CTau-1mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('of_mfv_stopdbardbar_tau001000um_M3000_2017', '/StopStopbarTo2Dbar2D_M-3000_CTau-1mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('of_mfv_stopdbardbar_tau010000um_M0400_2017', '/StopStopbarTo2Dbar2D_M-400_CTau-10mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('of_mfv_stopdbardbar_tau010000um_M0600_2017', '/StopStopbarTo2Dbar2D_M-600_CTau-10mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('of_mfv_stopdbardbar_tau010000um_M0800_2017', '/StopStopbarTo2Dbar2D_M-800_CTau-10mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 98000),
    MCSample('of_mfv_stopdbardbar_tau010000um_M1200_2017', '/StopStopbarTo2Dbar2D_M-1200_CTau-10mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('of_mfv_stopdbardbar_tau010000um_M1600_2017', '/StopStopbarTo2Dbar2D_M-1600_CTau-10mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('of_mfv_stopdbardbar_tau010000um_M3000_2017', '/StopStopbarTo2Dbar2D_M-3000_CTau-10mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('of_mfv_stopdbardbar_tau030000um_M0400_2017', '/StopStopbarTo2Dbar2D_M-400_CTau-30mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('of_mfv_stopdbardbar_tau030000um_M0600_2017', '/StopStopbarTo2Dbar2D_M-600_CTau-30mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('of_mfv_stopdbardbar_tau030000um_M0800_2017', '/StopStopbarTo2Dbar2D_M-800_CTau-30mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('of_mfv_stopdbardbar_tau030000um_M1200_2017', '/StopStopbarTo2Dbar2D_M-1200_CTau-30mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 98000),
    MCSample('of_mfv_stopdbardbar_tau030000um_M1600_2017', '/StopStopbarTo2Dbar2D_M-1600_CTau-30mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('of_mfv_stopdbardbar_tau030000um_M3000_2017', '/StopStopbarTo2Dbar2D_M-3000_CTau-30mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    ]

all_signal_samples_2017 = mfv_signal_samples_2017 + mfv_stopdbardbar_samples_2017
of_all_signal_samples_2017 = of_mfv_signal_samples_2017 + of_mfv_stopdbardbar_samples_2017

for s in all_signal_samples_2017 + of_all_signal_samples_2017:
    _set_signal_stuff(s)

########
# 2018 MC
########

qcd_samples_2018 = [
    MCSample('qcdht0700_2018', '/QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM',  43523821, nice='QCD, 700 < H_{T} < 1000 GeV',  color=805, syst_frac=0.20, xsec=6.351e3),
    MCSample('qcdht1000_2018', '/QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 15174716, nice='QCD, 1000 < H_{T} < 1500 GeV', color=806, syst_frac=0.20, xsec=1.096e3),
    MCSample('qcdht1500_2018', '/QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 11082955, nice='QCD, 1500 < H_{T} < 2000 GeV', color=807, syst_frac=0.20, xsec=99.0),
    MCSample('qcdht2000_2018', '/QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM',   5557453, nice='QCD, H_{T} > 2000',            color=808, syst_frac=0.20, xsec=20.2),
    ]

ttbar_samples_2018 = [
    MCSample('ttbarht0600_2018', '/TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM',   14363689, nice='t#bar{t}, 600 < H_{T} < 800 GeV',   color=600, syst_frac=0.15, xsec=1.817),
    MCSample('ttbarht0800_2018', '/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM',  10462756, nice='t#bar{t}, 800 < H_{T} < 1200 GeV',  color=601, syst_frac=0.15, xsec=0.7520),
    MCSample('ttbarht1200_2018', '/TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM',  2897601, nice='t#bar{t}, 1200 < H_{T} < 2500 GeV', color=602, syst_frac=0.15, xsec=0.1313),
    MCSample('ttbarht2500_2018', '/TTJets_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM',   1451104, nice='t#bar{t}, H_{T} > 2500 GeV',        color=603, syst_frac=0.15, xsec=1.41e-3),
    ]

mfv_signal_samples_2018 = [
    MCSample('mfv_neu_tau000100um_M0400_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-100um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau000100um_M0600_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-100um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau000100um_M0800_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-100um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau000100um_M1200_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-100um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau000100um_M1600_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-100um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 96000),
    MCSample('mfv_neu_tau000100um_M3000_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-100um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau000300um_M0400_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-300um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau000300um_M0600_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-300um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau000300um_M0800_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-300um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau000300um_M1200_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-300um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau000300um_M1600_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-300um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau000300um_M3000_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-300um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau001000um_M0400_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-1mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau001000um_M0600_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-1mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau001000um_M0800_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-1mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau001000um_M1200_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-1mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau001000um_M1600_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-1mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau001000um_M3000_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-1mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 99998),
    MCSample('mfv_neu_tau010000um_M0400_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-10mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau010000um_M0600_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-10mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 98000),
    MCSample('mfv_neu_tau010000um_M0800_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-10mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau010000um_M1200_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-10mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau010000um_M1600_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-10mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau010000um_M3000_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-10mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 99999),
    MCSample('mfv_neu_tau030000um_M0400_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-30mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau030000um_M0600_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-30mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau030000um_M0800_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-30mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau030000um_M1200_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-30mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau030000um_M1600_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-30mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau030000um_M3000_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-30mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    ]

mfv_stopdbardbar_samples_2018 = [
    MCSample('mfv_stopdbardbar_tau000100um_M0400_2018', '/StopStopbarTo2Dbar2D_M-400_CTau-100um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau000100um_M0600_2018', '/StopStopbarTo2Dbar2D_M-600_CTau-100um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau000100um_M0800_2018', '/StopStopbarTo2Dbar2D_M-800_CTau-100um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau000100um_M1200_2018', '/StopStopbarTo2Dbar2D_M-1200_CTau-100um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau000100um_M1600_2018', '/StopStopbarTo2Dbar2D_M-1600_CTau-100um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau000100um_M3000_2018', '/StopStopbarTo2Dbar2D_M-3000_CTau-100um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau000300um_M0400_2018', '/StopStopbarTo2Dbar2D_M-400_CTau-300um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau000300um_M0600_2018', '/StopStopbarTo2Dbar2D_M-600_CTau-300um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau000300um_M0800_2018', '/StopStopbarTo2Dbar2D_M-800_CTau-300um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau000300um_M1200_2018', '/StopStopbarTo2Dbar2D_M-1200_CTau-300um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau000300um_M1600_2018', '/StopStopbarTo2Dbar2D_M-1600_CTau-300um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 98000),
    MCSample('mfv_stopdbardbar_tau000300um_M3000_2018', '/StopStopbarTo2Dbar2D_M-3000_CTau-300um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau001000um_M0400_2018', '/StopStopbarTo2Dbar2D_M-400_CTau-1mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau001000um_M0600_2018', '/StopStopbarTo2Dbar2D_M-600_CTau-1mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau001000um_M0800_2018', '/StopStopbarTo2Dbar2D_M-800_CTau-1mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau001000um_M1200_2018', '/StopStopbarTo2Dbar2D_M-1200_CTau-1mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau001000um_M1600_2018', '/StopStopbarTo2Dbar2D_M-1600_CTau-1mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 96000),
    MCSample('mfv_stopdbardbar_tau001000um_M3000_2018', '/StopStopbarTo2Dbar2D_M-3000_CTau-1mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau010000um_M0400_2018', '/StopStopbarTo2Dbar2D_M-400_CTau-10mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau010000um_M0600_2018', '/StopStopbarTo2Dbar2D_M-600_CTau-10mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau010000um_M0800_2018', '/StopStopbarTo2Dbar2D_M-800_CTau-10mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau010000um_M1200_2018', '/StopStopbarTo2Dbar2D_M-1200_CTau-10mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau010000um_M1600_2018', '/StopStopbarTo2Dbar2D_M-1600_CTau-10mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau010000um_M3000_2018', '/StopStopbarTo2Dbar2D_M-3000_CTau-10mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau030000um_M0400_2018', '/StopStopbarTo2Dbar2D_M-400_CTau-30mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 98000),
    MCSample('mfv_stopdbardbar_tau030000um_M0600_2018', '/StopStopbarTo2Dbar2D_M-600_CTau-30mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 99000),
    MCSample('mfv_stopdbardbar_tau030000um_M0800_2018', '/StopStopbarTo2Dbar2D_M-800_CTau-30mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau030000um_M1200_2018', '/StopStopbarTo2Dbar2D_M-1200_CTau-30mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau030000um_M1600_2018', '/StopStopbarTo2Dbar2D_M-1600_CTau-30mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau030000um_M3000_2018', '/StopStopbarTo2Dbar2D_M-3000_CTau-30mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 100000),
    ]

all_signal_samples_2018 = mfv_signal_samples_2018 + mfv_stopdbardbar_samples_2018

for s in all_signal_samples_2018:
    _set_signal_stuff(s)

########
# data
########

data_samples_2017 = [                                              # in dataset      in json          int lumi avail (/fb)
    DataSample('JetHT2017B', '/JetHT/Run2017B-17Nov2017-v1/AOD'),  # 297047 299329   297050 299329     4.794
    DataSample('JetHT2017C', '/JetHT/Run2017C-17Nov2017-v1/AOD'),  # 299368 302029   299368 302029     9.631
    DataSample('JetHT2017D', '/JetHT/Run2017D-17Nov2017-v1/AOD'),  # 302031 302663   302031 302663     4.248
    DataSample('JetHT2017E', '/JetHT/Run2017E-17Nov2017-v1/AOD'),  # 303824 304797   303825 304797     9.315
    DataSample('JetHT2017F', '/JetHT/Run2017F-17Nov2017-v1/AOD'),  # 305040 306460   305044 306460    13.540
    ]

auxiliary_data_samples_2017 = [
    DataSample('SingleMuon2017B', '/SingleMuon/Run2017B-17Nov2017-v1/AOD'),
    DataSample('SingleMuon2017C', '/SingleMuon/Run2017C-17Nov2017-v1/AOD'),
    DataSample('SingleMuon2017D', '/SingleMuon/Run2017D-17Nov2017-v1/AOD'),
    DataSample('SingleMuon2017E', '/SingleMuon/Run2017E-17Nov2017-v1/AOD'),
    DataSample('SingleMuon2017F', '/SingleMuon/Run2017F-17Nov2017-v1/AOD'),
    ]

data_samples_2018 = [
    DataSample('JetHT2018A', '/JetHT/Run2018A-17Sep2018-v1/AOD'),  # 315257 316995   315257 316995   14.028
    DataSample('JetHT2018B', '/JetHT/Run2018B-17Sep2018-v1/AOD'),  # 317080 319310   317080 319077    7.067
    DataSample('JetHT2018C', '/JetHT/Run2018C-17Sep2018-v1/AOD'),  # 319337 320065   319337 320065    6.895
    DataSample('JetHT2018D', '/JetHT/Run2018D-PromptReco-v2/AOD'), # 320497 325175   320673 325172   31.747
    ]

auxiliary_data_samples_2018 = [
    DataSample('SingleMuon2018A', '/SingleMuon/Run2018A-17Sep2018-v2/AOD'),
    DataSample('SingleMuon2018B', '/SingleMuon/Run2018B-17Sep2018-v1/AOD'),
    DataSample('SingleMuon2018C', '/SingleMuon/Run2018C-17Sep2018-v1/AOD'),
    DataSample('SingleMuon2018D', '/SingleMuon/Run2018D-PromptReco-v2/AOD'),
    ]

########################################################################

registry = SamplesRegistry()

# shortcuts, be careful:
# - can't add data by primary (have the same primary for different datasets)
from functools import partial
_adbp = registry.add_dataset_by_primary
_adbp3 = partial(_adbp, dbs_inst='phys03')

__all__ = [
    'qcd_samples_2017',
    'ttbar_samples_2017',
    'leptonic_samples_2017',
    'leptonic_samples_sum_2017',
    'mfv_signal_samples_2017',
    'of_mfv_signal_samples_2017',
    'mfv_stopdbardbar_samples_2017',
    'of_mfv_stopdbardbar_samples_2017',
    'qcd_samples_2018',
    'ttbar_samples_2018',
    'mfv_signal_samples_2018',
    'mfv_stopdbardbar_samples_2018',
    'data_samples_2017',
    'auxiliary_data_samples_2017',
    'data_samples_2018',
    'auxiliary_data_samples_2018',

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
    'all_signal_samples_2017',
    'of_all_signal_samples_2017',
    'all_signal_samples_2018',
    ]

########################################################################

########
# Extra datasets and other overrides go here.
########

########
# miniaod
########

for sample in data_samples_2017 + auxiliary_data_samples_2017:
    sample.add_dataset('miniaod', sample.dataset.replace('17Nov2017-v1/AOD', '31Mar2018-v1/MINIAOD'))
for sample in data_samples_2018 + auxiliary_data_samples_2018:
    sample.add_dataset('miniaod', sample.dataset.replace('AOD', 'MINIAOD'))

_adbp('miniaod', '/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',          47724800)
_adbp('miniaod', '/QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1/MINIAODSIM', 16882838)
_adbp('miniaod', '/QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM',         11634434)
_adbp('miniaod', '/QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM',           5941306)
_adbp('miniaod', '/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1/MINIAODSIM',      154280331)
ttbarht0600_2017.add_dataset('miniaod', '/TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',    81507662)
ttbarht0800_2017.add_dataset('miniaod', '/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',   40191637)
ttbarht1200_2017.add_dataset('miniaod', '/TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',  13214871)
ttbarht2500_2017.add_dataset('miniaod', '/TTJets_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v3/MINIAODSIM',    5155687)
wjetstolnu_2017.add_dataset('miniaod', '/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 33073306)
wjetstolnuext_2017.add_dataset('miniaod', '/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14_ext1-v2/MINIAODSIM', 44767978)
dyjetstollM10_2017.add_dataset('miniaod', '/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 39521230)
#dyjetstollM10ext_2017.add_dataset('miniaod', '/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14_ext1-v1/MINIAODSIM', 39536839)
dyjetstollM50_2017.add_dataset('miniaod', '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017RECOSIMstep_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 48675378)
dyjetstollM50ext_2017.add_dataset('miniaod', '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017RECOSIMstep_12Apr2018_94X_mc2017_realistic_v14_ext1-v1/MINIAODSIM', 49125561)
_adbp('miniaod', '/QCD_Pt-20toInf_MuEnrichedPt15_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017RECOSIMstep_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',  21799788)
#_adbp('miniaod', '/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',  11215220)
#_adbp('miniaod', '/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',  11212810)
#_adbp('miniaod', '/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',  14766010)
#_adbp('miniaod', '/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',  10477146)
#_adbp('miniaod', '/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',  9104852)
#_adbp('miniaod', '/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM',  8515107)
#_adbp('miniaod', '/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',  2874295)
#_adbp('miniaod', '/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1/MINIAODSIM',  5678761)
#_adbp('miniaod', '/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',  16073047)
#_adbp('miniaod', '/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',  15999466)
#_adbp('miniaod', '/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',  9847660)
#_adbp('miniaod', '/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',  9996886)
# the 2018 samples have 'MLM' in them so this works still, ugh
_adbp('miniaod', '/QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM',  43523821)
_adbp('miniaod', '/QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 15065049)
_adbp('miniaod', '/QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 10955087)
_adbp('miniaod', '/QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM',   5475677)
ttbarht0600_2018.add_dataset('miniaod', '/TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM',  14149394)
ttbarht0800_2018.add_dataset('miniaod', '/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 10372802)
ttbarht1200_2018.add_dataset('miniaod', '/TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 2779427)
ttbarht2500_2018.add_dataset('miniaod', '/TTJets_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM',  1451104)

for sample in mfv_signal_samples_2017 + mfv_stopdbardbar_samples_2017:
    sample.add_dataset('miniaod', '/%s/None/USER' % sample.primary_dataset, sample.nevents_orig)
    sample.datasets['miniaod'].condor = True
    sample.datasets['miniaod'].xrootd_url = xrootd_sites['T3_US_FNALLPC']

_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-100um_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 96000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-100um_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-100um_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-100um_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-100um_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-100um_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 99997)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-300um_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-300um_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 98000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-300um_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-300um_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-300um_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-300um_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 97999)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-1mm_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-1mm_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-1mm_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-1mm_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 96000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-1mm_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-1mm_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 97999)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-10mm_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-10mm_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-10mm_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-10mm_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-10mm_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-10mm_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 97999)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-30mm_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-30mm_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-30mm_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-30mm_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-30mm_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-30mm_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 99999)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-400_CTau-100um_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-600_CTau-100um_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 96000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-800_CTau-100um_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-1200_CTau-100um_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-1600_CTau-100um_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-3000_CTau-100um_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 95000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-400_CTau-300um_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-600_CTau-300um_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-800_CTau-300um_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-1200_CTau-300um_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-1600_CTau-300um_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-3000_CTau-300um_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-400_CTau-1mm_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-600_CTau-1mm_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 97000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-800_CTau-1mm_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-1200_CTau-1mm_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 99000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-1600_CTau-1mm_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-3000_CTau-1mm_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-400_CTau-10mm_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-600_CTau-10mm_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-800_CTau-10mm_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 98000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-1200_CTau-10mm_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-1600_CTau-10mm_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-3000_CTau-10mm_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-400_CTau-30mm_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-600_CTau-30mm_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-800_CTau-30mm_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-1200_CTau-30mm_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 98000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-1600_CTau-30mm_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-3000_CTau-30mm_TuneCP2_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-100um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-100um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-100um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-100um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 96000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-100um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 96000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-100um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-300um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-300um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-300um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-300um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-300um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-300um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-1mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 97000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-1mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-1mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-1mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-1mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-1mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 99998)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-10mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-10mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 98000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-10mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-10mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-10mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-10mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 99999)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-30mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-30mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-30mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-30mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-30mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-30mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-400_CTau-100um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-600_CTau-100um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-800_CTau-100um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-1200_CTau-100um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-1600_CTau-100um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-3000_CTau-100um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-400_CTau-300um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-600_CTau-300um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-800_CTau-300um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 88000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-1200_CTau-300um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-1600_CTau-300um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 96000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-3000_CTau-300um_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-400_CTau-1mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-600_CTau-1mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-800_CTau-1mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 97000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-1200_CTau-1mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-1600_CTau-1mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 96000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-3000_CTau-1mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-400_CTau-10mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-600_CTau-10mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-800_CTau-10mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-1200_CTau-10mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-1600_CTau-10mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-3000_CTau-10mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-400_CTau-30mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 98000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-600_CTau-30mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 99000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-800_CTau-30mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-1200_CTau-30mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-1600_CTau-30mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)
_adbp('miniaod', '/StopStopbarTo2Dbar2D_M-3000_CTau-30mm_TuneCP2_13TeV_2018-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000)

########
# ntuples
########

for x in data_samples_2017 + qcd_samples_2017 + ttbar_samples_2017 + mfv_signal_samples_2017 + mfv_stopdbardbar_samples_2017 + \
         data_samples_2018 + qcd_samples_2018:
    x.add_dataset("ntuplev23m")
    if not x.is_signal:
        x.add_dataset("ntuplev23m_ntkseeds")

for x in data_samples_2017 + qcd_samples_2017 + data_samples_2018 + qcd_samples_2018:
    x.add_dataset("nr_trackingtreerv23mv3")
    x.add_dataset("nr_k0ntuplev23mv4")

for x in data_samples_2017 + qcd_samples_2017 + ttbar_samples_2017 + mfv_signal_samples_2017 + mfv_stopdbardbar_samples_2017 + \
         data_samples_2018 + qcd_samples_2018 + ttbar_samples_2018:
    x.add_dataset("ntuplev24m")
    if not x.is_signal:
        x.add_dataset("ntuplev24m_ntkseeds")

for x in of_mfv_neu_tau000100um_M0400_2017, of_mfv_neu_tau000100um_M0600_2017, of_mfv_neu_tau000100um_M0800_2017, of_mfv_neu_tau000100um_M1200_2017, of_mfv_neu_tau000100um_M1600_2017, of_mfv_neu_tau000100um_M3000_2017, of_mfv_neu_tau000300um_M0400_2017, of_mfv_neu_tau000300um_M0600_2017, of_mfv_neu_tau000300um_M0800_2017, of_mfv_neu_tau000300um_M1200_2017, of_mfv_neu_tau000300um_M1600_2017, of_mfv_neu_tau000300um_M3000_2017, of_mfv_neu_tau001000um_M0400_2017, of_mfv_neu_tau001000um_M0600_2017, of_mfv_neu_tau001000um_M0800_2017, of_mfv_neu_tau001000um_M1200_2017, of_mfv_neu_tau001000um_M1600_2017, of_mfv_neu_tau001000um_M3000_2017, of_mfv_neu_tau010000um_M0400_2017, of_mfv_neu_tau010000um_M0600_2017, of_mfv_neu_tau010000um_M0800_2017, of_mfv_neu_tau010000um_M1200_2017, of_mfv_neu_tau010000um_M1600_2017, of_mfv_neu_tau030000um_M0400_2017, of_mfv_neu_tau030000um_M0600_2017, of_mfv_neu_tau030000um_M0800_2017, of_mfv_neu_tau030000um_M1200_2017, of_mfv_neu_tau030000um_M1600_2017, of_mfv_stopdbardbar_tau000100um_M0400_2017, of_mfv_stopdbardbar_tau000100um_M0600_2017, of_mfv_stopdbardbar_tau000100um_M0800_2017, of_mfv_stopdbardbar_tau000100um_M1200_2017, of_mfv_stopdbardbar_tau000100um_M1600_2017, of_mfv_stopdbardbar_tau000100um_M3000_2017, of_mfv_stopdbardbar_tau000300um_M0400_2017, of_mfv_stopdbardbar_tau000300um_M0600_2017, of_mfv_stopdbardbar_tau000300um_M0800_2017, of_mfv_stopdbardbar_tau000300um_M1200_2017, of_mfv_stopdbardbar_tau000300um_M1600_2017, of_mfv_stopdbardbar_tau000300um_M3000_2017, of_mfv_stopdbardbar_tau001000um_M0400_2017, of_mfv_stopdbardbar_tau001000um_M0600_2017, of_mfv_stopdbardbar_tau001000um_M0800_2017, of_mfv_stopdbardbar_tau001000um_M1200_2017, of_mfv_stopdbardbar_tau001000um_M1600_2017, of_mfv_stopdbardbar_tau010000um_M0400_2017, of_mfv_stopdbardbar_tau010000um_M0600_2017, of_mfv_stopdbardbar_tau010000um_M0800_2017, of_mfv_stopdbardbar_tau010000um_M1200_2017, of_mfv_stopdbardbar_tau010000um_M1600_2017, of_mfv_stopdbardbar_tau030000um_M0400_2017, of_mfv_stopdbardbar_tau030000um_M0600_2017, of_mfv_stopdbardbar_tau030000um_M0800_2017, of_mfv_stopdbardbar_tau030000um_M1200_2017, of_mfv_stopdbardbar_tau030000um_M1600_2017, of_mfv_stopdbardbar_tau030000um_M3000_2017, mfv_neu_tau000100um_M0400_2018, mfv_neu_tau000100um_M0800_2018, mfv_neu_tau000100um_M1200_2018, mfv_neu_tau000100um_M1600_2018, mfv_neu_tau000100um_M3000_2018, mfv_neu_tau000300um_M0400_2018, mfv_neu_tau000300um_M0600_2018, mfv_neu_tau000300um_M0800_2018, mfv_neu_tau000300um_M1200_2018, mfv_neu_tau000300um_M1600_2018, mfv_neu_tau000300um_M3000_2018, mfv_neu_tau001000um_M0400_2018, mfv_neu_tau001000um_M0600_2018, mfv_neu_tau001000um_M0800_2018, mfv_neu_tau001000um_M1200_2018, mfv_neu_tau001000um_M1600_2018, mfv_neu_tau001000um_M3000_2018, mfv_neu_tau010000um_M0400_2018, mfv_neu_tau010000um_M0600_2018, mfv_neu_tau010000um_M0800_2018, mfv_neu_tau010000um_M1200_2018, mfv_neu_tau010000um_M1600_2018, mfv_neu_tau030000um_M0400_2018, mfv_neu_tau030000um_M0600_2018, mfv_neu_tau030000um_M0800_2018, mfv_neu_tau030000um_M1200_2018, mfv_neu_tau030000um_M1600_2018, mfv_stopdbardbar_tau000100um_M0400_2018, mfv_stopdbardbar_tau000100um_M0600_2018, mfv_stopdbardbar_tau000100um_M0800_2018, mfv_stopdbardbar_tau000100um_M1200_2018, mfv_stopdbardbar_tau000100um_M1600_2018, mfv_stopdbardbar_tau000100um_M3000_2018, mfv_stopdbardbar_tau000300um_M0400_2018, mfv_stopdbardbar_tau000300um_M0600_2018, mfv_stopdbardbar_tau000300um_M0800_2018, mfv_stopdbardbar_tau000300um_M1200_2018, mfv_stopdbardbar_tau000300um_M1600_2018, mfv_stopdbardbar_tau000300um_M3000_2018, mfv_stopdbardbar_tau001000um_M0400_2018, mfv_stopdbardbar_tau001000um_M0600_2018, mfv_stopdbardbar_tau001000um_M0800_2018, mfv_stopdbardbar_tau001000um_M1200_2018, mfv_stopdbardbar_tau001000um_M1600_2018, mfv_stopdbardbar_tau010000um_M0400_2018, mfv_stopdbardbar_tau010000um_M0600_2018, mfv_stopdbardbar_tau010000um_M0800_2018, mfv_stopdbardbar_tau010000um_M1200_2018, mfv_stopdbardbar_tau010000um_M1600_2018, mfv_stopdbardbar_tau030000um_M0400_2018, mfv_stopdbardbar_tau030000um_M0600_2018, mfv_stopdbardbar_tau030000um_M0800_2018, mfv_stopdbardbar_tau030000um_M1200_2018, mfv_stopdbardbar_tau030000um_M1600_2018, mfv_stopdbardbar_tau030000um_M3000_2018:
    x.add_dataset("ntuplev24m")

for x in qcd_samples_2017 + ttbar_samples_2017 + mfv_signal_samples_2017 + mfv_stopdbardbar_samples_2017:
    x.add_dataset("ntuplev24m_rescalednsigmadxy")

for x in qcd_samples_2017 + ttbar_samples_2017 + \
         qcd_samples_2018 + ttbar_samples_2018:
    x.add_dataset("ntuplev25m")

########
# automatic condor declarations for ntuples
########

ds4condor = ['ntuple', 'v0ntuple', 'pick1vtx']
for s in registry.all():
    for ds in s.datasets.keys():
        for ds4 in ds4condor:
            if ds.startswith(ds4):
                s.datasets[ds].condor = True
                s.datasets[ds].xrootd_url = xrootd_sites['T3_US_FNALLPC']

########
# other condor declarations, generate condorable dict with Shed/condor_list.py
########

# 2018-11-01
condorable = {
    "T3_US_FNALLPC": {
        "main": [],
        "miniaod": ttbar_samples_2017,
        },
    "T1_US_FNAL_Disk": {
        "miniaod": [qcdht0700_2017, qcdht1500_2017, qcdht2000_2017, ttbar_2017, dyjetstollM10_2017, qcdmupt15_2017, qcdht0700_2018, qcdht1000_2018, ttbarht0800_2018],
        },
    "T2_US_Wisconsin": {},
    "T2_US_Purdue": {
        "miniaod": [qcdht1500_2018],
        },
    "T2_DE_DESY": {
        "main": [],
        "miniaod": [],
        },
    }

for site, d in condorable.iteritems():
    if not xrootd_sites.has_key(site):
        raise ValueError('need entry in xrootd_sites for %s' % site)
    for ds, samples in d.iteritems():
        for s in samples:
            s.datasets[ds].condor = True
            s.datasets[ds].xrootd_url = xrootd_sites[site]

########
# other info
########

for ds in 'main', 'miniaod':
    # these in status=PRODUCTION
    #for s in ():
    #    s.datasets[ds].ignore_invalid = True

    # 'PU2017' in dataset can be a lie https://hypernews.cern.ch/HyperNews/CMS/get/physics-validation/3128.html
    for s in qcdht0700_2017, dyjetstollM10_2017, dyjetstollM50_2017, dyjetstollM50ext_2017:
        s.datasets[ds].notes['buggedpileup2017'] = True

    # set up jsons
    for y,ss in (2017, data_samples_2017 + auxiliary_data_samples_2017), (2018, data_samples_2018 + auxiliary_data_samples_2018):
        for s in ss:
            s.datasets[ds].json      = json_path('ana_%s.json'      % y)
            s.datasets[ds].json_10pc = json_path('ana_%s_10pc.json' % y)
            s.datasets[ds].json_1pc  = json_path('ana_%s_1pc.json'  % y)

########################################################################

if __name__ == '__main__':
    main(registry)

    import sys, re
    from pprint import pprint
    from JMTucker.Tools import DBS, colors
    from JMTucker.Tools.general import popen

    if 0:
        for year in 2017, 2018:
            for line in file(str(year)):
                if line.startswith('/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S'):
                    model = 'mfv_neu'
                elif line.startswith('/StopStopbarTo2Dbar2D'):
                    model = 'mfv_stopdbardbar'
                else:
                    print 'unrecognized line %r' % line
                    continue
                dataset = line.strip()
                mass, tau_s = re.search(r'M-(\d+)_CTau-(.*)_Tune', line).groups()
                mass, tau, tau_unit = int(mass), int(tau_s[:-2]), tau_s[-2:]
                if tau_unit == 'mm':
                    tau *= 1000
                else:
                    assert tau_unit == 'um'
                if mass in [400,600,800,1200,1600,3000] and tau in [100,300,1000,10000,30000]:
                    nevents = DBS.numevents_in_dataset(dataset)
                    print "    MCSample('%s_tau%06ium_M%04i_%s', '%s', %i)," % (model, tau, mass, year, dataset, nevents)

    if 0:
        for s in all_of_signal_samples_2017 + all_signal_samples_2018:
            l = DBS.datasets('/%s/*/MINIAODSIM' % s.primary_dataset)
            if len(l) == 1:
                nevents = DBS.numevents_in_dataset(l[0])
                print "_adbp('miniaod', '%s', %i)" % (l[0], nevents)
            else:
                print colors.boldred('no miniaod for %s' % s.name)
