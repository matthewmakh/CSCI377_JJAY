"""
Quick Start Guide - Bike-Sharing Station Planner System
========================================================

This guide will help you get started with the bike-sharing system quickly.
"""

# OPTION 1: Run the full demonstration
# This will show all features of the system

def run_full_demo():
    """
    Runs the complete demonstration including:
    - Shortest path algorithms (Dijkstra & A*)
    - Station placement optimization (3 methods)
    - Network visualization
    - Interactive route planning
    """
    import main
    main.main()


# OPTION 2: Create your own custom network
# This shows how to build a network from scratch

def create_custom_network():
    """Create a custom city network."""
    from graph import CityGraph, Node
    from shortest_path import ShortestPathFinder
    from visualization import NetworkVisualizer
    
    # Step 1: Create graph
    graph = CityGraph()
    
    # Step 2: Add locations
    locations = [
        ("home", "Home", 40.7580, -73.9855, False, 0),
        ("work", "Office", 40.7589, -73.9851, False, 0),
        ("gym", "Gym", 40.7600, -73.9840, True, 15),  # This is a station
        ("park", "Park", 40.7610, -73.9860, True, 20),  # This is a station
    ]
    
    for node_id, name, lat, lon, is_station, capacity in locations:
        node = Node(node_id, name, lat, lon, is_station, capacity)
        graph.add_node(node)
    
    # Step 3: Connect locations
    # Format: (source, destination, distance_km, time_minutes, traffic_factor)
    connections = [
        ("home", "work", 0.2, 2.0, 1.0),
        ("home", "park", 0.3, 3.0, 1.1),
        ("work", "gym", 0.25, 2.5, 1.2),
        ("gym", "park", 0.15, 1.5, 1.0),
    ]
    
    for source, dest, distance, time, traffic in connections:
        graph.add_edge(source, dest, distance, time, traffic, bidirectional=True)
    
    # Step 4: Find routes
    finder = ShortestPathFinder(graph)
    visualizer = NetworkVisualizer(graph)
    
    print("\n" + "="*60)
    print("Finding route from Home to Gym")
    print("="*60)
    
    result = finder.dijkstra("home", "gym")
    if result:
        visualizer.print_route(result)
        visualizer.create_ascii_map(highlight_path=result.path)
    
    return graph


# OPTION 3: Optimize station placement

def optimize_stations():
    """Demonstrate station placement optimization."""
    from graph import CityGraph, Node
    from station_placement import StationPlacementOptimizer
    from visualization import NetworkVisualizer
    
    # Create a simple grid city
    graph = CityGraph()
    
    # Add 3x3 grid of locations
    for i in range(3):
        for j in range(3):
            node_id = f"loc_{i}_{j}"
            name = f"Location ({i},{j})"
            lat = 40.75 + i * 0.01
            lon = -73.98 + j * 0.01
            
            node = Node(node_id, name, lat, lon, False, 0)
            graph.add_node(node)
    
    # Connect adjacent locations
    for i in range(3):
        for j in range(3):
            current = f"loc_{i}_{j}"
            
            if j < 2:  # Connect to right
                right = f"loc_{i}_{j+1}"
                graph.add_edge(current, right, 0.1, 1.0, 1.0)
            
            if i < 2:  # Connect to bottom
                bottom = f"loc_{i+1}_{j}"
                graph.add_edge(current, bottom, 0.1, 1.0, 1.0)
    
    # Optimize placement
    optimizer = StationPlacementOptimizer(graph)
    visualizer = NetworkVisualizer(graph)
    
    print("\n" + "="*60)
    print("STATION PLACEMENT OPTIMIZATION")
    print("="*60)
    
    # Try different algorithms
    num_stations = 3
    
    print(f"\nPlacing {num_stations} stations using greedy algorithm...")
    greedy_stations = optimizer.greedy_station_placement(num_stations)
    
    print("\nSelected stations:")
    visualizer.print_station_list(greedy_stations)
    
    # Evaluate placement
    metrics = optimizer.evaluate_placement(greedy_stations)
    print("\nEvaluation:")
    for metric, value in metrics.items():
        print(f"  {metric}: {value:.3f}")
    
    return graph, greedy_stations


