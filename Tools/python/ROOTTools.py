#!/usr/bin/env python

import sys, os
from array import array

if os.environ.has_key('JMT_ROOTTOOLS_NOBATCHMODE'):
    import ROOT
else:
    sys.argv.append('-b')     # Start ROOT in batch mode;
    import ROOT; ROOT.TCanvas # make sure libGui gets initialized while '-b' is specified;
    sys.argv.remove('-b')     # and don't mess up sys.argv.

def apply_hist_commands(hist, hist_cmds=None):
    """With hist_cmds a list of n-tuples, where the first entry of the
    tuple is a function name, call the function name on the histogram
    passing the n-1 remaining arguments to the function.

    E.g. if hist_cmds is [('SetMarkerStyle', 5), ('SetStats', 0)],
    this is equivalent to calling

    hist.SetMarkerStyle(5)
    hist.SetStats(0)

    Default is a no-op (hist_cmds = None).
    """

    if hist_cmds is None: return
    for fn, args in hist_cmds:
        t = type(args)
        if t != type(()) or t != type([]):
            args = (args,)
        getattr(hist, fn)(*args)

def bin_iterator(hist):
    """Loop over all bins of hist (which has whatever dimension) and
    yield the bin coordinates and the bin contents."""

    if issubclass(type(hist), ROOT.TH3):
        for ibin in xrange(0, hist.GetNbinsX()+2):
            for jbin in xrange(0, hist.GetNbinsY()+2):
                for kbin in xrange(0, hist.GetNbinsZ()+2):
                    yield (ibin, jbin, kbin), hist.GetBinContent(ibin, jbin, kbin)
    elif issubclass(type(hist), ROOT.TH2):
        for ibin in xrange(0, hist.GetNbinsX()+2):
            for jbin in xrange(0, hist.GetNbinsY()+2):
                yield (ibin, jbin), hist.GetBinContent(ibin, jbin)
    elif issubclass(type(hist), ROOT.TH1):
        for ibin in xrange(0, hist.GetNbinsX()+2):
            yield (ibin,), hist.GetBinContent(ibin)
    else:
        raise TypeError('input is not a histogram')

def check_consistency(h1, h2, log=True):
    def p(s):
        if not (log or log == ''):
            return
        if type(log) == str:
            print log, s
        else:
            print s
    t1 = type(h1)
    t2 = type(h2)
    assert issubclass(t1, ROOT.TH1) and issubclass(t2, ROOT.TH1)
    if t1 != t2:
        p('histograms have different types')
        return False

    for ax in 'XYZ':
        n = getattr(h1, 'GetNbins' + ax)()
        if n != getattr(h2, 'GetNbins' + ax)():
            p('histograms have different number of bins along %s' % ax)
            return False
        for i in xrange(0, n+2):
            if getattr(h1, 'Get%saxis' % ax)().GetBinLowEdge(i) != getattr(h2, 'Get%saxis' % ax)().GetBinLowEdge(i):
                p('histograms have different %s binning' % ax)
                return False

    return True

def poisson_interval(nobs, alpha=(1-0.6827)/2, beta=(1-0.6827)/2):
    lower = 0
    if nobs > 0:
        lower = 0.5 * ROOT.Math.chisquared_quantile_c(1-alpha, 2*nobs)
    elif nobs == 0:
        beta *= 2
    upper = 0.5 * ROOT.Math.chisquared_quantile_c(beta, 2*(nobs+1))
    return lower, upper

def poisson_intervalize(h, zero_x=False, include_zero_bins=False):
    h2 = ROOT.TGraphAsymmErrors(h)
    for i in xrange(1, h.GetNbinsX()+1):
        c = h.GetBinContent(i)
        if c == 0 and not include_zero_bins:
            continue
        l,u = poisson_interval(c)
        # i-1 in the following because ROOT TGraphs count from 0 but
        # TH1s count from 1
        if zero_x:
            h2.SetPointEXlow(i-1, 0)
            h2.SetPointEXhigh(i-1, 0)
        h2.SetPointEYlow(i-1, c-l)
        h2.SetPointEYhigh(i-1, u-c)
    return h2

def clopper_pearson(n_on, n_tot, alpha=1-0.6827, equal_tailed=True):
    if equal_tailed:
        alpha_min = alpha/2
    else:
        alpha_min = alpha

    lower = 0
    upper = 1

    if n_on > 0:
        lower = ROOT.Math.beta_quantile(alpha_min, n_on, n_tot - n_on + 1)
    if n_tot - n_on > 0:
        upper = ROOT.Math.beta_quantile_c(alpha_min, n_on + 1, n_tot - n_on)

    if n_on == 0 and n_tot == 0:
        return 0, lower, upper
    else:
        return float(n_on)/n_tot, lower, upper

def clopper_pearson_poisson_means(x, y, alpha=1-0.6827):
    r, rl, rh = clopper_pearson(x, x+y, alpha)
    pl = rl/(1-rl)
    if y == 0 or abs(rh - 1) < 1e-9:
        return None, pl, None
    return r/(1-r), pl, rh/(1 - rh)

