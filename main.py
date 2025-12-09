"""
Main application for Bike-Sharing Station Planner System.
Demonstrates graph traversal, shortest path algorithms, and station placement.
"""

from graph import CityGraph, Node
from shortest_path import ShortestPathFinder
from station_placement import StationPlacementOptimizer
from visualization import NetworkVisualizer
import random


def create_sample_city() -> CityGraph:
    """
    Create a sample city network for demonstration.
    
    Returns:
        CityGraph with sample data
    """
    graph = CityGraph()
    
    # Create a grid-based city with some realistic coordinates
    # Using coordinates roughly around New York City area
    base_lat, base_lon = 40.7589, -73.9851  # Times Square area
    
    # Define locations (simulating a city grid)
    locations = [
        # Residential areas
        ("RES_01", "Residential Area North", 40.7700, -73.9900, False, 0),
        ("RES_02", "Residential Area East", 40.7650, -73.9700, False, 0),
        ("RES_03", "Residential Area South", 40.7500, -73.9850, False, 0),
        ("RES_04", "Residential Area West", 40.7600, -74.0000, False, 0),
        
        # Commercial areas
        ("COM_01", "Downtown Business District", 40.7589, -73.9851, False, 0),
        ("COM_02", "Shopping Center", 40.7620, -73.9780, False, 0),
        ("COM_03", "Office Complex", 40.7560, -73.9920, False, 0),
        
        # Parks and recreation
        ("PARK_01", "Central Park South", 40.7678, -73.9815, False, 0),
        ("PARK_02", "Riverside Park", 40.7700, -73.9950, False, 0),
        
        # Transit hubs
        ("TRAN_01", "Main Train Station", 40.7527, -73.9772, False, 0),
        ("TRAN_02", "Bus Terminal", 40.7570, -73.9900, False, 0),
        
        # Educational institutions
        ("EDU_01", "University Campus", 40.7630, -73.9840, False, 0),
        ("EDU_02", "College District", 40.7660, -73.9760, False, 0),
        
        # Hospital/Medical
        ("MED_01", "City Hospital", 40.7540, -73.9800, False, 0),
        
        # Entertainment
        ("ENT_01", "Theater District", 40.7580, -73.9860, False, 0),
        ("ENT_02", "Sports Arena", 40.7510, -73.9930, False, 0),
    ]
    
    # Add nodes to graph
    for node_id, name, lat, lon, is_station, capacity in locations:
        node = Node(node_id, name, lat, lon, is_station, capacity)
        graph.add_node(node)
    
    # Define connections (edges) with realistic distances and times
    connections = [
        # Residential connections
        ("RES_01", "PARK_01", 0.3, 2.5, 1.0),
        ("RES_01", "PARK_02", 0.4, 3.0, 1.1),
        ("RES_02", "COM_02", 0.4, 3.0, 1.2),
        ("RES_02", "EDU_02", 0.3, 2.0, 1.0),
        ("RES_03", "TRAN_01", 0.3, 2.5, 1.3),
        ("RES_03", "MED_01", 0.5, 4.0, 1.1),
        ("RES_04", "COM_03", 0.4, 3.0, 1.0),
        ("RES_04", "PARK_02", 0.3, 2.5, 1.0),
        
        # Commercial connections
        ("COM_01", "ENT_01", 0.2, 1.5, 1.5),
        ("COM_01", "TRAN_01", 0.3, 2.0, 1.6),
        ("COM_01", "COM_02", 0.4, 3.0, 1.4),
        ("COM_02", "EDU_01", 0.3, 2.0, 1.1),
        ("COM_03", "TRAN_02", 0.3, 2.0, 1.2),
        ("COM_03", "COM_01", 0.4, 3.0, 1.3),
        
        # Park connections
        ("PARK_01", "EDU_01", 0.3, 2.0, 1.0),
        ("PARK_01", "COM_01", 0.4, 3.0, 1.1),
        ("PARK_02", "PARK_01", 0.5, 4.0, 1.0),
        
        # Transit connections
        ("TRAN_01", "TRAN_02", 0.4, 3.0, 1.5),
        ("TRAN_01", "MED_01", 0.3, 2.0, 1.2),
        ("TRAN_02", "ENT_02", 0.4, 3.0, 1.3),
        
        # Educational connections
        ("EDU_01", "COM_01", 0.3, 2.5, 1.2),
        ("EDU_01", "EDU_02", 0.4, 3.0, 1.0),
        ("EDU_02", "PARK_01", 0.3, 2.0, 1.0),
        
        # Medical connections
        ("MED_01", "ENT_02", 0.4, 3.0, 1.1),
        
        # Entertainment connections
        ("ENT_01", "ENT_02", 0.5, 4.0, 1.4),
        ("ENT_01", "COM_02", 0.4, 3.0, 1.3),
        ("ENT_02", "COM_03", 0.3, 2.5, 1.2),
    ]
    
    # Add edges to graph
    for source, dest, distance, time, traffic in connections:
        graph.add_edge(source, dest, distance, time, traffic, bidirectional=True)
    
    return graph


