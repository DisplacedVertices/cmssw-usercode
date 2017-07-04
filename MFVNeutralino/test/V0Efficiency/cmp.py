import sys, os
from JMTucker.Tools.ROOTTools import *
from JMTucker.Tools.Sample import norm_from_file
from JMTucker.Tools import Samples
set_style()

integ = lambda h: h.Integral(0,h.GetNbinsX()+2)

ilumi_d = { # in /pb
'qcd': 38529.0,
'qcdht1000and1500': 38529.0,

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

for x,l in ('BCD', ('B3', 'C', 'D')), ('EF', 'EF'), ('BCDEF', ('B3',) + tuple('CDEF')), ('H', ('H2', 'H3')), ('GH', ('G', 'H2', 'H3')):
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
    print integ(h), ilumi
    h.Scale(1./ilumi)
    return fn, sname, f, h

path = sys.argv[1]
fn1, name1, f1, h1 = getit(path, sys.argv[2])
fn2, name2, f2, h2 = getit(path, sys.argv[3])

h1.SetLineColor(2)
h2.SetLineColor(4)

ps = plot_saver(plot_dir('v0bkgsub/!cmp/%s_%s_%s' % (path, name1, name2)), size=(600,600))

i1, i2 = integ(h1), integ(h2)

h1.Draw('hist e')
h2.Draw('hist e same')
ps.save('cmp')

g = ROOT.TGraphAsymmErrors(h1, h2, 'pois midp')
g.Draw('AP')
g.GetYaxis().SetRangeUser(0, i1/i2 * 3)
g.SetLineColor(ROOT.kBlue)
fit_range = {'h_vtx_rho': (0.2, 2), 'h_track_dxybs': (-0.4, 0.4)}[path]
fcn = ROOT.TF1('fcn', 'pol1', *fit_range)
g.Fit(fcn, 'R')
ps.save('ratio')
