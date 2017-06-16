# for x in $crd/TrackMoverMCTruthV14/*.root ; do echo $(printf "%-50s" $(basename $x .root)) $(./mctruth.exe $x $(basename $x) 0.0252 ); done | tee mctruths.txt

import sys
from JMTucker.Tools.ROOTTools import *
from JMTucker.Tools import Samples
from JMTucker.MFVNeutralino.PerSignal import PerSignal

mctruths_fn = sys.argv[1]
plot_path = sys.argv[2]

set_style()
ps = plot_saver(plot_path, size=(600,600), log=False)

# ( for x in $crd/TrackMoverMCTruthV14/*.root; echo $(basename $x .root) $(./mctruth.exe $x $(basename x) 0.0084) ) | tee mctruths.txt
for line in open(mctruths_fn):
    line = line.strip().replace('+- ', '')
    if line and 'nan' not in line:
        line = line.split()
        sname = line.pop(0)
        den = float(line.pop(0))
        if hasattr(Samples, sname):
            sample = getattr(Samples, sname)
            sample.ys = [float(x) for x in line]
        else:
            print 'no sample', sname

def filter(ss):
    return [s for s in ss if not s.name.startswith('my_') and s.tau == 10000 and s.mass not in (500,3000)]
multijet = filter(Samples.mfv_signal_samples)
dijet    = filter(Samples.mfv_ddbar_samples)

# for x in nocuts ntracks all; do printf "# $x\n["; cat effs_* | grep -A4 background | grep $x | tr '-' ' ' | awk '{printf "(%.2f, %.2f),\n", $2, $NF}'; echo \],; done
trackmover_data = [
    # nocuts
    [(88.89, 0.01),
     (92.64, 0.02),
     (93.95, 0.05),
     (97.67, 0.00),
     (97.72, 0.01),
     (97.90, 0.04),
     ],
    # ntracks
    [(86.87, 0.01),
     (91.23, 0.02),
     (92.67, 0.06),
     (97.15, 0.00),
     (97.27, 0.01),
     (97.39, 0.05),
     ],
    # all
    [(71.94, 0.01),
     (85.83, 0.02),
     (89.74, 0.06),
     (94.71, 0.01),
     (96.25, 0.02),
     (96.79, 0.05),
     ],
    ]
trackmover_nice = ['n_{l} = %i, n_{b} = %i' % (l,b) for l in 2,3 for b in 0,1,2]
g,m = ROOT.kGreen, ROOT.kMagenta
trackmover_colors = [g+3,g+2,g+1,m+3,m+2,m+1]

for icuts, cuts in enumerate(('none', 'ntracks', 'full')):
    for s in multijet + dijet:
        if hasattr(s, 'ys'):
            s.y, s.ye = s.ys[icuts*2:icuts*2+2]

    per = PerSignal('efficiency with cuts=%s' % cuts, y_range=(0.,1.02))
    per.add(multijet, title='#tilde{N} #rightarrow tbs')
    per.add(dijet, title='X #rightarrow d#bar{d}', color=ROOT.kBlue)
    per.draw(canvas=ps.c, do_tau_paves=False, do_decay_paves=False)

    leg = ROOT.TLegend(0.495,0.149,0.870,0.604)
    leg.SetTextFont(42)
    leg.SetBorderSize(0)
    for curve in per.curves:
        leg.AddEntry(curve.g, curve.title, 'LPE')

    lines = []
    for iy, (y, ye) in enumerate(trackmover_data[icuts]):
        y  /= 100
        ye /= 100
        ye = max(ye, 0.01)
        l = ROOT.TBox(0, y-ye, per.nmasses, y+ye)
        l.SetFillStyle(3002)
        l.SetFillColor(trackmover_colors[iy])
        l.Draw()
        lines.append(l)
        leg.AddEntry(l, trackmover_nice[iy], 'F')

    leg.Draw()

    ps.save(cuts)
