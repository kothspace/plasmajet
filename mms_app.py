import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os
from PIL import Image

# ── Color palette ────────────────────────────────────────────────────────────
C = {
    "bg":         "#fafaf9",
    "navy":       "#162e4b",
    "navy2":      "#365579",
    "navy3":      "#6088b6",
    "cream":      "#faf7f2",
    "blush":      "#f5dde4",
    "pale_blue":  "#e8f3ff",
    "white":      "#ffffff",
    "text_light": "#a8bcd4",
    "border":     "#c8d8ea",
    "grid":       "#dde6f0",
    "accent":     "#365579",
    "hover_pink": "#fff1f9",
    "elec_b":     "#097bff",
    "dot":        "#ff6573",
    "traj":       "#3163d4",
}

st.set_page_config(
    page_title="String-of-Pearls Measurements of Supersonic Plasma Jets",
    layout="wide",
    page_icon="🛰"
)

st.markdown(f"""
<style>
    .main, .stApp, [data-testid="stAppViewContainer"] {{
        background-color: {C["bg"]} !important;
    }}
    .block-container {{ padding-top: 1rem; }}

    .header-box {{
        background-color: {C["pale_blue"]};
        color: {C["navy"]};
        padding: 16px 24px;
        border-radius: 8px;
        text-align: center;
        margin-bottom: 16px;
    }}
    .header-box h1 {{ font-size: 26px; font-weight: bold; margin: 0; color: {C["navy"]}; }}
    .header-box p  {{ font-size: 16px; color: {C["navy2"]}; margin: 4px 0 0 0; font-family: 'Times New Roman', monospace; }}

    .summary-box {{
        background-color: {C["pale_blue"]};
        border: 1.5px solid {C["navy"]};
        border-radius: 8px;
        padding: 14px;
        font-family: 'Times New Roman', monospace;
        font-size: 13px;
        color: {C["navy"]};
        line-height: 1.9;
    }}
    .section-header {{
        background-color: {C["navy"]};
        color: {C["white"]};
        padding: 7px 14px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: bold;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        margin-bottom: 8px;
    }}
    .event-box {{
        background-color: {C["pale_blue"]};
        border: 1.5px solid {C["border"]};
        border-radius: 8px;
        padding: 14px;
        font-family: 'Times New Roman', monospace;
        font-size: 13px;
        line-height: 2.0;
    }}
    .footer-bar {{
        background-color: {C["navy"]};
        color: {C["navy3"]};
        padding: 8px 16px;
        border-radius: 6px;
        font-size: 11px;
        margin-top: 16px;
    }}
    div.stButton > button {{
        background-color: {C["navy"]};
        color: {C["hover_pink"]};
        font-weight: bold;
        font-size: 15px;
        font-family: 'Times New Roman', monospace;
        width: 100%;
        border: none;
        padding: 10px;
        border-radius: 6px;
    }}
    div.stButton > button:hover {{
        background-color: {C["pale_blue"]};
        color: {C["navy"]};
    }}

    div.stDownloadButton > button {{
        background-color: {C["navy"]};
        color: {C["hover_pink"]};
        font-weight: bold;
        font-size: 15px;
        font-family: 'Times New Roman', monospace;
        width: 100%;
        border: none;
        padding: 10px;
        border-radius: 6px;
    }}
    div.stDownloadButton > button:hover {{
        background-color: {C["pale_blue"]};
        color: {C["navy"]};
    }}


</style>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="header-box">
    <h1>String-of-Pearls Measurements of Supersonic Plasma Jets Using Magnetospheric MultiScale Satellites</h1>
    <p>Laboratory for Solar-Magnetosphere-Ionosphere Research · Embry-Riddle Aeronautical University</p>
</div>
""", unsafe_allow_html=True)

