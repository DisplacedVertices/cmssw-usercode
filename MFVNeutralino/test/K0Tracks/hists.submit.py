from JMTucker.Tools.MetaSubmitter import *

samples = pick_samples(dataset, ttbar=False, all_signal=False)
NtupleReader_submit('K0HistsV25mv1', 'nr_k0ntuplev25mv1', samples)
