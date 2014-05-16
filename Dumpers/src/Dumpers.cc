#include "DataFormats/EcalDetId/interface/EBDetId.h"
#include "DataFormats/EcalDetId/interface/EEDetId.h"
#include "DataFormats/EcalDetId/interface/ESDetId.h"
#include "DataFormats/EcalDetId/interface/EcalSubdetector.h"
#include "DataFormats/MuonReco/interface/MuonSelectors.h"
#include "DataFormats/SiPixelDetId/interface/PXBDetId.h"
#include "DataFormats/SiPixelDetId/interface/PXFDetId.h"
#include "DataFormats/SiStripDetId/interface/TIBDetId.h"
#include "DataFormats/SiStripDetId/interface/TOBDetId.h"
#include "DataFormats/SiStripDetId/interface/TIDDetId.h"
#include "DataFormats/SiStripDetId/interface/TECDetId.h"
#include "Geometry/CommonDetUnit/interface/GlobalTrackingGeometry.h"
#include "Geometry/Records/interface/GlobalTrackingGeometryRecord.h"
#include "JMTucker/Dumpers/interface/Dumpers.h"

std::ostream& operator<<(std::ostream& out, const edm::Event& event) {
  edm::EventAuxiliary e = event.eventAuxiliary();
  out << "Event:\n  run: " << e.run() << " lumi: " << e.luminosityBlock() << " event: " << e.event() << std::endl
      << "  orbitNumber: " << e.orbitNumber() << " bunchCrossing: " << e.bunchCrossing() << " storeNumber: " << e.storeNumber() << std::endl
    //<< "  time: " << e.time().value() << std::endl
      << "  experimentType: " << e.experimentType() << " isRealData: " << e.isRealData() << std::endl;
  return out;
}

std::ostream& operator<<(std::ostream& out, const EncodedEventId& id) {
  out << "bunchCrossing: " << id.bunchCrossing() << " event: " << id.event() << " raw_id: " << id.rawId() << std::endl;
  return out;
}

std::ostream& operator<<(std::ostream& out, const DetId& d) {
  const unsigned raw_id = d.rawId();
  if (d.det() == DetId::Tracker) {
    if (d.subdetId() == StripSubdetector::TIB)
      out << "TIB " << TIBDetId(d);
    else if (d.subdetId() == StripSubdetector::TOB)
      out << "TOB " << TOBDetId(d);
    else if (d.subdetId() == StripSubdetector::TEC)
      out << "TEC " << TECDetId(d);
    else if (d.subdetId() == StripSubdetector::TID) 
      out << "TID " << TIDDetId(d);
    else if (d.subdetId() == (int) PixelSubdetector::PixelBarrel) 
      out << "PXB " << PXBDetId(d);
    else if (d.subdetId() == (int) PixelSubdetector::PixelEndcap)
      out << "PXF " << PXFDetId(d);
    else
      out << "unknown tk id " << raw_id << " in dump_detid";
  }
  else if (d.det() == DetId::Muon) {
    if (d.subdetId() == MuonSubdetId::DT)
      out << "DT " << DTWireId(d);
    else if (d.subdetId() == MuonSubdetId::CSC)
      out << "CSC " << CSCDetId(d);
    else if (d.subdetId() == MuonSubdetId::RPC)
      out << "RPC " << RPCDetId(d);
    else
      out << "unknown mu id " << raw_id << " in dump_detid";
  }
  else if (d.det() == DetId::Ecal) {
    if (d.subdetId() == EcalBarrel)
      out << "EB " << EBDetId(d);
    else if (d.subdetId() == EcalEndcap)
      out << "EE " << EEDetId(d);
    else if (d.subdetId() == EcalPreshower)
      out << "ES " << ESDetId(d);
    else
      out << "unknown ecal id " << raw_id << " in dump_detid";
  }
  else
    out << "unknown id " << raw_id << " in dump_detid";
  return out;
}

void dumpex_rpc_hit(std::ostream& out, const RPCRecHit& rpc) {
  out << "BunchX: " << rpc.BunchX() << " firstClusterStrip: " << rpc.firstClusterStrip() << " clusterSize: " << rpc.clusterSize();
}

