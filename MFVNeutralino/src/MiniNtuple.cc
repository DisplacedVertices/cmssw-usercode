#include "TFile.h"
#include "TTree.h"
#include "TH1F.h"
#include "JMTucker/MFVNeutralino/interface/MiniNtuple.h"
#include "JMTucker/MFVNeutralinoFormats/interface/TriggerEnum.h"
#include "JMTucker/Tools/interface/Year.h"

namespace mfv {
  MiniNtuple::MiniNtuple() {
    clear();
    p_tk0_qchi2 = p_tk0_ndof = p_tk0_vx = p_tk0_vy = p_tk0_vz = p_tk0_px = p_tk0_py = p_tk0_pz = p_tk1_qchi2 = p_tk1_ndof = p_tk1_vx = p_tk1_vy = p_tk1_vz = p_tk1_px = p_tk1_py = p_tk1_pz = 0;
    p_tk0_inpv = p_tk1_inpv = 0;
    p_tk0_cov = p_tk1_cov = 0;
    p_gen_daughters = p_gen_bquarks = p_gen_leptons = 0;
    p_gen_daughter_id = 0;
    p_misc_weights = 0;
  }

  void MiniNtuple::clear() {
    run = lumi = 0;
    event = 0;
    gen_flavor_code = pass_hlt = npv = npu = njets = nvtx = ntk0 = ntk1 = 0;
    l1_htt = l1_myhtt = l1_myhttwbug = hlt_ht = bsx = bsy = bsz = bsdxdz = bsdydz = pvx = pvy = pvz = weight = ren_weight_up = ren_weight_dn = fac_weight_up = fac_weight_dn = x0 = y0 = z0 = bs2derr0 = rescale_bs2derr0 = x1 = y1 = z1 = bs2derr1 = rescale_bs2derr1 = met = 0;
    genmatch0 = genmatch1 = 0;
    gen_pv_x0 = 0;
    gen_pv_y0 = 0;
    gen_pv_z0 = 0;
    for (int i = 0; i < 2; ++i)
      gen_x[i] = gen_y[i] = gen_z[i] = gen_lsp_pt[i] = gen_lsp_eta[i] = gen_lsp_phi[i] = gen_lsp_mass[i] = 0;
    gen_daughters.clear();
    gen_daughter_id.clear();
    gen_bquarks.clear();
    gen_leptons.clear();
    gen_jet_ht = gen_jet_ht40 = 0;
    for (int i = 0; i < 50; ++i) {
      jet_pt[i] = jet_eta[i] = jet_phi[i] = jet_energy[i] = jet_bdisc[i] = 0;
      jet_hlt_pt[i] = jet_hlt_eta[i] = jet_hlt_phi[i] = jet_hlt_energy[i] = 0;
      displaced_jet_hlt_pt[i] = displaced_jet_hlt_eta[i] = displaced_jet_hlt_phi[i] = displaced_jet_hlt_energy[i] = 0;
      jet_id[i] = 0;
    }
    tk0_qchi2.clear();
    tk0_ndof.clear();
    tk0_vx.clear();
    tk0_vy.clear();
    tk0_vz.clear();
    tk0_px.clear();
    tk0_py.clear();
    tk0_pz.clear();
    tk0_inpv.clear();
    tk0_cov.clear();
    tk1_qchi2.clear();
    tk1_ndof.clear();
    tk1_vx.clear();
    tk1_vy.clear();
    tk1_vz.clear();
    tk1_px.clear();
    tk1_py.clear();
    tk1_pz.clear();
    tk1_inpv.clear();
    tk1_cov.clear();
    misc_weights.clear();
  }

  float MiniNtuple::ht(float min_jet_pt) const {
    double sum = 0;
    for (int i = 0; i < njets; ++i)
      if (jet_pt[i] >= min_jet_pt)
        sum += jet_pt[i];
    return sum;
  }

  bool MiniNtuple::is_btagged(int i, float min_bdisc) const {
    return jet_bdisc[i] >= min_bdisc;
  }

  int MiniNtuple::nbtags_(float min_bdisc, bool old) const {
    int sum = 0;
    const float* bdisc = old ? jet_bdisc_old : jet_bdisc;
    for (int i = 0; i < njets; ++i)
      if (bdisc[i] >= min_bdisc)
        ++sum;
    return sum;
  }

  bool MiniNtuple::satisfiesTrigger(size_t trig) const {
    return bool((pass_hlt >> trig) & 1);
  }

