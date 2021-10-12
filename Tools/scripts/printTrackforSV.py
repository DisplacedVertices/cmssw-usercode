#!/usr/bin/env python

import ROOT as R
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--fn')
parser.add_argument('--event', default=-1, type=int)
args = parser.parse_args()


tree_name = "mfvMiniTree/t"

chain=R.TChain(tree_name)
chain.Add(args.fn)

for ievt, evt in enumerate(chain):
  if not evt.event==args.event:
    continue
  print("Event {0}: {1} tracks for SV0".format(evt.event, evt.ntk0))
  for itk in range(0, len(evt.tk0_px)):
    v = R.TVector3(evt.tk0_px[itk], evt.tk0_py[itk], evt.tk0_pz[itk])
    print("  tk {0}: pT: {1} eta: {2} phi: {3}".format(itk, v.Pt(), v.Eta(), v.Phi()))





