#!/usr/bin/env python

import os, sys
from collections import defaultdict
from fnmatch import fnmatch
from pprint import pprint
import JMTucker.Tools.DBS as DBS
from JMTucker.Tools.general import big_warn, typed_from_argv

########################################################################

us_aaa = [ 'T2_US_Caltech', 'T2_US_MIT', 'T2_US_Nebraska', 'T2_US_UCSD', 'T2_US_Vanderbilt', 'T2_US_Wisconsin' ]  # T2_US_Purdue,T2_US_Florida,T3_US_Brown,T3_US_Colorado,T3_US_NotreDame,T3_US_UMiss
eu_aaa = ['T2_AT_Vienna', 'T2_CH_CERN', 'T2_CH_CSCS', 'T2_DE_DESY', 'T2_EE_Estonia', 'T2_ES_CIEMAT', 'T2_ES_IFCA', 'T2_FR_CCIN2P3']

########################################################################

class Dataset(object):
    EVENTS_PER = 25000
    TOTAL_EVENTS = -1
    JSON = ''
    HLT_NAME = 'HLT'
    DBS_INST = 'global'
    AAA = []

    def __init__(self, dataset, nevents_orig, **kwargs):
        self.dataset = dataset
        self.nevents_orig = nevents_orig

        self.events_per = kwargs.get('events_per', self.EVENTS_PER)
        self.total_events = kwargs.get('total_events', self.TOTAL_EVENTS)
        self.json = kwargs.get('json', self.JSON)
        self.run_range = kwargs.get('run_range', None)

        self.hlt_name = kwargs.get('hlt_name', self.HLT_NAME)
        self.dbs_inst = kwargs.get('dbs_inst', self.DBS_INST)
        self.aaa = kwargs.get('aaa', self.AAA)
        self.condor = kwargs.get('condor', False)
        self.xrootd_url = kwargs.get('xrootd_url', '')
        self.filenames = kwargs.get('filenames', [])

    def job_control(self, conf_obj):
        conf_obj.splitting = 'EventAwareLumiBased'
        conf_obj.unitsPerJob = self.events_per
        conf_obj.totalUnits = self.total_events
        if self.json:
            conf_obj.lumiMask = self.json
        if self.run_range:
            conf_obj.runRange = self.run_range

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

    def has_dataset(self, c):
        return self.datasets.has_key(c)

    def set_curr_dataset(self, c):
        if not self.datasets.has_key(c):
            raise KeyError('no dataset with key %s registered in sample %s' % (c, self.name))
        self.curr_dataset = c

    def try_curr_dataset(self, c):
        if not self.has_dataset(c):
            return False
        self.curr_dataset = c
        return True

    def add_dataset(self, c, *args, **kwargs):
        if self.has_dataset(c):
            raise KeyError('sample %s already has dataset %s' % (self.name, c))
        if len(args) == 1:
            args = (args[0], -1)
        elif len(args) == 0:
            args = ('/%s/None/None' % self.datasets['main'].dataset.split('/')[1], -1)
        self.datasets[c] = Dataset(*args, **kwargs)

    def job_control(self, conf_obj):
        return self.datasets[self.curr_dataset].job_control(conf_obj)

    @property
    def dataset(self):
        return self.datasets[self.curr_dataset].dataset

    @property
    def nevents_orig(self):
        return self.datasets[self.curr_dataset].nevents_orig

    @property
    def events_per(self):
        return self.datasets[self.curr_dataset].events_per

    @events_per.setter
    def events_per(self, val):
        self.datasets[self.curr_dataset].events_per = val

    @property
    def total_events(self):
        return self.datasets[self.curr_dataset].total_events

    @total_events.setter
    def total_events(self, val):
        self.datasets[self.curr_dataset].total_events = val

    @property
    def json(self):
        return self.datasets[self.curr_dataset].json
        
    @json.setter
    def json(self, val):
        self.datasets[self.curr_dataset].json = val
        
    @property
    def run_range(self):
        return self.datasets[self.curr_dataset].run_range
        
    @run_range.setter
    def run_range(self, val):
        self.datasets[self.curr_dataset].run_range = val
        
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

########################################################################

class MCSample(Sample):
    def __init__(self, name, dataset, nevents_orig, **kwargs):
        super(MCSample, self).__init__(name, dataset, nevents_orig, **kwargs)

        self.nice = kwargs.get('nice', '')
        self.color = kwargs.get('color', -1)
        self.syst_frac = float(kwargs.get('syst_frac', -1))
        self.xsec = float(kwargs.get('xsec', -1)) # assumed pb

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
            
########################################################################

