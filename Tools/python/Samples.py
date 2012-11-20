#!/usr/bin/env python

import os, re
from JMTucker.Tools.DBS import files_in_dataset
from JMTucker.Tools.general import big_warn

class Sample(object):
    IS_MC = True
    IS_FASTSIM = False
    IS_PYTHIA8 = False
    SCHEDULER_NAME = 'glite'
    HLT_PROCESS_NAME = 'HLT'
    DBS_URL_NUM = 0
    ANA_DBS_URL_NUM = 2
    ANA_HASH = 'bd9748f60791b31d15ca5bb480d0e762'
    PUBLISH_USER = 'tucker'
    ANA_VERSION = 'v2'

    def __init__(self, name, nice_name, dataset):
        self.name = name
        self.nice_name = nice_name
        self.dataset = dataset

        self.is_mc = self.IS_MC
        self.is_fastsim = self.IS_FASTSIM
        self.is_pythia8 = self.IS_PYTHIA8
        self.hlt_process_name = self.HLT_PROCESS_NAME
        self.local_filenames = []
        self.scheduler_name = self.SCHEDULER_NAME
        self.dbs_url_num = self.DBS_URL_NUM
        self.ana_dbs_url_num = self.ANA_DBS_URL_NUM
        self.ana_hash = self.ANA_HASH
        self.publish_user = self.PUBLISH_USER
        self.ana_version = self.ANA_VERSION
        self.ana_ready = True

    @property
    def scheduler(self):
        if self.dbs_url_num > 0:
            return 'condor'
        else:
            return self.scheduler_name

    def _get_dbs_url(self, num):
        return '' if not num else 'dbs_url = https://cmsdbsprod.cern.ch:8443/cms_dbs_ph_analysis_0%i_writer/servlet/DBSServlet' % num
    
    @property
    def dbs_url(self):
        return self._get_dbs_url(self.dbs_url_num)
        
    @property
    def ana_dbs_url(self):
        return self._get_dbs_url(self.ana_dbs_url_num)

    @property
    def primary_dataset(self):
        return self.dataset.split('/')[1]
    
    @property
    def ana_dataset(self):
        return '/%(primary_dataset)s/%(publish_user)s-sstoptuple_%(ana_version)s_%(name)s-%(ana_hash)s/USER' % self

    @property
    def use_server(self):
        return 'use_server = 1' if self.scheduler != 'condor' else ''

    @property
    def filenames(self):
        # Return a list of filenames for running the histogrammer not
        # using crab.
        if self.local_filenames:
            return self.local_filenames
        return files_in_dataset(self.ana_dataset, ana01=self.ana_dbs_url_num == 1, ana02=self.ana_dbs_url_num == 2)

    def __getitem__(self, key):
        return getattr(self, key)

    def _dump(self, redump_existing=False):
        dst = os.path.join('/uscmst1b_scratch/lpc1/3DayLifetime/tucker', self.name)
        os.system('mkdir ' + dst)
        for fn in self.filenames:
            print fn
            if redump_existing or not os.path.isfile(os.path.join(dst, os.path.basename(fn))):
                os.system('dccp ~%s %s/' % (fn,dst))

    @property
    def job_control(self):
        raise NotImplementedError('job_control needs to be implemented')
    
class MCSample(Sample):
    def __init__(self, name, nice_name, dataset, nevents, color, syst_frac, cross_section, k_factor=1):
        super(MCSample, self).__init__(name, nice_name, dataset)
        
        self.nevents = nevents
        self.color = color
        self.syst_frac = float(syst_frac)
        self.cross_section = float(cross_section)
        self.k_factor = float(k_factor)

    @property
    def partial_weight(self):
        return self.cross_section / float(self.nevents) * self.k_factor # the total weight is partial_weight * integrated_luminosity (in 1/pb, cross_section is assumed to be in pb)

    @property
    def job_control(self):
        return '''
total_number_of_events = -1
events_per_job = 75000
'''

class DataSample(Sample):
    IS_MC = False
    JSON = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions12/8TeV/Prompt/Cert_190456-203002_8TeV_PromptReco_Collisions12_JSON_v2.txt'

    def __init__(self, name, dataset, run_range=None):
        super(DataSample, self).__init__(name, name, dataset)

        self.run_range = run_range
        self.json = self.JSON

    @property
    def lumi_mask(self):
        # JMTBAD run_range checking
        if type(self.json) == str:
            return 'lumi_mask = %s' % self.json
        elif self.json is None:
            return ''
        else: # implement LumiList object -> tmp.json
            raise NotImplementedError('need to do something more complicated when combining lumimasks')

    @property
    def job_control(self):
        return '''
total_number_of_lumis = -1
lumis_per_job = 250
''' + self.lumi_mask

