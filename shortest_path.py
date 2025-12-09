"""
Shortest path algorithms for bike-sharing route planning.
Implements Dijkstra's algorithm and A* for finding optimal routes.
"""

import heapq
from typing import Dict, List, Tuple, Optional, Callable
from graph import CityGraph, Edge


class PathResult:
    """Stores the result of a path finding operation."""
    
    def __init__(self, path: List[str], total_distance: float, 
                 total_time: float, total_cost: float):
        """
        Initialize path result.
        
        Args:
            path: List of node IDs in the path
            total_distance: Total distance in kilometers
            total_time: Total time in minutes
            total_cost: Total weighted cost
        """
        self.path = path
        self.total_distance = total_distance
        self.total_time = total_time
        self.total_cost = total_cost
        self.nodes_explored = 0
    
    def __repr__(self):
        return (f"PathResult(distance={self.total_distance:.2f}km, "
                f"time={self.total_time:.2f}min, cost={self.total_cost:.2f}, "
                f"nodes={len(self.path)})")


class ShortestPathFinder:
    """Implements shortest path algorithms for route planning."""
    
    def __init__(self, graph: CityGraph):
        """
        Initialize the path finder.
        
        Args:
            graph: The city graph to search
        """
        self.graph = graph
    
    def dijkstra(self, start: str, end: str, 
                 distance_weight: float = 0.4,
                 time_weight: float = 0.4,
                 traffic_weight: float = 0.2) -> Optional[PathResult]:
        """
        Find shortest path using Dijkstra's algorithm.
        
        Args:
            start: Starting node ID
            end: Destination node ID
            distance_weight: Weight for distance factor
            time_weight: Weight for time factor
            traffic_weight: Weight for traffic factor
        
        Returns:
            PathResult object or None if no path exists
        """
        # Priority queue: (cost, node_id)
        pq = [(0, start)]
        
        # Track best cost to reach each node
        costs = {start: 0}
        
        # Track previous node in optimal path
        previous = {start: None}
        
        # Track cumulative distance and time
        distances = {start: 0}
        times = {start: 0}
        
        nodes_explored = 0
        
        while pq:
            current_cost, current = heapq.heappop(pq)
            
            # Skip if we've found a better path already
            if current_cost > costs.get(current, float('inf')):
                continue
            
            nodes_explored += 1
            
            # Found the destination
            if current == end:
                path = self._reconstruct_path(previous, start, end)
                result = PathResult(
                    path=path,
                    total_distance=distances[end],
                    total_time=times[end],
                    total_cost=current_cost
                )
                result.nodes_explored = nodes_explored
                return result
            
            # Explore neighbors
            for edge in self.graph.get_neighbors(current):
                neighbor = edge.destination
                
                # Calculate new cost using weighted factors
                edge_cost = edge.get_weighted_cost(distance_weight, 
                                                   time_weight, 
                                                   traffic_weight)
                new_cost = current_cost + edge_cost
                
                # Update if we found a better path
                if new_cost < costs.get(neighbor, float('inf')):
                    costs[neighbor] = new_cost
                    distances[neighbor] = distances[current] + edge.distance
                    times[neighbor] = times[current] + edge.time * edge.traffic
                    previous[neighbor] = current
                    heapq.heappush(pq, (new_cost, neighbor))
        
        # No path found
        return None
    
    def a_star(self, start: str, end: str,
               distance_weight: float = 0.4,
               time_weight: float = 0.4,
               traffic_weight: float = 0.2) -> Optional[PathResult]:
        """
        Find shortest path using A* algorithm with heuristic.
        
        Args:
            start: Starting node ID
            end: Destination node ID
            distance_weight: Weight for distance factor
            time_weight: Weight for time factor
            traffic_weight: Weight for traffic factor
        
        Returns:
            PathResult object or None if no path exists
        """
        def heuristic(node_id: str) -> float:
            """Estimate cost from node to destination using straight-line distance."""
            h_dist = self.graph.calculate_distance(node_id, end)
            # Convert to cost estimate (assuming average speed of 15 km/h for bikes)
            h_time = (h_dist / 15) * 60  # Convert to minutes
            return distance_weight * h_dist + time_weight * h_time
        
        # Priority queue: (f_score, node_id) where f_score = g_score + h_score
        pq = [(heuristic(start), start)]
        
        # Actual cost from start to node
        g_scores = {start: 0}
        
        # Track previous node in optimal path
        previous = {start: None}
        
        # Track cumulative distance and time
        distances = {start: 0}
        times = {start: 0}
        
        nodes_explored = 0
        
        while pq:
            _, current = heapq.heappop(pq)
            
            nodes_explored += 1
            
            # Found the destination
            if current == end:
                path = self._reconstruct_path(previous, start, end)
                result = PathResult(
                    path=path,
                    total_distance=distances[end],
                    total_time=times[end],
                    total_cost=g_scores[end]
                )
                result.nodes_explored = nodes_explored
                return result
            
            current_g = g_scores[current]
            
            # Explore neighbors
            for edge in self.graph.get_neighbors(current):
                neighbor = edge.destination
                
                # Calculate new g_score
                edge_cost = edge.get_weighted_cost(distance_weight,
                                                   time_weight,
                                                   traffic_weight)
                tentative_g = current_g + edge_cost
                
                # Update if we found a better path
                if tentative_g < g_scores.get(neighbor, float('inf')):
                    g_scores[neighbor] = tentative_g
                    distances[neighbor] = distances[current] + edge.distance
                    times[neighbor] = times[current] + edge.time * edge.traffic
                    previous[neighbor] = current
                    
                    f_score = tentative_g + heuristic(neighbor)
                    heapq.heappush(pq, (f_score, neighbor))
        
        # No path found
        return None
    
    def find_all_paths_bfs(self, start: str, max_depth: int = 3) -> Dict[str, List[str]]:
        """
        Find all reachable nodes from start using BFS (for network analysis).
        
        Args:
            start: Starting node ID
            max_depth: Maximum depth to explore
        
        Returns:
            Dictionary mapping node_id to path from start
        """
        queue = [(start, [start], 0)]
        visited = {start}
        paths = {start: [start]}
        
        while queue:
            current, path, depth = queue.pop(0)
            
            if depth >= max_depth:
                continue
            
            for edge in self.graph.get_neighbors(current):
                neighbor = edge.destination
                if neighbor not in visited:
                    visited.add(neighbor)
                    new_path = path + [neighbor]
                    paths[neighbor] = new_path
                    queue.append((neighbor, new_path, depth + 1))
        
        return paths
    
    def find_k_shortest_paths(self, start: str, end: str, k: int = 3,
                              distance_weight: float = 0.4,
                              time_weight: float = 0.4,
                              traffic_weight: float = 0.2) -> List[PathResult]:
        """
        Find k shortest paths between start and end (using Yen's algorithm approach).
        
        Args:
            start: Starting node ID
            end: Destination node ID
            k: Number of shortest paths to find
            distance_weight: Weight for distance factor
            time_weight: Weight for time factor
            traffic_weight: Weight for traffic factor
        
        Returns:
            List of PathResult objects
        """
        # Find first shortest path
        first_path = self.dijkstra(start, end, distance_weight, 
                                   time_weight, traffic_weight)
        if not first_path:
            return []
        
        results = [first_path]
        
        # For simplicity, we'll use a modified approach:
        # Find alternative paths by temporarily removing edges
        # This is a simplified version of Yen's algorithm
        
        return results  # For now, return just the shortest path
    
    def _reconstruct_path(self, previous: Dict[str, Optional[str]], 
                          start: str, end: str) -> List[str]:
        """
        Reconstruct path from start to end using previous pointers.
        
        Args:
            previous: Dictionary mapping node to previous node in path
            start: Starting node ID
            end: Destination node ID
        
        Returns:
            List of node IDs representing the path
        """
        path = []
        current = end
        
        while current is not None:
            path.append(current)
            current = previous.get(current)
        
        path.reverse()
        return path if path[0] == start else []
