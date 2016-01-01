import FWCore.ParameterSet.Config as cms

def setup_trigger_filter_soup(process, path_name='pevtsel', filt_name='triggerFilter'):
    from HLTrigger.HLTfilters.hltHighLevel_cfi import hltHighLevel
    triggerFilter = hltHighLevel.clone()
    setattr(process, filt_name, triggerFilter)
    triggerFilter.HLTPaths = [
        'HLT_PFHT650_v*',
        'HLT_PFHT800_v*',
        'HLT_PFHT900_v*',
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
    triggerFilter.andOr = True # = OR
    triggerFilter.throw = False # = HT800 not in MC
    setattr(process, path_name, cms.Path(triggerFilter))
    if hasattr(process, 'out'):
        process.out.SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring(path_name))

def setup_trigger_filter(process, path_name='pevtsel', filt_name='emuht800', need_pat=False):
    from JMTucker.MFVNeutralino.EmulateHT800_cfi import emu
    emu = emu.clone()
    setattr(process, filt_name, emu)
    path = cms.Path(emu)
    setattr(process, path_name, path)

    if need_pat:
        process.load('PhysicsTools.PatAlgos.triggerLayer1.triggerProducer_cfi')
        process.load('PhysicsTools.PatAlgos.slimming.selectedPatTrigger_cfi')
        path.insert(0, process.patTrigger * process.selectedPatTrigger)

    if hasattr(process, 'out'):
        process.out.SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring(path_name))