def histogram_divide(h1, h2, confint=clopper_pearson, force_lt_1=True):
    nbins = h1.GetNbinsX()
    xax = h1.GetXaxis()
    if h2.GetNbinsX() != nbins: # or xax2.GetBinLowEdge(1) != xax.GetBinLowEdge(1) or xax2.GetBinLowEdge(nbins) != xax.GetBinLowEdge(nbins):
        raise ValueError('incompatible histograms to divide')
    x = []
    y = []
    exl = []
    exh = []
    eyl = []
    eyh = []
    xax = h1.GetXaxis()
    for ibin in xrange(1, nbins+1):
        s,t = h1.GetBinContent(ibin), h2.GetBinContent(ibin)
        if t == 0:
            continue

        p_hat = float(s)/t
        if s > t and force_lt_1:
            print 'warning: bin %i has p_hat > 1, in interval forcing p_hat = 1' % ibin
            s = t
        rat, a,b = confint(s,t)
        #print ibin, s, t, a, b

        if b is None: # JMTBAD
            assert confint is not clopper_pearson
            b = 1e99

        _x  = xax.GetBinCenter(ibin)
        _xw = xax.GetBinWidth(ibin)/2
        
        x.append(_x)
        exl.append(_xw)
        exh.append(_xw)

        y.append(p_hat)
        eyl.append(p_hat - a)
        eyh.append(b - p_hat)
    eff = ROOT.TGraphAsymmErrors(len(x), *[array('d', obj) for obj in (x,y,exl,exh,eyl,eyh)])
    return eff

def core_gaussian(hist, factor, i=[0]):
    core_mean  = hist.GetMean()
    core_width = factor*hist.GetRMS()
    f = ROOT.TF1('core%i' % i[0], 'gaus', core_mean - core_width, core_mean + core_width)
    i[0] += 1
    return f

class _hist_list:
    def __init__(self, hists):
        self.hists = dict(hists)
        if self.hists.has_key('all'):
            raise NameError("name 'all' is reserved")

    def __getattr__(self, name):
        if name == 'all':
            return self.hists.values()
        elif self.hists.has_key(name):
            return self.hists[name]
        else:
            raise AttributeError("no histogram '%s' found" % name)

def compare_all_hists(ps, samples, **kwargs):
    """For the common subset of histograms found in dir1..N, draw them
    superimposed, normalized to unit area, with different
    colors. samples is a list of [(sample_name, dir_name, color), ...].

    Options (see the list below) are specified as keyword arguments in
    kwargs, and so far include
    - sort_names: True: process the histograms in alphabetical
    order. False (default): in the order found in the ROOT directory.
    - show_progress: if True (default), print how far along we are
    processing the histograms.
    - only_n_first: if supplied, only do that that many histograms. If
    -1 (default), do all.
    
    Various callbacks (see the other list below) can be specified as
    keyword arguments to modify the drawing depending on the
    histogram. The callback receives the arguments (histogram_name,
    hist_list, current_sample_name), where hist_list is an instance of
    _hist_list above, and current_sample_name is the particular sample
    in question, if applicable. The hist_list object serves as proxy
    for any of the histograms by name, or to return the whole
    list. Some examples:

    draw_commands = lambda name, hists, curr: [hist.GetXaxis().SetRangeUser(0,1) for hist in hists.all]
    apply_commands = lambda name, hists, curr: (hists.ttbar.SetFillStyle(3004), hists.signal.SetFillStyle(3005))
    no_stats = lambda name, hists, curr: name == 'h_costheta'
    scaling = lambda name, hists, curr: {'ttbar': 1, 'signal': 0.01}[curr]
    """

    # options
    recurse        = kwargs.get('recurse',        False)
    sort_names     = kwargs.get('sort_names',     False)
    show_progress  = kwargs.get('show_progress',  True)
    only_n_first   = kwargs.get('only_n_first',   -1)

    def _get(arg, default):
        return kwargs.get(arg, lambda name, hists, curr: default)

    # callbacks
    no_stats       = _get('no_stats',       False)
    stat_size      = _get('stat_size',      (0.2, 0.2))
    skip           = _get('skip',           False)
    apply_commands = _get('apply_commands', None)
    legend         = _get('legend',         None)
    separate_plots = _get('separate_plots', False)
    draw_command   = _get('draw_command',   '')
    scaling        = _get('scaling',        1.)

    ###

    proto_dir = samples[0][1]
    if recurse:
        names = flatten_directory(proto_dir)
    else:
        names = [k.GetName() for k in proto_dir.GetListOfKeys()]
    names = [name for name in names if issubclass(type(proto_dir.Get(name)), ROOT.TH1)]
    if not names:
        raise ValueError('no TH1-descended objects found')

    if sort_names:
        names.sort()
    if only_n_first > 0:
        names = names[:only_n_first]

    def all_same(l, msg):
        if len(set(l)) != 1:
            raise ValueError(msg)
        return l[0]

    nnames = len(names)
    for iname, name in enumerate(names):
        if show_progress and (nnames < 10 or iname % (nnames/10) == 0):
            print '%5i/%5i' % (iname, nnames), name

        name_clean = name.replace('/','_').replace('#','n')

        hists = []
        for sample_name, dir, color in samples:
            hist = dir.Get(name)
            # Store these data in the histogram object so we don't
            # have to cross-reference later. If we give them unique
            # names (prefix 'cah_') ROOT probably won't mind...
            hist.cah_sample_name = sample_name
            hist.cah_color = color
            hists.append(hist)
        hist_list = _hist_list((hist.cah_sample_name, hist) for hist in hists)

        if skip(name, hist_list, None):
            continue

        is2d = all_same([issubclass(type(hist), ROOT.TH2) for hist in hists],
                        "for name %s, some samples' histograms are TH2, and some are not" % name)
        
        if not all_same([issubclass(type(hist), ROOT.TH1) for hist in hists],
                        "for name %s, some samples' histograms are TH1, and some are not" % name):
            continue

        for hist in hists:
            hist.cah_integral = hist.Integral(0, hist.GetNbinsX()+1) if not is2d else 0.
            hist.cah_scaling = scaling(name, hist_list, hist.cah_sample_name)

        nostat = no_stats(name, hist_list, None)
        for hist in hists:
            hist.SetLineWidth(2)

            if not is2d and hist.cah_integral > 0:
                hist.Scale(hist.cah_scaling/hist.cah_integral)
            if nostat:
                hist.SetStats(0)
            hist.SetLineColor(hist.cah_color)
            hist.SetMarkerColor(hist.cah_color)

            hist.SetName(hist.cah_sample_name)
            
        apply_commands(name, hist_list, None)

        draw_cmd = draw_command(name, hist_list, None)
        
        sep = separate_plots(name, hist_list, None)
        if sep == 'all' or (is2d and sep):
            for hist in hists:
                hist.Draw('colz' if is2d else draw_cmd)
                ps.save(name_clean + '_' + hist.cah_sample_name, logz=is2d)

        hists_sorted = hists[:]
        if not is2d:
            hists_sorted.sort(key=lambda hist: hist.GetMaximum(), reverse=True)

        for i,hist in enumerate(hists_sorted):
            if i == 0:
                hist.Draw(draw_cmd)
            else:
                hist.Draw((draw_cmd + ' sames').strip())

        ps.c.Update()
        if not no_stats(name, hist_list, None):
            ss = stat_size(name, hist_list, None)
            for i, hist in enumerate(hists):
                differentiate_stat_box(hist, i, hist.cah_color, ss)

        leg = legend(name, hist_list, None)
        if leg is not None:
            leg.Draw()
            
        ps.save(name_clean, logz=is2d)

