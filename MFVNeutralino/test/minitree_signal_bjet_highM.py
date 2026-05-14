# Bjet-channel MiniTree submission for high-M signal samples only.
# Submits mfv_signal_highM + mfv_stopdbardbar_highM + mfv_stopbbarbbar_highM.
# Same prerequisites as minitree_signal_bjet.py:
#   NtupleCommon.py: use_btag_vetoLepHT_triggers = True
#   Year.h: correct year defined, then scram b

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
        'minitree_signal_bjet_highM.py requires use_btag_vetoLepHT_triggers = True in NtupleCommon.py'
    )

input_files(process, '/store/group/lpclonglived/gdecastr/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-100um_TuneCP5_13TeV-pythia8/Ntuple_Table28Validation_CorrectedBvetoLHTm_NoEF_2018/260216_200739/0000/ntuple_0.root')
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

    highm_dataset = dataset + '_highM'  # 'ntuple_tag001bvetolhtm_highM'

    samples = (getattr(Samples, 'mfv_signal_highM_samples_%s'      % yr) +
               getattr(Samples, 'mfv_stopdbardbar_highM_samples_%s' % yr) +
               getattr(Samples, 'mfv_stopbbarbbar_highM_samples_%s' % yr))
    samples = [s for s in samples if s.has_dataset(highm_dataset)]
    print('Submitting %d high-M bjet-channel samples for year %s' % (len(samples), yr))

    pset_modifier = chain_modifiers(
        is_mc_modifier,
        per_sample_pileup_weights_modifier(),
        ttH_duplicate_check_modifier,
    )

    set_splitting(samples, highm_dataset, 'minitree', data_json=json_path('ana_run2_displacement_trigger.json'))

    cs = CondorSubmitter(
        'MiniTree' + version + '_bjet',
        ex=year,
        dataset=highm_dataset,
        pset_modifier=pset_modifier,
    )
    cs.submit_all(samples)
