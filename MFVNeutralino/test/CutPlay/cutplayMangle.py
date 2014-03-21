import sys, os
from JMTucker.Tools.ROOTTools import ROOT
import JMTucker.Tools.Samples as Samples

def depize(s):
    return float(s.replace('p','.').replace('n','-'))

def cutplayMangle(filename):
    debug = False

    file = ROOT.TFile.Open(filename)
    if not file.IsOpen():
        raise RuntimeError('could not open %s' % filename)

    x = file.Get('effs/triggers_pass_num')

    cutscans = {}
    nm1 = None

    # Extract from the big list of bins the numbers separately for each
    # cut.
    for i in xrange(1, x.GetNbinsX()+1):
        label = x.GetXaxis().GetBinLabel(i)

        if label == 'nm1':
            nm1 = x.GetBinContent(i), x.GetBinError(i)
            continue

        try:
            cut, cut_val = label.split('X')
        except ValueError:
            print 'warning: could not parse label %s' % label
            continue

        if not cutscans.has_key(cut):
            cutscans[cut] = []
        cutscans[cut].append((cut_val, x.GetBinContent(i)))

    h_intot = file.Get('effs/triggers_pass_den')
    ntot = h_intot.GetBinContent(1), h_intot.GetBinError(1)

    file.Close()

    output_fn = os.path.basename(filename).replace('.root', '_mangled.root')
    output_file = ROOT.TFile(output_fn, 'RECREATE')

    sample_name = os.path.basename(filename).replace('.root', '')
    sample = getattr(Samples, sample_name)

    h_ntot = ROOT.TH1F('ntot', '', 1, 0, 1)
    h_ntot.SetBinContent(1, ntot[0] / sample.ana_filter_eff)
    h_ntot.SetBinError(1, ntot[1] / sample.ana_filter_eff)

    if nm1 is not None:
        h_nm1 = ROOT.TH1F('nm1', '', 1, 0, 1)
        h_nm1.SetBinContent(1, nm1[0])
        h_nm1.SetBinError(1, nm1[1])
    else:
        raise ValueError('did not find nm1 value in input')

    output_hists = []
    
    for cut_name, scan in cutscans.iteritems():
        if debug:
            print 'cut: %s' % cut_name

        hmin = depize(scan[0][0])
        hminplus1 = depize(scan[1][0])
        binwidth = hminplus1 - hmin
        hmaxminus1 = depize(scan[-1][0])
        hmax = hmaxminus1 + binwidth
        if debug:
            print 'hmin: ', hmin, ' hminplus1: ', hminplus1, ' binwidth: ', binwidth, ' hmaxminus1: ', hmaxminus1, ' hmax: ', hmax

        hist = ROOT.TH1F(cut_name, '', len(scan), hmin, hmax)
        output_hists.append(hist)

        for cut_bin_name, nevents in scan:
            bin = hist.FindBin(depize(cut_bin_name) + 0.00001)
            bin_edge = hist.GetBinLowEdge(bin)
            if debug:
                print 'cut bin name: %s ibin: %i bin_edge: %s  number of events: %f' % (cut_bin_name, bin, bin_edge, nevents)
            hist.SetBinContent(bin, nevents)

    output_file.Write()
    output_file.Close()

filenames = [x for x in sys.argv if x.endswith('.root') and os.path.isfile(x)]
for fn in filenames:
    print fn
    cutplayMangle(fn)
