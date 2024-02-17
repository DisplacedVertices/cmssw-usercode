import ROOT
import array
import sys, os, math

def main() :
    fpath = "/eos/user/j/jreicher/dark_sector_review/StealthSUSY"
    os.system("mkdir -p "+fpath+"/reweighted/")

    generated_ctaus = [0.01, 0.1, 1, 10, 100, 1000]
    all_masses = ["mStop_1100_mS_100", "mStop_1100_mS_875", "mStop_1300_mS_100", "mStop_1300_mS_1075", "mStop_1500_mS_100", "mStop_1500_mS_1275", "mStop_300_mS_100", "mStop_300_mS_75", "mStop_500_mS_100", "mStop_500_mS_275", "mStop_700_mS_100", "mStop_700_mS_475", "mStop_900_mS_100", "mStop_900_mS_675"]

    for model in ["SHH", "SYY"] : 

        # FIXME hacky, this was originally a for loop, but I don't want to change the indentation everywhere
        # FIXME Also, I currently have a bug somewhere that runs the 0p1 and 1 mm points twice, but that just makes things take longer rather than taking up more disk space or causing any _real_ issues
        if True :

            for masses in all_masses :
                for year in ["2016", "2017", "2018"] :
                    name_template = "mfv_Stealth%s_%s_ctau_CTAU_%s.root" % (model, masses, year)

                    # get our pairings of low and high ctaus that we'll reweight from
                    for idx in xrange(0, len(generated_ctaus)) :
                        gen_ctau_low = generated_ctaus[idx]
                        if idx == len(generated_ctaus) - 1 :
                            gen_ctau_high = generated_ctaus[idx]+1 # bit of a hack, just to get it to go through the loop one more time
                        else :
                            gen_ctau_high = generated_ctaus[idx+1]

                        # start with the "low" value
                        out_ctau = gen_ctau_low
                        #print out_ctau, gen_ctau_high

                        while out_ctau < gen_ctau_high :

                            # avoid processing some samples twice due to float vs. int comparisons
                            diff = abs(out_ctau-gen_ctau_high)
                            if(diff < 1.0e-6) :
                                out_ctau += gen_ctau_low
                                continue

                            out_ctau_str = str(out_ctau)

                            # only reweight the 1eX and 3eX points, or I'll run out of disk space!
                            if not (out_ctau_str.startswith("1") or out_ctau_str.startswith("3") or out_ctau_str.startswith("0.1") or out_ctau_str.startswith("0.3") or out_ctau_str.startswith("0.01") or out_ctau_str.startswith("0.03")) : 
                                # e.g. for the 1-10mm range, increment by 1mm
                                out_ctau += gen_ctau_low
                                continue

                            # formatting for float value of 0.1mm -> file name string of 0p1mm
                            out_ctau_str = str(out_ctau).replace(".","p")

                            # weird edge case that I cannot otherwise avoid, possibly due to float vs. int comparisons
                            if out_ctau_str == "1p0" :
                                out_ctau_str = "1"

                            for in_ctau in generated_ctaus :
                                #print "makeReweightedTree", fpath, name_template, in_ctau, out_ctau
                                makeReweightedTree(fpath, name_template, in_ctau, out_ctau)

                            # makeReweightedTree formats the outputs as e.g. "mfv_HtoLLPto4j_tau5from1mm_M1000_450_2017.root", 
                            # i.e. keeping the string "from" between the output and input ctau, so that we can hadd them here
                            hadded_name = name_template.replace("CTAU", out_ctau_str)
                            hadd_inputs = name_template.replace("CTAU", out_ctau_str+"from*")

                            hadded_name = fpath+"/reweighted/"+hadded_name
                            hadd_inputs = fpath+"/reweighted/"+hadd_inputs

                            #print "hadd %s %s" % (hadded_name, hadd_inputs)
                            os.system("hadd %s %s" % (hadded_name, hadd_inputs) )

                            # e.g. for the 1-10mm range, increment by 1mm
                            out_ctau += gen_ctau_low



