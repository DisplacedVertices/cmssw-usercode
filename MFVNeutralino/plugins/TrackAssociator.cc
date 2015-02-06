#include "TH2F.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/BeamSpot/interface/BeamSpot.h"
#include "DataFormats/JetReco/interface/GenJet.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/METReco/interface/GenMET.h"
#include "DataFormats/METReco/interface/GenMETCollection.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "MagneticField/Records/interface/IdealMagneticFieldRecord.h"
#include "MagneticField/Engine/interface/MagneticField.h"
#include "SimDataFormats/TrackingAnalysis/interface/TrackingParticle.h"
#include "SimTracker/Records/interface/TrackAssociatorRecord.h"
#include "SimTracker/TrackAssociation/interface/TrackAssociatorBase.h"
#include "JMTucker/MFVNeutralino/interface/MCInteractionMFV3j.h"
#include "JMTucker/Tools/interface/Framework.h"
#include "JMTucker/Tools/interface/GenUtilities.h"

class MFVTrackAssociator : public edm::EDAnalyzer {
public:
  MFVTrackAssociator(const edm::ParameterSet&);
  virtual ~MFVTrackAssociator() {}
  virtual void analyze(const edm::Event&, const edm::EventSetup&);
  
private:
  const edm::InputTag tracks_src;
  const edm::InputTag sim_tracks_src;
  const edm::InputTag sim_vertices_src;
  const edm::InputTag tracking_particles_src;
  const edm::InputTag gen_particles_src;
  const edm::InputTag rec_vertices_src;
  const bool do_checks;

  TH1F* h_badtpcount;
  TH1F* h_reco2simnmatches;
  TH2F* h_missingtp_ptvseta;
  TH1F* h_fracsigmatched;
  TH1F* h_fracnonmatched;
  TH2F* h_fracsigmatched_vs_nvtx;
  TH2F* h_fracnonmatched_vs_nvtx;
  TH2F* h_ninvertsvsnsigtracks;
  TH1F* h_fracsigtracksinverts;
  TH1F* h_fracnonmatchedtracks;

  TH1F* h_sigtrack_simxy;
  TH1F* h_sigtrack_simz;
  TH1F* h_sigtrack_simxyz;
  TH1F* h_sigtrack_simcosth;
  TH1F* h_sigtrack_simpt;
  TH1F* h_sigtrack_simp;
  TH1F* h_sigtrack_invtx_simxy;
  TH1F* h_sigtrack_invtx_simz;
  TH1F* h_sigtrack_invtx_simxyz;
  TH1F* h_sigtrack_invtx_simcosth;
  TH1F* h_sigtrack_invtx_simpt;
  TH1F* h_sigtrack_invtx_simp;

  TH1F* h_ngenjet[3];
  TH1F* h_nconstituents[3];
  TH1F* h_cnstfromlsp[3];
  TH2F* h_cnstfromlspvsncnst[3];
  TH2F* h_cnstfromlsp2v1[3];
};

