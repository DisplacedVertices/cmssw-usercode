#!/usr/bin/env python

from base import *

fn_pattern = 'trees/mfv*root'
binning = array('d', [0.02*i for i in xrange(5)] + [0.1, .15]) # JMTBAD keep in sync with Templates.cc
nbins = len(binning) - 1

min_ntracks = 5

fns = glob.glob(fn_pattern)
fns.sort()

hs = []

masses = range(200, 1001, 200)
masses.insert(1, 300)

out_f = ROOT.TFile('combine/my-shapes.root', 'recreate')

def make_h(name, contents):
    assert contents is None or len(contents) == nbins
    h = ROOT.TH1F(name, '', nbins, binning)
    hs.append(h)
    if contents is not None:
        for i,c in enumerate(contents):
            h.SetBinContent(i+1, c)
    h.SetDirectory(out_f)
    return h

data_obs = make_h('data_obs', [6, 193, 45, 5, 1, 1])

background            = make_h('background',            [6.3,       192.4,       48.2,       3.5,       .34,      .26     ])
background_bkgshpUp   = make_h('background_bkgshpUp',   [6.3 - 1.1, 192.4 - 4.3, 48.2 + 3.8, 3.5 + 1.4, .34 + .1, .26 + .1])
background_bkgshpDown = make_h('background_bkgshpDown', [6.3 + 1.1, 192.4 + 4.3, 48.2 - 3.8, 3.5 - 1.4, .34 - .1, .26 - .1])

card_template = '''
imax 1
jmax 1
kmax *
---------------
shapes * * my-shapes.root $PROCESS $PROCESS_$SYSTEMATIC
---------------
bin 1
observation 251
---------------------------------------
bin             1            1
process         %(signame)s  background
process         0            1
rate            %(nsig)f     251
---------------------------------------
sigsyst lnN     1.20         -
bkgshp  shape   -            1
'''

sig_templates = []

for fn in fns:
    print fn
    signame = os.path.basename(fn).replace('.root','')
    f, t = get_f_t(fn, None)

    h = make_h(signame, None)
    x = detree(t, 'svdist', 'nvtx >= 2 && ntk0 >= %i && ntk1 >= %i' % (min_ntracks, min_ntracks), lambda x: (float(x[0]),))
    for (d,) in x:
        if d > binning[-1]:
            d = binning[-1] - 1e-4
        h.Fill(d)

    nsig_gen = 100000
    h.Scale(ac.int_lumi / 1000 * ac.scale_factor / nsig_gen)
    nsig = h.Integral(0, 1000)

    assert h.GetBinContent(nbins+1) < 1e-6
    x = [signame, nsig] + [h.GetBinContent(i) for i in xrange(1, nbins+1)]
    sig_templates.append(x)
    
    open(os.path.join('combine', signame + '.txt'), 'wt').write(card_template % locals())

out_f.Write()
out_f.Close()

title = '%30s %7s | %7s %7s %7s %7s | %7s %7s | %7s | %7s %7s %7s' % ('signal', 'nsig', 'c1', 'c2', 'c3', 'c456', 'c1/c2', 'c3/c2', 'sc', 'sc*c1', 'sc*c2', 'sc*c3')
line = len(title)*'-'
print
print title
for i,x in enumerate(sig_templates):
    if i % 6 == 0:
        print line
    signame = x.pop(0)
    nsig = x[0]
    c456 = x[4] + x[5] + x[6]
    scale = 3/c456
    print '%30s %7.2f | %7.2f %7.2f %7.2f %7.2f | %7.2f %7.2f | %7.2f | %7.2f %7.2f %7.2f' % (signame, nsig, x[1], x[2], x[3], c456, x[1]/x[2], x[3]/x[2], scale, x[1]*scale, x[2]*scale, x[3]*scale)
