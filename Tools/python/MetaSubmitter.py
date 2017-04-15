import sys
from JMTucker.Tools.CRAB3Submitter import CRABSubmitter
from JMTucker.Tools.CondorSubmitter import CondorSubmitter

class max_output_modifier:
    def __init__(self, n):
        self.n = n
    def __call__(self, sample):
        return ['process.maxEvents.output = cms.untracked.int32(500)'], []

def is_mc_modifier(sample):
    to_replace = []
    if not sample.is_mc:
        magic = 'is_mc = True'
        to_replace.append((magic, 'is_mc = False', 'trying to submit on data, and tuple template does not contain the magic string "%s"' % magic))
    return [], to_replace

def H_modifier(sample):
    to_replace = []
    if sample.name.startswith('JetHT2016H'):
        magic = 'H = False'
        to_replace.append((magic, 'H = True', 'trying to submit on 2016H and no magic string "%s"' % magic))
    return [], to_replace

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

####

def set_splitting(samples, dataset, jobtype):
    target = {
        'ntuple': 5000
        }[jobtype]
    d = {
        'ntuple' : {
            # sample       # events to run to get 1 event out   corresponding file frac
            'ttbar'       :  ( 5.00E+01, 5.76E-03 ),
            'qcdht0500'   :  ( 5.00E+02, 6.03E-02 ),
            'qcdht0700'   :  ( 3.85E+01, 4.54E-03 ),
            'qcdht1000'   :  ( 1.54E+00, 2.42E-04 ),
            'qcdht1500'   :  ( 1.19E+00, 2.03E-04 ),
            'qcdht2000'   :  ( 1.23E+00, 1.65E-04 ),
            'qcdht0500ext':  ( 5.00E+02, 6.10E-02 ),
            'qcdht0700ext':  ( 3.85E+01, 4.53E-03 ),
            'qcdht1000ext':  ( 1.54E+00, 2.16E-04 ),
            'qcdht1500ext':  ( 1.19E+00, 1.92E-04 ),
            'qcdht2000ext':  ( 1.23E+00, 1.84E-04 ),
            'JetHT2015C'  :  ( 1.75E+01, 8.30E-04 ),
            'JetHT2015D'  :  ( 1.75E+01, 7.65E-04 ),
            'JetHT2016B3' :  ( 1.75E+01, 1.05E-03 ),
            'JetHT2016C'  :  ( 1.61E+01, 1.12E-03 ),
            'JetHT2016D'  :  ( 1.85E+01, 1.27E-03 ),
            'JetHT2016E'  :  ( 1.37E+01, 1.02E-03 ),
            'JetHT2016F'  :  ( 1.47E+01, 1.23E-03 ),
            'JetHT2016G'  :  ( 1.10E+01, 8.97E-04 ),
            'JetHT2016H2' :  ( 1.11E+01, 8.81E-04 ),
            'JetHT2016H3' :  ( 1.11E+01, 8.83E-04 ),
            }
        }
    for sample in samples:
        sample.set_curr_dataset(dataset)
        if not d.has_key(sample.name):
            if 'mfv' in sample.name:
                sample.events_per = 1000
                sample.files_per = 10
            else:
                sample.events_per = 50000
                sample.files_per = 5
        else:
            erate, frate = d[sample.name]
            sample.events_per = min(int(target * erate + 1), 200000)
            sample.files_per = int(frate * sample.events_per / erate + 1)
    
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

    def submit(self, samples):
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
