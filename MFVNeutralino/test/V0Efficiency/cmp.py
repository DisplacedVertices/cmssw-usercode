import sys
from JMTucker.Tools.ROOTTools import *
set_style()

ps = plot_saver(plot_dir('v0bkgsub_cmp'), size=(600,600))

def getit(name, fn, w):
    f = ROOT.TFile(fn)
    h = f.Get('hsiglo').Clone(name)
    h.SetDirectory(0)
    h.Scale(w)
    return fn, f, h

fn1, f1, h1 = getit('one', sys.argv[1], eval(sys.argv[2]))
fn2, f2, h2 = getit('two', sys.argv[3], eval(sys.argv[4]))

h1.Draw()
ps.save('h1')
h2.Draw()
ps.save('h2')

g = ROOT.TGraphAsymmErrors(h1, h2, 'pois midp')
g.Draw('AP')
g.GetYaxis().SetRangeUser(0,3)
g.SetLineColor(ROOT.kBlue)
g.Fit('pol1')
ps.save('rat')
