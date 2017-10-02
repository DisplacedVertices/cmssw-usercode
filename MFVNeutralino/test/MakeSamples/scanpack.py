import os, sys
from collections import defaultdict
from itertools import product
from pprint import pprint
from modify import set_mfv_neutralino, set_gluino_ddbar

# !!! DO NOT CHANGE ANYTHING THAT CHANGES WHICH JOB IS WHICH SAMPLE ONCE BATCHES ARE RUN WITH THAT SCANPACK !!!
# unless you delete all the output from that scanpack.
# Make a new subclass and go from there. E.g. scanpackbase100epj exists to just change events_per_job going forward.
# Adding helper functions or anything that has no side effects to scanpackbase is fine.

# conventions:
# kind are one of the set_* functions from modify
# tau are float, in mm like pythia and modify
# mass are int, GeV

class scanpackbase(object):
    jobs_per_batch = 5000
    events_per_job = 200

    def __init__(self):
        self.name = self.__class__.__name__
        self.build_samples()
        self.njobs = 0
        self.job2isample = []
        for isample, (kind,tau,mass) in enumerate(self.samples):
            eps, epj = self.events_per_sample(kind,tau,mass), self.events_per_job
            assert eps > epj and eps % epj == 0
            njobs = eps / epj

            self.njobs += njobs
            self.job2isample += [isample]*njobs
        assert self.njobs > 0

        self.jobs_in_last_batch = self.njobs % self.jobs_per_batch
        if self.jobs_in_last_batch == 0:
            self.jobs_in_last_batch = self.jobs_per_batch

        int_ceil = lambda x,y: (x+y-1)/y
        self.nbatches = int_ceil(self.njobs, self.jobs_per_batch)
        self.ibatch = 0

    def build_samples(self):
        self.samples = list(product(self.kinds, self.taus, self.masses))

    def sample(self, batch, job):
        assert 0 <= batch < self.nbatches
        assert 0 <= job < self.jobs_per_batch
        if batch == self.nbatches - 1:
            assert job < self.jobs_in_last_batch
        return self.samples[self.job2isample[batch * self.jobs_per_batch + job]]

    def sample_name(self, kind, tau, mass):
        '''Samples-style naming'''
        kind = kind.__name__
        if kind == 'set_mfv_neutralino':
            kind = 'mfv_neu'
        elif kind == 'set_gluino_ddbar':
            kind = 'mfv_ddbar'
        else:
            raise ValueError('dunno %s' % kind)
        tau = int(tau*1000)
        return '%s_tau%05ium_M%04i' % (kind, tau, mass)

    def sample_details(self, name):
        '''inverse of sample_name'''
        kind, tau, mass = name.rsplit('_',2)
        if kind == 'mfv_neu':
            kind = set_mfv_neutralino
        elif kind == 'mfv_ddbar':
            kind = set_gluino_ddbar
        else:
            raise NameError('dunno %s' % kind)
        assert tau.startswith('tau') and tau.endswith('um')
        tau = int(tau[3:].replace('um','')) / 1000.
        assert mass.startswith('M')
        mass = int(mass[1:])
        return kind, tau, mass

    def isample(self, kind, tau, mass):
        target = kind, tau, mass
        for i,x in enumerate(self.samples):
            if x == target:
                return i

    def __iter__(self):
        for self.ibatch in xrange(self.nbatches):
            yield self

    @property
    def nevents(self):
        if self.ibatch < self.nbatches - 1:
            njobs = self.jobs_per_batch
        else:
            njobs = self.jobs_in_last_batch
        return self.events_per_job * njobs

    @property
    def batch_name(self):
        return '%s_%s' % (self.name, self.ibatch)

class scanpacktest(scanpackbase):
    kinds = [set_mfv_neutralino, set_gluino_ddbar]
    taus = [tau/1000. for tau in [100,10000]]
    masses = [400, 800]

    jobs_per_batch = 50
    events_per_job = 10
    def events_per_sample(self, kind, tau, mass):
        return 100

class scanpacktest2(scanpackbase):
    kinds = [set_mfv_neutralino, set_gluino_ddbar]
    taus = [tau/1000. for tau in [300,10000]]
    masses = [600, 800]

    jobs_per_batch = 39
    def events_per_sample(self, kind, tau, mass):
        return 1000

class scanpack1(scanpackbase):
    kinds = [set_mfv_neutralino, set_gluino_ddbar]
    taus = [tau/1000. for tau in range(100, 1000, 300) + range(1000, 40000, 3000) + range(40000, 1000001, 160000)]
    masses = range(300, 600, 100) + range(600, 3001, 200)

    def events_per_sample(self, kind, tau, mass):
        return 10000

def get_scanpack(x):
    return {
        'scanpacktest': scanpacktest,
        'scanpacktest2': scanpacktest2,
        'scanpack1': scanpack1,
        }[x]()

def do_scanpack(process, x, batch, job):
    sp = get_scanpack(x)
    set_kind, tau, mass = sp.sample(batch, job)
    print 'do_scanpack: %s nbatches %s njobs %s lastjobs %s batch %s job %s kind %s tau %s mass %s' % (x, sp.nbatches, sp.njobs, sp.jobs_in_last_batch, batch, job, set_kind.__name__, tau, mass)
    set_kind(process, tau, mass)

def export_scanpack(crab_dirs):
    from JMTucker.Tools.CRAB3ToolsSh import crab_hadd_files as crab_files

    sample_files = defaultdict(list)

    for wd in crab_dirs:
        bwd = os.path.basename(wd)

        _, scanpack, batch = bwd.split('_')
        batch = int(batch)
        scanpack = get_scanpack(scanpack)

        expected, files = crab_files(wd, True)
        assert expected == scanpack.jobs_per_batch or expected == scanpack.jobs_in_last_batch

        for fn in files:
            bn = os.path.basename(fn)
            if not bn.startswith('minitree'):
                continue

            job = int(bn.rsplit('_',1)[-1].replace('.root', '')) - 1
            kind, tau, mass = scanpack.sample(batch, job)
            sample_name = scanpack.sample_name(kind, tau, mass)
            sample_files[sample].append(fn)

    return dict(sample_files)

if __name__ == '__main__':
    todo = sys.argv[1]

    if todo == 'export':
        from JMTucker.Tools.CRAB3ToolsSh import crab_dirs_from_argv
        pprint(export_scanpack(crab_dirs_from_argv()))

    elif todo == 'missing':
        fn = sys.argv[2]
        lst = eval(open(fn).read())
        scanpack = get_scanpack(os.path.basename(fn).replace('.list', ''))

        for kind, tau, mass in scanpack.samples:
            name = scanpack.sample_name(kind, tau, mass)
            files = lst.get(name, [])
            nevents = scanpack.events_per_job * len(files)
            expected = scanpack.events_per_sample(kind, tau, mass)
            if not files:
                print 'empty', name
            elif expected > nevents:
                print 'incomplete', name, nevents, expected
            elif expected == nevents:
                print 'done', name, expected
            else:
                assert 0

    elif todo == 'test':
        from gensim import process
        for batch in 0,1,2,3: #,4
            for job in xrange(39):
                print batch, job,
                do_scanpack(process, 'scanpack1', batch, job)
