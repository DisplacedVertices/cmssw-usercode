import os, sys
from JMTucker.Tools.BasicAnalyzer_cfg import cms, process, geometry_etc
from JMTucker.Tools.CMSSWTools import silence_messages
import JMTucker.MFVNeutralino.TestFiles as TestFiles

process.setName_('MFVNtuple')
#process.MessageLogger.cerr.FwkReport.reportEvery = 1
process.source.fileNames = TestFiles.tau1000M0400
process.source.secondaryFileNames = TestFiles.tau1000M0400_sec
process.maxEvents.input = 2000
process.options.wantSummary = True
process.TFileService.fileName = 'ntuple_histos.root'
silence_messages(process, 'TwoTrackMinimumDistance')
geometry_etc(process, 'START53_V27::All')

process.out = cms.OutputModule('PoolOutputModule',
                               fileName = cms.untracked.string('ntuple.root'),
                               outputCommands = cms.untracked.vstring(
                                   'drop *',
                                   'keep MFVEvent_mfvEvent__*',
                                   'keep MFVVertexAuxs_mfvVerticesAux__*'),
                               )
process.outp = cms.EndPath(process.out)

process.load('CommonTools.ParticleFlow.goodOfflinePrimaryVertices_cfi')
process.goodOfflinePrimaryVertices.filter = cms.bool(False)

process.load('JMTucker.MFVNeutralino.Vertexer_cff')
process.load('JMTucker.MFVNeutralino.EventProducer_cfi')
process.load('JMTucker.MFVNeutralino.Histos_cff')
process.p = cms.Path(process.goodOfflinePrimaryVertices * process.mfvVertexSequence * process.mfvEvent * process.mfvHistos)

if not 'debug' in sys.argv:
    from JMTucker.Tools.general import big_warn
    big_warn("\nusing vertices stored in PAT tuple, hope you didn't mean to change their reco\n")
    process.p.remove(process.mfvVertices)
else:
    process.MessageLogger.cerr.FwkReport.reportEvery = 1
    process.mfvVertices.verbose = True

if 'testqcd' in sys.argv:
    process.source.fileNames = TestFiles.qcdht1000
    process.source.secondaryFileNames = TestFiles.qcdht1000_sec
elif 'testttbar' in sys.argv:
    process.source.fileNames = TestFiles.ttbarhadronic
    process.source.secondaryFileNames = TestFiles.ttbarhadronic_sec

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    if 'debug' in sys.argv:
        raise RuntimeError('refusing to submit jobs in debug (verbose print out) mode')

    import JMTucker.Tools.Samples as Samples
    samples = [Samples.mfv_neutralino_tau1000um_M0400, Samples.ttbarhadronic]
    
    from JMTucker.Tools.CRABSubmitter import CRABSubmitter
    cs = CRABSubmitter('MFVNtupleTest',
                       total_number_of_events = 99250,
                       events_per_job = 10000,
                       #job_control_from_sample = True,
                       use_ana_dataset = True,
                       use_parent = True,
                       get_edm_output = True,
                       data_retrieval = 'fnal',
                       publish_data_name = 'mfvntupletest',
                       )
    cs.submit_all(samples)
