#!/usr/bin/env python

'''
This script compares different plot within the same root file
'''

import ROOT as R
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--input", default="")
parser.add_argument("--plots", nargs='+')
parser.add_argument("--color", nargs='+', type=int)
parser.add_argument("--legend", nargs='+')
parser.add_argument("--norm", action='store_true')
parser.add_argument("--output")
args = parser.parse_args()

R.gROOT.SetBatch(R.kTRUE)
f = R.TFile(args.input)
h_list = []
for i in range(0,len(args.plots)):
  h = f.Get(args.plots[i])
  h.SetName(args.legend[i])
  h.SetLineColor(args.color[i])
  if args.norm:
    h.Scale(1.0/h.Integral())
  h_list.append(h)

for ih in range(len(h_list)):
  if ih==0:
    h_list[ih].SetTitle("");
    h_list[ih].Draw()
  else:
    h_list[ih].Draw("sames")
  R.gPad.Update()
  s = h_list[ih].FindObject('stats')
  s.SetTextColor(h_list[ih].GetLineColor())
  s.SetLineColor(h_list[ih].GetLineColor())
  y1,y2 = s.GetY1NDC(), s.GetY2NDC()
  s.SetY1NDC(y1 - (y2-y1)*ih)
  s.SetY2NDC(y2 - (y2-y1)*ih)
  R.gPad.Update()

#R.gPad.Update()
R.gPad.SaveAs(args.output)
#input("Type <Enter> to quit...")
