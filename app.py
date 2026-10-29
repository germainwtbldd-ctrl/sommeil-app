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

# ---------- Lire l'heure de début depuis l'URL ----------
params = st.query_params
start_str = params.get("start", None)

start_time = None
if start_str:
    try:
        start_time = datetime.fromisoformat(start_str)
    except ValueError:
        start_time = None

# ---------- Boutons ----------
col1, col2 = st.columns(2)
with col1:
    if st.button("▶️ Start", use_container_width=True):
        now = datetime.now().isoformat(timespec="seconds")
        st.query_params["start"] = now
        st.rerun()
with col2:
    if st.button("⏹️ Stop", use_container_width=True):
        if "start" in st.query_params:
            del st.query_params["start"]
        st.rerun()

# ---------- Calcul de la phase ----------
def get_phase(minutes_ecoulees):
    m = minutes_ecoulees % CYCLE_MIN
    cumul = 0
    for nom, duree, couleur in CYCLE:
        cumul += duree
        if m < cumul:
            return nom, couleur
    return CYCLE[-1][0], CYCLE[-1][2]

if start_time:
    ecoule_min = (datetime.now() - start_time).total_seconds() / 60
    nom, couleur = get_phase(ecoule_min)
    reste = CYCLE_MIN - (ecoule_min % CYCLE_MIN)
    nb_cycles = int(ecoule_min // CYCLE_MIN) + 1

    st.markdown(
        f'<div class="bigphase" style="background:{couleur}">{nom}</div>',
        unsafe_allow_html=True
    )

    h, m = divmod(int(ecoule_min), 60)
    st.markdown(f"⏱️ Temps écoulé : **{h} h {m} min**")
    st.markdown(f"🔁 Cycle n° **{nb_cycles}** — prochaine phase dans **{int(reste)} min**")
    st.markdown(f"🕐 Début : **{start_time.strftime('%H:%M:%S')}**")

    # Rafraîchissement auto toutes les 5 s (sans casser l'URL)
    time.sleep(5)
    st.rerun()
else:
    st.info("Appuie sur **Start** pour démarrer le suivi en temps réel. 😴")
