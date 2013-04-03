import os, sys, FWCore.ParameterSet.Config as cms
debug = 'debug' in sys.argv

process = cms.Process('MFVNeutralino')
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))
process.source = cms.Source('PoolSource', fileNames = cms.untracked.vstring('/store/user/tucker/mfv_gensimhlt_gluino_tau9900um_M0400/reco/a3f0d9ac5e396df027589da2067010b0/reco_1_1_ohS.root'))
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(False))
process.TFileService = cms.Service('TFileService', fileName = cms.string('gen_histos.root'))
process.load('FWCore.MessageLogger.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 100000

process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')

process.GenHistos = cms.EDAnalyzer('MFVNeutralinoGenHistos',
                                   gen_src = cms.InputTag('genParticles'),
                                   required_num_leptonic = cms.int32(-1),
                                   allowed_decay_types = cms.vint32(),
                                   print_info = cms.bool(False),
                                   )

process.p = cms.Path(process.GenHistos)

if 0:
    process.source.fileNames = ['file:/uscmst1b_scratch/lpc1/3DayLifetime/tucker/fastsim_21_3_oyS.root']
    from JMTucker.Tools.CMSSWTools import set_events_to_process
    set_events_to_process(process, [(1,74)])
    debug = True

if debug:
    process.printList = cms.EDAnalyzer('ParticleListDrawer',
                                       maxEventsToPrint = cms.untracked.int32(100),
                                       src = cms.InputTag('genParticles'),
                                       printOnlyHardInteraction = cms.untracked.bool(False),
                                       useMessageLogger = cms.untracked.bool(False),
                                       printVertex = cms.untracked.bool(True),
                                       )
    process.GenHistos.print_info = True
    process.p.insert(0, process.printList)


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    if debug:
        raise RuntimeError('refusing to submit jobs in debug (verbose print out) mode')

    crab_cfg = '''
[CRAB]
jobtype = cmssw
scheduler = glite

[CMSSW]
dbs_url = https://cmsdbsprod.cern.ch:8443/cms_dbs_ph_analysis_02_writer/servlet/DBSServlet
datasetpath = %(dataset)s
pset = gen_histos.py
total_number_of_events = -1
events_per_job = 50000

[USER]
jmt_skip_input_files = src/EGamma/EGammaAnalysisTools/data/*
ui_working_dir = crab/gen_histos/crab_mfv_gen_histos_%(name)s
return_data = 1
'''

    testing = 'testing' in sys.argv

    from JMTucker.Tools.Samples import mfv_signal_samples
    for sample in mfv_signal_samples:
        open('crab.cfg', 'wt').write(crab_cfg % sample)
        if not testing:
            os.system('crab -create -submit')
            os.system('rm crab.cfg')
