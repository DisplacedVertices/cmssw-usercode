import sys, os
from array import array
from JMTucker.Tools.general import typed_from_argv
from JMTucker.Tools.ROOTTools import *
from JMTucker.Tools import Samples
from JMTucker.Tools.Samples import *

#useElectron = True
useMETNoMu = True
version = ['2017v16_mu_MET', '2017v16_ele_MET']
useElectron = [False, True]
if useMETNoMu:
  for i in range(len(version)):
    version[i]+='NoMu'
zoom = False #(0.98,1.005)
save_more = True
data_only = False
use_qcd = False
fitting = False
num_dir, den_dir = 'num', 'den'
#num_dir, den_dir = 'numjet6pt75', 'denjet6pt75'

which = typed_from_argv(int, 0)
data_period, int_lumi = [
    ('p8',101037.),
    ('',   41525.),
    ('B',   4794.),
    ('C',   9631.),
    ('D',   4248.),
    ('E',   9314.),
    ('F',  13538.),
    ('',   59512.),
    ('A',  14002.),
    ('B',   7091.),
    ('C',   6937.),
    ('D',  31482.),
    ][which]
year = 2017 if which < 7 else 2018
print year, data_period, int_lumi

########################################################################

root_dir = ['/uscms/home/ali/nobackup/LLP/crabdir/TrigEff%s' % version[i] for i in range(len(version))]
plot_path = 'TrigEffComp_%s_%s_%s%s' % (version[0], version[1], year, data_period)
if zoom:
    plot_path += '_zoom'

set_style()
ROOT.gStyle.SetOptStat(0)
ps = plot_saver(plot_dir(plot_path), size=(600,600), log=False, pdf=True)
ROOT.TH1.AddDirectory(0)


########################################################################

kinds = ['']
#ns = ['h_jet_ht']
if useMETNoMu:
  ns = ['h_metpt_nomu']
else:
  ns = ['h_metpt']

lump_lower = 0.
#lump_lower = 1200.

def fit_limits(kind, n):
    if 'ht' in n:
        return 650, 5000
    elif 'met' in n:
        return 50, 1000
    else:
        if 'pf' in kind:
            if 'pt_4' in n:
                return 85, 250
            else:
                return 75, 250
        else:
            return 60, 250

def draw_limits(kind, n):
    if 'ht' in n:
        return 500, 5000
    else:
        if 'pf' in kind:
            if 'pt_4' in n:
                return 85, 250
            else:
                return 75, 250
        else:
            return 60, 250

def make_fcn(name, kind, n):
    #fcn = ROOT.TF1(name, '[0] + [1]*(0.5 + 0.5 * TMath::Erf((x - [2])/[3]))', *fit_limits(kind,n))
    fcn = ROOT.TF1(name, '[0] + [1]*(0.5 + 0.5 * TMath::TanH((x - [2])/[3]))', *fit_limits(kind,n))
    fcn.SetParNames('floor', 'ceil', 'turnmu', 'turnsig')
    if 'ht' in n:
        fcn.SetParameters(0, 1, 900, 100)
    else:
        fcn.SetParameters(0, 1, 150, 50)
    fcn.SetParLimits(1, 0, 1)
    fcn.SetLineWidth(2)
    fcn.SetLineStyle(2)
    
    return fcn

def rebin_met(h):
    a = to_array(range(0, 100, 5) + range(100, 200, 10) + [200, 225, 250, 275, 300, 350, 400, 450, 500, 600, 700, 800, 1000])
    return h.Rebin(len(a)-1, h.GetName() + '_rebin', a)

def rebin_pt(h):
    a = to_array(range(0, 100, 5) + range(100, 150, 10) + [150, 180, 220, 260, 370, 500])
    return h.Rebin(len(a)-1, h.GetName() + '_rebin', a)

def rebin_ht(h):
    a = to_array(range(0, 500, 20) + range(500, 1000, 50) + range(1000, 1500, 100) + range(1500, 2000, 250) + [2000, 3000, 5000])
    hnew = h.Rebin(len(a)-1, h.GetName() + '_rebin', a)
    move_overflow_into_last_bin(hnew)
    return hnew

def get(f, kind, n):
    def rebin(h):
        return h
    if 'met' in n:
      rebin = rebin_met
    elif 'pt' in n:
        rebin = rebin_pt
    elif 'ht' in n:
        rebin = rebin_ht
    return rebin(f.Get(kind + '%s/%s' % (num_dir, n))), rebin(f.Get(kind + '%s/%s' % (den_dir, n)))

