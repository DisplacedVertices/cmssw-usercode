from array import array
from JMTucker.Tools.ROOTTools import ROOT, plot_saver, set_style, differentiate_stat_box, sort_histogram_pair
set_style()
ROOT.gStyle.SetOptStat(100)
ps = plot_saver('plots/btag_counting', size=(600,600))

btags = 'CSVpt50bd0p244 CSVpt50bd0p679 CSVpt50bd0p898 JPpt50bd0p275 JPpt50bd0p545 JPpt50bd0p79 JBPpt50bd1p33 JBPpt50bd2p55 JBPpt50bd3p74 SSVHEpt50bd1p74 SSVHEpt50bd3p05 SSVHPpt50bd2p0 TCHEpt50bd1p7 TCHEpt50bd3p3 TCHEpt50bd10p2 TCHPpt50bd1p19 TCHPpt50bd1p93 TCHPpt50bd3p41'.split()
taus = '0 10um 100um 1mm 9p9mm'.split()
taus = [(tau, ROOT.TFile('mfvnu_btag_counting_tau%s.root' % tau)) for tau in taus]
tau_nice = {'0': '0', '10um': '10 #mum', '100um': '100 #mum', '1mm': '1 mm', '9p9mm': '9.9 mm'}
colors = [1,2,3,4,6]
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

