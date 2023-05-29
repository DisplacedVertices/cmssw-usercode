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
        print(sample.name)
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
    MCSample('qcdempt015_2017', '/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v1/AODSIM',   7966910, nice='QCD,  15 < #hat{p}_{T} <  20 GeV, EM enriched', color=801, syst_frac=0.20, xsec=1.324e6),
    MCSample('qcdmupt15_2017',  '/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v1/AODSIM',  17716270, nice='QCD, #hat{p}_{T} > 20 GeV, #mu p_{T} > 15 GeV', color=801, syst_frac=0.20, xsec=2.39e5),
    MCSample('qcdempt020_2017', '/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v1/AODSIM',   14166147, nice='QCD,  20 < #hat{p}_{T} <  30 GeV, EM enriched', color=801, syst_frac=0.20, xsec=4.896e6),
    MCSample('qcdempt030_2017', '/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v2/AODSIM',   8784542, nice='QCD,  30 < #hat{p}_{T} <  50 GeV, EM enriched', color=801, syst_frac=0.20, xsec=6.447e6),
    MCSample('qcdempt050_2017', '/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v2/AODSIM',   10590542, nice='QCD,  50 < #hat{p}_{T} <  80 GeV, EM enriched', color=801, syst_frac=0.20, xsec=1.988e6),
    MCSample('qcdempt080_2017', '/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v2/AODSIM',   9615795, nice='QCD,  80 < #hat{p}_{T} < 120 GeV, EM enriched', color=801, syst_frac=0.20, xsec=3.675e5),
    MCSample('qcdempt120_2017', '/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v2/AODSIM',  9904245, nice='QCD, 120 < #hat{p}_{T} < 170 GeV, EM enriched', color=801, syst_frac=0.20, xsec=6.659e4),
    MCSample('qcdempt170_2017', '/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v2/AODSIM',  3678200, nice='QCD, 170 < #hat{p}_{T} < 300 GeV, EM enriched', color=801, syst_frac=0.20, xsec=1.662e4),
    MCSample('qcdempt300_2017', '/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v2/AODSIM',  2214934, nice='QCD, #hat{p}_{T} > 300 GeV, EM enriched',       color=801, syst_frac=0.20, xsec=1104.0),
    MCSample('qcdbctoept020_2017', '/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v2/AODSIM',      14248556, nice='QCD,  20 < #hat{p}_{T} <  30 GeV, HF electrons', color=801, syst_frac=0.20, xsec=3.038e5),
    MCSample('qcdbctoept030_2017', '/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v2/AODSIM',      15656025, nice='QCD,  30 < #hat{p}_{T} <  80 GeV, HF electrons', color=801, syst_frac=0.20, xsec=3.623e5),
    MCSample('qcdbctoept080_2017', '/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v2/AODSIM',     16158199, nice='QCD,  80 < #hat{p}_{T} < 170 GeV, HF electrons', color=801, syst_frac=0.20, xsec=3.37e4),
    MCSample('qcdbctoept170_2017', '/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v2/AODSIM',    15940531, nice='QCD, 170 < #hat{p}_{T} < 250 GeV, HF electrons', color=801, syst_frac=0.20, xsec=2.125e3),
    MCSample('qcdbctoept250_2017', '/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v3/AODSIM',    16028600, nice='QCD, #hat{p}_{T} > 250 GeV, HF electrons',       color=801, syst_frac=0.20, xsec=562.5),
    ]
    
# ttbar with HT slices not available for UL now
ttbar_samples_2017 = [
]
bjet_samples_2017 = [
    ]

leptonic_samples_2017 = [
    MCSample('wjetstolnu_2017',       '/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v1/AODSIM', 81551529, nice='W + jets #rightarrow l#nu', color=  9, syst_frac=0.10, xsec=5.294e4),
    MCSample('dyjetstollM10_2017',    '/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v2/AODSIM',                  70516252, nice='DY + jets #rightarrow ll, 10 < M < 50 GeV', color= 29, syst_frac=0.10, xsec=1.58e4),
    MCSample('dyjetstollM50_2017',    '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v1/AODSIM',          103599638, nice='DY + jets #rightarrow ll, M > 50 GeV', color= 32, syst_frac=0.10, xsec=5.34e3),
    ]

example_samples_ttbar_2017 = [
    MCSample('example_ttbar_2017',     '/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/AODSIM',  249133364, nice='t#bar{t}',                   color=4,   syst_frac=0.15, xsec=831.76), 
    ]

met_samples_2017 = [
    #MCSample('ttbar_2017',     '/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v2/AODSIM',    249133364, nice='t#bar{t}',                   color=4,   syst_frac=0.15, xsec=831.76),
    MCSample('ttbar_2017',     '/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/AODSIM',  249133364, nice='t#bar{t}',                   color=4,   syst_frac=0.15, xsec=831.76), 
    ]

