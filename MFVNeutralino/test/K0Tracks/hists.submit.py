from JMTucker.Tools import CondorSubmitter as CS, Samples

samples = Samples.qcd_samples_2017 + Samples.data_samples_2017 + Samples.qcd_samples_2018 + Samples.data_samples_2018

if False:
    for sample in samples:
        sample.set_curr_dataset('nr_k0ntuplev23mv4')
        sample.filenames = sample.filenames[::10]

CS.NtupleReader_submit('K0HistsV23mv4_nsigdxy0p0_rhomin0p268_ctaumin0p0268_costh2min0p99975', 'nr_k0ntuplev23mv4', samples, split_default=1)