  bool MiniNtuple::satisfiesTriggerAndOffline(size_t trig) const {
    if(!satisfiesTrigger(trig)) return false;

    // note that this could be loosened if desired
    int nbtaggedjets = nbtags_tight();

    // for the trigger chains where we need to do any detailed matching
    bool passed_kinematics = false;

    switch(trig){
      case b_HLT_PFHT1050 :
        return ht(40) >= 1200 && njets >= 4;
      case b_HLT_DoublePFJets100MaxDeta1p6_DoubleCaloBTagCSV_p33 :
      {
        if(njets < 4) return false;
        if(nbtaggedjets < 2) return false;

        for(int j0 = 0; j0 < njets; ++j0){
          if(!jet_hlt_match(j0) || jet_pt[j0] < 140) continue;

          for(int j1 = j0+1; j1 < njets; ++j1){
            if(!jet_hlt_match(j1) || jet_pt[j1] < 140) continue;

            if(fabs(jet_eta[j0] - jet_eta[j1]) < 1.6){
              passed_kinematics = true;
            }
          }
        }
        return passed_kinematics;
      }
      case b_HLT_PFHT300PT30_QuadPFJet_75_60_45_40_TriplePFBTagCSV_3p0 :
      {
        if(ht(30) < 450 || njets < 4) return false;
        if(nbtaggedjets < 3) return false;

        for(int j0 = 0; j0 < njets; ++j0){
          if(!jet_hlt_match(j0) || jet_pt[j0] < 115) continue;

          for(int j1 = j0+1; j1 < njets; ++j1){
            if(!jet_hlt_match(j1) || jet_pt[j1] < 100) continue;

            for(int j2 = j1+1; j2 < njets; ++j2){
              if(!jet_hlt_match(j2) || jet_pt[j2] < 85) continue;

              for(int j3 = j2+1; j3 < njets; ++j3){
                if(!jet_hlt_match(j3) || jet_pt[j3] < 80) continue;

                passed_kinematics = true;
              }
            }
          }
        }
        return passed_kinematics;
      }
      case b_HLT_PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2 :
      {
        if(ht(40) < 530 || njets < 6) return false;
        if(nbtaggedjets < 2) return false;

        for(int j0 = 0; j0 < njets; ++j0){
          if(!jet_hlt_match(j0) || jet_pt[j0] < 72) continue;

          for(int j1 = j0+1; j1 < njets; ++j1){
            if(!jet_hlt_match(j1) || jet_pt[j1] < 72) continue;

            for(int j2 = j1+1; j2 < njets; ++j2){
              if(!jet_hlt_match(j2) || jet_pt[j2] < 72) continue;

              for(int j3 = j2+1; j3 < njets; ++j3){
                if(!jet_hlt_match(j3) || jet_pt[j3] < 72) continue;

                for(int j4 = j3+1; j4 < njets; ++j4){
                  if(!jet_hlt_match(j4) || jet_pt[j4] < 72) continue;

                  for(int j5 = j4+1; j5 < njets; ++j5){
                    if(!jet_hlt_match(j5) || jet_pt[j5] < 72) continue;

                    passed_kinematics = true;
                  }
                }
              }
            }
          }
        }

        return passed_kinematics;
      }
      case b_HLT_PFHT380_SixPFJet32_DoublePFBTagCSV_2p2 :
      {
        if(ht(40) < 530 || njets < 6) return false;
        if(nbtaggedjets < 2) return false;

        for(int j0 = 0; j0 < njets; ++j0){
          if(!jet_hlt_match(j0) || jet_pt[j0] < 72) continue;

          for(int j1 = j0+1; j1 < njets; ++j1){
            if(!jet_hlt_match(j1) || jet_pt[j1] < 72) continue;

            for(int j2 = j1+1; j2 < njets; ++j2){
              if(!jet_hlt_match(j2) || jet_pt[j2] < 72) continue;

              for(int j3 = j2+1; j3 < njets; ++j3){
                if(!jet_hlt_match(j3) || jet_pt[j3] < 72) continue;

                for(int j4 = j3+1; j4 < njets; ++j4){
                  if(!jet_hlt_match(j4) || jet_pt[j4] < 72) continue;

                  for(int j5 = j4+1; j5 < njets; ++j5){
                    if(!jet_hlt_match(j5) || jet_pt[j5] < 72) continue;

                    passed_kinematics = true;
                  }
                }
              }
            }
          }
        }

        return passed_kinematics;
      }
      case b_HLT_PFHT430_SixPFJet40_PFBTagCSV_1p5 :
      {
        if(ht(40) < 580 || njets < 6) return false;
        if(nbtaggedjets < 1) return false;

        for(int j0 = 0; j0 < njets; ++j0){
          if(!jet_hlt_match(j0) || jet_pt[j0] < 80) continue;

          for(int j1 = j0+1; j1 < njets; ++j1){
            if(!jet_hlt_match(j1) || jet_pt[j1] < 80) continue;

            for(int j2 = j1+1; j2 < njets; ++j2){
              if(!jet_hlt_match(j2) || jet_pt[j2] < 80) continue;

              for(int j3 = j2+1; j3 < njets; ++j3){
                if(!jet_hlt_match(j3) || jet_pt[j3] < 80) continue;

                for(int j4 = j3+1; j4 < njets; ++j4){
                  if(!jet_hlt_match(j4) || jet_pt[j4] < 80) continue;

                  for(int j5 = j4+1; j5 < njets; ++j5){
                    if(!jet_hlt_match(j5) || jet_pt[j5] < 80) continue;

                    passed_kinematics = true;
                  }
                }
              }
            }
          }
        }

        return passed_kinematics;
      }
      case b_HLT_DoublePFJets116MaxDeta1p6_DoubleCaloBTagDeepCSV_p71 :
      {
        if(njets < 4) return false;
        if(nbtaggedjets < 2) return false;

        for(int j0 = 0; j0 < njets; ++j0){
          if(!jet_hlt_match(j0) || jet_pt[j0] < 156) continue;

          for(int j1 = j0+1; j1 < njets; ++j1){
            if(!jet_hlt_match(j1) || jet_pt[j1] < 156) continue;

            if(fabs(jet_eta[j0] - jet_eta[j1]) < 1.6){
              passed_kinematics = true;
            }
          }
        }
        return passed_kinematics;
      }
      case b_HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepCSV_4p5 :
      {
        if(ht(30) < 480 || njets < 4) return false;
        if(nbtaggedjets < 3) return false;

        for(int j0 = 0; j0 < njets; ++j0){
          if(!jet_hlt_match(j0) || jet_pt[j0] < 115) continue;

          for(int j1 = j0+1; j1 < njets; ++j1){
            if(!jet_hlt_match(j1) || jet_pt[j1] < 100) continue;

            for(int j2 = j1+1; j2 < njets; ++j2){
              if(!jet_hlt_match(j2) || jet_pt[j2] < 85) continue;

              for(int j3 = j2+1; j3 < njets; ++j3){
                if(!jet_hlt_match(j3) || jet_pt[j3] < 80) continue;

                passed_kinematics = true;
              }
            }
          }
        }
        return passed_kinematics;
      }
      case b_HLT_PFHT400_FivePFJet_100_100_60_30_30_DoublePFBTagDeepCSV_4p5 :
      {
        if(ht(40) < 550 || njets < 5) return false;
        if(nbtaggedjets < 2) return false;

        for(int j0 = 0; j0 < njets; ++j0){
          if(!jet_hlt_match(j0) || jet_pt[j0] < 140) continue;

          for(int j1 = j0+1; j1 < njets; ++j1){
            if(!jet_hlt_match(j1) || jet_pt[j1] < 140) continue;

            for(int j2 = j1+1; j2 < njets; ++j2){
              if(!jet_hlt_match(j2) || jet_pt[j2] < 100) continue;

              for(int j3 = j2+1; j3 < njets; ++j3){
                if(!jet_hlt_match(j3) || jet_pt[j3] < 70) continue;

                for(int j4 = j3+1; j4 < njets; ++j4){
                  if(!jet_hlt_match(j4) || jet_pt[j4] < 70) continue;

                  passed_kinematics = true;
                }
              }
            }
          }
        }
        return passed_kinematics;
      }
      case b_HLT_PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94 :
      {
        if(ht(40) < 150 || njets < 6) return false;
        if(nbtaggedjets < 2) return false;

        for(int j0 = 0; j0 < njets; ++j0){
          if(!jet_hlt_match(j0) || jet_pt[j0] < 72) continue;

          for(int j1 = j0+1; j1 < njets; ++j1){
            if(!jet_hlt_match(j1) || jet_pt[j1] < 72) continue;

            for(int j2 = j1+1; j2 < njets; ++j2){
              if(!jet_hlt_match(j2) || jet_pt[j2] < 72) continue;

              for(int j3 = j2+1; j3 < njets; ++j3){
                if(!jet_hlt_match(j3) || jet_pt[j3] < 72) continue;

                for(int j4 = j3+1; j4 < njets; ++j4){
                  if(!jet_hlt_match(j4) || jet_pt[j4] < 72) continue;

                  for(int j5 = j4+1; j5 < njets; ++j5){
                    if(!jet_hlt_match(j5) || jet_pt[j5] < 72) continue;

                    passed_kinematics = true;
                  }
                }
              }
            }
          }
        }
        return passed_kinematics;
      }
      case b_HLT_PFHT450_SixPFJet36_PFBTagDeepCSV_1p59 :
      {
        if(ht(40) < 600 || njets < 6) return false;
        if(nbtaggedjets < 1) return false;

        for(int j0 = 0; j0 < njets; ++j0){
          if(!jet_hlt_match(j0) || jet_pt[j0] < 76) continue;

          for(int j1 = j0+1; j1 < njets; ++j1){
            if(!jet_hlt_match(j1) || jet_pt[j1] < 76) continue;

            for(int j2 = j1+1; j2 < njets; ++j2){
              if(!jet_hlt_match(j2) || jet_pt[j2] < 76) continue;

              for(int j3 = j2+1; j3 < njets; ++j3){
                if(!jet_hlt_match(j3) || jet_pt[j3] < 76) continue;

                for(int j4 = j3+1; j4 < njets; ++j4){
                  if(!jet_hlt_match(j4) || jet_pt[j4] < 76) continue;

                  for(int j5 = j4+1; j5 < njets; ++j5){
                    if(!jet_hlt_match(j5) || jet_pt[j5] < 76) continue;

                    passed_kinematics = true;
                  }
                }
              }
            }
          }
        }
        return passed_kinematics;
      }
      case b_HLT_HT430_DisplacedDijet40_DisplacedTrack :
      {
        if(ht(40) < 580 || njets < 4) return false;

        for(int j0 = 0; j0 < njets; ++j0){
          if(!displaced_jet_hlt_match(j0) || jet_pt[j0] < 80) continue;

          for(int j1 = j0+1; j1 < njets; ++j1){
            if(!displaced_jet_hlt_match(j1) || jet_pt[j1] < 80) continue;
            passed_kinematics = true;
          }
        }
        return passed_kinematics;
      }
      case b_HLT_HT650_DisplacedDijet60_Inclusive :
      {
        if(ht(40) < 800 || njets < 4) return false;

        for(int j0 = 0; j0 < njets; ++j0){
          if(!displaced_jet_hlt_match(j0) || jet_pt[j0] < 100) continue;

          for(int j1 = j0+1; j1 < njets; ++j1){
            if(!displaced_jet_hlt_match(j1) || jet_pt[j1] < 100) continue;
            passed_kinematics = true;
          }
        }
        return passed_kinematics;
      }
      case b_HLT_PFMET120_PFMHT120_IDTight : 
      {
        //if((met) < 200 || njets < 2) return false;
        if ( njets < 2 ) return false;
        return true;
      }
      default :
      {
        throw std::invalid_argument(std::string(hlt_paths[trig]) + " not implemented in satisfiesTrigger");
      }
    }

    return false;
  }

