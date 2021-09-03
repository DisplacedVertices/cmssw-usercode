import sys
from DVCode.Tools.BasicAnalyzer_cfg import *
from DVCode.Tools.Year import year

cmssw_settings = CMSSWSettings()
cmssw_settings.is_mc = True

#tfileservice(process, 'triggerfloats.root')
global_tag(process, which_global_tag(cmssw_settings))
want_summary(process)
max_events(process, -1)
input_files(process, {
    (2017,True): '/uscmst1b_scratch/lpc1/3DayLifetime/tucker/itch/store/mc/RunIIFall17MiniAOD/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/94X_mc2017_realistic_v10-v1/20000/FA596B3F-C303-E811-B69C-20CF3027A6DC.root',
    (2017,False):'/uscmst1b_scratch/lpc1/3DayLifetime/tucker/itch/store/data/Run2017F/SingleMuon/MINIAOD/17Nov2017-v1/70001/DC73F8F1-A5EA-E711-A5F3-141877410B4D.root',
    (2018,True): '/uscmst1b_scratch/lpc1/3DayLifetime/tucker/itch/store/mc/RunIIFall18MiniAOD/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/102X_upgrade2018_realistic_v12-v1/270000/DD8D39DE-C4B3-D241-99CC-79AF11E2EDE9.root',
    #(2018,False):'/uscmst1b_scratch/lpc1/3DayLifetime/tucker/itch/store/data/Run2018D/SingleMuon/MINIAOD/PromptReco-v2/000/321/457/00000/4402D66D-E0A5-E811-8A35-FA163EBDCF4F.root',
    (2018,False):'/uscmst1b_scratch/lpc1/3DayLifetime/tucker/itch/store/data/Run2018A/SingleMuon/MINIAOD/06Jun2018-v1/40000/60A09696-AD76-E811-BA6E-E0071B6CAD20.root',
    }[(year, cmssw_settings.is_mc)])

process.load('DVCode.MFVNeutralino.TriggerFilter_cfi')
process.load('DVCode.MFVNeutralino.TriggerFloats_cff')

process.load('DVCode.Tools.UpdatedJets_cff')
process.mfvTriggerFloats.jets_src = 'updatedJetsMiniAOD'
process.mfvTriggerFloats.prints = 1

process.p = cms.Path(process.mfvTriggerFilterJetsOnly * process.mfvTriggerFloats)


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    import DVCode.Tools.Samples as Samples 
    from DVCode.Tools.MetaSubmitter import *

    if year == 2017:
        samples = Samples.data_samples_2017
    elif year == 2018:
        samples = Samples.data_samples_2018

    dataset = 'miniaod'
    set_splitting(samples, dataset, 'default', json_path('ana_2017p8.json'), 50)

    cs = CRABSubmitter('TriggerFloats2017p8',
                       pset_modifier = is_mc_modifier,
                       job_control_from_sample = True,
                       dataset = 'miniaod',
                       )
    cs.submit_all(samples)
