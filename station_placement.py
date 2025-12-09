"""
Station placement optimization module for bike-sharing system.
Uses clustering, coverage analysis, and demand-based algorithms.
"""

from typing import List, Set, Tuple, Dict
import math
from graph import CityGraph, Node


class StationPlacementOptimizer:
    """Optimizes bike station placement in a city network."""
    
    def __init__(self, graph: CityGraph):
        """
        Initialize the optimizer.
        
        Args:
            graph: The city graph
        """
        self.graph = graph
    
    def calculate_coverage(self, station_ids: List[str], 
                          max_distance: float = 0.5) -> float:
        """
        Calculate what percentage of nodes are covered by stations.
        
        Args:
            station_ids: List of station node IDs
            max_distance: Maximum walking distance in kilometers
        
        Returns:
            Coverage percentage (0.0 to 1.0)
        """
        if not self.graph.nodes:
            return 0.0
        
        covered_nodes = set()
        
        for node_id in self.graph.nodes.keys():
            for station_id in station_ids:
                distance = self.graph.calculate_distance(node_id, station_id)
                if distance <= max_distance:
                    covered_nodes.add(node_id)
                    break
        
        return len(covered_nodes) / len(self.graph.nodes)
    
    def greedy_station_placement(self, num_stations: int, 
                                 existing_stations: List[str] = None,
                                 max_coverage_distance: float = 0.5) -> List[str]:
        """
        Use greedy algorithm to select optimal station locations.
        Selects stations that maximize coverage at each step.
        
        Args:
            num_stations: Number of stations to place
            existing_stations: List of existing station IDs
            max_coverage_distance: Maximum walking distance for coverage
        
        Returns:
            List of selected station node IDs
        """
        if existing_stations is None:
            existing_stations = []
        
        selected_stations = existing_stations.copy()
        remaining_nodes = [node_id for node_id in self.graph.nodes.keys() 
                          if node_id not in selected_stations]
        
        for _ in range(num_stations - len(selected_stations)):
            if not remaining_nodes:
                break
            
            best_node = None
            best_coverage = -1
            
            # Try each remaining node and see which gives best coverage
            for candidate in remaining_nodes:
                test_stations = selected_stations + [candidate]
                coverage = self.calculate_coverage(test_stations, max_coverage_distance)
                
                if coverage > best_coverage:
                    best_coverage = coverage
                    best_node = candidate
            
            if best_node:
                selected_stations.append(best_node)
                remaining_nodes.remove(best_node)
        
        return selected_stations
    
    def kmeans_clustering_placement(self, num_stations: int,
                                    max_iterations: int = 100) -> List[str]:
        """
        Use k-means clustering to place stations at cluster centroids.
        
        Args:
            num_stations: Number of stations to place
            max_iterations: Maximum iterations for k-means
        
        Returns:
            List of selected station node IDs
        """
        nodes = list(self.graph.nodes.values())
        
        if len(nodes) < num_stations:
            return [node.node_id for node in nodes]
        
        # Initialize centroids randomly
        import random
        random.seed(42)
        centroids = random.sample(nodes, num_stations)
        
        for iteration in range(max_iterations):
            # Assign each node to nearest centroid
            clusters = [[] for _ in range(num_stations)]
            
            for node in nodes:
                min_dist = float('inf')
                closest_cluster = 0
                
                for i, centroid in enumerate(centroids):
                    dist = self._euclidean_distance(node, centroid)
                    if dist < min_dist:
                        min_dist = dist
                        closest_cluster = i
                
                clusters[closest_cluster].append(node)
            
            # Update centroids
            new_centroids = []
            converged = True
            
            for i, cluster in enumerate(clusters):
                if not cluster:
                    # Keep old centroid if cluster is empty
                    new_centroids.append(centroids[i])
                    continue
                
                # Calculate cluster center
                avg_lat = sum(node.lat for node in cluster) / len(cluster)
                avg_lon = sum(node.lon for node in cluster) / len(cluster)
                
                # Find node closest to center
                closest_node = min(cluster, 
                                  key=lambda n: math.sqrt(
                                      (n.lat - avg_lat)**2 + (n.lon - avg_lon)**2))
                new_centroids.append(closest_node)
                
                if closest_node.node_id != centroids[i].node_id:
                    converged = False
            
            centroids = new_centroids
            
            if converged:
                break
        
        return [centroid.node_id for centroid in centroids]
    
    def demand_based_placement(self, num_stations: int, 
                              demand_threshold: float = 0.5) -> List[str]:
        """
        Place stations based on demand at each location.
        
        Args:
            num_stations: Number of stations to place
            demand_threshold: Minimum demand threshold
        
        Returns:
            List of selected station node IDs
        """
        # Sort nodes by demand (descending)
        nodes_by_demand = sorted(self.graph.nodes.values(),
                                key=lambda n: n.demand,
                                reverse=True)
        
        # Filter by demand threshold
        high_demand_nodes = [node for node in nodes_by_demand 
                            if node.demand >= demand_threshold]
        
        # Select top num_stations
        selected = high_demand_nodes[:num_stations]
        
        # If not enough high-demand nodes, add more
        if len(selected) < num_stations:
            remaining = [node for node in nodes_by_demand 
                        if node not in selected]
            selected.extend(remaining[:num_stations - len(selected)])
        
        return [node.node_id for node in selected]
    
    def optimize_network_connectivity(self, station_ids: List[str],
                                     min_connections: int = 2) -> List[Tuple[str, str]]:
        """
        Suggest additional edges to improve network connectivity.
        
        Args:
            station_ids: List of station node IDs
            min_connections: Minimum connections per station
        
        Returns:
            List of (source, destination) tuples for suggested edges
        """
        suggested_edges = []
        
        for station_id in station_ids:
            current_connections = len([e for e in self.graph.get_neighbors(station_id)
                                      if e.destination in station_ids])
            
            if current_connections < min_connections:
                # Find nearest stations not yet connected
                distances = []
                for other_id in station_ids:
                    if other_id == station_id:
                        continue
                    
                    # Check if already connected
                    already_connected = any(e.destination == other_id 
                                          for e in self.graph.get_neighbors(station_id))
                    
                    if not already_connected:
                        dist = self.graph.calculate_distance(station_id, other_id)
                        distances.append((dist, other_id))
                
                # Suggest connections to nearest stations
                distances.sort()
                needed = min_connections - current_connections
                
                for i in range(min(needed, len(distances))):
                    suggested_edges.append((station_id, distances[i][1]))
        
        return suggested_edges
    
    def evaluate_placement(self, station_ids: List[str]) -> Dict[str, float]:
        """
        Evaluate the quality of station placement.
        
        Args:
            station_ids: List of station node IDs
        
        Returns:
            Dictionary with evaluation metrics
        """
        metrics = {}
        
        # Coverage metric
        metrics['coverage'] = self.calculate_coverage(station_ids, max_distance=0.5)
        
        # Average distance between stations
        if len(station_ids) > 1:
            distances = []
            for i, s1 in enumerate(station_ids):
                for s2 in station_ids[i+1:]:
                    distances.append(self.graph.calculate_distance(s1, s2))
            metrics['avg_station_distance'] = sum(distances) / len(distances)
            metrics['min_station_distance'] = min(distances)
            metrics['max_station_distance'] = max(distances)
        else:
            metrics['avg_station_distance'] = 0
            metrics['min_station_distance'] = 0
            metrics['max_station_distance'] = 0
        
        # Connectivity metric
        total_connections = sum(len([e for e in self.graph.get_neighbors(sid)
                                    if e.destination in station_ids])
                               for sid in station_ids)
        metrics['avg_connections_per_station'] = (total_connections / len(station_ids) 
                                                   if station_ids else 0)
        
        return metrics
    
    def _euclidean_distance(self, node1: Node, node2: Node) -> float:
        """Calculate Euclidean distance between two nodes."""
        return math.sqrt((node1.lat - node2.lat)**2 + 
                        (node1.lon - node2.lon)**2)
    
    def set_demand_by_density(self, high_density_areas: List[Tuple[float, float, float]]):
        """
        Set demand for nodes based on proximity to high-density areas.
        
        Args:
            high_density_areas: List of (lat, lon, density) tuples
        """
        for node in self.graph.nodes.values():
            max_density = 0
            
            for lat, lon, density in high_density_areas:
                dist = self.graph._haversine_distance(node.lat, node.lon, lat, lon)
                # Demand decreases with distance (inverse square law)
                if dist < 2.0:  # Within 2km
                    local_demand = density / (1 + dist**2)
                    max_density = max(max_density, local_demand)
            
            node.demand = max_density