def cumulative_histogram(h, type='ge'):
    """Construct the cumulative histogram in which the value of each
    bin is the tail integral of the given histogram.
    """
    
    nb = h.GetNbinsX()
    hc = ROOT.TH1F(h.GetName() + '_cumulative_' + type, '', nb, h.GetXaxis().GetXmin(), h.GetXaxis().GetXmax())
    hc.Sumw2()
    if type == 'ge':
        first, last, step = nb+1, 0, -1
    elif type == 'le':
        first, last, step = 0, nb+1, 1
    else:
        raise ValueError('type %s not recognized' % type)
    for i in xrange(first, last, step):
        prev = 0 if i == first else hc.GetBinContent(i-step)
        c = h.GetBinContent(i) + prev
        hc.SetBinContent(i, c)
        hc.SetBinError(i, c**0.5)
    return hc

def cut(*cuts):
    """Take a sequence of cuts and join them with && (protecting with
    parentheses), suitable for use by TTree::Draw."""
    
    return ' && '.join('(%s)' % c.strip() for c in cuts if c.strip())

def data_mc_comparison(name,
                       background_samples,
                       signal_samples = [],
                       data_sample = None,
                       output_fn = None,
                       plot_saver = None,
                       histogram_path = None,
                       file_path = None,
                       int_lumi = None,
                       int_lumi_nice = None,
                       canvas_title = '',
                       canvas_size = (700, 840),
                       canvas_top_margin = 0.01,
                       canvas_bottom_margin = 0.3,
                       canvas_left_margin = 0.1,
                       canvas_right_margin = 0.1,
                       join_info_override = None,
                       stack_draw_cmd = 'hist',
                       x_title = '',
                       y_title = 'arb. units',
                       y_title_offset = 1.3,
                       y_label_size = 0.035,
                       x_range = (None, None),
                       y_range = (None, None),
                       signal_color_override = None,
                       signal_line_width = 3,
                       signal_draw_cmd = 'hist',
                       data_marker_style = 20,
                       data_marker_size = 1.3,
                       data_draw_cmd = 'pe',
                       res_line_width = 2,
                       res_line_color = ROOT.kBlue+3,
                       res_y_title = 'data/MC',
                       res_y_title_offset = None,
                       res_y_label_size = 0.03,
                       res_draw_cmd = 'apez',
                       legend_pos = None,
                       verbose = False,
                       ):
    """JMTBAD.

    If histogram_path and file_path are not supplied, all of the
    sample objects must have a member object named 'hist' that has the
    histogram preloaded.

    file_path is of the format
    'path/to/root/files/filename_%(sample_name)s.root'.

    histogram_path is the path to the histogram inside the ROOT
    files, e.g. 'histos/RecoJets/njets'.

    int_lumi is the integrated luminosity to scale the MC to, in
    pb^-1.
    
    """

    all_samples = background_samples + signal_samples
    if data_sample is not None:
         all_samples.append(data_sample)
    
    if output_fn is None and plot_saver is None:
        raise ValueError('at least one of output_fn, plot_saver must be supplied')

    check_params = (file_path is None, histogram_path is None, int_lumi is None)
    if any(check_params) and not all(check_params):
        raise ValueError('must supply all of file_path, histogram_path, int_lumi or none of them')

    if file_path is None:
        for sample in all_samples:
            if not hasattr(sample, 'hist') or not issubclass(type(sample.hist), ROOT.TH1):
                raise ValueError('all sample objects must have hist preloaded if file_path is not supplied')
    else:
        previous_file_paths = list(set(vars(sample).get('file_path', None) for sample in all_samples))
        previous_file_paths_ok = len(previous_file_paths) == 1 and previous_file_paths[0] is not None
        for sample in all_samples:
            if not previous_file_paths_ok:
                sample._datamccomp_file_path = file_path
                sample._datamccomp_filename = file_path % sample
                sample._datamccomp_file = ROOT.TFile(sample._datamccomp_filename)
            sample.hist = sample._datamccomp_file.Get(histogram_path)
            if not issubclass(type(sample.hist), ROOT.TH1):
                raise RuntimeError('histogram %s not found in %s' % (histogram_path, sample._datamccomp_filename))
            if sample != data_sample:
                sample.hist.Scale(sample.partial_weight * int_lumi)
           
    #####################

    no_data_no_adjust_margins = data_sample is None and canvas_size == (700,840) and canvas_bottom_margin == 0.3
    if no_data_no_adjust_margins:
        canvas_size = (700, 700)

    canvas = ROOT.TCanvas('c_datamc_' + name, canvas_title, *canvas_size)
    if not no_data_no_adjust_margins:
        canvas.SetTopMargin(canvas_top_margin)
        canvas.SetBottomMargin(canvas_bottom_margin)
        canvas.SetLeftMargin(canvas_left_margin)
        canvas.SetRightMargin(canvas_right_margin)

    if plot_saver is not None:
        plot_saver.old_c = plot_saver.c
        plot_saver.c = canvas

    legend_entries = []
    stack = ROOT.THStack('s_datamc_' + name, '')
    sum_background = None
    for sample in background_samples:
        join, nice_name, color = sample.join_info if join_info_override is None else join_info_override(sample)
        sample.hist.SetLineColor(color)
        sample.hist.SetFillColor(color)
        if nice_name not in [l[1] for l in legend_entries] or not join:
            legend_entries.append((sample.hist, nice_name, 'F'))
        stack.Add(sample.hist)
        if sum_background is None:
            sum_background = sample.hist.Clone('sum_background_' + name)
        else:
            sum_background.Add(sample.hist)

        if verbose:
            print sample.name, get_integral(sample.hist, 0)

    stack.Draw(stack_draw_cmd)
    stack.SetTitle(';%s;%s' % (x_title, y_title))

    if data_sample is not None:
        stack.GetXaxis().SetLabelSize(0) # the data/MC ratio part will show the labels
    stack.GetYaxis().SetTitleOffset(y_title_offset)
    stack.GetYaxis().SetLabelSize(y_label_size)

    y_range_min, y_range_max = y_range
    if y_range_min is not None:
        stack.SetMinimum(y_range_min)
    if y_range_max is not None:
        stack.SetMaximum(y_range_max)

    for sample in signal_samples:
        sample.hist.SetLineColor(sample.color if signal_color_override is None else signal_color_override(sample))
        sample.hist.SetLineWidth(signal_line_width)
        sample.hist.Draw('same ' + signal_draw_cmd)

    if data_sample is not None:
        data_sample.hist.SetMarkerStyle(data_marker_style)
        data_sample.hist.SetMarkerSize(data_marker_size)
        data_sample.hist.Draw('same ' + data_draw_cmd)

    if legend_pos is not None:
        legend_entries.reverse()
        legend = ROOT.TLegend(*legend_pos)
        legend.SetBorderSize(0)
        for l in legend_entries:
            legend.AddEntry(*l)
        for sample in signal_samples:
            legend.AddEntry(sample.hist, sample.nice_name, 'L')
        if data_sample is not None:
            legend.AddEntry(data_sample.hist, 'data', 'LPE')
        legend.Draw()

    if int_lumi_nice is not None:
        t = ROOT.TPaveLabel(0.293, 0.875, 0.953, 0.975, 'CMS 2012 preliminary   #sqrt{s} = 8 TeV    #int L dt = %s' % int_lumi_nice, 'brNDC')
        t.SetTextSize(0.25)
        t.SetBorderSize(0)
        t.SetFillColor(0)
        t.SetFillStyle(0)
        t.Draw()

    if verbose:
        print name
        print 'data integral:', data_sample.hist.Integral(0, data_sample.hist.GetNbinsX()+1)
        print 'bkg  integral:', sum_background.Integral(0, sum_background.GetNbinsX()+1)
    
    ratio_pad, res_g = None, None
    if data_sample is not None:
        ratio_pad = ROOT.TPad('ratio_pad_' + name, '', 0, 0, 1, 1)
        ratio_pad.SetTopMargin(0.71)
        ratio_pad.SetLeftMargin(canvas_left_margin)
        ratio_pad.SetRightMargin(canvas_right_margin)
        ratio_pad.SetFillColor(0)
        ratio_pad.SetFillStyle(0)
        ratio_pad.Draw()
        ratio_pad.cd(0)

        res_g = poisson_means_divide(data_sample.hist, sum_background)
        res_g.SetLineWidth(res_line_width)
        res_g.SetLineColor(res_line_color)
        res_g.GetXaxis().SetLimits(sum_background.GetXaxis().GetXmin(), sum_background.GetXaxis().GetXmax())
        res_g.GetYaxis().SetLabelSize(res_y_label_size)
        res_g.GetYaxis().SetTitleOffset(res_y_title_offset if res_y_title_offset is not None else y_title_offset)
        res_g.GetYaxis().SetRangeUser(0,3)
        res_g.SetTitle(';%s;%s' % (x_title, res_y_title))
        res_g.Draw(res_draw_cmd)
        ln = ROOT.TLine(0,1, sum_background.GetBinLowEdge(sum_background.GetNbinsX()+1), 1)
        ln.SetLineStyle(4)
        ln.SetLineColor(ROOT.kBlue+3)
        ln.Draw()

    if plot_saver is not None:
        plot_saver.save(name)
        plot_saver.c = plot_saver.old_c
        plot_saver.c.cd()
    elif output_fn is not None:
        canvas.SaveAs(output_fn)

    return canvas, stack, sum_background, legend, ratio_pad, res_g