# https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat8TeV or PREP for xsecs
background_samples = [
    #        name                title                                                      dataset                                                                                                nevents  clr  syst  xsec (pb)
    MCSample('ttzjets',          't#bar{t}+Z',                                              '/TTZJets_8TeV-madgraph_v2/Summer12-PU_S7_START52_V9-v1/AODSIM',                                        209741,  -1, 0.20, 0.172),
    MCSample('ttwjets',          't#bar{t}+W',                                              '/TTWJets_8TeV-madgraph/Summer12-PU_S7_START52_V9-v1/AODSIM',                                           195301,  -1, 0.20, 0.215),
    MCSample('ttgjets',          't#bar{t}+#gamma',                                         '/TTGJets_8TeV-madgraph/Summer12-PU_S7_START52_V9-v1/AODSIM',                                            71598,  -1, 0.20, 1.44),
    MCSample('singletop_s',      'single t (s-channel)',                                    '/T_s-channel_TuneZ2star_8TeV-powheg-tauola/Summer12-PU_S7_START52_V9-v1/AODSIM',                       259961,  -1, 0.20, 3.79),
    MCSample('singletop_s_tbar', 'single #bar{t} (s-channel)',                              '/Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola/Summer12-PU_S7_START52_V9-v1/AODSIM',                    139974,  -1, 0.20, 1.76),
    MCSample('singletop_t',      'single t (t-channel)',                                    '/T_t-channel_TuneZ2star_8TeV-powheg-tauola/Summer12-PU_S7_START52_V9-v2/AODSIM',                      3780839,  -1, 0.20, 56.4),
    MCSample('singletop_t_tbar', 'single #bar{t} (t-channel)',                              '/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola/Summer12-PU_S7_START52_V9-v1/AODSIM',                   1935072,  -1, 0.20, 30.7),
    MCSample('singletop_tW',     'single t (tW)',                                           '/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/Summer12-PU_S7_START52_V9-v1/AODSIM',                   497658,  42, 0.20, 11.1),
    MCSample('singletop_tW_tbar','single t (#bar{t}W)',                                     '/Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/Summer12-PU_S7_START52_V9-v1/AODSIM',                493460,  42, 0.20, 11.1),
    MCSample('wjetstolnu',       'W + jets #rightarrow l#nu',                               '/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball/Summer12-PU_S7_START52_V9-v2/AODSIM',                   58117034,   9, 0.10, 3.04e4),
    MCSample('ww',               'WW',                                                      '/WW_TuneZ2star_8TeV_pythia6_tauola/Summer12-PU_S7_START52_V9-v1/AODSIM',                             10000431,   4, 0.04, 57.1),
    MCSample('wz',               'WZ',                                                      '/WZ_TuneZ2star_8TeV_pythia6_tauola/Summer12-PU_S7_START52_V9-v1/AODSIM',                              9996622,  30, 0.04, 32.3),
    MCSample('zz',               'ZZ',                                                      '/ZZ_TuneZ2star_8TeV_pythia6_tauola/Summer12-PU_S7_START52_V9-v1/AODSIM',                              9799908,   6, 0.03, 8.3),
    MCSample('zjetstonunuHT050', 'Z #rightarrow #nu#nu + jets, 50 < H_{T} < 100 GeV',       '/ZJetsToNuNu_50_HT_100_TuneZ2Star_8TeV_madgraph/Summer12-PU_S7_START52_V9-v1/AODSIM',                 4053786,  -1, 0.10, 3.81e2),
    MCSample('zjetstonunuHT100', 'Z #rightarrow #nu#nu + jets, 100 < H_{T} < 200 GeV',      '/ZJetsToNuNu_100_HT_200_TuneZ2Star_8TeV_madgraph/Summer12-PU_S7_START52_V9-v1/AODSIM',                4416646,  -1, 0.10, 1.60e2),
    MCSample('zjetstonunuHT200', 'Z #rightarrow #nu#nu + jets, 200 < H_{T} < 400 GeV',      '/ZJetsToNuNu_200_HT_400_TuneZ2Star_8TeV_madgraph/Summer12-PU_S7_START52_V9-v3/AODSIM',                5066608,  -1, 0.10, 4.15e1),
    MCSample('zjetstonunuHT400', 'Z #rightarrow #nu#nu + jets, H_{T} > 400 GeV',            '/ZJetsToNuNu_400_HT_inf_TuneZ2Star_8TeV_madgraph/Summer12-PU_S7_START52_V9-v1/AODSIM',                1006928,  -1, 0.10, 5.27e0),
    MCSample('dyjetstollM10',    'DY + jets #rightarrow ll, 10 < M < 50 GeV',               '/DYJetsToLL_M-10To50filter_8TeV-madgraph/Summer12-PU_S7_START52_V9-v1/AODSIM',                        7132223,  -1, 0.10, 11050*0.069),
    MCSample('dyjetstollM50',    'DY + jets #rightarrow ll, M > 50 GeV',                    '/DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball/Summer12-PU_S7_START52_V9-v2/AODSIM',              30461028,  -1, 0.10, 2.95e3),
    MCSample('ttbar',            't#bar{t}',                                                '/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/Summer12_DR53X-PU_S10_START53_V7A-v3/AODSIM', 6923750,   4, 0.15, 225.2), # named 53 but really a 52 sample
    MCSample('qcd0000',          'QCD, #hat{p}_{T} < 5 GeV',                                '/QCD_Pt-0to5_TuneZ2star_8TeV_pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM',                             999788, 801, 0.10, 4.859e10),
    MCSample('qcd0005',          'QCD, 5 < #hat{p}_{T} < 15 GeV',                           '/QCD_Pt-5to15_TuneZ2star_8TeV_pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM',                           1489184, 802, 0.10, 4.264e10),
    MCSample('qcd0015',          'QCD, 15 < #hat{p}_{T} < 30 GeV',                          '/QCD_Pt-15to30_TuneZ2star_8TeV_pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM',                         10925056, 803, 0.10, 9.883e8),
    MCSample('qcd0030',          'QCD, 30 < #hat{p}_{T} < 50 GeV',                          '/QCD_Pt-30to50_TuneZ2star_8TeV_pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM',                          6000000, 804, 0.10, 6.629e7),
    MCSample('qcd0050',          'QCD, 50 < #hat{p}_{T} < 80 GeV',                          '/QCD_Pt-50to80_TuneZ2star_8TeV_pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM',                          5995944, 805, 0.10, 8.149e6),
    MCSample('qcd0080',          'QCD, 80 < #hat{p}_{T} < 120 GeV',                         '/QCD_Pt-80to120_TuneZ2star_8TeV_pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM',                         5981328, 806, 0.10, 1.034e6),
    MCSample('qcd0120',          'QCD, 120 < #hat{p}_{T} < 170 GeV',                        '/QCD_Pt-120to170_TuneZ2star_8TeV_pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM',                        5985732, 807, 0.10, 1.563e5),
    MCSample('qcd0170',          'QCD, 170 < #hat{p}_{T} < 300 GeV',                        '/QCD_Pt-170to300_TuneZ2star_8TeV_pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM',                        5814398, 808, 0.10, 3.414e4),
    MCSample('qcd0300',          'QCD, 300 < #hat{p}_{T} < 470 GeV',                        '/QCD_Pt-300to470_TuneZ2star_8TeV_pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM',                        5927300, 809, 0.10, 1.760e3),
    MCSample('qcd0470',          'QCD, 470 < #hat{p}_{T} < 600 GeV',                        '/QCD_Pt-470to600_TuneZ2star_8TeV_pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM',                        3994848, 810, 0.10, 1.139e2),
    MCSample('qcd0600',          'QCD, 600 < #hat{p}_{T} < 800 GeV',                        '/QCD_Pt-600to800_TuneZ2star_8TeV_pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM',                        3992760, 811, 0.10, 2.699e1),
    MCSample('qcd0800',          'QCD, 800 < #hat{p}_{T} < 1000 GeV',                       '/QCD_Pt-800to1000_TuneZ2star_8TeV_pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM',                       3998563, 812, 0.10, 3.550e0),
    MCSample('qcd1000',          'QCD, 1000 < #hat{p}_{T} < 1400 GeV',                      '/QCD_Pt-1000to1400_TuneZ2star_8TeV_pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM',                      1964088, 813, 0.10, 7.378e-1),
    MCSample('qcd1400',          'QCD, 1400 < #hat{p}_{T} < 1800 GeV',                      '/QCD_Pt-1400to1800_TuneZ2star_8TeV_pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM',                      2000062, 814, 0.10, 3.352e-2),
    MCSample('qcd1800',          'QCD, #hat{p}_{T} > 1800 GeV',                             '/QCD_Pt-1800_TuneZ2star_8TeV_pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM',                             977586, 815, 0.10, 1.829e-3),
    ]