  bool MiniNtuple::satisfiesHTOrBjetOrDisplacedDijetTrigger() const {
    bool at_least_one_trigger_passed = false;
    for(size_t trig : HTOrBjetOrDisplacedDijetTriggers){
      if(satisfiesTrigger(trig)){
        at_least_one_trigger_passed = true;
        break;
      }
    }
    return at_least_one_trigger_passed;
  }

  bool MiniNtuple::satisfiesHTOrBjetOrDisplacedDijetTriggerAndOffline() const {
    bool at_least_one_trigger_passed = false;
    for(size_t trig : HTOrBjetOrDisplacedDijetTriggers){
      if(satisfiesTriggerAndOffline(trig)){
        at_least_one_trigger_passed = true;
        break;
      }
    }
    return at_least_one_trigger_passed;
  }

  void write_to_tree(TTree* tree, MiniNtuple& nt) {
    tree->Branch("run", &nt.run);
    tree->Branch("lumi", &nt.lumi);
    tree->Branch("event", &nt.event);
    tree->Branch("gen_flavor_code", &nt.gen_flavor_code);
    tree->Branch("pass_hlt", &nt.pass_hlt);
    tree->Branch("l1_htt", &nt.l1_htt);
    tree->Branch("l1_myhtt", &nt.l1_myhtt);
    tree->Branch("l1_myhttwbug", &nt.l1_myhttwbug);
    tree->Branch("hlt_ht", &nt.hlt_ht);
    tree->Branch("met", &nt.met);
    tree->Branch("bsx", &nt.bsx);
    tree->Branch("bsy", &nt.bsy);
    tree->Branch("bsz", &nt.bsz);
    tree->Branch("bsdxdz", &nt.bsdxdz);
    tree->Branch("bsdydz", &nt.bsdydz);
    tree->Branch("npv", &nt.npv);
    tree->Branch("pvx", &nt.pvx);
    tree->Branch("pvy", &nt.pvy);
    tree->Branch("pvz", &nt.pvz);
    tree->Branch("npu", &nt.npu);
    tree->Branch("weight", &nt.weight);
    tree->Branch("ren_weight_up", &nt.ren_weight_up);
    tree->Branch("ren_weight_dn", &nt.ren_weight_dn);
    tree->Branch("fac_weight_up", &nt.fac_weight_up);
    tree->Branch("fac_weight_dn", &nt.fac_weight_dn);
    tree->Branch("njets", &nt.njets);
    tree->Branch("jet_pt", nt.jet_pt, "jet_pt[njets]/F");
    tree->Branch("jet_eta", nt.jet_eta, "jet_eta[njets]/F");
    tree->Branch("jet_phi", nt.jet_phi, "jet_phi[njets]/F");
    tree->Branch("jet_energy", nt.jet_energy, "jet_energy[njets]/F");
    tree->Branch("jet_id", nt.jet_id, "jet_id[njets]/b");
    tree->Branch("jet_bdisc_old", nt.jet_bdisc_old, "jet_bdisc_old[njets]/F");
    tree->Branch("jet_bdisc", nt.jet_bdisc, "jet_bdisc[njets]/F");
    tree->Branch("jet_hlt_pt", nt.jet_hlt_pt, "jet_hlt_pt[njets]/F");
    tree->Branch("jet_hlt_eta", nt.jet_hlt_eta, "jet_hlt_eta[njets]/F");
    tree->Branch("jet_hlt_phi", nt.jet_hlt_phi, "jet_hlt_phi[njets]/F");
    tree->Branch("jet_hlt_energy", nt.jet_hlt_energy, "jet_hlt_energy[njets]/F");
    tree->Branch("displaced_jet_hlt_pt", nt.displaced_jet_hlt_pt, "displaced_jet_hlt_pt[njets]/F");
    tree->Branch("displaced_jet_hlt_eta", nt.displaced_jet_hlt_eta, "displaced_jet_hlt_eta[njets]/F");
    tree->Branch("displaced_jet_hlt_phi", nt.displaced_jet_hlt_phi, "displaced_jet_hlt_phi[njets]/F");
    tree->Branch("displaced_jet_hlt_energy", nt.displaced_jet_hlt_energy, "displaced_jet_hlt_energy[njets]/F");
    tree->Branch("gen_pv_x0", &nt.gen_pv_x0);
    tree->Branch("gen_pv_y0", &nt.gen_pv_y0);
    tree->Branch("gen_pv_z0", &nt.gen_pv_z0);
    tree->Branch("gen_x", nt.gen_x, "gen_x[2]/F");
    tree->Branch("gen_y", nt.gen_y, "gen_y[2]/F");
    tree->Branch("gen_z", nt.gen_z, "gen_z[2]/F");
    tree->Branch("gen_lsp_pt", nt.gen_lsp_pt, "gen_lsp_pt[2]/F");
    tree->Branch("gen_lsp_eta", nt.gen_lsp_eta, "gen_lsp_eta[2]/F");
    tree->Branch("gen_lsp_phi", nt.gen_lsp_phi, "gen_lsp_phi[2]/F");
    tree->Branch("gen_lsp_mass", nt.gen_lsp_mass, "gen_lsp_mass[2]/F");
    tree->Branch("gen_daughters", &nt.gen_daughters, 32000, 0);
    tree->Branch("gen_daughter_id", &nt.gen_daughter_id);
    tree->Branch("gen_bquarks", &nt.gen_bquarks, 32000, 0);
    tree->Branch("gen_leptons", &nt.gen_leptons, 32000, 0);
    tree->Branch("gen_jet_ht", &nt.gen_jet_ht);
    tree->Branch("gen_jet_ht40", &nt.gen_jet_ht40);
    //tree->Branch("vertices", &nt.vertices); 
    tree->Branch("nvtx", &nt.nvtx);
    tree->Branch("ntk0", &nt.ntk0);
    tree->Branch("tk0_qchi2", &nt.tk0_qchi2);
    tree->Branch("tk0_ndof", &nt.tk0_ndof);
    tree->Branch("tk0_vx", &nt.tk0_vx);
    tree->Branch("tk0_vy", &nt.tk0_vy);
    tree->Branch("tk0_vz", &nt.tk0_vz);
    tree->Branch("tk0_px", &nt.tk0_px);
    tree->Branch("tk0_py", &nt.tk0_py);
    tree->Branch("tk0_pz", &nt.tk0_pz);
    tree->Branch("tk0_inpv", &nt.tk0_inpv);
    tree->Branch("tk0_cov", &nt.tk0_cov);
    tree->Branch("genmatch0", &nt.genmatch0);
    tree->Branch("x0", &nt.x0);
    tree->Branch("y0", &nt.y0);
    tree->Branch("z0", &nt.z0);
    tree->Branch("bs2derr0", &nt.bs2derr0);
    tree->Branch("rescale_bs2derr0", &nt.rescale_bs2derr0);
    tree->Branch("ntk1", &nt.ntk1);
    tree->Branch("tk1_qchi2", &nt.tk1_qchi2);
    tree->Branch("tk1_ndof", &nt.tk1_ndof);
    tree->Branch("tk1_vx", &nt.tk1_vx);
    tree->Branch("tk1_vy", &nt.tk1_vy);
    tree->Branch("tk1_vz", &nt.tk1_vz);
    tree->Branch("tk1_px", &nt.tk1_px);
    tree->Branch("tk1_py", &nt.tk1_py);
    tree->Branch("tk1_pz", &nt.tk1_pz);
    tree->Branch("tk1_inpv", &nt.tk1_inpv);
    tree->Branch("tk1_cov", &nt.tk1_cov);
    tree->Branch("genmatch1", &nt.genmatch1);
    tree->Branch("x1", &nt.x1);
    tree->Branch("y1", &nt.y1);
    tree->Branch("z1", &nt.z1);
    tree->Branch("bs2derr1", &nt.bs2derr1);
    tree->Branch("rescale_bs2derr1", &nt.rescale_bs2derr1);
    tree->Branch("misc_weights", &nt.misc_weights);

    tree->SetAlias("jetht", "Sum$((jet_pt>40)*jet_pt)");
    tree->SetAlias("dist0", "sqrt(x0**2 + y0**2)");
    tree->SetAlias("dist1", "sqrt(x1**2 + y1**2)");
    tree->SetAlias("phi0",  "atan2(y0,x0)");
    tree->SetAlias("phi1",  "atan2(y1,x1)");
    tree->SetAlias("svdist",  "(nvtx >= 2) * sqrt((x0-x1)**2 + (y0-y1)**2)");
    tree->SetAlias("svdphi",  "(nvtx >= 2) * TVector2::Phi_mpi_pi(atan2(y0,x0)-atan2(y1,x1))");
    tree->SetAlias("svdz",    "(nvtx >= 2) * (z0 - z1)");
  }

