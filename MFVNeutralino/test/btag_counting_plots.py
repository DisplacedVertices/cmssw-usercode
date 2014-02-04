from array import array
from JMTucker.Tools.ROOTTools import ROOT, plot_saver, set_style, differentiate_stat_box, sort_histogram_pair
set_style()
ROOT.gStyle.SetOptStat(100)
ps = plot_saver('plots/btag_counting', size=(600,600))

btags = 'CSVpt30bd0p244 CSVpt30bd0p679 CSVpt30bd0p898 JPpt30bd0p275 JPpt30bd0p545 JPpt30bd0p79 JBPpt30bd1p33 JBPpt30bd2p55 JBPpt30bd3p74 SSVHEpt30bd1p74 SSVHEpt30bd3p05 SSVHPpt30bd2p0 TCHEpt30bd1p7 TCHEpt30bd3p3 TCHEpt30bd10p2 TCHPpt30bd1p19 TCHPpt30bd1p93 TCHPpt30bd3p41'.split()
taus = '0000 0010 0100 1000 4000 9900'.split()
taus = [(tau, ROOT.TFile('mfv_reco_counting_gluino_tau%sum_M400.root' % tau)) for tau in taus]
tau_nice = {'0000': '0', '0010': '10 #mum', '0100': '100 #mum', '1000': '1 mm', '4000': '4 mm', '9900': '9.9 mm'}
colors = [1,2,3,4,6,46]
def btag_color(btag):
    if 'CSV' in btag:
        return ROOT.kRed
    elif 'JP' in btag:
        return ROOT.kBlue
    elif 'JBP' in btag:
        return ROOT.kGreen
    elif 'SSV' in btag:
        return ROOT.kCyan
    elif 'TCHE' in btag:
        return ROOT.kOrange
    elif 'TCHP' in btag:
        return ROOT.kMagenta
    
xs = [1e-3, 10e-3, 100e-3, 1, 9.9]
yys = []
for btag in btags:
    print btag
    hs = [(tau, tau_file.Get('%s/h_ndisc' % btag)) for tau, tau_file in taus]
    opt = ''
    leg = ROOT.TLegend(0.520, 0.638, 0.863, 0.866)
    m = 0
    for ih, ((tau, h), color) in enumerate(zip(hs, colors)):
#        print tau, h.GetMean()
        h.SetTitle(';# b-tagged jets (%s);frac. of events' % btag)
        h.SetLineColor(color)
        h.SetLineWidth(3)
        h.GetXaxis().SetRangeUser(0, 10)
        h.GetYaxis().SetTitleOffset(1.5)
        h.Scale(1./h.GetEntries())
        m = max(h.GetMaximum(), m)
        h.SetStats(0)
        h.Draw(opt)
        leg.AddEntry(h, '#tau_{0} = %s, mean = %.2f' % (tau_nice[tau], h.GetMean()), 'L')
        opt = 'sames'
    for tau, h in hs:
        h.SetMaximum(m*1.1)
    ys = [h.GetMean() for tau, h in hs]
    yys.append((btag, ys))
    leg.SetTextFont(42)
    leg.Draw()
    ps.save(btag)

for wp, yrange in ((0, (0,5)), (0, (0,5)), (1, (0,4)), (2, (0,3))): # yes the first one is there twice
    leg = ROOT.TLegend(0.143, 0.140, 0.455, 0.339)
    gs = []
    opt = 'ALP'
    #yys.sort(key=lambda l: -max(l[1]))
    to_leg = []
    for i,(btag, ys) in enumerate(yys): #reversed(range(len(yys))):
        btag,ys = yys[i]
        if i % 3 != wp:
            continue
        g = ROOT.TGraph(5, array('d',xs), array('d',ys))
        g.SetTitle(';#tau_{0} (mm);mean of #-b-jets distribution')
        gs.append(g)
        g.SetMarkerStyle(20)
        g.SetMarkerSize(1.1)
        color = btag_color(btag)
        g.SetMarkerColor(color)
        g.SetLineWidth(2)
        g.SetLineColor(color)
        g.Draw(opt)
        ps.c.Update()
        g.GetYaxis().SetRangeUser(*yrange)
        g.GetXaxis().SetTitleOffset(1.2)
        g.GetYaxis().SetTitleOffset(1.2)
        g.Draw(opt)
        opt = 'LP'
        to_leg.append((ys[0], (g, btag, 'LP')))
    to_leg.sort(key=lambda x: x[0], reverse=True)
    for y,args in to_leg:
        leg.AddEntry(*args)
    leg.SetTextFont(42)
    leg.Draw()
    ps.c.SetLogx()
    ps.save('means_wp%i' % wp, log=False)

