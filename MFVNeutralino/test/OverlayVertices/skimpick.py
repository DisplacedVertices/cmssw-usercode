import sys, os, gzip
from JMTucker.Tools.CMSSWTools import *

process = basic_process('SkimPick')
#want_summary(process)
#process.maxEvents.input = 100
report_every(process, 1000000)

process.load('JMTucker.MFVNeutralino.SkimmedTracks_cfi')
process.mfvSkimmedTracks.apply_sigmadxybs = True
process.p = cms.Path(process.mfvSkimmedTracks)

output_file(process, 'skimpick.root', [
        'drop *',
        'keep recoBeamSpot_offlineBeamSpot__*',
        'keep recoTracks_mfvSkimmedTracks__*',
        ])


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.MFVNeutralino.Year import year
    import JMTucker.Tools.Samples as Samples 
    if year == 2015:
        samples = Samples.data_samples_2015 + Samples.ttbar_samples_2015 + Samples.qcd_samples_2015 + Samples.qcd_samples_ext_2015
    elif year == 2016:
        samples = Samples.data_samples + Samples.ttbar_samples + Samples.qcd_samples + Samples.qcd_samples_ext

    for sample in samples:
        sample.files_per = 50
        sample.split_by = 'files'
        sample.json = 'json.%s' % sample.name

    def vetolist_fn(sample):
        fn = 'vetolist.%s.gz' % sample.name
        assert os.path.isfile(fn)
        return fn

    def pset_modifier(sample):
        l = gzip.GzipFile(vetolist_fn(sample)).read().replace('\n', ' ')
        r = ', run=1' if sample.is_mc else ''
        to_add = ['set_events_to_process(process, [%s]%s)' % (l, r)]
        return to_add, []

    from JMTucker.Tools.MetaSubmitter import *
    batch_name = 'Pick1VtxV14'
    ms = MetaSubmitter(batch_name)
    ms.common.ex = year
    ms.common.pset_modifier = pset_modifier
    ms.common.publish_name = batch_name + '_' + str(year)
    ms.crab.job_control_from_sample = True
    ms.condor.stageout_files = 'all'
    ms.submit(samples)
