# Graph data structure for city bike network
# Weighted edges with distance, time, and traffic

import math
from typing import Dict, List, Tuple, Optional, Set


class Edge:
    # Edge between two locations
    def __init__(self, destination: str, distance: float, time: float, traffic: float):
        self.destination = destination
        self.distance = distance  # km
        self.time = time  # minutes
        self.traffic = traffic  # multiplier (1.0 = normal, 2.0 = heavy)
    
    def get_weighted_cost(self, distance_weight: float = 0.4, 
                          time_weight: float = 0.4, 
                          traffic_weight: float = 0.2) -> float:
        # calculate combined cost using weights
        return (distance_weight * self.distance + 
                time_weight * self.time + 
                traffic_weight * (self.time * self.traffic))


class Node:
    # Location node (station or intersection)
    def __init__(self, node_id: str, name: str, lat: float, lon: float, 
                 is_station: bool = False, capacity: int = 0):
        self.node_id = node_id
        self.name = name
        self.lat = lat
        self.lon = lon
        self.is_station = is_station
        self.capacity = capacity
        self.demand = 0.0
    
    def __repr__(self):
        return f"Node({self.node_id}, {self.name}, station={self.is_station})"


class CityGraph:
    # main graph class
    def __init__(self):
        self.nodes: Dict[str, Node] = {}
        self.edges: Dict[str, List[Edge]] = {}
    
    def add_node(self, node: Node) -> None:
        self.nodes[node.node_id] = node
        if node.node_id not in self.edges:
            self.edges[node.node_id] = []
    
    def add_edge(self, source: str, destination: str, distance: float, 
                 time: float, traffic: float = 1.0, bidirectional: bool = True) -> None:
        # add edge, can be one-way or two-way
        if source not in self.edges:
            self.edges[source] = []
        
        self.edges[source].append(Edge(destination, distance, time, traffic))
        
        if bidirectional:
            if destination not in self.edges:
                self.edges[destination] = []
            self.edges[destination].append(Edge(source, distance, time, traffic))
    
    def get_neighbors(self, node_id: str) -> List[Edge]:
        return self.edges.get(node_id, [])
    
    def get_node(self, node_id: str) -> Optional[Node]:
        return self.nodes.get(node_id)
    
    def get_stations(self) -> List[Node]:
        return [node for node in self.nodes.values() if node.is_station]
    
    def calculate_distance(self, node1_id: str, node2_id: str) -> float:
        # haversine distance between two nodes
        node1 = self.nodes.get(node1_id)
        node2 = self.nodes.get(node2_id)
        
        if not node1 or not node2:
            return float('inf')
        
        return self._haversine_distance(node1.lat, node1.lon, node2.lat, node2.lon)
    
    @staticmethod
    def _haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        # calculate great circle distance
        R = 6371  # earth radius in km
        
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
        return list(self.nodes.values())
    
    def node_count(self) -> int:
        return len(self.nodes)
    
    def edge_count(self) -> int:
        return sum(len(edges) for edges in self.edges.values())
    
    def __repr__(self):
        return f"CityGraph(nodes={self.node_count()}, edges={self.edge_count()})"
