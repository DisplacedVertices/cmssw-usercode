from JMTucker.MFVNeutralino.MiniTreeBase import *

bins = to_array(0., 0.04, 0.07, 4)
nbins = len(bins) - 1

observed = [1,0,0]

int_lumi = ac.int_lumi_2015p6 * ac.scale_factor_2015p6

bkg_n1v = 3637.
bkg_n2v = 1.

sig_uncert = [0.20, 0.20, 0.20]
bkg_uncert = [0.13, 0.29, 0.52]

in_fn = '2v_from_jets_2015p6_5track_default_v15.root'
in_trees = '/uscms_data/d2/tucker/crab_dirs/MiniTreeV15_v3/mfv*root'

out_fn = 'limits_input.root'

assert len(observed) == nbins
assert len(sig_uncert) == nbins
assert len(bkg_uncert) == nbins

def make():
    ROOT.TH1.AddDirectory(1)
    in_f = ROOT.TFile(in_fn)
    f = ROOT.TFile(out_fn, 'recreate')

    h_int_lumi = ROOT.TH1D('h_int_lumi', '', 1, 0, 1)
    h_int_lumi.SetBinContent(1, int_lumi)

    h_observed = ROOT.TH1D('h_observed', '', nbins, bins)
    for i,v in enumerate(observed):
        h_observed.SetBinContent(i+1, v)
    
    # bkg comes from Jen's 2v_from_hists
    h_bkg_dbv  = to_TH1D(in_f.Get('h_1v_dbv') , 'h_bkg_dbv')
    h_bkg_dvv  = to_TH1D(in_f.Get('h_c1v_dvv'), 'h_bkg_dvv')

    h_bkg_dphi = ROOT.TH1D('h_bkg_dphi', '', 100, 0, pi)
    f_dphi = in_f.Get('f_dphi')
    for ibin in xrange(1, h_bkg_dphi.GetNbinsX()+1):
        a = h_bkg_dphi.GetXaxis().GetBinLowEdge(ibin)
        b = h_bkg_dphi.GetXaxis().GetBinLowEdge(ibin+1)
        h_bkg_dphi.SetBinContent(ibin, f_dphi.Integral(a,b)/(b-a))

    h_bkg_dbv.Scale(bkg_n1v/h_bkg_dbv.Integral())
    for h in h_bkg_dvv, h_bkg_dphi:
        h.Scale(bkg_n2v/h.Integral())

    h_bkg_dvv_rebin = h_bkg_dvv.Rebin(len(bins)-1, 'h_bkg_dvv_rebin', bins)
    move_overflow_into_last_bin(h_bkg_dvv_rebin)

    h_bkg_uncert = ROOT.TH1D('h_bkg_uncert', '', nbins, bins)
    for i,v in enumerate(bkg_uncert):
        h_bkg_uncert.SetBinContent(i+1, v)

    # now signals. grab the printout and put in signals.h for the fitting code to pick up
    fns = glob(in_trees)
    fns = sorted(x for x in fns if '_2015' not in x) + sorted(x for x in fns if '_2015' in x)
    hs_sig = []
    for ifn, fn in enumerate(fns):
        isample = -(ifn+1)
        name = os.path.basename(fn).replace('.root', '')
        print 'samples.push_back({%i, "%s", 0, 0});' % (isample, name)
        sig_f = ROOT.TFile(fn)
        sig_t = sig_f.Get('mfvMiniTree/t')

        f.cd()

        h_dbv_name = 'h_signal_%i_dbv' % isample
        h_dbv = ROOT.TH1D(h_dbv_name, name, 1250, 0, 2.5)
        sig_t.Draw('dist0>>%s' % h_dbv_name, 'weight*(nvtx==1)')

        h_dvv_name = 'h_signal_%i_dvv' % isample
        h_dvv = ROOT.TH1D(h_dvv_name, name, 4000, 0, 4)
        sig_t.Draw('svdist>>%s' % h_dvv_name, 'weight*(nvtx>=2)')

        h_dphi_name = 'h_signal_%i_dphi' % isample
        h_dphi = ROOT.TH1D(h_dphi_name, name, 10, -3.15, 3.15)
        sig_t.Draw('svdphi>>%s' % h_dphi_name, 'weight*(nvtx>=2)')

        h_norm = ROOT.TH1D('h_signal_%i_norm' % isample, name, 2, 0, 2)
        norm = 1e-3 / sig_f.Get('mfvWeight/h_sums').GetBinContent(1)  # 1 fb xsec in pb / number of events read, int lumi will be added in ToyThrower
        h_norm.SetBinContent(1, norm)
        h_norm.SetBinContent(2, norm)

        h_dvv_rebin = h_dvv.Rebin(len(bins)-1, 'h_signal_%i_dvv_rebin' % isample, bins)
        move_overflow_into_last_bin(h_dvv_rebin)

        h_uncert = ROOT.TH1D('h_signal_%i_uncert' % isample, '', nbins, bins)
        for i,v in enumerate(sig_uncert):
            h_uncert.SetBinContent(i+1, v)

        hs_sig += [h_dbv, h_dvv, h_dphi, h_norm, h_dvv_rebin, h_uncert]

    f.Write()
    f.Close()

