import sys
from JMTucker.Tools.BasicAnalyzer_cfg import cms, process, geometry_etc
from JMTucker.Tools import SampleFiles

wmore = False
run_pileup_weights = False

SampleFiles.setup(process, 'MFVNtupleV17', 'mfv_neutralino_tau1000um_M0400', 10000)
process.TFileService.fileName = 'histos.root'

process.load('JMTucker.MFVNeutralino.VertexSelector_cfi')
process.load('JMTucker.MFVNeutralino.Histos_cff')

process.p = cms.Path(process.mfvSelectedVerticesSeq * process.mfvHistos)

nm1s = [
    ('Ntracks', 'min_ntracks = 0'),
    ('Drmin',   'max_drmin = 1e9'),
    ('Drmax',   'max_drmax = 1e9'),
    ('Mindrmax','min_drmax = 0'),
    ('Bs2derr', 'max_bs2derr = 1e9'),
    ('Njets',   'min_njetsntks = 0'),
    ('Bs2dsig', 'min_bs2dsig = 0'),
    ('Ntracksptgt3', 'min_ntracksptgt3 = 0'),
    ('15p0', 'min_drmax = 0, max_sumnhitsbehind = 1000000'),
    ('Dr', 'max_drmin = 1e9, max_drmax = 1e9, min_drmax = 0'),
    ('Bs2d', 'max_bs2derr = 1e9, min_bs2dsig = 0'),
    ('DrOrBs2d', 'max_drmin = 1e9, max_drmax = 1e9, min_drmax = 0, max_bs2derr = 1e9, min_bs2dsig = 0'),
    ('DrOrNjets', 'max_drmin = 1e9, max_drmax = 1e9, min_drmax = 0, min_njetsntks = 0'),
    ('ButNtracksAndGt3', 'max_drmin = 1e9, max_drmax = 1e9, min_drmax = 0, max_bs2derr = 1e9, min_bs2dsig = 0, min_njetsntks = 0'),
    ('ButNtracks', 'max_drmin = 1e9, max_drmax = 1e9, min_drmax = 0, max_bs2derr = 1e9, min_bs2dsig = 0, min_njetsntks = 0, min_ntracksptgt3 = 0'),
    ]

if wmore:
    geometry_etc(process, 'START53_V27::All')
    process.source.fileNames = ['file:/eos/uscms/store/user/jchu/background_V17/ttbarhadronic.root']
    process.mfvSelectedVerticesTight.max_bs2derr = 1e9
    from JMTucker.MFVNeutralino.Vertexer_cff import mfvSelectedVerticesTmp
    process.mfvSelectedVerticesTmp = mfvSelectedVerticesTmp.clone(vertex_aux_src = 'mfvVerticesAux')
    process.load('JMTucker.MFVNeutralino.JetVertexAssociator_cfi')
    process.p.insert(0, process.mfvSelectedVerticesTmp * process.mfvVerticesToJets)
    process.mfvVertexHistos.vertex_src = 'mfvVertices'
    process.mfvVertexHistos.vertex_to_jets_src = cms.InputTag('mfvVerticesToJets','ByNtracks')
    process.load('CommonTools.ParticleFlow.goodOfflinePrimaryVertices_cfi')
    process.goodOfflinePrimaryVertices.filter = cms.bool(True)
    process.p.insert(0, process.goodOfflinePrimaryVertices)
    process.mfvEventHistos.primary_vertex_src = 'goodOfflinePrimaryVertices'
    process.mfvEventHistos.jets_src = 'selectedPatJetsPF'
    nm1s = []

for name, cut in nm1s:
    evt_cut = ''
    if type(cut) == tuple:
        cut, evt_cut = cut

    vtx = eval('process.mfvSelectedVerticesTight.clone(%s)' % cut)
    vtx_name = 'vtxNo' + name

    for nv in (1,2):
        ana = eval('process.mfvAnalysisCuts.clone(%s)' % evt_cut)
        ana.vertex_src = vtx_name
        ana.min_nvertex = nv
        ana_name = 'ana%iVNo' % nv + name

        evt_hst = process.mfvEventHistos.clone()
        evt_hst_name = 'evtHst%iVNo' % nv + name

        vtx_hst = process.mfvVertexHistos.clone(vertex_aux_src = vtx_name)
        vtx_hst_name = 'vtxHst%iVNo' % nv + name

        setattr(process, vtx_name, vtx)
        setattr(process, ana_name, ana)
        setattr(process, evt_hst_name, evt_hst)
        setattr(process, vtx_hst_name, vtx_hst)
        setattr(process, 'p%iV' % nv + name, cms.Path(vtx * ana * evt_hst * vtx_hst))

if 'ttbarhadronic' in sys.argv:
    process.source.fileNames = ['file:/eos/uscms/store/user/jchu/background_V17/ttbarhadronic.root']
    process.TFileService.fileName = 'histos_ttbarhadronic.root'
if 'ttbarsemilep' in sys.argv:
    process.source.fileNames = ['file:/eos/uscms/store/user/jchu/background_V17/ttbarsemilep.root']
    process.TFileService.fileName = 'histos_ttbarsemilep.root'
if 'qcdht0500' in sys.argv:
    process.source.fileNames = ['file:/eos/uscms/store/user/jchu/background_V17/qcdht0500.root']
    process.TFileService.fileName = 'histos_qcdht0500.root'
if 'qcdht1000' in sys.argv:
    process.source.fileNames = ['file:/eos/uscms/store/user/jchu/background_V17/qcdht1000.root']
    process.TFileService.fileName = 'histos_qcdht1000.root'

if run_pileup_weights:
    process.mfvWeight.weight_pileup = False

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    import JMTucker.Tools.Samples as Samples
    bkg_samples = Samples.ttbar_samples + Samples.qcd_samples
    samples = [Samples.mfv_neutralino_tau0100um_M0400, Samples.mfv_neutralino_tau0300um_M0400, Samples.mfv_neutralino_tau1000um_M0400, Samples.mfv_neutralino_tau9900um_M0400] + bkg_samples + Samples.data_samples
    if 'full' not in sys.argv:
        for sample in bkg_samples:
            sample.total_events = int(sample.nevents_orig/2 * sample.ana_filter_eff)

    for s in Samples.data_samples:
        s.json = 'ana_5pc.json'

    from JMTucker.Tools.CRABSubmitter import CRABSubmitter

    def modify(sample):
        to_add = []
        to_replace = []

        if not sample.is_mc:
            to_add.append('process.mfvWeight.weight_pileup = False')

        return to_add, to_replace

    ex = ''
    exn = ''

    if run_pileup_weights:
        exn += '_PileupWeights'
        samples = [Samples.mfv_neutralino_tau1000um_M0400, Samples.qcdht1000] + Samples.data_samples

    cs = CRABSubmitter('MFVHistosV17' + ex + exn,
                       pset_modifier = modify,
                       job_control_from_sample = True,
                       use_ana_dataset = True,
                       manual_datasets = SampleFiles.SampleFiles['MFVNtupleV17' + ex],
                       )

    cs.submit_all(samples)
