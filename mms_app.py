import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os
from PIL import Image

st.set_page_config(
    page_title="MMS Plasma Jet Trajectory Viewer",
    layout="wide",
    page_icon="🛰"
)

st.markdown("""
<style>
    .main { background-color: #f4f6fa; }
    .block-container { padding-top: 1rem; }
    .header-box {
        background-color: #0a1a3a;
        color: white;
        padding: 16px 24px;
        border-radius: 8px;
        text-align: center;
        margin-bottom: 16px;
    }
    .header-box h1 { font-size: 26px; font-weight: bold; margin: 0; color: white; }
    .header-box p  { font-size: 12px; color: #a8bcd4; margin: 4px 0 0 0; font-family: 'Times New Roman', monospace; }
    .summary-box {
        background-color: #eaf2fb;
        border: 1.5px solid #b0cce8;
        border-radius: 8px;
        padding: 14px;
        font-family: 'Times New Roman', monospace;
        font-size: 13px;
        color: #0a1a3a;
        line-height: 1.9;
    }
    .section-header {
        background-color: #0a1a3a;
        color: white;
        padding: 7px 14px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: bold;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        margin-bottom: 8px;
    }
    .event-box {
        background-color: white;
        border: 1.5px solid #c8d8ea;
        border-radius: 8px;
        padding: 14px;
        font-family: 'Times New Roman', monospace;
        font-size: 13px;
        line-height: 2.0;
    }
    .footer-bar {
        background-color: #0a1a3a;
        color: #7ab3e0;
        padding: 8px 16px;
        border-radius: 6px;
        font-size: 11px;
        margin-top: 16px;
    }
    div.stButton > button {
        background-color: #0a1a3a;
        color: #fcd4eb;
        font-weight: bold;
        font-size: 15px;
        font-family: 'Times New Roman', monospace;
        width: 100%;
        border: none;
        padding: 10px;
        border-radius: 6px;
    }
    div.stButton > button:hover {
        background-color: #fcd4eb;
        color: #0a1a3a;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header-box">
    <h1>🛰🛰🛰🛰 MMS Plasma Jet Trajectory Viewer</h1>
    <p>Laboratory for Solar-Magnetosphere-Ionosphere Research · Embry-Riddle Aeronautical University</p>
</div>
""", unsafe_allow_html=True)

MATLAB_DIR = os.path.dirname(os.path.abspath(__file__))

left_col, right_col = st.columns([3, 1.2])

