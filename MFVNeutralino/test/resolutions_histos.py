import os, sys
from JMTucker.Tools.BasicAnalyzer_cfg import cms, process, add_analyzer
from JMTucker.Tools.CMSSWTools import silence_messages

#process.MessageLogger.cerr.FwkReport.reportEvery = 1
process.maxEvents.input = 100
#process.source.fileNames = ['file:pat.root']
#process.source.secondaryFileNames = cms.untracked.vstring('/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_1_1_X2h.root')
process.source.fileNames = ['/store/user/jchu/mfv_neutralino_tau1000um_M0400/jtuple_v7/5d4c2a74c85834550d3f9609274e8548/pat_1_1_hdB.root']
process.source.secondaryFileNames = cms.untracked.vstring('/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_891_1_sZ9.root','/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_948_2_lgB.root')
#process.source.fileNames = ['/store/user/jchu/QCD_HT-1000ToInf_TuneZ2star_8TeV-madgraph-pythia6/jtuple_v7/fe6d9f80f9c0fe06cc80b089617fa99d/pat_1_1_NOT.root']
#process.source.secondaryFileNames = cms.untracked.vstring('/store/mc/Summer12_DR53X/QCD_HT-1000ToInf_TuneZ2star_8TeV-madgraph-pythia6/AODSIM/PU_S10_START53_V7A-v1/00000/0038E6D2-860D-E211-9211-00266CFACC38.root','/store/mc/Summer12_DR53X/QCD_HT-1000ToInf_TuneZ2star_8TeV-madgraph-pythia6/AODSIM/PU_S10_START53_V7A-v1/00000/D4C0816B-870D-E211-B094-00266CF258D8.root','/store/mc/Summer12_DR53X/QCD_HT-1000ToInf_TuneZ2star_8TeV-madgraph-pythia6/AODSIM/PU_S10_START53_V7A-v1/00000/A2CEDDF1-870D-E211-A98D-00266CF258D8.root','/store/mc/Summer12_DR53X/QCD_HT-1000ToInf_TuneZ2star_8TeV-madgraph-pythia6/AODSIM/PU_S10_START53_V7A-v1/00000/9E8E388F-970D-E211-8D78-848F69FD298E.root')
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
    #('combinedSecondaryVertexBJetTags',               (0.244, 0.679, 0.898)),
    ('jetProbabilityBJetTags',                        (0.275, 0.545, 0.790)),
    #('jetBProbabilityBJetTags',                       (1.33, 2.55, 3.74)),
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

for x in ['', 'WithTrigger', 'WithCuts', 'WithTriggerWithCuts', 'WTWCNB', 'WTWCNL', 'WTWCNBNL']:
    setattr(process, 'genHistos' + x, process.mfvGenHistos.clone())
    setattr(process, 'histos'    + x, histogrammer())

########################################################################

process.analysisCuts = cms.EDFilter('MFVAnalysisCuts',
                                    jet_src = cms.InputTag('mfvSelectedJets'),
                                    min_jet_pt = cms.double(20),
                                    min_4th_jet_pt = cms.double(60),
                                    min_5th_jet_pt = cms.double(0),
                                    min_6th_jet_pt = cms.double(0),
                                    min_njets = cms.int32(4),
                                    max_njets = cms.int32(100000),
                                    min_nbtags = cms.int32(0),
                                    min_sum_ht = cms.double(0),
                                    b_discriminator_name = cms.string('jetProbabilityBJetTags'),
                                    bdisc_min = cms.double(0.545),
                                    muon_src = cms.InputTag('selectedPatMuonsPF'), 
                                    electron_src = cms.InputTag('selectedPatElectronsPF'),
                                    min_nleptons = cms.int32(0),
                                    vertex_src = cms.InputTag('mfvSelectedVerticesTight'),
                                    min_nvertex = cms.int32(2),
                                    min_ntracks01 = cms.int32(15),
                                    min_maxtrackpt01 = cms.int32(15),
                                    )

process.load('JMTucker.MFVNeutralino.Vertexer_cff')
process.mfvVertexSequence.remove(process.mfvVertices)

