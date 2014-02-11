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

cuts = ''
#cuts = 'looser'
#cuts = 'tightest'

if cuts == 'looser':
    process.mfvAnalysisCuts.min_sumht = 500
    process.mfvSelectedVerticesTight.min_bs2dsig = 5
    process.mfvSelectedVerticesTight.min_ntracksptgt3 = 1
elif cuts == 'tightest':
    process.mfvAnalysisCuts.min_ntracks01 = 17
    process.mfvAnalysisCuts.min_maxtrackpt01 = 30

for name, cut in nm1s:
    vtx = eval('process.mfvSelectedVerticesTight.clone(%s)' % cut)
    vtx_name = 'vtxNo' + name
    ana = process.mfvAnalysisCuts.clone(vertex_src = vtx_name)
    ana_name = 'anaNo' + name
    hst = process.mfvVertexHistos.clone(vertex_aux_src = vtx_name)
    hst_name = 'hstNo' + name
    setattr(process, vtx_name, vtx)
    setattr(process, ana_name, ana)
    setattr(process, hst_name, hst)
    setattr(process, 'p' + name, cms.Path(vtx * ana * hst))

hackrundata = False # JMTBAD
if hackrundata:
    from FWCore.PythonUtilities.LumiList import LumiList
    l = LumiList('ana.json').getCMSSWString().split(',')
    process.source.lumisToProcess = cms.untracked.VLuminosityBlockRange(*l)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    import JMTucker.Tools.Samples as Samples
    samples = Samples.ttbar_samples + Samples.qcd_samples + Samples.leptonic_background_samples
    samples += [Samples.mfv_neutralino_tau0100um_M0400, Samples.mfv_neutralino_tau1000um_M0400, Samples.mfv_neutralino_tau9900um_M0400]

    samples = Samples.ttbar_samples + Samples.qcd_samples + Samples.leptonic_background_samples + Samples.smaller_background_samples + Samples.mfv_signal_samples

    samples = [
        Samples.TupleOnlyMCSample('dp_200_50_tau20to2000_1', '/HTo2LongLivedTo4F_MH-200_MFF-50_CTau20To2000_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM', 500),
        Samples.TupleOnlyMCSample('dp_400_50_tau8to800_1', '/HTo2LongLivedTo4F_MH-400_MFF-50_CTau8To800_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM', 500),
        Samples.TupleOnlyMCSample('dp_400_150_tau40to4000_1', '/HTo2LongLivedTo4F_MH-400_MFF-150_CTau40To4000_8TeV-pythia6/Summer12_DR53X-DEBUG_PU_S10_START53_V7A-v2/AODSIM', 500),
        Samples.TupleOnlyMCSample('dp_1000_150_tau10to1000_1', '/HTo2LongLivedTo4F_MH-1000_MFF-150_CTau10To1000_8TeV-pythia6/Summer12_DR53X-DEBUG_PU_S10_START53_V7A-v2/AODSIM', 500),
        Samples.TupleOnlyMCSample('dp_1000_350_tau35to3500_1', '/HTo2LongLivedTo4F_MH-1000_MFF-350_CTau35To3500_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM', 500),
        Samples.TupleOnlyMCSample('dp_200_50_tau20to2000_2', '/HTo2LongLivedTo4F_MH-200_MFF-50_CTau20To2000_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM', 500),
        Samples.TupleOnlyMCSample('dp_400_50_tau8to800_2', '/HTo2LongLivedTo4F_MH-400_MFF-50_CTau8To800_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM', 500),
        Samples.TupleOnlyMCSample('dp_400_150_tau40to4000_2', '/HTo2LongLivedTo4F_MH-400_MFF-150_CTau40To4000_8TeV-pythia6/Summer12_DR53X-DEBUG_PU_S10_START53_V7A-v2/AODSIM', 500),
        Samples.TupleOnlyMCSample('dp_1000_150_tau10to1000_2', '/HTo2LongLivedTo4F_MH-1000_MFF-150_CTau10To1000_8TeV-pythia6/Summer12_DR53X-DEBUG_PU_S10_START53_V7A-v2/AODSIM', 500),
        Samples.TupleOnlyMCSample('dp_1000_350_tau35to3500_2', '/HTo2LongLivedTo4F_MH-1000_MFF-350_CTau35To3500_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM', 500),
        Samples.TupleOnlyMCSample('dp_200_50_tau20to2000_3', '/HTo2LongLivedTo4F_MH-200_MFF-50_CTau20To2000_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM', 500),
        Samples.TupleOnlyMCSample('dp_400_50_tau8to800_3', '/HTo2LongLivedTo4F_MH-400_MFF-50_CTau8To800_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM', 500),
        Samples.TupleOnlyMCSample('dp_400_150_tau40to4000_3', '/HTo2LongLivedTo4F_MH-400_MFF-150_CTau40To4000_8TeV-pythia6/Summer12_DR53X-DEBUG_PU_S10_START53_V7A-v2/AODSIM', 500),
        Samples.TupleOnlyMCSample('dp_1000_150_tau10to1000_3', '/HTo2LongLivedTo4F_MH-1000_MFF-150_CTau10To1000_8TeV-pythia6/Summer12_DR53X-DEBUG_PU_S10_START53_V7A-v2/AODSIM', 500),
        Samples.TupleOnlyMCSample('dp_1000_350_tau35to3500_3', '/HTo2LongLivedTo4F_MH-1000_MFF-350_CTau35To3500_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM', 500),
        ]
    
    from JMTucker.Tools.CRABSubmitter import CRABSubmitter
    from JMTucker.Tools.SampleFiles import SampleFiles

    if cuts != '':
        cuts = '_' + cuts
    cs = CRABSubmitter('MFVHistosV15' + cuts,
                       total_number_of_events = -1,
                       events_per_job = 200000,
                       manual_datasets = SampleFiles['MFVNtupleV15'],
                       )

    if not hackrundata:
        cs.submit_all(samples)
    else:
        cs.submit_all([Samples.MultiJetPk2012B])
