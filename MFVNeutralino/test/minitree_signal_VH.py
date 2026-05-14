# Dedicated MiniTree submission for lepton-channel VH signals.
#
# Prerequisites before running:
#   1. NtupleCommon.py must have:
#        use_Lepton_triggers = True
#        use_btag_vetoLepHT_triggers = False
#      (this is the current default, so no change should be needed)
#
#   2. Year.h must have the correct year defined, e.g.:
#        #define MFVNEUTRALINO_2018
#      Then rebuild: scram b -j8
#      Repeat for each year before re-submitting.
#
# To submit (after setting year and rebuilding):
#   python minitree_signal_VH.py submit
#
# Samples submitted: ZH + WH+ + WH- + ggZH_bbbb + ggZH_dddd
# Dataset:           ntuple_tag001lepm

from JMTucker.Tools.BasicAnalyzer_cfg import *

is_mc = True

from JMTucker.MFVNeutralino.NtupleCommon import (
    ntuple_version_use as version,
    dataset,
    use_btag_vetoLepHT_triggers,
    use_Lepton_triggers,
)

if not use_Lepton_triggers:
    raise RuntimeError(
        'minitree_signal_VH.py requires use_Lepton_triggers = True in NtupleCommon.py'
    )

# Use an ntuple from the lepton dataset as a local test file
input_files(process, '/store/group/lpclonglived/joeyr/ZH_HToSSTodddd_ZToLL_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/NtupleOnnormdzULV30Lepm_2018/0000/ntuple_1.root')
tfileservice(process, 'minitree.root')
cmssw_from_argv(process)

process.load('JMTucker.MFVNeutralino.MiniTree_cff')

if not is_mc:
    del process.pMiniTreeNtk4
    del process.pMiniTreeNtk3or4
    del process.pMiniTree


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.MetaSubmitter import *
    import JMTucker.Tools.Samples as Samples
    from JMTucker.Tools.Year import year

    yr = str(year)

    attr = 'all_lep_signal_samples_%s' % yr
    samples = getattr(Samples, attr)
    samples = [s for s in samples if s.has_dataset(dataset)]
    print('Submitting %d lep-channel samples for year %s' % (len(samples), yr))

    pset_modifier = chain_modifiers(
        is_mc_modifier,
        per_sample_pileup_weights_modifier(),
        ttH_duplicate_check_modifier,
    )

    set_splitting(samples, dataset, 'minitree', data_json=json_path('ana_run2.json'))

    cs = CondorSubmitter(
        'MiniTree' + version + '_VH',
        ex=year,
        dataset=dataset,
        pset_modifier=pset_modifier,
    )
    cs.submit_all(samples)
