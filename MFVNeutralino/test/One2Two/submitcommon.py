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

class _config(object):
    def __init__(self):
        self.testing = bool_from_argv('testing') # just exercising this script
        self.submit_test = bool_from_argv('submit_test') # submit the job but don't run combine
        self.njobs = 2 if bool_from_argv('2jobs') else 50
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
        self.input_files = ['signal_efficiency.py', 'datacard.py', 'limitsinput.root', self.steering_fn]
        self.to_rm = [self.steering_fn]

        self.output_files = ['combine_output.txtgz', 'observed.root']
        if not self.no_expected:
            self.output_files += ['expected.root']
        if self.no_systematics:
            output_files += ['observedS0.root']
            if not self.no_expected:
                self.output_files += ['expectedS0.root']
        if self.goodness_of_fit:
            output_files += ['gof_observed.root']
            if not self.no_expected:
                output_files += ['gof_expected.root']
            if self.no_systematics:
                output_files += ['gof_S0_observed.root']
                if not self.no_expected:
                    output_files += ['gof_S0_expected.root']
        if self.significance:
            output_files += ['signif_observed.root']
            if not self.no_expected:
                output_files += ['signif_expected.root']
            if self.no_systematics:
                output_files += ['signif_S0_observed.root']
                if not self.no_expected:
                    output_files += ['signif_S0_expected.root']

        self.batch_name = 'combine_output' + self.ex
        self.work_area = crab_dirs_root(self.batch_name)
        if os.path.isdir(self.work_area):
            raise IOError('%s exists' % self.work_area)
        os.makedirs(self.work_area)
        self.gitstatus_dir = os.path.join(self.work_area, 'gitstatus_%s' % int(time()*1e6))
        save_git_status(self.gitstatus_dir)
        print 'work area:', self.work_area

    def batch_dir(self, sample):
        return 'signal_%05i' % sample.isample

    def steering_sh(self, job_env, sample):
        ib = lambda n,x: '%s=%i' % (n,int(bool(x)))
        steering = [
            'JOBENV=%s' % job_env.lower(),
            ib('TESTONLY', self.submit_test),
            'ISAMPLE=%i' % sample.isample,
            'DATACARDARGS="%s"' % self.datacard_args,
            ib('SAVETOYS', self.save_toys),
            ib('EXPECTED', not self.no_expected),
            ib('NOSYSTEMATICS', self.no_systematics),
            ib('GOODNESSOFFIT', self.goodness_of_fit),
            ib('SIGNIFICANCE', self.significance),
            ]
        return '\n'.join(steering) + '\n'

limitsinput_f = ROOT.TFile('limitsinput.root')
submit_config = _config()

def submit(job_env, callback):
    samples = limitsinput.sample_iterator(limitsinput_f,
                                          require_years=submit_config.years,
                                          test=submit_config.test_batch,
                                          slices_1d=submit_config.slices_1d
                                          )

    allowed = []
    allowed_fn = 'submit_isamples.py'
    if os.path.isfile(allowed_fn):
        allowed = eval(open(allowed_fn).read())

    for sample in samples:
        if allowed and sample.isample not in allowed:
            continue
        steering = submit_config.steering_sh(job_env, sample)
        open(submit_config.steering_fn, 'wt').write(steering)
        callback(sample)

def submit_finish():
    if not submit_config.testing:
        for x in submit_config.to_rm:
            os.remove(x)

# zcat signal_*/combine_output* | sort | uniq | egrep -v '^median expected limit|^mean   expected limit|^Observed|^Limit: r|^Generate toy|^Done in|random number generator seed is|^   ..% expected band|^DATACARD:' | tee /tmp/duh
