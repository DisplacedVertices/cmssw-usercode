import sys
from JMTucker.Tools.BasicAnalyzer_cfg import cms, process
import JMTucker.MFVNeutralino.TestFiles as TestFiles

process.options.wantSummary = True
TestFiles.set_test_files(process)
process.TFileService.fileName = 'histos.root'

process.load('JMTucker.MFVNeutralino.VertexSelector_cfi')
process.load('JMTucker.MFVNeutralino.Histos_cff')

from JMTucker.MFVNeutralino.VertexSelector_cfi import no_produce_refs 
from JMTucker.MFVNeutralino.Histos_cff import no_use_ref
no_produce_refs(process)
no_use_ref(process)

process.p = cms.Path(process.mfvSelectedVerticesSeq * process.mfvHistos)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    import JMTucker.Tools.Samples as Samples
    samples = Samples.mfv_signal_samples + Samples.ttbar_samples + Samples.qcd_samples

    from JMTucker.Tools.CRABSubmitter import CRABSubmitter
    cs = CRABSubmitter('MFVHistosMC',
                       job_control_from_sample = True,
                       use_ana_dataset = True,
                       )
    cs.submit_all(samples)
