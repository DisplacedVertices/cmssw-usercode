import os, sys, FWCore.ParameterSet.Config as cms

process = cms.Process('ResolutionsHistogrammer')
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))
process.source = cms.Source('PoolSource', fileNames = cms.untracked.vstring('/store/user/tucker/mfvneutralino_genfsimreco_tau10um/sstoptuple_v3_mfvN3jtau10um/ffbc82b68f588f5f183a150670744b16/pat_1_1_6Sq.root'))
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(False))
process.TFileService = cms.Service('TFileService', fileName = cms.string('mfv_resolutions_histos.root'))
process.load('FWCore.MessageLogger.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 100000

from HLTrigger.HLTfilters.hltHighLevel_cfi import hltHighLevel
process.goodDataFilter = hltHighLevel.clone()
process.goodDataFilter.TriggerResultsTag = cms.InputTag('TriggerResults', '', 'PAT')
process.goodDataFilter.HLTPaths = ['eventCleaningAll'] # can set to just 'goodOfflinePrimaryVertices', for example
process.goodDataFilter.andOr = False # = AND

process.triggerFilter = hltHighLevel.clone()
process.triggerFilter.HLTPaths = ['HLT_IsoMu17_eta2p1_TriCentralPFNoPUJet30_v*', 'HLT_Ele25_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_TriCentralPFNoPUJet30_v*']
process.triggerFilter.andOr = True # = OR

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
    return cms.EDAnalyzer('MFVNeutralinoResolutionsHistogrammer',
                          reweight_pileup = cms.bool(True),
                          force_weight = cms.double(-1),
                          vertex_src = cms.InputTag('goodOfflinePrimaryVertices'),
                          met_src = cms.InputTag('patMETsPF'),
                          jet_src = cms.InputTag('selectedPatJetsPF'),
                          b_discriminators = cms.vstring(*[name for name, discs in bdiscs]),
                          b_discriminator_mins = cms.vdouble(*[discs[1] for name, discs in bdiscs]),
                          muon_src = cms.InputTag('selectedPatMuonsPF'),
                          max_muon_dxy = cms.double(0.2),
                          max_muon_dz = cms.double(0.5),
                          muon_semilep_cut = selection.semilepMuonCut,
                          muon_dilep_cut = selection.dilepMuonCut,
                          electron_src = cms.InputTag('selectedPatElectronsPF'),
                          max_semilep_electron_dxy = cms.double(0.02),
                          max_dilep_electron_dxy = cms.double(0.04),
                          electron_semilep_cut = selection.semilepElectronCut,
                          electron_dilep_cut = selection.dilepElectronCut,
                          print_info = cms.bool(False),
                          )

process.histos              = histogrammer()
process.histosNoClean       = histogrammer()
process.histosNoTrig        = histogrammer()
process.histosNoCleanNoTrig = histogrammer()

process.eventIds = cms.EDAnalyzer('EventIdRecorder')

process.p0 = cms.Path(process.goodDataFilter * process.triggerFilter * process.eventIds * process.histos)
process.p1 = cms.Path(                         process.triggerFilter * process.eventIds * process.histosNoClean)
process.p2 = cms.Path(process.goodDataFilter *                         process.eventIds * process.histosNoTrig)
process.p3 = cms.Path(                                                 process.eventIds * process.histosNoCleanNoTrig)

if 'debug' in sys.argv:
    process.MessageLogger.cerr.FwkReport.reportEvery = 1
    process.histos.print_info = True
    process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
    process.printList = cms.EDAnalyzer('ParticleListDrawer',
                                       maxEventsToPrint = cms.untracked.int32(100),
                                       src = cms.InputTag('genParticles'),
                                       printOnlyHardInteraction = cms.untracked.bool(False),
                                       useMessageLogger = cms.untracked.bool(False)
                                       )
    process.p *= process.printList

def run_on_data(dataset=None, datasets=None):
    if 'debug' in sys.argv:
        process.p.remove(process.printList)

    if dataset and datasets:
        veto_filter = cms.EDFilter('VetoOtherDatasets', datasets_to_veto = cms.vstring(*[d for d in datasets if d != dataset]))
        setattr(process, 'dataset%sOnly' % dataset, veto_filter)
        for path_name, path in process.paths_().iteritems():
            path.insert(0, veto_filter)

#run_on_data('MultiJet', ['MultiJet', 'JetHT', 'MuHad', 'ElectronHad'])

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    if 'debug' in sys.argv:
        raise RuntimeError('refusing to submit jobs in debug (verbose print out) mode')
    
    crab_cfg = '''
[CRAB]
jobtype = cmssw
scheduler = condor

[CMSSW]
dbs_url = https://cmsdbsprod.cern.ch:8443/cms_dbs_ph_analysis_02_writer/servlet/DBSServlet
datasetpath = %(ana_dataset)s
pset = resolutions_crab.py
%(job_control)s

[USER]
ui_working_dir = crab/resolutions/crab_sstopresolutions_%(name)s_xxx
return_data = 1
'''
    
    just_testing = 'testing' in sys.argv

    def submit(sample):
        new_py = open('resolutions.py').read()

        if not sample.is_mc:
            new_py += '\nrun_on_data()\n'
        
        open('resolutions_crab.py', 'wt').write(new_py)
        open('crab.cfg', 'wt').write(crab_cfg % sample)
        if not just_testing:
            os.system('crab -create -submit')
            os.system('rm crab.cfg resolutions_crab.py resolutions_crab.pyc')
        else:
            print '.py diff:\n---------'
            os.system('diff -uN resolutions.py resolutions_crab.py')
            raw_input('ok?')
            print '\ncrab.cfg:\n---------'
            os.system('cat crab.cfg')
            raw_input('ok?')
            print

    from JMTucker.Tools.Samples import background_samples, mfv_signal_samples, data_samples
    for sample in mfv_signal_samples + background_samples: # + data_samples:
        if sample.ana_ready:
            submit(sample)
