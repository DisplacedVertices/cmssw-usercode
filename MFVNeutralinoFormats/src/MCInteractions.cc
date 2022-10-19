#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "JMTucker/MFVNeutralinoFormats/interface/MCInteractions.h"
#include "DataFormats/Math/interface/deltaR.h"

namespace mfv {
  bool MCInteractionHolderTtbar::valid() const {
    return
      tops[0].isNonnull() && bottoms[0].isNonnull() && Ws[0].isNonnull() && W_daughters[0][0].isNonnull() && W_daughters[0][1].isNonnull() &&
      tops[1].isNonnull() && bottoms[1].isNonnull() && Ws[1].isNonnull() && W_daughters[1][0].isNonnull() && W_daughters[1][1].isNonnull();
  }

  bool MCInteractionHolderMFVtbs::valid() const {
    return 
      MCInteractionHolderTtbar::valid() && 
      lsps[0].isNonnull() && stranges[0].isNonnull() && primary_bottoms[0].isNonnull() &&
      lsps[1].isNonnull() && stranges[1].isNonnull() && primary_bottoms[1].isNonnull();
  }

  bool MCInteractionHolderThruple::valid() const {
    return
      p[0].isNonnull() && s[0][0].isNonnull() && s[0][1].isNonnull() && s[0][2].isNonnull() &&
      p[1].isNonnull() && s[1][0].isNonnull() && s[1][1].isNonnull() && s[1][2].isNonnull();
  }

  bool MCInteractionHolderPair::valid() const {
    return
      p[0].isNonnull() &&
      p[1].isNonnull() &&
      s[0][0].isNonnull() &&
      s[0][1].isNonnull() &&
      s[1][0].isNonnull() &&
      s[1][1].isNonnull();
  }

  ////

  void MCInteraction::check_empty_() const {
    assert(type_ == mci_invalid);
    assert(primaries_.empty());
    assert(secondaries_.empty());
    assert(indices_.empty());
  }

  void MCInteraction::set(const MCInteractionHolderTtbar& h) {
    check_empty_();

    type_ = mci_Ttbar;
    primaries_ = { h.tops[0], h.tops[1] };
    secondaries_ = { h.bottoms[0], h.Ws[0], h.W_daughters[0][0], h.W_daughters[0][1],
                     h.bottoms[1], h.Ws[1], h.W_daughters[1][0], h.W_daughters[1][1] };
    indices_ = { 0, 4, 8 };

    num_leptonic_ = h.num_leptonic;
    decay_type_ = { h.decay_type[0], h.decay_type[1] };
  }

  void MCInteraction::set(const MCInteractionHolderMFVtbs& h, int type) {
    check_empty_();

    type_ = type;
    primaries_ = { h.lsps[0], h.lsps[1] };
    secondaries_ = { h.stranges[0], h.primary_bottoms[0], h.tops[0], h.bottoms[0], h.Ws[0], h.W_daughters[0][0], h.W_daughters[0][1],
                     h.stranges[1], h.primary_bottoms[1], h.tops[1], h.bottoms[1], h.Ws[1], h.W_daughters[1][0], h.W_daughters[1][1] };
    indices_ = { 0, 7, 14 };

    num_leptonic_ = h.num_leptonic;
    decay_type_ = { h.decay_type[0], h.decay_type[1] };
  }

  MCInteraction::GenRef MCInteraction::lsp           (size_t i) const { return primaries_  .at(i); }
  MCInteraction::GenRef MCInteraction::strange       (size_t i) const { return secondaries_.at(indices_[i]);   }
  MCInteraction::GenRef MCInteraction::primary_bottom(size_t i) const { return secondaries_.at(indices_[i]+1); }

  MCInteraction::GenRef MCInteraction::top(size_t i) const {
    if (type_ == mci_Ttbar)
      return primaries_.at(i);
    else
      return secondaries_.at(indices_[i]+2);
  }
    
