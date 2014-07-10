#include "Templater.h"
#include "TF1.h"
#include "TFile.h"
#include "TFitResult.h"
#include "TH2D.h"
#include "TRandom3.h"
#include "TTree.h"
#include "Prob.h"
#include "ROOTTools.h"
#include "Random.h"
#include "Templates.h"

namespace mfv {
  Templater::Templater(const std::string& name_, TFile* f, TRandom* r)
    : name (name_.size() ? " " + name_ : ""),
      uname(name_.size() ? "_" + name_ : ""),

      fout(f),
      dout(0),
      dtoy(0),
      rand(r),
      seed(r->GetSeed() - jmt::seed_base),

      one_vertices(0),
      two_vertices(0)
  {
  }

  Templater::~Templater() {
    clear_templates();
  }

  void Templater::clear_templates() {
    for (Template* t : templates)
      delete t;
    templates.clear();
  }

  void Templater::process(int toy_, const VertexSimples* toy_1v, const VertexPairs* toy_2v) {
    // toy negative if data?
    toy = toy_;
    one_vertices = toy_1v;
    two_vertices = toy_2v;

    process_imp();
  }
}
