import os, sys, math, struct
from collections import defaultdict
from DVCode.Tools.LumiLines import *
from DVCode.Tools.ROOTTools import *
from DVCode.Tools.CMSSWTools import json_path
from DVCode.Tools import Samples
set_style()

class ByRunPlotter:
    class result:
        pass

    def __init__(self, plot_saver, mask_fn=None, runs=[]):
        self.ps = plot_saver
        self.ps.c.SetRightMargin(0.01)
        self.runs = sorted(runs)
        self.mask_fn = mask_fn
        self._lls = None

    @property
    def lls(self):
        if not self._lls:
            self._lls = LumiLines('/uscms/home/tucker/public/mfv/lumi/2017p8.stripped.gzpickle', self.mask_fn)
        return self._lls

    def make(self, d, name, title, y_title, year, exclude, verbose=False, scale_by_lumi=False, scale_by_avgpu=False, draw_boundaries=True, use_index=True, do_fits=True, highlight=[]):
        r = ByRunPlotter.result()

        r.runs = self.runs if self.runs else self.lls.runs(year) # already sorted
        r.nruns = len(r.runs)
        r.runs_used = 0
        r.lumi_sum = 0.
        r.zero_lumis = []

        g, na, hl = [], [], []
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
                fmt = '%s'
                if type(n) == float:
                    fmt = '%.3g'
                elif type(n) == tuple and type(n[0]) in (float,int):
                    fmt = ' '.join(['%.3g']*len(n))
                print '(%3i) %i: %s' % (i,run,fmt%n)

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

                pt = (x, y, y-yl, yh-y)
                g.append(pt)
                if run in highlight:
                    hl.append(pt)

        r.g = ROOT.TGraphAsymmErrors(len(g))
        r.g.SetMarkerStyle(20)
        r.g.SetMarkerSize(0.5)
        for i, (x,y,el,eh) in enumerate(g):
            r.g.SetPoint(i, x, y)
            r.g.SetPointEYlow(i, el)
            r.g.SetPointEYhigh(i, eh)

        if hl:
            r.g_highlight = ROOT.TGraphAsymmErrors(len(hl))
            r.g_highlight.SetLineColor(ROOT.kBlue)
            r.g_highlight.SetMarkerColor(ROOT.kBlue)
            r.g_highlight.SetMarkerStyle(20)
            r.g_highlight.SetMarkerSize(0.5)
            for i, (x,y,el,eh) in enumerate(hl):
                r.g_highlight.SetPoint(i, x, y)
                r.g_highlight.SetPointEYlow(i, el)
                r.g_highlight.SetPointEYhigh(i, eh)

        r.runs_missing = len(na)
        r.g_na = ROOT.TGraphAsymmErrors(len(na))
        r.g_na.SetMarkerStyle(22)
        r.g_na.SetMarkerSize(0.8)
        for i, irun in enumerate(na):
            r.g_na.SetPoint(i, irun, 0)

        if verbose:
            print 'lumi sum:', r.lumi_sum/1e3, '/fb'
        if r.zero_lumis:
            for run in r.zero_lumis:
                print 'zero lumi for run %i with d[run]=%r' % (run, d[run])

        t = ROOT.TLatex()
        t.SetTextFont(42)

        r.g.SetTitle('%s  %i runs, %i missing;run index;%s' % (title, r.runs_used, r.runs_missing, y_title))
        r.g.Draw('AP')
        if hl:
            r.g_highlight.Draw('P')
            print '%i highlighted' % len(hl)

        if do_fits:
            miss = []
            r.fcns, r.frs = [], []
            ranges = era_boundaries[:]
            ranges.insert(0, 0)
            ranges.append(r.runs_used)
            first = None
            for i in xrange(len(ranges)-1):
                a, b = ranges[i], ranges[i+1]-1
                fcn = ROOT.TF1('fcn%i' % i, 'pol0', a, b)
                fcn.SetLineColor(ROOT.kRed)
                r.fcns.append(fcn)
                fr = r.g.Fit(fcn, 'QRS')
                fy  = fcn.GetParameter(0)
                fye = fcn.GetParError(0)
                if not first:
                    first = fy, fye, fye/fy if fy > 0 else None
                    ratio = 1,0
                else:
                    if first[0] > 0 and fy > 0:
                        ratio = fy/first[0], 0 if i == 0 else ((fye/fy)**2 + first[2]**2)**0.5
                    else:
                        ratio = -1,-1
                print '%i (%3i) - %i (%3i): %.3f +- %.3f  (%.4f +- %.4f)  chi2/ndf = %6.3f/%3i -> prob = %f' % (r.runs[a], a, r.runs[b], b, fy, fye, ratio[0], ratio[1], fr.Chi2(), fr.Ndf(), fr.Prob()),
                r.frs.append(fr)
                these_miss = []
                for j in xrange(a, b+1):
                    x,y = tgraph_getpoint(r.g, j)
                    yl = y - r.g.GetErrorYlow(j)
                    yh = y + r.g.GetErrorYhigh(j)
                    if fy < yl or fy > yh:
                        these_miss.append((x,y,yl,yh))
                n = b-a+1
                print '  %3i / %3i = %0.2f miss' % (len(these_miss), n, float(len(these_miss))/n)
                miss.extend(these_miss)
            for fcn in r.fcns:
                fcn.Draw('same')

        if do_fits and miss:
            r.g_miss = ROOT.TGraphAsymmErrors(len(miss))
            for i,(x,y,yl,yh) in enumerate(miss):
                r.g_miss.SetPoint(i,x,y)
                r.g_miss.SetPointEYlow(i, y-yl)
                r.g_miss.SetPointEYhigh(i, yh-y)
            r.g_miss.SetMarkerColor(ROOT.kOrange+2)
            r.g_miss.SetMarkerStyle(r.g.GetMarkerStyle())
            r.g_miss.SetMarkerSize(r.g.GetMarkerSize())
            r.g_miss.SetLineColor(ROOT.kOrange+2)
            r.g_miss.Draw('P')

        r.g_na.SetMarkerColor(ROOT.kBlue)
        r.g_na.Draw('P')

        if do_fits:
            t.DrawLatexNDC(0.12, 0.82, '#color[802]{%i / %i = %.2f points miss fit}' % (len(miss), r.g.GetN(), float(len(miss))/r.g.GetN()))

        r.g.GetXaxis().SetRangeUser(-2, r.nruns+2)
        if do_fits:
            r.g.GetYaxis().SetRangeUser(0, 7 * r.fcns[0].GetParameter(0))
        else:
            gg = g[:]
            gg.sort(key=lambda x: x[1]+x[3])
            r.g.GetYaxis().SetRangeUser(0, 1.05*gg[-5][1])

        hh = r.g.GetHistogram()
        ymin, ymax = hh.GetMinimum(), hh.GetMaximum()
        fill_lines = []
        for i in fill_boundaries + era_boundaries:
            l = ROOT.TLine(i-0.5, ymin, i-0.5, ymax)
            fill_lines.append(l)
            if i not in era_boundaries:
                l.SetLineStyle(2)
            else:
                l.SetLineWidth(4)
            l.Draw()

        self.ps.save(name)
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