auxiliary_background_samples = [
    MCSample('qcdht0100', 'QCD, 100 < H_{T} < 250 GeV',  '/QCD_HT-100To250_TuneZ2star_8TeV-madgraph-pythia/Summer12-PU_S7_START52_V9-v1/AODSIM',   50128222, 801, 0.10, 1.04e7),
    MCSample('qcdht0250', 'QCD, 250 < H_{T} < 500 GeV',  '/QCD_HT-250To500_TuneZ2star_8TeV-madgraph-pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM',  27057349, 801, 0.10, 2.76e5),
    MCSample('qcdht0500', 'QCD, 500 < H_{T} < 1000 GeV', '/QCD_HT-500To1000_TuneZ2star_8TeV-madgraph-pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM', 32255694, 801, 0.10, 8.43e3),
    MCSample('qcdht1000', 'QCD, H_{T} > 1000 GeV',       '/QCD_HT-1000ToInf_TuneZ2star_8TeV-madgraph-pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM', 13879218, 801, 0.10, 2.04e2),
    
    MCSample('qcdmu0015', 'QCDmu5, 15 < #hat{p}_{T} < 20 GeV',    '/QCD_Pt-15to20_MuEnrichedPt5_TuneZ2star_8TeV_pythia6/Summer12-PU_S7_START52_V9-v2/AODSIM',     1722681, 801, 0.10, 0.0039*7.02e8),
    MCSample('qcdmu0020', 'QCDmu5, 20 < #hat{p}_{T} < 30 GeV',    '/QCD_Pt-20to30_MuEnrichedPt5_TuneZ2star_8TeV_pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM',     8486904, 801, 0.10, 0.0065*2.87e8),
    MCSample('qcdmu0030', 'QCDmu5, 30 < #hat{p}_{T} < 50 GeV',    '/QCD_Pt-30to50_MuEnrichedPt5_TuneZ2star_8TeV_pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM',     9560265, 801, 0.10, 0.0122*6.61e7),
    MCSample('qcdmu0050', 'QCDmu5, 50 < #hat{p}_{T} < 80 GeV',    '/QCD_Pt-50to80_MuEnrichedPt5_TuneZ2star_8TeV_pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM',    10365230, 801, 0.10, 0.0218*8.08e6),
    MCSample('qcdmu0080', 'QCDmu5, 80 < #hat{p}_{T} < 120 GeV',   '/QCD_Pt-80to120_MuEnrichedPt5_TuneZ2star_8TeV_pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM',    9238642, 801, 0.10, 0.0395*1.02e6),
    MCSample('qcdmu0120', 'QCDmu5, 120 < #hat{p}_{T} < 170 GeV',  '/QCD_Pt-120to170_MuEnrichedPt5_TuneZ2star_8TeV_pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM',   8501935, 801, 0.10, 0.0473*1.58e5),
    MCSample('qcdmu0170', 'QCDmu5, 170 < #hat{p}_{T} < 300 GeV',  '/QCD_Pt-170to300_MuEnrichedPt5_TuneZ2star_8TeV_pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM',   7670288, 801, 0.10, 0.0676*3.40e4),
    MCSample('qcdmu0300', 'QCDmu5, 300 < #hat{p}_{T} < 470 GeV',  '/QCD_Pt-300to470_MuEnrichedPt5_TuneZ2star_8TeV_pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM',   7839607, 801, 0.10, 0.0864*1.76e3),
    MCSample('qcdmu0470', 'QCDmu5, 470 < #hat{p}_{T} < 600 GeV',  '/QCD_Pt-470to600_MuEnrichedPt5_TuneZ2star_8TeV_pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM',   3783069, 801, 0.10, 0.1024*1.15e2),
    MCSample('qcdmu0600', 'QCDmu5, 600 < #hat{p}_{T} < 800 GeV',  '/QCD_Pt-600to800_MuEnrichedPt5_TuneZ2star_8TeV_pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM',   4119000, 801, 0.10, 0.0996*2.70e1),
    MCSample('qcdmu0800', 'QCDmu5, 800 < #hat{p}_{T} < 1000 GeV', '/QCD_Pt-800to1000_MuEnrichedPt5_TuneZ2star_8TeV_pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM',  4108881, 801, 0.10, 0.1033*3.57e0),
    MCSample('qcdmu1000', 'QCDmu5, #hat{p}_{T} > 1000 GeV',       '/QCD_Pt-1000_MuEnrichedPt5_TuneZ2star_8TeV_pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM',       3873970, 801, 0.10, 0.1097*7.74e-1),

    MCSample('qcdmupt15', 'QCD, #hat{p}_{T} > 20 GeV, #mu p_{T} > 15 GeV', '/QCD_Pt_20_MuEnrichedPt_15_TuneZ2star_8TeV_pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM', 7529312, 801, 0.10, 3.64e8*3.7e-4),
]

