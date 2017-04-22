#!/usr/bin/env python

from JMTucker.MFVNeutralino.MiniTreeBase import *

out_dir = 'combine_new'
force_overwrite = 'force' in sys.argv

for arg in sys.argv:
    if arg.startswith('dir='):
        out_dir = arg.replace('dir=', '')

if os.path.isdir(out_dir) and not force_overwrite:
    raise RuntimeError('move existing out_dir %s out of the way first' % out_dir)
elif not force_overwrite:
    os.mkdir(out_dir)

fns = glob.glob('trees/mfv*root')
fns.sort()

hs = []

out_f = ROOT.TFile(os.path.join(out_dir, 'my-shapes.root'), 'recreate')

data_obs = [6, 193, 45, 5, 1, 1]
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
#data_obs = background[:]

scale = sum(data_obs) / sum(background)
print 'scale is', scale

sums = []

for b in 'data_obs background background_bkgshpUp background_bkgshpDown'.split():
    lb = eval(b)
    sc = 1 if b == 'data_obs' else scale
    lb = [sc*d for d in lb]
    sums.append(sum(lb))
    s = '%s = make_raw_h("%s", %r); %s.SetDirectory(out_f)' % (b, b, lb, b)
    exec s

nobs = data_obs.Integral()
nbkg = background.Integral()
sums.append(nobs)
#assert len(set([int(10*s) for s in sums])) == 1

print 'data', data_obs
print 'bckg', background
print 'bkup', background_bkgshpUp
print 'bkdn', background_bkgshpDown

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
    h = make_h(fn, signame)
    h.SetDirectory(out_f)

    nsig_gen = 100000
    h.Scale(ac.int_lumi / 1000 * ac.scale_factor / nsig_gen)
    nsig = h.Integral(0, 1000)

    assert h.GetBinContent(nbins+1) < 1e-6
    x = [signame, nsig] + [h.GetBinContent(i) for i in xrange(1, nbins+1)]
    sig_templates.append(x)
    
    open(os.path.join(out_dir, signame + '.txt'), 'wt').write(card_template % locals())

out_f.Write()
out_f.Close()

title = '%32s %6s | %6s %6s %6s %6s %6s %6s | %6s | %9s | %6s %6s | %6s | %6s %6s %6s' % ('signal', 'nsig', 'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c456', 'c123/c456', 'c1/c2', 'c3/c2', 'sc', 'sc*c1', 'sc*c2', 'sc*c3')
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
    print '%32s %6.2f | %6.2f %6.2f %6.2f %6.2f %6.2f %6.2f | %6.2f | %9.2f | %6.2f %6.2f | %6.2f | %6.2f %6.2f %6.2f' % (signame, nsig, x[1], x[2], x[3], x[4], x[5], x[6], c456, c123/c456, x[1]/x[2], x[3]/x[2], scale, x[1]*scale, x[2]*scale, x[3]*scale)