  MCInteraction::GenRef MCInteraction::bottom    (size_t i)           const { return secondaries_.at(indices_[i] + (type_ == mci_MFVtbs) * 3); }
  MCInteraction::GenRef MCInteraction::W         (size_t i)           const { return secondaries_.at(indices_[i] + (type_ == mci_MFVtbs) * 3 + 1); }
  MCInteraction::GenRef MCInteraction::W_daughter(size_t i, size_t j) const { return secondaries_.at(indices_[i] + (type_ == mci_MFVtbs) * 3 + 2 + j); }

  void MCInteraction::set(const MCInteractionHolderThruple& h, int type) {
    check_empty_();

    type_ = type;
    primaries_ = { h.p[0], h.p[1] };
    secondaries_ = { h.s[0][0], h.s[0][1], h.s[0][2],
                     h.s[1][0], h.s[1][1], h.s[1][2]  };
    indices_ = { 0, 3, 6 };

    num_leptonic_ = -1;
    decay_type_ = { 0, 0 };
  }

  MCInteraction::GenRef MCInteraction::up  (size_t i) const { return secondaries_.at(indices_[i] + 1 ); }
  MCInteraction::GenRef MCInteraction::down(size_t i) const { return secondaries_.at(indices_[i] + 2 ); }

  void MCInteraction::set(const MCInteractionHolderPair& h, int type) {
    check_empty_();

    type_ = type;

    primaries_ = { h.p[0], h.p[1] };
    secondaries_ = { h.s[0][0], h.s[0][1],
                     h.s[1][0], h.s[1][1] };
    indices_ = { 0, 2, 4 };

    num_leptonic_ = -1;
    decay_type_ = { h.decay_id[0], h.decay_id[1] };
  }

  void MCInteraction::set(const MCInteractionHolderXX4j& h)     { set(h, mci_XX4j);     }
  void MCInteraction::set(const MCInteractionHolderMFVddbar& h) { set(h, mci_MFVddbar); }
  void MCInteraction::set(const MCInteractionHolderMFVlq& h)    { set(h, mci_MFVlq);    }

  ////

  MCInteraction::GenRefs MCInteraction::secondaries(int which) const {
    if (which == -1 || which >= int(primaries_.size()))
      return secondaries_;

    MCInteraction::GenRefs v;
    for (size_t i = indices_[which]; i < indices_[which+1]; ++i)
      v.push_back(secondaries_[i]);
    return v;
  }

  MCInteraction::GenRefs MCInteraction::visible(int which) const {
    MCInteraction::GenRefs v;
    int b, e;
    if (which == -1 || which >= int(primaries_.size())) {
      b = 0;
      e = int(secondaries_.size());
    }
    else {
      b = indices_[which];
      e = indices_[which+1];
    }

    for (int i = b; i < e; ++i) {
      GenRef x = secondaries_[i];
      const int aid = abs(x->pdgId());
      if ((1 <= aid && aid <= 5) || aid == 11 || aid == 13 || aid == 15)
        v.push_back(x);
    }
    return v;
  }

  MCInteraction::GenRefs MCInteraction::light_leptons(int which) const {
    MCInteraction::GenRefs v;
    int b, e;
    if (which == -1 || which >= int(primaries_.size())) {
      b = 0;
      e = int(secondaries_.size());
    }
    else {
      b = indices_[which];
      e = indices_[which+1];
    }
      
    for (int i = b; i < e; ++i) {
      GenRef x = secondaries_[i];
      const int aid = abs(x->pdgId());
      if (aid == 11 || aid == 13)
        v.push_back(x);
    }
    return v;
  }
  
  MCInteraction::Point MCInteraction::decay_point(size_t i) const {
    MCInteraction::Point p;
    p.x = secondaries_[indices_[i]]->vx();
    p.y = secondaries_[indices_[i]]->vy();
    p.z = secondaries_[indices_[i]]->vz();
    return p;
  }


