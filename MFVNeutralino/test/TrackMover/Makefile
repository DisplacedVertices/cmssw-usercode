include $(CMSSW_BASE)/src/JMTucker/Tools/NtupleMakefile.in

SHADOWDEPS += $(CMSSW_BASE)/lib/$(SCRAM_ARCH)/libJMTuckerMFVNeutralino.so utils.h
FLAGS += -lJMTuckerMFVNeutralino

all: hists.exe mctruth.exe tests.exe

hists.exe: hists.cc BTagSFHelper.o $(SHADOWDEPS)
	g++ -o $@ $< BTagSFHelper.o $(FLAGS)

BTagCalibrationStandalone.h:
	ln -sf $(CMSSW_RELEASE_BASE)/src/CondTools/BTau/test/BTagCalibrationStandalone.h BTagCalibrationStandalone.h

BTagCalibrationStandalone.cc:
	ln -sf $(CMSSW_RELEASE_BASE)/src/CondTools/BTau/test/BTagCalibrationStandalone.cpp BTagCalibrationStandalone.cc

BTagSFHelper.o: BTagCalibrationStandalone.cc BTagCalibrationStandalone.h BTagSFHelper.h 
	g++ -c -o $@ $< $(FLAGS) -Wno-deprecated-declarations

clean:	
	-rm -f *.exe *.o BTagCalibrationStandalone.*
