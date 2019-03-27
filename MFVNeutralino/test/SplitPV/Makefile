FLAGS = \
	$(shell root-config --cflags --libs) \
	-I$(shell scram tool tag boost INCLUDE) -L$(shell scram tool tag boost LIBDIR) -lboost_program_options \
	-I$(CMSSW_BASE)/src -I$(CMSSW_RELEASE_BASE)/src \
        -L${CMSSW_BASE}/lib/${SCRAM_ARCH} -lJMTuckerTools -lJMTuckerMFVNeutralino \
	-std=c++17 -pedantic -Werror -Wall -Wextra -Wshadow -Wpointer-arith -Wcast-qual -O3

all: hists.exe

%.exe: %.cc
	g++ -o $@ $^ $(FLAGS)

clean:
	-rm -f *.exe *.o
