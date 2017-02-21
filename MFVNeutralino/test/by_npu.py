import sys
from JMTucker.Tools.BasicAnalyzer_cfg import *

sample_files(process, 'qcdht2000', 'ntuplev11')
process.TFileService.fileName = 'by_npu.root'
process.maxEvents.input = -1
file_event_from_argv(process)

process.load('JMTucker.MFVNeutralino.VertexSelector_cfi')
process.load('JMTucker.MFVNeutralino.AnalysisCuts_cfi')
process.mfvAnalysisCuts.apply_vertex_cuts = False

for mn,mx in (3,3), (3,4), (4,4):
    vtx_name = 'vtx%i%i' % (mn,mx)
    obj_name = 'byrun%i%i' % (mn,mx)
    pth_name = 'pth%i%i' % (mn,mx)

    vtx = process.mfvSelectedVerticesTight.clone(min_ntracks = mn, max_ntracks = mx)

    obj = cms.EDAnalyzer('MFVByX',
                         event_src = cms.InputTag('mfvEvent'),
                         vertex_src = cms.InputTag(vtx_name),
                         by_npu = cms.bool(True),
                         )

    pth = cms.Path(process.mfvAnalysisCuts * vtx * obj)
    setattr(process, vtx_name, vtx)
    setattr(process, obj_name, obj)
    setattr(process, pth_name, pth)

    obj_noana = obj.clone()
    pth_noana = cms.Path(vtx * obj_noana)
    setattr(process, obj_name + 'noana', obj_noana)
    setattr(process, pth_name + 'noana', pth_noana)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    import JMTucker.Tools.Samples as Samples 
    samples = [Samples.qcdht1500, Samples.qcdht1500ext, Samples.qcdht2000, Samples.qcdht2000ext]
    for sample in samples:
        sample.files_per = 10

    from JMTucker.Tools.CondorSubmitter import CondorSubmitter
    cs = CondorSubmitter('ByNpuV11_15', dataset='ntuplev11')
    cs.submit_all(samples)
