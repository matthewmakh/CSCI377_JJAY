# 🚴 Interactive Dashboard Guide

## Overview

The **Bike-Sharing Station Planner Dashboard** is a fully interactive web application with:
- 🗺️ **Interactive Maps** - Visualize routes and stations on real maps
- 📊 **Real-time Charts** - Compare algorithms and analyze performance
- 🎨 **Beautiful UI** - Modern, responsive design
- ⚡ **Live Updates** - See changes instantly

---

## 🚀 Quick Start

### Option 1: One-Click Launch

```bash
./launch_dashboard.sh
```

### Option 2: Manual Launch

```bash
streamlit run app.py
```

The dashboard will automatically open in your browser at `http://localhost:8501`

---

## 📱 Dashboard Features

### 1. 🏠 Overview Page

**What you'll see:**
- Interactive map showing all locations
- Network statistics and metrics
- Complete location list with filtering
- Visual representation of the entire network

**Features:**
- Toggle connections on/off
- Highlight bike stations
- Click markers for detailed info
- Pan and zoom the map

### 2. 🗺️ Route Planning Page

**Find optimal routes between any two locations**

**Interactive Elements:**
- **Location Selectors** - Choose start and end points from dropdowns
- **Algorithm Choice** - Compare Dijkstra, A*, or both
- **Weight Sliders** - Adjust importance of distance, time, and traffic
  - Distance Weight (0-100%): How much distance matters
  - Time Weight (0-100%): How much time matters
  - Traffic Weight (0-100%): How much congestion matters

**What you get:**
- ✅ Interactive map with highlighted route
- ✅ Turn-by-turn directions
- ✅ Distance, time, and cost metrics
- ✅ Performance comparison charts
- ✅ Number of nodes explored by each algorithm

**Try different scenarios:**
- Rush hour (high traffic weight)
- Shortest distance (high distance weight)
- Fastest route (high time weight)

### 3. 📍 Station Placement Page

**Optimize bike station locations**

**Interactive Controls:**
- **Number of Stations** - Slider from 1-10
- **Algorithm Selection:**
  - **Greedy Coverage** - Maximizes area coverage
  - **K-Means Clustering** - Balanced geographic distribution
  - **Demand-Based** - Prioritizes high-demand areas
- **Coverage Radius** - Walking distance threshold
- **Demand Settings** - Set demand levels for different area types

**Visualizations:**
- 🗺️ Interactive map with placed stations
- 🌡️ Coverage heatmap showing accessibility
- 📊 Evaluation metrics (coverage %, distances, connections)
- 📋 Detailed station list

**Real-time updates:**
- Stations appear immediately on the map
- Metrics update dynamically
- Heatmap shows coverage areas

### 4. 📊 Network Analysis Page

**Analyze network performance and characteristics**

**Analytics:**
- **Network Overview** - Key statistics and metrics
- **Connectivity Distribution** - Histogram of node connections
- **Traffic Analysis** - Scatter plot of distance vs time
- **Most Congested Routes** - Top 10 high-traffic connections
- **Demand Distribution** - Bar chart of high-demand locations

**Interactive Charts:**
- Hover for details
- Zoom and pan
- Click legends to filter
- Export as images

---

## 🎯 Usage Examples

### Example 1: Plan Your Commute

1. Go to **🗺️ Route Planning**
2. Select your home as start location
3. Select your office as end location
4. Adjust traffic weight based on time of day
5. Click **Find Route**
6. View the optimal path on the map
7. Check turn-by-turn directions

### Example 2: Optimize Station Network

1. Go to **📍 Station Placement**
2. Set number of stations (e.g., 6)
3. Choose **Demand-Based** algorithm
4. Adjust demand sliders:
   - High downtown demand
   - Medium transit demand
   - High educational area demand
5. Click **Optimize Station Placement**
6. View stations on map and coverage heatmap
7. Check metrics to verify good coverage

### Example 3: Compare Algorithms

1. Go to **🗺️ Route Planning**
2. Select start and end locations
3. Choose **Both** algorithms
4. Click **Find Route**
5. View side-by-side comparison
6. Check performance chart to see efficiency differences

### Example 4: Analyze Network

1. Go to **📊 Network Analysis**
2. View connectivity distribution
3. Check traffic patterns
4. Identify congested routes
5. Review demand distribution
6. Use insights to improve network

---

## 🎨 UI Features

### Interactive Maps
- **Zoom**: Mouse wheel or pinch
- **Pan**: Click and drag
- **Markers**: Click for popup info
- **Routes**: Blue lines show paths
- **Stations**: Blue bicycle icons
- **Start/End**: Green play and red stop icons

### Color Coding
- 🟢 **Green** - Start location, low traffic
- 🔴 **Red** - End location, high traffic
- 🔵 **Blue** - Bike stations, selected routes
- 🟠 **Orange** - Waypoints, medium traffic
- ⚪ **Gray** - Regular locations

### Charts
- **Bar Charts** - Algorithm comparisons
- **Heatmaps** - Coverage visualization
- **Scatter Plots** - Traffic analysis
- **Histograms** - Distribution analysis

---

## ⚙️ Advanced Features

### Custom Weights

**Distance-Focused Routing:**
```
Distance: 80%
Time: 10%
Traffic: 10%
```
Use when you want the shortest physical distance.

