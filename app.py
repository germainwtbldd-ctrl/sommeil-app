import streamlit as st
import time
from datetime import datetime, timedelta

st.set_page_config(page_title="Suivi de sommeil", page_icon="😴", layout="centered")

# ---------- Thème sombre ----------
st.markdown("""
<style>
.stApp { background-color: #0e1117; color: #e6e6e6; }
h1, h2, h3 { color: #cfd8ff; }
.bigphase {
    font-size: 42px; font-weight: bold; text-align: center;
    padding: 25px; border-radius: 15px; margin: 15px 0;
    background: linear-gradient(135deg, #1e2a55, #3a2f6b);
    color: #ffffff;
}
</style>
""", unsafe_allow_html=True)

st.title("😴 Suivi de sommeil")

# ---------- État ----------
if "running" not in st.session_state:
    st.session_state.running = False
if "start_time" not in st.session_state:
    st.session_state.start_time = None

# ---------- Boutons ----------
col1, col2 = st.columns(2)
with col1:
    if st.button("▶️ Start", use_container_width=True):
        st.session_state.running = True
        st.session_state.start_time = datetime.now()
        st.rerun()
with col2:
    if st.button("⏹️ Stop", use_container_width=True):
        st.session_state.running = False
        st.rerun()

# ---------- Cycles de sommeil (durées en secondes, accéléré) ----------
# Un cycle réel ≈ 90 min. Ici on accélère pour la démo.
cycles = [
    ("🟢 Éveil / Endormissement", 8,  "#2e7d32"),
    ("🔵 Sommeil lent léger",     12, "#1565c0"),
    ("🟣 Sommeil lent profond",   15, "#6a1b9a"),
    ("🟠 Sommeil paradoxal (REM)",10, "#ef6c00"),
]

if st.session_state.running:
    st.success("Tu dors... 😴  (simulation accélérée)")
    place = st.empty()
    chrono = st.empty()
    progress = st.progress(0)

    total = sum(d for _, d, _ in cycles)
    ecoule = 0

    for nom, duree, couleur in cycles:
        for s in range(duree):
            if not st.session_state.running:
                break

            # Affichage de la phase en gros
            place.markdown(
                f'<div class="bigphase" style="background:{couleur}">{nom}</div>',
                unsafe_allow_html=True
            )

            # Chrono depuis Start
            if st.session_state.start_time:
                delta = datetime.now() - st.session_state.start_time
                mins, secs = divmod(int(delta.total_seconds()), 60)
                chrono.markdown(f"⏱️ Temps écoulé : **{mins} min {secs} s**")

            # Barre de progression du cycle
            ecoule += 1
            progress.progress(min(ecoule / total, 1.0))

            time.sleep(1)

        if not st.session_state.running:
            break

    if st.session_state.running:
        place.markdown("### ✅ Cycle terminé — tu peux relancer Start")
    else:
        place.markdown("### ⏹️ Simulation arrêtée")
else:
    st.info("Appuie sur **Start** pour simuler ton endormissement. 😴")
