#include "DataFormats/Math/interface/deltaR.h"
#include "JMTucker/Tools/interface/MCInteractionTop.h"
#include "JMTucker/Tools/interface/GenUtilities.h"
#include "JMTucker/Tools/interface/Utilities.h"

MCInteractionTop::dif_lepton_pair::dif_lepton_pair(const reco::Candidate* chg, const reco::Candidate* nu) :
  charged (dynamic_cast<const reco::GenParticle*>(chg)),
  neutrino(dynamic_cast<const reco::GenParticle*>(nu)),
  closest_jet(0),
  mother_jet(0),
  p4_charged (make_tlv(charged)),
  p4_neutrino(make_tlv(neutrino))
{}

void MCInteractionTop::SetFourVectors() {
  for (int i = 0; i < 2; ++i) {
    if (stop) {
      p4_stops[i] = make_tlv(stops[i]);
      p4_neutralinos[i] = make_tlv(neutralinos[i]);
    }
    p4_tops[i] = make_tlv(tops[i]);
    p4_Ws[i] = make_tlv(Ws[i]);
    p4_bottoms[i] = bottoms[i] ? make_tlv(bottoms[i]) : TLorentzVector();
    for (int j = 0; j < 2; ++j)
      p4_W_daughters[i][j] = make_tlv(W_daughters[i][j]);
  }

  p4_stopstopbar = p4_stop + p4_stopbar;
  p4_toptopbar = p4_top + p4_topbar;
  p4_neutralinosum = p4_neutralino_from_stop + p4_neutralino_from_stopbar;
    
  if (decay_plus < 3 && decay_minus < 3)
    p4_W_neutrinosum = p4_Wplus_neutrino + p4_Wminus_neutrino;
  else if (decay_plus < 3)
    p4_W_neutrinosum = p4_Wplus_neutrino;
  else if (decay_minus < 3)
    p4_W_neutrinosum = p4_Wminus_neutrino;
  else
    p4_W_neutrinosum = TLorentzVector();

  p4_dif_neutrinosum = TLorentzVector();
  for (int i = 0, ie = int(dif_leptons.size()); i < ie; ++i)
    p4_dif_neutrinosum += dif_leptons[i].p4_neutrino;

  p4_neutrinosum = p4_W_neutrinosum + p4_dif_neutrinosum;
  p4_missingsum = p4_neutralinosum + p4_neutrinosum;
}

