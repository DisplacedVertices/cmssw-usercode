# Change the units on histograms for paper from cm to mm.

import os
import JMTucker.Tools.Samples as Samples
from JMTucker.Tools.ROOTTools import ROOT

in_dir = '/uscms/home/jchu/nobackup/crab_dirs/mfv_5313/HistosV20'
out_dir = 'HistosV20_rebin_for_paper'
os.system('mkdir -p %s' % out_dir)

samples = Samples.data_samples + Samples.smaller_background_samples + Samples.leptonic_background_samples + Samples.ttbar_samples + Samples.qcd_samples + [Samples.mfv_neutralino_tau1000um_M0400]
paths = ['mfvVertexHistosOnlyOneVtx/h_sv_best0_bsbs2ddist', 'mfvVertexHistosWAnaCuts/h_svdist2d']

for sample in samples:
    print sample.name
    in_f = ROOT.TFile(os.path.join(in_dir, sample.name + '.root'))
    out_f = ROOT.TFile(os.path.join(out_dir, sample.name + '.root'), 'recreate')

    for path in paths:
        in_h = in_f.Get(path)
        assert type(in_h) == ROOT.TH1F
        nbins = in_h.GetNbinsX()
        lo = in_h.GetBinLowEdge(1)
        assert abs(lo) < 1e-6
        hi = in_h.GetBinLowEdge(nbins+1)
        width = in_h.GetBinWidth(1)
        assert abs(lo + width*nbins - hi) < 1e-6

        dir = out_f.mkdir(os.path.dirname(path))
        dir.cd()
        
        title = in_h.GetTitle()
        title = title.replace('cm', 'mm')

        out_h = ROOT.TH1F(in_h.GetName(), title, nbins, 0, hi*10)
        out_h.Sumw2()

        for ibin in xrange(0, nbins+2):
            out_h.SetBinContent(ibin, in_h.GetBinContent(ibin))
            out_h.SetBinError  (ibin, in_h.GetBinError  (ibin))

        out_h.Write()

    in_f.Close()
    out_f.Write()
    out_f.Close()