def detree(t, branches='run:lumi:event', cut='', xform=lambda x: tuple(int(y) for y in x)):
    """Dump specified branches from tree into a list of tuples, via an
    ascii file. By default all vars are converted into integers. The
    xform parameter specifies the function transforming the tuple of
    strings into the desired format."""
    
    tmp_fn = os.tmpnam()
    t.GetPlayer().SetScanRedirect(True)
    t.GetPlayer().SetScanFileName(tmp_fn)
    t.Scan(branches, cut, 'colsize=50')
    t.GetPlayer().SetScanRedirect(False)
    l = len(branches.split(':')) + 2
    for line in open(tmp_fn):
        if ' * ' in line and 'Row' not in line:
            yield xform(line.split('*')[2:l])

def differentiate_stat_box(hist, movement=1, new_color=None, new_size=None):
    """Move hist's stat box and change its line/text color. If
    movement is just an int, that number specifies how many units to
    move the box downward. If it is a 2-tuple of ints (m,n), the stat
    box will be moved to the left m units and down n units. A unit is
    the width or height of the stat box.

    Call TCanvas::Update first (and use TH1::Draw('sames') if
    appropriate) or else the stat box will not exist."""

    s = hist.FindObject('stats')

    if new_color is not None:
        s.SetTextColor(new_color)
        s.SetLineColor(new_color)

    if type(movement) == int:
        movement = (0,movement)
    m,n = movement
    
    x1,x2 = s.GetX1NDC(), s.GetX2NDC()
    y1,y2 = s.GetY1NDC(), s.GetY2NDC()

    if new_size is not None:
        x1 = x2 - new_size[0]
        y1 = y2 - new_size[1]

    s.SetX1NDC(x1 - (x2-x1)*m)
    s.SetX2NDC(x2 - (x2-x1)*m)
    s.SetY1NDC(y1 - (y2-y1)*n)
    s.SetY2NDC(y2 - (y2-y1)*n)