void dumpex_dt1dhit(std::ostream& out, const DTRecHit1D& d) {
  out << "digiTime: " << d.digiTime() << " lrSide: " << d.lrSide();
}

std::ostream& operator<<(std::ostream& out, const RPCRecHit& rpc) {
  out << rpc.geographicalId();
  out << "\n  ";
  dumpex_rpc_hit(out, rpc);
  out << "\n  localPos: " << rpc.localPosition()  << " localPosErr: " << rpc.localPositionError()  << std::endl;
  const GeomDet* geom = JMTDumper::geom_det(rpc.geographicalId());
  if (geom)
    out << "  globalPos: " << geom->toGlobal(rpc.localPosition()) << std::endl;
  else
    out << "  no geometry available in EventSetup";
  return out;
}
  
std::ostream& operator<<(std::ostream& out, const DTRecHit1D& hit) {
  out << hit.geographicalId();
  out << " wire id: ";
  out << hit.wireId();
  out << " lrSide: " << hit.lrSide() << " digiTime: " << hit.digiTime() << " localPos: " << hit.localPosition() << " +/- " << hit.localPositionError();
  const GeomDet* geom = JMTDumper::geom_det(hit.geographicalId());
  if (geom)
    out << "  globalPos: " << geom->toGlobal(hit.localPosition());
  else
    out << "  no geometry available in EventSetup";
  out << std::endl;
  return out;
}

std::ostream& operator<<(std::ostream& out, const DTRecHit1DPair& pair) {
  out << "left:\n";
  out << *pair.componentRecHit(DTEnums::Left);
  out << "right:\n";
  out << *pair.componentRecHit(DTEnums::Right);
  return out;
}

std::ostream& operator<<(std::ostream& out, const DTRecSegment2D& dt) {
  out << dt.geographicalId();
  out << "nhits: " << dt.recHits().size() << " chi2: " << dt.chi2() << " dof: " << dt.degreesOfFreedom() << std::endl
      << " localPos: " << dt.localPosition()  << " localPosErr: " << dt.localPositionError()  << std::endl
      << " localDir: " << dt.localDirection() << " localDirErr: " << dt.localDirectionError() << std::endl
      << " t0: " << dt.t0() << " vDrift: " << dt.vDrift() << std::endl;
  const GeomDet* geom = JMTDumper::geom_det(dt.geographicalId());
  if (geom) {
    const GlobalPoint  globalPos = geom->toGlobal(dt.localPosition());
    const GlobalVector globalDir = geom->toGlobal(dt.localDirection());
    out << " globalPos: " << globalPos << " globalDir: " << globalDir << std::endl;
  }
  else
    out << " no geometry available in EventSetup";
  return out;
}

std::ostream& operator<<(std::ostream& out, const DTRecSegment4D& dt) {
  unsigned raw_id = dt.geographicalId().rawId();
  out << raw_id;
  out << "nhits: " << dt.recHits().size() << " chi2: " << dt.chi2() << " dof: " << dt.degreesOfFreedom() << " hasPhi? " << dt.hasPhi() << " hasZed? " << dt.hasZed() << std::endl
      << " localPos: " << dt.localPosition()  << " localPosErr: " << dt.localPositionError()  << std::endl
      << " localDir: " << dt.localDirection() << " localDirErr: " << dt.localDirectionError() << std::endl;

  const GeomDet* geom = JMTDumper::geom_det(dt.geographicalId());
  if (geom) {
    const GlobalPoint  globalPos = geom->toGlobal(dt.localPosition());
    const GlobalVector globalDir = geom->toGlobal(dt.localDirection());
    out << " globalPos: " << globalPos << " globalDir: " << globalDir << std::endl;
  }
  else
    out << " no geometry available in EventSetup";

  out << " segments/hits:\n";
  for (const TrackingRecHit* trh : dt.recHits())
    out << "  " << trh;
  return out;
}

