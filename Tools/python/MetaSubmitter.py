import sys, re
from DVCode.Tools.CRAB3Submitter import CRABSubmitter
from DVCode.Tools.CondorSubmitter import CondorSubmitter, NtupleReader_submit
from DVCode.Tools.Year import year
from DVCode.Tools import Samples

class max_output_modifier:
    def __init__(self, n):
        self.n = n
    def __call__(self, sample):
        return ['process.maxEvents.output = cms.untracked.int32(%i)' % self.n], []

def is_mc_modifier(sample):
    to_replace = []
    if not sample.is_mc:
        magic = 'is_mc = True'
        to_replace.append((magic, 'is_mc = False', 'trying to submit on data, and tuple template does not contain the magic string "%s"' % magic))
    return [], to_replace

def zerobias_modifier(sample):
    if sample.name.startswith('ZeroBias'):
        magic = 'zerobias = False'
        return [], [(magic, 'zerobias = True', 'trying to submit on ZeroBias and no magic string "%s"' % magic)]
    else:
        return [], []

def era_modifier(sample):
    if not sample.is_mc:
        mo = re.search(r'(201\d)([A-Z])', sample.name)
        assert mo
        yr, era = mo.groups()
        assert year == int(yr)
        magic = '\nsettings.is_mc ='
        return [], [(magic, ('\nsettings.era = "%s"' % era) + magic, 'trying to submit on data and no magic string %r' % magic)]
    else:
        return [], []

def repro_modifier(sample):
    if sample.name.startswith('Repro'):
        magic = 'repro = False'
        return [], [(magic, 'repro = True', 'trying to submit on reprocessed dataset and no magic string "%s"' % magic)]
    else:
        return [], []

class half_mc_modifier:
    def __init__(self, first=True):
        self.first = first
    def __call__(self, sample):
        if sample.is_mc:
            x = '''
from DVCode.MFVNeutralino.WeightProducer_cfi import half_mc_by_lumi
half_mc_by_lumi(process, %r)
''' % self.first
            return [x], []
        else:
            return [], []

class quarter_mc_modifier:
    def __init__(self, first=True, second=False, third=False, fourth=False):
        self.first = first
        self.second = second
        self.third = third
        self.fourth = fourth
    def __call__(self, sample):
        if sample.is_mc:
            x = '''
from DVCode.MFVNeutralino.WeightProducer_cfi import quarter_mc_by_lumi
quarter_mc_by_lumi(process, %r, %r, %r, %r)
''' % (self.first, self.second, self.third, self.fourth)
            return [x], []
        else:
            return [], []

class npu_filter_modifier:
    def __init__(self, is_miniaod=False, samples={'qcdht0700_2017': 131, 'dyjetstollM10_2017': 126, 'dyjetstollM50_2017': 131, 'dyjetstollM50ext_2017': 129}, paths_to_skip=['pmcStat']):
        self.is_miniaod = is_miniaod
        self.samples = samples
        self.paths_to_skip = paths_to_skip
    def __call__(self, sample):
        if sample.name in self.samples:
            which = 'MiniAOD' if self.is_miniaod else ''
            max_npu = self.samples[sample.name]
            paths_to_skip = self.paths_to_skip
            x = '''
process.load('DVCode.Tools.NpuFilter_cfi')
process.jmtNpuFilter%(which)s.max_npu = %(max_npu)i
for n,p in process.paths.iteritems():
    if n not in %(paths_to_skip)r:
        p.insert(0, process.jmtNpuFilter%(which)s)
''' % locals()
            return [x], []
        else:
            return [], []

class per_sample_pileup_weights_modifier:
    def __init__(self, module_names=['jmtWeight', 'jmtWeightMiniAOD', 'mfvWeight'], cross=None):
        if type(module_names) == str:
            module_names = [module_names]
        self.module_names = module_names
        self.cross = cross
    def __call__(self, sample):
        if sample.is_mc:
            which = sample.name
            if sample.is_signal and sample.is_private:
                which = 'mfv_signals'
            x = '''
from DVCode.Tools.PileupWeights import get_pileup_weights
weights = get_pileup_weights(%r, %r)
''' % (which, self.cross)
            if self.module_names == 'auto':
                x += '''
for mname in dir(process):
    if hasattr(getattr(process, mname), 'pileup_weights'):
        getattr(process, mname).pileup_weights = weights
'''
            else:
                x += '''
for mname in %r:
     if hasattr(process, mname):
         getattr(process, mname).pileup_weights = weights
''' % self.module_names
            return [x], []
        else:
            return [], []

