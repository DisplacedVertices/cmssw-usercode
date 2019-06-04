from JMTucker.Tools.ROOTTools import *
import sys

version = 'V25m'
year = int(sys.argv[1])
ntk = int(sys.argv[2])

if len(sys.argv) > 3 :
  SF_syst_var = float(sys.argv[3])
else :
  SF_syst_var = 1.0

f = ROOT.TFile('output_btags_vs_bquarks_MiniTree%s_ntk%s_%s/background.root' % (version, ntk, year) )

def njets(hname):
  h = f.Get(hname)
  return h.Integral() * h.GetMean()

def btag_eff_per_jet(nvtx, jet_flavor, bdisc):
  num = njets('h_%dv_n%sjets_%s_btag' % (nvtx, jet_flavor, bdisc))
  den = njets('h_%dv_n%sjets' % (nvtx, jet_flavor))
  return num/den

def scale_factor(nvtx, jet_flavor, bdisc):
  h = f.Get('h_%dv_scalefactor_%s_%s_btag' % (nvtx, jet_flavor, bdisc))
  return h.GetMean() * SF_syst_var

def btag_eff_per_event_from_btag_eff_per_jet(nvtx, event_flavor, effb, effc, effl):
  num = 0
  den = 0
  h_nlcb = f.Get('h_%dv_nlcb' % nvtx)
  for nl in range(0, h_nlcb.GetNbinsX()):
    for nc in range(0, h_nlcb.GetNbinsY()):
      for nb in range(0, 1) if event_flavor == 'nobjets' else range(1, h_nlcb.GetNbinsZ()):
        nlcb = h_nlcb.GetBinContent(nl+1, nc+1, nb+1)
        num += nlcb * (1 - (1-effb)**nb * (1-effc)**nc * (1-effl)**nl)
        den += nlcb
  return num/den

def btag_eff_per_event(nvtx, event_flavor, bdisc):
  h = f.Get('h_%s_%dv_1%s_btag_flavor_code' % (event_flavor, nvtx, bdisc))
  return h.GetBinContent(2) / h.Integral()

# convenient printout to copy into bquark_fraction.py
bdisc = 'tight' # Tight WP
nvtx = 1
effb, sfb = btag_eff_per_jet(nvtx, 'b', bdisc), scale_factor(nvtx, 'b', bdisc)
effc, sfc = btag_eff_per_jet(nvtx, 'c', bdisc), scale_factor(nvtx, 'c', bdisc)
effl, sfl = btag_eff_per_jet(nvtx, 'l', bdisc), scale_factor(nvtx, 'l', bdisc)

event_eff = btag_eff_per_event_from_btag_eff_per_jet(nvtx, 'bjets', effb*sfb, effc*sfc, effl*sfl)
event_fakerate = btag_eff_per_event_from_btag_eff_per_jet(nvtx, 'nobjets', effb*sfb, effc*sfc, effl*sfl)

h_1v_1tight_btag_flavor_code = f.Get('h_1v_1tight_btag_flavor_code')
ft = h_1v_1tight_btag_flavor_code.GetBinContent(2) / h_1v_1tight_btag_flavor_code.Integral()

print
print 'Inputs for bquark_fraction.py (for per-event from per-jet*SF; %s; Tight WP)' % year
print '###########################'
print '    print \'f0,f1,cb,cbbar from sorting events by at least 1 tight btag and unfolding; assume the probability of finding two vertices is the one-vertex efficiency squared (s=1); %s\'' % year
print '    f2_val_%strk = print_f2(%s, fb(ft0, efft0, frt0), fb(%.3f, %.3f, %.3f), cb, cbbar, 1)' % (ntk, ntk, ft, event_eff, event_fakerate)
print '    print'
print '###########################'
print

# full table of information
print '%10s%90s%26s%26s%26s' % ('', 'per-jet', 'per-event from per-jet', 'per-event from per-jet*SF', 'per-event')
fmt = '%10s' + '%10s'*9 + '%13s'*6
print fmt % ('', 'effb', 'SFb', 'effb*SFb', 'effc', 'SFc', 'effc*SFc', 'effl', 'SFl', 'effl*SFl', 'btag eff', 'fake rate', 'btag eff', 'fake rate', 'btag eff', 'fake rate')
for nvtx in [1, 2]:
  print '%d-track %d-vertex' % (ntk, nvtx)
  for bdisc in ['loose', 'medium', 'tight']:
    effb, sfb = btag_eff_per_jet(nvtx, 'b', bdisc), scale_factor(nvtx, 'b', bdisc)
    effc, sfc = btag_eff_per_jet(nvtx, 'c', bdisc), scale_factor(nvtx, 'c', bdisc)
    effl, sfl = btag_eff_per_jet(nvtx, 'l', bdisc), scale_factor(nvtx, 'l', bdisc)
    print fmt % (bdisc, '%.3f' % effb, '%.3f' % sfb, '%.3f' % (effb*sfb),
                        '%.3f' % effc, '%.3f' % sfc, '%.3f' % (effc*sfc),
                        '%.3f' % effl, '%.3f' % sfl, '%.3f' % (effl*sfl),
                        '%.3f' % btag_eff_per_event_from_btag_eff_per_jet(nvtx, 'bjets', effb, effc, effl),
                        '%.3f' % btag_eff_per_event_from_btag_eff_per_jet(nvtx, 'nobjets', effb, effc, effl),
                        '%.3f' % btag_eff_per_event_from_btag_eff_per_jet(nvtx, 'bjets', effb*sfb, effc*sfc, effl*sfl),
                        '%.3f' % btag_eff_per_event_from_btag_eff_per_jet(nvtx, 'nobjets', effb*sfb, effc*sfc, effl*sfl),
                        '%.3f' % btag_eff_per_event(nvtx, 'bquarks', bdisc),
                        '%.3f' % btag_eff_per_event(nvtx, 'nobquarks', bdisc))