MFVTrackAssociator::MFVTrackAssociator(const edm::ParameterSet& cfg)
  : tracks_src(cfg.getParameter<edm::InputTag>("tracks_src")),
    sim_tracks_src(cfg.getParameter<edm::InputTag>("sim_tracks_src")),
    sim_vertices_src(cfg.getParameter<edm::InputTag>("sim_vertices_src")),
    tracking_particles_src(cfg.getParameter<edm::InputTag>("tracking_particles_src")),
    gen_particles_src(cfg.getParameter<edm::InputTag>("gen_particles_src")),
    rec_vertices_src(cfg.getParameter<edm::InputTag>("rec_vertices_src")),
    do_checks(cfg.getParameter<bool>("do_checks"))
{
  edm::Service<TFileService> fs;
  h_badtpcount = fs->make<TH1F>("h_badtpcount", "", 100, 0, 100);
  if (do_checks) {
    h_reco2simnmatches = fs->make<TH1F>("h_reco2simnmatches", "", 10, 0, 10);
    h_missingtp_ptvseta = fs->make<TH2F>("h_missingtp_ptvseta", "", 400, -10, 10, 400, 0, 100);
    h_fracsigmatched = fs->make<TH1F>("h_fracsigmatched", "", 101, 0, 1.01);
    h_fracnonmatched = fs->make<TH1F>("h_fracnonmatched", "", 101, 0, 1.01);
    h_fracsigmatched_vs_nvtx = fs->make<TH2F>("h_fracsigmatched_vs_nvtx", "", 100, 0, 100, 21, 0, 1.05);
    h_fracnonmatched_vs_nvtx = fs->make<TH2F>("h_fracnonmatched_vs_nvtx", "", 100, 0, 100, 21, 0, 1.05);
  }
  h_ninvertsvsnsigtracks = fs->make<TH2F>("h_ninvertsvsnsigtracks", "", 50, 0, 50, 50, 0, 50);
  h_fracsigtracksinverts = fs->make<TH1F>("h_fracsigtracksinverts", "", 21, 0, 1.05);
  h_fracnonmatchedtracks = fs->make<TH1F>("h_fracnonmatchedtracks", "", 21, 0, 1.05);
  h_sigtrack_simxy    = fs->make<TH1F>("h_sigtrack_simxy", "", 100, 0, 100);
  h_sigtrack_simz     = fs->make<TH1F>("h_sigtrack_simz", "", 100, 0, 100);
  h_sigtrack_simxyz   = fs->make<TH1F>("h_sigtrack_simxyz", "", 100, 0, 100);
  h_sigtrack_simcosth = fs->make<TH1F>("h_sigtrack_simcosth", "", 100, -1, 1);
  h_sigtrack_simpt    = fs->make<TH1F>("h_sigtrack_simpt", "", 100, 0, 500);
  h_sigtrack_simp     = fs->make<TH1F>("h_sigtrack_simp", "", 100, 0, 500);
  h_sigtrack_invtx_simxy    = fs->make<TH1F>("h_sigtrack_invtx_simxy", "", 100, 0, 100);
  h_sigtrack_invtx_simz     = fs->make<TH1F>("h_sigtrack_invtx_simz", "", 100, 0, 100);
  h_sigtrack_invtx_simxyz   = fs->make<TH1F>("h_sigtrack_invtx_simxyz", "", 100, 0, 100);
  h_sigtrack_invtx_simcosth = fs->make<TH1F>("h_sigtrack_invtx_simcosth", "", 100, -1, 1);
  h_sigtrack_invtx_simpt    = fs->make<TH1F>("h_sigtrack_invtx_simpt", "", 100, 0, 500);
  h_sigtrack_invtx_simp     = fs->make<TH1F>("h_sigtrack_invtx_simp", "", 100, 0, 500);

  const char* zzz[3] = { "hadronic", "semilep", "dilep" };
  for (int i = 0; i < 3; ++i) {
    h_ngenjet[i] = fs->make<TH1F>(TString::Format("h_ngenjet_%s", zzz[i]), "", 50, 0, 50);
    h_nconstituents[i] = fs->make<TH1F>(TString::Format("h_nconstituents_%s", zzz[i]), "", 100, 0, 100);
    h_cnstfromlsp[i] = fs->make<TH1F>(TString::Format("h_cnstfromlsp_%s", zzz[i]), "", 100, 0, 100);
    h_cnstfromlspvsncnst[i] = fs->make<TH2F>(TString::Format("h_cnstfromlspvsncnst_%s", zzz[i]), "", 50, 0, 100, 50, 0, 100);
    h_cnstfromlsp2v1[i] = fs->make<TH2F>(TString::Format("h_cnstfromlsp2v1_%s", zzz[i]), "", 50, 0, 100, 50, 0, 100);
  }
}


const reco::Candidate* any_mother_with_id(const reco::Candidate* c, const int id) {
  for (int i = 0, ie = c->numberOfMothers(); i < ie; ++i) {
    const reco::Candidate* mom = c->mother(i);
    if (mom == 0)
      continue;

    if (mom->pdgId() == id)
      return mom;
    else
      return any_mother_with_id(mom, id);
  }

  return 0;
}

