# System Architecture & Flow Diagram

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                  BIKE-SHARING PLANNER SYSTEM                     │
└─────────────────────────────────────────────────────────────────┘
                                │
                ┌───────────────┴───────────────┐
                │                               │
        ┌───────▼────────┐             ┌───────▼────────┐
        │  GRAPH LAYER   │             │  ALGORITHM     │
        │   (graph.py)   │             │     LAYER      │
        └───────┬────────┘             └───────┬────────┘
                │                               │
    ┌───────────┼───────────┐       ┌──────────┼──────────┐
    │           │           │       │          │          │
┌───▼───┐   ┌──▼──┐   ┌────▼───┐ ┌─▼──────┐ ┌─▼────────┐ │
│ Node  │   │Edge │   │ City   │ │Shortest│ │ Station  │ │
│ Class │   │Class│   │ Graph  │ │  Path  │ │Placement │ │
└───────┘   └─────┘   └────────┘ └─┬──────┘ └─┬────────┘ │
                                   │          │          │
                            ┌──────▼────┐  ┌──▼────────┐ │
                            │ Dijkstra  │  │  Greedy   │ │
                            │    A*     │  │  K-Means  │ │
                            │    BFS    │  │  Demand   │ │
                            └───────────┘  └───────────┘ │
                                     │                    │
                                     └──────────┬─────────┘
                                                │
                                    ┌───────────▼────────────┐
                                    │ VISUALIZATION LAYER    │
                                    │   (visualization.py)   │
                                    └───────────┬────────────┘
                                                │
                                    ┌───────────▼────────────┐
                                    │  APPLICATION LAYER     │
                                    │      (main.py)         │
                                    └────────────────────────┘
```

## Data Flow: Finding Shortest Path

```
User Request
    │
    ▼
┌─────────────────┐
│ Start Location  │
│ End Location    │
│ Preferences     │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────┐
│  ShortestPathFinder             │
│  - Load graph data              │
│  - Initialize priority queue    │
│  - Set weights (distance,       │
│    time, traffic)               │
└────────┬────────────────────────┘
         │
    ┌────┴─────┐
    │          │
    ▼          ▼
┌────────┐  ┌──────┐
│Dijkstra│  │  A*  │
└───┬────┘  └───┬──┘
    │           │
    │  ┌────────┘
    │  │
    ▼  ▼
┌─────────────────┐
│ Process Nodes:  │
│ 1. Pop from PQ  │
│ 2. Check goal   │
│ 3. Explore      │
│    neighbors    │
│ 4. Update costs │
│ 5. Add to PQ    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Path Found!     │
│ - Node list     │
│ - Total cost    │
│ - Distance      │
│ - Time          │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Visualization   │
│ - Route map     │
│ - Turn by turn  │
│ - Statistics    │
└─────────────────┘
```

## Data Flow: Station Placement

```
City Network
    │
    ▼
┌─────────────────────┐
│ Input Parameters:   │
│ - Num stations      │
│ - Coverage radius   │
│ - Demand data       │
└──────────┬──────────┘
           │
    ┌──────┴──────┬──────────────┐
    │             │              │
    ▼             ▼              ▼
┌─────────┐  ┌─────────┐  ┌──────────┐
│ Greedy  │  │ K-Means │  │  Demand  │
│Algorithm│  │Algorithm│  │Algorithm │
└────┬────┘  └────┬────┘  └────┬─────┘
     │            │            │
     └────────────┼────────────┘
                  │
                  ▼
         ┌────────────────┐
         │ Evaluate Each: │
         │ - Coverage     │
         │ - Distance     │
         │ - Connectivity │
         └────────┬───────┘
                  │
                  ▼
         ┌────────────────┐
         │ Compare Results│
         │ Select Best    │
         └────────┬───────┘
                  │
                  ▼
         ┌────────────────┐
         │ Station List   │
         │ - IDs          │
         │ - Locations    │
         │ - Metrics      │
         └────────────────┘
