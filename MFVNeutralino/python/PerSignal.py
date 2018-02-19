from JMTucker.Tools.ROOTTools import *

class PerSignal:
    tau_names = {100: '100 #mum', 300: '300 #mum', 1000: '1 mm', 10000: '10 mm', 30000: '30 mm'}

    @classmethod
    def clear_samples(_, samples):
        for s in samples:
            if hasattr(s, 'y' ): del s.y
            if hasattr(s, 'yl'): del s.yl
            if hasattr(s, 'yh'): del s.yh
            if hasattr(s, 'ye'): del s.ye

    class curve:
        def __init__(self):
            self.v = {}
        def set(self, tau, mass, y, eyl, eyh):
            self.v[(tau,mass)] = (y,eyl,eyh)
        def get(self, tau, mass):
            return self.v.get((tau,mass), None)

    def __init__(self, y_title='', y_range=(0.,1.)):
        self.masses = set()
        self.taus = set()
        self.y_title = y_title
        self.y_range = y_range
        self.y_span = y_range[1] - y_range[0]
        self.curves = []

    def add(self, samples, title='', color=ROOT.kRed, style=1, in_legend=True):
        # samples already has members y, ye or yl,yh for the ordinate
        # values, or will be marked absent on plot. This is why add
        # separate from TGraph creation in draw, have to know all the
        # (tau,mass) points first.

        samples = sorted(samples, key=lambda s: s.name)
        tm = [(s.tau, s.mass) for s in samples]
        if len(tm) != len(set(tm)):
            raise ValueError('duplicate (tau,mass) seen')

        c = PerSignal.curve()
        c.title = title
        c.color = color
        c.style = style
        c.in_legend = in_legend
        self.curves.append(c)
        for s in samples:
            self.taus.add(s.tau)
            self.masses.add(s.mass)
            if hasattr(s, 'y') and s.y is not None:
                if any((hasattr(s, 'yl') and not hasattr(s, 'yh'),
                        hasattr(s, 'yh') and not hasattr(s, 'yl'),
                        hasattr(s, 'ye') and (hasattr(s, 'yh') or hasattr(s, 'yl')))):
                    raise ValueError('may only specify y,yl,yh or y,ye')
                if hasattr(s, 'yl') and hasattr(s, 'yh') and s.yl is not None and s.yh is not None:
                    eyl = s.y - s.yl
                    eyh = s.yh - s.y
                elif hasattr(s, 'ye') and s.ye is not None:
                    eyl = eyh = s.ye
                else:
                    eyl = eyh = 0.
                c.set(s.tau, s.mass, s.y, eyl, eyh)

    def draw(self, draw_missing=True, canvas='c_per_signal', size=(600,600),
             do_tau_paves=True, do_decay_paves=True):
        if type(canvas) == str:
            canvas = ROOT.TCanvas(canvas, '', *size)
        self.canvas = canvas
        self.canvas.cd()

        taus   = sorted(self.taus)
        masses = sorted(self.masses)
        points = self.points = [(tau, mass) for tau in taus for mass in masses]
        npoints = self.npoints = len(points)

        for curve in self.curves:
            x,y,eyl,eyh = [], [], [], []
            x_missing = []
            for i, (tau, mass) in enumerate(points):
                p = curve.get(tau, mass)
                if p:
                    x.append(i+0.5)
                    y.append(p[0])
                    eyl.append(p[1])
                    eyh.append(p[2])
                else:
                    x_missing.append(i+0.5)

            n = len(x)
            curve.g = g = ROOT.TGraphAsymmErrors(n)
            for j in xrange(n):
                g.SetPoint(j, x[j], y[j])
                g.SetPointEXlow (j, 0.5)
                g.SetPointEXhigh(j, 0.5)
                g.SetPointEYlow (j, eyl[j])
                g.SetPointEYhigh(j, eyh[j])

            if x_missing:
                g = curve.g_missing = ROOT.TGraph(len(x_missing), to_array(x_missing), to_array([self.y_range[0] + self.y_span*0.01]*len(x_missing)))
                g.SetMarkerColor(curve.color)
                g.SetMarkerStyle(29)
                g.SetMarkerSize(2.0)
            else:
                curve.g_missing = None

        for ic, curve in enumerate(self.curves):
            g = curve.g
            g.SetTitle('')
            g.SetLineWidth(2)
            g.SetLineColor(curve.color)
            g.SetLineStyle(curve.style)
            g.Draw('APZ' if ic == 0 else 'PZ')
            # these must come after the draw because a TGraph* doesn't have an axis until it is drawn (when will I remember this the first time?)
            xax, yax = g.GetXaxis(), g.GetYaxis()
            xax.SetNdivisions(npoints, False)
            xax.SetLabelSize(0)
            xax.SetRangeUser(0, npoints)
            yax.SetRangeUser(*self.y_range)
            yax.SetTitle(self.y_title)

            if curve.g_missing:
                curve.g_missing.Draw('P')

        # now draw the accoutrements
        ntaus   = self.ntaus   = len(taus)
        nmasses = self.nmasses = len(masses)
        self.tau_paves = []
        self.tau_lines = []
        y_tau = self.y_range[1] + 0.025 * self.y_span
        for i, tau in enumerate(taus):
            if do_tau_paves:
                tau_name = PerSignal.tau_names[tau]
                ymin = y_tau
                if '#mu' not in tau_name:
                    ymin += 0.006 * self.y_span
                p = ROOT.TPaveText(i*nmasses+1, ymin, (i+1)*nmasses-1, ymin+0.07)
                p.SetTextFont(42)
                p.SetFillColor(ROOT.kWhite)
                p.AddText(tau_name)
                p.SetTextSize(0.042)
                p.SetBorderSize(0)
                p.Draw()
                self.tau_paves.append(p)

            if i > 0:
                for z in xrange(2):
                    l = ROOT.TLine(i*nmasses, self.y_range[0], i*nmasses, self.y_range[1])
                    l.SetLineWidth(1)
                    if z == 0:
                        l.SetLineColor(ROOT.kWhite)
                    else:
                        l.SetLineStyle(2)
                    l.Draw()
                    self.tau_lines.append(l)

        self.mass_paves = []
        for i, (_, mass) in enumerate(points):
            ymax = self.y_range[0]-0.04*self.y_span
            p = ROOT.TPaveText(i, ymax-0.02*self.y_span, i+1, ymax)
            p.SetFillColor(ROOT.kWhite)
            t = p.AddText(str(mass))
            t.SetTextAngle(90)
            p.SetTextFont(42)
            p.SetTextSize(0.025)
            p.SetBorderSize(0)
            p.Draw()
            self.mass_paves.append(p)

        self.decay_paves = []
        if do_decay_paves:
            for ic, curve in enumerate([c for c in self.curves if c.in_legend]):
                p = ROOT.TPaveText(0.5, 0.97*self.y_span-(ic+1)*self.y_span*0.05, nmasses, 0.97*self.y_span-ic*self.y_span*0.05)
                p.AddText(curve.title)
                p.SetTextFont(42)
                p.SetTextColor(curve.color) #if len(self.curves) > 1 else ROOT.kBlack)
                p.SetFillColor(ROOT.kWhite)
                p.SetBorderSize(0)
                p.Draw()
                self.decay_paves.append(p)

        self.lifetime_pave = ROOT.TPaveText(-3, y_tau, -0.01, y_tau + 0.07)
        self.lifetime_pave.SetTextFont(42)
        self.lifetime_pave.SetTextSize(0.048)
        self.lifetime_pave.AddText('#tau')
        self.lifetime_pave.SetFillColor(ROOT.kWhite)
        self.lifetime_pave.SetBorderSize(0)
        self.lifetime_pave.Draw()

        self.mass_pave = ROOT.TPaveText(0.013, 0.007, 0.119, 0.080, 'NDC')
        self.mass_pave.SetFillColor(ROOT.kWhite)
        self.mass_pave.SetTextFont(42)
        self.mass_pave.SetTextSize(0.03)
        self.mass_pave.AddText('M')
        self.mass_pave.AddText('(GeV)')
        self.mass_pave.SetBorderSize(0)
        self.mass_pave.Draw()