def draw():
    ps = plot_saver(plot_dir('o2t_templates_run2'), size=(600,600))

    whiches = [
        ('multijet', [
            (-39, ROOT.kRed,      'multijet M = 800 GeV, #tau = 100 #mum'),
            (-46, ROOT.kGreen+2,  'multijet M = 800 GeV, #tau = 300 #mum'),
            (-53, ROOT.kBlue,     'multijet M = 800 GeV, #tau = 1 mm'),
            (-60, ROOT.kMagenta,  'multijet M = 800 GeV, #tau = 10 mm'),
            (-67, ROOT.kOrange+2, 'multijet M = 800 GeV, #tau = 30 mm'),
            ]),
        ('dijet', [
            ( -5, ROOT.kRed,      'dijet M = 800 GeV, #tau = 100 #mum'),
            (-12, ROOT.kGreen+2,  'dijet M = 800 GeV, #tau = 300 #mum'),
            (-19, ROOT.kBlue,     'dijet M = 800 GeV, #tau = 1 mm'),
            (-26, ROOT.kMagenta,  'dijet M = 800 GeV, #tau = 10 mm'),
            (-33, ROOT.kOrange+2, 'dijet M = 800 GeV, #tau = 30 mm'),
            ]),
        ]

    f = ROOT.TFile(out_fn)

    def fmt(h, name, color, save=[]):
        binning = to_array(0., 0.04, 0.07, 0.15)
        h = h.Rebin(len(binning)-1, name, binning)
        h.Sumw2()
        h.SetStats(0)
        h.SetLineWidth(3)
        h.SetLineColor(color)
        h.SetTitle(';d_{VV} (cm);event rate (unit norm.)')
        move_overflow_into_last_bin(h)
        h.Scale(1./h.Integral(0,h.GetNbinsX()+2))
        save.append(h)
        return h
    
    for which_name, which in whiches: 
        hbkg = fmt(f.Get('h_bkg_dvv'), 'bkg', ROOT.kBlack)
        hbkg.Draw('hist e')
        hbkg.GetYaxis().SetRangeUser(0,1.5)

        leg = ROOT.TLegend(0.142, 0.657, 0.702, 0.857)
        leg.SetBorderSize(0)
        leg.AddEntry(hbkg, 'Simulated d_{VV}^{C}', 'LE')

        for isample, color, title in which:
            h = fmt(f.Get('h_signal_%i_dvv' % isample), title, color)
            h.Draw('hist e same')
            leg.AddEntry(h, title, 'LE')

        leg.Draw()

        ps.save(which_name, log=False)

    
if __name__ == '__main__':
    if 'make' in sys.argv:
        make()
    elif 'draw' in sys.argv:
        draw()
    elif 'combine_datacard' in sys.argv:
        combine_datacard()
    else:
        print 'dunno'
