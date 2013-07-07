import os, sys

template = '''
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-

cat > gensimhlt.py << EOF
%(gensimhlt)s
EOF

#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-

cat > minbias.py << EOF
%(minbias)s
EOF

# 2954 files

#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-

cat > modify.py << EOF
%(modify)s
EOF

# gluino mass = neutralino mass + 5 GeV

#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-

cat > pythia8_hack << EOF
%(pythia8_hack)s
EOF

#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-

cat > reco.py << EOF
%(reco)s
EOF

#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-

cat > pat.py << EOF
%(pat)s

process.source.fileNames = ['file:reco.root']
process.maxEvents.input = -1
no_skimming_cuts(process)
aod_plus_pat(process)
input_is_pythia8(process)
keep_random_state(process)
keep_mixing_info(process)
EOF

#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-

cat > patsel.py << EOF
%(patsel)s
EOF

#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-
'''

minbias = open('minbias.py', 'rt').read()
modify = open('modify.py', 'rt').read()
pythia8_hack = open('pythia8_hack', 'rt').read()
reco = open('reco.py', 'rt').read()
pat = open(os.path.join(os.environ['CMSSW_BASE'], 'src/JMTucker/Tools/python/PATTuple_cfg.py'), 'rt').read()
patsel = open(os.path.join(os.environ['CMSSW_BASE'], 'src/JMTucker/Tools/python/PATTupleSelection_cfi.py'), 'rt').read()

for fn in sys.argv[1:]:
    gensimhlt = open(fn, 'rt').read()
    open(fn + '.original', 'wt').write(gensimhlt)
    open(fn, 'wt').write(template % locals())
