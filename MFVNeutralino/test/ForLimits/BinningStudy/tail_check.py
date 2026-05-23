import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gErrorIgnoreLevel = ROOT.kError

N2V = {'bjet': 0.520, 'lep': 0.049}
FILES = {
    'bjet': '../BackgroundTemplates/bjet/2v_from_jets_run2_5track_default_ULV30BvetoLHTm.root',
    'lep':  '../BackgroundTemplates/lep/2v_from_jets_run2_5track_default_ULV30Lepm.root',
}

with open('/tmp/tail_result.txt', 'w') as out:
    for ch, fpath in FILES.items():
        f = ROOT.TFile(fpath)
        h = f.Get('h_c1v_sumdbv_w_errorbars')
        scale = N2V[ch] / h.Integral()
        nbins = h.GetNbinsX()
        tail = 0.0
        for i in range(nbins, 0, -1):
            tail += h.GetBinContent(i) * scale
            if tail >= 1e-3:
                line = '%s: x = %.3f cm  tail = %.2e events\n' % (ch, h.GetBinLowEdge(i), tail)
                out.write(line)
                break
        f.Close()
