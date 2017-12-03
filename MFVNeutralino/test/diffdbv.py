from JMTucker.MFVNeutralino.MiniTreeBase import *

set_style()
ps = plot_saver(plot_dir('fuh'), size=(350,500), log=False)

binning, binwidth = '(200,0,0.2)', '10 #mum'
npaths = 'v15', 'v16'
paths = '/uscms_data/d2/tucker/crab_dirs/MiniTreeV15_v5', '/uscms_data/d2/tucker/crab_dirs/MiniTreeV16'

hs = {}

for npath, path in zip(npaths, paths):
    for ntk in 3,7,4,5:
        t = ROOT.TChain(t_path(ntk))
        for fn in glob(os.path.join(path, 'JetHT*root')):
            t.Add(fn)

        name = '%sdbvntk%i' % (npath, ntk)
        t.Draw('dist0>>%s%s' % (name, binning))
        h = hs[name] = getattr(ROOT, name)
        move_overflow_into_last_bin(h)
        h.SetStats(0)

a,b = npaths
for ntk in 3,7,4,5:
    s = 'dbvntk%i' % ntk
    h = hs[b+s]
    h.Add(hs[a+s], -1)
    h.Draw('hist')
    h.SetTitle('ntk=%i, %s - %s;d_{BV} (cm);events/%s' % (ntk,b,a,binwidth))
    ps.save(s)
