import sys
from JMTucker.Tools.CRAB3Submitter import CRABSubmitter
from JMTucker.Tools.CondorSubmitter import CondorSubmitter

def is_mc_pset_modifier(sample):
    to_replace = []
    if not sample.is_mc:
        magic = 'is_mcX=XTrue'.replace('X', ' ')
        err = 'trying to submit on data, and tuple template does not contain the magic string "%s"' % magic
        to_replace.append((magic, 'is_mc = False', err))
    return [], to_replace

class MetaSubmitter:
    class args:
        pass

    def __init__(self, batch_name, dataset='main'):
        self.testing = 'testing' in sys.argv or 'cs_testing' in sys.argv
        self.batch_name = batch_name
        self.common = MetaSubmitter.args()
        self.common.dataset = dataset
        self.crab = MetaSubmitter.args()
        self.condor = MetaSubmitter.args()

    def submit(self, samples):
        crab_samples, condor_samples = [], []
        for s in samples:
            s.set_curr_dataset(self.common.dataset)
            (condor_samples if s.condor else crab_samples).append(s)

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
