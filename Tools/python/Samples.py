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
        'mfv_stoplb': r'\tilde{t} \rightarrow lb',
        'mfv_stopld': r'\tilde{t} \rightarrow ld', 
        'mfv_splitSUSY': r'\tilde{g} \rightarrow qq\tilde{\chi}',
        'ggHToSSTobbbb' : r'ggH \rightarrow SS \rightarrow b\bar{b}b\bar{b}',
        'ggHToSSTodddd' : r'ggH \rightarrow SS \rightarrow d\bar{d}d\bar{d}',
        'ggHToSSTo4l' : r'ggH \rightarrow SS \rightarrow llll',
        'ZHToSSTodddd' : r'ZH \rightarrow SS \rightarrow d\bar{d}d\bar{d}',
        'WplusHToSSTodddd' : r'W^{\plus}H \rightarrow SS \rightarrow d\bar{d}d\bar{d}',
        'WminusHToSSTodddd' : r'W^{\minus}H \rightarrow SS \rightarrow d\bar{d}d\bar{d}',
        }[_model(s)]
    year = int(s.rsplit('_')[-1])
    assert 2015 <= year <= 2018 or year==20161 or year == 20162
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
    #sample.xsec = 1e-3
    if (sample.name.startswith('WplusH')):
        sample.xsec = 3*(9.426e-02)*0.01# xsec(pp->3*(W+->lv)H) * br(1% of H->SS) for 3 lepton flavours as in https://twiki.cern.ch/twiki/bin/view/LHCPhysics/CERNYellowReportPageAt13TeV#ppWH_Total_Cross_Section_with_ap and https://github.com/cms-sw/genproductions/blob/master/bin/Powheg/production/2017/13TeV/Higgs/WplusHJ_HanythingJ_NNPDF31_13TeV/HWplusJ_HanythingJ_NNPDF31_13TeV_M125_Vleptonic.input  
    else:
        #print(sample.name)
        sample.xsec = 1e-3
    sample.is_private = sample.dataset.startswith('/mfv_') and sample.dataset.endswith('/USER')
    if sample.is_private:
        sample.dbs_inst = 'phys03'
        sample.condor = True
        sample.xrootd_url = xrootd_sites['T3_US_FNALLPC']

########################################################################

########
# 2016 1 MC
########

