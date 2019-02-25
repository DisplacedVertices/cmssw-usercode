from JMTucker.Tools.BasicAnalyzer_cfg import *

from JMTucker.MFVNeutralino.NtupleCommon import ntuple_version_use as version, dataset
sample_files(process, 'JetHT2017F', dataset, 1)
tfileservice(process, 'per_vertex.root')
file_event_from_argv(process)

process.load('JMTucker.MFVNeutralino.VertexSelector_cfi')
process.load('JMTucker.MFVNeutralino.AnalysisCuts_cfi')
process.load('JMTucker.MFVNeutralino.ByX_cfi')

process.mfvAnalysisCuts.min_nvertex = 1
process.mfvAnalysisCuts.max_nvertex = 1 # nsv >= 2 blinded in ByX but set this anyway

for ntk in 3,4: #,5:
    vtx_name = 'mfvSelectedVerticesTightNtk%i' % ntk
    vtx = getattr(process, vtx_name)
    ana = process.mfvAnalysisCuts.clone(vertex_src = vtx_name)
    byr = process.mfvByRun       .clone(vertex_src = vtx_name)
    setattr(process, 'mfvAnalysisCuts1VNtk%i' % ntk, ana)
    setattr(process, 'mfvByRunWVtxNtk%i'      % ntk, byr)
    setattr(process, 'p%i' % ntk, cms.Path(vtx * ana * byr))


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.MetaSubmitter import *
    from JMTucker.Tools.Year import year
    from JMTucker.Tools import Samples

    if year == 2017:
        samples = Samples.data_samples_2017
    elif year == 2018:
        samples = Samples.data_samples_2018

    #samples = [s for s in samples if s.has_dataset(dataset)]
    set_splitting(samples, dataset, 'minitree', data_json=json_path('ana_2017p8.json'))

    cs = CondorSubmitter('ByRunPerVertex' + version,
                         ex = year,
                         dataset = dataset,
                         )
    cs.submit_all(samples)
