import os
import sys
from pprint import pprint
from time import time
from JMTucker.Tools.CRAB3Tools import crab_dirs_root
from JMTucker.Tools.general import save_git_status, bool_from_argv
from JMTucker.Tools import colors
import ROOT; ROOT.gROOT.SetBatch()
import limitsinput

if os.path.basename(os.getcwd()) != 'One2Two':
    raise EnvironmentError('must be in One2Two dir')

class Submitter(object):
    def __init__(self):
        self.testing = bool_from_argv('testing') # just exercising this script
        self.submit_test = bool_from_argv('submit_test') # submit the job but don't run combine
        self.njobs_per_point = 2 if bool_from_argv('2jobs') else 50
        self.points_per_batch = 2 if bool_from_argv('2points') else 100
        self.njobs_per_batch = self.points_per_batch * self.njobs_per_point
        assert self.njobs_per_batch <= 5000
        self.test_batch = bool_from_argv('test_batch') # passed to limitsinput.sample_iterator
        self.slices_1d = bool_from_argv('slices_1d')
        self.save_toys = bool_from_argv('save_toys')
        self.include_2016 = bool_from_argv('include_2016')
        self.no_expected = bool_from_argv('no_expected')
        self.no_systematics = bool_from_argv('no_systematics')
        self.goodness_of_fit = bool_from_argv('goodness_of_fit')
        self.significance = bool_from_argv('significance')
        datacard_args = [x for x in ['bkg_fully_correlated', 'bkg_yearwise_correlated', 'bkg_binwise_correlated', 'bkg_mixed_correlated', 'bkg_fully_correlated'] if bool_from_argv(x)]

        if len(sys.argv) != 2:
            raise ValueError('need a str for the batch dir name (argv is %r)' % sys.argv)
        self.ex = sys.argv[1]
        if not self.ex.startswith('_'):
            self.ex = '_' + self.ex

        self.years = ('2016','2017','2018') if self.include_2016 else ('2017','2018')

        if len(datacard_args) > 1:
            raise ValueError('only one bkg_*_correlated option allowed')
        if self.include_2016:
            datacard_args.append('include_2016')
        self.datacard_args = ' '.join(datacard_args)

        self.steering_fn = 'steering.sh'
        self.isample_fn = 'isample.txt'
        self.firstjob_fn = 'firstjob.txt'
        self.tmp_fns = [self.steering_fn, self.isample_fn, self.firstjob_fn]
        self.input_files = ['signal_efficiency.py', 'datacard.py', 'limitsinput.root'] + self.tmp_fns
        self.output_files = ['output.txz']

        self.batch_name = 'combine_output' + self.ex
        self.work_area = crab_dirs_root(self.batch_name)
        if os.path.isdir(self.work_area):
            raise IOError('%s exists' % self.work_area)
        os.makedirs(self.work_area)
        self.gitstatus_dir = os.path.join(self.work_area, 'gitstatus_%s' % int(time()*1e6))
        save_git_status(self.gitstatus_dir)
        print 'work area:', self.work_area

    def batch_dir(self, samples):
        isamples = [-s.isample for s in samples]
        return 'signals_-%05i_-%05i' % (min(isamples), max(isamples))

    def _writeit(self, fn, l):
        open(fn, 'wt').write('\n'.join(l) + '\n')

    def steering(self, job_env):
        ib = lambda n,x: '%s=%i' % (n,int(bool(x)))
        steering = [
            'JOBENV=%s' % job_env.lower(),
            ib('TESTONLY', self.submit_test),
            'DATACARDARGS="%s"' % self.datacard_args,
            ib('SAVETOYS', self.save_toys),
            ib('EXPECTED', not self.no_expected),
            ib('NOSYSTEMATICS', self.no_systematics),
            ib('GOODNESSOFFIT', self.goodness_of_fit),
            ib('SIGNIFICANCE', self.significance),
            ]
        self._writeit(self.steering_fn, steering)

    def samplemaps(self, job_env, samples):
        map = [str(sample.isample)    for sample in samples for j in xrange(self.njobs_per_point)]
        self._writeit(self.isample_fn, map)
        map = ['1' if j == 0 else '0' for sample in samples for j in xrange(self.njobs_per_point)]
        self._writeit(self.firstjob_fn, map)

    def submit(self, job_env, callback):
        limitsinput_f = ROOT.TFile('limitsinput.root')
        samples = limitsinput.sample_iterator(limitsinput_f,
                                              require_years=self.years,
                                              test=self.test_batch,
                                              slices_1d=self.slices_1d)

        allowed = []
        allowed_fn = 'submit_isamples.py'
        if os.path.isfile(allowed_fn):
            allowed = eval(open(allowed_fn).read())

        samples = [sample for sample in samples if allowed == [] or sample.isample in allowed]
        nsamples = len(samples)
        for i in xrange(0, nsamples, self.points_per_batch):
            batch = samples[i:i+self.points_per_batch]
            self.steering(job_env)
            self.samplemaps(job_env, batch)
            njobs = len(batch) * self.njobs_per_point
            callback(njobs, batch)

        if not self.testing:
            for x in self.tmp_fns:
                os.remove(x)

# zcat signal_*/combine_output* | sort | uniq | egrep -v '^median expected limit|^mean   expected limit|^Observed|^Limit: r|^Generate toy|^Done in|random number generator seed is|^   ..% expected band|^DATACARD:' | tee /tmp/duh