std::ostream& operator<<(std::ostream& out, const CSCRecHit2D& hit) {
  out << "quality: " << hit.quality() << " positionWithinStrip: " << hit.positionWithinStrip() << " +/- " << hit.errorWithinStrip() << " badStrip: " << hit.badStrip() << " badWireGroup: " << hit.badWireGroup() << std::endl
      << "tpeak: " << hit.tpeak() << "\nstrips: ";
  //for (int x : hit.channels())
  //   out << x << " ";
  //out << "\nwiregroups: ";
  //for (int x : hit.wgroups())
  //  out << x << " ";
  return out;
}

std::ostream& operator<<(std::ostream& out, const CSCSegment& seg) {
  out << seg.geographicalId();
  out << "nhits: " << seg.nRecHits() << " chi2: " << seg.chi2() << std::endl
      << " localPos: " << seg.localPosition()  << " localPosErr: " << seg.localPositionError()  << std::endl
      << " localDir: " << seg.localDirection() << " localDirErr: " << seg.localDirectionError() << std::endl;
  for (const CSCRecHit2D& h : seg.specificRecHits())
    out << h;

  const GeomDet* geom = JMTDumper::geom_det(seg.geographicalId());
  if (geom) {
    const GlobalPoint  globalPos = geom->toGlobal(seg.localPosition());
    const GlobalVector globalDir = geom->toGlobal(seg.localDirection());
    out << " globalPos: " << globalPos << " globalDir: " << globalDir << std::endl;
  }
  else
    out << " no geometry available in EventSetup";
  return out;
}

std::ostream& operator<<(std::ostream& out, const reco::HitPattern& hp) {
  out << "# hits: " << hp.numberOfHits() << std::endl
      << "# valid: tot: " << hp.numberOfValidHits() << " tk: " << hp.numberOfValidTrackerHits() << " pxb: " << hp.numberOfValidPixelBarrelHits() << " pxe: " << hp.numberOfValidPixelEndcapHits() << " tib: " << hp.numberOfValidStripTIBHits() << " tob: " << hp.numberOfValidStripTOBHits() << " tid: " << hp.numberOfValidStripTIDHits() << " tec: " << hp.numberOfValidStripTECHits() << " mu: " << hp.numberOfValidMuonHits() << " csc: " << hp.numberOfValidMuonCSCHits() << " dt: " << hp.numberOfValidMuonDTHits() << " rpc: " << hp.numberOfValidMuonRPCHits() << std::endl
      << "# lost: tot: " << hp.numberOfLostHits() << " tk: " << hp.numberOfLostTrackerHits() << " pxb: " << hp.numberOfLostPixelBarrelHits() << " pxe: " << hp.numberOfLostPixelEndcapHits() << " tib: " << hp.numberOfLostStripTIBHits() << " tob: " << hp.numberOfLostStripTOBHits() << " tid: " << hp.numberOfLostStripTIDHits() << " tec: " << hp.numberOfLostStripTECHits() << " mu: " << hp.numberOfLostMuonHits() << " csc: " << hp.numberOfLostMuonCSCHits() << " dt: " << hp.numberOfLostMuonDTHits() << " rpc: " << hp.numberOfLostMuonRPCHits() << std::endl
      << "# bad: tot: " << hp.numberOfBadHits() << " mu: " << hp.numberOfBadMuonHits()  << " csc: " << hp.numberOfBadMuonCSCHits()  << " dt: " << hp.numberOfBadMuonDTHits()  << " rpc: " << hp.numberOfBadMuonRPCHits() << std::endl
      << "# tk layers: with meas: " << hp.trackerLayersWithMeasurement() << " without: " << hp.trackerLayersWithoutMeasurement() << " totallyofforbad: " << hp.trackerLayersTotallyOffOrBad() << " null: " << hp.trackerLayersNull() << std::endl
      << "# px layers: with meas: " << hp.pixelLayersWithMeasurement() << " without: " << hp.pixelLayersWithoutMeasurement() << " totallyofforbad: " << hp.pixelLayersTotallyOffOrBad() << " null: " << hp.pixelLayersNull() << std::endl
      << "# si layers: with meas: " << hp.stripLayersWithMeasurement() << " without: " << hp.stripLayersWithoutMeasurement() << " totallyofforbad: " << hp.stripLayersTotallyOffOrBad() << " null: " << hp.stripLayersNull() << std::endl;

  for (int i = 0, ie = hp.numberOfHits(); i < ie; ++i) {
    uint32_t hit = hp.getHitPattern(i);

    out << "hit #" << std::setw(2) << i << " in binary format = ";
    for (int j = 10; j >= 0; --j) {
      int bit = (hit >> j) & 0x1;
      out << bit;
      if (j == 10 || j == 7 || j == 3 || j == 2)
        out << " ";
    }
    out << std::endl;
  }
  
  return out;
}

