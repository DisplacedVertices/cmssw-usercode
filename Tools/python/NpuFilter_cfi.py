import FWCore.ParameterSet.Config as cms

jmtNpuFilter = cms.EDFilter('JMTNpuFilter',
                            pileup_info_src = cms.InputTag('addPileupInfo'),
                            min_npu = cms.double(-1e99),
                            max_npu = cms.double(1e99),
                            )

jmtNpuFilterMiniAOD = jmtNpuFilter.clone(pileup_info_src = 'slimmedAddPileupInfo')
