import os
from array import array
from JMTucker.Tools.ROOTTools import *
import JMTucker.Tools.Samples as Samples
import JMTucker.MFVNeutralino.AnalysisConstants as ac

set_style()
rainbow_palette()

def arr(l):
    return array('d', l)

def write(font, size, x, y, text):
    w = ROOT.TLatex()
    w.SetNDC()
    w.SetTextFont(font)
    w.SetTextSize(size)
    w.DrawLatex(x, y, text)
    return w

hs = []

def get_h(s):
    root_file_dir = 'HistosV20_rebin_for_paper'
    histogram_path = 'mfvVertexHistosWAnaCuts/h_svdist2d'

    fn = os.path.join(root_file_dir, s.name + '.root')
    s.f = ROOT.TFile(fn)
    s.in_h = s.f.Get(histogram_path)
    bins = arr([0, 0.2, 0.4, 0.6, 0.8, 1, 2])
    h = s.h = s.in_h.Rebin(len(bins) - 1, s.in_h.GetName() + '_rebin', bins)
    #h.Sumw2()
    h.SetStats(0)
    h.SetLineWidth(2)
    if hasattr(s, 'partial_weight'):
        h.Scale(s.partial_weight * ac.int_lumi * ac.scale_factor)

    h.SetTitle(';d_{VV} (mm);Events')

    # overflow in last
    nbins = h.GetNbinsX()
    cn, en   = h.GetBinContent(nbins),   h.GetBinError(nbins)
    cn1, en1 = h.GetBinContent(nbins+1), h.GetBinError(nbins+1)
    h.SetBinContent(nbins, cn + cn1)
    h.SetBinError  (nbins, (en**2 + en1**2)**0.5)
    h.SetBinContent(nbins+1, 0)
    h.SetBinError  (nbins+1, 0)

    xax = h.GetXaxis()
    xax.SetTitleSize(0.05)
    xax.SetLabelSize(0.04)
    xax.SetTitleOffset(0.91)

    yax = h.GetYaxis()
    yax.SetTitleOffset(1.)
    yax.SetTitleSize(0.05)
    yax.SetLabelSize(0.04)
    yax.SetRangeUser(0.1, 300)

def clone_add(name, color, samples):
    h = samples[0].h.Clone(name)
    if color is not None:
        h.SetLineColor(color)
        h.SetFillColor(color)
    for s in samples[1:]:
        h.Add(s.h)
    return h
    
data_samples = Samples.data_samples
background_samples = Samples.smaller_background_samples + Samples.leptonic_background_samples + Samples.ttbar_samples + Samples.qcd_samples
signal_sample = Samples.mfv_neutralino_tau1000um_M0400
signal_sample.cross_section = 0.001
all_samples = data_samples + background_samples + [signal_sample]

for s in all_samples:
    get_h(s)

h_data = clone_add('h_data', None, data_samples)
#h_data.SetBinErrorOption(ROOT.TH1.kPoisson)

h_qcd = clone_add('h_qcd', ROOT.kBlue-9, Samples.qcd_samples)
h_rest = clone_add('h_rest', ROOT.kBlue-7, Samples.ttbar_samples + Samples.smaller_background_samples + Samples.leptonic_background_samples)

integ = h_qcd.Integral() + h_rest.Integral()
scale = 251./integ
h_qcd.Scale(scale)
h_rest.Scale(scale)

h_qcdplusrest = h_qcd.Clone('h_qcdplusrest')
h_qcdplusrest.Add(h_rest)

s, v = 0., 0.
for ibin in xrange(0, h_qcdplusrest.GetNbinsX()+2):
    s += h_qcdplusrest.GetBinContent(ibin)
    v += h_qcdplusrest.GetBinError(ibin)**2
    print ibin, h_qcdplusrest.GetBinContent(ibin), h_qcdplusrest.GetBinError(ibin)
print s, '+-', v**0.5

c = ROOT.TCanvas('c', '', 800, 800)
c.SetBottomMargin(0.12)
c.SetLogy()

