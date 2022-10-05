#SHADOWDEPS = $(wildcard $(CMSSW_BASE)/src/JMTucker/MFVNeutralinoFormats/*/TriggerEnum*) /cvmfs/cms.cern.ch/$(SCRAM_ARCH)/external/tbb/2019_U3-pafccj/lib/libtbb.so.2 /cvmfs/cms.cern.ch/$(SCRAM_ARCH)/external/clhep/2.4.0.0-pafccj2/lib/libCLHEP.so $(CMSSW_RELEASE_BASE)/lib/$(SCRAM_ARCH)/*.so $(CMSSW_BASE)/lib/$(SCRAM_ARCH)/*.so
SHADOWDEPS = $(wildcard $(CMSSW_BASE)/src/JMTucker/MFVNeutralinoFormats/*/TriggerEnum*) /cvmfs/cms.cern.ch/$(SCRAM_ARCH)/external/tbb/2019_U3-pafccj/lib/libtbb.so.2 /cvmfs/cms.cern.ch/$(SCRAM_ARCH)/external/clhep/2.4.0.0-pafccj2/lib/libCLHEP.so $(CMSSW_RELEASE_BASE)/lib/$(SCRAM_ARCH)/libDataFormats*.so $(CMSSW_BASE)/lib/$(SCRAM_ARCH)/*.so


ROOTFLAGS=$(shell root-config --cflags --libs)
CFLAGS=-I${CMSSW_BASE}/src -I${CMSSW_RELEASE_BASE}/src -std=c++17 -O3

all: 2v_from_jets.exe statmodel.exe

MiniNtuple.o: ${CMSSW_BASE}/src/JMTucker/MFVNeutralino/src/MiniNtuple.cc ${CMSSW_BASE}/src/JMTucker/MFVNeutralino/interface/MiniNtuple.h
	g++ -I${CMSSW_BASE}/src -I${CLHEP_PARAM_PATH}/include -I/cvmfs/cms.cern.ch/${SCRAM_ARCH}/external/tbb/2019_U3-pafccj/include -I${CMSSW_RELEASE_BASE}/src -std=c++17 $(ROOTFLAGS) -c $< -o $@

2v_from_jets.exe: 2v_from_jets.cc MiniNtuple.o $(SHADOWDEPS)
	g++ -g -Wall -I${CMSSW_BASE}/src -I${CLHEP_PARAM_PATH}/include -I/cvmfs/cms.cern.ch/${SCRAM_ARCH}/external/tbb/2019_U3-pafccj/include -I${CMSSW_RELEASE_BASE}/src -std=c++17 $^ -o $@ $(ROOTFLAGS)

statmodel.exe: statmodel.cc 
	g++ -O3 -Wall -std=c++17 $^ -o $@ -lstdc++fs $(SMFLAGS) $(ROOTFLAGS) -I${CMSSW_BASE}/src -L${CMSSW_BASE}/lib/${SCRAM_ARCH} -lJMTuckerTools

clean:
	rm -f 2v_from_jets.exe statmodel.exe
