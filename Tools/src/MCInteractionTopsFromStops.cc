#include "JMTucker/Tools/interface/MCInteractionTopsFromStops.h"
#include "JMTucker/Tools/interface/GenUtilities.h"
#include "JMTucker/Tools/interface/Utilities.h"

void MCInteractionTopsFromStops::Clear() {
  MCInteractionTops::Clear();
  for (int i = 0; i < 2; ++i) {
    stops[i] = neutralinos[i] = 0;
    gluons_from_stops[i].clear();
    p4_stops[i] = p4_neutralinos[i] = TLorentzVector();
  }
  p4_stopstopbar = p4_neutralinosum = TLorentzVector();
}

bool MCInteractionTopsFromStops::Valid() {
  return MCInteractionTops::Valid();
}

void MCInteractionTopsFromStops::Fill() {
  // Find the stop and stopbar.
  for (int i = 0, ie = int(gen_particles->size()); i < ie; ++i) {
    const reco::GenParticle& gen = gen_particles->at(i);
    if      (gen.pdgId() ==  1000006) stops[0] = &gen;
    else if (gen.pdgId() == -1000006) stops[1] = &gen;
  }
  
  die_if_not((stops[0] == 0 && stops[1] == 0) ||
	     (stops[0] != 0 && stops[1] != 0),
	     "only one of stop (%p) or stopbar (%p) found",
	     stops[0], stops[1]);

  // Find the neutralinos and any ISR off the stops.
  if (stops[0]) {
    die_if_not(stops[0]->numberOfDaughters() >= 2 &&
	       stops[1]->numberOfDaughters() >= 2,
	       "at least one stop doesn't have at least two daughters: stop %i stopbar %i",
	       stops[0]->numberOfDaughters(), stops[1]->numberOfDaughters());

    neutralinos[0] = dynamic_cast<const reco::GenParticle*>(daughter_with_id(stops[0], 1000022));
    neutralinos[1] = dynamic_cast<const reco::GenParticle*>(daughter_with_id(stops[1], 1000022));
    die_if_not(neutralinos[0] && neutralinos[1],
	       "at least one neutralino not found: from_stop %p from_stopbar %p",
	       neutralinos[0], neutralinos[1]);

    daughters_with_id(stops[0], 21, gluons_from_stops[0]);
    daughters_with_id(stops[1], 21, gluons_from_stops[1]);
  }

  MCInteractionTops::Fill();

  // If we have stops and tops, make sure they're related.
  if (stops[0])
    die_if_not(tops[0]->numberOfMothers() == 1 && tops[0]->mother(0) == stops[0] &&
	       tops[1]->numberOfMothers() == 1 && tops[1]->mother(0) == stops[1],
	       "tops and stops found but tops not related to stops");
}

void MCInteractionTopsFromStops::SetFourVectors() {
  for (int i = 0; i < 2; ++i) {
    if (stops      [i]) p4_stops      [i] = make_tlv(stops      [i]);
    if (neutralinos[i]) p4_neutralinos[i] = make_tlv(neutralinos[i]);
  }

  p4_stopstopbar = p4_stop + p4_stopbar;
  p4_neutralinosum = p4_neutralino_from_stop + p4_neutralino_from_stopbar;
    
  MCInteractionTops::SetFourVectors(); // need to do this to set p4_W_neutrinosum and p4_dif_neutrinosum

  p4_missingsum += p4_neutralinosum;
}

void MCInteractionTopsFromStops::Print(std::ostream& out) {
  if (!Valid()) {
    out << "not valid\n";
    return;
  }
  print_gen_and_daus(0,                       "header",                  *gen_particles);
  print_gen_and_daus(stop,                    "stop",                    *gen_particles);
  print_gen_and_daus(stopbar,                 "stopbar",                 *gen_particles);
  print_gen_and_daus(neutralino_from_stop,    "neutralino_from_stop",    *gen_particles);
  print_gen_and_daus(neutralino_from_stopbar, "neutralino_from_stopbar", *gen_particles);
  MCInteractionTops::Print(out);
}
