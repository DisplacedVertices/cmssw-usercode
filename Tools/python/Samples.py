#!/usr/bin/env python

import os, re, sys
from copy import copy
from fnmatch import fnmatch
import JMTucker.Tools.DBS as DBS
from JMTucker.Tools.ROOTTools import ROOT
from JMTucker.Tools.general import big_warn

########################################################################

class Sample(object):
    PARENT_DATASET = None
    IS_MC = True
    IS_FASTSIM = False
    IS_PYTHIA8 = False
    NO_SKIMMING_CUTS = False
    RE_PAT = False
    SCHEDULER = 'remoteGlidein'
    ANA_SCHEDULER = 'condor'
    HLT_PROCESS_NAME = 'HLT'
    DBS_URL_NUM = 0
    ANA_DBS_URL_NUM = 3
    ANA_HASH = 'c761ddfa7f093d8f86a338439e06a1d4'
    PUBLISH_USER = 'tucker'
    ANA_VERSION = 'v18'

    def __init__(self, name, nice_name, dataset):
        self.name = name
        self.nice_name = nice_name
        self.dataset = dataset
        self.ana_dataset_override = None
        
        self.parent_dataset = self.PARENT_DATASET
        self.is_mc = self.IS_MC
        self.is_fastsim = self.IS_FASTSIM
        self.is_pythia8 = self.IS_PYTHIA8
        self.no_skimming_cuts = self.NO_SKIMMING_CUTS
        self.re_pat = self.RE_PAT
        self.hlt_process_name = self.HLT_PROCESS_NAME
        self.local_filenames = []
        self.scheduler = self.SCHEDULER
        self.ana_scheduler = self.ANA_SCHEDULER
        self.dbs_url_num = self.DBS_URL_NUM
        self.ana_dbs_url_num = self.ANA_DBS_URL_NUM
        self.ana_hash = self.ANA_HASH
        self.publish_user = self.PUBLISH_USER
        self.ana_version = self.ANA_VERSION
        self.ana_ready = False

    def dump(self, dump_all=False):
        xx = 'name nice_name dataset parent_dataset is_mc is_fastsim is_pythia8 scheduler_name dbs_url_num ana_ready ana_dbs_url_num ana_hash publish_user ana_version ana_dataset'
        for x in xx.split():
            a = getattr(self, x)
            if not dump_all and hasattr(self, x.upper()) and a == getattr(self, x.upper()):
                continue
            print x, ':', a

    def _get_dbs_url(self, num):
        if num < 0 or num > 3:
            raise ValueError('only supported nums for dbs_url are 0 (global) - 3')
        return '' if not num else 'dbs_url = phys0%i' % num
    
    @property
    def dbs_url(self):
        return self._get_dbs_url(self.dbs_url_num)
        
    @property
    def ana_dbs_url(self):
        return self._get_dbs_url(self.ana_dbs_url_num)

    def dbs_inst_dict(self, num):
        return dict(('ana0%i' % i, num == i) for i in xrange(1,4))

    @property
    def primary_dataset(self):
        return self.dataset.split('/')[1]
    
    @property
    def ana_dataset(self):
        if self.ana_dataset_override is not None:
            return self.ana_dataset_override
        return '/%(primary_dataset)s/%(publish_user)s-mfvntuple_%(ana_version)s-%(ana_hash)s/USER' % self

    def filenames(self, ana=True):
        # Return a list of filenames for running the histogrammer not
        # using crab.
        if self.local_filenames:
            return self.local_filenames
        if ana:
            return DBS.files_in_dataset(self.ana_dataset, **self.dbs_inst_dict(self.ana_dbs_url_num))
        else:
            return DBS.files_in_dataset(self.dataset,     **self.dbs_inst_dict(self.dbs_url_num))

    def __getitem__(self, key):
        return getattr(self, key)

    def _dump(self, redump_existing=False):
        dst = os.path.join('/uscmst1b_scratch/lpc1/3DayLifetime/tucker', self.name)
        os.system('mkdir ' + dst)
        for fn in self.filenames:
            print fn
            if redump_existing or not os.path.isfile(os.path.join(dst, os.path.basename(fn))):
                os.system('dccp ~%s %s/' % (fn,dst))

    def job_control_commands(self):
        raise NotImplementedError('job_control_commands needs to be implemented')

    @property
    def job_control(self):
        return '\n'.join('%s = %s' % cmd for cmd in self.job_control_commands)

########################################################################

class MCSample(Sample):
    EVENTS_PER = 5000
    ANA_EVENTS_PER = 100000
    TOTAL_EVENTS = -1
    
    def __init__(self, name, nice_name, dataset, nevents, color, syst_frac, cross_section, k_factor=1):
        super(MCSample, self).__init__(name, nice_name, dataset)
        
        self.nevents_orig = nevents
        self.color = color
        self.syst_frac = float(syst_frac)
        self.cross_section = float(cross_section)
        self.k_factor = float(k_factor)
        self.join_info = (False, self.nice_name, self.color)
        self.ana_filter_eff = -1.

        self.events_per = self.EVENTS_PER
        self.ana_events_per = self.ANA_EVENTS_PER
        self.total_events = self.TOTAL_EVENTS

    def nevents_from_file(self, hist_path, fn_pattern='%(name)s.root', f=None, last_bin=False):
        if f is None:
            fn = fn_pattern % self
            if not os.path.isfile(fn):
                return -999
            f = ROOT.TFile(fn)
        h = f.Get(hist_path)
        if last_bin:
            return h.GetBinContent(h.GetNbinsX())
        else:
            return h.GetEntries()

    # JMTBAD need to distinguish between total_events and ana_total_events
    # (and need a better name for total_events)

    @property
    def nevents(self):
        if self.total_events >= 0 and self.total_events < self.nevents_orig:
            return self.total_events
        else:
            return self.nevents_orig

    def reduce_total_events_by(self, minus):
        assert self.total_events < 0
        self.total_events = self.nevents_orig - minus

    @property
    def partial_weight(self):
        return self.cross_section / float(self.nevents) * self.k_factor # the total weight is partial_weight * integrated_luminosity (in 1/pb, cross_section is assumed to be in pb)

    @property
    def int_lumi(self):
        return 1./self.partial_weight

    def job_control_commands(self, ana=False):
        if ana:
            return (('total_number_of_events', self.total_events),
                    ('events_per_job',         self.ana_events_per))
        else:
            return (('total_number_of_events', self.total_events),
                    ('events_per_job',         self.events_per))

########################################################################

class TupleOnlyMCSample(MCSample):
    def __init__(self, name, dataset, events_per=25000, total_events=-1):
        super(TupleOnlyMCSample, self).__init__(name, '', dataset, -1, -1, -1, -1)
        self.events_per = events_per
        self.total_events = total_events

########################################################################

class DataSample(Sample):
    IS_MC = False
    JSON = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions12/8TeV/Reprocessing/Cert_190456-208686_8TeV_22Jan2013ReReco_Collisions12_JSON.txt'
    LUMIS_PER = 30
    ANA_LUMIS_PER = 500
    TOTAL_LUMIS = -1

    def __init__(self, name, dataset, run_range=None):
        super(DataSample, self).__init__(name, name, dataset)

        self.run_range = run_range
        self.json = self.JSON

        self.lumis_per = self.LUMIS_PER
        self.ana_lumis_per = self.ANA_LUMIS_PER
        self.total_lumis = self.TOTAL_LUMIS

    def lumi_mask(self, ana=False):
        # JMTBAD run_range checking
        # JMTBAD ana/not difference
        if type(self.json) == str:
            return 'lumi_mask', self.json
        elif self.json is None:
            return ''
        else: # implement LumiList object -> tmp.json
            raise NotImplementedError('need to do something more complicated when combining lumimasks')

    def job_control_commands(self, ana=False):
        if ana:
            return (self.lumi_mask(ana),
                    ('total_number_of_lumis', self.total_lumis),
                    ('lumis_per_job',         self.ana_lumis_per))
        else:
            return (self.lumi_mask(ana),
                    ('total_number_of_lumis', self.total_lumis),
                    ('lumis_per_job',         self.lumis_per))

