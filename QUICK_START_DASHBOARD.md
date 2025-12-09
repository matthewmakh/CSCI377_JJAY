# 🚴 Interactive Dashboard - Quick Reference

## 🚀 Launch the Dashboard

### Method 1: Launch Script (Easiest)
```bash
./launch_dashboard.sh
```

### Method 2: Direct Command
```bash
streamlit run app.py
```

### Method 3: Python
```bash
python3 -m streamlit run app.py
```

The dashboard will open automatically at: **http://localhost:8501**

---

## 📱 Dashboard Pages

### 1️⃣ Overview (🏠)
- View entire network on interactive map
- See all locations and connections
- Quick statistics dashboard
- Toggle edges and stations

### 2️⃣ Route Planning (🗺️)
- Select start and end locations
- Choose algorithm (Dijkstra, A*, or Both)
- Adjust weight preferences
- See route on map with turn-by-turn directions
- Compare algorithm performance

### 3️⃣ Station Placement (📍)
- Set number of stations (1-10)
- Choose optimization algorithm:
  - Greedy Coverage
  - K-Means Clustering  
  - Demand-Based
- Adjust demand for different areas
- View coverage heatmap
- See placement metrics

### 4️⃣ Network Analysis (📊)
- Network statistics
- Connectivity distribution
- Traffic analysis charts
- Most congested routes
- Demand distribution

---

## 🎯 Interactive Features

### On Maps:
- **🖱️ Click** markers for details
- **🔍 Zoom** with mouse wheel
- **🤚 Pan** by dragging
- **📍 Hover** for quick info

### On Charts:
- **📊 Hover** for data points
- **🔍 Zoom** by selecting area
- **📥 Export** via menu
- **🔲 Filter** via legend clicks

### Controls:
- **🎚️ Sliders** for weights and settings
- **📋 Dropdowns** for selections
- **🔘 Buttons** for actions
- **✅ Checkboxes** for toggles

---

## 💡 Quick Tips

### Best Practices:
1. Start with **Overview** to understand network
2. Use **Route Planning** for specific journeys
3. Try **Station Placement** with different algorithms
4. Check **Network Analysis** for insights

### Algorithm Choice:
- **Dijkstra** - Guaranteed optimal, explores more
- **A*** - Usually faster, explores fewer nodes
- **Both** - Compare performance

### Weight Settings:
- **Rush hour?** Increase traffic weight
- **Exercise?** Increase distance weight
- **In a hurry?** Increase time weight

---

## 🎨 Visual Guide

### Map Colors:
- 🟢 **Green** = Start location
- 🔴 **Red** = End location
- 🔵 **Blue** = Bike stations / Routes
- 🟠 **Orange** = Waypoints
- ⚪ **Gray** = Regular locations

### Traffic Colors:
- 🟢 **Green** = Low traffic (< 1.2x)
- 🟠 **Orange** = Medium traffic (1.2-1.4x)
- 🔴 **Red** = High traffic (> 1.4x)

---

## ⌨️ Keyboard Shortcuts

| Key | Action |
|-----|--------|
| **Ctrl + R** | Refresh page |
| **Ctrl + W** | Close tab |
| **Ctrl + +** | Zoom in |
| **Ctrl + -** | Zoom out |
| **F11** | Fullscreen |

---

## 🎓 Try These Scenarios

### Scenario 1: Morning Commute
1. Go to Route Planning
2. Select home → office
3. Set high traffic weight (0.6)
4. Compare Dijkstra vs A*

### Scenario 2: Station Network
1. Go to Station Placement
2. Set 6 stations
3. Try all 3 algorithms
4. Compare coverage %

### Scenario 3: Find Congestion
1. Go to Network Analysis
2. Check traffic analysis chart
3. View most congested routes
4. Plan improvements

---

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| Dashboard won't start | Check Python version (3.8+) |
| Map not loading | Check internet connection |
| Slow performance | Use A*, reduce stations |
| Route not found | Check locations are different |

---

## 📚 Documentation

- **DASHBOARD_GUIDE.md** - Detailed guide (this file is summary)
- **README.md** - Project overview
- **USAGE_GUIDE.md** - Code examples
- **ARCHITECTURE.md** - System design

---

## 🎉 Features at a Glance

✅ **Interactive Maps** - Real geographic visualization  
✅ **Live Updates** - See changes instantly  
✅ **Algorithm Comparison** - Side-by-side analysis  
✅ **Beautiful Charts** - Plotly visualizations  
✅ **Coverage Heatmaps** - Identify gaps  
✅ **Performance Metrics** - Track efficiency  
✅ **Responsive Design** - Works on all screens  
✅ **Easy to Use** - Intuitive interface  

---

**🚴 Ready to explore? Launch the dashboard now! 🚴**

```bash
./launch_dashboard.sh
```

or

```bash
streamlit run app.py
```

Then visit: **http://localhost:8501**
