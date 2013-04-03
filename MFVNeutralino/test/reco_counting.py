import os, sys, FWCore.ParameterSet.Config as cms

process = cms.Process('MFVNeutralino')
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))
process.source = cms.Source('PoolSource', fileNames = cms.untracked.vstring('/store/user/tucker/mfv_gensimhlt_gluino_tau9900um_M400/mfv_reco_gluino_tau9900um_M400/4b815091ea4b0e75a52a1ca758900a17/reco_1_1_cNq.root'))
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(False))
process.TFileService = cms.Service('TFileService', fileName = cms.string('reco_counting.root'))
process.load('FWCore.MessageLogger.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 10000

process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.Geometry.GeometryIdeal_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.load("Configuration.StandardSequences.Reconstruction_cff")
process.GlobalTag.globaltag = 'START53_V13::All'

debug = 'debug' in sys.argv


btag_srcs = [
        ('CSV',   'combinedSecondaryVertexBJetTags',      (0.244, 0.679, 0.898)),
        ('JP',    'jetProbabilityBJetTags',               (0.275, 0.545, 0.790)),
        ('JBP',   'jetBProbabilityBJetTags',              (1.33, 2.55, 3.74)),
        ('SSVHE', 'simpleSecondaryVertexHighEffBJetTags', (1.74, 3.05)),
        ('SSVHP', 'simpleSecondaryVertexHighPurBJetTags', (2.,)),
        ('TCHE',  'trackCountingHighEffBJetTags',         (1.7, 3.3, 10.2)),
        ('TCHP',  'trackCountingHighPurBJetTags',         (1.19, 1.93, 3.41)),
        ]

from RecoJets.JetProducers.kt4PFJets_cfi import kt4PFJets
assert not hasattr(process, 'kt6PFJetsForIsolation')
process.kt6PFJetsForIsolation = kt4PFJets.clone(rParam = 0.6, doRhoFastjet = True)
process.kt6PFJetsForIsolation.Rho_EtaMax = cms.double(2.5)

for name in ['elPFIsoValuePU04PFIdPFIso', 'elPFIsoValuePU03PFIdPFIso', 'elPFIsoValueCharged03PFIdPFIso', 'elPFIsoValueNeutral04NoPFIdPFIso', 'elPFIsoValueCharged04PFIdPFIso', 'elPFIsoValueNeutral03NoPFIdPFIso', 'elPFIsoValueChargedAll04NoPFIdPFIso', 'elPFIsoValueChargedAll03PFIdPFIso', 'elPFIsoValueChargedAll04PFIdPFIso', 'elPFIsoValueGamma04PFIdPFIso', 'elPFIsoDepositNeutralPFIso', 'elPFIsoValueCharged04NoPFIdPFIso', 'elPFIsoValueGamma03NoPFIdPFIso', 'elPFIsoDepositChargedAllPFIso', 'elPFIsoValuePU04NoPFIdPFIso', 'elPFIsoDepositPUPFIso', 'elPFIsoValueNeutral03PFIdPFIso', 'elPFIsoValueCharged03NoPFIdPFIso', 'elPFIsoDepositChargedPFIso', 'elPFIsoValueChargedAll03NoPFIdPFIso', 'elPFIsoDepositGammaPFIso', 'elPFIsoValuePU03NoPFIdPFIso', 'elPFIsoValueGamma03PFIdPFIso', 'elPFIsoValueNeutral04PFIdPFIso', 'elPFIsoValueGamma04NoPFIdPFIso']:
    assert not hasattr(process, name)
from CommonTools.ParticleFlow.Tools.pfIsolation import setupPFElectronIso
process.gsfEleIsoSequence = setupPFElectronIso(process, 'gsfElectrons')

pobj = (process.pfParticleSelectionSequence + process.gsfEleIsoSequence + process.kt6PFJetsForIsolation)

for btag_name, bdisc_src, bdisc_mins in btag_srcs:
    for bdisc_min in bdisc_mins:
        obj = cms.EDAnalyzer('MFVNeutralinoBTagCounting',
                             btag_src = cms.InputTag(bdisc_src),
                             bdisc_min = cms.double(bdisc_min),
                             jet_pt_min = cms.double(30),
                             vertex_src = cms.InputTag('offlinePrimaryVertices'),
                             muon_src = cms.InputTag('muons'),
                             electron_src = cms.InputTag('gsfElectrons'),
                             verbose = cms.bool(debug),
                             )
        name = btag_name + 'pt30bd' + str(bdisc_min).replace('.','p')
        setattr(process, name, obj)
        pobj *= obj
process.p = cms.Path(pobj)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    if 'debug' in sys.argv:
        raise RuntimeError('refusing to submit jobs in debug (verbose print out) mode')

    crab_cfg = '''
[CRAB]
jobtype = cmssw
scheduler = condor

[CMSSW]
%(dbs_url)s
datasetpath = %(dataset)s
pset = reco_counting.py
total_number_of_events = -1
events_per_job = 100000

[USER]
ui_working_dir = crab/reco_counting/crab_mfv_reco_counting_%(name)s
return_data = 1
'''

    testing = 'testing' in sys.argv

    def submit(sample):
        open('crab.cfg', 'wt').write(crab_cfg % sample)
        if not testing:
            os.system('crab -create -submit')
            os.system('rm crab.cfg')

    from JMTucker.Tools.Samples import mfv_signal_samples
    for sample in mfv_signal_samples:
        submit(sample)
