import os, sys
from JMTucker.Tools.BasicAnalyzer_cfg import cms, process
from JMTucker.Tools.CMSSWTools import silence_messages

from JMTucker.MFVNeutralino.SimFiles import load as load_files
load_files(process, 'tau1000um_M0400', 0)

process.TFileService.fileName = 'prepare_vis.root'
process.maxEvents.input = 20
silence_messages(process, 'TwoTrackMinimumDistance')

process.load('FWCore.MessageLogger.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 1
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('Configuration.Geometry.GeometryIdeal_cff')
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.GlobalTag.globaltag = 'START53_V21::All'
process.load('TrackingTools.TransientTrack.TransientTrackBuilder_cfi')
process.load('SimTracker.TrackAssociation.TrackAssociatorByHits_cfi')

from Configuration.EventContent.EventContent_cff import AODSIMEventContent
process.out = cms.OutputModule('PoolOutputModule', fileName = cms.untracked.string('/uscms/home/tucker/scratch/mfv_vis.root'), outputCommands = AODSIMEventContent.outputCommands)
process.out.outputCommands += ['keep *_*_*_BasicAnalyzer']
process.outp = cms.EndPath(process.out)

process.mfvGenParticles = cms.EDProducer('MFVGenParticles',
                                         gen_src = cms.InputTag('genParticles'),
                                         print_info = cms.bool(True),
                                         )

process.printList = cms.EDAnalyzer('JMTParticleListDrawer',
                                   src = cms.InputTag('genParticles'),
                                   printVertex = cms.untracked.bool(True),
                                   )

process.load('JMTucker.MFVNeutralino.MatchedTracks_cff')
process.load('JMTucker.MFVNeutralino.VertexReco_cff')
from JMTucker.MFVNeutralino.VertexReco_cff import cut_all, clone_all

process.pp = cms.Path(process.mfvGenParticles *
                      process.printList *
                      process.mfvTrackMatching *
                      process.mfvVertexReco
                      )

objs = clone_all(process, 'Cos75')
objs[0].vertexMinAngleCosine = 0.75
process.pp *= objs[-1] # the sequence

cut_name, cut = 'Qntk6M20', 'tracksSize >= 6 && p4.mass >= 20'
process.pp *= cut_all(process, '',      cut_name, cut)
process.pp *= cut_all(process, 'Cos75', cut_name, cut)