########################################################################

# https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat8TeV or PREP for xsecs
ttbar_samples = [
    #        name                title                                                      dataset                                                                                                nevents  clr  syst  xsec (pb)
    MCSample('ttbarhadronic',    't#bar{t}, hadronic',                                      '/TTJets_HadronicMGDecays_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM',                 10537444,   4, 0.15, 225.2 * 0.457),
    MCSample('ttbarsemilep',     't#bar{t}, semileptonic',                                  '/TTJets_SemiLeptMGDecays_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A_ext-v1/AODSIM',             25424818,   4, 0.15, 225.2 * 0.438),
    MCSample('ttbardilep',       't#bar{t}, dileptonic',                                    '/TTJets_FullLeptMGDecays_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v2/AODSIM',                 12119013,   4, 0.15, 225.2 * 0.105),
    ]

# JMTBAD
ttbarhadronicext = MCSample('ttbarhadronic', 't#bar{t}, hadronic', '/TTJets_HadronicMGDecays_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A_ext-v1/AODSIM', 31223821, 4, 0.15, 225.2 * 0.457)

qcd_samples = [
    MCSample('qcdht0100',        'QCD, 100 < H_{T} < 250 GeV',                              '/QCD_HT-100To250_TuneZ2star_8TeV-madgraph-pythia/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM',       50129518, 801, 0.10, 1.04e7),
    MCSample('qcdht0250',        'QCD, 250 < H_{T} < 500 GeV',                              '/QCD_HT-250To500_TuneZ2star_8TeV-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM',      27062078, 802, 0.10, 2.76e5),
    MCSample('qcdht0500',        'QCD, 500 < H_{T} < 1000 GeV',                             '/QCD_HT-500To1000_TuneZ2star_8TeV-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM',     30599292, 803, 0.10, 8.43e3),
    MCSample('qcdht1000',        'QCD, H_{T} > 1000 GeV',                                   '/QCD_HT-1000ToInf_TuneZ2star_8TeV-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM',     13843863, 804, 0.10, 2.04e2),
    ]

smaller_background_samples =[
    MCSample('singletop_s',      'single t (s-channel)',                                    '/T_s-channel_TuneZ2star_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM',               259961,  -1, 0.20, 3.79),
    MCSample('singletop_s_tbar', 'single #bar{t} (s-channel)',                              '/Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM',            139974,  -1, 0.20, 1.76),
    MCSample('singletop_t',      'single t (t-channel)',                                    '/T_t-channel_TuneZ2star_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM',              3758227,  -1, 0.20, 56.4),
    MCSample('singletop_t_tbar', 'single #bar{t} (t-channel)',                              '/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM',           1935072,  -1, 0.20, 30.7),
    MCSample('singletop_tW',     'single t (tW)',                                           '/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM',           497658,  42, 0.20, 11.1),
    MCSample('singletop_tW_tbar','single t (#bar{t}W)',                                     '/Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM',        493460,  42, 0.20, 11.1),
    MCSample('ww',               'WW',                                                      '/WW_TuneZ2star_8TeV_pythia6_tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM',                     10000431,   4, 0.04, 57.1),
    MCSample('wz',               'WZ',                                                      '/WZ_TuneZ2star_8TeV_pythia6_tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM',                     10000283,  30, 0.04, 32.3),
    MCSample('zz',               'ZZ',                                                      '/ZZ_TuneZ2star_8TeV_pythia6_tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM',                      9799908,   6, 0.03, 8.3),
    MCSample('ttzjets',          't#bar{t}+Z',                                              '/TTZJets_8TeV-madgraph_v2/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM',                                210160,  -1, 0.20, 0.172),
    MCSample('ttwjets',          't#bar{t}+W',                                              '/TTWJets_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM',                                   196046,  -1, 0.20, 0.215),
    MCSample('ttgjets',          't#bar{t}+#gamma',                                         '/TTGJets_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V19-v1/AODSIM',                                  1719954,  -1, 0.20, 1.44),
]

leptonic_background_samples = [
    MCSample('wjetstolnu',       'W + jets #rightarrow l#nu',                               '/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball/Summer12_DR53X-PU_S10_START53_V7A-v2/AODSIM',           57709905,   9, 0.10, 3.04e4),
    MCSample('dyjetstollM10',    'DY + jets #rightarrow ll, 10 < M < 50 GeV',               '/DYJetsToLL_M-10To50filter_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM',                7132223,  29, 0.10, 11050*0.069),
    MCSample('dyjetstollM50',    'DY + jets #rightarrow ll, M > 50 GeV',                    '/DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM',      30459503,  32, 0.10, 2.95e3),
]