**Time-Focused Routing:**
```
Distance: 10%
Time: 80%
Traffic: 10%
```
Use when you want the fastest route.

**Traffic-Avoiding Routing:**
```
Distance: 20%
Time: 20%
Traffic: 60%
```
Use during rush hour to avoid congestion.

### Coverage Optimization

**Maximum Coverage:**
- Use Greedy algorithm
- Set coverage radius to 0.5 km
- Maximize number of stations

**Balanced Distribution:**
- Use K-Means algorithm
- Adjust station count based on city size
- Check min/max distances

**Demand-Focused:**
- Use Demand-Based algorithm
- Set high demand in business areas
- Prioritize transit hubs

---

## 📊 Understanding Metrics

### Route Planning Metrics

- **Distance (km)** - Total path length
- **Time (min)** - Estimated travel time
- **Total Cost** - Weighted combination of factors
- **Nodes Explored** - Algorithm efficiency measure

### Station Placement Metrics

- **Coverage (%)** - Percentage of area within walking distance
- **Avg Station Distance** - Mean distance between stations
- **Min Distance** - Closest two stations
- **Avg Connections** - Mean connections per station

### Network Analysis Metrics

- **Total Nodes** - All locations in network
- **Total Edges** - All connections
- **Avg Connections** - Network density
- **Traffic Factor** - Congestion multiplier (1.0 = no traffic)

---

## 🎓 Educational Use

### Demonstrate Algorithms

**Compare Dijkstra vs A*:**
1. Choose both algorithms
2. Run on same route
3. Observe nodes explored
4. Note: A* typically explores fewer nodes

**Test Greedy Algorithm:**
1. Place 1 station at a time
2. Observe how coverage increases
3. See diminishing returns

**Analyze Traffic Impact:**
1. Adjust traffic weights
2. See how routes change
3. Understand real-world constraints

### Class Demonstrations

**Graph Theory:**
- Show nodes and edges visually
- Demonstrate connectivity
- Explain weighted graphs

**Algorithm Efficiency:**
- Compare node exploration counts
- Show time/space tradeoffs
- Demonstrate heuristic benefits

**Optimization:**
- Show multiple solutions
- Compare coverage metrics
- Discuss trade-offs

---

## 🔧 Troubleshooting

### Dashboard Won't Start

**Check Python version:**
```bash
python3 --version  # Should be 3.8 or higher
```

**Reinstall dependencies:**
```bash
pip3 install -r requirements.txt
```

**Try manual launch:**
```bash
streamlit run app.py
```

### Map Not Loading

- Check internet connection (maps need online access)
- Refresh the page
- Clear browser cache

### Slow Performance

- Reduce number of stations in placement
- Disable "Show all connections" on map
- Close other browser tabs
- Use A* instead of Dijkstra for large networks

### Route Not Found

- Ensure start and end are different
- Check if locations are connected
- Verify nodes exist in network

---

## 💡 Tips & Tricks

### Performance Tips

1. **Use A* for faster searches** - Especially in large networks
2. **Hide edges when not needed** - Reduces map clutter
3. **Start with fewer stations** - Then increase gradually
4. **Adjust weights carefully** - Small changes can have big impacts

### Visualization Tips

1. **Zoom in for details** - See exact station locations
2. **Use heatmap** - Quickly identify coverage gaps
3. **Check charts** - Hover for detailed information
4. **Export data** - Download charts as images

### Analysis Tips

1. **Compare multiple algorithms** - See which works best
2. **Test different demands** - Simulate various scenarios
3. **Check congested routes** - Identify problem areas
4. **Monitor coverage** - Aim for 80%+ coverage

---

## 🎯 Common Workflows

### Workflow 1: New City Planning

1. Start with **Overview** to understand network
2. Go to **Network Analysis** to check connectivity
3. Use **Station Placement** with Greedy algorithm
4. Check coverage metrics (aim for 80%+)
5. Test routes in **Route Planning**

### Workflow 2: Route Optimization

1. Go to **Route Planning**
2. Select start and end locations
3. Try both algorithms
4. Adjust weights for your priorities
5. Compare results
6. Choose best route

### Workflow 3: Coverage Analysis

1. Go to **Station Placement**
2. Set desired number of stations
3. Try all three algorithms
4. Compare coverage percentages
5. Check heatmap for gaps
6. Adjust and re-optimize

---

## 📱 Keyboard Shortcuts

- **Ctrl + R** - Refresh page
- **Ctrl + W** - Close tab
- **Ctrl + +/-** - Zoom in/out
- **Ctrl + 0** - Reset zoom
- **F11** - Fullscreen mode

---

## 🎉 Next Steps

1. **Explore the Overview** page to understand the network
2. **Try Route Planning** with different locations
3. **Optimize Stations** using different algorithms
4. **Analyze Network** characteristics
5. **Experiment** with different settings
6. **Compare** results and learn!

---

## 📚 Additional Resources

- **README.md** - Project documentation
- **USAGE_GUIDE.md** - Code usage examples
- **ARCHITECTURE.md** - System design
- **main.py** - Console-based demo

---

**🚴 Enjoy exploring the interactive dashboard! 🚴**

For questions or issues, refer to the main README.md or check the troubleshooting section above.
