import sys
from JMTucker.Tools.CRAB3Submitter import CRABSubmitter
from JMTucker.Tools.CondorSubmitter import CondorSubmitter

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

def H_modifier(sample):
    to_replace = []
    if '2016H' in sample.name:
        magic = 'H = False'
        to_replace.append((magic, 'H = True', 'trying to submit on 2016H and no magic string "%s"' % magic))
    return [], to_replace

def zerobias_modifier(sample):
    if sample.name.startswith('ZeroBias'):
        magic = 'zerobias = False'
        return [], [(magic, 'zerobias = True', 'trying to submit on ZeroBias and no magic string "%s"' % magic)]
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
from JMTucker.MFVNeutralino.WeightProducer_cfi import half_mc_by_lumi
half_mc_by_lumi(process, %r)
''' % self.first
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
from JMTucker.Tools.PileupWeights import get_pileup_weights
weights = get_pileup_weights(%r, %r)
for mname in %r:
     if hasattr(process, mname):
         getattr(process, mname).pileup_weights = weights
''' % (which, self.cross, self.module_names)
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

def set_splitting(samples, dataset, jobtype, data_json=None, default_files_per=20):
    def intround(x,y):
        return int(round(float(x)/y))

    if jobtype == 'trackmover':
        d = {
            'JetHT2015C':         ( 200000,    33),
            'JetHT2015D':         ( 665202,    29),
            'JetHT2016B3':        ( 288462,    17),
            'JetHT2016C':         ( 111940,     8),
            'JetHT2016D':         ( 245902,    17),
            'JetHT2016E':         ( 157895,    12),
            'JetHT2016F':         ( 104167,     9),
            'JetHT2016G':         ( 232826,    19),
            'JetHT2016H2':        ( 202703,    16),
            'JetHT2016H3':        ( 319149,    25),
            'qcdht0500':          (1657600,   200),
            'qcdht0500_2015':     (4762566,   333),
            'qcdht0500ext':       (1753088,   214),
            'qcdht0500ext_2015':  (4645127,   353),
            'qcdht0700':          (  98684,    12),
            'qcdht0700_2015':     ( 211212,    18),
            'qcdht0700ext':       ( 110422,    13),
            'qcdht0700ext_2015':  ( 200896,    16),
            'qcdht1000':          (  55762,     9),
            'qcdht1000_2015':     (  61176,     6),
            'qcdht1000ext':       (  56880,     8),
            'qcdht1000ext_2015':  (  60624,     6),
            'qcdht1500':          (  52785,     9),
            'qcdht1500_2015':     (  49775,     5),
            'qcdht1500ext':       (  49520,     8),
            'qcdht1500ext_2015':  (  48996,     4),
            'qcdht2000':          (  44922,     6),
            'qcdht2000_2015':     (  53304,     6),
            'qcdht2000ext':       (  40338,     6),
            'qcdht2000ext_2015':  (  49705,     5),
            'ttbar':              ( 399372,    46),
            'ttbar_2015':         ( 919380,    66),
            'qcdht1000_hip1p0_mit':( 55762,    25),
            'qcdht1500_hip1p0_mit':( 52785,     9),
            }
        for sample in samples:
            # prefer to split by file with CondorSubmitter  for these jobs to not overload xrootd aaa
            sample.set_curr_dataset(dataset)
            sample.split_by = 'files' if sample.condor else 'events'
            assert d.has_key(sample.name)
            sample.events_per = intround(d[sample.name][0], 4)
            sample.files_per  = intround(d[sample.name][1], 4)

    elif jobtype == 'histos' or jobtype == 'minitree':
        d = {
            'JetHT2015C': 2,
            'JetHT2015D': 67,
            'mfv_neu_tau00100um_M0300_2015': 2,
            'mfv_neu_tau00100um_M0400_2015': 2,
            'mfv_neu_tau00100um_M0800_2015': 2,
            'mfv_neu_tau00100um_M1200_2015': 2,
            'mfv_neu_tau00100um_M1600_2015': 2,
            'mfv_neu_tau00300um_M0300_2015': 2,
            'mfv_neu_tau00300um_M0400_2015': 2,
            'mfv_neu_tau00300um_M0800_2015': 2,
            'mfv_neu_tau00300um_M1200_2015': 2,
            'mfv_neu_tau00300um_M1600_2015': 2,
            'mfv_neu_tau01000um_M0300_2015': 2,
            'mfv_neu_tau01000um_M0400_2015': 2,
            'mfv_neu_tau01000um_M0800_2015': 2,
            'mfv_neu_tau01000um_M1200_2015': 2,
            'mfv_neu_tau01000um_M1600_2015': 2,
            'mfv_neu_tau10000um_M0300_2015': 2,
            'mfv_neu_tau10000um_M0400_2015': 2,
            'mfv_neu_tau10000um_M0800_2015': 2,
            'mfv_neu_tau10000um_M1200_2015': 2,
            'mfv_neu_tau10000um_M1600_2015': 2,
            'qcdht0500_2015': 229,
            'qcdht0500ext_2015': 269,
            'qcdht0700_2015': 93,
            'qcdht0700ext_2015': 141,
            'qcdht1000_2015': 10,
            'qcdht1000ext_2015': 15,
            'qcdht1500_2015': 12,
            'qcdht1500ext_2015': 12,
            'qcdht2000_2015': 8,
            'qcdht2000ext_2015': 10,
            'ttbar_2015': 168,
            'JetHT2016B3': 95,
            'JetHT2016C': 76,
            'JetHT2016D': 98,
            'JetHT2016E': 90,
            'JetHT2016F': 81,
            'JetHT2016G': 73,
            'JetHT2016H2': 115,
            'JetHT2016H3': 21,
            'mfv_ddbar_tau00100um_M0300': 50,
            'mfv_ddbar_tau00100um_M0400': 50,
            'mfv_ddbar_tau00100um_M0500': 50,
            'mfv_ddbar_tau00100um_M0600': 50,
            'mfv_ddbar_tau00100um_M0800': 50,
            'mfv_ddbar_tau00100um_M1200': 50,
            'mfv_ddbar_tau00100um_M1600': 50,
            'mfv_ddbar_tau00300um_M0300': 50,
            'mfv_ddbar_tau00300um_M0400': 50,
            'mfv_ddbar_tau00300um_M0500': 50,
            'mfv_ddbar_tau00300um_M0600': 50,
            'mfv_ddbar_tau00300um_M0800': 50,
            'mfv_ddbar_tau00300um_M1200': 50,
            'mfv_ddbar_tau00300um_M1600': 50,
            'mfv_ddbar_tau01000um_M0300': 50,
            'mfv_ddbar_tau01000um_M0400': 50,
            'mfv_ddbar_tau01000um_M0500': 50,
            'mfv_ddbar_tau01000um_M0600': 50,
            'mfv_ddbar_tau01000um_M0800': 50,
            'mfv_ddbar_tau01000um_M1200': 50,
            'mfv_ddbar_tau01000um_M1600': 50,
            'mfv_ddbar_tau10000um_M0300': 50,
            'mfv_ddbar_tau10000um_M0400': 50,
            'mfv_ddbar_tau10000um_M0500': 50,
            'mfv_ddbar_tau10000um_M0600': 50,
            'mfv_ddbar_tau10000um_M0800': 50,
            'mfv_ddbar_tau10000um_M1200': 50,
            'mfv_ddbar_tau10000um_M1600': 50,
            'mfv_ddbar_tau30000um_M0300': 50,
            'mfv_ddbar_tau30000um_M0400': 50,
            'mfv_ddbar_tau30000um_M0500': 50,
            'mfv_ddbar_tau30000um_M0600': 50,
            'mfv_ddbar_tau30000um_M0800': 50,
            'mfv_ddbar_tau30000um_M1200': 50,
            'mfv_ddbar_tau30000um_M1600': 50,
            'mfv_neu_tau00100um_M0300': 26,
            'mfv_neu_tau00100um_M0400': 54,
            'mfv_neu_tau00100um_M0600': 50,
            'mfv_neu_tau00100um_M0800': 7,
            'mfv_neu_tau00100um_M1200': 36,
            'mfv_neu_tau00100um_M1600': 8,
            'mfv_neu_tau00100um_M3000': 49,
            'mfv_neu_tau00300um_M0300': 1,
            'mfv_neu_tau00300um_M0400': 50,
            'mfv_neu_tau00300um_M0600': 100,
            'mfv_neu_tau00300um_M0800': 7,
            'mfv_neu_tau00300um_M1200': 27,
            'mfv_neu_tau00300um_M1600': 1,
            'mfv_neu_tau00300um_M3000': 49,
            'mfv_neu_tau01000um_M0300': 9,
            'mfv_neu_tau01000um_M0400': 48,
            'mfv_neu_tau01000um_M0600': 100,
            'mfv_neu_tau01000um_M0800': 4,
            'mfv_neu_tau01000um_M1200': 6,
            'mfv_neu_tau01000um_M1600': 1,
            'mfv_neu_tau01000um_M3000': 47,
            'mfv_neu_tau10000um_M0300': 12,
            'mfv_neu_tau10000um_M0400': 51,
            'mfv_neu_tau10000um_M0600': 50,
            'mfv_neu_tau10000um_M0800': 1,
            'mfv_neu_tau10000um_M1200': 4,
            'mfv_neu_tau10000um_M1600': 5,
            'mfv_neu_tau10000um_M3000': 48,
            'mfv_neu_tau30000um_M0300': 50,
            'mfv_neu_tau30000um_M0400': 50,
            'mfv_neu_tau30000um_M0600': 50,
            'mfv_neu_tau30000um_M0800': 50,
            'mfv_neu_tau30000um_M1200': 50,
            'mfv_neu_tau30000um_M1600': 50,
            'mfv_neu_tau30000um_M3000': 49,
            'my_mfv_neu_tau00300um_M0800': 100,
            'qcdht0500': 229,
            'qcdht0500ext': 269,
            'qcdht0700': 93,
            'qcdht0700ext': 141,
            'qcdht1000': 10,
            'qcdht1000ext': 15,
            'qcdht1500': 12,
            'qcdht1500ext': 12,
            'qcdht2000': 8,
            'qcdht2000ext': 10,
            'ttbar': 168,
            }
        for sample in samples:
            sample.set_curr_dataset(dataset)
            sample.split_by = 'files'
            n = sample.name.replace('_hip1p0_mit', '').replace('_hip1p0', '').replace('_retest', '')
            sample.files_per = d.get(n, 20)

    elif jobtype == 'ntuple':
        # Shed/presel_splitting.py
        d = {'miniaod': {
                'signal':           ( 1,     200),
                'JetHT':            (25, 2250000),
                'qcdht0700_2017':   (50, 3130000),
                'qcdht1000_2017':   (11,  551000),
                'qcdht1500_2017':   ( 4,  186000),
                'qcdht2000_2017':   ( 5,  202000),
                'ttbar_2017':       (50, 3040000),
                'ttbarht0600_2017': (10,  143000),
                'ttbarht0800_2017': ( 6,   90000),
                'ttbarht1200_2017': ( 6,   65000),
                'ttbarht2500_2017': ( 6,   55000),
                }
             }
        assert dataset == 'miniaod'

        for sample in samples:
            sample.set_curr_dataset(dataset)
            sample.split_by = 'files'

            name = sample.name

            if name.startswith('JetHT'):
                name = 'JetHT'
            elif sample.is_signal:
                name = 'signal'
                sample.split_by = 'events'

            sample.files_per, sample.events_per = d[dataset].get(name, (50, 100000))

    elif jobtype == 'default':
        for sample in samples:
            sample.set_curr_dataset(dataset)
            sample.split_by = 'files'
            sample.files_per = default_files_per 

    else:
        raise ValueError("don't know anything about jobtype %s" % jobtype)

    if data_json:
        for sample in samples:
            if not sample.is_mc:
                sample.json = data_json

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
        from JMTucker.Tools.Year import year
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
    'CRABSubmitter',
    'CondorSubmitter',
    'MetaSubmitter',
    'set_splitting',
    'max_output_modifier',
    'is_mc_modifier',
    'H_modifier',
    'zerobias_modifier',
    'repro_modifier',
    'half_mc_modifier',
    'per_sample_pileup_weights_modifier',
    'event_veto_modifier',
    'chain_modifiers',
    'secondary_files_modifier',
    ]
