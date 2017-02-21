import sys
from JMTucker.Tools.BasicAnalyzer_cfg import *

sample_files(process, 'JetHT2015D', 'ntuplev10')
process.TFileService.fileName = 'byrunseedtracks.root'
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
                         by_run = cms.bool(True),
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
    from JMTucker.Tools.CondorSubmitter import CondorSubmitter
    import JMTucker.Tools.Samples as Samples 

    samples = Samples.data_samples

    for sample in samples:
        sample.files_per = 50
        if not sample.is_mc:
            sample.json = '../ana_2015.json'

    cs = CondorSubmitter('ByRunStuff_2015_v5', dataset='ntuplev10')
    cs.submit_all(Samples.data_samples)
