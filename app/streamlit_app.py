import streamlit as st
from datetime import datetime
import time

from core.coordinator import run_pipeline

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Campus Safety Intelligence Console",
    layout="wide"
)

# ================= GLOBAL STYLE =================
st.markdown("""
<style>
/* App background */
.stApp {
    background: radial-gradient(circle at top, #3b1d5c, #0b0715 60%);
}

/* Hero section */
.hero {
    background: linear-gradient(135deg, #6d28d9, #4c1d95);
    padding: 56px;
    border-radius: 26px;
    margin-bottom: 32px;
    box-shadow: 0 0 80px rgba(124,58,237,0.35);
}

/* Cards */
.card {
    background: rgba(36, 20, 64, 0.65);
    backdrop-filter: blur(12px);
    padding: 22px;
    border-radius: 18px;
    margin-bottom: 18px;
    border: 1px solid rgba(124,58,237,0.35);
}

/* Text */
h1, h2, h3, h4 {
    color: #f5f3ff !important;
}
p, label {
    color: #e9d5ff !important;
}

/* Buttons */
.stButton>button {
    background: linear-gradient(135deg, #7c3aed, #5b21b6);
    color: white;
    border-radius: 14px;
    font-weight: 600;
}
.stButton>button:hover {
    background: linear-gradient(135deg, #8b5cf6, #6d28d9);
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #140c2e, #090314);
}

/* Risk borders */
.high { border-left: 6px solid #ef4444; }
.medium { border-left: 6px solid #facc15; }
.low { border-left: 6px solid #22c55e; }
</style>
""", unsafe_allow_html=True)

# ================= STATUS BAR =================
now = datetime.now()
st.markdown(f"""
<div style="display:flex;justify-content:space-between;
            padding:14px 24px;border-radius:14px;
            background:#120b26;border:1px solid #3b1d5c;
            margin-bottom:26px;">
<div>🏫 Campus: <b>Active Deployment</b></div>
<div>🕒 {now.strftime('%H:%M:%S')}</div>
<div>🟢 System: Operational</div>
<div>🌙 {"Night" if now.hour >= 20 else "Day"} Mode</div>
</div>
""", unsafe_allow_html=True)

# ================= HERO =================
st.markdown("""
<div class="hero">
<h1>Autonomous Campus Safety Intelligence</h1>
<p style="font-size:18px;">
One Standardized AI Core • Multi-Campus Deployment • Human-in-the-Loop Safety
</p>
</div>
""", unsafe_allow_html=True)

# ================= MAIN GRID =================
left, center, right = st.columns([1.2, 1.6, 1.2])

# --------------------------------------------------
# LEFT PANEL – INCIDENT INPUT
# --------------------------------------------------
with left:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📥 Incident Intake")

    incident_type = st.selectbox(
        "Incident Type",
        [
            "Fire",
            "Medical Emergency",
            "Harassment / Stalking",
            "Theft",
            "Lab Hazard",
            "Cyberbullying",
            "Suspicious Activity"
        ]
    )

    location = st.selectbox(
        "Location",
        [
            "Girls Hostel",
            "Boys Hostel",
            "Academic Block",
            "Laboratory",
            "Library",
            "Parking Area"
        ]
    )

    description = st.text_area("Description", height=110)
    role = st.selectbox("Reported By", ["Student", "Faculty", "Staff", "Security"])
    crowd = st.selectbox("Crowd Level", ["Low", "Medium", "High"])
    panic = st.checkbox("🚨 Panic Trigger")

    submit = st.button("Submit Incident", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --------------------------------------------------
# CENTER PANEL – LIVE SITUATION
# --------------------------------------------------
with center:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📊 Situation Overview")

    if not submit:
        st.info("System monitoring campus. No active incidents.")
    st.markdown('</div>', unsafe_allow_html=True)

    if submit and description.strip():
        text = f"{incident_type}. {description}"
        if panic:
            text = "EMERGENCY. " + text

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🧠 AI Agent Pipeline")

        steps = ["Intake", "Risk", "Response", "Audit"]
        progress = st.progress(0)
        for i, step in enumerate(steps):
            st.write(f"✔ {step} Agent")
            progress.progress((i + 1) / len(steps))
            time.sleep(0.3)

        st.markdown('</div>', unsafe_allow_html=True)

        result = run_pipeline(
            incident_text=text,
            location=location,
            user_role=role
        )

        audit = result["final"]
        contacts = result["emergency_contacts"]

        risk_class = "low"
        if audit.risk_level == "High":
            risk_class = "high"
        elif audit.risk_level == "Medium":
            risk_class = "medium"

        st.markdown(f'<div class="card {risk_class}">', unsafe_allow_html=True)
        st.subheader("⚠ Threat Assessment")

        st.write("**Risk Level:**", audit.risk_level)
        st.write("**Confidence:**", audit.confidence_level)
        st.write("**Action:**", audit.final_decision)
        st.markdown('</div>', unsafe_allow_html=True)

# --------------------------------------------------
# RIGHT PANEL – RESPONSE & GOVERNANCE
# --------------------------------------------------
with right:
    if submit and description.strip():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🚓 Response & Escalation")

        for i, auth in enumerate(audit.escalation_chain, start=1):
            st.write(f"{i}. {auth}")

        if audit.risk_level == "High":
            st.markdown("### Emergency Contacts")
            st.button(f"🚑 Ambulance ({contacts['external']['ambulance']})")
            st.button(f"🔥 Fire ({contacts['external']['fire']})")
            st.button(f"🚓 Police ({contacts['external']['police']})")

        st.markdown('</div>', unsafe_allow_html=True)

        with st.expander("🧾 Investigation Notes"):
            st.write(audit.explanation)

# ================= FOOTER =================
st.caption(
    "Policy-Driven AI • Explainable Decisions • Privacy-Aware • "
    "Human Authority Retained"
)

