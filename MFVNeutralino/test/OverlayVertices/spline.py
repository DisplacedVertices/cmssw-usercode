import sys
from math import ceil
from DVCode.Tools.ROOTTools import *
set_style()

ROOT.gStyle.SetPadTopMargin(0.01)
ROOT.gStyle.SetPadBottomMargin(0.04)
ROOT.gStyle.SetPadLeftMargin(0.04)
ROOT.gStyle.SetPadRightMargin(0.01)

fout = ROOT.TFile('export.root', 'recreate')

ps = plot_saver('plots/spline', log=False, size=(1250,600))

exs = [
    'ntk3',
    'ntk3_deltasvgaus',
    'ntk3_deltasvgaus_wevent',
    'ntk3_wevent',
    'ntk4',
    'ntk4_deltasvgaus',
    'ntk4_deltasvgaus_wevent',
    'ntk4_wevent',
    'ntk5',
    'ntk5_deltasvgaus',
    'ntk5_deltasvgaus_wevent',
    'ntk5_wevent',
    ]

for ex in exs:
    fn = 'plots/overlay/%s/h_dvv_pass_foundv0andv1bytracks.root' % ex
    f = ROOT.TFile(fn)
    g = f.Get('c0').FindObject('divide_h_dvv_pass_foundv0andv1bytracks_rebin_by_h_dvv_true_rebin')

    if 'deltasvgaus' in fn:
        print '*** kicking some points in deltasvgaus ***'
        _,y = tgraph_getpoint(g,3)
        for i in (0,1,2):
            x,_ = tgraph_getpoint(g,i)
            g.SetPoint(i,x,y)
        if 'ntk5' in fn:
            for i in (4,5):
                x,y = tgraph_getpoint(g,i)
                g.SetPoint(i,x,y-0.01)

    s3 = ROOT.TSpline3('s3', g)
    s5 = ROOT.TSpline5('s5', g)

    class smoother:
        def __init__(self, g):
            self.g = g
            self.n = 0
            self.gs = []
            self.gss = ROOT.TGraphSmooth()

        def smooth(self, bw, start, stop):
            step = 0.00005
            points = [start + step*i for i in xrange(int(ceil((stop-start)/step)))]
            name = 'piece%i' % self.n
            self.n += 1
            sg = self.gss.SmoothKern(g, 'normal', bw, len(points), array('d', points))
            sg = sg.Clone(name)
            self.gs.append(sg)

        def stitch(self):
            xs = []
            ys = []
            for g in self.gs:
                for i in xrange(g.GetN()):
                    x,y = tgraph_getpoint(g, i)
                    xs.append(x)
                    ys.append(y)
            return ROOT.TGraph(len(xs), array('d', xs), array('d', ys))

    s = smoother(g)

    if 'ntk3' in fn or 'ntk4' in fn:
    #    s.smooth(0.002, [       0.001*x for x in xrange(31)])
    #    s.smooth(0.005, [0.03 + 0.001*x for x in xrange(31)])
    #    s.smooth(0.020, [0.06 + 0.001*x for x in xrange(41)])
        s.smooth(0.002, 0., 0.03)
        s.smooth(0.005, 0.03, 0.06)
        s.smooth(0.020, 0.06, 0.1)
    elif 'ntk5' in fn:
        s.smooth(0.002, 0.00, 0.010)
        s.smooth(0.004, 0.01, 0.025)
    #    s.smooth(0.008, [0.03 + 0.001*x for x in xrange(21)])
    #    s.smooth(0.010, [0.05 + 0.001*x for x in xrange(51)])
        lastx,lasty = tgraph_getpoint(s.gs[-1], -1)
        fcn = ROOT.TF1('lastpiece', '[0]*(x-%f) + %f' % (lastx,lasty), lastx, 0.1)
        g.Fit(fcn, 'NQR')
        xs = [lastx + 0.001*x for x in xrange(76)]
        ys = [fcn.Eval(x) for x in xs]
        lastg = ROOT.TGraph(len(xs), array('d', xs), array('d', ys))
        s.gs.append(lastg)
    else:
        raise ValueError('dunno ntracks')

    sg = s.stitch()

    ps.c.cd()

    #for i in xrange(g.GetN()):
    #    x,y=tgraph_getpoint(g, i)
    #    g.SetPoint(i,x,y+0.05)
    g.Draw('AP')
    _,y0 = tgraph_getpoint(g, 0)
    _,y1 = tgraph_getpoint(g, -1)
    g.GetYaxis().SetRangeUser(y0-0.03, y1+0.03)

    for x,c in ((s3,3), (s5,5), (sg,6)):
        x.SetLineColor(c)
        x.SetLineWidth(2)
    for x in s.gs:
        x.SetLineColor(2)
        x.SetLineWidth(2)

    s3.Draw('Lsame')
    s5.Draw('Lsame')
    for x in s.gs:
        x.Draw('LP')
    sg.Draw('LP')

    ps.save(ex)

    _,y0 = tgraph_getpoint(sg, 0)
    _,y1 = tgraph_getpoint(sg, -1)
    for i in xrange(sg.GetN()):
        x,y = tgraph_getpoint(sg, i)
        y = (y - y0) / (y1 - y0)
        sg.SetPoint(i,x,y)

    fout.cd()
    hout = ROOT.TH1F(ex, '', 1000, 0, 0.1)
    for ibin in xrange(1, hout.GetNbinsX()+1):
        y = sg.Eval(hout.GetBinCenter(ibin))
        hout.SetBinContent(ibin, y)
    hout.Write()

fout.Write()
fout.Close()