def demo_shortest_path(graph: CityGraph):
    """Demonstrate shortest path algorithms."""
    print("\n" + "="*70)
    print("SHORTEST PATH ALGORITHMS DEMONSTRATION")
    print("="*70)
    
    finder = ShortestPathFinder(graph)
    visualizer = NetworkVisualizer(graph)
    
    # Example routes
    test_cases = [
        ("RES_01", "COM_01", "Residential North to Downtown"),
        ("EDU_01", "TRAN_01", "University to Train Station"),
        ("PARK_01", "MED_01", "Park to Hospital"),
    ]
    
    for start, end, description in test_cases:
        print(f"\n\n{'='*70}")
        print(f"Route: {description}")
        print(f"From: {graph.get_node(start).name}")
        print(f"To: {graph.get_node(end).name}")
        print("="*70)
        
        # Run Dijkstra's algorithm
        print("\n--- DIJKSTRA'S ALGORITHM ---")
        dijkstra_result = finder.dijkstra(start, end)
        
        if dijkstra_result:
            visualizer.print_route(dijkstra_result)
        else:
            print("No path found.")
        
        # Run A* algorithm
        print("\n--- A* ALGORITHM ---")
        astar_result = finder.a_star(start, end)
        
        if astar_result:
            visualizer.print_route(astar_result)
        else:
            print("No path found.")
        
        # Compare algorithms
        if dijkstra_result and astar_result:
            visualizer.compare_routes([
                ("Dijkstra", dijkstra_result),
                ("A*", astar_result)
            ])
            
            # Show ASCII map with path
            print("\nRoute Visualization:")
            visualizer.create_ascii_map(highlight_path=dijkstra_result.path)


def demo_station_placement(graph: CityGraph):
    """Demonstrate station placement optimization."""
    print("\n\n" + "="*70)
    print("STATION PLACEMENT OPTIMIZATION DEMONSTRATION")
    print("="*70)
    
    optimizer = StationPlacementOptimizer(graph)
    visualizer = NetworkVisualizer(graph)
    
    # Set realistic demand based on location type
    high_density_areas = [
        (40.7589, -73.9851, 1.0),  # Downtown (high demand)
        (40.7527, -73.9772, 0.9),  # Train station (high demand)
        (40.7630, -73.9840, 0.8),  # University (medium-high demand)
        (40.7678, -73.9815, 0.6),  # Park (medium demand)
    ]
    
    optimizer.set_demand_by_density(high_density_areas)
    
    print("\nDemand has been set based on high-density areas:")
    for lat, lon, density in high_density_areas:
        print(f"  - Location ({lat:.4f}, {lon:.4f}): Density {density:.2f}")
    
    # Test different placement algorithms
    num_stations = 6
    
    print(f"\n\n{'='*70}")
    print(f"PLACING {num_stations} BIKE STATIONS")
    print("="*70)
    
    # 1. Greedy placement
    print("\n--- METHOD 1: GREEDY COVERAGE ALGORITHM ---")
    greedy_stations = optimizer.greedy_station_placement(num_stations)
    print(f"\nSelected {len(greedy_stations)} stations using greedy algorithm:")
    visualizer.print_station_list(greedy_stations)
    
    greedy_metrics = optimizer.evaluate_placement(greedy_stations)
    print("\nEvaluation Metrics:")
    for metric, value in greedy_metrics.items():
        print(f"  {metric}: {value:.3f}")
    
    # 2. K-means clustering
    print("\n\n--- METHOD 2: K-MEANS CLUSTERING ALGORITHM ---")
    kmeans_stations = optimizer.kmeans_clustering_placement(num_stations)
    print(f"\nSelected {len(kmeans_stations)} stations using k-means clustering:")
    visualizer.print_station_list(kmeans_stations)
    
    kmeans_metrics = optimizer.evaluate_placement(kmeans_stations)
    print("\nEvaluation Metrics:")
    for metric, value in kmeans_metrics.items():
        print(f"  {metric}: {value:.3f}")
    
    # 3. Demand-based placement
    print("\n\n--- METHOD 3: DEMAND-BASED ALGORITHM ---")
    demand_stations = optimizer.demand_based_placement(num_stations, demand_threshold=0.3)
    print(f"\nSelected {len(demand_stations)} stations using demand-based algorithm:")
    visualizer.print_station_list(demand_stations)
    
    demand_metrics = optimizer.evaluate_placement(demand_stations)
    print("\nEvaluation Metrics:")
    for metric, value in demand_metrics.items():
        print(f"  {metric}: {value:.3f}")
    
    # Compare all methods
    print("\n\n" + "="*70)
    print("PLACEMENT ALGORITHM COMPARISON")
    print("="*70)
    
    print(f"\n{'Algorithm':<25} {'Coverage':<12} {'Avg Distance':<15} {'Connections':<12}")
    print("-" * 70)
    
    for name, metrics in [("Greedy Coverage", greedy_metrics),
                          ("K-Means Clustering", kmeans_metrics),
                          ("Demand-Based", demand_metrics)]:
        print(f"{name:<25} {metrics['coverage']:<12.3f} "
              f"{metrics['avg_station_distance']:<15.3f} "
              f"{metrics['avg_connections_per_station']:<12.3f}")
    
    # Use the best placement (greedy typically has best coverage)
    best_stations = greedy_stations
    
    # Mark nodes as stations
    for station_id in best_stations:
        node = graph.get_node(station_id)
        if node:
            node.is_station = True
            node.capacity = 20  # Each station can hold 20 bikes
    
    print("\n\nOptimal stations have been marked in the graph.")
    
    # Suggest connectivity improvements
    print("\n\n" + "="*70)
    print("NETWORK CONNECTIVITY ANALYSIS")
    print("="*70)
    
    suggested_edges = optimizer.optimize_network_connectivity(best_stations, min_connections=3)
    
    if suggested_edges:
        print(f"\nSuggesting {len(suggested_edges)} additional connections to improve network:")
        for i, (source, dest) in enumerate(suggested_edges[:10], 1):
            src_node = graph.get_node(source)
            dst_node = graph.get_node(dest)
            distance = graph.calculate_distance(source, dest)
            print(f"{i}. {src_node.name} ↔ {dst_node.name} ({distance:.2f} km)")
    else:
        print("\nNetwork connectivity is already optimal!")
    
    return best_stations


