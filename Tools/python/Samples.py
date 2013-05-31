#!/usr/bin/env python

import os, re, sys
from copy import copy
from JMTucker.Tools.DBS import files_in_dataset
from JMTucker.Tools.general import big_warn

########################################################################

class Sample(object):
    PARENT_DATASET = None
    IS_MC = True
    IS_FASTSIM = False
    IS_PYTHIA8 = False
    SCHEDULER_NAME = 'remoteGlidein'
    HLT_PROCESS_NAME = 'HLT'
    DBS_URL_NUM = 0
    ANA_DBS_URL_NUM = 2
    ANA_HASH = 'ce0f36575948071c2bc4232b86e12d14'
    PUBLISH_USER = 'tucker'
    ANA_VERSION = 'v6'

    def __init__(self, name, nice_name, dataset):
        self.name = name
        self.nice_name = nice_name
        self.dataset = dataset

        self.parent_dataset = self.PARENT_DATASET
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
        self.ana_ready = False

    def dump(self):
        xx = 'name nice_name dataset parent_dataset is_mc is_fastsim is_pythia8 scheduler_name dbs_url_num ana_ready ana_dbs_url_num ana_hash publish_user ana_version'
        for x in xx.split():
            a = getattr(self, x)
            if hasattr(self, x.upper()) and a == getattr(self, x.upper()):
                continue
            print x, ':', a

    @property
    def scheduler(self):
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
        return '/%(primary_dataset)s/%(publish_user)s-jtuple_%(ana_version)s-%(ana_hash)s/USER' % self

    @property
    def use_server(self):
        return ''

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

########################################################################

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
events_per_job = 25000
'''

########################################################################

class TupleOnlyMCSample(MCSample):
    def __init__(self, name, dataset, events_per=25000, max_events=-1):
        super(TupleOnlyMCSample, self).__init__(name, '', dataset, -1, -1, -1, -1)
        self.events_per = events_per
        self.max_events = max_events

    @property
    def job_control(self):
        return '''
