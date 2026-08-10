#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"

class GenParticlesGraphDumper : public edm::EDAnalyzer {
public:
  explicit GenParticlesGraphDumper(const edm::ParameterSet&);

private:
  virtual void analyze(const edm::Event&, const edm::EventSetup&);
  
  const edm::InputTag src;
  const bool use_mothers;
  const bool use_daughters;
  const bool include_id_and_stat;
};

GenParticlesGraphDumper::GenParticlesGraphDumper(const edm::ParameterSet& cfg) 
  : src(cfg.getParameter<edm::InputTag>("src")),
    use_mothers(cfg.getParameter<bool>("use_mothers")),
    use_daughters(cfg.getParameter<bool>("use_daughters")),
    include_id_and_stat(cfg.getParameter<bool>("include_id_and_stat"))
{
}

void GenParticlesGraphDumper::analyze(const edm::Event& event, const edm::EventSetup&) {
  edm::Handle<reco::GenParticleCollection> gen_particles;
  event.getByLabel(src, gen_particles);

  std::map<const reco::Candidate*, int> index_cache;
  for (int i = 0, ie = gen_particles->size(); i < ie; ++i)
    index_cache[&gen_particles->at(i)] = i;

  std::cout << "graph_" << event.id().run() << "_" << event.id().event() << " = {\n";
  for (int i = 0, ie = gen_particles->size(); i < ie; ++i) {
    const reco::GenParticle& gen = gen_particles->at(i);
    printf("    %i: %s[", i, include_id_and_stat ? "(" : "");
    if (use_mothers)
      for (int j = 0, je = gen.numberOfMothers(); j < je; ++j)
	printf("%i,", index_cache[gen.mother(j)]);
    if (use_daughters)
      for (int j = 0, je = gen.numberOfDaughters(); j < je; ++j)
	printf("%i,", index_cache[gen.daughter(j)]);
    if (include_id_and_stat)
      printf("],%i,%i),\n", gen.pdgId(), gen.status());
    else
      printf("],\n");
  }
  printf("}\n");
}

DEFINE_FWK_MODULE(GenParticlesGraphDumper);

//BFS to find all paths:
//from gzz import graph
//
//start = 2
//end = 3
//
//q = []
//temp_path = [start]
//q.append(temp_path)
//while q:
//    tmp_path = q.pop(0)
//    last_node = tmp_path[-1]
//    #print tmp_path
//    if last_node == end:
//        print "VALID_PATH : ",tmp_path
//    for link_node in graph[last_node]:
//        if link_node not in tmp_path:
//            new_path = tmp_path + [link_node]
//            q.append(new_path)

// To dump to graphviz dot format
//from gzz import graph
//print 'digraph G {'
//for k,(vs,id,stat) in graph.iteritems():
//    print '%i [label="#%i s%i\n%i"];' % (k, stat, id)
//for k,(vs,id,stat) in graph.iteritems():
//    for v in vs:
//        print '%i->%i;' % (k,v)
//print '}'

// To dump to BGL code
//from gzz import graph
//
//for k in graph.iterkeys():
//    print 'Vertex v%i = boost::add_vertex(std::string("v%i"), g);' % (k,k)
//
//for k,(vs,id,stat) in graph.iteritems():
//    for v in vs:
//        print 'boost::add_edge(v%i, v%i, weight, g);' % (k, v)

// To find the paths using BGL: gg.cc
// g++ -Wall -I/uscmst1/prod/sw/cms/slc5_amd64_gcc462/external/boost/1.47.0/include gg.cc && ./a.out
//
//#include <boost/config.hpp>
//#include <boost/graph/adjacency_list.hpp>
//#include <boost/graph/dijkstra_shortest_paths.hpp>
//#include <boost/graph/graph_traits.hpp>
//#include <boost/graph/iteration_macros.hpp>
//#include <boost/graph/properties.hpp>
//#include <boost/property_map/property_map.hpp>
//#include <iostream>
//#include <utility>
//#include <vector>
// 
//int main() {
//  typedef float Weight;
//  typedef boost::property<boost::edge_weight_t, Weight> WeightProperty;
//  typedef boost::property<boost::vertex_name_t, std::string> NameProperty;
//  typedef boost::adjacency_list < boost::listS, boost::vecS, boost::directedS, NameProperty, WeightProperty > Graph;
//  typedef boost::graph_traits < Graph >::vertex_descriptor Vertex;
//  typedef boost::property_map < Graph, boost::vertex_index_t >::type IndexMap;
//  typedef boost::property_map < Graph, boost::vertex_name_t >::type NameMap;
//  typedef boost::iterator_property_map < Vertex*, IndexMap, Vertex, Vertex& > PredecessorMap;
//  typedef boost::iterator_property_map < Weight*, IndexMap, Weight, Weight& > DistanceMap;
//  typedef std::vector<Graph::edge_descriptor> PathType;
// 
//  Graph g;
//  Weight weight = 1;
// 
//#include "graph.mothersonly.h"
//  Vertex& vstart = v1480;
//  Vertex& vend = v4;
//
//  std::vector<Vertex> predecessors(boost::num_vertices(g)); // To store parents
//  std::vector<Weight> distances(boost::num_vertices(g)); // To store distances
// 
//  IndexMap indexMap = boost::get(boost::vertex_index, g);
//  PredecessorMap predecessorMap(&predecessors[0], indexMap);
//  DistanceMap distanceMap(&distances[0], indexMap);
//
//  boost::dijkstra_shortest_paths(g, vstart, boost::distance_map(distanceMap).predecessor_map(predecessorMap));
// 
//  std::cout << "distances and parents:\n";
//  NameMap nameMap = boost::get(boost::vertex_name, g);
//  BGL_FORALL_VERTICES(v, g, Graph) {
//    std::cout << "distance(" << nameMap[vstart] << ", " << nameMap[v] << ") = " << distanceMap[v] << ", "
//	      << "predecessor(" << nameMap[v] << ") = " << nameMap[predecessorMap[v]] << "\n";
//  }
//  std::cout << "\n";
// 
//  PathType path;
// 
//  Vertex v = vend; // We want to start at the destination and work our way back to the source
//  for (Vertex u = predecessorMap[v]; // Start by setting 'u' to the destintaion node's predecessor
//      u != v; // Keep tracking the path until we get to the source
//      v = u, u = predecessorMap[v]) // Set the current vertex to the current predecessor, and the predecessor to one level up
//  {
//    std::pair<Graph::edge_descriptor, bool> edgePair = boost::edge(u, v, g);
//    Graph::edge_descriptor edge = edgePair.first;
//    path.push_back(edge);
//  }
// 
//  std::cout << "Shortest path from vstart to vend:" << std::endl;
//  for (PathType::reverse_iterator pathIterator = path.rbegin(); pathIterator != path.rend(); ++pathIterator)
//    std::cout << nameMap[boost::source(*pathIterator, g)] << " -> " << nameMap[boost::target(*pathIterator, g)] << " = " << boost::get(boost::edge_weight, g, *pathIterator) << "\n";
//  std::cout << "\nDistance: " << distanceMap[vend] << "\n";
//}
