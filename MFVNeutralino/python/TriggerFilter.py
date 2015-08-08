import FWCore.ParameterSet.Config as cms

def setup_trigger_filter(process, path_name='pevtsel'):
    from HLTrigger.HLTfilters.hltHighLevel_cfi import hltHighLevel
    process.triggerFilter = hltHighLevel.clone()
    process.triggerFilter.HLTPaths = [
        'HLT_PFHT650_v*',
        'HLT_PFHT550_4Jet_v*',
        'HLT_PFHT450_SixJet40_PFBTagCSV_v*',
        'HLT_PFHT400_SixJet30_BTagCSV0p5_2PFBTagCSV_v*',
        'HLT_PFHT450_SixJet40_v*',
        'HLT_PFHT400_SixJet30_v*',
        'HLT_QuadJet45_TripleCSV0p5_v*',
        'HLT_QuadJet45_DoubleCSV0p5_v*',
        'HLT_DoubleJet90_Double30_TripleCSV0p5_v*',
        'HLT_DoubleJet90_Double30_DoubleCSV0p5_v*',
        'HLT_HT650_DisplacedDijet80_Inclusive_v*',
        'HLT_HT750_DisplacedDijet80_Inclusive_v*',
        'HLT_HT500_DisplacedDijet40_Inclusive_v*',
        'HLT_HT550_DisplacedDijet40_Inclusive_v*',
        'HLT_HT350_DisplacedDijet40_DisplacedTrack_v*',
        'HLT_HT350_DisplacedDijet80_DisplacedTrack_v*',
        'HLT_HT350_DisplacedDijet80_Tight_DisplacedTrack_v*',
        ]
    process.triggerFilter.andOr = True # = OR
    setattr(process, path_name, cms.Path(process.triggerFilter))
    if hasattr(process, 'out'):
        process.out.SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring(path_name))
