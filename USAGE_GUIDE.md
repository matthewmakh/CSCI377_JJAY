# USAGE GUIDE: Bike-Sharing Station Planner System

## Quick Start (30 seconds)

```bash
# Run the complete demonstration
python3 main.py

# Run tests to verify everything works
python3 test_bike_system.py

# Run quick test
python3 quick_start.py
```

## Detailed Usage Instructions

### 1. Running the Full Demo

The main demonstration shows all features of the system:

```bash
python3 main.py
```

**What you'll see:**

1. **Shortest Path Algorithms Demo**
   - 3 example routes with different characteristics
   - Both Dijkstra and A* algorithms
   - Performance comparison
   - ASCII map visualization

2. **Station Placement Optimization**
   - 3 different algorithms (Greedy, K-Means, Demand-based)
   - Coverage analysis
   - Connectivity suggestions
   - Algorithm comparison

3. **Network Visualization**
   - Complete network summary
   - Station list with details
   - ASCII map of network
   - CSV export

4. **Interactive Route Planning**
   - Example routes between various locations
   - Step-by-step directions

**Expected Output Length:** ~500-1000 lines
**Run Time:** ~1-2 seconds

---

### 2. Using as a Library

#### Example 1: Create a Simple Network and Find Route

```python
from graph import CityGraph, Node
from shortest_path import ShortestPathFinder
from visualization import NetworkVisualizer

# Create graph
graph = CityGraph()

# Add locations
home = Node("home", "My Home", 40.7589, -73.9851, False, 0)
work = Node("work", "My Office", 40.7600, -73.9800, True, 20)
gym = Node("gym", "Gym", 40.7650, -73.9750, True, 15)

graph.add_node(home)
graph.add_node(work)
graph.add_node(gym)

# Connect locations (source, dest, distance_km, time_min, traffic_factor)
graph.add_edge("home", "work", 0.5, 4.0, 1.0, bidirectional=True)
graph.add_edge("work", "gym", 0.6, 5.0, 1.2, bidirectional=True)
graph.add_edge("home", "gym", 0.9, 7.5, 1.1, bidirectional=True)

# Find shortest path
finder = ShortestPathFinder(graph)
result = finder.dijkstra("home", "gym")

# Display result
visualizer = NetworkVisualizer(graph)
visualizer.print_route(result)
```

#### Example 2: Optimize Station Placement

```python
from graph import CityGraph, Node
from station_placement import StationPlacementOptimizer
from visualization import NetworkVisualizer

# Create graph with many locations
graph = CityGraph()

# Add 25 locations in a 5x5 grid
for i in range(5):
    for j in range(5):
        node_id = f"loc_{i}_{j}"
        name = f"Location {i},{j}"
        lat = 40.75 + i * 0.01
        lon = -73.98 + j * 0.01
        
        node = Node(node_id, name, lat, lon, False, 0)
        graph.add_node(node)

# Connect adjacent locations
for i in range(5):
    for j in range(5):
        current = f"loc_{i}_{j}"
        
        # Connect to right neighbor
        if j < 4:
            right = f"loc_{i}_{j+1}"
            graph.add_edge(current, right, 0.1, 1.0, 1.0)
        
        # Connect to bottom neighbor
        if i < 4:
            bottom = f"loc_{i+1}_{j}"
            graph.add_edge(current, bottom, 0.1, 1.0, 1.0)

# Optimize station placement
optimizer = StationPlacementOptimizer(graph)

# Try greedy algorithm
num_stations = 5
stations = optimizer.greedy_station_placement(num_stations)

print(f"Placed {len(stations)} stations:")
for station_id in stations:
    node = graph.get_node(station_id)
    print(f"  - {node.name} at ({node.lat:.4f}, {node.lon:.4f})")

# Evaluate placement
metrics = optimizer.evaluate_placement(stations)
print(f"\nCoverage: {metrics['coverage']*100:.1f}%")
print(f"Average distance between stations: {metrics['avg_station_distance']:.3f} km")
```

#### Example 3: Compare Algorithms

