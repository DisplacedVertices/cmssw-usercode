#ifndef JMTucker_MFVNeutralino_plugins_VertexNtuple_h
#define JMTucker_MFVNeutralino_plugins_VertexNtuple_h

struct VertexNtuple {
  typedef unsigned short ushort;
  typedef unsigned int uint;

  uint run;
  uint lumi;
  uint event;
  float minlspdist2d;
  float lspdist2d;
  float lspdist3d;
  short pass_trigger;
  ushort npfjets;
  ushort ntightpfjets;
  float pfjetpt4;
  float pfjetpt5;
  float tightpfjetpt4;
  float tightpfjetpt5;
  ushort nsv;

  short isv;
  ushort ntracks;
  ushort ntracksptgt10;
  ushort ntracksptgt20;
  ushort trackminnhits;
  ushort trackmaxnhits;
  ushort njetssharetks;
  float jetsmass;
  float chi2dof;
  float chi2dofprob;
  float p;
  float pt;
  float eta;
  float rapidity;
  float phi;
  float mass;
  float costhmombs;
  float costhmompv2d;
  float costhmompv3d;
  float sumpt2;
  ushort sumnhitsbehind;
  ushort maxnhitsbehind;
  float mintrackpt;
  float maxtrackpt;
  float maxm1trackpt;
  float maxm2trackpt;
  float drmin;
  float drmax;
  float dravg;
  float drrms;
  float dravgw;
  float drrmsw;
  float gen2ddist;
  float gen2derr;
  float gen2dsig;
  float gen3ddist;
  float gen3derr;
  float gen3dsig;
  ushort bs2dcompatscss;
  float bs2dcompat;
  float bs2ddist;
  float bs2derr;
  float bs2dsig;
  float bs3ddist;
  ushort pv2dcompatscss;
  float pv2dcompat;
  float pv2ddist;
  float pv2derr;
  float pv2dsig;
  ushort pv3dcompatscss;
  float pv3dcompat;
  float pv3ddist;
  float pv3derr;
  float pv3dsig;

  void clear(bool all) {
    if (all) {
      run = -1; lumi = -1; event = -1; minlspdist2d = -1; lspdist2d = -1; lspdist3d = -1; pass_trigger = -1; npfjets = -1; ntightpfjets = -1; pfjetpt4 = -1; pfjetpt5 = -1; tightpfjetpt4 = -1; tightpfjetpt5 = -1; nsv = -1;
    }
    isv = -1; ntracks = -1; ntracksptgt10 = -1; ntracksptgt20 = -1; trackminnhits = -1; trackmaxnhits = -1; njetssharetks = -1; jetsmass = -1; chi2dof = -1; chi2dofprob = -1; p = -1; pt = -1; eta = -1; rapidity = -1; phi = -1; mass = -1; costhmombs = -1; costhmompv2d = -1; costhmompv3d = -1; sumpt2 = -1; sumnhitsbehind = -1; maxnhitsbehind = -1; mintrackpt = -1; maxtrackpt = -1; maxm1trackpt = -1; maxm2trackpt = -1; drmin = -1; drmax = -1; dravg = -1; drrms = -1; dravgw = -1; drrmsw = -1; gen2ddist = -1; gen2derr = -1; gen2dsig = -1; gen3ddist = -1; gen3derr = -1; gen3dsig = -1; bs2dcompatscss = -1; bs2dcompat = -1; bs2ddist = -1; bs2derr = -1; bs2dsig = -1; bs3ddist = -1; pv2dcompatscss = -1; pv2dcompat = -1; pv2ddist = -1; pv2derr = -1; pv2dsig = -1; pv3dcompatscss = -1; pv3dcompat = -1; pv3ddist = -1; pv3derr = -1; pv3dsig = -1;
  }

