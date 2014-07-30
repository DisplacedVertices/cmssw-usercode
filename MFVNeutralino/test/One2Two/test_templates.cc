#include "TH1.h"
#include "TFile.h"
#include "TRandom3.h"

#include "Random.h"
#include "ROOTTools.h"

#include "ToyThrower.h"
#include "Templates.h"
#include "ClearedJetsTemplater.h"

int main() {
  jmt::set_root_style();

  TFile* out_f = new TFile("test_templates.root", "recreate");
  TRandom3* rand = new TRandom3(jmt::seed_base);
  mfv::ToyThrower* tt = new mfv::ToyThrower("", "jen_crab", out_f, rand);
  mfv::Templater* ter = new mfv::ClearedJetsTemplater("", out_f, rand);

  tt->throw_toy();
  ter->process(tt->toy_dataset);

  std::vector<double> a_bkg;
  mfv::TemplateInterpolator* interp = new mfv::TemplateInterpolator(ter->get_templates(), mfv::Template::binning().size(), ter->par_info(), a_bkg);

  mfv::Templates* ts = ter->get_templates();
  for (int i = 0; i < 4; ++i) {
    mfv::Template* t = (*ts)[i];
    printf("%s\n", t->title().c_str());
    for (int j = 0; j < t->h->GetNbinsX()+2; ++j)
      printf("  %2i: %f\n", j, t->h->GetBinContent(j));
    printf("\n");
  }

  printf("\n");

  double z[5][2] = {
    { 0, 0.0005 },
    { 0, 0.001 },
    { 0.001, 0.0005 },
    { 0.001, 0.001 },
    { 0.0005, 0.00075 }
  };

  for (auto x : z) {
    interp->interpolate(x[0], x[1]);
    printf("interpolate %f, %f:\n", x[0], x[1]);
    for (int i = 0; i < int(a_bkg.size()); ++i)
      printf("  %2i: %f\n", i, a_bkg[i]);
    printf("\n");
  }
  
  out_f->Write();
  out_f->Close();
  delete out_f;
  delete tt;
}
