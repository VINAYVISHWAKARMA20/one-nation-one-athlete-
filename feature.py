import streamlit as st

# ========== Page Config ==========
st.set_page_config(page_title="One Nation, One Athlete Platform - Features", page_icon="🏅", layout="wide")

# ========== Styles ==========
st.markdown(
    """
    <style>
    /* Full-page border wrapper */
    .page-border {
        border: 5px solid;
        border-image-slice: 1;
        border-width: 5px;
        border-image-source: linear-gradient(45deg, #007BFF, #00c6ff, #9c27b0, #ff4081);
        border-radius: 20px;
        padding: 25px;
        margin: 15px;
        background-color: rgba(255,255,255,0.95);
        box-shadow: 0 10px 25px rgba(0,0,0,0.15);
    }

    /* Animated background shapes */
    .animated-bg {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
        background: radial-gradient(circle, rgba(0,123,255,0.05) 10%, transparent 10%) repeat;
        background-size: 50px 50px;
        animation: moveBg 25s linear infinite;
    }
    @keyframes moveBg {
        0% { background-position: 0 0; }
        100% { background-position: 1000px 1000px; }
    }

    /* Main header centered */
    h1 {
        color: black !important;
        font-weight: 800;
        font-size: 40px;
        text-align: center;
        text-shadow: 2px 2px 6px rgba(0,0,0,0.15);
    }
    h2, h3 { color: #007BFF; }

    /* Feature cards with glow effect */
    .feature-card {
        background: white;
        padding: 20px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 8px 20px rgba(0,0,0,0.12);
        margin: 10px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        align-items: center;
        height: 320px;
        transition: transform 0.2s ease, box-shadow 0.25s ease, filter 0.2s ease;
        border-top: 5px solid #007BFF;
        position: relative;
    }
    .feature-card::after {
        content: "";
        position: absolute;
        top: -5px; left: -5px; right: -5px; bottom: -5px;
        border-radius: 25px;
        background: linear-gradient(45deg, #007BFF, #00c6ff, #9c27b0, #ff4081);
        opacity: 0;
        z-index: -1;
        transition: opacity 0.25s ease;
    }
    .feature-card:hover::after { opacity: 0.25; }
    .feature-card:hover { transform: translateY(-8px); box-shadow: 0 12px 25px rgba(0,0,0,0.22); }

    .feature-icon { font-size: 42px; margin-bottom: 10px; }
    .feature-title { font-size: 20px; font-weight: 700; margin-bottom: 8px; color: #007BFF; }
    .feature-desc { font-size: 14px; color: #444; line-height: 1.4; margin-bottom: 15px; padding: 0 6px; }

    /* Button styling */
    .card-footer { width: 100%; display: flex; justify-content: center; align-items: center; }
    .learn-btn {
        display: inline-block;
        background-color: #007BFF !important;
        color: #FFFFFF !important;
        padding: 10px 20px;
        border-radius: 8px;
        font-size: 14px;
        text-decoration: none !important;
        font-weight: 600;
        transition: background-color 0.18s, transform 0.08s;
    }
    .learn-btn:hover {
        background-color: #0056b3 !important;
        transform: scale(1.05);
    }

    @media (max-width: 900px) { .feature-card { height: auto; } }
    </style>
    """,
    unsafe_allow_html=True,
)

# ========== Background animation div ==========
st.markdown('<div class="animated-bg"></div>', unsafe_allow_html=True)

# ========== Helper Function ==========
def feature_card(icon, title, desc, link="#"):
    return f"""
    <div class="feature-card">
        <div>
            <div class="feature-icon">{icon}</div>
            <div class="feature-title">{title}</div>
            <div class="feature-desc">{desc}</div>
        </div>
        <div class="card-footer">
            <a href="{link}" class="learn-btn">Learn More</a>
        </div>
    </div>
    """

# ========== Wrap entire page in border ==========
st.markdown('<div class="page-border">', unsafe_allow_html=True)

# ========== Page Title ==========
st.title("🏅 One Nation, One Athlete Platform")
st.subheader("Ensuring Fairness, Access, and Opportunity in Sports")
st.header("🌟 Key Features of the Platform")
st.markdown("---")

# ========== Categories & Features ==========
categories = {
    "📊 Performance & Training": [
        ("📈", "Performance Tracking", "Track athlete performance over time with detailed analytics and downloadable reports."),
        ("🤸", "Personalized Training", "AI-driven customized training plans tailored to each athlete’s abilities and goals."),
        ("⏱️", "Injury Prevention", "Proactive monitoring and alerts to reduce injury risks via smart assessments.")
    ],
    "💰 Financial & Career Support": [
        ("💸", "Financial Guidance", "Resources for scholarships, sponsorship opportunities and financial literacy for athletes."),
        ("🎓", "Career Pathways", "Support for education, certifications and career transition planning after competitive sports."),
        ("🧾", "Resource Allocation", "Transparent allocation of funds, facilities, and equipment based on needs and performance.")
    ],
    "🌍 Inclusivity & Accessibility": [
        ("🧑‍🦽", "Disability Support", "Accessibility tools and specialized programs to empower differently-abled athletes."),
        ("🏞️", "Rural Outreach", "Talent identification and training programs focused on rural and underrepresented regions."),
        ("🤝", "Equity in Sports", "Policies and tools to ensure fair opportunities across genders, regions and communities.")
    ],
    "📡 Technology & Collaboration": [
        ("🔗", "Centralized Platform", "Unified system to manage athlete profiles, training modules, and institutional reporting."),
        ("📱", "Mobile Accessibility", "Responsive mobile access for athletes, coaches and administrators on the go."),
        ("👨‍🏫", "Coach Collaboration", "Tools for coaches to assign plans, comment on progress and communicate with athletes.")
    ],
    "🏆 Recognition & Growth": [
        ("🥇", "Achievements Showcase", "Feature athlete milestones, certificates and competition highlights on their profiles."),
        ("📢", "Talent Promotion", "Channels to promote promising athletes to scouts, sponsors and institutions."),
        ("🌐", "Global Exposure", "Opportunities to connect with international competitions, trials and networks.")
    ]
}

# ========== Display Features ==========
for category, features in categories.items():
    st.markdown(f"### {category}")
    cols_per_row = 3
    cols = st.columns(cols_per_row)
    for i, (icon, title, desc) in enumerate(features):
        with cols[i % cols_per_row]:
            st.markdown(feature_card(icon, title, desc), unsafe_allow_html=True)
    st.markdown("---")

st.markdown('</div>', unsafe_allow_html=True)
