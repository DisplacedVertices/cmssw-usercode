from JMTucker.Tools.BasicAnalyzer_cfg import cms, process
from JMTucker.MFVNeutralino.SimFiles import load as load_files
load_files(process, 'tau9900um_M0400', 0)
process.MessageLogger.cerr.FwkReport.reportEvery = 100
process.TFileService.fileName = 'checks.root'

#process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
#process.load('SimTracker.TrackAssociation.TrackAssociatorByHits_cfi')
#process.load('Configuration.Geometry.GeometryIdeal_cff')
#process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
#process.GlobalTag.globaltag = 'START53_V13::All'
#process.load('TrackingTools.TransientTrack.TransientTrackBuilder_cfi')

process.CheckGenParticleBarcodes = cms.EDAnalyzer('CheckGenParticleBarcodes',
                                                  gen_particles_src = cms.InputTag('genParticles'),
                                                  tracking_particles_src = cms.InputTag('mergedtruth','MergedTrackTruth'),
                                                  )

process.mfvGenParticles = cms.EDProducer('MFVGenParticles',
                                         gen_src = cms.InputTag('genParticles'),
                                         gen_jet_src = cms.InputTag('ak5GenJets'),
                                         gen_met_src = cms.InputTag('genMetTrue'),
                                         print_info = cms.bool(True),
                                         )

process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')

process.printList = cms.EDAnalyzer('ParticleListDrawer',
                                   maxEventsToPrint = cms.untracked.int32(100),
                                   src = cms.InputTag('genParticles'),
                                   printOnlyHardInteraction = cms.untracked.bool(False),
                                   useMessageLogger = cms.untracked.bool(False),
                                   printVertex = cms.untracked.bool(True),
                                   )

process.printList2 = process.printList.clone(src = cms.InputTag('mfvGenParticles', 'All'))
process.printList3 = process.printList.clone(src = cms.InputTag('mfvGenParticles', 'Visible'))

process.p = cms.Path(process.CheckGenParticleBarcodes)

import sys, os
if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    crab_cfg = '''
[CRAB]
jobtype = cmssw
scheduler = condor

[CMSSW]
datasetpath = %(dataset)s
dbs_url = https://cmsdbsprod.cern.ch:8443/cms_dbs_ph_analysis_02_writer/servlet/DBSServlet
pset = checks.py
get_edm_output = 1
events_per_job = 2000
total_number_of_events = -1

[USER]
ui_working_dir = crab/vtxrecochecks/crab_mfv_vtxrecochecks_%(name)s
return_data = 1
'''

    os.system('mkdir -p crab/vtxrecochecks')
    testing = 'testing' in sys.argv

    datasets = [
        ('gluino_tau0000um_M400', '/mfv_gensimhlt_gluino_tau0000um_M400/tucker-mfv_gensimhlt_gluino_tau0000um_M400-f418ab66d2aa2ce17edadebd0427e711/USER'),
        ('gluino_tau0010um_M1000', '/mfv_gensimhlt_gluino_tau0010um_M1000/tucker-mfv_gensimhlt_gluino_tau0010um_M1000-1a774d010111a1aed9668a1957d7b272/USER'),
        ('gluino_tau0010um_M600', '/mfv_gensimhlt_gluino_tau0010um_M600/tucker-mfv_gensimhlt_gluino_tau0010um_M600-1a774d010111a1aed9668a1957d7b272/USER'),
        ('gluino_tau0100um_M1000', '/mfv_gensimhlt_gluino_tau0100um_M1000/tucker-mfv_gensimhlt_gluino_tau0100um_M1000-cd908390df85e15f67c1b503d4c4278e/USER'),
        ('gluino_tau0100um_M800', '/mfv_gensimhlt_gluino_tau0100um_M800/tucker-mfv_gensimhlt_gluino_tau0100um_M800-cd908390df85e15f67c1b503d4c4278e/USER'),
        ('gluino_tau1000um_M200', '/mfv_gensimhlt_gluino_tau1000um_M200/tucker-mfv_gensimhlt_gluino_tau1000um_M200-11e502b9027fe454bec38485095c4f53/USER'),
        ('gluino_tau1000um_M400', '/mfv_gensimhlt_gluino_tau1000um_M400/tucker-mfv_gensimhlt_gluino_tau1000um_M400-11e502b9027fe454bec38485095c4f53/USER'),
        ('gluino_tau1000um_M600', '/mfv_gensimhlt_gluino_tau1000um_M600/tucker-mfv_gensimhlt_gluino_tau1000um_M600-11e502b9027fe454bec38485095c4f53/USER'),
        ('gluino_tau1000um_M800', '/mfv_gensimhlt_gluino_tau1000um_M800/tucker-mfv_gensimhlt_gluino_tau1000um_M800-11e502b9027fe454bec38485095c4f53/USER'),
        ('gluino_tau4000um_M1000', '/mfv_gensimhlt_gluino_tau4000um_M1000/tucker-mfv_gensimhlt_gluino_tau4000um_M1000-9dcf202e97da119ad22d8e489ec7b88e/USER'),
        ('gluino_tau4000um_M200', '/mfv_gensimhlt_gluino_tau4000um_M200/tucker-mfv_gensimhlt_gluino_tau4000um_M200-9dcf202e97da119ad22d8e489ec7b88e/USER'),
        ('gluino_tau4000um_M600', '/mfv_gensimhlt_gluino_tau4000um_M600/tucker-mfv_gensimhlt_gluino_tau4000um_M600-9dcf202e97da119ad22d8e489ec7b88e/USER'),
        ('gluino_tau9900um_M1000', '/mfv_gensimhlt_gluino_tau9900um_M1000/tucker-mfv_gensimhlt_gluino_tau9900um_M1000-dd93627319a5f24d5d7ad10ea45db562/USER'),
#        ('gluino_tau9900um_M400', '/mfv_gensimhlt_gluino_tau9900um_M400/tucker-mfv_gensimhlt_gluino_tau9900um_M400-dd93627319a5f24d5d7ad10ea45db562/USER'),
        ]

    for name, dataset in datasets:
        open('crab.cfg','wt').write(crab_cfg % locals())
        if not testing:
            os.system('crab -create -submit')
            os.system('rm -f crab.cfg')