auxiliary_background_samples = [
    MCSample('ttbarincl',        't#bar{t}',                                                '/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM', 6923750,   4, 0.15, 225.2),
    MCSample('qcdmupt15',        'QCD, #hat{p}_{T} > 20 GeV, #mu p_{T} > 15 GeV',           '/QCD_Pt_20_MuEnrichedPt_15_TuneZ2star_8TeV_pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM',      7529312, 801, 0.10, 3.64e8*3.7e-4),
    MCSample('tttt',             't#bar{t}t#bar{t}',                                        '/TTTT_TuneZ2star_8TeV-madgraph-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM',                     99994,  -1, 0.20, 7.16E-4),
    MCSample('tthbb',            'ttH, H #rightarrow bb',                                   '/TTH_HToBB_M-125_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM',                           1000008,  -1, 0.13, 0.1293 * 0.577),
    MCSample('zjetstonunuHT050', 'Z #rightarrow #nu#nu + jets, 50 < H_{T} < 100 GeV',       '/ZJetsToNuNu_50_HT_100_TuneZ2Star_8TeV_madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM',         4040980,  -1, 0.10, 3.81e2),
    MCSample('zjetstonunuHT100', 'Z #rightarrow #nu#nu + jets, 100 < H_{T} < 200 GeV',      '/ZJetsToNuNu_100_HT_200_TuneZ2Star_8TeV_madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM',        4416646,  -1, 0.10, 1.60e2),
    MCSample('zjetstonunuHT200', 'Z #rightarrow #nu#nu + jets, 200 < H_{T} < 400 GeV',      '/ZJetsToNuNu_200_HT_400_TuneZ2Star_8TeV_madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM',        5055885,  -1, 0.10, 4.15e1),
    MCSample('zjetstonunuHT400', 'Z #rightarrow #nu#nu + jets, H_{T} > 400 GeV',            '/ZJetsToNuNu_400_HT_inf_TuneZ2Star_8TeV_madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM',        1006928,  -1, 0.10, 5.27e0),
 
    MCSample('bjetsht0100', 'b jets, 100 < H_{T} < 250 GeV',  '/BJets_HT-100To250_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM',  14426854, 801, 0.10, 1.338e5),
    MCSample('bjetsht0250', 'b jets, 250 < H_{T} < 500 GeV',  '/BJets_HT-250To500_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM',  13183812, 802, 0.10, 5.828e3),
    MCSample('bjetsht0500', 'b jets, 500 < H_{T} < 1000 GeV', '/BJets_HT-500To1000_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM',  6650243, 803, 0.10, 2.176e2),
    MCSample('bjetsht1000', 'b jets, H_{T} > 1000 GeV',       '/BJets_HT-1000ToInf_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM',  3137949, 804, 0.10, 4.712e0),
 
    MCSample('qcdpt0000', 'QCD, #hat{p}_{T} < 5 GeV',           '/QCD_Pt-0to5_TuneZ2star_8TeV_pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM',       999788, 801, 0.10, 4.859e10),
    MCSample('qcdpt0005', 'QCD, 5 < #hat{p}_{T} < 15 GeV',      '/QCD_Pt-5to15_TuneZ2star_8TeV_pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM',     1489184, 802, 0.10, 4.264e10),
    MCSample('qcdpt0015', 'QCD, 15 < #hat{p}_{T} < 30 GeV',     '/QCD_Pt-15to30_TuneZ2star_8TeV_pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM',    9987968, 803, 0.10, 9.883e08),
    MCSample('qcdpt0030', 'QCD, 30 < #hat{p}_{T} < 50 GeV',     '/QCD_Pt-30to50_TuneZ2star_8TeV_pythia6/Summer12_DR53X-PU_S10_START53_V7A-v2/AODSIM',    6000000, 804, 0.10, 6.629e07),
    MCSample('qcdpt0050', 'QCD, 50 < #hat{p}_{T} < 80 GeV',     '/QCD_Pt-50to80_TuneZ2star_8TeV_pythia6/Summer12_DR53X-PU_S10_START53_V7A-v2/AODSIM',    5998860, 805, 0.10, 8.149e06),
    MCSample('qcdpt0080', 'QCD, 80 < #hat{p}_{T} < 120 GeV',    '/QCD_Pt-80to120_TuneZ2star_8TeV_pythia6/Summer12_DR53X-PU_S10_START53_V7A-v3/AODSIM',   5994864, 806, 0.10, 1.034e06),
    MCSample('qcdpt0120', 'QCD, 120 < #hat{p}_{T} < 170 GeV',   '/QCD_Pt-120to170_TuneZ2star_8TeV_pythia6/Summer12_DR53X-PU_S10_START53_V7A-v3/AODSIM',  5985732, 807, 0.10, 1.563e05),
    MCSample('qcdpt0170', 'QCD, 170 < #hat{p}_{T} < 300 GeV',   '/QCD_Pt-170to300_TuneZ2star_8TeV_pythia6/Summer12_DR53X-PU_S10_START53_V7A-v2/AODSIM',  5814398, 808, 0.10, 3.414e04),
    MCSample('qcdpt0300', 'QCD, 300 < #hat{p}_{T} < 470 GeV',   '/QCD_Pt-300to470_TuneZ2star_8TeV_pythia6/Summer12_DR53X-PU_S10_START53_V7A-v2/AODSIM',  5978500, 809, 0.10, 1.760e03),
    MCSample('qcdpt0470', 'QCD, 470 < #hat{p}_{T} < 600 GeV',   '/QCD_Pt-470to600_TuneZ2star_8TeV_pythia6/Summer12_DR53X-PU_S10_START53_V7A-v2/AODSIM',  3994848, 810, 0.10, 1.139e02),
    MCSample('qcdpt0600', 'QCD, 600 < #hat{p}_{T} < 800 GeV',   '/QCD_Pt-600to800_TuneZ2star_8TeV_pythia6/Summer12_DR53X-PU_S10_START53_V7A-v2/AODSIM',  3996864, 811, 0.10, 2.699e01),
    MCSample('qcdpt0800', 'QCD, 800 < #hat{p}_{T} < 1000 GeV',  '/QCD_Pt-800to1000_TuneZ2star_8TeV_pythia6/Summer12_DR53X-PU_S10_START53_V7A-v2/AODSIM', 3998563, 812, 0.10, 3.550e00),
    MCSample('qcdpt1000', 'QCD, 1000 < #hat{p}_{T} < 1400 GeV', '/QCD_Pt-1000to1400_TuneZ2star_8TeV_pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM',1964088, 813, 0.10, 7.378e-1),
    MCSample('qcdpt1400', 'QCD, 1400 < #hat{p}_{T} < 1800 GeV', '/QCD_Pt-1400to1800_TuneZ2star_8TeV_pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM',2000062, 814, 0.10, 3.352e-2),
    MCSample('qcdpt1800', 'QCD, #hat{p}_{T} > 1800 GeV',        '/QCD_Pt-1800_TuneZ2star_8TeV_pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM',       977586, 815, 0.10, 1.829e-3),
    
    MCSample('qcdmu0015', 'QCDmu5, 15 < #hat{p}_{T} < 20 GeV',    '/QCD_Pt-15to20_MuEnrichedPt5_TuneZ2star_8TeV_pythia6/Summer12_DR53X-PU_S10_START53_V7A-v2/AODSIM',     1722681, 801, 0.10, 0.0039*7.02e8),
    MCSample('qcdmu0020', 'QCDmu5, 20 < #hat{p}_{T} < 30 GeV',    '/QCD_Pt-20to30_MuEnrichedPt5_TuneZ2star_8TeV_pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM',     8486904, 801, 0.10, 0.0065*2.87e8),
    MCSample('qcdmu0030', 'QCDmu5, 30 < #hat{p}_{T} < 50 GeV',    '/QCD_Pt-30to50_MuEnrichedPt5_TuneZ2star_8TeV_pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM',     9560265, 801, 0.10, 0.0122*6.61e7),
    MCSample('qcdmu0050', 'QCDmu5, 50 < #hat{p}_{T} < 80 GeV',    '/QCD_Pt-50to80_MuEnrichedPt5_TuneZ2star_8TeV_pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM',    10365230, 801, 0.10, 0.0218*8.08e6),
    MCSample('qcdmu0080', 'QCDmu5, 80 < #hat{p}_{T} < 120 GeV',   '/QCD_Pt-80to120_MuEnrichedPt5_TuneZ2star_8TeV_pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM',    9238642, 801, 0.10, 0.0395*1.02e6),
    MCSample('qcdmu0120', 'QCDmu5, 120 < #hat{p}_{T} < 170 GeV',  '/QCD_Pt-120to170_MuEnrichedPt5_TuneZ2star_8TeV_pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM',   8501935, 801, 0.10, 0.0473*1.58e5),
    MCSample('qcdmu0170', 'QCDmu5, 170 < #hat{p}_{T} < 300 GeV',  '/QCD_Pt-170to300_MuEnrichedPt5_TuneZ2star_8TeV_pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM',   7669947, 801, 0.10, 0.0676*3.40e4),
    MCSample('qcdmu0300', 'QCDmu5, 300 < #hat{p}_{T} < 470 GeV',  '/QCD_Pt-300to470_MuEnrichedPt5_TuneZ2star_8TeV_pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM',   7832261, 801, 0.10, 0.0864*1.76e3),
    MCSample('qcdmu0470', 'QCDmu5, 470 < #hat{p}_{T} < 600 GeV',  '/QCD_Pt-470to600_MuEnrichedPt5_TuneZ2star_8TeV_pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM',   3783069, 801, 0.10, 0.1024*1.15e2),
    MCSample('qcdmu0600', 'QCDmu5, 600 < #hat{p}_{T} < 800 GeV',  '/QCD_Pt-600to800_MuEnrichedPt5_TuneZ2star_8TeV_pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM',   4119000, 801, 0.10, 0.0996*2.70e1),
    MCSample('qcdmu0800', 'QCDmu5, 800 < #hat{p}_{T} < 1000 GeV', '/QCD_Pt-800to1000_MuEnrichedPt5_TuneZ2star_8TeV_pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM',  4107853, 801, 0.10, 0.1033*3.57e0),
    MCSample('qcdmu1000', 'QCDmu5, #hat{p}_{T} > 1000 GeV',       '/QCD_Pt-1000_MuEnrichedPt5_TuneZ2star_8TeV_pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM',       3873970, 801, 0.10, 0.1097*7.74e-1),

    MCSample('qcdem020', 'QCDem, < #hat{p}_{T} < GeV', '/QCD_Pt_20_30_EMEnriched_TuneZ2star_8TeV_pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM',   35040695, 801, 0.10, 0.010*2.89e8),
    MCSample('qcdem030', 'QCDem, < #hat{p}_{T} < GeV', '/QCD_Pt_30_80_EMEnriched_TuneZ2star_8TeV_pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM',   33088888, 801, 0.10, 0.062*7.43e7),
    MCSample('qcdem080', 'QCDem, < #hat{p}_{T} < GeV', '/QCD_Pt_80_170_EMEnriched_TuneZ2star_8TeV_pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM',  34542763, 801, 0.10, 0.154*1.19e6),
    MCSample('qcdem170', 'QCDem, < #hat{p}_{T} < GeV', '/QCD_Pt_170_250_EMEnriched_TuneZ2star_8TeV_pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM', 31697066, 801, 0.10, 0.148*3.10e4),
    MCSample('qcdem250', 'QCDem, < #hat{p}_{T} < GeV', '/QCD_Pt_250_350_EMEnriched_TuneZ2star_8TeV_pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM', 34611322, 801, 0.10, 0.131*4.25e3),
    MCSample('qcdem350', 'QCDem, < #hat{p}_{T} < GeV', '/QCD_Pt_350_EMEnriched_TuneZ2star_8TeV_pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM',     34080562, 801, 0.10, 0.110*8.10e2),

    MCSample('qcdbce020', 'QCDbce, < #hat{p}_{T} < GeV', '/QCD_Pt_20_30_BCtoE_TuneZ2star_8TeV_pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM',   1740229, 801, 0.10, 5.80e-4*2.89e8),
    MCSample('qcdbce030', 'QCDbce, < #hat{p}_{T} < GeV', '/QCD_Pt_30_80_BCtoE_TuneZ2star_8TeV_pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM',   2048152, 801, 0.10, 2.25e-3*7.43e7),
    MCSample('qcdbce080', 'QCDbce, < #hat{p}_{T} < GeV', '/QCD_Pt_80_170_BCtoE_TuneZ2star_8TeV_pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM',  1945525, 801, 0.10, 1.09e-2*1.19e6),
    MCSample('qcdbce170', 'QCDbce, < #hat{p}_{T} < GeV', '/QCD_Pt_170_250_BCtoE_TuneZ2star_8TeV_pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM', 1948112, 801, 0.10, 2.04e-2*3.10e4),
    MCSample('qcdbce250', 'QCDbce, < #hat{p}_{T} < GeV', '/QCD_Pt_250_350_BCtoE_TuneZ2star_8TeV_pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM', 2026521, 801, 0.10, 2.43e-2*4.25e3),
    MCSample('qcdbce350', 'QCDbce, < #hat{p}_{T} < GeV', '/QCD_Pt_350_BCtoE_TuneZ2star_8TeV_pythia6/Summer12_DR53X-PU_S10_START53_V7A-v2/AODSIM',     1948532, 801, 0.10, 2.95e-2*8.10e2),

    MCSample('qcdb150', 'QCDb, #hat{p}_{T} > 150 GeV', '/QCD_Pt-150_bEnriched_TuneZ2star_8TeV-pythia6-evtgen/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM', 474151, 801, 0.10, 6.73e4*1.26e-1),
]