# ── Attribution banner ───────────────────────────────────────────────────────
st.markdown(f"""
<div style="
    background-color: {C["hover_pink"]};
    color: {C["navy"]};
    padding: 8px 20px;
    border-radius: 6px;
    text-align: center;
    font-family: 'Times New Roman', serif;
    font-size: 13px;
    margin-bottom: 10px;
    letter-spacing: 0.3px;
">
    By <strong>Amelia Köth</strong> &nbsp;·&nbsp;
    <a href="https://ameliakoth.com" target="_blank" style="
        color: {C["navy"]};
        font-weight: bold;
        text-decoration: underline;
        text-underline-offset: 3px;
    ">Learn more about her here →</a>
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
    st.markdown(f"""
    <div class="event-box">
        <b style="color:{C["accent"]};">Date:</b> 2025-02-27<br>
        <b style="color:{C["accent"]};">Pass:</b> 05:19:50 – 05:21:49 UT<br>
        <b style="color:{C["accent"]};">Region:</b> Magnetosheath<br>
        <b style="color:{C["accent"]};">Method:</b> Min. Variance Analysis
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
        line=dict(color=C["traj"], width=4),
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
            line=dict(color=C["navy"], width=1.5),
            name='Magnetic Field',
            showlegend=(i == 0),
            hoverinfo='skip'
        ))

    # jet core arrow
    nj = normals[jet_idx]
    sc = arrow_scale[jet_idx]
    fig.add_trace(go.Scatter3d(
        x=[xj, xj + nj[0]*sc],
        y=[yj, yj + nj[1]*sc],
        z=[zj, zj + nj[2]*sc],
        mode='lines',
        line=dict(color=C["dot"], width=3),
        name='Jet Core',
        hoverinfo='skip'
    ))

    # jet core dot
    fig.add_trace(go.Scatter3d(
        x=[xj], y=[yj], z=[zj],
        mode='markers',
        marker=dict(size=4, color=C["dot"]),
        name='Jet Core Position',
        hovertemplate=f'Jet Core<br>X:{xj:.4f} Y:{yj:.4f} Z:{zj:.4f}<extra></extra>'
    ))

    # 7. STYLE
    fig.update_layout(
        height=600,
        paper_bgcolor=C["cream"],
        plot_bgcolor=C["cream"],
        showlegend=True,
        legend=dict(
            x=0.01, y=0.99,
            bgcolor=C["cream"],
            bordercolor=C["navy2"],
            borderwidth=1,
            font=dict(size=11, color=C["navy"])
        ),
        margin=dict(l=0, r=0, t=10, b=0),
        scene=dict(
            bgcolor=C["cream"],
            xaxis=dict(
                title=dict(text='X [RE]'),
                backgroundcolor=C["white"],
                gridcolor=C["grid"],
                showbackground=True,
                tickfont=dict(size=10, color=C["navy"]),
                range=[10.455, 10.515]
            ),
            yaxis=dict(
                title=dict(text='Y [RE]'),
                backgroundcolor=C["white"],
                gridcolor=C["grid"],
                showbackground=True,
                tickfont=dict(size=10, color=C["navy"]),
                range=[0.7595, 0.7690]
            ),
            zaxis=dict(
                title=dict(text='Z [RE]'),
                backgroundcolor=C["white"],
                gridcolor=C["grid"],
                showbackground=True,
                tickfont=dict(size=10, color=C["navy"]),
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
    <b style="color:{C["accent"]};">Time:</b> {timestamps[jet_idx]}<br>
    <hr style="border:1px dashed {C["navy3"]}; margin:6px 0;">
    <b style="color:{C["accent"]};">X:</b> {xj:.4f} RE<br>
    <b style="color:{C["accent"]};">Y:</b> {yj:.4f} RE<br>
    <b style="color:{C["accent"]};">Z:</b> {zj:.4f} RE<br>
    <hr style="border:1px dashed {C["navy3"]}; margin:6px 0;">
    <b style="color:{C["accent"]};">|B|:</b> {B_mag_jet:.4f} nT<br>
    <b style="color:{C["accent"]};">Nx:</b> {normals[jet_idx,0]:.4f}<br>
    <b style="color:{C["accent"]};">Ny:</b> {normals[jet_idx,1]:.4f}<br>
    <b style="color:{C["accent"]};">Nz:</b> {normals[jet_idx,2]:.4f}<br>
    <hr style="border:1px dashed {C["navy3"]}; margin:6px 0;">
    <b style="color:{C["accent"]};">Index:</b> {jet_idx}
</div>
"""
    summary_placeholder.markdown(summary_html, unsafe_allow_html=True)

# POSTER SECTION
st.markdown("---")
st.markdown('<div class="section-header">Research Poster</div>', unsafe_allow_html=True)
st.markdown(f"""
<div style="
    background-color: {C["cream"]};
    border: 1.5px solid {C["border"]};
    border-radius: 8px;
    padding: 16px;
    text-align: center;
">
    <p style="
        font-size: 26px;
        color: {C["navy"]};
        font-weight: bold;
        margin-bottom: 10px;
        font-family: 'Times New Roman';
    ">
        String-of-Pearls Measurements of Supersonic Plasma Jets Using Magnetospheric MultiScale Satellites<br>
        <span style="font-weight:normal; color:{C["navy2"]};">Amelia Köth, Dr. Yu-Lun Liou, and Dr. Katariina Nykyri</span><br>
        <span style="font-weight:normal; color:{C["navy3"]};">Laboratory for Solar-Magnetosphere-Ionosphere Research · ERAU</span>
    </p>
</div>
""", unsafe_allow_html=True)

POSTER_PATH = os.path.join(MATLAB_DIR, "poster.png")
# Download button for poster
if os.path.exists(POSTER_PATH):
    poster_img = Image.open(POSTER_PATH)
    st.image(poster_img, use_container_width=True)
    with open(POSTER_PATH, "rb") as f:
        poster_bytes = f.read()
    st.download_button(
        label="⬇  Download Poster",
        data=poster_bytes,
        file_name="MMS_Plasma_Jet_Poster.png",
        mime="image/png"
        )
else:
    st.warning("poster.png not found — upload it to your GitHub repository")

st.markdown(f"""
<div class="footer-bar">
    MMS · Northward IMF Event · Feb 27 2025 &nbsp;&nbsp;|&nbsp;&nbsp; Amelia Köth · ERAU LASMIR
</div>
""", unsafe_allow_html=True)