qcd_lep_samples_20161 = [
    MCSample('qcdempt015_20161',    '/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM',   4062805, nice='QCD,  15 < #hat{p}_{T} <  20 GeV, EM enriched',  color=801, syst_frac=0.20, xsec=1.324e6),
    MCSample('qcdmupt15_20161',     '/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM',   8685279, nice='QCD, #hat{p}_{T} > 20 GeV, #mu p_{T} > 15 GeV',  color=801, syst_frac=0.20, xsec=2.39e5),
    MCSample('qcdempt020_20161',    '/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM',   7156441, nice='QCD,  20 < #hat{p}_{T} <  30 GeV, EM enriched',  color=801, syst_frac=0.20, xsec=4.896e6),
    MCSample('qcdempt030_20161',    '/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM',   4361931, nice='QCD,  30 < #hat{p}_{T} <  50 GeV, EM enriched',  color=801, syst_frac=0.20, xsec=6.447e6),
    MCSample('qcdempt050_20161',    '/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM',   5440758, nice='QCD,  50 < #hat{p}_{T} <  80 GeV, EM enriched',  color=801, syst_frac=0.20, xsec=1.988e6),
    MCSample('qcdempt080_20161',    '/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM',  4847354, nice='QCD,  80 < #hat{p}_{T} < 120 GeV, EM enriched',  color=801, syst_frac=0.20, xsec=3.675e5),
    MCSample('qcdempt120_20161',    '/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 4852573, nice='QCD, 120 < #hat{p}_{T} < 170 GeV, EM enriched',  color=801, syst_frac=0.20, xsec=6.659e4),
    MCSample('qcdempt170_20161',    '/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 1855461, nice='QCD, 170 < #hat{p}_{T} < 300 GeV, EM enriched',  color=801, syst_frac=0.20, xsec=1.662e4),
    MCSample('qcdempt300_20161',    '/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 1142775, nice='QCD, #hat{p}_{T} > 300 GeV, EM enriched',        color=801, syst_frac=0.20, xsec=1104.0),
    MCSample('qcdbctoept020_20161', '/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM',        7913320, nice='QCD,  20 < #hat{p}_{T} <  30 GeV, HF electrons', color=801, syst_frac=0.20, xsec=3.038e5),
    MCSample('qcdbctoept030_20161', '/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM',        7967312, nice='QCD,  30 < #hat{p}_{T} <  80 GeV, HF electrons', color=801, syst_frac=0.20, xsec=3.623e5),
    MCSample('qcdbctoept080_20161', '/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM',       7690702, nice='QCD,  80 < #hat{p}_{T} < 170 GeV, HF electrons', color=801, syst_frac=0.20, xsec=3.37e4),
    MCSample('qcdbctoept170_20161', '/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM',      7342849, nice='QCD, 170 < #hat{p}_{T} < 250 GeV, HF electrons', color=801, syst_frac=0.20, xsec=2.125e3),
    MCSample('qcdbctoept250_20161', '/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM',      6856820, nice='QCD, #hat{p}_{T} > 250 GeV, HF electrons',       color=801, syst_frac=0.20, xsec=562.5),
]

leptonic_samples_20161 = [
    MCSample('wjetstolnu_0j_20161',    '/WJetsToLNu_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM',      152373244,nice='W + jets #rightarrow l#nu', color= 9, syst_fac=0.10, xsec=52.780e3), 
    MCSample('wjetstolnu_1j_20161',    '/WJetsToLNu_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM',      173468850,nice='W + jets #rightarrow l#nu', color= 9, syst_fac=0.10, xsec=8.832e3), 
    MCSample('wjetstolnu_2j_20161',    '/WJetsToLNu_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM',      87929021,nice='W + jets #rightarrow l#nu', color= 9, syst_fac=0.10, xsec=3.276e3), 
    MCSample('dyjetstollM10_20161',    '/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM', 25799525, nice='DY + jets #rightarrow ll, 10 < M < 50 GeV', color= 29, syst_frac=0.10, xsec=1.58e4),
    MCSample('dyjetstollM50_20161',    '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM',     95170542, nice='DY + jets #rightarrow ll, M > 50 GeV',      color= 32, syst_frac=0.10, xsec=5.34e3),
]

met_samples_20161 = [
    #MCSample('ttbar_20161',     '/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM',                    94164991, nice='t#bar{t}',                                  color=4,   syst_frac=0.15, xsec=831.76),
]

ttbar_samples_20161 = [
    MCSample('ttbar_20161',     '/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM',                    94164991, nice='t#bar{t}',                                  color=4,   syst_frac=0.15, xsec=831.76),
]

diboson_samples_20161 = [
    MCSample('ww_20161', '/WW_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM', 15859000, nice='WW', color = 9, syst_frac=0.10, xsec=75.8),
    MCSample('zz_20161', '/ZZ_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM',  1282000, nice='ZZ', color = 9, syst_frac=0.10, xsec=12.140),
    MCSample('wz_20161', '/WZ_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM',  7934000, nice='WZ', color = 9, syst_frac=0.10, xsec=27.6)
]

mfv_stoplb_samples_20161 = [
    MCSample('mfv_stoplb_tau000100um_M1000_20161', '/DisplacedSUSY_stopToLBottom_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 98890),
    MCSample('mfv_stoplb_tau000300um_M1000_20161', '/DisplacedSUSY_stopToLBottom_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 99090),
    MCSample('mfv_stoplb_tau010000um_M1000_20161', '/DisplacedSUSY_stopToLBottom_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 49863),
    MCSample('mfv_stoplb_tau001000um_M1000_20161', '/DisplacedSUSY_stopToLBottom_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 99632),
    MCSample('mfv_stoplb_tau030000um_M1000_20161', '/DisplacedSUSY_stopToLBottom_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 99612),
    MCSample('mfv_stoplb_tau000100um_M1200_20161', '/DisplacedSUSY_stopToLBottom_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 99340),
    MCSample('mfv_stoplb_tau000300um_M1200_20161', '/DisplacedSUSY_stopToLBottom_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 99010),
    MCSample('mfv_stoplb_tau010000um_M1200_20161', '/DisplacedSUSY_stopToLBottom_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 49944),
    MCSample('mfv_stoplb_tau001000um_M1200_20161', '/DisplacedSUSY_stopToLBottom_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 97995),
    MCSample('mfv_stoplb_tau030000um_M1200_20161', '/DisplacedSUSY_stopToLBottom_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 101825),
    MCSample('mfv_stoplb_tau000100um_M1400_20161', '/DisplacedSUSY_stopToLBottom_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 100444),
    MCSample('mfv_stoplb_tau000300um_M1400_20161', '/DisplacedSUSY_stopToLBottom_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 98629),
    MCSample('mfv_stoplb_tau010000um_M1400_20161', '/DisplacedSUSY_stopToLBottom_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 49531),
    MCSample('mfv_stoplb_tau001000um_M1400_20161', '/DisplacedSUSY_stopToLBottom_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 99778),
    MCSample('mfv_stoplb_tau030000um_M1400_20161', '/DisplacedSUSY_stopToLBottom_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 99896),
    MCSample('mfv_stoplb_tau000100um_M1600_20161', '/DisplacedSUSY_stopToLBottom_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 99251),
    MCSample('mfv_stoplb_tau000300um_M1600_20161', '/DisplacedSUSY_stopToLBottom_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 99184),
    MCSample('mfv_stoplb_tau010000um_M1600_20161', '/DisplacedSUSY_stopToLBottom_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 50317),
    MCSample('mfv_stoplb_tau001000um_M1600_20161', '/DisplacedSUSY_stopToLBottom_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 49741),
    MCSample('mfv_stoplb_tau030000um_M1600_20161', '/DisplacedSUSY_stopToLBottom_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 48712),
    MCSample('mfv_stoplb_tau000100um_M1800_20161', '/DisplacedSUSY_stopToLBottom_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 100766),
    MCSample('mfv_stoplb_tau000300um_M1800_20161', '/DisplacedSUSY_stopToLBottom_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 81729),
    MCSample('mfv_stoplb_tau010000um_M1800_20161', '/DisplacedSUSY_stopToLBottom_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 49090),
    MCSample('mfv_stoplb_tau001000um_M1800_20161', '/DisplacedSUSY_stopToLBottom_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 49049),
    MCSample('mfv_stoplb_tau030000um_M1800_20161', '/DisplacedSUSY_stopToLBottom_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 49438),
    MCSample('mfv_stoplb_tau000100um_M0200_20161', '/DisplacedSUSY_stopToLBottom_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 99188),
    MCSample('mfv_stoplb_tau000300um_M0200_20161', '/DisplacedSUSY_stopToLBottom_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 100726),
    MCSample('mfv_stoplb_tau010000um_M0200_20161', '/DisplacedSUSY_stopToLBottom_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 99023),
    MCSample('mfv_stoplb_tau001000um_M0200_20161', '/DisplacedSUSY_stopToLBottom_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 99012),
    MCSample('mfv_stoplb_tau030000um_M0200_20161', '/DisplacedSUSY_stopToLBottom_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 99812),
    MCSample('mfv_stoplb_tau000100um_M0300_20161', '/DisplacedSUSY_stopToLBottom_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 100222),
    MCSample('mfv_stoplb_tau000300um_M0300_20161', '/DisplacedSUSY_stopToLBottom_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 100150),
    MCSample('mfv_stoplb_tau010000um_M0300_20161', '/DisplacedSUSY_stopToLBottom_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 98854),
    MCSample('mfv_stoplb_tau001000um_M0300_20161', '/DisplacedSUSY_stopToLBottom_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 100049),
    MCSample('mfv_stoplb_tau030000um_M0300_20161', '/DisplacedSUSY_stopToLBottom_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 99401),
    MCSample('mfv_stoplb_tau000100um_M0400_20161', '/DisplacedSUSY_stopToLBottom_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 100672),
    MCSample('mfv_stoplb_tau000300um_M0400_20161', '/DisplacedSUSY_stopToLBottom_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 98457),
    MCSample('mfv_stoplb_tau010000um_M0400_20161', '/DisplacedSUSY_stopToLBottom_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 99343),
    MCSample('mfv_stoplb_tau001000um_M0400_20161', '/DisplacedSUSY_stopToLBottom_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 99760),
    MCSample('mfv_stoplb_tau030000um_M0400_20161', '/DisplacedSUSY_stopToLBottom_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 98676),
    MCSample('mfv_stoplb_tau000100um_M0600_20161', '/DisplacedSUSY_stopToLBottom_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 100158),
    MCSample('mfv_stoplb_tau000300um_M0600_20161', '/DisplacedSUSY_stopToLBottom_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 98762),
    MCSample('mfv_stoplb_tau010000um_M0600_20161', '/DisplacedSUSY_stopToLBottom_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 99264),
    MCSample('mfv_stoplb_tau001000um_M0600_20161', '/DisplacedSUSY_stopToLBottom_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 101849),
    MCSample('mfv_stoplb_tau030000um_M0600_20161', '/DisplacedSUSY_stopToLBottom_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 100390),
    MCSample('mfv_stoplb_tau000100um_M0800_20161', '/DisplacedSUSY_stopToLBottom_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 98204),
    MCSample('mfv_stoplb_tau000300um_M0800_20161', '/DisplacedSUSY_stopToLBottom_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 100784),
    MCSample('mfv_stoplb_tau010000um_M0800_20161', '/DisplacedSUSY_stopToLBottom_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 48963),
    MCSample('mfv_stoplb_tau001000um_M0800_20161', '/DisplacedSUSY_stopToLBottom_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 100377),
    MCSample('mfv_stoplb_tau030000um_M0800_20161', '/DisplacedSUSY_stopToLBottom_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 99164)
]

mfv_stopld_samples_20161 = [
    MCSample('mfv_stopld_tau000100um_M1000_20161', '/DisplacedSUSY_stopToLD_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 99017),
    MCSample('mfv_stopld_tau000300um_M1000_20161', '/DisplacedSUSY_stopToLD_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 99362),
    MCSample('mfv_stopld_tau010000um_M1000_20161', '/DisplacedSUSY_stopToLD_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 49856),
    MCSample('mfv_stopld_tau001000um_M1000_20161', '/DisplacedSUSY_stopToLD_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 98183),
    MCSample('mfv_stopld_tau030000um_M1000_20161', '/DisplacedSUSY_stopToLD_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 100852),
    MCSample('mfv_stopld_tau000100um_M1200_20161', '/DisplacedSUSY_stopToLD_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 99830),
    MCSample('mfv_stopld_tau000300um_M1200_20161', '/DisplacedSUSY_stopToLD_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 99813),
    MCSample('mfv_stopld_tau010000um_M1200_20161', '/DisplacedSUSY_stopToLD_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 49767),
    MCSample('mfv_stopld_tau001000um_M1200_20161', '/DisplacedSUSY_stopToLD_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 100012),
    MCSample('mfv_stopld_tau030000um_M1200_20161', '/DisplacedSUSY_stopToLD_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 99996),
    MCSample('mfv_stopld_tau000100um_M1400_20161', '/DisplacedSUSY_stopToLD_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 100303),
    MCSample('mfv_stopld_tau000300um_M1400_20161', '/DisplacedSUSY_stopToLD_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 98700),
    MCSample('mfv_stopld_tau010000um_M1400_20161', '/DisplacedSUSY_stopToLD_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 49501),
    MCSample('mfv_stopld_tau001000um_M1400_20161', '/DisplacedSUSY_stopToLD_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 99221),
    MCSample('mfv_stopld_tau030000um_M1400_20161', '/DisplacedSUSY_stopToLD_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 99706),
    MCSample('mfv_stopld_tau000100um_M1600_20161', '/DisplacedSUSY_stopToLD_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 98875),
    MCSample('mfv_stopld_tau000300um_M1600_20161', '/DisplacedSUSY_stopToLD_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 98632),
    MCSample('mfv_stopld_tau010000um_M1600_20161', '/DisplacedSUSY_stopToLD_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 49359),
    MCSample('mfv_stopld_tau001000um_M1600_20161', '/DisplacedSUSY_stopToLD_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 50121),
    MCSample('mfv_stopld_tau030000um_M1600_20161', '/DisplacedSUSY_stopToLD_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 50681),
    MCSample('mfv_stopld_tau000100um_M1800_20161', '/DisplacedSUSY_stopToLD_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 99761),
    MCSample('mfv_stopld_tau000300um_M1800_20161', '/DisplacedSUSY_stopToLD_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 100032),
    MCSample('mfv_stopld_tau010000um_M1800_20161', '/DisplacedSUSY_stopToLD_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 49884),
    MCSample('mfv_stopld_tau001000um_M1800_20161', '/DisplacedSUSY_stopToLD_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 49871),
    MCSample('mfv_stopld_tau030000um_M1800_20161', '/DisplacedSUSY_stopToLD_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 49634),
    MCSample('mfv_stopld_tau000100um_M0200_20161', '/DisplacedSUSY_stopToLD_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 101080),
    MCSample('mfv_stopld_tau000300um_M0200_20161', '/DisplacedSUSY_stopToLD_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 98938),
    MCSample('mfv_stopld_tau010000um_M0200_20161', '/DisplacedSUSY_stopToLD_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 99845),
    MCSample('mfv_stopld_tau001000um_M0200_20161', '/DisplacedSUSY_stopToLD_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 99943),
    MCSample('mfv_stopld_tau030000um_M0200_20161', '/DisplacedSUSY_stopToLD_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 99418),
    MCSample('mfv_stopld_tau000100um_M0300_20161', '/DisplacedSUSY_stopToLD_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 101171),
    MCSample('mfv_stopld_tau000300um_M0300_20161', '/DisplacedSUSY_stopToLD_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 100455),
    MCSample('mfv_stopld_tau010000um_M0300_20161', '/DisplacedSUSY_stopToLD_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 100892),
    MCSample('mfv_stopld_tau001000um_M0300_20161', '/DisplacedSUSY_stopToLD_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 99556),
    MCSample('mfv_stopld_tau030000um_M0300_20161', '/DisplacedSUSY_stopToLD_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 99447),
    MCSample('mfv_stopld_tau000100um_M0400_20161', '/DisplacedSUSY_stopToLD_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 100509),
    MCSample('mfv_stopld_tau000300um_M0400_20161', '/DisplacedSUSY_stopToLD_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 99765),
    MCSample('mfv_stopld_tau010000um_M0400_20161', '/DisplacedSUSY_stopToLD_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 99682),
    MCSample('mfv_stopld_tau001000um_M0400_20161', '/DisplacedSUSY_stopToLD_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 99890),
    MCSample('mfv_stopld_tau030000um_M0400_20161', '/DisplacedSUSY_stopToLD_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 99531),
    MCSample('mfv_stopld_tau000100um_M0600_20161', '/DisplacedSUSY_stopToLD_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 100034),
    MCSample('mfv_stopld_tau000300um_M0600_20161', '/DisplacedSUSY_stopToLD_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 99611),
    MCSample('mfv_stopld_tau010000um_M0600_20161', '/DisplacedSUSY_stopToLD_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 99643),
    MCSample('mfv_stopld_tau001000um_M0600_20161', '/DisplacedSUSY_stopToLD_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 99924),
    MCSample('mfv_stopld_tau030000um_M0600_20161', '/DisplacedSUSY_stopToLD_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 101612),
    MCSample('mfv_stopld_tau000100um_M0800_20161', '/DisplacedSUSY_stopToLD_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 100466),
    MCSample('mfv_stopld_tau000300um_M0800_20161', '/DisplacedSUSY_stopToLD_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 98676),
    MCSample('mfv_stopld_tau010000um_M0800_20161', '/DisplacedSUSY_stopToLD_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 50147),
    MCSample('mfv_stopld_tau001000um_M0800_20161', '/DisplacedSUSY_stopToLD_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 98387),
    MCSample('mfv_stopld_tau030000um_M0800_20161', '/DisplacedSUSY_stopToLD_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 99914)
]

ZHToSSTodddd_samples_20161 = [ 
    MCSample('ZHToSSTodddd_tau1mm_M55_20161', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 49990), 
]

WplusHToSSTodddd_samples_20161 = [
    MCSample('WplusHToSSTodddd_tau1mm_M55_20161', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 24999),
]

WminusHToSSTodddd_samples_20161 = [
    MCSample('WminusHToSSTodddd_tau1mm_M55_20161', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 24995),
]



all_signal_samples_20161 = ZHToSSTodddd_samples_20161 + WplusHToSSTodddd_samples_20161 + WminusHToSSTodddd_samples_20161
#all_signal_samples_20161 = mfv_stoplb_samples_20161 + mfv_stopld_samples_20161

#######
#2016 2 MC
#######

qcd_lep_samples_20162 = [
    MCSample('qcdempt015_20162',    '/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM',   4026314, nice='QCD,  15 < #hat{p}_{T} <  20 GeV, EM enriched',  color=801, syst_frac=0.20, xsec=1.324e6),
    MCSample('qcdmupt15_20162',     '/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM',   8884250, nice='QCD, #hat{p}_{T} > 20 GeV, #mu p_{T} > 15 GeV',  color=801, syst_frac=0.20, xsec=2.39e5),
    MCSample('qcdempt020_20162',    '/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM',   7134788, nice='QCD,  20 < #hat{p}_{T} <  30 GeV, EM enriched',  color=801, syst_frac=0.20, xsec=4.896e6),
    MCSample('qcdempt030_20162',    '/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM',   4351014, nice='QCD,  30 < #hat{p}_{T} <  50 GeV, EM enriched',  color=801, syst_frac=0.20, xsec=6.447e6),
    MCSample('qcdempt050_20162',    '/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM',   5443934, nice='QCD,  50 < #hat{p}_{T} <  80 GeV, EM enriched',  color=801, syst_frac=0.20, xsec=1.988e6),
    MCSample('qcdempt080_20162',    '/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM',  4804788, nice='QCD,  80 < #hat{p}_{T} < 120 GeV, EM enriched',  color=801, syst_frac=0.20, xsec=3.675e5),
    MCSample('qcdempt120_20162',    '/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 5007347, nice='QCD, 120 < #hat{p}_{T} < 170 GeV, EM enriched',  color=801, syst_frac=0.20, xsec=6.659e4),
    MCSample('qcdempt170_20162',    '/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 1861129, nice='QCD, 170 < #hat{p}_{T} < 300 GeV, EM enriched',  color=801, syst_frac=0.20, xsec=1.662e4),
    MCSample('qcdempt300_20162',    '/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 1138742, nice='QCD, #hat{p}_{T} > 300 GeV, EM enriched',        color=801, syst_frac=0.20, xsec=1104.0),
    MCSample('qcdbctoept020_20162', '/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM',        7308299, nice='QCD,  20 < #hat{p}_{T} <  30 GeV, HF electrons', color=801, syst_frac=0.20, xsec=3.038e5),
    MCSample('qcdbctoept030_20162', '/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM',        7714512, nice='QCD,  30 < #hat{p}_{T} <  80 GeV, HF electrons', color=801, syst_frac=0.20, xsec=3.623e5),
    MCSample('qcdbctoept080_20162', '/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM',       7882938, nice='QCD,  80 < #hat{p}_{T} < 170 GeV, HF electrons', color=801, syst_frac=0.20, xsec=3.37e4),
    MCSample('qcdbctoept170_20162', '/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM',      7863538, nice='QCD, 170 < #hat{p}_{T} < 250 GeV, HF electrons', color=801, syst_frac=0.20, xsec=2.125e3),
    MCSample('qcdbctoept250_20162', '/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM',      8152626, nice='QCD, #hat{p}_{T} > 250 GeV, HF electrons',       color=801, syst_frac=0.20, xsec=562.5),
]
    
leptonic_samples_20162 = [
    MCSample('wjetstolnu_0j_20162',    '/WJetsToLNu_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM',      159895674,nice='W + jets #rightarrow l#nu', color= 9, syst_fac=0.10, xsec=52.780e3), 
    MCSample('wjetstolnu_1j_20162',    '/WJetsToLNu_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM',      167715035,nice='W + jets #rightarrow l#nu', color= 9, syst_fac=0.10, xsec=8.832e3), 
    MCSample('wjetstolnu_2j_20162',    '/WJetsToLNu_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM',      85825681,nice='W + jets #rightarrow l#nu', color= 9, syst_fac=0.10, xsec=3.276e3), 
    MCSample('dyjetstollM10_20162',    '/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM', 23706672, nice='DY + jets #rightarrow ll, 10 < M < 50 GeV', color= 29, syst_frac=0.10, xsec=1.58e4),
    MCSample('dyjetstollM50_20162',    '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM',     82448537, nice='DY + jets #rightarrow ll, M > 50 GeV',      color= 32, syst_frac=0.10, xsec=5.34e3),
]

met_samples_20162 = [
    #MCSample('ttbar_20162',     '/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM',                    90609841, nice='t#bar{t}',                                  color=4,   syst_frac=0.15, xsec=831.76),
]

ttbar_samples_20162 = [
    MCSample('ttbar_20162',     '/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM',                    90609841, nice='t#bar{t}',                                  color=4,   syst_frac=0.15, xsec=831.76),
]

diboson_samples_20162 = [
    MCSample('ww_20162', '/WW_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM', 15821000, nice='WW', color = 9, syst_frac=0.10, xsec=75.8),
    MCSample('zz_20162', '/ZZ_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM',  1151000, nice='ZZ', color = 9, syst_frac=0.10, xsec=12.140),
    MCSample('wz_20162', '/WZ_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM',  7584000, nice='WZ', color = 9, syst_frac=0.10, xsec=27.6)
]

mfv_stoplb_samples_20162 = [
    MCSample('mfv_stoplb_tau000100um_M1000_20162', '/DisplacedSUSY_stopToLBottom_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 99539),
    MCSample('mfv_stoplb_tau000300um_M1000_20162', '/DisplacedSUSY_stopToLBottom_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 99257),
    MCSample('mfv_stoplb_tau010000um_M1000_20162', '/DisplacedSUSY_stopToLBottom_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 47714),
    MCSample('mfv_stoplb_tau001000um_M1000_20162', '/DisplacedSUSY_stopToLBottom_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 98557),
    MCSample('mfv_stoplb_tau030000um_M1000_20162', '/DisplacedSUSY_stopToLBottom_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 99898),
    MCSample('mfv_stoplb_tau000100um_M1200_20162', '/DisplacedSUSY_stopToLBottom_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 100330),
    MCSample('mfv_stoplb_tau000300um_M1200_20162', '/DisplacedSUSY_stopToLBottom_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 98676),
    MCSample('mfv_stoplb_tau010000um_M1200_20162', '/DisplacedSUSY_stopToLBottom_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 49832),
    MCSample('mfv_stoplb_tau001000um_M1200_20162', '/DisplacedSUSY_stopToLBottom_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 98582),
    MCSample('mfv_stoplb_tau030000um_M1200_20162', '/DisplacedSUSY_stopToLBottom_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 100391),
    MCSample('mfv_stoplb_tau000100um_M1400_20162', '/DisplacedSUSY_stopToLBottom_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 100112),
    MCSample('mfv_stoplb_tau000300um_M1400_20162', '/DisplacedSUSY_stopToLBottom_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 99840),
    MCSample('mfv_stoplb_tau010000um_M1400_20162', '/DisplacedSUSY_stopToLBottom_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 49856),
    MCSample('mfv_stoplb_tau001000um_M1400_20162', '/DisplacedSUSY_stopToLBottom_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 99508),
    MCSample('mfv_stoplb_tau030000um_M1400_20162', '/DisplacedSUSY_stopToLBottom_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 99537),
    MCSample('mfv_stoplb_tau000100um_M1600_20162', '/DisplacedSUSY_stopToLBottom_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 99744),
    MCSample('mfv_stoplb_tau000300um_M1600_20162', '/DisplacedSUSY_stopToLBottom_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 99902),
    MCSample('mfv_stoplb_tau010000um_M1600_20162', '/DisplacedSUSY_stopToLBottom_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 49227),
    MCSample('mfv_stoplb_tau001000um_M1600_20162', '/DisplacedSUSY_stopToLBottom_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 50163),
    MCSample('mfv_stoplb_tau030000um_M1600_20162', '/DisplacedSUSY_stopToLBottom_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 50181),
    MCSample('mfv_stoplb_tau000100um_M1800_20162', '/DisplacedSUSY_stopToLBottom_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 98144),
    MCSample('mfv_stoplb_tau000300um_M1800_20162', '/DisplacedSUSY_stopToLBottom_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 101235),
    MCSample('mfv_stoplb_tau010000um_M1800_20162', '/DisplacedSUSY_stopToLBottom_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 50608),
    MCSample('mfv_stoplb_tau001000um_M1800_20162', '/DisplacedSUSY_stopToLBottom_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 49712),
    MCSample('mfv_stoplb_tau030000um_M1800_20162', '/DisplacedSUSY_stopToLBottom_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 49799),
    MCSample('mfv_stoplb_tau000100um_M0200_20162', '/DisplacedSUSY_stopToLBottom_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v3/MINIAODSIM', 99793),
    MCSample('mfv_stoplb_tau000300um_M0200_20162', '/DisplacedSUSY_stopToLBottom_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 99406),
    MCSample('mfv_stoplb_tau010000um_M0200_20162', '/DisplacedSUSY_stopToLBottom_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 99401),
    MCSample('mfv_stoplb_tau001000um_M0200_20162', '/DisplacedSUSY_stopToLBottom_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 97820),
    MCSample('mfv_stoplb_tau030000um_M0200_20162', '/DisplacedSUSY_stopToLBottom_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 101202),
    MCSample('mfv_stoplb_tau000100um_M0300_20162', '/DisplacedSUSY_stopToLBottom_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 99857),
    MCSample('mfv_stoplb_tau000300um_M0300_20162', '/DisplacedSUSY_stopToLBottom_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 99010),
    MCSample('mfv_stoplb_tau010000um_M0300_20162', '/DisplacedSUSY_stopToLBottom_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 101044),
    MCSample('mfv_stoplb_tau001000um_M0300_20162', '/DisplacedSUSY_stopToLBottom_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 99219),
    MCSample('mfv_stoplb_tau030000um_M0300_20162', '/DisplacedSUSY_stopToLBottom_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 99207),
    MCSample('mfv_stoplb_tau000100um_M0400_20162', '/DisplacedSUSY_stopToLBottom_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 98268),
    MCSample('mfv_stoplb_tau000300um_M0400_20162', '/DisplacedSUSY_stopToLBottom_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 100008),
    MCSample('mfv_stoplb_tau010000um_M0400_20162', '/DisplacedSUSY_stopToLBottom_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 101168),
    MCSample('mfv_stoplb_tau001000um_M0400_20162', '/DisplacedSUSY_stopToLBottom_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 99255),
    MCSample('mfv_stoplb_tau030000um_M0400_20162', '/DisplacedSUSY_stopToLBottom_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 99198),
    MCSample('mfv_stoplb_tau000100um_M0600_20162', '/DisplacedSUSY_stopToLBottom_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 100291),
    MCSample('mfv_stoplb_tau000300um_M0600_20162', '/DisplacedSUSY_stopToLBottom_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 86231),
    MCSample('mfv_stoplb_tau010000um_M0600_20162', '/DisplacedSUSY_stopToLBottom_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 100170),
    MCSample('mfv_stoplb_tau001000um_M0600_20162', '/DisplacedSUSY_stopToLBottom_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 99575),
    MCSample('mfv_stoplb_tau030000um_M0600_20162', '/DisplacedSUSY_stopToLBottom_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 100308),
    MCSample('mfv_stoplb_tau000100um_M0800_20162', '/DisplacedSUSY_stopToLBottom_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 100987),
    MCSample('mfv_stoplb_tau000300um_M0800_20162', '/DisplacedSUSY_stopToLBottom_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 100012),
    MCSample('mfv_stoplb_tau010000um_M0800_20162', '/DisplacedSUSY_stopToLBottom_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 50027),
    MCSample('mfv_stoplb_tau001000um_M0800_20162', '/DisplacedSUSY_stopToLBottom_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 99440),
    MCSample('mfv_stoplb_tau030000um_M0800_20162', '/DisplacedSUSY_stopToLBottom_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 98586)
]

mfv_stopld_samples_20162 = [
    MCSample('mfv_stopld_tau000100um_M1000_20162', '/DisplacedSUSY_stopToLD_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 99376),
    MCSample('mfv_stopld_tau000300um_M1000_20162', '/DisplacedSUSY_stopToLD_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 100018),
    MCSample('mfv_stopld_tau010000um_M1000_20162', '/DisplacedSUSY_stopToLD_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 49142),
    MCSample('mfv_stopld_tau001000um_M1000_20162', '/DisplacedSUSY_stopToLD_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 100845),
    MCSample('mfv_stopld_tau030000um_M1000_20162', '/DisplacedSUSY_stopToLD_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 99794),
    MCSample('mfv_stopld_tau000100um_M1200_20162', '/DisplacedSUSY_stopToLD_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 99574),
    MCSample('mfv_stopld_tau000300um_M1200_20162', '/DisplacedSUSY_stopToLD_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 99868),
    MCSample('mfv_stopld_tau010000um_M1200_20162', '/DisplacedSUSY_stopToLD_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 49886),
    MCSample('mfv_stopld_tau001000um_M1200_20162', '/DisplacedSUSY_stopToLD_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 99291),
    MCSample('mfv_stopld_tau030000um_M1200_20162', '/DisplacedSUSY_stopToLD_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 99929),
    MCSample('mfv_stopld_tau000100um_M1400_20162', '/DisplacedSUSY_stopToLD_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 100532),
    MCSample('mfv_stopld_tau000300um_M1400_20162', '/DisplacedSUSY_stopToLD_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 99932),
    MCSample('mfv_stopld_tau010000um_M1400_20162', '/DisplacedSUSY_stopToLD_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 49788),
    MCSample('mfv_stopld_tau001000um_M1400_20162', '/DisplacedSUSY_stopToLD_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 98682),
    MCSample('mfv_stopld_tau030000um_M1400_20162', '/DisplacedSUSY_stopToLD_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 101616),
    MCSample('mfv_stopld_tau000100um_M1600_20162', '/DisplacedSUSY_stopToLD_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 100675),
    MCSample('mfv_stopld_tau000300um_M1600_20162', '/DisplacedSUSY_stopToLD_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 100486),
    MCSample('mfv_stopld_tau010000um_M1600_20162', '/DisplacedSUSY_stopToLD_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 49732),
    MCSample('mfv_stopld_tau001000um_M1600_20162', '/DisplacedSUSY_stopToLD_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 50045),
    MCSample('mfv_stopld_tau030000um_M1600_20162', '/DisplacedSUSY_stopToLD_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 49682),
    MCSample('mfv_stopld_tau000100um_M1800_20162', '/DisplacedSUSY_stopToLD_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 99094),
    MCSample('mfv_stopld_tau000300um_M1800_20162', '/DisplacedSUSY_stopToLD_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 99749),
    MCSample('mfv_stopld_tau010000um_M1800_20162', '/DisplacedSUSY_stopToLD_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 49663),
    MCSample('mfv_stopld_tau001000um_M1800_20162', '/DisplacedSUSY_stopToLD_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 49813),
    MCSample('mfv_stopld_tau030000um_M1800_20162', '/DisplacedSUSY_stopToLD_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 50468),
    MCSample('mfv_stopld_tau000100um_M0200_20162', '/DisplacedSUSY_stopToLD_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 100260),
    MCSample('mfv_stopld_tau000300um_M0200_20162', '/DisplacedSUSY_stopToLD_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 99340),
    MCSample('mfv_stopld_tau010000um_M0200_20162', '/DisplacedSUSY_stopToLD_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 99542),
    MCSample('mfv_stopld_tau001000um_M0200_20162', '/DisplacedSUSY_stopToLD_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 97872),
    MCSample('mfv_stopld_tau030000um_M0200_20162', '/DisplacedSUSY_stopToLD_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 100076),
    MCSample('mfv_stopld_tau000100um_M0300_20162', '/DisplacedSUSY_stopToLD_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 100170),
    MCSample('mfv_stopld_tau000300um_M0300_20162', '/DisplacedSUSY_stopToLD_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 100594),
    MCSample('mfv_stopld_tau010000um_M0300_20162', '/DisplacedSUSY_stopToLD_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 99759),
    MCSample('mfv_stopld_tau001000um_M0300_20162', '/DisplacedSUSY_stopToLD_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 99504),
    MCSample('mfv_stopld_tau030000um_M0300_20162', '/DisplacedSUSY_stopToLD_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 99243),
    MCSample('mfv_stopld_tau000100um_M0400_20162', '/DisplacedSUSY_stopToLD_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 100052),
    MCSample('mfv_stopld_tau000300um_M0400_20162', '/DisplacedSUSY_stopToLD_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 99431),
    MCSample('mfv_stopld_tau010000um_M0400_20162', '/DisplacedSUSY_stopToLD_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 99314),
    MCSample('mfv_stopld_tau001000um_M0400_20162', '/DisplacedSUSY_stopToLD_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 100447),
    MCSample('mfv_stopld_tau030000um_M0400_20162', '/DisplacedSUSY_stopToLD_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 99547),
    MCSample('mfv_stopld_tau000100um_M0600_20162', '/DisplacedSUSY_stopToLD_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 100954),
    MCSample('mfv_stopld_tau000300um_M0600_20162', '/DisplacedSUSY_stopToLD_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 99589),
    MCSample('mfv_stopld_tau010000um_M0600_20162', '/DisplacedSUSY_stopToLD_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 100599),
    MCSample('mfv_stopld_tau001000um_M0600_20162', '/DisplacedSUSY_stopToLD_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 99859),
    MCSample('mfv_stopld_tau030000um_M0600_20162', '/DisplacedSUSY_stopToLD_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 100128),
    MCSample('mfv_stopld_tau000100um_M0800_20162', '/DisplacedSUSY_stopToLD_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 99282),
    MCSample('mfv_stopld_tau000300um_M0800_20162', '/DisplacedSUSY_stopToLD_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 99263),
    MCSample('mfv_stopld_tau010000um_M0800_20162', '/DisplacedSUSY_stopToLD_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 49387),
    MCSample('mfv_stopld_tau001000um_M0800_20162', '/DisplacedSUSY_stopToLD_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 100038),
    MCSample('mfv_stopld_tau030000um_M0800_20162', '/DisplacedSUSY_stopToLD_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 100282)
]

ZHToSSTodddd_samples_20162 = [ 
    MCSample('ZHToSSTodddd_tau1mm_M55_20162', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 49998), 
]

WplusHToSSTodddd_samples_20162 = [
    MCSample('WplusHToSSTodddd_tau1mm_M55_20162', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 24998),
]

WminusHToSSTodddd_samples_20162 = [
    MCSample('WminusHToSSTodddd_tau1mm_M55_20162', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 24998),
]



all_signal_samples_20162 = ZHToSSTodddd_samples_20162 + WplusHToSSTodddd_samples_20162 + WminusHToSSTodddd_samples_20162
#all_signal_samples_20162 = mfv_stoplb_samples_20162 + mfv_stopld_samples_20162 

########
# 2017 MC 
########

qcd_samples_2017 = [
    MCSample('qcdht0200_2017', '/QCD_HT200to300_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL17RECO-106X_mc2017_realistic_v6-v2/AODSIM', 57816581, nice='QCD, 200 < H_{T} < 300 GeV',  color=802, syst_frac=0.20, xsec=1.554e6),
    MCSample('qcdht0300_2017', '/QCD_HT300to500_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL17RECO-106X_mc2017_realistic_v6-v2/AODSIM', 57097305, nice='QCD, 300 < H_{T} < 500 GeV',  color=803, syst_frac=0.20, xsec=3.226e5), #xsec not available
    MCSample('qcdht0500_2017', '/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL17RECO-106X_mc2017_realistic_v6-v2/AODSIM', 9183471, nice='QCD, 500 < H_{T} < 700 GeV', color=804, syst_frac=0.20, xsec=3.028e4),
    MCSample('qcdht0500ext_2017', '/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL17RECO-106X_mc2017_realistic_v6_ext1-v1/AODSIM', 59037642, nice='QCD, 500 < H_{T} < 700 GeV', color=804, syst_frac=0.20, xsec=3.028e4),
    MCSample('qcdht0700_2017', '/QCD_HT700to1000_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL17RECO-106X_mc2017_realistic_v6-v2/AODSIM', 45774525, nice='QCD, 700 < H_{T} < 1000 GeV',  color=805, syst_frac=0.20, xsec=6.392e3),
    MCSample('qcdht1000_2017', '/QCD_HT1000to1500_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL17RECO-106X_mc2017_realistic_v6-v2/AODSIM', 15420054, nice='QCD, 1000 < H_{T} < 1500 GeV', color=806, syst_frac=0.20, xsec=1.096e3), #xsec not available
    MCSample('qcdht1500_2017', '/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraph-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v1/AODSIM',     7711548, nice='QCD, 1500 < H_{T} < 2000 GeV', color=807, syst_frac=0.20, xsec=99.0), #xsec not available
    MCSample('qcdht2000_2017', '/QCD_HT2000toInf_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL17RECO-106X_mc2017_realistic_v6-v2/AODSIM',   5451735, nice='QCD, H_{T} > 2000',            color=808, syst_frac=0.20, xsec=21.93),
    ]
qcd_samples_sum_2017 = [
    SumSample('qcdht0500sum_2017', qcd_samples_2017[2:4]),
    ]

qcd_lep_samples_2017 = [
    MCSample('qcdmupt15_2017',  '/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v1/AODSIM',  17716270, nice='QCD, #hat{p}_{T} > 20 GeV, #mu p_{T} > 15 GeV', color=801, syst_frac=0.20, xsec=2.39e5),
    MCSample('qcdpt15mupt5_2017',  '/QCD_Pt-15To20_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v9-v2/AODSIM',  9019841, nice='QCD, 20 GeV > #hat{p}_{T} > 15 GeV, #mu p_{T} > 5 GeV', color=801, syst_frac=0.20, xsec=2.8e6),
    MCSample('qcdpt20mupt5_2017',  '/QCD_Pt-20To30_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v9-v2/AODSIM',  64634535, nice='QCD, 30 GeV > #hat{p}_{T} > 20 GeV, #mu p_{T} > 5 GeV', color=801, syst_frac=0.20, xsec=2.527e6),
    MCSample('qcdpt30mupt5_2017',  '/QCD_Pt-30To50_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v9-v2/AODSIM',  58749714, nice='QCD, 50 GeV > #hat{p}_{T} > 30 GeV, #mu p_{T} > 5 GeV', color=801, syst_frac=0.20, xsec=1.367e6),
    MCSample('qcdpt50mupt5_2017',  '/QCD_Pt-50To80_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v9-v2/AODSIM',  40377957, nice='QCD, 80 GeV > #hat{p}_{T} > 50 GeV, #mu p_{T} > 5 GeV', color=801, syst_frac=0.20, xsec=3.817e5),
    MCSample('qcdpt80mupt5_2017',  '/QCD_Pt-80To120_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v9-v2/AODSIM',  45981017, nice='QCD, 120 GeV > #hat{p}_{T} > 80 GeV, #mu p_{T} > 5 GeV', color=801, syst_frac=0.20, xsec=8.774e4),
    MCSample('qcdpt120mupt5_2017',  '/QCD_Pt-120To170_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v9-v2/AODSIM',  39394151, nice='QCD, 170 GeV > #hat{p}_{T} > 120 GeV, #mu p_{T} > 5 GeV', color=801, syst_frac=0.20, xsec=2.128e4),
    MCSample('qcdpt170mupt5_2017',  '/QCD_Pt-170To300_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v9-v2/AODSIM', 73071987, nice='QCD, 300 GeV > #hat{p}_{T} > 170 GeV, #mu p_{T} > 5 GeV', color=801, syst_frac=0.20, xsec=7e3),
    MCSample('qcdpt300mupt5_2017',  '/QCD_Pt-300To470_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v9-v2/AODSIM', 58692910, nice='QCD, 470 GeV > #hat{p}_{T} > 300 GeV, #mu p_{T} > 5 GeV', color=801, syst_frac=0.20, xsec=6.226e2),
    MCSample('qcdpt470mupt5_2017',  '/QCD_Pt-470To600_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v9-v2/AODSIM', 39491752, nice='QCD, 600 GeV > #hat{p}_{T} > 470 GeV, #mu p_{T} > 5 GeV', color=801, syst_frac=0.20, xsec=58.9),
    MCSample('qcdpt600mupt5_2017',  '/QCD_Pt-600To800_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v9-v2/AODSIM', 39321940, nice='QCD, 800 GeV > #hat{p}_{T} > 600 GeV, #mu p_{T} > 5 GeV', color=801, syst_frac=0.20, xsec=18.12),
    MCSample('qcdpt800mupt5_2017',  '/QCD_Pt-800To1000_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v9-v2/AODSIM', 78215559, nice='QCD, 1 TeV GeV > #hat{p}_{T} > 800 GeV, #mu p_{T} > 5 GeV', color=801, syst_frac=0.20, xsec=3.318),
    MCSample('qcdpt1000mupt5_2017',  '/QCD_Pt-1000_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v9-v2/AODSIM', 27478273, nice='QCD, #hat{p}_{T} > 1 TeV, #mu p_{T} > 5 GeV', color=801, syst_frac=0.20, xsec=1.085),
    #MCSample('qcdempt015_2017', '/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v1/AODSIM',   7966910, nice='QCD,  15 < #hat{p}_{T} <  20 GeV, EM enriched', color=801, syst_frac=0.20, xsec=1.324e6), #Alec commented from here
    #MCSample('qcdempt020_2017', '/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v1/AODSIM',   14166147, nice='QCD,  20 < #hat{p}_{T} <  30 GeV, EM enriched', color=801, syst_frac=0.20, xsec=4.896e6),
    #MCSample('qcdempt030_2017', '/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v2/AODSIM',   8784542, nice='QCD,  30 < #hat{p}_{T} <  50 GeV, EM enriched', color=801, syst_frac=0.20, xsec=6.447e6),
    #MCSample('qcdempt050_2017', '/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v2/AODSIM',   10590542, nice='QCD,  50 < #hat{p}_{T} <  80 GeV, EM enriched', color=801, syst_frac=0.20, xsec=1.988e6),
    #MCSample('qcdempt080_2017', '/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v2/AODSIM',   9615795, nice='QCD,  80 < #hat{p}_{T} < 120 GeV, EM enriched', color=801, syst_frac=0.20, xsec=3.675e5),
    #MCSample('qcdempt120_2017', '/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v2/AODSIM',  9904245, nice='QCD, 120 < #hat{p}_{T} < 170 GeV, EM enriched', color=801, syst_frac=0.20, xsec=6.659e4),
    #MCSample('qcdempt170_2017', '/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v2/AODSIM',  3678200, nice='QCD, 170 < #hat{p}_{T} < 300 GeV, EM enriched', color=801, syst_frac=0.20, xsec=1.662e4),
    #MCSample('qcdempt300_2017', '/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v2/AODSIM',  2214934, nice='QCD, #hat{p}_{T} > 300 GeV, EM enriched',       color=801, syst_frac=0.20, xsec=1104.0), #Alec to here
    MCSample('qcdempt015_2017', '/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM',   7966910, nice='QCD,  15 < #hat{p}_{T} <  20 GeV, EM enriched', color=801, syst_frac=0.20, xsec=1.324e6), #Alec added from here 
    MCSample('qcdempt020_2017', '/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM',   14166147, nice='QCD,  20 < #hat{p}_{T} <  30 GeV, EM enriched', color=801, syst_frac=0.20, xsec=4.896e6),
    MCSample('qcdempt030_2017', '/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM',   8784542, nice='QCD,  30 < #hat{p}_{T} <  50 GeV, EM enriched', color=801, syst_frac=0.20, xsec=6.447e6),
    MCSample('qcdempt050_2017', '/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM',   10590542, nice='QCD,  50 < #hat{p}_{T} <  80 GeV, EM enriched', color=801, syst_frac=0.20, xsec=1.988e6),
    MCSample('qcdempt080_2017', '/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM',   9615795, nice='QCD,  80 < #hat{p}_{T} < 120 GeV, EM enriched', color=801, syst_frac=0.20, xsec=3.675e5),
    MCSample('qcdempt120_2017', '/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM',  9904245, nice='QCD, 120 < #hat{p}_{T} < 170 GeV, EM enriched', color=801, syst_frac=0.20, xsec=6.659e4),
    MCSample('qcdempt170_2017', '/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM',  3678200, nice='QCD, 170 < #hat{p}_{T} < 300 GeV, EM enriched', color=801, syst_frac=0.20, xsec=1.662e4),
    MCSample('qcdempt300_2017', '/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM',  2214934, nice='QCD, #hat{p}_{T} > 300 GeV, EM enriched',       color=801, syst_frac=0.20, xsec=1104.0), #Alec to here  
    #MCSample('qcdbctoept020_2017', '/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v2/AODSIM',      14248556, nice='QCD,  20 < #hat{p}_{T} <  30 GeV, HF electrons', color=801, syst_frac=0.20, xsec=3.038e5), #Alec commented from here
    #MCSample('qcdbctoept030_2017', '/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v2/AODSIM',      15656025, nice='QCD,  30 < #hat{p}_{T} <  80 GeV, HF electrons', color=801, syst_frac=0.20, xsec=3.623e5),
    #MCSample('qcdbctoept080_2017', '/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v2/AODSIM',     16158199, nice='QCD,  80 < #hat{p}_{T} < 170 GeV, HF electrons', color=801, syst_frac=0.20, xsec=3.37e4),
    #MCSample('qcdbctoept170_2017', '/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v2/AODSIM',    15940531, nice='QCD, 170 < #hat{p}_{T} < 250 GeV, HF electrons', color=801, syst_frac=0.20, xsec=2.125e3),
    #MCSample('qcdbctoept250_2017', '/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v3/AODSIM',    16028600, nice='QCD, #hat{p}_{T} > 250 GeV, HF electrons',       color=801, syst_frac=0.20, xsec=562.5), #Alec to here
    MCSample('qcdbctoept020_2017', '/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM',      14248556, nice='QCD,  20 < #hat{p}_{T} <  30 GeV, HF electrons', color=801, syst_frac=0.20, xsec=3.038e5), #Alec add from here 
    MCSample('qcdbctoept030_2017', '/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM',      15656025, nice='QCD,  30 < #hat{p}_{T} <  80 GeV, HF electrons', color=801, syst_frac=0.20, xsec=3.623e5),
    MCSample('qcdbctoept080_2017', '/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM',     16158199, nice='QCD,  80 < #hat{p}_{T} < 170 GeV, HF electrons', color=801, syst_frac=0.20, xsec=3.37e4),
    MCSample('qcdbctoept170_2017', '/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM',    15940531, nice='QCD, 170 < #hat{p}_{T} < 250 GeV, HF electrons', color=801, syst_frac=0.20, xsec=2.125e3),
    MCSample('qcdbctoept250_2017', '/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v3/MINIAODSIM',    16028600, nice='QCD, #hat{p}_{T} > 250 GeV, HF electrons',       color=801, syst_frac=0.20, xsec=562.5), #Alec to here
    ]
    
# ttbar with HT slices not available for UL now
ttbar_samples_2017 = [
    MCSample('ttbar_2017',     '/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/AODSIM',  249133364, nice='t#bar{t}', color=4,   syst_frac=0.15, xsec=831.76),
]
bjet_samples_2017 = [
    ]

leptonic_samples_2017 = [
    MCSample('wjetstolnu_0j_2017','/WJetsToLNu_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM', 169421340, nice='W + jets #rightarrow l#nu', color= 38, syst_fac=0.10, xsec=52.78e3),
    MCSample('wjetstolnu_1j_2017','/WJetsToLNu_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 180015088, nice='W + jets #rightarrow l#nu', color= 38, syst_fac=0.10, xsec=8.832e3),
    MCSample('wjetstolnu_2j_2017','/WJetsToLNu_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM', 96032711, nice='W + jets #rightarrow l#nu', color= 38, syst_fac=0.10, xsec=3.276e3),
    MCSample('dyjetstollM10_2017',    '/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/AODSIM',                  68480179, nice='DY + jets #rightarrow ll, 10 < M < 50 GeV', color= 29, syst_frac=0.10, xsec=1.58e4),
    MCSample('dyjetstollM50_2017',    '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/AODSIM',          103344974, nice='DY + jets #rightarrow ll, M > 50 GeV', color= 32, syst_frac=0.10, xsec=5.34e3),
    ]

example_samples_ttbar_2017 = [
    MCSample('example_ttbar_2017',     '/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/AODSIM',  249133364, nice='t#bar{t}',                   color=4,   syst_frac=0.15, xsec=831.76), 
    ]

example_samples_zz_2017 = [
    MCSample('example_zz_2017', '/ZZ_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2/MINIAODSIM', 2708000, nice='ZZ', color = 9, syst_frac=0.10, xsec=12.140),
    ]

met_samples_2017 = [
    #MCSample('ttbar_2017',     '/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v2/AODSIM',    249133364, nice='t#bar{t}',                   color=4,   syst_frac=0.15, xsec=831.76),
    #MCSample('ttbar_2017',     '/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/AODSIM',  249133364, nice='t#bar{t}',                   color=4,   syst_frac=0.15, xsec=831.76), Alec commented this line
    ]

diboson_samples_2017 = [
    #MCSample('ww_2017', '/WW_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2/MINIAODSIM', 15883000, nice='WW', color = 9, syst_frac=0.10, xsec=75.8),Alec commented here
    #MCSample('zz_2017', '/ZZ_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2/MINIAODSIM', 2708000, nice='ZZ', color = 9, syst_frac=0.10, xsec=12.140),
    #MCSample('wz_2017', '/WZ_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2/MINIAODSIM', 7898000, nice='WZ', color =9, syst_frac=0.10, xsec=27.6) Alec to here
    MCSample('ww_2017', '/WW_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM', 15883000, nice='WW', color = 9, syst_frac=0.10, xsec=75.8),
    MCSample('zz_2017', '/ZZ_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM', 2708000, nice='ZZ', color = 9, syst_frac=0.10, xsec=12.140),
    MCSample('wz_2017', '/WZ_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM', 7898000, nice='WZ', color =9, syst_frac=0.10, xsec=27.6)
    ]

Zvv_samples_2017 = [
    MCSample('zjetstonunuht0100_2017', '/ZJetsToNuNu_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v1/AODSIM', 19141242, nice='Z + jets #rightarrow #nu #nu 100 < H_{T} < 200 GeV', color=1, syst_frac=0.20, xsec=302.8),
    MCSample('zjetstonunuht0200_2017', '/ZJetsToNuNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v1/AODSIM', 17468549, nice='Z + jets #rightarrow #nu #nu 200 < H_{T} < 400 GeV', color=1, syst_frac=0.20, xsec=92.59),
    MCSample('zjetstonunuht0400_2017', '/ZJetsToNuNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v1/AODSIM', 13963690, nice='Z + jets #rightarrow #nu #nu 400 < H_{T} < 600 GeV', color=1, syst_frac=0.20, xsec=13.18),
    MCSample('zjetstonunuht0600_2017', '/ZJetsToNuNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v1/AODSIM', 4418971, nice='Z + jets #rightarrow #nu #nu 600 < H_{T} < 800 GeV', color=1, syst_frac=0.20, xsec=3.257),
    MCSample('zjetstonunuht0800_2017', '/ZJetsToNuNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v1/AODSIM', 1513585, nice='Z + jets #rightarrow #nu #nu 800 < H_{T} < 1200 GeV', color=1, syst_frac=0.20, xsec=1.49),
    MCSample('zjetstonunuht1200_2017', '/ZJetsToNuNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v1/AODSIM', 267125, nice='Z + jets #rightarrow #nu #nu 1200 < H_{T} < 2500 GeV', color=1, syst_frac=0.20, xsec=0.3419),
    MCSample('zjetstonunuht2500_2017', '/ZJetsToNuNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v1/AODSIM', 176201, nice='Z + jets #rightarrow #nu #nu H_{T} > 2500 GeV', color=1, syst_frac=0.20, xsec=0.005146),
    ]

mfv_splitSUSY_samples_2017 = [
  MCSample('mfv_splitSUSY_tau000001000um_M1400_1200_2017', '/mfv_splitSUSY_tau000001000um_M1400_1200_2017/None/USER', 10000),
  MCSample('mfv_splitSUSY_tau000010000um_M1400_1200_2017', '/mfv_splitSUSY_tau000010000um_M1400_1200_2017/None/USER', 10000),
  MCSample('mfv_splitSUSY_tau000001000um_M1200_1100_2017', '/mfv_splitSUSY_tau000001000um_M1200_1100_2017/None/USER', 10000),
  MCSample('mfv_splitSUSY_tau000010000um_M1200_1100_2017', '/mfv_splitSUSY_tau000010000um_M1200_1100_2017/None/USER', 10000),
  MCSample('mfv_splitSUSY_tau000000100um_M2000_1800_2017', '/mfv_splitSUSY_tau000000100um_M2000_1800_2017/None/USER', 10000),
  MCSample('mfv_splitSUSY_tau000000300um_M2000_1800_2017', '/mfv_splitSUSY_tau000000300um_M2000_1800_2017/None/USER', 10000),
  MCSample('mfv_splitSUSY_tau000010000um_M2000_1800_2017', '/mfv_splitSUSY_tau000010000um_M2000_1800_2017/None/USER', 10000),
  MCSample('mfv_splitSUSY_tau000001000um_M2000_1800_2017', '/mfv_splitSUSY_tau000001000um_M2000_1800_2017/None/USER', 10000),
  MCSample('mfv_splitSUSY_tau000000100um_M2000_1900_2017', '/mfv_splitSUSY_tau000000100um_M2000_1900_2017/None/USER', 10000),
  MCSample('mfv_splitSUSY_tau000000300um_M2000_1900_2017', '/mfv_splitSUSY_tau000000300um_M2000_1900_2017/None/USER', 10000),
  MCSample('mfv_splitSUSY_tau000010000um_M2000_1900_2017', '/mfv_splitSUSY_tau000010000um_M2000_1900_2017/None/USER', 10000),
  MCSample('mfv_splitSUSY_tau000001000um_M2000_1900_2017', '/mfv_splitSUSY_tau000001000um_M2000_1900_2017/None/USER', 10000),
  MCSample('mfv_splitSUSY_tau000000100um_M2400_100_2017', '/mfv_splitSUSY_tau000000100um_M2400_100_2017/None/USER', 10000),
  MCSample('mfv_splitSUSY_tau000000300um_M2400_100_2017', '/mfv_splitSUSY_tau000000300um_M2400_100_2017/None/USER', 10000),
  MCSample('mfv_splitSUSY_tau000010000um_M2400_100_2017', '/mfv_splitSUSY_tau000010000um_M2400_100_2017/None/USER', 10000),
  MCSample('mfv_splitSUSY_tau000001000um_M2400_100_2017', '/mfv_splitSUSY_tau000001000um_M2400_100_2017/None/USER', 10000),
  MCSample('mfv_splitSUSY_tau000000100um_M2400_2300_2017', '/mfv_splitSUSY_tau000000100um_M2400_2300_2017/None/USER', 10000),
  MCSample('mfv_splitSUSY_tau000000300um_M2400_2300_2017', '/mfv_splitSUSY_tau000000300um_M2400_2300_2017/None/USER', 10000),
  MCSample('mfv_splitSUSY_tau000010000um_M2400_2300_2017', '/mfv_splitSUSY_tau000010000um_M2400_2300_2017/None/USER', 10000),
  MCSample('mfv_splitSUSY_tau000001000um_M2400_2300_2017', '/mfv_splitSUSY_tau000001000um_M2400_2300_2017/None/USER', 10000),
]

#FIXME: Temporary, privately-produced samples for some masses/lifetimes
mfv_signal_samples_2017 = [
    MCSample('mfv_neu_tau000300um_M0300_2017', '/mfv_neu_tau000300um_M0300_2017/None/USER', 6400),
    MCSample('mfv_neu_tau000300um_M0600_2017', '/mfv_neu_tau000300um_M0600_2017/None/USER', 6400),
    MCSample('mfv_neu_tau000300um_M0800_2017', '/mfv_neu_tau000300um_M0800_2017/None/USER', 3200),
    MCSample('mfv_neu_tau001000um_M0300_2017', '/mfv_neu_tau001000um_M0300_2017/None/USER', 8000),
    MCSample('mfv_neu_tau001000um_M0600_2017', '/mfv_neu_tau001000um_M0600_2017/None/USER', 3200),
    MCSample('mfv_neu_tau001000um_M0800_2017', '/mfv_neu_tau001000um_M0800_2017/None/USER', 4800),
]


#FIXME: Temporary, privately-produced samples for some masses/lifetimes
mfv_stopdbardbar_samples_2017 = [
    MCSample('mfv_stopdbardbar_tau000300um_M0300_2017', 'mfv_stopdbardbar_tau000300um_M0300_2017/None/USER', 8000),
    MCSample('mfv_stopdbardbar_tau000300um_M0600_2017', 'mfv_stopdbardbar_tau000300um_M0600_2017/None/USER', 4800),
    MCSample('mfv_stopdbardbar_tau000300um_M0800_2017', 'mfv_stopdbardbar_tau000300um_M0800_2017/None/USER', 4800),
    MCSample('mfv_stopdbardbar_tau001000um_M0300_2017', 'mfv_stopdbardbar_tau001000um_M0300_2017/None/USER', 6400),
    MCSample('mfv_stopdbardbar_tau001000um_M0600_2017', 'mfv_stopdbardbar_tau001000um_M0600_2017/None/USER', 6400),
    MCSample('mfv_stopdbardbar_tau001000um_M0800_2017', 'mfv_stopdbardbar_tau001000um_M0800_2017/None/USER', 8000),
]


#FIXME: Temporary, privately-produced samples for some masses/lifetimes
mfv_stopbbarbbar_samples_2017 = [
    MCSample('mfv_stopbbarbbar_tau000300um_M0300_2017', 'mfv_stopbbarbbar_tau000300um_M0300_2017/None/USER', 4800),
    MCSample('mfv_stopbbarbbar_tau000300um_M0600_2017', 'mfv_stopbbarbbar_tau000300um_M0600_2017/None/USER', 6400),
    MCSample('mfv_stopbbarbbar_tau000300um_M0800_2017', 'mfv_stopbbarbbar_tau000300um_M0800_2017/None/USER', 4800),
    MCSample('mfv_stopbbarbbar_tau001000um_M0300_2017', 'mfv_stopbbarbbar_tau001000um_M0300_2017/None/USER', 8000),
    MCSample('mfv_stopbbarbbar_tau001000um_M0600_2017', 'mfv_stopbbarbbar_tau001000um_M0600_2017/None/USER', 4800),
    MCSample('mfv_stopbbarbbar_tau001000um_M0800_2017', 'mfv_stopbbarbbar_tau001000um_M0800_2017/None/USER', 6400),
]

mfv_stoplb_samples_2017 = [
    MCSample('mfv_stoplb_tau000100um_M1000_2017', '/DisplacedSUSY_stopToLBottom_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 194928),
    MCSample('mfv_stoplb_tau000300um_M1000_2017', '/DisplacedSUSY_stopToLBottom_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 200301),
    MCSample('mfv_stoplb_tau010000um_M1000_2017', '/DisplacedSUSY_stopToLBottom_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 98261),
    MCSample('mfv_stoplb_tau001000um_M1000_2017', '/DisplacedSUSY_stopToLBottom_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 197193),
    MCSample('mfv_stoplb_tau030000um_M1000_2017', '/DisplacedSUSY_stopToLBottom_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 200668),
    MCSample('mfv_stoplb_tau000100um_M1200_2017', '/DisplacedSUSY_stopToLBottom_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 199921),
    MCSample('mfv_stoplb_tau000300um_M1200_2017', '/DisplacedSUSY_stopToLBottom_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 195189),
    MCSample('mfv_stoplb_tau010000um_M1200_2017', '/DisplacedSUSY_stopToLBottom_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 100156),
    MCSample('mfv_stoplb_tau001000um_M1200_2017', '/DisplacedSUSY_stopToLBottom_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 197902),
    MCSample('mfv_stoplb_tau030000um_M1200_2017', '/DisplacedSUSY_stopToLBottom_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 200464),
    MCSample('mfv_stoplb_tau000100um_M1400_2017', '/DisplacedSUSY_stopToLBottom_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 199322),
    MCSample('mfv_stoplb_tau000300um_M1400_2017', '/DisplacedSUSY_stopToLBottom_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 200304),
    MCSample('mfv_stoplb_tau010000um_M1400_2017', '/DisplacedSUSY_stopToLBottom_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 98900),
    MCSample('mfv_stoplb_tau001000um_M1400_2017', '/DisplacedSUSY_stopToLBottom_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 196297),
    MCSample('mfv_stoplb_tau030000um_M1400_2017', '/DisplacedSUSY_stopToLBottom_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 198644),
    MCSample('mfv_stoplb_tau000100um_M1600_2017', '/DisplacedSUSY_stopToLBottom_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 202021),
    MCSample('mfv_stoplb_tau000300um_M1600_2017', '/DisplacedSUSY_stopToLBottom_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 199079),
    MCSample('mfv_stoplb_tau010000um_M1600_2017', '/DisplacedSUSY_stopToLBottom_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 98745),
    MCSample('mfv_stoplb_tau001000um_M1600_2017', '/DisplacedSUSY_stopToLBottom_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 98921),
    MCSample('mfv_stoplb_tau030000um_M1600_2017', '/DisplacedSUSY_stopToLBottom_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 100284),
    MCSample('mfv_stoplb_tau000100um_M1800_2017', '/DisplacedSUSY_stopToLBottom_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 199639),
    MCSample('mfv_stoplb_tau000300um_M1800_2017', '/DisplacedSUSY_stopToLBottom_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 200792),
    MCSample('mfv_stoplb_tau010000um_M1800_2017', '/DisplacedSUSY_stopToLBottom_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 101386),
    MCSample('mfv_stoplb_tau001000um_M1800_2017', '/DisplacedSUSY_stopToLBottom_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 98858),
    MCSample('mfv_stoplb_tau030000um_M1800_2017', '/DisplacedSUSY_stopToLBottom_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 100172),
    MCSample('mfv_stoplb_tau000100um_M0200_2017', '/DisplacedSUSY_stopToLBottom_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 198760),
    MCSample('mfv_stoplb_tau000300um_M0200_2017', '/DisplacedSUSY_stopToLBottom_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 198899),
    MCSample('mfv_stoplb_tau010000um_M0200_2017', '/DisplacedSUSY_stopToLBottom_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 199948),
    MCSample('mfv_stoplb_tau001000um_M0200_2017', '/DisplacedSUSY_stopToLBottom_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 196687),
    MCSample('mfv_stoplb_tau030000um_M0200_2017', '/DisplacedSUSY_stopToLBottom_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 199267),
    MCSample('mfv_stoplb_tau000100um_M0300_2017', '/DisplacedSUSY_stopToLBottom_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 198231),
    MCSample('mfv_stoplb_tau000300um_M0300_2017', '/DisplacedSUSY_stopToLBottom_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 198170),
    MCSample('mfv_stoplb_tau010000um_M0300_2017', '/DisplacedSUSY_stopToLBottom_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 199832),
    MCSample('mfv_stoplb_tau001000um_M0300_2017', '/DisplacedSUSY_stopToLBottom_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 200296),
    MCSample('mfv_stoplb_tau030000um_M0300_2017', '/DisplacedSUSY_stopToLBottom_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 200170),
    MCSample('mfv_stoplb_tau000100um_M0400_2017', '/DisplacedSUSY_stopToLBottom_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 197597),
    MCSample('mfv_stoplb_tau000300um_M0400_2017', '/DisplacedSUSY_stopToLBottom_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 200230),
    MCSample('mfv_stoplb_tau010000um_M0400_2017', '/DisplacedSUSY_stopToLBottom_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 198737),
    MCSample('mfv_stoplb_tau001000um_M0400_2017', '/DisplacedSUSY_stopToLBottom_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 197003),
    MCSample('mfv_stoplb_tau030000um_M0400_2017', '/DisplacedSUSY_stopToLBottom_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 198930),
    MCSample('mfv_stoplb_tau000100um_M0600_2017', '/DisplacedSUSY_stopToLBottom_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 201812),
    MCSample('mfv_stoplb_tau000300um_M0600_2017', '/DisplacedSUSY_stopToLBottom_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 201839),
    MCSample('mfv_stoplb_tau010000um_M0600_2017', '/DisplacedSUSY_stopToLBottom_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 197409),
    MCSample('mfv_stoplb_tau001000um_M0600_2017', '/DisplacedSUSY_stopToLBottom_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 195368),
    MCSample('mfv_stoplb_tau030000um_M0600_2017', '/DisplacedSUSY_stopToLBottom_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 200005),
    MCSample('mfv_stoplb_tau000100um_M0800_2017', '/DisplacedSUSY_stopToLBottom_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 198566),
    MCSample('mfv_stoplb_tau000300um_M0800_2017', '/DisplacedSUSY_stopToLBottom_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 197615),
    MCSample('mfv_stoplb_tau010000um_M0800_2017', '/DisplacedSUSY_stopToLBottom_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 98799),
    MCSample('mfv_stoplb_tau001000um_M0800_2017', '/DisplacedSUSY_stopToLBottom_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 197479),
    MCSample('mfv_stoplb_tau030000um_M0800_2017', '/DisplacedSUSY_stopToLBottom_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 201690),
]

mfv_stopld_samples_2017 = [
    MCSample('mfv_stopld_tau000100um_M1000_2017', '/DisplacedSUSY_stopToLD_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 199076),
    MCSample('mfv_stopld_tau000300um_M1000_2017', '/DisplacedSUSY_stopToLD_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 198992),
    MCSample('mfv_stopld_tau010000um_M1000_2017', '/DisplacedSUSY_stopToLD_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 98679),
    MCSample('mfv_stopld_tau001000um_M1000_2017', '/DisplacedSUSY_stopToLD_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 198608),
    MCSample('mfv_stopld_tau030000um_M1000_2017', '/DisplacedSUSY_stopToLD_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v3/MINIAODSIM', 199499),
    MCSample('mfv_stopld_tau000100um_M1200_2017', '/DisplacedSUSY_stopToLD_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 198263),
    MCSample('mfv_stopld_tau000300um_M1200_2017', '/DisplacedSUSY_stopToLD_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v3/MINIAODSIM', 0),
    MCSample('mfv_stopld_tau010000um_M1200_2017', '/DisplacedSUSY_stopToLD_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 100349),
    MCSample('mfv_stopld_tau001000um_M1200_2017', '/DisplacedSUSY_stopToLD_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 201191),
    MCSample('mfv_stopld_tau030000um_M1200_2017', '/DisplacedSUSY_stopToLD_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 200851),
    MCSample('mfv_stopld_tau000100um_M1400_2017', '/DisplacedSUSY_stopToLD_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 198812),
    MCSample('mfv_stopld_tau000300um_M1400_2017', '/DisplacedSUSY_stopToLD_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 194591),
    MCSample('mfv_stopld_tau010000um_M1400_2017', '/DisplacedSUSY_stopToLD_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 98583),
    MCSample('mfv_stopld_tau001000um_M1400_2017', '/DisplacedSUSY_stopToLD_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 198538),
    MCSample('mfv_stopld_tau030000um_M1400_2017', '/DisplacedSUSY_stopToLD_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 200714),
    MCSample('mfv_stopld_tau000100um_M1600_2017', '/DisplacedSUSY_stopToLD_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 201051),
    MCSample('mfv_stopld_tau000300um_M1600_2017', '/DisplacedSUSY_stopToLD_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 196540),
    MCSample('mfv_stopld_tau010000um_M1600_2017', '/DisplacedSUSY_stopToLD_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 100274),
    MCSample('mfv_stopld_tau001000um_M1600_2017', '/DisplacedSUSY_stopToLD_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 99126),
    MCSample('mfv_stopld_tau030000um_M1600_2017', '/DisplacedSUSY_stopToLD_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 100345),
    MCSample('mfv_stopld_tau000100um_M1800_2017', '/DisplacedSUSY_stopToLD_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 200828),
    MCSample('mfv_stopld_tau000300um_M1800_2017', '/DisplacedSUSY_stopToLD_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 198147),
    MCSample('mfv_stopld_tau010000um_M1800_2017', '/DisplacedSUSY_stopToLD_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 99667),
    MCSample('mfv_stopld_tau001000um_M1800_2017', '/DisplacedSUSY_stopToLD_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 101005),
    MCSample('mfv_stopld_tau030000um_M1800_2017', '/DisplacedSUSY_stopToLD_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 99787),
    MCSample('mfv_stopld_tau000100um_M0200_2017', '/DisplacedSUSY_stopToLD_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 201843),
    MCSample('mfv_stopld_tau000300um_M0200_2017', '/DisplacedSUSY_stopToLD_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 199789),
    MCSample('mfv_stopld_tau010000um_M0200_2017', '/DisplacedSUSY_stopToLD_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 197403),
    MCSample('mfv_stopld_tau001000um_M0200_2017', '/DisplacedSUSY_stopToLD_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 198275),
    MCSample('mfv_stopld_tau030000um_M0200_2017', '/DisplacedSUSY_stopToLD_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 198511),
    MCSample('mfv_stopld_tau000100um_M0300_2017', '/DisplacedSUSY_stopToLD_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 197379),
    MCSample('mfv_stopld_tau000300um_M0300_2017', '/DisplacedSUSY_stopToLD_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 197934),
    MCSample('mfv_stopld_tau010000um_M0300_2017', '/DisplacedSUSY_stopToLD_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 197990),
    MCSample('mfv_stopld_tau001000um_M0300_2017', '/DisplacedSUSY_stopToLD_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 199705),
    MCSample('mfv_stopld_tau030000um_M0300_2017', '/DisplacedSUSY_stopToLD_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 199931),
    MCSample('mfv_stopld_tau000100um_M0400_2017', '/DisplacedSUSY_stopToLD_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 202735),
    MCSample('mfv_stopld_tau000300um_M0400_2017', '/DisplacedSUSY_stopToLD_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 199890),
    MCSample('mfv_stopld_tau010000um_M0400_2017', '/DisplacedSUSY_stopToLD_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 201845),
    MCSample('mfv_stopld_tau001000um_M0400_2017', '/DisplacedSUSY_stopToLD_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 197130),
    MCSample('mfv_stopld_tau030000um_M0400_2017', '/DisplacedSUSY_stopToLD_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 198731),
    MCSample('mfv_stopld_tau000100um_M0600_2017', '/DisplacedSUSY_stopToLD_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 203406),
    MCSample('mfv_stopld_tau000300um_M0600_2017', '/DisplacedSUSY_stopToLD_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 199321),
    MCSample('mfv_stopld_tau010000um_M0600_2017', '/DisplacedSUSY_stopToLD_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 195818),
    MCSample('mfv_stopld_tau001000um_M0600_2017', '/DisplacedSUSY_stopToLD_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 203302),
    MCSample('mfv_stopld_tau030000um_M0600_2017', '/DisplacedSUSY_stopToLD_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 199944),
    MCSample('mfv_stopld_tau000100um_M0800_2017', '/DisplacedSUSY_stopToLD_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 200077),
    MCSample('mfv_stopld_tau000300um_M0800_2017', '/DisplacedSUSY_stopToLD_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 200814),
    MCSample('mfv_stopld_tau010000um_M0800_2017', '/DisplacedSUSY_stopToLD_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 99313),
    MCSample('mfv_stopld_tau001000um_M0800_2017', '/DisplacedSUSY_stopToLD_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 200829),
    MCSample('mfv_stopld_tau030000um_M0800_2017', '/DisplacedSUSY_stopToLD_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 200140),
]

HToSSTobbbb_samples_2017 = [
    #MCSample('ggHToSSTobbbb_tau1000mm_M15_2017', '/ggH_HToSSTobbbb_MH-125_MS-15_ctauS-1000_pT75_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 159693),
    #MCSample('ggHToSSTobbbb_tau100mm_M15_2017',  '/ggH_HToSSTobbbb_MH-125_MS-15_ctauS-100_pT75_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 159747),
    #MCSample('ggHToSSTobbbb_tau10mm_M15_2017',   '/ggH_HToSSTobbbb_MH-125_MS-15_ctauS-10_pT75_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 157205),
    #MCSample('ggHToSSTobbbb_tau1mm_M15_2017',    '/ggH_HToSSTobbbb_MH-125_MS-15_ctauS-1_pT75_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 168529),
    #MCSample('ggHToSSTobbbb_tau1000mm_M40_2017', '/ggH_HToSSTobbbb_MH-125_MS-40_ctauS-1000_pT75_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 168492),
    #MCSample('ggHToSSTobbbb_tau100mm_M40_2017',  '/ggH_HToSSTobbbb_MH-125_MS-40_ctauS-100_pT75_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 161541),
    #MCSample('ggHToSSTobbbb_tau10mm_M40_2017',   '/ggH_HToSSTobbbb_MH-125_MS-40_ctauS-10_pT75_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 174041),
    #MCSample('ggHToSSTobbbb_tau1mm_M40_2017',    '/ggH_HToSSTobbbb_MH-125_MS-40_ctauS-1_pT75_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 155202),
    #MCSample('ggHToSSTobbbb_tau1000mm_M55_2017', '/ggH_HToSSTobbbb_MH-125_MS-55_ctauS-1000_pT75_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 200804),
    #MCSample('ggHToSSTobbbb_tau100mm_M55_2017',  '/ggH_HToSSTobbbb_MH-125_MS-55_ctauS-100_pT75_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 174229),
    #MCSample('ggHToSSTobbbb_tau10mm_M55_2017',   '/ggH_HToSSTobbbb_MH-125_MS-55_ctauS-10_pT75_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 163136),
    #MCSample('ggHToSSTobbbb_tau1mm_M55_2017',    '/ggH_HToSSTobbbb_MH-125_MS-55_ctauS-1_pT75_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 182247),
]

HToSSTodddd_samples_2017 = [
    #MCSample('ggHToSSTodddd_tau1000mm_M15_2017', '/ggH_HToSSTodddd_MH-125_MS-15_ctauS-1000_pT75_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 164515),
    #MCSample('ggHToSSTodddd_tau100mm_M15_2017',  '/ggH_HToSSTodddd_MH-125_MS-15_ctauS-100_pT75_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 160691),
    #MCSample('ggHToSSTodddd_tau10mm_M15_2017',   '/ggH_HToSSTodddd_MH-125_MS-15_ctauS-10_pT75_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 202418),
    #MCSample('ggHToSSTodddd_tau1mm_M15_2017',    '/ggH_HToSSTodddd_MH-125_MS-15_ctauS-1_pT75_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 170288),
    #MCSample('ggHToSSTodddd_tau1000mm_M40_2017', '/ggH_HToSSTodddd_MH-125_MS-40_ctauS-1000_pT75_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 200772),
    #MCSample('ggHToSSTodddd_tau100mm_M40_2017',  '/ggH_HToSSTodddd_MH-125_MS-40_ctauS-100_pT75_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 178325),
    #MCSample('ggHToSSTodddd_tau10mm_M40_2017',   '/ggH_HToSSTodddd_MH-125_MS-40_ctauS-10_pT75_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 191158),
    #MCSample('ggHToSSTodddd_tau1mm_M40_2017',    '/ggH_HToSSTodddd_MH-125_MS-40_ctauS-1_pT75_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 176899),
    #MCSample('ggHToSSTodddd_tau1000mm_M55_2017', '/ggH_HToSSTodddd_MH-125_MS-55_ctauS-1000_pT75_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 233111),
    #MCSample('ggHToSSTodddd_tau100mm_M55_2017',  '/ggH_HToSSTodddd_MH-125_MS-55_ctauS-100_pT75_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 186454),
    #MCSample('ggHToSSTodddd_tau10mm_M55_2017',   '/ggH_HToSSTodddd_MH-125_MS-55_ctauS-10_pT75_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 171704),
    #MCSample('ggHToSSTodddd_tau1mm_M55_2017',    '/ggH_HToSSTodddd_MH-125_MS-55_ctauS-1_pT75_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 186554),
]

ggHToSSTo4l_samples_2017 = [
    MCSample('ggHToSSTo4l_tau1mm_M350_2017', '/ggH_HToSSTo4l_lowctau_MH-800_MS-350_ctauS-1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 49643),
]

ZHToSSTodddd_samples_2017 = [ 
    MCSample('ZHToSSTodddd_tau100um_M15_2017', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-15_ctauS-0p1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 49121), 
    MCSample('ZHToSSTodddd_tau300um_M15_2017', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-15_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 50000), 
    MCSample('ZHToSSTodddd_tau1mm_M15_2017', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-15_ctauS-1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 49999), 
    MCSample('ZHToSSTodddd_tau3mm_M15_2017', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-15_ctauS-3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 50000), 
    MCSample('ZHToSSTodddd_tau10mm_M15_2017', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-15_ctauS-10_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 50000), 
    MCSample('ZHToSSTodddd_tau30mm_M15_2017', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-15_ctauS-30_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 49999), 

    MCSample('ZHToSSTodddd_tau100um_M40_2017', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-40_ctauS-0p1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 49999), 
    MCSample('ZHToSSTodddd_tau300um_M40_2017', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-40_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 49999), 
    MCSample('ZHToSSTodddd_tau1mm_M40_2017', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-40_ctauS-1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 50000), 
    MCSample('ZHToSSTodddd_tau3mm_M40_2017', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-40_ctauS-3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 49996), 
    MCSample('ZHToSSTodddd_tau10mm_M40_2017', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-40_ctauS-10_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 49998), 
    MCSample('ZHToSSTodddd_tau30mm_M40_2017', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-40_ctauS-30_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 50000), 

    MCSample('ZHToSSTodddd_tau100um_M55_2017', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-55_ctauS-0p1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM', 49999), 
    MCSample('ZHToSSTodddd_tau300um_M55_2017', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-55_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM', 49997), 
    MCSample('ZHToSSTodddd_tau1mm_M55_2017', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 49997), 
    MCSample('ZHToSSTodddd_tau3mm_M55_2017', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-55_ctauS-3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 49995), 
    MCSample('ZHToSSTodddd_tau10mm_M55_2017', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-55_ctauS-10_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 49991), 
    MCSample('ZHToSSTodddd_tau30mm_M55_2017', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-55_ctauS-30_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 49998), 
]

WplusHToSSTodddd_samples_2017 = [
    MCSample('WplusHToSSTodddd_tau100um_M15_2017', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-0p1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 50000), 
    MCSample('WplusHToSSTodddd_tau300um_M15_2017', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 49000), 
    MCSample('WplusHToSSTodddd_tau1mm_M15_2017', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 49999), 
    MCSample('WplusHToSSTodddd_tau3mm_M15_2017', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 50000), 
    MCSample('WplusHToSSTodddd_tau30mm_M15_2017', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-30_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 50000), 
    
    #No WplusHToSSTodddd_tau100um_M40_2017
    MCSample('WplusHToSSTodddd_tau300um_M40_2017', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 49996), 
    MCSample('WplusHToSSTodddd_tau1mm_M40_2017', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 49999), 
    MCSample('WplusHToSSTodddd_tau3mm_M40_2017', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 48000), 
    MCSample('WplusHToSSTodddd_tau30mm_M40_2017', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-30_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 49997), 

    MCSample('WplusHToSSTodddd_tau100um_M55_2017', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-0p1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 49997), 
    MCSample('WplusHToSSTodddd_tau300um_M55_2017', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 49995), 
    MCSample('WplusHToSSTodddd_tau1mm_M55_2017', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 49991), 
    MCSample('WplusHToSSTodddd_tau3mm_M55_2017', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 49991), 
    MCSample('WplusHToSSTodddd_tau30mm_M55_2017', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-30_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 47998), 
    
    #No WplusHToSSTodddd_tau10mm_M55_2017
]

WminusHToSSTodddd_samples_2017 = [
    #No WminusHToSSTodddd_tau100um_M15_2017 
    #No WminusHToSSTodddd_tau300um_M40_2017 
    MCSample('WminusHToSSTodddd_tau1mm_M15_2017', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 48999), 
    MCSample('WminusHToSSTodddd_tau3mm_M15_2017', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 48999), 
    MCSample('WminusHToSSTodddd_tau10mm_M15_2017', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-10_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 50000), 
    MCSample('WminusHToSSTodddd_tau30mm_M15_2017', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-30_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 50000), 

    #No WminusHToSSTodddd_tau100um_M40_2017 
    MCSample('WminusHToSSTodddd_tau300um_M40_2017', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 49997), 
    MCSample('WminusHToSSTodddd_tau1mm_M40_2017', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 48000), 
    MCSample('WminusHToSSTodddd_tau3mm_M40_2017', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 49997), 
    MCSample('WminusHToSSTodddd_tau10mm_M40_2017', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-10_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 49999), 
    MCSample('WminusHToSSTodddd_tau30mm_M40_2017', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-30_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 49998), 
   
    #No WminusHToSSTodddd_tau100um_M55_2017 
    MCSample('WminusHToSSTodddd_tau300um_M55_2017', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 47995), 
    MCSample('WminusHToSSTodddd_tau1mm_M55_2017', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 49995), 
    MCSample('WminusHToSSTodddd_tau3mm_M55_2017', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 49992), 
    MCSample('WminusHToSSTodddd_tau10mm_M55_2017', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-10_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 49994), 
    MCSample('WminusHToSSTodddd_tau30mm_M55_2017', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-30_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 49993), 
]


#all_signal_samples_2017 = mfv_signal_samples_2017 + mfv_stopdbardbar_samples_2017 + mfv_stopbbarbbar_samples_2017 + mfv_stoplb_samples_2017 + mfv_stopld_samples_2017 + HToSSTobbbb_samples_2017 + HToSSTodddd_samples_2017 + mfv_splitSUSY_samples_2017
all_signal_samples_2017 = mfv_stoplb_samples_2017 + mfv_stopld_samples_2017 + ZHToSSTodddd_samples_2017 + WplusHToSSTodddd_samples_2017 + WminusHToSSTodddd_samples_2017 
#all_signal_samples_2017 = ZHToSSTodddd_samples_2017 + WplusHToSSTodddd_samples_2017 + WminusHToSSTodddd_samples_2017 
#all_signal_samples_2017 = WplusHToSSTodddd_samples_2017 

splitSUSY_samples_2017 = mfv_splitSUSY_samples_2017

########
# 2018 MC
########

qcd_samples_2018 = [
    MCSample('qcdht0200_2018', '/QCD_HT200to300_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v2/AODSIM', 22841038, nice='QCD, 200 < H_{T} < 300 GeV',  color=802, syst_frac=0.20, xsec=1.554e6),
    MCSample('qcdht0200ext_2018', '/QCD_HT200to300_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL18RECO-106X_upgrade2018_realistic_v11_L1v1_ext1-v1/AODSIM', 34740016, nice='QCD, 200 < H_{T} < 300 GeV',  color=802, syst_frac=0.20, xsec=1.554e6),
    MCSample('qcdht0300_2018', '/QCD_HT300to500_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v2/AODSIM', 55198123, nice='QCD, 300 < H_{T} < 500 GeV',  color=803, syst_frac=0.20, xsec=3.226e5), #xsec not available
    MCSample('qcdht0500_2018', '/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v2/AODSIM', 58437786, nice='QCD, 500 < H_{T} < 700 GeV', color=804, syst_frac=0.20, xsec=3.028e4),
    MCSample('qcdht0700_2018', '/QCD_HT700to1000_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v2/AODSIM', 47725353, nice='QCD, 700 < H_{T} < 1000 GeV',  color=805, syst_frac=0.20, xsec=6.392e3),
    MCSample('qcdht1000_2018', '/QCD_HT1000to1500_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v2/AODSIM', 15685044, nice='QCD, 1000 < H_{T} < 1500 GeV', color=806, syst_frac=0.20, xsec=1.096e3), #xsec not available
    MCSample('qcdht1500_2018', '/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v2/AODSIM', 10615310, nice='QCD, 1500 < H_{T} < 2000 GeV', color=807, syst_frac=0.20, xsec=99.0), #xsec not available
    MCSample('qcdht2000_2018', '/QCD_HT2000toInf_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v2/AODSIM',   4532754, nice='QCD, H_{T} > 2000',            color=808, syst_frac=0.20, xsec=21.93),
    ]
qcd_samples_sum_2018 = [
    SumSample('qcdht0200sum_2018', qcd_samples_2017[0:2]),
    ]

# need to make these MiniAODv2 
qcd_lep_samples_2018 = [
    MCSample('qcdmupt15_2018',  '/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM',    17392472, nice='QCD, #hat{p}_{T} > 20 GeV, #mu p_{T} > 15 GeV', color=801, syst_frac=0.20, xsec=2.39e5),
    MCSample('qcdempt015_2018', '/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM',    7899865, nice='QCD,  15 < #hat{p}_{T} <  20 GeV, EM enriched', color=801, syst_frac=0.20, xsec=1.324e6),
    MCSample('qcdempt020_2018', '/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM',    14328846, nice='QCD,  20 < #hat{p}_{T} <  30 GeV, EM enriched', color=801, syst_frac=0.20, xsec=4.896e6),
    MCSample('qcdempt030_2018', '/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM',    8574589, nice='QCD,  30 < #hat{p}_{T} <  50 GeV, EM enriched', color=801, syst_frac=0.20, xsec=6.447e6),
    MCSample('qcdempt050_2018', '/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM',    10524400, nice='QCD,  50 < #hat{p}_{T} <  80 GeV, EM enriched', color=801, syst_frac=0.20, xsec=1.988e6),
    MCSample('qcdempt080_2018', '/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM',    9468372, nice='QCD,  80 < #hat{p}_{T} < 120 GeV, EM enriched', color=801, syst_frac=0.20, xsec=3.675e5),
    MCSample('qcdempt120_2018', '/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM',   9677904, nice='QCD, 120 < #hat{p}_{T} < 170 GeV, EM enriched', color=801, syst_frac=0.20, xsec=6.659e4),
    MCSample('qcdempt170_2018', '/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM',   3714642, nice='QCD, 170 < #hat{p}_{T} < 300 GeV, EM enriched', color=801, syst_frac=0.20, xsec=1.662e4),
    MCSample('qcdempt300_2018', '/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM',   2215994, nice='QCD, #hat{p}_{T} > 300 GeV, EM enriched',       color=801, syst_frac=0.20, xsec=1104.0),
    MCSample('qcdbctoept015_2018', '/QCD_Pt_15to20_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM',      16549971, nice='QCD,  15 < #hat{p}_{T} <  20 GeV, HF electrons', color=801, syst_frac=0.20, xsec=1.862e5),
    MCSample('qcdbctoept020_2018', '/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM',      14061214, nice='QCD,  20 < #hat{p}_{T} <  30 GeV, HF electrons', color=801, syst_frac=0.20, xsec=3.038e5),
    MCSample('qcdbctoept030_2018', '/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM',      15358726, nice='QCD,  30 < #hat{p}_{T} <  80 GeV, HF electrons', color=801, syst_frac=0.20, xsec=3.623e5),
    MCSample('qcdbctoept080_2018', '/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM',     15186397, nice='QCD,  80 < #hat{p}_{T} < 170 GeV, HF electrons', color=801, syst_frac=0.20, xsec=3.37e4),
    MCSample('qcdbctoept170_2018', '/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v3/MINIAODSIM',    15735786, nice='QCD, 170 < #hat{p}_{T} < 250 GeV, HF electrons', color=801, syst_frac=0.20, xsec=2.125e3),
    MCSample('qcdbctoept250_2018', '/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v3/MINIAODSIM',    15767690, nice='QCD, #hat{p}_{T} > 250 GeV, HF electrons',       color=801, syst_frac=0.20, xsec=562.5),
]

ttbar_samples_2018 = [
    MCSample('ttbar_2018',            '/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM',            306142112, nice='t#bar{t}',                   color=4,   syst_frac=0.15, xsec=7.572e+02),
]

bjet_samples_2018 = []

leptonic_samples_2018 = [
    MCSample('wjetstolnu_0j_2018',    '/WJetsToLNu_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM',      172138190, nice='$W + jets #rightarrow l#nu$', color=  9, syst_frac=0.10, xsec=52.780e3),   
    MCSample('wjetstolnu_1j_2018',    '/WJetsToLNu_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM',      184564696, nice='$W + jets #rightarrow l#nu$', color=  9, syst_frac=0.10, xsec=8.832e3),   
    MCSample('wjetstolnu_2j_2018',    '/WJetsToLNu_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM',      94925903, nice='$W + jets #rightarrow l#nu$', color=  9, syst_frac=0.10, xsec=3.276e3),   
    MCSample('dyjetstollM10_2018',    '/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM', 99288125, nice='$DY + jets #rightarrow ll$, $10 < M < 50$ \\GeV', color= 29, syst_frac=0.10, xsec=1.589e4),
    MCSample('dyjetstollM50_2018',    '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM',     96233328, nice='$DY + jets #rightarrow ll$, $M > 50$ \\GeV', color= 32, syst_frac=0.10, xsec=5.398e3),
]

met_samples_2018 = [
    #MCSample('ttbar_2018',            '/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM',            306142112, nice='t#bar{t}',                   color=4,   syst_frac=0.15, xsec=7.572e+02),
]

# diboson_samples_2018 = [
#     MCSample('ww_2018',    '/WW_TuneCP5_13TeV-pythia8/RunIISummer20UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v2/AODSIM',          15679000, nice='WW', color= 32, syst_frac=0.10, xsec=7.587e+01),
#     MCSample('wz_2018',    '/WZ_TuneCP5_13TeV-pythia8/RunIISummer20UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v2/AODSIM',           7988000, nice='WZ', color= 32, syst_frac=0.10, xsec=2.756e+01),
#     MCSample('zz_2018',    '/ZZ_TuneCP5_13TeV-pythia8/RunIISummer20UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v2/AODSIM',           4000000, nice='ZZ', color= 32, syst_frac=0.10, xsec=1.214e+01),
# ]

diboson_samples_2018 = [
    MCSample('ww_2018',    '/WW_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM',          15679000, nice='WW', color= 32, syst_frac=0.10, xsec=7.587e+01),
    MCSample('wz_2018',    '/WZ_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM',           7988000, nice='WZ', color= 32, syst_frac=0.10, xsec=2.756e+01),
    MCSample('zz_2018',    '/ZZ_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM',           3526000, nice='ZZ', color= 32, syst_frac=0.10, xsec=1.214e+01),
]

Zvv_samples_2018 = [
    MCSample('zjetstonunuht0100_2018', '/ZJetsToNuNu_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v1/AODSIM', 29116252, nice='Z + jets #rightarrow #nu #nu 100 < H_{T} < 200 GeV', color=1, syst_frac=0.20, xsec=302.8),
    MCSample('zjetstonunuht0200_2018', '/ZJetsToNuNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v1/AODSIM', 23570033, nice='Z + jets #rightarrow #nu #nu 200 < H_{T} < 400 GeV', color=1, syst_frac=0.20, xsec=92.59),
    MCSample('zjetstonunuht0400_2018', '/ZJetsToNuNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v1/AODSIM', 20718934, nice='Z + jets #rightarrow #nu #nu 400 < H_{T} < 600 GeV', color=1, syst_frac=0.20, xsec=13.18),
    MCSample('zjetstonunuht0600_2018', '/ZJetsToNuNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v1/AODSIM',  5968910, nice='Z + jets #rightarrow #nu #nu 600 < H_{T} < 800 GeV', color=1, syst_frac=0.20, xsec=3.257),
    MCSample('zjetstonunuht0800_2018', '/ZJetsToNuNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v1/AODSIM', 2144959, nice='Z + jets #rightarrow #nu #nu 800 < H_{T} < 1200 GeV', color=1, syst_frac=0.20, xsec=1.49),
    MCSample('zjetstonunuht1200_2018', '/ZJetsToNuNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v1/AODSIM', 381695, nice='Z + jets #rightarrow #nu #nu 1200 < H_{T} < 2500 GeV', color=1, syst_frac=0.20, xsec=0.3419),
    MCSample('zjetstonunuht2500_2018', '/ZJetsToNuNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v1/AODSIM',  268224, nice='Z + jets #rightarrow #nu #nu H_{T} > 2500 GeV', color=1, syst_frac=0.20, xsec=0.005146),
    ]

mfv_splitSUSY_samples_2018 = []

mfv_stoplb_samples_2018 = [
    MCSample('mfv_stoplb_tau000100um_M1000_2018', '/DisplacedSUSY_stopToLBottom_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 202114),
    MCSample('mfv_stoplb_tau000300um_M1000_2018', '/DisplacedSUSY_stopToLBottom_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 196665),
    MCSample('mfv_stoplb_tau010000um_M1000_2018', '/DisplacedSUSY_stopToLBottom_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 99062),
    MCSample('mfv_stoplb_tau001000um_M1000_2018', '/DisplacedSUSY_stopToLBottom_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 196748),
    MCSample('mfv_stoplb_tau030000um_M1000_2018', '/DisplacedSUSY_stopToLBottom_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 199216),
    MCSample('mfv_stoplb_tau000100um_M1200_2018', '/DisplacedSUSY_stopToLBottom_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 197949),
    MCSample('mfv_stoplb_tau000300um_M1200_2018', '/DisplacedSUSY_stopToLBottom_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 198241),
    MCSample('mfv_stoplb_tau010000um_M1200_2018', '/DisplacedSUSY_stopToLBottom_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 98201),
    MCSample('mfv_stoplb_tau001000um_M1200_2018', '/DisplacedSUSY_stopToLBottom_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 199473),
    MCSample('mfv_stoplb_tau030000um_M1200_2018', '/DisplacedSUSY_stopToLBottom_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 199458),
    MCSample('mfv_stoplb_tau000100um_M1400_2018', '/DisplacedSUSY_stopToLBottom_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 199272),
    MCSample('mfv_stoplb_tau000300um_M1400_2018', '/DisplacedSUSY_stopToLBottom_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 200098),
    MCSample('mfv_stoplb_tau010000um_M1400_2018', '/DisplacedSUSY_stopToLBottom_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 99970),
    MCSample('mfv_stoplb_tau001000um_M1400_2018', '/DisplacedSUSY_stopToLBottom_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 200807),
    MCSample('mfv_stoplb_tau030000um_M1400_2018', '/DisplacedSUSY_stopToLBottom_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 200816),
    MCSample('mfv_stoplb_tau000100um_M1600_2018', '/DisplacedSUSY_stopToLBottom_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 199366),
    MCSample('mfv_stoplb_tau000300um_M1600_2018', '/DisplacedSUSY_stopToLBottom_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 202756),
    MCSample('mfv_stoplb_tau010000um_M1600_2018', '/DisplacedSUSY_stopToLBottom_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 101586),
    MCSample('mfv_stoplb_tau001000um_M1600_2018', '/DisplacedSUSY_stopToLBottom_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 99806),
    MCSample('mfv_stoplb_tau030000um_M1600_2018', '/DisplacedSUSY_stopToLBottom_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 100560),
    MCSample('mfv_stoplb_tau000100um_M1800_2018', '/DisplacedSUSY_stopToLBottom_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 200523),
    MCSample('mfv_stoplb_tau000300um_M1800_2018', '/DisplacedSUSY_stopToLBottom_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 199868),
    MCSample('mfv_stoplb_tau010000um_M1800_2018', '/DisplacedSUSY_stopToLBottom_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 101211),
    MCSample('mfv_stoplb_tau001000um_M1800_2018', '/DisplacedSUSY_stopToLBottom_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 100171),
    MCSample('mfv_stoplb_tau030000um_M1800_2018', '/DisplacedSUSY_stopToLBottom_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 100346),
    MCSample('mfv_stoplb_tau000100um_M0200_2018', '/DisplacedSUSY_stopToLBottom_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 198986),
    MCSample('mfv_stoplb_tau000300um_M0200_2018', '/DisplacedSUSY_stopToLBottom_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 199542),
    MCSample('mfv_stoplb_tau010000um_M0200_2018', '/DisplacedSUSY_stopToLBottom_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 198147),
    MCSample('mfv_stoplb_tau001000um_M0200_2018', '/DisplacedSUSY_stopToLBottom_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 198269),
    MCSample('mfv_stoplb_tau030000um_M0200_2018', '/DisplacedSUSY_stopToLBottom_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 197780),
    MCSample('mfv_stoplb_tau000100um_M0300_2018', '/DisplacedSUSY_stopToLBottom_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 198372),
    MCSample('mfv_stoplb_tau000300um_M0300_2018', '/DisplacedSUSY_stopToLBottom_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 203023),
    MCSample('mfv_stoplb_tau010000um_M0300_2018', '/DisplacedSUSY_stopToLBottom_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 196154),
    MCSample('mfv_stoplb_tau001000um_M0300_2018', '/DisplacedSUSY_stopToLBottom_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 197602),
    MCSample('mfv_stoplb_tau030000um_M0300_2018', '/DisplacedSUSY_stopToLBottom_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 196763),
    MCSample('mfv_stoplb_tau000100um_M0400_2018', '/DisplacedSUSY_stopToLBottom_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 200505),
    MCSample('mfv_stoplb_tau000300um_M0400_2018', '/DisplacedSUSY_stopToLBottom_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 200842),
    MCSample('mfv_stoplb_tau010000um_M0400_2018', '/DisplacedSUSY_stopToLBottom_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 198963),
    MCSample('mfv_stoplb_tau001000um_M0400_2018', '/DisplacedSUSY_stopToLBottom_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 199860),
    MCSample('mfv_stoplb_tau030000um_M0400_2018', '/DisplacedSUSY_stopToLBottom_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 198368),
    MCSample('mfv_stoplb_tau000100um_M0600_2018', '/DisplacedSUSY_stopToLBottom_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 198211),
    MCSample('mfv_stoplb_tau000300um_M0600_2018', '/DisplacedSUSY_stopToLBottom_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 199368),
    MCSample('mfv_stoplb_tau010000um_M0600_2018', '/DisplacedSUSY_stopToLBottom_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 197845),
    MCSample('mfv_stoplb_tau001000um_M0600_2018', '/DisplacedSUSY_stopToLBottom_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 196032),
    MCSample('mfv_stoplb_tau030000um_M0600_2018', '/DisplacedSUSY_stopToLBottom_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 201533),
    MCSample('mfv_stoplb_tau000100um_M0800_2018', '/DisplacedSUSY_stopToLBottom_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 202319),
    MCSample('mfv_stoplb_tau000300um_M0800_2018', '/DisplacedSUSY_stopToLBottom_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 200738),
    MCSample('mfv_stoplb_tau010000um_M0800_2018', '/DisplacedSUSY_stopToLBottom_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 99747),
    MCSample('mfv_stoplb_tau001000um_M0800_2018', '/DisplacedSUSY_stopToLBottom_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 202348),
    MCSample('mfv_stoplb_tau030000um_M0800_2018', '/DisplacedSUSY_stopToLBottom_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 199087),
]
mfv_stopld_samples_2018 = [
    MCSample('mfv_stopld_tau000100um_M1000_2018', '/DisplacedSUSY_stopToLD_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 198858),
    MCSample('mfv_stopld_tau000300um_M1000_2018', '/DisplacedSUSY_stopToLD_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 199006),
    MCSample('mfv_stopld_tau010000um_M1000_2018', '/DisplacedSUSY_stopToLD_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 98581),
    MCSample('mfv_stopld_tau001000um_M1000_2018', '/DisplacedSUSY_stopToLD_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 196285),
    MCSample('mfv_stopld_tau030000um_M1000_2018', '/DisplacedSUSY_stopToLD_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 199499),
    MCSample('mfv_stopld_tau000100um_M1200_2018', '/DisplacedSUSY_stopToLD_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 195354),
    MCSample('mfv_stopld_tau000300um_M1200_2018', '/DisplacedSUSY_stopToLD_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 195508,),
    MCSample('mfv_stopld_tau010000um_M1200_2018', '/DisplacedSUSY_stopToLD_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 98617),
    MCSample('mfv_stopld_tau001000um_M1200_2018', '/DisplacedSUSY_stopToLD_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 200103),
    MCSample('mfv_stopld_tau030000um_M1200_2018', '/DisplacedSUSY_stopToLD_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 200964),
    MCSample('mfv_stopld_tau000100um_M1400_2018', '/DisplacedSUSY_stopToLD_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 200045),
    MCSample('mfv_stopld_tau000300um_M1400_2018', '/DisplacedSUSY_stopToLD_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 202529),
    MCSample('mfv_stopld_tau010000um_M1400_2018', '/DisplacedSUSY_stopToLD_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 100228),
    MCSample('mfv_stopld_tau001000um_M1400_2018', '/DisplacedSUSY_stopToLD_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 196708),
    MCSample('mfv_stopld_tau030000um_M1400_2018', '/DisplacedSUSY_stopToLD_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 201992),
    MCSample('mfv_stopld_tau000100um_M1600_2018', '/DisplacedSUSY_stopToLD_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 201300),
    MCSample('mfv_stopld_tau000300um_M1600_2018', '/DisplacedSUSY_stopToLD_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 197421),
    MCSample('mfv_stopld_tau010000um_M1600_2018', '/DisplacedSUSY_stopToLD_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 99387),
    MCSample('mfv_stopld_tau001000um_M1600_2018', '/DisplacedSUSY_stopToLD_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 100838),
    MCSample('mfv_stopld_tau030000um_M1600_2018', '/DisplacedSUSY_stopToLD_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 97752),
    MCSample('mfv_stopld_tau000100um_M1800_2018', '/DisplacedSUSY_stopToLD_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 202746),
    MCSample('mfv_stopld_tau000300um_M1800_2018', '/DisplacedSUSY_stopToLD_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 199924),
    MCSample('mfv_stopld_tau010000um_M1800_2018', '/DisplacedSUSY_stopToLD_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 99400),
    MCSample('mfv_stopld_tau001000um_M1800_2018', '/DisplacedSUSY_stopToLD_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 99515),
    MCSample('mfv_stopld_tau030000um_M1800_2018', '/DisplacedSUSY_stopToLD_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 98449),
    MCSample('mfv_stopld_tau000100um_M0200_2018', '/DisplacedSUSY_stopToLD_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 197970),
    MCSample('mfv_stopld_tau000300um_M0200_2018', '/DisplacedSUSY_stopToLD_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 198800),
    MCSample('mfv_stopld_tau010000um_M0200_2018', '/DisplacedSUSY_stopToLD_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 199856),
    MCSample('mfv_stopld_tau001000um_M0200_2018', '/DisplacedSUSY_stopToLD_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 200411),
    MCSample('mfv_stopld_tau030000um_M0200_2018', '/DisplacedSUSY_stopToLD_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 202558),
    MCSample('mfv_stopld_tau000100um_M0300_2018', '/DisplacedSUSY_stopToLD_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 196635),
    MCSample('mfv_stopld_tau000300um_M0300_2018', '/DisplacedSUSY_stopToLD_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 198796),
    MCSample('mfv_stopld_tau010000um_M0300_2018', '/DisplacedSUSY_stopToLD_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 197769),
    MCSample('mfv_stopld_tau001000um_M0300_2018', '/DisplacedSUSY_stopToLD_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 200543),
    MCSample('mfv_stopld_tau030000um_M0300_2018', '/DisplacedSUSY_stopToLD_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 198495),
    MCSample('mfv_stopld_tau000100um_M0400_2018', '/DisplacedSUSY_stopToLD_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 201643),
    MCSample('mfv_stopld_tau000300um_M0400_2018', '/DisplacedSUSY_stopToLD_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 197079),
    MCSample('mfv_stopld_tau010000um_M0400_2018', '/DisplacedSUSY_stopToLD_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 198270),
    MCSample('mfv_stopld_tau001000um_M0400_2018', '/DisplacedSUSY_stopToLD_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 200098),
    MCSample('mfv_stopld_tau030000um_M0400_2018', '/DisplacedSUSY_stopToLD_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 203160),
    MCSample('mfv_stopld_tau000100um_M0600_2018', '/DisplacedSUSY_stopToLD_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 198964),
    MCSample('mfv_stopld_tau000300um_M0600_2018', '/DisplacedSUSY_stopToLD_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 198408),
    MCSample('mfv_stopld_tau010000um_M0600_2018', '/DisplacedSUSY_stopToLD_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 200404),
    MCSample('mfv_stopld_tau001000um_M0600_2018', '/DisplacedSUSY_stopToLD_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 199759),
    MCSample('mfv_stopld_tau030000um_M0600_2018', '/DisplacedSUSY_stopToLD_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 200030),
    MCSample('mfv_stopld_tau000100um_M0800_2018', '/DisplacedSUSY_stopToLD_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 197872),
    MCSample('mfv_stopld_tau000300um_M0800_2018', '/DisplacedSUSY_stopToLD_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 202036),
    MCSample('mfv_stopld_tau010000um_M0800_2018', '/DisplacedSUSY_stopToLD_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 100507),
    MCSample('mfv_stopld_tau001000um_M0800_2018', '/DisplacedSUSY_stopToLD_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 199217),
    MCSample('mfv_stopld_tau030000um_M0800_2018', '/DisplacedSUSY_stopToLD_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 197136),
]
# private samples 
# mfv_stopld_samples_2018 = [
#     MCSample('mfv_stopld_tau000100um_M0200_2018', '/DisplacedSUSY_stopToLD_M_200_0p1mm_TuneCP5_13TeV-pythia8/awarden-RunIISummer20UL18_MiniAOD-dd00e8e5190104a7aafdc4fba9805483/USER', 4089),
#     MCSample('mfv_stopld_tau000300um_M0200_2018', '/DisplacedSUSY_stopToLD_M_200_0p3mm_TuneCP5_13TeV-pythia8/awarden-RunIISummer20UL18_MiniAOD-dd00e8e5190104a7aafdc4fba9805483/USER', 4050),
#     MCSample('mfv_stopld_tau000100um_M0600_2018', '/DisplacedSUSY_stopToLD_M_600_0p1mm_TuneCP5_13TeV-pythia8/awarden-RunIISummer20UL18_MiniAOD-dd00e8e5190104a7aafdc4fba9805483/USER', 2821),
#     MCSample('mfv_stopld_tau000300um_M0600_2018', '/DisplacedSUSY_stopToLD_M_600_0p3mm_TuneCP5_13TeV-pythia8/awarden-RunIISummer20UL18_MiniAOD-dd00e8e5190104a7aafdc4fba9805483/USER', 2802),
#     MCSample('mfv_stopld_tau000100um_M1000_2018', '/DisplacedSUSY_stopToLD_M_1000_0p1mm_TuneCP5_13TeV-pythia8/awarden-RunIISummer20UL18_MiniAOD-dd00e8e5190104a7aafdc4fba9805483/USER', 2579),
#     MCSample('mfv_stopld_tau000300um_M1000_2018', '/DisplacedSUSY_stopToLD_M_1000_0p3mm_TuneCP5_13TeV-pythia8/awarden-RunIISummer20UL18_MiniAOD-dd00e8e5190104a7aafdc4fba9805483/USER', 2604),
#    # MCSample('mfv_stopld_tau001000um_M1000_2018', '/DisplacedSUSY_stopToLD_M_1000_1mm_TuneCP5_13TeV-pythia8/awarden-RunIISummer20UL18_MiniAOD-dd00e8e5190104a7aafdc4fba9805483/USER', 2555),
#     MCSample('mfv_stopld_tau000100um_M1600_2018', '/DisplacedSUSY_stopToLD_M_1600_0p1mm_TuneCP5_13TeV-pythia8/awarden-RunIISummer20UL18_MiniAOD-dd00e8e5190104a7aafdc4fba9805483/USER', 2472),
#     MCSample('mfv_stopld_tau000300um_M1600_2018', '/DisplacedSUSY_stopToLD_M_1600_0p3mm_TuneCP5_13TeV-pythia8/awarden-RunIISummer20UL18_MiniAOD-dd00e8e5190104a7aafdc4fba9805483/USER', 2478),
# ]

ZHToSSTodddd_samples_2018 = [ 
    MCSample('ZHToSSTodddd_tau1mm_M55_2018', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 49999), 
]

WplusHToSSTodddd_samples_2018 = [
    MCSample('WplusHToSSTodddd_tau1mm_M55_2018', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 49994),
]

WminusHToSSTodddd_samples_2018 = [
    MCSample('WminusHToSSTodddd_tau1mm_M55_2018', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 49995),
]



#all_signal_samples_2018 = mfv_splitSUSY_samples_2018
#all_signal_samples_2018 = mfv_stoplb_samples_2018 + mfv_stopld_samples_2018
all_signal_samples_2018 = ZHToSSTodddd_samples_2018 + WplusHToSSTodddd_samples_2018 + WminusHToSSTodddd_samples_2018 
########
# data
########


Lepton_data_samples_20161 = [
    DataSample('SingleMuon20161B1', '/SingleMuon/Run2016B-ver1_HIPM_UL2016_MiniAODv2-v2/MINIAOD'),
    DataSample('SingleMuon20161B2', '/SingleMuon/Run2016B-ver2_HIPM_UL2016_MiniAODv2-v2/MINIAOD'),
    DataSample('SingleMuon20161C',  '/SingleMuon/Run2016C-HIPM_UL2016_MiniAODv2-v2/MINIAOD'),
    DataSample('SingleMuon20161D',  '/SingleMuon/Run2016D-HIPM_UL2016_MiniAODv2-v2/MINIAOD'),
    DataSample('SingleMuon20161E',  '/SingleMuon/Run2016E-HIPM_UL2016_MiniAODv2-v2/MINIAOD'),
    DataSample('SingleMuon20161F',  '/SingleMuon/Run2016F-HIPM_UL2016_MiniAODv2-v2/MINIAOD'),
    DataSample('SingleElectron20161B1', '/SingleElectron/Run2016B-ver1_HIPM_UL2016_MiniAODv2-v2/MINIAOD'), #Alec added these
    DataSample('SingleElectron20161B2', '/SingleElectron/Run2016B-ver2_HIPM_UL2016_MiniAODv2-v2/MINIAOD'),
    DataSample('SingleElectron20161C',  '/SingleElectron/Run2016C-HIPM_UL2016_MiniAODv2-v2/MINIAOD'),
    DataSample('SingleElectron20161D',  '/SingleElectron/Run2016D-HIPM_UL2016_MiniAODv2-v2/MINIAOD'),
    DataSample('SingleElectron20161E',  '/SingleElectron/Run2016E-HIPM_UL2016_MiniAODv2-v5/MINIAOD'),
    DataSample('SingleElectron20161F',  '/SingleElectron/Run2016F-HIPM_UL2016_MiniAODv2-v2/MINIAOD'),
]


Lepton_data_samples_20162 = [
    DataSample('SingleMuon20162F', '/SingleMuon/Run2016F-UL2016_MiniAODv2-v2/MINIAOD'),
    DataSample('SingleMuon20162G', '/SingleMuon/Run2016G-UL2016_MiniAODv2-v2/MINIAOD'),
    DataSample('SingleMuon20162H', '/SingleMuon/Run2016H-UL2016_MiniAODv2-v2/MINIAOD'),
    DataSample('SingleElectron20162F', '/SingleElectron/Run2016F-UL2016_MiniAODv2-v2/MINIAOD'), #Alec added these
    DataSample('SingleElectron20162G', '/SingleElectron/Run2016G-UL2016_MiniAODv2-v2/MINIAOD'),
    DataSample('SingleElectron20162H', '/SingleElectron/Run2016H-UL2016_MiniAODv2-v2/MINIAOD'),
]


data_samples_2017 = [                                                       # in dataset      in json          int lumi avail (/fb)
    DataSample('MET2017B', '/MET/Run2017B-09Aug2019_UL2017_rsb-v1/AOD'),  
    DataSample('MET2017C', '/MET/Run2017C-09Aug2019_UL2017_rsb-v1/AOD'),  
    DataSample('MET2017D', '/MET/Run2017D-09Aug2019_UL2017_rsb-v1/AOD'),  
    DataSample('MET2017E', '/MET/Run2017E-09Aug2019_UL2017_rsb-v1/AOD'),  
    DataSample('MET2017F', '/MET/Run2017F-09Aug2019_UL2017_rsb-v1/AOD'),  
    ]

#FIXME: may need to reorganize how data is loaded for different cases
JetHT_data_samples_2017 = []

#Lepton_data_samples_2017 = [
#    DataSample('SingleMuon2017B', '/SingleMuon/Run2017B-09Aug2019_UL2017-v1/AOD'),
#    DataSample('SingleMuon2017C', '/SingleMuon/Run2017C-09Aug2019_UL2017-v1/AOD'),
#    DataSample('SingleMuon2017D', '/SingleMuon/Run2017D-09Aug2019_UL2017-v1/AOD'),
#    DataSample('SingleMuon2017E', '/SingleMuon/Run2017E-09Aug2019_UL2017-v1/AOD'),
#    DataSample('SingleMuon2017F', '/SingleMuon/Run2017F-09Aug2019_UL2017-v1/AOD'),
#    DataSample('SingleElectron2017B', '/SingleElectron/Run2017B-09Aug2019_UL2017-v1/AOD'),
#    DataSample('SingleElectron2017C', '/SingleElectron/Run2017C-09Aug2019_UL2017-v1/AOD'),
#    DataSample('SingleElectron2017D', '/SingleElectron/Run2017D-09Aug2019_UL2017-v1/AOD'),
#    DataSample('SingleElectron2017E', '/SingleElectron/Run2017E-09Aug2019_UL2017-v1/AOD'),
#    DataSample('SingleElectron2017F', '/SingleElectron/Run2017F-09Aug2019_UL2017_rsb-v2/AOD'),
#    ] Alec commented and replaced with below

Lepton_data_samples_2017 = [
    DataSample('SingleMuon2017B', '/SingleMuon/Run2017B-UL2017_MiniAODv2_GT36-v2/MINIAOD'),
    DataSample('SingleMuon2017C', '/SingleMuon/Run2017C-UL2017_MiniAODv2_GT36-v2/MINIAOD'),
    DataSample('SingleMuon2017D', '/SingleMuon/Run2017D-UL2017_MiniAODv2_GT36-v2/MINIAOD'),
    DataSample('SingleMuon2017E', '/SingleMuon/Run2017E-UL2017_MiniAODv2_GT36-v2/MINIAOD'),
    DataSample('SingleMuon2017F', '/SingleMuon/Run2017F-UL2017_MiniAODv2_GT36-v2/MINIAOD'),
    DataSample('SingleElectron2017B', '/SingleElectron/Run2017B-UL2017_MiniAODv2-v1/MINIAOD'),
    DataSample('SingleElectron2017C', '/SingleElectron/Run2017C-UL2017_MiniAODv2-v1/MINIAOD'),
    DataSample('SingleElectron2017D', '/SingleElectron/Run2017D-UL2017_MiniAODv2-v1/MINIAOD'),
    DataSample('SingleElectron2017E', '/SingleElectron/Run2017E-UL2017_MiniAODv2-v1/MINIAOD'),
    DataSample('SingleElectron2017F', '/SingleElectron/Run2017F-UL2017_MiniAODv2-v1/MINIAOD'),
    ]    

#auxiliary_data_samples_2017 = [
#    DataSample('SingleMuon2017B', '/SingleMuon/Run2017B-09Aug2019_UL2017-v1/AOD'),
#    DataSample('SingleMuon2017C', '/SingleMuon/Run2017C-09Aug2019_UL2017-v1/AOD'),
#    DataSample('SingleMuon2017D', '/SingleMuon/Run2017D-09Aug2019_UL2017-v1/AOD'),
#    DataSample('SingleMuon2017E', '/SingleMuon/Run2017E-09Aug2019_UL2017-v1/AOD'),
#    DataSample('SingleMuon2017F', '/SingleMuon/Run2017F-09Aug2019_UL2017-v1/AOD'),
#    ]   Alec commented and replaced with below 

auxiliary_data_samples_2017 = [
    DataSample('SingleMuon2017B', '/SingleMuon/Run2017B-UL2017_MiniAODv2_GT36-v2/MINIAOD'),
    DataSample('SingleMuon2017C', '/SingleMuon/Run2017C-UL2017_MiniAODv2_GT36-v2/MINIAOD'),
    DataSample('SingleMuon2017D', '/SingleMuon/Run2017D-UL2017_MiniAODv2_GT36-v2/MINIAOD'),
    DataSample('SingleMuon2017E', '/SingleMuon/Run2017E-UL2017_MiniAODv2_GT36-v2/MINIAOD'),
    DataSample('SingleMuon2017F', '/SingleMuon/Run2017F-UL2017_MiniAODv2_GT36-v2/MINIAOD'),
    ]

#singleelectron_data_samples_2017 = [
#    DataSample('SingleElectron2017B', '/SingleElectron/Run2017B-09Aug2019_UL2017-v1/AOD'),
#    DataSample('SingleElectron2017C', '/SingleElectron/Run2017C-09Aug2019_UL2017-v1/AOD'),
#    DataSample('SingleElectron2017D', '/SingleElectron/Run2017D-09Aug2019_UL2017-v1/AOD'),
#    DataSample('SingleElectron2017E', '/SingleElectron/Run2017E-09Aug2019_UL2017-v1/AOD'),
#    DataSample('SingleElectron2017F', '/SingleElectron/Run2017F-09Aug2019_UL2017_rsb-v2/AOD'),
#] Alec commented and replaced with below

singleelectron_data_samples_2017 = [
    DataSample('SingleElectron2017B', '/SingleElectron/Run2017B-UL2017_MiniAODv2-v1/MINIAOD'),
    DataSample('SingleElectron2017C', '/SingleElectron/Run2017C-UL2017_MiniAODv2-v1/MINIAOD'),
    DataSample('SingleElectron2017D', '/SingleElectron/Run2017D-UL2017_MiniAODv2-v1/MINIAOD'),
    DataSample('SingleElectron2017E', '/SingleElectron/Run2017E-UL2017_MiniAODv2-v1/MINIAOD'),
    DataSample('SingleElectron2017F', '/SingleElectron/Run2017F-UL2017_MiniAODv2-v1/MINIAOD'),
]

#Switching data with auxiliary data
auxiliary_data_samples_2018 = [
    DataSample('MET2018A', '/MET/Run2018A-12Nov2019_UL2018-v3/AOD'),  
    DataSample('MET2018B', '/MET/Run2018B-12Nov2019_UL2018-v3/AOD'),  
    DataSample('MET2018C', '/MET/Run2018C-12Nov2019_UL2018_rsb-v1/AOD'), 
    DataSample('MET2018D', '/MET/Run2018D-12Nov2019_UL2018_rsb-v2/AOD'), 
]

#FIXME: may need to reorganize how data is loaded for different cases
#JetHT_data_samples_2018 = [  #Alec commented from here
#    DataSample('SingleMuon2017B', '/SingleMuon/Run2017B-09Aug2019_UL2017-v1/AOD'),
#    DataSample('SingleMuon2017C', '/SingleMuon/Run2017C-09Aug2019_UL2017-v1/AOD'),
#    DataSample('SingleMuon2017D', '/SingleMuon/Run2017D-09Aug2019_UL2017-v1/AOD'),
#    DataSample('SingleMuon2017E', '/SingleMuon/Run2017E-09Aug2019_UL2017-v1/AOD'),
#    DataSample('SingleMuon2017F', '/SingleMuon/Run2017F-09Aug2019_UL2017-v1/AOD'),
#    DataSample('SingleElectron2017B', '/SingleElectron/Run2017B-09Aug2019_UL2017-v1/AOD'),
#    DataSample('SingleElectron2017C', '/SingleElectron/Run2017C-09Aug2019_UL2017-v1/AOD'),
#    DataSample('SingleElectron2017D', '/SingleElectron/Run2017D-09Aug2019_UL2017-v1/AOD'),
#    DataSample('SingleElectron2017E', '/SingleElectron/Run2017E-09Aug2019_UL2017-v1/AOD'),
#    DataSample('SingleElectron2017F', '/SingleElectron/Run2017F-09Aug2019_UL2017_rsb-v2/AOD'),
#] #Alec to here

# Lepton_data_samples_2018 = [
#     DataSample('SingleMuon2018A', '/SingleMuon/Run2018A-12Nov2019_UL2018-v5/AOD'),
#     DataSample('SingleMuon2018B', '/SingleMuon/Run2018B-12Nov2019_UL2018-v3/AOD'),
#     DataSample('SingleMuon2018C', '/SingleMuon/Run2018C-12Nov2019_UL2018-v3/AOD'),
#     DataSample('SingleMuon2018D', '/SingleMuon/Run2018D-12Nov2019_UL2018-v8/AOD'),
#     DataSample('EGamma2018A', '/EGamma/Run2018A-12Nov2019_UL2018-v2/AOD'),
#     DataSample('EGamma2018B', '/EGamma/Run2018B-12Nov2019_UL2018-v2/AOD'),
#     DataSample('EGamma2018C', '/EGamma/Run2018C-12Nov2019_UL2018-v2/AOD'),
#     DataSample('EGamma2018D', '/EGamma/Run2018D-12Nov2019_UL2018-v8/AOD'),
# ]


Lepton_data_samples_2018 = [
    DataSample('SingleMuon2018A', '/SingleMuon/Run2018A-UL2018_MiniAODv2-v3/MINIAOD'),
    DataSample('SingleMuon2018B', '/SingleMuon/Run2018B-UL2018_MiniAODv2-v2/MINIAOD'),
    DataSample('SingleMuon2018C', '/SingleMuon/Run2018C-UL2018_MiniAODv2-v2/MINIAOD'),
    DataSample('SingleMuon2018D', '/SingleMuon/Run2018D-UL2018_MiniAODv2-v3/MINIAOD'),
    DataSample('EGamma2018A', '/EGamma/Run2018A-UL2018_MiniAODv2-v1/MINIAOD'),
    DataSample('EGamma2018B', '/EGamma/Run2018B-UL2018_MiniAODv2-v1/MINIAOD'),
    DataSample('EGamma2018C', '/EGamma/Run2018C-UL2018_MiniAODv2-v1/MINIAOD'),
    DataSample('EGamma2018D', '/EGamma/Run2018D-UL2018_MiniAODv2-v2/MINIAOD'),
]

data_samples_2018 = [
    DataSample('SingleMuon2018A', '/SingleMuon/Run2018A-12Nov2019_UL2018-v3/AOD'),
    DataSample('SingleMuon2018B', '/SingleMuon/Run2018B-12Nov2019_UL2018-v3/AOD'),
    DataSample('SingleMuon2018C', '/SingleMuon/Run2018C-12Nov2019_UL2018-v3/AOD'),
    DataSample('SingleMuon2018D', '/SingleMuon/Run2018D-12Nov2019_UL2018-v8/AOD'),
    ]

egamma_data_samples_2018 = [
    DataSample('EGamma2018A', '/EGamma/Run2018A-12Nov2019_UL2018-v2/AOD'),
    DataSample('EGamma2018B', '/EGamma/Run2018B-12Nov2019_UL2018-v2/AOD'),
    DataSample('EGamma2018C', '/EGamma/Run2018C-12Nov2019_UL2018-v2/AOD'),
    DataSample('EGamma2018D', '/EGamma/Run2018D-12Nov2019_UL2018-v8/AOD'),
    ]


########################################################################

registry = SamplesRegistry()

# shortcuts, be careful:
# - can't add data by primary (have the same primary for different datasets)
from functools import partial
_adbp = registry.add_dataset_by_primary
_adbp3 = partial(_adbp, dbs_inst='phys03')

# have to comment out some sets due to repeated samples 
__all__ = [
    'qcd_lep_samples_20161',
    'qcd_lep_samples_20162',
    'leptonic_samples_20161',
    'leptonic_samples_20162',
    'Lepton_data_samples_20161',
    'Lepton_data_samples_20162',
    'met_samples_20161',
    'met_samples_20162',
    'ttbar_samples_20161',
    'ttbar_samples_20162',
    'diboson_samples_20161',
    'diboson_samples_20162',
    'mfv_stoplb_samples_20161',
    'mfv_stopld_samples_20161',
    'mfv_stoplb_samples_20162',
    'mfv_stopld_samples_20162',
    'example_samples_ttbar_2017',
    'example_samples_zz_2017',
    'qcd_samples_2017',
    'qcd_samples_sum_2017',
    'qcd_lep_samples_2017',
    'ttbar_samples_2017',
    'bjet_samples_2017',
    'leptonic_samples_2017',
    'diboson_samples_2017',
    'met_samples_2017',
    'Zvv_samples_2017',
    'mfv_splitSUSY_samples_2017',
    'mfv_signal_samples_2017',
    'mfv_stopdbardbar_samples_2017',
    'mfv_stopbbarbbar_samples_2017',
    'mfv_stoplb_samples_2017',
    'mfv_stopld_samples_2017',
    'ZHToSSTodddd_samples_20161',
    'WplusHToSSTodddd_samples_20161',
    'WminusHToSSTodddd_samples_20161',
    'ZHToSSTodddd_samples_20162',
    'WplusHToSSTodddd_samples_20162',
    'WminusHToSSTodddd_samples_20162',
    'HToSSTobbbb_samples_2017',
    'HToSSTodddd_samples_2017',
    'ggHToSSTo4l_samples_2017',
    'ZHToSSTodddd_samples_2017',
    'WplusHToSSTodddd_samples_2017',
    'WminusHToSSTodddd_samples_2017',
    'qcd_samples_2018',
    'qcd_samples_sum_2018',
    'qcd_lep_samples_2018',
    'ttbar_samples_2018',
    'bjet_samples_2018',
    'leptonic_samples_2018',
    'met_samples_2018',
    'diboson_samples_2018',
    'Zvv_samples_2018',
    'mfv_splitSUSY_samples_2018',
    'mfv_stoplb_samples_2018',
    'mfv_stopld_samples_2018',
    'ZHToSSTodddd_samples_2018',
    'WplusHToSSTodddd_samples_2018',
    'WminusHToSSTodddd_samples_2018',
    'data_samples_2017',
    'JetHT_data_samples_2017',
    'Lepton_data_samples_2017',
    #'auxiliary_data_samples_2017',
    #'singleelectron_data_samples_2017',
    #'data_samples_2018',
    'Lepton_data_samples_2018',
    #'JetHT_data_samples_2018',
    'auxiliary_data_samples_2018',
    #'egamma_data_samples_2018',

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


#span_signal_samples_2017 = [eval('mfv_%s_tau%06ium_M%04i_2017' % (a,b,c)) for a in ('neu','stopdbardbar') for b in (300,1000,10000) for c in (800,1600,3000)]
span_signal_samples_2017 = [
]
#span_signal_samples_2018 = [eval('mfv_%s_tau%06ium_M%04i_2018' % (a,b,c)) for a in ('neu','stopdbardbar') for b in (300,1000,10000) for c in (800,1600,3000)]
span_signal_samples_2018 = [
]

_alls = [
    'all_signal_samples_20161',
    'all_signal_samples_20162',
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

mfv_stoplb_tau000100um_M1000_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLBottom_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-156d89435dc24dc05c7b9ca8444ca8ea/USER', 193961)
mfv_stoplb_tau000300um_M1000_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLBottom_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-4f2025787882c0b249a5d1b050d8cf40/USER', 186260)
mfv_stoplb_tau010000um_M1000_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLBottom_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-a666c0292b01a06aeb32bb4ee0b314c0/USER', 98261)
mfv_stoplb_tau001000um_M1000_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLBottom_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-ff752ef3a66a47c527cd9a5474d74949/USER', 197193)
mfv_stoplb_tau030000um_M1000_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLBottom_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-486052cb94ff307639691b006b0d084d/USER', 200668)
mfv_stoplb_tau000100um_M1200_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLBottom_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-e0ad2f94e7d725e87033ffafeccb0a57/USER', 199921)
mfv_stoplb_tau000300um_M1200_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLBottom_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-6f595773237cc894435d9c623a23b740/USER', 195189)
mfv_stoplb_tau010000um_M1200_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLBottom_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-2baa85da998849315bd960b6e8619008/USER', 100156)
mfv_stoplb_tau001000um_M1200_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLBottom_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-68a1b3cd5950a077591ecbf603d9fcd2/USER', 197902)
mfv_stoplb_tau030000um_M1200_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLBottom_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-7ae5154544276f77b46a8c3985a1b599/USER', 200464)
mfv_stoplb_tau000100um_M1400_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLBottom_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-de954880995f97ec7d229b2124cdf6b9/USER', 187459)
mfv_stoplb_tau000300um_M1400_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLBottom_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-031a5aded741d4b6c7827c97862e4d86/USER', 200304)
mfv_stoplb_tau010000um_M1400_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLBottom_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-c3dc591ba3db2cab45733ac34083ac3e/USER', 98900)
mfv_stoplb_tau001000um_M1400_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLBottom_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-00e9cfbd303f5566d7a923aec3a1c20f/USER', 192400)
mfv_stoplb_tau030000um_M1400_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLBottom_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-89d8113f44eb20ac882c5aac8cd93578/USER', 197635)
mfv_stoplb_tau000100um_M1600_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLBottom_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-1831cbabbb9382abcea05609e1a5a971/USER', 130204)
mfv_stoplb_tau000300um_M1600_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLBottom_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-fe9911aad67cfcd529655034b0054dd4/USER', 198070)
mfv_stoplb_tau010000um_M1600_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLBottom_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-d98c9292edc01866b5628fdabf425986/USER', 98745)
mfv_stoplb_tau001000um_M1600_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLBottom_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-4e90b788c2ea88d123e2d7328da42c77/USER', 91871)
mfv_stoplb_tau030000um_M1600_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLBottom_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-c5c8e98843d88a12edabcd4cb4ff4386/USER', 82216)
mfv_stoplb_tau000100um_M1800_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLBottom_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-2e28ea5dd8c76c87846612d8ea2f3f56/USER', 191607)
mfv_stoplb_tau000300um_M1800_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLBottom_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-a033e678cc892560c5446efb4ee3d7a2/USER', 200792)
mfv_stoplb_tau010000um_M1800_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLBottom_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-911cde0521c877f6a9882674a30e99c1/USER', 101386)
mfv_stoplb_tau001000um_M1800_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLBottom_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-0ff37b7709386f345e4b76a3930bccf2/USER', 98858)
mfv_stoplb_tau030000um_M1800_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLBottom_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-d0c1efc631e4aebd03cac531ada008da/USER', 99225)
mfv_stoplb_tau000100um_M0200_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLBottom_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-d91c0c740c8a6c942a8993ed444e781a/USER', 198760)
mfv_stoplb_tau000300um_M0200_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLBottom_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-9658c47efeabf9bbe52bb45e5ccbb84f/USER', 187003)
mfv_stoplb_tau010000um_M0200_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLBottom_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-a12fbd076ee9963b5bbc3a3316b0c1dd/USER', 199948)
mfv_stoplb_tau001000um_M0200_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLBottom_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-314903a6d3f541c8f77c6ff7dd721562/USER', 196687)
mfv_stoplb_tau030000um_M0200_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLBottom_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-3d39fdeca36ab14d2c8efc548378e400/USER', 199267)
mfv_stoplb_tau000100um_M0300_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLBottom_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-be17a6eb878aeaa77b4cc3f1651be3ef/USER', 196246)
mfv_stoplb_tau000300um_M0300_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLBottom_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-101d9d67ef192c7c44ef878ecc47ed36/USER', 183219)
mfv_stoplb_tau010000um_M0300_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLBottom_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-6e619672b0f0e465362ed59731d28a5a/USER', 199832)
mfv_stoplb_tau001000um_M0300_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLBottom_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-4371e09c8f7ea604f2666143c2fb2ab1/USER', 200296)
mfv_stoplb_tau030000um_M0300_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLBottom_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-66d7d8b7233d68e661c419297afb5b6d/USER', 200170)
mfv_stoplb_tau000100um_M0400_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLBottom_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-42e5ee6937df6795a6a062d3760d675c/USER', 197597)
mfv_stoplb_tau000300um_M0400_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLBottom_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-0cd237ff2fd16957c0b5a35d29223c74/USER', 195221)
mfv_stoplb_tau010000um_M0400_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLBottom_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-1ef6d10951e88ef3c770e3b7e6cc3869/USER', 198737)
mfv_stoplb_tau001000um_M0400_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLBottom_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-1596d3db6ed70ce98c94a7efb9bcf1ab/USER', 197003)
mfv_stoplb_tau030000um_M0400_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLBottom_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-152928631efad479f488e1e115b23570/USER', 191913)
mfv_stoplb_tau000100um_M0600_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLBottom_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-110281738b645c1ef8d5ee5972a0b035/USER', 194663)
mfv_stoplb_tau000300um_M0600_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLBottom_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-d76e817be37322b8f1191b80bdfdba86/USER', 201839)
mfv_stoplb_tau010000um_M0600_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLBottom_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-d895a12d786463bf4dd253f1491aeab0/USER', 188463)
mfv_stoplb_tau001000um_M0600_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLBottom_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-05b74e1f15947065b71eaf0777e6dc4d/USER', 195368)
mfv_stoplb_tau030000um_M0600_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLBottom_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-2588130cc7dddf8d327fea5af8ade4e5/USER', 199015)
mfv_stoplb_tau000100um_M0800_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLBottom_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-e30f343caa276683f32da0f0ea87cf34/USER', 198566)
mfv_stoplb_tau000300um_M0800_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLBottom_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-3fc3df6cad9759e172805264961202e2/USER', 197615)
mfv_stoplb_tau010000um_M0800_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLBottom_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-ff0adf15b46e30b6ad0eef367d96740f/USER', 98799)
mfv_stoplb_tau001000um_M0800_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLBottom_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-9ad2680aa9624d9d67845edc540e41ff/USER', 146004)
mfv_stoplb_tau030000um_M0800_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLBottom_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-28fc473e7a040d30647554dd5f566cc2/USER', 199698)
mfv_stopld_tau000100um_M1000_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLD_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-f8313999f997ca3f44fb6d56de57b9dc/USER', 199076)
mfv_stopld_tau000300um_M1000_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLD_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-0b856e5f47260dd1095bb969ed6db25a/USER', 198992)
mfv_stopld_tau010000um_M1000_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLD_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-c06b640080abfacf38a5dfaf73f83f48/USER', 98679)
mfv_stopld_tau001000um_M1000_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLD_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-368ac477467d1ea3121e42abbc3b7cab/USER', 198608)
mfv_stopld_tau030000um_M1000_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLD_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-1294af63a9363b024511c9e088d0e7b6/USER', 187359)
mfv_stopld_tau000100um_M1200_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLD_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-97ce8a17c95f8a01743ddaa4f2a044c4/USER', 195326)
mfv_stopld_tau000300um_M1200_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLD_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-11eed516d155afb08fb0ad2e1fd83226/USER', 195508)
mfv_stopld_tau010000um_M1200_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLD_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-356643ede6fe1999136db67ec6711a19/USER', 100349)
mfv_stopld_tau001000um_M1200_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLD_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-d546a643c799b7879aae5768d05ad2e7/USER', 201191)
mfv_stopld_tau030000um_M1200_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLD_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-17a11452040298eeae3f8d09cdc129c7/USER', 200851)
mfv_stopld_tau000100um_M1400_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLD_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-929d22f0c660e3f4a41ad7cbd65e0c21/USER', 197836)
mfv_stopld_tau000300um_M1400_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLD_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-5ad51b8b5ccc12cc181dc94683eaefc2/USER', 192550)
mfv_stopld_tau010000um_M1400_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLD_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-f68d1e27fe3fad5039cbe6b07721ffb3/USER', 98583)
mfv_stopld_tau001000um_M1400_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLD_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-f5e439c7f431745c87bdca0e0e768883/USER', 198538)
mfv_stopld_tau030000um_M1400_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLD_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-893b4bd18c85d8a599e96f61d9ab5c44/USER', 200714)
mfv_stopld_tau000100um_M1600_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLD_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-15f853b4c6abc42d6bd7930f87abc9c2/USER', 201051)
mfv_stopld_tau000300um_M1600_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLD_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-bcb4c157f93b656de73394fe8fb2756e/USER', 196540)
mfv_stopld_tau010000um_M1600_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLD_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-da32e47314b4c0096cb5944a154576ce/USER', 100274)
mfv_stopld_tau001000um_M1600_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLD_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-49639b18d97f2075afb52cf6328ecdf3/USER', 99126)
mfv_stopld_tau030000um_M1600_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLD_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-16704665e684d94afd050c41c64f7562/USER', 98312)
mfv_stopld_tau000100um_M1800_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLD_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-b7df69fd005acb965b3629e4ff595d1f/USER', 200828)
mfv_stopld_tau000300um_M1800_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLD_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-b7291b195e6f1fcbb2330a9571ff44d2/USER', 198147)
mfv_stopld_tau010000um_M1800_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLD_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-41b0c7fd7dd18d02752b950a81326177/USER', 99667)
mfv_stopld_tau001000um_M1800_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLD_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-33cfacc6e384fbba8bfca1c23eda463e/USER', 101005)
mfv_stopld_tau030000um_M1800_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLD_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-7c47fb0d5879b592b8549c35b93b6ed4/USER', 97762)
mfv_stopld_tau000100um_M0200_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLD_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-1789e78e1e12327a45daa4aa18382d92/USER', 198799)
mfv_stopld_tau000300um_M0200_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLD_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-7055cff3d1073bfe1078cca1cfbb41db/USER', 155703)
mfv_stopld_tau010000um_M0200_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLD_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-c59fd6253cb7e5f497be99071c99e3a9/USER', 197403)
mfv_stopld_tau001000um_M0200_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLD_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-67eb59970b24dc31fdd2d3b2cb7f069a/USER', 193307)
mfv_stopld_tau030000um_M0200_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLD_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-871669d99303ca8753d59907d750eae3/USER', 198511)
mfv_stopld_tau000100um_M0300_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLD_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-1fc8a7cf4c2dae54a58fcabd0a123964/USER', 197379)
mfv_stopld_tau000300um_M0300_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLD_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-6329f9c6af13b5936f483cf97b4e4b09/USER', 197934)
mfv_stopld_tau010000um_M0300_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLD_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-abf9e1937b46576d69a9b9f987b723e1/USER', 195028)
mfv_stopld_tau001000um_M0300_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLD_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-d4fdd990ce4e35965deb73bb64a8a377/USER', 199705)
mfv_stopld_tau030000um_M0300_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLD_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-90bfe8894565eacc36d4a3d0ff664ca0/USER', 199931)
mfv_stopld_tau000100um_M0400_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLD_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-8adc1af59d70a2214af39d094c7a7dcd/USER', 201684)
mfv_stopld_tau000300um_M0400_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLD_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-357645537c9bd292ce20af62fbcd3147/USER', 199890)
mfv_stopld_tau010000um_M0400_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLD_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-e69745a11561f03f3b285f0af5264bfe/USER', 190765)
mfv_stopld_tau001000um_M0400_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLD_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-3cd4d40beef2ff9f0d86da22b1f0f1d3/USER', 192163)
mfv_stopld_tau030000um_M0400_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLD_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-2d8261f30ed59e66783ce23d0351e509/USER', 186742)
mfv_stopld_tau000100um_M0600_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLD_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-e11e22862073d8b29749ba64f3d02ef3/USER', 203406)
mfv_stopld_tau000300um_M0600_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLD_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-2a41e599bce9e64e6e126a4026db737a/USER', 199321)
mfv_stopld_tau010000um_M0600_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLD_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-3c46c6068456dfc7783b316de81d30ef/USER', 195818)
mfv_stopld_tau001000um_M0600_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLD_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-5d7e12c0934cb5c55ec638e86f9ec967/USER', 184999)
mfv_stopld_tau030000um_M0600_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLD_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-fb77851efdd76e36f6686ac3336ccc20/USER', 193864)
mfv_stopld_tau000100um_M0800_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLD_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-94eb3c025f47b83422a7feace8cef398/USER', 184102)
mfv_stopld_tau000300um_M0800_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLD_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-abeaada5ec996acbba073296c62b5dda/USER', 169590)
mfv_stopld_tau010000um_M0800_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLD_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-7c28a8071152225cd35a1a27e3828cda/USER', 99313)
mfv_stopld_tau001000um_M0800_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLD_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-4932078e155d4db80deb13cbbe933fdd/USER', 200829)
mfv_stopld_tau030000um_M0800_2017.add_dataset('stoplborld_preineff', '/DisplacedSUSY_stopToLD_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_preineffLepMum_2017-76df41eb40e0ec8282f4f3f2e203708d/USER', 197094)

mfv_stoplb_tau000100um_M1000_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLBottom_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-38b961d0167c38f246262d0cf0821e30/USER', 193961)
mfv_stoplb_tau000300um_M1000_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLBottom_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-2cdcb39286dab64cfc9ab4ff963c6075/USER', 186260)
mfv_stoplb_tau010000um_M1000_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLBottom_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-e62dfc4006e3145e1dedbf8f63cc9582/USER', 98261)
mfv_stoplb_tau001000um_M1000_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLBottom_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-6a01a7a9339568bccbacdf1249ba6ac0/USER', 197193)
mfv_stoplb_tau030000um_M1000_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLBottom_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-952a1cf50e57db4aee253871f260daf8/USER', 200668)
mfv_stoplb_tau000100um_M1200_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLBottom_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-edc449ca59c439e2cc23cd95cbbb49f0/USER', 199921)
mfv_stoplb_tau000300um_M1200_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLBottom_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-1c356b19c9eeff9d07b3258d9f03c643/USER', 195189)
mfv_stoplb_tau010000um_M1200_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLBottom_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-fc5646691cb126efdcd788951c0c3270/USER', 100156)
mfv_stoplb_tau001000um_M1200_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLBottom_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-781d04216a27cfba92f5b2708d8c7c89/USER', 197902)
mfv_stoplb_tau030000um_M1200_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLBottom_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-a1d5fc0db3501be34975a8c715cb60cf/USER', 200464)
mfv_stoplb_tau000100um_M1400_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLBottom_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-afe5873d585a3299d0cac1ee059a9f3d/USER', 187459)
mfv_stoplb_tau000300um_M1400_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLBottom_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-72ff811bc195807f49535920926374da/USER', 200304)
mfv_stoplb_tau010000um_M1400_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLBottom_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-cf2d47b47c4ed42a2dc5238ff1207542/USER', 98900)
mfv_stoplb_tau001000um_M1400_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLBottom_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-6c4cb9e1c6835fca9393f0c3c607a789/USER', 192400)
mfv_stoplb_tau030000um_M1400_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLBottom_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-e2a0c66a230d34bfd72db087f93425e2/USER', 197635)
mfv_stoplb_tau000100um_M1600_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLBottom_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-0f568bbb2e755ee38a5b8eb6edb288d7/USER', 130204)
mfv_stoplb_tau000300um_M1600_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLBottom_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-a7b8d3b3344fe4df0f1917df17ccaecc/USER', 198070)
mfv_stoplb_tau010000um_M1600_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLBottom_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-4771a3bbcaf3f5073b5e1fac5027de87/USER', 98745)
mfv_stoplb_tau001000um_M1600_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLBottom_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-c23105f2a1d509f933d21747664bfc7c/USER', 91871)
mfv_stoplb_tau030000um_M1600_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLBottom_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-1f819f9ac86a2526c35287e210f480a5/USER', 82216)
mfv_stoplb_tau000100um_M1800_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLBottom_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-45022ea641ad682b936c2e8db59228b9/USER', 191607)
mfv_stoplb_tau000300um_M1800_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLBottom_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-ffbcc7305e6ab87811178c1c073319ae/USER', 200792)
mfv_stoplb_tau010000um_M1800_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLBottom_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-f5729039f4fe5bec53c520d09e6bed2a/USER', 101386)
mfv_stoplb_tau001000um_M1800_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLBottom_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-82c7db99a9c3af254012988846195ae4/USER', 98858)
mfv_stoplb_tau030000um_M1800_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLBottom_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-476bb8d45ba40cc3a50e5466fbdfd0ef/USER', 99225)
mfv_stoplb_tau000100um_M0200_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLBottom_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-5eb14100fc75db5afc701d503006385d/USER', 198760)
mfv_stoplb_tau000300um_M0200_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLBottom_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-33eaf1a985802103d4a379c84c023833/USER', 187003)
mfv_stoplb_tau010000um_M0200_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLBottom_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-b2e41e7ebb710dbe0f40ba434f460b35/USER', 199948)
mfv_stoplb_tau001000um_M0200_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLBottom_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-de77d5496c954883187021aafbdddadb/USER', 196687)
mfv_stoplb_tau030000um_M0200_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLBottom_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-ba0d8aa9ee47146dab29a43e6ac13304/USER', 199267)
mfv_stoplb_tau000100um_M0300_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLBottom_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-5e0e08c6a469d71b13677e414ad25258/USER', 196246)
mfv_stoplb_tau000300um_M0300_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLBottom_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-4f1ea9372daca109bad6bd31f11d1b3b/USER', 183219)
mfv_stoplb_tau010000um_M0300_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLBottom_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-0c2dd0aa20a03993d9f0cf0691459005/USER', 199832)
mfv_stoplb_tau001000um_M0300_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLBottom_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-1444a1450ee018c16115f294c9cfeabd/USER', 200296)
mfv_stoplb_tau030000um_M0300_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLBottom_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-bb652f2f49deeecc962b96806311813a/USER', 200170)
mfv_stoplb_tau000100um_M0400_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLBottom_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-974b70c0222040a70b0ae8816762234e/USER', 197597)
mfv_stoplb_tau000300um_M0400_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLBottom_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-9fe337a9a399b512b8c41c3272781704/USER', 195221)
mfv_stoplb_tau010000um_M0400_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLBottom_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-0cbfdf404f38336205938f6302276a9a/USER', 198737)
mfv_stoplb_tau001000um_M0400_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLBottom_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-04b4f4446e4118cadef111d0480e6ef8/USER', 197003)
mfv_stoplb_tau030000um_M0400_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLBottom_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-2682217e3c061ae0e109059ac0de2f26/USER', 191913)
mfv_stoplb_tau000100um_M0600_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLBottom_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-535063703c8053e530823b9fddad0623/USER', 194663)
mfv_stoplb_tau000300um_M0600_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLBottom_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-1d7452fc5eb954118859b515fb0e5bbb/USER', 201839)
mfv_stoplb_tau010000um_M0600_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLBottom_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-b4efe373e6205106449b49d72ebf74d6/USER', 188463)
mfv_stoplb_tau001000um_M0600_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLBottom_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-041a97dcc7e735b93dc7221e7a4fcd17/USER', 195368)
mfv_stoplb_tau030000um_M0600_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLBottom_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-975b44b68dd28366881b11e8246dca9e/USER', 199015)
mfv_stoplb_tau000100um_M0800_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLBottom_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-a517eb4f99399460107570ae0628b3da/USER', 198566)
mfv_stoplb_tau000300um_M0800_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLBottom_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-01ad281d8f84b98ee6261a7a24816fe9/USER', 197615)
mfv_stoplb_tau010000um_M0800_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLBottom_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-c9daa7dba3db7147ea09ab0715f55bb8/USER', 98799)
mfv_stoplb_tau001000um_M0800_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLBottom_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-d761691bb111adc15ea85fc20badc84a/USER', 146004)
mfv_stoplb_tau030000um_M0800_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLBottom_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-a02136e4043402545a1d0b8a5fa98856/USER', 199698)
mfv_stopld_tau000100um_M1000_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLD_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-d664b8a3f7830690e0b48db57e713a62/USER', 199076)
mfv_stopld_tau000300um_M1000_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLD_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-95286d2dddcd9ff751509258d69d77f8/USER', 198992)
mfv_stopld_tau010000um_M1000_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLD_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-e31ff6f6cc2e362c6f1f5d4d44570e6d/USER', 98679)
mfv_stopld_tau001000um_M1000_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLD_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-21fb3253a6b15fc7e188ed60693b8272/USER', 198608)
mfv_stopld_tau030000um_M1000_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLD_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-abf271171e039e27ad20c96f1236289d/USER', 187359)
mfv_stopld_tau000100um_M1200_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLD_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-fabc3ab947bc78fc7fed9d8ca41c7371/USER', 195326)
mfv_stopld_tau000300um_M1200_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLD_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-ab3ed3c7cf3ddd4cebef95c471c2ee98/USER', 195508)
mfv_stopld_tau010000um_M1200_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLD_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-00147be307ac6e040cf5f49309199ba5/USER', 100349)
mfv_stopld_tau001000um_M1200_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLD_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-89f3f7fd5ced7a1e27e9cdf4a1e7f4b6/USER', 201191)
mfv_stopld_tau030000um_M1200_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLD_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-0986bdad269a6dae02dd875719e8723d/USER', 200851)
mfv_stopld_tau000100um_M1400_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLD_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-cb999eec7ec8f09019e0761d26801530/USER', 197836)
mfv_stopld_tau000300um_M1400_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLD_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-1588461bc8c8fe662437cd86d9170a38/USER', 192550)
mfv_stopld_tau010000um_M1400_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLD_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-b74496a7d4a388d6c0c71340724f00f8/USER', 98583)
mfv_stopld_tau001000um_M1400_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLD_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-1338bf24c067f482b17a62010b334d2e/USER', 198538)
mfv_stopld_tau030000um_M1400_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLD_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-b71798213247765c5d818bc328358d24/USER', 200714)
mfv_stopld_tau000100um_M1600_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLD_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-a8267d1c87c529b64cf3f993bcce4268/USER', 201051)
mfv_stopld_tau000300um_M1600_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLD_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-b7bf26d160d056f57000b9a6f680fbad/USER', 196540)
mfv_stopld_tau010000um_M1600_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLD_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-838543d4a0a6e8f36364aafc49528ac1/USER', 100274)
mfv_stopld_tau001000um_M1600_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLD_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-4911b39c84a628185d0afcc1e3dff9ce/USER', 99126)
mfv_stopld_tau030000um_M1600_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLD_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-5b69a8c069c1b12576318fa902dc8e7c/USER', 98312)
mfv_stopld_tau000100um_M1800_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLD_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-b3620fe6456abd8c3a7be2ef2cc039c6/USER', 200828)
mfv_stopld_tau000300um_M1800_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLD_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-99a75db53bd4074648d6453f80fa656e/USER', 198147)
mfv_stopld_tau010000um_M1800_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLD_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-603f845b5b9799398ca153c1a233ee2a/USER', 99667)
mfv_stopld_tau001000um_M1800_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLD_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-3c3c301b2aecc621f58d9e696b64327b/USER', 101005)
mfv_stopld_tau030000um_M1800_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLD_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-7e60b8bdbb597b96dc6f916e847c5e8c/USER', 97762)
mfv_stopld_tau000100um_M0200_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLD_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-315214235ff729970dd511d62f0ff0f1/USER', 198799)
mfv_stopld_tau000300um_M0200_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLD_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-c421e66561f90e37c803895094e32d48/USER', 155703)
mfv_stopld_tau010000um_M0200_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLD_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-0b83473c114548f9e221d288e13e267c/USER', 197403)
mfv_stopld_tau001000um_M0200_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLD_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-42b17fff56ef48d28709583b76b95f35/USER', 193307)
mfv_stopld_tau030000um_M0200_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLD_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-5e6194d9572cf69aaa1b07e0c2e90711/USER', 198511)
mfv_stopld_tau000100um_M0300_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLD_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-16e1b1b4ded34d645347429bc7175290/USER', 197379)
mfv_stopld_tau000300um_M0300_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLD_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-79c90a974430e12edf1943c5ad4b4d0d/USER', 197934)
mfv_stopld_tau010000um_M0300_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLD_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-e9a6b4ba697567a01707fe16272016eb/USER', 195028)
mfv_stopld_tau001000um_M0300_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLD_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-122422c44c0aac55ac2642939b8742d8/USER', 199705)
mfv_stopld_tau030000um_M0300_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLD_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-06c874dd4b2d9f11f5b86828b54159a4/USER', 199931)
mfv_stopld_tau000100um_M0400_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLD_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-02ae066e133622f1649750a93802083a/USER', 201684)
mfv_stopld_tau000300um_M0400_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLD_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-8c27c26f7ed4b632f73ac864f143cced/USER', 199890)
mfv_stopld_tau010000um_M0400_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLD_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-f55a7cf7663455170acd979d0eaa2bf8/USER', 190765)
mfv_stopld_tau001000um_M0400_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLD_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-6de84fbb745d7473232df7156234eb45/USER', 192163)
mfv_stopld_tau030000um_M0400_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLD_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-cca1a62720698065f204dc54c20c5e5e/USER', 186742)
mfv_stopld_tau000100um_M0600_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLD_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-1e63c70adcf0d137d8063ae5c6a68a73/USER', 203406)
mfv_stopld_tau000300um_M0600_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLD_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-578eee879ef3a9306f7d2a3ad6d8c7eb/USER', 199321)
mfv_stopld_tau010000um_M0600_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLD_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-e53579a6d6771d80748791bb02ce429b/USER', 195818)
mfv_stopld_tau001000um_M0600_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLD_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-43f43c12e9f0f6e82bc7d3245647a9a6/USER', 184999)
mfv_stopld_tau030000um_M0600_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLD_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-b93295920aa12ccfc6e9556d74e56ca9/USER', 193864)
mfv_stopld_tau000100um_M0800_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLD_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-3c801e4b88177b05db71c8c0328e782d/USER', 184102)
mfv_stopld_tau000300um_M0800_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLD_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-e91baa41d617e0c276c1d61f7446f059/USER', 169590)
mfv_stopld_tau010000um_M0800_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLD_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-0f8f76d129bc883c84ff9fd780a2d92d/USER', 99313)
mfv_stopld_tau001000um_M0800_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLD_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-2d672c40a238018c3b8d0a8cb9bc8757/USER', 200829)
mfv_stopld_tau030000um_M0800_2017.add_dataset('stoplborld_postineff', '/DisplacedSUSY_stopToLD_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/aduquett-NtuplestoplborldULV30_postineffLepMum_2017-606d105d2ba8ee8259c51d544f1030d7/USER', 197094)

wjetstolnu_0j_2017.add_dataset('wjetstolnu_preineff', '/WJetsToLNu_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8/aduquett-NtupleOnnormdzULV30_preineffLepMum_2017-0f6c022d9cdc7028e517b0fff8732cfe/USER', 86756)
wjetstolnu_1j_2017.add_dataset('wjetstolnu_preineff', '/WJetsToLNu_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8/aduquett-NtupleOnnormdzULV30_preineffLepMum_2017-77e3d4c897439bd2278d207d58fa89aa/USER', 186256)
wjetstolnu_2j_2017.add_dataset('wjetstolnu_preineff', '/WJetsToLNu_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8/aduquett-NtupleOnnormdzULV30_preineffLepMum_2017-bd45d297fe163d2124aeb164ae832b63/USER', 177007)
dyjetstollM10_2017.add_dataset('wjetstolnu_preineff', '/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/aduquett-NtupleOnnormdzULV30_preineffLepMum_2017-4df0bd0a778e6d377b3c3b6b0bee485a/USER', 2138)
dyjetstollM50_2017.add_dataset('wjetstolnu_preineff', '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/aduquett-NtupleOnnormdzULV30_preineffLepMum_2017-270e6bfbbc74b7e48a43e7741624ead6/USER', 91449)
ZHToSSTodddd_tau100um_M15_2017.add_dataset('wjetstolnu_preineff', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-15_ctauS-0p1_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_preineffLepMum_2017-4b0c3a1fafec13dcc4344d1fb4dcdb6d/USER', 49121)
ZHToSSTodddd_tau300um_M15_2017.add_dataset('wjetstolnu_preineff', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-15_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_preineffLepMum_2017-b17deca23072a157b98cfa55e4ab1bd5/USER', 50000)
ZHToSSTodddd_tau1mm_M15_2017.add_dataset('wjetstolnu_preineff', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-15_ctauS-1_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_preineffLepMum_2017-74a6dd19f3b620053cb659f6cded6ca8/USER', 49999)
ZHToSSTodddd_tau3mm_M15_2017.add_dataset('wjetstolnu_preineff', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-15_ctauS-3_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_preineffLepMum_2017-f3c18118db57bb20d6e04e74b5649bc1/USER', 50000)
ZHToSSTodddd_tau10mm_M15_2017.add_dataset('wjetstolnu_preineff', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-15_ctauS-10_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_preineffLepMum_2017-8f56768d7046821d82886380299bcadc/USER', 50000)
ZHToSSTodddd_tau30mm_M15_2017.add_dataset('wjetstolnu_preineff', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-15_ctauS-30_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_preineffLepMum_2017-1a1dd94f3c0e01167db4ac37b3863817/USER', 49999)
ZHToSSTodddd_tau100um_M40_2017.add_dataset('wjetstolnu_preineff', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-40_ctauS-0p1_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_preineffLepMum_2017-17662f360bf2ea6746d5e9600f01287a/USER', 49999)
ZHToSSTodddd_tau300um_M40_2017.add_dataset('wjetstolnu_preineff', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-40_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_preineffLepMum_2017-c19fe1fb02567c06f4bf39b41de79d22/USER', 49999)
ZHToSSTodddd_tau1mm_M40_2017.add_dataset('wjetstolnu_preineff', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-40_ctauS-1_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_preineffLepMum_2017-9771b21c2a0e98730dde498bb81472fd/USER', 50000)
ZHToSSTodddd_tau3mm_M40_2017.add_dataset('wjetstolnu_preineff', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-40_ctauS-3_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_preineffLepMum_2017-9eafc9c6e9b249540085089bc7030f90/USER', 49996)
ZHToSSTodddd_tau10mm_M40_2017.add_dataset('wjetstolnu_preineff', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-40_ctauS-10_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_preineffLepMum_2017-fb52d7c0b47e5546ea7fc91757417da3/USER', 49998)
ZHToSSTodddd_tau30mm_M40_2017.add_dataset('wjetstolnu_preineff', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-40_ctauS-30_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_preineffLepMum_2017-4f75a9b26e632cf215cc5a35ebf38227/USER', 50000)
ZHToSSTodddd_tau100um_M55_2017.add_dataset('wjetstolnu_preineff', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-55_ctauS-0p1_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_preineffLepMum_2017-ab16a2adb0682a8f72f0e6350a23be14/USER', 49999)
ZHToSSTodddd_tau300um_M55_2017.add_dataset('wjetstolnu_preineff', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-55_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_preineffLepMum_2017-67b20ccfa03687ac1ca98fec78dcda00/USER', 49997)
ZHToSSTodddd_tau1mm_M55_2017.add_dataset('wjetstolnu_preineff', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_preineffLepMum_2017-892a2cdf648086816d29d741b3936d49/USER', 49997)
ZHToSSTodddd_tau3mm_M55_2017.add_dataset('wjetstolnu_preineff', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-55_ctauS-3_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_preineffLepMum_2017-4a5345a73c3c81fa634a9182c6e0b258/USER', 49995)
ZHToSSTodddd_tau10mm_M55_2017.add_dataset('wjetstolnu_preineff', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-55_ctauS-10_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_preineffLepMum_2017-f9ccff64ae5f5b325c1784d7bfc4ad7b/USER', 49991)
ZHToSSTodddd_tau30mm_M55_2017.add_dataset('wjetstolnu_preineff', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-55_ctauS-30_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_preineffLepMum_2017-0b769a67e5a944604d385f321d6b36a9/USER', 49998)
WplusHToSSTodddd_tau100um_M15_2017.add_dataset('wjetstolnu_preineff', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-0p1_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_preineffLepMum_2017-4df1b75652af4d8f15fc9bfefee981bf/USER', 50000)
WplusHToSSTodddd_tau300um_M15_2017.add_dataset('wjetstolnu_preineff', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_preineffLepMum_2017-69e99fc68fd992aad90505bc7384ea0b/USER', 49000)
WplusHToSSTodddd_tau1mm_M15_2017.add_dataset('wjetstolnu_preineff', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-1_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_preineffLepMum_2017-50cc845f6fc4503b943cf2cf7c774031/USER', 49999)
WplusHToSSTodddd_tau3mm_M15_2017.add_dataset('wjetstolnu_preineff', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-3_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_preineffLepMum_2017-927386be5d1e89b854a99ccb81821fb6/USER', 50000)
WplusHToSSTodddd_tau30mm_M15_2017.add_dataset('wjetstolnu_preineff', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-30_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_preineffLepMum_2017-779e2f7eb993029b48b20168fcd1b161/USER', 50000)
WplusHToSSTodddd_tau300um_M40_2017.add_dataset('wjetstolnu_preineff', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_preineffLepMum_2017-530111ab49969a659ab2a8e3f9acaee9/USER', 49996)
WplusHToSSTodddd_tau1mm_M40_2017.add_dataset('wjetstolnu_preineff', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-1_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_preineffLepMum_2017-e9a38a14532c2067226c185341a14955/USER', 49999)
WplusHToSSTodddd_tau3mm_M40_2017.add_dataset('wjetstolnu_preineff', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-3_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_preineffLepMum_2017-c14aae83878c66014a0f54de4f658638/USER', 48000)
WplusHToSSTodddd_tau30mm_M40_2017.add_dataset('wjetstolnu_preineff', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-30_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_preineffLepMum_2017-e1b45eceaa81572155b336661746fedd/USER', 49997)
WplusHToSSTodddd_tau100um_M55_2017.add_dataset('wjetstolnu_preineff', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-0p1_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_preineffLepMum_2017-390d8a6e0a8ed1abb47aeb82ff11a7ba/USER', 49997)
WplusHToSSTodddd_tau300um_M55_2017.add_dataset('wjetstolnu_preineff', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_preineffLepMum_2017-7a076c45ce0447d69616b347b352e68a/USER', 49995)
WplusHToSSTodddd_tau1mm_M55_2017.add_dataset('wjetstolnu_preineff', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_preineffLepMum_2017-fcbb6c694872c8060d992f3e98086303/USER', 49991)
WplusHToSSTodddd_tau3mm_M55_2017.add_dataset('wjetstolnu_preineff', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-3_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_preineffLepMum_2017-06ce0650577c38e5d7bfc2d875875eb2/USER', 49994)
WplusHToSSTodddd_tau30mm_M55_2017.add_dataset('wjetstolnu_preineff', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-30_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_preineffLepMum_2017-e7257148a4f288513bfbd3f84eca445d/USER', 47998)
WminusHToSSTodddd_tau1mm_M15_2017.add_dataset('wjetstolnu_preineff', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-1_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_preineffLepMum_2017-0e8cd3619d5c2685d83fab8a0818bd3e/USER', 48999)
WminusHToSSTodddd_tau3mm_M15_2017.add_dataset('wjetstolnu_preineff', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-3_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_preineffLepMum_2017-94100bb10c763d6adea0250a024a8933/USER', 48999)
WminusHToSSTodddd_tau10mm_M15_2017.add_dataset('wjetstolnu_preineff', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-10_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_preineffLepMum_2017-59a6820af7982a838fc729d9ee6c9ff6/USER', 50000)
WminusHToSSTodddd_tau30mm_M15_2017.add_dataset('wjetstolnu_preineff', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-30_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_preineffLepMum_2017-b1b1d291fff6e9815a4b1183fad71a02/USER', 50000)
WminusHToSSTodddd_tau300um_M40_2017.add_dataset('wjetstolnu_preineff', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_preineffLepMum_2017-a39c914b617e55a7d59803feb6593990/USER', 49997)
WminusHToSSTodddd_tau1mm_M40_2017.add_dataset('wjetstolnu_preineff', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-1_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_preineffLepMum_2017-effd26fa36b38c214b1b692039782763/USER', 48000)
WminusHToSSTodddd_tau3mm_M40_2017.add_dataset('wjetstolnu_preineff', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-3_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_preineffLepMum_2017-702f2531a8d5ca3def2e921cd372e5c0/USER', 49997)
WminusHToSSTodddd_tau10mm_M40_2017.add_dataset('wjetstolnu_preineff', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-10_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_preineffLepMum_2017-60b40f496d920180618b0bc1e33150e0/USER', 49999)
WminusHToSSTodddd_tau30mm_M40_2017.add_dataset('wjetstolnu_preineff', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-30_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_preineffLepMum_2017-181ef0144186f4c2edd308a7e9edc763/USER', 49998)
WminusHToSSTodddd_tau300um_M55_2017.add_dataset('wjetstolnu_preineff', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_preineffLepMum_2017-c2b9d396bb90b617954951a3895ef5d9/USER', 47995)
WminusHToSSTodddd_tau1mm_M55_2017.add_dataset('wjetstolnu_preineff', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_preineffLepMum_2017-d1136e70d376764bed15783cfce6ee21/USER', 49995)
WminusHToSSTodddd_tau3mm_M55_2017.add_dataset('wjetstolnu_preineff', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-3_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_preineffLepMum_2017-c34dd8f84477cb350097976ad963065a/USER', 49992)
WminusHToSSTodddd_tau10mm_M55_2017.add_dataset('wjetstolnu_preineff', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-10_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_preineffLepMum_2017-673b42ac3b79af3bb51e59a6690feab6/USER', 49994)
WminusHToSSTodddd_tau30mm_M55_2017.add_dataset('wjetstolnu_preineff', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-30_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_preineffLepMum_2017-cfabbdde4ff4f407a076c182284c700b/USER', 49993)

wjetstolnu_0j_2017.add_dataset('wjetstolnu_postineff', '/WJetsToLNu_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8/aduquett-NtupleOnnormdzULV30_postineffLepMum_2017-c3c18495f24fb7a96d410618de71d556/USER', 84217)
wjetstolnu_1j_2017.add_dataset('wjetstolnu_postineff', '/WJetsToLNu_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8/aduquett-NtupleOnnormdzULV30_postineffLepMum_2017-c3c015414273d93bb688b378b2bda21a/USER', 180758)
wjetstolnu_2j_2017.add_dataset('wjetstolnu_postineff', '/WJetsToLNu_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8/aduquett-NtupleOnnormdzULV30_postineffLepMum_2017-e0bb6d0b21a66efaf5ef43be913f3b75/USER', 170804)
dyjetstollM10_2017.add_dataset('wjetstolnu_postineff', '/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/aduquett-NtupleOnnormdzULV30_postineffLepMum_2017-f10150f77d002ae747efe35eb649d337/USER', 1964)
dyjetstollM50_2017.add_dataset('wjetstolnu_postineff', '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/aduquett-NtupleOnnormdzULV30_postineffLepMum_2017-ea85cbb21fda36b7caafa0e9c86494ca/USER', 75694)
ZHToSSTodddd_tau100um_M15_2017.add_dataset('wjetstolnu_postineff', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-15_ctauS-0p1_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_postineffLepMum_2017-0004df3ee32eb62627bf007391492ef3/USER', 49121)
ZHToSSTodddd_tau300um_M15_2017.add_dataset('wjetstolnu_postineff', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-15_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_postineffLepMum_2017-e3b75358ddddab68d9220b701d609ebf/USER', 50000)
ZHToSSTodddd_tau1mm_M15_2017.add_dataset('wjetstolnu_postineff', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-15_ctauS-1_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_postineffLepMum_2017-d1688f6cbec5a86f542ae971e9071b95/USER', 49999)
ZHToSSTodddd_tau3mm_M15_2017.add_dataset('wjetstolnu_postineff', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-15_ctauS-3_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_postineffLepMum_2017-3a5fe39fb2554accc6101541a34b412a/USER', 50000)
ZHToSSTodddd_tau10mm_M15_2017.add_dataset('wjetstolnu_postineff', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-15_ctauS-10_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_postineffLepMum_2017-3a4f111dfa476b4a90cded8edbdde54d/USER', 50000)
ZHToSSTodddd_tau30mm_M15_2017.add_dataset('wjetstolnu_postineff', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-15_ctauS-30_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_postineffLepMum_2017-cbf03296790c3cdf01d10b5ba9736c3a/USER', 49999)
ZHToSSTodddd_tau100um_M40_2017.add_dataset('wjetstolnu_postineff', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-40_ctauS-0p1_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_postineffLepMum_2017-722bad29d3f678df74db9167545ea733/USER', 49999)
ZHToSSTodddd_tau300um_M40_2017.add_dataset('wjetstolnu_postineff', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-40_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_postineffLepMum_2017-fd6c2b29527a98611a80af8cf6f8443c/USER', 49999)
ZHToSSTodddd_tau1mm_M40_2017.add_dataset('wjetstolnu_postineff', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-40_ctauS-1_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_postineffLepMum_2017-ebfd9756cab285670051ebd4a6d0bb60/USER', 50000)
ZHToSSTodddd_tau3mm_M40_2017.add_dataset('wjetstolnu_postineff', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-40_ctauS-3_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_postineffLepMum_2017-63d451f0d7622b42eb7480856544db44/USER', 49996)
ZHToSSTodddd_tau10mm_M40_2017.add_dataset('wjetstolnu_postineff', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-40_ctauS-10_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_postineffLepMum_2017-d6f43bd923a5b1f6544fbe29a90e1594/USER', 49998)
ZHToSSTodddd_tau30mm_M40_2017.add_dataset('wjetstolnu_postineff', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-40_ctauS-30_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_postineffLepMum_2017-16f9254d04c870b6827ec306f2179888/USER', 50000)
ZHToSSTodddd_tau100um_M55_2017.add_dataset('wjetstolnu_postineff', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-55_ctauS-0p1_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_postineffLepMum_2017-aabdf53c5324ed23da667e621a01077b/USER', 49999)
ZHToSSTodddd_tau300um_M55_2017.add_dataset('wjetstolnu_postineff', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-55_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_postineffLepMum_2017-ceb75ac530df633f66588f44b4d83b07/USER', 49997)
ZHToSSTodddd_tau1mm_M55_2017.add_dataset('wjetstolnu_postineff', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_postineffLepMum_2017-83bea8899a99f8803e9e1edf095ee502/USER', 49997)
ZHToSSTodddd_tau3mm_M55_2017.add_dataset('wjetstolnu_postineff', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-55_ctauS-3_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_postineffLepMum_2017-b126aa96a5c0dd96c428efafbabf2313/USER', 49995)
ZHToSSTodddd_tau10mm_M55_2017.add_dataset('wjetstolnu_postineff', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-55_ctauS-10_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_postineffLepMum_2017-e34fbfa4d530f03e59f41578f91d25f0/USER', 48343)
ZHToSSTodddd_tau30mm_M55_2017.add_dataset('wjetstolnu_postineff', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-55_ctauS-30_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_postineffLepMum_2017-f60a9fd2ec4c5da8e1fdf0af3cb18727/USER', 49998)
WplusHToSSTodddd_tau100um_M15_2017.add_dataset('wjetstolnu_postineff', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-0p1_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_postineffLepMum_2017-b9aabc2fc3433cc32ff88f22e2e30b8a/USER', 50000)
WplusHToSSTodddd_tau300um_M15_2017.add_dataset('wjetstolnu_postineff', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_postineffLepMum_2017-c8039708b081780d994db3d1ef30d36a/USER', 49000)
WplusHToSSTodddd_tau1mm_M15_2017.add_dataset('wjetstolnu_postineff', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-1_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_postineffLepMum_2017-711ae0390b92df53b76a91529cfdde37/USER', 49999)
WplusHToSSTodddd_tau3mm_M15_2017.add_dataset('wjetstolnu_postineff', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-3_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_postineffLepMum_2017-96bf90a223e098712a75941f8cd755f7/USER', 50000)
WplusHToSSTodddd_tau30mm_M15_2017.add_dataset('wjetstolnu_postineff', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-30_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_postineffLepMum_2017-38d43c2372bad0e49bc38d45ecfcef13/USER', 50000)
WplusHToSSTodddd_tau300um_M40_2017.add_dataset('wjetstolnu_postineff', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_postineffLepMum_2017-2edd06aa1d1b1f51baf575ca6529a70e/USER', 49996)
WplusHToSSTodddd_tau1mm_M40_2017.add_dataset('wjetstolnu_postineff', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-1_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_postineffLepMum_2017-1ca2b1f78dfb142abd479f6084c47f1d/USER', 49999)
WplusHToSSTodddd_tau3mm_M40_2017.add_dataset('wjetstolnu_postineff', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-3_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_postineffLepMum_2017-14ebddbeaa69d040def78d34ab4693c4/USER', 48000)
WplusHToSSTodddd_tau30mm_M40_2017.add_dataset('wjetstolnu_postineff', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-30_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_postineffLepMum_2017-2c00bf675fef859129a1bf449ea8aa90/USER', 49997)
WplusHToSSTodddd_tau100um_M55_2017.add_dataset('wjetstolnu_postineff', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-0p1_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_postineffLepMum_2017-ba73c3c59af6ec760f0b3582a737c4ba/USER', 49997)
WplusHToSSTodddd_tau300um_M55_2017.add_dataset('wjetstolnu_postineff', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_postineffLepMum_2017-f01707cc01b70423954dcfc735b88431/USER', 49995)
WplusHToSSTodddd_tau1mm_M55_2017.add_dataset('wjetstolnu_postineff', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_postineffLepMum_2017-99e0eb0a81a71ea7095930d6016d27a2/USER', 49991)
WplusHToSSTodddd_tau3mm_M55_2017.add_dataset('wjetstolnu_postineff', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-3_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_postineffLepMum_2017-f19c8a1722a04003b0c6f270c99e97c3/USER', 49994)
WplusHToSSTodddd_tau30mm_M55_2017.add_dataset('wjetstolnu_postineff', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-30_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_postineffLepMum_2017-6cf3aaad49670c491975388f99fe3c77/USER', 47998)
WminusHToSSTodddd_tau1mm_M15_2017.add_dataset('wjetstolnu_postineff', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-1_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_postineffLepMum_2017-adba71fccb3f4641e64ff308e6c11a7e/USER', 48999)
WminusHToSSTodddd_tau3mm_M15_2017.add_dataset('wjetstolnu_postineff', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-3_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_postineffLepMum_2017-13659781ae6f4aa29b63d598282247c8/USER', 48999)
WminusHToSSTodddd_tau10mm_M15_2017.add_dataset('wjetstolnu_postineff', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-10_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_postineffLepMum_2017-4589cc25756afc0bafe34c428ca58a16/USER', 50000)
WminusHToSSTodddd_tau30mm_M15_2017.add_dataset('wjetstolnu_postineff', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-30_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_postineffLepMum_2017-52ee63ead9cdb0626bad6e2d93183742/USER', 50000)
WminusHToSSTodddd_tau300um_M40_2017.add_dataset('wjetstolnu_postineff', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_postineffLepMum_2017-be7ee03e85b47ddd1bc616f98c7ef965/USER', 49997)
WminusHToSSTodddd_tau1mm_M40_2017.add_dataset('wjetstolnu_postineff', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-1_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_postineffLepMum_2017-5b4eebc0636d1e20e6224f0399ce3640/USER', 48000)
WminusHToSSTodddd_tau3mm_M40_2017.add_dataset('wjetstolnu_postineff', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-3_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_postineffLepMum_2017-00b51fd6c5f65e7bff98ea0cb95cfbf7/USER', 49997)
WminusHToSSTodddd_tau10mm_M40_2017.add_dataset('wjetstolnu_postineff', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-10_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_postineffLepMum_2017-2d811a15acc7d990b337c338f3b207c6/USER', 49999)
WminusHToSSTodddd_tau30mm_M40_2017.add_dataset('wjetstolnu_postineff', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-30_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_postineffLepMum_2017-d4230878791603590ab0e628ded6cef6/USER', 49998)
WminusHToSSTodddd_tau300um_M55_2017.add_dataset('wjetstolnu_postineff', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_postineffLepMum_2017-a2b47e671855f71233078ce251025e8d/USER', 47995)
WminusHToSSTodddd_tau1mm_M55_2017.add_dataset('wjetstolnu_postineff', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_postineffLepMum_2017-fe46f8fef69a004f13efd5f299c05c9e/USER', 49995)
WminusHToSSTodddd_tau3mm_M55_2017.add_dataset('wjetstolnu_postineff', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-3_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_postineffLepMum_2017-5dfcc313bf5c242400582c99b3ca9397/USER', 48992)
WminusHToSSTodddd_tau10mm_M55_2017.add_dataset('wjetstolnu_postineff', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-10_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_postineffLepMum_2017-41113d77a3c03edebcec81693dbdf6d9/USER', 49994)
WminusHToSSTodddd_tau30mm_M55_2017.add_dataset('wjetstolnu_postineff', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-30_TuneCP5_13TeV-powheg-pythia8/aduquett-NtupleOnnormdzULV30_postineffLepMum_2017-d95e896f6d72baa1e82b50cd817023e3/USER', 49993)

for sample in Lepton_data_samples_20161:
    sample.add_dataset('miniaod', sample.dataset)
for sample in Lepton_data_samples_20162:
    sample.add_dataset('miniaod', sample.dataset)
for sample in data_samples_2017: #+ Lepton_data_samples_2017: #auxiliary_data_samples_2017 + singleelectron_data_samples_2017:
    sample.add_dataset('miniaod', sample.dataset.replace('AOD', 'MINIAOD'))
for sample in data_samples_2018 + auxiliary_data_samples_2018 + egamma_data_samples_2018:
    sample.add_dataset('miniaod', sample.dataset.replace('AOD', 'MINIAOD'))
for sample in Lepton_data_samples_2018:
    sample.add_dataset('miniaod', sample.dataset)

for sample in qcd_lep_samples_20161 + leptonic_samples_20161 + diboson_samples_20161 + met_samples_20161 + ttbar_samples_20161: 
    sample.add_dataset('miniaod', sample.dataset)
for sample in qcd_lep_samples_20162 + leptonic_samples_20162 + diboson_samples_20162 + met_samples_20162 + ttbar_samples_20162: 
    sample.add_dataset('miniaod', sample.dataset)

qcdht0200_2017.add_dataset('miniaod', '/QCD_HT200to300_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v2/MINIAODSIM', 57721120)
qcdht0300_2017.add_dataset('miniaod', '/QCD_HT300to500_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v2/MINIAODSIM',   57191140)
qcdht0500_2017.add_dataset('miniaod', '/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v2/MINIAODSIM',  9188310)
qcdht0500ext_2017.add_dataset('miniaod', '/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6_ext1-v1/MINIAODSIM',  57880117)
qcdht0700_2017.add_dataset('miniaod', '/QCD_HT700to1000_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v2/MINIAODSIM',  45812757)
qcdht1000_2017.add_dataset('miniaod', '/QCD_HT1000to1500_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v2/MINIAODSIM', 15346629)
qcdht1500_2017.add_dataset('miniaod', '/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v1/MINIAODSIM',    7497684)
qcdht2000_2017.add_dataset('miniaod', '/QCD_HT2000toInf_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v2/MINIAODSIM',  5457021)

qcdmupt15_2017.add_dataset('miniaod', '/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v1/MINIAODSIM', 17580112)
qcdpt15mupt5_2017.add_dataset('miniaod', '/QCD_Pt-15To20_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 9019841)
qcdpt20mupt5_2017.add_dataset('miniaod', '/QCD_Pt-20To30_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 64634535)
qcdpt30mupt5_2017.add_dataset('miniaod', '/QCD_Pt-30To50_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 58749714)
qcdpt50mupt5_2017.add_dataset('miniaod', '/QCD_Pt-50To80_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 40377957)
qcdpt80mupt5_2017.add_dataset('miniaod', '/QCD_Pt-80To120_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 45981017)
qcdpt120mupt5_2017.add_dataset('miniaod', '/QCD_Pt-120To170_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 39394151)
qcdpt170mupt5_2017.add_dataset('miniaod', '/QCD_Pt-170To300_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 73071987)
qcdpt300mupt5_2017.add_dataset('miniaod', '/QCD_Pt-300To470_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 58692910)
qcdpt470mupt5_2017.add_dataset('miniaod', '/QCD_Pt-470To600_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 39491752)
qcdpt600mupt5_2017.add_dataset('miniaod', '/QCD_Pt-600To800_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 39321940)
qcdpt800mupt5_2017.add_dataset('miniaod', '/QCD_Pt-800To1000_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 78215559)
qcdpt1000mupt5_2017.add_dataset('miniaod', '/QCD_Pt-1000_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 27478273)
qcdempt015_2017.add_dataset('miniaod', '/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 7908107)
qcdempt020_2017.add_dataset('miniaod', '/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 14146285)
qcdempt030_2017.add_dataset('miniaod', '/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 8784542)
qcdempt050_2017.add_dataset('miniaod', '/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 10590542)
qcdempt080_2017.add_dataset('miniaod', '/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 9615719)
qcdempt120_2017.add_dataset('miniaod', '/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 9892235)
qcdempt170_2017.add_dataset('miniaod', '/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 3681297)
qcdempt300_2017.add_dataset('miniaod', '/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 2214934)
#qcdbctoept020_2017.add_dataset('miniaod', '/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2/MINIAODSIM', 14156589) Alec commented from here
#qcdbctoept030_2017.add_dataset('miniaod', '/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2/MINIAODSIM', 15153568)
#qcdbctoept080_2017.add_dataset('miniaod', '/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2/MINIAODSIM', 15908608)
#qcdbctoept170_2017.add_dataset('miniaod', '/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2/MINIAODSIM', 15588245)
#qcdbctoept250_2017.add_dataset('miniaod', '/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v3/MINIAODSIM', 15557421) Alec to here
qcdbctoept020_2017.add_dataset('miniaod', '/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 14156589) #Alec added from here
qcdbctoept030_2017.add_dataset('miniaod', '/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 15153568)
qcdbctoept080_2017.add_dataset('miniaod', '/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 15908608)
qcdbctoept170_2017.add_dataset('miniaod', '/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 15588245)
qcdbctoept250_2017.add_dataset('miniaod', '/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v3/MINIAODSIM', 15557421) #Alec to here

ttbar_2017.add_dataset('miniaod', '/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 249133364) #FIXME ? new MiniAOD
#ttbarht0600_2017.add_dataset('miniaod', '/TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',    81507662)
#ttbarht0800_2017.add_dataset('miniaod', '/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',   40191637)
#ttbarht1200_2017.add_dataset('miniaod', '/TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',  13214871)
#ttbarht2500_2017.add_dataset('miniaod', '/TTJets_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v3/MINIAODSIM',    5155687)

wjetstolnu_0j_2017.add_dataset('miniaod', '/WJetsToLNu_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM', 169421340)
wjetstolnu_1j_2017.add_dataset('miniaod', '/WJetsToLNu_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 180015088)
wjetstolnu_2j_2017.add_dataset('miniaod', '/WJetsToLNu_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM', 96032711)
dyjetstollM10_2017.add_dataset('miniaod', '/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM', 68480179)
dyjetstollM50_2017.add_dataset('miniaod', '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 103344974)

#dyjetstollM50ext_2017.add_dataset('miniaod', '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017RECOSIMstep_12Apr2018_94X_mc2017_realistic_v14_ext1-v1/MINIAODSIM', 49125561)

zjetstonunuht0100_2017.add_dataset('miniaod', '/ZJetsToNuNu_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v1/MINIAODSIM', 19040741)
zjetstonunuht0200_2017.add_dataset('miniaod', '/ZJetsToNuNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v1/MINIAODSIM', 16547983)
zjetstonunuht0400_2017.add_dataset('miniaod', '/ZJetsToNuNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v1/MINIAODSIM', 13948916)
zjetstonunuht0600_2017.add_dataset('miniaod', '/ZJetsToNuNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v1/MINIAODSIM', 4403555)
zjetstonunuht0800_2017.add_dataset('miniaod', '/ZJetsToNuNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v1/MINIAODSIM', 1446755)
zjetstonunuht1200_2017.add_dataset('miniaod', '/ZJetsToNuNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v1/MINIAODSIM', 267125)
zjetstonunuht2500_2017.add_dataset('miniaod', '/ZJetsToNuNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v1/MINIAODSIM', 172487)

SingleMuon2017B.add_dataset('miniaod', '/SingleMuon/Run2017B-UL2017_MiniAODv2_GT36-v2/MINIAOD', 136294038) #Alec added from here
SingleMuon2017C.add_dataset('miniaod', '/SingleMuon/Run2017C-UL2017_MiniAODv2_GT36-v2/MINIAOD', 167202975)
SingleMuon2017D.add_dataset('miniaod', '/SingleMuon/Run2017D-UL2017_MiniAODv2_GT36-v2/MINIAOD', 70354014)
SingleMuon2017E.add_dataset('miniaod', '/SingleMuon/Run2017E-UL2017_MiniAODv2_GT36-v2/MINIAOD', 154607963)
SingleMuon2017F.add_dataset('miniaod', '/SingleMuon/Run2017F-UL2017_MiniAODv2_GT36-v2/MINIAOD', 242140980)
SingleElectron2017B.add_dataset('miniaod', '/SingleElectron/Run2017B-UL2017_MiniAODv2-v1/MINIAOD', 60537490)
SingleElectron2017C.add_dataset('miniaod', '/SingleElectron/Run2017C-UL2017_MiniAODv2-v1/MINIAOD', 136637888)
SingleElectron2017D.add_dataset('miniaod', '/SingleElectron/Run2017D-UL2017_MiniAODv2-v1/MINIAOD', 51526521)
SingleElectron2017E.add_dataset('miniaod', '/SingleElectron/Run2017E-UL2017_MiniAODv2-v1/MINIAOD', 102122055)
SingleElectron2017F.add_dataset('miniaod', '/SingleElectron/Run2017F-UL2017_MiniAODv2-v1/MINIAOD', 128467223) #Alec to here

#ww_2017.add_dataset('miniaod', '/WW_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2/MINIAODSIM', 15883000) Alec commented
#wz_2017.add_dataset('miniaod', '/WZ_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2/MINIAODSIM', 2708000) Alec commented 
#zz_2017.add_dataset('miniaod', '/ZZ_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2/MINIAODSIM', 7898000) Alec commented 
ww_2017.add_dataset('miniaod', '/WW_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM', 15883000) #Alec added
wz_2017.add_dataset('miniaod', '/ZZ_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM', 2708000) #Alec added
zz_2017.add_dataset('miniaod', '/WZ_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM', 7898000) #Alec added

# the 2018 samples have 'MLM' in them so this works still, ugh
qcdht0200_2018.add_dataset('miniaod', '/QCD_HT200to300_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v2/MINIAODSIM', 22826901)
qcdht0200ext_2018.add_dataset('miniaod', '/QCD_HT200to300_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1_ext1-v1/MINIAODSIM', 34740016)
qcdht0300_2018.add_dataset('miniaod', ' /QCD_HT300to500_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v2/MINIAODSIM',   55135074)
qcdht0500_2018.add_dataset('miniaod', '/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v2/MINIAODSIM',   58487165)
qcdht0700_2018.add_dataset('miniaod', '/QCD_HT700to1000_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v2/MINIAODSIM',  47703400)
qcdht1000_2018.add_dataset('miniaod', '/QCD_HT1000to1500_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v2/MINIAODSIM', 15675643)
qcdht1500_2018.add_dataset('miniaod', '/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v2/MINIAODSIM', 10612885)
qcdht2000_2018.add_dataset('miniaod', '/QCD_HT2000toInf_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v2/MINIAODSIM',   4504262)
#wjetstolnu_0j_2018.add_dataset('miniaod', '/WJetsToLNu_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM',      172138190)
#wjetstolnu_1j_2018.add_dataset('miniaod', '/WJetsToLNu_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM',      184564696)
#wjetstolnu_2j_2018.add_dataset('miniaod', '/WJetsToLNu_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM',      94925903)
# wjetstolnu_2018.add_dataset('miniaod', '/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v1/MINIAODSIM', 83009353)
# dyjetstollM10_2018.add_dataset('miniaod', '/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v2/MINIAODSIM', 99515235)
# dyjetstollM50_2018.add_dataset('miniaod', '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v1/MINIAODSIM', 98433266)
# ttbar_2018.add_dataset('miniaod', '/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v1/MINIAODSIM', 340531078)
zjetstonunuht0100_2018.add_dataset('miniaod', '/ZJetsToNuNu_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v1/MINIAODSIM', 29021808)
zjetstonunuht0200_2018.add_dataset('miniaod', '/ZJetsToNuNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v1/MINIAODSIM', 23490705)
zjetstonunuht0400_2018.add_dataset('miniaod', '/ZJetsToNuNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v1/MINIAODSIM', 20667047)
zjetstonunuht0600_2018.add_dataset('miniaod', '/ZJetsToNuNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v1/MINIAODSIM', 5959670)
zjetstonunuht0800_2018.add_dataset('miniaod', '/ZJetsToNuNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v1/MINIAODSIM', 2144959)
zjetstonunuht1200_2018.add_dataset('miniaod', '/ZJetsToNuNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v1/MINIAODSIM', 375241)
zjetstonunuht2500_2018.add_dataset('miniaod', '/ZJetsToNuNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v1/MINIAODSIM', 268224)
#ttbarht0600_2018.add_dataset('miniaod', '/TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM',  14149394)
#ttbarht0800_2018.add_dataset('miniaod', '/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 10372802)
#ttbarht1200_2018.add_dataset('miniaod', '/TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 2779427)
#ttbarht2500_2018.add_dataset('miniaod', '/TTJets_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM',  1451104)

for sample in qcd_lep_samples_2018 + leptonic_samples_2018 + diboson_samples_2018 + met_samples_2018 + ttbar_samples_2018: 
    sample.add_dataset('miniaod', sample.dataset)
    
# ww_2018.add_dataset('miniaod', '/WW_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v2/MINIAODSIM', 15670000)
# wz_2018.add_dataset('miniaod', '/ZZ_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v2/MINIAODSIM', 3907000)
# zz_2018.add_dataset('miniaod', '/WZ_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v2/MINIAODSIM', 7986000)

mfv_splitSUSY_tau000010000um_M1200_1100_2017.add_dataset('miniaod', '/splitSUSY_M1200_1100_ctau10p0_TuneCP2_13TeV_pythia8/lian-RunIISummer20UL17_MiniAOD-e67f9b5d033cede4d000433a2a96d4fb/USER', 10000)
mfv_splitSUSY_tau000001000um_M1200_1100_2017.add_dataset('miniaod', '/splitSUSY_M1200_1100_ctau1p0_TuneCP2_13TeV_pythia8/lian-RunIISummer20UL17_MiniAOD-e67f9b5d033cede4d000433a2a96d4fb/USER', 10000)
mfv_splitSUSY_tau000010000um_M1400_1200_2017.add_dataset('miniaod', '/splitSUSY_M1400_1200_ctau10p0_TuneCP2_13TeV_pythia8/lian-RunIISummer20UL17_MiniAOD-e67f9b5d033cede4d000433a2a96d4fb/USER', 10000)
mfv_splitSUSY_tau000001000um_M1400_1200_2017.add_dataset('miniaod', '/splitSUSY_M1400_1200_ctau1p0_TuneCP2_13TeV_pythia8/lian-RunIISummer20UL17_MiniAOD-e67f9b5d033cede4d000433a2a96d4fb/USER', 10000)
mfv_splitSUSY_tau000000100um_M2000_1800_2017.add_dataset('miniaod', '/splitSUSY_M2000_1800_ctau0p1_TuneCP2_13TeV_pythia8/lian-RunIISummer20UL17_MiniAOD-e67f9b5d033cede4d000433a2a96d4fb/USER', 10000)
mfv_splitSUSY_tau000000300um_M2000_1800_2017.add_dataset('miniaod', '/splitSUSY_M2000_1800_ctau0p3_TuneCP2_13TeV_pythia8/lian-RunIISummer20UL17_MiniAOD-e67f9b5d033cede4d000433a2a96d4fb/USER', 10000)
mfv_splitSUSY_tau000010000um_M2000_1800_2017.add_dataset('miniaod', '/splitSUSY_M2000_1800_ctau10p0_TuneCP2_13TeV_pythia8/lian-RunIISummer20UL17_MiniAOD-e67f9b5d033cede4d000433a2a96d4fb/USER', 10000)
mfv_splitSUSY_tau000001000um_M2000_1800_2017.add_dataset('miniaod', '/splitSUSY_M2000_1800_ctau1p0_TuneCP2_13TeV_pythia8/lian-RunIISummer20UL17_MiniAOD-e67f9b5d033cede4d000433a2a96d4fb/USER', 10000)
mfv_splitSUSY_tau000000100um_M2000_1900_2017.add_dataset('miniaod', '/splitSUSY_M2000_1900_ctau0p1_TuneCP2_13TeV_pythia8/lian-RunIISummer20UL17_MiniAOD-e67f9b5d033cede4d000433a2a96d4fb/USER', 10000)
mfv_splitSUSY_tau000000300um_M2000_1900_2017.add_dataset('miniaod', '/splitSUSY_M2000_1900_ctau0p3_TuneCP2_13TeV_pythia8/lian-RunIISummer20UL17_MiniAOD-e67f9b5d033cede4d000433a2a96d4fb/USER', 10000)
mfv_splitSUSY_tau000010000um_M2000_1900_2017.add_dataset('miniaod', '/splitSUSY_M2000_1900_ctau10p0_TuneCP2_13TeV_pythia8/lian-RunIISummer20UL17_MiniAOD-e67f9b5d033cede4d000433a2a96d4fb/USER', 10000)
mfv_splitSUSY_tau000001000um_M2000_1900_2017.add_dataset('miniaod', '/splitSUSY_M2000_1900_ctau1p0_TuneCP2_13TeV_pythia8/lian-RunIISummer20UL17_MiniAOD-e67f9b5d033cede4d000433a2a96d4fb/USER', 10000)
mfv_splitSUSY_tau000000100um_M2400_100_2017.add_dataset('miniaod', '/splitSUSY_M2400_100_ctau0p1_TuneCP2_13TeV_pythia8/lian-RunIISummer20UL17_MiniAOD-e67f9b5d033cede4d000433a2a96d4fb/USER', 10000)
mfv_splitSUSY_tau000000300um_M2400_100_2017.add_dataset('miniaod', '/splitSUSY_M2400_100_ctau0p3_TuneCP2_13TeV_pythia8/lian-RunIISummer20UL17_MiniAOD-e67f9b5d033cede4d000433a2a96d4fb/USER', 10000)
mfv_splitSUSY_tau000010000um_M2400_100_2017.add_dataset('miniaod', '/splitSUSY_M2400_100_ctau10p0_TuneCP2_13TeV_pythia8/lian-RunIISummer20UL17_MiniAOD-e67f9b5d033cede4d000433a2a96d4fb/USER', 10000)
mfv_splitSUSY_tau000001000um_M2400_100_2017.add_dataset('miniaod', '/splitSUSY_M2400_100_ctau1p0_TuneCP2_13TeV_pythia8/lian-RunIISummer20UL17_MiniAOD-e67f9b5d033cede4d000433a2a96d4fb/USER', 10000)
mfv_splitSUSY_tau000000100um_M2400_2300_2017.add_dataset('miniaod', '/splitSUSY_M2400_2300_ctau0p1_TuneCP2_13TeV_pythia8/lian-RunIISummer20UL17_MiniAOD-e67f9b5d033cede4d000433a2a96d4fb/USER', 10000)
mfv_splitSUSY_tau000000300um_M2400_2300_2017.add_dataset('miniaod', '/splitSUSY_M2400_2300_ctau0p3_TuneCP2_13TeV_pythia8/lian-RunIISummer20UL17_MiniAOD-e67f9b5d033cede4d000433a2a96d4fb/USER', 10000)
mfv_splitSUSY_tau000010000um_M2400_2300_2017.add_dataset('miniaod', '/splitSUSY_M2400_2300_ctau10p0_TuneCP2_13TeV_pythia8/lian-RunIISummer20UL17_MiniAOD-e67f9b5d033cede4d000433a2a96d4fb/USER', 10000)
mfv_splitSUSY_tau000001000um_M2400_2300_2017.add_dataset('miniaod', '/splitSUSY_M2400_2300_ctau1p0_TuneCP2_13TeV_pythia8/lian-RunIISummer20UL17_MiniAOD-e67f9b5d033cede4d000433a2a96d4fb/USER', 10000)
mfv_neu_tau000300um_M0300_2017.add_dataset('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-300um_TuneCP5_13TeV-pythia8/shogan-RunIISummer20UL17_MiniAOD-e67f9b5d033cede4d000433a2a96d4fb/USER', 6400)
mfv_neu_tau000300um_M0600_2017.add_dataset('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-300um_TuneCP5_13TeV-pythia8/shogan-RunIISummer20UL17_MiniAOD-e67f9b5d033cede4d000433a2a96d4fb/USER', 6400)
mfv_neu_tau000300um_M0800_2017.add_dataset('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-300um_TuneCP5_13TeV-pythia8/shogan-RunIISummer20UL17_MiniAOD-e67f9b5d033cede4d000433a2a96d4fb/USER', 3200)
mfv_neu_tau001000um_M0300_2017.add_dataset('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-1mm_TuneCP5_13TeV-pythia8/shogan-RunIISummer20UL17_MiniAOD-e67f9b5d033cede4d000433a2a96d4fb/USER', 8000)
mfv_neu_tau001000um_M0600_2017.add_dataset('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-1mm_TuneCP5_13TeV-pythia8/shogan-RunIISummer20UL17_MiniAOD-e67f9b5d033cede4d000433a2a96d4fb/USER', 3200)
mfv_neu_tau001000um_M0800_2017.add_dataset('miniaod', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-1mm_TuneCP5_13TeV-pythia8/shogan-RunIISummer20UL17_MiniAOD-e67f9b5d033cede4d000433a2a96d4fb/USER', 4800)
mfv_stopdbardbar_tau000300um_M0300_2017.add_dataset('miniaod', '/StopStopbarTo2Dbar2D_M-300_CTau-300um_TuneCP5_13TeV-pythia8/shogan-RunIISummer20UL17_MiniAOD-e67f9b5d033cede4d000433a2a96d4fb/USER', 8000)
mfv_stopdbardbar_tau000300um_M0600_2017.add_dataset('miniaod', '/StopStopbarTo2Dbar2D_M-600_CTau-300um_TuneCP5_13TeV-pythia8/shogan-RunIISummer20UL17_MiniAOD-e67f9b5d033cede4d000433a2a96d4fb/USER', 4800)
mfv_stopdbardbar_tau000300um_M0800_2017.add_dataset('miniaod', '/StopStopbarTo2Dbar2D_M-800_CTau-300um_TuneCP5_13TeV-pythia8/shogan-RunIISummer20UL17_MiniAOD-e67f9b5d033cede4d000433a2a96d4fb/USER', 4800)
mfv_stopdbardbar_tau001000um_M0300_2017.add_dataset('miniaod', '/StopStopbarTo2Dbar2D_M-300_CTau-1mm_TuneCP5_13TeV-pythia8/shogan-RunIISummer20UL17_MiniAOD-e67f9b5d033cede4d000433a2a96d4fb/USER', 6400)
mfv_stopdbardbar_tau001000um_M0600_2017.add_dataset('miniaod', '/StopStopbarTo2Dbar2D_M-600_CTau-1mm_TuneCP5_13TeV-pythia8/shogan-RunIISummer20UL17_MiniAOD-e67f9b5d033cede4d000433a2a96d4fb/USER', 6400)
mfv_stopdbardbar_tau001000um_M0800_2017.add_dataset('miniaod', '/StopStopbarTo2Dbar2D_M-800_CTau-1mm_TuneCP5_13TeV-pythia8/shogan-RunIISummer20UL17_MiniAOD-e67f9b5d033cede4d000433a2a96d4fb/USER', 8000)
mfv_stopbbarbbar_tau000300um_M0300_2017.add_dataset('miniaod', '/StopStopbarTo2Bbar2B_M-300_CTau-300um_TuneCP5_13TeV-pythia8/shogan-RunIISummer20UL17_MiniAOD-e67f9b5d033cede4d000433a2a96d4fb/USER', 4800)
mfv_stopbbarbbar_tau000300um_M0600_2017.add_dataset('miniaod', '/StopStopbarTo2Bbar2B_M-600_CTau-300um_TuneCP5_13TeV-pythia8/shogan-RunIISummer20UL17_MiniAOD-e67f9b5d033cede4d000433a2a96d4fb/USER', 6400)
mfv_stopbbarbbar_tau000300um_M0800_2017.add_dataset('miniaod', '/StopStopbarTo2Bbar2B_M-800_CTau-300um_TuneCP5_13TeV-pythia8/shogan-RunIISummer20UL17_MiniAOD-e67f9b5d033cede4d000433a2a96d4fb/USER', 4800)
mfv_stopbbarbbar_tau001000um_M0300_2017.add_dataset('miniaod', '/StopStopbarTo2Bbar2B_M-300_CTau-1mm_TuneCP5_13TeV-pythia8/shogan-RunIISummer20UL17_MiniAOD-e67f9b5d033cede4d000433a2a96d4fb/USER', 8000)
mfv_stopbbarbbar_tau001000um_M0600_2017.add_dataset('miniaod', '/StopStopbarTo2Bbar2B_M-600_CTau-1mm_TuneCP5_13TeV-pythia8/shogan-RunIISummer20UL17_MiniAOD-e67f9b5d033cede4d000433a2a96d4fb/USER', 4800)
mfv_stopbbarbbar_tau001000um_M0800_2017.add_dataset('miniaod', '/StopStopbarTo2Bbar2B_M-800_CTau-1mm_TuneCP5_13TeV-pythia8/shogan-RunIISummer20UL17_MiniAOD-e67f9b5d033cede4d000433a2a96d4fb/USER', 6400)

for sample in ZHToSSTodddd_samples_20161 :
    sample.add_dataset('miniaod', sample.dataset, sample.nevents_orig)
for sample in WplusHToSSTodddd_samples_20161 :
    sample.add_dataset('miniaod', sample.dataset, sample.nevents_orig)
for sample in WminusHToSSTodddd_samples_20161 :
    sample.add_dataset('miniaod', sample.dataset, sample.nevents_orig)
for sample in ZHToSSTodddd_samples_20162 :
    sample.add_dataset('miniaod', sample.dataset, sample.nevents_orig)
for sample in WplusHToSSTodddd_samples_20162 :
    sample.add_dataset('miniaod', sample.dataset, sample.nevents_orig)
for sample in WminusHToSSTodddd_samples_20162 :
    sample.add_dataset('miniaod', sample.dataset, sample.nevents_orig)
for sample in HToSSTobbbb_samples_2017 :
    sample.add_dataset('miniaod', sample.dataset, sample.nevents_orig)
for sample in HToSSTodddd_samples_2017 :
    sample.add_dataset('miniaod', sample.dataset, sample.nevents_orig)
for sample in ZHToSSTodddd_samples_2017 :
    sample.add_dataset('miniaod', sample.dataset, sample.nevents_orig)
for sample in WplusHToSSTodddd_samples_2017 :
    sample.add_dataset('miniaod', sample.dataset, sample.nevents_orig)
for sample in WminusHToSSTodddd_samples_2017 :
    sample.add_dataset('miniaod', sample.dataset, sample.nevents_orig)
for sample in mfv_stoplb_samples_20161 :
    sample.add_dataset('miniaod', sample.dataset, sample.nevents_orig)
for sample in mfv_stopld_samples_20161 :
    sample.add_dataset('miniaod', sample.dataset, sample.nevents_orig)
for sample in mfv_stoplb_samples_20162 :
    sample.add_dataset('miniaod', sample.dataset, sample.nevents_orig)
for sample in mfv_stopld_samples_20162 :
    sample.add_dataset('miniaod', sample.dataset, sample.nevents_orig)
for sample in mfv_stoplb_samples_2017 :
    sample.add_dataset('miniaod', sample.dataset, sample.nevents_orig)
for sample in mfv_stopld_samples_2017 :
    sample.add_dataset('miniaod', sample.dataset, sample.nevents_orig)
for sample in mfv_stoplb_samples_2018 :
    sample.add_dataset('miniaod', sample.dataset, sample.nevents_orig)
for sample in mfv_stopld_samples_2018 :
    sample.add_dataset('miniaod', sample.dataset, sample.nevents_orig)
for sample in ZHToSSTodddd_samples_2018 :
    sample.add_dataset('miniaod', sample.dataset, sample.nevents_orig)
for sample in WplusHToSSTodddd_samples_2018 :
    sample.add_dataset('miniaod', sample.dataset, sample.nevents_orig)
for sample in WminusHToSSTodddd_samples_2018 :
    sample.add_dataset('miniaod', sample.dataset, sample.nevents_orig)
for s in all_signal_samples_20161: 
    _set_signal_stuff(s)
for s in all_signal_samples_20162:
    _set_signal_stuff(s)
for s in all_signal_samples_2017:
    _set_signal_stuff(s)
for s in all_signal_samples_2018:
    _set_signal_stuff(s)


########
# ntuples
########

for x in wjetstolnu_0j_20161, wjetstolnu_1j_20161, dyjetstollM10_20161, dyjetstollM50_20161, ww_20161, zz_20161, wz_20161, wjetstolnu_0j_20162, wjetstolnu_1j_20162, wjetstolnu_2j_20162, dyjetstollM10_20162, dyjetstollM50_20162, ww_20162, zz_20162, wz_20162, wjetstolnu_0j_2017, wjetstolnu_1j_2017, wjetstolnu_2j_2017, dyjetstollM10_2017, dyjetstollM50_2017, ww_2017, zz_2017, wz_2017, wjetstolnu_0j_2018, wjetstolnu_1j_2018, wjetstolnu_2j_2018, dyjetstollM10_2018, dyjetstollM50_2018, ww_2018, wz_2018, zz_2018, SingleMuon20161B1, SingleMuon20161B2, SingleMuon20161C, SingleMuon20161D, SingleMuon20161E, SingleMuon20161F, SingleMuon20162F, SingleMuon20162G, SingleMuon20162H, SingleMuon2017B, SingleMuon2017C, SingleMuon2017D, SingleMuon2017E, SingleMuon2017F, SingleMuon2018A, SingleMuon2018B, SingleMuon2018C, SingleMuon2018D:
    x.add_dataset("trackmoveronnormdzulv30lepmumv8")

WplusHToSSTodddd_tau1mm_M55_2017.add_dataset("trackmovermctruthonnormdzulv30lepmumv6")

for x in qcdmupt15_2017, qcdpt15mupt5_2017, qcdpt20mupt5_2017, qcdpt30mupt5_2017, qcdpt50mupt5_2017, qcdpt80mupt5_2017, qcdpt120mupt5_2017, qcdpt170mupt5_2017, qcdpt300mupt5_2017, qcdpt470mupt5_2017, qcdpt600mupt5_2017, qcdpt800mupt5_2017, qcdpt1000mupt5_2017, qcdempt015_2017, qcdempt020_2017, qcdempt030_2017, qcdempt050_2017, qcdempt080_2017, qcdempt120_2017, qcdempt170_2017, qcdempt300_2017, qcdbctoept020_2017, qcdbctoept030_2017, qcdbctoept080_2017, qcdbctoept170_2017, qcdbctoept250_2017, wjetstolnu_0j_2017, wjetstolnu_1j_2017, wjetstolnu_2j_2017, dyjetstollM10_2017, dyjetstollM50_2017, ttbar_2017, ww_2017, zz_2017, wz_2017, WplusHToSSTodddd_tau300um_M55_2017, WplusHToSSTodddd_tau1mm_M55_2017:
    x.add_dataset("ntupleonnorm3p5dzulv30lepmum")

#is this the correct ntuple version? 
#mfv_stopld_tau001000um_M1000_2018
#for x in mfv_stopld_tau000100um_M0200_2018, mfv_stopld_tau000300um_M0200_2018, mfv_stopld_tau000100um_M0600_2018, mfv_stopld_tau000300um_M0600_2018, mfv_stopld_tau000100um_M1000_2018, mfv_stopld_tau000300um_M1000_2018, mfv_stopld_tau000100um_M1600_2018, mfv_stopld_tau000300um_M1600_2018:

for x in ttbar_2017, wjetstolnu_0j_2017, wjetstolnu_1j_2017, wjetstolnu_2j_2017, dyjetstollM10_2017, dyjetstollM50_2017, ww_2017, zz_2017, wz_2017, SingleMuon2017B, SingleMuon2017C, SingleMuon2017D, SingleMuon2017E, SingleMuon2017F, SingleElectron2017B, SingleElectron2017C, SingleElectron2017D, SingleElectron2017E, SingleElectron2017F:
    x.add_dataset("mfvK0sNtuple2017_masswide_ULV30LepMumv1_isMCtrue_fixbjetsandmin_rLepMumv1")

for x in ttbar_2018, wjetstolnu_0j_2018, wjetstolnu_1j_2018, wjetstolnu_2j_2018, dyjetstollM10_2018, dyjetstollM50_2018, ww_2018, wz_2018, zz_2018:
    x.add_dataset("mfvK0sNtuple2018_masswide_ULV30LepMumv1_isMCtrue_fixbjetsandmin_rLepMumv1")

for x in ttbar_2018, wjetstolnu_0j_2018, wjetstolnu_1j_2018, wjetstolnu_2j_2018, dyjetstollM10_2018, dyjetstollM50_2018, ww_2018, wz_2018, zz_2018, SingleMuon2018A, SingleMuon2018B, SingleMuon2018C, SingleMuon2018D, EGamma2018A, EGamma2018B, EGamma2018C, EGamma2018D:
    x.add_dataset("mfvK0sNtuple2018_masswide_ULV30LepMumv1_fixbjetsandmin_rLepMumv1")

for x in ttbar_2018, wjetstolnu_0j_2018, wjetstolnu_1j_2018, wjetstolnu_2j_2018, dyjetstollM10_2018, dyjetstollM50_2018, ww_2018, wz_2018, zz_2018, SingleMuon2018A, SingleMuon2018B, SingleMuon2018C, SingleMuon2018D, EGamma2018A, EGamma2018B, EGamma2018C, EGamma2018D:
    x.add_dataset("mfvK0sNtuple2018_masswide_ULV30LepMumv1_fixmin_rLepMumv1")
                                                                                                             
SingleElectron2017B.add_dataset('ntuple_K0_DYmuontrig', '/FakeDataset/fakefile-FakePublish-8c7c2bda1cd22d80173e548f51d2f831/USER', -1)
SingleElectron2017C.add_dataset('ntuple_K0_DYmuontrig', '/FakeDataset/fakefile-FakePublish-e4d56933c86918c3bd148722113778ad/USER', -1)
SingleElectron2017E.add_dataset('ntuple_K0_DYmuontrig', '/FakeDataset/fakefile-FakePublish-b263ccec0b85cece65a88cc4bcb47b85/USER', -1)
SingleElectron2017F.add_dataset('ntuple_K0_DYmuontrig', '/FakeDataset/fakefile-FakePublish-618b1b5f1913656e40f0cfb572514b20/USER', -1)
for x in qcdmupt15_2017, qcdpt15mupt5_2017, qcdpt20mupt5_2017, qcdpt30mupt5_2017, qcdpt50mupt5_2017, qcdpt80mupt5_2017, qcdpt120mupt5_2017, qcdpt170mupt5_2017, qcdpt300mupt5_2017, qcdpt470mupt5_2017, qcdpt600mupt5_2017, qcdpt800mupt5_2017, qcdpt1000mupt5_2017, qcdempt015_2017, qcdempt020_2017, qcdempt030_2017, qcdempt050_2017, qcdempt080_2017, qcdempt120_2017, qcdempt170_2017, qcdempt300_2017, qcdbctoept020_2017, qcdbctoept030_2017, qcdbctoept080_2017, qcdbctoept170_2017, qcdbctoept250_2017, ttbar_2017, dyjetstollM10_2017, dyjetstollM50_2017, ww_2017, zz_2017, wz_2017, SingleMuon2017B, SingleMuon2017C, SingleMuon2017D, SingleMuon2017E, SingleMuon2017F, SingleElectron2017D:
    x.add_dataset("ntuple_K0_DYmuontrig")

ttbar_2018.add_dataset('ntuple2018_K0_DYmuontrig_masswide', '/FakeDataset/fakefile-FakePublish-01de2deb66994653f1489b8c96beff65/USER', -1)
wjetstolnu_0j_2018.add_dataset('ntuple2018_K0_DYmuontrig_masswide', '/FakeDataset/fakefile-FakePublish-b5dec11226cf690963517b9bc95b2a6a/USER', -1)
wjetstolnu_1j_2018.add_dataset('ntuple2018_K0_DYmuontrig_masswide', '/FakeDataset/fakefile-FakePublish-299041620b49ec195a3467f5c9489902/USER', -1)
wjetstolnu_2j_2018.add_dataset('ntuple2018_K0_DYmuontrig_masswide', '/FakeDataset/fakefile-FakePublish-c09aabf9dcd2f65100c8be50d8297258/USER', -1)
dyjetstollM10_2018.add_dataset('ntuple2018_K0_DYmuontrig_masswide', '/FakeDataset/fakefile-FakePublish-8615c2f1ebe454b9db502050cfa1a5f0/USER', -1)
dyjetstollM50_2018.add_dataset('ntuple2018_K0_DYmuontrig_masswide', '/FakeDataset/fakefile-FakePublish-18c7d6fcc0e115b3d58c09e9d2bc8d2c/USER', -1)
ww_2018.add_dataset('ntuple2018_K0_DYmuontrig_masswide', '/FakeDataset/fakefile-FakePublish-320b768fa55adaea054a8d1f1e297329/USER', -1)
wz_2018.add_dataset('ntuple2018_K0_DYmuontrig_masswide', '/FakeDataset/fakefile-FakePublish-73c99734c90a95b0d279204a7692e933/USER', -1)
zz_2018.add_dataset('ntuple2018_K0_DYmuontrig_masswide', '/FakeDataset/fakefile-FakePublish-94c33b0a028abecc0f53e4cdd32c5f1b/USER', -1)
SingleMuon2018A.add_dataset('ntuple2018_K0_DYmuontrig_masswide', '/FakeDataset/fakefile-FakePublish-ff1152844b6da49e054a4a480d0901c8/USER', -1)
SingleMuon2018B.add_dataset('ntuple2018_K0_DYmuontrig_masswide', '/FakeDataset/fakefile-FakePublish-b01df3e14db63816dc1cedf9ae1002be/USER', -1)
SingleMuon2018C.add_dataset('ntuple2018_K0_DYmuontrig_masswide', '/FakeDataset/fakefile-FakePublish-9668e0321c5a815fe071e5ccf84f5174/USER', -1)
SingleMuon2018D.add_dataset('ntuple2018_K0_DYmuontrig_masswide', '/FakeDataset/fakefile-FakePublish-00fb98a89ea42d2a4f94ccbb5c6bc3a1/USER', -1)
EGamma2018A.add_dataset('ntuple2018_K0_DYmuontrig_masswide', '/FakeDataset/fakefile-FakePublish-50a39c6931c8fb5b734b3571baeedbc6/USER', -1)
EGamma2018B.add_dataset('ntuple2018_K0_DYmuontrig_masswide', '/FakeDataset/fakefile-FakePublish-e827d0a970a1be68c6f01f5b70284951/USER', -1)
EGamma2018C.add_dataset('ntuple2018_K0_DYmuontrig_masswide', '/FakeDataset/fakefile-FakePublish-d6ea10da8b1f487607169ff57a07f983/USER', -1)
EGamma2018D.add_dataset('ntuple2018_K0_DYmuontrig_masswide', '/FakeDataset/fakefile-FakePublish-6e6c5a19c2c8d869e641c081723a6a70/USER', -1)
    
ttbar_2017.add_dataset('ntuple_K0_DYmuontrig_masswide', '/FakeDataset/fakefile-FakePublish-0b62fe2c2e68572d7b19020908d49d6d/USER', -1)
#wjetstolnu_amcatnlo_2017.add_dataset('ntuple_K0_DYmuontrig_masswide', '/FakeDataset/fakefile-FakePublish-60cc39a06694799dea9f2d0159f6f14f/USER', -1)
dyjetstollM10_2017.add_dataset('ntuple_K0_DYmuontrig_masswide', '/FakeDataset/fakefile-FakePublish-99411c72ade5979f99b481f27dd2ba8e/USER', -1)
dyjetstollM50_2017.add_dataset('ntuple_K0_DYmuontrig_masswide', '/FakeDataset/fakefile-FakePublish-a9976aaa8cda96912597725368bdee78/USER', -1)
ww_2017.add_dataset('ntuple_K0_DYmuontrig_masswide', '/FakeDataset/fakefile-FakePublish-6cd7d064e8348c4bfe63bac0035e610a/USER', -1)
zz_2017.add_dataset('ntuple_K0_DYmuontrig_masswide', '/FakeDataset/fakefile-FakePublish-b6cd6a80dc9138ea429a74c6b1c29c05/USER', -1)
wz_2017.add_dataset('ntuple_K0_DYmuontrig_masswide', '/FakeDataset/fakefile-FakePublish-99ffc914d00c091e9cddbc3ac2cd696a/USER', -1)
SingleMuon2017B.add_dataset('ntuple_K0_DYmuontrig_masswide', '/FakeDataset/fakefile-FakePublish-74ddfb1a658d0533a28148c11269a049/USER', -1)
SingleMuon2017C.add_dataset('ntuple_K0_DYmuontrig_masswide', '/FakeDataset/fakefile-FakePublish-64a61bd220abd9a9181478ca1c6ea276/USER', -1)
SingleMuon2017D.add_dataset('ntuple_K0_DYmuontrig_masswide', '/FakeDataset/fakefile-FakePublish-f9ea7deae9a0cc186751fff11ec12be4/USER', -1)
SingleMuon2017E.add_dataset('ntuple_K0_DYmuontrig_masswide', '/FakeDataset/fakefile-FakePublish-0bddb82dedbe9c6e67f0b6c20885d0f0/USER', -1)
SingleMuon2017F.add_dataset('ntuple_K0_DYmuontrig_masswide', '/FakeDataset/fakefile-FakePublish-6caa49f987d65320974610076f13f9f1/USER', -1)
SingleElectron2017B.add_dataset('ntuple_K0_DYmuontrig_masswide', '/FakeDataset/fakefile-FakePublish-fffd5d27db72a108c4bf9c34c49242f1/USER', -1)
SingleElectron2017C.add_dataset('ntuple_K0_DYmuontrig_masswide', '/FakeDataset/fakefile-FakePublish-9a4aa03a14030ee0b61bcd34f0ab13f1/USER', -1)
SingleElectron2017D.add_dataset('ntuple_K0_DYmuontrig_masswide', '/FakeDataset/fakefile-FakePublish-657210c092ccffd2f73f4b3ec4718cb7/USER', -1)
SingleElectron2017E.add_dataset('ntuple_K0_DYmuontrig_masswide', '/FakeDataset/fakefile-FakePublish-255956d95e24e484da66a0e321b65d10/USER', -1)
SingleElectron2017F.add_dataset('ntuple_K0_DYmuontrig_masswide', '/FakeDataset/fakefile-FakePublish-080e1718700dbe488f081d85bf920901/USER', -1)
    
#WplusHToSSTodddd_tau1mm_M55_2017.add_dataset('trackmovermctruthulv30lepmv9', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)

WplusHToSSTodddd_tau1mm_M55_2017.add_dataset('trackmovermctruthulv30lepmumv7', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
WplusHToSSTodddd_tau1mm_M15_2017.add_dataset('trackmovermctruthulv30lepmumv7', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)


SingleElectron2017B.add_dataset('trackmoverulv30lepelemv7', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
SingleElectron2017C.add_dataset('trackmoverulv30lepelemv7', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
SingleElectron2017E.add_dataset('trackmoverulv30lepelemv7', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
SingleElectron2017F.add_dataset('trackmoverulv30lepelemv7', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
for x in qcdmupt15_2017, qcdempt015_2017, qcdempt020_2017, qcdempt030_2017, qcdempt050_2017, qcdempt080_2017, qcdempt120_2017, qcdempt170_2017, qcdempt300_2017, qcdbctoept020_2017, qcdbctoept030_2017, qcdbctoept080_2017, qcdbctoept170_2017, qcdbctoept250_2017, dyjetstollM10_2017, dyjetstollM50_2017, ttbar_2017, ww_2017, zz_2017, wz_2017, SingleElectron2017D:                                                    # ^   wjetstolnu_2017,   Alec removed
    x.add_dataset("trackmoverulv30lepelemv7")

"""
# #for tracking tree : cut 0
# for x in ttbar_2017:
#     x.add_dataset("trackingtreerulv1_lepm_cut0")
for x in qcdempt015_2017, qcdmupt15_2017, qcdempt020_2017, qcdempt030_2017, qcdempt050_2017, qcdempt080_2017, qcdempt120_2017, qcdempt170_2017, qcdempt300_2017, qcdbctoept020_2017, qcdbctoept030_2017, qcdbctoept080_2017, qcdbctoept170_2017, qcdbctoept250_2017, dyjetstollM10_2017, dyjetstollM50_2017, ttbar_2017, ww_2017, zz_2017, wz_2017, SingleMuon2017B, SingleMuon2017C, SingleMuon2017D, SingleMuon2017E, SingleMuon2017F, SingleElectron2017B, SingleElectron2017C, SingleElectron2017D, SingleElectron2017E, SingleElectron2017F:
    x.add_dataset("trackingtreerulv1_lepm_cut0")

#For tracking tree : cut 0
# including info on leptons and lepton tracks

for x in dyjetstollM10_2017, dyjetstollM50_2017, SingleMuon2017B, SingleMuon2017C, SingleMuon2017D, SingleMuon2017E, SingleMuon2017F, SingleElectron2017B, SingleElectron2017C, SingleElectron2017D, SingleElectron2017E, SingleElectron2017F:
    x.add_dataset("trackingtreerulv1_lepm_wlep")

# #including info on leptons (including lepton sel tracks & good lepton sel tracks 
# for x in wjetstolnu_2017, dyjetstollM10_2017, dyjetstollM50_2017, SingleMuon2017B, SingleMuon2017C, SingleMuon2017D, SingleMuon2017E, SingleMuon2017F, SingleElectron2017B, SingleElectron2017C, SingleElectron2017D, SingleElectron2017E, SingleElectron2017F:
#     x.add_dataset("trackingtreerulv1_lepm_wsellep")

#we now have run over everything : good lepton sel tracks + tracks matched to a good lepton

for x in qcdempt015_2017, qcdmupt15_2017, qcdempt020_2017, qcdempt030_2017, qcdempt050_2017, qcdempt080_2017, qcdempt120_2017, qcdempt170_2017, qcdempt300_2017, qcdbctoept020_2017, qcdbctoept030_2017, qcdbctoept080_2017, qcdbctoept170_2017, qcdbctoept250_2017, dyjetstollM10_2017, dyjetstollM50_2017, ttbar_2017, ww_2017, zz_2017, wz_2017, SingleMuon2017B, SingleMuon2017C, SingleMuon2017D, SingleMuon2017E, SingleMuon2017F:
    x.add_dataset("trackingtreerulv1_lepm_wsellep")
"""

#for tracking tree : cut 1

for x in dyjetstollM10_2017, dyjetstollM50_2017:
    x.add_dataset("trackingtreerulv1_lepm_cut1")
    
#bakcground mc vs data (only single lepton triggers used) 
# qcdmupt15_2017.add_dataset('ntupleulv1lepm', '/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/awarden-NtupleULV1Lepm_2017-a0e559ed691b9ba065183ce34b4d6106/USER', 985)
# qcdempt020_2017.add_dataset('ntupleulv1lepm', '/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV1Lepm_2017-84408862823d6968fd890862da0d49b2/USER', 0)
# qcdempt030_2017.add_dataset('ntupleulv1lepm', '/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV1Lepm_2017-7db081dba1d39226de5de2eea02e41d3/USER', 1)
# qcdempt050_2017.add_dataset('ntupleulv1lepm', '/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV1Lepm_2017-5dc866fd0d951550e62c26721b796af2/USER', 2)
# qcdempt080_2017.add_dataset('ntupleulv1lepm', '/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV1Lepm_2017-fcc1efe099b4d9a07a1e00baab9762b4/USER', 16)
# qcdempt120_2017.add_dataset('ntupleulv1lepm', '/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV1Lepm_2017-2cea27cdaadd2421bc6a21e5693462f5/USER', 25)
# qcdempt170_2017.add_dataset('ntupleulv1lepm', '/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV1Lepm_2017-46a7c4774f49303236df584aebfd2749/USER', 19)
# qcdbctoept020_2017.add_dataset('ntupleulv1lepm', '/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV1Lepm_2017-9766de266b7ac90ce15868ee7c83b90a/USER', 3)
# qcdbctoept030_2017.add_dataset('ntupleulv1lepm', '/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV1Lepm_2017-ee19d520c8b663773bb3137a0a593d59/USER', 22)
# qcdbctoept080_2017.add_dataset('ntupleulv1lepm', '/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV1Lepm_2017-b258e3358ddb16518aebce917e89f6d0/USER', 127)
# qcdbctoept170_2017.add_dataset('ntupleulv1lepm', '/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV1Lepm_2017-45aa456833854841dc220e4781205803/USER', 254)
# qcdbctoept250_2017.add_dataset('ntupleulv1lepm', '/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV1Lepm_2017-19ea96c21beccbec48123f2a87f7da56/USER', 225)
# wjetstolnu_2017.add_dataset('ntupleulv1lepm', '/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/awarden-NtupleULV1Lepm_2017-2a9d14a75057a2560ebdc7a043162c80/USER', 15086)
# dyjetstollM10_2017.add_dataset('ntupleulv1lepm', '/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/awarden-NtupleULV1Lepm_2017-0258fd3aaebbe51ab595a2958eb34147/USER', 620)
# dyjetstollM50_2017.add_dataset('ntupleulv1lepm', '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/awarden-NtupleULV1Lepm_2017-541a5b29e0584826721d00f6a8f1f3ca/USER', 47108)
# ww_2017.add_dataset('ntupleulv1lepm', '/WW_TuneCP5_13TeV-pythia8/awarden-NtupleULV1Lepm_2017-4426673a03f6d0e98154aa4c197eca5d/USER', 5428)
# zz_2017.add_dataset('ntupleulv1lepm', '/WZ_TuneCP5_13TeV-pythia8/awarden-NtupleULV1Lepm_2017-836ba84ef310ba8aa80d049840b8ab52/USER', 4911)
# wz_2017.add_dataset('ntupleulv1lepm', '/ZZ_TuneCP5_13TeV-pythia8/awarden-NtupleULV1Lepm_2017-3e09513b56d2b31d08d63c947bfb8a7e/USER', 1800)
# SingleMuon2017C.add_dataset('ntupleulv1lepm', '/SingleMuon/awarden-NtupleULV1Lepm_2017-ee46985df5e00f16f85663aec6b35211/USER', 21458)
# SingleMuon2017E.add_dataset('ntupleulv1lepm', '/SingleMuon/awarden-NtupleULV1Lepm_2017-098e227518fc33335cef81109c342887/USER', 23991)
# SingleMuon2017F.add_dataset('ntupleulv1lepm', '/SingleMuon/awarden-NtupleULV1Lepm_2017-5ac1f06debba0541ff3bb1890f902adc/USER', 24597)
# SingleElectron2017C.add_dataset('ntupleulv1lepm', '/SingleElectron/awarden-NtupleULV1Lepm_2017-2ccfd2e730c1a6c2e84728d94a6ce605/USER', 8845)
# SingleElectron2017F.add_dataset('ntupleulv1lepm', '/SingleElectron/awarden-NtupleULV1Lepm_2017-d2f51bcb845d79fddcfab238bb3fc4d2/USER', 7572)
# for x in ttbar_2017, SingleMuon2017B, SingleMuon2017D, SingleElectron2017B, SingleElectron2017D, SingleElectron2017E:
#     x.add_dataset("ntupleulv1lepm")

#background mc vs signal (setup for both single and displaced dilepton triggers) 
#eventfilter used for background : min njets(leptons) = 2, ele/mu pt min 5 GeV => also have required all offline selection (minus pt) uncertain if this is good 
#also uncertain if it was a good idea to require two leptons now that I think about it... 
qcdempt015_2017.add_dataset('ntupleulv1lepm', '/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV1Lepm_2017-bc0c7352f55efbe738e3d4a1dcb8d840/USER', 0)
qcdmupt15_2017.add_dataset('ntupleulv1lepm', '/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/awarden-NtupleULV1Lepm_2017-a9df51e9aee3b5d7fef7efcc0999e971/USER', 73)
qcdempt020_2017.add_dataset('ntupleulv1lepm', '/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV1Lepm_2017-9d22178f36c446a301e53b2787b785b2/USER', 0)
qcdempt030_2017.add_dataset('ntupleulv1lepm', '/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV1Lepm_2017-a178ca314e2a8d25f80f7c5b95e39f14/USER', 0)
qcdempt050_2017.add_dataset('ntupleulv1lepm', '/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV1Lepm_2017-f22757d09fd5b02795235e44005765d7/USER', 0)
qcdempt080_2017.add_dataset('ntupleulv1lepm', '/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV1Lepm_2017-840d6d79c310d64427fa167f69f2aa3a/USER', 2)
qcdempt120_2017.add_dataset('ntupleulv1lepm', '/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV1Lepm_2017-94a583155eac2736d63885634a5c8d42/USER', 0)
qcdempt170_2017.add_dataset('ntupleulv1lepm', '/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV1Lepm_2017-c531f091adfd55c370b3b4c3ba52de2c/USER', 1)
qcdempt300_2017.add_dataset('ntupleulv1lepm', '/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV1Lepm_2017-1f714fabf363f897159cda41f173da6b/USER', 1)
qcdbctoept020_2017.add_dataset('ntupleulv1lepm', '/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV1Lepm_2017-58791afffac543748f01e993cd164637/USER', 0)
qcdbctoept030_2017.add_dataset('ntupleulv1lepm', '/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV1Lepm_2017-aa50353abbee571899237a2aedac3a9d/USER', 2)
qcdbctoept080_2017.add_dataset('ntupleulv1lepm', '/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV1Lepm_2017-f1aaccdbf7b26691391a41ebcfdcff26/USER', 7)
qcdbctoept170_2017.add_dataset('ntupleulv1lepm', '/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV1Lepm_2017-4ab0f32366d7f7e3cb9171131b21d0c1/USER', 18)
qcdbctoept250_2017.add_dataset('ntupleulv1lepm', '/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV1Lepm_2017-4d0c0035c1094e1fab4097c7eec38593/USER', 22)
dyjetstollM10_2017.add_dataset('ntupleulv1lepm', '/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/awarden-NtupleULV1Lepm_2017-36cbe68276a547570757ee92cb3d3cd9/USER', 251)
dyjetstollM50_2017.add_dataset('ntupleulv1lepm', '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/awarden-NtupleULV1Lepm_2017-947386ff5c048a7bc28a1b95a6542e0c/USER', 29868)
ww_2017.add_dataset('ntupleulv1lepm', '/WW_TuneCP5_13TeV-pythia8/awarden-NtupleULV1Lepm_2017-5f5b98a91a7a4345e74b7dafd0293c08/USER', 437)
zz_2017.add_dataset('ntupleulv1lepm', '/WZ_TuneCP5_13TeV-pythia8/awarden-NtupleULV1Lepm_2017-496f921dc1a4f8a1fe02d9af648e8200/USER', 498)
wz_2017.add_dataset('ntupleulv1lepm', '/ZZ_TuneCP5_13TeV-pythia8/awarden-NtupleULV1Lepm_2017-480e0d6118ccdb02c77fab10365b72c1/USER', 1085)
mfv_stoplb_tau000100um_M1000_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-bc68908fb594460711e61657110aa32b/USER', 194928)
mfv_stoplb_tau000300um_M1000_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-58ba196e7e68aa78bd6f0db3bf9894a2/USER', 200301)
mfv_stoplb_tau010000um_M1000_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-12e6b0f63350a836117febdcaea62981/USER', 98261)
mfv_stoplb_tau001000um_M1000_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-6707845d622b89ed22d6ee1306a4b405/USER', 197193)
mfv_stoplb_tau030000um_M1000_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-f11fd9ac0ead16a026a6f07d93fbcad8/USER', 200668)
mfv_stoplb_tau000100um_M1200_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-d8709c913023e8f420c93365477a1eea/USER', 199921)
mfv_stoplb_tau000300um_M1200_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-5689d8075a1a4ec2ac147aa931e29754/USER', 195189)
mfv_stoplb_tau010000um_M1200_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-4f2a5c7b2309cf28f13e7f8b8c70df56/USER', 100156)
mfv_stoplb_tau001000um_M1200_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-0a4732012850b03498157b14784788b9/USER', 197902)
mfv_stoplb_tau030000um_M1200_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-8e191de4f0eff7b06bfff3c8b556ee55/USER', 200464)
mfv_stoplb_tau000100um_M1400_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-7fa533813934cc9a81f166bea3c32263/USER', 199322)
mfv_stoplb_tau000300um_M1400_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-ba5e9eb7e685b2016276d6584b3e8148/USER', 200304)
mfv_stoplb_tau010000um_M1400_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-2b0d389d036bf346e5f508b31392034f/USER', 98900)
mfv_stoplb_tau001000um_M1400_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-d507ca3ede734bcc7a9e967d67024229/USER', 196297)
mfv_stoplb_tau030000um_M1400_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-86766444475c9a5a463b92c9f37c843e/USER', 198644)
mfv_stoplb_tau000100um_M1600_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-dfc2c40222d67054951e9ab3eb929e42/USER', 202021)
mfv_stoplb_tau000300um_M1600_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-be03acb877fcf5d4445669c066f5f5c4/USER', 199079)
mfv_stoplb_tau010000um_M1600_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-31abc59805c734d664d41205673355ff/USER', 98745)
mfv_stoplb_tau001000um_M1600_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-3a6679e1f1cbfdb19ce7f6cadd04c0e5/USER', 98921)
mfv_stoplb_tau030000um_M1600_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-68791ffd41ebfc7e2b0e5b61e549f150/USER', 100284)
mfv_stoplb_tau000100um_M1800_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-725bbc729a4f8be7d56dbce37c475a95/USER', 199639)
mfv_stoplb_tau000300um_M1800_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-47165f47ddc34eeaab6d519d3919470b/USER', 200792)
mfv_stoplb_tau010000um_M1800_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-6da3c05e966be8a1dcfbbf4739375138/USER', 101386)
mfv_stoplb_tau001000um_M1800_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-c227ffd51172aca322978aaf7c51af74/USER', 98858)
mfv_stoplb_tau030000um_M1800_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-1620b474144b6fbaa417d5ea5ac82e4e/USER', 100172)
mfv_stoplb_tau000100um_M0200_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-23107909e32a7eca3a4a40911b677f61/USER', 198760)
mfv_stoplb_tau000300um_M0200_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-7fe6567fd9d2f3823db83cff8be10381/USER', 198899)
mfv_stoplb_tau010000um_M0200_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-8f4c6d1d33b21bec705f4dc04d7b1781/USER', 199948)
mfv_stoplb_tau030000um_M0200_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-e0a593cc112838f77f9bf2e5a5c46b3a/USER', 199267)
mfv_stoplb_tau000100um_M0300_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-cf158f0a9312f2bfb1b6bb647ac08fba/USER', 198231)
mfv_stoplb_tau000300um_M0300_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-70aad128cd852ab533938c0d4e01cada/USER', 198170)
mfv_stoplb_tau010000um_M0300_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-f4799e4c525b5ec6ae9fb6543f4a226d/USER', 199832)
mfv_stoplb_tau030000um_M0300_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-6159b6d2c52814656cc62f61f4a16bfe/USER', 200170)
mfv_stoplb_tau000100um_M0400_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-5c6f740efff6863b26177522b4f32512/USER', 197597)
mfv_stoplb_tau000300um_M0400_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-30144e48c8a3b0b1519397f3142d30e2/USER', 200230)
mfv_stoplb_tau010000um_M0400_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-fffd42e1f7f9118e4f877f8c838e76b3/USER', 198737)
mfv_stoplb_tau030000um_M0400_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-a8c201bcddbbc10b5b1c03dbe2bc320e/USER', 198930)
mfv_stoplb_tau000100um_M0600_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-25eda93f3ae7508d116bb661e886ae9b/USER', 201812)
mfv_stoplb_tau000300um_M0600_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-12d54a72f7494c96957b84a6486f9a7a/USER', 201839)
mfv_stoplb_tau010000um_M0600_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-f199b4271f76e662df73f520a74b3e98/USER', 197409)
mfv_stoplb_tau030000um_M0600_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-1ea02d7376db95e4cce2c5afd8f48294/USER', 200005)
mfv_stoplb_tau000100um_M0800_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-d2d9467a5ce1df1438cebf6c46308a30/USER', 198566)
mfv_stoplb_tau000300um_M0800_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-f63c6dcac78c40df19fd02c8b68923f3/USER', 197615)
mfv_stoplb_tau010000um_M0800_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-9a5ec718047240d2186e07e7ee91d89c/USER', 98799)
mfv_stoplb_tau030000um_M0800_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-0b9907119d47b9016061b4eeb65072b8/USER', 201690)
mfv_stopld_tau000100um_M1000_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-20d50a1ec22d0c149706bae2c6d0e762/USER', 199076)
mfv_stopld_tau000300um_M1000_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-e818969e65e77d1eb01ddbbc1cc4378f/USER', 198992)
mfv_stopld_tau010000um_M1000_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-765427a7df0b86dc24613285d2507023/USER', 98679)
mfv_stopld_tau001000um_M1000_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-0941bde3884742c5e2ef082a223722de/USER', 198608)
mfv_stopld_tau030000um_M1000_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-426c08069b5cb0dc5c06f5515d1015db/USER', 199499)
mfv_stopld_tau000100um_M1200_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-1f59665289339c12705e9ee4aef6c7cb/USER', 198263)
mfv_stopld_tau000300um_M1200_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-f07aff5e5d36b835e2007795d1d568f6/USER', 195508)
mfv_stopld_tau010000um_M1200_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-65a0d2ba2601e5794b82a698d0ae8df6/USER', 100349)
mfv_stopld_tau001000um_M1200_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-cbb676f82187e34ffd043b24e6a3239c/USER', 201191)
mfv_stopld_tau030000um_M1200_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-758208308a5982381f8f5af59361ba0d/USER', 200851)
mfv_stopld_tau000100um_M1400_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-e39b27e926b6c2b4eb8eee7bc096f93e/USER', 198812)
mfv_stopld_tau000300um_M1400_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-a5aec2e8f0b195e1bd514bdd4a6784dc/USER', 193575)
mfv_stopld_tau010000um_M1400_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-b774aa53c72d77d73ed4575182caa6b9/USER', 98583)
mfv_stopld_tau001000um_M1400_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-c2021848d1503868f83f4942d908a32c/USER', 198538)
mfv_stopld_tau030000um_M1400_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-7dca09e1ee5fdfa2b8e15df026ce2bb5/USER', 199735)
mfv_stopld_tau000100um_M1600_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-0349211eaa5a3074bec311737578f601/USER', 200067)
mfv_stopld_tau000300um_M1600_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-efcbb5fb22d4c4fe82602cc052581bf6/USER', 196540)
mfv_stopld_tau010000um_M1600_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-ed66e2764c8fc48257cd88adc764fb03/USER', 100274)
mfv_stopld_tau001000um_M1600_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-fbff8906fda8f761b2a590f63f672bd7/USER', 99126)
mfv_stopld_tau030000um_M1600_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-707e1e99057e82d7d0eb16a8657824d4/USER', 99333)
mfv_stopld_tau000100um_M1800_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-0405f8942220c60ba0545da2f68db7fb/USER', 200828)
mfv_stopld_tau000300um_M1800_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-05f985017e61182cfb11a4001ec04e21/USER', 198147)
mfv_stopld_tau010000um_M1800_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-707c199a1ed8aab5440eef840173eca2/USER', 99667)
mfv_stopld_tau001000um_M1800_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-2b198b7217f8309a4abab255ebf4b06c/USER', 101005)
mfv_stopld_tau030000um_M1800_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-84273ffbc9e55a7d0b96dfaf3f710ca8/USER', 99787)
mfv_stopld_tau000100um_M0200_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-af622c497502c5e86336d99ce6a0c9a4/USER', 201843)
mfv_stopld_tau000300um_M0200_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-62c18fdc9f067fb9594bb231bf7256d9/USER', 199789)
mfv_stopld_tau010000um_M0200_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-02c58de911aaa88c7ae3e1ed0b54c816/USER', 197403)
mfv_stopld_tau030000um_M0200_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-d3f7648accb1a29202402f7454aaa639/USER', 198511)
mfv_stopld_tau000100um_M0300_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-314378fcddb9b5da4a490aa17c2f5fe0/USER', 195420)
mfv_stopld_tau000300um_M0300_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-7033381f222f238d6629a4db6d6ee640/USER', 195932)
mfv_stopld_tau010000um_M0300_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-acaa9f6b17c7adc3a0ded8f2748c1460/USER', 197990)
mfv_stopld_tau030000um_M0300_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-7cd0e7cd2d16b67546c45564e3667589/USER', 199931)
mfv_stopld_tau000100um_M0400_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-ccb7511faf0f9a5334cb3972feb641ba/USER', 202735)
mfv_stopld_tau000300um_M0400_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-fbb34a9d3865f41acbda6ebb892d034f/USER', 199890)
mfv_stopld_tau010000um_M0400_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-a85040158f87ba1e72da703da43605eb/USER', 201845)
mfv_stopld_tau030000um_M0400_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-8715dcaa4220c2e7bc14f28858041b93/USER', 198731)
mfv_stopld_tau000100um_M0600_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-4502efc7016d1e30bf50c4ab3dbcc8e6/USER', 203406)
mfv_stopld_tau000300um_M0600_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-e521277c2a52a7df74a4a3d66af4aa79/USER', 199321)
mfv_stopld_tau010000um_M0600_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-6392ee8e9ae0c792a66aa961bd1f26ae/USER', 195818)
mfv_stopld_tau030000um_M0600_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-77271f99cbe39081100ebbe26c9b3ce7/USER', 199944)
mfv_stopld_tau000100um_M0800_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-8421c0a080daf6730d5eba129e4e03d2/USER', 200077)
mfv_stopld_tau000300um_M0800_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-4a5b260041543f62eea95d0749ac8e18/USER', 200814)
mfv_stopld_tau010000um_M0800_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-e65ac315c3e655f1ada2aebe241af5e1/USER', 99313)
mfv_stopld_tau030000um_M0800_2017.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2017-1d21bce64cd13933963c2420b7770972/USER', 200140)
# for x in ttbar_2017:
#     x.add_dataset("ntupleulv1lepm")
ttbar_2017.add_dataset("ntupleulv1lepm")


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
# be careful about the list, some samples are distributed at different samples so it won't work
condorable = {
    "T2_DE_DESY": {
        "miniaod": [MET2017E, MET2018A, MET2018B, zjetstonunuht0100_2018, zjetstonunuht0200_2018, zjetstonunuht0400_2018, zjetstonunuht0600_2018, zjetstonunuht0800_2018, zjetstonunuht1200_2018], #EGamma2018D
        },
    "T3_US_FNALLPC": {
        "miniaod": mfv_splitSUSY_samples_2017 + mfv_signal_samples_2017 + mfv_stopdbardbar_samples_2017 + mfv_stopbbarbbar_samples_2017
        
        },
    "T1_US_FNAL_Disk": {
        #"miniaod": [MET2018D, qcdht0300_2018, qcdht0700_2018, qcdht1000_2018, qcdht1500_2018, zjetstonunuht2500_2018, qcdht0200_2017, qcdht0500_2017, qcdht0700_2017, qcdht0300_2017,ttbar_2017, ttbar_2018, SingleMuon2017B, SingleMuon2017C, SingleMuon2017D, SingleMuon2017E, SingleMuon2017F, SingleElectron2017D] + diboson_samples_2017 + leptonic_samples_2017 + qcd_lep_samples_2017 # SingleElectron2017B, SingleElectron2017D, SingleElectron2017E,
        #"miniaod": Lepton_data_samples_2017 + all_signal_samples_2017 + diboson_samples_2017 + ttbar_samples_2017 + leptonic_samples_2017
        "miniaod": Lepton_data_samples_20161 + all_signal_samples_20161 + diboson_samples_20161 + ttbar_samples_20161 + leptonic_samples_20161 + qcd_lep_samples_20161 + met_samples_20161 + Lepton_data_samples_20162 + all_signal_samples_20162 + diboson_samples_20162 + ttbar_samples_20162 + leptonic_samples_20162 + qcd_lep_samples_20162 + met_samples_20162 + Lepton_data_samples_2017 +  all_signal_samples_2017 + diboson_samples_2017 + ttbar_samples_2017 + leptonic_samples_2017 + qcd_lep_samples_2017 +  qcd_samples_2017 + Lepton_data_samples_2018 + all_signal_samples_2018 + diboson_samples_2018 + ttbar_samples_2018 + leptonic_samples_2018 + qcd_lep_samples_2018 + met_samples_2018
        
                    #mfv_stoplb_tau010000um_M1000_2017, mfv_stoplb_tau000300um_M1200_2017, mfv_stoplb_tau010000um_M1200_2017, mfv_stoplb_tau001000um_M1200_2017, mfv_stoplb_tau000300um_M1600_2017, mfv_stoplb_tau001000um_M1600_2017, mfv_stoplb_tau000100um_M0300_2017, mfv_stoplb_tau000300um_M0300_2017, mfv_stoplb_tau001000um_M0300_2017, mfv_stoplb_tau001000um_M0400_2017, mfv_stoplb_tau010000um_M0600_2017, mfv_stopld_tau000300um_M1000_2017, mfv_stopld_tau010000um_M1000_2017, mfv_stopld_tau010000um_M1200_2017, mfv_stopld_tau001000um_M1400_2017, mfv_stopld_tau000300um_M1600_2017, mfv_stopld_tau010000um_M0200_2017, mfv_stopld_tau000300um_M0300_2017, mfv_stopld_tau001000um_M0400_2017, mfv_stopld_tau000300um_M0600_2017, mfv_stopld_tau010000um_M0600_2017, mfv_stopld_tau001000um_M0600_2017, mfv_stopld_tau010000um_M0800_2017, mfv_stoplb_tau010000um_M1200_2018, mfv_stoplb_tau001000um_M1200_2018, mfv_stoplb_tau010000um_M1400_2018, mfv_stoplb_tau001000um_M1400_2018, mfv_stoplb_tau010000um_M1600_2018, mfv_stoplb_tau001000um_M1600_2018, mfv_stoplb_tau001000um_M0200_2018, mfv_stoplb_tau010000um_M0300_2018, mfv_stoplb_tau010000um_M0400_2018, mfv_stoplb_tau001000um_M0400_2018, mfv_stoplb_tau001000um_M0600_2018, mfv_stoplb_tau000300um_M0800_2018, mfv_stoplb_tau001000um_M0800_2018, mfv_stopld_tau000300um_M1000_2018, mfv_stopld_tau000300um_M1200_2018, mfv_stopld_tau000100um_M1400_2018, mfv_stopld_tau000100um_M1600_2018, mfv_stopld_tau010000um_M1600_2018, mfv_stopld_tau000300um_M0200_2018, mfv_stopld_tau001000um_M0200_2018, mfv_stopld_tau001000um_M0300_2018, mfv_stopld_tau000300um_M0400_2018, mfv_stopld_tau001000um_M0600_2018],
        },
    "T2_US_Wisconsin": {
       # "miniaod": mfv_stopld_samples_2018 + [mfv_stopld_tau010000um_M0400_2018],
       # "miniaod": [mfv_stopld_tau010000um_M0400_2018],
        },
    "T2_US_Purdue": {
       # "miniaod" : [SingleElectron2017C],
        },
    "T2_US_UCSD": {
       # "miniaod" : [mfv_stoplb_tau000300um_M1000_2017, mfv_stoplb_tau000100um_M1200_2017, mfv_stoplb_tau030000um_M1200_2017, mfv_stoplb_tau030000um_M1400_2017, mfv_stoplb_tau000300um_M1800_2017, mfv_stoplb_tau000100um_M0200_2017, mfv_stoplb_tau000300um_M0200_2017, mfv_stoplb_tau001000um_M0200_2017, mfv_stoplb_tau030000um_M0200_2017, mfv_stoplb_tau010000um_M0300_2017, mfv_stoplb_tau030000um_M0300_2017, mfv_stoplb_tau000100um_M0400_2017, mfv_stoplb_tau000300um_M0400_2017, mfv_stoplb_tau030000um_M0400_2017, mfv_stoplb_tau000100um_M0800_2017, mfv_stoplb_tau000300um_M0800_2017, mfv_stoplb_tau001000um_M0800_2017, mfv_stoplb_tau030000um_M0800_2017, mfv_stopld_tau030000um_M1000_2017, mfv_stopld_tau030000um_M1200_2017, mfv_stopld_tau000100um_M1400_2017, mfv_stopld_tau030000um_M1600_2017, mfv_stopld_tau000300um_M1800_2017, mfv_stopld_tau030000um_M1800_2017, mfv_stopld_tau001000um_M0200_2017, mfv_stopld_tau000100um_M0300_2017, mfv_stopld_tau030000um_M0300_2017, mfv_stopld_tau000100um_M0400_2017, mfv_stopld_tau000300um_M0400_2017, mfv_stopld_tau010000um_M0400_2017, mfv_stopld_tau030000um_M0400_2017, mfv_stopld_tau030000um_M0600_2017, mfv_stopld_tau001000um_M0800_2017, mfv_stopld_tau030000um_M0800_2017, mfv_stoplb_tau000100um_M1000_2018, mfv_stoplb_tau001000um_M1000_2018, mfv_stoplb_tau000100um_M1200_2018, mfv_stoplb_tau030000um_M1600_2018, mfv_stoplb_tau010000um_M1800_2018, mfv_stoplb_tau000300um_M0200_2018, mfv_stoplb_tau010000um_M0200_2018, mfv_stoplb_tau000300um_M0300_2018, mfv_stoplb_tau030000um_M0400_2018, mfv_stoplb_tau000300um_M0600_2018, mfv_stoplb_tau000100um_M0800_2018, mfv_stopld_tau000100um_M1200_2018, mfv_stopld_tau010000um_M1200_2018, mfv_stopld_tau030000um_M1200_2018, mfv_stopld_tau030000um_M1400_2018, mfv_stopld_tau010000um_M1800_2018, mfv_stopld_tau001000um_M1800_2018, mfv_stopld_tau000100um_M0200_2018, mfv_stopld_tau010000um_M0200_2018, mfv_stopld_tau000100um_M0300_2018, mfv_stopld_tau001000um_M0400_2018, mfv_stopld_tau001000um_M0800_2018, mfv_stopld_tau030000um_M0800_2018],
        },
    # "T2_US_Caltech": {
    #     "miniaod" : [mfv_stoplb_tau001000um_M1000_2017, mfv_stoplb_tau030000um_M1000_2017, mfv_stoplb_tau010000um_M0400_2017, mfv_stoplb_tau030000um_M0600_2017, mfv_stoplb_tau010000um_M0800_2017, mfv_stopld_tau030000um_M1400_2017, mfv_stopld_tau001000um_M1600_2017, mfv_stopld_tau000100um_M1800_2017, mfv_stopld_tau030000um_M0200_2017, mfv_stopld_tau000100um_M0600_2017, mfv_stopld_tau000100um_M0800_2017, mfv_stopld_tau001000um_M1000_2018, mfv_stopld_tau001000um_M1600_2018, mfv_stopld_tau000100um_M1800_2018, mfv_stopld_tau030000um_M0200_2018, mfv_stopld_tau030000um_M0300_2018, mfv_stopld_tau000100um_M0600_2018],
    #     },
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
for s in mfv_splitSUSY_samples_2017:
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
    #for s in qcdht0700_2017, dyjetstollM10_2017, dyjetstollM50_2017, dyjetstollM50ext_2017:
    #    s.datasets[ds].notes['buggedpileup2017'] = True

    # set up jsons
    #for y,ss in (2017, data_samples_2017 + auxiliary_data_samples_2017 + singleelectron_data_samples_2017), (2018, data_samples_2018 + auxiliary_data_samples_2018 + egamma_data_samples_2018):
    for y,ss in (20161, Lepton_data_samples_20161), (2017, data_samples_2017 + Lepton_data_samples_2017), (2018, data_samples_2018 + auxiliary_data_samples_2018 + egamma_data_samples_2018 + Lepton_data_samples_2018):
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