stop_signal_samples = [
    MCSample('pythiastopm200',  'stop pair prod., M = 200 GeV',  '/sstop_genfsimreco_test/tucker-sstop_genfsimreco_test-15c4250952b10a469cc6da8beaecd65e/USER', 93000,  2, 0.15, 17),
    MCSample('smsT2ttFineBin',  'stop pair production',          '/SMS-T2tt_FineBin_Mstop-225to1200_mLSP-0to1000_8TeV-Pythia6Z/Summer12-START52_V9_FSIM-v1/AODSIM', 99944645, 2, 0.15, -1),
    ]

mfv_signal_samples = [
    MCSample('mfv3j_gluino_tau0000um_M0200', 'MFV signal, M = 200 GeV, #tau = 0',         '/mfv_genfsimreco_gluino_tau0000um_M200/tucker-mfv_genfsimreco_gluino_tau0000um_M200-adc7f942f50ab1cea63def6ed5bff99b/USER',    97998, -1, 0.2, 1),
    MCSample('mfv3j_gluino_tau0000um_M0400', 'MFV signal, M = 400 GeV, #tau = 0',         '/mfv_genfsimreco_gluino_tau0000um_M400/tucker-mfv_genfsimreco_gluino_tau0000um_M400-adc7f942f50ab1cea63def6ed5bff99b/USER',    98998, -1, 0.2, 1),
    MCSample('mfv3j_gluino_tau0000um_M0600', 'MFV signal, M = 600 GeV, #tau = 0',         '/mfv_genfsimreco_gluino_tau0000um_M600/tucker-mfv_genfsimreco_gluino_tau0000um_M600-adc7f942f50ab1cea63def6ed5bff99b/USER',    97999, -1, 0.2, 1),
    MCSample('mfv3j_gluino_tau0000um_M0800', 'MFV signal, M = 800 GeV, #tau = 0',         '/mfv_genfsimreco_gluino_tau0000um_M800/tucker-mfv_genfsimreco_gluino_tau0000um_M800-adc7f942f50ab1cea63def6ed5bff99b/USER',    18400, -1, 0.2, 1),
    MCSample('mfv3j_gluino_tau0000um_M1000', 'MFV signal, M = 1000 GeV, #tau = 0',        '/mfv_genfsimreco_gluino_tau0000um_M1000/tucker-mfv_genfsimreco_gluino_tau0000um_M1000-adc7f942f50ab1cea63def6ed5bff99b/USER',  85397, -1, 0.2, 1),
    MCSample('mfv3j_gluino_tau0010um_M0200', 'MFV signal, M = 200 GeV, #tau = 10 #mum',   '/mfv_genfsimreco_gluino_tau0010um_M200/tucker-mfv_genfsimreco_gluino_tau0010um_M200-2a899b36d80e4d3e25d055674a795172/USER',    94597, -1, 0.2, 1),
    MCSample('mfv3j_gluino_tau0010um_M0400', 'MFV signal, M = 400 GeV, #tau = 10 #mum',   '/mfv_genfsimreco_gluino_tau0010um_M400/tucker-mfv_genfsimreco_gluino_tau0010um_M400-2a899b36d80e4d3e25d055674a795172/USER',    96196, -1, 0.2, 1),
    MCSample('mfv3j_gluino_tau0010um_M0600', 'MFV signal, M = 600 GeV, #tau = 10 #mum',   '/mfv_genfsimreco_gluino_tau0010um_M600/tucker-mfv_genfsimreco_gluino_tau0010um_M600-2a899b36d80e4d3e25d055674a795172/USER',    81200, -1, 0.2, 1),
    MCSample('mfv3j_gluino_tau0010um_M0800', 'MFV signal, M = 800 GeV, #tau = 10 #mum',   '/mfv_genfsimreco_gluino_tau0010um_M800/tucker-mfv_genfsimreco_gluino_tau0010um_M800-2a899b36d80e4d3e25d055674a795172/USER',    93796, -1, 0.2, 1),
    MCSample('mfv3j_gluino_tau0010um_M1000', 'MFV signal, M = 1000 GeV, #tau = 10 #mum',  '/mfv_genfsimreco_gluino_tau0010um_M1000/tucker-mfv_genfsimreco_gluino_tau0010um_M1000-2a899b36d80e4d3e25d055674a795172/USER',  95799, -1, 0.2, 1),
    MCSample('mfv3j_gluino_tau0100um_M0200', 'MFV signal, M = 200 GeV, #tau = 100 #mum',  '/mfv_genfsimreco_gluino_tau0100um_M200/tucker-mfv_genfsimreco_gluino_tau0100um_M200-6659e500e34fc490bde56b86ad08e337/USER',    94996, -1, 0.2, 1),
    MCSample('mfv3j_gluino_tau0100um_M0400', 'MFV signal, M = 400 GeV, #tau = 100 #mum',  '/mfv_genfsimreco_gluino_tau0100um_M400/tucker-mfv_genfsimreco_gluino_tau0100um_M400-6659e500e34fc490bde56b86ad08e337/USER',    94997, -1, 0.2, 1),
    MCSample('mfv3j_gluino_tau0100um_M0600', 'MFV signal, M = 600 GeV, #tau = 100 #mum',  '/mfv_genfsimreco_gluino_tau0100um_M600/tucker-mfv_genfsimreco_gluino_tau0100um_M600-6659e500e34fc490bde56b86ad08e337/USER',    97199, -1, 0.2, 1),
    MCSample('mfv3j_gluino_tau0100um_M0800', 'MFV signal, M = 800 GeV, #tau = 100 #mum',  '/mfv_genfsimreco_gluino_tau0100um_M800/tucker-mfv_genfsimreco_gluino_tau0100um_M800-6659e500e34fc490bde56b86ad08e337/USER',    80799, -1, 0.2, 1),
    MCSample('mfv3j_gluino_tau0100um_M1000', 'MFV signal, M = 1000 GeV, #tau = 100 #mum', '/mfv_genfsimreco_gluino_tau0100um_M1000/tucker-mfv_genfsimreco_gluino_tau0100um_M1000-6659e500e34fc490bde56b86ad08e337/USER',  96200, -1, 0.2, 1),
    MCSample('mfv3j_gluino_tau1000um_M0200', 'MFV signal, M = 200 GeV, #tau = 1 mm',      '/mfv_genfsimreco_gluino_tau1000um_M200/tucker-mfv_genfsimreco_gluino_tau1000um_M200-e47fc4979466aacf88f2c30cc52afb0f/USER',    94996, -1, 0.2, 1),
    MCSample('mfv3j_gluino_tau1000um_M0400', 'MFV signal, M = 400 GeV, #tau = 1 mm',      '/mfv_genfsimreco_gluino_tau1000um_M400/tucker-mfv_genfsimreco_gluino_tau1000um_M400-e47fc4979466aacf88f2c30cc52afb0f/USER',    72800, -1, 0.2, 1),
    MCSample('mfv3j_gluino_tau1000um_M0600', 'MFV signal, M = 600 GeV, #tau = 1 mm',      '/mfv_genfsimreco_gluino_tau1000um_M600/tucker-mfv_genfsimreco_gluino_tau1000um_M600-e47fc4979466aacf88f2c30cc52afb0f/USER',    89399, -1, 0.2, 1),
    MCSample('mfv3j_gluino_tau1000um_M0800', 'MFV signal, M = 800 GeV, #tau = 1 mm',      '/mfv_genfsimreco_gluino_tau1000um_M800/tucker-mfv_genfsimreco_gluino_tau1000um_M800-e47fc4979466aacf88f2c30cc52afb0f/USER',    94600, -1, 0.2, 1),
    MCSample('mfv3j_gluino_tau1000um_M1000', 'MFV signal, M = 1000 GeV, #tau = 1 mm',     '/mfv_genfsimreco_gluino_tau1000um_M1000/tucker-mfv_genfsimreco_gluino_tau1000um_M1000-e47fc4979466aacf88f2c30cc52afb0f/USER',  93798, -1, 0.2, 1),
    MCSample('mfv3j_gluino_tau4000um_M0200', 'MFV signal, M = 200 GeV, #tau = 4 mm',      '/mfv_genfsimreco_gluino_tau4000um_M200/tucker-mfv_genfsimreco_gluino_tau4000um_M200-088b3b49967ef59b0610526875f2bb9f/USER',    91399, -1, 0.2, 1),
    MCSample('mfv3j_gluino_tau4000um_M0400', 'MFV signal, M = 400 GeV, #tau = 4 mm',      '/mfv_genfsimreco_gluino_tau4000um_M400/tucker-mfv_genfsimreco_gluino_tau4000um_M400-088b3b49967ef59b0610526875f2bb9f/USER',    85799, -1, 0.2, 1),
    MCSample('mfv3j_gluino_tau4000um_M0600', 'MFV signal, M = 600 GeV, #tau = 4 mm',      '/mfv_genfsimreco_gluino_tau4000um_M600/tucker-mfv_genfsimreco_gluino_tau4000um_M600-088b3b49967ef59b0610526875f2bb9f/USER',    95199, -1, 0.2, 1),
    MCSample('mfv3j_gluino_tau4000um_M0800', 'MFV signal, M = 800 GeV, #tau = 4 mm',      '/mfv_genfsimreco_gluino_tau4000um_M800/tucker-mfv_genfsimreco_gluino_tau4000um_M800-088b3b49967ef59b0610526875f2bb9f/USER',    86799, -1, 0.2, 1),
    MCSample('mfv3j_gluino_tau4000um_M1000', 'MFV signal, M = 1000 GeV, #tau = 4 mm',     '/mfv_genfsimreco_gluino_tau4000um_M1000/tucker-mfv_genfsimreco_gluino_tau4000um_M1000-088b3b49967ef59b0610526875f2bb9f/USER',  96998, -1, 0.2, 1),
    MCSample('mfv3j_gluino_tau9900um_M0200', 'MFV signal, M = 200 GeV, #tau = 9.9 mm',    '/mfv_genfsimreco_gluino_tau9900um_M200/tucker-mfv_genfsimreco_gluino_tau9900um_M200-e8f47d721e19ae8437a32cb76683750e/USER',    93994, -1, 0.2, 1),
    MCSample('mfv3j_gluino_tau9900um_M0400', 'MFV signal, M = 400 GeV, #tau = 9.9 mm',    '/mfv_genfsimreco_gluino_tau9900um_M400/tucker-mfv_genfsimreco_gluino_tau9900um_M400-e8f47d721e19ae8437a32cb76683750e/USER',    96399, -1, 0.2, 1),
    MCSample('mfv3j_gluino_tau9900um_M0600', 'MFV signal, M = 600 GeV, #tau = 9.9 mm',    '/mfv_genfsimreco_gluino_tau9900um_M600/tucker-mfv_genfsimreco_gluino_tau9900um_M600-e8f47d721e19ae8437a32cb76683750e/USER',    75599, -1, 0.2, 1),
    MCSample('mfv3j_gluino_tau9900um_M0800', 'MFV signal, M = 800 GeV, #tau = 9.9 mm',    '/mfv_genfsimreco_gluino_tau9900um_M800/tucker-mfv_genfsimreco_gluino_tau9900um_M800-e8f47d721e19ae8437a32cb76683750e/USER',    97197, -1, 0.2, 1),
    MCSample('mfv3j_gluino_tau9900um_M1000', 'MFV signal, M = 1000 GeV, #tau = 9.9 mm',   '/mfv_genfsimreco_gluino_tau9900um_M1000/tucker-mfv_genfsimreco_gluino_tau9900um_M1000-e8f47d721e19ae8437a32cb76683750e/USER',  96795, -1, 0.2, 1),
    ]

