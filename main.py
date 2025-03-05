import streamlit as st
from streamlit.script_run_context import get_script_run_ctx as get_run_context
import plotly.graph_objects as go
import numpy as np
from solar_calculations import calculate_analemma, get_current_position
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Explorateur d'Analemme Solaire",
    page_icon="☀️",
    layout="wide"
)

# Title and introduction
st.title("☀️ Explorateur d'Analemme Solaire - Cadran Solaire de Nice")
st.markdown("""
L'analemme solaire est la figure en forme de 8 tracée par la position du Soleil 
lorsqu'elle est observée à la même heure chaque jour tout au long d'une année. 
Ce motif est projeté sur un cadran solaire vertical avec orientation ajustable à Nice.
""")

# Sidebar controls
st.sidebar.header("Paramètres")
selected_hour = st.sidebar.slider(
    "Sélectionnez l'heure d'observation (format 24h)",
    0, 23, 12,
    help="Choisissez l'heure du jour pour le calcul de l'analemme"
)

orientation_angle = st.sidebar.slider(
    "Orientation du mur (degrés par rapport au sud)",
    -90, 90, 0,
    help="0° = plein sud, -90° = est, +90° = ouest"
)

# Calculate analemma for selected hour and orientation
x_positions, y_positions = calculate_analemma(selected_hour, orientation_angle)

# Create main visualization
fig = go.Figure()

# Add grid lines for hours
hour_lines_x = np.linspace(-2, 2, 9)  # 9 vertical lines
hour_lines_y = np.linspace(-2, 2, 9)  # 9 horizontal lines

for x in hour_lines_x:
    fig.add_shape(
        type="line",
        x0=x, x1=x, y0=-2, y1=2,
        line=dict(color="rgba(255, 255, 255, 0.1)", width=1)
    )

for y in hour_lines_y:
    fig.add_shape(
        type="line",
        x0=-2, x1=2, y0=y, y1=y,
        line=dict(color="rgba(255, 255, 255, 0.1)", width=1)
    )

# Add analemma trace
fig.add_trace(go.Scatter(
    x=x_positions,
    y=y_positions,
    mode='lines+markers',
    name=f'Analemme à {selected_hour:02d}:00',
    line=dict(color='#1E88E5', width=2),
    marker=dict(size=4, color='#1E88E5'),
))

# Add current sun position
current_x, current_y = get_current_position(orientation_angle)
if current_x is not None and current_y is not None:
    fig.add_trace(go.Scatter(
        x=[current_x],
        y=[current_y],
        mode='markers',
        name='Position actuelle du Soleil',
        marker=dict(size=12, color='yellow', symbol='star'),
    ))

# Configure layout
orientation_text = {
    0: "sud",
    90: "ouest",
    -90: "est"
}.get(orientation_angle, f"{orientation_angle}° du sud")

fig.update_layout(
    template="plotly_dark",
    title=f"Analemme Solaire à {selected_hour:02d}:00 sur un Cadran Solaire orienté vers le {orientation_text}",
    xaxis_title="Position Horizontale (Gauche ← 0 → Droite)",
    yaxis_title="Position Verticale",
    showlegend=True,
    hovermode='closest',
    plot_bgcolor='rgba(14, 17, 23, 0.8)',
    paper_bgcolor='rgba(14, 17, 23, 0.8)',
    xaxis=dict(range=[-2, 2], zeroline=True, zerolinecolor='white'),
    yaxis=dict(range=[-2, 2], zeroline=True, zerolinecolor='white'),
)

# Display the plot
st.plotly_chart(fig, use_container_width=True)

# Explanation section
st.header("Comprendre le Cadran Solaire")
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown(f"""
    ### Composants Clés:
    1. **Forme**: Le motif en 8 est causé par:
        - L'inclinaison de l'axe terrestre (23.5°)
        - L'orbite elliptique de la Terre
    2. **Temps**: Le motif montre la position du soleil à {selected_hour:02d}:00 chaque jour
    3. **Orientation**: Mur orienté à {orientation_angle}° du sud
    4. **Localisation**: Nice, France (43.7102°N, 7.2620°E)
    """)

with col2:
    st.markdown("""
    ### Lecture du Cadran:
    - **Axe Horizontal**: Position gauche-droite sur le mur
    - **Axe Vertical**: Hauteur du Soleil
    - **Boucle Supérieure**: Mois d'hiver
    - **Boucle Inférieure**: Mois d'été
    """)

# Current data display
st.sidebar.markdown("### Position Solaire Actuelle")
current_time = datetime.now().strftime("%H:%M:%S")
if current_x is not None and current_y is not None:
    st.sidebar.markdown(f"""
    - Heure: {current_time}
    - Position X: {current_x:.2f}
    - Position Y: {current_y:.2f}
    """)
else:
    st.sidebar.markdown("""
    Le soleil est actuellement derrière le mur 
    (pas visible sur le cadran solaire)
    """)

def main():
    ctx = get_run_context()
    if ctx is None:
        st.error("No script run context found")
    
if __name__ == "__main__":
    main()