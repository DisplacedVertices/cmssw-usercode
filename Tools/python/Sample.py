#!/usr/bin/env python

import os, sys
from collections import defaultdict
from fnmatch import fnmatch
import JMTucker.Tools.DBS as DBS
from JMTucker.Tools.general import big_warn, typed_from_argv

########################################################################

class Dataset(object):
    HLT_NAME = 'HLT'
    DBS_INST = 'global'
    AAA = []

    def __init__(self, dataset, nevents, **kwargs):
        self.dataset = dataset
        self.nevents = nevents

        self.hlt_name = kwargs.get('hlt_name', self.HLT_NAME)
        self.dbs_inst = kwargs.get('dbs_inst', self.DBS_INST)
        self.aaa = kwargs.get('aaa', self.AAA)
        self.filenames = kwargs.get('filenames', [])

########################################################################

class Sample(object):
    IS_MC = True
    IS_FASTSIM = False
    GENERATOR = 'pythia8'

    def __init__(self, name, dataset, nevents, **kwargs):
        self.name = name
        self.curr_dataset = 'main'
        self.datasets = {'main': Dataset(dataset, nevents, **kwargs)}
        
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
    def nevents(self):
        return self.datasets[self.curr_dataset].nevents

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
    def filenames(self):
        fns = self.datasets[self.curr_dataset].filenames
        if not fns:
            fns = self.datasets[self.curr_dataset].filenames = DBS.files_in_dataset(self.dataset, **self.dbs_inst_dict(self.dbs_url_num))
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
    
    def __init__(self, name, dataset, nevents, **kwargs):
        super(MCSample, self).__init__(name, dataset, nevents, **kwargs)

        self.nice = kwargs.get('nice', '')
        self.color = kwargs.get('color', -1)
        self.syst_frac = float(kwargs.get('syst_frac', -1))
        self.xsec = float(kwargs.get('xsec', -1)) # assumed pb
        self.filter_eff = float(kwargs.get('filter_eff', -1))

        self.events_per = kwargs.get('events_per', self.EVENTS_PER)
        self.total_events = kwargs.get('total_events', self.TOTAL_EVENTS)

        self.join_info = (False, self.nice, self.color)

    @property
    def partial_weight(self):
        return self.xsec / float(self.nevents) # total weight = partial_weight * integrated_luminosity in 1/pb

    @property
    def int_lumi(self):
        return 1./self.partial_weight # units of 1/pb

    def job_control(self, conf_obj):
        conf_obj.splitting = 'EventAwareLumiBased'
        conf_obj.unitsPerJob = self.events_per
        conf_obj.totalUnits = self.total_events

########################################################################

class DataSample(Sample):
    IS_MC = False
    JSON = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/Cert_246908-260627_13TeV_PromptReco_Collisions15_25ns_JSON_Silver_v2.txt'
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
            name, dataset, nevents = line
        else:
            if len(line) == 2:
                dataset, nevents = line
            else:
                dataset = line[0]
                nevents = -1
            name = dataset.split('/')[1]
            uniq[name] += 1
            if uniq[name] > 1:
                name += str(uniq[name])
        sample = MCSample(name, dataset, nevents)
        for k,v in kwargs.iteritems():
            setattr(sample, k, v)
        samples.append(sample)
    return samples

def nevents_from_file(sample, hist_path, fn_pattern='%(name)s.root', f=None, last_bin=False):
    from JMTucker.Tools.ROOTTools import ROOT
    if f is None:
        fn = fn_pattern % sample
        if not os.path.isfile(fn):
            return -999
        f = ROOT.TFile(fn)
    h = f.Get(hist_path)
    if last_bin:
        return h.GetBinContent(h.GetNbinsX())
    else:
        return h.GetEntries()

def check_nevents_from_files(samples, hist_path, fn_pattern='%(name)s.root'):
    disagreements = []
    nofiles = []
    ok = []
    for sample in samples:
        n = nevents_from_file(sample, hist_path, fn_pattern)
        #print sample.name, n
        if n == -999:
            nofiles.append(sample.name)
            continue
        if n != sample.nevents:
            disagreements.append('%s.nevents = %i' % (sample.name, n))
        else:
            ok.append(sample.name)
    print 'these are OK: %s' % ' '.join(ok)
    print '(no files found for %s)' % ' '.join(nofiles)
    if disagreements:
        print '\n'.join(disagreements)
        raise ValueError('different numbers of events')

def get_nevents_ran(samples):
    diffs = []
    for sample in samples:
        x,y = sample.nevents, DBS.numevents_in_dataset(sample.dataset, sample.dbs_instance)
        print '%30s %14i %14i %14i %s' % (sample.name, x, y, x == y)
        if x != y:
            diffs.append((sample.name, y, x))
    print '\nsuggested change:'
    print
    for sample, y, x in diffs:
        print '%s.nevents_ran = %i' % diff
    print
    for sample, y, x in diffs:
        eff = float(y)/x
        if abs(eff - sample.filter_eff) > 1e-4:
            print '%s.filter_eff = %9.4e  # %8i / %8i' % (sample.name, eff, y, x)

def merge(samples, output='merge.root', norm_to=1.):
    if norm_to > 0:
        print 'norm sum of weights to', norm_to
    else:
        print 'multiply every weight by', -norm_to

    print 'taking nevents from samples'

    weights = []
    for sample in samples:
        weights.append(sample.partial_weight)

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

def main(samples_registry):
    import sys
    if 'merge' in sys.argv:
        samples = samples_registry.from_argv(from_root_fns=True)
        out_fn = [x for x in sys.argv if x.endswith('.root') and not os.path.isfile(x)]
        if out_fn:
            merge(samples, output=out_fn[0], norm_to=typed_from_argv(float, default_value=1.))
        else:
            merge(samples, norm_to=typed_from_argv(float, default_value=1.))

__all__ = [
    'Dataset',
    'Sample',
    'MCSample',
    'DataSample',
    'SamplesRegistry',
    'anon_samples',
    'nevents_from_file',
    'check_nevents_from_files',
    'get_nevents_ran',
    'merge',
    'main',
    ]