process.p0 = cms.Path(process.mfvVertexSequence *                                                process.genHistos                    * process.histos)
process.p1 = cms.Path(process.mfvVertexSequence * process.triggerFilter *                        process.genHistosWithTrigger         * process.histosWithTrigger)
process.p2 = cms.Path(process.mfvVertexSequence *                         process.analysisCuts * process.genHistosWithCuts            * process.histosWithCuts)
process.p3 = cms.Path(process.mfvVertexSequence * process.triggerFilter * process.analysisCuts * process.genHistosWithTriggerWithCuts * process.histosWithTriggerWithCuts)

process.cutsnb = process.analysisCuts.clone(min_nbtags = 3)
process.cutsnl = process.analysisCuts.clone(min_nleptons = 1)
process.cutsnbnl = process.analysisCuts.clone(min_nbtags = 3, min_nleptons = 1)

process.p4 = cms.Path(process.mfvVertexSequence * process.triggerFilter * process.cutsnb   * process.histosWTWCNB)
process.p5 = cms.Path(process.mfvVertexSequence * process.triggerFilter * process.cutsnl   * process.histosWTWCNL)
process.p6 = cms.Path(process.mfvVertexSequence * process.triggerFilter * process.cutsnbnl * process.histosWTWCNBNL)

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

def de_mfv():
    if hasattr(process, 'mfvGenParticleFilter'):
        process.mfvGenParticleFilter.cut_invalid = False
    if hasattr(process, 'mfvGenVertices'):
        process.mfvGenVertices.is_mfv = False

def sample_ttbar():
    de_mfv()
    if hasattr(process, 'mfvGenVertices'):
        process.mfvGenVertices.is_ttbar = True

if 'ttbar' in sys.argv:
    sample_ttbar()
elif 'de_mfv' in sys.argv:
    de_mfv()

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

        if 'ttbar' in sample.name:
            to_add.append('sample_ttbar()')
        elif 'mfv' not in sample.name:
            to_add.append('de_mfv()')

        return to_add

    cs = CRABSubmitter('ResolutionsHistos',
                       total_number_of_events = -1,
                       events_per_job = 10000,
                       use_ana_dataset = True,
                       CMSSW_use_parent = 1,
                       pset_modifier = pset_adder
                       )
    from JMTucker.Tools.Samples import singletop_s, singletop_s_tbar, singletop_t, singletop_t_tbar, singletop_tW, singletop_tW_tbar, ww, wz, zz
    singletop_s.ana_dataset_override = '/T_s-channel_TuneZ2star_8TeV-powheg-tauola/jchu-jtuple_v7-e4d108e5d014df5f9335feb5272936d6/USER'
    singletop_s_tbar.ana_dataset_override = '/Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola/jchu-jtuple_v7-e4d108e5d014df5f9335feb5272936d6/USER'
    singletop_t.ana_dataset_override = '/T_t-channel_TuneZ2star_8TeV-powheg-tauola/jchu-jtuple_v7-e4d108e5d014df5f9335feb5272936d6/USER'
    singletop_t_tbar.ana_dataset_override = '/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola/jchu-jtuple_v7-e4d108e5d014df5f9335feb5272936d6/USER'
    singletop_tW.ana_dataset_override = '/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/jchu-jtuple_v7-e4d108e5d014df5f9335feb5272936d6/USER'
    singletop_tW_tbar.ana_dataset_override = '/Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/jchu-jtuple_v7-e4d108e5d014df5f9335feb5272936d6/USER'
    ww.ana_dataset_override = '/WW_TuneZ2star_8TeV_pythia6_tauola/jchu-jtuple_v7-e4d108e5d014df5f9335feb5272936d6/USER'
    wz.ana_dataset_override = '/WZ_TuneZ2star_8TeV_pythia6_tauola/jchu-jtuple_v7-e4d108e5d014df5f9335feb5272936d6/USER'
    zz.ana_dataset_override = '/ZZ_TuneZ2star_8TeV_pythia6_tauola/jchu-jtuple_v7-e4d108e5d014df5f9335feb5272936d6/USER'

    samples = mfv_signal_samples + background_samples + [singletop_s, singletop_s_tbar, singletop_t, singletop_t_tbar, singletop_tW, singletop_tW_tbar, ww, wz, zz]
    cs.submit_all(samples)
