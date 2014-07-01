#!/usr/bin/env python

########################

fn_pattern = 'crab/MiniTreeV18/mfv*root'
out_fn = 'signal_templates.root'
binning = '(20000,0,10)'
plot_dir = 'plots/o2t_signal_templates'
ntrackses = (5,6,7,8)

########################

from base import *
ps = plot_saver(plot_dir, size=(600,600))

ROOT.TH1.AddDirectory(1)
fout = ROOT.TFile(out_fn, 'recreate')

fns = glob.glob(fn_pattern)
fns.sort()

for fn in fns:
    print fn
    sig_name = os.path.basename(fn).replace('.root','')
    f, t = get_f_t(fn, None)
    
    for min_ntracks in ntrackses:
        name = 'h_sig_ntk%i_%s' % (min_ntracks, sig_name)
        t.Draw('svdist>>%s%s' % (name, binning), 'nvtx >= 2 && ntk0 >= %i && ntk1 >= %i' % (min_ntracks, min_ntracks))
        h = getattr(ROOT, name)
        h.SetDirectory(fout)
        h.GetXaxis().SetRangeUser(0, 1)
        ps.save(name)

fout.Write()
fout.Close()
