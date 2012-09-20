#!/usr/bin/env python

import os
from JMTucker.Tools.DBS import files_in_dataset
from JMTucker.Tools.general import big_warn

class MCSample(object):
    IS_FASTSIM = False
    IS_PYTHIA8 = False
    SCHEDULER_NAME = 'glite'
    HLT_PROCESS_NAME = 'HLT'
    DBS_URL_NUM = 0
    ANA_DBS_URL_NUM = 2
    ANA_HASH = 'bd9748f60791b31d15ca5bb480d0e762'
    PUBLISH_USER = 'tucker'
    ANA_VERSION = 'v2'
    
    def __init__(self, name, nice_name, dataset, nevents, color, syst_frac, cross_section, k_factor=1):
        self.name = name
        self.nice_name = nice_name
        self.dataset = dataset
        self.nevents = nevents
        self.color = color
        self.syst_frac = float(syst_frac)
        self.cross_section = float(cross_section)
        self.k_factor = float(k_factor)

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

    @property
    def partial_weight(self):
        return self.cross_section / float(self.nevents) * self.k_factor # the total weight is partial_weight * integrated_luminosity (in 1/pb, cross_section is assumed to be in pb)

    @property
    def scheduler(self):
        if self.dbs_url_ > 0:
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

class TupleOnlyMCSample(MCSample):
    def __init__(self, name, dataset, scheduler='condor', hlt_process_name='HLT'):
        super(TupleOnlyMCSample, self).__init__(name, 'dummy', dataset, 1, 1, 1, 1, scheduler=scheduler, hlt_process_name=hlt_process_name)

