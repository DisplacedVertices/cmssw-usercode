#!/usr/bin/env python

import os
from DVCode.Tools.ROOTTools import *
from DVCode.Tools.Sample import norm_from_file
from DVCode.Tools import Samples
from DVCode.MFVNeutralino.PerSignal import PerSignal

set_style()
ps = plot_saver(plot_dir('rmtracks_v15'), size=(1000,500), log=False)

multijet = [s for s in Samples.mfv_signal_samples if not s.name.startswith('my_')]
dijet = Samples.mfv_ddbar_samples

def getit(fn, ntk):
    f = ROOT.TFile(fn)
    den = norm_from_file(f)
    assert 3 <= ntk <= 5
    t = f.Get('mfvMiniTree%s/t' % ('Ntk%i' % ntk if ntk < 5 else ''))
    if not t:
        return None
    n1v = t.Draw('dist0', 'nvtx==1', 'goff')
    n2v = t.Draw('dist0', 'nvtx>=2', 'goff')
    return den, n1v, n2v

things = [
    ('nominal', ROOT.kRed    , 1, '/uscms_data/d2/tucker/crab_dirs/MiniTreeV15',                     ''),
#   ('nominal', ROOT.kRed,     1, '/uscms_data/d2/tucker/crab_dirs/MiniNtupleV15/!done',             ''),
    ('hip',     ROOT.kGreen+2, 1, '/uscms_data/d2/tucker/crab_dirs/MiniTreeV15',                     '_hip1p0'),
    ('rm28pc',  ROOT.kGreen,   1, '/uscms_data/d2/tucker/crab_dirs/MiniNtupleV15_rm28pcseedtk',      ''),
    ('hipmit',  ROOT.kBlue,    1, '/uscms_data/d2/tucker/crab_dirs/MiniTreeV15',                     '_hip1p0_mit'),
    ('rm6pc',   ROOT.kCyan,    1, '/uscms_data/d2/tucker/crab_dirs/MiniNtupleV15_rm6pcseedtk/!done', ''),
    ]

ratio_den_tag = things[0][0]
for do_ratio in 0,1:
    if do_ratio:
        print '\nratios:'

    for n1or2 in (2,): #(1,2):
        for ntracks in (5,): #(3,4,5):
            for samples_name, samples in (('multijet', multijet), ('dijet', dijet)):
                if do_ratio:
                    per = PerSignal('ratio to nominal', y_range=(0,1.3))
                else:
                    per = PerSignal('efficiency', y_range=(0,1.05))

                for sample in samples:
                    sample.ys = {}

                for ithing, (tag, color, style, path, suffix) in enumerate(things):
                    for sample in samples:
                        fn = os.path.join(path, sample.name + suffix + '.root')
                        print tag, sample.name, fn,
                        if os.path.isfile(fn):
                            den, n1v, n2v = getit(fn, ntracks)
                            num = n2v if n1or2 == 2 else n1v

                            ys = clopper_pearson(num, den)
                            if do_ratio and tag != ratio_den_tag and sample.ys[ratio_den_tag]:
                                y, yl, yh = ys
                                nm, nl, nh = sample.ys[ratio_den_tag]
                                ye = (yh - yl)/2
                                ne = (nh - nl)/2
                                ynew = y / nm
                                yenew = ynew*((ne/nm)**2 + (ye/y)**2)**0.5
                                ylnew, yhnew = ynew-yenew, ynew+yenew
                                ys = ynew, ylnew, yhnew
                            sample.y, sample.yl, sample.yh = sample.ys[tag] = ys
                            print den, num, sample.ys[tag]
                        else:
                            sample.ys[tag] = None
                            sample.y, sample.yl, sample.yh = None, None, None
                            print "doesn't exist"

                    if ithing != 0 or not do_ratio:
                        per.add(samples, title=tag, color=color, style=style)

                per.draw(canvas=ps.c)

                nm = 'n%iv_ntk%i_%s' % (n1or2, ntracks, samples_name)
                if do_ratio:
                    nm += '_ratios'
                ps.save(nm)
