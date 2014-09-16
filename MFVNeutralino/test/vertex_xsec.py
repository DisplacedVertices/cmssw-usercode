from collections import defaultdict
from JMTucker.Tools.LumiLines import *
from JMTucker.Tools.ROOTTools import *
set_style()
ps = plot_saver('plots/vertex_xsec_v20', size=(1200,600), log=False)

lls = LumiLines('/uscms/home/tucker/mfvrecipe/lumi.gzpickle')

f = ROOT.TFile('crab/MiniTreeV20_redux/MultiJetPk2012.root')
t = f.Get('mfvMiniTree/t')

nvtx = defaultdict(int)
for jentry in ttree_iterator(t):
    nvtx[t.run] += 1

runs = sorted(nvtx.keys())

excludes = [
    ('all', []),
    ('exclude_obvious', range(19) + [142,143,144]),
    ('only_low', range(19, 500)),
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
        avg_pu = lls.avg_pu(run) if lumi > 0 else -1
        if lumi > 0:
            if not exclude:
                print '(%3i) %i: %5i in %10.5g/pb -> %10.5g pb,  %10.5g pb/PU' % (i, run, n, lumi, n/lumi, n/lumi/avg_pu)
            lsum += lumi

            x = i
            y = n
            yl, yh = poisson_interval(n)
            y  /= lumi
            yl /= lumi
            yh /= lumi
            xsec.SetPoint(i, x, y)
            xsec.SetPointEYlow (i, y - yl)
            xsec.SetPointEYhigh(i, yh - y)

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

    for g in (xsec, xsec_per_pu):
        g.SetTitle('# runs: %i  total lumi: %.1f/fb;i_{run};1V event #sigma (pb)' % (runs_used, lsum/1e3))
        g.SetMarkerStyle(20)
        g.SetMarkerSize(0.5)

    xsec.Draw('AP')
    xsec.Fit('pol0')
    ps.save(exclude_name + '_xsec')

    xsec_per_pu.GetYaxis().SetTitle('1V event #sigma / PU (pb)')
    xsec_per_pu.Draw('AP')
    xsec_per_pu.Fit('pol0')
    ps.save(exclude_name + '_xsec_per_pu')

    print '\n'