  void read_from_tree(TTree* tree, MiniNtuple& nt) {
    tree->SetBranchAddress("run", &nt.run);
    tree->SetBranchAddress("lumi", &nt.lumi);
    tree->SetBranchAddress("event", &nt.event);
    tree->SetBranchAddress("gen_flavor_code", &nt.gen_flavor_code);
    tree->SetBranchAddress("pass_hlt", &nt.pass_hlt);
    tree->SetBranchAddress("l1_htt", &nt.l1_htt);
    tree->SetBranchAddress("l1_myhtt", &nt.l1_myhtt);
    tree->SetBranchAddress("l1_myhttwbug", &nt.l1_myhttwbug);
    tree->SetBranchAddress("hlt_ht", &nt.hlt_ht);
    tree->SetBranchAddress("met", &nt.met);
    tree->SetBranchAddress("bsx", &nt.bsx);
    tree->SetBranchAddress("bsy", &nt.bsy);
    tree->SetBranchAddress("bsz", &nt.bsz);
    tree->SetBranchAddress("bsdxdz", &nt.bsdxdz);
    tree->SetBranchAddress("bsdydz", &nt.bsdydz);
    tree->SetBranchAddress("npv", &nt.npv);
    tree->SetBranchAddress("pvx", &nt.pvx);
    tree->SetBranchAddress("pvy", &nt.pvy);
    tree->SetBranchAddress("pvz", &nt.pvz);
    tree->SetBranchAddress("npu", &nt.npu);
    tree->SetBranchAddress("weight", &nt.weight);
    tree->SetBranchAddress("ren_weight_up", &nt.ren_weight_up);
    tree->SetBranchAddress("ren_weight_dn", &nt.ren_weight_dn);
    tree->SetBranchAddress("fac_weight_up", &nt.fac_weight_up);
    tree->SetBranchAddress("fac_weight_dn", &nt.fac_weight_dn);
    tree->SetBranchAddress("njets", &nt.njets);
    tree->SetBranchAddress("jet_pt", nt.jet_pt);
    tree->SetBranchAddress("jet_eta", nt.jet_eta);
    tree->SetBranchAddress("jet_phi", nt.jet_phi);
    tree->SetBranchAddress("jet_energy", nt.jet_energy);
    tree->SetBranchAddress("jet_id", nt.jet_id);
    tree->SetBranchAddress("jet_bdisc_old", nt.jet_bdisc_old);
    tree->SetBranchAddress("jet_bdisc", nt.jet_bdisc);
    tree->SetBranchAddress("jet_hlt_pt", nt.jet_hlt_pt);
    tree->SetBranchAddress("jet_hlt_eta", nt.jet_hlt_eta);
    tree->SetBranchAddress("jet_hlt_phi", nt.jet_hlt_phi);
    tree->SetBranchAddress("jet_hlt_energy", nt.jet_hlt_energy);
    tree->SetBranchAddress("displaced_jet_hlt_pt", nt.displaced_jet_hlt_pt);
    tree->SetBranchAddress("displaced_jet_hlt_eta", nt.displaced_jet_hlt_eta);
    tree->SetBranchAddress("displaced_jet_hlt_phi", nt.displaced_jet_hlt_phi);
    tree->SetBranchAddress("displaced_jet_hlt_energy", nt.displaced_jet_hlt_energy);
    tree->SetBranchAddress("gen_pv_x0", &nt.gen_pv_x0);
    tree->SetBranchAddress("gen_pv_y0", &nt.gen_pv_y0);
    tree->SetBranchAddress("gen_pv_z0", &nt.gen_pv_z0);
    tree->SetBranchAddress("gen_x", nt.gen_x);
    tree->SetBranchAddress("gen_y", nt.gen_y);
    tree->SetBranchAddress("gen_z", nt.gen_z);
    tree->SetBranchAddress("gen_lsp_pt", nt.gen_lsp_pt);
    tree->SetBranchAddress("gen_lsp_eta", nt.gen_lsp_eta);
    tree->SetBranchAddress("gen_lsp_phi", nt.gen_lsp_phi);
    tree->SetBranchAddress("gen_lsp_mass", nt.gen_lsp_mass);
    tree->SetBranchAddress("gen_daughters", &nt.p_gen_daughters);
    tree->SetBranchAddress("gen_daughter_id", &nt.p_gen_daughter_id);
    tree->SetBranchAddress("gen_bquarks", &nt.p_gen_bquarks);
    tree->SetBranchAddress("gen_leptons", &nt.p_gen_leptons);
    tree->SetBranchAddress("gen_jet_ht", &nt.gen_jet_ht);
    tree->SetBranchAddress("gen_jet_ht40", &nt.gen_jet_ht40);
    //tree->SetBranchAddress("vertices",&nt.vertices);
    tree->SetBranchAddress("nvtx", &nt.nvtx);
    tree->SetBranchAddress("ntk0", &nt.ntk0);
    tree->SetBranchAddress("tk0_qchi2", &nt.p_tk0_qchi2);
    tree->SetBranchAddress("tk0_ndof", &nt.p_tk0_ndof);
    tree->SetBranchAddress("tk0_vx", &nt.p_tk0_vx);
    tree->SetBranchAddress("tk0_vy", &nt.p_tk0_vy);
    tree->SetBranchAddress("tk0_vz", &nt.p_tk0_vz);
    tree->SetBranchAddress("tk0_px", &nt.p_tk0_px);
    tree->SetBranchAddress("tk0_py", &nt.p_tk0_py);
    tree->SetBranchAddress("tk0_pz", &nt.p_tk0_pz);
    tree->SetBranchAddress("tk0_inpv", &nt.p_tk0_inpv);
    tree->SetBranchAddress("tk0_cov", &nt.p_tk0_cov);
    tree->SetBranchAddress("genmatch0", &nt.genmatch0);
    tree->SetBranchAddress("x0", &nt.x0);
    tree->SetBranchAddress("y0", &nt.y0);
    tree->SetBranchAddress("z0", &nt.z0);
    tree->SetBranchAddress("bs2derr0", &nt.bs2derr0);
    tree->SetBranchAddress("rescale_bs2derr0", &nt.rescale_bs2derr0);
    tree->SetBranchAddress("ntk1", &nt.ntk1);
    tree->SetBranchAddress("tk1_qchi2", &nt.p_tk1_qchi2);
    tree->SetBranchAddress("tk1_ndof", &nt.p_tk1_ndof);
    tree->SetBranchAddress("tk1_vx", &nt.p_tk1_vx);
    tree->SetBranchAddress("tk1_vy", &nt.p_tk1_vy);
    tree->SetBranchAddress("tk1_vz", &nt.p_tk1_vz);
    tree->SetBranchAddress("tk1_px", &nt.p_tk1_px);
    tree->SetBranchAddress("tk1_py", &nt.p_tk1_py);
    tree->SetBranchAddress("tk1_pz", &nt.p_tk1_pz);
    tree->SetBranchAddress("tk1_inpv", &nt.p_tk1_inpv);
    tree->SetBranchAddress("tk1_cov", &nt.p_tk1_cov);
    tree->SetBranchAddress("genmatch1", &nt.genmatch1);
    tree->SetBranchAddress("x1", &nt.x1);
    tree->SetBranchAddress("y1", &nt.y1);
    tree->SetBranchAddress("z1", &nt.z1);
    tree->SetBranchAddress("bs2derr1", &nt.bs2derr1);
    tree->SetBranchAddress("rescale_bs2derr1", &nt.rescale_bs2derr1);
    tree->SetBranchAddress("misc_weights", &nt.p_misc_weights);
  }

