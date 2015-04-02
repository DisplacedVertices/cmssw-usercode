BLOCK SPINFO
     1   Minimal
     2   1.0.0

BLOCK MODSEL
     1     1

BLOCK MASS
#  PDG id          mass      particle
  1000021     0.450e+03      # ~g
  1000022     0.400e+03      # ~chi_10

DECAY   1000021     0.01e01   # gluino decays
#          BR         NDA      ID1       ID2
      1.0E+00           2      1000022    21   # BR(~g -> ~chi_10  g)

DECAY   1000022     0.0197E-11  # neutralino decays
#           BR         NDA      ID1       ID2       ID3
     0.5E+00          3            3          5           6   # BR(~chi_10 -> s b t)
     0.5E+00          3           -3         -5          -6   # BR(~chi_10 -> sbar bbar tbar)


