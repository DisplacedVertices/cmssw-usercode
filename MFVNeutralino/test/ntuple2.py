#!/usr/bin/env python

from JMTucker.Tools.CMSSWTools import *
from JMTucker.MFVNeutralino.Year import year

if year == 2015:
    raise NotImplementedError("won't bother to understand 2015 miniaod")

is_mc = True
H = False
repro = False
# JMTBAD implement these
#run_n_tk_seeds = False
#minitree_only = False
#prepare_vis = not run_n_tk_seeds and False
#keep_all = prepare_vis
#keep_gen = False
event_filter = True #not keep_all
version = 'v17m'
batch_name = 'Ntuple' + version.capitalize()
#if run_n_tk_seeds:
#    batch_name += '_NTkSeeds'

####

process = basic_process('Ntuple')
report_every(process, 1000000)
#want_summary(process)
registration_warnings(process)
geometry_etc(process, which_global_tag(is_mc, year, H=False, repro=False))
random_service(process, {'mfvVertices': 1222})
tfileservice(process, 'vertex_histos.root')
input_files(process, '/uscmst1b_scratch/lpc1/3DayLifetime/tucker/itch/A00610B3-00B7-E611-8546-A0000420FE80.root')
file_event_from_argv(process)
output_file(process, 'ntuple.root', [
        'drop *',
        'keep *_mcStat_*_*',
        'keep MFVVertexAuxs_mfvVerticesAux_*_*',
        'keep MFVEvent_mfvEvent__*',
        ])

process.load('CommonTools.ParticleFlow.goodOfflinePrimaryVertices_cfi')
process.load('PhysicsTools.PatAlgos.selectionLayer1.jetSelector_cfi')
process.load('PhysicsTools.PatAlgos.selectionLayer1.muonSelector_cfi')
process.load('PhysicsTools.PatAlgos.selectionLayer1.electronSelector_cfi')
process.load('JMTucker.Tools.MCStatProducer_cff')
process.load('JMTucker.Tools.PATTupleSelection_cfi')
process.load('JMTucker.MFVNeutralino.UnpackedCandidateTracks_cfi')
process.load('JMTucker.MFVNeutralino.Vertexer_cff')
process.load('JMTucker.MFVNeutralino.TriggerFloats_cff')
process.load('JMTucker.MFVNeutralino.EventProducer_cfi')

process.goodOfflinePrimaryVertices.src = 'offlineSlimmedPrimaryVertices'

process.selectedPatJets.src = 'slimmedJets'
process.selectedPatJets.cut = process.jtupleParams.jetCut

process.selectedPatMuons.src = 'slimmedMuons'
process.selectedPatMuons.cut = process.jtupleParams.muonCut

process.selectedPatElectrons.src = 'slimmedElectrons'
process.selectedPatElectrons.cut = process.jtupleParams.electronCut

process.mfvGenParticles.gen_particles_src = 'prunedGenParticles'
process.mfvGenParticles.last_flag_check = False

process.mfvVertices.track_src = 'mfvUnpackedCandidateTracks'

#process.mfvVerticesToJets.enable = False # have to figure out how to use daughters of slimmed jets and the map we make in UnpackedCandidateTracks
process.mfvVerticesToJets.input_is_miniaod = True
process.mfvVerticesAuxTmp.input_is_miniaod = True
process.mfvVerticesAuxPresel.input_is_miniaod = True

process.mfvEvent.gen_particles_src = 'prunedGenParticles' # no idea if this lets gen_flavor_code, gen_bquarks, gen_leptons work. I think for the latter you'd want the packed ones that have status 1 particles
process.mfvEvent.gen_jets_src = 'slimmedGenJets'
process.mfvEvent.pileup_info_src = 'slimmedAddPileupInfo'
process.mfvEvent.met_src = 'slimmedMETs'

process.p = cms.Path(process.goodOfflinePrimaryVertices *
                     process.selectedPatJets *
                     process.selectedPatMuons *
                     process.selectedPatElectrons *
                     process.mfvTriggerFloats *
                     process.mfvUnpackedCandidateTracks *
                     process.mfvVertexSequence *
                     process.mfvEvent)

if event_filter:
    import JMTucker.MFVNeutralino.EventFilter
    JMTucker.MFVNeutralino.EventFilter.setup_event_filter(process, path_name='p', event_filter=True, input_is_miniaod=True)


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.MetaSubmitter import *
    import JMTucker.Tools.Samples as Samples

    samples = [s for s in
               #Samples.data_samples +
               Samples.ttbar_samples + Samples.qcd_samples + Samples.qcd_samples_ext +
               Samples.mfv_signal_samples + Samples.mfv_ddbar_samples
               if s.has_dataset('miniaod')]

    set_splitting(samples, 'miniaod', 'ntuple')

#    if run_n_tk_seeds:
#        samples = [s for s in samples if not s.is_signal]

    modify = chain_modifiers(is_mc_modifier, H_modifier, repro_modifier)
    ms = MetaSubmitter(batch_name, dataset='miniaod')
    ms.common.ex = year
    ms.common.pset_modifier = modify
    ms.common.publish_name = batch_name + '_' + str(year)
    ms.crab.job_control_from_sample = True
    ms.condor.stageout_files = 'all'
    ms.submit(samples)
