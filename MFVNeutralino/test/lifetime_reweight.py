import ROOT
import array
import sys, os, math

#in_file = ROOT.TFile("/uscms/home/joeyr/crabdirs/MiniTree_NoVtxV27darksectorreview_withGenInfom/mfv_HtoLLPto4j_tau10mm_M1000_450_2017.root", "OPEN")
in_file = ROOT.TFile("/uscms/home/joeyr/crabdirs/MiniTreeV27darksectorreview_withGenInfom/mfv_HtoLLPto4j_tau10mm_M1000_450_2017.root", "OPEN")

out_file = ROOT.TFile("~/scratch/out_tree.root", "RECREATE")
in_tree = in_file.Get("mfvMiniTree/t")
#in_tree = in_file.Get("mfvMiniTreePreSelEvtFilt/t") # only for custom MiniTrees where we even save events with no vertices, to truly see ctau from all events

out_dir = out_file.mkdir("mfvMiniTree")
#out_dir = out_file.mkdir("mfvMiniTreePreSelEvtFilt")
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

    h_input_ctau.Fill(rest_disp1, entry.weight)
    h_input_ctau.Fill(rest_disp2, entry.weight)

    in_tau_mm  = 10 
    out_tau_mm = 3

    # note that the float division by 10. is important, or we could have a bunch of int division here!
    in_tau_cm  = in_tau_mm/10. 
    out_tau_cm = out_tau_mm/10.

    weight1 = (in_tau_cm / out_tau_cm) * math.exp( -(1/out_tau_cm - 1/in_tau_cm)*rest_disp1 )
    weight2 = (in_tau_cm / out_tau_cm) * math.exp( -(1/out_tau_cm - 1/in_tau_cm)*rest_disp2 )

    new_weight = entry.weight * weight1 * weight2

    #print weight1, weight2, new_weight

    weight_branch[0] = new_weight
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
# And need to make some improvements e.g. to automatically grab the in_tau and then use the out_tau to set the output file name (and to smartly pick the input file to use for a given output... in principle could even use more than one sample as input to build a given output, say 1mm and 10mm to build the 5mm sample)
# And need to pick a granularity. Maybe just go for 10 divisions for each, i.e. 1-10mm in steps of 1mm, 10-100mm in steps of 10mm, etc.
# And need to double check that the denominator is okay! i.e. do we need to apply a denominator-level ctau reweighting too? I think maybe we already account for it in our math but I would rather be 100000% sure.
