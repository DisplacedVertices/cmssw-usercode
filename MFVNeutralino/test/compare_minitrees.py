from JMTucker.MFVNeutralino.MiniTreeBase import *

ps = plot_saver(plot_dir('compare_minitrees'), size=(600,600))

fn1 = '/uscms_data/d2/tucker/crab_dirs/MiniTreeV16/mfv_neu_tau10000um_M0800.root'
fn2 = '/uscms_data/d2/tucker/crab_dirs/MiniTreeV16m/mfv_neu_tau10000um_M0800.root'
nice1 = 'aod'
nice2 = 'miniaod'

f1, t1 = get_f_t(fn1)
f2, t2 = get_f_t(fn2)
n1, n2 = float(t1.GetEntries()), float(t2.GetEntries())
print 'entries %6i %6i' % (n1, n2)

def foo(which, var_name, title, draw_str, cut):
    nm1 = '%s_%s' % (var_name, nice1)
    nm2 = '%s_%s' % (var_name, nice2)
    x1 = t1.Draw(draw_str % nm1, cut) 
    h1 = getattr(ROOT, nm1).Clone(nm1)
    x2 = t2.Draw(draw_str % nm2, cut) 
    h2 = getattr(ROOT, nm2).Clone(nm2)
    #h1.Scale(1/h1.Integral())
    #h2.Scale(1/h2.Integral())
    h1.SetLineColor(ROOT.kRed)
    h2.SetLineColor(ROOT.kBlue)
    for h in h1,h2:
        h.SetTitle(title)
        h.SetLineWidth(2)
    ratios_plot(var_name,
                (h1,h2),
                plot_saver=ps,
                res_divide_opt={'confint': clopper_pearson_poisson_means, 'force_le_1': False},
                statbox_size=(0.2,0.2),
                res_y_range=0.05,
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

foo('dbv1vtx',   '1dbv', 'nvtx==1;d_{BV} (cm);events/200 #mum', 'dist0>>%s(100,0,2)',  'nvtx==1')
foo('dbvge2vtx', '2dbv', 'nvtx>=2;d_{BV} (cm);events/200 #mum', 'dist0>>%s(100,0,2)',  'nvtx>=2')
foo('ge2vtx', 'dvv',  'nvtx>=2;d_{VV} (cm);events/200 #mum', 'svdist>>%s(200,0,4)', 'nvtx>=2')
foo('2vtx',   'dvv2', 'nvtx==2;d_{VV} (cm);events/200 #mum', 'svdist>>%s(200,0,4)', 'nvtx==2')
foo('ge3vtx', 'dvv3', 'nvtx>=3;d_{VV} (cm);events/400 #mum', 'svdist>>%s(100,0,4)', 'nvtx>=3')

xform = lambda x: tuple(int(y) for y in x[:-1]) + (float(x[-1]),)
d1, d2 = [dict(((a,b,c),(d,e)) for a,b,c,d,e in detree(t, 'run:lumi:event:nvtx:svdist*(nvtx>=2)', xform=xform)) for t in (t1,t2)]
rles = list(set(d1.keys()) | set(d2.keys()))
h_nvtx = ROOT.TH2F('h_nvtx', ';nvtx %s;nvtx %s' % (nice1, nice2), 10, 0, 10, 10, 0, 10)
h_svdist = ROOT.TH2F('h_svdist', ';svdist %s;svdist %s' % (nice1, nice2), 100, 0, 4, 100, 0, 4)
h_svdistzoom = ROOT.TH2F('h_svdistzoom', ';svdist %s;svdist %s' % (nice1, nice2), 100, 0, 0.4, 100, 0, 0.4)
h_svdisteq = ROOT.TH2F('h_svdisteq', ';svdist %s;svdist %s' % (nice1, nice2), 100, 0, 4, 100, 0, 4)
h_svdistneq = ROOT.TH2F('h_svdistneq', ';svdist %s;svdist %s' % (nice1, nice2), 100, 0, 4, 100, 0, 4)


for rle in rles:
    nvtx1, svdist1 = d1.get(rle,(0,0))
    nvtx2, svdist2 = d2.get(rle,(0,0))
    h_nvtx.Fill(nvtx1, nvtx2)
    h_svdist.Fill(svdist1, svdist2)
    h_svdistzoom.Fill(svdist1, svdist2)
    if nvtx1 == nvtx2 and nvtx2 == 2 or nvtx2 == 3:
        h_svdisteq.Fill(svdist1, svdist2)
    if set([nvtx1, nvtx2]) == set([2,3]):
        h_svdistneq.Fill(svdist1, svdist2)

h1 = h_nvtx.ProjectionX()
h2 = h_nvtx.ProjectionY()
h1.SetName(nice1)
h2.SetName(nice2)
h1.SetLineColor(ROOT.kRed)
h2.SetLineColor(ROOT.kBlue)
for h in h1,h2:
    h.SetLineWidth(2)
h1.Draw('hist')
h2.Draw('hist sames')
ps.c.Update()
differentiate_stat_box(h1, (1,0), new_size=(0.3,0.3))
differentiate_stat_box(h2, (0,0), new_size=(0.3,0.3))
ps.save('h_nvtx')

h_nvtx.Draw('colz text00')
h_nvtx.SetStats(0)
ps.save('h_nvtx_scatter', logz=True)

h_svdist.Draw('colz')
h_svdist.SetStats(0)
ps.save('h_svdist', logz=True)

h_svdistzoom.Draw('colz')
h_svdistzoom.SetStats(0)
ps.save('h_svdistzoom', logz=True)

h_svdisteq.Draw('colz')
h_svdisteq.SetStats(0)
ps.save('h_svdisteq', logz=True)

h_svdistneq.Draw('colz')
h_svdistneq.SetStats(0)
ps.save('h_svdistneq', logz=True)