namespace {
  template <typename T>
  T mag(const T& x, const T& y) {
    return sqrt(x*x + y*y);
  }

  template <typename T>
  T mag(const T& x, const T& y, const T& z) {
    return sqrt(x*x + y*y + z*z);
  }

  template <typename T1, typename T2>
  double costh(const T1& a, const T2& b) {
    double ax = a.x();
    double ay = a.y();
    double az = a.z();
    double bx = b.x();
    double by = b.y();
    double bz = b.z();
    return (ax*bx + ay*by + az*bz)/mag(ax,ay,az)/mag(bx,by,bz);
  }

  void hist_fill(std::map<int,int>& hist, int bin) {
    if (hist.find(bin) != hist.end())
      hist[bin] += 1;
    else
      hist[bin] = 1;
  }
  void hist_draw(std::map<int,int>& hist, const std::string& name) {
    std::cout << name << "\n";
    for (auto& c : hist)
      printf("%i: %i\n", c.first, c.second);
  }
}

template <typename T>
std::pair<TrackingParticleRef, double> reco2sim(const reco::RecoToSimCollection& reco_to_sim, const T& track_ref) {
  std::vector<std::pair<TrackingParticleRef, double> > matches;
  try {
    matches = reco_to_sim[track_ref];
  }
  catch (const edm::Exception& e) {
  }
  if (matches.size() > 1)
    throw cms::Exception("reco2sim") << "more than one tracking particle match for " << track_ref;
  else if (matches.size() == 1)
    return matches[0];
  else
    return std::make_pair(TrackingParticleRef(), -1e99);
}

