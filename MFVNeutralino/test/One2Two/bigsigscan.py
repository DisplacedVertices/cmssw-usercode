import sys

tau0s = [0.1*x for x in xrange(1,10)] + [1.*x for x in xrange(1,11)] + range(12,31,2)
masses = range(300, 1501, 100)

def make_name(tau0, mass):
    return 'mfv_neutralino_tau%05ium_M%04i' % (int(tau0*1000), mass)

name2num = {}
num2name = {}
name2mass = {}
name2fn = {}

i = -100
for tau0 in tau0s:
    for mass in masses:
        i -= 1
        name = make_name(tau0, mass)
        if name == 'mfv_neutralino_tau12000um_M0900':
            continue
        name2num[name] = i
        num2name[i] = name
        name2mass[name] = mass

        path = 'root://cmsxrootd.fnal.gov//store/user/tucker/mfv_sample_scan/'
        if mass in [300, 500, 700, 900, 1300]:
            path = path.replace('tucker', 'jchu')
        fn = path + name + '.root'
        name2fn[name] = fn

print 'last i =', i

def make_templates(out_fn):
    from base import ROOT, make_h

    f = ROOT.TFile(out_fn, 'recreate')
    hs = []

    for num in reversed(num2name.keys()):
        name = num2name[num]
        fn = name2fn[name]
        print fn

        h = make_h(fn, 'sig%i' % num)
        hs.append(h)
        h.SetDirectory(f)

    f.Write()
    f.Close()

if __name__ == '__main__':
    if 'make' in sys.argv:
        make_templates('bigsigscan.root')