class event_veto_modifier:
    def __init__(self, d, filter_path):
        self.d = d
        self.filter_path = filter_path
    def __call__(self, sample):
        to_add, to_replace = [], []
        if self.d.has_key(sample.name):
            d2 = self.d[sample.name]
            if d2.has_key('runs'):
                x = '''
process.eventVeto = cms.EDFilter('EventIdVeto',
                                 list_fn = cms.string(''),
                                 use_run = cms.bool(True),
                                 runs = cms.vuint32(%(runs)s),
                                 lumis = cms.vuint32(%(lumis)s),
                                 events = cms.vuint64(%(events)s))
process.FILTER_PATH.insert(0, process.eventVeto)
'''.replace('FILTER_PATH', self.filter_path)
            else:
                x = '''
process.eventVeto = cms.EDFilter('EventIdVeto',
                                 list_fn = cms.string(''),
                                 use_run = cms.bool(False),
                                 lumis = cms.vuint32(%(lumis)s),
                                 events = cms.vuint64(%(events)s))
process.FILTER_PATH.insert(0, process.eventVeto)
'''.replace('FILTER_PATH', self.filter_path)
            to_add = [x % d2]
        return to_add, to_replace

class chain_modifiers:
    def __init__(self, *modifiers):
        self.modifiers = list(modifiers)
    def append(self, x):
        self.modifiers.append(x)
    def __call__(self, sample):
        to_add, to_replace = [], []
        for m in self.modifiers:
            a,b = m(sample)
            to_add.extend(a)
            to_replace.extend(b)
        return to_add, to_replace

class secondary_files_modifier:
    def __init__(self, dataset=None, fns=None, use_sample_xrootd_url=True):
        if (not dataset and not fns) or (dataset and fns):
            raise ValueError('must specify exactly one of dataset (string with dataset name) or fns (list with filenames)')
        if use_sample_xrootd_url and not dataset:
            raise ValueError('if use_sample_xrootd_url, must specify dataset and not fns')
        self.dataset, self.fns = dataset, fns
        self.use_sample_xrootd_url = use_sample_xrootd_url

    def __call__(self, sample):
        if self.dataset:
            save_ds = sample.curr_dataset
            sample.set_curr_dataset(self.dataset)
            fns = sample.filenames
            if self.use_sample_xrootd_url and sample.xrootd_url:
                fns = [sample.xrootd_url + fn for fn in fns]
            sample.set_curr_dataset(save_ds)
        elif self.fns:
            fns = self.fns

        to_add = [
            'jmt_secondary_files_modifier_secondaryFileNames = %r' % fns,
            'process.source.secondaryFileNames = cms.untracked.vstring(*jmt_secondary_files_modifier_secondaryFileNames)'
            ]
        return to_add, []

####

def set_splitting(samples, dataset, jobtype='default', data_json=None, default_files_per=20, limit_ttbar=False):
    if jobtype == 'histos' or jobtype == 'minitree':
        d = {
            'qcdht1000_2017': 11,
            'qcdht1500_2017': 11,
            'qcdht2000_2017': 11,
            'ttbar_2017': 22,
            'ttbarht0600_2017': 8,
            'ttbarht0800_2017': 8,
            'ttbarht1200_2017': 8,
            'ttbarht2500_2017': 8,
            'qcdht1000_2018': 11,
            'qcdht1500_2018': 11,
            'qcdht2000_2018': 11,
            'ttbar_2018': 22,
            'ttbarht0600_2018': 8,
            'ttbarht0800_2018': 8,
            'ttbarht1200_2018': 8,
            'ttbarht2500_2018': 8,
            }
        for sample in samples:
            sample.set_curr_dataset(dataset)
            sample.split_by = 'files'
            sample.files_per = d.get(sample.name, 10000)

    elif jobtype == 'ntuple' or jobtype == 'trackmover':
        # Shed/presel_splitting.py
        d = {'miniaod': {
                'signal':           ( 1,     200),
                'JetHT':            (15, 1350000),
                'qcdht0300_2017':   (50, 3130000),
                'qcdht0500_2017':   (50, 3130000),
                'qcdht0700_2017':   (50, 3130000),
                'qcdht1000_2017':   (11,  551000),
                'qcdht1500_2017':   ( 4,  186000),
                'qcdht2000_2017':   ( 5,  202000),
                'ttbar_2017':       (50, 3040000),
                'ttbarht0600_2017': ( 5,   71500),
                'ttbarht0800_2017': ( 3,   45000),
                'ttbarht1200_2017': ( 3,   32500),
                'ttbarht2500_2017': ( 3,   27500),
                'qcdht0300_2018':   (50, 3130000),
                'qcdht0500_2018':   (50, 3130000),
                'qcdht0700_2018':   (50, 3130000),
                'qcdht1000_2018':   (11,  551000),
                'qcdht1500_2018':   ( 4,  186000),
                'qcdht2000_2018':   ( 5,  202000),
                'ttbar_2018':       (50, 3040000),
                'ttbarht0600_2018': ( 5,   71500),
                'ttbarht0800_2018': ( 3,   45000),
                'ttbarht1200_2018': ( 3,   32500),
                'ttbarht2500_2018': ( 3,   27500),
                }
             }
        assert dataset == 'miniaod'

        for sample in samples:
            sample.set_curr_dataset(dataset)
            sample.split_by = 'files'
            name = sample.name

            if 'JetHT' in name:
                name = 'JetHT'
            elif sample.is_signal:
                name = 'signal'
                sample.split_by = 'events'

            sample.files_per, sample.events_per = d[dataset].get(name, (50, 100000))

            if jobtype == 'trackmover':
                if name.startswith('ttbarht'):
                    fp = sample.files_per
                    sample.events_per /= fp
                    sample.files_per = 1
                elif name != 'signal':
                    sample.files_per = int(round(sample.files_per / 3.))
                    sample.events_per /= 3

    elif jobtype == 'default':
        for sample in samples:
            sample.set_curr_dataset(dataset)
            sample.split_by = 'files'
            sample.files_per = default_files_per 

    else:
        raise ValueError("don't know anything about jobtype %s" % jobtype)

    if limit_ttbar:
        d = { # get ~400/fb
            'ttbarht0600_2017':  (20, 726800),
            'ttbarht0800_2017':  ( 8, 300800),
            'ttbarht1200_2017':  ( 2,  52500),
            'ttbarht2500_2017':  ( 1,   1000),
            'ttbarht0600_2018':  (25, 726800),
            'ttbarht0800_2018':  (11, 300800),
            'ttbarht1200_2018':  ( 2,  52500),
            'ttbarht2500_2018':  ( 1,   1000),
            }
        for sample in samples:
            n = d.get(sample.name)
            if n:
                sample.total_files, sample.total_events = n

    if data_json:
        for sample in samples:
            if not sample.is_mc:
                sample.json = data_json

