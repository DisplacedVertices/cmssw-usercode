import sys
from JMTucker.Tools.BasicAnalyzer_cfg import cms, process, geometry_etc
from JMTucker.Tools import SampleFiles

SampleFiles.setup(process, 'MFVNtupleV15', 'mfv_neutralino_tau1000um_M0400', 10000)
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
    ]

if False:
    geometry_etc(process, 'START53_V27::All')
    SampleFiles.setup(process, 'MFVNtupleV15WMore', 'ttbarhadronic', 500)
    process.mfvVertexHistosOneVtx.vertex_src = 'mfvVertices'
    nm1s = []

for name, cut in nm1s:
    vtx = eval('process.mfvSelectedVerticesTight.clone(%s)' % cut)
    vtx_name = 'vtxNo' + name
    ana = process.mfvAnalysisCuts.clone(vertex_src = vtx_name)
    ana_name = 'anaNo' + name
    evt_hst = process.mfvEventHistos.clone()
    evt_hst_name = 'evtHstNo' + name
    vtx_hst = process.mfvVertexHistos.clone(vertex_aux_src = vtx_name)
    vtx_hst_name = 'vtxHstNo' + name
    setattr(process, vtx_name, vtx)
    setattr(process, ana_name, ana)
    setattr(process, evt_hst_name, evt_hst)
    setattr(process, vtx_hst_name, vtx_hst)
    setattr(process, 'p' + name, cms.Path(vtx * ana * evt_hst * vtx_hst))

hackrundata = False # JMTBAD
if hackrundata:
    from FWCore.PythonUtilities.LumiList import LumiList
    l = LumiList('ana.json').getCMSSWString().split(',')
    process.source.lumisToProcess = cms.untracked.VLuminosityBlockRange(*l)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    import JMTucker.Tools.Samples as Samples
    #samples = Samples.ttbar_samples + Samples.qcd_samples + Samples.leptonic_background_samples + Samples.smaller_background_samples + Samples.mfv_signal_samples
    bkg_samples = Samples.ttbar_samples + Samples.qcd_samples
    samples = [Samples.mfv_neutralino_tau0100um_M0400, Samples.mfv_neutralino_tau1000um_M0400, Samples.mfv_neutralino_tau9900um_M0400] + bkg_samples
    if 'full' not in sys.argv:
        for sample in bkg_samples:
            sample.total_events = int(sample.nevents_orig/2 * sample.ana_filter_eff)

    from JMTucker.Tools.CRABSubmitter import CRABSubmitter
    from JMTucker.Tools.SampleFiles import SampleFiles

    cs = CRABSubmitter('MFVHistosV15',
                       job_control_from_sample = True,
                       use_ana_dataset = True,
                       manual_datasets = SampleFiles['MFVNtupleV15'],
                       )

    if 'two' in sys.argv:
        samples = [Samples.ttbarhadronic, Samples.mfv_neutralino_tau1000um_M0400]

    if not hackrundata:
        cs.submit_all(samples)
    else:
        cs.submit_all([Samples.MultiJetPk2012B])
