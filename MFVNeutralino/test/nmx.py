import os, sys
from itertools import *
from DVCode.Tools.BasicAnalyzer_cfg import cms, process

process.source.fileNames = ['/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20/aaaa7d7d2dcfa08aa71c1469df6ebf05/ntuple_1_1_NQ9.root']
process.TFileService.fileName = 'nmx.root'

cuts = {
    'A': 'min_ntracks = 5',
    'B': 'max_drmin = 0.4',
    'C': 'max_drmax = 4',
    'D': 'min_drmax = 1.2',
    'E': 'max_geo2ddist = 2.5',
    'F': 'max_bs2derr = 0.0025',
    'G': 'min_njetsntks = 1',
    'H': 'min_ntracksptgt3 = 3',
    #'I': 'max_sumnhitsbehind = 0',
    }

all_cuts = ''.join(sorted(cuts.keys()))

process.load('DVCode.MFVNeutralino.AnalysisCuts_cfi')
process.ana = process.mfvAnalysisCuts.clone(apply_vertex_cuts = False)

process.load('DVCode.MFVNeutralino.VertexSelector_cfi')
vtx_sel = process.mfvSelectedVertices

process.p = cms.Path(process.ana)

process.load('DVCode.MFVNeutralino.WeightProducer_cfi')
process.p *= process.mfvWeight

vtx_srcs = []

for i in xrange(len(cuts)+1):
    for cut_combs in combinations(all_cuts, i):
        name = ''.join(cut_combs)
        if name == '':
            name = 'none'
        cut = ', '.join(cuts[x] for x in cut_combs)
        obj = eval('vtx_sel.clone(vertex_src = "%s", %s)' % (name, cut))
        print name, cut
        setattr(process, name, obj)
        process.p *= obj
        vtx_srcs.append(cms.InputTag(name))

process.nmx = cms.EDAnalyzer('NmxHistos',
                             weight_src = cms.InputTag('mfvWeight'),
                             use_weight = cms.bool(False),
                             vertex_srcs = cms.VInputTag(*vtx_srcs),
                             )

process.p *= process.nmx

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    import DVCode.Tools.Samples as Samples
    samples = Samples.from_argv([Samples.mfv_neutralino_tau0100um_M0400,
                                 Samples.mfv_neutralino_tau1000um_M0400,
                                 Samples.mfv_neutralino_tau0300um_M0400,
                                 Samples.mfv_neutralino_tau9900um_M0400] + Samples.ttbar_samples + Samples.qcd_samples + Samples.data_samples)

    for s in Samples.data_samples:
        s.json = 'ana_all.json'

    from DVCode.Tools.CRABSubmitter import CRABSubmitter
    cs = CRABSubmitter('NmxV20',
                       job_control_from_sample = True,
                       use_ana_dataset = True,
                       )
    cs.submit_all(samples)

