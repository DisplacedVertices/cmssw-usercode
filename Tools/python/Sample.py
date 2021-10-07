#!/usr/bin/env python

import os, sys
from collections import defaultdict
from fnmatch import fnmatch
from JMTucker.Tools import DBS

########################################################################

xrootd_sites = {
    'T3_US_FNALLPC': 'root://cmseos.fnal.gov/',
    'T1_US_FNAL_Disk': 'root://cmsxrootd-site.fnal.gov/',
    'T2_US_Nebraska': 'root://cmsxrootd.fnal.gov/',
    'T2_US_Wisconsin': 'root://pubxrootd.hep.wisc.edu/',
    'T2_US_Purdue': 'root://xrootd.rcac.purdue.edu/',
    'T2_DE_DESY': 'root://dcache-cms-xrootd.desy.de/',
    'T2_US_Florida': 'root://cmsio5.rc.ufl.edu/',
    'T2_US_MIT': 'root://xrootd.cmsaf.mit.edu/',
    'T2_US_UCSD': 'root://redirector.t2.ucsd.edu/',
    'global_redirect': 'root://cmsxrootd.fnal.gov/',
    }

########################################################################

class Dataset(object):
    EVENTS_PER = 25000
    TOTAL_EVENTS = -1
    FILES_PER = 10
    TOTAL_FILES = -1
    SPLIT_BY = 'files'
    JSON = ''
    HLT_NAME = 'HLT'
    DBS_INST = 'global'
    IGNORE_INVALID = False

    def __init__(self, dataset, nevents_orig, **kwargs):
        self.dataset = dataset
        self.nevents_orig = nevents_orig

        self.events_per = kwargs.get('events_per', self.EVENTS_PER)
        self.total_events = kwargs.get('total_events', self.TOTAL_EVENTS)
        self.files_per = kwargs.get('files_per', self.FILES_PER)
        self.total_files = kwargs.get('total_files', self.TOTAL_FILES)
        self.split_by = kwargs.get('split_by', self.SPLIT_BY)
        self.json = kwargs.get('json', self.JSON)
        self.run_range = kwargs.get('run_range', None)

        self.hlt_name = kwargs.get('hlt_name', self.HLT_NAME)
        self.dbs_inst = kwargs.get('dbs_inst', self.DBS_INST)
        self.ignore_invalid = kwargs.get('ignore_invalid', self.IGNORE_INVALID)
        self.condor = kwargs.get('condor', False)
        self.xrootd_url = kwargs.get('xrootd_url', '')
        self.notes = kwargs.get('notes', {})
        self.filenames = kwargs.get('filenames', [])

    def job_control(self, conf_obj):
        if self.split_by == 'events':
            conf_obj.splitting = 'EventAwareLumiBased'
            conf_obj.unitsPerJob = self.events_per
            conf_obj.totalUnits = self.total_events
        elif self.split_by == 'files':
            conf_obj.splitting = 'FileBased'
            conf_obj.unitsPerJob = self.files_per
            conf_obj.totalUnits = self.total_files
        if self.json:
            conf_obj.lumiMask = self.json
        if self.run_range:
            conf_obj.runRange = self.run_range

########################################################################

class Sample(object):
    IS_MC = True
    IS_FASTSIM = False
    GENERATOR = 'pythia8'

    NSAMPLES = 0

    def __init__(self, name, dataset, nevents_orig, **kwargs):
        self.name = name
        self.curr_dataset = 'main'
        self.datasets = {'main': Dataset(dataset, nevents_orig, **kwargs)}
        self.is_signal = False

        self.is_mc      = kwargs.get('is_mc',      self.IS_MC)
        self.is_fastsim = kwargs.get('is_fastsim', self.IS_FASTSIM)
        self.generator  = kwargs.get('generator',  self.GENERATOR)

        self.ready = True

        self.isample = Sample.NSAMPLES
        Sample.NSAMPLES += 1

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
    def files_per(self):
        return self.datasets[self.curr_dataset].files_per

    @files_per.setter
    def files_per(self, val):
        self.datasets[self.curr_dataset].files_per = val

    @property
    def total_files(self):
        return self.datasets[self.curr_dataset].total_files

    @total_files.setter
    def total_files(self, val):
        self.datasets[self.curr_dataset].total_files = val

    @property
    def split_by(self):
        return self.datasets[self.curr_dataset].split_by

    @split_by.setter
    def split_by(self, val):
        allowed = ('events', 'files')
        if val not in allowed:
            raise ValueError('split_by may only be one of %r while it is %r' % (allowed, val))
        self.datasets[self.curr_dataset].split_by = val

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
    def ignore_invalid(self):
        return self.datasets[self.curr_dataset].ignore_invalid

    @ignore_invalid.setter
    def ignore_invalid(self, val):
        self.datasets[self.curr_dataset].ignore_invalid = val

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
    def notes(self):
        return self.datasets[self.curr_dataset].notes

    @notes.setter
    def notes(self, val):
        self.datasets[self.curr_dataset].notes = val

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

    @filenames.setter
    def filenames(self, val):
        self.datasets[self.curr_dataset].filenames = val

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

