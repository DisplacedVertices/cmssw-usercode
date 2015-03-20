import sys
from JMTucker.Tools.BasicAnalyzer_cfg import cms, process

process.source.fileNames = '''/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_10_1_cUZ.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_11_1_g7H.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_12_1_HZL.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_13_1_DBl.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_14_1_ZAk.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_15_1_q8c.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_16_1_WXy.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_17_1_gz0.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_18_1_RSd.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_19_1_RAW.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_1_1_WwV.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_20_1_AJ1.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_21_1_TyW.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_22_1_4dW.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_23_1_kAv.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_24_1_RXW.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_25_1_g97.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_26_1_f0l.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_27_1_968.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_28_1_wAo.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_29_1_Ap2.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_2_1_aSP.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_30_1_Lbq.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_31_1_Kbr.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_32_1_sJO.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_33_1_5jX.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_34_1_yum.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_35_1_kXz.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_36_1_9f7.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_37_1_ZDs.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_38_1_BGe.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_39_1_x69.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_3_1_87r.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_40_1_ipP.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_41_1_qkw.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_42_1_WVb.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_43_1_Y8L.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_44_1_gup.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_45_1_dSN.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_46_1_ezj.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_47_1_A6t.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_48_1_OSp.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_49_1_Dna.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_4_1_oFW.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_50_1_NN6.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_5_1_RSz.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_6_1_JNY.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_7_1_Wuf.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_8_1_9eh.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_9_1_YYJ.root'''.split('\n')

process.source.fileNames = ['/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_1_1_WwV.root']
process.TFileService.fileName = 'resolutions.root'

process.load('JMTucker.MFVNeutralino.VertexSelector_cfi')
process.load('JMTucker.MFVNeutralino.AnalysisCuts_cfi')

mfvResolutions = cms.EDAnalyzer('MFVResolutions',
                                vertex_src = cms.InputTag('mfvSelectedVerticesTight'),
                                mevent_src = cms.InputTag('mfvEvent'),
                                which_mom = cms.int32(0),
                                max_dr = cms.double(-1),
                                max_dist = cms.double(0.012),
                                gen_src = cms.InputTag('genParticles'),
                                gen_jet_src = cms.InputTag('ak5GenJets'),
                                )

process.p = cms.Path(process.mfvSelectedVertices * process.mfvSelectedVerticesSeq)

process.mfvResolutionsNoCutsNoCuts = mfvResolutions.clone(vertex_src = 'mfvSelectedVertices')
process.p *= process.mfvResolutionsNoCutsNoCuts

process.mfvResolutionsTightNoCuts = mfvResolutions.clone()
process.p *= process.mfvResolutionsTightNoCuts


process.mfvAnalysisCutsPreSel = process.mfvAnalysisCuts.clone(apply_vertex_cuts = False)
process.p *= process.mfvAnalysisCutsPreSel

process.mfvResolutionsNoCutsPreSel = mfvResolutions.clone(vertex_src = 'mfvSelectedVertices')
process.p *= process.mfvResolutionsNoCutsPreSel

process.mfvResolutionsTightPreSel = mfvResolutions.clone()
process.p *= process.mfvResolutionsTightPreSel


process.p *= process.mfvAnalysisCuts

process.mfvResolutionsTightFullSel = mfvResolutions.clone()
process.p *= process.mfvResolutionsTightFullSel


nm1s = [
    ('Ntracks', 'min_ntracks = 0, min_njetsntks = 0'),
    ('Ntracksptgt3', 'min_ntracksptgt3 = 0'),
    ('Drmin', 'max_drmin = 1e9'),
    ('Mindrmax', 'min_drmax = 0'),
    ('Drmax', 'max_drmax = 1e9'),
    ('Njets', 'min_njetsntks = 0'),
    ('Bs2derr', 'max_bs2derr = 1e9'),
    ('Geo2ddist', 'max_geo2ddist = 1e9'),
    ('Sumnhitsbehind', 'max_sumnhitsbehind = 1000000'),
    ]

for name, cut in nm1s:
    vtx = eval('process.mfvSelectedVerticesTight.clone(%s)' % cut)
    vtx_name = 'vtxNo' + name

    res_hst = mfvResolutions.clone(vertex_src = vtx_name)
    res_hst_name = 'mfvResolutionsNo%sPreSel' % name

    setattr(process, vtx_name, vtx)
    setattr(process, res_hst_name, res_hst)
    setattr(process, 'p%s' % name, cms.Path(vtx * process.mfvAnalysisCutsPreSel * res_hst))



