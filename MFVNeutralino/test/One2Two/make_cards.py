#!/usr/bin/env python

from base import *

out_dir = 'combine_new'
force_overwrite = 'force' in sys.argv
binning = array('d', [0.02*i for i in xrange(5)] + [0.1, .15]) # JMTBAD keep in sync with Templates.cc
nbins = len(binning) - 1

if os.path.isdir(out_dir) and not force_overwrite:
    raise RuntimeError('move existing out_dir %s out of the way first' % out_dir)
elif not force_overwrite:
    os.mkdir(out_dir)

min_ntracks = 5

fns = glob.glob('trees/mfv*root')
fns.sort()
#fns = [
#    'trees/mfv_neutralino_tau0300um_M0300.root'
#    'root://cmsxrootd.fnal.gov//store/user/jchu/mfv_sample_scan/mfv_neutralino_tau01000um_M0300.root',
#    'root://cmsxrootd.fnal.gov//store/user/tucker/mfv_sample_scan/mfv_neutralino_tau01000um_M0400.root',
#    'root://cmsxrootd.fnal.gov//store/user/jchu/mfv_sample_scan/mfv_neutralino_tau01000um_M0500.root',
#    'root://cmsxrootd.fnal.gov//store/user/tucker/mfv_sample_scan/mfv_neutralino_tau01000um_M0600.root',
#    'root://cmsxrootd.fnal.gov//store/user/jchu/mfv_sample_scan/mfv_neutralino_tau01000um_M0700.root',
#    'root://cmsxrootd.fnal.gov//store/user/jchu/mfv_sample_scan/mfv_neutralino_tau01000um_M0900.root',
#    'root://cmsxrootd.fnal.gov//store/user/tucker/mfv_sample_scan/mfv_neutralino_tau01000um_M1000.root',
#    'M1200temp.root',
#    'root://cmsxrootd.fnal.gov//store/user/tucker/mfv_sample_scan/mfv_neutralino_tau01000um_M1500.root'
#    ]

hs = []

out_f = ROOT.TFile(os.path.join(out_dir, 'my-shapes.root'), 'recreate')

def make_h(name, contents):
    assert contents is None or len(contents) == nbins
    h = ROOT.TH1F(name, '', nbins, binning)
    hs.append(h)
    if contents is not None:
        for i,c in enumerate(contents):
            h.SetBinContent(i+1, c)
    h.SetDirectory(out_f)
    return h

data_obs = [6, 193, 45, 5, 1, 1]
#data_obs = [a+5*b for a,b in zip(data_obs, [0.098629340529441833, 0.23323343694210052, 0.35974752902984619, 0.41603338718414307, 0.4215414822101593, 2.748539924621582])]

background = [6.2, 192.2, 48., 3.5, .34, .26]
s = systematics = [0, 0, 3.8, 1.4, .1, .1]
pivot = 2
#s[0] = 1.1; s[1] = 4.3 # divide between first two bins by some ratio
#s[1] = 5.4 # put it all in the second bin
s[0] = 0.17; s[1] = 5.23 # divide between first two bins keeping shape fixed
#s[0] = 0.14; s[1] = 4.21; s[2] = 1.05; pivot = 3 # divide between first three bins ditto

background_bkgshpUp, background_bkgshpDown = [], []
for i in xrange(nbins):
    sign = -1 if i < pivot else 1
    up = background[i] + sign * systematics[i]
    dn = background[i] - sign * systematics[i]
    background_bkgshpUp.append(up)
    background_bkgshpDown.append(dn)
print background
print background_bkgshpUp
print background_bkgshpDown
#data_obs = background[:]

scale = sum(data_obs) / sum(background)
print 'scale is', scale

sums = []

for b in 'data_obs background background_bkgshpUp background_bkgshpDown'.split():
    lb = eval(b)
    sc = 1 if b == 'data_obs' else scale
    lb = [sc*d for d in lb]
    sums.append(sum(lb))
    s = '%s = make_h("%s", %r)' % (b, b, lb)
    exec s

nobs = data_obs.Integral()
nbkg = background.Integral()
sums.append(nobs)
#assert len(set([int(10*s) for s in sums])) == 1


card_template = '''
imax 1
jmax 1
kmax *
---------------
shapes * * my-shapes.root $PROCESS $PROCESS_$SYSTEMATIC
---------------
bin 1
observation %(nobs)f
---------------------------------------
bin             1            1
process         %(signame)s  background
process         0            1
rate            %(nsig)f     %(nbkg)f
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

    nsig_gen = 471*200 if 'M1200' in fn else 100000
    h.Scale(ac.int_lumi / 1000 * ac.scale_factor / nsig_gen)
    nsig = h.Integral(0, 1000)

    assert h.GetBinContent(nbins+1) < 1e-6
    x = [signame, nsig] + [h.GetBinContent(i) for i in xrange(1, nbins+1)]
    sig_templates.append(x)
    
    open(os.path.join(out_dir, signame + '.txt'), 'wt').write(card_template % locals())

out_f.Write()
out_f.Close()

title = '%32s %6s | %6s %6s %6s %6s | %9s | %6s %6s | %6s | %6s %6s %6s' % ('signal', 'nsig', 'c1', 'c2', 'c3', 'c456', 'c123/c456', 'c1/c2', 'c3/c2', 'sc', 'sc*c1', 'sc*c2', 'sc*c3')
line = len(title)*'-'
print
print title
for i,x in enumerate(sig_templates):
    if i % 6 == 0:
        print line
    signame = x.pop(0)
    nsig = x[0]
    c123 = x[1] + x[2] + x[3]
    c456 = x[4] + x[5] + x[6]
    scale = 3/c456
    print '%32s %6.2f | %6.2f %6.2f %6.2f %6.2f | %9.2f | %6.2f %6.2f | %6.2f | %6.2f %6.2f %6.2f' % (signame, nsig, x[1], x[2], x[3], c456, c123/c456, x[1]/x[2], x[3]/x[2], scale, x[1]*scale, x[2]*scale, x[3]*scale)