std::ostream& operator<<(std::ostream& out, const reco::Track& tk) {
  out << "algo: " << tk.algoName() << " qualityMask: " << tk.qualityMask()
      << " q: " << tk.charge() << " p: " << tk.p()
      << " q/p error: " << tk.qoverpError() << " theta: " << tk.theta() << " theta error: " << tk.thetaError() << " phi error: " << tk.phiError()
      << " pt: " << tk.pt() << " pt error: " << tk.ptError() << " eta: " << tk.eta()
      << " phi: " << tk.phi() << " chi2: " << tk.chi2() << " dof: " << tk.ndof() << std::endl
      << "  d0: " << tk.d0() << " d0 error: " << tk.d0Error()
      << " reference point: " << tk.referencePoint() << std::endl;

  if (tk.extra().isAvailable())
    out << "  innerPosition: " << tk.innerPosition() << " outerPosition: " << tk.outerPosition() << std::endl
	<< "  innerMomentum: " << tk.innerMomentum() << " outerMomentum: " << tk.outerMomentum() << std::endl;
  else
    out << "  no TrackExtra available\n";

  out << "HitPattern:\n" << tk.hitPattern();

  if (tk.extra().isAvailable() && tk.recHit(0).isAvailable()) {
    out << "  hits (size: " << tk.recHitsSize() << "):\n";
    for (int i = 0, ie = int(tk.recHitsSize()); i < ie; ++i)
      out << "    trh #" << i << ": " << *tk.recHit(i);
  }
  else
    out << "  hits not available!\n";
  return out;
}

std::ostream& operator<<(std::ostream& out, const reco::Muon& mu) {
  static const char* names[3] = {"global", "inner ", "outer "};
  const reco::TrackRef refs[3] = { mu.globalTrack(), mu.innerTrack(), mu.outerTrack() };

  out << "pt: " << mu.pt() << " eta: " << mu.eta() << " phi: " << mu.phi() << "   " 
      << "isGlobal: " << mu.isGlobalMuon() << " isTracker: " << mu.isTrackerMuon() << " isStandAlone: " << mu.isStandAloneMuon() << std::endl;
  for (int i = 0; i < 3; ++i) {
    if (refs[i].isAvailable()) {
      out << " " << names[i] << " track (pt: " << refs[i]->pt() << "): "; // (id: " << refs[i].index() << "): " << std::endl;
      JMTDumper::dump_ref(out, refs[i]);
      //dump_tk(out, *refs[i]);
    }
    else
      out << " " << names[i] << " track is not available!\n";
  }

  return out;

  static const char* id_algos[] = {
    "TrackerMuonArbitrated",
    "AllArbitrated",
    "GlobalMuonPromptTight",
    "TMLastStationLoose",
    "TMLastStationTight",
    "TM2DCompatibilityLoose",
    "TM2DCompatibilityTight",
    "TMOneStationLoose",
    "TMOneStationTight",
    "TMLastStationOptimizedLowPtLoose",
    "TMLastStationOptimizedLowPtTight",
    "GMTkChiCompatibility",
    "GMStaChiCompatibility",
    "GMTkKinkTight",
    "TMLastStationAngLoose",
    "TMLastStationAngTight",
    "TMOneStationAngLoose",
    "TMOneStationAngTight",
    "TMLastStationOptimizedBarrelLowPtLoose",
    "TMLastStationOptimizedBarrelLowPtTight",
    0
  };

  out << "muon id:\n";
  for (size_t i = 0; id_algos[i] != 0; ++i)
    out << "  " << std::setw(40) << id_algos[i] << ": " << muon::isGoodMuon(mu, muon::selectionTypeFromString(id_algos[i])) << std::endl;

  if (mu.isTimeValid()) {
    const reco::MuonTime& mt = mu.time();
    out << "Muon timing info: direction: " << mt.direction() << " nDof: " << mt.nDof
	<< " timeAtIpInOut: " << mt.timeAtIpInOut << " +/- " << mt.timeAtIpInOutErr
	<< " timeAtIpOutIn: " << mt.timeAtIpOutIn << " +/- " << mt.timeAtIpOutInErr << std::endl;
  }
  else
    out << "MuonTime structure unavailable!\n";

  if (mu.isEnergyValid()) {
    //const MuonEnergy& me = mu.calEnergy();
  }
  out << "MuonEnergy structure unavailable!\n";
  return out;
}