def num_den_draw(num, den):
    x = []
    for h in num, den:
        h2 = h.Clone(num.GetName() + '_drawscaled')
        #h2.Scale(1., 'width')
        x.append(h2)
    num, den = x
    num.SetFillColor(den.GetLineColor())
    num.SetFillStyle(3004)
    den.Draw('e')
    num.Draw('hist same')
    return num, den

########################################################################
bkg_eff = []
data_eff = []
for i in range(len(root_dir)):

  if useElectron[i]:
    data_fn = os.path.join(root_dir[i], 'SingleElectron%s%s.root' % (year, data_period))
  else:
    data_fn = os.path.join(root_dir[i], 'SingleMuon%s%s.root' % (year, data_period))
  
  data_f = ROOT.TFile(data_fn)
  
  if data_only:
      bkg_samples, sig_samples = [], []
  else:
      if year == 2017 or year == 2018:
          if useElectron[i]:
            bkg_samples = [ttbar_2017, wjetstolnusum_2017, dyjetstollM50sum_2017]
          else:
            bkg_samples = [ttbar_2017, wjetstolnusum_2017, dyjetstollM50sum_2017, dyjetstollM10_2017, qcdmupt15_2017]
          if use_qcd:
              bkg_samples.append(qcdmupt15_2017)
          sig_samples = Samples.mfv_splitSUSY_samples_2017
  
  n_bkg_samples = len(bkg_samples)
  for samples in bkg_samples, sig_samples:
      for sample in samples:
          sample.fn = os.path.join(root_dir[i], sample.name + '.root')
          sample.f = ROOT.TFile(sample.fn) if os.path.isfile(sample.fn) else None
          if not os.path.isfile(sample.fn):
            print("{} not found!".format(sample.fn))
  
  for kind in kinds:
      for n in ns:
          print
          print '============================================================================='
          print kind, n
          print '-----------------------'
          subname = '%s_%s_%s' % (kind, n, version[i]) if kind else n+version[i]
  
          bkg_num, bkg_den = None, None
          sum_scaled_nums, sum_scaled_dens = 0., 0.
          sum_scaled_nums_var, sum_scaled_dens_var = 0., 0.
  
          reses = []
          for sample in bkg_samples:
              subsubname = subname + '_' + sample.name
  
              num, den = sample.num, sample.den = get(sample.f, kind, n)
  
              if save_more:
                  x = num_den_draw(num, den)
                  ps.save(subsubname + '_num_den',log=True)
  
              if den.Integral():
                  rat = histogram_divide(num, den)
                  rat.Draw('AP')
                  if 'met' in n:
                      rat.GetXaxis().SetLimits(0, 1000)
                  elif 'pt' in n:
                      rat.GetXaxis().SetLimits(0, 260)
                  elif 'ht' in n:
                      rat.GetXaxis().SetLimits(0, draw_limits(kind,n)[1])
  
                  fcn = make_fcn('f_' + subsubname, kind, n)
                  res = rat.Fit(fcn, 'RQS')
                  reses.append(res)
                  if save_more:
                      rat.SetTitle('')
                      ps.c.Update()
                      move_stat_box(rat, 'inf' if zoom else (0.518, 0.133, 0.866, 0.343))
                      ps.save(subsubname)
              else:
                  reses.append(None)
  
              sample.total_events = -1
              scale = sample.partial_weight(sample.f) * int_lumi
  
              print '%s (%f)' % (sample.name, scale)
              ib = num.FindBin(lump_lower)
              ni = num.Integral(ib, 10000)
              di = den.Integral(ib, 10000)
              sum_scaled_nums += ni*scale
              sum_scaled_dens += di*scale
              sum_scaled_nums_var += scale**2 * ni
              sum_scaled_dens_var += scale**2 * di
              print '   %10i %10i %10.2f %10.2f  %.6f [%.6f, %.6f]' % ((ni, di, ni*scale, di*scale) + clopper_pearson(ni, di))
              #res.Print()
  
              num.Scale(scale)
              den.Scale(scale)
              if bkg_num is None and bkg_den is None:
                  bkg_num = num.Clone('bkg_num')
                  bkg_den = den.Clone('bkg_den')
              else:
                  bkg_num.Add(num)
                  bkg_den.Add(den)
  
          if reses:
              pars = [reses[0].GetParameterName(i) for i in xrange(reses[0].NPar())]
              for ipar, parname in enumerate(pars):
                  subsubname = subname + '_' + parname
                  hpar = ROOT.TH1F(parname, '', n_bkg_samples, 0, n_bkg_samples)
                  for isam, sample in enumerate(bkg_samples):
                      #if sample.name == 'qcdmupt15' and 'Mu1' in kind:
                      #    continue
                      #print isam, reses[isam].Parameter(ipar), reses[isam].ParError(ipar)
                      hpar.SetBinContent(isam+1, reses[isam].Parameter(ipar))
                      hpar.SetBinError  (isam+1, reses[isam].ParError (ipar))
                      hpar.GetXaxis().SetBinLabel(isam+1, sample.name)
                  hpar.Draw('hist e')
                  hpar.SetLineWidth(2)
                  fcnpar = ROOT.TF1('f_'  + subsubname, 'pol0')
                  fcnpar.SetLineWidth(1)
                  hpar.Fit(fcnpar, 'Q')
                  ps.c.Update()
                  move_stat_box(hpar, (0.507, 0.664, 0.864, 0.855))
                  if parname == 'floor':
                      hpar.GetYaxis().SetRangeUser(0, 0.3)
                  elif parname == 'ceil':
                      hpar.GetYaxis().SetRangeUser(0.2, 1)
                      move_stat_box(hpar, (0.143, 0.147, 0.5, 0.339))
                  elif parname == 'turnmu':
                      hpar.GetYaxis().SetRangeUser(0, 1500)
                  elif parname == 'turnsig':
                      hpar.GetYaxis().SetRangeUser(0, 300)
                  ps.save(subsubname)
  
          if sum_scaled_dens_var > 0 and sum_scaled_dens > 0:
              bkg_effective_den = sum_scaled_dens**2 / sum_scaled_dens_var
              bkg_effective_num = sum_scaled_nums / sum_scaled_dens * bkg_effective_den
              print 'sum bkgs with effective n =', bkg_effective_den
              print '   %10.2f %10.2f %10s %10s  %.6f [%.6f, %.6f]' % ((sum_scaled_nums, sum_scaled_dens, '', '') + clopper_pearson(bkg_effective_num, bkg_effective_den))
              print '+- %10.2f %10.2f' % (sum_scaled_nums_var**0.5, sum_scaled_dens_var**0.5)
  
          if 'gen' in n:
              continue
  
          print 'data' #, data_num.GetEntries(), data_den.GetEntries()
          data_num, data_den = get(data_f, kind, n)
          if save_more:
              x = num_den_draw(data_num, data_den)
              ps.save(subname + '_data_num_den', log=True)
  
          ib = data_num.FindBin(lump_lower)
          ni = data_num.Integral(ib, 10000)
          di = data_den.Integral(ib, 10000)
          print '   %10i %10i %10s %10s  %.6f [%.6f, %.6f]' % ((ni, di, '', '') + clopper_pearson(ni, di))
          print '+- %10.2f %10.2f' % (ni**0.5, di**0.5)
          if sum_scaled_nums and sum_scaled_dens:
              print 'data/mc:'
              print '   %10.4f %10.4f' % (ni/sum_scaled_nums, di/sum_scaled_dens)
              ivnum = clopper_pearson_poisson_means(ni, sum_scaled_nums)
              ivden = clopper_pearson_poisson_means(di, sum_scaled_dens)
              print '+- %10.4f %10.4f' % ((ivnum[2] - ivnum[1])/2, (ivden[2] - ivden[1])/2)
  
          data_rat = histogram_divide(data_num, data_den)
          bkg_rat = histogram_divide(bkg_num, bkg_den, use_effective=True) if bkg_num and bkg_den else None
          data_eff.append(data_rat)
          bkg_eff.append(bkg_rat)
  
          #for r in (data_rat, bkg_rat):
          #    if not r:
          #        continue
          #    if 'met' in n:
          #        r.GetXaxis().SetLimits(0, 1000)
          #        r.SetTitle('; MET p_{T} (GeV);efficiency')
          #        if 'nomu' in n:
          #          r.SetTitle('; METnoMu p_{T} (GeV);efficiency')
          #    elif 'pt' in n:
          #        r.GetXaxis().SetLimits(0, 260)
          #        i = int(n.split('_')[-1])
          #        k = 'PF' if 'pf' in kind else 'calo'
          #        r.SetTitle(';%ith %s jet p_{T} (GeV);efficiency' % (i, k))
          #    elif 'ht' in n:
          #        r.GetXaxis().SetLimits(0, draw_limits(kind, n)[1])
          #        k = ''
          #        r.SetTitle(';%s H_{T} (GeV);efficiency' % k)
          #    r.GetHistogram().SetMinimum(0)
          #    r.GetHistogram().SetMaximum(1.05)
          #    r.SetLineWidth(2)
  
          #data_rat.Draw('AP')
          #if zoom:
          #    data_rat.GetYaxis().SetRangeUser(*zoom)
          #ROOT.gStyle.SetOptFit(1111)
          #data_fcn = make_fcn('f_data', kind, n)
          #data_fcn.SetLineColor(ROOT.kBlack)
          #data_res = data_rat.Fit(data_fcn, 'RQS',"",0,1000)
          #print '\ndata:'
          #data_res.Print()
          #if bkg_rat:
          #    bkg_fcn = make_fcn('f_bkg', kind, n)
          #    bkg_fcn.SetLineColor(2)
          #    bkg_res = bkg_rat.Fit(bkg_fcn, 'RQS',"",0,1000)
          #    print '\nbkg:'
          #    bkg_res.Print()
  
          #    bkg_rat.SetFillStyle(3001)
          #    bkg_rat.SetFillColor(2)
          #    bkg_rat.Draw('E2 same')
  
          #ps.c.Update()
          #move_stat_box(data_rat, 'inf' if zoom else (0.518, 0.133, 0.866, 0.343))
          #if bkg_rat:
          #    s = move_stat_box(bkg_rat, 'inf' if zoom else (0.518, 0.350, 0.866, 0.560))
          #    s.SetLineColor(2)
          #    s.SetTextColor(2)
  
          #ps.save(subname)
  
          #print '\nsignals'
          #for sample in sig_samples:
          #    if sample.f:
          #        sig_num, sig_den = get(sample.f, kind, n)
          #        ib = sig_num.FindBin(lump_lower)
          #        ni = sig_num.Integral(ib, 10000)
          #        di = sig_den.Integral(ib, 10000)
          #        print '   %10i %10i %10s %10s  %.6f [%.6f, %.6f]' % ((ni, di, '', '') + clopper_pearson(ni, di))
          #        print '+- %10.2f %10.2f' % (ni**0.5, di**0.5)

