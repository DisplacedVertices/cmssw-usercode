import os, sys
from JMTucker.Tools.BasicAnalyzer_cfg import cms, process, add_analyzer
from JMTucker.Tools.CMSSWTools import silence_messages

#process.MessageLogger.cerr.FwkReport.reportEvery = 1
process.source.fileNames = ['file:pat.root']
process.source.secondaryFileNames = cms.untracked.vstring('/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_1_1_X2h.root')
process.TFileService.fileName = 'resolutions_histos.root'
silence_messages(process, 'TwoTrackMinimumDistance')

########################################################################

process.load('JMTucker.MFVNeutralino.GenParticleFilter_cfi')
process.mfvGenParticleFilter.required_num_leptonic = 1
process.mfvGenParticleFilter.min_lepton_pt = 30
process.mfvGenParticleFilter.max_lepton_eta = 2.1

########################################################################

from HLTrigger.HLTfilters.hltHighLevel_cfi import hltHighLevel
process.goodDataFilter = hltHighLevel.clone()
process.goodDataFilter.TriggerResultsTag = cms.InputTag('TriggerResults', '', 'PAT')
process.goodDataFilter.HLTPaths = ['eventCleaningAll'] # can set to just 'goodOfflinePrimaryVertices', for example
process.goodDataFilter.andOr = False # = AND

process.triggerFilter = hltHighLevel.clone()
process.triggerFilter.HLTPaths = ['HLT_QuadJet50_v*']
process.triggerFilter.andOr = True # = OR

########################################################################

process.load('Configuration.Geometry.GeometryIdeal_cff')
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.GlobalTag.globaltag = 'START53_V21::All'
process.load('TrackingTools.TransientTrack.TransientTrackBuilder_cfi')

########################################################################

import JMTucker.Tools.PATTupleSelection_cfi
selection = JMTucker.Tools.PATTupleSelection_cfi.jtupleParams

bdiscs = [
    ('combinedSecondaryVertexBJetTags',               (0.244, 0.679, 0.898)),
    ('jetProbabilityBJetTags',                        (0.275, 0.545, 0.790)),
    ('jetBProbabilityBJetTags',                       (1.33, 2.55, 3.74)),
    ('simpleSecondaryVertexHighEffBJetTags',          (1.74, 3.05)),
    ('simpleSecondaryVertexHighPurBJetTags',          (2., 2.)),
    ('trackCountingHighEffBJetTags',                  (1.7, 3.3, 10.2)),
    ('trackCountingHighPurBJetTags',                  (1.19, 1.93, 3.41)),
    ('combinedMVABJetTags',                           (0.5, 0.5)),
    ('combinedSecondaryVertexMVABJetTags',            (0.5, 0.5)),
    ('simpleInclusiveSecondaryVertexHighEffBJetTags', (0.5, 0.5)),
    ('simpleInclusiveSecondaryVertexHighPurBJetTags', (0.5, 0.5)),
    ('combinedInclusiveSecondaryVertexBJetTags',      (0.5, 0.5)),
    ('doubleSecondaryVertexHighEffBJetTags',          (0.5, 0.5)),
    ]

def histogrammer():
    return cms.EDAnalyzer('MFVResolutionsHistogrammer',
                          reweight_pileup = cms.bool(True),
                          force_weight = cms.double(-1),
                          vertex_src = cms.InputTag('goodOfflinePrimaryVertices'),
                          met_src = cms.InputTag('patMETsPF'),
                          jet_src = cms.InputTag('selectedPatJetsPF'),
                          b_discriminators = cms.vstring(*[name for name, discs in bdiscs]),
                          b_discriminator_mins = cms.vdouble(*[discs[1] for name, discs in bdiscs]),
                          muon_src = cms.InputTag('selectedPatMuonsPF'),
                          max_muon_dxy = cms.double(1e99),
                          max_muon_dz = cms.double(1e99),
                          muon_semilep_cut = selection.semilepMuonCut,
                          muon_dilep_cut = selection.dilepMuonCut,
                          electron_src = cms.InputTag('selectedPatElectronsPF'),
                          max_semilep_electron_dxy = cms.double(1e99),
                          max_dilep_electron_dxy = cms.double(1e99),
                          electron_semilep_cut = selection.semilepElectronCut,
                          electron_dilep_cut = selection.dilepElectronCut,
                          print_info = cms.bool(False),
                          )