def demo_network_visualization(graph: CityGraph, station_ids: list):
    """Demonstrate network visualization."""
    print("\n\n" + "="*70)
    print("NETWORK VISUALIZATION")
    print("="*70)
    
    visualizer = NetworkVisualizer(graph)
    
    # Print complete network summary
    visualizer.print_network_summary()
    
    # Create ASCII map
    print("\n")
    visualizer.create_ascii_map()
    
    # Export to CSV
    csv_filename = "bike_sharing_network.csv"
    visualizer.export_to_csv(csv_filename)


def interactive_route_planner(graph: CityGraph):
    """Interactive route planning interface."""
    print("\n\n" + "="*70)
    print("INTERACTIVE ROUTE PLANNER")
    print("="*70)
    
    visualizer = NetworkVisualizer(graph)
    finder = ShortestPathFinder(graph)
    
    # Show available locations
    print("\nAvailable Locations:")
    print("-" * 70)
    nodes = list(graph.nodes.values())
    for i, node in enumerate(nodes, 1):
        station_mark = " [STATION]" if node.is_station else ""
        print(f"{i}. {node.name}{station_mark} (ID: {node.node_id})")
    
    print("\n\nExample routes you can try:")
    print("1. From Residential Area North to Downtown Business District")
    print("2. From University Campus to Train Station")
    print("3. From any residential area to a bike station")
    
    # Demo a few automatic routes
    example_routes = [
        ("RES_01", "COM_01"),
        ("EDU_01", "TRAN_01"),
    ]
    
    for start, end in example_routes:
        start_node = graph.get_node(start)
        end_node = graph.get_node(end)
        
        print(f"\n\n{'='*70}")
        print(f"Route from {start_node.name} to {end_node.name}")
        print("="*70)
        
        result = finder.dijkstra(start, end)
        if result:
            visualizer.print_route(result)
            visualizer.create_ascii_map(highlight_path=result.path)


def main():
    """Main entry point for the bike-sharing planner system."""
    print("="*70)
    print(" " * 10 + "BIKE-SHARING STATION PLANNER SYSTEM")
    print(" " * 15 + "Graph Algorithms & Optimization")
    print("="*70)
    
    print("\nInitializing city network...")
    graph = create_sample_city()
    
    print(f"✓ Created city graph with {graph.node_count()} locations")
    print(f"✓ Established {graph.edge_count()} connections")
    
    # Demo 1: Shortest Path Algorithms
    demo_shortest_path(graph)
    
    # Demo 2: Station Placement Optimization
    best_stations = demo_station_placement(graph)
    
    # Demo 3: Network Visualization
    demo_network_visualization(graph, best_stations)
    
    # Demo 4: Interactive Route Planner
    interactive_route_planner(graph)
    
    # Final summary
    print("\n\n" + "="*70)
    print("SYSTEM SUMMARY")
    print("="*70)
    
    print("\n✓ Implemented Graph Data Structure")
    print("  - Nodes represent locations (stations, intersections)")
    print("  - Weighted edges represent routes (distance, time, traffic)")
    
    print("\n✓ Shortest Path Algorithms")
    print("  - Dijkstra's Algorithm: Optimal path with weighted costs")
    print("  - A* Algorithm: Optimized search with heuristic guidance")
    
    print("\n✓ Station Placement Optimization")
    print("  - Greedy Coverage Algorithm: Maximizes area coverage")
    print("  - K-Means Clustering: Geographic distribution")
    print("  - Demand-Based Placement: Prioritizes high-demand areas")
    
    print("\n✓ Network Analysis & Visualization")
    print("  - Coverage analysis and connectivity optimization")
    print("  - ASCII map visualization")
    print("  - CSV export for external analysis")
    
    print("\n" + "="*70)
    print("System demonstration complete!")
    print("="*70)


if __name__ == "__main__":
    main()
