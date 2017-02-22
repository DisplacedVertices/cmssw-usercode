#!/usr/bin/env python

import os, sys
from collections import defaultdict
from fnmatch import fnmatch
import JMTucker.Tools.DBS as DBS
from JMTucker.Tools.general import big_warn, typed_from_argv

########################################################################

us_aaa = [ 'T2_US_Caltech', 'T2_US_MIT', 'T2_US_Nebraska', 'T2_US_UCSD', 'T2_US_Vanderbilt', 'T2_US_Wisconsin' ]  # T2_US_Purdue,T2_US_Florida,T3_US_Brown,T3_US_Colorado,T3_US_NotreDame,T3_US_UMiss
eu_aaa = ['T2_AT_Vienna', 'T2_CH_CERN', 'T2_CH_CSCS', 'T2_DE_DESY', 'T2_EE_Estonia', 'T2_ES_CIEMAT', 'T2_ES_IFCA', 'T2_FR_CCIN2P3']

########################################################################

class Dataset(object):
    HLT_NAME = 'HLT'
    DBS_INST = 'global'
    AAA = []

    def __init__(self, dataset, nevents_orig, **kwargs):
        self.dataset = dataset
        self.nevents_orig = nevents_orig

        self.hlt_name = kwargs.get('hlt_name', self.HLT_NAME)
        self.dbs_inst = kwargs.get('dbs_inst', self.DBS_INST)
        self.aaa = kwargs.get('aaa', self.AAA)
        self.condor = kwargs.get('condor', False)
        self.xrootd_url = kwargs.get('xrootd_url', '')
        self.filenames = kwargs.get('filenames', [])

########################################################################

class Sample(object):
    IS_MC = True
    IS_FASTSIM = False
    GENERATOR = 'pythia8'

    def __init__(self, name, dataset, nevents_orig, **kwargs):
        self.name = name
        self.curr_dataset = 'main'
        self.datasets = {'main': Dataset(dataset, nevents_orig, **kwargs)}
        
        self.is_mc      = kwargs.get('is_mc',      self.IS_MC)
        self.is_fastsim = kwargs.get('is_fastsim', self.IS_FASTSIM)
        self.generator  = kwargs.get('generator',  self.GENERATOR)

        self.ready = True

    def set_curr_dataset(self, c):
        if not self.datasets.has_key(c):
            raise KeyError('no dataset with key %s registered in sample %s' % (c, self.name))
        self.curr_dataset = c

    def add_dataset(self, c, *args, **kwargs):
        self.datasets[c] = Dataset(*args, **kwargs)

    @property
    def dataset(self):
        return self.datasets[self.curr_dataset].dataset

    @property
    def nevents_orig(self):
        return self.datasets[self.curr_dataset].nevents_orig

    @property
    def hlt_name(self):
        return self.datasets[self.curr_dataset].hlt_name

    @hlt_name.setter
    def hlt_name(self, val):
        self.datasets[self.curr_dataset].hlt_name = val

    @property
    def dbs_inst(self):
        return self.datasets[self.curr_dataset].dbs_inst

    @dbs_inst.setter
    def dbs_inst(self, val):
        self.datasets[self.curr_dataset].dbs_inst = val

    @property
    def aaa(self):
        return self.datasets[self.curr_dataset].aaa

    @aaa.setter
    def aaa(self, val):
        self.datasets[self.curr_dataset].aaa = val

    @property
    def condor(self):
        return self.datasets[self.curr_dataset].condor

    @condor.setter
    def condor(self, val):
        self.datasets[self.curr_dataset].condor = val

    @property
    def xrootd_url(self):
        return self.datasets[self.curr_dataset].xrootd_url

    @xrootd_url.setter
    def xrootd_url(self, val):
        self.datasets[self.curr_dataset].xrootd_url = val

    @property
    def filenames(self):
        fns = self.datasets[self.curr_dataset].filenames
        if not fns:
            try:
                import JMTucker.Tools.SampleFiles as sfns
                x = sfns.get(self.name, self.curr_dataset)
                if x is not None:
                    nfns, fns = x
                    if len(fns) != nfns:
                        raise ValueError('problem with JMTucker.Tools.SampleFiles')
            except ImportError:
                pass

            if not fns:
                print 'hitting DBS for filenames for', self.name, self.curr_dataset, self.dataset
                fns = self.datasets[self.curr_dataset].filenames = DBS.files_in_dataset(self.dataset, self.dbs_inst)
        return fns

    @property
    def primary_dataset(self):
        return self.dataset.split('/')[1]

    def __getitem__(self, key):
        return getattr(self, key)

    def job_control(self, conf_obj):
        raise NotImplementedError('job_control needs to be implemented')

