import streamlit as st
from datetime import datetime
import time

st.set_page_config(page_title="Suivi de sommeil", page_icon="😴", layout="centered")

st.markdown("""
<style>
.stApp { background-color: #0e1117; color: #e6e6e6; }
h1, h2, h3 { color: #cfd8ff; }
.bigphase {
    font-size: 40px; font-weight: bold; text-align: center;
    padding: 25px; border-radius: 15px; margin: 15px 0;
    color: #ffffff;
}
</style>
""", unsafe_allow_html=True)

st.title("😴 Suivi de sommeil (temps réel)")

# ---------- Durées réelles (en minutes) ----------
CYCLE = [
    ("🟢 Éveil / Endormissement", 10, "#2e7d32"),
    ("🔵 Sommeil lent léger",     30, "#1565c0"),
    ("🟣 Sommeil lent profond",   30, "#6a1b9a"),
    ("🟠 Sommeil paradoxal (REM)",20, "#ef6c00"),
]
CYCLE_MIN = sum(d for _, d, _ in CYCLE)  # 90 min

# ---------- État ----------
if "start_time" not in st.session_state:
    st.session_state.start_time = None

col1, col2 = st.columns(2)
with col1:
    if st.button("▶️ Start", use_container_width=True):
        st.session_state.start_time = datetime.now()
        st.rerun()
with col2:
    if st.button("⏹️ Stop", use_container_width=True):
        st.session_state.start_time = None
        st.rerun()

# ---------- Fonction : phase selon minutes écoulées ----------
def get_phase(minutes_ecoulees):
    m = minutes_ecoulees % CYCLE_MIN
    cumul = 0
    for nom, duree, couleur in CYCLE:
        cumul += duree
        if m < cumul:
            return nom, couleur, m, cumul - duree
    return CYCLE[-1][0], CYCLE[-1][2], m, 0

if st.session_state.start_time:
    start = st.session_state.start_time
    ecoule_min = (datetime.now() - start).total_seconds() / 60

    nom, couleur, m_dans_cycle, debut_phase = get_phase(ecoule_min)
    reste = CYCLE_MIN - (ecoule_min % CYCLE_MIN)
    nb_cycles = int(ecoule_min // CYCLE_MIN) + 1

    st.markdown(
        f'<div class="bigphase" style="background:{couleur}">{nom}</div>',
        unsafe_allow_html=True
    )

    h, m = divmod(int(ecoule_min), 60)
    st.markdown(f"⏱️ Temps écoulé : **{h} h {m} min**")
    st.markdown(f"🔁 Cycle n° **{nb_cycles}** — prochaine phase dans **{int(reste)} min**")
    st.markdown(f"🕐 Début : {start.strftime('%H:%M:%S')} — Réveil estimé (1 cycle) : "
                f"{(start.replace(second=0)).strftime('%H:%M')} + 90 min")

    # Rafraîchissement automatique toutes les 5 secondes
    time.sleep(5)
    st.rerun()
else:
    st.info("Appuie sur **Start** pour démarrer le suivi en temps réel. 😴")
