import sys
from JMTucker.Tools.BasicAnalyzer_cfg import *

debug = 'debug' in sys.argv

sample_files(process, 'mfv_neu_tau010000um_M1200_2017', 'main', 1)
tfileservice(process, 'gen_histos.root')
file_event_from_argv(process)

process.load('JMTucker.MFVNeutralino.GenParticles_cff')
#process.load('JMTucker.MFVNeutralino.GenParticleFilter_cfi')
#process.mfvGenParticleFilter.required_num_leptonic = 0

process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.mfvGenHistos = cms.EDAnalyzer('MFVGenHistos',
                                      gen_src = cms.InputTag('genParticles'),
                                      gen_jet_src = cms.InputTag('ak4GenJetsNoNu'),
                                      gen_vertex_src = cms.InputTag('mfvGenParticles', 'genVertex'),
                                      mci_src = cms.InputTag('mfvGenParticles'),
                                      )

#process.p = cms.Path(process.mfvGenParticles * process.mfvGenParticleFilter * process.mfvGenHistos)
process.p = cms.Path(process.mfvGenParticles * process.mfvGenHistos)

if debug:
    process.mfvGenParticles.debug = True

    process.printList = cms.EDAnalyzer('JMTParticleListDrawer',
                                       src = cms.InputTag('genParticles'),
                                       printVertex = cms.untracked.bool(True),
                                       )
    process.p.insert(0, process.printList)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.Sample import anon_samples
    from JMTucker.Tools.MetaSubmitter import *
    from JMTucker.Tools.Year import year

    samples = anon_samples('''
GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_1200_CTau_100um /store/user/tucker/cfgtest/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_1200_CTau_100um.root 10000
GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_1200_CTau_10mm /store/user/tucker/cfgtest/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_1200_CTau_10mm.root 10000
GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_1200_CTau_1mm /store/user/tucker/cfgtest/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_1200_CTau_1mm.root 10000
GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_1200_CTau_300um /store/user/tucker/cfgtest/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_1200_CTau_300um.root 10000
GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_1200_CTau_30mm /store/user/tucker/cfgtest/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_1200_CTau_30mm.root 10000
GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_1600_CTau_100um /store/user/tucker/cfgtest/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_1600_CTau_100um.root 10000
GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_1600_CTau_10mm /store/user/tucker/cfgtest/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_1600_CTau_10mm.root 10000
GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_1600_CTau_1mm /store/user/tucker/cfgtest/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_1600_CTau_1mm.root 10000
GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_1600_CTau_300um /store/user/tucker/cfgtest/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_1600_CTau_300um.root 10000
GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_1600_CTau_30mm /store/user/tucker/cfgtest/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_1600_CTau_30mm.root 10000
GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_200_CTau_100um /store/user/tucker/cfgtest/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_200_CTau_100um.root 10000
GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_200_CTau_10mm /store/user/tucker/cfgtest/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_200_CTau_10mm.root 10000
GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_200_CTau_1mm /store/user/tucker/cfgtest/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_200_CTau_1mm.root 10000
GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_200_CTau_300um /store/user/tucker/cfgtest/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_200_CTau_300um.root 10000
GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_200_CTau_30mm /store/user/tucker/cfgtest/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_200_CTau_30mm.root 10000
GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_2400_CTau_100um /store/user/tucker/cfgtest/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_2400_CTau_100um.root 10000
GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_2400_CTau_10mm /store/user/tucker/cfgtest/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_2400_CTau_10mm.root 10000
GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_2400_CTau_1mm /store/user/tucker/cfgtest/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_2400_CTau_1mm.root 10000
GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_2400_CTau_300um /store/user/tucker/cfgtest/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_2400_CTau_300um.root 10000
GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_2400_CTau_30mm /store/user/tucker/cfgtest/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_2400_CTau_30mm.root 10000
GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_3000_CTau_100um /store/user/tucker/cfgtest/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_3000_CTau_100um.root 10000
GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_3000_CTau_10mm /store/user/tucker/cfgtest/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_3000_CTau_10mm.root 10000
GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_3000_CTau_1mm /store/user/tucker/cfgtest/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_3000_CTau_1mm.root 10000
GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_3000_CTau_300um /store/user/tucker/cfgtest/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_3000_CTau_300um.root 10000
GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_3000_CTau_30mm /store/user/tucker/cfgtest/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_3000_CTau_30mm.root 10000
GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_300_CTau_100um /store/user/tucker/cfgtest/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_300_CTau_100um.root 10000
GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_300_CTau_10mm /store/user/tucker/cfgtest/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_300_CTau_10mm.root 10000
GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_300_CTau_1mm /store/user/tucker/cfgtest/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_300_CTau_1mm.root 10000
GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_300_CTau_300um /store/user/tucker/cfgtest/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_300_CTau_300um.root 10000
GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_300_CTau_30mm /store/user/tucker/cfgtest/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_300_CTau_30mm.root 10000
GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_400_CTau_100um /store/user/tucker/cfgtest/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_400_CTau_100um.root 10000
GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_400_CTau_10mm /store/user/tucker/cfgtest/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_400_CTau_10mm.root 10000
GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_400_CTau_1mm /store/user/tucker/cfgtest/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_400_CTau_1mm.root 10000
GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_400_CTau_300um /store/user/tucker/cfgtest/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_400_CTau_300um.root 10000
GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_400_CTau_30mm /store/user/tucker/cfgtest/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_400_CTau_30mm.root 10000
GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_600_CTau_100um /store/user/tucker/cfgtest/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_600_CTau_100um.root 10000
GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_600_CTau_10mm /store/user/tucker/cfgtest/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_600_CTau_10mm.root 10000
GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_600_CTau_1mm /store/user/tucker/cfgtest/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_600_CTau_1mm.root 10000
GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_600_CTau_300um /store/user/tucker/cfgtest/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_600_CTau_300um.root 10000
GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_600_CTau_30mm /store/user/tucker/cfgtest/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_600_CTau_30mm.root 10000
GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_800_CTau_100um /store/user/tucker/cfgtest/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_800_CTau_100um.root 10000
GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_800_CTau_10mm /store/user/tucker/cfgtest/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_800_CTau_10mm.root 10000
GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_800_CTau_1mm /store/user/tucker/cfgtest/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_800_CTau_1mm.root 10000
GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_800_CTau_300um /store/user/tucker/cfgtest/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_800_CTau_300um.root 10000
GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_800_CTau_30mm /store/user/tucker/cfgtest/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M_800_CTau_30mm.root 10000
StopStopTo2Dbar2Dbar_M_1200_CTau_100um /store/user/tucker/cfgtest/StopStopTo2Dbar2Dbar_M_1200_CTau_100um.root 10000
StopStopTo2Dbar2Dbar_M_1200_CTau_10mm /store/user/tucker/cfgtest/StopStopTo2Dbar2Dbar_M_1200_CTau_10mm.root 10000
StopStopTo2Dbar2Dbar_M_1200_CTau_1mm /store/user/tucker/cfgtest/StopStopTo2Dbar2Dbar_M_1200_CTau_1mm.root 10000
StopStopTo2Dbar2Dbar_M_1200_CTau_300um /store/user/tucker/cfgtest/StopStopTo2Dbar2Dbar_M_1200_CTau_300um.root 10000
StopStopTo2Dbar2Dbar_M_1200_CTau_30mm /store/user/tucker/cfgtest/StopStopTo2Dbar2Dbar_M_1200_CTau_30mm.root 10000
StopStopTo2Dbar2Dbar_M_1600_CTau_100um /store/user/tucker/cfgtest/StopStopTo2Dbar2Dbar_M_1600_CTau_100um.root 10000
StopStopTo2Dbar2Dbar_M_1600_CTau_10mm /store/user/tucker/cfgtest/StopStopTo2Dbar2Dbar_M_1600_CTau_10mm.root 10000
StopStopTo2Dbar2Dbar_M_1600_CTau_1mm /store/user/tucker/cfgtest/StopStopTo2Dbar2Dbar_M_1600_CTau_1mm.root 10000
StopStopTo2Dbar2Dbar_M_1600_CTau_300um /store/user/tucker/cfgtest/StopStopTo2Dbar2Dbar_M_1600_CTau_300um.root 10000
StopStopTo2Dbar2Dbar_M_1600_CTau_30mm /store/user/tucker/cfgtest/StopStopTo2Dbar2Dbar_M_1600_CTau_30mm.root 10000
StopStopTo2Dbar2Dbar_M_200_CTau_100um /store/user/tucker/cfgtest/StopStopTo2Dbar2Dbar_M_200_CTau_100um.root 10000
StopStopTo2Dbar2Dbar_M_200_CTau_10mm /store/user/tucker/cfgtest/StopStopTo2Dbar2Dbar_M_200_CTau_10mm.root 10000
StopStopTo2Dbar2Dbar_M_200_CTau_1mm /store/user/tucker/cfgtest/StopStopTo2Dbar2Dbar_M_200_CTau_1mm.root 10000
StopStopTo2Dbar2Dbar_M_200_CTau_300um /store/user/tucker/cfgtest/StopStopTo2Dbar2Dbar_M_200_CTau_300um.root 10000
StopStopTo2Dbar2Dbar_M_200_CTau_30mm /store/user/tucker/cfgtest/StopStopTo2Dbar2Dbar_M_200_CTau_30mm.root 10000
StopStopTo2Dbar2Dbar_M_2400_CTau_100um /store/user/tucker/cfgtest/StopStopTo2Dbar2Dbar_M_2400_CTau_100um.root 10000
StopStopTo2Dbar2Dbar_M_2400_CTau_10mm /store/user/tucker/cfgtest/StopStopTo2Dbar2Dbar_M_2400_CTau_10mm.root 10000
StopStopTo2Dbar2Dbar_M_2400_CTau_1mm /store/user/tucker/cfgtest/StopStopTo2Dbar2Dbar_M_2400_CTau_1mm.root 10000
StopStopTo2Dbar2Dbar_M_2400_CTau_300um /store/user/tucker/cfgtest/StopStopTo2Dbar2Dbar_M_2400_CTau_300um.root 10000
StopStopTo2Dbar2Dbar_M_2400_CTau_30mm /store/user/tucker/cfgtest/StopStopTo2Dbar2Dbar_M_2400_CTau_30mm.root 10000
StopStopTo2Dbar2Dbar_M_3000_CTau_100um /store/user/tucker/cfgtest/StopStopTo2Dbar2Dbar_M_3000_CTau_100um.root 10000
StopStopTo2Dbar2Dbar_M_3000_CTau_10mm /store/user/tucker/cfgtest/StopStopTo2Dbar2Dbar_M_3000_CTau_10mm.root 10000
StopStopTo2Dbar2Dbar_M_3000_CTau_1mm /store/user/tucker/cfgtest/StopStopTo2Dbar2Dbar_M_3000_CTau_1mm.root 10000
StopStopTo2Dbar2Dbar_M_3000_CTau_300um /store/user/tucker/cfgtest/StopStopTo2Dbar2Dbar_M_3000_CTau_300um.root 10000
StopStopTo2Dbar2Dbar_M_3000_CTau_30mm /store/user/tucker/cfgtest/StopStopTo2Dbar2Dbar_M_3000_CTau_30mm.root 10000
StopStopTo2Dbar2Dbar_M_300_CTau_100um /store/user/tucker/cfgtest/StopStopTo2Dbar2Dbar_M_300_CTau_100um.root 10000
StopStopTo2Dbar2Dbar_M_300_CTau_10mm /store/user/tucker/cfgtest/StopStopTo2Dbar2Dbar_M_300_CTau_10mm.root 10000
StopStopTo2Dbar2Dbar_M_300_CTau_1mm /store/user/tucker/cfgtest/StopStopTo2Dbar2Dbar_M_300_CTau_1mm.root 10000
StopStopTo2Dbar2Dbar_M_300_CTau_300um /store/user/tucker/cfgtest/StopStopTo2Dbar2Dbar_M_300_CTau_300um.root 10000
StopStopTo2Dbar2Dbar_M_300_CTau_30mm /store/user/tucker/cfgtest/StopStopTo2Dbar2Dbar_M_300_CTau_30mm.root 10000
StopStopTo2Dbar2Dbar_M_400_CTau_100um /store/user/tucker/cfgtest/StopStopTo2Dbar2Dbar_M_400_CTau_100um.root 10000
StopStopTo2Dbar2Dbar_M_400_CTau_10mm /store/user/tucker/cfgtest/StopStopTo2Dbar2Dbar_M_400_CTau_10mm.root 10000
StopStopTo2Dbar2Dbar_M_400_CTau_1mm /store/user/tucker/cfgtest/StopStopTo2Dbar2Dbar_M_400_CTau_1mm.root 10000
StopStopTo2Dbar2Dbar_M_400_CTau_300um /store/user/tucker/cfgtest/StopStopTo2Dbar2Dbar_M_400_CTau_300um.root 10000
StopStopTo2Dbar2Dbar_M_400_CTau_30mm /store/user/tucker/cfgtest/StopStopTo2Dbar2Dbar_M_400_CTau_30mm.root 10000
StopStopTo2Dbar2Dbar_M_600_CTau_100um /store/user/tucker/cfgtest/StopStopTo2Dbar2Dbar_M_600_CTau_100um.root 10000
StopStopTo2Dbar2Dbar_M_600_CTau_10mm /store/user/tucker/cfgtest/StopStopTo2Dbar2Dbar_M_600_CTau_10mm.root 10000
StopStopTo2Dbar2Dbar_M_600_CTau_1mm /store/user/tucker/cfgtest/StopStopTo2Dbar2Dbar_M_600_CTau_1mm.root 10000
StopStopTo2Dbar2Dbar_M_600_CTau_300um /store/user/tucker/cfgtest/StopStopTo2Dbar2Dbar_M_600_CTau_300um.root 10000
StopStopTo2Dbar2Dbar_M_600_CTau_30mm /store/user/tucker/cfgtest/StopStopTo2Dbar2Dbar_M_600_CTau_30mm.root 10000
StopStopTo2Dbar2Dbar_M_800_CTau_100um /store/user/tucker/cfgtest/StopStopTo2Dbar2Dbar_M_800_CTau_100um.root 10000
StopStopTo2Dbar2Dbar_M_800_CTau_10mm /store/user/tucker/cfgtest/StopStopTo2Dbar2Dbar_M_800_CTau_10mm.root 10000
StopStopTo2Dbar2Dbar_M_800_CTau_1mm /store/user/tucker/cfgtest/StopStopTo2Dbar2Dbar_M_800_CTau_1mm.root 10000
StopStopTo2Dbar2Dbar_M_800_CTau_300um /store/user/tucker/cfgtest/StopStopTo2Dbar2Dbar_M_800_CTau_300um.root 10000
StopStopTo2Dbar2Dbar_M_800_CTau_30mm /store/user/tucker/cfgtest/StopStopTo2Dbar2Dbar_M_800_CTau_30mm.root 10000
''', condor=True)

    ms = MetaSubmitter('GenHistos_Test%i'%year)
    ms.common.ex = year
    ms.submit(samples)