if __name__ == '__main__':
    import argparse, os, sys
    parser = argparse.ArgumentParser(description = 'PerSignal: given a dir of root files, plot a specified statistic for each signal point')
                                  #   usage = '%(prog)s [statistic options] dir histogram plotdir')
    parser.add_argument('rootdir', help='Path to root files.')
    parser.add_argument('hist', help='Path to histogram in the root files.')
    parser.add_argument('plotpath', help='Where to save plots.')
    parser.add_argument('--ytitle', default='changeme', help='Title for y-axis.')
    parser.add_argument('--yrange', nargs=2, type=float, metavar=('YMIN', 'YMAX'), default=None, help='Range for y-axis.')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i', '--integral', nargs=2, type=float, metavar=('A','B'), help='Statistic plotted is the integral with the specified range (A and B are floats that will be converted to inclusive bin indices), with Poisson uncertainty from #entries.')
    group.add_argument('-j', '--integral-ratio', nargs=4, type=float, metavar=('A','B', 'C', 'D'), help='Statistic plotted is the ratio of the integrals with the specified ranges AB / CD (A,B,C,D are floats that will be converted to inclusive bin indices), with Poisson uncertainty from #entries.')
    group.add_argument('-m', '--mean', action='store_true', help='Statistic plotted is the mean.')
    group.add_argument('-r', '--rms', action='store_true', help='Statistic plotted is the rms.')
    options = parser.parse_args()

    set_style()
    ps = plot_saver(options.plotpath, size=(600,600))
    
    from JMTucker.Tools import Samples

    multijet = [s for s in Samples.mfv_signal_samples]
    dijet = Samples.mfv_ddbar_samples
    samples = multijet + dijet

    for sample in samples:
        fn = os.path.join(options.rootdir, sample.name + '.root')
        if not os.path.exists(fn):
            continue
        f = ROOT.TFile(fn)
        h = f.Get(options.hist)
        if options.integral:
            sample.y, sample.ye = get_integral(h, *options.integral)
        if options.integral_ratio:
            n, en = get_integral(h, *options.integral_ratio[:2])
            d, ed = get_integral(h, *options.integral_ratio[2:])
            neff = (n/en)**2 if en > 0 else 0
            deff = (d/ed)**2 if ed > 0 else 0
            sample.y, sample.yl, sample.yh = clopper_pearson_poisson_means(neff,deff)
        elif options.mean:
            sample.y = h.GetMean()
            sample.ye = h.GetMeanError()
            sample.ye = h.GetMeanError()
        elif options.rms:
            sample.y = h.GetRMS()
            sample.ye = h.GetRMSError()

        if hasattr(sample, 'ye'):
            print '%26s: %12.6f +- %12.6f' % (sample.name, sample.y, sample.ye)
        else:
            print '%26s: %12.6f [%12.6f, %12.6f]' % (sample.name, sample.y, sample.yl, sample.yh)

    def _g(s,l):
        if hasattr(s, 'ye'):
            return s.y - l*s.ye
        else:
            return s.yl if l else s.yh

    if not options.yrange:
        l = [_g(s, 1) for s in samples]; l = min(l) - max(abs(x) for x in l)*0.05
        h = [_g(s,-1) for s in samples]; h = max(h) + max(abs(x) for x in h)*0.05
        options.yrange = l,h

    per = PerSignal(options.ytitle, options.yrange)
    per.add(multijet,  title='#tilde{N} #rightarrow tbs')
    per.add(dijet, title='X #rightarrow d#bar{d}', color=ROOT.kBlue)
    per.draw(canvas=ps.c)
    ps.save('plot')