########################################################################

# xsecs from https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SUSYCrossSections8TeVgluglu (M_glu = M_neu + 5 GeV...)
mfv_xsec = {
     200: (0.153, 8.88e2),
     300: (0.149, 9.64e1),
     400: (0.151, 1.74e1),
     600: (0.173, 1.24e0),
     800: (0.202, 1.50e-1),
    1000: (0.257, 2.33e-2),
    }

mfv_signal_samples_ex = [
    (   0,  200, MCSample('mfv_neutralino_tau0000um_M0200', 'M_{tbs} = 200 GeV, prompt',           '/mfv_neutralino_tau0000um_M0200/tucker-mfv_neutralino_tau0000um_M0200-4c5a3e1bd487f486a1b444615e104727/USER',  99850, 2, *mfv_xsec[ 200]),),
    (   0,  400, MCSample('mfv_neutralino_tau0000um_M0400', 'M_{tbs} = 400 GeV, prompt',           '/mfv_neutralino_tau0000um_M0400/tucker-mfv_neutralino_tau0000um_M0400-4c5a3e1bd487f486a1b444615e104727/USER', 100000, 2, *mfv_xsec[ 400]),),
    (   0,  600, MCSample('mfv_neutralino_tau0000um_M0600', 'M_{tbs} = 600 GeV, prompt',           '/mfv_neutralino_tau0000um_M0600/tucker-mfv_neutralino_tau0000um_M0600-4c5a3e1bd487f486a1b444615e104727/USER', 100000, 2, *mfv_xsec[ 600]),),
    (   0,  800, MCSample('mfv_neutralino_tau0000um_M0800', 'M_{tbs} = 800 GeV, prompt',           '/mfv_neutralino_tau0000um_M0800/tucker-mfv_neutralino_tau0000um_M0800-4c5a3e1bd487f486a1b444615e104727/USER',  99900, 2, *mfv_xsec[ 800]),),
    (   0, 1000, MCSample('mfv_neutralino_tau0000um_M1000', 'M_{tbs} = 1000 GeV, prompt',          '/mfv_neutralino_tau0000um_M1000/tucker-mfv_neutralino_tau0000um_M1000-4c5a3e1bd487f486a1b444615e104727/USER',  99996, 2, *mfv_xsec[1000]),),
    (  10,  200, MCSample('mfv_neutralino_tau0010um_M0200', 'M_{tbs} = 200 GeV, #tau = 10 #mum',   '/mfv_neutralino_tau0010um_M0200/tucker-mfv_neutralino_tau0010um_M0200-1c71e23d89dd4b2c2e4deb43ae6cdc5a/USER', 100000, 2, *mfv_xsec[ 200]),),
    (  10,  400, MCSample('mfv_neutralino_tau0010um_M0400', 'M_{tbs} = 400 GeV, #tau = 10 #mum',   '/mfv_neutralino_tau0010um_M0400/tucker-mfv_neutralino_tau0010um_M0400-1c71e23d89dd4b2c2e4deb43ae6cdc5a/USER', 100000, 2, *mfv_xsec[ 400]),),
    (  10,  600, MCSample('mfv_neutralino_tau0010um_M0600', 'M_{tbs} = 600 GeV, #tau = 10 #mum',   '/mfv_neutralino_tau0010um_M0600/tucker-mfv_neutralino_tau0010um_M0600-1c71e23d89dd4b2c2e4deb43ae6cdc5a/USER',  99700, 2, *mfv_xsec[ 600]),),
    (  10,  800, MCSample('mfv_neutralino_tau0010um_M0800', 'M_{tbs} = 800 GeV, #tau = 10 #mum',   '/mfv_neutralino_tau0010um_M0800/tucker-mfv_neutralino_tau0010um_M0800-1c71e23d89dd4b2c2e4deb43ae6cdc5a/USER',  99950, 2, *mfv_xsec[ 800]),),
    (  10, 1000, MCSample('mfv_neutralino_tau0010um_M1000', 'M_{tbs} = 1000 GeV, #tau = 10 #mum',  '/mfv_neutralino_tau0010um_M1000/tucker-mfv_neutralino_tau0010um_M1000-1c71e23d89dd4b2c2e4deb43ae6cdc5a/USER',  99899, 2, *mfv_xsec[1000]),),
    ( 100,  200, MCSample('mfv_neutralino_tau0100um_M0200', 'M_{tbs} = 200 GeV, #tau = 100 #mum',  '/mfv_neutralino_tau0100um_M0200/tucker-mfv_neutralino_tau0100um_M0200-86ebc7c9963ad7f892ad94c512f4c308/USER',  99700, 2, *mfv_xsec[ 200]),),
    ( 100,  400, MCSample('mfv_neutralino_tau0100um_M0400', 'M_{tbs} = 400 GeV, #tau = 100 #mum',  '/mfv_neutralino_tau0100um_M0400/tucker-mfv_neutralino_tau0100um_M0400-86ebc7c9963ad7f892ad94c512f4c308/USER',  99250, 2, *mfv_xsec[ 400]),),
    ( 100,  600, MCSample('mfv_neutralino_tau0100um_M0600', 'M_{tbs} = 600 GeV, #tau = 100 #mum',  '/mfv_neutralino_tau0100um_M0600/tucker-mfv_neutralino_tau0100um_M0600-86ebc7c9963ad7f892ad94c512f4c308/USER',  99650, 2, *mfv_xsec[ 600]),),
    ( 100,  800, MCSample('mfv_neutralino_tau0100um_M0800', 'M_{tbs} = 800 GeV, #tau = 100 #mum',  '/mfv_neutralino_tau0100um_M0800/tucker-mfv_neutralino_tau0100um_M0800-86ebc7c9963ad7f892ad94c512f4c308/USER', 100000, 2, *mfv_xsec[ 800]),),
    ( 100, 1000, MCSample('mfv_neutralino_tau0100um_M1000', 'M_{tbs} = 1000 GeV, #tau = 100 #mum', '/mfv_neutralino_tau0100um_M1000/tucker-mfv_neutralino_tau0100um_M1000-86ebc7c9963ad7f892ad94c512f4c308/USER',  99749, 2, *mfv_xsec[1000]),),
    (1000,  200, MCSample('mfv_neutralino_tau1000um_M0200', 'M_{tbs} = 200 GeV, #tau = 1 mm',      '/mfv_neutralino_tau1000um_M0200/tucker-mfv_neutralino_tau1000um_M0200-a6ab3419cb64660d6c68351b3cff9fb0/USER',  99752, 2, *mfv_xsec[ 200]),),
    (1000,  400, MCSample('mfv_neutralino_tau1000um_M0400', 'M_{tbs} = 400 GeV, #tau = 1 mm',      '/mfv_neutralino_tau1000um_M0400/tucker-mfv_neutralino_tau1000um_M0400-a6ab3419cb64660d6c68351b3cff9fb0/USER',  99850, 2, *mfv_xsec[ 400]),),
    (1000,  600, MCSample('mfv_neutralino_tau1000um_M0600', 'M_{tbs} = 600 GeV, #tau = 1 mm',      '/mfv_neutralino_tau1000um_M0600/tucker-mfv_neutralino_tau1000um_M0600-a6ab3419cb64660d6c68351b3cff9fb0/USER',  99851, 2, *mfv_xsec[ 600]),),
    (1000,  800, MCSample('mfv_neutralino_tau1000um_M0800', 'M_{tbs} = 800 GeV, #tau = 1 mm',      '/mfv_neutralino_tau1000um_M0800/tucker-mfv_neutralino_tau1000um_M0800-a6ab3419cb64660d6c68351b3cff9fb0/USER',  99949, 2, *mfv_xsec[ 800]),),
    (1000, 1000, MCSample('mfv_neutralino_tau1000um_M1000', 'M_{tbs} = 1000 GeV, #tau = 1 mm',     '/mfv_neutralino_tau1000um_M1000/tucker-mfv_neutralino_tau1000um_M1000-a6ab3419cb64660d6c68351b3cff9fb0/USER', 100000, 2, *mfv_xsec[1000]),),
    (9900,  200, MCSample('mfv_neutralino_tau9900um_M0200', 'M_{tbs} = 200 GeV, #tau = 9.9 mm',    '/mfv_neutralino_tau9900um_M0200/tucker-mfv_neutralino_tau9900um_M0200-3c4ccd1d95a3d8658f6b5a18424712b3/USER',  99950, 2, *mfv_xsec[ 200]),),
    (9900,  400, MCSample('mfv_neutralino_tau9900um_M0400', 'M_{tbs} = 400 GeV, #tau = 9.9 mm',    '/mfv_neutralino_tau9900um_M0400/tucker-mfv_neutralino_tau9900um_M0400-3c4ccd1d95a3d8658f6b5a18424712b3/USER', 100000, 2, *mfv_xsec[ 400]),),
    (9900,  600, MCSample('mfv_neutralino_tau9900um_M0600', 'M_{tbs} = 600 GeV, #tau = 9.9 mm',    '/mfv_neutralino_tau9900um_M0600/tucker-mfv_neutralino_tau9900um_M0600-3c4ccd1d95a3d8658f6b5a18424712b3/USER',  99950, 2, *mfv_xsec[ 600]),),
    (9900,  800, MCSample('mfv_neutralino_tau9900um_M0800', 'M_{tbs} = 800 GeV, #tau = 9.9 mm',    '/mfv_neutralino_tau9900um_M0800/tucker-mfv_neutralino_tau9900um_M0800-3c4ccd1d95a3d8658f6b5a18424712b3/USER',  99900, 2, *mfv_xsec[ 800]),),
    (9900, 1000, MCSample('mfv_neutralino_tau9900um_M1000', 'M_{tbs} = 1000 GeV, #tau = 9.9 mm',   '/mfv_neutralino_tau9900um_M1000/tucker-mfv_neutralino_tau9900um_M1000-3c4ccd1d95a3d8658f6b5a18424712b3/USER',  99899, 2, *mfv_xsec[1000]),), 

    (   0,  300, MCSample('mfv_neutralino_tau0000um_M0300', 'M_{tbs} = 300 GeV, prompt',           '/mfv_neutralino_tau0000um_M0300/jchu-mfv_neutralino_tau0000um_M0300-4c5a3e1bd487f486a1b444615e104727/USER', 100000, 2, *mfv_xsec[ 300]),),
    (  10,  300, MCSample('mfv_neutralino_tau0010um_M0300', 'M_{tbs} = 300 GeV, #tau = 10 #mum',   '/mfv_neutralino_tau0010um_M0300/jchu-mfv_neutralino_tau0010um_M0300-1c71e23d89dd4b2c2e4deb43ae6cdc5a/USER',  99700, 2, *mfv_xsec[ 300]),),
    ( 100,  300, MCSample('mfv_neutralino_tau0100um_M0300', 'M_{tbs} = 300 GeV, #tau = 100 #mum',  '/mfv_neutralino_tau0100um_M0300/jchu-mfv_neutralino_tau0100um_M0300-86ebc7c9963ad7f892ad94c512f4c308/USER', 100000, 2, *mfv_xsec[ 300]),),
    ( 300,  200, MCSample('mfv_neutralino_tau0300um_M0200', 'M_{tbs} = 200 GeV, #tau = 300 #mum',  '/mfv_neutralino_tau0300um_M0200/jchu-mfv_neutralino_tau0300um_M0200-0fcc6f04c7b2260cb6c49261d41edaca/USER',  98950, 2, *mfv_xsec[ 200]),),
    ( 300,  300, MCSample('mfv_neutralino_tau0300um_M0300', 'M_{tbs} = 300 GeV, #tau = 300 #mum',  '/mfv_neutralino_tau0300um_M0300/jchu-mfv_neutralino_tau0300um_M0300-0fcc6f04c7b2260cb6c49261d41edaca/USER',  94850, 2, *mfv_xsec[ 300]),),
    ( 300,  400, MCSample('mfv_neutralino_tau0300um_M0400', 'M_{tbs} = 400 GeV, #tau = 300 #mum',  '/mfv_neutralino_tau0300um_M0400/jchu-mfv_neutralino_tau0300um_M0400-0fcc6f04c7b2260cb6c49261d41edaca/USER', 100000, 2, *mfv_xsec[ 400]),),
    ( 300,  600, MCSample('mfv_neutralino_tau0300um_M0600', 'M_{tbs} = 600 GeV, #tau = 300 #mum',  '/mfv_neutralino_tau0300um_M0600/jchu-mfv_neutralino_tau0300um_M0600-0fcc6f04c7b2260cb6c49261d41edaca/USER',  94450, 2, *mfv_xsec[ 600]),),
    ( 300,  800, MCSample('mfv_neutralino_tau0300um_M0800', 'M_{tbs} = 800 GeV, #tau = 300 #mum',  '/mfv_neutralino_tau0300um_M0800/jchu-mfv_neutralino_tau0300um_M0800-0fcc6f04c7b2260cb6c49261d41edaca/USER',  99450, 2, *mfv_xsec[ 800]),),
    ( 300, 1000, MCSample('mfv_neutralino_tau0300um_M1000', 'M_{tbs} = 1000 GeV, #tau = 300 #mum', '/mfv_neutralino_tau0300um_M3000/jchu-mfv_neutralino_tau0300um_M1000-0fcc6f04c7b2260cb6c49261d41edaca/USER',  99149, 2, *mfv_xsec[1000]),),
    (1000,  300, MCSample('mfv_neutralino_tau1000um_M0300', 'M_{tbs} = 300 GeV, #tau = 1 mm',      '/mfv_neutralino_tau1000um_M0300/jchu-mfv_neutralino_tau1000um_M0300-a6ab3419cb64660d6c68351b3cff9fb0/USER',  91800, 2, *mfv_xsec[ 300]),),
    (9900,  300, MCSample('mfv_neutralino_tau9900um_M0300', 'M_{tbs} = 300 GeV, #tau = 9.9 mm',    '/mfv_neutralino_tau9900um_M0300/jchu-mfv_neutralino_tau9900um_M0300-3c4ccd1d95a3d8658f6b5a18424712b3/USER', 100000, 2, *mfv_xsec[ 300]),),

    (1000,  400, MCSample('mysignaltune3',       '', '/mfv_neutralino_tau1000um_M0400_tune_3/jchavesb-mfv_neutralino_tau1000um_M0400_tune_3-e17c423e411c7625ebf79112981b92b0/USER',        100000, 2, *mfv_xsec[ 400]),),
    (1000,  400, MCSample('mysignaltune4',       '', '/mfv_neutralino_tau1000um_M0400_tune_4/jchavesb-mfv_neutralino_tau1000um_M0400_tune_4-832390b7c0947e4b08135391c0924f95/USER',        100000, 2, *mfv_xsec[ 400]),),
    (1000,  400, MCSample('mysignaltune5',       '', '/mfv_neutralino_tau1000um_M0400_tune_5/jchavesb-mfv_neutralino_tau1000um_M0400_tune_5-998e97fcda3ca47d1d647f0835952d27/USER',        100000, 2, *mfv_xsec[ 400]),),
    (1000,  400, MCSample('mysignaltune6',       '', '/mfv_neutralino_tau1000um_M0400_tune_6/jchavesb-mfv_neutralino_tau1000um_M0400_tune_6-0369ff42a15fed597e0a363b3f8edc1c/USER',        100000, 2, *mfv_xsec[ 400]),),
    (1000,  400, MCSample('mysignaltune7',       '', '/mfv_neutralino_tau1000um_M0400_tune_7/jchavesb-mfv_neutralino_tau1000um_M0400_tune_7-6003addd1979663f588d0c5aa78e6346/USER',        100000, 2, *mfv_xsec[ 400]),),
    (1000,  400, MCSample('mysignaltune8',       '', '/mfv_neutralino_tau1000um_M0400_tune_8/jchavesb-mfv_neutralino_tau1000um_M0400_tune_8-dd3c8ceba2a82a60a712f74b7ca5a607/USER',        100000, 2, *mfv_xsec[ 400]),),
    (1000,  400, MCSample('mysignaltune12',      '', '/mfv_neutralino_tau1000um_M0400_tune_12/jchavesb-mfv_neutralino_tau1000um_M0400_tune_12-60f88ed1269b264f1bd7c4bb048dc5d9/USER',      100000, 2, *mfv_xsec[ 400]),),
    (1000,  400, MCSample('mysignaltune13',      '', '/mfv_neutralino_tau1000um_M0400_tune_13/jchavesb-mfv_neutralino_tau1000um_M0400_tune_13-8a6cd8ad72ac2ecdec2acf901a5ae85a/USER',      100000, 2, *mfv_xsec[ 400]),),

    (1000,  400, MCSample('mysignaltune10',      '', '/mfv_neutralino_tau1000um_M0400_tune_10/jchavesb-mfv_neutralino_tau1000um_M0400_tune_10-55f49472d01964c4ac6513539e4c2ae0/USER',      100000, 2, *mfv_xsec[ 400]),),
    (1000,  400, MCSample('mysignaltune11',      '', '/mfv_neutralino_tau1000um_M0400_tune_11/jchavesb-mfv_neutralino_tau1000um_M0400_tune_11-a748cba579d381b275857b446cd677ea/USER',      100000, 2, *mfv_xsec[ 400]),),
    ]