  bool MCInteraction::isBhadron(int pdgID) const {
	  return (int(abs(pdgID) / 100) % 10) == 5 || (int(abs(pdgID) / 1000) % 10) == 5;
  }
  bool MCInteraction::isBquark(int pdgID) const {
	  return fabs(pdgID) == 5;
  }
  bool MCInteraction::isValidLeptonic(const reco:: GenParticle* parent, int pdgID) const {
	  bool found_lepton_pair = false;			// this is a photon radiated from a b-quark to l-l+ and two neutrinos 
	  for (size_t i = 0, ie = parent->numberOfDaughters(); i < ie; ++i) {
		  const reco::GenParticle* dau = (reco::GenParticle*) parent->daughter(i);
		  if (pdgID == -1 * dau->pdgId() && (abs(pdgID) == 11 || abs(pdgID) == 13 || abs(pdgID) == 15))
			  found_lepton_pair = true;
	  }
	  return !found_lepton_pair;
  }
  bool MCInteraction::isBvtx(const reco::GenParticle* parent, int pdgID, double dist3d, std::vector<int> vec_pdgID) const {
	  for (size_t i = 0, ie = vec_pdgID.size() - 1; i < ie; ++i) {
		  if (!(isBhadron(abs(vec_pdgID[i])) == true  	  // the chain of b-hadrons
			  || isBquark(abs(vec_pdgID[i])) == true
			  || (i < vec_pdgID.size() - 2 && vec_pdgID[i] == 21 && isBhadron(abs(vec_pdgID[i + 1])) == true)))	// allow gluons to b-mesons 
			  return false;

	  }

	 
	  return dist3d > 0 && isValidLeptonic(parent, pdgID);
  }

  size_t MCInteraction::mindR_dau(int& nth_chain, const reco::GenParticle* parent, std::vector<size_t> & excl_idx_first_dRmin, std::vector<size_t> & excl_idx_second_dRmin) const {

	  double mindR = 200;
	  size_t idx_mindR = 0;
	  for (size_t i = 0, ie = parent->numberOfDaughters(); i < ie; ++i) {


		  if (nth_chain == 1 && std::count(excl_idx_first_dRmin.begin(), excl_idx_first_dRmin.end(), i) == 1)
			  continue;

		  if (nth_chain == 2 && std::count(excl_idx_second_dRmin.begin(), excl_idx_second_dRmin.end(), i) == 1)
			  continue;

		  const reco::GenParticle* dau = (const reco::GenParticle*) parent->daughter(i);
		  
		  double dau_dR = reco::deltaR(dau->eta(), dau->phi(), parent->eta(), parent->phi());
		  if (dau_dR < mindR) {
			  mindR = dau_dR;
			  idx_mindR = i;
		  }
	  }
	  return idx_mindR;
  }

  bool MCInteraction::Is_bdecay_done(int& nth_chain, const reco::GenParticle* bquark, const reco::GenParticle* parent, std::vector<int> & vec_pdgID, std::vector<double> & vec_decay, std::vector<std::vector<const reco::GenParticle*>> & vec_of_vec_nonb_p, std::vector<const reco::GenParticle*>& vec_b_p, std::vector<size_t> & excl_idx_first_dRmin, std::vector<size_t> & excl_idx_second_dRmin) const {


	  for (size_t i = 0, ie = parent->numberOfDaughters(); i < ie; ++i) {
		  // gdau stage
		  if (nth_chain == 2 && excl_idx_second_dRmin.size() == parent->numberOfDaughters())
			  break;

		  if (nth_chain == 1 || nth_chain == 2) {
			  if (i != mindR_dau(nth_chain, parent, excl_idx_first_dRmin, excl_idx_second_dRmin))
				  continue;
		  }
		  if (nth_chain == 1 && std::count(excl_idx_first_dRmin.begin(), excl_idx_first_dRmin.end(), i) == 0) {
			  excl_idx_first_dRmin.push_back(i);
			  excl_idx_second_dRmin = {};
		  }
		  if (nth_chain == 2 && std::count(excl_idx_second_dRmin.begin(), excl_idx_second_dRmin.end(), i) == 0) {
			  excl_idx_second_dRmin.push_back(i);
		  }

		  const reco::GenParticle* dau = (const reco::GenParticle*) parent->daughter(i);

		  int dau_pdgID = dau->pdgId();
		  double dau_dist3d = sqrt(pow(dau->vx() - bquark->vx(), 2) + pow(dau->vy() - bquark->vy(), 2) + pow(dau->vz() - bquark->vz(), 2));
		  vec_pdgID.push_back(dau_pdgID);
		  if (isBhadron(dau_pdgID)) {
			  if (isBvtx(parent, dau_pdgID, dau_dist3d, vec_pdgID)) {
				  vec_decay.push_back(dau_dist3d);
				  break;
			  }
		  }
		  else {
			  if (!isBquark(dau_pdgID)) {
				  if (isBvtx(parent, dau_pdgID, dau_dist3d, vec_pdgID)) {
					  std::vector <const reco::GenParticle*> vec_nonb_p = {};
					  for (size_t j = 0, je = parent->numberOfDaughters(); j < je; ++j) {
						  const reco::GenParticle* idau = (const reco::GenParticle*) parent->daughter(j);
						  vec_nonb_p.push_back(idau);
					  }
					  vec_of_vec_nonb_p.push_back(vec_nonb_p);
					  vec_b_p.push_back(parent);
					  vec_decay.push_back(dau_dist3d);
					  break;
				  }
			  }
		  }

		  nth_chain += 1;
		  return Is_bdecay_done(nth_chain, bquark, dau, vec_pdgID, vec_decay, vec_of_vec_nonb_p, vec_b_p, excl_idx_first_dRmin, excl_idx_second_dRmin);
	  }
	  return true;
  }


