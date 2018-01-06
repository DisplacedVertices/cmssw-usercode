from JMTucker.Tools.ROOTTools import *
set_style()
ps = plot_saver('plots/o2t_interpcompare', size=(600,600))

class template:
    def __init__(self, line):
        line = line.strip().split()
        self.mu = line.pop(0)
        self.sig = line.pop(0)
        assert len(line) == 6
        self.a = [float(x) for x in line]

def template_map(templates):
    d = {}
    for t in templates:
        d[(t.mu, t.sig)] = t
    return d

def parse(fn):
    lines = open(fn).readlines()
    steps = lines.pop(0).strip().split()
    orig, interp = [], []
    is_interp = False
    for line in lines:
        if line == 'interp:\n':
            is_interp = True
        else:
            line = line.strip()
            if not line:
                continue
            t = template(line)
            if is_interp:
                interp.append(t)
            else:
                orig.append(t)
    print fn, steps
    print '# orig:', len(orig), '# interp', len(interp)
    return template_map(orig), template_map(interp)

nointerp = parse('nointerp.txt')[0]
interp2x_orig, interp2x = parse('interp2x.txt')
interp4x_orig, interp4x = parse('interp4x.txt')

def compare_orig(orig):
    s = 0.
    for p,t in orig.iteritems():
        t_no = nointerp[p]
        s += sum(abs(t.a[i] - t_no.a[i]) for i in xrange(6))
    return s

print '2x orig diff:', compare_orig(interp2x_orig)
print '4x orig diff:', compare_orig(interp4x_orig)


def make_h(name, templates, stat):
    nmu, mu0, mus, nsig, sig0, sigs = 180, 0.000000, 0.000500, 100, 0.000500, 0.000500
    h = ROOT.TH2D(name, ';mu;sig', nmu, mu0, mus*nmu, nsig, sig0, nsig*sigs)
    h.SetStats(0)
    h.GetZaxis().SetLabelSize(0.02)
    for p, t in templates.iteritems():
        mu = float(p[0])
        sig = float(p[1])
        #imu = int((mu - mu0)/mus)
        #isig = int((sig - sig0)/sigs)
        nb = h.FindBin(mu, sig)
        c = stat(t.a)
        h.SetBinContent(nb, c)
    return h

def avg(a):
    return sum(a)/len(a)
def rms(a):
    m = avg(a)
    return (sum((x-m)**2 for x in a)/(len(a)-1))**0.5
def tail(a):
    return a[-1] + a[-2]
def last(a):
    return a[-1]

stats = 'sum min max avg rms tail last'.split()

for thing in 'nointerp interp2x interp4x'.split():
    for stat in stats:
        name = thing + '_' + stat
        h = make_h(name, eval(thing), eval(stat))
        exec '%s = h' % name
        h.Draw('colz')
        ps.save(name, logz=True)

for thing in 'interp2x interp4x'.split():
    for stat in stats:
        name = thing + '_' + stat
        h = eval(name)
        hdiff = h.Clone('diff_' + name)
        hno = eval('nointerp_' + stat)
        hdiff.Add(hno, -1)
        hdiff.Draw('colz')
        ps.save('diff_' + name, logz=True)
