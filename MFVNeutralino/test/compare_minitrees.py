from DVCode.MFVNeutralino.MiniTreeBase import *

ps = plot_saver(plot_dir('compare_minitrees', temp=True), size=(600,600))

fn1 = '/uscms_data/d2/tucker/crab_dirs/MiniTreeV25mv3/mfv_stopdbardbar_tau010000um_M0800_2017.root'
fn2 = '/uscms_data/d2/tucker/crab_dirs/MiniTreeV25mv3_maxnm1dz50um_onlyonce/mfv_stopdbardbar_tau010000um_M0800_2017.root'
nice1 = 'nom'
nice2 = 'mxdz20'
req_genmatch = False # whether to only use 1/2 vtx events where one/both vertices "match" a generated lsp
one2one = True # whether to compare result event by event (must be same events but processed differently)
scale1, scale2 = 1., 1.  # not smart enough to figure out the appropriate scaling by e.g. nevents generated
dbvbinning = '200 #mum', '100,0,2'
dvvbinning = '400 #mum', '100,0,4'

########################################################################

f1, t1 = get_f_t(fn1)
f2, t2 = get_f_t(fn2)
n1, n2 = float(t1.GetEntries()), float(t2.GetEntries())
nr1, nr2 = Samples.norm_from_file(f1), Samples.norm_from_file(f2)
print 'entries %6i/%6i %6i/%6i -> nr2/nr1 = %.3f' % (n1, nr1, n2, nr2, nr2/nr1)

def foo(which, var_name, title, draw_str, cut):
    nm1 = '%s_%s' % (var_name, nice1)
    nm2 = '%s_%s' % (var_name, nice2)
    x1 = t1.Draw(draw_str % nm1, cut) 
    h1 = getattr(ROOT, nm1).Clone(nm1)
    x2 = t2.Draw(draw_str % nm2, cut) 
    h2 = getattr(ROOT, nm2).Clone(nm2)
    h1.Scale(scale1)
    h2.Scale(scale2)
    h1.SetLineColor(ROOT.kRed)
    h2.SetLineColor(ROOT.kBlue)
    for h in h1,h2:
        h.SetTitle(title)
        h.SetLineWidth(2)
    ratios_plot(var_name,
                (h1,h2),
                plot_saver=ps,
                res_fit='pol1',
                res_divide_opt={'confint': clopper_pearson_poisson_means, 'force_le_1': False},
                statbox_size=(0.2,0.2),
                res_y_range=0.25,
                res_lines = [(1.0, 1, 1, 2)],
                )
    ef1, ef1l, ef1h = clopper_pearson(x1, n1)
    ef2, ef2l, ef2h = clopper_pearson(x2, n2)
    ef1e = (ef1h - ef1l) / 2
    ef2e = (ef2h - ef2l) / 2
    m1, m1e = h1.GetMean(), h1.GetMeanError()
    m2, m2e = h2.GetMean(), h2.GetMeanError()
    r1, r1e = h1.GetRMS(), h1.GetRMSError()
    r2, r2e = h2.GetRMS(), h2.GetRMSError()
    to_print = (which,) + \
        (x1, ef1, ef1e) + \
        (x2, ef2, ef2e) + \
        (m1, m1e, m2, m2e, m1 - m2, (m1e**2 + m2e**2)**0.5) + \
        (r1, r1e, r2, r2e, r1 - r2, (r1e**2 + r2e**2)**0.5)
    fmt = '%10s: n1 %5i (%.3f +- %.3f) n2 %5i (%.3f +- %.3f)  means (%.3f +- %.3f) - (%.3f +- %.3f) = %.3f +- %.3f  rmses (%.3f +- %.3f) - (%.3f +- %.3f) = %.3f +- %.3f'
    print fmt % to_print

def genmatch_cut(c, n):
    if not req_genmatch:
        return c
    if n == 1:
        gmc = 'genmatch0'
    elif n >= 2:
        gmc = 'genmatch0 && genmatch1'
    if c:
        return '(%s) && (%s)' % (c, gmc)
    else:
        return gmc

foo('dbv1vtx',   '1dbv', 'nvtx==1;d_{BV} (cm);events/' + dbvbinning[0], 'dist0>>%s('  + dbvbinning[1] + ')', genmatch_cut('nvtx==1', 1))
foo('dbvge2vtx', '2dbv', 'nvtx>=2;d_{BV} (cm);events/' + dbvbinning[0], 'dist0>>%s('  + dbvbinning[1] + ')', genmatch_cut('nvtx>=2', 2))
foo('ge2vtx',    'dvv',  'nvtx>=2;d_{VV} (cm);events/' + dvvbinning[0], 'svdist>>%s(' + dvvbinning[1] + ')', genmatch_cut('nvtx>=2', 2))
foo('2vtx',      'dvv2', 'nvtx==2;d_{VV} (cm);events/' + dvvbinning[0], 'svdist>>%s(' + dvvbinning[1] + ')', genmatch_cut('nvtx==2', 2))
foo('ge3vtx',    'dvv3', 'nvtx>=3;d_{VV} (cm);events/' + dvvbinning[0], 'svdist>>%s(' + dvvbinning[1] + ')', genmatch_cut('nvtx>=3', 3))

