import os, sys
from JMTucker.Tools.ROOTTools import *
set_style()
ps = plot_saver('plots/phitest', log=False)

ROOT.TH1.AddDirectory(0)

fns = []
for fn in sys.argv[1:]:
    if not os.path.isfile(fn):
        continue
    fns.append((fn, int(os.path.basename(fn).replace('vertexer_debug_', '').replace('.root', ''))))

fns.sort(key=lambda x: x[1])

pvals = []

for fn, job in fns:
    f = ROOT.TFile(fn)

    h_nev = f.Get('mfvVertices/h_phitest_nev')
    h_nvtx = f.Get('mfvVertices/h_phitest_nvtx')
    h_mean = f.Get('mfvVertices/phitest_mean')
    h_rms = f.Get('mfvVertices/phitest_rms')
    h_p0 = f.Get('mfvVertices/phitest_p0')
    h_p1 = f.Get('mfvVertices/phitest_p1')

    hs = (h_nev, h_nvtx, h_mean, h_rms, h_p0, h_p1)
    for h in hs:
        h.SetStats(0)

    h_nev.Draw()
    ps.save('h_nev_%i' % job)

    max_bin = 0
    for ibin in xrange(1, h_nvtx.GetNbinsX()+1):
        if h_nvtx.GetBinContent(ibin) <= 0:
            max_bin = ibin-1
            break

    h_nvtx.Draw()
    ps.save('h_nvtx_%i' % job)

    h_mean.GetXaxis().SetRangeUser(0, max_bin)
    h_mean.Draw()
    l = ROOT.TLine(0, 0, max_bin, 0)
    l.Draw()
    ps.save('h_mean_%i' % job)
    
    h_rms.GetXaxis().SetRangeUser(0, max_bin)
    h_rms.Draw()
    y = 2*3.1416/12**0.5
    l = ROOT.TLine(0, y, max_bin, y)
    l.Draw()
    ps.save('h_rms_%i' % job)
    
    h_p0.GetXaxis().SetRangeUser(0, max_bin)
    h_p0.Draw()
    ps.save('h_p0_%i' % job)

    h_p1.GetXaxis().SetRangeUser(0, max_bin)
    h_p1.Draw()
    y = 0
    l = ROOT.TLine(0, y, max_bin, y)
    l.Draw()
    ps.save('h_p1_%i' % job)

    phi = f.Get('mfvVertices/h_noshare_vertex_phi')
    phi.Scale(1./phi.Integral())
    pval = cumulative_histogram(phi)
    for ibin in xrange(1, pval.GetNbinsX()+1):
        pval.SetBinError(ibin, 0)
    pval.SetName('pval_%i' % job)
    pvals.append(pval)

pvals[0].Draw('hist')
for p in pvals[1:]:
    p.Draw('hist same')
l = ROOT.TLine(-3.1416,1,3.1416,0)
l.Draw()
ps.save('pvals')
