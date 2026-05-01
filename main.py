import sys
import streamlit as st
from controller import Controller
from streamlit_visualizer import StreamlitVisualizer
from input_handler import InputHandler

# ==========================================
# PAGE CONFIG - MUST BE FIRST STREAMLIT COMMAND
# ==========================================
st.set_page_config(
    page_title="Smart Parking System",
    page_icon="P",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# COMPLETE CSS - Copy your working CSS here
# ==========================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Black+Ops+One&family=Bungee&family=Bungee+Shade&family=Fugaz+One&family=Monoton&family=Orbitron:wght@700;800;900&family=Righteous&family=Russo+One&family=Titan+One&display=swap');
    
    /* REMOVE ALL EMPTY CONTAINERS */
    .st-emotion-cache-1jicfl2, .st-emotion-cache-16idsys, 
    .st-emotion-cache-1aehpvj, .element-container:empty,
    div[data-testid="stVerticalBlock"] > div:empty,
    div[data-testid="stHorizontalBlock"] > div:empty {
        display: none !important;
    }
    
    /* PREMIUM CAR PARKING BACKGROUND */
    .stApp {
        background: 
            linear-gradient(135deg, rgba(0, 0, 0, 0.7) 0%, rgba(0, 0, 0, 0.6) 100%),
            url('https://images.unsplash.com/photo-1506521781263-d8422e82f27a?q=80&w=2070');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    
    /* MAIN CONTENT AREA */
    .main {
        background: rgba(255, 255, 255, 0.97);
        backdrop-filter: blur(5px);
        border-radius: 50px 0 0 50px;
        padding: 2rem 2.5rem;
        margin: 1rem 0 1rem 2rem;
        box-shadow: -15px 0 40px rgba(0, 0, 0, 0.4);
        border-left: 6px solid #ef4444;
    }
    
    /* ========== HEADER ========== */
    .app-header {
        text-align: center;
        margin-bottom: 2.5rem;
        padding: 2.5rem 1rem;
        background: linear-gradient(145deg, #0a0f1a 0%, #1a1f2e 100%);
        border-radius: 50px;
        box-shadow: 0 30px 40px -10px rgba(0, 0, 0, 0.7);
        border: 2px solid rgba(255,255,255,0.1);
        position: relative;
        overflow: hidden;
    }

    .app-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: rotate 20s linear infinite;
    }

    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    .app-title {
        font-family: 'Righteous', cursive;
        font-size: 4.8rem !important;
        font-weight: 700;
        background: linear-gradient(135deg, #ef4444, #3b82f6, #10b981, #f59e0b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 3px 3px 0 #0f172a, 6px 6px 15px rgba(0, 0, 0, 0.5);
        letter-spacing: 2px;
        text-transform: uppercase;
        margin: 0;
        animation: float 4s ease-in-out infinite;
    }

    @keyframes float {
        0% { transform: translateY(0); }
        50% { transform: translateY(-8px); }
        100% { transform: translateY(0); }
    }

    .app-subtitle {
        font-family: 'Orbitron', sans-serif;
        font-size: 1.4rem;
        font-weight: 800;
        background: linear-gradient(135deg, #ffffff, #e0f2fe, #bae6fd, #7dd3fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: 1.5rem;
        letter-spacing: 5px;
        text-transform: uppercase;
        border-top: 3px solid #ef4444;
        border-bottom: 3px solid #3b82f6;
        display: inline-block;
        padding: 0.8rem 3rem;
        backdrop-filter: blur(5px);
        border-radius: 50px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.3);
    }
    
    /* ========== SIDEBAR ========== */
    section[data-testid="stSidebar"] {
        background: linear-gradient(145deg, #0a0f1a 0%, #141b2b 100%) !important;
        border-right: 4px solid #ef4444;
        padding: 2rem 1rem !important;
        box-shadow: 5px 0 20px rgba(0, 0, 0, 0.5);
    }
    
    /* ========== INPUT SECTIONS ========== */
    .input-section-1, .input-section-2, .input-section-3, .input-section-4 {
        margin-bottom: 2rem;
        padding: 1rem 0.5rem;
        border-bottom: 2px solid rgba(255,255,255,0.1);
    }
    
    .section-header-1 {
        font-family: 'Bungee', cursive;
        font-size: 1.5rem;
        background: linear-gradient(135deg, #ef4444, #f87171);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-transform: uppercase;
        border-left: 6px solid #ef4444;
        padding-left: 1rem;
        margin-bottom: 1rem;
    }
    
    .section-header-2 {
        font-family: 'Bungee', cursive;
        font-size: 1.5rem;
        background: linear-gradient(135deg, #3b82f6, #60a5fa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-transform: uppercase;
        border-left: 6px solid #3b82f6;
        padding-left: 1rem;
        margin-bottom: 1rem;
    }
    
    .section-header-3 {
        font-family: 'Bungee', cursive;
        font-size: 1.5rem;
        background: linear-gradient(135deg, #10b981, #34d399);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-transform: uppercase;
        border-left: 6px solid #10b981;
        padding-left: 1rem;
        margin-bottom: 1rem;
    }
    
    .section-header-4 {
        font-family: 'Bungee', cursive;
        font-size: 1.5rem;
        background: linear-gradient(135deg, #f59e0b, #fbbf24);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-transform: uppercase;
        border-left: 6px solid #f59e0b;
        padding-left: 1rem;
        margin-bottom: 1rem;
    }
    
    /* NUMBER INPUT */
    .stNumberInput input {
        background: #1e293b !important;
        border: 2px solid #334155 !important;
        border-radius: 12px !important;
        color: white !important;
        font-family: 'Righteous', cursive !important;
        font-size: 1.3rem !important;
        text-align: center !important;
    }
    
    .stNumberInput button {
        background: #2d3b4f !important;
        border: 2px solid #3b82f6 !important;
        color: white !important;
        font-size: 1.2rem !important;
        border-radius: 10px !important;
        width: 36px !important;
        height: 36px !important;
        transition: all 0.2s ease !important;
    }
    
    .stNumberInput button:hover {
        background: #3b82f6 !important;
        transform: scale(1.1) !important;
    }
    
    /* SLIDER */
    div[data-baseweb="slider"] {
        height: 8px !important;
        background: linear-gradient(90deg, #ef4444, #f59e0b, #3b82f6, #10b981) !important;
        border-radius: 20px !important;
    }
    
    div[role="slider"] {
        width: 24px !important;
        height: 24px !important;
        background: white !important;
        border: 4px solid #ef4444 !important;
        border-radius: 50% !important;
        box-shadow: 0 0 15px #ef4444 !important;
    }
    
    /* BUTTON */
    .stButton > button {
        background: linear-gradient(135deg, #ef4444, #dc2626);
        color: white;
        font-family: 'Black Ops One', cursive;
        font-size: 1.4rem;
        letter-spacing: 3px;
        padding: 1.2rem;
        border-radius: 60px;
        border: 3px solid rgba(255,255,255,0.3);
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 15px 25px rgba(239, 68, 68, 0.5);
    }
    
    .stButton > button:hover {
        transform: translateY(-5px);
        box-shadow: 0 25px 35px rgba(239, 68, 68, 0.7);
    }
    
    
    
    .results-title {
        font-family: 'Fugaz One', cursive;
        font-size: 2rem;
        background: linear-gradient(135deg, #ef4444, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1.5rem;
        border-bottom: 4px solid #ef4444;
    }
    
    /* STATS BLOCKS */
    .stat-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
        margin-bottom: 1rem;
    }
    
    .stat-block-1 { background: linear-gradient(145deg, #ef4444, #dc2626); border-radius: 25px; padding: 1rem; text-align: center; border: 2px solid rgba(255,255,255,0.2); }
    .stat-block-2 { background: linear-gradient(145deg, #3b82f6, #2563eb); border-radius: 25px; padding: 1rem; text-align: center; border: 2px solid rgba(255,255,255,0.2); }
    .stat-block-3 { background: linear-gradient(145deg, #10b981, #059669); border-radius: 25px; padding: 1rem; text-align: center; border: 2px solid rgba(255,255,255,0.2); }
    .stat-block-4 { background: linear-gradient(145deg, #f59e0b, #d97706); border-radius: 25px; padding: 1rem; text-align: center; border: 2px solid rgba(255,255,255,0.2); }
    
    .stat-number {
        font-family: 'Titan One', cursive;
        font-size: 2.5rem;
        color: white;
    }
    
    .stat-label {
        font-family: 'Russo One', sans-serif;
        font-size: 0.8rem;
        color: rgba(255,255,255,0.9);
        text-transform: uppercase;
    }
    
    /* LEGEND */
    .legend-title {
        font-family: 'Fugaz One', cursive;
        font-size: 1.5rem;
        background: linear-gradient(135deg, #f59e0b, #ef4444);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 1rem 0;
    }
    
    .legend-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 0.5rem;
    }
    
    .legend-item {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        background: rgba(30, 41, 59, 0.8);
        padding: 0.5rem;
        border-radius: 10px;
    }
    
    .color-dot {
        width: 20px;
        height: 20px;
        border-radius: 6px;
    }
    
    .legend-text {
        font-family: 'Righteous', cursive;
        font-size: 0.8rem;
        color: white;
    }
    
    .gate-error {
        font-family: 'Orbitron', sans-serif;
        color: #ef4444;
        font-weight: 700;
        margin-top: 0.8rem;
        text-align: center;
        background: rgba(239, 68, 68, 0.15);
        padding: 0.6rem;
        border-radius: 10px;
        border: 2px solid #ef4444;
    }
    
    hr { display: none !important; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# HEADER
# ==========================================
st.markdown("""
<div class="app-header">
    <h1 class="app-title">SMART PARKING</h1>
    <div class="app-subtitle">A* SEARCH · MANHATTAN HEURISTIC · MULTI-CAR</div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# SIDEBAR INPUTS
# ==========================================
with st.sidebar:
    st.markdown('<div class="input-section-1">', unsafe_allow_html=True)
    st.markdown('<div class="section-header-1">GRID</div>', unsafe_allow_html=True)
    rows = st.number_input("ROWS", min_value=3, max_value=15, value=7, key="rows")
    cols = st.number_input("COLUMNS", min_value=3, max_value=15, value=6, key="cols")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="input-section-2">', unsafe_allow_html=True)
    st.markdown('<div class="section-header-2">GATE</div>', unsafe_allow_html=True)
    gate_row = st.number_input("ROW", min_value=0, max_value=rows-1, value=1, key="gate_row")
    gate_col = st.number_input("COLUMN", min_value=0, max_value=cols-1, value=0, key="gate_col")
    gate_valid = (gate_row == 0 or gate_row == rows-1 or gate_col == 0 or gate_col == cols-1)
    if not gate_valid:
        st.markdown('<div class="gate-error">MUST BE ON BORDER</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="input-section-3">', unsafe_allow_html=True)
    st.markdown('<div class="section-header-3">OCCUPANCY</div>', unsafe_allow_html=True)
    occupancy = st.slider("PERCENTAGE", min_value=0, max_value=80, value=40, key="occ")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="input-section-4">', unsafe_allow_html=True)
    st.markdown('<div class="section-header-4">VEHICLES</div>', unsafe_allow_html=True)
    num_cars = st.number_input("NUMBER OF CARS", min_value=1, max_value=10, value=3, key="cars")
    st.markdown('</div>', unsafe_allow_html=True)

    run_button = st.button("FIND PARKING SPOTS", use_container_width=True, disabled=not gate_valid)

# ==========================================
# MAIN CONTENT
# ==========================================
params = {
    'rows': rows,
    'cols': cols,
    'gate': (gate_row, gate_col),
    'occupancy': occupancy
}

ctrl = Controller.get_instance()

if run_button and gate_valid:
    ctrl.run(params, mode='gui', num_cars=num_cars)

    left_col, right_col = st.columns([2, 1])

    with left_col:
        fig = ctrl.visualizer.render()
        st.pyplot(fig)

    with right_col:
        st.markdown('<div class="results-card">', unsafe_allow_html=True)
        st.markdown('<div class="results-title">RESULTS</div>', unsafe_allow_html=True)

        stats = ctrl.collect_metrics()
        st.markdown('<div class="stat-grid">', unsafe_allow_html=True)
        st.markdown(f'<div class="stat-block-1"><div class="stat-number">{stats["parked"]}</div><div class="stat-label">PARKED</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="stat-block-2"><div class="stat-number">{stats["avg_nodes"]}</div><div class="stat-label">NODES</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="stat-block-3"><div class="stat-number">{stats["total_steps"]}</div><div class="stat-label">STEPS</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="stat-block-4"><div class="stat-number">{stats["free_left"]}</div><div class="stat-label">FREE</div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # K-Means status
        clustering_status = stats.get('clustering', 'Disabled')
        if "Enabled" in str(clustering_status):
            status_color = "#10b981"
            status_icon = "ACTIVE"
        else:
            status_color = "#f59e0b"
            status_icon = "INACTIVE"

        st.markdown(f"""
        <div style="background: linear-gradient(145deg, #1e293b, #0f172a); border-radius: 15px; padding: 0.8rem; margin: 1rem 0; border-left: 6px solid {status_color};">
            <div style="display: flex; justify-content: space-between;">
                <span style="font-family: 'Orbitron'; font-size: 0.8rem; color: #94a3b8;">K-MEANS CLUSTERING</span>
                <span style="background: {status_color}; padding: 0.2rem 0.6rem; border-radius: 20px; font-size: 0.7rem; color: white;">{status_icon}</span>
            </div>
            <div style="font-family: 'Righteous'; font-size: 0.9rem; color: white; margin-top: 0.3rem;">{clustering_status}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### Allocated Spots")
        for spot, label in ctrl.allocated_spots.items():
            st.write(f"{label}: ({spot[0]}, {spot[1]})")

        st.markdown('<div class="legend-title">LEGEND</div>', unsafe_allow_html=True)
        st.markdown('<div class="legend-grid">', unsafe_allow_html=True)
        legend = [('#86efac', 'FREE'), ('#f87171', 'OCCUPIED'), ('#94a3b8', 'ROAD'),
                  ('#fbbf24', 'PATH'), ('#60a5fa', 'GATE'), ('#c084fc', 'CAR')]
        for color, label in legend:
            st.markdown(f'<div class="legend-item"><div class="color-dot" style="background:{color};"></div><span class="legend-text">{label}</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

else:
    ctrl.run(params, mode='gui', num_cars=0)
    left_col, right_col = st.columns([2, 1])
    with left_col:
        fig = ctrl.visualizer.render()
        if fig:
            st.pyplot(fig)
    with right_col:
        st.markdown('<div class="results-card">', unsafe_allow_html=True)
        st.markdown('<div class="results-title">READY</div>', unsafe_allow_html=True)
        st.markdown("""
        <div style="text-align: center; padding: 2rem;">
            <span style="font-family: 'Russo One'; font-size: 1.2rem;">CONFIGURE PARAMETERS</span><br>
            <span style="font-family: 'Black Ops One'; font-size: 1.6rem;">↓ CLICK FIND SPOTS ↓</span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)