std::ostream& operator<<(std::ostream& out, const reco::GenParticle& genp) {
  out << "pdgId: " << genp.pdgId() << " status: " << genp.status()
      << " q: " << genp.charge() << " pt: " << genp.pt()
      << " eta: " << genp.eta() << " phi: " << genp.phi()
      << " mass: " << genp.mass() << " vertex: " << genp.vertex() << std::endl;
  return out;
}

std::ostream& operator<<(std::ostream& out, const TrackingRecHit& trh) {
  out << "isValid: " << trh.isValid() << " type: " << trh.type() << " detId: " << trh.geographicalId().rawId() << " ";
  out << trh.geographicalId();
  if (trh.isValid()) {
    out << " weight: " << trh.weight() << " dim: " << trh.dimension();
    if (trh.hasPositionAndError()) {
      out << " localPos: " << trh.localPosition() << " localPosErr: " << trh.localPositionError();

      const GeomDet* geom = JMTDumper::geom_det(trh.geographicalId());
      if (geom) {
	const GlobalPoint globalPos = geom->toGlobal(trh.localPosition());
	out << " globalPos: " << globalPos;
      }
      else
	out << " no geometry available in EventSetup";
    }
  }

  const RPCRecHit* rpc = dynamic_cast<const RPCRecHit*>(&trh);
  const DTRecHit1D* dt1d = dynamic_cast<const DTRecHit1D*>(&trh);
  if (rpc || dt1d) {
    out << " ";
    if (rpc)       dumpex_rpc_hit(out, *rpc);
    else if (dt1d) dumpex_dt1dhit(out, *dt1d);
  }

  out << std::endl;
  return out;
}

std::ostream& operator<<(std::ostream& out, const TrajectorySeed& seed) {
  out << "nHits: " << seed.nHits() << " direction: " << seed.direction() << std::endl;
  out << "hits:\n";
  TrajectorySeed::range p = seed.recHits();
  TrajectorySeed::const_iterator b = p.first, e = p.second;
  for ( ; b != e; ++b)
    out << *b;
  return out;
}

std::ostream& operator<<(std::ostream& out, const reco::TrackToTrackMap& map) {
  out << "map size: " << map.size() << std::endl;
  int ipair = 0; // subtracting iterators below doesn't work
  for (reco::TrackToTrackMap::const_iterator it = map.begin(), ite = map.end(); it != ite; ++it) {
    out << "pair #" << ipair << ":\n  key ref: ";
    JMTDumper::dump_ref(out, it->key);
    out << "  val ref: ";
    JMTDumper::dump_ref(out, it->val);
  }
  return out;
}

std::ostream& operator<<(std::ostream& out, const reco::BeamSpot& bs) {
  out << "type: " << bs.type() << " x0: " << bs.x0() << " y0: " << bs.y0() << " z0: " << bs.z0() << "\ncovariance matrix:\n";
  for (int i = 0; i < 7; ++i) {
    for (int j = 0; j < 7; ++j)
      out << bs.covariance(i,j) << " ";
    out << std::endl;
  }
  out << "sigmaZ: " << bs.sigmaZ() << " dxdz: " << bs.dxdz() << " dydz: " << bs.dydz() << std::endl
      << " BeamWidthX: " << bs.BeamWidthX() << " BeamWidthY: " << bs.BeamWidthY() << std::endl
      << " emittanceX: " << bs.emittanceX() << " emittanceY: " << bs.emittanceY() << " betaStar: " << bs.betaStar();
  return out;
}

