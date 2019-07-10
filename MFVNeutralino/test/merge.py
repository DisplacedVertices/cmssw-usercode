from JMTucker.Tools.Merge_cfg import *

process.out.maxSize = cms.untracked.int32(2**19) # in kB, ~537 MB


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.MetaSubmitter import *

    dataset = 'ntuplev25m'
    batch_name = 'NtupleV25m_sigs_merge'
    publish_name = 'NtupleV25m_%s' % year

    samples = pick_samples(dataset, all_signal='only')

    for sample in samples:
        sample.set_curr_dataset(dataset)
        sample.split_by = 'files'
        sample.files_per = -1000000 # hope we never have more than 1M files

    from JMTucker.Tools.CondorSubmitter import CondorSubmitter
    cs = CondorSubmitter(batch_name,
                         ex = year,
                         dataset = dataset,
                         publish_name = publish_name,
                         skip_output_files = ['merge.root'], # don't autodetect it
                         stageout_files = ['merge*.root'], # let the wrapper script glob merge.root, merge001.root, ...
                         )
    cs.submit_all(samples)

# for now, can publish output with mpublish --partial --no-coderep
