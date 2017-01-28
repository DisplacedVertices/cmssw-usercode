from collections import defaultdict
from JMTucker.Tools.LumiLines import *
from JMTucker.Tools.ROOTTools import *
set_style()

year, ntracks, oneortwo = 2015, 3, 1

plot_path = 'vertex_xsec_%i_%itrk_%iV' % (year, ntracks, oneortwo)
title = '%i, %i-track %i-vtx' % (year, ntracks, oneortwo)
fns = ['/uscms_data/d2/tucker/crab_dirs/MinitreeV10_sidebanddata2015/JetHT2015D.root'] if year == 2015 else []
tree_path = 'tre%i%i/t' % (ntracks, ntracks) if ntracks < 5 else 'mfvMiniTree/t'

ps = plot_saver(plot_dir(plot_path), size=(1200,600), log=False, pdf=True)
lls = LumiLines('/uscms/home/tucker/public/mfv/2015plus2016.gzpickle')

runs = lls.runs(year)
nvtx = defaultdict(int)

for fn in fns:
    f = ROOT.TFile(fn)
    t = f.Get(tree_path)
    for (run,) in detree(t, 'run', 'nvtx==%i' % oneortwo):
        nvtx[run] += 1

excludes = [
    ('all', []),
#    ('exclude_small_lumi', [9,43] if year == 2015 else []),
#    ('exclude_one_small_lumi_run', [1]),
#    ('exclude_obvious', range(19) + [142,143,144]),
#    ('only_low', range(19, 500)),
    ]

for exclude_name, exclude in excludes:
    print 'excludes:', exclude_name

    min_nvtx = 1e99
    max_nvtx = 0
    zero_lumis = []
    lsum = 0
    nruns = len(runs)
    xsec        = ROOT.TGraphAsymmErrors(nruns)
    xsec_per_pu = ROOT.TGraphAsymmErrors(nruns)

    runs_used = 0
    for i, run in enumerate(runs):
        if i in exclude:
            continue

        n = nvtx[run]
        min_nvtx = min(n, min_nvtx)
        max_nvtx = max(n, max_nvtx)
        lumi = lls.recorded(run)/1e6
        lumi_frac_uncert = 0.027 if run <= 260627 else 0.062
        lumi_uncert = lumi_frac_uncert * lumi
        avg_pu = lls.avg_pu(run) if lumi > 0 else -1

        if lumi > 0:
            if not exclude:
                print '(%3i) %i: %5i in %10.5g +- %10.5g/pb -> %10.5g pb,  %10.5g pb/PU' % (i, run, n, lumi, lumi_uncert, n/lumi, n/lumi/avg_pu)
            lsum += lumi

            x = i
            y = n
            yl, yh = poisson_interval(n)
            y  /= lumi
            yl /= lumi
            yh /= lumi
            el = y - yl
            eh = yh - y
            #el = (el**2 + (lumi_frac_uncert*lumi)**2)**0.5
            #eh = (eh**2 + (lumi_frac_uncert*lumi)**2)**0.5
            #yl = y - el
            #yh = y + eh
            xsec.SetPoint(i, x, y)
            xsec.SetPointEYlow (i, el)
            xsec.SetPointEYhigh(i, eh)

            y  /= avg_pu
            yl /= avg_pu
            yh /= avg_pu
            xsec_per_pu.SetPoint(i, x, y)
            xsec_per_pu.SetPointEYlow (i, y - yl)
            xsec_per_pu.SetPointEYhigh(i, yh - y)

            runs_used += 1
        else:
            zero_lumis.append(run)

    print 'min nvtx:', min_nvtx
    print 'max nvtx:', max_nvtx

    if zero_lumis:
        for run in zero_lumis:
            print 'zero lumi for run %i with %i 1V events' % (run, nvtx[run])

    print 'lumi sum:', lsum/1e3, '/fb'

    fit_range = (0, nruns-1)
    if year == 2015 and len(fns) == 1:
        fit_range = (8,nruns-1)
    fcn = ROOT.TF1('fcn', 'pol0', *fit_range)

    for i,g in enumerate((xsec, xsec_per_pu)):
        g.SetTitle('%s events  # runs: %i;i_{run};#sigma (pb)' % (title, runs_used))
        g.SetMarkerStyle(20)
        g.SetMarkerSize(0.5)
        g.SetFillColor(38)
        g.SetFillStyle(3001)
        if i == 1:
            g.GetYaxis().SetTitle('#sigma / PU (pb)')
        g.Draw('A2')
        g.Draw('P')
        g.Fit(fcn, 'QR')
        name = exclude_name + ('_xsec' if i == 0 else '_xsec_per_pu')
        ps.save(name)
        g.GetYaxis().SetRangeUser(0, 6 * fcn.GetParameter(0))
        ps.save(name + '_zoom')

    print '\n'