mfv_signal_samples_nouse = []
mfv_signal_samples = []
mfv_signal_samples_systematics = []
for tau, mass, sample in mfv_signal_samples_ex:
    is_syst = 'jchavesb' in sample.dataset
    if tau < 100:
        mfv_signal_samples_nouse.append(sample)
    elif is_syst:
        mfv_signal_samples_systematics.append(sample)
    else:
        mfv_signal_samples.append(sample)
    sample.tau = tau
    sample.mass = mass
    sample.events_per = 1500
    sample.no_skimming_cuts = True
    sample.is_pythia8 = True
    sample.dbs_url_num = 3 if ('0300' in sample.name or is_syst) else 2
    sample.re_pat = True
    if not ('tune10' in sample.name or 'tune11' in sample.name):
        sample.scheduler = 'condor' 
    sample.ana_hash = '0a90ffb9bb56aadc18a0859a54bf4f31' if not is_syst else '0db49a3df21e20de5584b04b90b2376b'
    sample.cross_section = 0.001

########################################################################

myttbar_samples = [
    MCSample('myttbarpythia',       '', '/mfv_ttbar_default/tucker-mfv_ttbar_default-84bbc883c4d7ec08aa60419295f8ddab/USER',        99850, 4, 0.15, 225.2 * 0.457),
    MCSample('myttbarpynopu',       '', '/mfv_ttbar_nopu/tucker-mfv_ttbar_nopu-de5b96ddc03a24cfcdf41da57e270038/USER',              99950, 4, 0.15, 225.2 * 0.457),
    MCSample('myttbarpydesignnopu', '', '/mfv_ttbar_designnopu/tucker-mfv_ttbar_designnopu-03e053ea4788fabdfdc6964bc26befc0/USER', 100000, 4, 0.15, 225.2 * 0.457),
    MCSample('myttbarpydesignnoputkex', '', '/mfv_ttbar_designnoputkex/tucker-mfv_ttbar_designnoputkex-03e053ea4788fabdfdc6964bc26befc0/USER', 750000, 4, 0.15, 225.2 * 0.457),
    MCSample('myttbartune3',       '', '/mfv_ttbar_tune_3/jchavesb-mfv_ttbar_tune_3-e3674fd6eec136ae079fabace84be5fa/USER',        100000, 4, 0.15, 225.2 * 0.457),
    MCSample('myttbartune4',       '', '/mfv_ttbar_tune_4/jchavesb-mfv_ttbar_tune_4-2ab11a6f2e6e96d6779b5e2cdd1bc9d7/USER',        100000, 4, 0.15, 225.2 * 0.457),
    MCSample('myttbartune5',       '', '/mfv_ttbar_tune_5/jchavesb-mfv_ttbar_tune_5-84bbc883c4d7ec08aa60419295f8ddab/USER',        100000, 4, 0.15, 225.2 * 0.457),
    MCSample('myttbartune6',       '', '/mfv_ttbar_tune_6/jchavesb-mfv_ttbar_tune_6-5e5c8b6e5ae97e632829881f70a96bef/USER',        100000, 4, 0.15, 225.2 * 0.457),
    MCSample('myttbartune7',       '', '/mfv_ttbar_tune_7/jchavesb-mfv_ttbar_tune_7-aed1494d928e44cf1085663860ab1a07/USER',        100000, 4, 0.15, 225.2 * 0.457),
    MCSample('myttbartune8',       '', '/mfv_ttbar_tune_8/jchavesb-mfv_ttbar_tune_8-39b59d827dfea83a5b26108b211413ab/USER',        100000, 4, 0.15, 225.2 * 0.457),
    MCSample('myttbartune9',       '', '/mfv_ttbar_tune_9/jchavesb-mfv_ttbar_tune_9-90218df95d8a7fe3d94d722599f21aa6/USER',        100000, 4, 0.15, 225.2 * 0.457),
    MCSample('myttbartune10',       '', '/mfv_ttbar_tune_10/jchavesb-mfv_ttbar_tune_10-f90c435f681f63bce4d0bb86d798a78b/USER',        100000, 4, 0.15, 225.2 * 0.457),
    MCSample('myttbartune11',      '', '/mfv_ttbar_tune_11/jchavesb-mfv_ttbar_tune_11-941817f3c97288ac74e8b6edc1ce6faa/USER',      100000, 4, 0.15, 225.2 * 0.457),
    MCSample('myttbarelliptical',    '', '/mfv_ttbar_ali_elliptical/jchavesb-mfv_ttbar_ali_elliptical-84bbc883c4d7ec08aa60419295f8ddab/USER',       100000, 4, 0.15, 225.2 * 0.457),
    MCSample('myttbarsagitta',       '', '/mfv_ttbar_ali_sagitta/jchavesb-mfv_ttbar_ali_sagitta-84bbc883c4d7ec08aa60419295f8ddab/USER',             100000, 4, 0.15, 225.2 * 0.457),
    MCSample('myttbarskew',          '', '/mfv_ttbar_ali_skew/jchavesb-mfv_ttbar_ali_skew-84bbc883c4d7ec08aa60419295f8ddab/USER',                   100000, 4, 0.15, 225.2 * 0.457),
    MCSample('myttbartwist',         '', '/mfv_ttbar_ali_twist/jchavesb-mfv_ttbar_ali_twist-84bbc883c4d7ec08aa60419295f8ddab/USER',                 100000, 4, 0.15, 225.2 * 0.457),
    MCSample('myttbarzexpansion',    '', '/mfv_ttbar_ali_zexpansion/jchavesb-mfv_ttbar_ali_zexpansion-84bbc883c4d7ec08aa60419295f8ddab/USER',       100000, 4, 0.15, 225.2 * 0.457),
    MCSample('myttbartelescope',    '', '/mfv_ttbar_ali_telescope/jchavesb-mfv_ttbar_ali_telescope-84bbc883c4d7ec08aa60419295f8ddab/USER',       100000, 4, 0.15, 225.2 * 0.457),
    ]

