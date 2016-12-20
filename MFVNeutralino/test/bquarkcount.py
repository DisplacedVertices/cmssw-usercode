import sys
from JMTucker.Tools.BasicAnalyzer_cfg import *

process.source.fileNames = ['/store/user/tucker/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/ntuplev9/161019_211934/0000/ntuple_1.root']
process.TFileService.fileName = 'bquarkcount.root'
file_event_from_argv(process)

process.load('JMTucker.MFVNeutralino.WeightProducer_cfi')
process.load('JMTucker.MFVNeutralino.AnalysisCuts_cfi')
process.load('JMTucker.MFVNeutralino.VertexSelector_cfi')
process.mfvAnalysisCuts.apply_vertex_cuts = False
process.p = cms.Path(process.mfvWeight * process.mfvAnalysisCuts)

for i in (3,4,5):
    vtx = process.mfvSelectedVerticesTight.clone(min_ntracks = i)
    if vtx != 5:
        vtx.max_ntracks = i
    vtx_name = 'v%i' % i
    setattr(process, vtx_name, vtx)

    ana = cms.EDAnalyzer('MFVBQuarkCount',
                         event_src = cms.InputTag('mfvEvent'),
                         vertex_src = cms.InputTag(vtx_name),
                         weight_src = cms.InputTag('mfvWeight'),
                         )
    setattr(process, 'bqcount%i' % i, ana)

    process.p *= vtx * ana

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.CondorSubmitter import CondorSubmitter
    import JMTucker.Tools.Samples as Samples

    samples = Samples.ttbar_samples + Samples.qcd_samples

    for sample in samples:
        sample.files_per = 50
        if not sample.is_mc:
            sample.json = 'ana_10pc.json'

    cs = CondorSubmitter('BQuarkCountV10', dataset='ntuplev10')
    cs.submit_all(samples)