  std::vector < std::vector <const reco::GenParticle*>> MCInteraction::set_bdecay_hadron_chain() const{
	  std::vector < std::vector <const reco::GenParticle*>> vec_of_vec_c_nonb_had_gen_particle = {};
	  std::vector <const reco::GenParticle*> vec_c_b_had_gen_particle = {};
	  std::vector < std::vector <const reco::GenParticle*>> vec_c_chain_had_gen_particle = {};
	  std::vector<double> vec_c_nonb_decay = {};

	  if (primaries_.size() == 2 and secondaries_.size() == 4) {
			  size_t nth_bquark = 0;
			  for (auto genref_p : secondaries_) {
				  nth_bquark += 1;
				  bool catch_b_vtx = false;
				  std::vector<int> vec_dau_pdgID = {};
				  std::vector<size_t> excl_idx_first_dRmin = {};
				  std::vector<size_t> excl_idx_second_dRmin = {};
				  int nth_chain = 1;
				  const reco::GenParticle* p = genref_p.get();
				  if (p->numberOfDaughters() == 0)
					  continue;
				  int count_while_1 = 0;
				  int count_while_2 = 0;
				  while (!catch_b_vtx || (vec_c_nonb_decay.size() != nth_bquark || (vec_c_nonb_decay.size() == nth_bquark && std::count(vec_c_nonb_decay.begin(), vec_c_nonb_decay.end(), vec_c_nonb_decay[nth_bquark - 1]) > 1))) {

					  size_t num_daus = p->numberOfDaughters();

					  if (excl_idx_first_dRmin.size() == num_daus) {
						  break;
					  }

					  if (vec_c_nonb_decay.size() == nth_bquark && std::count(vec_c_nonb_decay.begin(), vec_c_nonb_decay.end(), vec_c_nonb_decay[nth_bquark - 1]) > 1) {
						  vec_of_vec_c_nonb_had_gen_particle.pop_back();
						  vec_c_b_had_gen_particle.pop_back();
						  vec_c_nonb_decay.pop_back();
					  }

					  if (nth_chain == 1 || (excl_idx_first_dRmin.size() > 0 && excl_idx_second_dRmin.size() == p->daughter(excl_idx_first_dRmin[excl_idx_first_dRmin.size() - 1])->numberOfDaughters())) {
						  count_while_1 += 1;

						  vec_dau_pdgID = {};
						  nth_chain = 1;
						  catch_b_vtx = Is_bdecay_done(nth_chain, p, p, vec_dau_pdgID, vec_c_nonb_decay, vec_of_vec_c_nonb_had_gen_particle, vec_c_b_had_gen_particle, excl_idx_first_dRmin, excl_idx_second_dRmin);
					  }
					  else {
						  count_while_2 += 1;
						  size_t idx_first_chain = excl_idx_first_dRmin[excl_idx_first_dRmin.size() - 1];
						  while (vec_dau_pdgID.size() != 1)
							  vec_dau_pdgID.pop_back();
						  nth_chain = 2;
						  catch_b_vtx = Is_bdecay_done(nth_chain, p, (const reco::GenParticle*) p->daughter(idx_first_chain), vec_dau_pdgID, vec_c_nonb_decay, vec_of_vec_c_nonb_had_gen_particle, vec_c_b_had_gen_particle, excl_idx_first_dRmin, excl_idx_second_dRmin);

					  }

					  if (count_while_1 == 10 || count_while_2 == 10) {
						  std::cout << "STUCK:" << " 2 " << count_while_2 << " 1 " << count_while_1 << std::endl;
						  std::cout << "nth b-quark : " << nth_bquark << " b-vertices : " << vec_c_nonb_decay.size() << std::endl;
						  int n = int(vec_c_nonb_decay.size()) - 1;
						  std::cout << "so far we have..." << std::endl;
						  while (!(n < 0)) {
							  std::cout << n << "th b-quark displ (cm) " << vec_c_nonb_decay[n] << std::endl;
							  n--;
						  }
						  std::cout << "1th chain exclusion size : " << excl_idx_first_dRmin.size() << " is equal to # of b-quark's daus ?" << num_daus << std::endl;
						  std::cout << "the current chain is down to " << nth_chain << std::endl;
						  std::cout << "so as its history size " << vec_dau_pdgID.size() << std::endl;
						  std::cout << "with its 2th chain exclusion size : " << excl_idx_second_dRmin.size() << std::endl;
						  if (excl_idx_first_dRmin.size() != 0)
							  std::cout << "hopefully the 2nd is not yet equal to # of b-quark's gdaus" << p->daughter(excl_idx_first_dRmin[excl_idx_first_dRmin.size() - 1])->numberOfDaughters() << std::endl;

						  break;
					  }

				  }

			  }
	  }
	  if (vec_c_nonb_decay.size() == 4) {
		  for (size_t i = 0, ie = vec_c_b_had_gen_particle.size(); i < ie; ++i) {
			  std::vector <const reco::GenParticle*> vec_c_chain_had_per_b = {};
			  vec_c_chain_had_per_b.push_back(vec_c_b_had_gen_particle[i]);
			  for (size_t j = 0, je = vec_of_vec_c_nonb_had_gen_particle[i].size(); j < je; ++j) {
				  vec_c_chain_had_per_b.push_back(vec_of_vec_c_nonb_had_gen_particle[i][j]);
			  }
			  vec_c_chain_had_gen_particle.push_back(vec_c_chain_had_per_b);
		  }
	  }

	  return vec_c_chain_had_gen_particle;
  }
  
