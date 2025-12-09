"""
Graph data structure for representing city network with bike-sharing stations.
Supports weighted edges for distance, time, and traffic factors.
"""

import math
from typing import Dict, List, Tuple, Optional, Set


class Edge:
    """Represents a weighted edge between two locations."""
    
    def __init__(self, destination: str, distance: float, time: float, traffic: float):
        """
        Initialize an edge.
        
        Args:
            destination: The destination node ID
            distance: Distance in kilometers
            time: Time in minutes
            traffic: Traffic factor (1.0 = no traffic, 2.0 = double time)
        """
        self.destination = destination
        self.distance = distance
        self.time = time
        self.traffic = traffic
    
    def get_weighted_cost(self, distance_weight: float = 0.4, 
                          time_weight: float = 0.4, 
                          traffic_weight: float = 0.2) -> float:
        """
        Calculate weighted cost considering all factors.
        
        Args:
            distance_weight: Weight for distance factor
            time_weight: Weight for time factor
            traffic_weight: Weight for traffic factor
        
        Returns:
            Combined weighted cost
        """
        return (distance_weight * self.distance + 
                time_weight * self.time + 
                traffic_weight * (self.time * self.traffic))


class Node:
    """Represents a location (bike station or intersection) in the city."""
    
    def __init__(self, node_id: str, name: str, lat: float, lon: float, 
                 is_station: bool = False, capacity: int = 0):
        """
        Initialize a node.
        
        Args:
            node_id: Unique identifier for the node
            name: Human-readable name
            lat: Latitude coordinate
            lon: Longitude coordinate
            is_station: Whether this is a bike station
            capacity: Number of bikes the station can hold
        """
        self.node_id = node_id
        self.name = name
        self.lat = lat
        self.lon = lon
        self.is_station = is_station
        self.capacity = capacity
        self.demand = 0.0  # Estimated demand for this location
    
    def __repr__(self):
        return f"Node({self.node_id}, {self.name}, station={self.is_station})"


class CityGraph:
    """Graph representation of city network for bike-sharing system."""
    
    def __init__(self):
        """Initialize an empty city graph."""
        self.nodes: Dict[str, Node] = {}
        self.edges: Dict[str, List[Edge]] = {}
    
    def add_node(self, node: Node) -> None:
        """Add a node to the graph."""
        self.nodes[node.node_id] = node
        if node.node_id not in self.edges:
            self.edges[node.node_id] = []
    
    def add_edge(self, source: str, destination: str, distance: float, 
                 time: float, traffic: float = 1.0, bidirectional: bool = True) -> None:
        """
        Add an edge between two nodes.
        
        Args:
            source: Source node ID
            destination: Destination node ID
            distance: Distance in kilometers
            time: Time in minutes
            traffic: Traffic factor
            bidirectional: Whether to create edge in both directions
        """
        if source not in self.edges:
            self.edges[source] = []
        
        self.edges[source].append(Edge(destination, distance, time, traffic))
        
        if bidirectional:
            if destination not in self.edges:
                self.edges[destination] = []
            self.edges[destination].append(Edge(source, distance, time, traffic))
    
    def get_neighbors(self, node_id: str) -> List[Edge]:
        """Get all edges from a given node."""
        return self.edges.get(node_id, [])
    
    def get_node(self, node_id: str) -> Optional[Node]:
        """Get a node by its ID."""
        return self.nodes.get(node_id)
    
    def get_stations(self) -> List[Node]:
        """Get all bike station nodes."""
        return [node for node in self.nodes.values() if node.is_station]
    
    def calculate_distance(self, node1_id: str, node2_id: str) -> float:
        """
        Calculate haversine distance between two nodes.
        
        Args:
            node1_id: First node ID
            node2_id: Second node ID
        
        Returns:
            Distance in kilometers
        """
        node1 = self.nodes.get(node1_id)
        node2 = self.nodes.get(node2_id)
        
        if not node1 or not node2:
            return float('inf')
        
        return self._haversine_distance(node1.lat, node1.lon, node2.lat, node2.lon)
    
    @staticmethod
    def _haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculate the great circle distance between two points on Earth.
        
        Args:
            lat1, lon1: Coordinates of first point
            lat2, lon2: Coordinates of second point
        
        Returns:
            Distance in kilometers
        """
        R = 6371  # Earth's radius in kilometers
        
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lon = math.radians(lon2 - lon1)
        
        a = (math.sin(delta_lat / 2) ** 2 +
             math.cos(lat1_rad) * math.cos(lat2_rad) *
             math.sin(delta_lon / 2) ** 2)
        c = 2 * math.asin(math.sqrt(a))
        
        return R * c
    
    def get_all_nodes(self) -> List[Node]:
        """Get all nodes in the graph."""
        return list(self.nodes.values())
    
    def node_count(self) -> int:
        """Get the number of nodes in the graph."""
        return len(self.nodes)
    
    def edge_count(self) -> int:
        """Get the total number of edges in the graph."""
        return sum(len(edges) for edges in self.edges.values())
    
    def __repr__(self):
        return f"CityGraph(nodes={self.node_count()}, edges={self.edge_count()})"