for s in myttbar_samples:
    s.is_pythia8 = True
    s.dbs_url_num = 3
    if 'jchavesb' in s.dataset and not 'tune10' in s.name and not 'telescope' in s.name:
        s.scheduler = 'condor'

########################################################################

data_samples = [
    DataSample('MultiJetPk2012B', '/MultiJet1Parked/Run2012B-05Nov2012-v2/AOD'),
    DataSample('MultiJetPk2012C1', '/MultiJet1Parked/Run2012C-part1_05Nov2012-v2/AOD'),
    DataSample('MultiJetPk2012C2', '/MultiJet1Parked/Run2012C-part2_05Nov2012-v2/AOD'),
    DataSample('MultiJetPk2012D1', '/MultiJet1Parked/Run2012D-part1_10Dec2012-v1/AOD'),
    DataSample('MultiJetPk2012D2', '/MultiJet1Parked/Run2012D-part2_17Jan2013-v1/AOD'),
    ]

auxiliary_data_samples = [
    DataSample('SingleMu2012B', '/SingleMu/Run2012B-22Jan2013-v1/AOD')
    ]

########################################################################

all_data_samples = data_samples + auxiliary_data_samples
all_mc_samples = ttbar_samples + qcd_samples + smaller_background_samples + leptonic_background_samples + auxiliary_background_samples + mfv_signal_samples + mfv_signal_samples_nouse + mfv_signal_samples_systematics + myttbar_samples
all_samples = all_data_samples + all_mc_samples