  MiniNtuple* clone(const MiniNtuple& nt) {
    MiniNtuple* nnt = new MiniNtuple(nt);

    if (nt.p_gen_daughters) nnt->gen_daughters = *nt.p_gen_daughters;
    if (nt.p_gen_daughter_id) nnt->gen_daughter_id = *nt.p_gen_daughter_id;
    if (nt.p_gen_bquarks) nnt->gen_bquarks = *nt.p_gen_bquarks;
    if (nt.p_gen_leptons) nnt->gen_leptons = *nt.p_gen_leptons;

    //nnt->vertices = nt.vertices;
    
    if (nt.p_tk0_qchi2) nnt->tk0_qchi2 = *nt.p_tk0_qchi2;
    if (nt.p_tk0_ndof ) nnt->tk0_ndof  = *nt.p_tk0_ndof;
    if (nt.p_tk0_vx   ) nnt->tk0_vx    = *nt.p_tk0_vx;
    if (nt.p_tk0_vy   ) nnt->tk0_vy    = *nt.p_tk0_vy;
    if (nt.p_tk0_vz   ) nnt->tk0_vz    = *nt.p_tk0_vz;
    if (nt.p_tk0_px   ) nnt->tk0_px    = *nt.p_tk0_px;
    if (nt.p_tk0_py   ) nnt->tk0_py    = *nt.p_tk0_py;
    if (nt.p_tk0_pz   ) nnt->tk0_pz    = *nt.p_tk0_pz;
    if (nt.p_tk0_inpv ) nnt->tk0_inpv  = *nt.p_tk0_inpv;
    if (nt.p_tk0_cov  ) nnt->tk0_cov   = *nt.p_tk0_cov;

    if (nt.p_tk1_qchi2) nnt->tk1_qchi2 = *nt.p_tk1_qchi2;
    if (nt.p_tk1_ndof ) nnt->tk1_ndof  = *nt.p_tk1_ndof;
    if (nt.p_tk1_vx   ) nnt->tk1_vx    = *nt.p_tk1_vx;
    if (nt.p_tk1_vy   ) nnt->tk1_vy    = *nt.p_tk1_vy;
    if (nt.p_tk1_vz   ) nnt->tk1_vz    = *nt.p_tk1_vz;
    if (nt.p_tk1_px   ) nnt->tk1_px    = *nt.p_tk1_px;
    if (nt.p_tk1_py   ) nnt->tk1_py    = *nt.p_tk1_py;
    if (nt.p_tk1_pz   ) nnt->tk1_pz    = *nt.p_tk1_pz;
    if (nt.p_tk1_inpv ) nnt->tk1_inpv  = *nt.p_tk1_inpv;
    if (nt.p_tk1_cov  ) nnt->tk1_cov   = *nt.p_tk1_cov;

    if (nt.p_misc_weights) nnt->misc_weights = *nt.p_misc_weights;

    nnt->p_gen_daughters = nnt->p_gen_bquarks = nnt->p_gen_leptons = 0;
    nnt->p_gen_daughter_id = 0;
    
    nnt->p_tk0_qchi2 = nnt->p_tk0_ndof = nnt->p_tk0_vx = nnt->p_tk0_vy = nnt->p_tk0_vz = nnt->p_tk0_px = nnt->p_tk0_py = nnt->p_tk0_pz = nnt->p_tk1_qchi2 = nnt->p_tk1_ndof = nnt->p_tk1_vx = nnt->p_tk1_vy = nnt->p_tk1_vz = nnt->p_tk1_px = nnt->p_tk1_py = nnt->p_tk1_pz = 0;
    nnt->p_tk0_inpv = nnt->p_tk1_inpv = 0;
    nnt->p_tk0_cov = nnt->p_tk1_cov = 0;

    nnt->p_misc_weights = 0;

    return nnt;
  }