# https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat8TeV or PREP for xsecs
background_samples = [
    #        name                title                                                      dataset                                                                                        nevents  clr  syst  xsec (pb)
    MCSample('ttzjets',          't#bar{t}+Z',                                              '/TTZJets_8TeV-madgraph_v2/Summer12-PU_S7_START52_V9-v1/AODSIM',                                209741,  -1, 0.20, 0.172),
    MCSample('ttwjets',          't#bar{t}+W',                                              '/TTWJets_8TeV-madgraph/Summer12-PU_S7_START52_V9-v1/AODSIM',                                   195301,  -1, 0.20, 0.215),
    MCSample('ttgjets',          't#bar{t}+#gamma',                                         '/TTGJets_8TeV-madgraph/Summer12-PU_S7_START52_V9-v1/AODSIM',                                    71598,  -1, 0.20, 1.44),
    MCSample('t_s',              't (s-channel)',                                           '/T_s-channel_TuneZ2star_8TeV-powheg-tauola/Summer12-PU_S7_START52_V9-v1/AODSIM',               259961,  -1, 0.20, 3.79),
    MCSample('tbar_s',           '#bar{t} (s-channel)',                                     '/Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola/Summer12-PU_S7_START52_V9-v1/AODSIM',            139974,  -1, 0.20, 1.76),
    MCSample('tW',               'tW',                                                      '/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/Summer12-PU_S7_START52_V9-v1/AODSIM',           497658,  42, 0.20, 11.1),
    MCSample('tbarW',            '#bar{t}W',                                                '/Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/Summer12-PU_S7_START52_V9-v1/AODSIM',        493460,  42, 0.20, 11.1),
    MCSample('t_t',              't (t-channel)',                                           '/T_t-channel_TuneZ2star_8TeV-powheg-tauola/Summer12-PU_S7_START52_V9-v1/AODSIM',                23777,  -1, 0.20, 56.4),
    MCSample('tbar_t',           '#bar{t} (t-channel)',                                     '/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola/Summer12-PU_S7_START52_V9-v1/AODSIM',           1935072,  -1, 0.20, 30.7),
    MCSample('wjetstolnu',       'W + jets #rightarrow l#nu',                               '/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball/Summer12-PU_S7_START52_V9-v1/AODSIM',           18393090,   9, 0.10, 3.04e4),
    MCSample('zjetstonunuHT50',  'Z #rightarrow #nu#nu + jets, 50 < H_{T} < 100 GeV',       '/ZJetsToNuNu_50_HT_100_TuneZ2Star_8TeV_madgraph/Summer12-PU_S7_START52_V9-v1/AODSIM',         4053786,  -1, 0.10, 3.81e2),
    MCSample('zjetstonunuHT100', 'Z #rightarrow #nu#nu + jets, 100 < H_{T} < 200 GeV',      '/ZJetsToNuNu_100_HT_200_TuneZ2Star_8TeV_madgraph/Summer12-PU_S7_START52_V9-v1/AODSIM',        4416646,  -1, 0.10, 1.60e2),
    MCSample('zjetstonunuHT200', 'Z #rightarrow #nu#nu + jets, 200 < H_{T} < 400 GeV',      '/ZJetsToNuNu_200_HT_400_TuneZ2Star_8TeV_madgraph/Summer12-PU_S7_START52_V9-v3/AODSIM',        5066608,  -1, 0.10, 4.15e1),
    MCSample('zjetstonunuHT400', 'Z #rightarrow #nu#nu + jets, H_{T} > 400 GeV',            '/ZJetsToNuNu_400_HT_inf_TuneZ2Star_8TeV_madgraph/Summer12-PU_S7_START52_V9-v1/AODSIM',        1006928,  -1, 0.10, 5.27e0),
    MCSample('dyjetstollM10',    'DY + jets #rightarrow ll, 10 < M < 50 GeV',               '/DYJetsToLL_M-10To50filter_8TeV-madgraph/Summer12-PU_S7_START52_V9-v1/AODSIM',                7132223,  -1, 0.10, 11050*0.069),
    MCSample('dyjetstollM50',    'DY + jets #rightarrow ll, M > 50 GeV',                    '/DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball/Summer12-PU_S7_START52_V9-v2/AODSIM',      30461028,  -1, 0.10, 2.95e3),
    MCSample('ttbar',            't#bar{t}',                                                '/TTJets_TuneZ2star_8TeV-madgraph-tauola/Summer12-PU_S7_START52_V9-v1/AODSIM',                 6736135,   4, 0.15, 225.2),
    MCSample('qcd0',             'QCD, #hat{p}_{T} < 5 GeV',                                '/QCD_Pt-0to5_TuneZ2star_8TeV_pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM',                     999788, 801, 0.10, 4.859e10),
    MCSample('qcd5',             'QCD, 5 < #hat{p}_{T} < 15 GeV',                           '/QCD_Pt-5to15_TuneZ2star_8TeV_pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM',                   1489184, 802, 0.10, 4.264e10),
    MCSample('qcd15',            'QCD, 15 < #hat{p}_{T} < 30 GeV',                          '/QCD_Pt-15to30_TuneZ2star_8TeV_pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM',                 10925056, 803, 0.10, 9.883e8),
    MCSample('qcd30',            'QCD, 30 < #hat{p}_{T} < 50 GeV',                          '/QCD_Pt-30to50_TuneZ2star_8TeV_pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM',                  6000000, 804, 0.10, 6.629e7),
    MCSample('qcd50',            'QCD, 50 < #hat{p}_{T} < 80 GeV',                          '/QCD_Pt-50to80_TuneZ2star_8TeV_pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM',                  5995944, 805, 0.10, 8.149e6),
    MCSample('qcd80',            'QCD, 80 < #hat{p}_{T} < 120 GeV',                         '/QCD_Pt-80to120_TuneZ2star_8TeV_pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM',                 5981328, 806, 0.10, 1.034e6),
    MCSample('qcd120',           'QCD, 120 < #hat{p}_{T} < 170 GeV',                        '/QCD_Pt-120to170_TuneZ2star_8TeV_pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM',                5985732, 807, 0.10, 1.563e5),
    MCSample('qcd170',           'QCD, 170 < #hat{p}_{T} < 300 GeV',                        '/QCD_Pt-170to300_TuneZ2star_8TeV_pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM',                5814398, 808, 0.10, 3.414e4),
    MCSample('qcd300',           'QCD, 300 < #hat{p}_{T} < 470 GeV',                        '/QCD_Pt-300to470_TuneZ2star_8TeV_pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM',                5927300, 809, 0.10, 1.760e3),
    MCSample('qcd470',           'QCD, 470 < #hat{p}_{T} < 600 GeV',                        '/QCD_Pt-470to600_TuneZ2star_8TeV_pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM',                3994848, 810, 0.10, 1.139e2),
    MCSample('qcd600',           'QCD, 600 < #hat{p}_{T} < 800 GeV',                        '/QCD_Pt-600to800_TuneZ2star_8TeV_pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM',                3992760, 811, 0.10, 2.699e1),
    MCSample('qcd800',           'QCD, 800 < #hat{p}_{T} < 1000 GeV',                       '/QCD_Pt-800to1000_TuneZ2star_8TeV_pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM',               3998563, 812, 0.10, 3.550e0),
    MCSample('qcd1000',          'QCD, 1000 < #hat{p}_{T} < 1400 GeV',                      '/QCD_Pt-1000to1400_TuneZ2star_8TeV_pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM',              1964088, 813, 0.10, 7.378e-1),
    MCSample('qcd1400',          'QCD, 1400 < #hat{p}_{T} < GeV',                           '/QCD_Pt-1400to1800_TuneZ2star_8TeV_pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM',              2000062, 814, 0.10, 3.352e-2),
    MCSample('qcd1800',          'QCD, #hat{p}_{T} > 1800 GeV',                             '/QCD_Pt-1800_TuneZ2star_8TeV_pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM',                     977586, 815, 0.10, 1.829e-3),
]

