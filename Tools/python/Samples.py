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
    MCSample('wjetstolnu_20161',       '/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM',          74676454, nice='W + jets #rightarrow l#nu',                 color=  9, syst_frac=0.10, xsec=5.294e4),
    MCSample('dyjetstollM10_20161',    '/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM', 25799525, nice='DY + jets #rightarrow ll, 10 < M < 50 GeV', color= 29, syst_frac=0.10, xsec=1.58e4),
    MCSample('dyjetstollM50_20161',    '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM',     95170542, nice='DY + jets #rightarrow ll, M > 50 GeV',      color= 32, syst_frac=0.10, xsec=5.34e3),
]

met_samples_20161 = [
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

all_signal_samples_20161 = mfv_stoplb_samples_20161 + mfv_stopld_samples_20161

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
    MCSample('wjetstolnu_20162',       '/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM',          82754918, nice='W + jets #rightarrow l#nu',                 color=  9, syst_frac=0.10, xsec=5.294e4),
    MCSample('dyjetstollM10_20162',    '/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM', 23706672, nice='DY + jets #rightarrow ll, 10 < M < 50 GeV', color= 29, syst_frac=0.10, xsec=1.58e4),
    MCSample('dyjetstollM50_20162',    '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM',     82448537, nice='DY + jets #rightarrow ll, M > 50 GeV',      color= 32, syst_frac=0.10, xsec=5.34e3),
]

met_samples_20162 = [
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

all_signal_samples_20162 = mfv_stoplb_samples_20162 + mfv_stopld_samples_20162 

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
    MCSample('qcdempt015_2017', '/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM',   7966910, nice='QCD,  15 < #hat{p}_{T} <  20 GeV, EM enriched', color=801, syst_frac=0.20, xsec=1.324e6),
    MCSample('qcdmupt15_2017',  '/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM',  17716270, nice='QCD, #hat{p}_{T} > 20 GeV, #mu p_{T} > 15 GeV', color=801, syst_frac=0.20, xsec=2.39e5),
    MCSample('qcdempt020_2017', '/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM',   14166147, nice='QCD,  20 < #hat{p}_{T} <  30 GeV, EM enriched', color=801, syst_frac=0.20, xsec=4.896e6),
    MCSample('qcdempt030_2017', '/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM',   8784542, nice='QCD,  30 < #hat{p}_{T} <  50 GeV, EM enriched', color=801, syst_frac=0.20, xsec=6.447e6),
    MCSample('qcdempt050_2017', '/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM',   10590542, nice='QCD,  50 < #hat{p}_{T} <  80 GeV, EM enriched', color=801, syst_frac=0.20, xsec=1.988e6),
    MCSample('qcdempt080_2017', '/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM',   9615795, nice='QCD,  80 < #hat{p}_{T} < 120 GeV, EM enriched', color=801, syst_frac=0.20, xsec=3.675e5),
    MCSample('qcdempt120_2017', '/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM',  9904245, nice='QCD, 120 < #hat{p}_{T} < 170 GeV, EM enriched', color=801, syst_frac=0.20, xsec=6.659e4),
    MCSample('qcdempt170_2017', '/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM',  3678200, nice='QCD, 170 < #hat{p}_{T} < 300 GeV, EM enriched', color=801, syst_frac=0.20, xsec=1.662e4),
    MCSample('qcdempt300_2017', '/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM',  2214934, nice='QCD, #hat{p}_{T} > 300 GeV, EM enriched',       color=801, syst_frac=0.20, xsec=1104.0),
    MCSample('qcdbctoept015_2017', '/QCD_Pt_15to20_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM',      18671506, nice='QCD,  15 < #hat{p}_{T} <  20 GeV, HF electrons', color=801, syst_frac=0.20, xsec=1.862e5),
    MCSample('qcdbctoept020_2017', '/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM',      14171260, nice='QCD,  20 < #hat{p}_{T} <  30 GeV, HF electrons', color=801, syst_frac=0.20, xsec=3.038e5),
    MCSample('qcdbctoept030_2017', '/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM',      15238384, nice='QCD,  30 < #hat{p}_{T} <  80 GeV, HF electrons', color=801, syst_frac=0.20, xsec=3.623e5),
    MCSample('qcdbctoept080_2017', '/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM',     15571255, nice='QCD,  80 < #hat{p}_{T} < 170 GeV, HF electrons', color=801, syst_frac=0.20, xsec=3.37e4),
    MCSample('qcdbctoept170_2017', '/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM',    15502839, nice='QCD, 170 < #hat{p}_{T} < 250 GeV, HF electrons', color=801, syst_frac=0.20, xsec=2.125e3),
    MCSample('qcdbctoept250_2017', '/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v3/MINIAODSIM',    15557421, nice='QCD, #hat{p}_{T} > 250 GeV, HF electrons',       color=801, syst_frac=0.20, xsec=562.5),
    ]
    
# ttbar with HT slices not available for UL now
ttbar_samples_2017 = [
]
bjet_samples_2017 = [
    ]

