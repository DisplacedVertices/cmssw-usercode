import ROOT
import array
import sys, os, math

in_file = ROOT.TFile("/uscms/home/joeyr/crabdirs/MiniTreeV27darksectorreview_withGenInfom/mfv_HtoLLPto4j_tau1mm_M1000_450_2017.root", "OPEN")

out_file = ROOT.TFile("~/scratch/out_tree.root", "RECREATE")
in_tree = in_file.Get("mfvMiniTree/t")

out_dir = out_file.mkdir("mfvMiniTree")
out_dir.cd()
out_tree = in_tree.CloneTree(0)

weight_branch = array.array('f', [0])
out_tree.SetBranchAddress("weight", weight_branch)

h_input_ctau = ROOT.TH1F("input ctau", "input ctau", 100, 0, 5)
h_output_ctau = ROOT.TH1F("output ctau", "output ctau", 100, 0, 5)

for entry in in_tree :

    rest_tlv1 = ROOT.TLorentzVector() 
    rest_tlv2 = ROOT.TLorentzVector() 

    lab_disp1 = ((entry.bsx + entry.gen_x[0] - entry.gen_pv_x0) ** 2 + (entry.bsy + entry.gen_y[0] - entry.gen_pv_y0) ** 2 + (entry.bsz + entry.gen_z[0] - entry.gen_pv_z0) ** 2) ** 0.5
    lab_disp2 = ((entry.bsx + entry.gen_x[1] - entry.gen_pv_x0) ** 2 + (entry.bsy + entry.gen_y[1] - entry.gen_pv_y0) ** 2 + (entry.bsz + entry.gen_z[1] - entry.gen_pv_z0) ** 2) ** 0.5

    rest_tlv1.SetPtEtaPhiM(entry.gen_lsp_pt[0], entry.gen_lsp_eta[0], entry.gen_lsp_phi[0], entry.gen_lsp_mass[0])
    rest_tlv2.SetPtEtaPhiM(entry.gen_lsp_pt[1], entry.gen_lsp_eta[1], entry.gen_lsp_phi[1], entry.gen_lsp_mass[1])
    rest_disp1 = lab_disp1 / rest_tlv1.Gamma() / rest_tlv1.Beta()
    rest_disp2 = lab_disp2 / rest_tlv2.Gamma() / rest_tlv2.Beta()

    # FIXME!!!! I think this sample has low stats ==> large weights. ARTIFICIALLY setting to 1 for the second
    #entry.weight = 1

    h_input_ctau.Fill(rest_disp1, entry.weight)
    h_input_ctau.Fill(rest_disp2, entry.weight)

    in_tau = 1 # mm
    out_tau = 0.5 # mm

    weight1 = (in_tau / out_tau) * math.exp( -(1/out_tau - 1/in_tau)*rest_disp1 )
    weight2 = (in_tau / out_tau) * math.exp( -(1/out_tau - 1/in_tau)*rest_disp2 )

    new_weight = entry.weight * weight1 * weight2

    #print weight1, weight2, new_weight

    weight_branch[0] = new_weight
    #weight_branch[0] = -999 # just to prove it worked!
    h_output_ctau.Fill(rest_disp1, new_weight)
    h_output_ctau.Fill(rest_disp2, new_weight)

    out_tree.Fill()


out_dir.cd()
out_tree.Write()

out_hist_file = ROOT.TFile("out_hist.root", "RECREATE")
out_hist_file.cd()
h_input_ctau.Write()
h_output_ctau.Write()

# FIXME have to copy over the h_nsv type plots in the folder as well
