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
        'mfv_splitSUSY': r'\tilde{g} \rightarrow qq\tilde{\chi}'
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
    #MCSample('qcdht0300_2017', '/QCD_HT300to500_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 59569132, nice='QCD, 300 < H_{T} < 500 GeV',  color=803, syst_frac=0.20, xsec=3.226e5),
    #MCSample('qcdht0500_2017', '/QCD_HT500to700_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v2/AODSIM', 56854504, nice='QCD, 500 < H_{T} < 700 GeV', color=804, syst_frac=0.20, xsec=2.998e4),
    MCSample('qcdht0700_2017', '/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/AODSIM',                 48042655, nice='QCD, 700 < H_{T} < 1000 GeV',  color=805, syst_frac=0.20, xsec=6.351e3),
    MCSample('qcdht1000_2017', '/QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17DRPremix-PU2017_new_pmx_94X_mc2017_realistic_v11-v1/AODSIM', 16882838, nice='QCD, 1000 < H_{T} < 1500 GeV', color=806, syst_frac=0.20, xsec=1.096e3),
    MCSample('qcdht1500_2017', '/QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v2/AODSIM',         11634434, nice='QCD, 1500 < H_{T} < 2000 GeV', color=807, syst_frac=0.20, xsec=99.0),
    MCSample('qcdht2000_2017', '/QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v2/AODSIM',           5941306, nice='QCD, H_{T} > 2000',            color=808, syst_frac=0.20, xsec=20.2),
    ]

