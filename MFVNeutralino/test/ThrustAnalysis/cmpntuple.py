import sys
from itertools import izip
from JMTucker.Tools.ROOTTools import ROOT, detree

def lify(s):
    return [x.strip() for x in s.split('\n') if x.strip()]

tv3s = lify('''
vtxGHad
vtxBgHad
vtxSHad
vtxTHad
vtxBtHad
vtxQ0
vtxQ1
vtxGLep
vtxBgLep
vtxSLep
vtxTLep
vtxBtLep
vtxLep
vtxNu
vthr3
vthr2
vthr3j
vthr2j
vthr3jAll
vthr2jAll
beamspot
''')

tlvs = lify('''
p4GHad
p4BgHad
p4SHad
p4THad
p4BtHad
p4Q0
p4Q1
p4GLep
p4BgLep
p4SLep
p4TLep
p4BtLep
p4Lep
p4Nu
p4jBgHad
p4jSHad
p4jBtHad
p4jQ0
p4jQ1
p4jBgLep
p4jSLep
p4jBtLep
p4MET
''')

dbls = lify('''
thr3
thr2
thr3j
thr2j
thr3jAll
thr2jAll
''')

vtlvs = lify('''
vp4jQOther
vp4jBOther
vvtxQOther
vvtxBOther
''')

branches = dbls[:]

for x in tv3s:
    branches.append('%s.X()' % x)
    branches.append('%s.Y()' % x)
    branches.append('%s.Z()' % x)

for x in tlvs:
    branches.append('%s.X()' % x)
    branches.append('%s.Y()' % x)
    branches.append('%s.Z()' % x)
    branches.append('%s.T()' % x)

for x in vtlvs:
    branches.append('%s@.size()' % x)
    branches.append('%s.X()' % x)
    branches.append('%s.Y()' % x)
    branches.append('%s.Z()' % x)
    if 'vtx' not in x:
        branches.append('%s.T()' % x)

branches = ':'.join(branches)

#print branches
#raise 1

def foo(fn):
    f = ROOT.TFile(fn)
    t = f.Get([x.GetName() for x in f.GetListOfKeys()][0]).Get('tree')
    print fn, f, t
    return f,t,t.GetEntries(), detree(t, branches, cut='', xform=lambda x: tuple(float(y.strip() if y.strip() else 0) for y in x))

f1,t1,n1,nt1 = foo(sys.argv[1])
f2,t2,n2,nt2 = foo(sys.argv[2])

assert n1 == n2
print n1, 'entries'

nt1 = sorted(nt1)
nt2 = sorted(nt2)

for r1,r2 in izip(nt1,nt2):
    assert len(r1) == len(r2)
    for v1,v2 in izip(r1, r2):
        #print v1,v2
        assert abs(v1-v2) < 1e-8

print 'all OK!'