samples_by_name = {}
for sample in all_samples:
    exec '%s = sample' % sample.name
    samples_by_name[sample.name] = sample

def from_argv(default=None, sort_and_set=True):
    samples = []
    all_samples_names = samples_by_name.keys()
    for arg in sys.argv:
        if any(c in arg for c in '[]*?!'):
            for sample in all_samples:
                if fnmatch(sample.name, arg):
                    samples.append(sample)
        elif arg in all_samples_names:
            samples.append(sample)
    if samples:
        if sort_and_set:
            samples = sorted(set(samples))
        return samples
    else:
        return default

########################################################################

# Bookkeeping of numbers of events in missing jobs/etc. goes here.

for sample in ttbar_samples + qcd_samples + mfv_signal_samples:
    if '0300' not in sample.name:
        sample.ana_ready = True

# JMTBAD replace ana_ready with ana_dict and check that

for sample, reduce_by in [
    ]:
    sample.reduce_total_events_by(reduce_by)

mfv_neutralino_tau0000um_M0200.ana_filter_eff = 4.7518e-01  #    47447 /    99850
mfv_neutralino_tau0000um_M0400.ana_filter_eff = 9.6890e-01  #    96890 /   100000
mfv_neutralino_tau0000um_M0600.ana_filter_eff = 9.9495e-01  #    99495 /   100000
mfv_neutralino_tau0000um_M0800.ana_filter_eff = 9.9796e-01  #    99696 /    99900
mfv_neutralino_tau0000um_M1000.ana_filter_eff = 9.9866e-01  #    99862 /    99996
mfv_neutralino_tau0010um_M0200.ana_filter_eff = 4.7647e-01  #    47647 /   100000
mfv_neutralino_tau0010um_M0400.ana_filter_eff = 9.6750e-01  #    96750 /   100000
mfv_neutralino_tau0010um_M0600.ana_filter_eff = 9.9530e-01  #    99231 /    99700
mfv_neutralino_tau0010um_M0800.ana_filter_eff = 9.9795e-01  #    99745 /    99950
mfv_neutralino_tau0010um_M1000.ana_filter_eff = 9.9892e-01  #    99791 /    99899

mfv_neutralino_tau0100um_M0200.ana_filter_eff = 4.7951e-01  #    47807 /    99700
mfv_neutralino_tau0100um_M0400.ana_filter_eff = 9.6769e-01  #    96043 /    99250
mfv_neutralino_tau0100um_M0600.ana_filter_eff = 9.9554e-01  #    99206 /    99650
mfv_neutralino_tau0100um_M0800.ana_filter_eff = 9.9795e-01  #    99795 /   100000
mfv_neutralino_tau0100um_M1000.ana_filter_eff = 9.9890e-01  #    99639 /    99749
mfv_neutralino_tau1000um_M0200.ana_filter_eff = 4.7873e-01  #    47754 /    99752
mfv_neutralino_tau1000um_M0400.ana_filter_eff = 9.6798e-01  #    96653 /    99850
mfv_neutralino_tau1000um_M0600.ana_filter_eff = 9.9508e-01  #    99360 /    99851
mfv_neutralino_tau1000um_M0800.ana_filter_eff = 9.9825e-01  #    99774 /    99949
mfv_neutralino_tau1000um_M1000.ana_filter_eff = 9.9866e-01  #    99866 /   100000
mfv_neutralino_tau9900um_M0200.ana_filter_eff = 4.7714e-01  #    47690 /    99950
mfv_neutralino_tau9900um_M0400.ana_filter_eff = 9.6734e-01  #    96734 /   100000
mfv_neutralino_tau9900um_M0600.ana_filter_eff = 9.9511e-01  #    99461 /    99950
mfv_neutralino_tau9900um_M0800.ana_filter_eff = 9.9818e-01  #    99718 /    99900
mfv_neutralino_tau9900um_M1000.ana_filter_eff = 9.9904e-01  #    99803 /    99899

#mfv_neutralino_tau0100um_M0300.ana_filter_eff = 8.6538e-01  #    86538 /   100000
#mfv_neutralino_tau0300um_M0200.ana_filter_eff = 4.7439e-01  #    47439 /   100000
#mfv_neutralino_tau0300um_M0300.ana_filter_eff = 8.2247e-01  #    82247 /   100000
#mfv_neutralino_tau0300um_M0400.ana_filter_eff = 9.6975e-01  #    96975 /   100000
#mfv_neutralino_tau0300um_M0600.ana_filter_eff = 9.3989e-01  #    93989 /   100000
#mfv_neutralino_tau0300um_M0800.ana_filter_eff = 9.9264e-01  #    99264 /   100000
#mfv_neutralino_tau0300um_M1000.ana_filter_eff = 9.9035e-01  #    99035 /   100000
#mfv_neutralino_tau1000um_M0300.ana_filter_eff = 7.9684e-01  #    79286 /    99500
#mfv_neutralino_tau9900um_M0300.ana_filter_eff = 8.6473e-01  #    86473 /   100000

