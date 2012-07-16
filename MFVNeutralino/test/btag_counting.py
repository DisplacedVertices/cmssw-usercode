import os, sys, FWCore.ParameterSet.Config as cms

process = cms.Process('MFVNeutralino')
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))
process.source = cms.Source('PoolSource', fileNames = cms.untracked.vstring('file:pat.root'))
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(False))
process.TFileService = cms.Service('TFileService', fileName = cms.string('btag_counting.root'))
process.load('FWCore.MessageLogger.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 10000

btag_srcs = [
    ('CSV',   'combinedSecondaryVertexBJetTags',      (0.244, 0.679, 0.898)),
    ('JP',    'jetProbabilityBJetTags',               (0.275, 0.545, 0.790)),
    ('JBP',   'jetBProbabilityBJetTags',              (1.33, 2.55, 3.74)),
    ('SSVHE', 'simpleSecondaryVertexHighEffBJetTags', (1.74, 3.05)),
    ('SSVHP', 'simpleSecondaryVertexHighPurBJetTags', (2.,)),
    ('TCHE',  'trackCountingHighEffBJetTags',         (1.7, 3.3, 10.2)),
    ('TCHP',  'trackCountingHighPurBJetTags',         (1.19, 1.93, 3.41)),
    ]

debug = 'debug' in sys.argv

process.p = cms.Path()
for btag_name, src, bdisc_mins in btag_srcs:
    for bdisc_min in bdisc_mins:
        obj = cms.EDAnalyzer('MFVNeutralinoPATBTagCounting',
                             jet_src = cms.InputTag('selectedPatJetsPF'),
                             b_discriminator_name = cms.string(src),
                             jet_pt_min = cms.double(50),
                             bdisc_min = cms.double(bdisc_min),
                             verbose = cms.bool(debug),
                             )
        name = btag_name + 'pt50bd' + str(bdisc_min).replace('.','p')
        setattr(process, name, obj)
        process.p *= obj
    
if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    if 'debug' in sys.argv:
        raise RuntimeError('refusing to submit jobs in debug (verbose print out) mode')

    crab_cfg = '''
[CRAB]
jobtype = cmssw
scheduler = condor

[CMSSW]
%(ana_dbs_url)s
datasetpath = %(ana_dataset)s
pset = btag_counting.py
total_number_of_events = -1
events_per_job = 100000

[USER]
ui_working_dir = crab/crab_mfvnu_btag_counting_%(name)s
return_data = 1
'''

    testing = 'testing' in sys.argv

    from JMTucker.Tools.Samples import background_samples, mfv_signal_samples
    for sample in background_samples + mfv_signal_samples:
        open('crab.cfg', 'wt').write(crab_cfg % sample)
        if not testing:
            os.system('crab -create -submit')
            os.system('rm crab.cfg')