```python
from graph import CityGraph, Node
from shortest_path import ShortestPathFinder
from visualization import NetworkVisualizer

# Create graph (reuse from Example 1)
# ... graph creation code ...

finder = ShortestPathFinder(graph)
visualizer = NetworkVisualizer(graph)

# Compare Dijkstra and A*
dijkstra_result = finder.dijkstra("home", "gym")
astar_result = finder.a_star("home", "gym")

# Display comparison
visualizer.compare_routes([
    ("Dijkstra", dijkstra_result),
    ("A*", astar_result)
])

print("\nObservations:")
print(f"Dijkstra explored {dijkstra_result.nodes_explored} nodes")
print(f"A* explored {astar_result.nodes_explored} nodes")
print(f"A* was {dijkstra_result.nodes_explored / astar_result.nodes_explored:.1f}x more efficient")
```

#### Example 4: Set Demand and Optimize

```python
from station_placement import StationPlacementOptimizer

# Create optimizer (assume graph already created)
optimizer = StationPlacementOptimizer(graph)

# Define high-density areas (lat, lon, density_value)
high_density_areas = [
    (40.7589, -73.9851, 1.0),   # Downtown - very high
    (40.7630, -73.9840, 0.8),   # University - high
    (40.7700, -73.9900, 0.6),   # Residential - medium
]

# Set demand based on density
optimizer.set_demand_by_density(high_density_areas)

# Place stations based on demand
stations = optimizer.demand_based_placement(6, demand_threshold=0.3)

# Show stations with their demand
for station_id in stations:
    node = graph.get_node(station_id)
    print(f"{node.name}: demand = {node.demand:.3f}")
```

---

### 3. Understanding the Weights

The system uses a weighted cost function to find optimal routes:

```python
cost = distance_weight * distance + 
       time_weight * time + 
       traffic_weight * (time * traffic_factor)
```

**Default weights:**
- Distance: 40% (0.4)
- Time: 40% (0.4)  
- Traffic: 20% (0.2)

**Customize weights:**

```python
# Prioritize speed over distance
result = finder.dijkstra("start", "end",
                         distance_weight=0.2,  # Less important
                         time_weight=0.6,       # More important
                         traffic_weight=0.2)

# Avoid traffic at all costs
result = finder.dijkstra("start", "end",
                         distance_weight=0.3,
                         time_weight=0.2,
                         traffic_weight=0.5)    # Most important
```

---

### 4. Working with Real Data

#### Loading from CSV (example structure)

```python
import csv
from graph import CityGraph, Node

def load_graph_from_csv(nodes_file, edges_file):
    graph = CityGraph()
    
    # Load nodes
    with open(nodes_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            node = Node(
                node_id=row['id'],
                name=row['name'],
                lat=float(row['lat']),
                lon=float(row['lon']),
                is_station=row['is_station'].lower() == 'true',
                capacity=int(row['capacity'])
            )
            graph.add_node(node)
    
    # Load edges
    with open(edges_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            graph.add_edge(
                source=row['source'],
                destination=row['destination'],
                distance=float(row['distance']),
                time=float(row['time']),
                traffic=float(row['traffic']),
                bidirectional=True
            )
    
    return graph

# Usage
graph = load_graph_from_csv('nodes.csv', 'edges.csv')
```

**Expected CSV format for nodes:**
```csv
id,name,lat,lon,is_station,capacity
A,Location A,40.7589,-73.9851,false,0
B,Station B,40.7600,-73.9800,true,20
```

**Expected CSV format for edges:**
```csv
source,destination,distance,time,traffic
A,B,0.5,4.0,1.0
B,C,0.6,5.0,1.2
```

---

### 5. Advanced Usage

#### Custom Heuristic for A*

If you want to modify the A* heuristic:

```python
# In shortest_path.py, modify the heuristic function in a_star method

def heuristic(node_id: str) -> float:
    # Custom heuristic: consider elevation or other factors
    h_dist = self.graph.calculate_distance(node_id, end)
    
    # Example: penalize uphill routes
    elevation_penalty = get_elevation_difference(node_id, end)
    
    return distance_weight * h_dist + elevation_penalty
```

#### Multi-Criteria Optimization

```python
# Find multiple routes and let user choose
finder = ShortestPathFinder(graph)

# Fastest route (prioritize time)
fastest = finder.dijkstra("A", "B", 
                          distance_weight=0.2, 
                          time_weight=0.7, 
                          traffic_weight=0.1)

# Shortest route (prioritize distance)
shortest = finder.dijkstra("A", "B",
                           distance_weight=0.8,
                           time_weight=0.1,
                           traffic_weight=0.1)

# Traffic-avoiding route
traffic_free = finder.dijkstra("A", "B",
                               distance_weight=0.2,
                               time_weight=0.2,
                               traffic_weight=0.6)

# Present options
print("Option 1 (Fastest):", fastest.total_time, "minutes")
print("Option 2 (Shortest):", shortest.total_distance, "km")
print("Option 3 (Avoid Traffic):", traffic_free.total_time * traffic_free.traffic)
```