def draw_in_order(hists_and_cmds, sames=False):
    hists = [(h, h.GetMaximum(), cmd) for h,cmd in hists_and_cmds]
    hists.sort(key=lambda x: x[1], reverse=True)
    for i, (h, m, cmd) in enumerate(hists):
        if i > 0 and 'same' not in cmd:
            cmd += ' same'
            if sames:
                cmd += 's'
        h.Draw(cmd)

def flatten_directory(dir, prefix=''):
    """Take an input TDirectory object (a TFile is a TDirectory) and
    flatten its structure. E.g. for an input File with structure

    File
    \A
     \a1
     \a2
     \B
      \b1
    \c
    \d

    where uppercase names are directories and lowercase names are
    objects e.g. histos, we return
    ['A/a1', 'A/a2', 'A/B/b1', 'c', 'd'].
    """
    
    result = []
    for key in dir.GetListOfKeys():
        name = key.GetName()
        obj = dir.Get(name)
        if issubclass(type(obj), ROOT.TDirectory):
            for sub_name in flatten_directory(obj, name):
                result.append(name + '/' + sub_name)
        else:
            result.append(name)
    return result

def fit_gaussian(hist, factor=None, draw=False, cache=[]):
    """Fit a Gaussian to the histogram, and return a dict with fitted
    parameters and errors. If factor is supplied, fit only to range in
    hist.mean +/- factor * hist.rms.
    """

    if draw:
        opt = 'qr'
    else:
        opt = 'qr0'

    if factor is not None:
        fcn = core_gaussian(hist, factor)
        cache.append(fcn)
        hist.Fit(fcn, opt)
    else:
        hist.Fit('gaus', opt)
        fcn = hist.GetFunction('gaus')
        
    return {
        'constant': (fcn.GetParameter(0), fcn.GetParError(0)),
        'mu':       (fcn.GetParameter(1), fcn.GetParError(1)),
        'sigma':    (fcn.GetParameter(2), fcn.GetParError(2))
        }
    
def get_bin_content_error(hist, value):
    """For the given histogram, find the bin corresponding to the
    value and return its contents and associated
    error. Multi-dimensional histograms are supported; value may be a
    tuple in those cases.
    """

    if type(value) != type(()):
        value = (value,)
    bin = hist.FindBin(*value)
    return (hist.GetBinContent(bin), hist.GetBinError(bin))

def get_integral(hist, xlo=None, xhi=None, integral_only=False, include_last_bin=True):
    """For the given histogram, return the integral of the bins
    corresponding to the values xlo to xhi along with its error.
    """

    if xlo is None:
        binlo = 0
    else:
        binlo = hist.FindBin(xlo)

    if xhi is None:
        binhi = hist.GetNbinsX()+1
    else:
        binhi = hist.FindBin(xhi)
        if not include_last_bin:
            binhi -= 1

    integral = hist.Integral(binlo, binhi)
    if integral_only:
        return integral

    wsq = 0
    for i in xrange(binlo, binhi+1):
        wsq += hist.GetBinError(i)**2
    return integral, wsq**0.5

def get_hist_stats(hist, factor=None, draw=False):
    """For the given histogram, return a five-tuple of the number of
    entries, the underflow and overflow counts, the fitted sigma
    (using the function specified by fcnname, which must be an
    already-made ROOT.TF1 whose parameter(2) is the value used), and the
    RMS.
    """
    
    results = fit_gaussian(hist, factor, draw)
    results.update({
        'entries': hist.GetEntries(),
        'under':   hist.GetBinContent(0),
        'over':    hist.GetBinContent(hist.GetNbinsX()+1),
        'mean':    (hist.GetMean(), hist.GetMeanError()),
        'rms':     (hist.GetRMS(), hist.GetRMSError())
        })
    return results