leptonic_samples_2017 = [
    MCSample('wjetstolnu_2017',       '/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v1/AODSIM', 81551529, nice='W + jets #rightarrow l#nu', color=  9, syst_frac=0.10, xsec=5.294e4),
    MCSample('wjetstolnu_amcatnlo_2017','/WJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 26838734, nice='NLO W + jets #rightarrow l#nu', color= 38, syst_fac=0.10, xsec=6.735e4),
    MCSample('dyjetstollM10_2017',    '/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v2/AODSIM',                  70516252, nice='DY + jets #rightarrow ll, 10 < M < 50 GeV', color= 29, syst_frac=0.10, xsec=1.58e4),
    MCSample('dyjetstollM50_2017',    '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v1/AODSIM',          103599638, nice='DY + jets #rightarrow ll, M > 50 GeV', color= 32, syst_frac=0.10, xsec=5.34e3),
    ]

example_samples_ttbar_2017 = [
    MCSample('example_ttbar_2017',     '/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/AODSIM',  249133364, nice='t#bar{t}',                   color=4,   syst_frac=0.15, xsec=831.76), 
    ]

met_samples_2017 = [
    MCSample('ttbar_2017',     '/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM',    249133364, nice='t#bar{t}',                   color=4,   syst_frac=0.15, xsec=831.76),
    ]

diboson_samples_2017 = [
    MCSample('ww_2017', '/WW_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM', 15634000, nice='WW', color = 9, syst_frac=0.10, xsec=75.8),
    MCSample('zz_2017', '/ZZ_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM', 2706000, nice='ZZ', color = 9, syst_frac=0.10, xsec=12.140),
    MCSample('wz_2017', '/WZ_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM', 7889000, nice='WZ', color =9, syst_frac=0.10, xsec=27.6)
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

ZHToSSTodddd_samples_2017 = [ 
    MCSample('ZHToSSTodddd_tau1mm_M55_2017', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 49997), 
    MCSample('ZHToSSTodddd_tau300um_M55_2017', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-55_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM', 49997), 
]

WplusHToSSTodddd_samples_2017 = [
    MCSample('WplusHToSSTodddd_tau30mm_M55_2017', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-30_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 47998), 
    MCSample('WplusHToSSTodddd_tau1mm_M55_2017', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 49991), 
    MCSample('WplusHToSSTodddd_tau300um_M55_2017', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 49995), 
]

WminusHToSSTodddd_samples_2017 = [
    MCSample('WminusHToSSTodddd_tau1mm_M55_2017', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 49995), 
    MCSample('WminusHToSSTodddd_tau300um_M55_2017', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 47995), 
]
#all_signal_samples_2017 = mfv_signal_samples_2017 + mfv_stopdbardbar_samples_2017 + mfv_stopbbarbbar_samples_2017 + mfv_stoplb_samples_2017 + mfv_stopld_samples_2017 + HToSSTobbbb_samples_2017 + HToSSTodddd_samples_2017 + mfv_splitSUSY_samples_2017
all_signal_samples_2017 = mfv_stoplb_samples_2017 + mfv_stopld_samples_2017 + ZHToSSTodddd_samples_2017 + WplusHToSSTodddd_samples_2017 + WminusHToSSTodddd_samples_2017 

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

ttbar_samples_2018 = []

bjet_samples_2018 = []

# leptonic_samples_2018 = [
#     MCSample('dyjetstollM10_2018',    '/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v2/AODSIM', 99573483, nice='$DY + jets #rightarrow ll$, $10 < M < 50$ \\GeV', color= 29, syst_frac=0.10, xsec=1.589e4),
#     MCSample('dyjetstollM50_2018',    '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v1/AODSIM',     98594572, nice='$DY + jets #rightarrow ll$, $M > 50$ \\GeV', color= 32, syst_frac=0.10, xsec=5.398e3),
#     MCSample('wjetstolnu_2018',       '/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v1/AODSIM',          83115836, nice='$W + jets #rightarrow l#nu$', color=  9, syst_frac=0.10, xsec=5.294e4),
#     ]

leptonic_samples_2018 = [
    MCSample('wjetstolnu_2018',       '/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM',          82442496, nice='$W + jets #rightarrow l#nu$', color=  9, syst_frac=0.10, xsec=5.294e4),
    MCSample('dyjetstollM10_2018',    '/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM', 99288125, nice='$DY + jets #rightarrow ll$, $10 < M < 50$ \\GeV', color= 29, syst_frac=0.10, xsec=1.589e4),
    MCSample('dyjetstollM50_2018',    '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM',     96233328, nice='$DY + jets #rightarrow ll$, $M > 50$ \\GeV', color= 32, syst_frac=0.10, xsec=5.398e3),
]

met_samples_2018 = [
    MCSample('ttbar_2018',            '/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM',            306142112, nice='t#bar{t}',                   color=4,   syst_frac=0.15, xsec=7.572e+02),
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


#all_signal_samples_2018 = mfv_splitSUSY_samples_2018
all_signal_samples_2018 = mfv_stoplb_samples_2018 + mfv_stopld_samples_2018
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
    DataSample('SingleElectron20161B1', '/SingleElectron/Run2016B-ver1_HIPM_UL2016_MiniAODv2-v2/MINIAOD'),
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
    DataSample('SingleElectron20162F', '/SingleElectron/Run2016F-UL2016_MiniAODv2-v2/MINIAOD'),
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

Lepton_data_samples_2017 = [
    DataSample('SingleMuon2017B', '/SingleMuon/Run2017B-09Aug2019_UL2017-v1/AOD'),
    DataSample('SingleMuon2017C', '/SingleMuon/Run2017C-09Aug2019_UL2017-v1/AOD'),
    DataSample('SingleMuon2017D', '/SingleMuon/Run2017D-09Aug2019_UL2017-v1/AOD'),
    DataSample('SingleMuon2017E', '/SingleMuon/Run2017E-09Aug2019_UL2017-v1/AOD'),
    DataSample('SingleMuon2017F', '/SingleMuon/Run2017F-09Aug2019_UL2017-v1/AOD'),
    DataSample('SingleElectron2017B', '/SingleElectron/Run2017B-09Aug2019_UL2017-v1/AOD'),
    DataSample('SingleElectron2017C', '/SingleElectron/Run2017C-09Aug2019_UL2017-v1/AOD'),
    DataSample('SingleElectron2017D', '/SingleElectron/Run2017D-09Aug2019_UL2017-v1/AOD'),
    DataSample('SingleElectron2017E', '/SingleElectron/Run2017E-09Aug2019_UL2017-v1/AOD'),
    DataSample('SingleElectron2017F', '/SingleElectron/Run2017F-09Aug2019_UL2017_rsb-v2/AOD'),
    ]
    

auxiliary_data_samples_2017 = [
    DataSample('SingleMuon2017B', '/SingleMuon/Run2017B-09Aug2019_UL2017-v1/AOD'),
    DataSample('SingleMuon2017C', '/SingleMuon/Run2017C-09Aug2019_UL2017-v1/AOD'),
    DataSample('SingleMuon2017D', '/SingleMuon/Run2017D-09Aug2019_UL2017-v1/AOD'),
    DataSample('SingleMuon2017E', '/SingleMuon/Run2017E-09Aug2019_UL2017-v1/AOD'),
    DataSample('SingleMuon2017F', '/SingleMuon/Run2017F-09Aug2019_UL2017-v1/AOD'),
    ]

singleelectron_data_samples_2017 = [
    DataSample('SingleElectron2017B', '/SingleElectron/Run2017B-09Aug2019_UL2017-v1/AOD'),
    DataSample('SingleElectron2017C', '/SingleElectron/Run2017C-09Aug2019_UL2017-v1/AOD'),
    DataSample('SingleElectron2017D', '/SingleElectron/Run2017D-09Aug2019_UL2017-v1/AOD'),
    DataSample('SingleElectron2017E', '/SingleElectron/Run2017E-09Aug2019_UL2017-v1/AOD'),
    DataSample('SingleElectron2017F', '/SingleElectron/Run2017F-09Aug2019_UL2017_rsb-v2/AOD'),
]

#Switching data with auxiliary data
auxiliary_data_samples_2018 = [
    DataSample('MET2018A', '/MET/Run2018A-12Nov2019_UL2018-v3/AOD'),  
    DataSample('MET2018B', '/MET/Run2018B-12Nov2019_UL2018-v3/AOD'),  
    DataSample('MET2018C', '/MET/Run2018C-12Nov2019_UL2018_rsb-v1/AOD'), 
    DataSample('MET2018D', '/MET/Run2018D-12Nov2019_UL2018_rsb-v2/AOD'), 
]

#FIXME: may need to reorganize how data is loaded for different cases
JetHT_data_samples_2018 = [
    DataSample('SingleMuon2017B', '/SingleMuon/Run2017B-09Aug2019_UL2017-v1/AOD'),
    DataSample('SingleMuon2017C', '/SingleMuon/Run2017C-09Aug2019_UL2017-v1/AOD'),
    DataSample('SingleMuon2017D', '/SingleMuon/Run2017D-09Aug2019_UL2017-v1/AOD'),
    DataSample('SingleMuon2017E', '/SingleMuon/Run2017E-09Aug2019_UL2017-v1/AOD'),
    DataSample('SingleMuon2017F', '/SingleMuon/Run2017F-09Aug2019_UL2017-v1/AOD'),
    DataSample('SingleElectron2017B', '/SingleElectron/Run2017B-09Aug2019_UL2017-v1/AOD'),
    DataSample('SingleElectron2017C', '/SingleElectron/Run2017C-09Aug2019_UL2017-v1/AOD'),
    DataSample('SingleElectron2017D', '/SingleElectron/Run2017D-09Aug2019_UL2017-v1/AOD'),
    DataSample('SingleElectron2017E', '/SingleElectron/Run2017E-09Aug2019_UL2017-v1/AOD'),
    DataSample('SingleElectron2017F', '/SingleElectron/Run2017F-09Aug2019_UL2017_rsb-v2/AOD'),
]

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
    'met_samples_20161',
    'met_samples_20162',
    'diboson_samples_20161',
    'diboson_samples_20162',
    'mfv_stoplb_samples_20161',
    'mfv_stopld_samples_20161',
    'mfv_stoplb_samples_20162',
    'mfv_stopld_samples_20162',
    'example_samples_ttbar_2017',
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
    'HToSSTobbbb_samples_2017',
    'HToSSTodddd_samples_2017',
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

for sample in data_samples_2017 + Lepton_data_samples_2017: #auxiliary_data_samples_2017 + singleelectron_data_samples_2017:
    sample.add_dataset('miniaod', sample.dataset.replace('AOD', 'MINIAOD'))
for sample in data_samples_2018 + auxiliary_data_samples_2018 + egamma_data_samples_2018:
    sample.add_dataset('miniaod', sample.dataset.replace('AOD', 'MINIAOD'))
for sample in Lepton_data_samples_2018:
    sample.add_dataset('miniaod', sample.dataset)


qcdht0200_2017.add_dataset('miniaod', '/QCD_HT200to300_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v2/MINIAODSIM', 57721120)
qcdht0300_2017.add_dataset('miniaod', '/QCD_HT300to500_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v2/MINIAODSIM',   57191140)
qcdht0500_2017.add_dataset('miniaod', '/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v2/MINIAODSIM',  9188310)
qcdht0500ext_2017.add_dataset('miniaod', '/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6_ext1-v1/MINIAODSIM',  57880117)
qcdht0700_2017.add_dataset('miniaod', '/QCD_HT700to1000_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v2/MINIAODSIM',  45812757)
qcdht1000_2017.add_dataset('miniaod', '/QCD_HT1000to1500_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v2/MINIAODSIM', 15346629)
qcdht1500_2017.add_dataset('miniaod', '/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v1/MINIAODSIM',    7497684)
qcdht2000_2017.add_dataset('miniaod', '/QCD_HT2000toInf_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v2/MINIAODSIM',  5457021)

# qcdmupt15_2017.add_dataset('miniaod', '/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v1/MINIAODSIM', 17580112)
# qcdempt015_2017.add_dataset('miniaod', '/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v1/MINIAODSIM', 7908107)
# qcdempt020_2017.add_dataset('miniaod', '/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v1/MINIAODSIM', 14146285)
# qcdempt030_2017.add_dataset('miniaod', '/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2/MINIAODSIM', 8784542)
# qcdempt050_2017.add_dataset('miniaod', '/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2/MINIAODSIM', 10590542)
# qcdempt080_2017.add_dataset('miniaod', '/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2/MINIAODSIM', 9615719)
# qcdempt120_2017.add_dataset('miniaod', '/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2/MINIAODSIM', 9892235)
# qcdempt170_2017.add_dataset('miniaod', '/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2/MINIAODSIM', 3681297)
# qcdempt300_2017.add_dataset('miniaod', '/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2/MINIAODSIM', 2214934)
# qcdbctoept020_2017.add_dataset('miniaod', '/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2/MINIAODSIM', 14156589)
# qcdbctoept030_2017.add_dataset('miniaod', '/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2/MINIAODSIM', 15153568)
# qcdbctoept080_2017.add_dataset('miniaod', '/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2/MINIAODSIM', 15908608)
# qcdbctoept170_2017.add_dataset('miniaod', '/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2/MINIAODSIM', 15588245)
# qcdbctoept250_2017.add_dataset('miniaod', '/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v3/MINIAODSIM', 15557421)
 
    
ttbar_2017.add_dataset('miniaod', '/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 249133364) #FIXME ? new MiniAOD
#ttbarht0600_2017.add_dataset('miniaod', '/TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',    81507662)
#ttbarht0800_2017.add_dataset('miniaod', '/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',   40191637)
#ttbarht1200_2017.add_dataset('miniaod', '/TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',  13214871)
#ttbarht2500_2017.add_dataset('miniaod', '/TTJets_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v3/MINIAODSIM',    5155687)
#wjetstolnu_2017.add_dataset('miniaod', '/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v1/MINIAODSIM', 81254459)
wjetstolnu_amcatnlo_2017.add_dataset('miniaod', '/WJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 26838734)
dyjetstollM10_2017.add_dataset('miniaod', '/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2/MINIAODSIM', 70530127)
dyjetstollM50_2017.add_dataset('miniaod', '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v1/MINIAODSIM', 103287684)
#dyjetstollM50ext_2017.add_dataset('miniaod', '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017RECOSIMstep_12Apr2018_94X_mc2017_realistic_v14_ext1-v1/MINIAODSIM', 49125561)

zjetstonunuht0100_2017.add_dataset('miniaod', '/ZJetsToNuNu_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v1/MINIAODSIM', 19040741)
zjetstonunuht0200_2017.add_dataset('miniaod', '/ZJetsToNuNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v1/MINIAODSIM', 16547983)
zjetstonunuht0400_2017.add_dataset('miniaod', '/ZJetsToNuNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v1/MINIAODSIM', 13948916)
zjetstonunuht0600_2017.add_dataset('miniaod', '/ZJetsToNuNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v1/MINIAODSIM', 4403555)
zjetstonunuht0800_2017.add_dataset('miniaod', '/ZJetsToNuNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v1/MINIAODSIM', 1446755)
zjetstonunuht1200_2017.add_dataset('miniaod', '/ZJetsToNuNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v1/MINIAODSIM', 267125)
zjetstonunuht2500_2017.add_dataset('miniaod', '/ZJetsToNuNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v1/MINIAODSIM', 172487)

ww_2017.add_dataset('miniaod', '/WW_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2/MINIAODSIM', 15883000)
wz_2017.add_dataset('miniaod', '/WZ_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2/MINIAODSIM', 2708000)
zz_2017.add_dataset('miniaod', '/ZZ_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2/MINIAODSIM', 7898000)

# the 2018 samples have 'MLM' in them so this works still, ugh
qcdht0200_2018.add_dataset('miniaod', '/QCD_HT200to300_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v2/MINIAODSIM', 22826901)
qcdht0200ext_2018.add_dataset('miniaod', '/QCD_HT200to300_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1_ext1-v1/MINIAODSIM', 34740016)
qcdht0300_2018.add_dataset('miniaod', ' /QCD_HT300to500_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v2/MINIAODSIM',   55135074)
qcdht0500_2018.add_dataset('miniaod', '/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v2/MINIAODSIM',   58487165)
qcdht0700_2018.add_dataset('miniaod', '/QCD_HT700to1000_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v2/MINIAODSIM',  47703400)
qcdht1000_2018.add_dataset('miniaod', '/QCD_HT1000to1500_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v2/MINIAODSIM', 15675643)
qcdht1500_2018.add_dataset('miniaod', '/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v2/MINIAODSIM', 10612885)
qcdht2000_2018.add_dataset('miniaod', '/QCD_HT2000toInf_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v2/MINIAODSIM',   4504262)
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

for sample in qcd_lep_samples_2018 + leptonic_samples_2018 + diboson_samples_2018 + met_samples_2018: 
    sample.add_dataset('miniaod', sample.dataset)
    
for sample in met_samples_2017:
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


for sample in HToSSTobbbb_samples_2017 + HToSSTodddd_samples_2017:
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
#is this the correct ntuple version? 
#mfv_stopld_tau001000um_M1000_2018
#for x in mfv_stopld_tau000100um_M0200_2018, mfv_stopld_tau000300um_M0200_2018, mfv_stopld_tau000100um_M0600_2018, mfv_stopld_tau000300um_M0600_2018, mfv_stopld_tau000100um_M1000_2018, mfv_stopld_tau000300um_M1000_2018, mfv_stopld_tau000100um_M1600_2018, mfv_stopld_tau000300um_M1600_2018:                                                                                                                                                  
example_ttbar_2017.add_dataset('trackmoverulv30lepmv2')


for x in WplusHToSSTodddd_tau30mm_M55_2017, WplusHToSSTodddd_tau1mm_M55_2017, WplusHToSSTodddd_tau300um_M55_2017:
    x.add_dataset("trackmovermctruthulv30lepmumv3")


qcdmupt15_2017.add_dataset('trackmovertestulv30lepmumv5', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)

"""
qcdempt015_2017.add_dataset('trackmoverulv30lepmumv5', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
qcdmupt15_2017.add_dataset('trackmoverulv30lepmumv5', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
qcdempt020_2017.add_dataset('trackmoverulv30lepmumv5', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
qcdempt030_2017.add_dataset('trackmoverulv30lepmumv5', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
qcdempt050_2017.add_dataset('trackmoverulv30lepmumv5', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
qcdempt080_2017.add_dataset('trackmoverulv30lepmumv5', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
qcdempt120_2017.add_dataset('trackmoverulv30lepmumv5', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
qcdempt170_2017.add_dataset('trackmoverulv30lepmumv5', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
qcdempt300_2017.add_dataset('trackmoverulv30lepmumv5', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
qcdbctoept020_2017.add_dataset('trackmoverulv30lepmumv5', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
qcdbctoept030_2017.add_dataset('trackmoverulv30lepmumv5', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
qcdbctoept080_2017.add_dataset('trackmoverulv30lepmumv5', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
qcdbctoept170_2017.add_dataset('trackmoverulv30lepmumv5', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
qcdbctoept250_2017.add_dataset('trackmoverulv30lepmumv5', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
wjetstolnu_2017.add_dataset('trackmoverulv30lepmumv5', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
wjetstolnu_amcatnlo_2017.add_dataset('trackmoverulv30lepmumv5', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
dyjetstollM10_2017.add_dataset('trackmoverulv30lepmumv5', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
dyjetstollM50_2017.add_dataset('trackmoverulv30lepmumv5', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
ww_2017.add_dataset('trackmoverulv30lepmumv5', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
zz_2017.add_dataset('trackmoverulv30lepmumv5', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
wz_2017.add_dataset('trackmoverulv30lepmumv5', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
SingleMuon2017B.add_dataset('trackmoverulv30lepmumv5', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
SingleMuon2017C.add_dataset('trackmoverulv30lepmumv5', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
SingleMuon2017D.add_dataset('trackmoverulv30lepmumv5', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
SingleMuon2017E.add_dataset('trackmoverulv30lepmumv5', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
SingleMuon2017F.add_dataset('trackmoverulv30lepmumv5', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
SingleElectron2017B.add_dataset('trackmoverulv30lepmumv5', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
SingleElectron2017C.add_dataset('trackmoverulv30lepmumv5', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
SingleElectron2017D.add_dataset('trackmoverulv30lepmumv5', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
SingleElectron2017E.add_dataset('trackmoverulv30lepmumv5', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
SingleElectron2017F.add_dataset('trackmoverulv30lepmumv5', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
ttbar_2017.add_dataset("trackmoverulv30lepmumv5")
"""

qcdempt015_2017.add_dataset('trackmoverulv30lepelemv5', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
qcdmupt15_2017.add_dataset('trackmoverulv30lepelemv5', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
qcdempt020_2017.add_dataset('trackmoverulv30lepelemv5', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
qcdempt030_2017.add_dataset('trackmoverulv30lepelemv5', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
qcdempt050_2017.add_dataset('trackmoverulv30lepelemv5', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
qcdempt080_2017.add_dataset('trackmoverulv30lepelemv5', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
qcdempt120_2017.add_dataset('trackmoverulv30lepelemv5', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
qcdempt170_2017.add_dataset('trackmoverulv30lepelemv5', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
qcdempt300_2017.add_dataset('trackmoverulv30lepelemv5', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
qcdbctoept020_2017.add_dataset('trackmoverulv30lepelemv5', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
qcdbctoept030_2017.add_dataset('trackmoverulv30lepelemv5', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
qcdbctoept080_2017.add_dataset('trackmoverulv30lepelemv5', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
qcdbctoept170_2017.add_dataset('trackmoverulv30lepelemv5', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
qcdbctoept250_2017.add_dataset('trackmoverulv30lepelemv5', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
wjetstolnu_2017.add_dataset('trackmoverulv30lepelemv5', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
wjetstolnu_amcatnlo_2017.add_dataset('trackmoverulv30lepelemv5', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
dyjetstollM10_2017.add_dataset('trackmoverulv30lepelemv5', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
#dyjetstollM50_2017.add_dataset('trackmoverulv30lepelemv5', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
ww_2017.add_dataset('trackmoverulv30lepelemv5', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
zz_2017.add_dataset('trackmoverulv30lepelemv5', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
wz_2017.add_dataset('trackmoverulv30lepelemv5', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
SingleMuon2017B.add_dataset('trackmoverulv30lepelemv5', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
SingleMuon2017C.add_dataset('trackmoverulv30lepelemv5', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
SingleMuon2017D.add_dataset('trackmoverulv30lepelemv5', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
SingleMuon2017E.add_dataset('trackmoverulv30lepelemv5', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
SingleMuon2017F.add_dataset('trackmoverulv30lepelemv5', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
SingleElectron2017B.add_dataset('trackmoverulv30lepelemv5', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
SingleElectron2017C.add_dataset('trackmoverulv30lepelemv5', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
SingleElectron2017D.add_dataset('trackmoverulv30lepelemv5', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
SingleElectron2017E.add_dataset('trackmoverulv30lepelemv5', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
SingleElectron2017F.add_dataset('trackmoverulv30lepelemv5', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
ttbar_2017.add_dataset("trackmoverulv30lepelemv5")


#    x.add_dataset("ntupleulv1lepm")
#WplusHToSSTodddd_tau1mm_M55_2017.add_dataset('ntupleulsed2ndxyv29lepm', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/pekotamn-NtupleULsed2ndxyV29Lepm_2017-1ea75a506c8d2d1e690db79eb01e9fee/USER', 48991)
"""
qcdempt015_2017.add_dataset('ntupleultkrec1p1v30lepm', '/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/pekotamn-NtupleULtkrec1p1V30Lepm_2017-e174bf093e29bc2636c80c13a8c539e2/USER', 0)
qcdmupt15_2017.add_dataset('ntupleultkrec1p1v30lepm', '/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/pekotamn-NtupleULtkrec1p1V30Lepm_2017-d21448ae93ecd92747dda37d84a05a10/USER', 981)
qcdempt020_2017.add_dataset('ntupleultkrec1p1v30lepm', '/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/pekotamn-NtupleULtkrec1p1V30Lepm_2017-86894347ae77c776a9a127a0f047a36f/USER', 0)
#qcdempt030_2017.add_dataset('ntupleultkrec1p1v30lepm', '/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/pekotamn-NtupleULtkrec1p1V30Lepm_2017-39196d3b7fddb5c4ec45cc4405ac034b/USER', 1)
qcdempt050_2017.add_dataset('ntupleultkrec1p1v30lepm', '/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/pekotamn-NtupleULtkrec1p1V30Lepm_2017-f812e59ca07feed634cabc59720eeb18/USER', 3)
qcdempt080_2017.add_dataset('ntupleultkrec1p1v30lepm', '/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/pekotamn-NtupleULtkrec1p1V30Lepm_2017-04e8f46312798e378f212680f7a44fc7/USER', 15)
#qcdempt120_2017.add_dataset('ntupleultkrec1p1v30lepm', '/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/pekotamn-NtupleULtkrec1p1V30Lepm_2017-71e663173b67001e58dbf95ccd753490/USER', 25)
qcdempt170_2017.add_dataset('ntupleultkrec1p1v30lepm', '/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/pekotamn-NtupleULtkrec1p1V30Lepm_2017-648a967cc0204746a26b482209db6685/USER', 18)
qcdempt300_2017.add_dataset('ntupleultkrec1p1v30lepm', '/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/pekotamn-NtupleULtkrec1p1V30Lepm_2017-3341ee812431099f2cbeec30938b1591/USER', 32)
#qcdbctoept020_2017.add_dataset('ntupleultkrec1p1v30lepm', '/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/pekotamn-NtupleULtkrec1p1V30Lepm_2017-af9545748bab85f3817fdd2bf21de76b/USER', 2)
qcdbctoept030_2017.add_dataset('ntupleultkrec1p1v30lepm', '/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/pekotamn-NtupleULtkrec1p1V30Lepm_2017-2238b2b38655fe17401559332a07fbdb/USER', 17)
qcdbctoept080_2017.add_dataset('ntupleultkrec1p1v30lepm', '/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/pekotamn-NtupleULtkrec1p1V30Lepm_2017-33d4ce9a547e566f2399f8b18ef7172d/USER', 145)
#qcdbctoept170_2017.add_dataset('ntupleultkrec1p1v30lepm', '/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/pekotamn-NtupleULtkrec1p1V30Lepm_2017-99fc4d8fc015d19424e5253773a805be/USER', 297)
qcdbctoept250_2017.add_dataset('ntupleultkrec1p1v30lepm', '/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/pekotamn-NtupleULtkrec1p1V30Lepm_2017-0736f232df1df27a29fb89801a285301/USER', 343)
wjetstolnu_2017.add_dataset('ntupleultkrec1p1v30lepm', '/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/pekotamn-NtupleULtkrec1p1V30Lepm_2017-2b7ea64235d9661b39b04b1822a88e8d/USER', 13453)
dyjetstollM10_2017.add_dataset('ntupleultkrec1p1v30lepm', '/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/pekotamn-NtupleULtkrec1p1V30Lepm_2017-8592d5c4e61d4acba487f3bed7628557/USER', 551)
#dyjetstollM50_2017.add_dataset('ntupleultkrec1p1v30lepm', '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/pekotamn-NtupleULtkrec1p1V30Lepm_2017-a49d43bc6b6debffbbb304b6cab37634/USER', 45838)
ww_2017.add_dataset('ntupleultkrec1p1v30lepm', '/WW_TuneCP5_13TeV-pythia8/pekotamn-NtupleULtkrec1p1V30Lepm_2017-7ba92c650f8bb42738d43bb5c51930a7/USER', 5044)
zz_2017.add_dataset('ntupleultkrec1p1v30lepm', '/WZ_TuneCP5_13TeV-pythia8/pekotamn-NtupleULtkrec1p1V30Lepm_2017-851e8cac915711e2e9ba1997f38b845c/USER', 4631)
wz_2017.add_dataset('ntupleultkrec1p1v30lepm', '/ZZ_TuneCP5_13TeV-pythia8/pekotamn-NtupleULtkrec1p1V30Lepm_2017-b9f606762f987332e464ccebd24e32ee/USER', 1819)
WplusHToSSTodddd_tau1mm_M55_2017.add_dataset('ntupleultkrec1p1v30lepm', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/pekotamn-NtupleULtkrec1p1V30Lepm_2017-346b67f34683a8793ed44761d3fd3560/USER', 49991)
ttbar_2017.add_dataset("ntupleultkrec1p1v30lepm")
"""
"""
qcdempt015_2017.add_dataset('ntupleultkrec0p9v30lepm', '/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/pekotamn-NtupleULtkrec0p9V30Lepm_2017-669d0e0f0cde3b7afe61e6752aa42dd8/USER', 0)
qcdmupt15_2017.add_dataset('ntupleultkrec0p9v30lepm', '/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/pekotamn-NtupleULtkrec0p9V30Lepm_2017-f069a29cdf10473b6a29513808aeacf1/USER', 1162)
qcdempt020_2017.add_dataset('ntupleultkrec0p9v30lepm', '/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/pekotamn-NtupleULtkrec0p9V30Lepm_2017-10a5c67777e987333b2a041dba0a60df/USER', 0)
#qcdempt030_2017.add_dataset('ntupleultkrec0p9v30lepm', '/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/pekotamn-NtupleULtkrec0p9V30Lepm_2017-2d51037731ee8e80ec7638c77c748f6e/USER', 1)
qcdempt050_2017.add_dataset('ntupleultkrec0p9v30lepm', '/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/pekotamn-NtupleULtkrec0p9V30Lepm_2017-b274bedede9866f76fcf07c899001262/USER', 5)
qcdempt080_2017.add_dataset('ntupleultkrec0p9v30lepm', '/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/pekotamn-NtupleULtkrec0p9V30Lepm_2017-2efeb12e6b7435a91f92fa4d06fbbadf/USER', 16)
#qcdempt120_2017.add_dataset('ntupleultkrec0p9v30lepm', '/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/pekotamn-NtupleULtkrec0p9V30Lepm_2017-9c853e42f9acd4873efdd7f995d4297c/USER', 32)
qcdempt170_2017.add_dataset('ntupleultkrec0p9v30lepm', '/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/pekotamn-NtupleULtkrec0p9V30Lepm_2017-9fd4ea68362024e8c0f213d6732163f3/USER', 24)
qcdempt300_2017.add_dataset('ntupleultkrec0p9v30lepm', '/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/pekotamn-NtupleULtkrec0p9V30Lepm_2017-bb975ca7d3050f55918436635b0e4e85/USER', 36)
#qcdbctoept020_2017.add_dataset('ntupleultkrec0p9v30lepm', '/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/pekotamn-NtupleULtkrec0p9V30Lepm_2017-f13b21b8eab8167011de542898010078/USER', 3)
qcdbctoept030_2017.add_dataset('ntupleultkrec0p9v30lepm', '/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/pekotamn-NtupleULtkrec0p9V30Lepm_2017-fa15158f91870cc8e3c7728c28caa50b/USER', 20)
qcdbctoept080_2017.add_dataset('ntupleultkrec0p9v30lepm', '/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/pekotamn-NtupleULtkrec0p9V30Lepm_2017-59d40a1ef456ccc80554096c52541a74/USER', 172)
#qcdbctoept170_2017.add_dataset('ntupleultkrec0p9v30lepm', '/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/pekotamn-NtupleULtkrec0p9V30Lepm_2017-c355622c0d06ebc135feb98073cb2e14/USER', 368)
qcdbctoept250_2017.add_dataset('ntupleultkrec0p9v30lepm', '/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/pekotamn-NtupleULtkrec0p9V30Lepm_2017-42b49903f4934828af022a3f0bd8ee46/USER', 434)
wjetstolnu_2017.add_dataset('ntupleultkrec0p9v30lepm', '/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/pekotamn-NtupleULtkrec0p9V30Lepm_2017-f65028bd0cc3b17ef5ba65fa2dbeecfb/USER', 18489)
dyjetstollM10_2017.add_dataset('ntupleultkrec0p9v30lepm', '/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/pekotamn-NtupleULtkrec0p9V30Lepm_2017-92eb698c798d9f6f9bc3a1119f4f47c4/USER', 715)
#dyjetstollM50_2017.add_dataset('ntupleultkrec0p9v30lepm', '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/pekotamn-NtupleULtkrec0p9V30Lepm_2017-399483b3e0f9cb20fddea3f08217f709/USER', 60530)
ww_2017.add_dataset('ntupleultkrec0p9v30lepm', '/WW_TuneCP5_13TeV-pythia8/pekotamn-NtupleULtkrec0p9V30Lepm_2017-2a771487d2960a24e9c4d4a7dddea1f1/USER', 6683)
zz_2017.add_dataset('ntupleultkrec0p9v30lepm', '/WZ_TuneCP5_13TeV-pythia8/pekotamn-NtupleULtkrec0p9V30Lepm_2017-2019dbee7cc403624a955f317462046a/USER', 5733)
wz_2017.add_dataset('ntupleultkrec0p9v30lepm', '/ZZ_TuneCP5_13TeV-pythia8/pekotamn-NtupleULtkrec0p9V30Lepm_2017-3fdf4f37033be500d0e9e6c5b1eda755/USER', 2230)
WplusHToSSTodddd_tau1mm_M55_2017.add_dataset('ntupleultkrec0p9v30lepm', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/pekotamn-NtupleULtkrec0p9V30Lepm_2017-0c883bb0cd9b99f7f47586f3be03c55d/USER', 49991)
ttbar_2017.add_dataset("ntupleultkrec0p9v30lepm")
"""

"""
qcdempt015_2017.add_dataset('ntupleuloffshjv30lepm', '/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/pekotamn-NtupleULoffshjV30Lepm_2017-6d20d00f6c5ebc9510bd8f377a244a84/USER', 0)
qcdmupt15_2017.add_dataset('ntupleuloffshjv30lepm', '/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/pekotamn-NtupleULoffshjV30Lepm_2017-8678ca1ffcefb50a8541d53235ed2942/USER', 1039)
qcdempt020_2017.add_dataset('ntupleuloffshjv30lepm', '/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/pekotamn-NtupleULoffshjV30Lepm_2017-6f46d948f7d88215cb915e18518736d2/USER', 0)
qcdempt030_2017.add_dataset('ntupleuloffshjv30lepm', '/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/pekotamn-NtupleULoffshjV30Lepm_2017-fe2b2f0359b1d3bdd8f8df7fb9d8cbac/USER', 1)
qcdempt050_2017.add_dataset('ntupleuloffshjv30lepm', '/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/pekotamn-NtupleULoffshjV30Lepm_2017-7e639af6eedd5c9895267bc00ce276dd/USER', 3)
qcdempt080_2017.add_dataset('ntupleuloffshjv30lepm', '/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/pekotamn-NtupleULoffshjV30Lepm_2017-f66b16f2753a2bd37ce98aac93ef70f2/USER', 16)
qcdempt120_2017.add_dataset('ntupleuloffshjv30lepm', '/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/pekotamn-NtupleULoffshjV30Lepm_2017-d778ca5ee72babbb748ae3fb11fed51e/USER', 27)
qcdbctoept020_2017.add_dataset('ntupleuloffshjv30lepm', '/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/pekotamn-NtupleULoffshjV30Lepm_2017-422a3e901e2960cc60fc69073b302967/USER', 3)
qcdbctoept030_2017.add_dataset('ntupleuloffshjv30lepm', '/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/pekotamn-NtupleULoffshjV30Lepm_2017-fc7b953679563de5613873e1bbb81161/USER', 18)
qcdbctoept080_2017.add_dataset('ntupleuloffshjv30lepm', '/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/pekotamn-NtupleULoffshjV30Lepm_2017-5701906e1a7ccc1f21989fb6d9bea9d6/USER', 158)
qcdbctoept170_2017.add_dataset('ntupleuloffshjv30lepm', '/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/pekotamn-NtupleULoffshjV30Lepm_2017-441b6760314191f963570754443c34eb/USER', 329)
qcdbctoept250_2017.add_dataset('ntupleuloffshjv30lepm', '/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/pekotamn-NtupleULoffshjV30Lepm_2017-9cb58053cb0897ddd2b03925fbc1946c/USER', 387)
wjetstolnu_2017.add_dataset('ntupleuloffshjv30lepm', '/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/pekotamn-NtupleULoffshjV30Lepm_2017-66a3468c10265803f09abeb56759cffd/USER', 15541)
dyjetstollM10_2017.add_dataset('ntupleuloffshjv30lepm', '/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/pekotamn-NtupleULoffshjV30Lepm_2017-0fa2945620f50558eea5cef278655850/USER', 623)
dyjetstollM50_2017.add_dataset('ntupleuloffshjv30lepm', '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/pekotamn-NtupleULoffshjV30Lepm_2017-63c14ad83a67de765612db4f2f646292/USER', 53700)
ww_2017.add_dataset('ntupleuloffshjv30lepm', '/WW_TuneCP5_13TeV-pythia8/pekotamn-NtupleULoffshjV30Lepm_2017-039c2a18d30b0ba429aa542226914030/USER', 5744)
zz_2017.add_dataset('ntupleuloffshjv30lepm', '/WZ_TuneCP5_13TeV-pythia8/pekotamn-NtupleULoffshjV30Lepm_2017-33d99ce1e1ac4bde5df3f706aa465abc/USER', 5113)
wz_2017.add_dataset('ntupleuloffshjv30lepm', '/ZZ_TuneCP5_13TeV-pythia8/pekotamn-NtupleULoffshjV30Lepm_2017-a5237143b49548c5fbd29b068544b45b/USER', 2001)
ttbar_2017.add_dataset("ntupleuloffshjv30lepm")
"""

"""
qcdempt015_2017.add_dataset('ntupleulv30lepm', '/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/pekotamn-NtupleULV30Lepm_2017-9978bb4b98cfc56ae5630fa1bd7044b3/USER', 0)
qcdmupt15_2017.add_dataset('ntupleulv30lepm', '/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/pekotamn-NtupleULV30Lepm_2017-8dc0271a6c5ba30b5ac810c9fe35fdc1/USER', 1064)
qcdempt020_2017.add_dataset('ntupleulv30lepm', '/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/pekotamn-NtupleULV30Lepm_2017-cd60535f6f08e120b12215558713503e/USER', 0)
qcdempt030_2017.add_dataset('ntupleulv30lepm', '/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/pekotamn-NtupleULV30Lepm_2017-1b1251eab96407f26b2a4fc9a5f63153/USER', 1)
qcdempt050_2017.add_dataset('ntupleulv30lepm', '/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/pekotamn-NtupleULV30Lepm_2017-b90433d96ea93951ac26293b1b88ab01/USER', 3)
qcdempt080_2017.add_dataset('ntupleulv30lepm', '/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/pekotamn-NtupleULV30Lepm_2017-06f5efb19504d079a76ce5ef18a04709/USER', 16)
qcdempt120_2017.add_dataset('ntupleulv30lepm', '/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/pekotamn-NtupleULV30Lepm_2017-09e5379127971c9225259d9a87c95f7a/USER', 28)
qcdempt170_2017.add_dataset('ntupleulv30lepm', '/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/pekotamn-NtupleULV30Lepm_2017-0afb68774d1e54a7a214ee3fa5fb7d57/USER', 21)
qcdempt300_2017.add_dataset('ntupleulv30lepm', '/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/pekotamn-NtupleULV30Lepm_2017-f7e95e7fb34392dd29f5d9b6503fdf53/USER', 32)
qcdbctoept020_2017.add_dataset('ntupleulv30lepm', '/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/pekotamn-NtupleULV30Lepm_2017-6daf381bd6bbcc52f558d240758c23ad/USER', 3)
qcdbctoept030_2017.add_dataset('ntupleulv30lepm', '/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/pekotamn-NtupleULV30Lepm_2017-639c98fb2014ee9e2832c93844899a2d/USER', 18)
qcdbctoept080_2017.add_dataset('ntupleulv30lepm', '/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/pekotamn-NtupleULV30Lepm_2017-edfc63adbeafce3570a1443d81a3bcd3/USER', 158)
qcdbctoept170_2017.add_dataset('ntupleulv30lepm', '/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/pekotamn-NtupleULV30Lepm_2017-b73c2ab3a105c049b1eb88caf3f756e5/USER', 329)
qcdbctoept250_2017.add_dataset('ntupleulv30lepm', '/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/pekotamn-NtupleULV30Lepm_2017-fa211d110e4fba630eea9e6437b11437/USER', 387)
#wjetstolnu_2017.add_dataset('ntupleulv30lepm', '/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/pekotamn-NtupleULV30Lepm_2017-4497c885993fd1eed1071065bde1db47/USER', 15541)
#dyjetstollM10_2017.add_dataset('ntupleulv30lepm', '/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/pekotamn-NtupleULV30Lepm_2017-47bd9f033c83c3dfedee1ddb8de2a475/USER', 623)
dyjetstollM50_2017.add_dataset('ntupleulv30lepm', '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/pekotamn-NtupleULV30Lepm_2017-90e9f5483457df9399b65fbd1036198c/USER', 54098)
ww_2017.add_dataset('ntupleulv30lepm', '/WW_TuneCP5_13TeV-pythia8/pekotamn-NtupleULV30Lepm_2017-98be00e9dc3f01558c85f81f1e37d957/USER', 5744)
zz_2017.add_dataset('ntupleulv30lepm', '/WZ_TuneCP5_13TeV-pythia8/pekotamn-NtupleULV30Lepm_2017-de2759ad869964d2cf26cf584294708e/USER', 5113)
wz_2017.add_dataset('ntupleulv30lepm', '/ZZ_TuneCP5_13TeV-pythia8/pekotamn-NtupleULV30Lepm_2017-21f8eaed8f79ac77741c7f8751c85331/USER', 2001)
mfv_stoplb_tau010000um_M0400_2017.add_dataset('ntupleulv30lepm', '/DisplacedSUSY_stopToLBottom_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/pekotamn-NtupleULV30Lepm_2017-4b0a4fc92cfd83c809658507172e94f7/USER', 198737)
mfv_stoplb_tau001000um_M0400_2017.add_dataset('ntupleulv30lepm', '/DisplacedSUSY_stopToLBottom_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/pekotamn-NtupleULV30Lepm_2017-8ef31118e61e71aba89336aacd62f4b3/USER', 197003)
mfv_stopld_tau010000um_M0400_2017.add_dataset('ntupleulv30lepm', '/DisplacedSUSY_stopToLD_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/pekotamn-NtupleULV30Lepm_2017-c275abe32c4fd9b54d06cb5180840087/USER', 201845)
mfv_stopld_tau001000um_M0400_2017.add_dataset('ntupleulv30lepm', '/DisplacedSUSY_stopToLD_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/pekotamn-NtupleULV30Lepm_2017-d7b5786b77cb76c7dc14edba963069e7/USER', 197130)
WplusHToSSTodddd_tau30mm_M55_2017.add_dataset('ntupleulv30lepm', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-30_TuneCP5_13TeV-powheg-pythia8/pekotamn-NtupleULV30Lepm_2017-179ae03d8cca56dbf79b10ec8a577b20/USER', 47998)
WplusHToSSTodddd_tau1mm_M55_2017.add_dataset('ntupleulv30lepm', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/pekotamn-NtupleULV30Lepm_2017-cbbf712451aef07fd4a0ba890552b5fc/USER', 49991)
WplusHToSSTodddd_tau300um_M55_2017.add_dataset('ntupleulv30lepm', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/pekotamn-NtupleULV30Lepm_2017-bbe91de2f33c8d866685c55d4767669a/USER', 49995)
ttbar_2017.add_dataset("ntupleulv30lepm")
"""

"""
qcdempt015_2017.add_dataset('ntupleulsed3p5ndxyv29lepm', '/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/pekotamn-NtupleULsed3p5ndxyV29Lepm_2017-c85b19e0cc795becea0ebfb1df7ea777/USER', 0)
qcdmupt15_2017.add_dataset('ntupleulsed3p5ndxyv29lepm', '/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/pekotamn-NtupleULsed3p5ndxyV29Lepm_2017-1e0bd8b905851ad987b27e5639a5cd9c/USER', 1052)
qcdempt020_2017.add_dataset('ntupleulsed3p5ndxyv29lepm', '/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/pekotamn-NtupleULsed3p5ndxyV29Lepm_2017-fd127b1a85412228ba823e932e83ed74/USER', 0)
qcdempt030_2017.add_dataset('ntupleulsed3p5ndxyv29lepm', '/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/pekotamn-NtupleULsed3p5ndxyV29Lepm_2017-3c99e12e4f5f1405e7d4103976033b5a/USER', 1)
qcdempt050_2017.add_dataset('ntupleulsed3p5ndxyv29lepm', '/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/pekotamn-NtupleULsed3p5ndxyV29Lepm_2017-633d0606e73ba06d0d0bb5bad5fb1477/USER', 4)
qcdempt080_2017.add_dataset('ntupleulsed3p5ndxyv29lepm', '/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/pekotamn-NtupleULsed3p5ndxyV29Lepm_2017-67f1c5cbda3a8a91ad79f7cd19bfe168/USER', 15)
qcdempt120_2017.add_dataset('ntupleulsed3p5ndxyv29lepm', '/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/pekotamn-NtupleULsed3p5ndxyV29Lepm_2017-d79bb9ef11c97758873b2363a4e43749/USER', 31)
qcdempt170_2017.add_dataset('ntupleulsed3p5ndxyv29lepm', '/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/pekotamn-NtupleULsed3p5ndxyV29Lepm_2017-48d9db55cad3b9ad9205e2af69c31ce3/USER', 24)
qcdempt300_2017.add_dataset('ntupleulsed3p5ndxyv29lepm', '/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/pekotamn-NtupleULsed3p5ndxyV29Lepm_2017-8c58236cea9a9c049fd544a8138d588d/USER', 32)
qcdbctoept020_2017.add_dataset('ntupleulsed3p5ndxyv29lepm', '/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/pekotamn-NtupleULsed3p5ndxyV29Lepm_2017-3002429588aa4d24d9af057e5a644ce0/USER', 3)
qcdbctoept030_2017.add_dataset('ntupleulsed3p5ndxyv29lepm', '/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/pekotamn-NtupleULsed3p5ndxyV29Lepm_2017-75ace3b204bc02a63d98b68b797b34f5/USER', 21)
qcdbctoept080_2017.add_dataset('ntupleulsed3p5ndxyv29lepm', '/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/pekotamn-NtupleULsed3p5ndxyV29Lepm_2017-da58f72735db68f7c112120157ba7fc8/USER', 160)
qcdbctoept170_2017.add_dataset('ntupleulsed3p5ndxyv29lepm', '/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/pekotamn-NtupleULsed3p5ndxyV29Lepm_2017-4e8e6e4196a647eb2fd64c1007b5e1a5/USER', 332)
qcdbctoept250_2017.add_dataset('ntupleulsed3p5ndxyv29lepm', '/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/pekotamn-NtupleULsed3p5ndxyV29Lepm_2017-df414b29be7143f3281f3de025440645/USER', 397)
wjetstolnu_2017.add_dataset('ntupleulsed3p5ndxyv29lepm', '/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/pekotamn-NtupleULsed3p5ndxyV29Lepm_2017-8a8c073b232e23e8f0ac6898b42276b5/USER', 17541)
dyjetstollM10_2017.add_dataset('ntupleulsed3p5ndxyv29lepm', '/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/pekotamn-NtupleULsed3p5ndxyV29Lepm_2017-96f9d592b8bec85331423813e23b7058/USER', 679)
dyjetstollM50_2017.add_dataset('ntupleulsed3p5ndxyv29lepm', '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/pekotamn-NtupleULsed3p5ndxyV29Lepm_2017-81a17641caace8b37c665640348a6ff9/USER', 59535)
ww_2017.add_dataset('ntupleulsed3p5ndxyv29lepm', '/WW_TuneCP5_13TeV-pythia8/pekotamn-NtupleULsed3p5ndxyV29Lepm_2017-60940362bb8260ca35dfae6825136745/USER', 6337)
zz_2017.add_dataset('ntupleulsed3p5ndxyv29lepm', '/WZ_TuneCP5_13TeV-pythia8/pekotamn-NtupleULsed3p5ndxyV29Lepm_2017-aa8dcce95d3d8234a6bf3d71c01aa736/USER', 5390)
wz_2017.add_dataset('ntupleulsed3p5ndxyv29lepm', '/ZZ_TuneCP5_13TeV-pythia8/pekotamn-NtupleULsed3p5ndxyV29Lepm_2017-67f0292abeba0c8cd126b7fbab4b8b2a/USER', 2124)
WplusHToSSTodddd_tau30mm_M55_2017.add_dataset('ntupleulsed3p5ndxyv29lepm', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-30_TuneCP5_13TeV-powheg-pythia8/pekotamn-NtupleULsed3p5ndxyV29Lepm_2017-f94e1c897d9bbdb12e772e851d8f1ce1/USER', 47998)
WplusHToSSTodddd_tau300um_M55_2017.add_dataset('ntupleulsed3p5ndxyv29lepm', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/pekotamn-NtupleULsed3p5ndxyV29Lepm_2017-63b96c87dbc20b8daa7772b4e526b759/USER', 49995)
ttbar_2017.add_dataset("ntupleulsed3p5ndxyv29lepm")
"""


qcdempt015_2017.add_dataset('ntupleultrkattchsed4ndxyv29lepm', '/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/pekotamn-NtupleULtrkattchsed4ndxyV29Lepm_2017-58ba8a86a6bb63d8598b4af43b1ed7fb/USER', 0)
qcdmupt15_2017.add_dataset('ntupleultrkattchsed4ndxyv29lepm', '/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/pekotamn-NtupleULtrkattchsed4ndxyV29Lepm_2017-7f211c4ee8bd7f343519c61ef8d74e5a/USER', 1751)
qcdempt020_2017.add_dataset('ntupleultrkattchsed4ndxyv29lepm', '/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/pekotamn-NtupleULtrkattchsed4ndxyV29Lepm_2017-15df197918412bdf5976e17f9c4d96e0/USER', 0)
qcdempt030_2017.add_dataset('ntupleultrkattchsed4ndxyv29lepm', '/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/pekotamn-NtupleULtrkattchsed4ndxyV29Lepm_2017-be974e3d723b4435aa3728f1387ffac0/USER', 2)
qcdempt050_2017.add_dataset('ntupleultrkattchsed4ndxyv29lepm', '/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/pekotamn-NtupleULtrkattchsed4ndxyV29Lepm_2017-f110499c8255f57890c0adc759699712/USER', 8)
qcdempt080_2017.add_dataset('ntupleultrkattchsed4ndxyv29lepm', '/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/pekotamn-NtupleULtrkattchsed4ndxyV29Lepm_2017-1ea1295d014751ee06955883bca34ab5/USER', 26)
qcdempt120_2017.add_dataset('ntupleultrkattchsed4ndxyv29lepm', '/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/pekotamn-NtupleULtrkattchsed4ndxyV29Lepm_2017-2c7612c445fb2b516dd2808a939afadf/USER', 56)
qcdempt170_2017.add_dataset('ntupleultrkattchsed4ndxyv29lepm', '/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/pekotamn-NtupleULtrkattchsed4ndxyV29Lepm_2017-4b37b7dfa4c15e5e80ede2ffbfdca3b4/USER', 44)
qcdempt300_2017.add_dataset('ntupleultrkattchsed4ndxyv29lepm', '/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/pekotamn-NtupleULtrkattchsed4ndxyV29Lepm_2017-e262361355446d3bc672f6daf2b93dc6/USER', 56)
qcdbctoept020_2017.add_dataset('ntupleultrkattchsed4ndxyv29lepm', '/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/pekotamn-NtupleULtrkattchsed4ndxyV29Lepm_2017-727de6b267ec1c9d7bac3e5fd05a0c26/USER', 3)
qcdbctoept030_2017.add_dataset('ntupleultrkattchsed4ndxyv29lepm', '/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/pekotamn-NtupleULtrkattchsed4ndxyV29Lepm_2017-86c37048c252c76c02c24210d3ee7d9c/USER', 44)
qcdbctoept080_2017.add_dataset('ntupleultrkattchsed4ndxyv29lepm', '/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/pekotamn-NtupleULtrkattchsed4ndxyV29Lepm_2017-6bddb34a2f9945f51bb9add4585658b8/USER', 275)
qcdbctoept170_2017.add_dataset('ntupleultrkattchsed4ndxyv29lepm', '/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/pekotamn-NtupleULtrkattchsed4ndxyV29Lepm_2017-509be360daeacf0cc7db35a644572bb7/USER', 641)
qcdbctoept250_2017.add_dataset('ntupleultrkattchsed4ndxyv29lepm', '/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/pekotamn-NtupleULtrkattchsed4ndxyV29Lepm_2017-2fa0c85c32dd59f15a7283bc452451c3/USER', 701)
wjetstolnu_2017.add_dataset('ntupleultrkattchsed4ndxyv29lepm', '/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/pekotamn-NtupleULtrkattchsed4ndxyV29Lepm_2017-c1dc19bb51b8e9fe3a6edbda9cc1940b/USER', 33961)
dyjetstollM10_2017.add_dataset('ntupleultrkattchsed4ndxyv29lepm', '/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/pekotamn-NtupleULtrkattchsed4ndxyV29Lepm_2017-910d052c3a139a0fe334852d6fbefa50/USER', 1165)
dyjetstollM50_2017.add_dataset('ntupleultrkattchsed4ndxyv29lepm', '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/pekotamn-NtupleULtrkattchsed4ndxyV29Lepm_2017-3b633cd4b9b5590f7b24a06bd5aaab51/USER', 109685)
ww_2017.add_dataset('ntupleultrkattchsed4ndxyv29lepm', '/WW_TuneCP5_13TeV-pythia8/pekotamn-NtupleULtrkattchsed4ndxyV29Lepm_2017-18237a78fa4eaac93236c486c2df4f7a/USER', 11757)
zz_2017.add_dataset('ntupleultrkattchsed4ndxyv29lepm', '/WZ_TuneCP5_13TeV-pythia8/pekotamn-NtupleULtrkattchsed4ndxyV29Lepm_2017-dc6804ba932550fa7b015c517e9f8dc7/USER', 9384)
wz_2017.add_dataset('ntupleultrkattchsed4ndxyv29lepm', '/ZZ_TuneCP5_13TeV-pythia8/pekotamn-NtupleULtrkattchsed4ndxyV29Lepm_2017-22e0f1f8201a4ab70b156a5150df2fdc/USER', 3632)
WplusHToSSTodddd_tau30mm_M55_2017.add_dataset('ntupleultrkattchsed4ndxyv29lepm', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-30_TuneCP5_13TeV-powheg-pythia8/pekotamn-NtupleULtrkattchsed4ndxyV29Lepm_2017-d5660e2e7360215ecec3ee565c038a39/USER', 47998)
WplusHToSSTodddd_tau300um_M55_2017.add_dataset('ntupleultrkattchsed4ndxyv29lepm', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/pekotamn-NtupleULtrkattchsed4ndxyV29Lepm_2017-df20246686dc98049ca0195541f4ab5a/USER', 49995)
ttbar_2017.add_dataset("ntupleultrkattchsed4ndxyv29lepm")


"""
mfv_stoplb_tau010000um_M0400_2017.add_dataset('ntupleulsed4ndxyv29lepm', '/DisplacedSUSY_stopToLBottom_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/pekotamn-NtupleULsed4ndxyV29Lepm_2017-bd2d827c377ae0b408e0b17bd28e9f50/USER', 198737)
mfv_stoplb_tau001000um_M0400_2017.add_dataset('ntupleulsed4ndxyv29lepm', '/DisplacedSUSY_stopToLBottom_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/pekotamn-NtupleULsed4ndxyV29Lepm_2017-68b718cd1319e9d08a8044af8a240265/USER', 197003)
mfv_stopld_tau010000um_M0400_2017.add_dataset('ntupleulsed4ndxyv29lepm', '/DisplacedSUSY_stopToLD_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/pekotamn-NtupleULsed4ndxyV29Lepm_2017-fda48751a879e21411c097b192fee218/USER', 201845)
mfv_stopld_tau001000um_M0400_2017.add_dataset('ntupleulsed4ndxyv29lepm', '/DisplacedSUSY_stopToLD_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/pekotamn-NtupleULsed4ndxyV29Lepm_2017-7e88484fbf085347b1950fac0dd90c31/USER', 197130)
ZHToSSTodddd_tau300um_M55_2017.add_dataset('ntupleulsed4ndxyv29lepm', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-55_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/pekotamn-NtupleULsed4ndxyV29Lepm_2017-be31559dfcab8ff18a43a5ce9ebc8ee7/USER', 49997)
WplusHToSSTodddd_tau30mm_M55_2017.add_dataset('ntupleulsed4ndxyv29lepm', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-30_TuneCP5_13TeV-powheg-pythia8/pekotamn-NtupleULsed4ndxyV29Lepm_2017-9d2279ab7bd9a5ed0f19321f91283f99/USER', 47998)
WplusHToSSTodddd_tau1mm_M55_2017.add_dataset('ntupleulsed4ndxyv29lepm', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/pekotamn-NtupleULsed4ndxyV29Lepm_2017-579b54aa4f9391b684b3be11029d372b/USER', 49991)
WplusHToSSTodddd_tau300um_M55_2017.add_dataset('ntupleulsed4ndxyv29lepm', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/pekotamn-NtupleULsed4ndxyV29Lepm_2017-49576bc770db30a3be64a77727747c42/USER', 49995)
"""

"""
qcdempt015_2017.add_dataset('ntupleulsed2ndxyv29lepm', '/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/pekotamn-NtupleULsed2ndxyV29Lepm_2017-42dd711bd9fe3b1460cf6f4c6e066848/USER', 1)
qcdmupt15_2017.add_dataset('ntupleulsed2ndxyv29lepm', '/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/pekotamn-NtupleULsed2ndxyV29Lepm_2017-e7e892c5f8fd218be2e64e5a88da69f0/USER', 4029)
qcdempt020_2017.add_dataset('ntupleulsed2ndxyv29lepm', '/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/pekotamn-NtupleULsed2ndxyV29Lepm_2017-070019812a7db99e31c570899dae94d7/USER', 0)
qcdempt030_2017.add_dataset('ntupleulsed2ndxyv29lepm', '/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/pekotamn-NtupleULsed2ndxyV29Lepm_2017-5b0d9a458137d5e3c9909cea394543ce/USER', 11)
qcdempt050_2017.add_dataset('ntupleulsed2ndxyv29lepm', '/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/pekotamn-NtupleULsed2ndxyV29Lepm_2017-6bfef1c7f896b2f90bdf7e4784b2816a/USER', 42)
qcdempt080_2017.add_dataset('ntupleulsed2ndxyv29lepm', '/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/pekotamn-NtupleULsed2ndxyV29Lepm_2017-37e10cb976664cd4cae53875710829bf/USER', 99)
qcdempt120_2017.add_dataset('ntupleulsed2ndxyv29lepm', '/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/pekotamn-NtupleULsed2ndxyV29Lepm_2017-d1fdeefe3bc0816d86cb09ad3a9d51a6/USER', 244)
qcdempt170_2017.add_dataset('ntupleulsed2ndxyv29lepm', '/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/pekotamn-NtupleULsed2ndxyV29Lepm_2017-5e044ce07b3a15bb8937e42f8b8d4801/USER', 221)
qcdempt300_2017.add_dataset('ntupleulsed2ndxyv29lepm', '/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/pekotamn-NtupleULsed2ndxyV29Lepm_2017-e7ca5929fdfbd8876d8946534bfd738d/USER', 378)
qcdbctoept020_2017.add_dataset('ntupleulsed2ndxyv29lepm', '/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/pekotamn-NtupleULsed2ndxyV29Lepm_2017-c12955a592cf5ba98f94a9684b2b76a5/USER', 4)
qcdbctoept030_2017.add_dataset('ntupleulsed2ndxyv29lepm', '/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/pekotamn-NtupleULsed2ndxyV29Lepm_2017-c800fed30323c9a7273ab06ae9f7748a/USER', 108)
qcdbctoept080_2017.add_dataset('ntupleulsed2ndxyv29lepm', '/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/pekotamn-NtupleULsed2ndxyV29Lepm_2017-f6f85af1077e1550b59d65db3c6b78ca/USER', 600)
qcdbctoept170_2017.add_dataset('ntupleulsed2ndxyv29lepm', '/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/pekotamn-NtupleULsed2ndxyV29Lepm_2017-3ec3b741658a57def909dbfb66a20c8a/USER', 1444)
qcdbctoept250_2017.add_dataset('ntupleulsed2ndxyv29lepm', '/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/pekotamn-NtupleULsed2ndxyV29Lepm_2017-c08b0bc07c4c41acb05d92902eb07903/USER', 2049)
wjetstolnu_2017.add_dataset('ntupleulsed2ndxyv29lepm', '/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/pekotamn-NtupleULsed2ndxyV29Lepm_2017-938222dc29a3350481eb7c21e7f22374/USER', 282369)
dyjetstollM10_2017.add_dataset('ntupleulsed2ndxyv29lepm', '/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/pekotamn-NtupleULsed2ndxyV29Lepm_2017-9ce55f7181152366fd4f714d556dc9a2/USER', 6901)
dyjetstollM50_2017.add_dataset('ntupleulsed2ndxyv29lepm', '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/pekotamn-NtupleULsed2ndxyV29Lepm_2017-61a66d1792fb792f292394f9f4197868/USER', 775071)
ww_2017.add_dataset('ntupleulsed2ndxyv29lepm', '/WW_TuneCP5_13TeV-pythia8/pekotamn-NtupleULsed2ndxyV29Lepm_2017-8fb4079df7b45a5cb6138c51f9501e38/USER', 81569)
zz_2017.add_dataset('ntupleulsed2ndxyv29lepm', '/WZ_TuneCP5_13TeV-pythia8/pekotamn-NtupleULsed2ndxyV29Lepm_2017-60fc61ec1d036dce60a1ecfb1f03bc9e/USER', 37322)
wz_2017.add_dataset('ntupleulsed2ndxyv29lepm', '/ZZ_TuneCP5_13TeV-pythia8/pekotamn-NtupleULsed2ndxyV29Lepm_2017-513e9ac4efd76d94574e408357be2846/USER', 11158)
mfv_stoplb_tau010000um_M0400_2017.add_dataset('ntupleulsed2ndxyv29lepm', '/DisplacedSUSY_stopToLBottom_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/pekotamn-NtupleULsed2ndxyV29Lepm_2017-3c9d977de98026e27de906209e7e379e/USER', 198737)
mfv_stoplb_tau001000um_M0400_2017.add_dataset('ntupleulsed2ndxyv29lepm', '/DisplacedSUSY_stopToLBottom_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/pekotamn-NtupleULsed2ndxyV29Lepm_2017-90d8291fa694cdef891f0828131e1369/USER', 197003)
mfv_stopld_tau010000um_M0400_2017.add_dataset('ntupleulsed2ndxyv29lepm', '/DisplacedSUSY_stopToLD_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/pekotamn-NtupleULsed2ndxyV29Lepm_2017-46de699dad3742c49f9eddb2f061cdf7/USER', 201845)
mfv_stopld_tau001000um_M0400_2017.add_dataset('ntupleulsed2ndxyv29lepm', '/DisplacedSUSY_stopToLD_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/pekotamn-NtupleULsed2ndxyV29Lepm_2017-f453abafeed4069c154919791ea262c7/USER', 17946)
ZHToSSTodddd_tau300um_M55_2017.add_dataset('ntupleulsed2ndxyv29lepm', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-55_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/pekotamn-NtupleULsed2ndxyV29Lepm_2017-09d4aa78034e733b8bd390533e81b30a/USER', 49997)
WplusHToSSTodddd_tau30mm_M55_2017.add_dataset('ntupleulsed2ndxyv29lepm', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-30_TuneCP5_13TeV-powheg-pythia8/pekotamn-NtupleULsed2ndxyV29Lepm_2017-ee45da75d7866f6418c53acce016c638/USER', 47998)
WplusHToSSTodddd_tau1mm_M55_2017.add_dataset('ntupleulsed2ndxyv29lepm', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/pekotamn-NtupleULsed2ndxyV29Lepm_2017-1ea75a506c8d2d1e690db79eb01e9fee/USER', 49991)
WplusHToSSTodddd_tau300um_M55_2017.add_dataset('ntupleulsed2ndxyv29lepm', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/pekotamn-NtupleULsed2ndxyV29Lepm_2017-906c7d799c3078cf41141a4a1ed49a6c/USER', 7999)
WminusHToSSTodddd_tau300um_M55_2017.add_dataset('ntupleulsed2ndxyv29lepm', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/pekotamn-NtupleULsed2ndxyV29Lepm_2017-fcb910e1e77689158ecc5a5c8d45b2e2/USER', 47995)
ttbar_2017.add_dataset("ntupleulsed2ndxyv29lepm")
"""

"""
qcdempt015_2017.add_dataset('ntupleulv27lepm', '/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/pekotamn-NtupleULV27Lepm_2017-4c2a604bd321f6876c3e102761681e76/USER', 0)
qcdmupt15_2017.add_dataset('ntupleulv27lepm', '/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/pekotamn-NtupleULV27Lepm_2017-f65708f06d0960f464130983228b4488/USER', 941)
qcdempt020_2017.add_dataset('ntupleulv27lepm', '/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/pekotamn-NtupleULV27Lepm_2017-9a13e9e92cea8f7544c798796cda168a/USER', 0)
qcdempt030_2017.add_dataset('ntupleulv27lepm', '/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/pekotamn-NtupleULV27Lepm_2017-b1b85860b4e104cf1f9159dfdc8ec870/USER', 1)
qcdempt050_2017.add_dataset('ntupleulv27lepm', '/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/pekotamn-NtupleULV27Lepm_2017-c491d2265f86be9da4f8c669f3b7c522/USER', 2)
qcdempt080_2017.add_dataset('ntupleulv27lepm', '/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/pekotamn-NtupleULV27Lepm_2017-b07a2215c7f331f520c0d71ce2fcb7d1/USER', 15)
qcdempt120_2017.add_dataset('ntupleulv27lepm', '/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/pekotamn-NtupleULV27Lepm_2017-f9c40a47ea2f410e07d9204d32922be6/USER', 27)
qcdempt170_2017.add_dataset('ntupleulv27lepm', '/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/pekotamn-NtupleULV27Lepm_2017-49567a698d75a54388390d58f7b5d56c/USER', 21)
qcdempt300_2017.add_dataset('ntupleulv27lepm', '/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/pekotamn-NtupleULV27Lepm_2017-952a0ab6c0b8abe17d6051799154fc9f/USER', 27)
qcdbctoept020_2017.add_dataset('ntupleulv27lepm', '/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/pekotamn-NtupleULV27Lepm_2017-60c161cd7cc83fe4e61384c109cf92ca/USER', 3)
qcdbctoept030_2017.add_dataset('ntupleulv27lepm', '/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/pekotamn-NtupleULV27Lepm_2017-a3d10073d3c78e7bb9cd02cf6b630bfd/USER', 17)
qcdbctoept080_2017.add_dataset('ntupleulv27lepm', '/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/pekotamn-NtupleULV27Lepm_2017-9ac15194a17b90dcb46b6e089a47653b/USER', 138)
qcdbctoept170_2017.add_dataset('ntupleulv27lepm', '/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/pekotamn-NtupleULV27Lepm_2017-ff507612238ed36ae57cafe46962e226/USER', 290)
qcdbctoept250_2017.add_dataset('ntupleulv27lepm', '/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/pekotamn-NtupleULV27Lepm_2017-913b63ffda528158d69c45e9b3f27bb3/USER', 333)
wjetstolnu_2017.add_dataset('ntupleulv27lepm', '/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/pekotamn-NtupleULV27Lepm_2017-5526f662e9779122da3bd56353aa5ed2/USER', 14033)
dyjetstollM10_2017.add_dataset('ntupleulv27lepm', '/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/pekotamn-NtupleULV27Lepm_2017-c4569eb980ec46f826539af8ee319b8e/USER', 571)
dyjetstollM50_2017.add_dataset('ntupleulv27lepm', '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/pekotamn-NtupleULV27Lepm_2017-fdd1a37f92d2f150cc35de7e5ab5d1e4/USER', 48927)
ww_2017.add_dataset('ntupleulv27lepm', '/WW_TuneCP5_13TeV-pythia8/pekotamn-NtupleULV27Lepm_2017-ad6c60aecd1beba61f29ddfa4e69b52f/USER', 5180)
zz_2017.add_dataset('ntupleulv27lepm', '/WZ_TuneCP5_13TeV-pythia8/pekotamn-NtupleULV27Lepm_2017-f857a1e39831de7d5375d43a82c26697/USER', 4647)
wz_2017.add_dataset('ntupleulv27lepm', '/ZZ_TuneCP5_13TeV-pythia8/pekotamn-NtupleULV27Lepm_2017-62374ab982d76725dc5ee67dda5ae3d9/USER', 1831)
ZHToSSTodddd_tau1mm_M55_2017.add_dataset('ntupleulv27lepm', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/pekotamn-NtupleULV27Lepm_2017-c496424b354f77455b5e052ac02fef34/USER', 49997)
WplusHToSSTodddd_tau1mm_M55_2017.add_dataset('ntupleulv27lepm', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/pekotamn-NtupleULV27Lepm_2017-3c988531a091bca812ef3c0c9f7aaf6d/USER', -1)
WminusHToSSTodddd_tau1mm_M55_2017.add_dataset('ntupleulv27lepm', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/pekotamn-NtupleULV27Lepm_2017-7ffa2c418f3d8ede21086c363111fbb3/USER', 49995)
ttbar_2017.add_dataset("ntupleulv27lepm")
"""
"""
qcdempt015_2017.add_dataset('ntupleulv29lepm', '/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/pekotamn-NtupleULV29Lepm_2017-c9c414174e0ddcd96d3dd21f31d45215/USER', 0)
qcdmupt15_2017.add_dataset('ntupleulv29lepm', '/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/pekotamn-NtupleULV29Lepm_2017-0f202a4c683063a3800319fca11985b9/USER', 945)
qcdempt020_2017.add_dataset('ntupleulv29lepm', '/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/pekotamn-NtupleULV29Lepm_2017-8efe3e9cb0448e5ffe825e0449f794c4/USER', 0)
qcdempt030_2017.add_dataset('ntupleulv29lepm', '/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/pekotamn-NtupleULV29Lepm_2017-dab8339603de189650d5f63792a7e0ec/USER', 1)
qcdempt050_2017.add_dataset('ntupleulv29lepm', '/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/pekotamn-NtupleULV29Lepm_2017-341fa3bee5c49212fe2c0c51781be828/USER', 2)
qcdempt080_2017.add_dataset('ntupleulv29lepm', '/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/pekotamn-NtupleULV29Lepm_2017-93207cc54a2904c972ea0d98e896336c/USER', 15)
qcdempt120_2017.add_dataset('ntupleulv29lepm', '/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/pekotamn-NtupleULV29Lepm_2017-07f04f42fe4c7542ed01447b14f897f2/USER', 27)
qcdempt170_2017.add_dataset('ntupleulv29lepm', '/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/pekotamn-NtupleULV29Lepm_2017-b21350bf19c3292686c53f30b2c7e033/USER', 21)
qcdempt300_2017.add_dataset('ntupleulv29lepm', '/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/pekotamn-NtupleULV29Lepm_2017-4b96c199ec2fc25a13048a907647f9f7/USER', 29)
qcdbctoept020_2017.add_dataset('ntupleulv29lepm', '/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/pekotamn-NtupleULV29Lepm_2017-08ac89e8742d20dd1918c6bd7964205b/USER', 3)
qcdbctoept030_2017.add_dataset('ntupleulv29lepm', '/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/pekotamn-NtupleULV29Lepm_2017-32c09ae8d89f7e024eb18ac01af64b2e/USER', 17)
qcdbctoept080_2017.add_dataset('ntupleulv29lepm', '/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/pekotamn-NtupleULV29Lepm_2017-26c2f83ce3f220c22d352cc93dac5c0e/USER', 139)
qcdbctoept170_2017.add_dataset('ntupleulv29lepm', '/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/pekotamn-NtupleULV29Lepm_2017-fe4496287f6ad3ddc96edba358c3eead/USER', 293)
qcdbctoept250_2017.add_dataset('ntupleulv29lepm', '/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/pekotamn-NtupleULV29Lepm_2017-38ace47a53d0cf39e41d96e1f2dd1c8d/USER', 334)
wjetstolnu_2017.add_dataset('ntupleulv29lepm', '/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/pekotamn-NtupleULV29Lepm_2017-95be6ea6cba6991859c2ff9d20872bfb/USER', 13845)
dyjetstollM10_2017.add_dataset('ntupleulv29lepm', '/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/pekotamn-NtupleULV29Lepm_2017-d24c8911af27f255c2391cb41ad104aa/USER', 572)
dyjetstollM50_2017.add_dataset('ntupleulv29lepm', '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/pekotamn-NtupleULV29Lepm_2017-88721e0db7bbeb697d1c8b4aaa0f9ec7/USER', 49052)
ww_2017.add_dataset('ntupleulv29lepm', '/WW_TuneCP5_13TeV-pythia8/pekotamn-NtupleULV29Lepm_2017-a1a3a24b72778ce1b77dbdeea2d0bce1/USER', 5197)
zz_2017.add_dataset('ntupleulv29lepm', '/WZ_TuneCP5_13TeV-pythia8/pekotamn-NtupleULV29Lepm_2017-6f38a4b73e65478c501edcfc6e10de61/USER', 4663)
wz_2017.add_dataset('ntupleulv29lepm', '/ZZ_TuneCP5_13TeV-pythia8/pekotamn-NtupleULV29Lepm_2017-0c55fa3ece8fc8c106549e4ad6547b7e/USER', 1842)

ZHToSSTodddd_tau1mm_M55_2017.add_dataset('ntupleulv29lepm', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/pekotamn-NtupleULV29Lepm_2017-1cb59748d5a820293596a5f187b235f7/USER', 49997)
WplusHToSSTodddd_tau1mm_M55_2017.add_dataset('ntupleulv29lepm', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/pekotamn-NtupleULV29Lepm_2017-f1c3d1cf39d3f1a227d59ae477ab709a/USER', 49991)
WminusHToSSTodddd_tau1mm_M55_2017.add_dataset('ntupleulv29lepm', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/pekotamn-NtupleULV29Lepm_2017-7e420633fcddb0463b053b088b1100c7/USER', 48995)

ttbar_2017.add_dataset("ntupleulv29lepm")
"""

#ZHToSSTodddd_tau1mm_M55_2017.add_dataset('ntupleulv28lepm', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/pekotamn-NtupleULV28Lepm_2017-6c89113d805617ceb4dad495467603ec/USER', 48266)
#WplusHToSSTodddd_tau1mm_M55_2017.add_dataset('ntupleulv28lepm', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/pekotamn-NtupleULV28Lepm_2017-d0c0d37f2cf2b2bb1351c2470019417b/USER', 49991)
#WminusHToSSTodddd_tau1mm_M55_2017.add_dataset('ntupleulv28lepm', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/pekotamn-NtupleULV28Lepm_2017-56e10dbcaac7c8a5b1aa9e557b34b56e/USER', 3000)

# #for tracking tree : cut 0
# for x in ttbar_2017:
#     x.add_dataset("trackingtreerulv1_lepm_cut0")
for x in qcdempt015_2017, qcdmupt15_2017, qcdempt020_2017, qcdempt030_2017, qcdempt050_2017, qcdempt080_2017, qcdempt120_2017, qcdempt170_2017, qcdempt300_2017, qcdbctoept020_2017, qcdbctoept030_2017, qcdbctoept080_2017, qcdbctoept170_2017, qcdbctoept250_2017, wjetstolnu_2017, dyjetstollM10_2017, dyjetstollM50_2017, ttbar_2017, ww_2017, zz_2017, wz_2017, SingleMuon2017B, SingleMuon2017C, SingleMuon2017D, SingleMuon2017E, SingleMuon2017F, SingleElectron2017B, SingleElectron2017C, SingleElectron2017D, SingleElectron2017E, SingleElectron2017F:
    x.add_dataset("trackingtreerulv1_lepm_cut0")

#For tracking tree : cut 0
# including info on leptons and lepton tracks
for x in wjetstolnu_2017, dyjetstollM10_2017, dyjetstollM50_2017, SingleMuon2017B, SingleMuon2017C, SingleMuon2017D, SingleMuon2017E, SingleMuon2017F, SingleElectron2017B, SingleElectron2017C, SingleElectron2017D, SingleElectron2017E, SingleElectron2017F:
    x.add_dataset("trackingtreerulv1_lepm_wlep")

# #including info on leptons (including lepton sel tracks & good lepton sel tracks 
# for x in wjetstolnu_2017, dyjetstollM10_2017, dyjetstollM50_2017, SingleMuon2017B, SingleMuon2017C, SingleMuon2017D, SingleMuon2017E, SingleMuon2017F, SingleElectron2017B, SingleElectron2017C, SingleElectron2017D, SingleElectron2017E, SingleElectron2017F:
#     x.add_dataset("trackingtreerulv1_lepm_wsellep")

#we now have run over everything : good lepton sel tracks + tracks matched to a good lepton
for x in qcdempt015_2017, qcdmupt15_2017, qcdempt020_2017, qcdempt030_2017, qcdempt050_2017, qcdempt080_2017, qcdempt120_2017, qcdempt170_2017, qcdempt300_2017, qcdbctoept020_2017, qcdbctoept030_2017, qcdbctoept080_2017, qcdbctoept170_2017, qcdbctoept250_2017, wjetstolnu_2017, dyjetstollM10_2017, dyjetstollM50_2017, ttbar_2017, ww_2017, zz_2017, wz_2017, SingleMuon2017B, SingleMuon2017C, SingleMuon2017D, SingleMuon2017E, SingleMuon2017F, SingleElectron2017B, SingleElectron2017C, SingleElectron2017D, SingleElectron2017E, SingleElectron2017F:
    x.add_dataset("trackingtreerulv1_lepm_wsellep")

#for tracking tree : cut 1
for x in wjetstolnu_2017, dyjetstollM10_2017, dyjetstollM50_2017:
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
wjetstolnu_2017.add_dataset('ntupleulv1lepm', '/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/awarden-NtupleULV1Lepm_2017-00b30f18371d0ceaccbb1b156e2fc35f/USER', 282)
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

#2018 --> now including all missdist info for leptons (both those that are and are not associated to sv) + min r for leptons 
qcdmupt15_2018.add_dataset('ntupleulv1lepm', '/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/awarden-NtupleULV1Lepm_2018-ce904f50a96ee1353085f39728ce7c5d/USER', 894)
qcdempt015_2018.add_dataset('ntupleulv1lepm', '/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV1Lepm_2018-cf3d481706cbebd15805ca69a6308eda/USER', 1)
qcdempt020_2018.add_dataset('ntupleulv1lepm', '/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV1Lepm_2018-10e3d87ebc5a5c5887674ecc88973913/USER', 0)
qcdempt030_2018.add_dataset('ntupleulv1lepm', '/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV1Lepm_2018-79f57ad3c45bdb3919bba61faba44785/USER', 1)
qcdempt050_2018.add_dataset('ntupleulv1lepm', '/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV1Lepm_2018-d7c9472666008da228beb559e9e4e994/USER', 6)
qcdempt080_2018.add_dataset('ntupleulv1lepm', '/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV1Lepm_2018-3287403b74ee7e84a483bf34e186b294/USER', 21)
qcdempt120_2018.add_dataset('ntupleulv1lepm', '/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV1Lepm_2018-5117256673ce80fbaf53d855894a6ad8/USER', 38)
qcdempt170_2018.add_dataset('ntupleulv1lepm', '/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV1Lepm_2018-ea35b5de51f77d3d42c8737191577c70/USER', 22)
qcdempt300_2018.add_dataset('ntupleulv1lepm', '/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV1Lepm_2018-9735d238632d1781458fc2d5bdb3255d/USER', 33)
qcdbctoept015_2018.add_dataset('ntupleulv1lepm', '/QCD_Pt_15to20_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV1Lepm_2018-a1c538c630d5cff0381fcc67586a20ce/USER', 0)
qcdbctoept020_2018.add_dataset('ntupleulv1lepm', '/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV1Lepm_2018-55f83e3d2d4dbe5217b043435f37c2b1/USER', 1)
qcdbctoept030_2018.add_dataset('ntupleulv1lepm', '/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV1Lepm_2018-700831359ac18ae56e1e7b4d6808ee44/USER', 37)
qcdbctoept080_2018.add_dataset('ntupleulv1lepm', '/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV1Lepm_2018-a55e7e6cb50b37d2da0da0db65a0dbfb/USER', 147)
qcdbctoept170_2018.add_dataset('ntupleulv1lepm', '/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV1Lepm_2018-9390b042af934dbb34ae78eaf808e62b/USER', 323)
qcdbctoept250_2018.add_dataset('ntupleulv1lepm', '/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV1Lepm_2018-80910997bf034e98e207c7b11330bbff/USER', 413)
dyjetstollM10_2018.add_dataset('ntupleulv1lepm', '/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/awarden-NtupleULV1Lepm_2018-6258b07ed42ffde5876c3ae92bc22598/USER', 640)
dyjetstollM50_2018.add_dataset('ntupleulv1lepm', '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/awarden-NtupleULV1Lepm_2018-7d8f939e90fc98361ac74515ec5f5df0/USER', 21368)
wjetstolnu_2018.add_dataset('ntupleulv1lepm', '/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/awarden-NtupleULV1Lepm_2018-cc3b5bd7402146471ef3131aa210b622/USER', 6939)
ww_2018.add_dataset('ntupleulv1lepm', '/WW_TuneCP5_13TeV-pythia8/awarden-NtupleULV1Lepm_2018-15f8cb53eee86459b37af5b5e5d76f4b/USER', 4459)
wz_2018.add_dataset('ntupleulv1lepm', '/WZ_TuneCP5_13TeV-pythia8/awarden-NtupleULV1Lepm_2018-ed85ffbc0a7913ed0e33f5840eaafcd4/USER', 3878)
zz_2018.add_dataset('ntupleulv1lepm', '/ZZ_TuneCP5_13TeV-pythia8/awarden-NtupleULV1Lepm_2018-f19c75fbeb90a615aa9eec4c7887f144/USER', 2225)
mfv_stoplb_tau000100um_M1000_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-b977022694a4993a33ebd97c273f2938/USER', 200069)
mfv_stoplb_tau000300um_M1000_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-1eb4c5be51cab8613a4385308d5107d0/USER', 196665)
mfv_stoplb_tau010000um_M1000_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-ce0c563bdd400ee1007b31eb85245440/USER', 99062)
mfv_stoplb_tau001000um_M1000_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-660d12339758fc7b5008656c1da9d86c/USER', 196748)
mfv_stoplb_tau030000um_M1000_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-b76e6b38c656080f4d9c7ea152adcd01/USER', 199216)
mfv_stoplb_tau000100um_M1200_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-6065524909118e47a104c2c629af67bf/USER', 197949)
mfv_stoplb_tau000300um_M1200_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-07877656a18c65187b1251e718595596/USER', 198241)
mfv_stoplb_tau010000um_M1200_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-e7e64fa50f0397b87e413f1d813b05d6/USER', 98201)
mfv_stoplb_tau001000um_M1200_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-ddcbdd05c150be991146c5dab710b969/USER', 199473)
mfv_stoplb_tau030000um_M1200_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-ce0fc5414d6af29b44bf3e605f3bbfdb/USER', 199458)
mfv_stoplb_tau000100um_M1400_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-b17d7518a4d37a86c2c65edd5fa24fb6/USER', 199272)
mfv_stoplb_tau000300um_M1400_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-8758cc62be52fbcda62d944a36f414b5/USER', 200098)
mfv_stoplb_tau010000um_M1400_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-81c0ba472c76cbf6fbed294369eb0038/USER', 99970)
mfv_stoplb_tau001000um_M1400_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-06fc084b50005ab5587de43bc442a486/USER', 200807)
mfv_stoplb_tau030000um_M1400_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-620306a48831a6d056698bc802f9197b/USER', 200816)
mfv_stoplb_tau000100um_M1600_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-ccd85c79df7fd4137edcb40ce4d9817a/USER', 199366)
mfv_stoplb_tau000300um_M1600_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-36e50bf8d68bfb2cf3d5081bbde0cffe/USER', 202756)
mfv_stoplb_tau010000um_M1600_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-7062209557b1575f30ea21fac07cf908/USER', 101586)
mfv_stoplb_tau001000um_M1600_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-96387629d06392de9d86dc0ec5371c03/USER', 98806)
mfv_stoplb_tau030000um_M1600_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-50ed7ed8730dab3df09ce18e48e2fe87/USER', 100560)
mfv_stoplb_tau000100um_M1800_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-7ccd5baea7c48c828d36a0c024dc5052/USER', 200523)
mfv_stoplb_tau000300um_M1800_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-f31be744870c6d0a6e48e828eb976edd/USER', 197916)
mfv_stoplb_tau010000um_M1800_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-08f74ba9df41605ecb0e6274a9bfcb6e/USER', 101211)
mfv_stoplb_tau001000um_M1800_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-0f3dcf98cbaca83544a42bda49133c5c/USER', 100171)
mfv_stoplb_tau030000um_M1800_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-f46208eb824e851f8f82d3ce756f2b9b/USER', 100346)
mfv_stoplb_tau000100um_M0200_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-a669cdf0a42a8aa2dd48cdee7c7fa4ac/USER', 198986)
mfv_stoplb_tau000300um_M0200_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-5154522e9405ad6212590c3ecb4d9196/USER', 199542)
mfv_stoplb_tau010000um_M0200_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-e30e821d97a7d0496aa5f410600fb78f/USER', 198147)
mfv_stoplb_tau001000um_M0200_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-29d97ccfab6427ade6c71a8434a3fe55/USER', 198269)
mfv_stoplb_tau030000um_M0200_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-1c19b9b4b915af238ae6afeb152db299/USER', 197780)
mfv_stoplb_tau000100um_M0300_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-2db10d97a8ea37062d90f032ade2b532/USER', 198372)
mfv_stoplb_tau000300um_M0300_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-50eb5dc30e3ba8ffd3db008ebe4dce9c/USER', 203023)
mfv_stoplb_tau010000um_M0300_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-4fe5e9c890278f25405f0e68cfccb30e/USER', 196154)
mfv_stoplb_tau030000um_M0300_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-3ae95909200d294e673ab704ab82ced1/USER', 196763)
mfv_stoplb_tau000100um_M0400_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-c8a44d9f8e6c5853261beb16dded4237/USER', 200505)
mfv_stoplb_tau000300um_M0400_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-fa6ad12d92d0f19af0850b31c58083f7/USER', 200842)
mfv_stoplb_tau010000um_M0400_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-dd69cce642a736c3e98ce2218f0f52ba/USER', 198963)
mfv_stoplb_tau030000um_M0400_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-2786f4441b398d369c623847a43684ca/USER', 198368)
mfv_stoplb_tau000100um_M0600_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-263fc0f91651dd382d03cb5943cd9cf8/USER', 198211)
mfv_stoplb_tau000300um_M0600_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-80160d8bf3a064601cd24fdb2297c136/USER', 199368)
mfv_stoplb_tau010000um_M0600_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-a016282cded9bfde6cd99ea7985f8951/USER', 197845)
mfv_stoplb_tau001000um_M0600_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-3c84e76c971bbd40cbb4a0095d329466/USER', 196032)
mfv_stoplb_tau030000um_M0600_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-b87e998f40c6e8ecc1c5ac6bed61fd2f/USER', 201533)
mfv_stoplb_tau000100um_M0800_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-c6cee29f7713cf2b41cb2088203b28dd/USER', 202319)
mfv_stoplb_tau000300um_M0800_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-536bf10a01b4d2304e86566e42c32e67/USER', 200738)
mfv_stoplb_tau010000um_M0800_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-5d45bce7625224432bf781d57b9b4c8a/USER', 99747)
mfv_stoplb_tau001000um_M0800_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-643144567e3ca7aa12996c21b67b94a6/USER', 202348)
mfv_stoplb_tau030000um_M0800_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLBottom_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-e353f9309848199a186055dd6e9c713c/USER', 199087)
mfv_stopld_tau000100um_M1000_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-4554c4891d79d8ab021d294a83b7c73a/USER', 197843)
mfv_stopld_tau000300um_M1000_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-202cce0acdf60ee39809d6b90a47f773/USER', 199006)
mfv_stopld_tau010000um_M1000_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-65499c407195f91ae6b421784eefd521/USER', 98581)
mfv_stopld_tau001000um_M1000_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-224d317b80de8a7d719764439e5263a2/USER', 196285)
mfv_stopld_tau030000um_M1000_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-626c98091d2e7b58e38436a56ceaa7d5/USER', 197592)
mfv_stopld_tau000100um_M1200_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-b9ddb00138dda1cd768aae32855b0dbc/USER', 195354)
mfv_stopld_tau000300um_M1200_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-a0bba25ecffce75348918cd5ffae4fd0/USER', 199435)
mfv_stopld_tau010000um_M1200_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-b04b155c466bf974815931a9d55b273c/USER', 96663)
mfv_stopld_tau001000um_M1200_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-08c612ac7cb0ed25bafb39eccc0fdc19/USER', 200103)
mfv_stopld_tau030000um_M1200_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-d1ad8e1329de31b2cdcba66f554f9220/USER', 200964)
mfv_stopld_tau000100um_M1400_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-eadfd504d2acf9a051da1dd6c7a810ac/USER', 200045)
mfv_stopld_tau000300um_M1400_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-c23e73ede9c7cebcc4ad7e645bc00131/USER', 202529)
mfv_stopld_tau010000um_M1400_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-cb75c84531a728cb7fea4a2131ad327e/USER', 100228)
mfv_stopld_tau001000um_M1400_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-c682b295846396755d7e3d50c7a5c0f1/USER', 196708)
mfv_stopld_tau030000um_M1400_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-c77d0bc5a0c7c085d0844871c9dedd6e/USER', 201992)
mfv_stopld_tau000100um_M1600_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-f51c2e061f25142fce54417b38c50a92/USER', 201300)
mfv_stopld_tau000300um_M1600_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-b59ac4804de384d35833c682d2123f12/USER', 197421)
mfv_stopld_tau010000um_M1600_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-f6280c79140f684777640cddc5eb24af/USER', 99387)
mfv_stopld_tau001000um_M1600_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-dba19137891beeea8d98569b90661103/USER', 100838)
mfv_stopld_tau030000um_M1600_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-fa7cb00fd69229cc5b610f5af9554b3a/USER', 97752)
mfv_stopld_tau000100um_M1800_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-98cb84451421e908516f71f37864b144/USER', 202746)
mfv_stopld_tau000300um_M1800_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-573ca3d15b9cecdfc006fabd552d770a/USER', 199924)
mfv_stopld_tau010000um_M1800_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-f9c6f7e1cf207e873911825ab57ff321/USER', 99400)
mfv_stopld_tau001000um_M1800_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-47afcf801829c27c9d14aa7b1a58579d/USER', 99515)
mfv_stopld_tau030000um_M1800_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-5222357e30d64fc8c4f9237b0faa1c1f/USER', 98449)
mfv_stopld_tau000100um_M0200_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-ca15a89e275b2775aa9c37ca5255fc0a/USER', 197970)
mfv_stopld_tau000300um_M0200_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-266a38928e83ba353b3468aebc26fee7/USER', 198800)
mfv_stopld_tau010000um_M0200_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-db74502d65a7912d219023833ef975a7/USER', 199856)
mfv_stopld_tau001000um_M0200_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-bc448daeea7f80f6d0090716bdc86727/USER', 200411)
mfv_stopld_tau030000um_M0200_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-6537a8266bfd901fb0bdb8fae3760898/USER', 202558)
mfv_stopld_tau000100um_M0300_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-b8ad17353bf96783955725a6dd5a1b14/USER', 196635)
mfv_stopld_tau000300um_M0300_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-114acb539d5a5fa96dde48a19227b12c/USER', 198796)
mfv_stopld_tau010000um_M0300_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-8556ae82482b2b49fd048bfb48ffa7ad/USER', 197769)
mfv_stopld_tau001000um_M0300_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-861bbea6d66a82951d33f784c4d38d21/USER', 200543)
mfv_stopld_tau030000um_M0300_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-eb374045c015a72c2334b555af405c3a/USER', 198495)
mfv_stopld_tau000100um_M0400_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-33caf269d6521ab963e0874368bd8e04/USER', 198574)
mfv_stopld_tau000300um_M0400_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-a6fe2d511cc6086e026e2fb52d7fab4f/USER', 197079)
mfv_stopld_tau010000um_M0400_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-619182765b9b81e8b4b989a937b3e808/USER', 198270)
mfv_stopld_tau001000um_M0400_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-07c77cd6295e9a2c582152442bdb2c59/USER', 200098)
mfv_stopld_tau030000um_M0400_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-f23e5584ce48587f04e8d8ca5174da9c/USER', 203160)
mfv_stopld_tau000100um_M0600_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-3876a7421ab11510008c8c5f7e1888fb/USER', 198964)
mfv_stopld_tau000300um_M0600_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-8dee928b875b74640f0499ece6bd49f3/USER', 198408)
mfv_stopld_tau010000um_M0600_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-b5abfe5c8d39c543f782dceb02f242b7/USER', 199355)
mfv_stopld_tau001000um_M0600_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-fdd339ef6f03949afbc150e97ffd97f2/USER', 199759)
mfv_stopld_tau030000um_M0600_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-e937704fa11ed85fd5c0204011f33796/USER', 200030)
mfv_stopld_tau000100um_M0800_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-038de9d140dfb5f7fe1767ea4a7a7f27/USER', 195939)
mfv_stopld_tau000300um_M0800_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-c29704470cd81f43d310a87a9385def0/USER', 202036)
mfv_stopld_tau010000um_M0800_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-0e9f55a24ce53bf3cb5e7b16627b9409/USER', 100507)
mfv_stopld_tau001000um_M0800_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-af53939a3c03291ffa222cf700f275e0/USER', 199217)
mfv_stopld_tau030000um_M0800_2018.add_dataset('ntupleulv1lepm', '/DisplacedSUSY_stopToLD_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV1Lepm_2018-e36bd8d0a47f1a737bd8a78f6d25db54/USER', 196145)
ttbar_2018.add_dataset("ntupleulv1lepm")

##splitting lepton tracks and have relaxed seed track requirements for leptons >-= 20 GeV 
qcdmupt15_2018.add_dataset('ntupleulv2lepm', '/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/awarden-NtupleULV2Lepm_2018-ed138a8761363725585a9afc85b9be9c/USER', 918)
qcdempt015_2018.add_dataset('ntupleulv2lepm', '/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV2Lepm_2018-6c5e87618e2443c64778cee87ef43894/USER', 1)
qcdempt020_2018.add_dataset('ntupleulv2lepm', '/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV2Lepm_2018-ae041029aa89329fb6a421aef3da5de6/USER', 0)
qcdempt030_2018.add_dataset('ntupleulv2lepm', '/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV2Lepm_2018-818eb8cbef5de5785f675e2347928ecd/USER', 1)
qcdempt050_2018.add_dataset('ntupleulv2lepm', '/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV2Lepm_2018-f54858e0d30c4d201ff63e40fb951ca2/USER', 6)
qcdempt080_2018.add_dataset('ntupleulv2lepm', '/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV2Lepm_2018-5cd58a6824b96f263b9b108dabaeb067/USER', 20)
qcdempt120_2018.add_dataset('ntupleulv2lepm', '/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV2Lepm_2018-4f750e42e4b746ad5cab7fb955b1462c/USER', 36)
qcdempt170_2018.add_dataset('ntupleulv2lepm', '/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV2Lepm_2018-fdc46fb79e05587dedf663e92d9046db/USER', 19)
qcdempt300_2018.add_dataset('ntupleulv2lepm', '/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV2Lepm_2018-feb37a8699ff4f1c6cf9648f19673549/USER', 34)
qcdbctoept015_2018.add_dataset('ntupleulv2lepm', '/QCD_Pt_15to20_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV2Lepm_2018-5cc1d6af2c29b64ce89d4b2a27d95dee/USER', 0)
qcdbctoept020_2018.add_dataset('ntupleulv2lepm', '/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV2Lepm_2018-2bb04987c1e15504317116ddc15462c0/USER', 1)
qcdbctoept030_2018.add_dataset('ntupleulv2lepm', '/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV2Lepm_2018-ca173b30e7e3eb0a938775c424b19d7c/USER', 37)
qcdbctoept080_2018.add_dataset('ntupleulv2lepm', '/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV2Lepm_2018-c33a8662703a7dc62003b9268ca68739/USER', 150)
qcdbctoept170_2018.add_dataset('ntupleulv2lepm', '/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV2Lepm_2018-6486af5b2579d6f4342421679854b361/USER', 330)
qcdbctoept250_2018.add_dataset('ntupleulv2lepm', '/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV2Lepm_2018-6312b7cfbbbeac63039319c751a002c0/USER', 414)
wjetstolnu_2018.add_dataset('ntupleulv2lepm', '/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/awarden-NtupleULV2Lepm_2018-ef463b3275b8a927c4855589eb437e0a/USER', 6843)
dyjetstollM10_2018.add_dataset('ntupleulv2lepm', '/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/awarden-NtupleULV2Lepm_2018-878fe2fa4e90e031942258e672f69fdb/USER', 633)
dyjetstollM50_2018.add_dataset('ntupleulv2lepm', '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/awarden-NtupleULV2Lepm_2018-52a772c3f0d338cc327bce6972aeb44b/USER', 24891)
ww_2018.add_dataset('ntupleulv2lepm', '/WW_TuneCP5_13TeV-pythia8/awarden-NtupleULV2Lepm_2018-9612cd8d605cbbf73dda1a017ccb54f3/USER', 4195)
wz_2018.add_dataset('ntupleulv2lepm', '/WZ_TuneCP5_13TeV-pythia8/awarden-NtupleULV2Lepm_2018-16054619ae0508b20185abd2ee1e0912/USER', 4450)
zz_2018.add_dataset('ntupleulv2lepm', '/ZZ_TuneCP5_13TeV-pythia8/awarden-NtupleULV2Lepm_2018-47f5d8c80bf27071575129aa4e64090d/USER', 2240)
mfv_stoplb_tau000100um_M1000_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLBottom_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-2b9eb2e5126a8c21970545d0bc4756ab/USER', 202114)
mfv_stoplb_tau000300um_M1000_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLBottom_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-82c8f79565dcafc36fc60a542264324c/USER', 196665)
mfv_stoplb_tau010000um_M1000_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLBottom_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-7ac66b8c625549bd384ef879f7111205/USER', 99062)
mfv_stoplb_tau001000um_M1000_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLBottom_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-a2c75803c401b47d59113b4177da36fd/USER', 196748)
mfv_stoplb_tau030000um_M1000_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLBottom_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-b3e06c3ebb0dd619de34a088949947d0/USER', 199216)
mfv_stoplb_tau000100um_M1200_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLBottom_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-1d34ebbe0fb4e7b90583c1a06254bcbd/USER', 197949)
mfv_stoplb_tau000300um_M1200_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLBottom_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-eed03d9e75a96db18b5d1d8f8436357c/USER', 198241)
mfv_stoplb_tau010000um_M1200_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLBottom_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-4fa783920b238fe8941504124ca0c51e/USER', 98201)
mfv_stoplb_tau001000um_M1200_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLBottom_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-f5de2a3539e56ee5d21520d79ecf7cbf/USER', 199473)
mfv_stoplb_tau030000um_M1200_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLBottom_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-07e3f275fc5cb2ee396f615b7c4e278a/USER', 199458)
mfv_stoplb_tau000100um_M1400_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLBottom_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-66757c940a8d29e83280d4c26da3ea7c/USER', 199272)
mfv_stoplb_tau000300um_M1400_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLBottom_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-facceb5b12681d175d2e03845bd5b45c/USER', 198999)
mfv_stoplb_tau010000um_M1400_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLBottom_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-a2b361535124973bd8b76ee2e9b6d5be/USER', 99970)
mfv_stoplb_tau001000um_M1400_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLBottom_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-3d688f95b58732e0473c0c880a4ec488/USER', 200807)
mfv_stoplb_tau030000um_M1400_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLBottom_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-877cc17f835c22dfefbb144909873ae9/USER', 200816)
mfv_stoplb_tau000100um_M1600_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLBottom_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-f27e3416c05a3bb8023a7d15b4a71a57/USER', 199366)
mfv_stoplb_tau000300um_M1600_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLBottom_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-704ac348dc33a8e39cc9fb61269d0f1e/USER', 202756)
mfv_stoplb_tau010000um_M1600_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLBottom_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-8029e14b4096c984ce7174f07b4cbd81/USER', 101586)
mfv_stoplb_tau001000um_M1600_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLBottom_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-888dc8070902d615734ba00d81cac98e/USER', 99806)
mfv_stoplb_tau030000um_M1600_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLBottom_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-1570da7ace44bbcc3e7c5f0381adbb3f/USER', 100560)
mfv_stoplb_tau000100um_M1800_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLBottom_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-8b39c13e2c4ffb61b00675ebe6c50b06/USER', 200523)
mfv_stoplb_tau000300um_M1800_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLBottom_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-5d997a1356b227237d89e957995d3c53/USER', 199868)
mfv_stoplb_tau010000um_M1800_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLBottom_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-2446e9e76b6bf9e30937e6a1b9856ad7/USER', 101211)
mfv_stoplb_tau001000um_M1800_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLBottom_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-046e6921ae9c458dfb091f4222cd194c/USER', 100171)
mfv_stoplb_tau030000um_M1800_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLBottom_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-39ed65047e93769d208360220e23e7c1/USER', 100346)
mfv_stoplb_tau000100um_M0200_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLBottom_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-db5605691e9fb9101c17a8bcfb76a052/USER', 198986)
mfv_stoplb_tau000300um_M0200_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLBottom_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-291b1c956e7e67e31b428c783dcdf8e6/USER', 199542)
mfv_stoplb_tau010000um_M0200_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLBottom_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-f0fde517ce6ebca09d2b2ef5b666614a/USER', 198147)
mfv_stoplb_tau001000um_M0200_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLBottom_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-1f77dda6f4a68aa0ee512931df6dcaac/USER', 198269)
mfv_stoplb_tau030000um_M0200_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLBottom_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-221d3c45722d998600339c2d0f0a86d0/USER', 197780)
mfv_stoplb_tau000100um_M0300_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLBottom_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-463595ee270040e4d01bf3bde90f9355/USER', 198372)
mfv_stoplb_tau000300um_M0300_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLBottom_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-1283b60c72361f7e958db0ededb8b1c7/USER', 203023)
mfv_stoplb_tau010000um_M0300_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLBottom_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-5ca12bbc47dc1e36d94f9ecd347e05aa/USER', 195200)
mfv_stoplb_tau001000um_M0300_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLBottom_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-1a7f2cc7bd08a8257947d3c968a4dff2/USER', 197602)
mfv_stoplb_tau030000um_M0300_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLBottom_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-10ce1c408ab5641fb7f448cc49ad5d2b/USER', 196763)
mfv_stoplb_tau000100um_M0400_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLBottom_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-202a77488814641dc02151cd3d78f008/USER', 199520)
mfv_stoplb_tau000300um_M0400_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLBottom_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-f8d3c654657544e47462da9fc877aea0/USER', 200842)
mfv_stoplb_tau010000um_M0400_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLBottom_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-767f52270c0cd6c49a883b8d02cbe4f7/USER', 198963)
mfv_stoplb_tau001000um_M0400_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLBottom_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-39db064f04cd35fea4e3edcc9bdc2eed/USER', 199860)
mfv_stoplb_tau030000um_M0400_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLBottom_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-28d7137947c9e7391091b258dbae0454/USER', 198368)
mfv_stoplb_tau000100um_M0600_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLBottom_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-6aeb41feb877d4c1c47e89f6d3fda30c/USER', 198211)
mfv_stoplb_tau000300um_M0600_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLBottom_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-f0c3fb76a59e583b48d99e3a19278925/USER', 199368)
mfv_stoplb_tau010000um_M0600_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLBottom_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-e1b3be86a7b7297968ceca7e513fb587/USER', 197845)
mfv_stoplb_tau001000um_M0600_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLBottom_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-ab396dded7891ec180c5864bf65d4bda/USER', 196032)
mfv_stoplb_tau030000um_M0600_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLBottom_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-85201b96524768e3f8a77bcc4c1705b1/USER', 201533)
mfv_stoplb_tau000100um_M0800_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLBottom_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-971bbdb9f87d983742309ed3b1e4024a/USER', 202319)
mfv_stoplb_tau000300um_M0800_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLBottom_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-ada949f3534d0f2f4ba8035e9b0b510c/USER', 199758)
mfv_stoplb_tau010000um_M0800_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLBottom_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-47a2e131e17e713054e8cb3c3c97ea13/USER', 99747)
mfv_stoplb_tau001000um_M0800_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLBottom_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-982ebefc9e8d0c63a2c2676376206561/USER', 202348)
mfv_stoplb_tau030000um_M0800_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLBottom_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-7116b86f212dd5bd0e55d9abd022597d/USER', 199087)
mfv_stopld_tau000100um_M1000_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLD_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-07f1f1847a6267417a37bd1b5a28f540/USER', 197890)
mfv_stopld_tau000300um_M1000_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLD_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-e4e108196918d47e93aa0c8ff770af6b/USER', 199006)
mfv_stopld_tau010000um_M1000_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLD_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-72cd9d5b2eed60ed3a37c185d698f05b/USER', 98581)
mfv_stopld_tau001000um_M1000_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLD_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-601b0e86290b743bf0d2b36558b71268/USER', 196285)
mfv_stopld_tau030000um_M1000_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLD_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-aa1e65b7e67ffbd8dc000a9e4a4b7f82/USER', 197592)
mfv_stopld_tau000100um_M1200_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLD_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-2995b4b67d7915dde06faba3aef4c1b3/USER', 195354)
mfv_stopld_tau000300um_M1200_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLD_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-f7796442ac3da45f16be06b39a97f35e/USER', 199435)
mfv_stopld_tau010000um_M1200_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLD_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-c05ccc3c1651c67e5ee15c006543e55b/USER', 98617)
mfv_stopld_tau001000um_M1200_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLD_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-8349847fa60c0116cd6abcb68213c49a/USER', 200103)
mfv_stopld_tau030000um_M1200_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLD_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-c989e760e85ca1a36d08288dbf4e91f6/USER', 200964)
mfv_stopld_tau000100um_M1400_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLD_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-52dcd92872b788f370e3be78149e42e5/USER', 200045)
mfv_stopld_tau000300um_M1400_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLD_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-25f691726629600d52ab049acc18e863/USER', 202529)
mfv_stopld_tau010000um_M1400_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLD_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-8837278d3c6efe777e19d330ad099cba/USER', 99216)
mfv_stopld_tau001000um_M1400_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLD_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-4cb86fb562bc01a13e1cc49c327ae301/USER', 196708)
mfv_stopld_tau030000um_M1400_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLD_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-91e16271aa0101b1774840fe6d7e6054/USER', 201992)
mfv_stopld_tau000100um_M1600_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLD_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-6c3d04738c03dfb58944b9488f8303c3/USER', 201300)
mfv_stopld_tau000300um_M1600_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLD_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-31fad4ceba6e3902a8b53f8fb5ade08e/USER', 197421)
mfv_stopld_tau010000um_M1600_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLD_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-3594943174bff0b58fd7bddbf91b8bd5/USER', 99387)
mfv_stopld_tau001000um_M1600_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLD_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-731c52ea6caa05bfa47b1bab2e86c45e/USER', 100838)
mfv_stopld_tau030000um_M1600_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLD_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-56e816684c1eddab2e17dba622ddefcd/USER', 97752)
mfv_stopld_tau000100um_M1800_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLD_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-14aa22c9950f7908ac189c98a4f46891/USER', 202746)
mfv_stopld_tau000300um_M1800_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLD_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-546815d79da88db5b0696e72dd87b774/USER', 199924)
mfv_stopld_tau010000um_M1800_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLD_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-1ea9059531055dd146c4738d5e9e6696/USER', 99400)
mfv_stopld_tau001000um_M1800_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLD_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-5e2656924395edb968427c271bc8d316/USER', 99515)
mfv_stopld_tau030000um_M1800_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLD_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-0ac54771e057ab2449de694902cd60e6/USER', 98449)
mfv_stopld_tau000100um_M0200_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLD_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-03bd58dc7daeca7d0bb8080b4460fd54/USER', 197970)
mfv_stopld_tau000300um_M0200_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLD_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-8357d9858bd2ea5cab4c9763accbae84/USER', 198800)
mfv_stopld_tau010000um_M0200_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLD_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-98d7d2041cd76807569e48946811dff5/USER', 199856)
mfv_stopld_tau001000um_M0200_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLD_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-420f0711b890940d27c8debdad870a01/USER', 200411)
mfv_stopld_tau030000um_M0200_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLD_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-ef1ee1c8de8fa730ec203d88f77cfc81/USER', 202558)
mfv_stopld_tau000100um_M0300_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLD_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-65d2fbbcdad5fb8c725529d0cfc543a0/USER', 196635)
mfv_stopld_tau000300um_M0300_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLD_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-9ca922e6269b22e0b85fa1784b56bdfa/USER', 198796)
mfv_stopld_tau010000um_M0300_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLD_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-f21de08cdac25a7d593af20d615ced12/USER', 197769)
mfv_stopld_tau001000um_M0300_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLD_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-d8aa7094dfd5fc6ea4c018148d30f1f6/USER', 200543)
mfv_stopld_tau030000um_M0300_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLD_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-c9f8326a3e52e3f38385e8518d24584b/USER', 198495)
mfv_stopld_tau000100um_M0400_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLD_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-0252f788ffe154026dbf89eba8dce719/USER', 201643)
mfv_stopld_tau000300um_M0400_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLD_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-c900cdbdf0c36eb29ee1cf164a95cfd6/USER', 197079)
mfv_stopld_tau010000um_M0400_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLD_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-2d8da977305c24c1f135986e3de4a266/USER', 198270)
mfv_stopld_tau001000um_M0400_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLD_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-ae7bdb44843e21e323fc40d9c5baafef/USER', 200098)
mfv_stopld_tau030000um_M0400_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLD_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-984859cb3d16d850c35858a0f7f74b60/USER', 203160)
mfv_stopld_tau000100um_M0600_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLD_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-8e883f8e22e5fbc6525c73fb6869114a/USER', 198964)
mfv_stopld_tau000300um_M0600_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLD_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-62dcb3814e2f7a047209c30f2b3d02b1/USER', 198408)
mfv_stopld_tau010000um_M0600_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLD_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-efdb10c53797563d7f9062c1f704c948/USER', 200404)
mfv_stopld_tau001000um_M0600_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLD_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-c29e4c3727b5b08aeed252402b20b51d/USER', 199759)
mfv_stopld_tau030000um_M0600_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLD_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-7a935bfd54f1d811d5cb4b6221f2318a/USER', 200030)
mfv_stopld_tau000100um_M0800_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLD_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-dcf1d61b979b9f2da135263bfbb8211c/USER', 197872)
mfv_stopld_tau000300um_M0800_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLD_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-e224d149a2ef0d8f40f1805f38c8e7f5/USER', 202036)
mfv_stopld_tau010000um_M0800_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLD_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-55d09c73525961d6dd7ea20f3be31172/USER', 100507)
mfv_stopld_tau001000um_M0800_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLD_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-40ad64b09fbb5c51645bf5db0d7d6a7e/USER', 199217)
mfv_stopld_tau030000um_M0800_2018.add_dataset('ntupleulv2lepm', '/DisplacedSUSY_stopToLD_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV2Lepm_2018-2e55859909bd0e00d32b8cc8a17d346e/USER', 197136)
ttbar_2018.add_dataset("ntupleulv2lepm")

qcdmupt15_2018.add_dataset('ntupleulv5lepm', '/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/awarden-NtupleULV5Lepm_2018-9437843c58fac6a76b5d567bfe15b42a/USER', 1208)
qcdempt015_2018.add_dataset('ntupleulv5lepm', '/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV5Lepm_2018-5b5a27bf4c43dc50709197250a35b8ec/USER', 2)
qcdempt020_2018.add_dataset('ntupleulv5lepm', '/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV5Lepm_2018-a8b00ecee96ebe7a327d88bd995455be/USER', 0)
qcdempt030_2018.add_dataset('ntupleulv5lepm', '/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV5Lepm_2018-93874cf96a55cda5231ca13258fdc0d4/USER', 3)
qcdempt050_2018.add_dataset('ntupleulv5lepm', '/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV5Lepm_2018-4b58060f7f418eccaff78cc79f2033bb/USER', 5)
qcdempt080_2018.add_dataset('ntupleulv5lepm', '/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV5Lepm_2018-c7ee99415fa5dd450e4b9399534525e1/USER', 21)
qcdempt120_2018.add_dataset('ntupleulv5lepm', '/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV5Lepm_2018-0402730cd3a351e404f26fc5977b4899/USER', 41)
qcdempt170_2018.add_dataset('ntupleulv5lepm', '/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV5Lepm_2018-1a53e171d37ffdbe12d5586236049068/USER', 22)
qcdempt300_2018.add_dataset('ntupleulv5lepm', '/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV5Lepm_2018-a9cb0f9f11bf2e1eb26ec90b4fb10cdb/USER', 24)
qcdbctoept015_2018.add_dataset('ntupleulv5lepm', '/QCD_Pt_15to20_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV5Lepm_2018-a635f2ba3153fbed164df1759a6a1ad7/USER', 0)
qcdbctoept020_2018.add_dataset('ntupleulv5lepm', '/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV5Lepm_2018-b13404d8fc01e817f41506ee29d3c6ec/USER', 1)
qcdbctoept030_2018.add_dataset('ntupleulv5lepm', '/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV5Lepm_2018-bd00b078d1e102b8d2ba5683a144cf44/USER', 65)
qcdbctoept080_2018.add_dataset('ntupleulv5lepm', '/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV5Lepm_2018-baefacbb291ff9946904a587277a302b/USER', 199)
qcdbctoept170_2018.add_dataset('ntupleulv5lepm', '/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV5Lepm_2018-5840f61b79df560908dbf3eff1a2fab1/USER', 372)
qcdbctoept250_2018.add_dataset('ntupleulv5lepm', '/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV5Lepm_2018-bbabef2fc36eddaad65eeec12586858b/USER', 448)
wjetstolnu_2018.add_dataset('ntupleulv5lepm', '/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/awarden-NtupleULV5Lepm_2018-54e88eda4946f0cd85914815e67bb986/USER', 12491)
dyjetstollM10_2018.add_dataset('ntupleulv5lepm', '/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/awarden-NtupleULV5Lepm_2018-f632cccc11343b35ee91aeb84b8c4a49/USER', 873)
dyjetstollM50_2018.add_dataset('ntupleulv5lepm', '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/awarden-NtupleULV5Lepm_2018-6f81e07b2a0a8d64d1bc9218d819efae/USER', 42460)
ww_2018.add_dataset('ntupleulv5lepm', '/WW_TuneCP5_13TeV-pythia8/awarden-NtupleULV5Lepm_2018-902c15daa3d056fb63dccca64a6e4c6c/USER', 5076)
wz_2018.add_dataset('ntupleulv5lepm', '/WZ_TuneCP5_13TeV-pythia8/awarden-NtupleULV5Lepm_2018-1bbb86e3aaa952cfea374f994d806cc9/USER', 5209)
zz_2018.add_dataset('ntupleulv5lepm', '/ZZ_TuneCP5_13TeV-pythia8/awarden-NtupleULV5Lepm_2018-f5ede7096c1f8e11ada8ba0e5d75fdf8/USER', 2561)
mfv_stoplb_tau000100um_M1000_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLBottom_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-4e3ffa4a49fecea0650e9343593d7b75/USER', 202114)
mfv_stoplb_tau000300um_M1000_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLBottom_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-3cff870ad5483c55b3762b0fc4382e30/USER', 196665)
mfv_stoplb_tau010000um_M1000_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLBottom_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-bd81a5b6c8c746a44d35999bd492f8bc/USER', 83262)
mfv_stoplb_tau001000um_M1000_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLBottom_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-b9ee7791078d90b2a88cd8c9354028c8/USER', 194766)
mfv_stoplb_tau030000um_M1000_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLBottom_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-7971ee1f0fdaf2829369faf3507c22c0/USER', 196254)
mfv_stoplb_tau000100um_M1200_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLBottom_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-4a890b671f88e31adec7edcaca512c2b/USER', 197949)
mfv_stoplb_tau000300um_M1200_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLBottom_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-656f2c01c42dba3a57fca47b1645a0ed/USER', 198241)
mfv_stoplb_tau010000um_M1200_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLBottom_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-09b7f2ae9b2b33dff0b26b7df623ddf9/USER', 85269)
mfv_stoplb_tau001000um_M1200_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLBottom_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-24b8f172ecf9b9915f2876b035c131e5/USER', 199473)
mfv_stoplb_tau030000um_M1200_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLBottom_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-77a3478ed75d42c9c63a1e0a8bcd1218/USER', 169466)
mfv_stoplb_tau000100um_M1400_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLBottom_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-c7245f7807dc3055492c44e524b8369a/USER', 190336)
mfv_stoplb_tau000300um_M1400_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLBottom_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-4e3a8b6fa5255f160a1de281cc7a06da/USER', 200098)
mfv_stoplb_tau010000um_M1400_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLBottom_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-09d053fda71b82cbbfd41804ecd465fb/USER', 99970)
mfv_stoplb_tau001000um_M1400_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLBottom_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-2ead623d7f5e06bd795d16d9fd03e5fd/USER', 200807)
mfv_stoplb_tau030000um_M1400_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLBottom_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-0fe3306ddcd92eaef5baf1daa2f47345/USER', 191976)
mfv_stoplb_tau000100um_M1600_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLBottom_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-59e326e3f84cf256595b870f2dfdd2f9/USER', 199366)
mfv_stoplb_tau000300um_M1600_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLBottom_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-b6422be52dff84a3bdd91fee5361a63b/USER', 161012)
mfv_stoplb_tau010000um_M1600_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLBottom_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-b627a1b08db02dc2a5bc27ab6b31dbba/USER', 101586)
mfv_stoplb_tau001000um_M1600_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLBottom_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-2607da266e2be8a221f06600f0078a66/USER', 99806)
mfv_stoplb_tau030000um_M1600_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLBottom_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-72f245b5798c645a7a8fe30bfe1aa0ff/USER', 94498)
mfv_stoplb_tau000100um_M1800_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLBottom_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-ef5adc6be059c82b546f4db1f3cf8810/USER', 200523)
mfv_stoplb_tau000300um_M1800_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLBottom_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-410b406bb87f63c9fa298cb30c8e615a/USER', 199868)
mfv_stoplb_tau010000um_M1800_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLBottom_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-157628c01ed0c3a665f7c8cc96dff65b/USER', 101211)
mfv_stoplb_tau001000um_M1800_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLBottom_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-93ecae1e2bf00b00010d4e4c6926f9d3/USER', 90148)
mfv_stoplb_tau030000um_M1800_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLBottom_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-84b58fe98a1d3f6f7facdc543cf12f65/USER', 94383)
mfv_stoplb_tau000100um_M0200_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLBottom_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-76c056ffa32b68461315b98bc1accea6/USER', 188016)
mfv_stoplb_tau000300um_M0200_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLBottom_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-094a4ff0d75c79111a29240a43c30968/USER', 196529)
mfv_stoplb_tau010000um_M0200_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLBottom_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-249ad14e3e8d93e10c1a6ad5b22b2071/USER', 198147)
mfv_stoplb_tau001000um_M0200_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLBottom_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-5259045ccfcb7a7630f95d40775073e9/USER', 193325)
mfv_stoplb_tau030000um_M0200_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLBottom_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-f5a1abc8c5f71b128e812c00f9bfd133/USER', 197780)
mfv_stoplb_tau000100um_M0300_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLBottom_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-e98d6df3214ad676f74e1085f8a75591/USER', 182511)
mfv_stoplb_tau000300um_M0300_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLBottom_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-6e91e578c57f475dcd46a19d2394d24b/USER', 157476)
mfv_stoplb_tau010000um_M0300_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLBottom_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-735ab0767ad86c612414e7b1619323c8/USER', 189236)
mfv_stoplb_tau001000um_M0300_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLBottom_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-f925b5c9c038638a986e861deeb24042/USER', 197602)
mfv_stoplb_tau030000um_M0300_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLBottom_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-d1e723bc84ab95d4bb1d2205c89b6771/USER', 196763)
mfv_stoplb_tau000100um_M0400_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLBottom_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-1c1a12609a5718e40dac68c5726c9c2e/USER', 200505)
mfv_stoplb_tau000300um_M0400_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLBottom_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-c4b4a9aff0670987765bd381fe98a2a7/USER', 200842)
mfv_stoplb_tau010000um_M0400_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLBottom_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-66801825a8c0c49df8f91c773a4abe11/USER', 182081)
mfv_stoplb_tau001000um_M0400_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLBottom_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-35af45bbdbe2ec5be356b81c1e89b1ea/USER', 193835)
mfv_stoplb_tau030000um_M0400_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLBottom_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-1f7f7f8b0e7175c8b990c2be17d28fbf/USER', 185380)
mfv_stoplb_tau000100um_M0600_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLBottom_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-85cb1bba264bbe98b7e1ae0928dd07a5/USER', 195134)
mfv_stoplb_tau000300um_M0600_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLBottom_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-29d0d97ebfd72284ab4fec5204a8eca3/USER', 177329)
mfv_stoplb_tau010000um_M0600_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLBottom_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-570aa29323f076b61ab35c216bbbd5dc/USER', 197845)
mfv_stoplb_tau001000um_M0600_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLBottom_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-6246ea340ca3ef5bc0a2a1ca4b3a8777/USER', 196032)
mfv_stoplb_tau030000um_M0600_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLBottom_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-d020f13fc860717c049c9c86d4fbc454/USER', 201533)
mfv_stoplb_tau000100um_M0800_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLBottom_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-eab8313d2509151221a3c98151a8b140/USER', 186104)
mfv_stoplb_tau000300um_M0800_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLBottom_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-c78f2ad928abbb4048a86ce780063033/USER', 190748)
mfv_stoplb_tau010000um_M0800_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLBottom_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-939b904e017aedae37712a38af4601be/USER', 96623)
mfv_stoplb_tau001000um_M0800_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLBottom_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-a8a3b3e6b4b301d82b82ebd898448e6b/USER', 168137)
mfv_stoplb_tau030000um_M0800_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLBottom_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-5413eca9fd7aa1baeeeee4d56d5fe574/USER', 180997)
mfv_stopld_tau000100um_M1000_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLD_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-b0b20be9d702f9aaef05552c51d1b114/USER', 198858)
mfv_stopld_tau000300um_M1000_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLD_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-8a455592b4bee9e6d547d7d12f3fc95c/USER', 181939)
mfv_stopld_tau010000um_M1000_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLD_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-2d81155dd28ca1c011c0238b57e58fe2/USER', 98581)
mfv_stopld_tau001000um_M1000_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLD_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-84d0ab42ea117b2b978176c7cb1e7137/USER', 196285)
mfv_stopld_tau030000um_M1000_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLD_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-6f80326e715bc7de69371071bfc53465/USER', 174920)
mfv_stopld_tau000100um_M1200_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLD_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-8b663df5aaad3dbc0230996a565aa234/USER', 195354)
mfv_stopld_tau000300um_M1200_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLD_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-f33b69b7e2e6cfb265371d52912e20fb/USER', 194540)
mfv_stopld_tau010000um_M1200_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLD_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-f8b5abf29709e783707c2a6cfcf86779/USER', 96609)
mfv_stopld_tau001000um_M1200_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLD_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-72225d230fd146547291c5edab88bcb2/USER', 200103)
mfv_stopld_tau030000um_M1200_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLD_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-e4d7983e82b839f0f61376ddd07e2403/USER', 200964)
mfv_stopld_tau000100um_M1400_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLD_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-7d9b431dfcfda7771e56e90b8f1340f0/USER', 200045)
mfv_stopld_tau000300um_M1400_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLD_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-37e789d349e5753bb46e2db45d51b43a/USER', 202529)
mfv_stopld_tau010000um_M1400_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLD_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-eef5ec701bfea08fc188e9d65756f28f/USER', 100228)
mfv_stopld_tau001000um_M1400_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLD_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-8e8dc10230fab3c7ef7ab52ea99f320f/USER', 183846)
mfv_stopld_tau030000um_M1400_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLD_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-2d9206c0bb8c8b2055e15fc52c3da733/USER', 168530)
mfv_stopld_tau000100um_M1600_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLD_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-bc5e0683a48c3fdc5a41127f84e8aba5/USER', 183118)
mfv_stopld_tau000300um_M1600_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLD_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-b701fc2a1fd8616ed8fa902b95b943e1/USER', 197421)
mfv_stopld_tau010000um_M1600_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLD_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-688daaf85f2df7336428f1c9ef3bf6a1/USER', 99387)
mfv_stopld_tau001000um_M1600_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLD_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-55ea519cb170bab12f102b17d8459f8b/USER', 100838)
mfv_stopld_tau030000um_M1600_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLD_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-8e6449af9e3c2c12c40e323fa9d0d927/USER', 97752)
mfv_stopld_tau000100um_M1800_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLD_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-789a2374813414571a5e4f03143b44f5/USER', 202746)
mfv_stopld_tau000300um_M1800_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLD_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-a59480da6bc38414e064ab351a42afb4/USER', 191999)
mfv_stopld_tau010000um_M1800_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLD_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-a32f6e61bfa1e5680d7680ddd17f6635/USER', 90384)
mfv_stopld_tau001000um_M1800_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLD_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-9ee763cb6a5eb9a2742a224bfeb9bc5a/USER', 97471)
mfv_stopld_tau030000um_M1800_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLD_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-f3ded24ee1ae6144fc2d4756a959f967/USER', 88523)
mfv_stopld_tau000100um_M0200_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLD_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-da9e961fe8a92bdbbb4a0d373af688cb/USER', 179217)
mfv_stopld_tau000300um_M0200_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLD_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-ff1366903622652de7c25e01cfadabb0/USER', 180109)
mfv_stopld_tau010000um_M0200_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLD_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-ef62e613ac488663bccff1c8f51af2bf/USER', 178877)
mfv_stopld_tau001000um_M0200_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLD_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-78e58fea3018bb76b84a630433111aca/USER', 184419)
mfv_stopld_tau030000um_M0200_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLD_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-e6ffd9584b87943f27ab58b1da3876ca/USER', 202558)
mfv_stopld_tau000100um_M0300_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLD_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-a5eeb706a3867b0c0e1c747719825572/USER', 187851)
mfv_stopld_tau000300um_M0300_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLD_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-6aa9642f86b80522cf0b0c969b2a4789/USER', 198796)
mfv_stopld_tau010000um_M0300_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLD_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-9e1c6fab602bd5871447079ab9b870c2/USER', 176176)
mfv_stopld_tau001000um_M0300_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLD_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-942c4b387866e8b2f8ac573c94985582/USER', 187448)
mfv_stopld_tau030000um_M0300_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLD_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-93c857c99b15b7fe6ecc9571576f98a5/USER', 173801)
mfv_stopld_tau000100um_M0400_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLD_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-0d120f5bf2afcfd332f6131257150596/USER', 201643)
mfv_stopld_tau000300um_M0400_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLD_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-20891c28a19a8b20e051ef72d328ba02/USER', 192218)
mfv_stopld_tau010000um_M0400_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLD_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-815aac4af5fb0398750a4a7083264750/USER', 198270)
mfv_stopld_tau001000um_M0400_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLD_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-38b3db90e6106cb7b5b43f148bb53993/USER', 200098)
mfv_stopld_tau030000um_M0400_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLD_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-550a1f1a633e0182efbdf17cb3e95793/USER', 203160)
mfv_stopld_tau000100um_M0600_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLD_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-750b6e0dc54dd2ba020a9cc5ff0fa1e1/USER', 178049)
mfv_stopld_tau000300um_M0600_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLD_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-b449063c8b60444900974ef93d506e0e/USER', 186643)
mfv_stopld_tau010000um_M0600_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLD_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-a3d1a88db6a987fabcfec278b1ed10a5/USER', 180081)
mfv_stopld_tau001000um_M0600_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLD_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-f3943aa711efb1bf3e6428060286880e/USER', 192805)
mfv_stopld_tau030000um_M0600_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLD_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-2219204f68a7a9713577c3eed5dc5f28/USER', 200030)
mfv_stopld_tau000100um_M0800_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLD_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-5851af286315013493c89720608b82db/USER', 197872)
mfv_stopld_tau000300um_M0800_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLD_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-96041090a3b12ce67f280d86ee380550/USER', 189928)
mfv_stopld_tau010000um_M0800_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLD_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-575819f49e8593c3d1ddd99e99f8bff8/USER', 99486)
mfv_stopld_tau001000um_M0800_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLD_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-a23ea5b82748464d07e39cfd08ad4ba0/USER', 178173)
mfv_stopld_tau030000um_M0800_2018.add_dataset('ntupleulv5lepm', '/DisplacedSUSY_stopToLD_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV5Lepm_2018-54fa62ed33890232aeff323b1b7afd94/USER', 197136)
ttbar_2018.add_dataset("ntupleulv5lepm")


##same as above, however, lepton track collections have cutbasedID ++ iso(for muons) 
mfv_stoplb_tau010000um_M1000_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-c5720e0bedd8cbff8d85960a98fae274/USER', 99062)
mfv_stoplb_tau001000um_M1000_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-b2ba8c754e8995be6c3712e7215aaf2e/USER', 196748)
mfv_stoplb_tau030000um_M1000_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-c64335a1f95d8a4da1af650806e9fcf6/USER', 199216)
mfv_stoplb_tau000100um_M1200_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-1ad27bc9c83675d1fdf560635da49dbe/USER', 197949)
mfv_stoplb_tau000300um_M1200_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-4f95637d85e847a15b5461382275e407/USER', 198241)
mfv_stoplb_tau010000um_M1200_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-6f56639a0fc410c16c071acb2f95160e/USER', 98201)
mfv_stoplb_tau001000um_M1200_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-bcde8cb98abcd14f31bd34ea46379d64/USER', 199473)
mfv_stoplb_tau030000um_M1200_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-d91b03a0f91909c66ae7839ec21b300e/USER', 199458)
mfv_stoplb_tau000100um_M1400_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-1c3586cb52e2bb140f95a648fe8bf2a1/USER', 199272)
mfv_stoplb_tau000300um_M1400_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-a4f38b7e27aaf0b4452f09da8437a9e9/USER', 200098)
mfv_stoplb_tau010000um_M1400_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-8d7ad4bf862582d65d5543f0fad42aff/USER', 99970)
mfv_stoplb_tau001000um_M1400_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-c1155b0855f712c3b4516d30032f7895/USER', 200807)
mfv_stoplb_tau030000um_M1400_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-41dd0eb3845a9cd8878965daf030e8b5/USER', 200816)
mfv_stoplb_tau000100um_M1600_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-92cf23766af262eca6db46470b969381/USER', 199366)
mfv_stoplb_tau000300um_M1600_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-37f9f1cb64ee5a17674a197adec864ae/USER', 183573)
mfv_stoplb_tau010000um_M1600_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-d59f3c22cebaca3fc04a78f3522caeec/USER', 92372)
mfv_stoplb_tau001000um_M1600_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-5a76e7d43526e793ab65f68c658b9664/USER', 99806)
mfv_stoplb_tau030000um_M1600_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-e3470bbf8087d65262f84f4309a1a69e/USER', 100560)
mfv_stoplb_tau000100um_M1800_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-d4cf6999efb249155812c3997a35ef21/USER', 200523)
mfv_stoplb_tau000300um_M1800_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-35207b918770a337943a2ed574d16977/USER', 199868)
mfv_stoplb_tau010000um_M1800_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-f2e6f64d124c5c6608ab6e64b241e802/USER', 101211)
mfv_stoplb_tau001000um_M1800_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-eaee98babe23e294f3bce1cb9f56c082/USER', 100171)
mfv_stoplb_tau030000um_M1800_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-208f78008e75e1fcb9b9ffa8f6dc654e/USER', 100346)
mfv_stoplb_tau000100um_M0200_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-163012d429be847f7ee67d4062686a1b/USER', 198986)
mfv_stoplb_tau000300um_M0200_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-bd6a031414891e790ab8d395186b6eea/USER', 199542)
mfv_stoplb_tau010000um_M0200_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-e908755082f7b52cc102dc38b25db8ff/USER', 166542)
mfv_stoplb_tau001000um_M0200_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-0507d11d638dde293932f9d22bfe5115/USER', 198269)
mfv_stoplb_tau030000um_M0200_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-c64f4a4f5aa00d7f0433065ababdd6bb/USER', 197780)
mfv_stoplb_tau000100um_M0300_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-3f67d73d605a1db108cc84795f019a1c/USER', 198372)
mfv_stoplb_tau000300um_M0300_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-98eda3933543f5d37691e05773fd9442/USER', 203023)
mfv_stoplb_tau010000um_M0300_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-1c16e03cda5ac48d5c24b8988f95c70d/USER', 196154)
mfv_stoplb_tau001000um_M0300_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-035ffa6dfd0d1bdd14ba3417274979f8/USER', 197602)
mfv_stoplb_tau030000um_M0300_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-b409c2d0bce75dcf511b9852b6f40b80/USER', 196763)
mfv_stoplb_tau000100um_M0400_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-b52a6fd1fd0157eead25846a5528b091/USER', 200505)
mfv_stoplb_tau000300um_M0400_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-223f36c4252a9035ecddea16d795ac8e/USER', 200842)
mfv_stoplb_tau010000um_M0400_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-d7ae24d866fc9238912a26fad97df9a5/USER', 198963)
mfv_stoplb_tau001000um_M0400_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-e34a8e6630215ab4e7d65e95fad8e8f8/USER', 199860)
mfv_stoplb_tau030000um_M0400_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-f1494597a3f885d2e1babfe6a92b0899/USER', 198368)
mfv_stoplb_tau000100um_M0600_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-077936c47f0a97438f5005b1628afa04/USER', 198211)
mfv_stoplb_tau000300um_M0600_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-c8d770dfda361f78e62ba83445fb98c6/USER', 199368)
mfv_stoplb_tau010000um_M0600_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-897abe8ccee0404f16ee9577e6a116e3/USER', 197845)
mfv_stoplb_tau001000um_M0600_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-4c8b4e0d5f5ae2d59afa0eeb901dcab9/USER', 196032)
mfv_stoplb_tau030000um_M0600_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-7a2ef2b0d8b7a02b343eed110c002cc3/USER', 201533)
mfv_stoplb_tau000100um_M0800_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-c2b0451c8bcecde24c007a747de0dbc0/USER', 202319)
mfv_stoplb_tau000300um_M0800_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-b9e7acd8d9c4710fbf6d9cd78210eee4/USER', 200738)
mfv_stoplb_tau010000um_M0800_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-9c8a7b83247a5a45ca27da73591dee6d/USER', 99747)
mfv_stoplb_tau001000um_M0800_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-549ddc3f8408bcc3ab0ac81d1c5c1f4e/USER', 202348)
mfv_stoplb_tau030000um_M0800_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-214d635e03ab584ad4be7c26305007e2/USER', 199087)
mfv_stopld_tau000100um_M1000_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLD_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-2e3a449ed3bda107954b1db9c8da07e3/USER', 198858)
mfv_stopld_tau000300um_M1000_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLD_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-9d2183f4cda3929c4f62de5ba80f8208/USER', 199006)
mfv_stopld_tau010000um_M1000_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLD_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-40f8b2851d10ff2d61de01c319ec516b/USER', 98581)
mfv_stopld_tau001000um_M1000_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLD_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-064816fbd97e14f780348e4f0942c585/USER', 196285)
mfv_stopld_tau030000um_M1000_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLD_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-7cf674de4943a404bda0a1ec52c6d13c/USER', 197592)
mfv_stopld_tau000100um_M1200_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLD_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-dd7bc7450b984285e586f3b850681aea/USER', 195354)
mfv_stopld_tau000300um_M1200_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLD_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-d8f7086e8f74c2f15e2bd606be614ee9/USER', 199435)
mfv_stopld_tau010000um_M1200_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLD_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-86d06ad1c32f2d83d013c25938f95d7f/USER', 98617)
mfv_stopld_tau001000um_M1200_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLD_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-3ba915f4de98c471b1502775c0bda42c/USER', 200103)
mfv_stopld_tau030000um_M1200_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLD_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-6420f27cb1a8d1759c8ab4dc58b7c1bc/USER', 200964)
mfv_stopld_tau000100um_M1400_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLD_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-43664e7847bcd0bfcb1bd0338af70d78/USER', 200045)
mfv_stopld_tau000300um_M1400_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLD_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-b7cd7a9625038d20e2fd4431de2821ea/USER', 202529)
mfv_stopld_tau010000um_M1400_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLD_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-1463e5f8218b634258f3583cd450114c/USER', 100228)
mfv_stopld_tau001000um_M1400_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLD_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-36b4b6c4533bd9c047fd1cc4682ed9b0/USER', 196708)
mfv_stopld_tau030000um_M1400_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLD_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-b401a76739c09432324ff03f24ee9bde/USER', 201992)
mfv_stopld_tau000100um_M1600_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLD_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-b27b4a5475188e8425616ac3a6d7758c/USER', 201300)
mfv_stopld_tau000300um_M1600_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLD_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-9730ba787a172fb348823216ece55e51/USER', 197421)
mfv_stopld_tau010000um_M1600_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLD_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-8ccf148e819978456015bb5083a53f8d/USER', 99387)
mfv_stopld_tau001000um_M1600_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLD_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-12414b811ad267aea59820e0813b455b/USER', 100838)
mfv_stopld_tau030000um_M1600_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLD_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-640cd3f748ad2c5e679a5102c57289d5/USER', 97752)
mfv_stopld_tau000100um_M1800_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLD_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-1c787ce69689bce81fd112596989fb0d/USER', 198595)
mfv_stopld_tau000300um_M1800_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLD_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-2ced6ca1e377f6ed8aac2a36ca5e0d5a/USER', 199924)
mfv_stopld_tau010000um_M1800_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLD_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-653c7a57fca0b124f4a8cb292cbb1517/USER', 99400)
mfv_stopld_tau001000um_M1800_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLD_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-e5e7a36f08540ce557b5f10e6a58a062/USER', 99515)
mfv_stopld_tau030000um_M1800_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLD_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-63468e814093f3918d100cf977115fe3/USER', 98449)
mfv_stopld_tau000100um_M0200_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLD_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-4725a0ff2811ac11ba878fdc62a820bc/USER', 197970)
mfv_stopld_tau000300um_M0200_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLD_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-7544b5798f515eb6188db4051e3e4ab6/USER', 198800)
mfv_stopld_tau010000um_M0200_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLD_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-6962833bb1b5da0a5a24ccf2adcc3004/USER', 199856)
mfv_stopld_tau001000um_M0200_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLD_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-9246abd5689a8a1f2ef4f9064179d4d5/USER', 200411)
mfv_stopld_tau030000um_M0200_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLD_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-7f1468499347a74dc62eb680d442bfe6/USER', 202558)
mfv_stopld_tau000100um_M0300_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLD_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-687a4dc23d16385fef24a8df38dbb7f0/USER', 196635)
mfv_stopld_tau000300um_M0300_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLD_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-26644f6105cb787225d77ee987ecb5f4/USER', 198796)
mfv_stopld_tau010000um_M0300_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLD_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-4eaaa453ece2169d6e0d906db2379ab6/USER', 197769)
mfv_stopld_tau001000um_M0300_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLD_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-dc1f57746b7596655a7bec325036fae9/USER', 200543)
mfv_stopld_tau030000um_M0300_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLD_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-b73296d7123a1e687761ac6dcf94cc7b/USER', 198495)
mfv_stopld_tau000100um_M0400_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLD_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-385d2540bda8069e62a9cd2b875b122b/USER', 201643)
mfv_stopld_tau000300um_M0400_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLD_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-3615cf9296530e74d877f761eaff304e/USER', 197079)
mfv_stopld_tau010000um_M0400_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLD_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-231117e75bed47f5105398202a581f33/USER', 198270)
mfv_stopld_tau001000um_M0400_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLD_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-75c1177d194fdab03ed5b8b204fbcbda/USER', 200098)
mfv_stopld_tau030000um_M0400_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLD_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-3dcf813a3006ae53f4dcf06f4f47ff65/USER', 203160)
mfv_stopld_tau000100um_M0600_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLD_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-a501b7583c3829c78ab7e0c53db1b7ca/USER', 198964)
mfv_stopld_tau000300um_M0600_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLD_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-1b21784318a6db3330ceb75ca256516d/USER', 198408)
mfv_stopld_tau010000um_M0600_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLD_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-e9396aa973c59ac1cd03f3dded37d1ee/USER', 200404)
mfv_stopld_tau001000um_M0600_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLD_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-34b8d344d48257477bb26148e19ddab0/USER', 194658)
mfv_stopld_tau030000um_M0600_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLD_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-a9807e8f392d9bcb24abfc54994638f6/USER', 200030)
mfv_stopld_tau000100um_M0800_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLD_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-c6552bd052ba43dc980bc5888c7ec2a3/USER', 197872)
mfv_stopld_tau000300um_M0800_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLD_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-6feadb8e97ca054db58c2345fed8c1a1/USER', 202036)
mfv_stopld_tau010000um_M0800_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLD_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-a4e3f3ed97c08902f60114c74d840d44/USER', 100507)
mfv_stopld_tau001000um_M0800_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLD_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-b04e2a27ebd5e4bbcb96ebf5c60398ec/USER', 199217)
mfv_stopld_tau030000um_M0800_2018.add_dataset('ntupleulv3lepm_wgen', '/DisplacedSUSY_stopToLD_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV3Lepm_WGen_2018-80561298d0536e2889617ae43116030b/USER', 197136)

#add lost tracks 
mfv_stoplb_tau000300um_M1000_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLBottom_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-bee4bf2346fa67c1a3d3a42889a0b2a2/USER', 196665)
mfv_stoplb_tau010000um_M1000_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLBottom_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-6e3aa3527fe74ae3eb2b9566c588a570/USER', 98069)
mfv_stoplb_tau001000um_M1000_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLBottom_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-5d34740f5f7b03610fd54775cda6cbd2/USER', 195789)
mfv_stoplb_tau030000um_M1000_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLBottom_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-b0bdf7fd74fae91327c0d39b839ea5b5/USER', 187306)
mfv_stoplb_tau000100um_M1200_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLBottom_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-9da96d8b0e93470bdc859dd2ca30aea4/USER', 197949)
mfv_stoplb_tau000300um_M1200_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLBottom_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-3c1166ad0431f09c23f8454c7ab6c6ee/USER', 196265)
mfv_stoplb_tau010000um_M1200_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLBottom_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-2f846c13a88889d9096fc05f8339ca0e/USER', 94249)
mfv_stoplb_tau001000um_M1200_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLBottom_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-9f92c1d89b0e91e6877a7c1c7f34bc64/USER', 199473)
mfv_stoplb_tau030000um_M1200_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLBottom_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-832128b5d90268ed6c5495b202b43062/USER', 191513)
mfv_stoplb_tau000100um_M1400_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLBottom_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-9b54133e5ade0b9663788b003560a4c7/USER', 190405)
mfv_stoplb_tau000300um_M1400_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLBottom_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-5387b1dce6d9371441626c9efa4efbd0/USER', 200098)
mfv_stoplb_tau010000um_M1400_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLBottom_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-4f888509584ae26da0eca083e0cff6e2/USER', 81935)
mfv_stoplb_tau001000um_M1400_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLBottom_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-c8d094ec604d1383f083aaeb252c8d39/USER', 199809)
mfv_stoplb_tau030000um_M1400_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLBottom_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-3605c526f30e2919af5f146317b84f88/USER', 196806)
mfv_stoplb_tau000100um_M1600_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLBottom_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-5b20abde8547abd74bb7bc2583778bdd/USER', 199366)
mfv_stoplb_tau000300um_M1600_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLBottom_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-104c598637cbbb4df4d0939b1cf86d5a/USER', 202756)
mfv_stoplb_tau010000um_M1600_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLBottom_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-852f84a02fff72084b89b669e297373b/USER', 101586)
mfv_stoplb_tau001000um_M1600_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLBottom_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-39efaeb63ad15e3440c5ea411fb28175/USER', 99806)
mfv_stoplb_tau030000um_M1600_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLBottom_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-50d0800eeacb119fd68f386a721ba433/USER', 99590)
mfv_stoplb_tau000100um_M1800_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLBottom_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-6ebe4ccf4453ca2e6d4519e67cc090fa/USER', 200523)
mfv_stoplb_tau000300um_M1800_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLBottom_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-79184e200b9db30760404007367754e5/USER', 199868)
mfv_stoplb_tau010000um_M1800_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLBottom_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-149d57fc9c50aa874e6346c45f45102e/USER', 100224)
mfv_stoplb_tau001000um_M1800_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLBottom_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-4b547e98a92f1c6e957b34139a762217/USER', 97144)
mfv_stoplb_tau030000um_M1800_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLBottom_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-ed4fbde53463cfd03b18b985c2f1621e/USER', 99376)
mfv_stoplb_tau000100um_M0200_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLBottom_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-3dfc3414fa89a34e374138d420ff09ab/USER', 197015)
mfv_stoplb_tau000300um_M0200_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLBottom_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-b34557126d1d6c946fb6842d74478881/USER', 199542)
mfv_stoplb_tau010000um_M0200_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLBottom_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-1b3e952b7b0d1dbbe29b02323a91b191/USER', 185261)
mfv_stoplb_tau001000um_M0200_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLBottom_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-d145e2e6f5dee37b276282cbb25074de/USER', 198269)
mfv_stoplb_tau030000um_M0200_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLBottom_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-b21e289d5fc33383b088bc11415f904b/USER', 197780)
mfv_stoplb_tau000100um_M0300_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLBottom_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-bfe0806ecfd951976f912a004bbf276f/USER', 198372)
mfv_stoplb_tau000300um_M0300_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLBottom_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-101c1ad38a7a8177944b60b468527edf/USER', 203023)
mfv_stoplb_tau010000um_M0300_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLBottom_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-f25f2ed1f7b5739652a7e7d2f3c7ef7f/USER', 196154)
mfv_stoplb_tau001000um_M0300_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLBottom_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-7bce18a78fbb7a39f0f1029627bc78e6/USER', 196615)
mfv_stoplb_tau030000um_M0300_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLBottom_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-1b984ed6b4ee267403b1576adc7fc63e/USER', 196763)
mfv_stoplb_tau000100um_M0400_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLBottom_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-bc5d94260437757ea8027241fbbb1c75/USER', 200505)
mfv_stoplb_tau000300um_M0400_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLBottom_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-e40c7a28d449dcacce45e3e2a1aedf23/USER', 200842)
mfv_stoplb_tau010000um_M0400_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLBottom_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-5d19bc453886a3d53fea90eabd1b2e53/USER', 198963)
mfv_stoplb_tau001000um_M0400_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLBottom_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-ff88a8fe65a2ee9637abb5413298e4a9/USER', 199860)
mfv_stoplb_tau030000um_M0400_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLBottom_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-79bbb7a0c4404029bb569c470b3acab5/USER', 198368)
mfv_stoplb_tau000100um_M0600_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLBottom_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-ec02f36a22f1bed97407bed43c6cc55d/USER', 198211)
mfv_stoplb_tau000300um_M0600_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLBottom_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-d27ec6aeaf6a01cde64c35275eb5c67a/USER', 180286)
mfv_stoplb_tau010000um_M0600_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLBottom_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-fbe0824dff9cd878f6b899872cb48514/USER', 197845)
mfv_stoplb_tau001000um_M0600_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLBottom_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-8e6f474fb10247eb77f11e83dcf1c0a8/USER', 196032)
mfv_stoplb_tau030000um_M0600_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLBottom_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-a2674d4b3f14d095f9f87df1f05e1ea5/USER', 201533)
mfv_stoplb_tau000100um_M0800_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLBottom_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-e980c5b337c476a9fa7c58cde06abe21/USER', 202319)
mfv_stoplb_tau000300um_M0800_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLBottom_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-37fe92690acc18ec8eac3caae6861ecc/USER', 200738)
mfv_stoplb_tau010000um_M0800_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLBottom_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-03ab69e295b62592e791716f82ac5fdc/USER', 99747)
mfv_stoplb_tau001000um_M0800_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLBottom_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-d6ea43b80192d2c92f22e5e710990db1/USER', 202348)
mfv_stoplb_tau030000um_M0800_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLBottom_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-9cc743be3b8c6cea3682c755b9b17564/USER', 199087)
mfv_stopld_tau000100um_M1000_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLD_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-4629054cb66ffd24de67b23c7b8b928a/USER', 186784)
mfv_stopld_tau000300um_M1000_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLD_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-cf1b260e3885989d84743ba7c4d05d63/USER', 199006)
mfv_stopld_tau010000um_M1000_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLD_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-38aa292d037bb1f617cc72c2dd3d0d4b/USER', 98581)
mfv_stopld_tau001000um_M1000_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLD_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-756381468f9adeb574697b4afbe92500/USER', 196285)
mfv_stopld_tau030000um_M1000_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLD_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-ab79328f4804097e9627ed1e72b3d865/USER', 197592)
mfv_stopld_tau000100um_M1200_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLD_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-bb09b41755bf08c9f8667cafa4d15f89/USER', 195354)
mfv_stopld_tau000300um_M1200_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLD_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-6de6e300ed7a4c867dd65b23b7eb0c9b/USER', 199435)
mfv_stopld_tau010000um_M1200_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLD_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-6513492bf5761568c1f5314cfa747bc0/USER', 98617)
mfv_stopld_tau001000um_M1200_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLD_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-a0a3ff5b4c9b9c02ab6386c3252de783/USER', 200103)
mfv_stopld_tau030000um_M1200_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLD_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-08c561eec8c86d11800d06f466a9aaac/USER', 200964)
mfv_stopld_tau000100um_M1400_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLD_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-bb9aaa506005a028bee6928b4931cf16/USER', 200045)
mfv_stopld_tau000300um_M1400_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLD_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-a3cc171efe478a7ae14867669364ff1a/USER', 202529)
mfv_stopld_tau010000um_M1400_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLD_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-49206a1fb08df5304757dbfe55ce6c29/USER', 100228)
mfv_stopld_tau001000um_M1400_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLD_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-ffcae0f5125f585dab2c264c0a0bbd81/USER', 196708)
mfv_stopld_tau030000um_M1400_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLD_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-25d72611981f56291ccbac968412e9cd/USER', 201992)
mfv_stopld_tau000100um_M1600_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLD_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-7791b76b548405865dca665bc967b798/USER', 201300)
mfv_stopld_tau000300um_M1600_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLD_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-43915ec31154e885feec7d76b5812cfa/USER', 197421)
mfv_stopld_tau010000um_M1600_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLD_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-a4b7f446d53aef2f048a14cb236d5247/USER', 99387)
mfv_stopld_tau001000um_M1600_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLD_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-544adf661a65c0c6ba9caa660feb8ef9/USER', 100838)
mfv_stopld_tau030000um_M1600_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLD_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-a60f2cf41ee9270177e92e2228457d5b/USER', 97752)
mfv_stopld_tau000100um_M1800_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLD_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-d552bb38e42e173ed63d80299cba4726/USER', 202746)
mfv_stopld_tau000300um_M1800_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLD_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-c35a5731503285a09dba5eb4140439a2/USER', 199924)
mfv_stopld_tau010000um_M1800_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLD_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-d7ac8ffbccf504dd4a202705ad45dffe/USER', 99400)
mfv_stopld_tau001000um_M1800_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLD_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-cf3cb7b8105cd6403fc8f04e450b320a/USER', 99515)
mfv_stopld_tau030000um_M1800_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLD_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-feeb8a753e7fce38bc1016250c707998/USER', 98449)
mfv_stopld_tau000100um_M0200_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLD_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-46fa1f24e14e945ab93b734bcad6b352/USER', 196979)
mfv_stopld_tau000300um_M0200_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLD_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-ac36e6af5e233f758dde1eddb442fbd2/USER', 198800)
mfv_stopld_tau010000um_M0200_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLD_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-d2dc65ba8326f8623d79778d4e897f15/USER', 199856)
mfv_stopld_tau001000um_M0200_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLD_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-147876c3b5a1a954ba57f0e99283abd7/USER', 200411)
mfv_stopld_tau030000um_M0200_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLD_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-cd93f8c468b0e03af937ac40af9d1098/USER', 202558)
mfv_stopld_tau000100um_M0300_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLD_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-081614e3f0254c4778a395c4337d1a8a/USER', 196635)
mfv_stopld_tau000300um_M0300_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLD_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-96cb864b4f2ab4a1b899fd3ac67d2bf6/USER', 198796)
mfv_stopld_tau010000um_M0300_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLD_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-bc932dc23deb5b894a076f575f4644b9/USER', 197769)
mfv_stopld_tau001000um_M0300_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLD_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-a7f784199fbb87b5df124b10f01b5ae9/USER', 200543)
mfv_stopld_tau030000um_M0300_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLD_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-bbc843eb54abbe1ac519be575a73063f/USER', 198495)
mfv_stopld_tau000100um_M0400_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLD_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-e911569e326177ba0104fb408e78d857/USER', 201643)
mfv_stopld_tau000300um_M0400_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLD_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-052e28351968c64a7e139346ba65281a/USER', 197079)
mfv_stopld_tau010000um_M0400_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLD_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-74c792b16defa033fc260b2544887bb6/USER', 198270)
mfv_stopld_tau001000um_M0400_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLD_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-55a9fcb7cf6aaa990e30ddb029badc95/USER', 200098)
mfv_stopld_tau030000um_M0400_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLD_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-92aa1c5c89ce1fb97842c87b87ef0064/USER', 203160)
mfv_stopld_tau000100um_M0600_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLD_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-fe13962431bc06c28f6335d429f3cf13/USER', 198964)
mfv_stopld_tau000300um_M0600_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLD_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-0f8c0cf3ac5ecabc133d110988c403ff/USER', 198408)
mfv_stopld_tau010000um_M0600_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLD_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-b664688ab5bd2b91ef79a02a03f24ff9/USER', 200404)
mfv_stopld_tau001000um_M0600_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLD_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-19af270448250f71e8b4285fee37d7be/USER', 199759)
mfv_stopld_tau030000um_M0600_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLD_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-50774ff5e8555eddd6c582fac3237775/USER', 200030)
mfv_stopld_tau000100um_M0800_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLD_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-db2f82d554bcfd730e454b0e11e64806/USER', 195881)
mfv_stopld_tau000300um_M0800_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLD_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-80cad6f6fc8c3e8b197392ecfff58aaf/USER', 202036)
mfv_stopld_tau010000um_M0800_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLD_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-3dba685926b6304bf74f1ae75e602d1c/USER', 100507)
mfv_stopld_tau001000um_M0800_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLD_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-02cb21850d7f3314981d6dfa4964b10a/USER', 199217)
mfv_stopld_tau030000um_M0800_2018.add_dataset('ntupleulv4lepm', '/DisplacedSUSY_stopToLD_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV4Lepm_2018-3feacf59d7114dfbe09cab37bd20ade9/USER', 197136)


## Tracking Treer (EF in place -- lep pass pt > 5, eta, ID, iso & min 1 jet; Single Lep Trigger)
qcdmupt15_2018.add_dataset('trackingtreerulv1_lepm', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
qcdempt015_2018.add_dataset('trackingtreerulv1_lepm', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
qcdempt020_2018.add_dataset('trackingtreerulv1_lepm', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
qcdempt030_2018.add_dataset('trackingtreerulv1_lepm', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
qcdempt050_2018.add_dataset('trackingtreerulv1_lepm', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
qcdempt080_2018.add_dataset('trackingtreerulv1_lepm', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
qcdempt120_2018.add_dataset('trackingtreerulv1_lepm', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
qcdempt170_2018.add_dataset('trackingtreerulv1_lepm', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
qcdempt300_2018.add_dataset('trackingtreerulv1_lepm', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
qcdbctoept015_2018.add_dataset('trackingtreerulv1_lepm', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
qcdbctoept020_2018.add_dataset('trackingtreerulv1_lepm', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
qcdbctoept030_2018.add_dataset('trackingtreerulv1_lepm', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
qcdbctoept080_2018.add_dataset('trackingtreerulv1_lepm', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
qcdbctoept170_2018.add_dataset('trackingtreerulv1_lepm', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
qcdbctoept250_2018.add_dataset('trackingtreerulv1_lepm', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
dyjetstollM10_2018.add_dataset('trackingtreerulv1_lepm', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
dyjetstollM50_2018.add_dataset('trackingtreerulv1_lepm', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
wjetstolnu_2018.add_dataset('trackingtreerulv1_lepm', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
ww_2018.add_dataset('trackingtreerulv1_lepm', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
wz_2018.add_dataset('trackingtreerulv1_lepm', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
zz_2018.add_dataset('trackingtreerulv1_lepm', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
SingleMuon2018A.add_dataset('trackingtreerulv1_lepm', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
SingleMuon2018B.add_dataset('trackingtreerulv1_lepm', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
SingleMuon2018C.add_dataset('trackingtreerulv1_lepm', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
SingleMuon2018D.add_dataset('trackingtreerulv1_lepm', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
EGamma2018A.add_dataset('trackingtreerulv1_lepm', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
EGamma2018B.add_dataset('trackingtreerulv1_lepm', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
EGamma2018C.add_dataset('trackingtreerulv1_lepm', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
EGamma2018D.add_dataset('trackingtreerulv1_lepm', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
ttbar_2018.add_dataset("trackingtreerulv1_lepm")

ttbar_2018.add_dataset("trackingtreerulv2_lepm")
########
# automatic condor declarations for ntuples
########

for s in registry.all():
    for ds in s.datasets.keys():
        for ds4 in 'ntuple', 'nr_':
            if ds.startswith(ds4):
                s.datasets[ds].condor = True
                #s.datasets[ds].xrootd_url = xrootd_sites['T3_US_FNALLPC']
                s.datasets[ds].xrootd_url = xrootd_sites['T2_US_Wisconsin']
                

########
# other condor declarations, generate condorable dict with Shed/condor_list.py
########
# be careful about the list, some samples are distributed at different samples so it won't work
condorable = {
    "T2_DE_DESY": {
        "miniaod": [MET2017E, MET2018A, MET2018B, zjetstonunuht0100_2018, zjetstonunuht0200_2018, zjetstonunuht0400_2018, zjetstonunuht0600_2018, zjetstonunuht0800_2018, zjetstonunuht1200_2018],
        },
    "T3_US_FNALLPC": {
        "miniaod": mfv_splitSUSY_samples_2017 + mfv_signal_samples_2017 + mfv_stopdbardbar_samples_2017 + mfv_stopbbarbbar_samples_2017 #+ ZHToSSTodddd_samples_2017 + WminusHToSSTodddd_samples_2017 + WplusHToSSTodddd_samples_2017
        
        },
    "T1_US_FNAL_Disk": {
        "miniaod": [SingleMuon2017B, SingleMuon2017D, SingleMuon2017E, SingleElectron2017B, SingleElectron2017D, SingleElectron2017E, MET2018D, qcdht0300_2018, qcdht0700_2018, qcdht1000_2018, qcdht1500_2018, zjetstonunuht2500_2018, qcdht0200_2017, qcdht0500_2017, qcdht0700_2017, qcdht0300_2017, ttbar_2017, ttbar_2018],

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
    for y,ss in (2017, data_samples_2017 + Lepton_data_samples_2017), (2018, data_samples_2018 + auxiliary_data_samples_2018 + egamma_data_samples_2018 + Lepton_data_samples_2018):
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
