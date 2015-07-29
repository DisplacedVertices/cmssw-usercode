#!/usr/bin/env python

import os, sys
from fnmatch import fnmatch
import JMTucker.Tools.DBS as DBS
from JMTucker.Tools.general import big_warn

########################################################################

class Dataset(object):
    HLT_NAME = 'HLT'
    DBS_INST = 'global'

    def __init__(self, dataset, nevents, **kwargs):
        self.dataset = dataset
        self.nevents = nevents

        self.hlt_process_name = kwargs.get('hlt_name', self.HLT_NAME)
        self.dbs_instance     = kwargs.get('dbs_inst', self.DBS_INST)
        self.filenames        = kwargs.get('filenames', [])

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

    @property
    def dataset(self):
        return self.datasets[self.curr_dataset].dataset

    @property
    def nevents(self):
        return self.datasets[self.curr_dataset].nevents

    @property
    def primary_dataset(self):
        return self.dataset.split('/')[1]

    @property
    def filenames(self):
        if self.dataset.filenames:
            return self.dataset.filenames
        else:
            return DBS.files_in_dataset(self.dataset, **self.dbs_inst_dict(self.dbs_url_num))

    def __getitem__(self, key):
        return getattr(self, key)

    def job_control(self, conf_obj):
        raise NotImplementedError('job_control needs to be implemented')

########################################################################

class MCSample(Sample):
    EVENTS_PER = 5000
    
    def __init__(self, name, dataset, nevents, **kwargs):
        super(MCSample, self).__init__(name, dataset, nevents, **kwargs)

        self.nice = kwargs.get('nice', '')
        self.color = kwargs.get('color', -1)
        self.syst_frac = float(kwargs.get('syst_frac', -1))
        self.xsec = float(kwargs.get('xsec', -1)) # assumed pb
        self.filter_eff = float(kwargs.get('filter_eff', -1))

        self.events_per = kwargs.get('events_per', self.EVENTS_PER)

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
        conf_obj.totalUnits = self.nevents_ran

########################################################################

class DataSample(Sample):
    IS_MC = False
    JSON = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/Cert_246908-251883_13TeV_PromptReco_Collisions15_JSON_v2.txt'
    LUMIS_PER = 30
    TOTAL_LUMIS = -1

    def __init__(self, name, dataset, **kwargs):
        super(DataSample, self).__init__(name, dataset, -1, **kwargs)

        self.run_range = kwargs.get('run_range', None)
        self.json = kwargs.get('json', self.JSON)

        self.lumis_per = kwargs.get('lumis_per', self.LUMIS_PER)
        self.total_lumis = kwargs.get('total_lumis', self.TOTAL_LUMIS)

    def lumi_mask(self):
        # JMTBAD run_range checking
        if type(self.json) == str:
            return 'lumi_mask', self.json
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

    def from_argv(self, default=None, sort_and_set=True):
        ready_only = 'fa_ready_only' in sys.argv
        check = 'fa_check' in sys.argv
        use_all = 'fa_all' in sys.argv

        samples = []

        if use_all:
            samples = self.all()
        else:
            for arg in sys.argv:
                by_match = any(c in arg for c in '[]*?!')
                for sample in self.d_samples.values():
                    if arg == sample.name or (by_match and fnmatch(sample.name, arg)):
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

def anon_samples(txt):
    samples = []
    lines = [line.strip() for line in txt.split('\n') if line.strip()]
    for i, line in enumerate(lines):
        line = line.split()
        if len(line) == 3:
            name, dataset, nevents = line
        elif len(line) == 2:
            dataset, nevents = line
            name = 'anon%03i' % i
        samples.append(MCSample(name, dataset, nevents))
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
        if abs(eff - sample.ana_filter_eff) > 1e-4:
            print '%s.filter_eff = %9.4e  # %8i / %8i' % (sample.name, eff, y, x)

def merge(samples, output='merge.root', norm_to=1, path_for_nevents='', last_bin=False):
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
            sample.nevents = nevents_from_file(sample, path_for_nevents, fn, last_bin=last_bin)
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
    'merge'
    ]
