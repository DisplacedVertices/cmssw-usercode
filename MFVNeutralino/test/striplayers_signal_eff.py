import sys, os
from pprint import pprint
from collections import defaultdict
from JMTucker.Tools.Sample import norm_from_file
from JMTucker.Tools.ROOTTools import *
set_style()
ps = plot_saver(plot_dir('stleff'), size=(900,400))

nvtx = 1 if 'one' in sys.argv else 2
ntk = ''
if 'ntk3' in sys.argv:
    ntk = 'Ntk3'
elif 'ntk4' in sys.argv:
    ntk = 'Ntk4'
elif 'ntk3or4' in sys.argv:
    ntk = 'Ntk3or4'

fns = [x for x in sys.argv[1:] if x.endswith('.root')]
fs = { fn : ROOT.TFile(fn) for fn in fns }
samples = defaultdict(list)
for fn in fns:
    s = os.path.basename(fn).replace('.root', '').replace('stl6_', '').replace('stl8_', '')
    if s == 'mfv_neu_tau00300um_M0800':
        continue
        #s = 'my_' + s
    s = s.replace('official_', '')
    samples[s].append(fn)
samples = samples.items()
samples.sort()
nsamples = len(samples)

heff = {}
seen = {}
for x in 'nom', 'stl6', 'stl8':
    for y in 'all', 'mid', 'far':
        name = '%s_%s' % (x,y)
        heff[name] = h = ROOT.TH1F(name, '', nsamples, 0, nsamples)
        h.Sumw2()
        h.SetLineWidth(2)
        h.SetStats(0)
        for i in xrange(nsamples):
            sam = samples[i][0].replace('mfv_', '').replace('tau', 't')
            h.GetXaxis().SetBinLabel(i+1, sam)

colors = { 'nom': ROOT.kRed, 'stl6': ROOT.kBlue, 'stl8': ROOT.kGreen+2 }

for isample, (s, s_fns) in enumerate(samples):
    print s, s_fns
    hs = {}
    for ifn, fn in enumerate(s_fns):
        cn = os.path.basename(fn).replace('.root', '')
        z = cn.replace(s, '').replace('official_', '').replace('_', '')
        if not z:
            z = 'nom'

        n = fs[fn].Get('mcStat/h_sums').GetBinContent(1)
        t = fs[fn].Get('mfvMiniTree%s/t' % ntk)

        if nvtx == 2:
            hs[z] = h = ROOT.TH1F('h_' + cn, ';d_{VV} (cm);events/0.1 cm', 40, 0, 4)
        elif nvtx == 1:
            hs[z] = h = ROOT.TH1F('h_' + cn, ';d_{BV} (cm);events/0.01 cm', 200, 0, 2)
        h.Sumw2()
        h.SetLineWidth(2)
        h.SetStats(0)
        h.SetLineColor(colors[z])

        if nvtx == 2:
            a = t.Draw('svdist>>%s' % h.GetName(), 'nvtx >= 2')
            b = get_integral(h, 0.04)[0]
            c = get_integral(h, 0.07)[0]
            ranges = ('all', a), ('mid', b), ('far', c)
        elif nvtx == 1:
            a = t.Draw('dist0>>%s' % h.GetName(), 'nvtx >= 1')
            b = get_integral(h, 0.02)[0]
            c = get_integral(h, 0.035)[0]
        
        ranges = ('all', a), ('mid', b), ('far', c)
        print z.ljust(6), '%6i/%6i -> %7.4f  >%s um: %6i -> %7.4f  >%s um: %6i -> %7.4f' % (int(a), n, a/n, ranges[1][0], int(b), b/n, ranges[2][0], int(c), c/n)

        for which, j in ranges:
            e, ea, _ = wilson_score(a, n)
            ee = e - ea
            seen[(isample,z)] = True
            heff['%s_%s' % (z, which)].SetBinContent(isample+1, e)
            heff['%s_%s' % (z, which)].SetBinError  (isample+1, ee)

    otherh = []
    for name in 'nom', 'stl6', 'stl8':
        if not hs.has_key(name):
            continue
        h = hs[name].Clone(s + name + 'norm')
        otherh.append(h)
        n = h.Integral()
        if n > 0:
            h.Scale(1./n)
        if len(otherh) == 1:
            h.Draw('hist')
        else:
            h.Draw('hist same')
    ps.save(s, log=False)

    otherh = []
    for name in 'stl6', 'stl8':
        if not hs.has_key(name) or not hs.has_key('nom'):
            continue
        h_alt = hs[name].Clone(s + name + 'num')
        otherh.append(h_alt)
        h_alt.GetYaxis().SetTitle('ratio to nominal')
        h_alt.Divide(hs['nom'])
        if len(otherh) == 1:
            h_alt.Draw('e')
        else:
            h_alt.Draw('e same')
    ps.save(s + '_rat', log=False)

for y in 'all', 'mid', 'far':
    h_nom = heff['nom_%s' % y]
    #h_nom.Draw()
    #ps.save('nom_%s' % y)
    for x in 'stl6', 'stl8':
        name = '%s_%s' % (x,y)
        h_alt = heff[name]
        h_alt.Draw()
        ps.save(name)

        h_diff = h_nom.Clone('h_diff_' + name)
        h_diff.GetYaxis().SetTitle('difference in absolute efficiency')
        for ibin in xrange(1, nsamples+1):
            if not seen.has_key((ibin-1,'nom')) or not seen.has_key((ibin-1,x)):
                h_diff.SetBinContent(ibin, 0)
                h_diff.SetBinError  (ibin, 0)
            else:
                n,ne = h_nom.GetBinContent(ibin), h_nom.GetBinError(ibin) 
                a,ae = h_alt.GetBinContent(ibin), h_alt.GetBinError(ibin) 
                h_diff.SetBinContent(ibin, n-a)
                h_diff.SetBinError(ibin, (ne**2 + ae**2)**0.5)
        heff['diff_%s_%s' % (x,y)] = h_diff
        h_diff.Draw()
        ps.save('diff_' + name, log=False)

heff['nom_all' ].SetLineColor(ROOT.kRed)
heff['stl6_all'].SetLineColor(ROOT.kBlue)
heff['stl8_all'].SetLineColor(ROOT.kGreen+2)
heff['nom_all' ].Draw()
heff['stl6_all'].Draw('same')
heff['stl8_all'].Draw('same')
ps.save('all')

heff['diff_stl6_all'].SetLineColor(ROOT.kBlue)
heff['diff_stl8_all'].SetLineColor(ROOT.kGreen+2)
heff['diff_stl8_all'].Draw()
heff['diff_stl6_all'].Draw('same')
ps.save('diff')