data_samples = [
    DataSample('MultiJetPrompt12A',    '/MultiJet/Run2012A-PromptReco-v1/AOD'),
    DataSample('MultiJetPrompt12B',    '/MultiJet/Run2012B-PromptReco-v1/AOD'),
    DataSample('MuHadPrompt12A',       '/MuHad/Run2012A-PromptReco-v1/AOD'),
    DataSample('MuHadPrompt12B',       '/MuHad/Run2012B-PromptReco-v1/AOD'),
]    

all_mc_samples = background_samples + auxiliary_background_samples + stop_signal_samples + mfv_signal_samples 
all_samples = data_samples + all_mc_samples

for sample in all_samples:
    exec '%s = sample' % sample.name


# Exceptions to the defaults.

singletop_t.scheduler_name = 'condor'

pythiastopm200.dbs_url_num = 2
pythiastopm200.is_fastsim = True
pythiastopm200.ana_hash = 'd1c7726c69d89f45da05a992a40b425c'

smsT2ttFineBin.is_fastsim = True

for sample in mfv_signal_samples:
    mo = re.search(r'tau0*(\d+)um_M0*(\d+)', s.name)
    sample.tau  = int(mo.group(1))
    sample.mass = int(mo.group(2))

    sample.ana_hash = 'ffbc82b68f588f5f183a150670744b16'
    sample.is_fastsim = True
    sample.is_pythia8 = True
    sample.dbs_url_num = 2
    sample.ana_version = 'vX'