# OPTION 4: Compare algorithms

def compare_algorithms():
    """Compare Dijkstra and A* algorithms."""
    from graph import CityGraph, Node
    from shortest_path import ShortestPathFinder
    from visualization import NetworkVisualizer
    
    # Create test network
    graph = CityGraph()
    
    # Add nodes in a line
    for i in range(5):
        node = Node(f"N{i}", f"Location {i}", 40.75 + i*0.01, -73.98)
        graph.add_node(node)
    
    # Connect sequentially
    for i in range(4):
        graph.add_edge(f"N{i}", f"N{i+1}", 0.5, 4.0, 1.0)
    
    # Find path using both algorithms
    finder = ShortestPathFinder(graph)
    visualizer = NetworkVisualizer(graph)
    
    print("\n" + "="*60)
    print("ALGORITHM COMPARISON")
    print("="*60)
    
    dijkstra_result = finder.dijkstra("N0", "N4")
    astar_result = finder.a_star("N0", "N4")
    
    visualizer.compare_routes([
        ("Dijkstra", dijkstra_result),
        ("A*", astar_result)
    ])
    
    print("\nKey Observations:")
    print(f"- Dijkstra explored {dijkstra_result.nodes_explored} nodes")
    print(f"- A* explored {astar_result.nodes_explored} nodes")
    print(f"- Both found paths with same cost: {dijkstra_result.total_cost:.2f}")
    print("- A* is typically more efficient due to heuristic guidance")


# OPTION 5: Quick test

def quick_test():
    """Quick test to verify everything works."""
    print("\n" + "="*60)
    print("QUICK SYSTEM TEST")
    print("="*60)
    
    from graph import CityGraph, Node
    from shortest_path import ShortestPathFinder
    
    # Create minimal network
    graph = CityGraph()
    graph.add_node(Node("A", "Start", 40.7, -73.9))
    graph.add_node(Node("B", "End", 40.71, -73.89))
    graph.add_edge("A", "B", 1.0, 10.0, 1.0)
    
    # Find path
    finder = ShortestPathFinder(graph)
    result = finder.dijkstra("A", "B")
    
    if result:
        print("✓ Graph creation: SUCCESS")
        print("✓ Shortest path: SUCCESS")
        print(f"✓ Distance: {result.total_distance:.2f} km")
        print(f"✓ Time: {result.total_time:.2f} minutes")
        print("\nSystem is working correctly!")
    else:
        print("✗ Test failed")


# =============================================================================
# MAIN - Choose what to run
# =============================================================================

if __name__ == "__main__":
    import sys
    
    print("\n" + "="*70)
    print("BIKE-SHARING SYSTEM - QUICK START GUIDE")
    print("="*70)
    print("\nChoose an option:")
    print("1. Run full demonstration")
    print("2. Create custom network")
    print("3. Optimize station placement")
    print("4. Compare algorithms")
    print("5. Quick test")
    print("0. Exit")
    
    # For automated demo, run option 5
    if len(sys.argv) == 1:
        print("\nRunning quick test...")
        quick_test()
        print("\n\nTo run full demo, use: python3 main.py")
        print("To see all options, edit quick_start.py\n")
    else:
        choice = input("\nEnter your choice (0-5): ")
        
        if choice == "1":
            run_full_demo()
        elif choice == "2":
            create_custom_network()
        elif choice == "3":
            optimize_stations()
        elif choice == "4":
            compare_algorithms()
        elif choice == "5":
            quick_test()
        elif choice == "0":
            print("Goodbye!")
        else:
            print("Invalid choice!")