def makeReweightedTree(fpath, name_template, in_ctau_mm, out_ctau_mm) :

    debug = True
    apply_gen_filter = False # in principle, we only want this for the buggy Zprime samples that accidentally had some prompt decays (but I checked it to have no impact for the heavy Higgs samples)

    in_ctau_str = str(in_ctau_mm).replace(".","p")
    out_ctau_str = str(out_ctau_mm).replace(".","p")

    # weird edge case that I cannot otherwise avoid, possibly due to float vs. int comparisons
    if in_ctau_str == "1p0" :
        in_ctau_str = "1"
    if out_ctau_str == "1p0" :
        out_ctau_str = "1"
    
    in_fname = fpath+"/"+name_template.replace("CTAU", in_ctau_str)
    in_file = ROOT.TFile(in_fname, "OPEN")

    out_fname = name_template.replace("CTAU", out_ctau_str+"from"+in_ctau_str)
    print "making %s" % (fpath+"/reweighted/"+out_fname)
    out_file = ROOT.TFile(fpath+"/reweighted/"+out_fname, "RECREATE")
    in_tree = in_file.Get("mfvMiniTree/t")
    nopresel_tree = in_file.Get("mfvMiniTreePreSelEvtFilt/t") # only for custom MiniTrees where we even save events with no vertices, to truly see ctau or count sumw from all events

    # sum of weights for normalizations, must come from the nopresel_tree (i.e. number of events generated, *after* applying any gen filtering)
    sumw = 0
    sumw2 = 0

    # output directory for the tree itself
    out_dir = out_file.mkdir("mfvMiniTree")
    out_dir.cd()
    out_tree = in_tree.CloneTree(0)

    weight_branch = array.array('f', [0])
    out_tree.SetBranchAddress("weight", weight_branch)

    # for debugging purposes
    printed_once = False

    if debug :
        h_input_ctau = ROOT.TH1F("input ctau", "input ctau", 100, 0, 5)
        h_output_ctau = ROOT.TH1F("output ctau", "output ctau", 100, 0, 5)

    for tree in [in_tree, nopresel_tree] :

        fill_output_tree = True
        add_to_sumw = False

        if tree == nopresel_tree :
            fill_output_tree = False
            add_to_sumw = True

        for entry in tree :

            # mostly needed for Zprime samples where Zprime -> qq was accidentally enabled, so the LLP mass is set to 0 GeV
            if apply_gen_filter :
                if entry.gen_lsp_mass[0] < 1 or entry.gen_lsp_mass[1] < 1 : 
                    if not printed_once :
                        print "sample: %s, gen_lsp_mass[0]: %.3f, gen_lsp_mass[1]: %.3f" % (in_fname, entry.gen_lsp_mass[0], entry.gen_lsp_mass[1])
                        printed_once = True
                    continue

            # initialize and set 4-vectors in rest-frame
            rest_tlv1 = ROOT.TLorentzVector() 
            rest_tlv2 = ROOT.TLorentzVector() 
            rest_tlv1.SetPtEtaPhiM(entry.gen_lsp_pt[0], entry.gen_lsp_eta[0], entry.gen_lsp_phi[0], entry.gen_lsp_mass[0])
            rest_tlv2.SetPtEtaPhiM(entry.gen_lsp_pt[1], entry.gen_lsp_eta[1], entry.gen_lsp_phi[1], entry.gen_lsp_mass[1])

            # get the lab frame displacements from beamspot, gen-level PV, and gen-level decay point positions
            lab_disp1 = ((entry.bsx + entry.gen_x[0] - entry.gen_pv_x0) ** 2 + (entry.bsy + entry.gen_y[0] - entry.gen_pv_y0) ** 2 + (entry.bsz + entry.gen_z[0] - entry.gen_pv_z0) ** 2) ** 0.5
            lab_disp2 = ((entry.bsx + entry.gen_x[1] - entry.gen_pv_x0) ** 2 + (entry.bsy + entry.gen_y[1] - entry.gen_pv_y0) ** 2 + (entry.bsz + entry.gen_z[1] - entry.gen_pv_z0) ** 2) ** 0.5

            # compute rest frame "displacement" as ctau = lab_disp / (gamma*beta)
            rest_disp1 = lab_disp1 / rest_tlv1.Gamma() / rest_tlv1.Beta()
            rest_disp2 = lab_disp2 / rest_tlv2.Gamma() / rest_tlv2.Beta()

            # note that the float division by 10. is important, or we could have a bunch of int division here!
            # need to do use cm here since the x/y/z are all in our natural CMS units of cm
            in_ctau_cm  = in_ctau_mm/10. 
            out_ctau_cm = out_ctau_mm/10.

            weight1 = (in_ctau_cm / out_ctau_cm) * math.exp( -(1/out_ctau_cm - 1/in_ctau_cm)*rest_disp1 )
            weight2 = (in_ctau_cm / out_ctau_cm) * math.exp( -(1/out_ctau_cm - 1/in_ctau_cm)*rest_disp2 )

            new_weight = entry.weight * weight1 * weight2

            if add_to_sumw :
                # Note that we track the sumw based only on these lifetime weights, under the assumption that the other gen weights are all 1. 
                # If we used new_weight itself here, we would be including reco weights in our denominator, which would be incorrect
                sumw += (weight1 * weight2)
                sumw2 += (weight1 * weight2)**2

                # fill plots of original and output ctau, for testing.
                # only do it here for the nopresel tree, to get the full ctau distribution without any bias from cuts applied
                if debug :
                    #print weight1, weight2, new_weight
                    h_input_ctau.Fill(rest_disp1, 1)
                    h_input_ctau.Fill(rest_disp2, 1)
                    h_output_ctau.Fill(rest_disp1, weight1 * weight2)
                    h_output_ctau.Fill(rest_disp2, weight1 * weight2)

            if fill_output_tree :
                weight_branch[0] = new_weight
                out_tree.Fill()

    # write out the sumw hist
    sumw_dir = out_file.mkdir("mfvWeight")
    sumw_dir.cd()
    h_sums = in_file.Get("mfvWeight/h_sums").Clone()
    h_sums.Reset()
    # NOTE that we are filling all of the bins identically; this is fine for now since we don't use all of the bins for the limit calculation, but may not be ideal for all uses!
    for ibin in xrange(1, h_sums.GetNbinsX()+1) :
        h_sums.SetBinContent(ibin, sumw)
        h_sums.SetBinError(ibin, math.sqrt(sumw2))
    h_sums.Write()

    # write out the tree
    out_dir.cd()
    out_tree.Write()

    if debug :
        os.system("mkdir -p "+fpath+"/debugging_hists")
        out_hist_file = ROOT.TFile(fpath+"/debugging_hists/hists_"+out_fname, "RECREATE")
        out_hist_file.cd()
        h_input_ctau.Write()
        h_output_ctau.Write()

main()
