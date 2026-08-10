import ROOT as R
import numpy as np
import pandas as pd
import pickle

chain = R.TChain("mfvVertexTreer/tree_DV")
chain.Add("mfv_splitSUSY_tau000000000um_M2000_1800_2017.root")

