import sys, os
from pprint import pprint
from time import time
from JMTucker.Tools.CRAB3Tools import crab_dirs_root
from JMTucker.Tools.general import save_git_status
from JMTucker.Tools import colors
import ROOT; ROOT.gROOT.SetBatch()
import limitsinput

class _config(object):
    def __init__(self):
        self.testing = 'testing' in sys.argv # just exercising this script
        self.njobs = 2 if '2jobs' in sys.argv else 50
        self.test_batch = 'test_batch' in sys.argv # passed to limitsinput.sample_iterator
        self.slices_1d = 'slices_1d' in sys.argv
        self.save_toys = 'save_toys' in sys.argv
        self.include_2016 = 'include_2016' in sys.argv
        self.expected = 'no_expected' not in sys.argv
        self.no_systematics = 'no_systematics' in sys.argv
        self.goodness_of_fit = 'goodness_of_fit' in sys.argv

        self.years = ('2016','2017','2018') if self.include_2016 else ('2017','2018')

        self.bkg_correlation = [x for x in ['bkg_fully_correlated', 'bkg_yearwise_correlated', 'bkg_binwise_correlated', 'bkg_mixed_correlated', 'bkg_fully_correlated'] if x in sys.argv]
        assert len(self.bkg_correlation) <= 1

        datacard_args = self.bkg_correlation
        if self.include_2016:
            datacard_args.append('include_2016')
        self.datacard_args = ' '.join(datacard_args)

    def batch_dir(self, sample):
        return 'signal_%05i' % sample.isample

    def steering_sh(self, sample, xrdcp_combine_tarball):
        ib = lambda n,x: '%s=%i' % (n,int(bool(x)))
        steering = [
            'ISAMPLE=%i' % sample.isample,
            'DATACARDARGS="%s"' % self.datacard_args,
            ib('XRDCPCOMBINETARBALL', xrdcp_combine_tarball),
            ib('SAVETOYS', self.save_toys),
            ib('EXPECTED', self.expected),
            ib('NOSYSTEMATICS', self.no_systematics),
            ib('GOODNESSOFFIT', self.goodness_of_fit),
            ]
        return '\n'.join(steering) + '\n'

limitsinput_f = ROOT.TFile('limitsinput.root')
submit_config = _config()

def submit(callback):
    samples = limitsinput.sample_iterator(limitsinput_f,
                                          require_years=submit_config.years,
                                          test=submit_config.test_batch,
                                          slices_1d=submit_config.slices_1d
                                          )
    
    names = set(s.name for s in samples)
    allowed = [arg for arg in sys.argv if arg in names]

    for sample in samples:
        if allowed and sample.name not in allowed:
            continue
        callback(sample)
