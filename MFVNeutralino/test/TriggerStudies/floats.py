import sys
from JMTucker.Tools.BasicAnalyzer_cfg import *
from JMTucker.Tools.Year import year

cmssw_settings = CMSSWSettings()
cmssw_settings.is_mc = False

#tfileservice(process, 'triggerfloats.root')
global_tag(process, which_global_tag(cmssw_settings))
want_summary(process)
max_events(process, -1)
input_files(process, {
    ###(2017,True): '/store/mc/RunIIFall17MiniAODv2/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1/10000/74BD6031-75AA-E811-AF2D-001E67E6F8DC.root',
    (2017,False): '/uscms/home/joeyr/scratch/itch/samples/data/Run2017B/SingleMuon/MINIAOD/31Mar2018-v1/100000/0EF77FEA-6338-E811-ADF8-0025905A48BC.root',
    ##(2018,True): '/uscmst1b_scratch/lpc1/3DayLifetime/tucker/itch/store/mc/RunIIFall18MiniAOD/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/102X_upgrade2018_realistic_v12-v1/270000/DD8D39DE-C4B3-D241-99CC-79AF11E2EDE9.root',
    ###(2018,False):'/uscmst1b_scratch/lpc1/3DayLifetime/tucker/itch/store/data/Run2018D/SingleMuon/MINIAOD/PromptReco-v2/000/321/457/00000/4402D66D-E0A5-E811-8A35-FA163EBDCF4F.root',
    ##(2018,False):'/uscmst1b_scratch/lpc1/3DayLifetime/tucker/itch/store/data/Run2018A/SingleMuon/MINIAOD/06Jun2018-v1/40000/60A09696-AD76-E811-BA6E-E0071B6CAD20.root',
    }[(year, cmssw_settings.is_mc)])

process.load('JMTucker.MFVNeutralino.TriggerFilter_cfi')
process.load('JMTucker.MFVNeutralino.TriggerFloats_cff')

process.load('JMTucker.Tools.UpdatedJets_cff')
process.mfvTriggerFloats.jets_src = 'updatedJetsMiniAOD'
process.mfvTriggerFloats.prints = 1

process.p = cms.Path(process.mfvTriggerFilterJetsOnly * process.mfvTriggerFloats)


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    import JMTucker.Tools.Samples as Samples 
    from JMTucker.Tools.MetaSubmitter import *

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