####

def pick_samples(dataset, both_years=False,
                 qcd=True, ttbar=True, all_signal=True, data=True, leptonic=False, bjet=False,
                 span_signal=False):

    if span_signal:
        print 'cannot use both span and all_signal, turning off the latter'
        all_signal = False

    argnames = 'qcd', 'ttbar', 'all_signal', 'span_signal', 'data', 'leptonic', 'bjet'
    args = dict([(a,eval(a)) for a in argnames])
    if not set(args.values()).issubset([True, False, 'only']):
        raise ValueError('arg must be one of True, False, "only"')

    onlys = [a for a in args if args[a] == 'only']
    if len(onlys) > 1:
        raise ValueError('only one only allowed')
    elif len(onlys) == 1:
        a = onlys[0]
        args[a] = True
        for a2 in args:
            if a2 != a:
                args[a2] = False

    years = [2017, 2018] if both_years else [year]

    samples = []
    for a in argnames:
        if args[a]:
            for yr in years:
                samples += getattr(Samples, '%s_samples_%i' % (a, yr))
    return [s for s in samples if s.has_dataset(dataset)]

####

class MetaSubmitter:
    class args:
        pass

    def __init__(self, batch_name, dataset='main', override=None):
        self.testing = 'testing' in sys.argv or 'cs_testing' in sys.argv
        self.batch_name = batch_name
        self.common = MetaSubmitter.args()
        self.common.dataset = dataset
        self.crab = MetaSubmitter.args()
        self.condor = MetaSubmitter.args()
        self.override = override

    def normalize(self):
        assert not hasattr(self.common, 'ex')
        self.common.ex = year
        if not hasattr(self.common, 'publish_name'):
            self.common.publish_name = '%s_%s' % (self.batch_name, year)
        if not hasattr(self.crab, 'job_control_from_sample'):
            self.crab.job_control_from_sample = True

    def submit(self, samples):
        self.normalize()

        crab_samples, condor_samples = [], []
        for s in samples:
            s.set_curr_dataset(self.common.dataset)
            if s.condor or self.override == 'condor':
                condor_samples.append(s)
            elif not s.condor or self.override == 'crab':
                crab_samples.append(s)

        if self.testing:
            print 'MetaSubmitter: crab samples ='
            for s in crab_samples:
                print s.name
            print 'MetaSubmitter: condor samples ='
            for s in condor_samples:
                print s.name

        if crab_samples:
            args = dict(self.common.__dict__)
            args.update(self.crab.__dict__)
            cs = CRABSubmitter(self.batch_name, **args)
            cs.submit_all(crab_samples)
        if condor_samples:
            args = dict(self.common.__dict__)
            args.update(self.condor.__dict__)
            cs = CondorSubmitter(self.batch_name, **args)
            cs.submit_all(condor_samples)

####

__all__ = [
    'year',
    'Samples',
    'CRABSubmitter',
    'CondorSubmitter',
    'NtupleReader_submit',
    'MetaSubmitter',
    'pick_samples',
    'set_splitting',
    'max_output_modifier',
    'is_mc_modifier',
    'zerobias_modifier',
    'era_modifier',
    'repro_modifier',
    'half_mc_modifier',
    'quarter_mc_modifier',
    'npu_filter_modifier',
    'per_sample_pileup_weights_modifier',
    'event_veto_modifier',
    'chain_modifiers',
    'secondary_files_modifier',
    ]
