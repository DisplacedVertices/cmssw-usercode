from JMTucker.Tools import CondorSubmitter as CS, Samples

samples = Samples.qcd_samples_2017 + Samples.data_samples_2017 + Samples.qcd_samples_2018 + Samples.data_samples_2018

CS.NtupleReader_submit('TrackingTreerHistsV23mv3', 'nr_trackingtreerv23mv3', samples)