void MCInteractionTop::Fill(const reco::GenParticleCollection& gens) {
  Clear();
  gen_particles = &gens;

  // Find the stop and stopbar (but they might not be there for
  // e.g. regular ttbar sample.) Raise an exception if only one of the
  // pair is found.
  // Also find the top and topbar. Mandatory, so raise an exception if
  // either is not found.
  for (int i = 0, ie = int(gens.size()); i < ie; ++i) {
    const reco::GenParticle& gen = gens.at(i);
    if      (gen.pdgId() ==  1000006) stops[0] = &gen;
    else if (gen.pdgId() == -1000006) stops[1] = &gen;
    else if (gen.pdgId() ==  6) tops[0] = &gen;
    else if (gen.pdgId() == -6) tops[1] = &gen;
  }
  
  die_if_not((stops[0] == 0 && stops[1] == 0) ||
	     (stops[0] != 0 && stops[1] != 0),
	     "only one of stop (%p) or stopbar (%p) found",
	     stops[0], stops[1]);

  // JMTBAD modify for singletop
  if (tops[0] == 0 || tops[1] == 0)
    return;

  // If we have stops and tops, make sure they're related. (We didn't
  // just go to top from stop because we might run this code on plain
  // ttbar events.)
  if (stops[0])
    die_if_not(tops[0]->numberOfMothers() == 1 && tops[0]->mother(0) == stops[0] &&
	       tops[1]->numberOfMothers() == 1 && tops[1]->mother(0) == stops[1],
	       "tops and stops found but tops not related to stops");

  // Find the neutralinos and any ISR off the stops.
  if (stops[0]) {
    die_if_not(stops[0]->numberOfDaughters() >= 2 &&
	       stops[1]->numberOfDaughters() >= 2,
	       "at least one stop doesn't have at least two daughters: stop %i stopbar %i",
	       stops[0]->numberOfDaughters(), stops[1]->numberOfDaughters());

    neutralinos[0] = dynamic_cast<const reco::GenParticle*>(get_daughter_with_id(stops[0], 1000022));
    neutralinos[1] = dynamic_cast<const reco::GenParticle*>(get_daughter_with_id(stops[1], 1000022));
    die_if_not(neutralinos[0] && neutralinos[1],
	       "at least one neutralino not found: from_stop %p from_stopbar %p",
	       neutralinos[0], neutralinos[1]);

    get_daughters_with_id(stops[0], 21, gluons_from_stops[0]);
    get_daughters_with_id(stops[1], 21, gluons_from_stops[1]);
  }

  // Find the Ws and bs from top decay, and any gluons off the
  // tops. Bottom or bottombar might not be there, since |Vtb| isn't
  // exactly 1.
  die_if_not(tops[0]->numberOfDaughters() >= 2 &&
	     tops[1]->numberOfDaughters() >= 2,
	     "at least one top doesn't have at least two daughters: top %i topbar %i",
	     tops[0]->numberOfDaughters(), tops[1]->numberOfDaughters());

  Ws[0] = dynamic_cast<const reco::GenParticle*>(get_daughter_with_id(top,     24));
  Ws[1] = dynamic_cast<const reco::GenParticle*>(get_daughter_with_id(topbar, -24));
  bottoms[0] = dynamic_cast<const reco::GenParticle*>(get_daughter_with_id(top,     5));
  bottoms[1] = dynamic_cast<const reco::GenParticle*>(get_daughter_with_id(topbar, -5));
  die_if_not(Ws[0] && Ws[1], "at least one W not found: W+ %p W- %p", Ws[0], Ws[1]);

  get_daughters_with_id(tops[0], 21, gluons_from_tops[0]);
  get_daughters_with_id(tops[1], 21, gluons_from_tops[1]);

  // W decays: hadronic, semi-leptonic, or dileptonic?
  assert(Ws[0]->numberOfDaughters() == 3 &&
	 Ws[1]->numberOfDaughters() == 3); // 3 because one W daughter is a status-2 W, plus 2 decay products

  // Find the non-status-2-W daughters, and store them in the order
  // (down-type quark, up-type quark) or (charged lepton, neutrino).
  // JMTBAD actually we're just getting the status-2 daughters...
  for (int i = 0; i < 2; ++i) {
    std::vector<const reco::GenParticle*> daus;
    for (int j = 0; j < 3; ++j) {
      const reco::Candidate* d = Ws[i]->daughter(j);
      if (d->pdgId() != Ws[i]->pdgId())
	daus.push_back(dynamic_cast<const reco::GenParticle*>(d));
    }
    die_if_not(daus.size() == 2, "a W did not have exactly two non-W daughters: i=%i", i);
    const int order = abs(daus[0]->pdgId()) % 2 == 0;
    W_daughters[i][0] = daus[ order];
    W_daughters[i][1] = daus[!order];
  }

  // Count and store decay types: e, mu, tau, hadronic (0-3).
  num_leptonic = 0;
  for (int i = 0; i < 2; ++i) {
    if (is_quark(W_daughters[i][0]))
      die_if_not(is_quark(W_daughters[i][1]), "one W daughter is quark but other is not");
    else {
      die_if_not(is_lepton(W_daughters[i][0]) && is_lepton(W_daughters[i][1]), "one W daughter is lepton and other is not");
      ++num_leptonic;
    }

    decay_type[i] = lepton_code(W_daughters[i][0]);
  }

  // Find neutrinos and their charged lepton partners from
  // decays-in-flight. Don't include the "immediate" neutrinos from
  // the leptonic top decays.
  for (int i = 0, ie = int(gens.size()); i < ie; ++i) {
    const reco::GenParticle& gen = gens.at(i);
    if (gen.status() != 1 || !is_neutrino(&gen))
      continue;

    const reco::Candidate* nu = &gen;
    die_if_not(nu->numberOfMothers() == 1, "neutrino at index %i with # mothers = %i", i, nu->numberOfMothers());
    const reco::Candidate* nu_mom = nu->mother();
    if (nu_mom->pdgId() == nu->pdgId())
      while (nu_mom->status() != 3)
	nu_mom = nu_mom->mother();

    bool immediate = false;
    for (int j = 0; j < 2; ++j)
      for (int k = 0; k < 2; ++k)
	if (nu_mom == W_daughters[j][k]) // the W daughters above are the status-3 ones JMTBAD should set the status-1 leptons for the daughters above
	  immediate = true;

    if (immediate)
      continue;

    // Find the charged lepton partner. Should be the "sister" of the
    // nu, i.e. -11 for nu.id = 12. If nu is a nu_tau not from the
    // leptonic top decay, it won't have a sister, but rather a tau
    // mother that may or may not be from the leptonic top decay. In
    // either case, keep that tau.
    const reco::Candidate* chg = 0;
    for (size_t j = 0; j < nu_mom->numberOfDaughters(); ++j) {
      const reco::Candidate* dau = nu_mom->daughter(j);
      if (dau->pdgId() * nu->pdgId() < 0 && abs(nu->pdgId()) - abs(dau->pdgId()) == 1) {
	die_if_not(chg == 0, "found more than one sister charged lepton for nu");
	chg = dau; // don't break because we want to see if there's other possibilities
      }
    }

    if (chg == 0) {
      die_if_not(abs(nu->pdgId()) == 16, "did not find any sister charged lepton for nu (e or mu) at index %i", i);
      die_if_not(abs(nu_mom->pdgId()) == 15, "mother of nu_tau at index %i is not a tau", i);
      chg = nu_mom;
    }

    dif_leptons.push_back(dif_lepton_pair(chg, nu));
  }

  // Set up the "plain" four-vectors for the above.
  SetFourVectors();
}

