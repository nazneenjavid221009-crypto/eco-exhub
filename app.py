import streamlit as st
import random
import time

# ---------------- CONFIG ----------------
st.set_page_config(page_title="EcoTree", page_icon="🌱", layout="centered")

# ---------------- STYLE ----------------
st.markdown("""
<style>
body { background: linear-gradient(135deg,#081c15,#1b4332); }
.card { background:#ffffff12; padding:32px; border-radius:32px; margin-top:40px; }
.title { font-size:48px; font-weight:900; color:#d8f3dc; text-align:center; }
.center { text-align:center; }
.timer { font-size:36px; font-weight:bold; color:#ffdd57; text-align:center; }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>EcoTree</div>", unsafe_allow_html=True)

# ---------------- DATA ----------------
PRODUCTS = {
    "plastic_bottle": ("Plastic Bottle", 25, ["Steel bottle", "Glass bottle"]),
    "plastic_bag": ("Plastic Bag", 10, ["Cloth bag", "Jute bag"]),
    "shampoo_bottle": ("Shampoo Bottle", 40, ["Shampoo bar", "Refill packs"]),
}

QUESTIONS = [
    ("Plastic decomposes in?", ["10 years","50 years","450 years"], "450 years"),
    ("Best eco choice?", ["Reusable","Single-use","Extra packaging"], "Reusable"),
    ("Which pollutes most?", ["Plastic","Paper","Glass"], "Plastic"),
    ("Fast fashion causes?", ["Low cost","High waste","Trendy"], "High waste"),
    ("Renewable energy?", ["Coal","Solar","Diesel"], "Solar"),
] * 10  # ~50

# ---------------- STATE ----------------
if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.quiz = random.sample(QUESTIONS, 5)
    st.session_state.qi = 0
    st.session_state.score = 0
    st.session_state.timer_start = None

# ---------------- QR PARAM ----------------
pid = st.experimental_get_query_params().get("product", [None])[0]

# ================= STEP 0: WAIT =================
if st.session_state.step == 0:
    st.markdown("<div class='card center'>📷 Scan a product QR code</div>", unsafe_allow_html=True)

    if pid in PRODUCTS:
        st.session_state.product = PRODUCTS[pid]
        st.session_state.step = 1
        st.experimental_rerun()

# ================= STEP 1: RESULT =================
elif st.session_state.step == 1:
    name, eco, alts = st.session_state.product

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader(name)
    st.progress(eco)

    if eco < 30:
        st.write("🌱 A weak sapling")
    elif eco < 60:
        st.write("🌿 A growing tree")
    else:
        st.write("🌳 A thriving tree")

    st.subheader("Better alternatives")
    for a in alts:
        st.write("✅", a)

    if st.button("Continue"):
        st.session_state.step = 2
        st.experimental_rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# ================= STEP 2: QUIZ =================
elif st.session_state.step == 2:
    if st.session_state.timer_start is None:
        st.session_state.timer_start = time.time()

    q, opts, ans = st.session_state.quiz[st.session_state.qi]
    remaining = 10 - int(time.time() - st.session_state.timer_start)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader(f"Question {st.session_state.qi+1} / 5")
    st.markdown(f"<div class='timer'>⏱ {max(0,remaining)}</div>", unsafe_allow_html=True)

    choice = st.radio(q, opts, key=f"q{st.session_state.qi}")

    if remaining <= 0 or st.button("Next"):
        if choice == ans:
            st.session_state.score += 1

        st.session_state.qi += 1
        st.session_state.timer_start = time.time()

        if st.session_state.qi == 5:
            st.session_state.step = 3

        st.experimental_rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# ================= STEP 3: OUTRO =================
elif st.session_state.step == 3:
    st.markdown("<div class='card center'>", unsafe_allow_html=True)
    st.write("🌍 Thank you for exploring EcoTree")
    st.write(f"🔥 Quiz Score: {st.session_state.score} / 5")
    st.write("Every choice matters.")

    if st.button("Reset for next person"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.experimental_rerun()

    st.markdown("</div>", unsafe_allow_html=True)