def SumSample(name, samples):
    for sample in samples:
        assert sample.is_mc
    return MCSample(name, '/None/', sum(y.nevents_orig for y in samples), nice=samples[0].nice, color=samples[0].color, syst_frac=samples[0].syst_frac, xsec=samples[0].xsec)

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
            samples = sorted(set(samples), key=lambda s: s.isample)

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
        check = 'fa_ds_check' in sys.argv
        use_all = 'fa_ds_all' in sys.argv

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
            if dataset.endswith('.root'):
                name = os.path.basename(dataset).replace('.root', '')
            else:
                name = dataset.split('/')[1]
            uniq[name] += 1
            if uniq[name] > 1:
                name += str(uniq[name])
        filename = None
        if dataset.endswith('.root'):
            filename, dataset = dataset, '/%s/None/USER' % os.path.basename(dataset).replace('.root', '')
        sample = MCSample(name, dataset, nevents_orig)
        for k,v in kwargs.iteritems():
            setattr(sample, k, v)
        if filename:
            sample.filenames = [filename]
        samples.append(sample)
    return samples

def fn_to_sample(Samples, fn):
    sn = os.path.basename(fn).replace('.root', '')
    return sn, getattr(Samples, sn, None)

class sums_from_file(object):
    def __init__(self, f_or_fn, path=None):
        if type(f_or_fn) == str:
            from JMTucker.Tools.ROOTTools import ROOT
            self._f = ROOT.TFile.Open(f_or_fn)
        else:
            self._f = f_or_fn
        if path:
            self._h = self._f.Get(path)
        else:
            if hasattr(self._f, 'mcStat'):
                self._h = self._f.Get('mcStat/h_sums')
            elif hasattr(self._f, 'mfvWeight'):
                self._h = self._f.Get('mfvWeight/h_sums')
            else:
                raise ValueError("don't know where to get norm from %r" % f_or_fn)
        self._labels = [self._h.GetXaxis().GetBinLabel(ibin) for ibin in xrange(1, self._h.GetNbinsX()+1)]
        assert len(set(self._labels)) == len(self._labels)

        self._norm = None
        self._yearcode = None
        self._yearcodemult = 2371
        self._year = None
        self._nfiles = None

    def _get(self, bin_label):
        return self._h.GetBinContent(self._labels.index(bin_label)+1)

    def norm(self):
        if self._norm is None:
            self._norm = self._get('sum_nevents_total')
        return self._norm

    def norm_weight(self, weight_name):
        return self._get(weight_name)

    def yearcode(self):
        if self._yearcode is None:
            c = self._get('yearcode_x_nfiles')
            assert c.is_integer
            self._yearcode = int(c)
        return self._yearcode

    def year(self):
        if self._year is None:
            c = self.yearcode()
            for y in 2017, 2018:
                if c % (y*self._yearcodemult) == 0:
                    self._year = y
            if self._year is None:
                raise ValueError('not in sync with multiplier in Year.h? %s' % n)
        return self._year

    def nfiles(self):
        if self._nfiles is None:
            c,y = self.yearcode(), self.year()
            n = c / float(y*self._yearcodemult)
            assert n.is_integer()
            self._nfiles = int(n)
        return self._nfiles

def norm_from_file(f_or_fn, path=None):
    return sums_from_file(f_or_fn, path).norm()

def norm_from_file_weight(f_or_fn, path=None, weight_name=""):
    return sums_from_file(f_or_fn, path).norm_weight(weight_name)

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
    ocmd = cmd.split(' 2>&1')[0]
    print ocmd
    open(output + '.log', 'wt').write(ocmd)
    os.system(cmd)

def sample_from_end_string(namespace, d):
    l = [x for x in vars(namespace).itervalues() if issubclass(type(x), Sample)]
    l.sort(key=lambda x: -len(x.name))
    for x in l:
        if d.endswith(x.name):
            return x

