from JMTucker.Tools.ROOTTools import *

ntk = 3
f = ROOT.TFile('output_btags_vs_bquarks_MiniTreeV23m_ntk%s/background.root' % ntk)

def njets(hname):
  h = f.Get(hname)
  return h.Integral() * h.GetMean()

def btag_eff_per_jet(nvtx, jet_flavor, bdisc):
  num = njets('h_%dv_n%sjets_%s_btag' % (nvtx, jet_flavor, bdisc))
  den = njets('h_%dv_n%sjets' % (nvtx, jet_flavor))
  return num/den

def btag_eff_per_event_from_btag_eff_per_jet(nvtx, event_flavor, bdisc):
  effb = btag_eff_per_jet(nvtx, 'b', bdisc)
  effc = btag_eff_per_jet(nvtx, 'c', bdisc)
  effl = btag_eff_per_jet(nvtx, 'l', bdisc)
  num = 0
  den = 0
  for nc in range(0, 40):
    h_nbnl = f.Get('h_%dv_%dcjets_nljets_vs_nbjets' % (nvtx, nc))
    for nb in range(0, 1) if event_flavor == 'nobjets' else range(1, h_nbnl.GetNbinsX()):
      for nl in range(0, h_nbnl.GetNbinsY()):
        n_nbnl = h_nbnl.GetBinContent(nb+1, nl+1)
        num += n_nbnl * (1 - (1-effb)**nb * (1-effc)**nc * (1-effl)**nl)
        den += n_nbnl
  return num/den

def btag_eff_per_event(nvtx, event_flavor, bdisc):
  h = f.Get('h_%s_%dv_1%s_btag_flavor_code' % (event_flavor, nvtx, bdisc))
  return h.GetBinContent(2) / h.Integral()

print '%10s%60s%40s%40s' % ('', 'per-jet', 'per-event from per-jet', 'per-event')
fmt = '%10s%20s%20s%20s%20s%20s%20s%20s'
print fmt % ('', 'btag efficiency', 'c misid prob', 'udsg misid prob', 'btag efficiency', 'fake rate', 'btag efficiency', 'fake rate')
for nvtx in [1, 2]:
  print '%d-track %d-vertex' % (ntk, nvtx)
  for bdisc in ['loose', 'medium', 'tight']:
    print fmt % (bdisc, '%.3f' % btag_eff_per_jet(nvtx, 'b', bdisc), '%.3f' % btag_eff_per_jet(nvtx, 'c', bdisc), '%.3f' % btag_eff_per_jet(nvtx, 'l', bdisc),
                        '%.3f' % btag_eff_per_event_from_btag_eff_per_jet(nvtx, 'bjets', bdisc), '%.3f' % btag_eff_per_event_from_btag_eff_per_jet(nvtx, 'nobjets', bdisc),
                        '%.3f' % btag_eff_per_event(nvtx, 'bquarks', bdisc),                     '%.3f' % btag_eff_per_event(nvtx, 'nobquarks', bdisc))
