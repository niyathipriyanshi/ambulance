import streamlit as st
import time
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random
import math

# Page configuration
st.set_page_config(
    page_title="NEXUS Traffic AI - Delhi Emergency Response",
    page_icon="🚁",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Advanced CSS with animations and modern design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Inter:wght@300;400;500;600;700&display=swap');
    
    .main {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
        color: #ffffff;
        font-family: 'Inter', sans-serif;
    }
    
    .stApp > header {
        background-color: transparent;
    }
    
    /* Hide default streamlit elements */
    .css-1d391kg, .css-18e3th9, .css-1rs6os, .css-17eq0hr {
        background-color: transparent !important;
    }
    
    /* Custom title styling */
    .nexus-title {
        font-family: 'Orbitron', monospace;
        background: linear-gradient(45deg, #00d4ff, #ff6b35, #ff006e);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: gradientShift 3s ease infinite;
        text-align: center;
        font-size: 3.5rem;
        font-weight: 900;
        margin-bottom: 10px;
        text-shadow: 0 0 30px rgba(0, 212, 255, 0.5);
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .subtitle {
        text-align: center;
        color: #8892b0;
        font-size: 1.2rem;
        margin-bottom: 30px;
        font-weight: 300;
    }
    
    /* Emergency Control Panel */
    .control-panel {
        background: linear-gradient(135deg, #1e2139 0%, #2a2d5a 100%);
        border: 1px solid #00d4ff;
        border-radius: 20px;
        padding: 25px;
        margin: 20px 0;
        box-shadow: 0 10px 30px rgba(0, 212, 255, 0.2);
        position: relative;
        overflow: hidden;
    }
    
    .control-panel::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(0, 212, 255, 0.1), transparent);
        animation: scanline 3s infinite;
    }
    
    @keyframes scanline {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    /* Emergency Alert */
    .emergency-alert {
        background: linear-gradient(45deg, #ff006e, #ff4757, #ff6b35);
        background-size: 300% 300%;
        animation: gradientShift 1s ease infinite, emergencyPulse 0.5s ease-in-out infinite alternate;
        color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        font-weight: bold;
        font-size: 1.1rem;
        margin: 20px 0;
        border: 2px solid #fff;
        box-shadow: 0 0 30px rgba(255, 0, 110, 0.6);
    }
    
    @keyframes emergencyPulse {
        from { transform: scale(1); box-shadow: 0 0 30px rgba(255, 0, 110, 0.6); }
        to { transform: scale(1.02); box-shadow: 0 0 40px rgba(255, 0, 110, 0.8); }
    }
    
    /* Traffic Intersection Cards */
    .intersection-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border: 1px solid #444;
        border-radius: 15px;
        padding: 20px;
        margin: 10px;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
        min-height: 200px;
    }
    
    .intersection-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0, 212, 255, 0.3);
        border-color: #00d4ff;
    }
    
    .ambulance-route {
        background: linear-gradient(135deg, #ff6b35 0%, #f7931e 100%);
        border: 2px solid #fff;
        animation: routeGlow 2s ease-in-out infinite alternate;
        color: #fff;
    }
    
    .ambulance-here {
        background: linear-gradient(45deg, #00d4ff, #ff006e, #ff6b35);
        background-size: 300% 300%;
        animation: gradientShift 1s ease infinite, ambulancePulse 1s ease-in-out infinite alternate;
        border: 3px solid #fff;
        color: #fff;
        font-weight: bold;
    }
    
    @keyframes routeGlow {
        from { box-shadow: 0 0 20px rgba(255, 107, 53, 0.6); }
        to { box-shadow: 0 0 30px rgba(255, 107, 53, 0.9); }
    }
    
    @keyframes ambulancePulse {
        from { transform: scale(1); }
        to { transform: scale(1.05); }
    }
    
    /* Traffic Light Animation */
    .traffic-light {
        font-size: 4rem;
        margin: 15px 0;
        display: block;
        text-align: center;
        filter: drop-shadow(0 0 10px currentColor);
        animation: lightPulse 2s ease-in-out infinite;
    }
    
    @keyframes lightPulse {
        0%, 100% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.1); opacity: 0.8; }
    }
    
    /* Metrics Cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 25px;
        text-align: center;
        color: white;
        margin: 10px 0;
        transition: transform 0.3s ease;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .metric-card:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        font-family: 'Orbitron', monospace;
        margin: 10px 0;
        text-shadow: 0 0 15px currentColor;
    }
    
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Status Indicators */
    .status-indicator {
        display: inline-block;
        padding: 8px 15px;
        border-radius: 25px;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin: 5px;
    }
    
    .status-emergency {
        background: linear-gradient(45deg, #ff006e, #ff4757);
        color: white;
        animation: statusPulse 1s ease-in-out infinite alternate;
    }
    
    .status-normal {
        background: linear-gradient(45deg, #2ed573, #17a2b8);
        color: white;
    }
    
    .status-route {
        background: linear-gradient(45deg, #ff6b35, #f7931e);
        color: white;
    }
    
    @keyframes statusPulse {
        from { opacity: 1; }
        to { opacity: 0.7; }
    }
    
    /* Control Buttons */
    .control-button {
        background: linear-gradient(45deg, #00d4ff, #0099cc);
        border: none;
        border-radius: 10px;
        color: white;
        padding: 15px 30px;
        font-size: 1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        margin: 10px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .control-button:hover {
        background: linear-gradient(45deg, #0099cc, #00d4ff);
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(0, 212, 255, 0.4);
    }
    
    .emergency-button {
        background: linear-gradient(45deg, #ff006e, #ff4757);
        animation: buttonPulse 2s ease-in-out infinite;
    }
    
    .emergency-button:hover {
        background: linear-gradient(45deg, #ff4757, #ff006e);
    }
    
    @keyframes buttonPulse {
        0%, 100% { box-shadow: 0 0 0 0 rgba(255, 0, 110, 0.7); }
        50% { box-shadow: 0 0 0 10px rgba(255, 0, 110, 0); }
    }
    
    /* Vehicle Counter Animation */
    .vehicle-counter {
        font-family: 'Orbitron', monospace;
        font-size: 1.2rem;
        font-weight: 600;
        color: #00d4ff;
        text-shadow: 0 0 10px #00d4ff;
    }
    
    /* Route Progress Bar */
    .route-progress {
        width: 100%;
        height: 8px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 4px;
        overflow: hidden;
        margin: 15px 0;
    }
    
    .route-progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #00d4ff, #ff6b35);
        border-radius: 4px;
        transition: width 0.5s ease;
        animation: progressGlow 2s ease-in-out infinite alternate;
    }
    
    @keyframes progressGlow {
        from { box-shadow: 0 0 10px rgba(0, 212, 255, 0.5); }
        to { box-shadow: 0 0 20px rgba(255, 107, 53, 0.8); }
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .nexus-title { font-size: 2.5rem; }
        .intersection-card { margin: 5px; padding: 15px; }
        .metric-value { font-size: 2rem; }
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'emergency_active' not in st.session_state:
    st.session_state.emergency_active = False
    st.session_state.emergency_start_time = None
    st.session_state.ambulance_route = []
    st.session_state.ambulance_position = 0
    st.session_state.traffic_history = []
    st.session_state.route_progress = 0
    st.session_state.emergency_id = 0

# Delhi intersections with enhanced data
DELHI_INTERSECTIONS = {
    "Connaught Place": {
        "lat": 28.6315, "lon": 77.2167, "status": "red", "vehicles": 45, 
        "normal_cycle": "red", "zone": "Central", "priority": "high",
        "ambulance_time": 0, "congestion_level": 0.8
    },
    "India Gate": {
        "lat": 28.6129, "lon": 77.2295, "status": "green", "vehicles": 32, 
        "normal_cycle": "yellow", "zone": "Central", "priority": "medium",
        "ambulance_time": 0, "congestion_level": 0.6
    },
    "Red Fort": {
        "lat": 28.6562, "lon": 77.2410, "status": "yellow", "vehicles": 28, 
        "normal_cycle": "green", "zone": "Old Delhi", "priority": "medium",
        "ambulance_time": 0, "congestion_level": 0.5
    },
    "Karol Bagh": {
        "lat": 28.6519, "lon": 77.1906, "status": "green", "vehicles": 38, 
        "normal_cycle": "red", "zone": "West", "priority": "high",
        "ambulance_time": 0, "congestion_level": 0.7
    },
    "Chandni Chowk": {
        "lat": 28.6506, "lon": 77.2334, "status": "red", "vehicles": 52, 
        "normal_cycle": "yellow", "zone": "Old Delhi", "priority": "high",
        "ambulance_time": 0, "congestion_level": 0.9
    },
    "Rajouri Garden": {
        "lat": 28.6470, "lon": 77.1203, "status": "yellow", "vehicles": 25, 
        "normal_cycle": "green", "zone": "West", "priority": "low",
        "ambulance_time": 0, "congestion_level": 0.4
    },
    "Lajpat Nagar": {
        "lat": 28.5677, "lon": 77.2428, "status": "green", "vehicles": 33, 
        "normal_cycle": "red", "zone": "South", "priority": "medium",
        "ambulance_time": 0, "congestion_level": 0.6
    },
    "Nehru Place": {
        "lat": 28.5494, "lon": 77.2524, "status": "red", "vehicles": 41, 
        "normal_cycle": "yellow", "zone": "South", "priority": "high",
        "ambulance_time": 0, "congestion_level": 0.75
    }
}

# Enhanced ambulance routes with estimated times
AMBULANCE_ROUTES = {
    "🏥 AIIMS → Red Fort (Critical)": {
        "route": ["Connaught Place", "India Gate", "Red Fort"],
        "hospital": "AIIMS", "destination": "Red Fort Hospital",
        "estimated_time": "8 min", "priority": "Critical"
    },
    "🚑 Safdarjung → Chandni Chowk": {
        "route": ["Connaught Place", "Karol Bagh", "Chandni Chowk"],
        "hospital": "Safdarjung", "destination": "LNJP Hospital",
        "estimated_time": "12 min", "priority": "High"
    },
    "🏥 Max Hospital → LNJP (Emergency)": {
        "route": ["Rajouri Garden", "Karol Bagh", "Connaught Place", "Chandni Chowk"],
        "hospital": "Max Hospital", "destination": "LNJP Hospital",
        "estimated_time": "15 min", "priority": "Emergency"
    },
    "🚁 Apollo → Fortis (Trauma)": {
        "route": ["Lajpat Nagar", "Nehru Place", "India Gate", "Connaught Place"],
        "hospital": "Apollo", "destination": "Fortis Hospital",
        "estimated_time": "10 min", "priority": "Trauma"
    }
}

def get_traffic_light_emoji(status):
    emojis = {"red": "🔴", "yellow": "🟡", "green": "🟢"}
    return emojis[status]

def simulate_emergency_response():
    """Enhanced emergency response with realistic timing"""
    if st.session_state.emergency_active and st.session_state.ambulance_route:
        route = st.session_state.ambulance_route
        elapsed_time = time.time() - st.session_state.emergency_start_time
        
        # Calculate route progress
        total_route_time = 30  # seconds
        progress = min(100, (elapsed_time / total_route_time) * 100)
        st.session_state.route_progress = progress
        
        # Dynamic ambulance position
        position_in_route = min(len(route) - 1, int((elapsed_time / 6) % len(route)))
        st.session_state.ambulance_position = position_in_route
        
        # Clear the route dynamically
        for i, intersection in enumerate(DELHI_INTERSECTIONS):
            if intersection in route:
                # Turn route intersections green with timing
                DELHI_INTERSECTIONS[intersection]["status"] = "green"
                DELHI_INTERSECTIONS[intersection]["ambulance_time"] = elapsed_time
                
                # Reduce vehicles as ambulance passes
                if i <= position_in_route:
                    DELHI_INTERSECTIONS[intersection]["vehicles"] = max(3, 
                        DELHI_INTERSECTIONS[intersection]["vehicles"] - 3)
            else:
                # Turn other intersections red
                DELHI_INTERSECTIONS[intersection]["status"] = "red"
                # Gradually increase vehicles at stopped intersections
                DELHI_INTERSECTIONS[intersection]["vehicles"] = min(65, 
                    DELHI_INTERSECTIONS[intersection]["vehicles"] + 1)
        
        # Auto-end emergency after 45 seconds
        if elapsed_time > 45:
            end_emergency()

def end_emergency():
    """Enhanced emergency ending with restoration"""
    st.session_state.emergency_active = False
    st.session_state.emergency_start_time = None
    st.session_state.ambulance_route = []
    st.session_state.ambulance_position = 0
    st.session_state.route_progress = 0
    st.session_state.emergency_id += 1
    
    # Gradually restore normal traffic patterns
    for intersection in DELHI_INTERSECTIONS:
        DELHI_INTERSECTIONS[intersection]["status"] = DELHI_INTERSECTIONS[intersection]["normal_cycle"]
        DELHI_INTERSECTIONS[intersection]["vehicles"] = random.randint(20, 55)
        DELHI_INTERSECTIONS[intersection]["ambulance_time"] = 0

def create_enhanced_network_map():
    """Create an advanced animated network visualization"""
    # Dynamic positioning with slight movement
    base_positions = {
        "Connaught Place": (0, 0), "India Gate": (1.2, -0.8),
        "Red Fort": (0.6, 1.5), "Karol Bagh": (-1.3, 0.7),
        "Chandni Chowk": (0.2, 2), "Rajouri Garden": (-2, 0.2),
        "Lajpat Nagar": (0.8, -1.5), "Nehru Place": (1.5, -2)
    }
    
    # Add slight animation to positions
    time_factor = time.time() * 0.5
    positions = {}
    for intersection, (x, y) in base_positions.items():
        # Add subtle movement
        offset_x = 0.05 * math.sin(time_factor + x)
        offset_y = 0.05 * math.cos(time_factor + y)
        positions[intersection] = (x + offset_x, y + offset_y)
    
    fig = go.Figure()
    
    # Add background grid with animation
    for i in range(-3, 4):
        opacity = 0.1 + 0.05 * math.sin(time_factor + i)
        fig.add_shape(
            type="line", x0=i, y0=-3, x1=i, y1=3,
            line=dict(color=f"rgba(0,212,255,{opacity})", width=1)
        )
        fig.add_shape(
            type="line", x0=-3, y0=i, x1=3, y1=i,
            line=dict(color=f"rgba(0,212,255,{opacity})", width=1)
        )
    
    # Add route connections first (behind intersections)
    if st.session_state.emergency_active and st.session_state.ambulance_route:
        route = st.session_state.ambulance_route
        route_x = [positions[intersection][0] for intersection in route]
        route_y = [positions[intersection][1] for intersection in route]
        
        # Animated route line
        progress = st.session_state.route_progress / 100
        
        fig.add_trace(go.Scatter(
            x=route_x, y=route_y,
            mode='lines',
            line=dict(width=8, color='rgba(255,107,53,0.3)'),
            showlegend=False, hoverinfo='skip'
        ))
        
        # Progress line
        if progress > 0:
            prog_points = int(progress * len(route_x))
            if prog_points > 1:
                fig.add_trace(go.Scatter(
                    x=route_x[:prog_points], y=route_y[:prog_points],
                    mode='lines',
                    line=dict(width=12, color='#ff6b35'),
                    showlegend=False, hoverinfo='skip'
                ))
    
    # Add intersection nodes
    x_coords, y_coords, colors, sizes, texts, symbols = [], [], [], [], [], []
    
    for intersection, data in DELHI_INTERSECTIONS.items():
        x, y = positions[intersection]
        x_coords.append(x)
        y_coords.append(y)
        
        # Enhanced color mapping with glow effects
        if data["status"] == "green":
            colors.append("#2ed573")
        elif data["status"] == "yellow":
            colors.append("#ffa502")
        else:
            colors.append("#ff4757")
        
        # Dynamic sizing based on vehicles and congestion
        base_size = 25
        congestion_multiplier = 1 + (data["congestion_level"] * 0.5)
        vehicle_multiplier = 1 + (data["vehicles"] / 100)
        final_size = base_size * congestion_multiplier * vehicle_multiplier
        sizes.append(min(60, max(20, final_size)))
        
        # Check ambulance status
        is_on_route = intersection in st.session_state.ambulance_route
        is_ambulance_here = (st.session_state.emergency_active and is_on_route and 
                           len(st.session_state.ambulance_route) > st.session_state.ambulance_position and
                           st.session_state.ambulance_route[st.session_state.ambulance_position] == intersection)
        
        if is_ambulance_here:
            symbols.append("star")
            texts.append(f"🚑 AMBULANCE ACTIVE<br><b>{intersection}</b><br>Signal: {data['status'].upper()}<br>Vehicles: {data['vehicles']}<br>Zone: {data['zone']}<br>Priority: {data['priority'].upper()}")
        elif is_on_route:
            symbols.append("diamond")
            texts.append(f"🚨 EMERGENCY CORRIDOR<br><b>{intersection}</b><br>Signal: {data['status'].upper()}<br>Vehicles: {data['vehicles']}<br>Zone: {data['zone']}")
        else:
            symbols.append("circle")
            texts.append(f"<b>{intersection}</b><br>Signal: {data['status'].upper()}<br>Vehicles: {data['vehicles']}<br>Zone: {data['zone']}<br>Congestion: {int(data['congestion_level']*100)}%")
    
    # Main intersection scatter plot
    fig.add_trace(go.Scatter(
        x=x_coords, y=y_coords,
        mode='markers+text',
        marker=dict(
            size=sizes, color=colors, symbol=symbols,
            opacity=0.9, line=dict(width=3, color='white')
        ),
        text=[name.replace(' ', '<br>') for name in DELHI_INTERSECTIONS.keys()],
        textposition="bottom center",
        textfont=dict(size=9, color='white', family='Inter'),
        hovertext=texts,
        hovertemplate='%{hovertext}<extra></extra>',
        showlegend=False
    ))
    
    # Add ambulance trail effect
    if st.session_state.emergency_active and st.session_state.ambulance_position > 0:
        trail_route = st.session_state.ambulance_route[:st.session_state.ambulance_position+1]
        trail_x = [positions[intersection][0] for intersection in trail_route]
        trail_y = [positions[intersection][1] for intersection in trail_route]
        
        fig.add_trace(go.Scatter(
            x=trail_x, y=trail_y,
            mode='markers',
            marker=dict(size=15, color='cyan', symbol='circle', opacity=0.6),
            showlegend=False, hoverinfo='skip'
        ))
    
    # Layout with dark theme and animations
    fig.update_layout(
        title=dict(
            text="🌐 NEXUS Traffic Network - Real-time Monitoring",
            font=dict(size=20, color='white', family='Orbitron'),
            x=0.5
        ),
        xaxis=dict(
            showgrid=False, showticklabels=False, 
            range=[-3, 3], color='white'
        ),
        yaxis=dict(
            showgrid=False, showticklabels=False, 
            range=[-3, 3], color='white'
        ),
        height=600,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(26,26,46,0.3)',
        font=dict(color='white', family='Inter')
    )
    
    return fig

# Main Application
st.markdown('<h1 class="nexus-title">🚁 NEXUS TRAFFIC AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Advanced Emergency Response & Traffic Optimization System</p>', unsafe_allow_html=True)

# Emergency Control Panel
st.markdown('<div class="control-panel">', unsafe_allow_html=True)
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    st.markdown("### 🚨 Emergency Control Center")
    selected_route_key = st.selectbox(
        "Select Emergency Route:",
        list(AMBULANCE_ROUTES.keys()),
        help="Choose ambulance route for emergency response activation"
    )
    
    route_info = AMBULANCE_ROUTES[selected_route_key]
    st.markdown(f"**Route:** {route_info['hospital']} → {route_info['destination']}")
    st.markdown(f"**Estimated Time:** {route_info['estimated_time']} | **Priority:** {route_info['priority']}")

with col2:
    if st.button("🚑 ACTIVATE EMERGENCY", type="primary", disabled=st.session_state.emergency_active):
        st.session_state.emergency_active = True
        st.session_state.emergency_start_time = time.time()
        st.session_state.ambulance_route = route_info["route"]
        st.session_state.ambulance_position = 0
        st.session_state.route_progress = 0
        st.success("Emergency Activated!")

with col3:
    if st.session_state.emergency_active and st.button("🛑 END EMERGENCY", type="secondary"):
        end_emergency()
        st.info("Emergency Terminated")

st.markdown('</div>', unsafe_allow_html=True)

# Emergency Status Display
if st.session_state.emergency_active:
    elapsed = time.time() - st.session_state.emergency_start_time
    remaining = max(0, 45 - elapsed)
    
    st.markdown(f"""
    <div class="emergency-alert">
        🚨 EMERGENCY PROTOCOL ACTIVE: {selected_route_key.split('→')[0]} 🚨<br>
        <strong>Time Remaining: {remaining:.1f}s | Route Progress: {st.session_state.route_progress:.1f}%</strong>
    </div>
    """, unsafe_allow_html=True)
    
    # Route Progress Bar
    st.markdown(f"""
    <div class="route-progress">
        <div class="route-progress-fill" style="width: {st.session_state.route_progress}%"></div>
    </div>
    """, unsafe_allow_html=True)

# Simulate emergency response
simulate_emergency_response()

# Main Dashboard
col1, col2 = st.columns([2.5, 1])

with col1:
    st.markdown("### 🗺️ Live Network Visualization")
    network_map = create_enhanced_network_map()
    st.plotly_chart(network_map, use_container_width=True)

with col2:
    st.markdown("### 📊 System Metrics")
    
    # Calculate enhanced metrics
    total_vehicles = sum(data["vehicles"] for data in DELHI_INTERSECTIONS.values())
    green_lights = sum(1 for data in DELHI_INTERSECTIONS.values() if data["status"] == "green")
    avg_congestion = np.mean([data["congestion_level"] for data in DELHI_INTERSECTIONS.values()])
    
    # Display metrics with enhanced styling
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Total Vehicles</div>
        <div class="metric-value">{total_vehicles}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Active Green Signals</div>
        <div class="metric-value">{green_lights}/8</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Network Congestion</div>
        <div class="metric-value">{int(avg_congestion*100)}%</div>
    </div>
    """, unsafe_allow_html=True)
    
    response_time = "< 2 min" if st.session_state.emergency_active else "4.2 min"
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Response Time</div>
        <div class="metric-value">{response_time}</div>
    </div>
    """, unsafe_allow_html=True)

# Enhanced Intersection Status Grid
st.markdown("### 🚦 Live Intersection Control Matrix")

# Create 4 columns for better layout
cols = st.columns(4)
intersections = list(DELHI_INTERSECTIONS.items())

for idx, (intersection, data) in enumerate(intersections):
    col_idx = idx % 4
    
    with cols[col_idx]:
        # Determine card styling based on status
        is_on_route = intersection in st.session_state.ambulance_route
        is_ambulance_here = (st.session_state.emergency_active and is_on_route and 
                           len(st.session_state.ambulance_route) > st.session_state.ambulance_position and
                           st.session_state.ambulance_route[st.session_state.ambulance_position] == intersection)
        
        card_class = "intersection-card"
        status_class = "status-normal"
        
        if is_ambulance_here:
            card_class += " ambulance-here"
            status_class = "status-emergency"
            status_text = "🚑 AMBULANCE"
        elif is_on_route:
            card_class += " ambulance-route"
            status_class = "status-route"
            status_text = "🚨 ROUTE"
        else:
            status_text = "🔄 NORMAL"
        
        # Enhanced intersection card with animations
        st.markdown(f"""
        <div class="{card_class}">
            <div class="status-indicator {status_class}">{status_text}</div>
            <h4 style="margin: 15px 0 10px 0; color: #fff;">{intersection.split(',')[0] if ',' in intersection else intersection}</h4>
            <div class="traffic-light">{get_traffic_light_emoji(data['status'])}</div>
            <p><strong>Status:</strong> <span style="color: {'#2ed573' if data['status'] == 'green' else '#ffa502' if data['status'] == 'yellow' else '#ff4757'};">{data['status'].upper()}</span></p>
            <p><strong>Vehicles:</strong> <span class="vehicle-counter">🚗 {data['vehicles']}</span></p>
            <p><strong>Zone:</strong> {data['zone']}</p>
            <p><strong>Priority:</strong> <span style="color: {'#ff4757' if data['priority'] == 'high' else '#ffa502' if data['priority'] == 'medium' else '#2ed573'};">{data['priority'].upper()}</span></p>
            <p><strong>Congestion:</strong> {int(data['congestion_level']*100)}%</p>
        </div>
        """, unsafe_allow_html=True)

# Advanced Analytics Section
st.markdown("### 📈 Real-time Traffic Analytics & Predictions")

# Update traffic history with enhanced data
current_time = datetime.now()
st.session_state.traffic_history.append({
    'time': current_time,
    'total_vehicles': total_vehicles,
    'green_lights': green_lights,
    'avg_congestion': avg_congestion,
    'emergency_active': st.session_state.emergency_active,
    'emergency_id': st.session_state.emergency_id
})

# Keep last 50 data points
if len(st.session_state.traffic_history) > 50:
    st.session_state.traffic_history = st.session_state.traffic_history[-50:]

# Create enhanced analytics charts
if len(st.session_state.traffic_history) > 2:
    df = pd.DataFrame(st.session_state.traffic_history)
    
    # Multi-metric chart
    fig_analytics = go.Figure()
    
    # Traffic volume
    fig_analytics.add_trace(go.Scatter(
        x=df['time'], y=df['total_vehicles'],
        mode='lines+markers',
        name='Total Vehicles',
        line=dict(color='#00d4ff', width=3),
        fill='tonexty'
    ))
    
    # Green lights (scaled for visualization)
    fig_analytics.add_trace(go.Scatter(
        x=df['time'], y=df['green_lights'] * 50,  # Scale for better visualization
        mode='lines+markers',
        name='Green Signals (×50)',
        line=dict(color='#2ed573', width=2),
        yaxis='y2'
    ))
    
    # Congestion level
    fig_analytics.add_trace(go.Scatter(
        x=df['time'], y=df['avg_congestion'] * 500,  # Scale for visualization
        mode='lines+markers',
        name='Avg Congestion (×500)',
        line=dict(color='#ffa502', width=2),
        yaxis='y2'
    ))
    
    # Highlight emergency periods
    emergency_groups = df.groupby('emergency_id')
    for eid, group in emergency_groups:
        if group['emergency_active'].any():
            emergency_start = group['time'].min()
            emergency_end = group['time'].max() + timedelta(seconds=45)
            
            fig_analytics.add_vrect(
                x0=emergency_start, x1=emergency_end,
                fillcolor="rgba(255,0,110,0.2)",
                layer="below",
                line_width=0,
            )
            
            fig_analytics.add_annotation(
                x=emergency_start + (emergency_end - emergency_start) / 2,
                y=df['total_vehicles'].max(),
                text="🚑 EMERGENCY",
                showarrow=False,
                font=dict(color="white", size=12),
                bgcolor="rgba(255,0,110,0.8)",
                bordercolor="white",
                borderwidth=1
            )
    
    fig_analytics.update_layout(
        title=dict(
            text="🔍 Network Performance Analytics",
            font=dict(size=18, color='white'),
            x=0.5
        ),
        xaxis_title="Time",
        yaxis_title="Vehicles",
        yaxis2=dict(overlaying='y', side='right', title="Scaled Metrics"),
        template="plotly_dark",
        height=400,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(26,26,46,0.3)'
    )
    
    st.plotly_chart(fig_analytics, use_container_width=True)

# Emergency Response Stats
if st.session_state.emergency_active:
    st.markdown("### 🚨 Live Emergency Response Data")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, #ff006e, #ff4757);">
            <div class="metric-label">Emergency Duration</div>
            <div class="metric-value">{int(time.time() - st.session_state.emergency_start_time)}s</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        current_intersection = st.session_state.ambulance_route[st.session_state.ambulance_position] if st.session_state.ambulance_route else "N/A"
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, #ff6b35, #f7931e);">
            <div class="metric-label">Current Location</div>
            <div class="metric-value" style="font-size: 1.2rem;">{current_intersection.split()[0]}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        route_vehicles = sum(DELHI_INTERSECTIONS[intersection]["vehicles"] for intersection in st.session_state.ambulance_route)
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, #2ed573, #17a2b8);">
            <div class="metric-label">Route Vehicles</div>
            <div class="metric-value">{route_vehicles}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        cleared_signals = sum(1 for intersection in st.session_state.ambulance_route 
                            if DELHI_INTERSECTIONS[intersection]["status"] == "green")
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, #667eea, #764ba2);">
            <div class="metric-label">Cleared Signals</div>
            <div class="metric-value">{cleared_signals}/{len(st.session_state.ambulance_route)}</div>
        </div>
        """, unsafe_allow_html=True)

# System Status Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    system_status = "🟢 OPERATIONAL" if not st.session_state.emergency_active else "🚨 EMERGENCY MODE"
    st.markdown(f"**System Status:** {system_status}")

with col2:
    last_update = datetime.now().strftime("%H:%M:%S")
    st.markdown(f"**Last Update:** {last_update}")

with col3:
    total_emergencies = st.session_state.emergency_id
    st.markdown(f"**Total Emergencies:** {total_emergencies}")

# Auto-refresh with dynamic interval
refresh_interval = 1 if st.session_state.emergency_active else 2
time.sleep(refresh_interval)
st.rerun()