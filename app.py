"""
Interactive Bike-Sharing Station Planner Dashboard
A web-based interactive application with maps and visualizations
"""

import streamlit as st
import folium
from streamlit_folium import st_folium
import plotly.graph_objects as go
import plotly.express as px
from graph import CityGraph, Node
from shortest_path import ShortestPathFinder, PathResult
from station_placement import StationPlacementOptimizer
import random
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Bike-Sharing Planner",
    page_icon="🚴",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #e3f2fd 0%, #bbdefb 100%);
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 1rem 2rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def create_sample_network():
    """Create and cache the sample city network."""
    graph = CityGraph()
    
    # Define locations with realistic NYC area coordinates
    locations = [
        ("RES_01", "Residential Area North", 40.7700, -73.9900, False, 0),
        ("RES_02", "Residential Area East", 40.7650, -73.9700, False, 0),
        ("RES_03", "Residential Area South", 40.7500, -73.9850, False, 0),
        ("RES_04", "Residential Area West", 40.7600, -74.0000, False, 0),
        ("COM_01", "Downtown Business District", 40.7589, -73.9851, False, 0),
        ("COM_02", "Shopping Center", 40.7620, -73.9780, False, 0),
        ("COM_03", "Office Complex", 40.7560, -73.9920, False, 0),
        ("PARK_01", "Central Park South", 40.7678, -73.9815, False, 0),
        ("PARK_02", "Riverside Park", 40.7700, -73.9950, False, 0),
        ("TRAN_01", "Main Train Station", 40.7527, -73.9772, False, 0),
        ("TRAN_02", "Bus Terminal", 40.7570, -73.9900, False, 0),
        ("EDU_01", "University Campus", 40.7630, -73.9840, False, 0),
        ("EDU_02", "College District", 40.7660, -73.9760, False, 0),
        ("MED_01", "City Hospital", 40.7540, -73.9800, False, 0),
        ("ENT_01", "Theater District", 40.7580, -73.9860, False, 0),
        ("ENT_02", "Sports Arena", 40.7510, -73.9930, False, 0),
    ]
    
    for node_id, name, lat, lon, is_station, capacity in locations:
        node = Node(node_id, name, lat, lon, is_station, capacity)
        graph.add_node(node)
    
    # Define connections
    connections = [
        ("RES_01", "PARK_01", 0.3, 2.5, 1.0),
        ("RES_01", "PARK_02", 0.4, 3.0, 1.1),
        ("RES_02", "COM_02", 0.4, 3.0, 1.2),
        ("RES_02", "EDU_02", 0.3, 2.0, 1.0),
        ("RES_03", "TRAN_01", 0.3, 2.5, 1.3),
        ("RES_03", "MED_01", 0.5, 4.0, 1.1),
        ("RES_04", "COM_03", 0.4, 3.0, 1.0),
        ("RES_04", "PARK_02", 0.3, 2.5, 1.0),
        ("COM_01", "ENT_01", 0.2, 1.5, 1.5),
        ("COM_01", "TRAN_01", 0.3, 2.0, 1.6),
        ("COM_01", "COM_02", 0.4, 3.0, 1.4),
        ("COM_02", "EDU_01", 0.3, 2.0, 1.1),
        ("COM_03", "TRAN_02", 0.3, 2.0, 1.2),
        ("COM_03", "COM_01", 0.4, 3.0, 1.3),
        ("PARK_01", "EDU_01", 0.3, 2.0, 1.0),
        ("PARK_01", "COM_01", 0.4, 3.0, 1.1),
        ("PARK_02", "PARK_01", 0.5, 4.0, 1.0),
        ("TRAN_01", "TRAN_02", 0.4, 3.0, 1.5),
        ("TRAN_01", "MED_01", 0.3, 2.0, 1.2),
        ("TRAN_02", "ENT_02", 0.4, 3.0, 1.3),
        ("EDU_01", "COM_01", 0.3, 2.5, 1.2),
        ("EDU_01", "EDU_02", 0.4, 3.0, 1.0),
        ("EDU_02", "PARK_01", 0.3, 2.0, 1.0),
        ("MED_01", "ENT_02", 0.4, 3.0, 1.1),
        ("ENT_01", "ENT_02", 0.5, 4.0, 1.4),
        ("ENT_01", "COM_02", 0.4, 3.0, 1.3),
        ("ENT_02", "COM_03", 0.3, 2.5, 1.2),
    ]
    
    for source, dest, distance, time, traffic in connections:
        graph.add_edge(source, dest, distance, time, traffic, bidirectional=True)
    
    return graph