h_qcdplusrest.Draw('hist')
h_rest.Draw('hist same')
h_qcdplusrest.Draw('axis same')

xax = h_qcdplusrest.GetXaxis()
yax = h_qcdplusrest.GetYaxis()
yax.SetRangeUser(0.1, 300)

h_uncert = h_qcdplusrest.Clone('h_uncert')
h_uncert.SetLineColor(1)
h_uncert.SetFillColor(1)
h_uncert.SetFillStyle(3002)
h_uncert.Draw('E2 same')

h_signal = signal_sample.h
h_signal.SetLineWidth(2)
h_signal.SetLineColor(8)
h_signal.Draw('same hist')

# this gets rid of the stupid color on the stupid x-axis
h_dummy = h_uncert.Clone()
for i in xrange(1, h_dummy.GetNbinsX()+1):
    h_dummy.SetBinContent(i, 0)
    h_dummy.SetBinError(i, 0)
h_dummy.Draw('same')

leg = ROOT.TLegend(0.381, 0.609, 0.871, 0.852)
#leg = ROOT.TLegend(0.438, 0.641, 0.875, 0.869)
leg.SetTextFont(42)
leg.SetBorderSize(0)
leg.AddEntry(h_qcdplusrest, 'Multijet events', 'F')
leg.AddEntry(h_rest, 't#bar{t}, single t, V+jets, t#bar{t}+V, VV', 'F')
leg.AddEntry(h_uncert, 'MC stat. uncertainty', 'F')
leg.AddEntry(h_signal, 'Signal: #sigma = 1 fb,', 'L')
leg.Draw()

entryt = ROOT.TLatex(.670,.592, 'c#tau = 1 mm, M = 400 GeV')
entryt.SetNDC()
entryt.SetTextAlign(22)
entryt.SetTextFont(43)
entryt.SetTextSize(26)
entryt.Draw()

cms = write(61, 0.050, 0.099, 0.913, 'CMS')
sim = write(52, 0.040, 0.212, 0.912, 'Simulation')
lum = write(42, 0.050, 0.586, 0.913, '17.6 fb^{-1} (8 TeV)')

# do a broken x axis. thanks root (throot)

boxcenter = 1.8
boxwidth = 0.02
boxy1 = 0.065
boxy2 = 0.14
box1 = ROOT.TBox(boxcenter-boxwidth, boxy1, boxcenter+boxwidth, 3)
box1.SetLineColor(ROOT.kWhite)
box1.SetFillColor(ROOT.kWhite)
box1.Draw()

box2 = ROOT.TBox(1.74, 0.065, 2.1, 0.095)
box2.SetLineColor(ROOT.kWhite)
box2.SetFillColor(ROOT.kWhite)
box2.Draw()

#lab1 = ROOT.TText(1.714, 0.06989, '49.8')
#lab1.SetTextFont(xax.GetLabelFont())
#lab1.SetTextSize(xax.GetLabelSize())
#lab1.Draw()

lab2 = ROOT.TText(1.914, 0.06989, '50.0')
lab2.SetTextFont(xax.GetLabelFont())
lab2.SetTextSize(xax.GetLabelSize())
lab2.Draw()

lineslantdx = 0.009
lineybackoff = 0.01

line1 = ROOT.TLine(boxcenter-boxwidth-lineslantdx, boxy1+lineybackoff, boxcenter-boxwidth+lineslantdx, boxy2-lineybackoff)
line1.SetLineWidth(2)
line1.Draw()

line2 = ROOT.TLine(boxcenter+boxwidth-lineslantdx, boxy1+lineybackoff, boxcenter+boxwidth+lineslantdx, boxy2-lineybackoff)
line2.SetLineWidth(2)
line2.Draw()

name = 'plots/after_referee/dvv_log'
c.SaveAs(name + '.pdf')
c.SaveAs(name + '.png')
c.SaveAs(name + '.root')
del c