diboson_samples_2017 = [
    MCSample('ww_2017', '/WW_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2/MINIAODSIM', 15883000, nice='WW', color = 9, syst_frac=0.10, xsec=75.8),
    MCSample('zz_2017', '/ZZ_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2/MINIAODSIM', 2708000, nice='ZZ', color = 9, syst_frac=0.10, xsec=12.140),
    MCSample('wz_2017', '/WZ_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2/MINIAODSIM', 7898000, nice='WZ', color =9, syst_frac=0.10, xsec=27.6)
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
    MCSample('dyjetstollM10_2018',    '/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM', 99288125, nice='$DY + jets #rightarrow ll$, $10 < M < 50$ \\GeV', color= 29, syst_frac=0.10, xsec=1.589e4),
    MCSample('dyjetstollM50_2018',    '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM',     96233328, nice='$DY + jets #rightarrow ll$, $M > 50$ \\GeV', color= 32, syst_frac=0.10, xsec=5.398e3),
    MCSample('wjetstolnu_2018',       '/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM',          82442496, nice='$W + jets #rightarrow l#nu$', color=  9, syst_frac=0.10, xsec=5.294e4),
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

qcdmupt15_2017.add_dataset('miniaod', '/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v1/MINIAODSIM', 17580112)
qcdempt015_2017.add_dataset('miniaod', '/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v1/MINIAODSIM', 7908107)
qcdempt020_2017.add_dataset('miniaod', '/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v1/MINIAODSIM', 14146285)
qcdempt030_2017.add_dataset('miniaod', '/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2/MINIAODSIM', 8784542)
qcdempt050_2017.add_dataset('miniaod', '/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2/MINIAODSIM', 10590542)
qcdempt080_2017.add_dataset('miniaod', '/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2/MINIAODSIM', 9615719)
qcdempt120_2017.add_dataset('miniaod', '/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2/MINIAODSIM', 9892235)
qcdempt170_2017.add_dataset('miniaod', '/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2/MINIAODSIM', 3681297)
qcdempt300_2017.add_dataset('miniaod', '/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2/MINIAODSIM', 2214934)
qcdbctoept020_2017.add_dataset('miniaod', '/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2/MINIAODSIM', 14156589)
qcdbctoept030_2017.add_dataset('miniaod', '/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2/MINIAODSIM', 15153568)
qcdbctoept080_2017.add_dataset('miniaod', '/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2/MINIAODSIM', 15908608)
qcdbctoept170_2017.add_dataset('miniaod', '/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2/MINIAODSIM', 15588245)
qcdbctoept250_2017.add_dataset('miniaod', '/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v3/MINIAODSIM', 15557421)
 
    
ttbar_2017.add_dataset('miniaod', '/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 249133364) #FIXME ? new MiniAOD
#ttbarht0600_2017.add_dataset('miniaod', '/TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',    81507662)
#ttbarht0800_2017.add_dataset('miniaod', '/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',   40191637)
#ttbarht1200_2017.add_dataset('miniaod', '/TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',  13214871)
#ttbarht2500_2017.add_dataset('miniaod', '/TTJets_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v3/MINIAODSIM',    5155687)
wjetstolnu_2017.add_dataset('miniaod', '/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v1/MINIAODSIM', 81254459)
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
wz_2017.add_dataset('miniaod', '/ZZ_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2/MINIAODSIM', 2708000)
zz_2017.add_dataset('miniaod', '/WZ_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2/MINIAODSIM', 7898000)

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
example_ttbar_2017.add_dataset('nr_trackmoverulv30lepmv2')


for x in WplusHToSSTodddd_tau30mm_M55_2017, WplusHToSSTodddd_tau1mm_M55_2017, WplusHToSSTodddd_tau300um_M55_2017:
    x.add_dataset("trackmovermctruthulv30lepmv2")

#qcdmupt15_2017, qcdempt020_2017, qcdempt120_2017, dyjetstollM50_2017
qcdempt015_2017.add_dataset('trackmoverulv30lepmv2', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
qcdmupt15_2017.add_dataset('trackmoverulv30lepmv2', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
qcdempt020_2017.add_dataset('trackmoverulv30lepmv2', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
qcdempt030_2017.add_dataset('trackmoverulv30lepmv2', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
qcdempt050_2017.add_dataset('trackmoverulv30lepmv2', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
qcdempt080_2017.add_dataset('trackmoverulv30lepmv2', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
qcdempt120_2017.add_dataset('trackmoverulv30lepmv2', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
qcdempt170_2017.add_dataset('trackmoverulv30lepmv2', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
qcdempt300_2017.add_dataset('trackmoverulv30lepmv2', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
qcdbctoept020_2017.add_dataset('trackmoverulv30lepmv2', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
qcdbctoept030_2017.add_dataset('trackmoverulv30lepmv2', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
qcdbctoept080_2017.add_dataset('trackmoverulv30lepmv2', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
qcdbctoept170_2017.add_dataset('trackmoverulv30lepmv2', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
qcdbctoept250_2017.add_dataset('trackmoverulv30lepmv2', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
wjetstolnu_2017.add_dataset('trackmoverulv30lepmv2', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
dyjetstollM10_2017.add_dataset('trackmoverulv30lepmv2', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
dyjetstollM50_2017.add_dataset('trackmoverulv30lepmv2', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
ww_2017.add_dataset('trackmoverulv30lepmv2', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
zz_2017.add_dataset('trackmoverulv30lepmv2', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
wz_2017.add_dataset('trackmoverulv30lepmv2', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
SingleMuon2017C.add_dataset('trackmoverulv30lepmv2', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
SingleMuon2017F.add_dataset('trackmoverulv30lepmv2', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
SingleElectron2017F.add_dataset('trackmoverulv30lepmv2', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
for x in ttbar_2017, SingleElectron2017C:
    x.add_dataset("trackmoverulv30lepmv2")
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
        "miniaod": [EGamma2018D, MET2017E, MET2018A, MET2018B, zjetstonunuht0100_2018, zjetstonunuht0200_2018, zjetstonunuht0400_2018, zjetstonunuht0600_2018, zjetstonunuht0800_2018, zjetstonunuht1200_2018],
        },
    "T3_US_FNALLPC": {
        "miniaod": mfv_splitSUSY_samples_2017 + mfv_signal_samples_2017 + mfv_stopdbardbar_samples_2017 + mfv_stopbbarbbar_samples_2017 #+ ZHToSSTodddd_samples_2017 + WminusHToSSTodddd_samples_2017 + WplusHToSSTodddd_samples_2017
        
        },
    "T1_US_FNAL_Disk": {
        "miniaod": [MET2018D, qcdht0300_2018, qcdht0700_2018, qcdht1000_2018, qcdht1500_2018, zjetstonunuht2500_2018, qcdht0200_2017, qcdht0500_2017, qcdht0700_2017, qcdht0300_2017,ttbar_2017, ttbar_2018,], #[SingleMuon2017B, SingleMuon2017D, SingleMuon2017E, SingleElectron2017B, SingleElectron2017D, SingleElectron2017E, 

                    #mfv_stoplb_tau010000um_M1000_2017, mfv_stoplb_tau000300um_M1200_2017, mfv_stoplb_tau010000um_M1200_2017, mfv_stoplb_tau001000um_M1200_2017, mfv_stoplb_tau000300um_M1600_2017, mfv_stoplb_tau001000um_M1600_2017, mfv_stoplb_tau000100um_M0300_2017, mfv_stoplb_tau000300um_M0300_2017, mfv_stoplb_tau001000um_M0300_2017, mfv_stoplb_tau001000um_M0400_2017, mfv_stoplb_tau010000um_M0600_2017, mfv_stopld_tau000300um_M1000_2017, mfv_stopld_tau010000um_M1000_2017, mfv_stopld_tau010000um_M1200_2017, mfv_stopld_tau001000um_M1400_2017, mfv_stopld_tau000300um_M1600_2017, mfv_stopld_tau010000um_M0200_2017, mfv_stopld_tau000300um_M0300_2017, mfv_stopld_tau001000um_M0400_2017, mfv_stopld_tau000300um_M0600_2017, mfv_stopld_tau010000um_M0600_2017, mfv_stopld_tau001000um_M0600_2017, mfv_stopld_tau010000um_M0800_2017, mfv_stoplb_tau010000um_M1200_2018, mfv_stoplb_tau001000um_M1200_2018, mfv_stoplb_tau010000um_M1400_2018, mfv_stoplb_tau001000um_M1400_2018, mfv_stoplb_tau010000um_M1600_2018, mfv_stoplb_tau001000um_M1600_2018, mfv_stoplb_tau001000um_M0200_2018, mfv_stoplb_tau010000um_M0300_2018, mfv_stoplb_tau010000um_M0400_2018, mfv_stoplb_tau001000um_M0400_2018, mfv_stoplb_tau001000um_M0600_2018, mfv_stoplb_tau000300um_M0800_2018, mfv_stoplb_tau001000um_M0800_2018, mfv_stopld_tau000300um_M1000_2018, mfv_stopld_tau000300um_M1200_2018, mfv_stopld_tau000100um_M1400_2018, mfv_stopld_tau000100um_M1600_2018, mfv_stopld_tau010000um_M1600_2018, mfv_stopld_tau000300um_M0200_2018, mfv_stopld_tau001000um_M0200_2018, mfv_stopld_tau001000um_M0300_2018, mfv_stopld_tau000300um_M0400_2018, mfv_stopld_tau001000um_M0600_2018],
        },
    "T2_US_Wisconsin": {
       # "miniaod": mfv_stopld_samples_2018 + [mfv_stopld_tau010000um_M0400_2018],
       # "miniaod": [mfv_stopld_tau010000um_M0400_2018],
        },
    "T2_US_Purdue": {
        "miniaod" : [SingleElectron2017C],
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
