import os, sys
from JMTucker.Tools.BasicAnalyzer_cfg import cms, process

process.source.fileNames = ['/store/mc/Summer12_DR53X/TTJets_HadronicMGDecays_8TeV-madgraph/AODSIM/PU_S10_START53_V7A-v1/00000/002A756C-FA15-E211-9FA6-485B39800B75.root']
process.TFileService.fileName = 'tracker_mapper.root'

from HLTrigger.HLTfilters.hltHighLevel_cfi import hltHighLevel
process.triggerFilter = hltHighLevel.clone()
process.triggerFilter.HLTPaths = ['HLT_QuadJet50_v*']
process.triggerFilter.andOr = True # = OR

process.TrackerMapper = cms.EDAnalyzer('TrackerMapper',
                                       track_src = cms.InputTag('generalTracks'),
                                       beamspot_src = cms.InputTag('offlineBeamSpot'),
                                       primary_vertex_src = cms.InputTag('offlinePrimaryVertices'),
                                       pileup_weights = cms.vdouble(0.30249552182308997, 0.65359274010367707, 7.6502895268202904, 0.16943388206921614, 0.14660360387319543, 0.72425867161687918, 0.55155999738229444, 0.54806416920939871, 0.7454646466080318, 1.0706380035560332, 1.4535826899955075, 1.7428350826171437, 1.7173327052480303, 1.4997486977220611, 1.2674916780217131, 1.1006648727380504, 1.0177568207992902, 0.99570087383433104, 1.0217479778330991, 1.0727808651375432, 1.119232994074125, 1.1544093975704233, 1.1798535741641614, 1.1925027049862622, 1.1870235128100819, 1.1473107003277687, 1.0813875063899978, 0.9903171658643829, 0.88460484407781392, 0.761882278559328, 0.63908238702217468, 0.520019143691136, 0.4111564625168076, 0.31425730636402721, 0.23366701625388003, 0.16912685350548012, 0.12076196114421867, 0.086827535170015402, 0.065533776822654446, 0.053606580014003126, 0.048363977043935261, 0.048858878953777433, 0.052680995414911967, 0.059950209794645791, 0.06956224840691605, 0.081535086413525651, 0.095672616825258044, 0.11248771352363893, 0.13839976681824853, 0.16508646294078161, 0.19766567530745904, 0.2405017332616616, 0.28954354638717633, 0.36074164376918039, 0.43096815865746924, 0.5120812783478047, 0.6625045180182213, 0.75950777570844552, 0.927524022062575, 2.3453791559829837),
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
