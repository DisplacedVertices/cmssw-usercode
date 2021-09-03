from DVCode.Tools.ROOTTools import *
cmssw_setup()
set_style()

from DataFormats.FWLite import Handle, Events

muons, muonLabel = Handle("std::vector<pat::Muon>"), "slimmedMuons"
vertices, vertexLabel = Handle("std::vector<reco::Vertex>"), "offlineSlimmedPrimaryVertices"

events = Events("file:/uscms/home/tucker/scratch/zzz.root")

h_nmu = ROOT.TH1F('h_nmu', '', 10, 0, 10)
h_muq = ROOT.TH1F('h_muq', '', 3, -1, 2)
h_mupt = ROOT.TH1F('h_mupt', '', 150, 0, 3000)
h_mueta = ROOT.TH1F('h_mueta', '', 50, -2.5, 2.5)
h_muphi = ROOT.TH1F('h_muphi', '', 50, -3.15, 3.15)
h_mudpt = ROOT.TH1F('h_mudpt', '', 100, 0, 3)
h_mures = ROOT.TH1F('h_mures', '', 100, -0.75, 0.75)

hs = h_nmu, h_muq, h_mupt, h_mueta, h_muphi, h_mudpt, h_mures

for iev,event in enumerate(events):
    if iev >= 1000: break
    print "\nEvent %d: run %6d, lumi %4d, event %12d" % (iev,event.eventAuxiliary().run(), event.eventAuxiliary().luminosityBlock(),event.eventAuxiliary().event())                                                                                                                                                                                                                         

    event.getByLabel(muonLabel, muons)
    event.getByLabel(vertexLabel, vertices)

    if len(vertices.product()) == 0 or vertices.product()[0].ndof() < 4:                                                                                                                                                                                                                                                                                                                    
        print "Event has no good primary vertex."
        continue
    else:
        PV = vertices.product()[0]
        print "PV at x,y,z = %+5.3f, %+5.3f, %+6.3f, ndof: %.1f" % (PV.x(), PV.y(), PV.z(), PV.ndof())

    nmu = 0
    for i,mu in enumerate(muons.product()):
        if mu.isHighPtMuon(PV):
            nmu += 1
            gen = mu.genParticle()
            if gen:
                genqpt = gen.pt() * gen.charge()
            else:
                genqpt = None
            tk = mu.tunePMuonBestTrack()
            q, pt, eta, phi, pterr = tk.charge(), tk.pt(), tk.eta(), tk.phi(), tk.ptError()

            print 'muon: q*pt %f eta %f phi %f dpt %f  gen q*pt %s' % (q*pt, eta, phi, pterr, genqpt)
            h_muq.Fill(q)
            h_mupt.Fill(pt)
            h_mueta.Fill(eta)
            h_muphi.Fill(phi)
            h_mudpt.Fill(pterr / pt)
            if genqpt and 500 < pt < 2000 and abs(eta) < 0.9:
                h_mures.Fill((1./q/pt - 1./genqpt) / (1./genqpt))
    h_nmu.Fill(nmu)

ps = plot_saver('plots/mures')

for h in hs:
    h.Draw()
    ps.save(h.GetName())
