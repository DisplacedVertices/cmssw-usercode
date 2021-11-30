import sys
from JMTucker.Tools.BasicAnalyzer_cfg import *
from JMTucker.MFVNeutralino.NtupleCommon import signal_alt_random_pars_modifier

settings = CMSSWSettings()
settings.is_mc = True
settings.is_miniaod = True
settings.cross = '' # 2017to2018' # 2017to2017p8'

this_rp_mode = 'None'

sample_files(process, 'qcdht1000_2017', 'miniaod')
#sample_files(process, 'ZH_HToSSTodddd_ZToll_tau010000um_M15_2017', 'miniaod')
geometry_etc(process, settings)
tfileservice(process, 'filtercheck.root')
cmssw_from_argv(process)

from JMTucker.MFVNeutralino.EventFilter import setup_event_filter
sef = lambda *a,**kwa: setup_event_filter(process, *a, input_is_miniaod=True, rp_mode = this_rp_mode, **kwa)
sef('pTrigger', mode = 'trigger jets only')
sef('pTriggerBjets', mode = 'trigger bjets only',name_ex = 'bjets')
sef('pTriggerDispDijet', mode = 'trigger displaced dijet only',name_ex = 'displaced_dijet')
sef('pTriggerOR', mode = 'trigger HT OR bjets OR displaced dijet', name_ex = 'HT_OR_bjets_OR_displaced_dijet')
sef('pJets',    mode = 'jets only novtx',   name_ex = 'NoVtx') # be sure to generate a different name for each subsequent use
sef('pNoJESUp', mode = 'jets only novtx',   name_ex = 'NoJESUp', event_filter_jes_mult = 0)
sef('pFull',    mode = 'jets only',         name_ex = 'Full') # uncomment to get efficiency of ntuple-level vertex filter

if len(process.mfvTriggerFilter.HLTPaths) > 1:
    for x in process.mfvTriggerFilter.HLTPaths:
        filt_name = ''.join(x.split('_')[1:-1])
        sef('p%s' % filt_name, name_ex=x)
        getattr(process, filt_name).HLTPaths = [x]

import JMTucker.Tools.SimpleTriggerEfficiency_cfi as SimpleTriggerEfficiency
SimpleTriggerEfficiency.setup_endpath(process)


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.MetaSubmitter import *
    from JMTucker.Tools import Samples

    if year == 2017:
        samples = Samples.ttbar_samples_2017 + Samples.qcd_samples_2017 + Samples.all_signal_samples_2017 + Samples.data_samples_2017
    elif year == 2018:
        samples = Samples.qcd_samples_2018 + Samples.data_samples_2018

    ms = MetaSubmitter('TrigFiltCheckV1_lept', dataset='miniaod')
    ms.common.pset_modifier = chain_modifiers(is_mc_modifier, era_modifier, npu_filter_modifier(settings.is_miniaod), per_sample_pileup_weights_modifier(cross=settings.cross), signal_alt_random_pars_modifier)
    ms.submit(samples)
