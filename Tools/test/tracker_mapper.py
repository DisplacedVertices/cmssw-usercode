import os, sys
from JMTucker.Tools.BasicAnalyzer_cfg import cms, process

process.source.fileNames = ['/store/mc/RunIIFall15DR76/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/AODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/00000/0078199A-3FC1-E511-86E1-001E6739801B.root']
process.TFileService.fileName = 'tracker_mapper.root'

from HLTrigger.HLTfilters.hltHighLevel_cfi import hltHighLevel
process.triggerFilter = hltHighLevel.clone()
process.triggerFilter.HLTPaths = ['HLT_PFHT800_v*']
process.triggerFilter.andOr = True # = OR

process.TrackerMapper = cms.EDAnalyzer('TrackerMapper',
                                       track_src = cms.InputTag('generalTracks'),
                                       beamspot_src = cms.InputTag('offlineBeamSpot'),
                                       primary_vertex_src = cms.InputTag('offlinePrimaryVertices'),
                                       pileup_weights = cms.vdouble(0.4430900689834877, 0.7774946230174374, 1.211532146615326, 1.5555095481485082, 1.3656299694579321, 1.9513380206283242, 1.4311409855780286, 1.2555573073998676, 1.3509572272968273, 1.3430021765269047, 1.2671533450149761, 1.1830775671347276, 1.0767805180896135, 0.9110431461207203, 0.6971726104245397, 0.48543658081115554, 0.32209366814732293, 0.22848641867558733, 0.19027360131827362, 0.15527725489164057, 0.09487219082044276, 0.04095796584834362, 0.013672759117602781, 0.003987335129679708, 0.0011389782126837726, 0.00033784224878244623, 0.00010191256127555789, 2.9928259966798484e-05, 8.357594204838038e-06, 2.2051905560049044e-06, 5.493198439639333e-07, 1.2915574040259908e-07, 2.8638852677561204e-08, 5.978815170388724e-09, 1.1718664799704302e-09, 2.147556635829967e-10, 3.658973660525496e-11, 5.759196292572524e-12, 8.200005561089732e-13, 1.0437472148786202e-13),
                                       )

process.p = cms.Path(process.triggerFilter * process.TrackerMapper)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    import JMTucker.Tools.Samples as Samples

    for s in Samples.ttbar_samples + Samples.qcd_samples:
        s.events_per = 500000
    for s in Samples.data_samples:
        s.json = '../../MFVNeutralino/test/ana_all.json'

    from JMTucker.Tools.CRABSubmitter import CRABSubmitter
    cs = CRABSubmitter('TrackerMapper',
                       job_control_from_sample = True,
                       )
    cs.submit_all(Samples.ttbar_samples + Samples.qcd_samples + Samples.data_samples)