def create_map(graph, highlight_path=None, stations=None, show_all_edges=False):
    """Create an interactive Folium map."""
    # Calculate map center
    lats = [node.lat for node in graph.nodes.values()]
    lons = [node.lon for node in graph.nodes.values()]
    center_lat = sum(lats) / len(lats)
    center_lon = sum(lons) / len(lons)
    
    # Create map
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=13,
        tiles='OpenStreetMap'
    )
    
    # Add edges if requested
    if show_all_edges:
        for node_id, edges in graph.edges.items():
            node = graph.get_node(node_id)
            for edge in edges:
                dest_node = graph.get_node(edge.destination)
                if node and dest_node:
                    # Color based on traffic
                    if edge.traffic < 1.2:
                        color = 'green'
                    elif edge.traffic < 1.4:
                        color = 'orange'
                    else:
                        color = 'red'
                    
                    folium.PolyLine(
                        locations=[[node.lat, node.lon], [dest_node.lat, dest_node.lon]],
                        color=color,
                        weight=2,
                        opacity=0.3,
                        popup=f"{edge.distance:.2f}km, {edge.time:.1f}min, traffic: {edge.traffic}x"
                    ).add_to(m)
    
    # Add path if provided
    if highlight_path:
        path_coords = []
        for node_id in highlight_path:
            node = graph.get_node(node_id)
            if node:
                path_coords.append([node.lat, node.lon])
        
        if len(path_coords) > 1:
            folium.PolyLine(
                locations=path_coords,
                color='blue',
                weight=5,
                opacity=0.8,
                popup="Selected Route"
            ).add_to(m)
            
            # Add markers for start and end
            folium.Marker(
                path_coords[0],
                popup="Start",
                icon=folium.Icon(color='green', icon='play')
            ).add_to(m)
            
            folium.Marker(
                path_coords[-1],
                popup="End",
                icon=folium.Icon(color='red', icon='stop')
            ).add_to(m)
    
    # Add nodes
    station_list = stations if stations else []
    for node in graph.nodes.values():
        is_highlighted = highlight_path and node.node_id in highlight_path
        is_station = node.is_station or node.node_id in station_list
        
        if is_station:
            color = 'blue'
            icon = 'bicycle'
        elif is_highlighted:
            color = 'orange'
            icon = 'info-sign'
        else:
            color = 'gray'
            icon = 'circle'
        
        popup_text = f"""
        <b>{node.name}</b><br>
        ID: {node.node_id}<br>
        Location: ({node.lat:.4f}, {node.lon:.4f})<br>
        {"<b>BIKE STATION</b><br>" if is_station else ""}
        {"Capacity: " + str(node.capacity) + " bikes<br>" if is_station else ""}
        Demand: {node.demand:.2f}
        """
        
        folium.Marker(
            [node.lat, node.lon],
            popup=folium.Popup(popup_text, max_width=300),
            icon=folium.Icon(color=color, icon=icon)
        ).add_to(m)
    
    return m


def create_performance_chart(results_dict):
    """Create a comparison chart for algorithm performance."""
    algorithms = list(results_dict.keys())
    distances = [r.total_distance for r in results_dict.values()]
    times = [r.total_time for r in results_dict.values()]
    nodes_explored = [r.nodes_explored for r in results_dict.values()]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Distance (km)',
        x=algorithms,
        y=distances,
        marker_color='lightblue'
    ))
    
    fig.add_trace(go.Bar(
        name='Time (min)',
        x=algorithms,
        y=times,
        marker_color='lightcoral'
    ))
    
    fig.add_trace(go.Bar(
        name='Nodes Explored',
        x=algorithms,
        y=nodes_explored,
        marker_color='lightgreen'
    ))
    
    fig.update_layout(
        title='Algorithm Performance Comparison',
        barmode='group',
        xaxis_title='Algorithm',
        yaxis_title='Value',
        hovermode='x unified'
    )
    
    return fig