# Other exceptions due to jobs being missed, mixing dataset versions
# (that don't affect actual physics), etc.

warning = []
for sample in (qcd0170, qcd0600, dyjetstollM10, dyjetstollM50, singletop_tW, singletop_s, singletop_t, singletop_s_tbar, singletop_t_tbar, wjetstolnu, ttbar, ww, wz, zz):
    warning.append(sample.name)
    sample.ana_version = 'v3'
    sample.ana_hash = '5e1021f6ad80ccbe13b7c6abc1eb101a'
big_warn('other datasets v2, these datasets v3:\n' + ', '.join(warning))

for sample in (ttbar, ww, wz, zz):
    sample.ana_hash = 'e652915bbe1a42db11af87351dcd4bba'

temp_neventses = []
temp_neventses = [(qcd0015, 10918100), (qcd0050, 5306688), (qcd0120, 5235732), (ttbar, 6917788), (ww, 2391447), (wz, 9896622)]
if temp_neventses:
    warning = ['partial datasets published:']
    for sample, temp_nevents in temp_neventses:
        if temp_nevents > sample.nevents:
            raise ValueError('for sample %s, will not set temp nevents to %i, greater than original %i' % (sample.name, temp_nevents, sample.nevents))
        elif temp_nevents == sample.nevents:
            warning.append('sample %s: temp nevents %i is equal to original' % (sample.name, temp_nevents))
        else:
            warning.append('sample %s: new temp nevents %i (original %i, weight increased by %.1f%%)' % (sample.name, temp_nevents, sample.nevents, 100.*sample.nevents/temp_nevents))
            sample.nevents = temp_nevents
    big_warn('\n'.join(warning))

