from JMTucker.MFVNeutralino.MiniTreeBase import *
ps = plot_saver('plots/phiplot_zzz', size=(800,800))

bad = [1,3,7,67,177]
h_bad   = ROOT.TH1F('h_bad', '', 5, 0, 3.141593)
model = [4,10,29,70,136]
h_model = ROOT.TH1F('h_model', '', 5, 0, 3.141593)

for l,h in ((bad,h_bad),(model,h_model)):
    s = sum(l)/251.
    for i in xrange(5):
        l[i] /= s
        h.SetBinContent(i+1, l[i])
        h.SetBinError(i+1, 1)


f,t = get_f_t('trees/MultiJetPk2012.root')
t.Draw('abs(svdphi)>>h_data(5,0,3.141593)', 'nvtx>=2')
h_data = ROOT.h_data
#for i in xrange(5):
    
for (h,c) in ((h_bad, ROOT.kBlue), (h_model,ROOT.kRed), (h_data, 1)):
    h.SetLineWidth(2)
    h.SetLineColor(c)
    h.SetStats(0)
    h.SetTitle(';#Delta#phi_{VV};events')
    h.GetYaxis().SetTitleOffset(1.25)

h_bad.Draw()
h_model.Draw('same')
h_data.Draw('same e')

leg = ROOT.TLegend(0.148, 0.633, 0.691, 0.856)
leg.AddEntry(h_data,  'data',      'LE')
leg.AddEntry(h_model, 'jet model', 'LE')
leg.AddEntry(h_bad,   'bootstrapped from two-vertex MC', 'LE')
leg.SetBorderSize(0)
leg.SetTextFont(42)
leg.Draw()

ps.save('duh')
