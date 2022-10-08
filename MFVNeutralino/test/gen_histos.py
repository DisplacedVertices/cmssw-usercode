import sys
from JMTucker.Tools.BasicAnalyzer_cfg import *

debug = 'debug' in sys.argv

#sample_files(process, 'mfv_neu_tau010000um_M1200_2017', 'main', 1)
input_files(process, 'C47DA2BF-B0FF-EA11-A2BC-001E67586629.root') #HSSbbbb 1mm 55GeV
#input_files(process, '02F9E1F8-1BF9-EA11-A44E-0242AC1C0501.root') #HSSbbbb 1mm 15GeV
max_events(process, 400)
tfileservice(process, 'gen_histos_HSSbbbb_1mm_55GeV.root')
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
ggHSSbbbb_M_55_CTau_1mm /store/mc/RunIIFall17MiniAODv2/ggH_HToSSTobbbb_MH-125_MS-55_ctauS-1_pT75_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/130000/E2FA02E4-C3EF-EA11-ABDA-0025905C3D96.root 24517
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