class draw_hist_register:
    """Keep track of the otherwise-anonymous histograms produced by
    TTree::Draw. Can specify binning as well (same syntax as Draw
    expects). Use something like:

    hr = hist_register(tree)
    hist = hr.draw('ordinate:abscissa', '100,0,1,100,0,5')
    hist.SetTitle('ordinate vs. abscissa')
    """
    uniq = [0]
    
    def __init__(self, tree, use_weight=False):
        self.id = self.uniq[0]
        self.uniq[0] += 1
        self.tree = tree
        self.n = 0
        self.use_weight = use_weight
        self.clear()

    def clear(self):
        # don't reset self.n
        self.names = []
        self.hists = []
        
    def name_for_draw(self, draw_str, binning=''):
        name = 'h_%i_%i' % (self.id, self.n)
        self.names.append(name)
        self.n += 1
        if binning:
            binning = '(%s)' % binning
        return draw_str + '>>' + name + binning

    def draw(self, draw_str, cut='', binning='', get_n=False, tree=None, nice_name=None):
        if self.use_weight:
            if cut:
                cut = 'weight*(%s)' % cut
            else:
                cut = 'weight'
        varexp = self.name_for_draw(draw_str, binning)
        option = 'e' if self.use_weight else ''
        n = (tree if tree else self.tree).Draw(varexp, cut, option)
        h = getattr(ROOT, self.names[-1])
        self.hists.append(h)
        h.is2d = ':' in draw_str
        if nice_name is None:
            nice_name = draw_str.replace(':', '_vs_')
        h.nice_name = nice_name
        return (h,n) if get_n else h

def make_rms_hist(prof, name='', bins=None, cache={}):
    """Takes an input TProfile and produces a histogram whose bin contents are
    the RMS of the bins of the profile. Caches the histogram so that it doesn't
    get deleted by python before it gets finalized onto a TCanvas.

    If bins is a list of bin lower edges + last bin high edge,
    rebinning is done before making the RMS histogram. Due to a bug in
    ROOT's TProfile in versions less than 5.22 (?), rebinning is done
    manually here.
    """
    
    nbins = prof.GetNbinsX()
    if name == '':
        name = 'RMS' + prof.GetName()
    title = 'RMS ' + prof.GetTitle()
    old_axis = prof.GetXaxis()

    # Play nice with same-name histograms that were OK because they
    # were originally in different directories.
    while cache.has_key(name):
        name += '1'

    # Format of contents list: [(new_bin, (new_bin_content, new_bin_error)), ...]
    contents = []
    
    if bins:
        if type(bins) == type([]):
            bins = array('f', bins)
        new_hist = ROOT.TH1F(name, title, len(bins)-1, bins)
        new_axis = new_hist.GetXaxis()
        new_bins = {}
        for old_bin in xrange(1, nbins+1):
            new_bin = new_axis.FindBin(old_axis.GetBinLowEdge(old_bin))
            if not new_bins.has_key(new_bin):
                new_bins[new_bin] = [0., 0.]
            N = prof.GetBinEntries(old_bin)
            new_bins[new_bin][0] += N*prof.GetBinContent(old_bin)
            new_bins[new_bin][1] += N
        for val in new_bins.values():
            if val[1] > 0:
                val[0] /= val[1]
        contents = new_bins.items()
    else:
        new_hist = ROOT.TH1F(name, title, nbins, old_axis.GetXmin(), old_axis.GetXmax())
        for old_bin in xrange(1, nbins+1):
            f_bin = float(prof.GetBinContent(old_bin))
            ent_bin = float(prof.GetBinEntries(old_bin))
            contents.append((old_bin, (f_bin, ent_bin)))

    for new_bin, (f_bin, ent_bin) in contents:
        if f_bin > 0:
            f_bin = f_bin**0.5
        else:
            f_bin = 0
            
        if ent_bin > 0:
            err_bin = f_bin/(2.*ent_bin)**0.5
        else:
            err_bin = 0

        new_hist.SetBinContent(new_bin, f_bin)
        new_hist.SetBinError(new_bin, err_bin)
        
    cache[name] = new_hist
    return new_hist

def move_below_into_bin(h,a):
    """Given the TH1 h, add the contents of the bins below the one
    corresponding to a into that bin, and zero the bins below."""
    assert(h.Class().GetName().startswith('TH1')) # i bet there's a better way to do this...
    b = h.FindBin(a)
    bc = h.GetBinContent(b)
    bcv = h.GetBinError(b)**2
    for nb in xrange(0, b):
        bc += h.GetBinContent(nb)
        bcv += h.GetBinError(nb)**2
        h.SetBinContent(nb, 0)
        h.SetBinError(nb, 0)
    h.SetBinContent(b, bc)
    h.SetBinError(b, bcv**0.5)

def move_above_into_bin(h,a):
    """Given the TH1 h, add the contents of the bins above the one
    corresponding to a into that bin, and zero the bins above."""
    assert(h.Class().GetName().startswith('TH1')) # i bet there's a better way to do this...
    b = h.FindBin(a)
    bc = h.GetBinContent(b)
    bcv = h.GetBinError(b)**2
    for nb in xrange(b+1, h.GetNbinsX()+2):
        bc += h.GetBinContent(nb)
        bcv += h.GetBinError(nb)**2
        h.SetBinContent(nb, 0)
        h.SetBinError(nb, 0)
    h.SetBinContent(b, bc)
    h.SetBinError(b, bcv**0.5)

def move_overflow_into_last_bin(h):
    """Given the TH1 h, Add the contents of the overflow bin into the
    last bin, and zero the overflow bin."""
    assert(h.Class().GetName().startswith('TH1')) # i bet there's a better way to do this...
    nb = h.GetNbinsX()
    h.SetBinContent(nb, h.GetBinContent(nb) + h.GetBinContent(nb+1))
    h.SetBinError(nb, (h.GetBinError(nb)**2 + h.GetBinError(nb+1)**2)**0.5)
    h.SetBinContent(nb+1, 0)
    h.SetBinError(nb+1, 0)