if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    import JMTucker.Tools.Samples as Samples
    from JMTucker.Tools.CRABSubmitter import CRABSubmitter

    Samples.mfv_neutralino_tau0100um_M0200.ana_dataset_override = '/mfv_neutralino_tau0100um_M0200/tucker-mfvntuple_v20_wgen-4c67a9d5a51f11cf2da50127721f7362/USER'
    Samples.mfv_neutralino_tau0100um_M0300.ana_dataset_override = '/mfv_neutralino_tau0100um_M0300/tucker-mfvntuple_v20_wgen-4c67a9d5a51f11cf2da50127721f7362/USER'
    Samples.mfv_neutralino_tau0100um_M0400.ana_dataset_override = '/mfv_neutralino_tau0100um_M0400/tucker-mfvntuple_v20_wgen-4c67a9d5a51f11cf2da50127721f7362/USER'
    Samples.mfv_neutralino_tau0100um_M0600.ana_dataset_override = '/mfv_neutralino_tau0100um_M0600/tucker-mfvntuple_v20_wgen-4c67a9d5a51f11cf2da50127721f7362/USER'
    Samples.mfv_neutralino_tau0100um_M0800.ana_dataset_override = '/mfv_neutralino_tau0100um_M0800/tucker-mfvntuple_v20_wgen-4c67a9d5a51f11cf2da50127721f7362/USER'
    Samples.mfv_neutralino_tau0100um_M1000.ana_dataset_override = '/mfv_neutralino_tau0100um_M1000/tucker-mfvntuple_v20_wgen-4c67a9d5a51f11cf2da50127721f7362/USER'
    Samples.mfv_neutralino_tau0300um_M0200.ana_dataset_override = '/mfv_neutralino_tau0300um_M0200/tucker-mfvntuple_v20_wgen-4c67a9d5a51f11cf2da50127721f7362/USER'
    Samples.mfv_neutralino_tau0300um_M0300.ana_dataset_override = '/mfv_neutralino_tau0300um_M0300/tucker-mfvntuple_v20_wgen-4c67a9d5a51f11cf2da50127721f7362/USER'
    Samples.mfv_neutralino_tau0300um_M0400.ana_dataset_override = '/mfv_neutralino_tau0300um_M0400/tucker-mfvntuple_v20_wgen-4c67a9d5a51f11cf2da50127721f7362/USER'
    Samples.mfv_neutralino_tau0300um_M0600.ana_dataset_override = '/mfv_neutralino_tau0300um_M0600/tucker-mfvntuple_v20_wgen-4c67a9d5a51f11cf2da50127721f7362/USER'
    Samples.mfv_neutralino_tau0300um_M0800.ana_dataset_override = '/mfv_neutralino_tau0300um_M0800/tucker-mfvntuple_v20_wgen-4c67a9d5a51f11cf2da50127721f7362/USER'
    Samples.mfv_neutralino_tau0300um_M1000.ana_dataset_override = '/mfv_neutralino_tau0300um_M1000/tucker-mfvntuple_v20_wgen-4c67a9d5a51f11cf2da50127721f7362/USER'
    Samples.mfv_neutralino_tau1000um_M0200.ana_dataset_override = '/mfv_neutralino_tau1000um_M0200/tucker-mfvntuple_v20_wgen-4c67a9d5a51f11cf2da50127721f7362/USER'
    Samples.mfv_neutralino_tau1000um_M0300.ana_dataset_override = '/mfv_neutralino_tau1000um_M0300/tucker-mfvntuple_v20_wgen-4c67a9d5a51f11cf2da50127721f7362/USER'
    Samples.mfv_neutralino_tau1000um_M0400.ana_dataset_override = '/mfv_neutralino_tau1000um_M0400/tucker-mfvntuple_v20_wgen-4c67a9d5a51f11cf2da50127721f7362/USER'
    Samples.mfv_neutralino_tau1000um_M0600.ana_dataset_override = '/mfv_neutralino_tau1000um_M0600/tucker-mfvntuple_v20_wgen-4c67a9d5a51f11cf2da50127721f7362/USER'
    Samples.mfv_neutralino_tau1000um_M0800.ana_dataset_override = '/mfv_neutralino_tau1000um_M0800/tucker-mfvntuple_v20_wgen-4c67a9d5a51f11cf2da50127721f7362/USER'
    Samples.mfv_neutralino_tau1000um_M1000.ana_dataset_override = '/mfv_neutralino_tau1000um_M1000/tucker-mfvntuple_v20_wgen-4c67a9d5a51f11cf2da50127721f7362/USER'
    Samples.mfv_neutralino_tau9900um_M0200.ana_dataset_override = '/mfv_neutralino_tau9900um_M0200/tucker-mfvntuple_v20_wgen-4c67a9d5a51f11cf2da50127721f7362/USER'
    Samples.mfv_neutralino_tau9900um_M0300.ana_dataset_override = '/mfv_neutralino_tau9900um_M0300/tucker-mfvntuple_v20_wgen-4c67a9d5a51f11cf2da50127721f7362/USER'
    Samples.mfv_neutralino_tau9900um_M0400.ana_dataset_override = '/mfv_neutralino_tau9900um_M0400/tucker-mfvntuple_v20_wgen-4c67a9d5a51f11cf2da50127721f7362/USER'
    Samples.mfv_neutralino_tau9900um_M0600.ana_dataset_override = '/mfv_neutralino_tau9900um_M0600/tucker-mfvntuple_v20_wgen-4c67a9d5a51f11cf2da50127721f7362/USER'
    Samples.mfv_neutralino_tau9900um_M0800.ana_dataset_override = '/mfv_neutralino_tau9900um_M0800/tucker-mfvntuple_v20_wgen-4c67a9d5a51f11cf2da50127721f7362/USER'
    Samples.mfv_neutralino_tau9900um_M1000.ana_dataset_override = '/mfv_neutralino_tau9900um_M1000/tucker-mfvntuple_v20_wgen-4c67a9d5a51f11cf2da50127721f7362/USER'

    for sample in Samples.mfv_signal_samples:
      sample.ana_scheduler = 'remoteGlidein'

    cs = CRABSubmitter('MFVResolutionsV20',
                       job_control_from_sample = True,
                       use_ana_dataset = True,
                       )
    cs.submit_all([Samples.mfv_neutralino_tau1000um_M0400])