  std::vector < MCInteraction::Point> MCInteraction::b_llp0_decay_points() const {
	  
	  std::vector<MCInteraction::Point > vec_c_mcp = {};
	  std::vector < std::vector <const reco::GenParticle*>> hadron_chains = set_bdecay_hadron_chain();
	  if (hadron_chains.size() == 4) {
		  if (primaries_.size() == 2 and secondaries_.size() == 4) {
			  size_t nth_bquark = 0;
			  for (auto p : secondaries_) {
				  MCInteraction::Point dau_p;
				  nth_bquark += 1;
				  if (p->numberOfDaughters() == 0 || nth_bquark == 3 || nth_bquark == 4)
					  continue;
				  dau_p.x = hadron_chains[nth_bquark - 1][1]->vx();
				  dau_p.y = hadron_chains[nth_bquark - 1][1]->vy();
				  dau_p.z = hadron_chains[nth_bquark - 1][1]->vz();
				  vec_c_mcp.push_back(dau_p);
			  }
		  }
	  }
	  return vec_c_mcp;

  }

  std::vector < MCInteraction::Point> MCInteraction::b_llp1_decay_points() const {	
	  std::vector<MCInteraction::Point> vec_c_mcp = {};
	  std::vector < std::vector <const reco::GenParticle*>> hadron_chains = set_bdecay_hadron_chain();
	  if (hadron_chains.size() == 4) {
		  if (primaries_.size() == 2 and secondaries_.size() == 4) {
			  size_t nth_bquark = 0;
			  for (auto p : secondaries_) {
				  MCInteraction::Point dau_p;
				  nth_bquark += 1;
				  if (p->numberOfDaughters() == 0 || nth_bquark == 1 || nth_bquark == 2)
					  continue;
				  dau_p.x = hadron_chains[nth_bquark - 1][1]->vx();
				  dau_p.y = hadron_chains[nth_bquark - 1][1]->vy();
				  dau_p.z = hadron_chains[nth_bquark - 1][1]->vz();
				  vec_c_mcp.push_back(dau_p);
			  }
		  }
	  }
	  return vec_c_mcp;

  }
  
