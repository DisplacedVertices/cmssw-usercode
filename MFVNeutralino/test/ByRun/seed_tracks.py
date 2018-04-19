import sys
from JMTucker.Tools.BasicAnalyzer_cfg import *

sample_files(process, 'JetHT2016G', 'ntuplev14')
process.TFileService.fileName = 'byrunseedtracks.root'
process.maxEvents.input = -1
file_event_from_argv(process)

process.load('JMTucker.MFVNeutralino.VertexSelector_cfi')
process.load('JMTucker.MFVNeutralino.AnalysisCuts_cfi')
process.mfvAnalysisCuts.apply_vertex_cuts = False

process.byrunInclusive = cms.EDAnalyzer('MFVByX',
                                        event_src = cms.InputTag('mfvEvent'),
                                        vertex_src = cms.InputTag(''),
                                        by_run = cms.bool(True),
                                        )

process.byrunInclusiveNoAna = process.byrunInclusive.clone()
process.p = cms.Path(process.byrunInclusiveNoAna * process.mfvAnalysisCuts * process.byrunInclusive)

for mn,mx in (3,3), (3,4), (4,4):
    vtx_name = 'vtx%i%i' % (mn,mx)
    obj_name = 'byrun%i%i' % (mn,mx)
    pth_name = 'pth%i%i' % (mn,mx)

    vtx = process.mfvSelectedVerticesTight.clone(min_ntracks = mn, max_ntracks = mx)
    obj = process.byrunInclusive.clone(vertex_src = vtx_name)
    pth = cms.Path(process.mfvAnalysisCuts * vtx * obj)
    setattr(process, vtx_name, vtx)
    setattr(process, obj_name, obj)
    setattr(process, pth_name, pth)

    obj_noana = obj.clone()
    pth_noana = cms.Path(vtx * obj_noana)
    setattr(process, obj_name + 'noana', obj_noana)
    setattr(process, pth_name + 'noana', pth_noana)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.Year import year
    import JMTucker.Tools.Samples as Samples 
    if year == 2015:
        samples = Samples.data_samples_2015
    elif year == 2016:
        samples = Samples.data_samples

    for sample in samples:
        sample.files_per = 50
        if not sample.is_mc:
            sample.json = '../jsons/ana_2015p6.json'

    from JMTucker.Tools.CondorSubmitter import CondorSubmitter
    cs = CondorSubmitter('ByRunStuffV14', dataset='ntuplev14')
    cs.submit_all(samples)
