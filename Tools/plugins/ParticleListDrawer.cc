#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "SimGeneral/HepPDTRecord/interface/ParticleDataTable.h"
#include "DVCode/Tools/interface/GenUtilities.h"

class JMTParticleListDrawer : public edm::EDAnalyzer {
public:
  explicit JMTParticleListDrawer(const edm::ParameterSet&);
  void analyze(const edm::Event&, const edm::EventSetup&);

private:
  const edm::InputTag src;
  const edm::EDGetTokenT<reco::GenParticleCollection> token;
  int maxEventsToPrint;
  const bool printVertex;
  const bool useMessageLogger;
};

JMTParticleListDrawer::JMTParticleListDrawer(const edm::ParameterSet& cfg)
  : src(cfg.getParameter<edm::InputTag>("src")),
    token(consumes<reco::GenParticleCollection>(src)),
    maxEventsToPrint(cfg.getUntrackedParameter<int>("maxEventsToPrint", -1)),
    printVertex(cfg.getUntrackedParameter<bool>("printVertex", false)),
    useMessageLogger(cfg.getUntrackedParameter<bool>("useMessageLogger", false))
{
}

void JMTParticleListDrawer::analyze(const edm::Event& event, const edm::EventSetup& setup) {
  edm::Handle<reco::GenParticleCollection> particles;
  event.getByToken(token, particles);

  edm::ESHandle<ParticleDataTable> pdt;
  setup.getData(pdt);

  if (maxEventsToPrint == 0)
    return;
  else if (maxEventsToPrint > 0)
    --maxEventsToPrint;

  std::ostringstream out;
  char buf[512];

  out << "\n[JMTParticleListDrawer] particle collection " << src.label() << "\n";
  out << "Run: " << event.id().run() << " LS: " << event.luminosityBlock() << " Event: " << event.id().event() << "\n";
  snprintf(buf, 512, 
           " %5s | %7s - %12s | %4s | %4s %4s %4s %4s | %4s %4s | %10s %10s %10s | %10s %10s %10s %10s %10s",
           "index", "pdgId", "name", "stat", "mom1", "mom2", "dau1", "dau2", "nmom", "ndau", "pt", "eta", "phi", "px", "py", "pz", "energy", "mass");
  out << buf;
  if (printVertex) {
    snprintf(buf, 512, " | %10s %10s %10s", "vx", "vy", "vz");
    out << buf;
  }
  out << "\n";

  int idx = 0;
  for (reco::GenParticleCollection::const_iterator p = particles->begin(), pe = particles->end(); p != pe; ++p, ++idx) {
    const int id = p->pdgId();
    const ParticleData* pd = pdt->particle(id);
    std::string particleName;
    if (!pd) {
      snprintf(buf, 512, "P%i", id);
      particleName = buf;
    }
    else
      particleName = pd->name();

    const int nMo = p->numberOfMothers();
    const int nDa = p->numberOfDaughters();
    snprintf(buf, 512,
	     " %5d | %7d - %12s | %4d | %4d %4d %4d %4d | %4d %4d | %10.3f %10.3f %10.3f | %10.3f %10.3f %10.3f %10.3f %10.3f",
             idx,
             p->pdgId(),
             particleName.c_str(),
             p->status(),
             original_index(p->mother  (0),     *particles),
             original_index(p->mother  (nMo-1), *particles),
             original_index(p->daughter(0),     *particles),
             original_index(p->daughter(nDa-1), *particles),
             nMo,
             nDa,
             p->pt(),
             p->eta(),
             p->phi(),
             p->px(),
             p->py(),
             p->pz(),
             p->energy(),
             p->mass()
             );
    out << buf;

    if (printVertex) {
      snprintf(buf, 512, " | %10.3f %10.3f %10.3f", p->vertex().x(), p->vertex().y(), p->vertex().z());
      out << buf;
    }

    out << "\n";
  }

  if (useMessageLogger)
    edm::LogVerbatim("JMTParticleListDrawer") << out.str();
  else
    std::cout << out.str();
}

DEFINE_FWK_MODULE(JMTParticleListDrawer);
