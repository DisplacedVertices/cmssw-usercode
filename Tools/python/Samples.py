#!/usr/bin/env python

import os
from JMTucker.Tools.DBS import files_in_dataset

class MCSample(object):
    DBS_ANA02 = True
    
    def __init__(self, name, nice_name, dataset, nevents, color, syst_frac, cross_section, k_factor=1, filenames=None, scheduler='condor', hlt_process_name='HLT', dbs_url=None, ana_dataset=None, ana_dbs_url=2, is_fastsim=False, is_pythia8=False):
        self.name = name
        self.nice_name = nice_name
        self.dataset = dataset
        self.nevents = nevents
        self.color = color
        self.syst_frac = float(syst_frac)
        self.cross_section = float(cross_section)
        self.k_factor = float(k_factor)
        self.filenames_ = filenames
        self.scheduler_ = scheduler
        self.hlt_process_name = hlt_process_name
        self.dbs_url_ = dbs_url
        self.ana_dataset = ana_dataset
        self.ana_dbs_url_ = ana_dbs_url
        self.is_fastsim = is_fastsim
        self.is_pythia8 = is_pythia8

    @property
    def partial_weight(self):
        return self.cross_section / float(self.nevents) * self.k_factor # the total weight is partial_weight * integrated_luminosity (in 1/pb, cross_section is assumed to be in pb)

    @property
    def scheduler(self):
        if self.dbs_url_ > 0:
            return 'condor'
        else:
            return self.scheduler_

    def _get_dbs_url(self, num):
        return '' if not num else 'dbs_url = https://cmsdbsprod.cern.ch:8443/cms_dbs_ph_analysis_0%i_writer/servlet/DBSServlet' % num
    
    @property
    def dbs_url(self):
        return self._get_dbs_url(self.dbs_url_)
        
    @property
    def ana_dbs_url(self):
        return self._get_dbs_url(self.ana_dbs_url_)

    @property
    def use_server(self):
        return 'use_server = 1' if self.scheduler != 'condor' else ''
        
    @property
    def filenames(self):
        # Return a list of filenames for running the histogrammer not
        # using crab.
        if self.filenames_ is not None:
            return self.filenames_
        return files_in_dataset(self.ana_dataset, ana01=self.ana_dbs_url_ == 1, ana02=self.ana_dbs_url_ == 2)

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
        super(tupleonlysample, self).__init__(name, 'dummy', dataset, 1, 1, 1, 1, scheduler=scheduler, hlt_process_name=hlt_process_name)