eff = [data_eff, bkg_eff]
eff_name = ["data",'bkg']
n = ns[0]
kind = kinds[0]
for idx in range(len(eff)):
  eff_use = eff[idx]
  eff_n = eff_name[idx]
  l = ROOT.TLegend(0.518, 0.133, 0.866, 0.343)
  print("number of graph {}".format(len(eff_use)))
  for i in range(len(eff_use)):
    r = eff_use[i]
    if not r:
        continue
    if 'met' in n:
        r.GetXaxis().SetLimits(0, 1000)
        r.SetTitle('; MET p_{T} (GeV);efficiency')
        if 'nomu' in n:
          r.SetTitle('; METnoMu p_{T} (GeV);efficiency')
    elif 'pt' in n:
        r.GetXaxis().SetLimits(0, 260)
        i = int(n.split('_')[-1])
        k = 'PF' if 'pf' in kind else 'calo'
        r.SetTitle(';%ith %s jet p_{T} (GeV);efficiency' % (i, k))
    elif 'ht' in n:
        r.GetXaxis().SetLimits(0, draw_limits(kind, n)[1])
        k = ''
        r.SetTitle(';%s H_{T} (GeV);efficiency' % k)
    r.GetHistogram().SetMinimum(0)
    r.GetHistogram().SetMaximum(1.05)
    r.SetLineWidth(2)
    r.SetLineColor(i+1)
    r.SetFillColor(0)

    if i==0:
      r.Draw('AP')
    else:
      r.Draw('E same')

    if useElectron[i]:
      l.AddEntry(r, "SingleElectron")
    else:
      l.AddEntry(r, "SingleMuon")

    if fitting:
      ROOT.gStyle.SetOptFit(1111)
      r_fcn = make_fcn('f', kind, n)
      r_fcn.SetLineColor(i+1)
      r_res = r.Fit(r_fcn, 'RQS',"",0,1000)
    ps.c.Update()
    if fitting:
      s = move_stat_box(r, 'inf' if zoom else (0.518, 0.133, 0.866, 0.343))
      s.SetLineColor(i+1)
      s.SetTextColor(i+1)

  l.Draw()
  ps.save(eff_n)