void MCInteractionTop::FindDIFJets(const reco::GenJetCollection& gen_jets) {
  for (int i = 0, ie = int(dif_leptons.size()); i < ie; ++i) {
    MCInteractionTop::dif_lepton_pair& dif = dif_leptons[i];
    
    double dR, closest_dR = 1e99;
    for (int j = 0, je = int(gen_jets.size()); j < je; ++j) {
      const reco::GenJet& gen_jet = gen_jets[j];

      // Look for a closest GenJet (in deltaR) to the charged
      // lepton. Only consider GenJets with p more than the lepton.
      if (gen_jet.pt() > dif.charged->pt() && (dR = reco::deltaR(gen_jet, *dif.charged)) < closest_dR) {
	closest_dR = dR;
	dif.closest_jet = &gen_jet;
      }

      // See if this GenJet has the charged lepton or neutrino as its
      // mother (should probably check for both), recording it if
      // so. Ensure that two GenJets don't wind up being associated to
      // the DIF in this way. JMTBAD need to revisit because of taus
      const std::vector<const reco::GenParticle*>& constituents = gen_jet.getGenConstituents();
      for (int k = 0, ke = int(constituents.size()); k < ke; ++k) {
	if ((abs(dif.charged->pdgId()) == 15 && constituents[k]->mother() == dif.charged) || constituents[k] == dif.charged) { // || constituents[k] == dif.neutrino) {
	  dif.mother_jet = &gen_jet;
	  break;
	}
      }
    }
  }
}

void MCInteractionTop::Print(std::ostream& out) {
  printf("MCInteractionTop:\n");
  printf("num_leptons: %i\n", num_leptonic);
  const char* decay_types[4] = {"e", "mu", "tau", "h"};
  printf("decay type: W+ -> %s,  W- -> %s\n", decay_types[decay_plus], decay_types[decay_minus]);
  print_gen_and_daus(0,                       "header",                  *gen_particles);
  print_gen_and_daus(stop,                    "stop",                    *gen_particles);
  print_gen_and_daus(stopbar,                 "stopbar",                 *gen_particles);
  print_gen_and_daus(neutralino_from_stop,    "neutralino_from_stop",    *gen_particles);
  print_gen_and_daus(neutralino_from_stopbar, "neutralino_from_stopbar", *gen_particles);
  print_gen_and_daus(top,                     "top",                     *gen_particles);
  print_gen_and_daus(topbar,                  "topbar",                  *gen_particles);
  print_gen_and_daus(Wplus,                   "Wplus",                   *gen_particles);
  print_gen_and_daus(Wminus,                  "Wminus",                  *gen_particles);
  print_gen_and_daus(bottom,                  "bottom",                  *gen_particles);
  print_gen_and_daus(bottombar,               "bottombar",               *gen_particles);
  print_gen_and_daus(W_daughters[0][0],       "Wplus daughter 0",        *gen_particles);
  print_gen_and_daus(W_daughters[0][1],       "Wplus daughter 1",        *gen_particles);
  print_gen_and_daus(W_daughters[1][0],       "Wminus daughter 0",       *gen_particles);
  print_gen_and_daus(W_daughters[1][1],       "Wminus daughter 1",       *gen_particles);
  if (!dif_leptons.empty())
    printf("charged leptons/neutrinos from decays-in-flight:\n");
  for (int i = 0, ie = int(dif_leptons.size()); i < ie; ++i) {
    print_gen_and_daus(dif_leptons[i].charged,     TString::Format("chg #%i", i), *gen_particles);
    print_gen_and_daus(dif_leptons[i].neutrino,    TString::Format("nu  #%i", i), *gen_particles);
    print_gen_and_daus(dif_leptons[i].closest_jet, TString::Format("closest jet #%i", i), *gen_particles, false);
    print_gen_and_daus(dif_leptons[i].mother_jet,  TString::Format("mother  jet #%i", i), *gen_particles, false);
  }
  printf("p4_missingsum ex: %.2f  ey: %.2f    et: %.2f  phi: %.3f\n", p4_missingsum.Px(), p4_missingsum.Py(), p4_missingsum.Pt(), p4_missingsum.Phi());
}
