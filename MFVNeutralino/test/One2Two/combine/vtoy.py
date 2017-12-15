import sys, os
from collections import defaultdict
from JMTucker.Tools.ROOTTools import *
from JMTucker.Tools.general import bool_from_argv
set_style()
ROOT.gStyle.SetOptStat(1110)
ROOT.gStyle.SetPadTopMargin(0.05)
ROOT.gStyle.SetPadBottomMargin(0.1)
ROOT.gStyle.SetPadLeftMargin(0.05)
ROOT.gStyle.SetPadRightMargin(0.02)

draw_individual_dists = bool_from_argv('draw_individual_dists')

if draw_individual_dists:
    ps = plot_saver(plot_dir('vtoy'), size=(400,300), log=False)
else:
    ps = plot_saver(plot_dir('vtoy'), size=(1200,500))

path = sys.argv[1]
fn = os.path.join(path, 'expected.root')
f = ROOT.TFile(fn)

limit_t = f.Get('limit')
limit_by_toy = {}
for _ in ttree_iterator(limit_t):
    limit_by_toy[limit_t.iToy] = limit_t.limit

limit_by_dist = defaultdict(list)
toys = f.Get('toys')
for ktoy in toys.GetListOfKeys():
    toy = ktoy.GetName()
    assert toy.startswith('toy_')
    itoy = int(toy.replace('toy_',''))

    a,b,c = x = [int(ktoy.ReadObj().get()['n_obs_binb%i'%i].getVal()) for i in 0,1,2]
    k = (sum(x), a,b,c)
    limit_by_dist[k].append(limit_by_toy[itoy])

dists = sorted(limit_by_dist.keys())

for dist in dists:
    l = limit_by_dist[dist]
    mn, mx = min(l), max(l)
    print dist, '%.3f %.3f %.3f' % (mn, mx, mx-mn)

hs = []
mv = max(max(x) for x in limit_by_dist.values())
print 'mv=',mv; mv2 = 0.8; assert mv < mv2; mv = mv2

for dist in dists:
    name = '%i:[%i,%i,%i]' % dist
    h = ROOT.TH1D(name, 'sum=%i, [%i,%i,%i];limit (fb);toys/0.0008' % dist, 1000, 0, mv)
    h.jmt_dist = dist
    hs.append(h)
    for v in limit_by_dist[dist]:
        h.Fill(v)
    if draw_individual_dists:
        h.Draw('hist')
        ps.c.Update()
        resize_stat_box(h, (0.2, 0.1))
        ps.save(name)

hs.sort(key=lambda h: -h.GetMaximum())

base_colors = [ROOT.kRed, ROOT.kGreen, ROOT.kBlue, ROOT.kMagenta, ROOT.kOrange, ROOT.kCyan]
color_pools = [range(3, -11, -1)+range(3, -11, -1) for c in base_colors]

for ih, h in enumerate(hs):
    n = h.jmt_dist[-1]
    if n >= len(base_colors):
        color = ROOT.kBlack
    else:
        color = base_colors[n] + color_pools[n].pop(0)

    h.SetTitle('')
    h.SetStats(0)
    h.SetLineWidth(2)
    h.SetLineColor(color)
    h.SetFillColor(color)
    h.GetYaxis().SetTitleOffset(0.6)

    if ih == 0:
        h.Draw('hist')
    else:
        h.Draw('hist same')

    t = h.jmt_t = ROOT.TText(h.GetMean(), h.GetMaximum()*1.03, h.GetName())
    t.SetTextColor(color)
    t.SetTextFont(63)
    t.SetTextSize(20)
    t.SetTextAngle(30)
    t.Draw()

y0,y1=0.3, 600
hs[0].GetYaxis().SetRangeUser(y0,y1)
h = ROOT.TH1D('hhh', '', 1000, 0, mv)
h.SetLineColor(1)
h.Draw('same')

quantiles = [float(line.split()[-1]) for line in open(os.path.join(path, 'results')) if '16.0%' in line or '50.0%' in line or '84.0%' in line]
ll = []
for iq,q in enumerate(quantiles):
    l = ROOT.TLine(q,y0,q,y1)
    ll.append(l)
    l.SetLineWidth(2)
    l.SetLineColor(1)
    if iq != 1:
        l.SetLineStyle(2)
    l.Draw()

ps.save('overlay')

