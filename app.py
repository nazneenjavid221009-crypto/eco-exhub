import streamlit as st
import random
import time

# ---------- PAGE ----------
st.set_page_config(page_title="EcoTree Exhibition", page_icon="🌱")

# ---------- STYLE ----------
st.markdown("""
<style>
body { background: linear-gradient(135deg,#081c15,#1b4332); }
.card { background:#ffffff12; padding:30px; border-radius:30px; margin-top:30px; }
.title { font-size:48px; font-weight:900; color:#d8f3dc; text-align:center; }
.center { text-align:center; }
.timer { font-size:32px; color:#ffdd57; font-weight:bold; }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>EcoTree</div>", unsafe_allow_html=True)

# ---------- DATA ----------
PRODUCTS = {
    "plastic_bottle": ("Plastic Water Bottle", 25, ["Steel bottle", "Glass bottle"]),
    "plastic_bag": ("Plastic Bag", 10, ["Cloth bag", "Jute bag"]),
    "shampoo_bottle": ("Shampoo Bottle", 40, ["Shampoo bar", "Refill packs"]),
    "chips_packet": ("Chips Packet", 30, ["Bulk snacks", "Homemade snacks"]),
}

QUESTIONS = [
    ("Plastic decomposes in?", ["10 years","50 years","450 years"], "450 years"),
    ("Best eco choice?", ["Reusable","Single-use","Extra packaging"], "Reusable"),
    ("Which pollutes most?", ["Plastic","Paper","Glass"], "Plastic"),
    ("Fast fashion causes?", ["Low cost","High waste","Trendy clothes"], "High waste"),
    ("Renewable energy?", ["Coal","Solar","Diesel"], "Solar"),
] * 10   # ~50 questions

# ---------- STATE ----------
if "screen" not in st.session_state:
    st.session_state.screen = 0

if "quiz_set" not in st.session_state:
    st.session_state.quiz_set = random.sample(QUESTIONS, 5)
    st.session_state.qn = 0
    st.session_state.score = 0
    st.session_state.start_time = time.time()

# ---------- QR PARAM ----------
params = st.experimental_get_query_params()
pid = params.get("product", [None])[0]

# ---------- SCREEN 0 : WAIT ----------
if st.session_state.screen == 0:
    st.markdown("<div class='card center'>📷 Scan a product QR code</div>", unsafe_allow_html=True)
    if pid in PRODUCTS:
        st.session_state.product = PRODUCTS[pid]
        st.session_state.screen = 1
        st.experimental_rerun()

# ---------- SCREEN 1 : RESULT ----------
elif st.session_state.screen == 1:
    name, eco, alts = st.session_state.product

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader(name)
    st.progress(eco)

    if eco < 30: st.write("🌱 A fragile sapling")
    elif eco < 60: st.write("🌿 Growing tree")
    else: st.write("🌳 Thriving ecosystem")

    st.subheader("Better alternatives")
    for a in alts: st.write("✅", a)

    if st.button("Next"):
        st.session_state.screen = 2
        st.experimental_rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# ---------- SCREEN 2 : QUIZ DECISION ----------
elif st.session_state.screen == 2:
    st.markdown("<div class='card center'>", unsafe_allow_html=True)
    st.write("Do you want to try the Rapid Fire Quiz?")
    if st.button("Yes ⚡"):
        st.session_state.start_time = time.time()
        st.session_state.screen = 3
        st.experimental_rerun()
    if st.button("No"):
        st.session_state.screen = 5
        st.experimental_rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ---------- SCREEN 3 : QUIZ ----------
elif st.session_state.screen == 3:
    q, opts, ans = st.session_state.quiz_set[st.session_state.qn]

    elapsed = int(time.time() - st.session_state.start_time)
    remaining = 10 - elapsed

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader(f"Question {st.session_state.qn+1} / 5")
    st.markdown(f"<div class='timer'>⏱ {max(0,remaining)} sec</div>", unsafe_allow_html=True)

    choice = st.radio(q, opts, key=st.session_state.qn)

    if remaining <= 0 or st.button("Submit"):
        if choice == ans:
            st.session_state.score += 1

        st.session_state.qn += 1
        st.session_state.start_time = time.time()

        if st.session_state.qn == 5:
            st.session_state.screen = 5
        st.experimental_rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# ---------- SCREEN 5 : OUTRO ----------
elif st.session_state.screen == 5:
    st.markdown("<div class='card center'>", unsafe_allow_html=True)
    st.write("🌍 Thank you for exploring EcoTree")
    st.write(f"🔥 Quiz Score: {st.session_state.score} / 5")
    st.write("Every choice matters.")
    st.markdown("</div>", unsafe_allow_html=True)
