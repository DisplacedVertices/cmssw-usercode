from JMTucker.MFVNeutralino.MiniTreeBase import *
ROOT.TH1.AddDirectory(1)

in_fn = sys.argv[1]
in_f = ROOT.TFile(in_fn)

f = ROOT.TFile('throwhists.root', 'recreate')

h_bkg_dbv  = to_TH1D(in_f.Get('h_1v_dbv') , 'h_bkg_dbv')
h_bkg_dvv  = to_TH1D(in_f.Get('h_c1v_dvv'), 'h_bkg_dvv')

h_bkg_dphi = ROOT.TH1D('h_bkg_dphi', '', 100, 0, pi)
f_dphi = in_f.Get('f_dphi')
for ibin in xrange(1, h_bkg_dphi.GetNbinsX()+1):
    a = h_bkg_dphi.GetXaxis().GetBinLowEdge(ibin)
    b = h_bkg_dphi.GetXaxis().GetBinLowEdge(ibin+1)
    h_bkg_dphi.SetBinContent(ibin, f_dphi.Integral(a,b)/(b-a))

n1v = 1100.
n2v = 1.
h_bkg_dbv.Scale(n1v/h_bkg_dbv.Integral())
for h in h_bkg_dvv, h_bkg_dphi:
    h.Scale(n2v/h.Integral())


fns = glob('trees/mfv*root')
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
    n1v = sig_t.Draw('dist0>>%s' % h_dbv_name, 'nvtx==1')

    h_dvv_name = 'h_signal_%i_dvv' % isample
    h_dvv = ROOT.TH1D(h_dvv_name, name, 4000, 0, 4)
    n2v = sig_t.Draw('svdist>>%s' % h_dvv_name, 'nvtx>=2')

    h_dphi_name = 'h_signal_%i_dphi' % isample
    h_dphi = ROOT.TH1D(h_dphi_name, name, 10, -3.15, 3.15)
    sig_t.Draw('svdphi>>%s' % h_dphi_name, 'nvtx>=2')

    h_norm = ROOT.TH1D('h_signal_%i_norm' % isample, name, 2, 0, 2)
    norm = 1e-3 / sig_f.Get('mfvWeight/h_sums').GetBinContent(1)  # 1 fb xsec in pb / number of events read, int lumi will be added in ToyThrower
    h_norm.SetBinContent(1, norm * n1v)
    h_norm.SetBinContent(2, norm * n2v)

    hs_sig += [h_dbv, h_dvv, h_dphi, h_norm]

f.Write()
f.Close()
