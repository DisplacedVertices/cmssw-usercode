from JMTucker.Tools.CRAB3Submitter import CRABSubmitter
from JMTucker.Tools.Sample import anon_samples
import JMTucker.Tools.Samples as Samples 

version = 'v5'
batch_name = 'Ntuple' + version.upper()
#batch_name += '_ChangeMeIfNotDefault'

samples = Samples.ttbar_samples + Samples.qcd_samples + [Samples.mfv_neu_tau00100um_M0800, Samples.mfv_neu_tau00300um_M0800, Samples.mfv_neu_tau01000um_M0800, Samples.mfv_neu_tau10000um_M0800]

def modify(sample):
    to_add = []
    to_replace = []

    if sample.is_mc:
        if sample.is_fastsim:
            raise NotImplementedError('zzzzzzz')
    else:
        magic = 'is_mc = True'
        err = 'trying to submit on data, and tuple template does not contain the magic string "%s"' % magic
        to_replace.append((magic, 'is_mc = False', err))
        # JMTBAD different globaltags?

    return to_add, to_replace

cs = CRABSubmitter(batch_name,
                   pset_modifier = modify,
                   job_control_from_sample = True,
                   publish_name = batch_name.lower(),
                   )

#timing = { 'dyjetstollM10': 0.011203, 'dyjetstollM50': 0.019867, 'qcdbce020': 0.008660, 'qcdbce030': 0.007796, 'qcdbce080': 0.061260, 'qcdbce170': 0.328891, 'qcdbce250': 0.481813, 'qcdbce350': 0.519482, 'qcdem020': 0.010137, 'qcdem030': 0.01, 'qcdem080': 0.037925, 'qcdem170': 0.286123, 'qcdem250': 0.471398, 'qcdem350': 0.686303, 'qcdht0100': 0.008273, 'qcdht0250': 0.116181, 'qcdht0500': 0.738374, 'qcdht1000': 1.002745, 'qcdmu0020': 0.012301, 'qcdmu0030': 0.015762, 'qcdmu0050': 0.018178, 'qcdmu0080': 0.119300, 'qcdmu0120': 0.245562, 'qcdmu0170': 0.32, 'qcdmu0300': 0.419818, 'qcdmu0470': 0.584266, 'qcdmu0600': 0.455305, 'qcdmu0800': 0.879171, 'qcdmu1000': 1.075712, 'singletop_s': 0.093429, 'singletop_s_tbar': 0.146642, 'singletop_tW': 0.327386, 'singletop_tW_tbar': 0.184349, 'singletop_t': 0.092783, 'singletop_t_tbar': 0.060983, 'ttbarhadronic': 0.752852, 'ttbarsemilep': 0.419073, 'ttbardilep': 0.295437, 'ttgjets': 0.861987, 'ttwjets': 0.714156, 'ttzjets': 0.827464, 'wjetstolnu': 0.010842, 'ww': 0.046754, 'wz': 0.049839, 'zz': 0.059791, }
#for sample in Samples.all_mc_samples:
#    if timing.has_key(sample.name):
#        sample.events_per = int(3.5*3600/timing[sample.name])
#        sample.timed = True
#        nj = int(sample.nevents_orig / float(sample.events_per)) + 1
#        assert nj < 5000
#
#for s in Samples.mfv_signal_samples + Samples.mfv_signal_samples_systematics + Samples.exo12038_samples:
#    s.events_per = 2000
#    s.timed = True
#
#for sample in samples:
#    if sample.is_mc:
#        sample.total_events = -1
#        assert hasattr(sample, 'timed')
#    else:
#        sample.json = 'ana_all.json'

cs.submit_all(samples)
