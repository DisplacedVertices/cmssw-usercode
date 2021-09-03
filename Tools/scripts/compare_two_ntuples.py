#! /usr/bin/env python

import ROOT
import sys,os
from DataFormats.FWLite import Events, Handle

from DVCode.Tools.ROOTTools import *
cmssw_setup()

# FIXME you can replace this with the usual stuff for putting plots into our publicweb areas and generating the html
outputdir = "~/publicweb/testTwoNtuples"
outputdir += "/" # in case we forget it...
os.system("mkdir -p "+outputdir)

events_ntuple1 = Events (sys.argv[1])
events_ntuple2 = Events (sys.argv[2])

# create handle and labels outside of loop
vertices_handle1  = Handle ("std::vector<MFVVertexAux>")
vertices_label1 = ("mfvVerticesAux")

vertices_handle2  = Handle ("std::vector<MFVVertexAux>")
vertices_label2 = ("mfvVerticesAux")

# FIXME should be able to do the same for our mfv events, just didn't do anything with it yet
#event_handle1  = Handle ("MFVEvent")
#event_label1 = ("mfvEvent")

# Create histograms, etc.
ROOT.gROOT.SetBatch() # don't pop up canvases

# create an output root file
outfile = ROOT.TFile(outputdir+"out.root", "RECREATE")

# Define histograms here (obviously this one doesn't matter for you, but I stole it from some other code of mine)
h_zmass = ROOT.TH1F ("zmass", "Z Candidate Mass;mass [GeV];entries", 50, 20, 220)

nevents_processed = 0
for event1 in events_ntuple1 :

    if nevents_processed % 1000 == 0 :
        print "Processing event #%s" % (nevents_processed)

    run_lumi_event_number1 = (event1.eventAuxiliary().id().run(), event1.eventAuxiliary().id().luminosityBlock(), event1.eventAuxiliary().id().event())

    # associate the handle with the label and the event
    event1.getByLabel (vertices_label1, vertices_handle1)

    # get the product: these are the objects that we'll access!
    vertices_from_ntuple1 = vertices_handle1.product()


    for event2 in events_ntuple2 :

        run_lumi_event_number2 = (event2.eventAuxiliary().id().run(), event2.eventAuxiliary().id().luminosityBlock(), event2.eventAuxiliary().id().event())

        # FIXME don't forget, you'll need to think about how you want to handle cases where an event is present in one ntuple but not the other
        if run_lumi_event_number1 != run_lumi_event_number2 : continue

        # Okay! we have the same event in both ntuples here now
        event2.getByLabel (vertices_label2, vertices_handle2)
        vertices_from_ntuple2 = vertices_handle2.product()

        print "Number of vertices_from_ntuple1 is %s" % len(vertices_from_ntuple1)
        print "Number of vertices_from_ntuple2 is %s" % len(vertices_from_ntuple2)

        for vtx_ntuple1 in vertices_from_ntuple1 :
            print vtx_ntuple1.bs2derr, vtx_ntuple1.pt[0], vtx_ntuple1.eta[0], vtx_ntuple1.mass[0] # etc to access other vars

        for vtx_ntuple2 in vertices_from_ntuple2 :
            print vtx_ntuple2.bs2derr, vtx_ntuple2.pt[0], vtx_ntuple2.eta[0], vtx_ntuple2.mass[0] # etc to access other vars

        # fill the histogram -- obviously you'll need to make the relevant ones
        #h_zmass.Fill(zmass)
    
    # reset event2
    events_ntuple2.toBegin()

    nevents_processed += 1

# make a canvas, draw, and save it
c1 = ROOT.TCanvas()
h_zmass.Draw()
c1.Print (outputdir+"h_zmass.png")
