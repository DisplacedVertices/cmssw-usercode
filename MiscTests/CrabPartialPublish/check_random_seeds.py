import sys
sys.argv.append('-b')
import ROOT

ROOT.gSystem.Load('libFWCoreFWLite')
ROOT.AutoLibraryLoader.enable()

def go(fn):
    f = ROOT.TFile.Open('dcap://cmsdca3.fnal.gov:24145/pnfs/fnal.gov/usr/cms/WAX/11/store/user/tucker/crabpubtest/crabpubtest/f6dce6c88e8fb644ac5156ff537dca5b/%s' % fn)
    f.Events.SetAlias('gen', 'recoGenParticles_genParticles__HLT.obj')
    f.Events.Draw('gen.pz()', 'Iteration$ == 2')
    ROOT.c1.SaveAs('~/asdf/' + fn.replace('.root','.png'))

[go(x) for x in '''fastsim_1_2_DZK.root
fastsim_2_1_QRU.root
fastsim_3_1_uek.root'''.split('\n')]
