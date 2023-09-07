from JMTucker.Tools.ROOTTools import *
import sys

version = 'V25mv3'
year = sys.argv[1]
ntk = int(sys.argv[2])

if len(sys.argv) > 3 :
  syst_var_str = str(sys.argv[3])
  if syst_var_str != 'nom' and syst_var_str != 'bcjet_down' and syst_var_str != 'bcjet_up' and syst_var_str != 'ljet_down' and syst_var_str != 'ljet_up' :
    exit("invalid syst_var_str (%s), exiting!" % syst_var_str)
else :
  syst_var_str = 'nom'

f = ROOT.TFile('output_btags_vs_bquarks_MiniTree%s_ntk%s_%s/background.root' % (version, ntk, year) )

def njets(hname):
  h = f.Get(hname)
  return h.Integral() * h.GetMean()

def btag_eff_per_jet(nvtx, jet_flavor, bdisc):
  num = njets('h_%dv_n%sjets_%s_btag' % (nvtx, jet_flavor, bdisc))
  den = njets('h_%dv_n%sjets' % (nvtx, jet_flavor))
  return num/den if den > 0 else 0

def scale_factor(nvtx, jet_flavor, bdisc):

  h = f.Get('h_%dv_scalefactor_%s_%s_btag' % (nvtx, jet_flavor, bdisc))
  SF = h.GetMean()

  if   'up'   in syst_var_str : SF_var = 1
  elif 'down' in syst_var_str : SF_var = -1
  else                        : SF_var = 0

  # bjets and cjets have SF variations of the form SF +/- var
  # light jets have SF variations of the form SF * (1 +/- var)
  if jet_flavor == 'b' :
    if 'bcjet' in syst_var_str :
      # max variation from the csv files for 30 GeV < pT < 600 GeV; 
      # note that the variations for 20 GeV < pT < 30 GeV and for pT > 600 GeV 
      # are slightly larger in some cases
      SF_var *= 0.05 
      SF += SF_var

  elif jet_flavor == 'c' :
    if 'bcjet' in syst_var_str :
      # max variation from the csv files for 30 GeV < pT < 600 GeV; 
      # note that the variations for 20 GeV < pT < 30 GeV and for pT > 600 GeV 
      # are slightly larger in some cases
      SF_var *= 0.18 
      SF += SF_var

  elif jet_flavor == 'l' :
    if 'ljet' in syst_var_str :
      # max variation from the csv files (occurs near pT = 450 GeV)
      SF_var *= 0.28
      SF *= (1+SF_var)

  return SF


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
  return h.GetBinContent(2) / h.Integral() if h.Integral() > 0 else 0

# Convenient inputs for bquark_fraction.py
bdisc = 'tight' # Tight WP
nvtx = 1
effb, sfb = btag_eff_per_jet(nvtx, 'b', bdisc), scale_factor(nvtx, 'b', bdisc)
effc, sfc = btag_eff_per_jet(nvtx, 'c', bdisc), scale_factor(nvtx, 'c', bdisc)
effl, sfl = btag_eff_per_jet(nvtx, 'l', bdisc), scale_factor(nvtx, 'l', bdisc)

event_eff = btag_eff_per_event_from_btag_eff_per_jet(nvtx, 'bjets', effb*sfb, effc*sfc, effl*sfl)
event_fakerate = btag_eff_per_event_from_btag_eff_per_jet(nvtx, 'nobjets', effb*sfb, effc*sfc, effl*sfl)

h_1v_1tight_btag_flavor_code = f.Get('h_1v_1tight_btag_flavor_code')
ft = h_1v_1tight_btag_flavor_code.GetBinContent(2) / h_1v_1tight_btag_flavor_code.Integral() if h_1v_1tight_btag_flavor_code.Integral() > 0 else 0

# for the .csv file
variant = '%strk_1v_%s_%s' % (ntk,year,syst_var_str)
outfile = open('efficiencies/effs_%s.csv' % (variant),'w')
outfile.write('%s,%s,%s,%s\n' % (variant, ft, event_eff, event_fakerate))
outfile.close()

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