---

### 6. Troubleshooting

#### Problem: No path found

```python
result = finder.dijkstra("A", "Z")
if result is None:
    print("No path exists between these locations")
    
    # Check if nodes exist
    if not graph.get_node("A"):
        print("Start node doesn't exist")
    if not graph.get_node("Z"):
        print("End node doesn't exist")
    
    # Check connectivity
    paths = finder.find_all_paths_bfs("A", max_depth=10)
    if "Z" not in paths:
        print("Z is not reachable from A")
```

#### Problem: Unexpected route

```python
# Visualize to debug
result = finder.dijkstra("A", "Z")
visualizer.print_route(result)
visualizer.create_ascii_map(highlight_path=result.path)

# Check edge weights
for node_id in result.path[:-1]:
    edges = graph.get_neighbors(node_id)
    for edge in edges:
        print(f"{node_id} -> {edge.destination}: "
              f"dist={edge.distance}, time={edge.time}, traffic={edge.traffic}")
```

---

### 7. Performance Tips

1. **For large graphs:** Use A* instead of Dijkstra
   ```python
   result = finder.a_star(start, end)  # Faster for large graphs
   ```

2. **For station placement:** Use greedy with limited candidates
   ```python
   # Pre-filter high-demand nodes
   high_demand_nodes = [n.node_id for n in graph.nodes.values() 
                        if n.demand > 0.5]
   stations = optimizer.greedy_station_placement(
       num_stations=10,
       existing_stations=high_demand_nodes[:2]
   )
   ```

3. **For repeated queries:** Cache distance calculations
   ```python
   # Pre-compute all-pairs distances for small graphs
   distances = {}
   for n1 in graph.nodes:
       for n2 in graph.nodes:
           if n1 != n2:
               distances[(n1, n2)] = graph.calculate_distance(n1, n2)
   ```

---

### 8. Export and Visualization

#### Export to CSV

```python
visualizer = NetworkVisualizer(graph)
visualizer.export_to_csv("my_network.csv")
```

#### Create reports

```python
# Generate comprehensive report
with open("network_report.txt", "w") as f:
    import sys
    sys.stdout = f  # Redirect output to file
    
    visualizer.print_network_summary()
    
    # Test multiple routes
    for start, end in route_pairs:
        result = finder.dijkstra(start, end)
        visualizer.print_route(result)
    
    sys.stdout = sys.__stdout__  # Reset output

print("Report saved to network_report.txt")
```

---

## Command Reference

### Key Classes and Methods

**CityGraph**
- `add_node(node)` - Add a location
- `add_edge(src, dst, dist, time, traffic)` - Connect locations
- `get_neighbors(node_id)` - Get connections
- `calculate_distance(n1, n2)` - Haversine distance
- `get_stations()` - Get all bike stations

**ShortestPathFinder**
- `dijkstra(start, end, weights...)` - Find optimal path
- `a_star(start, end, weights...)` - Find path with heuristic
- `find_all_paths_bfs(start, max_depth)` - Network reachability

**StationPlacementOptimizer**
- `greedy_station_placement(num)` - Maximize coverage
- `kmeans_clustering_placement(num)` - Balanced distribution
- `demand_based_placement(num, threshold)` - High-demand areas
- `evaluate_placement(stations)` - Get metrics
- `set_demand_by_density(areas)` - Set demand values

**NetworkVisualizer**
- `print_route(result)` - Display route details
- `print_network_summary()` - Show network stats
- `compare_routes(list)` - Compare algorithms
- `create_ascii_map(path)` - Visual map
- `export_to_csv(filename)` - Export data

---

## Need Help?

- **Check examples:** Run `python3 main.py` for comprehensive examples
- **Read tests:** See `test_bike_system.py` for usage patterns
- **Quick start:** Run `python3 quick_start.py` for interactive guide
- **Documentation:** See README.md and ARCHITECTURE.md

---

**Happy Route Planning! 🚴‍♂️**
