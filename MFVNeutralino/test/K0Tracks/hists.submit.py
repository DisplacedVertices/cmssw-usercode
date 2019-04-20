from JMTucker.Tools import CondorSubmitter as CS, Samples

samples = Samples.qcd_samples_2017 + Samples.data_samples_2017 + Samples.qcd_samples_2018 + Samples.data_samples_2018
Samples.qcdht0700_2017.njobs = 1
Samples.qcdht0700_2018.njobs = 1

CS.NtupleReader_submit('K0HistsV23mv3_nsigdxy0_norhomin', 'root://cmseos.fnal.gov//store/user/tucker/hadded/K0NtupleV23mv3', samples)