# https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat8TeV or PREP for xsecs
background_samples = [
    #        name               title                                dataset                                                                              nevents  clr  syst  xsec (pb)
    MCSample('ttbar',           't#bar{t}',                          '/TTJets_TuneZ2star_8TeV-madgraph-tauola/Summer12-PU_S7_START52_V9-v1/AODSIM',       6736135,   4, 0.15, 225.2),
    MCSample('wjetstolnu',      'W+jets #rightarrow l#nu',           '/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball/Summer12-PU_S7_START52_V9-v1/AODSIM', 18393090,   8, 0.10, 3.04e4),
    MCSample('qcd0',            'QCD, #hat{p}{T} < 5 GeV',           '/QCD_Pt-0to5_TuneZ2star_8TeV_pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM',           999788, 801, 0.10, 4.859e10, scheduler='glite'),
    MCSample('qcd5',            'QCD, 5 < #hat{p}{T} < 15 GeV',      '/QCD_Pt-5to15_TuneZ2star_8TeV_pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM',         1489184, 802, 0.10, 4.264e10, scheduler='glite'),
    MCSample('qcd15',           'QCD, 15 < #hat{p}{T} < 30 GeV',     '/QCD_Pt-15to30_TuneZ2star_8TeV_pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM',       10925056, 803, 0.10, 9.883e8,  scheduler='glite'),
    MCSample('qcd30',           'QCD, 30 < #hat{p}{T} < 50 GeV',     '/QCD_Pt-30to50_TuneZ2star_8TeV_pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM',        6000000, 804, 0.10, 6.629e7,  scheduler='glite'),
    MCSample('qcd50',           'QCD, 50 < #hat{p}{T} < 80 GeV',     '/QCD_Pt-50to80_TuneZ2star_8TeV_pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM',        5995944, 805, 0.10, 8.149e6,  scheduler='glite'),
    MCSample('qcd80',           'QCD, 80 < #hat{p}{T} < 120 GeV',    '/QCD_Pt-80to120_TuneZ2star_8TeV_pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM',       5981328, 806, 0.10, 1.034e6,  scheduler='glite'),
    MCSample('qcd120',          'QCD, 120 < #hat{p}{T} < 170 GeV',   '/QCD_Pt-120to170_TuneZ2star_8TeV_pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM',      5985732, 807, 0.10, 1.563e5,  scheduler='glite'),
    MCSample('qcd170',          'QCD, 170 < #hat{p}{T} < 300 GeV',   '/QCD_Pt-170to300_TuneZ2star_8TeV_pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM',      5814398, 808, 0.10, 3.414e4),
    MCSample('qcd300',          'QCD, 300 < #hat{p}{T} < 470 GeV',   '/QCD_Pt-300to470_TuneZ2star_8TeV_pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM',      5927300, 809, 0.10, 1.760e3),
    MCSample('qcd470',          'QCD, 470 < #hat{p}{T} < 600 GeV',   '/QCD_Pt-470to600_TuneZ2star_8TeV_pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM',      3994848, 810, 0.10, 1.139e2),
    MCSample('qcd600',          'QCD, 600 < #hat{p}{T} < 800 GeV',   '/QCD_Pt-600to800_TuneZ2star_8TeV_pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM',      3992760, 811, 0.10, 2.699e1),
    MCSample('qcd800',          'QCD, 800 < #hat{p}{T} < 1000 GeV',  '/QCD_Pt-800to1000_TuneZ2star_8TeV_pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM',     3998563, 812, 0.10, 3.550e0),
    MCSample('qcd1000',         'QCD, 1000 < #hat{p}{T} < 1400 GeV', '/QCD_Pt-1000to1400_TuneZ2star_8TeV_pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM',    1964088, 813, 0.10, 7.378e-1),
    MCSample('qcd1400',         'QCD, 1400 < #hat{p}{T} < GeV',      '/QCD_Pt-1400to1800_TuneZ2star_8TeV_pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM',    2000062, 814, 0.10, 3.352e-2),
    MCSample('qcd1800',         'QCD, #hat{p}{T} > 1800 GeV',        '/QCD_Pt-1800_TuneZ2star_8TeV_pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM',           977586, 815, 0.10, 1.829e-3),
]

stop_signal_samples = [
    MCSample('pythiastopm200',  'stop pair prod., Mstop = 200 GeV',  '/sstop_genfsimreco_test/tucker-sstop_genfsimreco_test-15c4250952b10a469cc6da8beaecd65e/USER', 93000,  2, 0.15, 17),
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
    sample.ana_dataset = '/%s/tucker-sstoptuple_v1_%s-3312fbeda721580c3cdebaec6739016e/USER' % (sample.dataset.split('/')[1], sample.name)

pythiastopm200.dbs_url_ = 2
pythiastopm200.is_fastsim = True
for sample in [mfvN3jtau0, mfvN3jtau100um, mfvN3jtau10um, mfvN3jtau1mm, mfvN3jtau9p9mm]:
    sample.ana_dataset = sample.ana_dataset.replace('3312fbeda721580c3cdebaec6739016e', 'd4b76361cb50b072f07d02828189ae78')
    sample.is_fastsim = True
    sample.is_pythia8 = True
    sample.dbs_url_ = 2

from JMTucker.Tools.general import big_warn
#big_warn('nothing')

temp_neventses = []
temp_neventses = [(ttbar, 6606135), (qcd15, 10801196), (qcd30, 5990000), (qcd80, 5931328), (qcd120, 5935732), (qcd170, 5704398), (qcd470, 3674848), (qcd600, 3712760), (qcd800, 3828563)]

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

__all__ = ['background_samples', 'stop_signal_samples', 'mfv_signal_samples'] + [s.name for s in _samples]
