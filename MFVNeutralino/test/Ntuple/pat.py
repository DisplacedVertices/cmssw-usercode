#!/usr/bin/env python

from JMTucker.Tools.general import bool_from_argv
from JMTucker.Tools.MiniAOD_cfg import cms, pat_tuple_process, report_every
from JMTucker.Tools.CMSSWTools import file_event_from_argv

is_mc = not bool_from_argv('is_data')
keep_all = bool_from_argv('keep_all')
trig_filter = not keep_all
# JMTBAD different globaltags?

def customize_before_unscheduled(process):
    process.load('JMTucker.Tools.MCStatProducer_cff')

    process.out.outputCommands = output_commands = [
            'drop *',
            'keep *_mcStat_*_*',
            'keep edmTriggerResults_TriggerResults__HLT',
            'keep edmTriggerResults_TriggerResults__PAT',
            'keep *_addPileupInfo_*_*',
            'keep *_generator_*_*',
            'keep *_genParticles_*_*',
            'keep *_ak4GenJets*_*_*',
            'keep *_generalTracks_*_*',
            'keep *_offlineBeamSpot_*_*',
            'keep *_goodOfflinePrimaryVertices_*_*',
            'keep *_selectedPatJets_*_*',
            'keep *_selectedPatMuons_*_*',
            'keep *_selectedPatElectrons_*_*',
            'keep patMETs_patMETsNoHF_*_*',
            'drop CaloTowers_selectedPatJets_caloTowers_*',
            'keep recoGsfElectronCores_*_*_*', # sigh
            # not sure how these three sneak past the drop *
            'drop patMETs_patPFMetPuppi__PAT',
            'drop patMETs_patCaloMet__PAT',
            'drop patMETs_patMETPuppi__PAT',
            ]

    if keep_all:
        def dedrop(l):
            return [x for x in l if not x.strip().startswith('drop')]
        if is_mc:
            process.out.outputCommands += \
                process.AODSIMEventContent.outputCommands + \
                dedrop(process.MINIAODSIMEventContent.outputCommands) + \
                dedrop(output_commands)
        else:
            process.out.outputCommands += \
                process.AODEventContent.outputCommands + \
                dedrop(process.MINIAODEventContent.outputCommands) + \
                dedrop(output_commands)

process = pat_tuple_process(customize_before_unscheduled, is_mc)

# If the embedding is on for these, then we can't match leptons by track to vertices.
process.patMuons.embedTrack = False
process.patElectrons.embedTrack = False

# Instead of keeping the original branches in the temp file.
process.patElectrons.embedSuperCluster = True
process.patJets.embedPFCandidates = True

if trig_filter:
    import JMTucker.MFVNeutralino.TriggerFilter
    JMTucker.MFVNeutralino.TriggerFilter.setup_trigger_filter(process)

#process.options.wantSummary = True
file_event_from_argv(process)