  double MCInteraction::dvv() const {
    auto p0 = decay_point(0);
    auto p1 = decay_point(1);
    return sqrt(pow(p0.x - p1.x, 2) + 
                pow(p0.y - p1.y, 2));
  }

  double MCInteraction::d3d() const {
    auto p0 = decay_point(0);
    auto p1 = decay_point(1);
    return sqrt(pow(p0.x - p1.x, 2) + 
                pow(p0.y - p1.y, 2) +
                pow(p0.z - p1.z, 2));
  }
}
////


std::ostream& operator<<(std::ostream& o, const mfv::MCInteraction& x) {
  using std::setw;
  using std::setprecision;
  auto printit = [&o](const reco::GenParticleRef& p) {
    std::streamsize prec = o.precision();
    o << "key " << setw(5) << p.key() << " id " << setw(10) << p->pdgId() << " pt " << setw(7) << setprecision(1) << p->pt() << " eta " << setw(6) << setprecision(2) << p->eta() << " phi " << setw(6) << setprecision(2) << p->phi() << " mass " << setw(7) << setprecision(1) << p->mass();
    o.precision(prec);
    o << " mother ids: ";
    if (p->numberOfMothers() == 0) o << " none ";
    else for (size_t i = 0, ie = p->numberOfMothers(); i < ie; ++i)
           o << " " << p->mother(i)->pdgId();
    o << " daughter ids: ";
    if (p->numberOfDaughters() == 0) o << " none ";
    else for (size_t i = 0, ie = p->numberOfDaughters(); i < ie; ++i)
           o << " " << p->daughter(i)->pdgId();
    o << "\n";
  };

  o << "MCInteraction: type " << x.type() << " valid? " << x.valid() << "\n";

  if (x.valid()) {
    o << "# primaries: " << x.primaries().size() << "\n";
    for (auto p : x.primaries())   { o << "  "; printit(p); }
    o << "# secondaries: " << x.secondaries().size() << "\n";
    for (auto p : x.secondaries()) { o << "  "; printit(p); }

    if (x.type() == mfv::mci_MFVtbs || x.type() == mfv::mci_Ttbar) {
      for (int i = 0; i < 2; ++i) {
        if (x.type() == mfv::mci_MFVtbs) {
          o << "lsp #" << i << "        : ";
          printit(x.lsp(i));
          o << "      strange: ";
          printit(x.strange(i));
          o << "  pri. bottom: ";
          printit(x.primary_bottom(i));
          o << "          ";
        }
        o << "top";
        if (x.type() == mfv::mci_Ttbar)
          o << " #" << i;
        o << ": ";
        printit(x.top(i));
        o << "       bottom: ";
        printit(x.bottom(i));
        o << "            W: ";
        printit(x.W(i));
        for (int j = 0; j < 2; ++j) {
          o << "W daughter #" << j << ": ";
          printit(x.W_daughter(i, j));
        }
      } 
    }
  }

  return o;
}



#if 0

