# Ntuple production for high-M bjet-channel signal samples.
# Submits mfv_signal_highM + mfv_stopdbardbar_highM + mfv_stopbbarbbar_highM for one year.
# Prerequisites:
#   NtupleCommon.py: use_btag_vetoLepHT_triggers = True
#   Year.h: correct year #define, then scram b inside el7

import FWCore.ParameterSet.Config as cms
from JMTucker.Tools.general import named_product
from JMTucker.MFVNeutralino.NtupleCommon import *
from JMTucker.Tools.Year import year

if not use_btag_vetoLepHT_triggers:
    raise RuntimeError('ntuple_highM.py requires use_btag_vetoLepHT_triggers = True in NtupleCommon.py')

settings = NtupleSettings()
settings.is_mc = True
settings.is_miniaod = True
settings.run_n_tk_seeds = False
settings.minitree_only = False
settings.prepare_vis = False
settings.keep_all = False
settings.keep_gen = False
settings.keep_tk = False
settings.event_filter = 'bjets OR displaced dijet veto leptons and HT'
settings.randpars_filter = False

process = ntuple_process(settings)
dataset = 'miniaod' if settings.is_miniaod else 'main'
input_files(process, '/uscms/home/joeyr/nobackup/13DF01B3-1BC9-0246-8C88-DF26E2F16793.root')
cmssw_from_argv(process)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.MetaSubmitter import *

    yr = str(year)

    samples = (getattr(Samples, 'mfv_signal_highM_samples_%s'       % yr) +
               getattr(Samples, 'mfv_stopdbardbar_highM_samples_%s'  % yr) +
               getattr(Samples, 'mfv_stopbbarbbar_highM_samples_%s'  % yr))
    samples = [s for s in samples if s.has_dataset(dataset)]
    print 'Submitting %d high-M bjet-channel ntuple samples for year %s' % (len(samples), yr)

    json_filename = 'ana_run2_displacement_trigger.json'
    set_splitting(samples, dataset, 'ntuple', data_json=json_path(json_filename))

    ms = MetaSubmitter(settings.batch_name() + '_highM', dataset=dataset)
    ms.common.pset_modifier = chain_modifiers(is_mc_modifier, era_modifier, npu_filter_modifier(settings.is_miniaod), signals_no_event_filter_modifier, ttH_duplicate_check_modifier)
    ms.crab.crab_cfg_Data_outLFNDirBase = '/store/group/lpcdisplacedvertices/gdecastr/'
    ms.condor.stageout_files = 'all'
    ms.condor.local_stage = True
    ms.condor.stageout_path = (
        'root://cmseos.fnal.gov//store/group/lpcdisplacedvertices/gdecastr'
        '/$(<cs_primaryds)/' + settings.batch_name() + '_highM_' + yr +
        '/$(<cs_timestamp)/$(printf "%04i" $(($job/1000)))'
    )
    ms.submit(samples)