std::ostream& operator<<(std::ostream& out, const PSimHit& hit) {
  out << "  processType: " << hit.processType() << " trackId: " << hit.trackId() << " energyLoss: " << hit.energyLoss() << std::endl
      << "    particleType: " << hit.particleType() << " pAtEntry: " << hit.pabs() << " phiAtEntry: " << hit.phiAtEntry().degrees() << " thetaAtEntry: " << hit.thetaAtEntry().value()/3.14159*180 << std::endl
      << "    detUnitId: " << hit.detUnitId() << " ";
  out << hit.detUnitId();
  out << std::endl;
  out << "    entryPoint: " << hit.entryPoint() << " exitPoint: " << hit.exitPoint() << "\n";
  out << "    localDirection: " << hit.localDirection() << " localPosition: " << hit.localPosition() << "\n";

  const GeomDet* geom = JMTDumper::geom_det(hit.detUnitId());
  if (geom) {
    const GlobalPoint& globalPosition = geom->toGlobal(hit.localPosition());
    const GlobalVector& globalDirection = geom->toGlobal(hit.localDirection());
    out << "    globalDirection: " << globalDirection << " globalPosition: " << globalPosition << "\n";
  }
  else
    out << "    no geometry available in EventSetup, no global direction/position available\n";
  return out;
}

std::ostream& operator<<(std::ostream& out, const SimVertex& vtx) {
  out << "encodedEventId: " << vtx.eventId()
      << "parentIndex: " << vtx.parentIndex() << " position: (" <<  vtx.position().x() << ", " << vtx.position().y() << ", " <<  vtx.position().z() << ")\n";
  return out;
}

std::ostream& operator<<(std::ostream& out, const SimTrack& tk) {
  out << "encodedEventId: " << tk.eventId()
      << "type: " << tk.type() << " charge: " << tk.charge() << " trackId: " << tk.trackId()
      << " genpartIndex: " << tk.genpartIndex() << " vertIndex: " << tk.vertIndex() << std::endl
      << "  momentum: (" << tk.momentum().x() << ", " << tk.momentum().y() << ", " << tk.momentum().z() << ", " << tk.momentum().t() << ")\n";
  return out;
}

std::ostream& operator<<(std::ostream& out, const TrackingParticle& tp) {
  out << "encodedEventId: " << tp.eventId()
      << "pdgId: " << tp.pdgId() << " charge: " << tp.charge() << " mass: " << tp.mass() << " pt,eta,phi,E: ("
      << tp.pt() << ", " << tp.eta() << ", " << tp.phi() << ", " << tp.energy() << ") matchedHit: " << tp.matchedHit() << std::endl
      << "simTracks:\n";
  for (const SimTrack& tk : tp.g4Tracks())
    out << tk;
  out << "simHits:\n";
  for (const PSimHit& hit : tp.trackPSimHit())
    out << hit;
  return out;
}

std::ostream& operator<<(std::ostream& out, const pat::CompositeCandidate& cc) {
  out << "mass: " << cc.mass() << " pt: " << cc.pt() << " rap: " << cc.rapidity() << " phi: " << cc.phi() << " eta: " << cc.eta() << "\n";
  return out;
}

bool JMTDumper::warn = true;
const edm::Event* JMTDumper::event = 0;
const edm::EventSetup* JMTDumper::event_setup = 0;

const GeomDet* JMTDumper::geom_det(const DetId& id) {
  if (event_setup) {
    try {
      edm::ESHandle<GlobalTrackingGeometry> geometry;
      event_setup->get<GlobalTrackingGeometryRecord>().get(geometry);
      return geometry->idToDet(id);
    }
    catch (const cms::Exception& ex) {
      if (warn)
	std::cerr << "JMTDumper::geom_det ERROR: no geometry available in EventSetup\n";
    }
  }
    
  return 0;
}