  void branch(TTree* tree) {
    tree->Branch("run", &run, "run/i");
    tree->Branch("lumi", &lumi, "lumi/i");
    tree->Branch("event", &event, "event/i");
    tree->Branch("minlspdist2d", &minlspdist2d, "minlspdist2d/F");
    tree->Branch("lspdist2d", &lspdist2d, "lspdist2d/F");
    tree->Branch("lspdist3d", &lspdist3d, "lspdist3d/F");
    tree->Branch("pass_trigger", &pass_trigger, "pass_trigger/S");
    tree->Branch("npfjets", &npfjets, "npfjets/s");
    tree->Branch("ntightpfjets", &ntightpfjets, "ntightpfjets/s");
    tree->Branch("pfjetpt4", &pfjetpt4, "pfjetpt4/F");
    tree->Branch("pfjetpt5", &pfjetpt5, "pfjetpt5/F");
    tree->Branch("tightpfjetpt4", &tightpfjetpt4, "tightpfjetpt4/F");
    tree->Branch("tightpfjetpt5", &tightpfjetpt5, "tightpfjetpt5/F");
    tree->Branch("nsv", &nsv, "nsv/s");
    tree->Branch("isv", &isv, "isv/S");
    tree->Branch("ntracks", &ntracks, "ntracks/s");
    tree->Branch("ntracksptgt10", &ntracksptgt10, "ntracksptgt10/s");
    tree->Branch("ntracksptgt20", &ntracksptgt20, "ntracksptgt20/s");
    tree->Branch("trackminnhits", &trackminnhits, "trackminnhits/s");
    tree->Branch("trackmaxnhits", &trackmaxnhits, "trackmaxnhits/s");
    tree->Branch("njetssharetks", &njetssharetks, "njetssharetks/s");
    tree->Branch("jetsmass", &jetsmass, "jetsmass/s");
    tree->Branch("chi2dof", &chi2dof, "chi2dof/F");
    tree->Branch("chi2dofprob", &chi2dofprob, "chi2dofprob/F");
    tree->Branch("p", &pt, "p/F");
    tree->Branch("pt", &pt, "pt/F");
    tree->Branch("eta", &eta, "eta/F");
    tree->Branch("rapidity", &rapidity, "rapidity/F");
    tree->Branch("phi", &phi, "phi/F");
    tree->Branch("mass", &mass, "mass/F");
    tree->Branch("costhmombs", &costhmombs, "costhmombs/F");
    tree->Branch("costhmompv2d", &costhmompv2d, "costhmompv2d/F");
    tree->Branch("costhmompv3d", &costhmompv3d, "costhmompv3d/F");
    tree->Branch("sumpt2", &sumpt2, "sumpt2/F");
    tree->Branch("sumnhitsbehind", &sumnhitsbehind, "sumnhitsbehind/s");
    tree->Branch("maxnhitsbehind", &maxnhitsbehind, "maxnhitsbehind/s");
    tree->Branch("mintrackpt", &mintrackpt, "mintrackpt/F");
    tree->Branch("maxtrackpt", &maxtrackpt, "maxtrackpt/F");
    tree->Branch("maxm1trackpt", &maxm1trackpt, "maxm1trackpt/F");
    tree->Branch("maxm2trackpt", &maxm2trackpt, "maxm2trackpt/F");
    tree->Branch("drmin", &drmin, "drmin/F");
    tree->Branch("drmax", &drmax, "drmax/F");
    tree->Branch("dravg", &dravg, "dravg/F");
    tree->Branch("drrms", &drrms, "drrms/F");
    tree->Branch("dravgw", &dravgw, "dravgw/F");
    tree->Branch("drrmsw", &drrmsw, "drrmsw/F");
    tree->Branch("gen2ddist", &gen2ddist, "gen2ddist/F");
    tree->Branch("gen2derr", &gen2derr, "gen2derr/F");
    tree->Branch("gen2dsig", &gen2dsig, "gen2dsig/F");
    tree->Branch("gen3ddist", &gen3ddist, "gen3ddist/F");
    tree->Branch("gen3derr", &gen3derr, "gen3derr/F");
    tree->Branch("gen3dsig", &gen3dsig, "gen3dsig/F");
    tree->Branch("bs2dcompatscss", &bs2dcompatscss, "bs2dcompatscss/s");
    tree->Branch("bs2dcompat", &bs2dcompat, "bs2dcompat/F");
    tree->Branch("bs2ddist", &bs2ddist, "bs2ddist/F");
    tree->Branch("bs2derr", &bs2derr, "bs2derr/F");
    tree->Branch("bs2dsig", &bs2dsig, "bs2dsig/F");
    tree->Branch("bs3ddist", &bs3ddist, "bs3ddist/F");
    tree->Branch("pv2dcompatscss", &pv2dcompatscss, "pv2dcompatscss/s");
    tree->Branch("pv2dcompat", &pv2dcompat, "pv2dcompat/F");
    tree->Branch("pv2ddist", &pv2ddist, "pv2ddist/F");
    tree->Branch("pv2derr", &pv2derr, "pv2derr/F");
    tree->Branch("pv2dsig", &pv2dsig, "pv2dsig/F");
    tree->Branch("pv3dcompatscss", &pv3dcompatscss, "pv3dcompatscss/s");
    tree->Branch("pv3dcompat", &pv3dcompat, "pv3dcompat/F");
    tree->Branch("pv3ddist", &pv3ddist, "pv3ddist/F");
    tree->Branch("pv3derr", &pv3derr, "pv3derr/F");
    tree->Branch("pv3dsig", &pv3dsig, "pv3dsig/F");
  }
};

#endif
