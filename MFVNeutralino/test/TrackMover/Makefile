FLAGS = \
	$(shell root-config --cflags --libs) \
	-I$(shell scram tool tag boost INCLUDE) -L$(shell scram tool tag boost LIBDIR) -lboost_program_options \
	-I$(CMSSW_BASE)/src -I$(CMSSW_RELEASE_BASE)/src \
        -L${CMSSW_BASE}/lib/${SCRAM_ARCH} -lJMTuckerTools -lJMTuckerMFVNeutralino \
	-std=c++17 -pedantic -Werror -Wall -Wextra -Wshadow -Wpointer-arith -Wcast-qual -O3

all: hists.exe mctruth.exe tests.exe

hists.exe: hists.cc utils.h BTagSFHelper.o
	g++ -o $@ $^ $(FLAGS)

%.exe: %.cc utils.h
	g++ -o $@ $^ $(FLAGS)

BTagCalibrationStandalone.h:
	ln -sf $(CMSSW_RELEASE_BASE)/src/CondTools/BTau/test/BTagCalibrationStandalone.h BTagCalibrationStandalone.h

BTagCalibrationStandalone.cc:
	ln -sf $(CMSSW_RELEASE_BASE)/src/CondTools/BTau/test/BTagCalibrationStandalone.cpp BTagCalibrationStandalone.cc

BTagSFHelper.o: BTagCalibrationStandalone.cc BTagCalibrationStandalone.h BTagSFHelper.h 
	g++ -c -o $@ $< $(FLAGS) -Wno-deprecated-declarations

clean:	
	-rm -f *.exe *.o BTagCalibrationStandalone.*