with right_col:
    st.markdown('<div class="section-header">Mission Data</div>', unsafe_allow_html=True)

    csv_files     = sorted([f for f in os.listdir(MATLAB_DIR) if f.endswith('.csv')])
    selected_file = st.selectbox("Select CSV File", csv_files)
    CSV_PATH      = os.path.join(MATLAB_DIR, selected_file)

    run = st.button("▶  Run Plot")

    st.markdown("---")
    st.markdown('<div class="section-header">Jet Core Summary</div>', unsafe_allow_html=True)
    summary_placeholder = st.empty()
    summary_placeholder.markdown(
        '<div class="summary-box">Press Run to load data...</div>',
        unsafe_allow_html=True
    )

    st.markdown("---")
    st.markdown('<div class="section-header">Event Info</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="event-box">
        <b style="color:#c0392b;">Date:</b> 2025-02-27<br>
        <b style="color:#c0392b;">Pass:</b> 05:19:50 – 05:21:49 UT<br>
        <b style="color:#c0392b;">Region:</b> Magnetosheath<br>
        <b style="color:#c0392b;">Method:</b> Min. Variance Analysis
    </div>
    """, unsafe_allow_html=True)

with left_col:
    st.markdown('<div class="section-header">3D GSE Trajectory — Normal-to-B Vectors</div>',
                unsafe_allow_html=True)
    plot_placeholder = st.empty()
    plot_placeholder.info("Select a CSV file and press Run Plot")

if run:

    # 1. LOAD DATA
    df         = pd.read_csv(CSV_PATH, header=None, names=['time','Bx','By','Bz'])
    timestamps = df['time'].values
    Bx         = df['Bx'].values
    By         = df['By'].values
    Bz         = df['Bz'].values
    N          = len(Bx)

    # 2. UNIT NORMALS
    B_mag   = np.sqrt(Bx**2 + By**2 + Bz**2)
    normals = np.column_stack([Bx, By, Bz]) / B_mag[:, None]

    # 3. TRAJECTORY
    t_norm = np.linspace(0, 1, N)
    X = 10.460 + t_norm * (10.510 - 10.460)
    Y =  0.768 + t_norm * ( 0.760 -  0.768)
    Z =  2.330 + t_norm * ( 2.318 -  2.330)

    # 4. JET CORE
    jet_idx = 28 if 'test' in selected_file else 55
    xj, yj, zj = X[jet_idx], Y[jet_idx], Z[jet_idx]
    Bmin = B_mag.min()
    Bmax = B_mag.max()
    B_mag_jet = np.sqrt(Bx[jet_idx]**2 + By[jet_idx]**2 + Bz[jet_idx]**2)

    # 5. ARROW SCALE
    ARROW_MIN   = 0.0008
    ARROW_MAX   = 0.0030
    arrow_scale = ARROW_MIN + (ARROW_MAX - ARROW_MIN) * (B_mag - Bmin) / (Bmax - Bmin)

    # 6. BUILD FIGURE
    fig = go.Figure()

    # trajectory line
    fig.add_trace(go.Scatter3d(
        x=X, y=Y, z=Z,
        mode='lines',
        line=dict(color='blue', width=4),
        name='Trajectory',
        hovertemplate='X: %{x:.4f} RE<br>Y: %{y:.4f} RE<br>Z: %{z:.4f} RE<extra></extra>'
    ))

    # normal arrows
    for i in range(N):
        if i == jet_idx:
            continue
        scale = arrow_scale[i]
        fig.add_trace(go.Scatter3d(
            x=[X[i], X[i] + normals[i,0]*scale],
            y=[Y[i], Y[i] + normals[i,1]*scale],
            z=[Z[i], Z[i] + normals[i,2]*scale],
            mode='lines',
            line=dict(color='black', width=1.5),
            name='Magnetic Field',
            showlegend=(i == 0),
            hoverinfo='skip'
        ))

    # red jet core arrow
    nj = normals[jet_idx]
    sc = arrow_scale[jet_idx]
    fig.add_trace(go.Scatter3d(
        x=[xj, xj + nj[0]*sc],
        y=[yj, yj + nj[1]*sc],
        z=[zj, zj + nj[2]*sc],
        mode='lines',
        line=dict(color='red', width=3),
        name='Jet Core',
        hoverinfo='skip'
    ))

    # red jet core dot
    fig.add_trace(go.Scatter3d(
        x=[xj], y=[yj], z=[zj],
        mode='markers',
        marker=dict(size=4, color='red'),
        name='Jet Core Position',
        hovertemplate=f'Jet Core<br>X:{xj:.4f} Y:{yj:.4f} Z:{zj:.4f}<extra></extra>'
    ))

    # 7. STYLE
    fig.update_layout(
        height=600,
        paper_bgcolor='white',
        plot_bgcolor='white',
        showlegend=True,
        legend=dict(
            x=0.01, y=0.99,
            bgcolor='rgba(255,255,255,0.9)',
            bordercolor='#cccccc',
            borderwidth=1,
            font=dict(size=11)
        ),
        margin=dict(l=0, r=0, t=10, b=0),
        scene=dict(
            bgcolor='white',
            xaxis=dict(
                title=dict(text='X [RE]'),
                backgroundcolor='white',
                gridcolor='#dddddd',
                showbackground=True,
                tickfont=dict(size=10, color='gray'),
                range=[10.455, 10.515]
            ),
            yaxis=dict(
                title=dict(text='Y [RE]'),
                backgroundcolor='white',
                gridcolor='#dddddd',
                showbackground=True,
                tickfont=dict(size=10, color='gray'),
                range=[0.7595, 0.7690]
            ),
            zaxis=dict(
                title=dict(text='Z [RE]'),
                backgroundcolor='white',
                gridcolor='#dddddd',
                showbackground=True,
                tickfont=dict(size=10, color='gray'),
                range=[2.3170, 2.3310]
            ),
            camera=dict(eye=dict(x=1.8, y=1.2, z=0.8))
        )
    )

    with left_col:
        plot_placeholder.plotly_chart(fig, use_container_width=True)

    # 8. SUMMARY
    summary_html = f"""
<div class="summary-box">
    <b style="color:#c0392b;">Time:</b> {timestamps[jet_idx]}<br>
    <hr style="border:1px dashed #b0cce8; margin:6px 0;">
    <b style="color:#c0392b;">X:</b> {xj:.4f} RE<br>
    <b style="color:#c0392b;">Y:</b> {yj:.4f} RE<br>
    <b style="color:#c0392b;">Z:</b> {zj:.4f} RE<br>
    <hr style="border:1px dashed #b0cce8; margin:6px 0;">
    <b style="color:#c0392b;">|B|:</b> {B_mag_jet:.4f} nT<br>
    <b style="color:#c0392b;">Nx:</b> {normals[jet_idx,0]:.4f}<br>
    <b style="color:#c0392b;">Ny:</b> {normals[jet_idx,1]:.4f}<br>
    <b style="color:#c0392b;">Nz:</b> {normals[jet_idx,2]:.4f}<br>
    <hr style="border:1px dashed #b0cce8; margin:6px 0;">
    <b style="color:#c0392b;">Index:</b> {jet_idx}
</div>
"""
    summary_placeholder.markdown(summary_html, unsafe_allow_html=True)

# POSTER SECTION
st.markdown("---")
st.markdown('<div class="section-header">Research Poster</div>', unsafe_allow_html=True)
st.markdown("""
<div style="
    background-color: white;
    border: 1.5px solid #c8d8ea;
    border-radius: 8px;
    padding: 16px;
    text-align: center;
">
    <p style="
        font-size: 13px;
        color: #0a1a3a;
        font-weight: bold;
        margin-bottom: 10px;
        font-family: 'Times New Roman';
    ">
        String-of-Pearls Measurements of Supersonic Plasma Jets Using Magnetospheric MultiScale Satellites<br>
        <span style="font-weight:normal; color:#555;">Amelia Köth, Dr. Yu-Lun Liou, and Dr. Katariina Nykyri</span><br>
        <span style="font-weight:normal; color:#555;">Laboratory for Solar-Magnetosphere-Ionosphere Research · ERAU</span>
    </p>
</div>
""", unsafe_allow_html=True)

POSTER_PATH = os.path.join(MATLAB_DIR, "poster.png")
if os.path.exists(POSTER_PATH):
    poster_img = Image.open(POSTER_PATH)
    st.image(poster_img, use_container_width=True)
else:
    st.warning("poster.png not found — upload it to your GitHub repository")

st.markdown("""
<div class="footer-bar">
    MMS · Northward IMF Event · Feb 27 2025 &nbsp;&nbsp;|&nbsp;&nbsp; Amelia Köth · ERAU LASMIR
</div>
""", unsafe_allow_html=True)
