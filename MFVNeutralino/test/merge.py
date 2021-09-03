from DVCode.Tools.Merge_cfg import *

process.out.maxSize = cms.untracked.int32(2**19) # in kB, ~537 MB


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from DVCode.Tools.MetaSubmitter import *

    from DVCode.MFVNeutralino.NtupleCommon import ntuple_version_use as version, dataset
    batch_name = 'Ntuple%s_sigs_merge' % version
    publish_name = 'Ntuple%s_%s' % (version, year)

    samples = pick_samples(dataset, all_signal='only')

    for sample in samples:
        sample.set_curr_dataset(dataset)
        sample.split_by = 'files'
        sample.files_per = -1000000 # hope we never have more than 1M files

    from DVCode.Tools.CondorSubmitter import CondorSubmitter
    cs = CondorSubmitter(batch_name,
                         ex = year,
                         dataset = dataset,
                         publish_name = publish_name,
                         skip_output_files = ['merge.root'], # don't autodetect it
                         stageout_files = ['merge*.root'], # let the wrapper script glob merge.root, merge001.root, ...
                         )
    cs.submit_all(samples)

# for now, can publish output with mpublish --partial --no-coderep