process.load('JMTucker.MFVNeutralino.GenHistos_cff')

for x in ['', 'WithTrigger', 'WithCuts', 'WithTriggerWithCuts']:
    setattr(process, 'genHistos' + x, process.mfvGenHistos.clone())
    setattr(process, 'histos'    + x, histogrammer())

########################################################################

process.analysisCuts = cms.EDFilter('MFVAnalysisCuts',
                                    jet_src = cms.InputTag('selectedPatJetsPF'),
                                    min_jet_pt = cms.double(30),
                                    min_4th_jet_pt = cms.double(60),
                                    min_5th_jet_pt = cms.double(0),
                                    min_6th_jet_pt = cms.double(0),
                                    min_njets = cms.int32(5),
                                    min_nbtags = cms.int32(3),
                                    min_sum_ht = cms.double(400),
                                    b_discriminator_name = cms.string('jetProbabilityBJetTags'),
                                    bdisc_min = cms.double(0.545),
                                    muon_src = cms.InputTag('selectedPatMuonsPF'), 
                                    electron_src = cms.InputTag('selectedPatElectronsPF'),
                                    )

process.p0 = cms.Path(                                               process.genHistos                    * process.histos)
process.p1 = cms.Path(process.triggerFilter *                        process.genHistosWithTrigger         * process.histosWithTrigger)
process.p2 = cms.Path(                        process.analysisCuts * process.genHistosWithCuts            * process.histosWithCuts)
process.p3 = cms.Path(process.triggerFilter * process.analysisCuts * process.genHistosWithTriggerWithCuts * process.histosWithTriggerWithCuts)

if 'debug' in sys.argv:
    from JMTucker.Tools.CMSSWTools import file_event_from_argv
    file_event_from_argv(process)
    process.MessageLogger.cerr.FwkReport.reportEvery = 1
    process.histos.print_info = True
    process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
    process.printList = cms.EDAnalyzer('ParticleListDrawer',
                                       maxEventsToPrint = cms.untracked.int32(100),
                                       src = cms.InputTag('genParticles'),
                                       printOnlyHardInteraction = cms.untracked.bool(False),
                                       useMessageLogger = cms.untracked.bool(False)
                                       )
    process.p0.insert(0, process.printList)

def remove_genhistos():
    for path_name in process.paths:
        path = getattr(process, path_name)
        for mod_name in path.moduleNames():
            if mod_name.startswith('genHistos'):
                path.remove(getattr(process, mod_name))

def run_on_data(dataset=None, datasets=None):
    if 'debug' in sys.argv:
        process.p.remove(process.printList)

    add_analyzer('EventIdRecorder')

    if dataset and datasets:
        veto_filter = cms.EDFilter('VetoOtherDatasets', datasets_to_veto = cms.vstring(*[d for d in datasets if d != dataset]))
        setattr(process, 'dataset%sOnly' % dataset, veto_filter)
        for path_name, path in process.paths_().iteritems():
            path.insert(0, veto_filter)

#run_on_data('MultiJet', ['MultiJet', 'JetHT', 'MuHad', 'ElectronHad'])

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    if 'debug' in sys.argv:
        raise RuntimeError('refusing to submit jobs in debug (verbose print out) mode')

    from JMTucker.Tools.Samples import background_samples, mfv_signal_samples, data_samples
    from JMTucker.Tools.CRABSubmitter import CRABSubmitter

    def pset_adder(sample):
        to_add = []
        if not sample.is_mc:
            to_add.append('run_on_data()')
        if 'mfv' not in sample.name:
            to_add.append('remove_genhistos()')
        return to_add

    cs = CRABSubmitter('ResolutionsHistos',
                       total_number_of_events = -1,
                       events_per_job = 10000,
                       use_ana_dataset = True,
                       CMSSW_use_parent = 1,
                       pset_modifier = pset_adder
                       )
    cs.submit_all(samples)
