# Bike-Sharing Station Planner System

A comprehensive system for optimizing bike-sharing station placement and route planning in urban environments using graph algorithms.

## 🎉 NEW: Interactive Web Dashboard!

**Launch the beautiful interactive dashboard with maps and visualizations:**

```bash
streamlit run app.py
```

Then visit: **http://localhost:8501**

Features:
- 🗺️ **Interactive Maps** - Real-time route visualization
- 📊 **Live Charts** - Algorithm performance comparison  
- 🎨 **Beautiful UI** - Modern, responsive design
- ⚡ **Real-time Updates** - See changes instantly

[📱 Dashboard Guide](DASHBOARD_GUIDE.md) | [🚀 Quick Start](QUICK_START_DASHBOARD.md)

---

## Project Overview

This project implements a bike-sharing station placement and route planning system that uses advanced graph traversal and shortest path algorithms to:
- **Plan optimal routes** between locations considering distance, time, and traffic
- **Optimize station placement** using multiple algorithms (greedy, k-means, demand-based)
- **Analyze network coverage** and connectivity
- **Visualize routes** and network structure (both console and web-based)

## Key Features

### 1. Graph Data Structure (`graph.py`)
- **Node Class**: Represents locations (bike stations, intersections) with coordinates and properties
- **Edge Class**: Represents connections with multiple weights (distance, time, traffic)
- **CityGraph Class**: Complete graph implementation with:
  - Node and edge management
  - Haversine distance calculation for geographic coordinates
  - Neighbor traversal
  - Network statistics

### 2. Shortest Path Algorithms (`shortest_path.py`)
- **Dijkstra's Algorithm**: 
  - Finds optimal path with weighted cost function
  - Considers distance, time, and traffic factors
  - Returns complete path with cumulative statistics
  
- **A* Algorithm**: 
  - Uses heuristic (straight-line distance) for efficient search
  - Typically explores fewer nodes than Dijkstra
  - Guaranteed to find optimal path with admissible heuristic

- **BFS Traversal**: 
  - Finds all reachable nodes for network analysis

### 3. Station Placement Optimization (`station_placement.py`)
- **Greedy Coverage Algorithm**: 
  - Maximizes area coverage at each step
  - Best for ensuring widespread access
  
- **K-Means Clustering**: 
  - Geographic distribution based on clustering
  - Balances station spacing
  
- **Demand-Based Placement**: 
  - Prioritizes high-demand locations
  - Uses density-based demand calculation

- **Coverage Analysis**: 
  - Calculates percentage of nodes within walking distance
  - Evaluates network connectivity
  - Suggests improvements

### 4. Visualization (`visualization.py`)
- Route information with step-by-step directions
- Network summary with statistics
- Algorithm comparison
- ASCII map visualization
- CSV export for external analysis

## Algorithms Explained

### Graph Traversal
- **BFS (Breadth-First Search)**: Used for network reachability analysis
- **Priority Queue**: Used in Dijkstra and A* for efficient node exploration

### Shortest Path
- **Dijkstra's Algorithm**: Time complexity O((V + E) log V)
  - Guarantees optimal path
  - Explores nodes in order of increasing cost
  
- **A* Algorithm**: Time complexity O((V + E) log V) with better practical performance
  - Uses heuristic to guide search
  - Typically explores fewer nodes than Dijkstra

### Optimization
- **Greedy Algorithm**: Time complexity O(n²k) where n=nodes, k=stations
  - Local optimal choice at each step
  
- **K-Means Clustering**: Time complexity O(ikn) where i=iterations
  - Iteratively refines cluster centers

## Project Structure

```
.
├── app.py                      # 🌟 Interactive web dashboard (NEW!)
├── graph.py                    # Graph data structure
├── shortest_path.py            # Shortest path algorithms
├── station_placement.py        # Station placement optimization
├── visualization.py            # Console visualization utilities
├── main.py                     # Console application with demos
├── test_bike_system.py         # Unit tests (22 tests)
├── quick_start.py              # Quick start guide
├── launch_dashboard.sh         # Dashboard launch script
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── DASHBOARD_GUIDE.md          # Interactive dashboard guide
├── QUICK_START_DASHBOARD.md    # Dashboard quick reference
├── USAGE_GUIDE.md              # Code usage guide
├── ARCHITECTURE.md             # System architecture
├── PROJECT_SUMMARY.md          # Project summary
└── HIGHLIGHTS.md               # Project highlights
```

**Total:** ~4,500+ lines of well-documented code + comprehensive documentation
├── station_placement.py        # Station placement optimization
├── visualization.py            # Visualization utilities
├── main.py                     # Main application with demos
├── test_bike_system.py         # Unit tests
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Installation

```bash
# Clone or download the project
cd "Alorithms John Jay"

# Install dependencies (for interactive dashboard)
pip3 install streamlit folium streamlit-folium plotly pandas

# OR use requirements file
pip3 install -r requirements.txt
```

## Usage

### Option 1: Interactive Web Dashboard (Recommended! ⭐)

```bash
streamlit run app.py
```

