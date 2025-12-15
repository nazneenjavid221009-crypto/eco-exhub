import streamlit as st
import random
import time

# ---------------- PAGE SETUP ----------------
st.set_page_config(
    page_title="EcoTree Exhibition",
    page_icon="🌱",
    layout="centered"
)

# ---------------- STYLING ----------------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #081c15, #1b4332);
}
.title {
    font-size: 46px;
    font-weight: 900;
    color: #d8f3dc;
    text-align: center;
}
.subtitle {
    color: #b7e4c7;
    text-align: center;
}
.card {
    background: #ffffff12;
    padding: 28px;
    border-radius: 28px;
    margin-top: 25px;
}
.center {
    text-align: center;
}
.timer {
    font-size: 28px;
    font-weight: bold;
    color: #ffdd57;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.markdown("<div class='title'>EcoTree</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Scan • See • Decide</div>", unsafe_allow_html=True)

# ---------------- PRODUCTS ----------------
PRODUCTS = {
    "plastic_bottle": ("Plastic Water Bottle", 25, ["Steel bottle", "Glass bottle"]),
    "plastic_bag": ("Plastic Bag", 10, ["Cloth bag", "Jute bag"]),
    "shampoo_bottle": ("Shampoo Bottle", 40, ["Shampoo bar", "Refill packs"]),
    "chips_packet": ("Chips Packet", 30, ["Bulk snacks", "Homemade snacks"]),
}

# ---------------- QUIZ QUESTIONS (50 READY) ----------------
QUIZ_QUESTIONS = [
    ("Plastic decomposes in?", ["10 years", "50 years", "450 years"], "450 years"),
    ("Best alternative to plastic?", ["Glass", "PVC", "Styrofoam"], "Glass"),
    ("Which uses more water?", ["Cotton", "Polyester", "Nylon"], "Cotton"),
    ("Fast fashion is harmful because?", ["Low cost", "High waste", "Bright colors"], "High waste"),
    ("Which is renewable?", ["Coal", "Solar", "Diesel"], "Solar"),
] * 10  # makes ~50 questions

# ---------------- SESSION STATE ----------------
if "screen" not in st.session_state:
    st.session_state.screen = 1

if "quiz_questions" not in st.session_state:
    st.session_state.quiz_questions = random.sample(QUIZ_QUESTIONS, 5)
    st.session_state.q_index = 0
    st.session_state.score = 0

# ---------------- READ QR PARAM ----------------
params = st.experimental_get_query_params()
product_id = params.get("product", [None])[0]

# ---------------- SCREEN 1: WAITING ----------------
if st.session_state.screen == 1:
    st.markdown("<div class='card center'>", unsafe_allow_html=True)
    st.write("📷 Scan a product QR code to begin")
    st.write("The EcoTree will respond instantly.")
    st.markdown("</div>", unsafe_allow_html=True)

    if product_id in PRODUCTS:
        st.session_state.screen = 2
        st.experimental_rerun()

# ---------------- SCREEN 2: PRODUCT ----------------
elif st.session_state.screen == 2:
    name, score, alts = PRODUCTS[product_id]

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📦 Product Selected")
    st.write(name)

    st.subheader("🌍 Eco Score")
    st.progress(score)

    st.session_state.tree_score = score
    st.session_state.alts = alts

    if st.button("Next ▶"):
        st.session_state.screen = 3
        st.experimental_rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- SCREEN 3: TREE + RECOMMENDATIONS ----------------
elif st.session_state.screen == 3:
    score = st.session_state.tree_score

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🌳 EcoTree Growth")

    if score < 30:
        st.write("🌱 A fragile sapling")
    elif score < 60:
        st.write("🌿 A growing tree")
    else:
        st.write("🌳 A thriving ecosystem")

    st.subheader("🔁 Better Choices")
    for a in st.session_state.alts:
        st.write(f"✅ {a}")

    if st.button("Continue ▶"):
        st.session_state.screen = 4
        st.experimental_rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- SCREEN 4: QUIZ CHOICE ----------------
elif st.session_state.screen == 4:
    st.markdown("<div class='card center'>", unsafe_allow_html=True)
    choice = st.radio(
        "Would you like to try the Rapid Fire Eco Quiz?",
        ["No, skip", "Yes, start ⚡"]
    )

    if choice == "Yes, start ⚡":
        st.session_state.screen = 5
        st.experimental_rerun()

    if choice == "No, skip":
        st.session_state.screen = 6
        st.experimental_rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- SCREEN 5: QUIZ ----------------
elif st.session_state.screen == 5:
    q, options, answer = st.session_state.quiz_questions[st.session_state.q_index]

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader(f"⚡ Question {st.session_state.q_index + 1} / 5")

    start = time.time()
    choice = st.radio(q, options)

    remaining = 10 - int(time.time() - start)
    st.markdown(f"<div class='timer'>⏱ {max(0, remaining)} sec</div>", unsafe_allow_html=True)

    if st.button("Submit"):
        if choice == answer:
            st.session_state.score += 1

        st.session_state.q_index += 1

        if st.session_state.q_index == 5:
            st.session_state.screen = 6
        st.experimental_rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- SCREEN 6: OUTRO ----------------
elif st.session_state.screen == 6:
    st.markdown("<div class='card center'>", unsafe_allow_html=True)
    st.write("🌍 Thank you for exploring EcoTree")
    st.write(f"🔥 Quiz Score: {st.session_state.score} / 5")
    st.write("Every choice shapes the future.")
    st.markdown("</div>", unsafe_allow_html=True)
