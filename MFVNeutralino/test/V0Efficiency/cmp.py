import sys, os
from JMTucker.Tools.ROOTTools import *
from JMTucker.Tools.Sample import norm_from_file
from JMTucker.Tools import Samples
set_style()

integ = lambda h: h.Integral(0,h.GetNbinsX()+2)

fit_range = {
    'h_vtx_rho': (0.2, 2),
    'h_track_dxybs': (-0.4, 0.4),
    'h_track_sigmadxy': (0, 0.025),
    }

x_range = {
    'h_vtx_rho': (0, 2.2),
    'h_track_dxybs': (-2, 2),
}

orig_y_range = {
    'h_vtx_rho': (0., 0.45),
    'h_track_dxybs': (0., 4.2),
    }

y_range = {
    'h_vtx_rho': (0, 2),
    'h_track_dxybs': (0, 2),
    'h_track_dxypv': (0, 2),
    'h_track_sigmadxy': (0, 9),
    'h_track_eta': (0, 3),
    'h_track_phi': (0, 2),
    'h_track_npxlayers': (0, 1),
    'h_track_nstlayers': (0, 2),
    'h_track_npxhits': (0, 2),
    'h_track_nsthits': (0, 2),
    }

ilumi_d = { # in /pb
'qcd': 38529.0,
'qcdht1000and1500': 38529.0,
'qcdht1000and1500_hip1p0_mit': 38529.0,

'JetHT2016B3': 5746.3,
'JetHT2016C':  2572.8,
'JetHT2016D':  4224.6,
'JetHT2016E':  3957.9,
'JetHT2016F':  3104.5,
'JetHT2016G':  7574.8,
'JetHT2016H2': 8434.6,
'JetHT2016H3':  216.0,

'ZeroBias2016B3': 12235.0*1e-6,
'ZeroBias2016C' :  1268.2*1e-6,
'ZeroBias2016D' :  1895.9*1e-6,
'ZeroBias2016E' :  3024.9*1e-6,
'ZeroBias2016F' :  1709.7*1e-6,
'ZeroBias2016G' :  3180.7*1e-6,
'ZeroBias2016H2':  5547.9*1e-6,
'ZeroBias2016H3':   181.0*1e-6,
}

for x,l in ('', ('B3', 'C', 'D', 'E', 'F', 'G', 'H2', 'H3')), ('BCD', ('B3', 'C', 'D')), ('EF', 'EF'), ('BCDEF', ('B3',) + tuple('CDEF')), ('H', ('H2', 'H3')), ('GH', ('G', 'H2', 'H3')):
    for y in 'ZeroBias', 'JetHT':
        ilumi_d[y + '2016' + x] = sum(ilumi_d[y + '2016' + z] for z in l)

def getit(path, fn):
    sname = os.path.basename(fn).replace('.root', '')
    if ilumi_d.has_key(sname):
        ilumi = ilumi_d[sname]
    else:
        sample = getattr(Samples, sname)
        assert sample.is_mc
        ilumi = sample.int_lumi(fn)
    f = ROOT.TFile(fn)
    h = f.Get('%s/hsig' % path).Clone(sname)
    h.SetDirectory(0)
    #print integ(h), ilumi
    h.Scale(1./ilumi)
    h.GetYaxis().SetTitle(h.GetYaxis().GetTitle() + '/pb^{-1}')
    h.GetYaxis().SetTitleOffset(1.25)
    return fn, sname, f, h

cuts = sys.argv[1]
path = sys.argv[2]
fn1, name1, f1, h1 = getit(path, sys.argv[3])
fn2, name2, f2, h2 = getit(path, sys.argv[4])
#i1, i2 = integ(h1), integ(h2)

h1.SetLineColor(2)
h2.SetLineColor(4)
if orig_y_range.has_key(path):
    for h in h1, h2:
        h.GetYaxis().SetRangeUser(*orig_y_range[path])

ps = plot_saver(plot_dir('v0bkgsub/!!cmp/%s_%s_%s_%s' % (cuts, path, name1, name2)), size=(600,600))

draw_in_order(((h1,h2), 'hist e'), True)
ps.c.Update()
differentiate_stat_box(h1, 0, new_size=(0.2,0.2))
differentiate_stat_box(h2, 1, new_size=(0.2,0.2))
ps.save('cmp')

g = ROOT.TGraphAsymmErrors(h1, h2, 'pois')
g.Draw('AP')
g.SetLineColor(ROOT.kBlue)
if 0:
    if fit_range.has_key(path):
        fcn = ROOT.TF1('fcn', 'pol1', *fit_range[path])
        res = g.Fit(fcn, 'RNSQ')
    else:
        fcn = ROOT.TF1('fcn', 'pol1')
        res = g.Fit(fcn, 'NSQ')
    if res.Prob() > 1e-3:
        fcn.Draw('same')
g.GetXaxis().SetRangeUser(h1.GetXaxis().GetXmin(), h1.GetXaxis().GetXmax())
g.GetXaxis().SetTitle(h1.GetXaxis().GetTitle())
g.GetYaxis().SetTitle('ratio %s/%s' % (name1, name2))
g.GetYaxis().SetTitleOffset(1.25)
#g.GetYaxis().SetRangeUser(0, i1/i2 * 3)
if x_range.has_key(path):
    g.GetXaxis().SetRangeUser(*x_range[path])
if y_range.has_key(path):
    g.GetYaxis().SetRangeUser(*y_range[path])
ps.save('ratio')
