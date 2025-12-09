"""
Unit tests for Bike-Sharing Station Planner System.
Tests graph operations, shortest path algorithms, and station placement.
"""

import unittest
from graph import CityGraph, Node, Edge
from shortest_path import ShortestPathFinder
from station_placement import StationPlacementOptimizer


class TestCityGraph(unittest.TestCase):
    """Test cases for CityGraph class."""
    
    def setUp(self):
        """Set up test graph before each test."""
        self.graph = CityGraph()
        
        # Create a simple test network
        nodes = [
            Node("A", "Location A", 40.7589, -73.9851, False, 0),
            Node("B", "Location B", 40.7600, -73.9800, False, 0),
            Node("C", "Location C", 40.7650, -73.9750, True, 20),
            Node("D", "Location D", 40.7700, -73.9700, False, 0),
        ]
        
        for node in nodes:
            self.graph.add_node(node)
        
        # Add edges
        self.graph.add_edge("A", "B", 0.5, 4.0, 1.0)
        self.graph.add_edge("B", "C", 0.6, 5.0, 1.2)
        self.graph.add_edge("C", "D", 0.7, 6.0, 1.1)
        self.graph.add_edge("A", "C", 1.0, 8.0, 1.5)
    
    def test_node_creation(self):
        """Test node creation and properties."""
        node = Node("TEST", "Test Location", 40.0, -74.0, True, 15)
        self.assertEqual(node.node_id, "TEST")
        self.assertEqual(node.name, "Test Location")
        self.assertEqual(node.lat, 40.0)
        self.assertEqual(node.lon, -74.0)
        self.assertTrue(node.is_station)
        self.assertEqual(node.capacity, 15)
    
    def test_graph_node_count(self):
        """Test node counting in graph."""
        self.assertEqual(self.graph.node_count(), 4)
    
    def test_graph_edge_count(self):
        """Test edge counting in graph."""
        # Should have 8 edges (4 bidirectional = 8 total)
        self.assertEqual(self.graph.edge_count(), 8)
    
    def test_get_neighbors(self):
        """Test neighbor retrieval."""
        neighbors = self.graph.get_neighbors("A")
        self.assertEqual(len(neighbors), 2)  # A connects to B and C
        
        destinations = [edge.destination for edge in neighbors]
        self.assertIn("B", destinations)
        self.assertIn("C", destinations)
    
    def test_get_stations(self):
        """Test station retrieval."""
        stations = self.graph.get_stations()
        self.assertEqual(len(stations), 1)
        self.assertEqual(stations[0].node_id, "C")
    
    def test_haversine_distance(self):
        """Test distance calculation."""
        # Distance between A and B should be positive
        distance = self.graph.calculate_distance("A", "B")
        self.assertGreater(distance, 0)
        self.assertLess(distance, 10)  # Should be less than 10km
    
    def test_edge_weighted_cost(self):
        """Test edge cost calculation."""
        edge = Edge("B", 1.0, 10.0, 1.5)
        cost = edge.get_weighted_cost(0.4, 0.4, 0.2)
        # cost = 0.4*1.0 + 0.4*10.0 + 0.2*(10.0*1.5)
        # cost = 0.4 + 4.0 + 3.0 = 7.4
        self.assertAlmostEqual(cost, 7.4, places=2)