########################################################################

class MCSample(Sample):
    EVENTS_PER = 25000
    TOTAL_EVENTS = -1
    
    def __init__(self, name, dataset, nevents_orig, **kwargs):
        super(MCSample, self).__init__(name, dataset, nevents_orig, **kwargs)

        self.nice = kwargs.get('nice', '')
        self.color = kwargs.get('color', -1)
        self.syst_frac = float(kwargs.get('syst_frac', -1))
        self.xsec = float(kwargs.get('xsec', -1)) # assumed pb

        self.events_per = kwargs.get('events_per', self.EVENTS_PER)
        self.total_events = kwargs.get('total_events', self.TOTAL_EVENTS)

        self.join_info = (False, self.nice, self.color)

        self.norm_path = None

    @property
    def partial_weight_orig(self):
        return self.xsec / float(self.nevents_orig) # total weight = partial_weight * integrated_luminosity in 1/pb

    @property
    def int_lumi_orig(self):
        return 1./self.partial_weight_orig # units of 1/pb

    def nevents(self, f_or_fn):
        return norm_from_file(f_or_fn, self.norm_path)

    def partial_weight(self, f_or_fn):
        return self.xsec / self.nevents(f_or_fn)

    def int_lumi(self, f_or_fn):
        return 1./self.partial_weight(f_or_fn)
            
    def job_control(self, conf_obj):
        conf_obj.splitting = 'EventAwareLumiBased'
        conf_obj.unitsPerJob = self.events_per
        conf_obj.totalUnits = self.total_events

########################################################################

class DataSample(Sample):
    IS_MC = False
    JSON = None
    LUMIS_PER = 30
    TOTAL_LUMIS = -1

    def __init__(self, name, dataset, **kwargs):
        super(DataSample, self).__init__(name, dataset, -1, **kwargs)

        self.run_range = kwargs.get('run_range', None)
        self.json = kwargs.get('json', self.JSON)

        self.lumis_per = kwargs.get('lumis_per', self.LUMIS_PER)
        self.total_lumis = kwargs.get('total_lumis', self.TOTAL_LUMIS)

    def add_dataset(self, c, *args, **kwargs):
        assert len(args) == 1 and type(args[0]) == str # JMTBAD
        self.datasets[c] = Dataset(args[0], -1, **kwargs)

    def lumi_mask(self):
        # JMTBAD run_range checking
        if type(self.json) == str and os.path.isfile(self.json):
            return self.json
        elif self.json is None:
            return ''
        else: # implement LumiList object -> tmp.json
            raise NotImplementedError('need to do something more complicated when combining lumimasks')

    def job_control(self, conf_obj):
        conf_obj.splitting = 'LumiBased'
        conf_obj.unitsPerJob = self.lumis_per
        conf_obj.totalUnits = self.total_lumis
        lumi_mask = self.lumi_mask()
        if lumi_mask:
            conf_obj.lumiMask = lumi_mask
        if self.run_range:
            conf_obj.runRange = self.run_range

########################################################################

