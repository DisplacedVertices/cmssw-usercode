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

    files_per = {'JetHT2015C': 16, 'JetHT2015D': 55, 'JetHT2016B3': 37, 'JetHT2016C': 34, 'JetHT2016D': 31, 'JetHT2016E': 58, 'JetHT2016F': 56, 'JetHT2016G': 40, 'JetHT2016H2': 37, 'JetHT2016H3': 36, 'qcdht0500': 100, 'qcdht0500_2015': 100, 'qcdht0500ext': 100, 'qcdht0500ext_2015': 100, 'qcdht0700': 100, 'qcdht0700_2015': 100, 'qcdht0700ext': 100, 'qcdht0700ext_2015': 100, 'qcdht1000': 6, 'qcdht1000_2015': 6, 'qcdht1000ext': 5, 'qcdht1000ext_2015': 6, 'qcdht1500': 3, 'qcdht1500_2015': 3, 'qcdht1500ext': 3, 'qcdht1500ext_2015': 3, 'qcdht2000': 2, 'qcdht2000_2015': 3, 'qcdht2000ext': 2, 'qcdht2000ext_2015': 2, 'ttbar': 36, 'ttbar_2015': 26}
    for sample in samples:
        sample.split_by = 'files'
        sample.files_per = files_per[sample.name]
        sample.json = 'json.%s' % sample.name

    def eventlist_fn(sample):
        fn = 'eventlist.%s.gz' % sample.name
        assert os.path.isfile(fn)
        return fn

    def pset_modifier(sample):
        l = gzip.GzipFile(eventlist_fn(sample)).read().replace('\n', ' ')
        r = ', run=1' if sample.is_mc else ''
        to_add = ['set_events(process, [%s]%s)' % (l, r)]
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

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submitmerge' in sys.argv:
    from JMTucker.MFVNeutralino.Year import year
    import JMTucker.Tools.Samples as Samples 
    if year == 2015:
        samples = Samples.data_samples_2015 + Samples.ttbar_samples_2015 + Samples.qcd_samples_2015 + Samples.qcd_samples_ext_2015
    elif year == 2016:
        samples = Samples.data_samples + Samples.ttbar_samples + Samples.qcd_samples + Samples.qcd_samples_ext

    dataset = 'pick1vtxv14'
    for sample in samples:
        sample.datasets[dataset].files_per = 100000

    from JMTucker.Tools.CondorSubmitter import CondorSubmitter
    cs = CondorSubmitter('Pick1VtxV14_merge',
                         pset_template_fn = '$CMSSW_BASE/src/JMTucker/Tools/python/Merge_cfg.py',
                         ex = year,
                         dataset = dataset,
                         publish_name = 'pick1vtxv14_merge',
                         stageout_files = 'all'
                         )
    cs.submit_all(samples)


'''
# little zsh (bash?) for-loop to help figure out the job splitting
for x in eventlist.*.gz; do
z=${x/eventlist./}
sample=${z/.gz/}
nsel=$(zcat $x | wc -l)
nevt=$(samples nevents $sample main)
nfile=$(samples file $sample main 10000000 | grep root | wc -l)
filesper=$(python -c "from math import ceil; nevtarget=100; filesmax=100; print min(ceil(${nfile}*nevtarget/${nsel}),filesmax)")
njobs=$(( (nfile+filesper-1)/filesper ))
echo $sample $nsel $nevt $nfile $filesper $njobs
done
'''
