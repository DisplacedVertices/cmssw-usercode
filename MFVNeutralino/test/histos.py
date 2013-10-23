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

control_region = 'SemimuLE3jets'

if control_region:
    process.mfvAnalysisCuts.min_nvertex = 0
    process.mfvAnalysisCuts.min_ntracks01 = 0
    process.mfvAnalysisCuts.min_maxtrackpt01 = 0

    process.mfvAnalysisCuts.min_4th_jet_pt = 0
    process.mfvAnalysisCuts.min_njets = 0
    process.mfvAnalysisCuts.max_njets = 3

    from JMTucker.MFVNeutralino.Histos_cff import re_trigger
    re_trigger(process)
    process.mfvAnalysisCuts.trigger_bit = 4
    process.mfvAnalysisCuts.min_nsemilepmuons = 1

process.p = cms.Path(process.mfvSelectedVerticesTight * process.mfvHistos)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    import JMTucker.Tools.Samples as Samples
    samples = Samples.mfv_signal_samples + Samples.ttbar_samples + Samples.smaller_background_samples
    if 'mu' in control_region:
        samples += [Samples.SingleMu2012B] + Samples.leptonic_background_samples
    else:
        samples += [Samples.MultiJetPk2012B] + Samples.qcd_samples

    from JMTucker.Tools.CRABSubmitter import CRABSubmitter
    cs = CRABSubmitter('MFVHistos' + control_region,
                       job_control_from_sample = True,
                       use_ana_dataset = True,
                       use_parent = process.mfvAnalysisCuts.re_trigger.value(),
                       )
    cs.submit_all(samples)
