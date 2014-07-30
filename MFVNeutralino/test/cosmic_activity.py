import sys, os, FWCore.ParameterSet.Config as cms

limited_reco = True
write_reco = False

process = cms.Process('LocalReco')

process.load('Configuration.StandardSequences.Services_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.RawToDigi_Data_cff')
process.load('Configuration.StandardSequences.L1Reco_cff')
process.load('Configuration.StandardSequences.Reconstruction_cff')

process.source = cms.Source('PoolSource', fileNames = cms.untracked.vstring('/store/user/tucker/162F7B5B-579A-E111-8EAD-BCAEC518FF68.root'))
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))
process.MessageLogger.cerr.FwkReport.reportEvery = 1

if not 'debug' in sys.argv:
    process.options.wantSummary = False
    process.MessageLogger.cerr.FwkReport.reportEvery = 1000000
    for category in ['TwoTrackMinimumDistance']:
        process.MessageLogger.categories.append(category)
        setattr(process.MessageLogger.cerr, category, cms.untracked.PSet(limit=cms.untracked.int32(0)))

process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'FT_R_53_V6C::All', '')

process.TFileService = cms.Service('TFileService', fileName = cms.string('cosmic_activity.root'))
process.CosmicActivity = cms.EDAnalyzer('MFVCosmicActivity')

from HLTrigger.HLTfilters.hltHighLevel_cfi import hltHighLevel
process.triggerFilter = hltHighLevel.clone()
process.triggerFilter.HLTPaths = ['HLT_QuadJet50_v*']
process.triggerFilter.andOr = True # = OR

process.p = cms.Path(process.triggerFilter)

if limited_reco:
    process.p *= (process.muonCSCDigis * process.muonDTDigis * process.muonRPCDigis *
                  process.L1Reco *
                  process.offlineBeamSpot *
                  process.muonlocalreco * process.standAloneMuonSeeds * process.standAloneMuons *
                  process.CosmicMuonSeed * process.cosmicMuons * process.cosmicMuons1Leg)
else:
    process.p *= process.RawToDigi * process.L1Reco * process.reconstruction
    process.p.remove(process.castorreco)
    process.p.remove(process.CastorFullReco)

process.p *= process.CosmicActivity

if write_reco:
    to_keep = [
        'drop *',
        'keep triggerTriggerEvent_hltTriggerSummaryAOD__HLT',
        'keep L1GlobalTriggerObjectMapRecord_hltL1GtObjectMap__HLT',
        'keep edmTriggerResults_TriggerResults__HLT',
        'keep *_offlineBeamSpot_*_*',
        'keep *_offlinePrimaryVertices_*_*',
        'drop *_offlinePrimaryVertices_WithBS_*',
        'keep *_dt1DRecHits_*_*',
        'keep *_dt4DSegments_*_*',
        'keep *_dt1DCosmicRecHits_*_*',
        'keep *_dt4DCosmicSegments_*_*',
        'keep *_csc2DRecHits_*_*',
        'keep *_cscSegments_*_*',
        'keep *_rpcRecHits_*_*',
        'keep *_ancientMuonSeed_*_*',
        'keep *_standAloneMuons_*_*',
        'drop *_standAloneMuons_UpdatedAtVtx_*',
        'keep *_CosmicMuonSeed_*_*',
        'keep *_cosmicMuons_*_*',
        'keep *_cosmicMuons1Leg_*_*',
        ]

    process.out = cms.OutputModule('PoolOutputModule',
                                   fileName = cms.untracked.string('cosmicac.root'),
                                   SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring('p')),
                                   outputCommands = cms.untracked.vstring(*to_keep),
                                   )
    process.outp = cms.EndPath(process.out)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.Samples import DataSample

    samples = [
        DataSample('MultiJetPk2012B', '/MultiJet1Parked/Run2012B-v1/RAW'),
        DataSample('MultiJetPk2012C', '/MultiJet1Parked/Run2012C-v1/RAW'),
        DataSample('MultiJetPk2012D', '/MultiJet1Parked/Run2012D-v1/RAW'),
    ]

    def modify(sample):
        to_add = []
        to_replace = []

        tag = None
        if sample.name.endswith('C'):
            tag = 'FT_P_V42C'
        elif sample.name.endswith('D'):
            tag = 'FT_P_V42D'
        if tag is not None:
            to_add.append("process.GlobalTag.globaltag = '%s::All'" % tag)

        return to_add, to_replace
    
    from JMTucker.Tools.CRABSubmitter import CRABSubmitter
    cs = CRABSubmitter('CosmicActivity',
                       pset_modifier = modify,
                       total_number_of_lumis = -1,
                       lumis_per_job = 20,
                       CMSSW_lumi_mask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions12/8TeV/Reprocessing/Cert_190456-208686_8TeV_22Jan2013ReReco_Collisions12_JSON.txt',
                       GRID_data_location_override = 'T2_US',
                       skip_common = True,
                       )
    cs.submit_all(samples)
