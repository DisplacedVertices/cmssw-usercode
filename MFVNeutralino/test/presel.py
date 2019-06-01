from JMTucker.MFVNeutralino.NtupleCommon import *

settings = NtupleSettings()
settings.is_mc = True
settings.is_miniaod = True

process = ntuple_process(settings)
tfileservice(process, 'presel.root')
del process.out
del process.outp
del process.p

dataset = 'miniaod' if settings.is_miniaod else 'main'
sample_files(process, 'qcdht2000_2017' if settings.is_mc else 'JetHT2017F', dataset, 1)
cmssw_from_argv(process)

process.load('JMTucker.MFVNeutralino.WeightProducer_cfi')
process.load('JMTucker.MFVNeutralino.AnalysisCuts_cfi')
process.load('JMTucker.MFVNeutralino.EventHistos_cfi')
process.load('JMTucker.MFVNeutralino.ByX_cfi')

process.mfvEvent.vertex_seed_tracks_src = cms.InputTag('mfvVertexTracks', 'seed')
process.mfvWeight.throw_if_no_mcstat = False

process.mfvAnalysisCutsJet    = process.mfvAnalysisCuts.clone(apply_vertex_cuts = False)
process.mfvAnalysisCutsLepton = process.mfvAnalysisCuts.clone(apply_vertex_cuts = False, apply_presel = 2)

process.preSeq = cms.Sequence(process.goodOfflinePrimaryVertices *
                              process.updatedJetsSeqMiniAOD *
                              process.selectedPatJets *
                              process.selectedPatMuons *
                              process.selectedPatElectrons *
                              process.mfvTriggerFloats *
                              process.mfvGenParticles *
                              process.jmtUnpackedCandidateTracks *
                              process.jmtRescaledTracks *
                              process.mfvVertexTracks *
                              process.prefiringweight *
                              process.mfvEvent *
                              process.mfvWeight)

def doit(name):
    obj = getattr(process, name)
    setattr(process, '%sJetTriggered'    % name, obj.clone())
    setattr(process, '%sJetPreSel'       % name, obj.clone())
    setattr(process, '%sLeptonTriggered' % name, obj.clone())
    setattr(process, '%sLeptonPreSel'    % name, obj.clone())
    setattr(process, 'p%sJet' % name, cms.Path(process.mfvTriggerFilterJetsOnly    * process.preSeq * getattr(process, '%sJetTriggered'    % name) * process.mfvAnalysisCutsJet    * getattr(process, '%sJetPreSel'    % name)))
    setattr(process, 'p%sLep' % name, cms.Path(process.mfvTriggerFilterLeptonsOnly * process.preSeq * getattr(process, '%sLeptonTriggered' % name) * process.mfvAnalysisCutsLepton * getattr(process, '%sLeptonPreSel' % name)))

doit('mfvEventHistos')
if not settings.is_mc:
    doit('mfvByRun')


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.MetaSubmitter import *

    samples = pick_samples(dataset, all_signal=False)
    set_splitting(samples, dataset, 'ntuple', data_json=json_path('ana_2017p8.json'), limit_ttbar=True)

    ms = MetaSubmitter('PreselHistos' + settings.version, dataset=dataset)
    ms.common.pset_modifier = chain_modifiers(is_mc_modifier, era_modifier, per_sample_pileup_weights_modifier())
    ms.condor.stageout_files = 'all'
    ms.submit(samples)