std::ostream& operator<<(std::ostream& o, const MCInteractionTtbar& x) {
  if (!x.valid())
    o << "not valid\n";
  else {
#if 0
    printf("num_leptons: %i\n", num_leptonic);
    const char* decay_types[4] = {"e", "mu", "tau", "h"};
    printf("decay type: W+ -> %s,  W- -> %s\n", decay_types[decay_plus], decay_types[decay_minus]);
    print_gen_and_daus(0,                       "header",                  *gen_particles);
    print_gen_and_daus(tops[0],                     "top",                     *gen_particles);
    print_gen_and_daus(tops[1],                  "topbar",                  *gen_particles);
    print_gen_and_daus(Ws[0],                   "Wplus",                   *gen_particles);
    print_gen_and_daus(Ws[1],                  "Wminus",                  *gen_particles);
    print_gen_and_daus(bottoms[0],                  "bottom",                  *gen_particles);
    print_gen_and_daus(bottoms[1],               "bottombar",               *gen_particles);
    print_gen_and_daus(W_daughters[0][0],       "Wplus daughter 0",        *gen_particles);
    print_gen_and_daus(W_daughters[0][1],       "Wplus daughter 1",        *gen_particles);
    print_gen_and_daus(W_daughters[1][0],       "Wminus daughter 0",       *gen_particles);
    print_gen_and_daus(W_daughters[1][1],       "Wminus daughter 1",       *gen_particles);
#endif
  }
  return o;
}

std::ostream& operator<<(std::ostream& o, const MCInteractionTtbar& x) {
  if (!x.valid())
    o << "not valid\n";
  else {
#if 0
    printf("num_leptons: %i\n", num_leptonic);
    const char* decay_types[4] = {"e", "mu", "tau", "h"};
    printf("decay type: Ws[0] -> %s,  Ws[1] -> %s\n", decay_types[decay_type[0]], decay_types[decay_type[1]]);
    print_gen_and_daus(0,                      "header",                  *gen_particles, true, true);
    print_gen_and_daus(lsps[0],                "lsps[0]",                 *gen_particles, true, true);
    print_gen_and_daus(lsps[1],                "lsps[1]",                 *gen_particles, true, true);
    print_gen_and_daus(stranges[0],            "stranges[0]",             *gen_particles, true, true);
    print_gen_and_daus(stranges[1],            "stranges[1]",             *gen_particles, true, true);
    print_gen_and_daus(bottoms[0],             "bottoms[0]",              *gen_particles, true, true);
    print_gen_and_daus(bottoms[1],             "bottoms[1]",              *gen_particles, true, true);
    print_gen_and_daus(tops[0],                "tops[0]",                 *gen_particles, true, true);
    print_gen_and_daus(tops[1],                "tops[1]",                 *gen_particles, true, true);
    print_gen_and_daus(Ws[0],                  "Ws[0]",                   *gen_particles, true, true);
    print_gen_and_daus(Ws[1],                  "Ws[1]",                   *gen_particles, true, true);
    print_gen_and_daus(bottoms_from_tops[0],   "bottoms_from_tops[0]",    *gen_particles, true, true);
    if (abs(bottoms_from_tops[0]->pdgId()) != 5)
      printf("NB: this was not a bottom quark!\n");
    print_gen_and_daus(bottoms_from_tops[1],   "bottoms_from_tops[1]",    *gen_particles, true, true);
    if (abs(bottoms_from_tops[1]->pdgId()) != 5)
      printf("NB: this was not a bottom quark!\n");
    print_gen_and_daus(W_daughters[0][0],      "Wplus daughter 0",        *gen_particles, true, true);
    print_gen_and_daus(W_daughters[0][1],      "Wplus daughter 1",        *gen_particles, true, true);
    print_gen_and_daus(W_daughters[1][0],      "Wminus daughter 0",       *gen_particles, true, true);
    print_gen_and_daus(W_daughters[1][1],      "Wminus daughter 1",       *gen_particles, true, true);
    MCInteraction::Print(out);
#endif
  }
  return o;
}

std::ostream& operator<<(std::ostream& o, const MCInteractionPair& x) {
  if (!x.valid())
    o << "not valid\n";
  else {
#if 0
    print_gen_and_daus(0, "header", *gen_particles, true, true);
    print_gen_and_daus(hs[0], "hs[0]", *gen_particles, true, true);
    print_gen_and_daus(qs[0][0], "qs[0][0]", *gen_particles, true, true);
    print_gen_and_daus(qs[0][1], "qs[0][1]", *gen_particles, true, true);
    print_gen_and_daus(hs[1], "hs[1]", *gen_particles, true, true);
    print_gen_and_daus(qs[1][0], "qs[1][0]", *gen_particles, true, true);
    print_gen_and_daus(qs[1][1], "qs[1][1]", *gen_particles, true, true);
#endif
  }
  return o;
}
#endif
