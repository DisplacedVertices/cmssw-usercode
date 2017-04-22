from JMTucker.MFVNeutralino.MiniTreeBase import *
ROOT.gStyle.SetOptStat(2211)

int_lumi = 39501.
min_ntracks, tree_path = 3, '/uscms_data/d2/tucker/crab_dirs/MinitreeV10_ntk3'
min_ntracks, tree_path = 4, '/uscms_data/d2/tucker/crab_dirs/MinitreeV10_ntk4'
min_ntracks, tree_path = 5, '/uscms_data/d2/tucker/crab_dirs/MinitreeV10'

ps = plot_saver(plot_dir('pileupdbvdvv_run2_ntk%i' % min_ntracks), size=(600,600),pdf=True)

f,t = get_f_t(bkg_samples[0], min_ntracks, tree_path)
t.Draw('npu>>h_npu_1v(38,0,38)', 'nvtx==1')
ps.save('npu_1v')
t.Draw('npu>>h_npu_2v(38,0,38)', 'nvtx>=2')
ps.save('npu_2v')

if 0: # run this to figure out the npu_bins
    #h, per = ROOT.h_npu_1v, 2000
    h, per = ROOT.h_npu_2v, 40
    bins = [0]
    for ibin in xrange(1,38):
        i = h.Integral(bins[-1], ibin)
        if i > per:
            bins.append(ibin)
    print bins
    bins.append(1000)
    for a,b in zip(bins, bins[1:]):
        print a,b,h.Integral(a,b)
    raise 1

npu_bins = [(0,9),(10,12),(13,15),(16,50)]
nbins = len(npu_bins)

for q in ['dbv', 'dvv']:
    if q == 'dbv':
        hs = [ROOT.TH1F('h_dbv_%i_%i' % ab, ';d_{BV} (cm);events/0.01 cm', 100, 0, 1) for ab in npu_bins]
    else:
        if min_ntracks == 5:
            continue
        hs = [ROOT.TH1F('h_dvv_%i_%i' % ab, ';d_{VV} (cm);events/0.01 cm', 30, 0, 0.3) for ab in npu_bins]

    for sample in bkg_samples:
        if min_ntracks == 5 and sample.name in ['qcdht0500sum']:
            continue

        f,t = get_f_t(sample, min_ntracks, tree_path)
        weight = sample.partial_weight_orig * int_lumi
        for i,(a,b) in enumerate(npu_bins):
            hn = 'h_%s_%i_%i_%s' % (q,a,b,sample.name)
            if q == 'dbv':
                print sample.name, t.Draw('dist0>>%s(100,0,1)'%hn, '(nvtx == 1 && npu >= %i && npu <= %i) * weight * %e' % (a,b,weight))
            else:
                print sample.name, t.Draw('svdist>>%s(30,0,0.3)'%hn, '(nvtx >= 2 && npu >= %i && npu <= %i) * weight * %e' % (a,b,weight))
            htemp = getattr(ROOT, hn)
            hs[i].Add(htemp)

    colors = [2,ROOT.kGreen+2,4,6]
    things = means, rmses = [], []
    for scale in (0,1):
        for i,h in enumerate(hs):
            if scale == 0:
                means.append((h.GetMean(), h.GetMeanError()))
                rmses.append((h.GetRMS(), h.GetRMSError()))
            move_overflow_into_last_bin(h)
            h.SetLineWidth(2)
            h.SetLineColor(colors[i])
            d = h.DrawNormalized if scale else h.Draw
            d() if i == 0 else d('sames')
            ps.c.Update()
            differentiate_stat_box(h, (nbins-1-i,0), new_size=(0.2,0.2))
        ps.save(q + '_v_npu' + ('_scale' if scale else ''))

    for thing, name in zip(things, ('mean', 'rms')):
        h = ROOT.TH1F('hs_%s' % thing, '%s, %s' % (q, name), nbins, 0, nbins)
        h.SetStats(0)
        for i,(y,ey) in enumerate(thing):
            h.SetBinContent(i+1, y)
            h.SetBinError(i+1, ey)
        for i,ab in enumerate(npu_bins):
            h.GetXaxis().SetBinLabel(i+1, '%i-%i' % ab)
        h.Draw()
        h.GetYaxis().SetRangeUser(0, 0.05 if q == 'dbv' else 0.1)
        ps.save(q + '_' + name, log=False)
