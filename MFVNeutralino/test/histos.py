import sys
from JMTucker.Tools.BasicAnalyzer_cfg import cms, process
from JMTucker.Tools import SampleFiles

SampleFiles.setup(process, 'MFVNtupleV15', 'qcdht1000', 200000)
process.TFileService.fileName = 'histos.root'

process.load('JMTucker.MFVNeutralino.VertexSelector_cfi')
process.load('JMTucker.MFVNeutralino.Histos_cff')

process.p = cms.Path(process.mfvSelectedVerticesSeq * process.mfvHistos)

nm1s = [
    ('Ntracks', 'min_ntracks = 0'),
    ('Drmin',   'max_drmin = 1e9'),
    ('Drmax',   'max_drmax = 1e9'),
    ('Bs2derr', 'max_bs2derr = 1e9'),
    ('Njets',   'min_njetsntks = 0'),
    ('Bs2dsig', 'min_bs2dsig = 0'),
    ('Ntracksptgt3', 'min_ntracksptgt3 = 0'),
    ]

for name, cut in nm1s:
    vtx = eval('process.mfvSelectedVerticesTight.clone(%s)' % cut)
    vtx_name = 'vtxNo' + name
    hst = process.mfvVertexHistos.clone(vertex_aux_src = vtx_name)
    hst_name = 'hstNo' + name
    setattr(process, vtx_name, vtx)
    setattr(process, hst_name, hst)
    process.p *= vtx * hst

nosigorptgt3 = False
if nosigorptgt3:
    process.mfvSelectedVerticesTight.min_bs2dsig = 0
    process.mfvSelectedVerticesTight.min_ntracksptgt3 = 0

hackrundata = False # JMTBAD
if hackrundata:
    from FWCore.PythonUtilities.LumiList import LumiList
    l = LumiList('ana.json').getCMSSWString().split(',')
    process.source.lumisToProcess = cms.untracked.VLuminosityBlockRange(*l)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    import JMTucker.Tools.Samples as Samples
    samples = Samples.ttbar_samples + Samples.qcd_samples + Samples.leptonic_background_samples
    samples += [Samples.mfv_neutralino_tau0100um_M0400, Samples.mfv_neutralino_tau1000um_M0400, Samples.mfv_neutralino_tau9900um_M0400]

    samples = Samples.ttbar_samples + Samples.qcd_samples + Samples.leptonic_background_samples + Samples.smaller_background_samples + \
              [sample for sample in Samples.mfv_signal_samples if '0300' not in sample.name]
    
    from JMTucker.Tools.CRABSubmitter import CRABSubmitter
    from JMTucker.Tools.SampleFiles import SampleFiles

    subname = '_nosigorptgt3' if nosigorptgt3 else ''
    cs = CRABSubmitter('MFVHistosV15' + subname,
                       total_number_of_events = -1,
                       events_per_job = 200000,
                       manual_datasets = SampleFiles['MFVNtupleV15'],
                       )

    if not hackrundata:
        cs.submit_all(samples)
    else:
        cs.submit_all([Samples.MultiJetPk2012B])
