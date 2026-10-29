import streamlit as st
import time

st.set_page_config(page_title="Suivi de sommeil", page_icon="😴")

st.title("😴 Suivi de sommeil")
st.write("Clique sur **Start** pour simuler ton endormissement.")

# Initialisation de l'état
if "running" not in st.session_state:
    st.session_state.running = False

col1, col2 = st.columns(2)

with col1:
    if st.button("▶️ Start", use_container_width=True):
        st.session_state.running = True
        st.rerun()

with col2:
    if st.button("⏹️ Stop", use_container_width=True):
        st.session_state.running = False
        st.rerun()

# Les cycles de sommeil (durées en secondes pour la démo)
cycles = [
    ("🟢 Éveil / Endormissement", 8),
    ("🔵 Sommeil lent léger", 12),
    ("🟣 Sommeil lent profond", 15),
    ("🟠 Sommeil paradoxal (REM)", 10),
]

if st.session_state.running:
    st.success("Tu dors... 😴")
    place = st.empty()
    progress = st.progress(0)

    total = sum(d for _, d in cycles)
    ecoule = 0

    for nom, duree in cycles:
        for s in range(duree):
            place.markdown(f"### Phase en cours : {nom}")
            place.markdown(f"Temps dans cette phase : **{s}s** / {duree}s")
            ecoule += 1
            progress.progress(min(ecoule / total, 1.0))
            time.sleep(1)
            if not st.session_state.running:
                break
        if not st.session_state.running:
            break

    place.markdown("### ✅ Cycle terminé (ou arrêté)")
else:
    st.info("Appuie sur **Start** pour commencer.")
