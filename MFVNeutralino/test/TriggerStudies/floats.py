import sys
from JMTucker.Tools.BasicAnalyzer_cfg import *
from JMTucker.Tools.MiniAOD_cfg import which_global_tag

is_mc = True

process.source.fileNames = ['/store/mc/RunIIFall15MiniAODv2/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/40000/E4574C7F-EACB-E511-817A-001E67DDC119.root']
process.source.fileNames = ['/store/data/Run2015C_25ns/JetHT/MINIAOD/16Dec2015-v1/20000/1C42421A-49B5-E511-B76E-0CC47A4D7666.root']
process.source.fileNames = ['/store/data/Run2015D/JetHT/MINIAOD/16Dec2015-v1/50001/9E62C986-A9AA-E511-BB43-0CC47A4D9A10.root']
process.source.fileNames = ['/store/mc/RunIIFall15MiniAODv2/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/10000/C6CD95B8-45B9-E511-A12B-141877411FED.root']

process.source.fileNames = ['/store/data/Run2016H/JetHT/MINIAOD/PromptReco-v3/000/284/044/00000/BE5F4C22-D29F-E611-AEAA-02163E011C32.root']

process.maxEvents.input = 100
process.TFileService.fileName = 'triggerfloats.root'

global_tag(process, which_global_tag(is_mc))

process.mfvTriggerFloats = cms.EDProducer('MFVTriggerFloats',
                                          l1_results_src = cms.InputTag('gtStage2Digis'),
                                          trigger_results_src = cms.InputTag('TriggerResults', '', 'HLT'),
                                          trigger_objects_src = cms.InputTag('selectedPatTrigger'),
                                          prints = cms.untracked.bool(False),
                                          tree = cms.untracked.bool(True),
                                          )
process.p = cms.Path(process.mfvTriggerFloats)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    import JMTucker.Tools.Samples as Samples 
    samples = Samples.data_samples
    for sample in samples:
        sample.lumis_per = 50
        sample.json = '../ana_2015p6.json'

    def pset_modifier(sample):
        to_add = []
        to_replace = []

        if not sample.is_mc:
            magic = 'is_mcX=XTrue'.replace('X', ' ')
            err = 'trying to submit on data, and tuple template does not contain the magic string "%s"' % magic
            to_replace.append((magic, 'is_mc = False', err))

        return to_add, to_replace

    from JMTucker.Tools.CRAB3Submitter import CRABSubmitter
    cs = CRABSubmitter('TriggerFloats_16',
                       pset_modifier = pset_modifier,
                       job_control_from_sample = True,
                       dataset = 'miniaod',
                       )
    cs.submit_all(samples)