def create_coverage_heatmap(graph, stations, optimizer):
    """Create a heatmap showing station coverage."""
    # Create grid of points
    lats = [node.lat for node in graph.nodes.values()]
    lons = [node.lon for node in graph.nodes.values()]
    
    lat_range = max(lats) - min(lats)
    lon_range = max(lons) - min(lons)
    
    grid_size = 20
    lat_points = [min(lats) + i * lat_range / grid_size for i in range(grid_size)]
    lon_points = [min(lons) + i * lon_range / grid_size for i in range(grid_size)]
    
    coverage_data = []
    for lat in lat_points:
        row = []
        for lon in lon_points:
            # Find distance to nearest station
            min_dist = float('inf')
            for station_id in stations:
                station = graph.get_node(station_id)
                dist = graph._haversine_distance(lat, lon, station.lat, station.lon)
                min_dist = min(min_dist, dist)
            
            # Coverage score (1 if within 0.5km, 0 if beyond 1km)
            if min_dist <= 0.5:
                score = 1.0
            elif min_dist >= 1.0:
                score = 0.0
            else:
                score = 1.0 - (min_dist - 0.5) / 0.5
            row.append(score)
        coverage_data.append(row)
    
    fig = go.Figure(data=go.Heatmap(
        z=coverage_data,
        x=lon_points,
        y=lat_points,
        colorscale='RdYlGn',
        colorbar=dict(title="Coverage"),
    ))
    
    fig.update_layout(
        title='Station Coverage Heatmap',
        xaxis_title='Longitude',
        yaxis_title='Latitude',
        height=400
    )
    
    return fig