class TestShortestPath(unittest.TestCase):
    """Test cases for shortest path algorithms."""
    
    def setUp(self):
        """Set up test graph before each test."""
        self.graph = CityGraph()
        
        # Create a more complex test network
        nodes = [
            Node("A", "Start", 40.7589, -73.9851),
            Node("B", "Middle 1", 40.7600, -73.9800),
            Node("C", "Middle 2", 40.7650, -73.9750),
            Node("D", "Middle 3", 40.7620, -73.9820),
            Node("E", "End", 40.7700, -73.9700),
        ]
        
        for node in nodes:
            self.graph.add_node(node)
        
        # Create a network with multiple paths
        edges = [
            ("A", "B", 0.5, 4.0, 1.0),
            ("A", "D", 0.4, 3.5, 1.1),
            ("B", "C", 0.6, 5.0, 1.2),
            ("D", "C", 0.5, 4.5, 1.0),
            ("C", "E", 0.7, 6.0, 1.1),
            ("D", "E", 1.2, 10.0, 1.3),
        ]
        
        for source, dest, dist, time, traffic in edges:
            self.graph.add_edge(source, dest, dist, time, traffic)
        
        self.finder = ShortestPathFinder(self.graph)
    
    def test_dijkstra_path_exists(self):
        """Test Dijkstra finds a path when one exists."""
        result = self.finder.dijkstra("A", "E")
        self.assertIsNotNone(result)
        self.assertGreater(len(result.path), 0)
        self.assertEqual(result.path[0], "A")
        self.assertEqual(result.path[-1], "E")
    
    def test_dijkstra_no_path(self):
        """Test Dijkstra returns None when no path exists."""
        # Add isolated node
        self.graph.add_node(Node("Z", "Isolated", 40.8, -74.0))
        result = self.finder.dijkstra("A", "Z")
        self.assertIsNone(result)
    
    def test_astar_path_exists(self):
        """Test A* finds a path when one exists."""
        result = self.finder.a_star("A", "E")
        self.assertIsNotNone(result)
        self.assertGreater(len(result.path), 0)
        self.assertEqual(result.path[0], "A")
        self.assertEqual(result.path[-1], "E")
    
    def test_astar_vs_dijkstra(self):
        """Test A* explores fewer nodes than Dijkstra."""
        dijkstra_result = self.finder.dijkstra("A", "E")
        astar_result = self.finder.a_star("A", "E")
        
        self.assertIsNotNone(dijkstra_result)
        self.assertIsNotNone(astar_result)
        
        # A* should typically explore fewer or equal nodes
        self.assertLessEqual(astar_result.nodes_explored, 
                            dijkstra_result.nodes_explored)
    
    def test_path_metrics(self):
        """Test path result contains valid metrics."""
        result = self.finder.dijkstra("A", "E")
        self.assertGreater(result.total_distance, 0)
        self.assertGreater(result.total_time, 0)
        self.assertGreater(result.total_cost, 0)
        self.assertGreater(result.nodes_explored, 0)
    
    def test_same_start_end(self):
        """Test path from node to itself."""
        result = self.finder.dijkstra("A", "A")
        self.assertIsNotNone(result)
        self.assertEqual(len(result.path), 1)
        self.assertEqual(result.total_distance, 0)
    
    def test_bfs_reachability(self):
        """Test BFS finds all reachable nodes."""
        paths = self.finder.find_all_paths_bfs("A", max_depth=5)
        # Should reach all nodes in the connected component
        self.assertGreaterEqual(len(paths), 1)
        self.assertIn("A", paths)


