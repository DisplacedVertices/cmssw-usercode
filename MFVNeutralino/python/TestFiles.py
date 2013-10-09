import sys, FWCore.ParameterSet.Config as cms

tau1000M0400 = ['/store/user/jchu/mfv_neutralino_tau1000um_M0400/jtuple_v7/5d4c2a74c85834550d3f9609274e8548/pat_1_1_hdB.root']
tau1000M0400_sec = cms.untracked.vstring(
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_891_1_sZ9.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_948_2_lgB.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_1185_1_JKO.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_1198_1_miF.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_1202_1_6Rq.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_1330_1_emA.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_842_1_2Hs.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_180_1_X9e.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_425_2_ZeH.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_426_3_7Ql.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_645_2_WPD.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_1368_1_0Cu.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_1372_1_Rce.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_1840_1_OPG.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_1847_1_ceP.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_1981_1_9Va.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_1983_1_QCo.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_574_1_GvQ.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_579_1_Y9Z.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_614_1_Qgx.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_707_1_GYJ.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_717_1_IO1.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_1946_1_YCr.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_107_2_9uk.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_847_2_MbS.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_1930_1_i4a.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_1933_1_C1w.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_42_2_0A8.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_46_2_Ceq.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_53_1_yFF.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_772_1_NOh.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_773_1_jbZ.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_774_1_cKg.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_782_1_RDa.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_1838_1_sTl.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_1842_1_YG6.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_780_4_4jN.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_1751_3_Mid.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_2000_1_THr.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_179_2_WvC.root'
    )

qcdht1000 = ['/store/user/jchu/QCD_HT-1000ToInf_TuneZ2star_8TeV-madgraph-pythia6/jtuple_v7/fe6d9f80f9c0fe06cc80b089617fa99d/pat_1_1_NOT.root']
qcdht1000_sec = cms.untracked.vstring(
    '/store/mc/Summer12_DR53X/QCD_HT-1000ToInf_TuneZ2star_8TeV-madgraph-pythia6/AODSIM/PU_S10_START53_V7A-v1/00000/0038E6D2-860D-E211-9211-00266CFACC38.root',
    '/store/mc/Summer12_DR53X/QCD_HT-1000ToInf_TuneZ2star_8TeV-madgraph-pythia6/AODSIM/PU_S10_START53_V7A-v1/00000/D4C0816B-870D-E211-B094-00266CF258D8.root',
    '/store/mc/Summer12_DR53X/QCD_HT-1000ToInf_TuneZ2star_8TeV-madgraph-pythia6/AODSIM/PU_S10_START53_V7A-v1/00000/A2CEDDF1-870D-E211-A98D-00266CF258D8.root',
    '/store/mc/Summer12_DR53X/QCD_HT-1000ToInf_TuneZ2star_8TeV-madgraph-pythia6/AODSIM/PU_S10_START53_V7A-v1/00000/9E8E388F-970D-E211-8D78-848F69FD298E.root'
    )

ttbarhadronic = ['/store/user/jchu/TTJets_HadronicMGDecays_8TeV-madgraph/jtuple_v7/fe6d9f80f9c0fe06cc80b089617fa99d/pat_1_1_HLq.root']
ttbarhadronic_sec = cms.untracked.vstring(
    '/store/mc/Summer12_DR53X/TTJets_HadronicMGDecays_8TeV-madgraph/AODSIM/PU_S10_START53_V7A-v1/00001/BCE41FBC-BE17-E211-9679-00259073E3FC.root',
    '/store/mc/Summer12_DR53X/TTJets_HadronicMGDecays_8TeV-madgraph/AODSIM/PU_S10_START53_V7A-v1/00001/562EF878-5017-E211-976D-E0CB4E5536A7.root'
    )

def set_test_files(process):
    if 'testqcd' in sys.argv:
        process.source.fileNames = qcdht1000
        process.source.secondaryFileNames = qcdht1000_sec
    elif 'testttbar' in sys.argv:
        process.source.fileNames = ttbarhadronic
        process.source.secondaryFileNames = ttbarhadronic_sec
    else:
        process.source.fileNames = tau1000M0400
        process.source.secondaryFileNames = tau1000M0400_sec
