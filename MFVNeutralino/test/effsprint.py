import sys, os
from JMTucker.Tools.ROOTTools import *
import JMTucker.Tools.Samples as Samples
import JMTucker.MFVNeutralino.AnalysisConstants as ac

plots = 'plots' in sys.argv
if plots:
    set_style()
    ROOT.gStyle.SetPaintTextFormat('.2g')
    ps = plot_saver('plots/nm1s', size=(500,500), log=False)

sum = 0.
var = 0.
cuts = () if 'nonm1' in sys.argv else ('Ntracks', 'Drmin', 'Drmax', 'Mindrmax', 'Bs2derr', 'Njets', 'Ntracksptgt3', 'Sumnhitsbehind', 'ButNtracksAndGt3')
max_cut_name_len = max(len(x) for x in cuts) if cuts else -1
integral = 'entries' not in sys.argv
nvtx = 1 if 'one' in sys.argv else 2
only = 'Only' if 'only' in sys.argv else ''
if not integral:
    print 'using GetEntries(), but "pass vtx only" and all nm1s still use Integral()'

def effs(fn):
    global sum, var
    f = ROOT.TFile(fn)
    def get_n(dir_name):
        h = f.Get('%s/h_npv' % dir_name)
        return h.Integral(0,1000000) if integral else h.GetEntries()

    namenumall = 'mfvEventHistos%s' % ('OneVtx' if nvtx == 1 else '')
    namenumvtx = 'mfvVertexHistos%s/h_nsv' % ('OneVtx' if nvtx == 1 else '')
    if nvtx == 1 and only:
        namenumall = namenumall.replace('One', 'OnlyOne')
        namenumvtx = namenumvtx.replace('One', 'OnlyOne')

    den = get_n('mfvEventHistosNoCuts')
    numall = get_n(namenumall)
    h = f.Get(namenumvtx)
    numvtx = h.Integral(h.FindBin(nvtx), 1000000)
    sname = os.path.basename(fn).replace('.root','')
    try:
        s = getattr(Samples, sname)
        ana_filter_eff = s.ana_filter_eff
        weight = s.xsec*ac.int_lumi/(den/ana_filter_eff)
        weighted = True
    except AttributeError:
        weight = 1.
        weighted = False
        ana_filter_eff = -1
    sum += numall * weight
    var += numall * weight**2
    print '%s (w = %.3e): # ev: %10.1f (%10i)  pass evt+vtx: %5.1f -> %5.3e  pass vtx only: %5.1f -> %5.3e' % (sname.ljust(30), weight, den, den/ana_filter_eff, numall, float(numall)/den, numvtx, float(numvtx)/den)
    if weighted:
        print '  weighted to %.1f/fb: %5.2f +/- %5.2f' % (ac.int_lumi, numall*weight, numall**0.5 * weight)
    else:
        print '  number of events: %5.2f +/- %5.2f' % (numall*weight, numall**0.5 * weight)
    if cuts:
        nm1s_name = 'h_nm1_%s' % sname
        h_nm1_abs = ROOT.TH1F(nm1s_name + '_abs', ';cut;abs. eff. w/o cut', len(cuts)+1, 0, len(cuts)+1)
        h_nm1_rel = ROOT.TH1F(nm1s_name + '_rel', ';cut;n-1 eff.', len(cuts), 0, len(cuts))
        for icut, cut in enumerate(cuts):
            h_nm1_abs.GetXaxis().SetBinLabel(icut+1, cut)
            h_nm1_rel.GetXaxis().SetBinLabel(icut+1, cut)
            nm1 = get_n('evtHst%s%sVNo%s' % (only, nvtx, cut))
            nm1_abs = float(nm1)/den
            nm1_rel = float(numall)/nm1 if nm1 > 0 else -1
            h_nm1_abs.SetBinContent(icut+1, nm1_abs)
            h_nm1_rel.SetBinContent(icut+1, nm1_rel)
            print '    remove %s cut: %5i -> %5.3e (n-1: %5.3e)' % (cut.ljust(max_cut_name_len), nm1, nm1_abs, nm1_rel)
        h_nm1_abs.GetXaxis().SetBinLabel(len(cuts)+1, 'all')
        h_nm1_abs.SetBinContent(len(cuts)+1, float(numall)/den)
        def draw(h):
            if not plots:
                return
            h.SetStats(0)
            h.GetYaxis().SetRangeUser(0,1.05)
            h.SetMarkerSize(2)
            h.Draw('hist text')
            ps.save(h.GetName())
        draw(h_nm1_abs)
        draw(h_nm1_rel)

nosort = 'nosort' in sys.argv
fns = [x for x in sys.argv[1:] if os.path.isfile(x) and x.endswith('.root')]
if not fns:
    dir = [x for x in sys.argv[1:] if os.path.isdir(x)][0]
    fns = [os.path.join(dir, fn) for fn in 'qcdht0100.root qcdht0250.root qcdht0500.root qcdht1000.root ttbarhadronic.root ttbarsemilep.root ttbardilep.root'.split()]
    nosort = True
if not nosort:
    fns.sort()
for fn in fns:
    effs(fn)
print 'sum for %.1f/fb: %5.2f +/- %5.2f' % (ac.int_lumi, sum, var**0.5)
