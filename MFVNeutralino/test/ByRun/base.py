import os, sys, math, struct
from collections import defaultdict
from JMTucker.Tools.LumiLines import *
from JMTucker.Tools.ROOTTools import *
set_style()

class ByRunPlotter:
    class result:
        pass

    def __init__(self, plot_saver, mask_fn=None, runs=[]):
        self.ps = plot_saver
        self.runs = sorted(runs)
        self.mask_fn = mask_fn
        self._lls = None

    @property
    def lls(self):
        if not self._lls:
            self._lls = LumiLines('/uscms/home/tucker/public/mfv/2015plus2016stripped2.gzpickle', self.mask_fn)
        return self._lls

    def make(self, d, name, title, y_title, year, exclude, verbose=False, scale_by_lumi=False, scale_by_avgpu=False, draw_boundaries=True, use_index=True):
        r = ByRunPlotter.result()

        r.runs = self.runs if self.runs else self.lls.runs(year) # already sorted
        r.nruns = len(r.runs)
        r.runs_used = 0
        r.lumi_sum = 0.
        r.zero_lumis = []

        g, na = [], []
        fill_boundaries = []
        era_boundaries = []
        for i, run in enumerate(r.runs):
            x = i if use_index else run
            n = d.get(run, 0)

            if draw_boundaries and i > 0:
                prevrun = r.runs[i-1]
                for fr in self.lls.fill_boundaries:
                    if prevrun < fr and run >= fr:
                        fill_boundaries.append(i)
                        break
                for fr in self.lls.era_boundaries:
                    if prevrun < fr and run >= fr:
                        era_boundaries.append(i)
                        break

            if verbose:
                print '(%3i) %i: %r' % (i,run,n)

            if scale_by_lumi or scale_by_avgpu:
                lumi = self.lls.recorded(run)/1e6
                r.lumi_sum += lumi
                if lumi == 0:
                    r.zero_lumis.append(run)
                lumi_frac_uncert = 0.027 if run <= 260627 else 0.062
                lumi_uncert = lumi_frac_uncert * lumi

            if i in exclude or run in exclude or n is None or (scale_by_lumi and lumi == 0):
                na.append(x)
            else:
                r.runs_used += 1

                if type(n) == int:
                    y = n
                    yl, yh = poisson_interval(n)
                elif type(n) == float:
                    y = yl = yh = n
                elif type(n) == tuple:
                    if len(n) == 2:
                        y = n[0]
                        yl = y - n[1]
                        yh = y + n[1]
                    elif len(n) == 3:
                        y, yl, yh = n

                if scale_by_lumi:
                    y  /= lumi
                    yl /= lumi
                    yh /= lumi
                    #el = y - yl
                    #eh = yh - y
                    #el = (el**2 + lumi_uncert**2)**0.5
                    #eh = (eh**2 + lumi_uncert**2)**0.5
                    #yl = y - el
                    #yh = y + eh

                if scale_by_avgpu:
                    avgpu = self.lls.avg_pu(run) if lumi > 0 else -1
                    y  /= avgpu
                    yl /= avgpu
                    yh /= avgpu

                g.append((x, y, y-yl, yh-y))


        r.g = ROOT.TGraphAsymmErrors(len(g))
        for i, (x,y,el,eh) in enumerate(g):
            r.g.SetPoint(i, x, y)
            r.g.SetPointEYlow(i, el)
            r.g.SetPointEYhigh(i, eh)

        r.g_na = ROOT.TGraphAsymmErrors(len(na))
        for i, irun in enumerate(na):
            r.g_na.SetPoint(i, irun, 0)

        r.g.SetMarkerStyle(20)
        r.g.SetMarkerSize(0.5)
        r.g_na.SetMarkerStyle(22)
        r.g_na.SetMarkerSize(0.8)

        if verbose:
            print 'lumi sum:', r.lumi_sum/1e3, '/fb'
        if r.zero_lumis:
            for run in r.zero_lumis:
                print 'zero lumi for run %i with d[run]=%r' % (run, d[run])

        t = ROOT.TLatex()
        t.SetTextFont(42)

        r.g.SetTitle('%s  # runs: %i;run index;%s' % (title, r.runs_used, y_title))
        r.g.Draw('AP')

        a = tgraph_getpoint(r.g,  0)[0] - 100
        b = tgraph_getpoint(r.g, -1)[0] + 100
        r.fcn0 = ROOT.TF1('fcn0', 'pol0', a,b)
        r.fcn1 = ROOT.TF1('fcn1', 'pol1', a,b)
        r.fcn0.SetLineColor(ROOT.kRed)
        r.fcn1.SetLineColor(ROOT.kGreen+2)

        fr0 = r.g.Fit(r.fcn0, 'QRS')
        fr1 = r.g.Fit(r.fcn1, 'QRS')
        r.fcn0.Draw('same')

        hh = r.g.GetHistogram()
        ymin, ymax = hh.GetMinimum(), hh.GetMaximum()

        fill_lines = []
        for i in fill_boundaries + era_boundaries:
            l = ROOT.TLine(i-0.5, ymin, i-0.5, ymax)
            fill_lines.append(l)
            if i not in era_boundaries:
                l.SetLineStyle(2)
            else:
                l.SetLineWidth(2)
            l.Draw()

        miss = []
        fy = r.fcn0.GetParameter(0)
        for j in xrange(r.g.GetN()):
            x,y = tgraph_getpoint(r.g, j)
            yl = y - r.g.GetErrorYlow(j)
            yh = y + r.g.GetErrorYhigh(j)
            if fy < yl or fy > yh:
                miss.append((x,y,yl,yh))
        if miss:
            g_miss = ROOT.TGraphAsymmErrors(len(miss))
            for i,(x,y,yl,yh) in enumerate(miss):
                g_miss.SetPoint(i,x,y)
                g_miss.SetPointEYlow(i, y-yl)
                g_miss.SetPointEYhigh(i, yh-y)
            g_miss.SetMarkerColor(ROOT.kOrange+2)
            g_miss.SetMarkerStyle(r.g.GetMarkerStyle())
            g_miss.SetMarkerSize(r.g.GetMarkerSize())
            g_miss.SetLineColor(ROOT.kOrange+2)
            g_miss.Draw('P')

        s0 = 'pol0 fit #chi^{2}/ndf = %.2f / %i  prob = %.2f  p0 = %.2g #pm %.2g' % (fr0.Chi2(), fr0.Ndf(), fr0.Prob(), r.fcn0.GetParameter(0), r.fcn0.GetParError(0))
        s1 = 'pol1 fit #chi^{2}/ndf = %.2f / %i  prob = %.2f  p0 = %.2g #pm %.2g  p1 = %.2g #pm %.2g' % (fr1.Chi2(), fr1.Ndf(), fr1.Prob(), r.fcn1.GetParameter(0), r.fcn1.GetParError(0), r.fcn1.GetParameter(1), r.fcn1.GetParError(1))

        r.g_na.SetMarkerColor(ROOT.kBlue)
        r.g_na.Draw('P')

        t.DrawLatexNDC(0.12, 0.82, '#color[632]{%s}' % s0)
        t.DrawLatexNDC(0.12, 0.76, '#color[418]{%s}' % s1)
        t.DrawLatexNDC(0.12, 0.70, '#color[600]{# missing runs: %i}' % r.g_na.GetN())
        t.DrawLatexNDC(0.12, 0.64, '#color[802]{%i / %i = %.2f points miss pol0 fit}' % (len(miss), r.g.GetN(), float(len(miss))/r.g.GetN()))

        r.g.GetXaxis().SetRangeUser(-2, r.nruns+2)

        self.ps.save(name)

        r.g.GetYaxis().SetRangeUser(0, 6 * r.fcn0.GetParameter(0))
        self.ps.save(name + '_zoom')

        return r

class EventFilter:
    def __init__(self, fn):
        self.s = set()
        f = open(fn, 'rb')
        evsize = struct.calcsize('=HHQ')
        assert evsize == 12
        block_size = evsize * 10240
        while 1:
            x = f.read(block_size)
            if not x:
                break
            assert len(x) % evsize == 0
            for i in xrange(len(x) / evsize):
                y = struct.unpack_from('=HHQ', x, i*evsize)
                self.s.add(y)

    def __contains__(self, rle):
        r,l,e = rle
        r -= 254231
        return (r,l,e) in self.s