class DataSample(Sample):
    IS_MC = False
    def __init__(self, name, dataset, **kwargs):
        super(DataSample, self).__init__(name, dataset, -1, **kwargs)

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
        assert not self.d_samples.has_key(s.name)
        self.d_samples[s.name] = s

    def add_list(self, name, l):
        assert not self.d_lists.has_key(name)
        self.d_lists[name] = l

    def by_primary_dataset(self, pd):
        x = []
        for s in self.all():
            if s.primary_dataset == pd:
                x.append(s)
        return x

    def add_dataset_by_primary(self, ds_name, dataset, nevents_orig=-1, **kwargs):
        x = self.by_primary_dataset(dataset.split('/')[1])
        if len(x) != 1:
            raise ValueError('could not find sample for %s by primary dataset: %r' % (dataset, x))
        sample = x[0]
        sample.add_dataset(ds_name, dataset, nevents_orig, **kwargs)

    def from_argv(self, default=[], sort_and_set=True, from_root_fns=False, raise_if_none=False):
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

        if raise_if_none and not samples:
            raise ValueError('no samples found in argv')

        return samples if samples else default

    def known_datasets(self):
        ds = []
        for s in self.all():
            ds.extend(s.datasets.keys())
        return sorted(set(ds))

    def datasets_from_argv(self, default=[], sort_and_set=True, raise_if_none=False):
        check = 'fa_check' in sys.argv
        use_all = 'fa_all' in sys.argv

        ds = []
        if use_all:
            ds = self.known_datasets()
        else:
            known = self.known_datasets()
            for arg in sys.argv:
                if arg in known:
                    ds.append(arg)

        if sort_and_set:
            ds = sorted(set(ds))

        if check:
            print 'from_argv got these datasets:'
            for s in ds:
                print s
            raw_input('ok?')

        if raise_if_none and not ds:
            raise ValueError('no ds found in argv')

        return ds if ds else default
        
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
    l = [x for x in vars(namespace).itervalues() if issubclass(type(x), Sample)]
    l.sort(key=lambda x: -len(x.name))
    for x in l:
        if d.endswith(x.name):
            return x

def main(samples_registry):
    import sys

    if 'merge' in sys.argv:
        samples = samples_registry.from_argv(from_root_fns=True, raise_if_none=True)
        out_fn = [x for x in sys.argv if x.endswith('.root') and not os.path.isfile(x)]
        out_fn = out_fn[0] if out_fn else 'merge.root'
        norm_to = typed_from_argv(float, default_value=1.)
        norm_path = typed_from_argv(str, default_value='', name='norm_path')
        merge(samples, output=out_fn, norm_to=norm_to, norm_path=norm_path)

    elif 'ds' in sys.argv:
        samples = samples_registry.from_argv(raise_if_none=True)
        if len(samples) != 1:
            raise ValueError('must have exactly one sample in argv')
        sample = samples[0]
        dataset = sys.argv[sys.argv.index(sample.name)+1]
        if not sample.has_dataset(dataset):
            raise KeyError('no dataset %s in %s' % (dataset, sample))
        print sample.datasets[dataset].dataset

    elif 'file' in sys.argv:
        samples = samples_registry.from_argv(raise_if_none=True)
        if len(samples) != 1:
            raise ValueError('must have exactly one sample in argv')
        sample = samples[0]
        dataset = sys.argv[sys.argv.index(sample.name)+1]
        if not sample.has_dataset(dataset):
            raise KeyError('no dataset %s in %s' % (dataset, sample))
        sample.set_curr_dataset(dataset)
        for x in sample.filenames[:typed_from_argv(int, 5)]:
            print x

    elif 'site' in sys.argv:
        samples = samples_registry.from_argv(raise_if_none=True)
        dataset = samples_registry.datasets_from_argv()
        if len(dataset) > 1:
            raise ValueError('only zero/one dataset allowed')
        dataset = dataset[0] if len(dataset) == 1 else 'main'
        mlen = max(len(s.name) for s in samples)
        for sample in samples:
            sample.set_curr_dataset(dataset)
            try:
                sites = DBS.sites_for_dataset(sample.dataset)
            except RuntimeError:
                print sample.name, 'PROBLEM'
                continue
            print sample.name.ljust(mlen+5), ' '.join(s for s in sites if not s.endswith('_Buffer') and not s.endswith('_MSS'))

    elif 'samplefiles' in sys.argv:
        samples = samples_registry.from_argv(raise_if_none=True)
        dataset = 'main'
        for arg in sys.argv[1:]:
            if arg == 'miniaod' or arg.startswith('ntuple'):
                dataset = arg
                break
        print 'getting files for dataset %s:' % dataset, ', '.join(s.name for s in samples)
        import SampleFiles as sf
        d = {}
        for s in samples:
            if sf.has(s.name, dataset):
                raise KeyError('SampleFiles already has an entry for %s' % s.name)
            else:
                fns = s.filenames
                print 'DBS has %i files for %s' % (len(fns), s.name)
                d[(s.name, dataset)] = (len(fns), fns)
        print 'encoded line:'
        print "_add('%s')" % sf._enc(d)

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