def poisson_means_divide(h1, h2):
    return histogram_divide(h1, h2, confint=clopper_pearson_poisson_means, force_lt_1=False)

class plot_saver:
    i = 0
    
    def __init__(self, plot_dir=None, html=True, log=True, root=True, pdf=False, pdf_log=False, C=False, C_log=False, size=(820,630), per_page=-1):
        self.c = ROOT.TCanvas('c%i' % plot_saver.i, '', *size)
        plot_saver.i += 1
        self.saved = []
        self.html = html
        self.set_plot_dir(plot_dir)
        self.log = log
        self.root = root
        self.pdf = pdf
        self.pdf_log = pdf_log
        self.C = C
        self.C_log = C_log
        self.per_page = per_page

    def __del__(self):
        self.write_index()

    def anchor_name(self, fn):
        return os.path.splitext(os.path.basename(fn))[0].replace('.', '_').replace('/', '_')
    
    def write_index(self):
        if not self.saved or not self.html:
            return
        html = open(os.path.join(self.plot_dir, 'index.html'), 'wt')
        if self.per_page > 0:
            nsaved = len(self.saved)
            ndxs = range(0, nsaved, self.per_page)
            npages = len(ndxs)
            for page, ndx in enumerate(ndxs):
                self.write_index_page(self.saved[ndx:ndx+self.per_page], page, npages)
        else:
            self.write_index_page(self.saved, 0, 1)
            
    def write_index_page(self, saved, page, num_pages):
        def html_fn(page):
            if page == 0:
                return 'index.html'
            else:
                return 'index_%i.html' % page
            return 
        html = open(os.path.join(self.plot_dir, html_fn(page)), 'wt')
        html.write('<html><body><pre>\n')
        def write_pages_line():
            html.write('pages: ')
            for i in xrange(num_pages):
                if i == page:
                    html.write('<b>%i</b>  ' % i)
                else:
                    html.write('<a href="%s">%i</a>  ' % (html_fn(i), i))
            html.write('\n')
        if num_pages > 1:
            write_pages_line()
        html.write('<a href="..">.. (parent directory)</a>\n')
        for i, save in enumerate(saved):
            if type(save) == str:
                # this is just a directory link
                html.write('<a href="%s">%10i%32s%s</a>\n' % (save, i, 'change directory: ', save))
                continue

            fn, log, root, pdf, pdf_log, C, C_log = save

            bn = os.path.basename(fn)
            html.write('<a href="#%s">%10i</a> ' % (self.anchor_name(fn), i))
            if log:
                html.write(' <a href="%s">log</a>' % os.path.basename(log))
            else:
                html.write('    ')
            if root:
                html.write(' <a href="%s">root</a>' % os.path.basename(root))
            else:
                html.write('     ')
            if pdf:
                html.write(' <a href="%s">pdf</a>' % os.path.basename(pdf))
            else:
                html.write('     ')
            if pdf_log:
                html.write(' <a href="%s">pdf_log</a>' % os.path.basename(pdf_log))
            else:
                html.write('     ')
            if C:
                html.write(' <a href="%s">C</a>' % os.path.basename(C))
            else:
                html.write('     ')
            if C_log:
                html.write(' <a href="%s">C_log</a>' % os.path.basename(C_log))
            else:
                html.write('     ')
            html.write('  <a href="%s">%s</a>' % (bn, bn))
            html.write('\n')
        html.write('<br><br>')
        for i, save in enumerate(saved):
            if type(save) == str:
                continue # skip dir entries
            fn, log, root, pdf, pdf_log, C, C_log = save
            bn = os.path.basename(fn)
            if root:
                rootlink = ', <a href="%s">root</a>' % os.path.basename(root)
            html.write('<h4 id="%s"><a href="#%s">%s</a>%s</h4><br>\n' % (self.anchor_name(fn), self.anchor_name(fn), bn.replace('.png', ''), rootlink))
            if log:
                html.write('<img src="%s"><img src="%s"><br><br>\n' % (bn, os.path.basename(log)))
            else:
                html.write('<img src="%s"><br><br>\n' % bn)
        if num_pages > 1:
            write_pages_line()
        html.write('</pre></body></html>\n')
        
    def set_plot_dir(self, plot_dir):
        self.write_index()
        self.saved = []
        if plot_dir is not None and '~' in plot_dir:
            plot_dir = os.path.expanduser(plot_dir)
        self.plot_dir = plot_dir
        if plot_dir is not None:
            os.system('mkdir -p %s' % self.plot_dir)

    def save_dir(self, n):
        if self.plot_dir is None:
            raise ValueError('save_dir called before plot_dir set!')
        self.saved.append(n)

    def save(self, n, log=None, root=None, pdf=None, pdf_log=None, C=None, C_log=None, logz=None):
        if logz:
            logfcn = self.c.SetLogz
        else:
            logfcn = self.c.SetLogy

        log = self.log if log is None else log
        root = self.root if root is None else root
        pdf = self.pdf if pdf is None else pdf
        pdf_log = self.pdf_log if pdf_log is None else pdf_log
        C = self.C if C is None else C
        C_log = self.C_log if C_log is None else C_log
        
        if self.plot_dir is None:
            raise ValueError('save called before plot_dir set!')
        self.c.SetLogy(0)
        fn = os.path.join(self.plot_dir, n + '.png')
        self.c.SaveAs(fn)
        if root:
            root = os.path.join(self.plot_dir, n + '.root')
            self.c.SaveAs(root)
        if log:
            logfcn(1)
            log = os.path.join(self.plot_dir, n + '_log.png')
            self.c.SaveAs(log)
            logfcn(0)
        if pdf:
            pdf = os.path.join(self.plot_dir, n + '.pdf')
            self.c.SaveAs(pdf)
        if pdf_log:
            logfcn(1)
            pdf_log = os.path.join(self.plot_dir, n + '_log.pdf')
            self.c.SaveAs(pdf_log)
            logfcn(0)
        if C:
            C = os.path.join(self.plot_dir, n + '.C')
            self.c.SaveAs(C_fn)
        if C_log:
            logfcn(1)
            C_log = os.path.join(self.plot_dir, n + '_log.C')
            self.c.SaveAs(C_log)
            logfcn(0)
        self.saved.append((fn, log, root, pdf, pdf_log, C, C_log))

