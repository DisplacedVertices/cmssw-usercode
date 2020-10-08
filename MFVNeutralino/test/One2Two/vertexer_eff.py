import os
from JMTucker.Tools.ROOTTools import *

version = 'V27p1Bm'
#path = '/uscms_data/d2/tucker/crab_dirs/VertexerPairEffs' + version.capitalize()
#path = '/uscms/home/joeyr/crabdirs/VertexerPairEffsV27p1Bm'
#path = '/uscms/home/joeyr/crabdirs/VertexerPairEffsV27p1Bm_BEnrichedLowHTQCD'
#path = '/uscms/home/joeyr/crabdirs/VertexerPairEffsWithBSamplesV27p1Bm'
#path = '/uscms/home/joeyr/crabdirs/VertexerPairEffsWithBSamplesAllMCV27p1Bm'
path = '/uscms/home/joeyr/crabdirs/VertexerPairEffsAllMCV27p1Bm'

set_style()

def write(font, size, x, y, text):
    w = ROOT.TLatex()
    w.SetNDC()
    w.SetTextFont(font)
    w.SetTextSize(size)
    w.DrawLatex(x, y, text)
    return w

for is_mc in [True]:
    for year in [2017,2018]:
        in_fn = os.path.join(path, ('background_btagpresel_%s.root' if is_mc else 'JetHT%s.root') % year)
        in_f = ROOT.TFile(in_fn)

        for ntkseeds in True, False:
            ps = plot_saver(plot_dir('VertexerPairEffs%s/vertexer_pair_effs%s_%s%s' % (version.capitalize(), '' if is_mc else '_data', year, '_ntkseeds' if ntkseeds else '')), size=(700,700), log=False)
            fh = ROOT.TFile('vpeffs%s_%s_%s%s.root' % ('' if is_mc else '_data', year, version, '_ntkseeds' if ntkseeds else ''), 'recreate')
            h_merges, h_adds = {}, {}

            for itk in 3,4,5:
                d = in_f.Get('mfvVertexerPairEffs%iTkSeed' % itk if ntkseeds else 'mfvVertexerPairEffs')
                h_merge = d.Get('h_merge_d2d_mintk0_maxtk%i' % itk)
                h_erase = d.Get('h_erase_d2d_mintk0_maxtk%i' % itk)
                h_pairs = d.Get('h_pairs_d2d_mintk0_maxtk%i' % itk)

                for h in h_merge, h_erase, h_pairs:
                    h.Rebin(10)

                h_merges[itk] = h_merge.Clone('maxtk%i_merge' % itk)
                h_adds[itk] = h_merge.Clone('maxtk%i' % itk)
                h_adds[itk].Add(h_erase)

                for ih,h in enumerate((h_adds[itk], h_merges[itk])):
                    is_merge = h == h_merges[itk]
                    h.Divide(h, h_pairs, 1,1,'B')
                    for i in xrange(1, h.GetNbinsX()+2):
                        h.SetBinContent(i, 1-h.GetBinContent(i))
#                    h.Scale(1./h.GetBinContent(h.GetNbinsX()))
                    h.SetTitle('maxtk%i%s;d_{VV} (cm);efficiency' % (itk, ' merge' if is_merge else ''))
                    h.GetYaxis().SetRangeUser(0,1.05)
                    h.SetLineColor(ROOT.kBlue if is_merge else ROOT.kGreen+2)
                    h.SetStats(0)
                    if ih == 0: 
                        h.Draw()
                    else:
                        h.Draw('sames')

                # FIXME consider replacing the plots by their erf fit (and ideally save the original as well + overlay it!)
                #h_adds_fit = ROOT.TF1("fit_adds_maxtk%i" % itk, "[0] + 0.5*[1]*(1+TMath::Erf( (x - 0.005) / 0.2))", 0.0, 1)
                #h_adds[itk].Fit("fit_adds_maxtk%i" % itk)
                #h_adds_fit.Draw("sames")

                l = ROOT.TLegend(0.50,0.55,0.85,0.70)
                l.AddEntry(h_merges[itk], '1 - merge / pairs')
                l.AddEntry(h_adds[itk], '1 - (merge + erase) / pairs')
                l.SetFillColor(0)
                l.Draw()

                ps.save('h_eff_maxtk%i' % itk)
                fh.cd()
                h_adds[itk].Write()
                h_merges[itk].Write()

            l = ROOT.TLegend(0.50,0.15,0.85,0.30)
            for ih, (itk, color) in enumerate(zip((3,4,5), (ROOT.kRed, ROOT.kBlue, ROOT.kGreen+2))):
                h = h_adds[itk]
                h.SetLineColor(color)
                h.SetLineWidth(3)
                h.SetTitle(';d_{VV} (cm);Efficiency')
                h.GetXaxis().SetRangeUser(0,0.4)
                if ih == 0:
                    h.Draw('hist E1')
                else:
                    h.Draw('hist E1 sames')
                l.AddEntry(h, '%i-track' % itk)
            l.SetFillColor(0)
            l.Draw()
            ps.save('efficiency')

            if not ntkseeds:
                h = h_adds[3]
                h.GetXaxis().SetRangeUser(0,0.4)
                h.Draw('hist')
                if not is_mc and year == '2015p6':
                    write(61, 0.050, 0.098, 0.913, 'CMS')
                    write(52, 0.035, 0.200, 0.913, 'Preliminary')
                    write(42, 0.050, 0.560, 0.913, '38.5 fb^{-1} (13 TeV)')
                ps.save('efficiency3')

                ROOT.TH1.AddDirectory(0)

                for ntk in [3, 4, 5]:
                    h2 = ROOT.TFile('vpeffs%s_%s_%s_ntkseeds.root' % ('' if is_mc else '_data', year, version)).Get('maxtk%s' % ntk)
                    if not is_mc and year == '2015p6':
                        h2.Scale(1./h2.GetMaximum())
                    h2.SetLineWidth(3)
                    h.GetXaxis().SetRangeUser(0,0.4)
                    h.Draw('hist')
                    h2.Draw('hist sames')
                    l = ROOT.TLegend(0.50,0.15,0.85,0.30)
                    l.AddEntry(h, 'default')
                    l.AddEntry(h2, '%s-track variation' % ntk)
                    l.Draw()
                    if not is_mc and year == '2015p6':
                        write(61, 0.050, 0.098, 0.913, 'CMS')
                        write(52, 0.035, 0.200, 0.913, 'Preliminary')
                        write(42, 0.050, 0.560, 0.913, '38.5 fb^{-1} (13 TeV)')
                    ps.save('compare_efficiency_%s-track' % ntk)
    
                    ratio = h2.Clone('ratio')
                    ratio.Divide(h)
                    ratio.GetYaxis().SetRangeUser(0.5, 6)
                    ratio.GetXaxis().SetRangeUser(0,0.4)
                    ratio.Draw('hist')
                    ps.save('variation_ratio_%s-track' % ntk)
