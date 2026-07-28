from JMTucker.Tools.BasicAnalyzer_cfg import *
#from JMTucker.MFVNeutralino.NtupleCommon import *

from JMTucker.MFVNeutralino.NtupleCommon import ntuple_version_use as version, dataset, use_BTagDispJet_vetoLepHT_triggers, use_Lepton_triggers
is_mc = False
study_20pc = False

dataset += '_ntkseeds'
#sample_files(process, 'qcdht2000_2017', dataset, 1)
#sample_files(process, 'EGamma_2018A', dataset, 1)
#input_files(process, '/store/group/lpcdisplacedvertices/alecduqu/EGamma/Ntuple_tag001LepElem_NTkSeeds_2018/260630_154342/0000/ntkseeds_0.root') #data electron
input_files(process, '/store/group/lpcdisplacedvertices/alecduqu/SingleMuon/Ntuple_tag001LepMum_NTkSeeds_2018/260611_081143/0000/ntkseeds_0.root') #data Muon
#input_files(process, '/store/group/lpcdisplacedvertices/alecduqu/WJetsToLNu_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8/Ntuple_tag001Lepm_NTkSeeds_2018/260703_160302/0000/ntkseeds_0.root') #MC
#input_files(process, '/store/group/lpcdisplacedvertices/alecduqu/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/Ntuple_tag001BvetoLHTm_NTkSeeds_2017/260429_002902/0000/ntkseeds_0.root') #old working ntuples
process.TFileService.fileName = 'vertexer_pair_effs.root'
cmssw_from_argv(process)

process.load('JMTucker.MFVNeutralino.WeightProducer_cfi')
process.load('JMTucker.MFVNeutralino.AnalysisCuts_cfi')

process.mfvAnalysisCuts.apply_vertex_cuts = False
process.mfvAnalysisCuts.apply_presel = -1 #To acount for lightweight applied to ntuples, presel already applied in ntuple

process.mfvVertexerPairEffs = e = cms.EDAnalyzer('MFVVertexerPairEffs',
                                                 vpeff_src = cms.InputTag('mfvVertices'),
                                                 weight_src = cms.InputTag('mfvWeight'),
                                                 allow_duplicate_pairs = cms.bool(True),
                                                 verbose = cms.untracked.bool(False),
                                                 )

process.mfvVertexerPairEffs3TkSeed = e.clone(vpeff_src = 'mfvVertices3TkSeed')
process.mfvVertexerPairEffs4TkSeed = e.clone(vpeff_src = 'mfvVertices4TkSeed')
process.mfvVertexerPairEffs5TkSeed = e.clone(vpeff_src = 'mfvVertices5TkSeed')

process.p = cms.Path(process.mfvWeight * process.mfvAnalysisCuts * process.mfvVertexerPairEffs * process.mfvVertexerPairEffs3TkSeed * process.mfvVertexerPairEffs4TkSeed * process.mfvVertexerPairEffs5TkSeed)


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.MetaSubmitter import *

    if use_BTagDispJet_vetoLepHT_triggers :
        if is_mc:
            #samples = pick_samples(dataset, qcd=True, ttbar=True, all_signal=False, data=True, bjet=False) # no data currently; no sliced ttbar since inclusive is used
            samples = pick_samples(dataset, all_bjet_signal=True, qcd=True, ttbar=True)
            pset_modifier = chain_modifiers(per_sample_pileup_weights_modifier())
        else:
            #samples = pick_samples(dataset, qcd=True, ttbar=True, all_signal=False, data=True, bjet=False) # no data currently; no sliced ttbar since inclusive is used
            samples = pick_samples(dataset, BTagCSV_data=True, DisplacedJet_data=True)
            pset_modifier = None
    elif use_Lepton_triggers:
        if is_mc :
            samples = pick_samples(dataset, all_lep_signal=True, qcd_lep=True, leptonic=True, ttbar=True, diboson=True)
            pset_modifier = chain_modifiers(is_mc_modifier, per_sample_pileup_weights_modifier(), ttH_duplicate_check_modifier)
        else :
            print dataset
            samples = pick_samples(dataset, Muon_data=True, Electron_data=True)
            pset_modifier = None

    #set_splitting(samples, dataset, 'histos', data_json=json_path('ana_2017p8.json'))

    json_filename = 'ana_run2_displacement_trigger.json' if use_btag_vetoLepHT_triggers else 'ana_run2.json'
    if study_20pc :
        json_filename = json_filename.replace(".json", "_20pc.json")
    print "json file is:", json_filename

    set_splitting(samples, dataset, 'histos', data_json=json_path(json_filename))

    cs = CondorSubmitter('VertexerPairEffs' + version,
                         ex = year,
                         dataset = dataset,
                         pset_modifier = pset_modifier,
                         )
    cs.submit_all(samples)
