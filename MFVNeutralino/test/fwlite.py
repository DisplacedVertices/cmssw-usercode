from JMTucker.MFVNeutralino.NtupleCommon import dataset
from JMTucker.Tools import colors
from JMTucker.Tools.ROOTTools import *
from JMTucker.Tools.SampleFiles import get_local_fns

cmssw_setup()
set_style()

from DataFormats.FWLite import Handle, Events

auxes, auxesLabel = Handle('std::vector<MFVVertexAux>'), 'mfvVerticesAux'
mfvev, mfvevLabel = Handle('MFVEvent'), 'mfvEvent'

events = Events(get_local_fns('mfv_stopdbardbar_tau001000um_M0800_2017', dataset))

JByNtracks = 0
PTracksOnly, PJetsByNtracks, PTracksPlusJetsByNtracks = 0,1,2

# pyroot doesn't grok uchars as numbers
def uchar2int(x):
    assert len(x) == 1
    x = ord(x)
    assert 0 <= x <= 255
    return x
    
for iev,event in enumerate(events):
    if iev >= 1000: break
    print '\nEvent %d: run %6d, lumi %4d, event %12d' % (iev, event.eventAuxiliary().run(), event.eventAuxiliary().luminosityBlock(), event.eventAuxiliary().event())                                                                                                                                                                                                                         

    event.getByLabel(auxesLabel, auxes)
    event.getByLabel(mfvevLabel, mfvev)
    e = mfvev.product()

    fmt = '  %4i%4i%10.4f%5i%10.4f%10.4f%10.4f%6i%10.4f%10.4f%10.4f%10.4f%10.4f%10.4f'
    print fmt.replace('.4f','s').replace('i','s') % ('isv', 'sel', 'gen3ddist', 'ntk', 'dbv', 'geo2ddist', 'bs2derr', 'njets', 'tkonlyphi', 'tkonlymass', 'jetsphi', 'jetsmass', 'tksjetsphi', 'tksjetsmass')

    for ia,a in enumerate(auxes.product()):
        dbv = e.bs2ddist(a.x, a.y, a.z)
        njets = uchar2int(a.njets[JByNtracks])
        sel = a.ntracks() >= 5 and dbv >= 0.01 and a.geo2ddist() < 2. and a.bs2derr < 0.0025

        color = colors.green if sel else colors.yellow
        if sel and abs(a.phi[PJetsByNtracks]) < 0.125:
            color = colors.boldred

        print color(fmt % (ia, sel, a.gen3ddist, a.ntracks(), dbv, a.geo2ddist(), a.bs2derr,
                           njets, 
                           a.phi[PTracksOnly], a.mass[PTracksOnly],
                           a.phi[PJetsByNtracks], a.mass[PJetsByNtracks],
                           a.phi[PTracksPlusJetsByNtracks], a.mass[PTracksPlusJetsByNtracks]))