void MFVTrackAssociator::analyze(const edm::Event& event, const edm::EventSetup& setup) {
  std::cout << "run " << event.id().run() << " lumi " << event.luminosityBlock() << " event " << event.id().event() << std::endl;

  edm::Handle<reco::BeamSpot> bs;
  event.getByLabel("offlineBeamSpot", bs);
  printf("beamspot x,y: %f, %f\n", bs->x0(), bs->y0());

  edm::Handle<reco::GenParticleCollection> gen_particles;
  edm::Handle<std::vector<int> > gen_particles_barcodes;
  event.getByLabel(gen_particles_src, gen_particles);
  event.getByLabel(gen_particles_src, gen_particles_barcodes);
  edm::Handle<reco::GenJetCollection> gen_jets;
  event.getByLabel("ak5GenJets", gen_jets);
  edm::Handle<reco::GenMETCollection> gen_mets;
  event.getByLabel("genMetTrue", gen_mets);
  const reco::GenMET& gen_met = gen_mets->at(0);

  GenParticlePrinter gpp(*gen_particles);
  gpp.print_vertex = true;

  MCInteractionMFV3j mci;
  mci.Init(*gen_particles, *gen_jets, gen_met);
  if (!mci.Valid()) {
    edm::LogWarning("GenHistos") << "MCInteractionMFV3j invalid!";
  }
  //  mci.Print(std::cout);

  edm::Handle<TrackingParticleCollection> tracking_particles;
  event.getByLabel(tracking_particles_src, tracking_particles);

#if 0
  int bad_tp_c = 0;
  for (const auto& tp : *tracking_particles)
    if (tp.genParticle().refVector().refCore().productPtr() == 0)      // WHAT THE
      ++bad_tp_c;
  h_badtpcount->Fill(bad_tp_c);
  if (bad_tp_c > 0)
    return;
#endif

#if 0
  edm::Handle<reco::PFJetCollection> jets;
  event.getByLabel("ak5PFJets", jets);

  reco::PFJetCollection selected_jets;
  for (const reco::PFJet& jet : *jets) {
    if (jet.pt() > 20 && 
	fabs(jet.eta()) < 2.5 && 
	jet.numberOfDaughters() > 1 &&
	jet.neutralHadronEnergyFraction() < 0.99 && 
	jet.neutralEmEnergyFraction() < 0.99 && 
	(fabs(jet.eta()) >= 2.4 || (jet.chargedEmEnergyFraction() < 0.99 && jet.chargedHadronEnergyFraction() > 0. && jet.chargedMultiplicity() > 0)))
      selected_jets.push_back(jet);
  }
#endif

  edm::ESHandle<MagneticField> magnetic_field; // not explicitly used below, but if you don't have the record defined in the cfg then the TABH record-getting will fail without telling you this is why
  setup.get<IdealMagneticFieldRecord>().get(magnetic_field);

  edm::ESHandle<TrackAssociatorBase> associator_handle;
  setup.get<TrackAssociatorRecord>().get("TrackAssociatorByHits", associator_handle);
  TrackAssociatorBase* associator = (TrackAssociatorBase*) associator_handle.product();

  edm::Handle<edm::View<reco::Track> > tracks;
  event.getByLabel(tracks_src, tracks);
  
  edm::Handle<edm::SimTrackContainer> sim_tracks;
  event.getByLabel(sim_tracks_src, sim_tracks);
  
  edm::Handle<edm::SimVertexContainer> sim_vertices;
  event.getByLabel(sim_vertices_src, sim_vertices);

  edm::Handle<reco::VertexCollection> rec_vertices;
  event.getByLabel(rec_vertices_src, rec_vertices);

  reco::RecoToSimCollection reco_to_sim = associator->associateRecoToSim(tracks, tracking_particles, &event, &setup);

  if (do_checks) {
    std::cout << "checking hepmc -> genparticles by barcodes\n";
    //  std::cout << "but first a 'unittest'\n";
    //  std::cout << "1293 -> 1846? " << are_directly_related(&gen_particles->at(1293), &gen_particles->at(1846)) << "\n";
    //  std::cout << "1846 -> 1293? " << are_directly_related(&gen_particles->at(1846), &gen_particles->at(1293)) << "\n";
    //  std::cout << "1846 -> 1298? " << are_directly_related(&gen_particles->at(1846), &gen_particles->at(1298)) << "\n";
    //  std::cout << "1864 -> 1349? " << are_directly_related(&gen_particles->at(1864), &gen_particles->at(1349)) << "\n";

    std::cout << "\nEvent ID = " << event.id() << "\n"
	      << "                      ****************** Reco To Sim ****************** \n"
	      << "-- Associator by hits --\n";

    for (size_t i = 0, ie = tracks->size(); i < ie; ++i) {
      edm::RefToBase<reco::Track> track(tracks, i);
      std::vector<std::pair<TrackingParticleRef, double> > matches;
      try {
	matches = reco_to_sim[track];
      }
      catch (const edm::Exception& e) {
	std::cout << "->   Track pT: " << std::setprecision(2) << std::setw(6) << track->pt() <<  " matched to 0  MC Tracks\n";
      }
      h_reco2simnmatches->Fill(matches.size());
      if (matches.size() > 0) {
	std::cout << "Reco Track pT: " << std::setw(6) << track->pt() <<  " matched to " << matches.size() << " MC Tracks\n";
	for (const auto& match : matches) {
	  TrackingParticleRef tp = match.first;
	  double quality = match.second;
	  std::cout << "\t\tMCTrack " << std::setw(2) << tp.index() << " pT: " << std::setw(6) << tp->pt() << " NShared: " << quality << "\n\t\tTrackingParticle genParticles:\n";
	  for (const reco::GenParticleRef& gen : tp->genParticles()) {
	    std::cout << "\t\t\t";
	    printf("\t\t\tVTX INFO %.3f %.3f %.3f\n", gen->vx(), gen->vy(), gen->vz());
	    if (has_any_ancestor_with_id(&*gen, 1000021) && track->pt() > 7) {
	      printf("HELLO / IS IT ME YOU'RE LOOKING FOR\n");
	      gpp.PrintHeader();
	      gpp.Print(any_mother_with_id(&*gen, 1000021), "LIONEL");
	    }
	  }
	}
      }
    }

    std::cout << "                      ****************** Sim To Reco ****************** \n"
	      << "-- Associator by hits --\n";
    reco::SimToRecoCollection sim_to_reco = associator->associateSimToReco(tracks, tracking_particles, &event, &setup);
    for (size_t i = 0, ie = tracking_particles->size(); i < ie; ++i) {
      TrackingParticleRef tp(tracking_particles, i);
      std::vector<std::pair<edm::RefToBase<reco::Track>, double> > matches;
      std::cout << "tracking particle #" << i << " hepmc particles:\n";
      for (const reco::GenParticleRef& gen : tp->genParticles()) {
	if (has_any_ancestor_with_id(&*gen, 1000021))
	  printf("HELLO / IS IT ME YOU'RE LOOKING FOR\n");
      }
      try { 
	matches = sim_to_reco[tp];
      }
      catch (const edm::Exception& e) {
	std::cout << "->   TrackingParticle " << std::setw(2) << tp.index() << " pT: " << std::setprecision(2) << std::setw(6) << tp->pt() <<  " matched to 0  reco::Tracks\n";
      }
      if (matches.size() > 0) {
	std::cout << "Sim Track " << std::setw(2) << tp.index() << " pT: "  << std::setw(6) << tp->pt() << " matched to " << matches.size() << " reco::Tracks\n";
	for (const auto& match : matches) {
	  edm::RefToBase<reco::Track> track = match.first;
	  double quality = match.second;
	  std::cout << "\t\treco::Track pT: " << std::setw(6) << track->pt() << " NShared: " << quality << "\n";
	}
      }


    }

    std::map<int,int> signal_tracks_seen;
    std::map<int,int> signal_tracks_ids;
    std::map<int,int> signal_tracks_charges;
    for (int i = 0, ie = gen_particles->size(); i < ie; ++i) {
      const reco::GenParticle& g = gen_particles->at(i);
      if (g.status() == 1 && 
	  //	fabs(g.eta()) < 2.55 &&
	  !is_neutrino(&g) &&
	  g.pdgId() != 22 && 
	  mag(g.vx(), g.vy()) < 120 &&
	  abs(g.vz()) < 300 &&
	  //	g.pdgId() != 130 && 
	  //	g.pdgId() != 310 && 
	  has_any_ancestor_with_id(&g, 1000021)) {
	hist_fill(signal_tracks_ids, g.pdgId());
	hist_fill(signal_tracks_charges, g.charge());
	signal_tracks_seen[i] = 0;
      }
    }
    printf("'signal' tracks:\n");
    hist_draw(signal_tracks_ids, "signal_tracks_ids");
    hist_draw(signal_tracks_charges, "signal_tracks_charges");
    for (const auto& tp : *tracking_particles) {
      for (const reco::GenParticleRef& gen : tp.genParticles()) {
	int ndx = gen.key(); // this check next is probably now useless after tp uses genparticles directly instead of hepmc::genparticles
	if (signal_tracks_seen.find(ndx) != signal_tracks_seen.end())
	  signal_tracks_seen[ndx] += 1;
      }
    }
    int counts[10] = {0};
    std::vector<int> missing, morethan1;
    for (const auto& it : signal_tracks_seen) {
      int i = it.second < 10 ? it.second : 9;
      counts[i] += 1;
      if      (i == 0) missing.push_back(it.first);
      else if (i  > 1) morethan1.push_back(it.first);
    }
    printf("# signal tracks: %i\n", int(signal_tracks_seen.size()));
    printf("histogram of tracking particles assoc'd to them:\n");
    for (auto c : counts)
      printf("%i  ", c);
    printf("genparticles without trackingparticles:\n");
    gpp.PrintHeader();
    for (auto ndx : missing) {
      const reco::GenParticle& g = gen_particles->at(ndx);
      gpp.Print(&g, "missing");
      printf("       vtx: %.4f %.4f %.4f\n", g.vx(), g.vy(), g.vz());
      h_missingtp_ptvseta->Fill(g.eta(), g.pt());
    }
  }

  {
    const bool save_gpp = gpp.print_mothers;
    gpp.print_mothers = true;

    printf("testing final_candidate_with_copies\n");
    int igen = 0;
    std::set<const reco::Candidate*> finals_already;
    for (const reco::GenParticle& gen : *gen_particles) {
      if (abs(gen.pdgId()) != 3)
	continue;

      std::pair<const reco::Candidate*, std::vector<const reco::Candidate*> > top_copies = final_candidate_with_copies(&gen, 3);
      if (finals_already.count(top_copies.second.back()) > 0)
	continue;
      finals_already.insert(top_copies.second.back());

      printf("found a strange!\n");
      gpp.PrintHeader();
      for (int icopy = 0, icopye = int(top_copies.second.size()); icopy < icopye; ++icopy) {
	char buf[64];
	snprintf(buf, 64, "copy #%i", icopy);
	gpp.Print(top_copies.second[icopy], buf);
      }

      ++igen;
    }

    gpp.print_mothers = save_gpp;
  }
      
  {
    int zzz = -1;
    if (mci.decay_type[0] == 3 && mci.decay_type[1] == 3)
      zzz = 0;
    else if ((mci.decay_type[0] != 3 && mci.decay_type[1] == 3) || (mci.decay_type[0] == 3 && mci.decay_type[1] != 3))
      zzz = 1;
    else if (mci.decay_type[0] != 3 && mci.decay_type[1] != 3)
      zzz = 2;
    else
      assert(0);

    h_ngenjet[zzz]->Fill(gen_jets->size());
    int ijet = 0;
    for (const reco::GenJet& gen_jet : *gen_jets) {
      const std::vector<const reco::GenParticle*>& constituents = gen_jet.getGenConstituents();
      h_nconstituents[zzz]->Fill(constituents.size());
      printf("gen jet #%i: pt %.2f  eta %.2f  phi %.2f  nconstituents = %i\n", ijet++, gen_jet.pt(), gen_jet.eta(), gen_jet.phi(), int(constituents.size()));
      int iconst = 0;
      gpp.PrintHeader();
      char buf[64];
      int nfromlsp = 0;
      int lspseen[2] = {0};
      for (const reco::GenParticle* g : constituents) {
	bool from_lsp = has_any_ancestor_with_id(g, 1000021);
	bool from_lsp_new = mci.Ancestor(g, "lsp") != 0;
	bool from_quark = mci.Ancestor(g, "quark") != 0;
	if (is_ancestor_of(g, mci.lsps[0]))
	  ++lspseen[0];
	else if (is_ancestor_of(g, mci.lsps[1]))
	  ++lspseen[1];
	if (from_lsp_new)
	  ++nfromlsp;
	snprintf(buf, 64, "cnst #%2i: %i %i %i", iconst++, from_lsp, from_lsp_new, from_quark); 
	gpp.Print(g, buf);
	if (from_lsp != from_lsp_new)
	  printf("FROM LSP DIFF\n");
      }

      h_cnstfromlsp[zzz]->Fill(nfromlsp);
      h_cnstfromlspvsncnst[zzz]->Fill(constituents.size(), nfromlsp);
      h_cnstfromlsp2v1[zzz]->Fill(lspseen[0], lspseen[1]);
    }
  }

  int ivtx = 0;
  std::set<int> tracks_in_vertices;
  const int nvtx = int(rec_vertices->size());
  for (const reco::Vertex& vtx : *rec_vertices) {
    const int ntracks = int(vtx.tracksSize());
    printf("inclusivevertex #%i with %i tracks:\n", ivtx, ntracks);
    int sigmatched = 0;
    int nonmatched = 0;

    for (auto it = vtx.tracks_begin(), ite = vtx.tracks_end(); it != ite; ++it) {
      //const reco::Track& tk = tracks->at(it->key());
      const reco::TrackBaseRef& track = *it;
      tracks_in_vertices.insert(track.key());
      std::vector<std::pair<TrackingParticleRef, double> > matches;
      try {
	matches = reco_to_sim[track];
      }
      catch (const edm::Exception& e) {
      }
      if (matches.size() > 0) {
	for (const auto& match : matches) {
	  TrackingParticleRef tp = match.first;
	  //printf("\t\ttp match quality %.4f\n", match.second);
	  for (const reco::GenParticleRef& gen : tp->genParticles()) {
	    if (has_any_ancestor_with_id(&*gen, 1000021))
	      ++sigmatched;
	  }
	}
      }
      else
	++nonmatched;
    }

    if (do_checks) {
      h_fracsigmatched->Fill(sigmatched/float(ntracks));
      h_fracnonmatched->Fill(nonmatched/float(ntracks));
      h_fracsigmatched_vs_nvtx->Fill(nvtx, sigmatched/float(ntracks));
      h_fracnonmatched_vs_nvtx->Fill(nvtx, nonmatched/float(ntracks));
      printf("\tsignal matched: %i (%.2f%%)  no match: %i (%.2f%%)\n", sigmatched, 100*sigmatched/float(ntracks), nonmatched, 100*nonmatched/float(ntracks));
    }
    ++ivtx;
  }

  const int ntracks = tracks->size();
  int ninvertex = 0;
  int nsigtracks = 0;
  int nnonmatched = 0;
  for (int i = 0; i < ntracks; ++i) {
    const bool in_a_vertex = tracks_in_vertices.count(i) > 0;

    reco::TrackBaseRef track(tracks, i);
    if (track->pt() < 10)
      continue;

    std::vector<std::pair<TrackingParticleRef, double> > matches;
    try {
      matches = reco_to_sim[track];
    }
    catch (const edm::Exception& e) {
    }
    if (matches.size() > 0) {
      for (const auto& match : matches) {
	TrackingParticleRef tp = match.first;
	//printf("\t\ttp match quality %.4f\n", match.second);
	for (const reco::GenParticleRef& gen : tp->genParticles()) {
	  if (has_any_ancestor_with_id(&*gen, 1000021)) {
	    ++nsigtracks;
	    
	    h_sigtrack_simxy->Fill(mag(gen->vx(), gen->vy()));
	    h_sigtrack_simz->Fill(gen->vz());
	    h_sigtrack_simxyz->Fill(mag(gen->vx(), gen->vy(), gen->vz()));
	    h_sigtrack_simcosth->Fill(costh(gen->momentum(), gen->vertex()));
	    h_sigtrack_simpt->Fill(gen->pt());
	    h_sigtrack_simp->Fill(gen->p());

	    if (in_a_vertex) {
	      ++ninvertex;
	      h_sigtrack_invtx_simxy->Fill(mag(gen->vx(), gen->vy()));
	      h_sigtrack_invtx_simz->Fill(gen->vz());
	      h_sigtrack_invtx_simxyz->Fill(mag(gen->vx(), gen->vy(), gen->vz()));
	      h_sigtrack_invtx_simcosth->Fill(costh(gen->momentum(), gen->vertex()));
	      h_sigtrack_invtx_simpt->Fill(gen->pt());
	      h_sigtrack_invtx_simp->Fill(gen->p());
	    }
	  }
	}
      }
    }
    else
      ++nnonmatched;
  }

  h_ninvertsvsnsigtracks->Fill(nsigtracks, ninvertex);
  h_fracsigtracksinverts->Fill(ninvertex/float(nsigtracks));
  h_fracnonmatchedtracks->Fill(nnonmatched/float(ntracks));


  printf("pat jet time\n");
  edm::Handle<pat::JetCollection> pat_jets;
  event.getByLabel("selectedPatJetsPF", pat_jets);
  
  int ijet = 0;
  for (const auto& jet : *pat_jets) {
    printf("ijet %i\n", ijet);
    const reco::TrackRefVector& tracks = jet.associatedTracks();
    for (int itrk = 0; itrk < int(tracks.size()); ++itrk) {
      const reco::TrackRef& track = tracks.at(itrk);
      dump_ref(std::cout, track, &event);
    }
    ++ijet;
  }

  std::cout << std::endl;
  std::cout << std::endl;
}

DEFINE_FWK_MODULE(MFVTrackAssociator);
