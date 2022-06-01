#!/usr/bin/env python

import ROOT
import sys, os, argparse
from glob import glob
from pprint import pprint

parser = argparse.ArgumentParser(description = 'run an analyis on *.root minitree files in a given pathA', usage = '%(prog)s [options] pathA')

parser.add_argument('positional', nargs='*')


options = parser.parse_args()

if len(options.positional) is not 1:
    print 'Required args missing, including just one path\n'
    parser.print_help()
    sys.exit(1)

pathA = options.positional[0]
filename_i_list = glob(pathA+'minitree.root') #FIXME : may consider using a wild card to make multiple histograms at once from multiple samples (in *.root files) 

for i in filename_i_list:
    fA = ROOT.TFile.Open(i)
    if not fA.IsOpen():
         raise IOError('could not open input file %s' % fnA)
    t = fA.Get("mfvMiniTree/t") #FIXME : this example opens a tree of a specific event category of >=2vtx >=5trk events (vertices in all event categories have all quality cuts applied except bs2derr)

    h = ROOT.TH1F("h_bs2derr_wcut","apply bs2derr < 25um to >=2vtx >=5trk events; bs2derr (cm); vertices", 50, 0.0, 0.01)
    #FIXME : add more histograms to study the differences between old and new vertices due to 'tight merging' (e.g. how the number of selected vertices has changed given a fixed GEN-level displacement between the two LLPs in an event) 

    for entry in t:    
        evt_vertices = entry.vertices
        for vtx in evt_vertices: 
          if (vtx.rescale_bs2derr < 0.0025): #FIXME : one of vertex quality selection cuts is bs2derr and it can be varied by samples -- H->SS->4d uses 0.0080 cm and LSP models used 0.0025
                h.Fill(vtx.rescale_bs2derr)
                #FIXME : your implementation here
    
    
    c0 = ROOT.TCanvas()
    h.Draw()
    c0.Update()
    c0.Print("h_bs2derr_wcut.png")
    #FIXME : new histograms to look at! 
    fA.Close()
