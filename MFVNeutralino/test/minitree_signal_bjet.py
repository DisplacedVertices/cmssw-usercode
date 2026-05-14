# Dedicated MiniTree submission for displaced-trigger bjet-channel signals.
#
# Prerequisites before running:
#   1. NtupleCommon.py must have:
#        use_btag_vetoLepHT_triggers = True
#        use_Lepton_triggers = False
#      Edit NtupleCommon.py and rebuild: scram b -j8
#      Remember to restore NtupleCommon.py to use_Lepton_triggers = True afterwards.
#
#   2. Year.h must have the correct year defined, e.g.:
#        #define MFVNEUTRALINO_2018
#      Then rebuild: scram b -j8
#      Repeat for each year before re-submitting.
#
# To submit (after setting year and rebuilding):
#   python minitree_signal_bjet.py submit
#
# Samples submitted: mfv_neu (neutralino/gluino) + mfv_stopdbardbar + ggH
# Dataset:           ntuple_tag001bvetolhtm

from JMTucker.Tools.BasicAnalyzer_cfg import *

is_mc = True

from JMTucker.MFVNeutralino.NtupleCommon import (
    ntuple_version_use as version,
    dataset,
    use_btag_vetoLepHT_triggers,
    use_Lepton_triggers,
)

if not use_btag_vetoLepHT_triggers:
    raise RuntimeError(
        'minitree_signal_bjet.py requires use_btag_vetoLepHT_triggers = True in NtupleCommon.py'
    )

# Use an ntuple from the bjet dataset as a local test file
input_files(process, '/store/group/lpclonglived/joeyr/mfv_neu_tau01000um_M0400_2018/NtupleOnnormdzULV30BvetoLHTm_2018/0000/ntuple_1.root')
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

    attr = 'all_bjet_signal_samples_%s' % yr
    samples = getattr(Samples, attr)
    samples = [s for s in samples if s.has_dataset(dataset)]
    print('Submitting %d bjet-channel samples for year %s' % (len(samples), yr))

    pset_modifier = chain_modifiers(
        is_mc_modifier,
        per_sample_pileup_weights_modifier(),
        ttH_duplicate_check_modifier,
    )

    set_splitting(samples, dataset, 'minitree', data_json=json_path('ana_run2_displacement_trigger.json'))

    cs = CondorSubmitter(
        'MiniTree' + version + '_bjet',
        ex=year,
        dataset=dataset,
        pset_modifier=pset_modifier,
    )
    cs.submit_all(samples)
