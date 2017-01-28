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
    ana_name = 'ana%i%i' % (mn,mx)
    obj_name = 'byrunseedtracks%i%i' % (mn,mx)
    pth_name = 'pth%i%i' % (mn,mx)
    vtx = process.mfvSelectedVerticesTight.clone(min_ntracks = mn, max_ntracks = mx)
    obj = cms.EDAnalyzer('MFVByRunSeedTracks',
                         event_src = cms.InputTag('mfvEvent'),
                         vertex_src = cms.InputTag(vtx_name),
                         )
    pth = cms.Path(process.mfvAnalysisCuts * vtx * obj)
    setattr(process, vtx_name, vtx)
    setattr(process, obj_name, obj)
    setattr(process, pth_name, pth)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.CondorSubmitter import CondorSubmitter
    import JMTucker.Tools.Samples as Samples 

    samples = Samples.data_samples

    for sample in samples:
        sample.files_per = 50
        if not sample.is_mc:
            sample.json = '../ana_2015.json'

    cs = CondorSubmitter('ByRunSeedTracks_2015', dataset='ntuplev10')
    cs.submit_all(Samples.data_samples[1:])

elif __name__ == '__main__' and hasattr(sys, 'argv') and 'ana' in sys.argv:
    from JMTucker.Tools.ROOTTools import *
