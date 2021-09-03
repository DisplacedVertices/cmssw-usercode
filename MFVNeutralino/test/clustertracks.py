import sys
from DVCode.Tools.BasicAnalyzer_cfg import *

process.source.fileNames = ['/store/user/tucker/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/ntuplev9/161019_211934/0000/ntuple_1.root']
process.TFileService.fileName = 'clustertracks.root'
process.maxEvents.input = -1
file_event_from_argv(process)

process.load('DVCode.MFVNeutralino.VertexSelector_cfi')
process.load('DVCode.MFVNeutralino.AnalysisCuts_cfi')
process.load('DVCode.MFVNeutralino.WeightProducer_cfi')
process.mfvAnalysisCuts.min_nvertex = 1

process.p = cms.Path(process.mfvWeight * process.mfvSelectedVerticesTight * process.mfvAnalysisCuts)

for min_dbv in [0., 0.02, 0.05, 0.1]:
    ana = cms.EDAnalyzer('MFVClusterTracksHistos',
                         event_src = cms.InputTag('mfvEvent'),
                         vertex_src = cms.InputTag('mfvSelectedVerticesTight'),
                         weight_src = cms.InputTag('mfvWeight'),
                         min_dbv = cms.double(min_dbv),
                         )
    name = 'mfvClusterTracksMindBV0p%02i' % int(min_dbv*100)
    setattr(process, name, ana)
    process.p *= ana

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from DVCode.Tools.CondorSubmitter import CondorSubmitter
    import DVCode.Tools.Samples as Samples 

    samples = Samples.ttbar_samples + Samples.qcd_samples + Samples.qcd_samples_ext + \
        [Samples.mfv_neu_tau00100um_M0800, Samples.mfv_neu_tau00300um_M0800, Samples.mfv_neu_tau01000um_M0800, Samples.mfv_neu_tau10000um_M0800] + \
        [Samples.xx4j_tau00001mm_M0300, Samples.xx4j_tau00010mm_M0300, Samples.xx4j_tau00001mm_M0700, Samples.xx4j_tau00010mm_M0700]

    for sample in samples:
        sample.files_per = 50
        if not sample.is_mc:
            sample.json = 'ana_10pc.json'

    cs = CondorSubmitter('ClusterTracksV10', dataset='ntuplev10')
    cs.submit_all(samples)