not_ready = [ttgjets, ttwjets, ttzjets, smsT2ttFineBin, zz] + auxiliary_background_samples + mfv_signal_samples
big_warn('samples not ana_ready: %s' % ' '.join(s.name for s in not_ready))
for sample in not_ready:
    sample.ana_ready = False

__all__ = ['data_samples', 'background_samples', 'auxiliary_background_samples', 'stop_signal_samples', 'mfv_signal_samples']
__all__ += [s.name for s in all_samples]

if __name__ == '__main__':
    import sys
    if 'sites' in sys.argv:
        from mydbs import *
        for sample in _samples:
            sites = sites_for_dataset(sample.dataset)
            print '%20s%15s %s' % (sample.name, num_events(sample.dataset), 'AT fnal' if [x for x in sites if 'fnal' in x] else 'NOT at fnal')
    elif 'checkpubnumfiles' in sys.argv:
        fmt = '%160s%15s'
        print fmt % ('ana_dataset', 'num files')
        for sample in _samples:
            print fmt % (sample.ana_dataset, len(sample.filenames))
    elif 'numevents' in sys.argv:
        from DBS import *
        for name, nn, ds in auxiliary_background_samples:
            print name, numevents_in_dataset(ds)
    elif 'mfvsignals' in sys.argv:
        line_re = re.compile(r'total events: (\d+) in dataset: (/.*USER)')
        dataset_re = re.compile(r'tau0*(\d+)um_M(\d+)-([0-9a-f]*)/USER')
        nice = {0: '0', 10: '10 #mum', 100: '100 #mum', 1000: '1 mm', 4000: '4 mm', 9900: '9.9 mm'}
        lines = []
        for arg in sys.argv:
            if os.path.isfile(arg) and 'publish' in arg:
                for line in open(arg):
                    mo = line_re.search(line)
                    if mo is not None:
                        nevents = int(mo.group(1))
                        dataset = mo.group(2)
                        tau, mass, hash = dataset_re.search(dataset).groups()
                        tau = int(tau)
                        mass = int(mass)
                        tau_nice = nice[tau]
                        #print nevents, dataset, tau, mass, hash
                        lines.append((tau, mass, "MCSample('mfv3j_gluino_tau%(tau)04ium_M%(mass)04i', 'MFV signal, M = %(mass)i GeV, #tau = %(tau_nice)s', '%(dataset)s', %(nevents)6i, -1, 0.2, 1)," % locals()))
                        break
        lines.sort()
        for tau, mass, line in lines:
            print line
