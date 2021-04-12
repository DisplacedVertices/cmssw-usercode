import FWCore.ParameterSet.Config as cms

mfvINscore = cms.EDProducer('INoutputProducer',
                            #graphPath=cms.string("/uscms/home/ali/nobackup/LLP/ML/IN_jets/constantgraph.pb"),
                            graphPath=cms.string("/uscms/home/ali/nobackup/LLP/ML/IN_jets/savedModel"),
                            mevent_src = cms.InputTag('mfvEvent'),
                            njets = cms.int32(10),
                           )
