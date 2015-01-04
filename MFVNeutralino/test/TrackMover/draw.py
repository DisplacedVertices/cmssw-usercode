from JMTucker.Tools.ROOTTools import *
set_style()

njets = 2
nbjets = 1
ex = '%i%i' % (njets, nbjets)

ps = plot_saver('plots/trackmover' + ex)

def get_em(fn, alpha=1-0.6827):
    f = ROOT.TFile(fn)
    d = {}

    l = []
    ltmp = []

    for key in f.GetListOfKeys():
        name = key.GetName()
        obj = f.Get(name)
        if name.startswith('h_'):
            l.append(name)
        else:
            ltmp.append(name)
        obj = f.Get(name)
        d[name] = obj

    ltmp.sort()

    for name in ltmp:
        if name.endswith('_num'):
            num = d[name]
            den = d[name.replace('_num', '_den')]
            g = histogram_divide(num, den, confint_params=(alpha,))
            g.SetTitle(num.GetTitle())
            rat_name = name.replace('_num', '_rat')
            d[rat_name] = g

            l.append(rat_name)

    return f, l, d

f_data, l_data, d_data = get_em('ddddata.root')
f_mc,   l_mc,   d_mc   = get_em('mc.root', 0.001)
assert l_data == l_mc
assert len(d_data) == len(d_mc)
l = l_data

for name in l:
    data = d_data[name]
    mc   = d_mc  [name]
    both = (data, mc)

    if name.endswith('_rat'):
        data.SetLineWidth(2)
        data.SetMarkerStyle(20)
        data.SetMarkerSize(0.8)
        data.Draw('ALP')

        mc.SetFillStyle(3001)
        mc.SetFillColor(2)
        mc.Draw('E2 same')

        for g in both:
            g.GetYaxis().SetRangeUser(0., 1.05)

        ps.save(name)

    elif not name.endswith('_num') and not name.endswith('_den'):
        data.Draw()
        mc.SetLineColor(ROOT.kRed)
        mc.Draw('sames')

        ps.c.Update()
        for i,h in enumerate((data, mc)):
            h.SetLineWidth(2)
            differentiate_stat_box(h, i, new_size=(0.2,0.2))

        ps.save(name)
