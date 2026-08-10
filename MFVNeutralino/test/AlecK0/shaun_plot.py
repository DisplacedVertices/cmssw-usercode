#!/usr/bin/env python

import os
import ROOT
import numpy as np
from JMTucker.Tools.ROOTTools import *
from JMTucker.MFVNeutralino.PerSignal import PerSignal

def prepare_plot(fn, dirstr, rebin, color=ROOT.kBlack):
    f = ROOT.TFile(fn)
    h = f.Get(dirstr).Get('h_dbv')

    h.Rebin(rebin)
    h.Scale(1.0/h.Integral())

    h.SetLineWidth(2)
    h.SetLineColor(color)
    h.SetDirectory(0)

    return h

ROOT.gStyle.SetOptStat(0)

set_style()
version = 'test'
ps = plot_saver(plot_dir('k0_debug_%s' % version), size=(1000,800), pdf=False, log=False)

fdir = '/uscms/home/alecduqu/crab_dirs/histsp10_k0ntupleulv1bmv2_summer20ul_miniaodv2/'
fnames = ['qcdht0200_2017', 'qcdht0300_2017', 'qcdht0500_2017', 'qcdht0700_2017', 'qcdht1000_2017', 'qcdht1500_2017', 'ttbar_2017']
colors = [ROOT.kRed,        ROOT.kOrange+2,   ROOT.kGreen+2,    ROOT.kBlue,       ROOT.kViolet,      ROOT.kGray,      ROOT.kBlack]


rebin = 5

c1 = ROOT.TCanvas('c1', '', 1000, 800)
h0 = prepare_plot(fdir+fnames[0]+'.root', 'massall', rebin, colors[0])
h1 = prepare_plot(fdir+fnames[1]+'.root', 'massall', rebin, colors[1])
h2 = prepare_plot(fdir+fnames[2]+'.root', 'massall', rebin, colors[2])
h3 = prepare_plot(fdir+fnames[3]+'.root', 'massall', rebin, colors[3])
h4 = prepare_plot(fdir+fnames[4]+'.root', 'massall', rebin, colors[4])
h5 = prepare_plot(fdir+fnames[5]+'.root', 'massall', rebin, colors[5])
h6 = prepare_plot(fdir+fnames[6]+'.root', 'massall', rebin, colors[6])


print("here 0")
h0.GetYaxis().SetRangeUser(0.00, 0.25)
h0.Draw()
print("here 1")
h1.Draw("same")
h2.Draw("same")
h3.Draw("same")
h4.Draw("same")
h5.Draw("same")
h6.Draw("same")

ps.save('hist_dbv', other_c=c1)
