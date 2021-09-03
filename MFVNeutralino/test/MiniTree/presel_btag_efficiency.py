from DVCode.Tools.ROOTTools import *
import sys

year = sys.argv[1]
version = 'V25m'

if len(sys.argv) > 2 :
  syst_var_str = str(sys.argv[2])
  if syst_var_str != 'nom' and syst_var_str != 'bcjet_down' and syst_var_str != 'bcjet_up' and syst_var_str != 'ljet_down' and syst_var_str != 'ljet_up' :
    exit("invalid syst_var_str (%s), exiting!" % syst_var_str)
else :
  syst_var_str = 'nom'

f_btageff = ROOT.TFile('/uscms_data/d2/tucker/crab_dirs/BTagEff%sv1/background_%s.root' % (version, year) )
f_presel = ROOT.TFile('/uscms_data/d2/tucker/crab_dirs/PreselHistos%s/background_%s.root' % (version, year))

def njets(hname):
  h = f_btageff.Get(hname)
  return h.Integral(0, h.GetNbinsX()+1, 0, h.GetNbinsY()+1)

def btag_eff_per_jet(jet_flavor, bdisc):
  num = njets('JMTBTagEfficiency/num_%s_%s' % (jet_flavor, bdisc))
  den = njets('JMTBTagEfficiency/den_%s' % jet_flavor)
  return num/den

def scale_factor(jet_flavor, bdisc):

  h = f_btageff.Get('JMTBTagEfficiency/scalefactor_%s_%s' % (jet_flavor, bdisc))
  SF = h.GetMean()

  if   'up'   in syst_var_str : SF_var = 1
  elif 'down' in syst_var_str : SF_var = -1
  else                        : SF_var = 0

  # bjets and cjets have SF variations of the form SF +/- var
  # light jets have SF variations of the form SF * (1 +/- var)
  if jet_flavor == 'bottom' :
    if 'bcjet' in syst_var_str :
      # max variation from the csv files for 30 GeV < pT < 600 GeV; 
      # note that the variations for 20 GeV < pT < 30 GeV and for pT > 600 GeV 
      # are slightly larger in some cases
      SF_var *= 0.05 
      SF += SF_var

  elif jet_flavor == 'charm' :
    if 'bcjet' in syst_var_str :
      # max variation from the csv files for 30 GeV < pT < 600 GeV; 
      # note that the variations for 20 GeV < pT < 30 GeV and for pT > 600 GeV 
      # are slightly larger in some cases
      SF_var *= 0.18 
      SF += SF_var

  elif jet_flavor == 'light' :
    if 'ljet' in syst_var_str :
      # max variation from the csv files (occurs near pT = 450 GeV)
      SF_var *= 0.28
      SF *= (1+SF_var)

  return SF


def btag_eff_per_event_from_btag_eff_per_jet(event_flavor, effb, effc, effl):
  num = 0
  den = 0
  h_nlcb = f_btageff.Get('JMTBTagEfficiency/h_nlcb')
  for nl in range(0, h_nlcb.GetNbinsX()):
    for nc in range(0, h_nlcb.GetNbinsY()):
      for nb in range(0, 1) if event_flavor == 'nobjets' else range(1, h_nlcb.GetNbinsZ()):
        nlcb = h_nlcb.GetBinContent(nl+1, nc+1, nb+1)
        num += nlcb * (1 - (1-effb)**nb * (1-effc)**nc * (1-effl)**nl)
        den += nlcb
  return num/den

def btag_eff_per_event(event_flavor, bdisc):
  (firstxbin,lastxbin) = (3,3) if event_flavor == 'bquarks' else (1,2)
  h = f_presel.Get('mfvEventHistosJetPreSel/h_nbtags_v_bquark_code_%s' % bdisc).ProjectionY('h_nbtags', firstxbin, lastxbin)
  return h.Integral(2,4)/h.Integral(1,4)

# Convenient inputs for bquark_fraction.py
bdisc = '2' # Tight WP
effb, sfb = btag_eff_per_jet('bottom', bdisc), scale_factor('bottom', bdisc)
effc, sfc = btag_eff_per_jet('charm', bdisc), scale_factor('charm', bdisc)
effl, sfl = btag_eff_per_jet('light', bdisc), scale_factor('light', bdisc)

event_eff = btag_eff_per_event_from_btag_eff_per_jet('bjets', effb*sfb, effc*sfc, effl*sfl)
event_fakerate = btag_eff_per_event_from_btag_eff_per_jet('nobjets', effb*sfb, effc*sfc, effl*sfl)

h_nbtags_tight = f_presel.Get('mfvEventHistosJetPreSel/h_nbtags_2')
ft = h_nbtags_tight.Integral(2,11) / h_nbtags_tight.Integral(1,11)

# for the .csv file
variant = 'presel_%s_%s' % (year,syst_var_str)
outfile = open('efficiencies/effs_%s.csv' % (variant),'w')
outfile.write('%s,%s,%s,%s\n' % (variant,ft, event_eff, event_fakerate))
outfile.close()

# full table of information
print 'preselected events'
print '%10s%90s%26s%26s%26s' % ('', 'per-jet', 'per-event from per-jet', 'per-event from per-jet*SF', 'per-event')
fmt = '%10s' + '%10s'*9 + '%13s'*6
print fmt % ('', 'effb', 'SFb', 'effb*SFb', 'effc', 'SFc', 'effc*SFc', 'effl', 'SFl', 'effl*SFl', 'btag eff', 'fake rate', 'btag eff', 'fake rate', 'btag eff', 'fake rate')
for bdisc in ['0', '1', '2']:
  effb, sfb = btag_eff_per_jet('bottom', bdisc), scale_factor('bottom', bdisc)
  effc, sfc = btag_eff_per_jet('charm', bdisc), scale_factor('charm', bdisc)
  effl, sfl = btag_eff_per_jet('light', bdisc), scale_factor('light', bdisc)
  print fmt % (bdisc, '%.3f' % effb, '%.3f' % sfb, '%.3f' % (effb*sfb),
                      '%.3f' % effc, '%.3f' % sfc, '%.3f' % (effc*sfc),
                      '%.3f' % effl, '%.3f' % sfl, '%.3f' % (effl*sfl),
                      '%.3f' % btag_eff_per_event_from_btag_eff_per_jet('bjets', effb, effc, effl),
                      '%.3f' % btag_eff_per_event_from_btag_eff_per_jet('nobjets', effb, effc, effl),
                      '%.3f' % btag_eff_per_event_from_btag_eff_per_jet('bjets', effb*sfb, effc*sfc, effl*sfl),
                      '%.3f' % btag_eff_per_event_from_btag_eff_per_jet('nobjets', effb*sfb, effc*sfc, effl*sfl),
                      '%.3f' % btag_eff_per_event('bquarks', bdisc),
                      '%.3f' % btag_eff_per_event('nobquarks', bdisc))
