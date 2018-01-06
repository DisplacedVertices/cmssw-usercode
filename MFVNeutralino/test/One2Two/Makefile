2v_from_jets.exe: 2v_from_jets.cc ${CMSSW_BASE}/src/JMTucker/MFVNeutralino/src/MiniNtuple.cc ${CMSSW_BASE}/src/JMTucker/MFVNeutralino/interface/MiniNtuple.h
	g++ -g -Wall -I${CMSSW_BASE}/src -I${CMSSW_RELEASE_BASE}/src -std=c++14 2v_from_jets.cc -o 2v_from_jets.exe $(shell root-config --cflags --libs) ${CMSSW_BASE}/src/JMTucker/MFVNeutralino/src/MiniNtuple.cc

clean:
	rm 2v_from_jets.exe
