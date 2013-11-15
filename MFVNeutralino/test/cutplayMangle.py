import sys, os
from JMTucker.Tools.ROOTTools import ROOT

def depize(s):
  print repr(s)
  return float(s.replace('p','.').replace('n','-'))

def cutplayMangle(filename):
  debug = True

  file = ROOT.TFile.Open(filename)
  if not file.IsOpen():
    raise RuntimeError('could not open %s' % filename)
    
  x = file.Get('effs/triggers_pass_num')

#  typedef std::vector<std::pair<std::string, float> > cutscan_t;
#  std::map<std::string, cutscan_t> cutscans;


  cutscans = {}

  # Extract from the big list of bins the numbers separately for each
  # cut.
  for i in xrange(1, x.GetNbinsX()+1):
    label = x.GetXaxis().GetBinLabel(i)
    cut, cut_val = label.split('X')

    if not cutscans.has_key(cut):
      cutscans[cut] = []
    cutscans[cut].append((cut_val, x.GetBinContent(i)))

  file.Close()

  output_fn = os.path.basename(filename).replace('.root', '_mangled.root')
  output_file = ROOT.TFile(output_fn, 'RECREATE')
  
  output_hists = []

  for cut_name, scan in cutscans.iteritems():
    if debug:
      print 'cut: %s' % cut_name

    hmin = depize(scan[0][0])
    hminplus1 = depize(scan[1][0])
    binwidth = hminplus1 - hmin
    hmaxminus1 = depize(scan[-1][0])
    hmax = hmaxminus1 + binwidth
    print 'hmin: ', hmin, ' hminplus1: ', hminplus1, ' binwidth: ', binwidth, ' hmaxminus1: ', hmaxminus1, ' hmax: ', hmax

    hist = ROOT.TH1F(cut_name, '', len(scan), hmin, hmax)
    output_hists.append(hist)

    for cut_bin_name, nevents in scan:
      bin = hist.FindBin(depize(cut_bin_name) + 0.00001)
      bin_edge = hist.GetBinLowEdge(bin)
      if debug:
        print 'cut bin name: %s  ibin: %i  bin_edge: %s   number of events: %f' % (cut_bin_name, bin, bin_edge, nevents)
      hist.SetBinContent(bin, nevents)

  output_file.Write()
  output_file.Close()

filenames = [x for x in sys.argv if x.endswith('.root') and os.path.isfile(x)]
for fn in filenames:
  print fn
  cutplayMangle(fn)