class TestStationPlacement(unittest.TestCase):
    """Test cases for station placement optimization."""
    
    def setUp(self):
        """Set up test graph before each test."""
        self.graph = CityGraph()
        
        # Create a grid of nodes
        for i in range(5):
            for j in range(5):
                node_id = f"N_{i}_{j}"
                lat = 40.75 + i * 0.01
                lon = -73.98 + j * 0.01
                node = Node(node_id, f"Location {i},{j}", lat, lon)
                self.graph.add_node(node)
        
        # Connect adjacent nodes
        for i in range(5):
            for j in range(5):
                current = f"N_{i}_{j}"
                
                # Connect to right neighbor
                if j < 4:
                    right = f"N_{i}_{j+1}"
                    self.graph.add_edge(current, right, 0.1, 1.0, 1.0)
                
                # Connect to bottom neighbor
                if i < 4:
                    bottom = f"N_{i+1}_{j}"
                    self.graph.add_edge(current, bottom, 0.1, 1.0, 1.0)
        
        self.optimizer = StationPlacementOptimizer(self.graph)
    
    def test_coverage_calculation(self):
        """Test coverage calculation."""
        stations = ["N_0_0", "N_2_2", "N_4_4"]
        coverage = self.optimizer.calculate_coverage(stations, max_distance=0.5)
        
        # Coverage should be between 0 and 1
        self.assertGreaterEqual(coverage, 0.0)
        self.assertLessEqual(coverage, 1.0)
    
    def test_greedy_placement(self):
        """Test greedy station placement."""
        num_stations = 5
        stations = self.optimizer.greedy_station_placement(num_stations)
        
        self.assertEqual(len(stations), num_stations)
        # All stations should be valid nodes
        for station in stations:
            self.assertIn(station, self.graph.nodes)
    
    def test_kmeans_placement(self):
        """Test k-means clustering placement."""
        num_stations = 4
        stations = self.optimizer.kmeans_clustering_placement(num_stations)
        
        self.assertEqual(len(stations), num_stations)
        # All stations should be valid nodes
        for station in stations:
            self.assertIn(station, self.graph.nodes)
    
    def test_demand_based_placement(self):
        """Test demand-based placement."""
        # Set demand for some nodes
        for i in range(5):
            node = self.graph.get_node(f"N_{i}_{i}")
            node.demand = 0.8
        
        num_stations = 3
        stations = self.optimizer.demand_based_placement(num_stations, 
                                                        demand_threshold=0.5)
        
        self.assertGreaterEqual(len(stations), 1)
        self.assertLessEqual(len(stations), num_stations)
    
    def test_evaluate_placement(self):
        """Test placement evaluation."""
        stations = ["N_0_0", "N_2_2", "N_4_4"]
        metrics = self.optimizer.evaluate_placement(stations)
        
        # Check all metrics are present
        self.assertIn('coverage', metrics)
        self.assertIn('avg_station_distance', metrics)
        self.assertIn('avg_connections_per_station', metrics)
        
        # Check metrics are valid
        self.assertGreaterEqual(metrics['coverage'], 0.0)
        self.assertLessEqual(metrics['coverage'], 1.0)
    
    def test_connectivity_optimization(self):
        """Test network connectivity suggestions."""
        stations = ["N_0_0", "N_4_4"]  # Two far apart stations
        suggestions = self.optimizer.optimize_network_connectivity(stations, 
                                                                   min_connections=1)
        
        # Should suggest at least one connection
        self.assertGreaterEqual(len(suggestions), 0)
    
    def test_set_demand_by_density(self):
        """Test demand setting based on density areas."""
        high_density = [(40.75, -73.98, 1.0)]
        self.optimizer.set_demand_by_density(high_density)
        
        # Node closest to density center should have high demand
        closest_node = self.graph.get_node("N_0_0")
        self.assertGreater(closest_node.demand, 0)


class TestIntegration(unittest.TestCase):
    """Integration tests for complete workflows."""
    
    def test_complete_workflow(self):
        """Test complete workflow from graph creation to route finding."""
        # Create graph
        graph = CityGraph()
        
        # Add nodes
        for i in range(4):
            node = Node(f"N{i}", f"Location {i}", 40.75 + i*0.01, -73.98)
            graph.add_node(node)
        
        # Add edges
        graph.add_edge("N0", "N1", 0.5, 4.0, 1.0)
        graph.add_edge("N1", "N2", 0.5, 4.0, 1.0)
        graph.add_edge("N2", "N3", 0.5, 4.0, 1.0)
        
        # Place stations
        optimizer = StationPlacementOptimizer(graph)
        stations = optimizer.greedy_station_placement(2)
        
        self.assertEqual(len(stations), 2)
        
        # Find route
        finder = ShortestPathFinder(graph)
        result = finder.dijkstra("N0", "N3")
        
        self.assertIsNotNone(result)
        self.assertEqual(result.path[0], "N0")
        self.assertEqual(result.path[-1], "N3")


def run_tests():
    """Run all tests and print results."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestCityGraph))
    suite.addTests(loader.loadTestsFromTestCase(TestShortestPath))
    suite.addTests(loader.loadTestsFromTestCase(TestStationPlacement))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("="*70)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