  long long loop(const char* fn, const char* tree_path, bool (*fcn)(long long, long long, const mfv::MiniNtuple&)) {
    TFile* f = TFile::Open(fn);
    assert(f);

    // Set the year for the proper btagging WPs
    int year = 0;
    TH1F* h_sums = (TH1F*) f->Get("mfvWeight/h_sums");
    assert(h_sums);

    for(int ibin = 1; ibin < h_sums->GetNbinsX()+1; ++ibin){
      const std::string bin_label = h_sums->GetXaxis()->GetBinLabel(ibin);
      if(bin_label == "yearcode_x_nfiles"){
        const double yearcode_val = h_sums->GetBinContent(ibin);
        year = jmt::yearcode(yearcode_val).year();
      }
    }
    assert(year > 0);
    jmt::Year::set(year);

    TTree* tree = (TTree*)f->Get(tree_path);
    assert(tree);

    mfv::MiniNtuple nt;
    mfv::read_from_tree(tree, nt);

    long long j = 0, je = tree->GetEntriesFast();
    for (; j < je; ++j) {
      if (tree->LoadTree(j) < 0) break;
      if (tree->GetEntry(j) <= 0) continue;
      if (!fcn(j, je, nt)) break;
    }

    f->Close();
    delete f;

    return j;
  }
}