def main():
    """Main application."""
    
    # Header
    st.markdown('<div class="main-header">🚴 Bike-Sharing Station Planner Dashboard</div>', 
                unsafe_allow_html=True)
    
    # Initialize session state
    if 'graph' not in st.session_state:
        st.session_state.graph = create_sample_network()
        st.session_state.stations = []
        st.session_state.current_path = None
    
    graph = st.session_state.graph
    
    # Sidebar
    with st.sidebar:
        st.image("https://raw.githubusercontent.com/twitter/twemoji/master/assets/72x72/1f6b4.png", width=100)
        st.title("Navigation")
        st.caption("Choose a page to explore different features")
        
        page = st.radio(
            "Select Page",
            ["🏠 Overview", "🗺️ Route Planning", "📍 Station Placement", "📊 Network Analysis"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        st.markdown("### Quick Stats")
        st.caption("Real-time network information")
        st.metric("Total Locations", graph.node_count(), help="All locations in the network")
        st.metric("Total Connections", graph.edge_count(), help="All routes between locations")
        st.metric("Bike Stations", len(st.session_state.stations), help="Active bike stations")
        
        st.markdown("---")
        st.markdown("### 💡 Quick Tips")
        if page == "🏠 Overview":
            st.info("Explore the map and see all network locations. Click markers for details!")
        elif page == "🗺️ Route Planning":
            st.info("Try adjusting the weight sliders to see how it changes your route!")
        elif page == "📍 Station Placement":
            st.info("Compare all three algorithms to find the best station placement strategy!")
        elif page == "📊 Network Analysis":
            st.info("Use these insights to identify bottlenecks and optimize your network!")
    
    # Main content based on selected page
    if page == "🏠 Overview":
        show_overview_page(graph)
    elif page == "🗺️ Route Planning":
        show_route_planning_page(graph)
    elif page == "📍 Station Placement":
        show_station_placement_page(graph)
    elif page == "📊 Network Analysis":
        show_network_analysis_page(graph)


def show_overview_page(graph):
    """Display overview page."""
    st.header("🏠 Welcome to the Bike-Sharing Station Planner")
    
    st.info("""📖 **What is this dashboard?** 
    A complete tool for planning and optimizing bike-sharing networks. This page shows your entire network with all locations and possible routes.
    """)
    
    st.markdown("""
    ### What You Can Do Here:
    - 🗺️ **Plan optimal routes** - Find the best path between any two locations considering distance, time, and traffic
    - 📍 **Optimize station placement** - Use smart algorithms to decide where to put bike stations for maximum coverage
    - 📊 **Analyze network performance** - Get insights into connectivity, traffic patterns, and demand
    - 🔍 **Visualize everything** - See your data on interactive maps and charts
    
    💡 **New to this?** Start by exploring the map below, then try the Route Planning page!
    """)
    
    # Network map
    st.subheader("🗺️ City Network Map")
    st.markdown("**Interactive map controls:** Click markers for details • Pan to explore • Zoom for closer view")
    
    col1, col2 = st.columns([3, 1])
    
    with col2:
        show_edges = st.checkbox("Show all connections", value=False, help="Display all routes between locations")
        show_stations = st.checkbox("Highlight stations", value=True, help="Show bike station markers in blue")
        st.info("🔵 **Blue bicycle icons** = Bike stations\n\n⚪ **Gray circles** = Other locations")
    
    with col1:
        m = create_map(
            graph, 
            stations=st.session_state.stations if show_stations else None,
            show_all_edges=show_edges
        )
        st_folium(m, width=900, height=500)
    
    # Key metrics
    st.subheader("📊 Network Statistics")
    st.markdown("**Quick overview** of your bike-sharing network size and connectivity:")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Locations", graph.node_count(), help="Total number of locations in the network")
        st.caption("🏘️ Network size")
    with col2:
        st.metric("Connections", graph.edge_count(), help="Total number of routes between locations")
        st.caption("🔗 Available routes")
    with col3:
        avg_connections = graph.edge_count() / graph.node_count() if graph.node_count() > 0 else 0
        st.metric("Avg Connections/Node", f"{avg_connections:.1f}", help="Average routes per location (higher = better connected)")
        st.caption("🌐 Connectivity")
    with col4:
        st.metric("Bike Stations", len(st.session_state.stations), help="Number of active bike stations")
        st.caption("🚲 Active stations")
    
    # Location list
    st.subheader("📍 All Locations")
    st.markdown("**Complete directory** of all locations in your network. ✓ indicates active bike stations.")
    
    locations_data = []
    for node in graph.get_all_nodes():
        locations_data.append({
            "ID": node.node_id,
            "Name": node.name,
            "Latitude": f"{node.lat:.4f}",
            "Longitude": f"{node.lon:.4f}",
            "Station": "✓" if (node.is_station or node.node_id in st.session_state.stations) else "",
            "Demand": f"{node.demand:.2f}"
        })
    
    df = pd.DataFrame(locations_data)
    st.dataframe(df, use_container_width=True)


def show_route_planning_page(graph):
    """Display route planning page."""
    st.header("🗺️ Route Planning")
    
    st.info("""📖 **What is this?** 
    This page helps you find the best route between any two locations in the network. 
    You can choose different algorithms and adjust how important distance, time, and traffic are to you.
    """)
    
    with st.expander("ℹ️ Understanding Route Planning"):
        st.markdown("""
        **Why Route Planning Matters:**
        - Helps users find the fastest or shortest path to their destination
        - Considers real-world factors like traffic congestion and road conditions
        - Different algorithms offer different trade-offs between speed and accuracy
        
        **How It Works:**
        1. Select your start and end locations
        2. Choose which factors matter most (distance, time, traffic)
        3. Pick an algorithm (or compare both!)
        4. See your optimal route on the map with turn-by-turn directions
        """)
    
    # Route selection
    col1, col2 = st.columns(2)
    
    node_names = {node.node_id: node.name for node in graph.get_all_nodes()}
    node_ids = list(node_names.keys())
    
    with col1:
        start_id = st.selectbox(
            "Start Location",
            node_ids,
            format_func=lambda x: node_names[x],
            key="start_location"
        )
    
    with col2:
        end_id = st.selectbox(
            "End Location",
            node_ids,
            format_func=lambda x: node_names[x],
            index=5 if len(node_ids) > 5 else 0,
            key="end_location"
        )
    
    # Algorithm and weight settings
    st.subheader("⚙️ Algorithm Settings")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        algorithm = st.selectbox(
            "Algorithm",
            ["Dijkstra", "A*", "Both"],
            help="Dijkstra: Explores all possibilities (thorough). A*: Uses smart heuristics (faster). Both: Compare them side-by-side!"
        )
        st.caption("🔍 **Dijkstra** is guaranteed optimal but explores more. **A*** is faster using geographic hints.")
    
    with col2:
        dist_weight = st.slider(
            "Distance Weight", 
            0.0, 1.0, 0.4, 0.1,
            help="How much does physical distance matter? Higher = prioritize shorter routes."
        )
        st.caption("📏 Prefer shortest physical distance")
    
    with col3:
        time_weight = st.slider(
            "Time Weight", 
            0.0, 1.0, 0.4, 0.1,
            help="How much does travel time matter? Higher = prioritize faster routes."
        )
        st.caption("⏱️ Prefer quickest travel time")
    
    with col4:
        traffic_weight = st.slider(
            "Traffic Weight", 
            0.0, 1.0, 0.2, 0.1,
            help="How much do you want to avoid traffic? Higher = avoid congested routes."
        )
        st.caption("🚦 Avoid heavy traffic areas")
    
    # Find route button
    col1, col2 = st.columns([1, 4])
    with col1:
        find_button = st.button("🔍 Find Route", type="primary")
    with col2:
        if hasattr(st.session_state, 'route_results') and st.session_state.route_results:
            if st.button("🗑️ Clear Route"):
                st.session_state.route_results = None
                st.session_state.current_path = None
                st.rerun()
    
    if find_button:
        if start_id == end_id:
            st.warning("⚠️ Start and end locations are the same!")
            st.session_state.route_results = None
        else:
            finder = ShortestPathFinder(graph)
            
            results = {}
            
            with st.spinner("Finding optimal route..."):
                if algorithm in ["Dijkstra", "Both"]:
                    results["Dijkstra"] = finder.dijkstra(
                        start_id, end_id, dist_weight, time_weight, traffic_weight
                    )
                
                if algorithm in ["A*", "Both"]:
                    results["A*"] = finder.a_star(
                        start_id, end_id, dist_weight, time_weight, traffic_weight
                    )
            
            # Store results in session state
            st.session_state.route_results = results if results else None
            st.session_state.current_path = list(results.values())[0].path if results else None
    
    # Display results from session state (persists across reruns)
    if hasattr(st.session_state, 'route_results') and st.session_state.route_results:
        results = st.session_state.route_results
        
        st.success("✅ Route found! Your optimal path is highlighted in blue on the map.")
        
        # Show map
        st.subheader("🗺️ Route Visualization")
        st.markdown("🟢 **Green marker** = Start • 🔴 **Red marker** = End • 🔵 **Blue line** = Your route")
        m = create_map(
            graph,
            highlight_path=st.session_state.current_path,
            stations=st.session_state.stations
        )
        st_folium(m, width=900, height=500)
        
        # Route details
        st.subheader("📋 Route Details")
        st.markdown("**Performance metrics and step-by-step directions** for your journey:")
        
        for algo_name, result in results.items():
            with st.expander(f"🔍 {algo_name} Algorithm Results", expanded=True):
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Distance", f"{result.total_distance:.2f} km", help="Total physical distance")
                    st.caption("📏 Physical length")
                with col2:
                    st.metric("Time", f"{result.total_time:.1f} min", help="Estimated travel time")
                    st.caption("⏱️ Duration")
                with col3:
                    st.metric("Total Cost", f"{result.total_cost:.2f}", help="Weighted cost based on your preferences")
                    st.caption("💰 Optimized score")
                with col4:
                    st.metric("Nodes Explored", result.nodes_explored, help="How many locations the algorithm checked")
                    st.caption("🔍 Efficiency")
                
                st.markdown("**Turn-by-turn directions:**")
                st.caption("Follow these waypoints from start to finish:")
                for i, node_id in enumerate(result.path):
                    node = graph.get_node(node_id)
                    if i == 0:
                        st.markdown(f"🟢 **Start:** {node.name}")
                    elif i == len(result.path) - 1:
                        st.markdown(f"🔴 **End:** {node.name}")
                    else:
                        st.markdown(f"↓ {node.name}")
                        
                        # Show segment info
                        if i < len(result.path) - 1:
                            next_id = result.path[i + 1]
                            for edge in graph.get_neighbors(node_id):
                                if edge.destination == next_id:
                                    st.caption(
                                        f"   → {edge.distance:.2f} km, "
                                        f"{edge.time:.1f} min, "
                                        f"traffic: {edge.traffic:.1f}x"
                                    )
                                    break
        
        # Performance comparison
        if len(results) > 1:
            st.subheader("📊 Algorithm Comparison")
            st.markdown("""**Side-by-side comparison** of both algorithms. 
            💡 **Key insight:** A* typically explores fewer nodes but may have slightly different routes than Dijkstra.""")
            fig = create_performance_chart(results)
            st.plotly_chart(fig, use_container_width=True)
    elif hasattr(st.session_state, 'route_results') and st.session_state.route_results is None:
        st.error("❌ No route found between these locations!")


def show_station_placement_page(graph):
    """Display station placement page."""
    st.header("📍 Station Placement Optimization")
    
    st.info("""📖 **What is this?** 
    This page uses smart algorithms to decide where to place bike stations for maximum effectiveness. 
    The goal is to ensure people can easily access stations while considering demand and coverage.
    """)
    
    with st.expander("ℹ️ Understanding Station Placement"):
        st.markdown("""
        **Why This Matters:**
        - Poor station placement = wasted resources and unhappy users
        - Good placement = high usage, better coverage, satisfied customers
        - Optimization algorithms help find the best locations mathematically
        
        **Three Different Approaches:**
        - **Greedy Coverage**: Spreads stations out to maximize geographic coverage
        - **K-Means Clustering**: Groups locations and places stations at cluster centers
        - **Demand-Based**: Prioritizes high-demand areas (downtown, transit hubs, etc.)
        
        **Key Metrics to Watch:**
        - **Coverage %**: How much of the network is within reach of a station
        - **Station Distance**: How far apart stations are (not too close, not too far)
        - **Connections**: Well-connected stations serve more routes
        """)
    
    # Settings
    col1, col2, col3 = st.columns(3)
    
    with col1:
        num_stations = st.slider(
            "Number of Stations", 
            1, 10, 5,
            help="More stations = better coverage but higher cost. Find the right balance!"
        )
        st.caption("💰 Budget vs Coverage trade-off")
    
    with col2:
        algorithm = st.selectbox(
            "Placement Algorithm",
            ["Greedy Coverage", "K-Means Clustering", "Demand-Based"],
            help="Each algorithm optimizes differently. Try them all to compare!"
        )
        st.caption("🎯 Different optimization strategies")
    
    with col3:
        coverage_radius = st.slider(
            "Coverage Radius (km)", 
            0.1, 2.0, 0.5, 0.1,
            help="How far are people willing to walk to a station? Typical: 0.5km (5-10 min walk)"
        )
        st.caption("🚶 Acceptable walking distance")
    
    # Demand settings
    st.subheader("🔥 High-Demand Areas")
    st.markdown("""Adjust demand levels for different area types. Higher demand = more likely to place a station there.
    💡 **Real-world insight:** Business districts see peak demand during work hours, transit hubs during rush hour, educational areas during school terms.""")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        downtown_demand = st.slider(
            "Downtown/Business", 
            0.0, 1.0, 1.0, 0.1,
            help="Office workers, shoppers, business travelers - typically highest demand!"
        )
        st.caption("👔 Business & commercial centers")
    with col2:
        transit_demand = st.slider(
            "Transit Hubs", 
            0.0, 1.0, 0.9, 0.1,
            help="Train stations, bus terminals - crucial connection points for commuters!"
        )
        st.caption("🚉 Trains, buses, subways")
    with col3:
        education_demand = st.slider(
            "Educational", 
            0.0, 1.0, 0.8, 0.1,
            help="Students are major bike-share users! Universities see high, consistent usage."
        )
        st.caption("🎓 Universities & colleges")
    
    # Optimize button
    col1, col2 = st.columns([1, 4])
    with col1:
        optimize_button = st.button("🎯 Optimize Station Placement", type="primary")
    with col2:
        if hasattr(st.session_state, 'placement_results') and st.session_state.placement_results:
            if st.button("🗑️ Clear Placement"):
                st.session_state.placement_results = None
                st.rerun()
    
    if optimize_button:
        optimizer = StationPlacementOptimizer(graph)
        
        # Set demand
        high_density_areas = [
            (40.7589, -73.9851, downtown_demand),  # Downtown
            (40.7527, -73.9772, transit_demand),    # Train station
            (40.7630, -73.9840, education_demand),  # University
        ]
        optimizer.set_demand_by_density(high_density_areas)
        
        with st.spinner("Optimizing station placement..."):
            if algorithm == "Greedy Coverage":
                stations = optimizer.greedy_station_placement(
                    num_stations, max_coverage_distance=coverage_radius
                )
            elif algorithm == "K-Means Clustering":
                stations = optimizer.kmeans_clustering_placement(num_stations)
            else:  # Demand-Based
                stations = optimizer.demand_based_placement(num_stations, demand_threshold=0.3)
            
            # Update stations in graph
            for node in graph.nodes.values():
                node.is_station = node.node_id in stations
                if node.is_station:
                    node.capacity = 20
            
            st.session_state.stations = stations
            
            # Calculate metrics
            metrics = optimizer.evaluate_placement(stations)
            
            # Store in session state
            st.session_state.placement_results = {
                'stations': stations,
                'algorithm': algorithm,
                'metrics': metrics,
                'optimizer': optimizer
            }
    
    # Display results from session state (persists across reruns)
    if hasattr(st.session_state, 'placement_results') and st.session_state.placement_results:
        results = st.session_state.placement_results
        stations = results['stations']
        metrics = results['metrics']
        optimizer = results['optimizer']
        
        st.success(f"✅ Placed {len(stations)} stations using {results['algorithm']}!")
        
        # Show map
        st.subheader("🗺️ Station Placement Map")
        m = create_map(graph, stations=stations)
        st_folium(m, width=900, height=500)
        
        # Evaluation metrics
        st.subheader("📊 Placement Evaluation")
        st.markdown("""**How good is this placement?** These metrics help you evaluate the quality of your station network:""")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Coverage", 
                f"{metrics['coverage']*100:.1f}%",
                help="Percentage of network within walking distance of a station. Aim for 80%+!"
            )
            st.caption("🎯 Target: 80-90%")
        with col2:
            st.metric(
                "Avg Station Distance", 
                f"{metrics['avg_station_distance']:.2f} km",
                help="Average distance between stations. Too close = wasteful, too far = poor coverage."
            )
            st.caption("📏 Sweet spot: 0.8-1.5 km")
        with col3:
            st.metric(
                "Min Distance", 
                f"{metrics['min_station_distance']:.2f} km",
                help="Closest two stations. Should not be too close (cannibalization) or too far."
            )
            st.caption("⚠️ Avoid: < 0.3 km")
        with col4:
            st.metric(
                "Avg Connections", 
                f"{metrics['avg_connections_per_station']:.1f}",
                help="Average routes per station. More = better utility and flexibility."
            )
            st.caption("🌟 Higher is better")
        
        # Coverage heatmap
        st.subheader("🌡️ Coverage Heatmap")
        st.markdown("""**Visual coverage analysis:** 
        - 🟢 **Green areas**: Well served (< 0.5km to station) - Great!
        - 🟡 **Yellow areas**: Moderate coverage (0.5-1km) - Acceptable
        - 🔴 **Red areas**: Poor coverage (> 1km) - Need attention!
        
        💡 **Use this to:** Identify coverage gaps and decide where to add more stations.""")
        fig = create_coverage_heatmap(graph, stations, optimizer)
        st.plotly_chart(fig, use_container_width=True)
        
        # Station list
        st.subheader("📋 Selected Stations")
        st.markdown("**Detailed information** about each optimally-placed station. These locations will serve as bike pickup/dropoff points.")
        station_data = []
        for station_id in stations:
            node = graph.get_node(station_id)
            station_data.append({
                "ID": node.node_id,
                "Name": node.name,
                "Latitude": f"{node.lat:.4f}",
                "Longitude": f"{node.lon:.4f}",
                "Demand": f"{node.demand:.2f}",
                "Capacity": node.capacity
            })
        
        df = pd.DataFrame(station_data)
        st.dataframe(df, use_container_width=True)


def show_network_analysis_page(graph):
    """Display network analysis page."""
    st.header("📊 Network Analysis")
    
    st.info("""📖 **What is this?** 
    This page provides data-driven insights into your bike-sharing network. 
    Understand connectivity patterns, traffic bottlenecks, and demand distribution to make informed decisions.
    """)
    
    with st.expander("ℹ️ Understanding Network Analytics"):
        st.markdown("""
        **Why Analytics Matter:**
        - Identify bottlenecks before they become problems
        - Understand usage patterns to optimize resources
        - Data-driven decisions beat guesswork every time
        
        **What to Look For:**
        - **High connectivity nodes**: Natural hub locations for stations
        - **Traffic hotspots**: Routes that need capacity improvements
        - **Demand clusters**: Areas that need more stations
        - **Coverage gaps**: Underserved areas needing attention
        
        **Actionable Insights:**
        - Use connectivity data to prioritize station placement
        - Traffic analysis helps identify infrastructure needs
        - Demand distribution guides marketing and expansion
        """)
    
    optimizer = StationPlacementOptimizer(graph)
    
    # Network overview
    st.subheader("🌐 Network Overview")
    st.markdown("**Key metrics** about your bike-sharing network. These numbers tell you about network size and effectiveness.")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Nodes", graph.node_count(), help="Total locations in the network")
        st.metric("Total Edges", graph.edge_count(), help="Total connections between locations")
        st.caption("📊 Network size")
    
    with col2:
        avg_connections = graph.edge_count() / graph.node_count() if graph.node_count() > 0 else 0
        st.metric("Avg Connections per Node", f"{avg_connections:.2f}", help="Average routes per location - higher is better!")
        st.metric("Bike Stations", len(st.session_state.stations), help="Active bike stations")
        st.caption("🔗 Connectivity")
    
    with col3:
        if st.session_state.stations:
            coverage = optimizer.calculate_coverage(st.session_state.stations, 0.5)
            st.metric("Network Coverage", f"{coverage*100:.1f}%", help="Percentage of network within 0.5km of a station")
        else:
            st.metric("Network Coverage", "0%", help="No stations placed yet - visit Station Placement page!")
        
        st.metric("Coverage Radius", "0.5 km", help="Maximum acceptable walking distance")
        st.caption("🎯 Reach")
    
    # Degree distribution
    st.subheader("📈 Node Connectivity Distribution")
    st.markdown("""This histogram shows how many connections each location has. 
    **Well-connected locations** (more connections) are better candidates for bike stations because they serve more routes.
    💡 **Look for:** Peaks on the right side indicate highly connected hub locations.""")
    
    degrees = [len(graph.get_neighbors(node_id)) for node_id in graph.nodes.keys()]
    
    fig = go.Figure(data=[go.Histogram(x=degrees, nbinsx=20)])
    fig.update_layout(
        title="Distribution of Node Connections",
        xaxis_title="Number of Connections",
        yaxis_title="Number of Nodes",
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Traffic analysis
    st.subheader("🚦 Traffic Analysis")
    st.markdown("""This scatter plot shows the relationship between distance and actual travel time. 
    **Color indicates traffic level** - red dots are heavily congested routes that take much longer than expected.
    💡 **Action:** Consider adding stations on congested routes to provide relief alternatives.""")
    
    traffic_data = []
    for node_id, edges in graph.edges.items():
        for edge in edges:
            traffic_data.append({
                "From": graph.get_node(node_id).name,
                "To": graph.get_node(edge.destination).name,
                "Distance (km)": edge.distance,
                "Time (min)": edge.time,
                "Traffic Factor": edge.traffic,
                "Effective Time": edge.time * edge.traffic
            })
    
    df = pd.DataFrame(traffic_data)
    
    fig = px.scatter(
        df,
        x="Distance (km)",
        y="Effective Time",
        color="Traffic Factor",
        size="Time (min)",
        hover_data=["From", "To"],
        title="Distance vs Effective Travel Time (colored by traffic)"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Top connections
    st.subheader("🔝 Most Congested Routes")
    st.markdown("""These are the most congested routes in your network. High traffic routes may need:
    - **Additional bike stations** to distribute demand
    - **Alternative paths** to relieve congestion
    - **Increased bike availability** during peak hours
    💡 **Strategy:** Prioritize improvements on routes with both high traffic AND high demand.""")
    
    df_sorted = df.nlargest(10, "Traffic Factor")
    st.dataframe(df_sorted[["From", "To", "Distance (km)", "Time (min)", "Traffic Factor"]], 
                 use_container_width=True)
    
    # Demand distribution
    if any(node.demand > 0 for node in graph.nodes.values()):
        st.subheader("🔥 Demand Distribution")
        st.markdown("""High-demand locations need more attention and resources. 
        **These locations should be top priorities** for station placement, maintenance, and bike availability.
        💡 **Real-world tip:** Demand can vary by time of day - consider peak hours in your planning!""")
        
        demand_data = {
            "Location": [node.name for node in graph.get_all_nodes()],
            "Demand": [node.demand for node in graph.get_all_nodes()]
        }
        
        df_demand = pd.DataFrame(demand_data)
        df_demand = df_demand[df_demand["Demand"] > 0].sort_values("Demand", ascending=False)
        
        fig = px.bar(
            df_demand.head(10),
            x="Demand",
            y="Location",
            orientation='h',
            title="Top 10 High-Demand Locations"
        )
        st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    main()