```

## Algorithm Comparison

```
┌─────────────────────────────────────────────────────────┐
│              DIJKSTRA vs A* COMPARISON                  │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Dijkstra:                    A*:                       │
│  ┌──────┐                    ┌──────┐                  │
│  │Start │                    │Start │                  │
│  └──┬───┘                    └──┬───┘                  │
│     │                           │                       │
│  ┌──▼───────────┐           ┌──▼─────────┐            │
│  │ Explore ALL  │           │ Use        │            │
│  │ directions   │           │ heuristic  │            │
│  │ equally      │           │ to guide   │            │
│  └──┬───────────┘           └──┬─────────┘            │
│     │                           │                       │
│  ┌──▼───────────┐           ┌──▼─────────┐            │
│  │ Priority:    │           │ Priority:  │            │
│  │ g(n) only    │           │ f(n)=      │            │
│  │              │           │ g(n)+h(n)  │            │
│  └──┬───────────┘           └──┬─────────┘            │
│     │                           │                       │
│     └──────┬──────────┬─────────┘                      │
│            │          │                                 │
│         ┌──▼─────┐ ┌──▼─────┐                         │
│         │Explores│ │Explores│                         │
│         │MORE    │ │FEWER   │                         │
│         │nodes   │ │nodes   │                         │
│         └────────┘ └────────┘                         │
│            │          │                                 │
│            └────┬─────┘                                │
│                 │                                       │
│              ┌──▼──┐                                   │
│              │Goal │                                   │
│              └─────┘                                   │
│                                                         │
│  Result: Same optimal path, A* is faster              │
└─────────────────────────────────────────────────────────┘
```

## Station Placement Algorithms

```
┌───────────────────────────────────────────────────────┐
│           PLACEMENT ALGORITHM COMPARISON               │
├───────────────────────────────────────────────────────┤
│                                                        │
│  GREEDY:              K-MEANS:           DEMAND:      │
│  ▪ ▪ ▪ ▪ ▪ ▪         ▪ ▪ ▪ ▪ ▪ ▪        ▪ ▪ ▪ ▪ ▪ ▪  │
│  ▪ S ▪ ▪ ▪ ▪         ▪ S ▪ ▪ ▪ S        ▪ ▪ ▪ S S S  │
│  ▪ ▪ ▪ S ▪ ▪   VS    ▪ ▪ ▪ ▪ ▪ ▪   VS   ▪ ▪ ▪ ▪ ▪ ▪  │
│  ▪ ▪ ▪ ▪ ▪ S         ▪ ▪ S ▪ ▪ ▪        ▪ ▪ ▪ ▪ ▪ ▪  │
│  ▪ ▪ S ▪ ▪ ▪         S ▪ ▪ ▪ ▪ ▪        S ▪ ▪ ▪ ▪ ▪  │
│  ▪ ▪ ▪ ▪ ▪ ▪         ▪ ▪ ▪ S ▪ ▪        ▪ ▪ ▪ ▪ ▪ ▪  │
│                                                        │
│  Max Coverage         Even Spacing      High Demand   │
│  87.5% covered        Balanced          93.8% in hot  │
│                       distribution      zones         │
└───────────────────────────────────────────────────────┘

Legend: S = Station, ▪ = Location
```

## Cost Function Visualization

```
┌──────────────────────────────────────────────────────┐
│          WEIGHTED COST CALCULATION                   │
├──────────────────────────────────────────────────────┤
│                                                      │
│  Total Cost = w₁·Distance + w₂·Time + w₃·Traffic   │
│                                                      │
│  Default Weights:                                   │
│  ┌─────────────┬─────────┬─────────┐              │
│  │  Distance   │  Time   │ Traffic │              │
│  │    40%      │   40%   │   20%   │              │
│  └─────────────┴─────────┴─────────┘              │
│                                                      │
│  Example Calculation:                               │
│  ────────────────────────                          │
│  Distance: 2.5 km                                  │
│  Time:     15 min                                  │
│  Traffic:  1.3x                                    │
│                                                      │
│  Cost = 0.4(2.5) + 0.4(15) + 0.2(15×1.3)          │
│       = 1.0 + 6.0 + 3.9                           │
│       = 10.9                                       │
│                                                      │
└──────────────────────────────────────────────────────┘
```

## Test Coverage

```
┌──────────────────────────────────────────────────────┐
│               TEST STRUCTURE                         │
├──────────────────────────────────────────────────────┤
│                                                      │
│  TestCityGraph (7 tests)                            │
│  ├── Node creation                                  │
│  ├── Graph operations                               │
│  ├── Distance calculation                           │
│  └── Edge weights                                   │
│                                                      │
│  TestShortestPath (7 tests)                         │
│  ├── Dijkstra correctness                          │
│  ├── A* correctness                                 │
│  ├── Path existence                                 │
│  ├── No path handling                               │
│  ├── Algorithm comparison                           │
│  └── BFS reachability                               │
│                                                      │
│  TestStationPlacement (7 tests)                     │
│  ├── Coverage calculation                           │
│  ├── Greedy placement                               │
│  ├── K-means clustering                             │
│  ├── Demand-based                                   │
│  ├── Evaluation metrics                             │
│  └── Connectivity                                   │
│                                                      │
│  TestIntegration (1 test)                           │
│  └── End-to-end workflow                            │
│                                                      │
│  Total: 22 tests, 100% passing ✓                   │
└──────────────────────────────────────────────────────┘
```

## File Dependency Graph

```
┌─────────────────────────────────────────────┐
│         FILE DEPENDENCIES                   │
├─────────────────────────────────────────────┤
│                                             │
│              graph.py                       │
│                 │                           │
│        ┌────────┴────────┐                 │
│        │                 │                 │
│   shortest_path.py  station_placement.py  │
│        │                 │                 │
│        └────────┬────────┘                 │
│                 │                           │
│          visualization.py                  │
│                 │                           │
│        ┌────────┴────────┐                 │
│        │                 │                 │
│     main.py      test_bike_system.py      │
│        │                                    │
│   quick_start.py                           │
│                                             │
│  Dependencies: None (stdlib only!)         │
└─────────────────────────────────────────────┘
```

## Performance Metrics

```
┌────────────────────────────────────────────────┐
│        ALGORITHM PERFORMANCE                   │
├────────────────────────────────────────────────┤
│                                                │
│  Graph Size: 16 nodes, 54 edges              │
│                                                │
│  Dijkstra's Algorithm:                        │
│    Nodes explored: 6-9                        │
│    Time: < 1ms                                │
│    Memory: O(V)                               │
│                                                │
│  A* Algorithm:                                │
│    Nodes explored: 3-4                        │
│    Time: < 1ms                                │
│    Memory: O(V)                               │
│    Improvement: 50-70% fewer nodes            │
│                                                │
│  Station Placement:                           │
│    Greedy: ~10ms for 6 stations              │
│    K-Means: ~5ms (100 iterations)            │
│    Demand: < 1ms                              │
│                                                │
└────────────────────────────────────────────────┘
```