class SamplesRegistry:
    def __init__(self):
        self.d_samples = {}
        self.d_lists = {}

    def all(self, as_set=False):
        a = set(self.d_samples.values())
        for n,l in self.d_lists.iteritems():
            for s in l:
                a.add(s)
        if as_set:
            return a
        else:
            return sorted(a)

    def add(self, s):
        self.d_samples[s.name] = s

    def add_list(self, name, l):
        self.d_lists[name] = l

    def by_primary_dataset(self, pd):
        x = []
        for s in self.all():
            if s.primary_dataset == pd:
                x.append(s)
        return x

    def from_argv(self, default=[], sort_and_set=True, from_root_fns=False):
        ready_only = 'fa_ready_only' in sys.argv
        check = 'fa_check' in sys.argv
        use_all = 'fa_all' in sys.argv

        fns = []
        samples = []

        if use_all:
            samples = self.all()
        else:
            for arg in sys.argv:
                if from_root_fns:
                    orig_arg = arg
                    arg = os.path.basename(arg).replace('.root', '')
                by_match = any(c in arg for c in '[]*?!')
                for sample in self.d_samples.values():
                    if arg == sample.name or (by_match and fnmatch(sample.name, arg)):
                        if from_root_fns:
                            sample.fn = orig_arg
                        samples.append(sample)
                for name, l in self.d_lists.iteritems():
                    if arg == name:
                        samples.extend(l)

        if ready_only:
            samples = [s for s in samples if s.ready]

        if sort_and_set:
            samples = sorted(set(samples))

        if check:
            print 'from_argv got these:'
            for s in samples:
                print s.name
            raw_input('ok?')

        return samples if samples else default

########################################################################

def anon_samples(txt, **kwargs):
    samples = []
    lines = [line.strip() for line in txt.split('\n') if line.strip()]
    uniq = defaultdict(int)
    for line in lines:
        if line.startswith('#'):
            continue
        line = line.split()
        if len(line) == 3:
            name, dataset, nevents_orig = line
        else:
            if len(line) == 2:
                dataset, nevents_orig = line
            else:
                dataset = line[0]
                nevents_orig = -1
            name = dataset.split('/')[1]
            uniq[name] += 1
            if uniq[name] > 1:
                name += str(uniq[name])
        sample = MCSample(name, dataset, nevents_orig)
        for k,v in kwargs.iteritems():
            setattr(sample, k, v)
        samples.append(sample)
    return samples

def norm_from_file(f_or_fn, path=None):
    if type(f_or_fn) == str:
        from JMTucker.Tools.ROOTTools import ROOT
        f = ROOT.TFile(f_or_fn)
    else:
        f = f_or_fn
    if path:
        h = f.Get(path)
    else:
        if hasattr(f, 'mfvWeight'):
            h = f.Get('mfvWeight/h_sums')
        elif hasattr(f, 'mcStat'):
            h = f.Get('mcStat/h_sums')
        else:
            raise ValueError('duh')
        assert h.GetXaxis().GetBinLabel(1) == 'sum_nevents_total'
    return h.GetBinContent(1)

def merge(samples, output='merge.root', norm_to=1., norm_path=''):
    if norm_to > 0:
        print 'norm sum of weights to', norm_to
    else:
        print 'multiply every weight by', -norm_to

    weights = []
    for sample in samples:
        if norm_path:
            sample.norm_path = norm_path
        weights.append(sample.partial_weight(sample.fn))

    if norm_to > 0:
        norm_to /= sum(weights)
    else:
        norm_to *= -1.

    weights = [w*norm_to for w in weights]
    weights = ','.join('%f' % w for w in weights)

    files = [s.fn for s in samples]
    files = ' '.join(files)

    cmd = 'mergeTFileServiceHistograms -w %s -i %s -o %s 2>&1 | grep -v "Sum of squares of weights structure already created"' % (weights, files, output)
    print cmd
    os.system(cmd)

def sample_from_end_string(namespace, d):
    for x in vars(namespace).itervalues():
        if issubclass(type(x), Sample) and d.endswith(x.name):
            return x

def main(samples_registry):
    import sys
    if 'merge' in sys.argv:
        samples = samples_registry.from_argv(from_root_fns=True)
        out_fn = [x for x in sys.argv if x.endswith('.root') and not os.path.isfile(x)]
        out_fn = out_fn[0] if out_fn else 'merge.root'
        norm_to = typed_from_argv(float, default_value=1.)
        norm_path = typed_from_argv(str, default_value='', name='norm_path')
        merge(samples, output=out_fn, norm_to=norm_to, norm_path=norm_path)

__all__ = [
    'us_aaa',
    'eu_aaa',
    'Dataset',
    'Sample',
    'MCSample',
    'DataSample',
    'SamplesRegistry',
    'anon_samples',
    'norm_from_file',
    'merge',
    'sample_from_end_string',
    'main',
    ]
