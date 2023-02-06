import sys
from JMTucker.Tools.BasicAnalyzer_cfg import *

debug = 'debug' in sys.argv

sample_files(process, 'ggHToSSTodddd_tau1mm_M55_2017', 'ntupleulv1am', 5)
tfileservice(process, 'gen_histos.root')
file_event_from_argv(process)

process.load('JMTucker.MFVNeutralino.GenParticles_cff')
#process.load('JMTucker.MFVNeutralino.GenParticleFilter_cfi')
#process.mfvGenParticleFilter.required_num_leptonic = 0

process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.mfvGenHistos = cms.EDAnalyzer('MFVGenHistos',
                                      gen_src = cms.InputTag('prunedGenParticles'),
                                      gen_jet_src = cms.InputTag('slimmedGenJets'),
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
    ms.submit(samples)

elif __name__ == '__main__' and hasattr(sys, 'argv') and 'validate' in sys.argv:
    import os, re
    from math import exp
    from JMTucker.Tools.ROOTTools import ROOT
    from JMTucker.Tools import colors

    fn_re = re.compile(r'(GluinoGluinoToNeutralinoNeutralinoTo2T2B2S|StopStopTo2Dbar2Dbar)_M_(\d+)_CTau_(\d+[um]m).root')

    for fn in sys.argv:
        if not fn.endswith('.root') or not os.path.isfile(fn):
            continue

        bn = os.path.basename(fn)
        mo = fn_re.match(bn)
        if not mo:
            raise ValueError('cannot parse fn %s' % fn)

        model, mass, tau_s = mo.groups()
        mass = float(mass)
        tau, tauunit = float(tau_s[:-2]), tau_s[-2:]
        if tauunit == 'um':
            tau *= 1e-4
        elif tauunit == 'mm':
            tau *= 1e-1

        nevents_expected = 10000
        if model == 'GluinoGluinoToNeutralinoNeutralinoTo2T2B2S':
            nevents_missing_allowed = 0
            folder_name = 'Lsps'
        elif model == 'StopStopTo2Dbar2Dbar':
            nevents_missing_allowed = 10
            folder_name = 'Hs'

        f = ROOT.TFile(fn)
        hs = [f.Get('mfvGenHistos/%s#%i/M' % (folder_name, i)) for i in 0,1]
        ok = all(nevents_expected - h.GetEntries() <= nevents_missing_allowed and abs(h.GetMean() - mass) < 0.01 for h in hs)

        h = f.Get('mfvGenHistos/h_ctaubig')
        xmax = h.GetXaxis().GetXmax()
        mean_expected = (tau - exp(-xmax/tau) * (xmax + tau)) / (1 - exp(-xmax/tau))
        ok = ok and nevents_expected - h.GetEntries()/2. <= nevents_missing_allowed and abs(h.GetMean() - mean_expected) < 2*h.GetMeanError()

        print (colors.green if ok else colors.red)('%s (%s %s %s) %s (%s %s) %s (%s)' % (fn, hs[0].GetEntries(), hs[1].GetEntries(), h.GetEntries(), mass, hs[0].GetMean(), hs[1].GetMean(), mean_expected, h.GetMean()))