def rainbow_palette(num_colors=500):
    """Make a rainbow palette with the specified number of
    colors. Also call SetNumberContours so it actually gets used when
    drawing COLZ."""
    
    r = array('d', [0, 0, 0, 1, 1])
    g = array('d', [0, 1, 1, 1, 0])
    b = array('d', [1, 1, 0, 0, 0])
    stops = array('d', [float(i)/4 for i in xrange(5)])
    ROOT.TColor.CreateGradientColorTable(5, stops, r, g, b, num_colors)
    ROOT.gStyle.SetNumberContours(num_colors)

def real_hist_max(h, return_bin=False, user_range=None, use_error_bars=True):
    """Find the real maximum value of the histogram, taking into
    account the error bars and/or the specified range."""

    m_ibin = None
    m = 0

    if user_range is None:
        b1, b2 = 1, h.GetNbinsX() + 1
    else:
        b1, b2 = h.FindBin(user_range[0]), h.FindBin(user_range[1])+1
    
    for ibin in xrange(b1, b2):
        if use_error_bars:
            v = h.GetBinContent(ibin) + h.GetBinError(ibin)
        else:
            v = h.GetBinContent(ibin)
        if v > m:
            m = v
            m_ibin = ibin
    if return_bin:
        return m_ibin, m
    else:
        return m

def real_hist_min(h, return_bin=False, user_range=None):
    """Find the real minimum value of the histogram, ignoring empty
    bins, and taking into account the specified range."""

    m_ibin = None
    m = 99e99

    if user_range is None:
        b1, b2 = 1, h.GetNbinsX() + 1
    else:
        b1, b2 = h.FindBin(user_range[0]), h.FindBin(user_range[1])+1
    
    for ibin in xrange(b1, b2):
        v = h.GetBinContent(ibin)
        if v > 0 and v < m:
            m = v
            m_ibin = ibin
    if return_bin:
        return m_ibin, m
    else:
        return m

def set_style(date_pages=False):
    ROOT.gROOT.SetStyle('Plain')
    ROOT.gStyle.SetFillColor(0)
    if date_pages:
        ROOT.gStyle.SetOptDate()
    ROOT.gStyle.SetOptStat(111111)
    ROOT.gStyle.SetOptFit(1111)
    ROOT.gStyle.SetPadTickX(1)
    ROOT.gStyle.SetPadTickY(1)
    ROOT.gStyle.SetMarkerSize(.1)
    ROOT.gStyle.SetMarkerStyle(8)
    ROOT.gStyle.SetGridStyle(3)
    ROOT.gStyle.SetPaperSize(ROOT.TStyle.kA4)
    ROOT.gStyle.SetStatW(0.25)
    ROOT.gStyle.SetStatFormat('6.4g')
    ROOT.gStyle.SetPalette(1)
    ROOT.gStyle.SetTitleFont(42, 'XYZ')
    ROOT.gStyle.SetLabelFont(42, 'XYZ')
    ROOT.gStyle.SetStatFont(42)
    ROOT.gStyle.SetLegendFont(42)
    ROOT.gErrorIgnoreLevel = 1001 # Suppress TCanvas::SaveAs messages.

def sort_histogram_pair(h1, h2, by=real_hist_max):
    """Return the pair ordered by e.g. real_hist_max to know which to
    draw first."""
    
    if real_hist_max(h1) > real_hist_max(h2):
        return h1,h2
    else:
        return h2,h1

def ttree_iterator(tree, return_tree=False):
    for jentry in xrange(tree.GetEntriesFast()):
        if tree.LoadTree(jentry) < 0: break
        if tree.GetEntry(jentry) <= 0: continue
        if return_tree:
            yield jentry, tree
        else:
            yield jentry
            
__all__ = [
    'apply_hist_commands',
    'bin_iterator',
    'check_consistency',
    'histogram_divide',
    'clopper_pearson',
    'clopper_pearson_poisson_means',
    'compare_all_hists',
    'core_gaussian',
    'cumulative_histogram',
    'cut',
    'data_mc_comparison',
    'detree',
    'differentiate_stat_box',
    'draw_in_order',
    'flatten_directory',
    'fit_gaussian',
    'get_bin_content_error',
    'get_integral',
    'get_hist_stats',
    'draw_hist_register',
    'make_rms_hist',
    'move_below_into_bin',
    'move_above_into_bin',
    'move_overflow_into_last_bin',
    'plot_saver',
    'poisson_intervalize',
    'poisson_means_divide',
    'rainbow_palette',
    'real_hist_max',
    'real_hist_min',
    'set_style',
    'sort_histogram_pair',
    'ttree_iterator',
    'ROOT',
    ]