if one2one:
    xform = lambda x: tuple(int(y) for y in x[:3]) + tuple(float(y) for y in x[3:])
    d1, d2 = [{tuple(x[:3]) : tuple(x[3:]) for x in detree(t, 'run:lumi:event:nvtx:svdist:ntk0:ntk1', genmatch_cut('', 2), xform=xform)} for t in (t1,t2)]
    rles = list(set(d1.keys()) | set(d2.keys()))
    h_nvtx = ROOT.TH2F('h_nvtx', ';nvtx %s;nvtx %s' % (nice1, nice2), 10, 0, 10, 10, 0, 10)
    h_svdist = ROOT.TH2F('h_svdist', ';svdist %s;svdist %s' % (nice1, nice2), 100, 0, 4, 100, 0, 4)
    h_svdistzoom = ROOT.TH2F('h_svdistzoom', ';svdist %s;svdist %s' % (nice1, nice2), 100, 0, 0.4, 100, 0, 0.4)
    h_svdisteq = ROOT.TH2F('h_svdisteq', ';svdist %s;svdist %s' % (nice1, nice2), 100, 0, 4, 100, 0, 4)
    h_svdistneq = ROOT.TH2F('h_svdistneq', ';svdist %s;svdist %s' % (nice1, nice2), 100, 0, 4, 100, 0, 4)
    h_ntk0 = ROOT.TH2F('h_ntk0', ';ntk0 %s;ntk0 %s' % (nice1, nice2), 50, 0, 50, 50, 0, 50)
    h_ntk1 = ROOT.TH2F('h_ntk1', ';ntk1 %s;ntk1 %s' % (nice1, nice2), 50, 0, 50, 50, 0, 50)
    h_ntk0eq = ROOT.TH2F('h_ntk0eq', ';ntk0 %s;ntk0 %s' % (nice1, nice2), 50, 0, 50, 50, 0, 50)
    h_ntk1eq = ROOT.TH2F('h_ntk1eq', ';ntk1 %s;ntk1 %s' % (nice1, nice2), 50, 0, 50, 50, 0, 50)
    h_ntk0neq = ROOT.TH2F('h_ntk0neq', ';ntk0 %s;ntk0 %s' % (nice1, nice2), 50, 0, 50, 50, 0, 50)
    h_ntk1neq = ROOT.TH2F('h_ntk1neq', ';ntk1 %s;ntk1 %s' % (nice1, nice2), 50, 0, 50, 50, 0, 50)

    na = 0,0,0,0
    for rle in rles:
        nvtx1, svdist1, ntk01, ntk11 = d1.get(rle, na)
        nvtx2, svdist2, ntk02, ntk12 = d2.get(rle, na)
        h_nvtx.Fill(nvtx1, nvtx2)
        h_svdist.Fill(svdist1, svdist2)
        h_svdistzoom.Fill(svdist1, svdist2)
        h_ntk0.Fill(ntk01, ntk02)
        h_ntk1.Fill(ntk11, ntk12)
        if nvtx1 == nvtx2 and nvtx2 == 2 or nvtx2 == 3:
            h_svdisteq.Fill(svdist1, svdist2)
            h_ntk0eq.Fill(ntk01, ntk02)
            h_ntk1eq.Fill(ntk11, ntk12)
        if set([nvtx1, nvtx2]) == set([2,3]):
            h_svdistneq.Fill(svdist1, svdist2)
            h_ntk0neq.Fill(ntk01, ntk02)
            h_ntk1neq.Fill(ntk11, ntk12)

    for nh in 'nvtx', 'ntk0', 'ntk1':
        h = eval('h_%s' % nh)
        h1 = h.ProjectionX()
        h2 = h.ProjectionY()
        h1.SetName(nice1)
        h2.SetName(nice2)
        h1.SetLineColor(ROOT.kRed)
        h2.SetLineColor(ROOT.kBlue)
        for h in h1,h2:
            h.SetLineWidth(2)
        draw_in_order(((h1,h2), 'hist'), True)
        ps.c.Update()
        differentiate_stat_box(h1, (1,0), new_size=(0.3,0.3))
        differentiate_stat_box(h2, (0,0), new_size=(0.3,0.3))
        ps.save(nh + '_1d')

    for nh in 'nvtx', 'svdist', 'svdistzoom', 'svdisteq', 'svdistneq', 'ntk0', 'ntk1', 'ntk0eq', 'ntk1eq', 'ntk0neq', 'ntk1neq':
        h = eval('h_%s' % nh)
        cmd = 'colz'
        if nh == 'nvtx':
            cmd += ' text00'
        h.Draw(cmd)
        h.SetStats(0)
        ps.save(nh, logz=True)