dyjetstollM10.ana_filter_eff        = 4.3913e-04  #     3132 /  7132223
dyjetstollM50.ana_filter_eff        = 2.8337e-03  #    86313 / 30459503
qcdht0100.ana_filter_eff            = 7.4784e-04  #    37489 / 50129518
qcdht0250.ana_filter_eff            = 6.0783e-02  #  1644907 / 27062078
qcdht0500.ana_filter_eff            = 3.1108e-01  #  9518716 / 30599292
qcdht1000.ana_filter_eff            = 4.4614e-01  #  6176270 / 13843863
singletop_s.ana_filter_eff          = 7.3030e-02  #    18985 /   259961
singletop_s_tbar.ana_filter_eff     = 6.7548e-02  #     9455 /   139974
singletop_t.ana_filter_eff          = 5.4126e-02  #   203416 /  3758227
singletop_tW.ana_filter_eff         = 1.8520e-01  #    92167 /   497658
singletop_tW_tbar.ana_filter_eff    = 1.8475e-01  #    91167 /   493460
singletop_t_tbar.ana_filter_eff     = 5.3102e-02  #   102756 /  1935072
ttbardilep.ana_filter_eff           = 1.3151e-01  #  1593779 / 12119013
ttbarhadronic.ana_filter_eff        = 4.7517e-01  #  5007127 / 10537444
ttbarsemilep.ana_filter_eff         = 2.7453e-01  #  6979960 / 25424818
ttgjets.ana_filter_eff              = 5.0128e-01  #   862177 /  1719954
ttwjets.ana_filter_eff              = 6.0494e-01  #   118596 /   196046
ttzjets.ana_filter_eff              = 6.3787e-01  #   134054 /   210160
wjetstolnu.ana_filter_eff           = 6.6758e-04  #    38526 / 57709905
ww.ana_filter_eff                   = 2.2439e-02  #   224401 / 10000431
wz.ana_filter_eff                   = 2.8131e-02  #   281321 / 10000283
zz.ana_filter_eff                   = 2.9762e-02  #   291664 /  9799908
qcdpt0000.ana_filter_eff =  7.001e-06
qcdpt0005.ana_filter_eff =  1.410e-05
qcdpt0015.ana_filter_eff =  1.332e-05
qcdpt0030.ana_filter_eff =  5.733e-05
qcdpt0050.ana_filter_eff =  1.313e-03
qcdpt0080.ana_filter_eff =  1.476e-02
qcdpt0120.ana_filter_eff =  5.763e-02
qcdpt0170.ana_filter_eff =  1.235e-01
qcdpt0300.ana_filter_eff =  2.067e-01
qcdpt0470.ana_filter_eff =  2.439e-01
qcdpt0600.ana_filter_eff =  2.534e-01
qcdpt0800.ana_filter_eff =  2.505e-01
qcdpt1000.ana_filter_eff =  2.341e-01
qcdpt1400.ana_filter_eff =  1.969e-01
qcdpt1800.ana_filter_eff =  1.546e-01
bjetsht0100.ana_filter_eff = 1.0520e-03  #    15177 / 14426854
bjetsht0250.ana_filter_eff = 8.1803e-02  #  1042986 / 12750008
bjetsht0500.ana_filter_eff = 3.4381e-01  #  2262942 /  6581987
bjetsht1000.ana_filter_eff = 4.7193e-01  #  1480886 /  3137949

########################################################################

def check_nevents(samples, hist_path, fn_pattern='%(name)s.root'):
    disagreements = []
    nofiles = []
    ok = []
    for sample in samples:
        n = sample.nevents_from_file(hist_path, fn_pattern)
        #print sample.name, n
        if n == -999:
            nofiles.append(sample.name)
            continue
        if n != sample.nevents:
            disagreements.append('%s.total_events = %i' % (sample.name, n))
        else:
            ok.append(sample.name)
    print 'these are OK: %s' % ' '.join(ok)
    print '(no files found for %s)' % ' '.join(nofiles)
    if disagreements:
        print '\n'.join(disagreements)
        raise ValueError('different numbers of events')

########################################################################

__all__ = ['data_samples', 'auxiliary_data_samples', 'all_data_samples']
__all__ += ['ttbar_samples', 'qcd_samples', 'smaller_background_samples', 'leptonic_background_samples', 'auxiliary_background_samples', 'mfv_signal_samples', 'mfv_signal_samples_nouse', 'mfv_signal_samples_systematics', 'myttbar_samples', 'all_mc_samples']
__all__ += ['all_samples']
__all__ += [s.name for s in all_samples]
__all__ += ['check_nevents', 'from_argv']

if __name__ == '__main__':
    if 'dump' in sys.argv:
        for sample in all_samples:
            sample.dump()
            print

    elif 'sites' in sys.argv:
        for sample in all_samples:
            sites = DBS.sites_for_dataset(sample.dataset)
            print '%20s%15s %s' % (sample.name, num_events(sample.dataset), 'AT fnal' if [x for x in sites if 'fnal' in x] else 'NOT at fnal')

    elif 'checknumevents' in sys.argv:
        # this only applies if there is no filter applied
        diffs = []
        for sample in all_mc_samples:
            if not sample.ana_ready:
                continue
            x,y = sample.nevents, DBS.numevents_in_dataset(sample.ana_dataset, **sample.dbs_inst_dict(sample.ana_dbs_url_num))
            print '%30s %14i %14i %14i %s' % (sample.name, x, y, x == y)
            if x != y:
                diffs.append((sample.name, y))
        print '\nsuggested change:'
        for diff in diffs:
            print '%s.total_events = %i' % diff

    elif 'filtereffs' in sys.argv:
        diffs = []
        for sample in all_mc_samples:
            if not sample.ana_ready:
                continue
            o,x,y = sample.nevents_orig, sample.nevents, DBS.numevents_in_dataset(sample.ana_dataset, **sample.dbs_inst_dict(sample.ana_dbs_url_num))
            print '%30s %14i %14i %14i' % (sample.name, o, y, x)
            if x != y:
                diffs.append((sample, y, x))
        print '\nsuggested change:'
        for sample, y, x in diffs:
            eff = float(y)/x
            if abs(eff - sample.ana_filter_eff) > 1e-4:
                print '%s.ana_filter_eff = %9.4e  # %8i / %8i' % (sample.name, eff, y, x)

    elif 'getnewevents' in sys.argv:
        path = sys.argv[sys.argv.index('getnewevents')+1]
        check_nevents(all_mc_samples, path)

    elif 'merge' in sys.argv:
        files = []
        output = 'merge.root'
        norm_to = 1
        path_for_nevents = ''
        last_bin = False

        for x in sys.argv:
            if x.endswith('.root'):
                if os.path.isfile(x):
                    files.append(x)
                else:
                    output = x
            elif x.startswith('path_for_nevents='):
                path_for_nevents = x.replace('path_for_nevents=', '')
            elif x == 'last_bin':
                last_bin = True
            else:
                try:
                    norm_to = float(x)
                except ValueError:
                    pass

        if norm_to > 0:
            print 'norm sum of weights to', norm_to
        else:
            print 'multiply every weight by', -norm_to

        if not path_for_nevents:
            if last_bin:
                raise ValueError('cannot last_bin if no path_for_nevents')
            print 'taking nevents from samples'
        else:
            print 'taking nevents from file with path %s%s' % (path_for_nevents, (' using last bin contents' if last_bin else ''))

        weights = []
        for fn in files:
            sname = os.path.splitext(os.path.basename(fn))[0]
            sample = samples_by_name[sname]
            if path_for_nevents:
                sample.total_events = sample.nevents_from_file(path_for_nevents, fn, last_bin=last_bin)
            weights.append(sample.partial_weight)

        if norm_to > 0:
            norm_to /= sum(weights)
        else:
            norm_to *= -1

        weights = [w*norm_to for w in weights]
        
        weights = ','.join('%f' % w for w in weights)
        cmd = 'mergeTFileServiceHistograms -w %s -i %s -o %s 2>&1 | grep -v "Sum of squares of weights structure already created"' % (weights, ' '.join(files), output)
        print cmd
        os.system(cmd)