ttbar_samples_2017 = [
    #MCSample('ttbar_2017',     '/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM',    155582358, nice='t#bar{t}',                   color=4,   syst_frac=0.15, xsec=832.),
    MCSample('ttbarht0600_2017', '/TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM',   81565576, nice='t#bar{t}, 600 < H_{T} < 800 GeV',   color=600, syst_frac=0.15, xsec=1.817),
    MCSample('ttbarht0800_2017', '/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM',  40248127, nice='t#bar{t}, 800 < H_{T} < 1200 GeV',  color=601, syst_frac=0.15, xsec=0.7520),
    MCSample('ttbarht1200_2017', '/TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 13214871, nice='t#bar{t}, 1200 < H_{T} < 2500 GeV', color=602, syst_frac=0.15, xsec=0.1313),
    MCSample('ttbarht2500_2017', '/TTJets_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v3/AODSIM',   5155687, nice='t#bar{t}, H_{T} > 2500 GeV',        color=603, syst_frac=0.15, xsec=1.41e-3),
    ]

bjet_samples_2017 = [
    MCSample('qcdht0200_2017', '/QCD_HT200to300_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 59427619, nice='QCD, 200 < H_{T} < 300 GeV',  color=802, syst_frac=0.20, xsec=1.547e6),
    MCSample('qcdht0300_2017', '/QCD_HT300to500_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 59569132, nice='QCD, 300 < H_{T} < 500 GeV',  color=803, syst_frac=0.20, xsec=3.226e5),
    MCSample('qcdht0500_2017', '/QCD_HT500to700_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v2/AODSIM', 56854504, nice='QCD, 500 < H_{T} < 700 GeV', color=804, syst_frac=0.20, xsec=2.998e4),
    MCSample('ttbar_2017',     '/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM',    155582358, nice='t#bar{t}',                   color=4,   syst_frac=0.15, xsec=832.),
    MCSample('ttHbb_2017',     '/ttHJetTobb_M125_TuneCP5_13TeV_amcatnloFXFX_madspin_pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM',      10055168, nice='ttHbb', color=1, syst_frac=0.20, xsec=0.5269), # FIXME note syst_frac here isn't correct here or below, but is probably irrelevant
    MCSample('ttZ_2017',       '/ttZJets_TuneCP5_13TeV_madgraphMLM_pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM',                        9771320, nice='ttZ', color=1, syst_frac=0.20, xsec=0.5407),
    MCSample('ttZext_2017',    '/ttZJets_TuneCP5_13TeV_madgraphMLM_pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11_ext1-v3/AODSIM',                   8536618, nice='ttZ', color=1, syst_frac=0.20, xsec=0.5407),
    MCSample('singletop_tchan_top_2017',    '/ST_t-channel_top_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM',             5982064, nice='singletop t-channel top', color=1, syst_frac=0.20, xsec=113.3),
    MCSample('singletop_tchan_antitop_2017','/ST_t-channel_antitop_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8/RunIIFall17DRPremix-PU2017_new_pmx_94X_mc2017_realistic_v11-v2/AODSIM', 3675910, nice='singletop t-channel antitop', color=1, syst_frac=0.20, xsec=67.91),
    ]
bjet_samples_sum_2017 = [
    SumSample('ttZsum_2017', bjet_samples_2017[4:6]),
]

leptonic_samples_2017 = [
    #MCSample('ttbar_2017',            '/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 155582358, nice='t#bar{t}', color=4, syst_frac=0.15, xsec=832.), # inclusive ttbar sample has been moved to bjet_samples_2017
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

Zvv_samples_2017 = [
    MCSample('zjetstonunuht0100_2017', '/ZJetsToNuNu_HT-100To200_13TeV-madgraph/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/AODSIM', 22880098, nice='Z + jets #rightarrow #nu #nu 100 < H_{T} < 200 GeV', color=1, syst_frac=0.20, xsec=302.8),
    MCSample('zjetstonunuht0200_2017', '/ZJetsToNuNu_HT-200To400_13TeV-madgraph/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/AODSIM', 21675916, nice='Z + jets #rightarrow #nu #nu 200 < H_{T} < 400 GeV', color=1, syst_frac=0.20, xsec=92.59),
    MCSample('zjetstonunuht0400_2017', '/ZJetsToNuNu_HT-400To600_13TeV-madgraph/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/AODSIM', 9134120, nice='Z + jets #rightarrow #nu #nu 400 < H_{T} < 600 GeV', color=1, syst_frac=0.20, xsec=13.18),
    MCSample('zjetstonunuht0600_2017', '/ZJetsToNuNu_HT-600To800_13TeV-madgraph/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/AODSIM', 5697594, nice='Z + jets #rightarrow #nu #nu 600 < H_{T} < 800 GeV', color=1, syst_frac=0.20, xsec=3.257),
    MCSample('zjetstonunuht0800_2017', '/ZJetsToNuNu_HT-800To1200_13TeV-madgraph/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/AODSIM', 2058077, nice='Z + jets #rightarrow #nu #nu 800 < H_{T} < 1200 GeV', color=1, syst_frac=0.20, xsec=1.49),
    MCSample('zjetstonunuht1200_2017', '/ZJetsToNuNu_HT-1200To2500_13TeV-madgraph/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/AODSIM', 338948, nice='Z + jets #rightarrow #nu #nu 1200 < H_{T} < 2500 GeV', color=1, syst_frac=0.20, xsec=0.3419),
    MCSample('zjetstonunuht2500_2017', '/ZJetsToNuNu_HT-2500ToInf_13TeV-madgraph/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/AODSIM', 6734, nice='Z + jets #rightarrow #nu #nu H_{T} > 2500 GeV', color=1, syst_frac=0.20, xsec=0.005146),
    ]

mfv_signal_samples_2017 = [
    MCSample('mfv_neu_tau000100um_M0400_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-100um_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 96000),
    MCSample('mfv_neu_tau000100um_M0600_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-100um_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau000100um_M0800_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-100um_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau000100um_M1200_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-100um_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau000100um_M1600_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-100um_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau000100um_M3000_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-100um_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 99997),
    MCSample('mfv_neu_tau000300um_M0400_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-300um_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau000300um_M0600_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-300um_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 98000),
    MCSample('mfv_neu_tau000300um_M0800_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-300um_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau000300um_M1200_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-300um_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau000300um_M1600_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-300um_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau000300um_M3000_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-300um_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 97999),
    MCSample('mfv_neu_tau001000um_M0400_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-1mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau001000um_M0600_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-1mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau001000um_M0800_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-1mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau001000um_M1200_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-1mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 98000),
    MCSample('mfv_neu_tau001000um_M1600_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-1mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau001000um_M3000_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-1mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 97999),
    MCSample('mfv_neu_tau010000um_M0400_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-10mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau010000um_M0600_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-10mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau010000um_M0800_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-10mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau010000um_M1200_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-10mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau010000um_M1600_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-10mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau010000um_M3000_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-10mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 97999),
    MCSample('mfv_neu_tau030000um_M0400_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-30mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau030000um_M0600_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-30mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau030000um_M0800_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-30mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau030000um_M1200_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-30mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau030000um_M1600_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-30mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_neu_tau030000um_M3000_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-30mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 99999),
    ]

mfv_stopdbardbar_samples_2017 = [
    MCSample('mfv_stopdbardbar_tau000100um_M0400_2017', '/StopStopbarTo2Dbar2D_M-400_CTau-100um_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau000100um_M0600_2017', '/StopStopbarTo2Dbar2D_M-600_CTau-100um_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 96000),
    MCSample('mfv_stopdbardbar_tau000100um_M0800_2017', '/StopStopbarTo2Dbar2D_M-800_CTau-100um_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau000100um_M1200_2017', '/StopStopbarTo2Dbar2D_M-1200_CTau-100um_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau000100um_M1600_2017', '/StopStopbarTo2Dbar2D_M-1600_CTau-100um_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau000100um_M3000_2017', '/StopStopbarTo2Dbar2D_M-3000_CTau-100um_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 95000),
    MCSample('mfv_stopdbardbar_tau000300um_M0400_2017', '/StopStopbarTo2Dbar2D_M-400_CTau-300um_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau000300um_M0600_2017', '/StopStopbarTo2Dbar2D_M-600_CTau-300um_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau000300um_M0800_2017', '/StopStopbarTo2Dbar2D_M-800_CTau-300um_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau000300um_M1200_2017', '/StopStopbarTo2Dbar2D_M-1200_CTau-300um_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau000300um_M1600_2017', '/StopStopbarTo2Dbar2D_M-1600_CTau-300um_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau000300um_M3000_2017', '/StopStopbarTo2Dbar2D_M-3000_CTau-300um_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau001000um_M0400_2017', '/StopStopbarTo2Dbar2D_M-400_CTau-1mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau001000um_M0600_2017', '/StopStopbarTo2Dbar2D_M-600_CTau-1mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 97000),
    MCSample('mfv_stopdbardbar_tau001000um_M0800_2017', '/StopStopbarTo2Dbar2D_M-800_CTau-1mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau001000um_M1200_2017', '/StopStopbarTo2Dbar2D_M-1200_CTau-1mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 99000),
    MCSample('mfv_stopdbardbar_tau001000um_M1600_2017', '/StopStopbarTo2Dbar2D_M-1600_CTau-1mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau001000um_M3000_2017', '/StopStopbarTo2Dbar2D_M-3000_CTau-1mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau010000um_M0400_2017', '/StopStopbarTo2Dbar2D_M-400_CTau-10mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau010000um_M0600_2017', '/StopStopbarTo2Dbar2D_M-600_CTau-10mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau010000um_M0800_2017', '/StopStopbarTo2Dbar2D_M-800_CTau-10mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 98000),
    MCSample('mfv_stopdbardbar_tau010000um_M1200_2017', '/StopStopbarTo2Dbar2D_M-1200_CTau-10mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau010000um_M1600_2017', '/StopStopbarTo2Dbar2D_M-1600_CTau-10mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau010000um_M3000_2017', '/StopStopbarTo2Dbar2D_M-3000_CTau-10mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau030000um_M0400_2017', '/StopStopbarTo2Dbar2D_M-400_CTau-30mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau030000um_M0600_2017', '/StopStopbarTo2Dbar2D_M-600_CTau-30mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau030000um_M0800_2017', '/StopStopbarTo2Dbar2D_M-800_CTau-30mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau030000um_M1200_2017', '/StopStopbarTo2Dbar2D_M-1200_CTau-30mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 98000),
    MCSample('mfv_stopdbardbar_tau030000um_M1600_2017', '/StopStopbarTo2Dbar2D_M-1600_CTau-30mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau030000um_M3000_2017', '/StopStopbarTo2Dbar2D_M-3000_CTau-30mm_TuneCP2_13TeV-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM', 100000),
    ]

all_signal_samples_2017 = mfv_signal_samples_2017 + mfv_stopdbardbar_samples_2017

for s in all_signal_samples_2017:
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

bjet_samples_2018 = [
    MCSample('qcdht0300_2018', '/QCD_HT300to500_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 55094256, nice='QCD, 300 < H_{T} < 500 GeV',  color=803, syst_frac=0.20, xsec=3.226e5),
    MCSample('qcdht0500_2018', '/QCD_HT500to700_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM', 55195716, nice='QCD, 500 < H_{T} < 700 GeV',  color=804, syst_frac=0.20, xsec=2.998e4),
    MCSample('ttbar_2018',     '/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15_ext1-v2/AODSIM',  145295353, nice='t#bar{t}', color=4, syst_frac=0.15, xsec=832.),
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

mfv_splitSUSY_samples_M2000_2017 = [
  MCSample('mfv_splitSUSY_tau000000000um_M2000_1800_2017', '/mfv_splitSUSY_tau000000000um_M2000_1800_2017/None/USER', 10000),
  MCSample('mfv_splitSUSY_tau100000000um_M2000_1800_2017', '/mfv_splitSUSY_tau100000000um_M2000_1800_2017/None/USER', 10000),
  MCSample('mfv_splitSUSY_tau010000000um_M2000_1800_2017', '/mfv_splitSUSY_tau010000000um_M2000_1800_2017/None/USER', 10000),
  MCSample('mfv_splitSUSY_tau001000000um_M2000_1800_2017', '/mfv_splitSUSY_tau001000000um_M2000_1800_2017/None/USER', 10000),
  MCSample('mfv_splitSUSY_tau000100000um_M2000_1800_2017', '/mfv_splitSUSY_tau000100000um_M2000_1800_2017/None/USER', 10000),
  MCSample('mfv_splitSUSY_tau000010000um_M2000_1800_2017', '/mfv_splitSUSY_tau000010000um_M2000_1800_2017/None/USER', 10000),
  MCSample('mfv_splitSUSY_tau000001000um_M2000_1800_2017', '/mfv_splitSUSY_tau000001000um_M2000_1800_2017/None/USER', 10000),
  MCSample('mfv_splitSUSY_tau000000000um_M2000_1900_2017', '/mfv_splitSUSY_tau000000000um_M2000_1900_2017/None/USER', 10000),
  MCSample('mfv_splitSUSY_tau100000000um_M2000_1900_2017', '/mfv_splitSUSY_tau100000000um_M2000_1900_2017/None/USER', 10000),
  MCSample('mfv_splitSUSY_tau010000000um_M2000_1900_2017', '/mfv_splitSUSY_tau010000000um_M2000_1900_2017/None/USER', 10000),
  MCSample('mfv_splitSUSY_tau001000000um_M2000_1900_2017', '/mfv_splitSUSY_tau001000000um_M2000_1900_2017/None/USER', 10000),
  MCSample('mfv_splitSUSY_tau000100000um_M2000_1900_2017', '/mfv_splitSUSY_tau000100000um_M2000_1900_2017/None/USER', 10000),
  MCSample('mfv_splitSUSY_tau000010000um_M2000_1900_2017', '/mfv_splitSUSY_tau000010000um_M2000_1900_2017/None/USER', 10000),
  MCSample('mfv_splitSUSY_tau000001000um_M2000_1900_2017', '/mfv_splitSUSY_tau000001000um_M2000_1900_2017/None/USER', 10000),

]

mfv_splitSUSY_samples_M2400_2017 = [
  MCSample('mfv_splitSUSY_tau000000000um_M2400_100_2017', '/mfv_splitSUSY_tau000000000um_M2400_100_2017/None/USER', 10000),
  MCSample('mfv_splitSUSY_tau100000000um_M2400_100_2017', '/mfv_splitSUSY_tau100000000um_M2400_100_2017/None/USER', 10000),
  MCSample('mfv_splitSUSY_tau010000000um_M2400_100_2017', '/mfv_splitSUSY_tau010000000um_M2400_100_2017/None/USER', 10000),
  MCSample('mfv_splitSUSY_tau001000000um_M2400_100_2017', '/mfv_splitSUSY_tau001000000um_M2400_100_2017/None/USER', 10000),
  MCSample('mfv_splitSUSY_tau000100000um_M2400_100_2017', '/mfv_splitSUSY_tau000100000um_M2400_100_2017/None/USER', 10000),
  MCSample('mfv_splitSUSY_tau000010000um_M2400_100_2017', '/mfv_splitSUSY_tau000010000um_M2400_100_2017/None/USER', 10000),
  MCSample('mfv_splitSUSY_tau000001000um_M2400_100_2017', '/mfv_splitSUSY_tau000001000um_M2400_100_2017/None/USER', 10000),
  MCSample('mfv_splitSUSY_tau000000000um_M2400_2300_2017', '/mfv_splitSUSY_tau000000000um_M2400_2300_2017/None/USER', 10000),
  MCSample('mfv_splitSUSY_tau100000000um_M2400_2300_2017', '/mfv_splitSUSY_tau100000000um_M2400_2300_2017/None/USER', 10000),
  MCSample('mfv_splitSUSY_tau010000000um_M2400_2300_2017', '/mfv_splitSUSY_tau010000000um_M2400_2300_2017/None/USER', 10000),
  MCSample('mfv_splitSUSY_tau001000000um_M2400_2300_2017', '/mfv_splitSUSY_tau001000000um_M2400_2300_2017/None/USER', 10000),
  MCSample('mfv_splitSUSY_tau000100000um_M2400_2300_2017', '/mfv_splitSUSY_tau000100000um_M2400_2300_2017/None/USER', 10000),
  MCSample('mfv_splitSUSY_tau000010000um_M2400_2300_2017', '/mfv_splitSUSY_tau000010000um_M2400_2300_2017/None/USER', 10000),
  MCSample('mfv_splitSUSY_tau000001000um_M2400_2300_2017', '/mfv_splitSUSY_tau000001000um_M2400_2300_2017/None/USER', 10000),

]

mfv_splitSUSY_samples_2017 = mfv_splitSUSY_samples_M2000_2017 + mfv_splitSUSY_samples_M2400_2017

for s in mfv_splitSUSY_samples_2017:
    _set_signal_stuff(s)

splitSUSY_samples_2017 = mfv_splitSUSY_samples_2017


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
    'bjet_samples_2017',
    'leptonic_samples_2017',
    'leptonic_samples_sum_2017',
    'Zvv_samples_2017',
    'mfv_signal_samples_2017',
    'mfv_stopdbardbar_samples_2017',
    'qcd_samples_2018',
    'ttbar_samples_2018',
    'bjet_samples_2018',
    'mfv_signal_samples_2018',
    'mfv_stopdbardbar_samples_2018',
    'mfv_splitSUSY_samples_2017',
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

span_signal_samples_2017 = [eval('mfv_%s_tau%06ium_M%04i_2017' % (a,b,c)) for a in ('neu','stopdbardbar') for b in (300,1000,10000) for c in (800,1600,3000)]
span_signal_samples_2018 = [eval('mfv_%s_tau%06ium_M%04i_2018' % (a,b,c)) for a in ('neu','stopdbardbar') for b in (300,1000,10000) for c in (800,1600,3000)]

_alls = [
    'all_signal_samples_2017',
    'all_signal_samples_2018',
    'span_signal_samples_2017',
    'span_signal_samples_2018',
    ]
__all__ += _alls
for x in _alls:
    registry.add_list(x, eval(x))

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

_adbp('miniaod', '/QCD_HT200to300_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v2/MINIAODSIM', 59427619)
_adbp('miniaod', '/QCD_HT300to500_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1/MINIAODSIM',   59569132)
_adbp('miniaod', '/QCD_HT500to700_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM',           56207744)
_adbp('miniaod', '/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',          47724800)
_adbp('miniaod', '/QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1/MINIAODSIM', 16882838)
_adbp('miniaod', '/QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM',         11634434)
_adbp('miniaod', '/QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM',           5941306)
ttbar_2017.add_dataset('miniaod', '/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1/MINIAODSIM',      154280331)
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
ttHbb_2017.add_dataset('miniaod', '/ttHJetTobb_M125_TuneCP5_13TeV_amcatnloFXFX_madspin_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1/MINIAODSIM', 10055168)
ttZ_2017.add_dataset('miniaod', '/ttZJets_TuneCP5_13TeV_madgraphMLM_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 9698473)
ttZext_2017.add_dataset('miniaod', '/ttZJets_TuneCP5_13TeV_madgraphMLM_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14_ext1-v3/MINIAODSIM', 8536618)
singletop_tchan_top_2017.add_dataset('miniaod', '/ST_t-channel_top_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1/MINIAODSIM', 5982064)
singletop_tchan_antitop_2017.add_dataset('miniaod', '/ST_t-channel_antitop_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 3675910)

zjetstonunuht0100_2017.add_dataset('miniaod', '/ZJetsToNuNu_HT-100To200_13TeV-madgraph/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 22737266)
zjetstonunuht0200_2017.add_dataset('miniaod', '/ZJetsToNuNu_HT-200To400_13TeV-madgraph/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 21675916)
zjetstonunuht0400_2017.add_dataset('miniaod', '/ZJetsToNuNu_HT-400To600_13TeV-madgraph/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 9134120)
zjetstonunuht0600_2017.add_dataset('miniaod', '/ZJetsToNuNu_HT-600To800_13TeV-madgraph/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 5697594)
zjetstonunuht0800_2017.add_dataset('miniaod', '/ZJetsToNuNu_HT-800To1200_13TeV-madgraph/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 2058077)
zjetstonunuht1200_2017.add_dataset('miniaod', '/ZJetsToNuNu_HT-1200To2500_13TeV-madgraph/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 338948)
zjetstonunuht2500_2017.add_dataset('miniaod', '/ZJetsToNuNu_HT-2500ToInf_13TeV-madgraph/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 6734)



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
_adbp('miniaod', '/QCD_HT300to500_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM',   54661579)
_adbp('miniaod', '/QCD_HT500to700_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM',   55152960)
_adbp('miniaod', '/QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM',  43523821)
_adbp('miniaod', '/QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 15065049)
_adbp('miniaod', '/QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 10955087)
_adbp('miniaod', '/QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM',   5475677)
ttbar_2018.add_dataset('miniaod', '/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15_ext1-v2/MINIAODSIM', 142155064)
ttbarht0600_2018.add_dataset('miniaod', '/TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM',  14149394)
ttbarht0800_2018.add_dataset('miniaod', '/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 10372802)
ttbarht1200_2018.add_dataset('miniaod', '/TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 2779427)
ttbarht2500_2018.add_dataset('miniaod', '/TTJets_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM',  1451104)

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

_adbp('miniaod', '/mfv_splitSUSY_tau000000000um_M2000_1800_2017/None/USER', 10000)
_adbp('miniaod', '/mfv_splitSUSY_tau100000000um_M2000_1800_2017/None/USER', 10000)
_adbp('miniaod', '/mfv_splitSUSY_tau010000000um_M2000_1800_2017/None/USER', 10000)
_adbp('miniaod', '/mfv_splitSUSY_tau001000000um_M2000_1800_2017/None/USER', 10000)
_adbp('miniaod', '/mfv_splitSUSY_tau000100000um_M2000_1800_2017/None/USER', 10000)
_adbp('miniaod', '/mfv_splitSUSY_tau000010000um_M2000_1800_2017/None/USER', 10000)
_adbp('miniaod', '/mfv_splitSUSY_tau000001000um_M2000_1800_2017/None/USER', 10000)
_adbp('miniaod', '/mfv_splitSUSY_tau000000000um_M2000_1900_2017/None/USER', 10000)
_adbp('miniaod', '/mfv_splitSUSY_tau100000000um_M2000_1900_2017/None/USER', 10000)
_adbp('miniaod', '/mfv_splitSUSY_tau010000000um_M2000_1900_2017/None/USER', 10000)
_adbp('miniaod', '/mfv_splitSUSY_tau001000000um_M2000_1900_2017/None/USER', 10000)
_adbp('miniaod', '/mfv_splitSUSY_tau000100000um_M2000_1900_2017/None/USER', 10000)
_adbp('miniaod', '/mfv_splitSUSY_tau000010000um_M2000_1900_2017/None/USER', 10000)
_adbp('miniaod', '/mfv_splitSUSY_tau000001000um_M2000_1900_2017/None/USER', 10000)

_adbp('miniaod', '/mfv_splitSUSY_tau000000000um_M2400_100_2017/None/USER', 10000)
_adbp('miniaod', '/mfv_splitSUSY_tau100000000um_M2400_100_2017/None/USER', 10000)
_adbp('miniaod', '/mfv_splitSUSY_tau010000000um_M2400_100_2017/None/USER', 10000)
_adbp('miniaod', '/mfv_splitSUSY_tau001000000um_M2400_100_2017/None/USER', 10000)
_adbp('miniaod', '/mfv_splitSUSY_tau000100000um_M2400_100_2017/None/USER', 10000)
_adbp('miniaod', '/mfv_splitSUSY_tau000010000um_M2400_100_2017/None/USER', 10000)
_adbp('miniaod', '/mfv_splitSUSY_tau000001000um_M2400_100_2017/None/USER', 10000)
_adbp('miniaod', '/mfv_splitSUSY_tau000000000um_M2400_2300_2017/None/USER', 10000)
_adbp('miniaod', '/mfv_splitSUSY_tau100000000um_M2400_2300_2017/None/USER', 10000)
_adbp('miniaod', '/mfv_splitSUSY_tau010000000um_M2400_2300_2017/None/USER', 10000)
_adbp('miniaod', '/mfv_splitSUSY_tau001000000um_M2400_2300_2017/None/USER', 10000)
_adbp('miniaod', '/mfv_splitSUSY_tau000100000um_M2400_2300_2017/None/USER', 10000)
_adbp('miniaod', '/mfv_splitSUSY_tau000010000um_M2400_2300_2017/None/USER', 10000)
_adbp('miniaod', '/mfv_splitSUSY_tau000001000um_M2400_2300_2017/None/USER', 10000)


########
# ntuples
########

for x in data_samples_2017 + qcd_samples_2017 + data_samples_2018 + qcd_samples_2018:
    x.add_dataset("nr_trackingtreerv23mv3")
    x.add_dataset("nr_k0ntuplev25mv1")

for x in data_samples_2017 + qcd_samples_2017 + ttbar_samples_2017 + all_signal_samples_2017 + \
         data_samples_2018 + qcd_samples_2018 + ttbar_samples_2018 + all_signal_samples_2018:
    x.add_dataset("ntuplev27m")
    if not x.is_signal:
        x.add_dataset("ntuplev27m_ntkseeds")
        x.add_dataset("ntuplev27m_norefitdzcut")
        x.add_dataset("nr_trackmoverv27mv1")
        x.add_dataset("nr_trackmoverv27mv1_norefitdzcut")
mfv_neu_tau010000um_M0800_2017.add_dataset('ntuplev27m_norefitdzcut')

for x in all_signal_samples_2017 + all_signal_samples_2018:
    x.add_dataset("ntuplev27m_norescaling")
    if x not in (mfv_stopdbardbar_tau001000um_M0800_2018, mfv_neu_tau001000um_M1600_2018):
        x.add_dataset("ntuplev27m_wgen")

for x in all_signal_samples_2017 + all_signal_samples_2018:
    x.add_dataset("nr_trackmovermctruthv27mv1")
    x.add_dataset("nr_trackmovermctruthv27mv1_norefitdzcut")
    x.add_dataset("nr_trackmovermctruthv27mv2")

singletop_tchan_top_2017.add_dataset('ntuplev28bm', '/ST_t-channel_top_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8/jreicher-NtupleV28Bm_2017-283eecf66b16e33c5d0ced53996ceea7/USER', 4336)
singletop_tchan_antitop_2017.add_dataset('ntuplev28bm', '/ST_t-channel_antitop_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8/jreicher-NtupleV28Bm_2017-f3c243cb29cdedee385e0375ca43ddd0/USER', 2653)
for x in qcdht0700_2017, qcdht1000_2017, qcdht1500_2017, qcdht2000_2017, qcdht0300_2017, qcdht0500_2017, ttbar_2017, ttHbb_2017, ttZ_2017, ttZext_2017, mfv_neu_tau000100um_M0400_2017, mfv_neu_tau000100um_M0600_2017, mfv_neu_tau000100um_M0800_2017, mfv_neu_tau000100um_M1200_2017, mfv_neu_tau000100um_M1600_2017, mfv_neu_tau000100um_M3000_2017, mfv_neu_tau000300um_M0400_2017, mfv_neu_tau000300um_M0600_2017, mfv_neu_tau000300um_M0800_2017, mfv_neu_tau000300um_M1200_2017, mfv_neu_tau000300um_M1600_2017, mfv_neu_tau000300um_M3000_2017, mfv_neu_tau001000um_M0400_2017, mfv_neu_tau001000um_M0600_2017, mfv_neu_tau001000um_M0800_2017, mfv_neu_tau001000um_M1200_2017, mfv_neu_tau001000um_M1600_2017, mfv_neu_tau001000um_M3000_2017, mfv_neu_tau010000um_M0400_2017, mfv_neu_tau010000um_M0600_2017, mfv_neu_tau010000um_M0800_2017, mfv_neu_tau010000um_M1200_2017, mfv_neu_tau010000um_M1600_2017, mfv_neu_tau010000um_M3000_2017, mfv_neu_tau030000um_M0400_2017, mfv_neu_tau030000um_M0600_2017, mfv_neu_tau030000um_M0800_2017, mfv_neu_tau030000um_M1200_2017, mfv_neu_tau030000um_M1600_2017, mfv_neu_tau030000um_M3000_2017, mfv_stopdbardbar_tau000100um_M0400_2017, mfv_stopdbardbar_tau000100um_M0600_2017, mfv_stopdbardbar_tau000100um_M0800_2017, mfv_stopdbardbar_tau000100um_M1200_2017, mfv_stopdbardbar_tau000100um_M1600_2017, mfv_stopdbardbar_tau000100um_M3000_2017, mfv_stopdbardbar_tau000300um_M0400_2017, mfv_stopdbardbar_tau000300um_M0600_2017, mfv_stopdbardbar_tau000300um_M0800_2017, mfv_stopdbardbar_tau000300um_M1200_2017, mfv_stopdbardbar_tau000300um_M1600_2017, mfv_stopdbardbar_tau000300um_M3000_2017, mfv_stopdbardbar_tau001000um_M0400_2017, mfv_stopdbardbar_tau001000um_M0600_2017, mfv_stopdbardbar_tau001000um_M0800_2017, mfv_stopdbardbar_tau001000um_M1200_2017, mfv_stopdbardbar_tau001000um_M1600_2017, mfv_stopdbardbar_tau001000um_M3000_2017, mfv_stopdbardbar_tau010000um_M0400_2017, mfv_stopdbardbar_tau010000um_M0600_2017, mfv_stopdbardbar_tau010000um_M0800_2017, mfv_stopdbardbar_tau010000um_M1200_2017, mfv_stopdbardbar_tau010000um_M1600_2017, mfv_stopdbardbar_tau010000um_M3000_2017, mfv_stopdbardbar_tau030000um_M0400_2017, mfv_stopdbardbar_tau030000um_M0600_2017, mfv_stopdbardbar_tau030000um_M0800_2017, mfv_stopdbardbar_tau030000um_M1200_2017, mfv_stopdbardbar_tau030000um_M1600_2017, mfv_stopdbardbar_tau030000um_M3000_2017:
    x.add_dataset("ntuplev28bm")

singletop_tchan_top_2017.add_dataset('ntuplev28bm_ntkseeds', '/ST_t-channel_top_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8/jreicher-NtupleV28Bm_NTkSeeds_2017-4fd43c30c720063db8c53a24e852c239/USER', 6619)
singletop_tchan_antitop_2017.add_dataset('ntuplev28bm_ntkseeds', '/ST_t-channel_antitop_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8/jreicher-NtupleV28Bm_NTkSeeds_2017-c23d1a276623eee9668ca7711bbfadef/USER', 2731)
for x in qcdht0700_2017, qcdht1000_2017, qcdht1500_2017, qcdht2000_2017, qcdht0300_2017, qcdht0500_2017, ttbar_2017, ttHbb_2017, ttZ_2017, ttZext_2017:
    x.add_dataset("ntuplev28bm_ntkseeds")


for x in mfv_splitSUSY_tau000000000um_M2000_1800_2017, mfv_splitSUSY_tau100000000um_M2000_1800_2017, mfv_splitSUSY_tau010000000um_M2000_1800_2017, mfv_splitSUSY_tau001000000um_M2000_1800_2017, mfv_splitSUSY_tau000100000um_M2000_1800_2017, mfv_splitSUSY_tau000010000um_M2000_1800_2017, mfv_splitSUSY_tau000001000um_M2000_1800_2017, mfv_splitSUSY_tau000000000um_M2000_1900_2017, mfv_splitSUSY_tau100000000um_M2000_1900_2017, mfv_splitSUSY_tau010000000um_M2000_1900_2017, mfv_splitSUSY_tau001000000um_M2000_1900_2017, mfv_splitSUSY_tau000100000um_M2000_1900_2017, mfv_splitSUSY_tau000010000um_M2000_1900_2017, mfv_splitSUSY_tau000001000um_M2000_1900_2017, mfv_splitSUSY_tau000000000um_M2400_100_2017, mfv_splitSUSY_tau100000000um_M2400_100_2017, mfv_splitSUSY_tau010000000um_M2400_100_2017, mfv_splitSUSY_tau001000000um_M2400_100_2017, mfv_splitSUSY_tau000100000um_M2400_100_2017, mfv_splitSUSY_tau000010000um_M2400_100_2017, mfv_splitSUSY_tau000001000um_M2400_100_2017, mfv_splitSUSY_tau000000000um_M2400_2300_2017, mfv_splitSUSY_tau100000000um_M2400_2300_2017, mfv_splitSUSY_tau010000000um_M2400_2300_2017, mfv_splitSUSY_tau001000000um_M2400_2300_2017, mfv_splitSUSY_tau000100000um_M2400_2300_2017, mfv_splitSUSY_tau000010000um_M2400_2300_2017, mfv_splitSUSY_tau000001000um_M2400_2300_2017:
    x.add_dataset("ntuplev29metm")

for x in mfv_splitSUSY_tau000000000um_M2000_1800_2017, mfv_splitSUSY_tau100000000um_M2000_1800_2017, mfv_splitSUSY_tau010000000um_M2000_1800_2017, mfv_splitSUSY_tau001000000um_M2000_1800_2017, mfv_splitSUSY_tau000100000um_M2000_1800_2017, mfv_splitSUSY_tau000010000um_M2000_1800_2017, mfv_splitSUSY_tau000001000um_M2000_1800_2017, mfv_splitSUSY_tau000000000um_M2000_1900_2017, mfv_splitSUSY_tau100000000um_M2000_1900_2017, mfv_splitSUSY_tau010000000um_M2000_1900_2017, mfv_splitSUSY_tau001000000um_M2000_1900_2017, mfv_splitSUSY_tau000100000um_M2000_1900_2017, mfv_splitSUSY_tau000010000um_M2000_1900_2017, mfv_splitSUSY_tau000001000um_M2000_1900_2017, mfv_splitSUSY_tau000000000um_M2400_100_2017, mfv_splitSUSY_tau100000000um_M2400_100_2017, mfv_splitSUSY_tau010000000um_M2400_100_2017, mfv_splitSUSY_tau001000000um_M2400_100_2017, mfv_splitSUSY_tau000100000um_M2400_100_2017, mfv_splitSUSY_tau000010000um_M2400_100_2017, mfv_splitSUSY_tau000001000um_M2400_100_2017, mfv_splitSUSY_tau000000000um_M2400_2300_2017, mfv_splitSUSY_tau100000000um_M2400_2300_2017, mfv_splitSUSY_tau010000000um_M2400_2300_2017, mfv_splitSUSY_tau001000000um_M2400_2300_2017, mfv_splitSUSY_tau000100000um_M2400_2300_2017, mfv_splitSUSY_tau000010000um_M2400_2300_2017, mfv_splitSUSY_tau000001000um_M2400_2300_2017:
    x.add_dataset("ntuplev30m")

for x in qcdht0700_2017, qcdht1000_2017, qcdht1500_2017, qcdht2000_2017, ttbarht0600_2017, ttbarht0800_2017, ttbarht1200_2017, ttbarht2500_2017, mfv_splitSUSY_tau000000000um_M2000_1800_2017, mfv_splitSUSY_tau100000000um_M2000_1800_2017, mfv_splitSUSY_tau010000000um_M2000_1800_2017, mfv_splitSUSY_tau001000000um_M2000_1800_2017, mfv_splitSUSY_tau000100000um_M2000_1800_2017, mfv_splitSUSY_tau000010000um_M2000_1800_2017, mfv_splitSUSY_tau000001000um_M2000_1800_2017, mfv_splitSUSY_tau000000000um_M2000_1900_2017, mfv_splitSUSY_tau100000000um_M2000_1900_2017, mfv_splitSUSY_tau010000000um_M2000_1900_2017, mfv_splitSUSY_tau001000000um_M2000_1900_2017, mfv_splitSUSY_tau000100000um_M2000_1900_2017, mfv_splitSUSY_tau000010000um_M2000_1900_2017, mfv_splitSUSY_tau000001000um_M2000_1900_2017, mfv_splitSUSY_tau000000000um_M2400_100_2017, mfv_splitSUSY_tau100000000um_M2400_100_2017, mfv_splitSUSY_tau010000000um_M2400_100_2017, mfv_splitSUSY_tau001000000um_M2400_100_2017, mfv_splitSUSY_tau000100000um_M2400_100_2017, mfv_splitSUSY_tau000010000um_M2400_100_2017, mfv_splitSUSY_tau000001000um_M2400_100_2017, mfv_splitSUSY_tau000000000um_M2400_2300_2017, mfv_splitSUSY_tau100000000um_M2400_2300_2017, mfv_splitSUSY_tau010000000um_M2400_2300_2017, mfv_splitSUSY_tau001000000um_M2400_2300_2017, mfv_splitSUSY_tau000100000um_M2400_2300_2017, mfv_splitSUSY_tau000010000um_M2400_2300_2017, mfv_splitSUSY_tau000001000um_M2400_2300_2017:
    x.add_dataset("ntuplev32m")

for x in qcdht0700_2017, qcdht1000_2017, qcdht1500_2017, qcdht2000_2017, ttbarht0600_2017, ttbarht0800_2017, ttbarht1200_2017, ttbarht2500_2017, mfv_splitSUSY_tau000000000um_M2000_1800_2017, mfv_splitSUSY_tau100000000um_M2000_1800_2017, mfv_splitSUSY_tau010000000um_M2000_1800_2017, mfv_splitSUSY_tau001000000um_M2000_1800_2017, mfv_splitSUSY_tau000100000um_M2000_1800_2017, mfv_splitSUSY_tau000010000um_M2000_1800_2017, mfv_splitSUSY_tau000001000um_M2000_1800_2017, mfv_splitSUSY_tau000000000um_M2000_1900_2017, mfv_splitSUSY_tau100000000um_M2000_1900_2017, mfv_splitSUSY_tau010000000um_M2000_1900_2017, mfv_splitSUSY_tau001000000um_M2000_1900_2017, mfv_splitSUSY_tau000100000um_M2000_1900_2017, mfv_splitSUSY_tau000010000um_M2000_1900_2017, mfv_splitSUSY_tau000001000um_M2000_1900_2017, mfv_splitSUSY_tau000000000um_M2400_100_2017, mfv_splitSUSY_tau100000000um_M2400_100_2017, mfv_splitSUSY_tau010000000um_M2400_100_2017, mfv_splitSUSY_tau001000000um_M2400_100_2017, mfv_splitSUSY_tau000100000um_M2400_100_2017, mfv_splitSUSY_tau000010000um_M2400_100_2017, mfv_splitSUSY_tau000001000um_M2400_100_2017, mfv_splitSUSY_tau000000000um_M2400_2300_2017, mfv_splitSUSY_tau100000000um_M2400_2300_2017, mfv_splitSUSY_tau010000000um_M2400_2300_2017, mfv_splitSUSY_tau001000000um_M2400_2300_2017, mfv_splitSUSY_tau000100000um_M2400_2300_2017, mfv_splitSUSY_tau000010000um_M2400_2300_2017, mfv_splitSUSY_tau000001000um_M2400_2300_2017:
    x.add_dataset("ntuplev33metm")


########
# automatic condor declarations for ntuples
########

for s in registry.all():
    for ds in s.datasets.keys():
        for ds4 in 'ntuple', 'nr_':
            if ds.startswith(ds4):
                s.datasets[ds].condor = True
                s.datasets[ds].xrootd_url = xrootd_sites['T3_US_FNALLPC']

########
# other condor declarations, generate condorable dict with Shed/condor_list.py
########

condorable = {
    "T3_US_FNALLPC": {
        "miniaod": ttbar_samples_2017 + [qcdht1000_2017, qcdht1500_2018, qcdht2000_2018, ttbarht0600_2018, ttbarht1200_2018, ttbarht2500_2018,
                                         mfv_neu_tau000100um_M0400_2017, mfv_neu_tau000100um_M0800_2017, mfv_neu_tau000100um_M1200_2017, mfv_neu_tau000100um_M1600_2017, mfv_neu_tau000100um_M3000_2017, mfv_neu_tau000300um_M0600_2017, mfv_neu_tau000300um_M1200_2017, mfv_neu_tau000300um_M1600_2017, mfv_neu_tau001000um_M0400_2017, mfv_neu_tau001000um_M0600_2017, mfv_neu_tau001000um_M0800_2017, mfv_neu_tau001000um_M1200_2017, mfv_neu_tau001000um_M1600_2017, mfv_neu_tau001000um_M3000_2017, mfv_neu_tau010000um_M0600_2017, mfv_neu_tau010000um_M1200_2017, mfv_neu_tau010000um_M3000_2017, mfv_neu_tau030000um_M0400_2017, mfv_neu_tau030000um_M0600_2017, mfv_neu_tau030000um_M1200_2017, mfv_stopdbardbar_tau000100um_M0400_2017, mfv_stopdbardbar_tau000100um_M0800_2017, mfv_stopdbardbar_tau000100um_M3000_2017, mfv_stopdbardbar_tau000300um_M0400_2017, mfv_stopdbardbar_tau000300um_M0800_2017, mfv_stopdbardbar_tau000300um_M1600_2017, mfv_stopdbardbar_tau000300um_M3000_2017, mfv_stopdbardbar_tau001000um_M0600_2017, mfv_stopdbardbar_tau001000um_M0800_2017, mfv_stopdbardbar_tau001000um_M1600_2017, mfv_stopdbardbar_tau010000um_M0400_2017, mfv_stopdbardbar_tau010000um_M0600_2017, mfv_stopdbardbar_tau010000um_M1200_2017, mfv_stopdbardbar_tau010000um_M1600_2017, mfv_stopdbardbar_tau030000um_M0400_2017, mfv_stopdbardbar_tau030000um_M0600_2017, mfv_stopdbardbar_tau030000um_M0800_2017, mfv_stopdbardbar_tau030000um_M3000_2017,
                                         mfv_neu_tau000100um_M0400_2018, mfv_neu_tau000100um_M0600_2018, mfv_neu_tau000100um_M0800_2018, mfv_neu_tau000100um_M1200_2018, mfv_neu_tau000100um_M1600_2018, mfv_neu_tau000100um_M3000_2018, mfv_neu_tau000300um_M0400_2018, mfv_neu_tau000300um_M0600_2018, mfv_neu_tau000300um_M0800_2018, mfv_neu_tau000300um_M1200_2018, mfv_neu_tau000300um_M1600_2018, mfv_neu_tau000300um_M3000_2018, mfv_neu_tau001000um_M0400_2018, mfv_neu_tau001000um_M0600_2018, mfv_neu_tau001000um_M1200_2018, mfv_neu_tau001000um_M1600_2018, mfv_neu_tau001000um_M3000_2018, mfv_neu_tau010000um_M0400_2018, mfv_neu_tau010000um_M0600_2018, mfv_neu_tau010000um_M0800_2018, mfv_neu_tau010000um_M1200_2018, mfv_neu_tau010000um_M1600_2018, mfv_neu_tau010000um_M3000_2018, mfv_neu_tau030000um_M0400_2018, mfv_neu_tau030000um_M0600_2018, mfv_neu_tau030000um_M0800_2018, mfv_neu_tau030000um_M1200_2018, mfv_neu_tau030000um_M1600_2018, mfv_neu_tau030000um_M3000_2018, mfv_stopdbardbar_tau000100um_M0400_2018, mfv_stopdbardbar_tau000100um_M0600_2018, mfv_stopdbardbar_tau000100um_M0800_2018, mfv_stopdbardbar_tau000100um_M1200_2018, mfv_stopdbardbar_tau000100um_M3000_2018, mfv_stopdbardbar_tau000300um_M0600_2018, mfv_stopdbardbar_tau000300um_M0800_2018, mfv_stopdbardbar_tau000300um_M1200_2018, mfv_stopdbardbar_tau000300um_M3000_2018, mfv_stopdbardbar_tau001000um_M0400_2018, mfv_stopdbardbar_tau001000um_M0600_2018, mfv_stopdbardbar_tau001000um_M0800_2018, mfv_stopdbardbar_tau001000um_M1200_2018, mfv_stopdbardbar_tau001000um_M1600_2018, mfv_stopdbardbar_tau001000um_M3000_2018, mfv_stopdbardbar_tau010000um_M0400_2018, mfv_stopdbardbar_tau010000um_M0600_2018, mfv_stopdbardbar_tau010000um_M0800_2018, mfv_stopdbardbar_tau010000um_M1600_2018, mfv_stopdbardbar_tau030000um_M0400_2018, mfv_stopdbardbar_tau030000um_M0600_2018, mfv_stopdbardbar_tau030000um_M0800_2018, mfv_stopdbardbar_tau030000um_M1200_2018, mfv_stopdbardbar_tau030000um_M3000_2018],
        },
    "T1_US_FNAL_Disk": {
        "miniaod": [qcdht0200_2017, zjetstonunuht0200_2017, zjetstonunuht1200_2017, qcdht1500_2017, qcdht2000_2017, dyjetstollM10_2017, qcdmupt15_2017, qcdht0300_2018, qcdht0700_2018, ttbarht0800_2018,
                    JetHT2017B, JetHT2017D, JetHT2017F, JetHT2018A, JetHT2018B, JetHT2018D,
                    mfv_neu_tau000100um_M0600_2017, mfv_neu_tau000300um_M0400_2017, mfv_neu_tau000300um_M0800_2017, mfv_neu_tau000300um_M3000_2017, mfv_neu_tau010000um_M0400_2017, mfv_neu_tau010000um_M0800_2017, mfv_neu_tau010000um_M1600_2017, mfv_neu_tau030000um_M0800_2017, mfv_neu_tau030000um_M3000_2017, mfv_stopdbardbar_tau000100um_M0600_2017, mfv_stopdbardbar_tau000100um_M1600_2017, mfv_stopdbardbar_tau000300um_M1200_2017, mfv_stopdbardbar_tau001000um_M0400_2017, mfv_stopdbardbar_tau001000um_M1200_2017, mfv_stopdbardbar_tau001000um_M3000_2017, mfv_stopdbardbar_tau010000um_M0800_2017, mfv_stopdbardbar_tau010000um_M3000_2017, mfv_stopdbardbar_tau030000um_M1200_2017, mfv_stopdbardbar_tau030000um_M1600_2017,
                    mfv_neu_tau001000um_M0800_2018, mfv_stopdbardbar_tau000100um_M1600_2018, mfv_stopdbardbar_tau000300um_M0400_2018, mfv_stopdbardbar_tau000300um_M1600_2018, mfv_stopdbardbar_tau010000um_M1200_2018, mfv_stopdbardbar_tau010000um_M3000_2018, mfv_stopdbardbar_tau030000um_M1600_2018, SingleMuon2017F],
        },
    "T2_DE_DESY": {
        "miniaod": [JetHT2017C, JetHT2017E, JetHT2018C, SingleMuon2017D],
        },
    "T2_US_MIT": {
        "miniaod": [qcdht0500_2018, ttHbb_2017, zjetstonunuht0800_2017],
        },
    "T2_US_Florida": {
        "miniaod": [ttbar_2018, ttZext_2017, qcdht0700_2017, qcdht0500_2017, zjetstonunuht2500_2017],
        },
    "T2_US_Nebraska": {
        "miniaod": [SingleMuon2017C, ttbar_2017, qcdht0300_2017, mfv_neu_tau030000um_M1600_2017],
        },
    "T2_US_Purdue": {
        "miniaod": [mfv_stopdbardbar_tau000100um_M1200_2017, zjetstonunuht0100_2017, zjetstonunuht0600_2017, wjetstolnu_2017],
        },
    "T2_US_Wisconsin" : {
        "miniaod": [ttZ_2017, mfv_stopdbardbar_tau000300um_M0600_2017, zjetstonunuht0400_2017, wjetstolnuext_2017],
        },
    }


_seen = set()
for site, d in condorable.iteritems():
    if not xrootd_sites.has_key(site):
        raise ValueError('need entry in xrootd_sites for %s' % site)
    for ds, samples in d.iteritems():
        for s in samples:
            if s in _seen:
                raise ValueError('%s duplicated in condorable dict' % s.name)
            _seen.add(s)
            s.datasets[ds].condor = True
            s.datasets[ds].xrootd_url = xrootd_sites[site]

# can only run signal ntuples via condor where we can split by nevents, so require they're all reachable
for s in mfv_signal_samples_2017 + mfv_signal_samples_2018 + mfv_stopdbardbar_samples_2017 + mfv_stopdbardbar_samples_2018:
    if s not in _seen:
        raise ValueError('%s not in condorable dict' % s.name)

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
        for s in all_signal_samples_2017 + all_signal_samples_2018:
            l = DBS.datasets('/%s/*/MINIAODSIM' % s.primary_dataset)
            if len(l) == 1:
                nevents = DBS.numevents_in_dataset(l[0])
                print "_adbp('miniaod', '%s', %i)" % (l[0], nevents)
            else:
                print colors.boldred('no miniaod for %s' % s.name)

    if 0:
        for s in qcd_samples_2017 + ttbar_samples_2017 + qcd_samples_2018 + ttbar_samples_2018:
            s.set_curr_dataset('miniaod')
            il = s.int_lumi_orig / 1000
            nfn = len(s.filenames)
            print s.name, nfn, il, '->', int(400/il*nfn), int(400/il*s.nevents_orig)