stop_signal_samples = [
    MCSample('pythiastopm200',  'stop pair prod., M = 200 GeV',  '/sstop_genfsimreco_test/tucker-sstop_genfsimreco_test-15c4250952b10a469cc6da8beaecd65e/USER', 93000,  2, 0.15, 17),
    ]

mfv_signal_samples = [
    MCSample('mfvN3jtau0',      'MFV N, #tau = 0',                   '/mfvneutralino_genfsimreco_tau0/tucker-mfvneutralino_genfsimreco_tau0-aa8b56a9a9cba6aa847bda9acf329ad0/USER',         24500, -1, 0.2, 9e99),
    MCSample('mfvN3jtau100um',  'MFV N, #tau = 100 #mum',            '/mfvneutralino_genfsimreco_tau100um/tucker-mfvneutralino_genfsimreco_tau100um-465709e5340ac2cc11e2751b48bbef3e/USER', 24000, -1, 0.2, 9e99),
    MCSample('mfvN3jtau10um',   'MFV N, #tau = 10 #mum',             '/mfvneutralino_genfsimreco_tau10um/tucker-mfvneutralino_genfsimreco_tau10um-719b1b049e9de8135afa1f308d0994e6/USER',   24500, -1, 0.2, 9e99),
    MCSample('mfvN3jtau1mm',    'MFV N, #tau = 1 mm',                '/mfvneutralino_genfsimreco_tau1mm/tucker-mfvneutralino_genfsimreco_tau1mm-f0b5b0c98c357fc0015e0194f7aef803/USER',     24500, -1, 0.2, 9e99),
    MCSample('mfvN3jtau9p9mm',  'MFV N, #tau = 9.9 mm',              '/mfvneutralino_genfsimreco_tau9p9mm/tucker-mfvneutralino_genfsimreco_tau9p9mm-891f0c49f79ad2222cb205736c37de4f/USER', 24000, -1, 0.2, 9e99),
    ]

_samples = background_samples + stop_signal_samples + mfv_signal_samples

for sample in _samples:
    exec '%s = sample' % sample.name


# Exceptions to the defaults.

pythiastopm200.dbs_url_num = 2
pythiastopm200.is_fastsim = True
pythiastopm200.ana_hash = 'd1c7726c69d89f45da05a992a40b425c'

for sample in (mfvN3jtau0, mfvN3jtau100um, mfvN3jtau10um, mfvN3jtau1mm, mfvN3jtau9p9mm):
    sample.ana_hash = 'ffbc82b68f588f5f183a150670744b16'
    sample.is_fastsim = True
    sample.is_pythia8 = True
    sample.dbs_url_num = 2


# Other exceptions due to jobs being missed, mixing dataset versions
# (that don't affect actual physics), etc.

warning = ['other datasets v2, these datasets v3:']
for sample in (qcd170, qcd600, dyjetstollM10, dyjetstollM50, tW, t_s, t_t, tbar_s, tbar_t, ttgjets, ttwjets, ttzjets, wjetstolnu):
    warning.append(sample.name)
    sample.ana_version = 'v3'
    sample.ana_hash = '5e1021f6ad80ccbe13b7c6abc1eb101a'
big_warn('\n'.join(warning))


temp_neventses = []
temp_neventses = [(qcd15, 10918100), (qcd50, 5306688), (qcd120, 5235732), (qcd170, 5764398), (qcd470, 3674848), (qcd600, 3712760), (qcd800, 3828563)]

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


big_warn('ttVjets samples not complete')
for o in (ttgjets, ttwjets, ttzjets):
    background_samples.remove(o)
    _samples.remove(o)
    del o


__all__ = ['background_samples', 'stop_signal_samples', 'mfv_signal_samples'] + [s.name for s in _samples]

if __name__ == '__main__':
    import sys
    if 'sites' in sys.argv:
        from mydbs import *
        for sample in _samples:
            sites = sites_for_dataset(sample.dataset)
            print '%20s%15s %s' % (sample.name, num_events(sample.dataset), 'AT fnal' if [x for x in sites if 'fnal' in x] else 'NOT at fnal')
