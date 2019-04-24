from JMTucker.Tools import CondorSubmitter as CS, Samples

samples = Samples.qcd_samples_2017 + Samples.data_samples_2017 + Samples.qcd_samples_2018 + Samples.data_samples_2018

CS.NtupleReader_submit('K0HistsV23mv4_nsigdxy1p5_rhomin0p2', 'nr_k0ntuplev23mv4', samples, split_default=1)
