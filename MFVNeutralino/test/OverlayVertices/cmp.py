import sys, os
from array import array
from DVCode.Tools.ROOTTools import *
set_style()

ROOT.gStyle.SetOptFit(0)

by_ntracks = False

class F:
    def __init__(self, fn):
        self.fn = fn
        self.n = n = fn.split('/')[2]
        self.ntracks = int(n.split('ntk')[1].split('_')[0])
        self.f = f = ROOT.TFile(fn)
        self.g = g = f.Get('c0').FindObject('divide_h_dvv_pass_foundv0andv1bytracks_rebin_by_h_dvv_true_rebin').Clone(n)

        if by_ntracks:
            color = {
                3: ROOT.kRed,
                4: ROOT.kGreen+2,
                5: ROOT.kBlue,
                }[self.ntracks]
        else:
            if n.endswith('_deltasvgaus_wevent'):
                color = ROOT.kBlue
            elif n.endswith('_deltasvgaus'):
                color = ROOT.kGreen+2
            elif n.endswith('_wevent'):
                color = ROOT.kMagenta
            else:
                color = ROOT.kRed

        g.SetLineColor(color)
        #print list(g.GetListOfFunctions())
        #g.GetListOfFunctions()[0].SetBit(ROOT.TF1.kNotDraw)
        #s = g.GetListOfFunctions()[1]
        #s.SetLineColor(0), s.SetTextColor(0), s.SetX1NDC(1), s.SetY1NDC(1), s.SetX2NDC(1), s.SetY2NDC(1) # grr

        end = 0.1
        self.fcns = [None, None]
        self.fits = [None, None]
        for ifcn, rng in enumerate(((0, 0.0175), (0.05, end))):
            if ifcn == 0:
                if 'wevent' in ex:
                    fcn = '[0]*exp([1]*x) - 1'
                else:
                    fcn = '[0] + [1]*x**2'
            else:
                fcn = 'pol1'
            fcn = self.fcns[ifcn] = ROOT.TF1(n + '_fcn%i' % ifcn, fcn, *rng)
            fcn.SetLineColor(1)
            fcn.SetLineWidth(1)
            res = g.Fit(fcn, 'RQS')
            x = res.GetParams()
            a,b = x[0], x[1]
            x = res.GetErrors()
            ea,eb = x[0], x[1]
            if ifcn == 0:
                self.fits[0] = (a,ea)
            else:
                e = fcn.Eval(end)
                ee = (ea**2 + eb**2 * end**2)**0.5
                self.fits[1] = (e, ee)
        
        a, ea = subtr, e_subtr = self.fits[0]
        e, ee = self.fits[1]
        mult = 1/(e-a)
        e_mult = (ee**2 + ea**2)**0.5 * mult**2

        self.scaled_g = sg = g.Clone(g.GetName() + '_scaled')
        self.scaled_g.SetTitle(';d_{VV} (cm);efficiency')
        self.scaled_g.GetListOfFunctions()[-1].SetBit(ROOT.TF1.kNotDraw)
        for i in xrange(g.GetN()):
            x,y = tgraph_getpoint(sg, i)
            eyl, eyh = sg.GetErrorYlow(i), sg.GetErrorYhigh(i)
            #print i,x,y,eyl,eyh
            y = (y - subtr) * mult
            # this is wrong
            exex = e_subtr**2 * mult**2 + e_mult**2 * (x**2 + subtr**2)
            eyl = (eyl**2 + exex)**0.5
            eyh = (eyh**2 + exex)**0.5
            #print '  ->', x,y,eyl,eyh
            sg.SetPoint(i, x, y)
            sg.SetPointEYlow(i, eyl)
            sg.SetPointEYhigh(i, eyh)

        print 'h_eff = book("%s")' % n
        for i in xrange(self.scaled_g.GetN()):
            x,y = tgraph_getpoint(self.scaled_g, i)
            print 'h_eff.SetBinContent(%i, %f)' % (i+1, y)

if by_ntracks:
    ex = '_deltasvgaus'
    ex = ''
    ex = '_wevent'
    ex = '_deltasvgaus_wevent'

    files = '''
plots/overlay/ntk3%(ex)s/h_dvv_pass_foundv0andv1bytracks.root
plots/overlay/ntk4%(ex)s/h_dvv_pass_foundv0andv1bytracks.root
plots/overlay/ntk5%(ex)s/h_dvv_pass_foundv0andv1bytracks.root
''' % locals()
else:
    ntk = 5
    ex = '_ntk%i' % ntk
    files = '''
plots/overlay/ntk%(ntk)i/h_dvv_pass_foundv0andv1bytracks.root
plots/overlay/ntk%(ntk)i_wevent/h_dvv_pass_foundv0andv1bytracks.root
plots/overlay/ntk%(ntk)i_deltasvgaus/h_dvv_pass_foundv0andv1bytracks.root
plots/overlay/ntk%(ntk)i_deltasvgaus_wevent/h_dvv_pass_foundv0andv1bytracks.root
''' % locals()

fs = [F(fn.strip()) for fn in files.split('\n') if fn.strip()]

ps = plot_saver('plots/overlay/compare%s' % ex, log=False)

for scaled in (0,1):
    print 'scaled?', scaled
    for i,f in enumerate(fs):
        g = f.scaled_g if scaled else f.g
        print i, f.n, g, g.GetN()
        g.GetXaxis().SetLimits(0, 0.115 if by_ntracks else 0.105)
        g.GetYaxis().SetRangeUser(-0.05 if scaled else 0, 1.2)
        g.Draw('AP' if i == 0 else 'P same')
        if not scaled:
            f.fcns[0].Draw('same')

    leg = ROOT.TLegend(0.131, 0.810, 0.725, 0.863)
    leg.SetNColumns(4)
    leg.SetBorderSize(0)
    leg.AddEntry(fs[0].g, 'simple', 'L')
    leg.AddEntry(fs[1].g, 'w. event', 'L')
    leg.AddEntry(fs[2].g, 'Gaus(#Deltaz)', 'L')
    leg.AddEntry(fs[3].g, 'Gaus(#Deltaz), w. event', 'L')
    leg.Draw()

    if not scaled and by_ntracks:
        txt = ROOT.TLatex()
        txt.SetTextSize(0.04)
        txt.SetTextFont(42)
        for i,ntk in enumerate([3,4,5]):
            f = fs[i]
            x,y = tgraph_getpoint(f.g, -1)
            xp = x + f.g.GetErrorXhigh(i) + 0.004
            txt.DrawLatex(xp, y, 'n_{tk}=%i' % ntk)

    ps.save('cmp_scaled' if scaled else 'cmp')
