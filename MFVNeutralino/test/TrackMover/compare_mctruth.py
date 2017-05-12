# for x in $crd/TrackMoverMCTruthV14/*.root ; do echo $(printf "%-50s" $(basename $x .root)) $(./mctruth.exe $x $(basename $x) 0.0252 ); done | tee mctruths.txt

import sys
from JMTucker.Tools.ROOTTools import *
from JMTucker.Tools import Samples
from JMTucker.MFVNeutralino.PerSignal import PerSignal

mctruths_fn = sys.argv[1]
plot_path = sys.argv[2]

set_style()
ps = plot_saver(plot_path, size=(800,500), log=False)

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

multijet = [s for s in Samples.mfv_signal_samples if not s.name.startswith('my_')]
dijet = Samples.mfv_ddbar_samples
for ss in multijet, dijet:
    ss.sort(key=lambda s: s.name)

trackmover_data = [
    [(89.07, 0.01),
     (92.73, 0.02),
     (93.99, 0.05),
     (97.68, 0.00),
     (97.74, 0.01),
     (97.91, 0.04),
     ],
    [(87.14, 0.01),
     (91.34, 0.02),
     (92.71, 0.05),
     (97.17, 0.00),
     (97.29, 0.01),
     (97.51, 0.04),
     ],
    [(71.92, 0.01),
     (85.92, 0.02),
     (89.76, 0.06),
     (94.68, 0.00),
     (96.28, 0.02),
     (96.81, 0.05),
     ]
    ]

for icuts, cuts in enumerate(('none', 'ntracks', 'full')):
    for s in multijet + dijet:
        if hasattr(s, 'ys'):
            s.y, s.ye = s.ys[icuts*2:icuts*2+2]

    per = PerSignal('efficiency with cuts=%s' % cuts, y_range=(0.,1.05))
    per.add(multijet, title='#tilde{N} #rightarrow tbs')
    per.add(dijet, title='X #rightarrow d#bar{d}', color=ROOT.kBlue)
    per.draw(canvas=ps.c)
    for p in per.decay_paves:
        p.SetY1(p.GetY1() - 0.7)
        p.SetY2(p.GetY2() - 0.7)

    lines = []
    for y, ye in trackmover_data[icuts]:
        y  /= 100
        ye /= 100
        ye = max(ye, 0.01)
        l = ROOT.TBox(per.nmasses * 3, y-ye, per.nmasses * 4, y+ye)
        l.SetFillStyle(3002)
        l.SetFillColor(ROOT.kGreen+2)
        l.Draw()
        lines.append(l)

    ps.save(cuts)
