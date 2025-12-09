"""
Visualization module for bike-sharing system.
Creates visual representations of routes, stations, and network.
"""

from typing import List, Optional, Tuple
from graph import CityGraph, Node
from shortest_path import PathResult


class NetworkVisualizer:
    """Visualizes bike-sharing network and routes."""
    
    def __init__(self, graph: CityGraph):
        """
        Initialize the visualizer.
        
        Args:
            graph: The city graph to visualize
        """
        self.graph = graph
    
    def print_route(self, path_result: PathResult) -> None:
        """
        Print a formatted route description.
        
        Args:
            path_result: The path result to display
        """
        if not path_result or not path_result.path:
            print("No route found.")
            return
        
        print("\n" + "="*60)
        print("ROUTE INFORMATION")
        print("="*60)
        
        print(f"\nTotal Distance: {path_result.total_distance:.2f} km")
        print(f"Estimated Time: {path_result.total_time:.2f} minutes")
        print(f"Total Cost: {path_result.total_cost:.2f}")
        print(f"Nodes Explored: {path_result.nodes_explored}")
        
        print(f"\nRoute ({len(path_result.path)} stops):")
        print("-" * 60)
        
        for i, node_id in enumerate(path_result.path):
            node = self.graph.get_node(node_id)
            if node:
                station_marker = " [STATION]" if node.is_station else ""
                print(f"{i+1}. {node.name}{station_marker}")
                print(f"   Location: ({node.lat:.4f}, {node.lon:.4f})")
                
                # Print segment information
                if i < len(path_result.path) - 1:
                    next_node_id = path_result.path[i + 1]
                    # Find the edge
                    for edge in self.graph.get_neighbors(node_id):
                        if edge.destination == next_node_id:
                            print(f"   → Next: {edge.distance:.2f} km, "
                                  f"{edge.time:.1f} min, "
                                  f"traffic: {edge.traffic:.1f}x")
                            break
                print()
        
        print("="*60)
    
    def print_network_summary(self) -> None:
        """Print a summary of the entire network."""
        print("\n" + "="*60)
        print("NETWORK SUMMARY")
        print("="*60)
        
        stations = self.graph.get_stations()
        total_nodes = self.graph.node_count()
        total_edges = self.graph.edge_count()
        
        print(f"\nTotal Nodes: {total_nodes}")
        print(f"Bike Stations: {len(stations)}")
        print(f"Regular Intersections: {total_nodes - len(stations)}")
        print(f"Total Edges: {total_edges}")
        print(f"Average Connections per Node: {total_edges / total_nodes:.2f}")
        
        if stations:
            print("\n" + "-"*60)
            print("BIKE STATIONS:")
            print("-"*60)
            
            for station in stations:
                print(f"\n{station.name}")
                print(f"  ID: {station.node_id}")
                print(f"  Location: ({station.lat:.4f}, {station.lon:.4f})")
                print(f"  Capacity: {station.capacity} bikes")
                print(f"  Demand: {station.demand:.2f}")
                
                connections = self.graph.get_neighbors(station.node_id)
                print(f"  Connections: {len(connections)}")
        
        print("\n" + "="*60)
    
    def print_station_list(self, station_ids: List[str]) -> None:
        """
        Print a formatted list of stations.
        
        Args:
            station_ids: List of station node IDs
        """
        print("\n" + "="*60)
        print(f"STATION LIST ({len(station_ids)} stations)")
        print("="*60)
        
        for i, station_id in enumerate(station_ids, 1):
            node = self.graph.get_node(station_id)
            if node:
                print(f"\n{i}. {node.name}")
                print(f"   ID: {station_id}")
                print(f"   Location: ({node.lat:.4f}, {node.lon:.4f})")
                if node.is_station:
                    print(f"   Capacity: {node.capacity}")
                print(f"   Demand: {node.demand:.2f}")
        
        print("\n" + "="*60)
    
    def compare_routes(self, routes: List[Tuple[str, PathResult]]) -> None:
        """
        Compare multiple routes side by side.
        
        Args:
            routes: List of (algorithm_name, PathResult) tuples
        """
        print("\n" + "="*60)
        print("ROUTE COMPARISON")
        print("="*60)
        
        print(f"\n{'Algorithm':<20} {'Distance (km)':<15} {'Time (min)':<15} "
              f"{'Cost':<10} {'Nodes':<10}")
        print("-" * 70)
        
        for algo_name, result in routes:
            if result:
                print(f"{algo_name:<20} {result.total_distance:<15.2f} "
                      f"{result.total_time:<15.2f} {result.total_cost:<10.2f} "
                      f"{result.nodes_explored:<10}")
            else:
                print(f"{algo_name:<20} {'No path found'}")
        
        print("\n" + "="*60)
    
    def export_to_csv(self, filename: str) -> None:
        """
        Export network data to CSV file.
        
        Args:
            filename: Output CSV filename
        """
        import csv
        
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            
            # Write nodes
            writer.writerow(['Node Data'])
            writer.writerow(['ID', 'Name', 'Latitude', 'Longitude', 
                           'Is Station', 'Capacity', 'Demand'])
            
            for node in self.graph.get_all_nodes():
                writer.writerow([
                    node.node_id,
                    node.name,
                    node.lat,
                    node.lon,
                    node.is_station,
                    node.capacity,
                    node.demand
                ])
            
            writer.writerow([])
            
            # Write edges
            writer.writerow(['Edge Data'])
            writer.writerow(['Source', 'Destination', 'Distance (km)', 
                           'Time (min)', 'Traffic Factor'])
            
            for source_id, edges in self.graph.edges.items():
                for edge in edges:
                    writer.writerow([
                        source_id,
                        edge.destination,
                        edge.distance,
                        edge.time,
                        edge.traffic
                    ])
        
        print(f"\nNetwork data exported to {filename}")
    
    def create_ascii_map(self, highlight_path: Optional[List[str]] = None) -> None:
        """
        Create a simple ASCII visualization of the network.
        
        Args:
            highlight_path: Optional path to highlight
        """
        if not self.graph.nodes:
            print("Empty network")
            return
        
        # Find bounds
        lats = [node.lat for node in self.graph.nodes.values()]
        lons = [node.lon for node in self.graph.nodes.values()]
        
        min_lat, max_lat = min(lats), max(lats)
        min_lon, max_lon = min(lons), max(lons)
        
        # Create grid
        height, width = 20, 60
        grid = [[' ' for _ in range(width)] for _ in range(height)]
        
        # Map nodes to grid
        for node in self.graph.nodes.values():
            if max_lat != min_lat and max_lon != min_lon:
                y = int((node.lat - min_lat) / (max_lat - min_lat) * (height - 1))
                x = int((node.lon - min_lon) / (max_lon - min_lon) * (width - 1))
                
                y = height - 1 - y  # Flip y axis
                
                if node.is_station:
                    grid[y][x] = 'S'
                else:
                    grid[y][x] = '·'
        
        # Highlight path if provided
        if highlight_path:
            for node_id in highlight_path:
                node = self.graph.get_node(node_id)
                if node and max_lat != min_lat and max_lon != min_lon:
                    y = int((node.lat - min_lat) / (max_lat - min_lat) * (height - 1))
                    x = int((node.lon - min_lon) / (max_lon - min_lon) * (width - 1))
                    y = height - 1 - y
                    
                    if node_id == highlight_path[0]:
                        grid[y][x] = 'A'  # Start
                    elif node_id == highlight_path[-1]:
                        grid[y][x] = 'B'  # End
                    else:
                        grid[y][x] = '*'  # Path
        
        # Print grid
        print("\n" + "="*62)
        print("ASCII NETWORK MAP")
        print("="*62)
        print("Legend: S=Station, ·=Intersection, A=Start, B=End, *=Path")
        print("-"*62)
        
        for row in grid:
            print('|' + ''.join(row) + '|')
        
        print("-"*62)
        print(f"Coverage: Lat [{min_lat:.4f}, {max_lat:.4f}], "
              f"Lon [{min_lon:.4f}, {max_lon:.4f}]")
        print("="*62)