def main(samples_registry):
    from glob import glob
    from sys import argv
    from pprint import pprint
    from JMTucker.Tools import colors
    from JMTucker.Tools.general import chunks, typed_from_argv

    samples = samples_registry.from_argv()
    datasets = samples_registry.datasets_from_argv()
    def prnt(*x):
        print ' '.join(str(y) for y in x)
    def runem(cb):
        for dataset in datasets:
            for sample in samples:
                if not sample.has_dataset(dataset):
                    print colors.yellow('no dataset %s for %s' % (dataset, sample.name))
                    continue
                sample.set_curr_dataset(dataset)
                cb(dataset, sample)

    if 'merge' in argv:
        samples = samples_registry.from_argv(from_root_fns=True, raise_if_none=True)
        out_fn = [x for x in argv if x.endswith('.root') and not os.path.isfile(x)]
        out_fn = out_fn[0] if out_fn else 'merge.root'
        norm_to = typed_from_argv(float, default_value=1.)
        norm_path = typed_from_argv(str, default_value='', name='norm_path')
        merge(samples, output=out_fn, norm_to=norm_to, norm_path=norm_path)

    elif 'printmissing' in argv:
        samples = [s.name for s in samples_registry.from_argv(raise_if_none=True)]
        samples.sort()
        look_for_root_files = 'no_root' not in sys.argv
        no_batch_dir, no_root_file = [], []
        for s in samples:
            if not os.path.isdir('condor_' + s) and not glob('crab_*_' + s):
                no_batch_dir.append(s)
            if not os.path.isfile('%s.root' % s):
                no_root_file.append(s)
        if no_batch_dir:
            print colors.yellow('no batch dir for these:')
            for s in no_batch_dir:
                print s
        if look_for_root_files and no_root_file:
            print colors.yellow('no root file for these:')
            for s in no_root_file:
                print s

    elif 'name' in argv:
        runem(lambda dataset, sample: prnt(sample.name, dataset))

    elif 'ds' in argv:
        runem(lambda dataset, sample: prnt(sample.name, dataset, sample.dataset))

    elif 'file' in argv:
        runem(lambda dataset, sample: [prnt(sample.name, dataset, x) for x in sample.filenames[:typed_from_argv(int, 5)]])

    elif 'nevents' in argv:
        runem(lambda dataset, sample: prnt(sample.name, dataset, DBS.numevents_in_dataset(sample.dataset)))

    elif 'files_for_events' in argv:
        rles = typed_from_argv(int, return_multiple=True)
        if len(rles) % 3 != 0:
            raise ValueError('expect list of ints in argv with length divisible by 3 [run1 lumi1 event1 ...]')
        rles = list(chunks(rles,3))
        runem(lambda dataset, sample: prnt(sample.name, dataset, ' '.join(DBS.files_for_events(rles, sample.dataset))))

    elif 'site' in argv:
        mlen = max(len(s.name) for s in samples)
        def cb(dataset, sample):
            ljname = sample.name.ljust(mlen+3)
            try:
                sites = DBS.sites_for_dataset(sample.dataset, json=True)
            except RuntimeError:
                print colors.boldred(ljname + ' DBS problem')
            else:
                print ljname,
                sites.sort(key=lambda x: x['name'])
                for site in sites:
                    if DBS.site_is_tape(site):
                        continue
                    is_complete = DBS.complete_at_site(site)
                    print (colors.green if is_complete else colors.yellow)(DBS.site_completions_string(site)), ' ',
                print
        runem(cb)

    elif 'samplefiles' in argv:
        import SampleFiles as sf
        def cb(dataset, sample):
            if sf.has(sample.name, dataset):
                raise KeyError('SampleFiles already has an entry for %s' % sample.name)
            fns = sample.filenames
            print 'DBS has %i files for %s' % (len(fns), sample.name)
            d = {(sample.name, dataset): (len(fns), fns)}
            print "('%s:%s', '%s')," % (sample.name, dataset, sf._enc(d))
        runem(cb)

    elif 'sfhas' in argv:
        neg = 'neg' in argv
        import SampleFiles as sf
        for dataset in datasets:
            for sample in samples:
                if sf.has(sample.name, dataset) != neg:
                    print sample.name

__all__ = [
    'xrootd_sites',
    'Dataset',
    'Sample',
    'MCSample',
    'DataSample',
    'SumSample',
    'SamplesRegistry',
    'anon_samples',
    'norm_from_file',
    'norm_from_file_weight',
    'merge',
    'sample_from_end_string',
    'main',
    ]
