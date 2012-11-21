import os, sys, FWCore.ParameterSet.Config as cms

process = cms.Process('MFVNeutralino')
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))
process.source = cms.Source('PoolSource', fileNames = cms.untracked.vstring('file:/uscms/home/tucker/private/mfv_genfsimreco_535/src/JMTucker/MFVNeutralino/test/fastsim.root'))
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(False))
process.TFileService = cms.Service('TFileService', fileName = cms.string('gen_histos.root'))
process.load('FWCore.MessageLogger.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 100000

process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')

process.GenHistos = cms.EDAnalyzer('MFVNeutralinoGenHistos',
                                   gen_src = cms.InputTag('genParticles'),
                                   gen_jet_src = cms.InputTag('ak5GenJets'),
                                   gen_met_src = cms.InputTag('genMetTrue'),
                                   required_num_leptonic = cms.int32(-1),
                                   allowed_decay_types = cms.vint32(),
                                   print_info = cms.bool(False),
                                   )

process.p = cms.Path(process.GenHistos)

if 'debug' in sys.argv:
    process.printList = cms.EDAnalyzer('ParticleListDrawer',
                                       maxEventsToPrint = cms.untracked.int32(100),
                                       src = cms.InputTag('genParticles'),
                                       printOnlyHardInteraction = cms.untracked.bool(False),
                                       useMessageLogger = cms.untracked.bool(False),
                                       printVertex = cms.untracked.bool(True),
                                       )
    process.GenHistos.print_info = True
    process.p *= process.printList


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    if 'debug' in sys.argv:
        raise RuntimeError('refusing to submit jobs in debug (verbose print out) mode')

    crab_cfg = '''
[CRAB]
jobtype = cmssw
scheduler = condor

[CMSSW]
dbs_url = https://cmsdbsprod.cern.ch:8443/cms_dbs_ph_analysis_02_writer/servlet/DBSServlet
datasetpath = %(dataset)s
pset = gen_histos.py
total_number_of_events = -1
events_per_job = 50000

[USER]
ui_working_dir = crab/crab_mfvnu_gen_histos_%(name)s
return_data = 1
'''

    testing = 'testing' in sys.argv

    jobs = [
        ('tau100um', '/mfvneutralino_genfsimreco_tau100um/tucker-mfvneutralino_genfsimreco_tau100um-465709e5340ac2cc11e2751b48bbef3e/USER'),
        ('tau10um',  '/mfvneutralino_genfsimreco_tau10um/tucker-mfvneutralino_genfsimreco_tau10um-719b1b049e9de8135afa1f308d0994e6/USER'),
        ('tau1mm',   '/mfvneutralino_genfsimreco_tau1mm/tucker-mfvneutralino_genfsimreco_tau1mm-f0b5b0c98c357fc0015e0194f7aef803/USER'),
        ('tau9p9mm', '/mfvneutralino_genfsimreco_tau9p9mm/tucker-mfvneutralino_genfsimreco_tau9p9mm-891f0c49f79ad2222cb205736c37de4f/USER'),
        ]

    for name, dataset in jobs:
        open('crab.cfg', 'wt').write(crab_cfg % locals())
        if not testing:
            os.system('crab -create -submit')
            os.system('rm crab.cfg')
