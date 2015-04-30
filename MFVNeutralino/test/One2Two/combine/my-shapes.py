from array import array
import sys
sys.argv.append('-b')
from ROOT import *

f = TFile('my-shapes.root', 'recreate')

binning = array('d', [0, .2, .4, .6, .8, 1, 2])
nbins = len(binning)-1

def h(name, contents):
    assert len(contents) == nbins
    h = TH1F(name, '', nbins, binning)
    for i,c in enumerate(contents):
        h.SetBinContent(i+1, c)
    h.SetDirectory(f)
    return h

data_obs = h('data_obs', [6, 193, 45, 5, 1, 1])

background            = h('background',            [6.3,       192.4,       48.2,       3.5,       .34,      .26     ])
background_bkgshpUp   = h('background_bkgshpUp',   [6.3 - 1.1, 192.4 - 4.3, 48.2 + 3.8, 3.5 + 1.4, .34 + .1, .26 + .1])
background_bkgshpDown = h('background_bkgshpDown', [6.3 + 1.1, 192.4 + 4.3, 48.2 - 3.8, 3.5 - 1.4, .34 - .1, .26 - .1])

signal = [1.15, 2.72, 4.2, 4.86, 4.93, 0.13*49/.2]
w = .25*17.2/sum(signal)
signal = [w*s for s in signal]
signal = h('signal', signal)

f.Write()
f.Close()
