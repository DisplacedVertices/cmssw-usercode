import os
from JMTucker.Tools.ROOTTools import *

is_mc = True
version = 'v20m'
path = '/uscms_data/d2/tucker/crab_dirs/VertexerPairEffs' + version.capitalize()
year = '2017'
ntkseeds = False

set_style()
ps = plot_saver(plot_dir('VertexerPairEffs%s/vertexer_pair_effs%s_%s%s' % (version.capitalize(), '' if is_mc else '_data', year, '_ntkseeds' if ntkseeds else '')), size=(700,700), log=False)

if is_mc:
    in_fn = os.path.join(path, 'background_%s.root' % year)
else:
    in_fn = os.path.join(path, 'JetHT%s.root' % year)

f = ROOT.TFile(in_fn)
fh = ROOT.TFile('vpeffs%s_%s_%s%s.root' % ('' if is_mc else '_data', year, version, '_ntkseeds' if ntkseeds else ''), 'recreate')

def write(font, size, x, y, text):
    w = ROOT.TLatex()
    w.SetNDC()
    w.SetTextFont(font)
    w.SetTextSize(size)
    w.DrawLatex(x, y, text)
    return w

for itk in [3,4,5]:
    h_merge = f.Get('mfvVertexerPairEffs%s/h_merge_d2d_mintk0_maxtk%i' % ('%iTkSeed' % itk if ntkseeds else '', itk))
    h_pairs = f.Get('mfvVertexerPairEffs%s/h_pairs_d2d_mintk0_maxtk%i' % ('%iTkSeed' % itk if ntkseeds else '', itk))
    h_erase = f.Get('mfvVertexerPairEffs%s/h_erase_d2d_mintk0_maxtk%i' % ('%iTkSeed' % itk if ntkseeds else '', itk))

    h_merge.Rebin(10)
    h_pairs.Rebin(10)
    h_erase.Rebin(10)

    h_add_eff = h_merge.Clone('maxtk%i' % itk)
    h_add_eff.Add(h_erase)
    h_add_eff.Divide(h_add_eff, h_pairs, 1,1,'B')
    for i in range(1, h_add_eff.GetNbinsX()+2):
        h_add_eff.SetBinContent(i, 1-h_add_eff.GetBinContent(i))
    h_add_eff.Scale(1./h_add_eff.GetBinContent(h_add_eff.GetNbinsX()))
    h_add_eff.SetTitle('maxtk%i;d_{VV} (cm);efficiency' % itk)
    h_add_eff.GetYaxis().SetRangeUser(0,1.05)
    h_add_eff.SetLineColor(ROOT.kGreen+2)
    h_add_eff.SetStats(0)
    h_add_eff.Draw()

    h_merge_eff = h_merge.Clone('maxtk%i_merge' % itk)
    h_merge_eff.Divide(h_merge_eff, h_pairs, 1,1,'B')
    for i in range(1, h_merge_eff.GetNbinsX()+2):
        h_merge_eff.SetBinContent(i, 1-h_merge_eff.GetBinContent(i))
    h_merge_eff.Scale(1./h_merge_eff.GetBinContent(h_merge_eff.GetNbinsX()))
    h_merge_eff.SetTitle('maxtk%i merge;d_{VV} (cm);efficiency' % itk)
    h_merge_eff.GetYaxis().SetRangeUser(0,1.05)
    h_merge_eff.SetLineColor(ROOT.kBlue)
    h_merge_eff.SetStats(0)
    h_merge_eff.Draw('sames')

    l = ROOT.TLegend(0.50,0.55,0.85,0.70)
    l.AddEntry(h_merge_eff, '1 - merge / pairs')
    l.AddEntry(h_add_eff, '1 - (merge + erase) / pairs')
    l.SetFillColor(0)
    l.Draw()

    ps.save('h_eff_maxtk%i' % itk)
    fh.cd()
    h_add_eff.Write()
    h_merge_eff.Write()

fh.Close()

f = ROOT.TFile('vpeffs%s_%s_%s%s.root' % ('' if is_mc else '_data', year, version, '_ntkseeds' if ntkseeds else ''))

colors = [0, 0, 0, ROOT.kRed, ROOT.kBlue, ROOT.kGreen+2]
l = ROOT.TLegend(0.50,0.15,0.85,0.30)
for i in [3,4,5]:
    h = f.Get('maxtk%i'%i)
    h.SetStats(0)
    h.SetLineWidth(3)
    h.SetLineColor(colors[i])
    if i == 3:
        h.SetTitle(';d_{VV} (cm);Efficiency')
        h.GetXaxis().SetRangeUser(0,0.4)
        h.Draw('hist')
    else:
        h.Draw('hist sames')
    l.AddEntry(h, '%i-track'%i)
l.SetFillColor(0)
l.Draw()
ps.save('efficiency')

if not ntkseeds:
    h = f.Get('maxtk3')
    h.Draw('hist')
    if not is_mc and year == '2015p6':
        write(61, 0.050, 0.098, 0.913, 'CMS')
        write(52, 0.035, 0.200, 0.913, 'Preliminary')
        write(42, 0.050, 0.560, 0.913, '38.5 fb^{-1} (13 TeV)')
    ps.save('efficiency3')

    ROOT.TH1.AddDirectory(0)

    h2 = ROOT.TFile('vpeffs%s_%s_%s_ntkseeds.root' % ('' if is_mc else '_data', year, version)).Get('maxtk5')
    if not is_mc and year == '2015p6':
        h2.Scale(1./h2.GetMaximum())
    h2.SetLineWidth(3)
    h.Draw('hist')
    h2.Draw('hist sames')
    l = ROOT.TLegend(0.50,0.15,0.85,0.30)
    l.AddEntry(h, 'default')
    l.AddEntry(h2, 'variation')
    l.Draw()
    if not is_mc and year == '2015p6':
        write(61, 0.050, 0.098, 0.913, 'CMS')
        write(52, 0.035, 0.200, 0.913, 'Preliminary')
        write(42, 0.050, 0.560, 0.913, '38.5 fb^{-1} (13 TeV)')
    ps.save('compare_efficiency')
