import os, sys, base64, cPickle as pickle
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
        if hasattr(self, 'samples_string'):
            details = pickle.loads(base64.b64decode(self.samples_string))
            details = sorted(details.items())
            self.samples = []
            self.__eps = {}
            for (kind_name, tau, mass), events in details:
                d = eval(kind_name), tau, mass
                self.samples.append(d)
                self.__eps[d] = events
        else:
            self.samples = list(product(self.kinds, self.taus, self.masses))

    def events_per_sample(self, kind, tau, mass):
        assert hasattr(self, 'samples_string')
        return self.__eps[(kind,tau,mass)]

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

class scanpackbase100epj(scanpackbase):
    events_per_job = 100

class scanpack1_100epj(scanpack1, scanpackbase100epj): # lol
    pass

class scanpack1p5(scanpackbase100epj):
    samples_string = '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'

####

def get_scanpack(x):
    return {
        'scanpacktest': scanpacktest,
        'scanpacktest2': scanpacktest2,
        'scanpack1': scanpack1,
        'scanpack1_100epj': scanpack1_100epj,
        'scanpack1p5': scanpack1p5,
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

if __name__ == '__main__' and len(sys.argv) > 1:
    cmd = sys.argv[1]

    if cmd == 'export':
        from JMTucker.Tools.CRAB3ToolsSh import crab_dirs_from_argv
        pprint(export_scanpack(crab_dirs_from_argv()))

    elif cmd == 'missing':
        fn = sys.argv[2]
        lst = eval(open(fn).read())
        scanpack = get_scanpack(os.path.basename(fn).replace('.list', ''))
        todo = {}

        for kind, tau, mass in scanpack.samples:
            name = scanpack.sample_name(kind, tau, mass)
            files = lst.get(name, [])
            nevents = scanpack.events_per_job * len(files)
            expected = scanpack.events_per_sample(kind, tau, mass)
            if not files:
                print 'empty', name
            elif expected > nevents:
                missing = todo[(kind.__name__,tau,mass)] = expected - nevents
                print 'incomplete', name, nevents, expected, missing
            elif expected == nevents:
                print 'done', name, expected
            else:
                assert 0

        pprint(todo)
        ps = pickle.dumps(todo, -1)
        print repr(base64.b64encode(ps))

    elif cmd == 'test':
        from gensim import process
        for batch in 0,1: #,2,3: #,4
            for job in xrange(5000):
                print batch, job,
                do_scanpack(process, 'scanpack1p5', batch, job)
