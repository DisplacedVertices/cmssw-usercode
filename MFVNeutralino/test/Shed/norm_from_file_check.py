import sys, glob, os
from JMTucker.Tools.Sample import norm_from_file
from JMTucker.Tools import Samples, colors

path = sys.argv[1]
dataset = sys.argv[2]
target = float(sys.argv[3]) if len(sys.argv) > 3 else 0.5

for fn in glob.glob(os.path.join(path, '*.root')):
    sname = os.path.basename(fn).replace('.root', '')
    s = getattr(Samples, sname)
    s.set_curr_dataset(dataset)
    n = norm_from_file(fn)
    frac = n/s.nevents_orig
    delta = abs(frac - target)/target
    if delta > 0.01:
        color = colors.red
    elif delta > 1e-3:
        color = colors.yellow
    else:
        color = colors.green
    print color('%-50s %15i %15i %e' % (fn, s.nevents_orig, n, frac))
