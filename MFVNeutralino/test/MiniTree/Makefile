ROOTFLAGS=$(shell root-config --cflags --libs)
CFLAGS=-I${CMSSW_BASE}/src -I${CMSSW_RELEASE_BASE}/src -std=c++17 -O3
EXES=looptrees.exe btags_vs_bquarks.exe

all: $(EXES)

MiniNtuple.o: ${CMSSW_BASE}/src/JMTucker/MFVNeutralino/src/MiniNtuple.cc ${CMSSW_BASE}/src/JMTucker/MFVNeutralino/interface/MiniNtuple.h
	g++ $(CFLAGS) $(ROOTFLAGS) -c $< -o $@

%.exe: %.cc MiniNtuple.o
	g++ $(CFLAGS) $(ROOTFLAGS) $^ -o $@

clean:
	rm -f MiniNtuple.o $(EXES)
