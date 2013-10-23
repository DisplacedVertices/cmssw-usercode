import sys
from JMTucker.Tools.BasicAnalyzer_cfg import cms, process
import JMTucker.MFVNeutralino.TestFiles as TestFiles

process.options.wantSummary = True
TestFiles.set_test_files(process)
process.TFileService.fileName = 'histos.root'

process.load('JMTucker.MFVNeutralino.VertexSelector_cfi')
process.load('JMTucker.MFVNeutralino.Histos_cff')
process.mfvVertexHistos        .use_ref = False
process.mfvVertexHistosNoCuts  .use_ref = False
process.mfvVertexHistosWAnaCuts.use_ref = False
process.mfvVertexHistosNoCutsWAnaCuts.use_ref = False

control_region = True
if control_region:
    process.mfvAnalysisCuts.min_nvertex = 0
    process.mfvAnalysisCuts.min_ntracks01 = 0
    process.mfvAnalysisCuts.min_maxtrackpt01 = 0

    process.mfvAnalysisCuts.min_4th_jet_pt = 0
    process.mfvAnalysisCuts.min_njets = 0
    process.mfvAnalysisCuts.max_njets = 3

    process.mfvAnalysisCuts     .re_trigger = True # JMTBAD make an "EventRedoer"
    process.mfvEventHistosNoCuts.re_trigger = True
    process.mfvEventHistos      .re_trigger = True
    process.mfvAnalysisCuts.trigger_bit = 4
    process.mfvAnalysisCuts.min_nsemilepmuons = 1

process.p = cms.Path(process.mfvSelectedVerticesTight * process.mfvHistos)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    import JMTucker.Tools.Samples as Samples
    samples = Samples.data_samples + Samples.mfv_signal_samples + Samples.background_samples + Samples.smaller_background_samples

    from JMTucker.Tools.CRABSubmitter import CRABSubmitter
    cs = CRABSubmitter('MFVHistos',
                       job_control_from_sample = True,
                       use_ana_dataset = True,
                       USER_jmt_skip_input_files = 'src/EGamma/EGammaAnalysisTools/data/*',
                       )
    cs.submit_all(samples)
