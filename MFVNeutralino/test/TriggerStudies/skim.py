import sys
from JMTucker.Tools.CMSSWTools import global_tag
from JMTucker.Tools.Merge_cfg import cms, process
from JMTucker.Tools.MiniAOD_cfg import which_global_tag

H = False
repro = False

global_tag(process, which_global_tag(False, 2016, H, repro))
process.options.wantSummary = True
process.source.fileNames = ['/store/data/Run2016H/SingleMuon/MINIAOD/PromptReco-v2/000/283/283/00000/780D7FAA-FF95-E611-AC56-02163E011B49.root' if True else '/store/data/Run2016G/SingleMuon/MINIAOD/23Sep2016-v1/90000/94F15529-0694-E611-9B67-848F69FD4FC1.root']

process.setName_('TrigSkim')
process.MessageLogger.cerr.FwkReport.reportEvery = 1000000
process.out.fileName = 'trigskim.root'
process.out.SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring())

from Configuration.EventContent.EventContent_cff import MINIAODSIMEventContent as miniaod
process.out.outputCommands = miniaod.outputCommands.value() + process.out.outputCommands.value()[1:]

process.load('JMTucker.MFVNeutralino.TriggerFloats_cff')
process.load('JMTucker.MFVNeutralino.TriggerFloatsFilter_cfi')
process.mfvTriggerFloats.jets_src = 'slimmedJets'

def a(name, **kwargs):
    obj = process.mfvTriggerFloatsFilter.clone(**kwargs)
    setattr(process, name, obj)

    pname = 'p' + name
    path = cms.Path(process.mfvTriggerFloats * obj)
    setattr(process, pname, path)
    process.out.SelectEvents.SelectEvents.append(pname)

a('myhtt',     ht_cut = 1000, myhtt_m_l1htt_cut     = 0.4)
a('myhttwbug', ht_cut = 1000, myhttwbug_m_l1htt_cut = 0.4)


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    import JMTucker.Tools.Samples as Samples
    samples = [s for s in Samples.auxiliary_data_samples if s.name.startswith('SingleMuon')]

    for sample in samples:
        sample.json = '../jsons/ana_2015p6.json'

    from JMTucker.Tools.CRAB3Submitter import CRABSubmitter
    from JMTucker.Tools.MetaSubmitter import *
    batch_name = 'TrigSkimV1'
    cs = CRABSubmitter(batch_name,
                       pset_modifier = chain_modifiers(H_modifier, repro_modifier),
                       splitting = 'FileBased',
                       units_per_job = 10,
                       total_units = -1,
                       dataset = 'miniaod',
                       publish_name = batch_name,
                       )
    cs.submit_all(samples)