total_number_of_events = %(max_events)s
events_per_job = %(events_per)s
''' % self

########################################################################

class DataSample(Sample):
    IS_MC = False
    PROMPT_JSON = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions12/8TeV/Prompt/Cert_190456-207469_8TeV_PromptReco_Collisions12_JSON.txt'

    def __init__(self, name, dataset, run_range=None):
        super(DataSample, self).__init__(name, name, dataset)

        self.run_range = run_range
        self.json = self.PROMPT_JSON

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

########################################################################

# https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat8TeV or PREP for xsecs
background_samples = [
    #        name                title                                                      dataset                                                                                                nevents  clr  syst  xsec (pb)
    MCSample('wjetstolnu',       'W + jets #rightarrow l#nu',                               '/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball/Summer12_DR53X-PU_S10_START53_V7A-v2/AODSIM',           57709905,   9, 0.10, 3.04e4),
    MCSample('ttbarhadronic',    't#bar{t}, hadronic',                                      '/TTJets_HadronicMGDecays_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A_ext-v1/AODSIM',             31223821,   4, 0.15, 225.2 * 0.457),
    MCSample('ttbarsemilep',     't#bar{t}, semileptonic',                                  '/TTJets_SemiLeptMGDecays_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A_ext-v1/AODSIM',             25424818,   4, 0.15, 225.2 * 0.438),
    MCSample('ttbardilep',       't#bar{t}, dileptonic',                                    '/TTJets_FullLeptMGDecays_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v2/AODSIM',                 12119013,   4, 0.15, 225.2 * 0.105),
    MCSample('qcdht0100',        'QCD, 100 < H_{T} < 250 GeV',                              '/QCD_HT-100To250_TuneZ2star_8TeV-madgraph-pythia/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM',       50129518, 801, 0.10, 1.04e7),
    MCSample('qcdht0250',        'QCD, 250 < H_{T} < 500 GeV',                              '/QCD_HT-250To500_TuneZ2star_8TeV-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM',      27062078, 801, 0.10, 2.76e5),
    MCSample('qcdht0500',        'QCD, 500 < H_{T} < 1000 GeV',                             '/QCD_HT-500To1000_TuneZ2star_8TeV-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM',     30599292, 801, 0.10, 8.43e3),
    MCSample('qcdht1000',        'QCD, H_{T} > 1000 GeV',                                   '/QCD_HT-1000ToInf_TuneZ2star_8TeV-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM',     13843863, 801, 0.10, 2.04e2),
    ]

auxiliary_background_samples = [
    MCSample('ttbarincl',        't#bar{t}',                                                '/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM', 6923750,   4, 0.15, 225.2),
    MCSample('ttzjets',          't#bar{t}+Z',                                              '/TTZJets_8TeV-madgraph_v2/Summer12-PU_S7_START52_V9-v1/AODSIM',                                        209741,  -1, 0.20, 0.172),
    MCSample('ttwjets',          't#bar{t}+W',                                              '/TTWJets_8TeV-madgraph/Summer12-PU_S7_START52_V9-v1/AODSIM',                                           195301,  -1, 0.20, 0.215),
    MCSample('ttgjets',          't#bar{t}+#gamma',                                         '/TTGJets_8TeV-madgraph/Summer12-PU_S7_START52_V9-v1/AODSIM',                                            71598,  -1, 0.20, 1.44),
    MCSample('singletop_s',      'single t (s-channel)',                                    '/T_s-channel_TuneZ2star_8TeV-powheg-tauola/Summer12-PU_S7_START52_V9-v1/AODSIM',                       259961,  -1, 0.20, 3.79),
    MCSample('singletop_s_tbar', 'single #bar{t} (s-channel)',                              '/Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola/Summer12-PU_S7_START52_V9-v1/AODSIM',                    139974,  -1, 0.20, 1.76),
    MCSample('singletop_t',      'single t (t-channel)',                                    '/T_t-channel_TuneZ2star_8TeV-powheg-tauola/Summer12-PU_S7_START52_V9-v2/AODSIM',                      3780839,  -1, 0.20, 56.4),
    MCSample('singletop_t_tbar', 'single #bar{t} (t-channel)',                              '/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola/Summer12-PU_S7_START52_V9-v1/AODSIM',                   1935072,  -1, 0.20, 30.7),
    MCSample('singletop_tW',     'single t (tW)',                                           '/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/Summer12-PU_S7_START52_V9-v1/AODSIM',                   497658,  42, 0.20, 11.1),
    MCSample('singletop_tW_tbar','single t (#bar{t}W)',                                     '/Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/Summer12-PU_S7_START52_V9-v1/AODSIM',                493460,  42, 0.20, 11.1),
    MCSample('ww',               'WW',                                                      '/WW_TuneZ2star_8TeV_pythia6_tauola/Summer12-PU_S7_START52_V9-v1/AODSIM',                             10000431,   4, 0.04, 57.1),
    MCSample('wz',               'WZ',                                                      '/WZ_TuneZ2star_8TeV_pythia6_tauola/Summer12-PU_S7_START52_V9-v1/AODSIM',                              9996622,  30, 0.04, 32.3),
    MCSample('zz',               'ZZ',                                                      '/ZZ_TuneZ2star_8TeV_pythia6_tauola/Summer12-PU_S7_START52_V9-v1/AODSIM',                              9799908,   6, 0.03, 8.3),
    MCSample('zjetstonunuHT050', 'Z #rightarrow #nu#nu + jets, 50 < H_{T} < 100 GeV',       '/ZJetsToNuNu_50_HT_100_TuneZ2Star_8TeV_madgraph/Summer12-PU_S7_START52_V9-v1/AODSIM',                 4053786,  -1, 0.10, 3.81e2),
    MCSample('zjetstonunuHT100', 'Z #rightarrow #nu#nu + jets, 100 < H_{T} < 200 GeV',      '/ZJetsToNuNu_100_HT_200_TuneZ2Star_8TeV_madgraph/Summer12-PU_S7_START52_V9-v1/AODSIM',                4416646,  -1, 0.10, 1.60e2),
    MCSample('zjetstonunuHT200', 'Z #rightarrow #nu#nu + jets, 200 < H_{T} < 400 GeV',      '/ZJetsToNuNu_200_HT_400_TuneZ2Star_8TeV_madgraph/Summer12-PU_S7_START52_V9-v3/AODSIM',                5066608,  -1, 0.10, 4.15e1),
    MCSample('zjetstonunuHT400', 'Z #rightarrow #nu#nu + jets, H_{T} > 400 GeV',            '/ZJetsToNuNu_400_HT_inf_TuneZ2Star_8TeV_madgraph/Summer12-PU_S7_START52_V9-v1/AODSIM',                1006928,  -1, 0.10, 5.27e0),
    MCSample('dyjetstollM10',    'DY + jets #rightarrow ll, 10 < M < 50 GeV',               '/DYJetsToLL_M-10To50filter_8TeV-madgraph/Summer12-PU_S7_START52_V9-v1/AODSIM',                        7132223,  -1, 0.10, 11050*0.069),
    MCSample('dyjetstollM50',    'DY + jets #rightarrow ll, M > 50 GeV',                    '/DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball/Summer12-PU_S7_START52_V9-v2/AODSIM',              30461028,  -1, 0.10, 2.95e3),

    MCSample('qcd0000', 'QCD, #hat{p}_{T} < 5 GeV',           '/QCD_Pt-0to5_TuneZ2star_8TeV_pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM',         999788, 801, 0.10, 4.859e10),
    MCSample('qcd0005', 'QCD, 5 < #hat{p}_{T} < 15 GeV',      '/QCD_Pt-5to15_TuneZ2star_8TeV_pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM',       1489184, 802, 0.10, 4.264e10),
    MCSample('qcd0015', 'QCD, 15 < #hat{p}_{T} < 30 GeV',     '/QCD_Pt-15to30_TuneZ2star_8TeV_pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM',     10925056, 803, 0.10, 9.883e08),
    MCSample('qcd0030', 'QCD, 30 < #hat{p}_{T} < 50 GeV',     '/QCD_Pt-30to50_TuneZ2star_8TeV_pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM',      6000000, 804, 0.10, 6.629e07),
    MCSample('qcd0050', 'QCD, 50 < #hat{p}_{T} < 80 GeV',     '/QCD_Pt-50to80_TuneZ2star_8TeV_pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM',      5995944, 805, 0.10, 8.149e06),
    MCSample('qcd0080', 'QCD, 80 < #hat{p}_{T} < 120 GeV',    '/QCD_Pt-80to120_TuneZ2star_8TeV_pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM',     5981328, 806, 0.10, 1.034e06),
    MCSample('qcd0120', 'QCD, 120 < #hat{p}_{T} < 170 GeV',   '/QCD_Pt-120to170_TuneZ2star_8TeV_pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM',    5985732, 807, 0.10, 1.563e05),
    MCSample('qcd0170', 'QCD, 170 < #hat{p}_{T} < 300 GeV',   '/QCD_Pt-170to300_TuneZ2star_8TeV_pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM',    5814398, 808, 0.10, 3.414e04),
    MCSample('qcd0300', 'QCD, 300 < #hat{p}_{T} < 470 GeV',   '/QCD_Pt-300to470_TuneZ2star_8TeV_pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM',    5927300, 809, 0.10, 1.760e03),
    MCSample('qcd0470', 'QCD, 470 < #hat{p}_{T} < 600 GeV',   '/QCD_Pt-470to600_TuneZ2star_8TeV_pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM',    3994848, 810, 0.10, 1.139e02),
    MCSample('qcd0600', 'QCD, 600 < #hat{p}_{T} < 800 GeV',   '/QCD_Pt-600to800_TuneZ2star_8TeV_pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM',    3992760, 811, 0.10, 2.699e01),
    MCSample('qcd0800', 'QCD, 800 < #hat{p}_{T} < 1000 GeV',  '/QCD_Pt-800to1000_TuneZ2star_8TeV_pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM',   3998563, 812, 0.10, 3.550e00),
    MCSample('qcd1000', 'QCD, 1000 < #hat{p}_{T} < 1400 GeV', '/QCD_Pt-1000to1400_TuneZ2star_8TeV_pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM',  1964088, 813, 0.10, 7.378e-1),
    MCSample('qcd1400', 'QCD, 1400 < #hat{p}_{T} < 1800 GeV', '/QCD_Pt-1400to1800_TuneZ2star_8TeV_pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM',  2000062, 814, 0.10, 3.352e-2),
    MCSample('qcd1800', 'QCD, #hat{p}_{T} > 1800 GeV',        '/QCD_Pt-1800_TuneZ2star_8TeV_pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM',         977586, 815, 0.10, 1.829e-3),
    
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

########################################################################

mfv_signal_samples_ex = [
    (1000,  400, 'c9c4c27381f6625ed3d8394ffaf0b9cd'),
    (   0,  400, '3e730b2f07d27fadb85eb50c5002cc81'),
    (9900,  400, 'c91fb7b9ece3e3abc0445dc6699e16d6'),
    (1000, 1000, 'c9c4c27381f6625ed3d8394ffaf0b9cd'),
    ]

mfv_signal_samples_nice = {0: '0', 10: '10 #mum', 100: '100 #mum', 1000: '1 mm', 4000: '4 mm', 9900: '9.9 mm'}

mfv_signal_samples = []
for tau, mass, gensimhlt_hash in mfv_signal_samples_ex:
    name_frag = 'neutralino_tau%04ium_M%04i' % (tau, mass)
    s = MCSample('mfv_' + name_frag,
                 'MFV signal, M = %i GeV, #tau = %s' % (mass, mfv_signal_samples_nice[tau]),
                 '/mfv_%s/tucker-reco-a3f0d9ac5e396df027589da2067010b0/USER' % name_frag,
                 10000, -1, 0.2, 1)
    s.ana_hash = '547d3313903142038335071634b26604'
    s.parent_dataset = '/mfv_%(name_frag)s/tucker-mfv_%(name_frag)s-%(gensimhlt_hash)s/USER' % locals()
    s.tau  = tau
    s.mass = mass
    s.is_pythia8 = True
    s.dbs_url_num = 2
    mfv_signal_samples.append(s)

########################################################################

data_samples = []    
auxiliary_data_samples = []

########################################################################

all_data_samples = data_samples + auxiliary_data_samples
all_mc_samples = background_samples + auxiliary_background_samples + mfv_signal_samples 
all_samples = all_data_samples + all_mc_samples

for sample in all_samples:
    exec '%s = sample' % sample.name

########################################################################

# Exceptions to the defaults.

singletop_t.scheduler_name = 'condor'

for sample in background_samples + auxiliary_background_samples + all_data_samples:
    sample.ana_ready = False
    
# Other exceptions due to jobs being missed, mixing dataset versions
# (that don't affect actual physics), etc.

temp_neventses = []
not_ready = []

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

if not_ready:
    big_warn('samples not ana_ready: %s' % ' '.join(s.name for s in not_ready))
for sample in not_ready:
    sample.ana_ready = False

########################################################################

__all__ = ['data_samples', 'auxiliary_data_samples', 'background_samples', 'auxiliary_background_samples', 'mfv_signal_samples']
__all__ += [s.name for s in all_samples]

if __name__ == '__main__':
    if 'dump' in sys.argv:
        for sample in all_samples:
            sample.dump()
            print
    elif 'sites' in sys.argv:
        from mydbs import *
        for sample in all_samples:
            sites = sites_for_dataset(sample.dataset)
            print '%20s%15s %s' % (sample.name, num_events(sample.dataset), 'AT fnal' if [x for x in sites if 'fnal' in x] else 'NOT at fnal')