Opens at: **http://localhost:8501**

**Features:**
- 🗺️ Interactive maps with real-time updates
- 📊 Beautiful charts and visualizations
- 🎯 Click-and-drag route planning
- 📈 Live algorithm comparisons
- 🌡️ Coverage heatmaps
- 📱 Responsive design

### Option 2: Console Demo

```bash
python3 main.py
```

This will demonstrate:
1. Shortest path algorithms (Dijkstra & A*)
2. Station placement optimization (3 algorithms)
3. Network visualization (ASCII art)
4. Route planning examples

### Option 3: Quick Test

```bash
python3 quick_start.py
```

### Run Tests

```bash
python3 test_bike_system.py
```

### Use as a Library

```python
from graph import CityGraph, Node
from shortest_path import ShortestPathFinder
from station_placement import StationPlacementOptimizer

# Create graph
graph = CityGraph()

# Add nodes
node1 = Node("A", "Location A", 40.7589, -73.9851)
graph.add_node(node1)

# Add edges
graph.add_edge("A", "B", distance=1.5, time=10, traffic=1.2)

# Find shortest path
finder = ShortestPathFinder(graph)
result = finder.dijkstra("A", "B")

# Optimize station placement
optimizer = StationPlacementOptimizer(graph)
stations = optimizer.greedy_station_placement(5)
```

## Example Output

### Shortest Path Result
```
ROUTE INFORMATION
================================================================
Total Distance: 2.40 km
Estimated Time: 18.50 minutes
Total Cost: 1.85
Nodes Explored: 8

Route (4 stops):
----------------------------------------------------------------
1. Residential Area North [STATION]
   Location: (40.7700, -73.9900)
   → Next: 0.30 km, 2.5 min, traffic: 1.0x

2. Central Park South
   Location: (40.7678, -73.9815)
   → Next: 0.40 km, 3.0 min, traffic: 1.1x
...
```

### Station Placement Comparison
```
PLACEMENT ALGORITHM COMPARISON
================================================================
Algorithm                 Coverage     Avg Distance    Connections
----------------------------------------------------------------------
Greedy Coverage          0.875        1.250           2.833
K-Means Clustering       0.812        1.180           2.667
Demand-Based             0.938        1.420           3.000
```

## Key Algorithms Implementation Details

### Dijkstra's Algorithm
```python
def dijkstra(start, end):
    priority_queue = [(0, start)]
    costs = {start: 0}
    
    while priority_queue:
        current_cost, current = heappop(priority_queue)
        
        if current == end:
            return reconstruct_path()
        
        for neighbor in get_neighbors(current):
            new_cost = current_cost + edge_cost
            if new_cost < costs.get(neighbor, infinity):
                costs[neighbor] = new_cost
                heappush(priority_queue, (new_cost, neighbor))
```

### A* Algorithm Enhancement
- Uses haversine distance as heuristic
- Estimates remaining cost to destination
- f(n) = g(n) + h(n) where:
  - g(n) = actual cost from start
  - h(n) = estimated cost to goal

## Project Considerations

### Distance Calculation
- Uses Haversine formula for accurate geographic distances
- Accounts for Earth's curvature
- Returns distances in kilometers

### Cost Function
- Weighted combination of factors:
  - Distance weight (default: 0.4)
  - Time weight (default: 0.4)
  - Traffic weight (default: 0.2)
- Customizable for different optimization goals

### Traffic Modeling
- Traffic factor multiplies travel time
- 1.0 = no traffic
- 2.0 = double travel time
- Can be set per edge based on time of day

## Performance

- **Graph Construction**: O(V + E)
- **Dijkstra's Algorithm**: O((V + E) log V)
- **A* Algorithm**: O((V + E) log V) with better practical performance
- **Station Placement (Greedy)**: O(k × n²) where k=stations, n=nodes
- **K-Means Clustering**: O(i × k × n) where i=iterations

## Future Enhancements

1. **Real-Time Data Integration**
   - Live traffic data
   - Real-time bike availability
   - Weather conditions

2. **Advanced Algorithms**
   - Genetic algorithms for multi-objective optimization
   - Ant colony optimization for route planning
   - Machine learning for demand prediction

3. **Additional Features**
   - Time-dependent routing (rush hour)
   - Multi-modal transportation
   - Rebalancing optimization (moving bikes between stations)

4. **Visualization**
   - Interactive web-based maps
   - Real-time route animation
   - Heat maps for demand and coverage

## Academic Context

This project demonstrates key concepts from algorithms and data structures courses:

- **Graph Theory**: Directed/undirected weighted graphs
- **Search Algorithms**: BFS, Dijkstra's, A*
- **Optimization**: Greedy algorithms, clustering
- **Data Structures**: Priority queues (heaps), hash maps
- **Complexity Analysis**: Time and space complexity
- **Heuristics**: Admissible heuristics in A*

## License

This is an educational project created for CSCI 377 - Algorithms course.

## Author

Created as a comprehensive demonstration of graph algorithms and optimization techniques for bike-sharing systems.
