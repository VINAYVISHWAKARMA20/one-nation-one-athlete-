import streamlit as st

# --- Page Config ---
st.set_page_config(
    page_title="One Nation, One Athlete Platform",
    page_icon="🏅",
    layout="wide",
)

# --- Global CSS Styles ---
st.markdown(
    """
    <style>
    /* ✅ Full page background */
    .stApp {
        background-color: #ffffff !important;
    }
    /* Page content */
    .block-container {
        padding: 2rem 4rem;
        color: #002b5c !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* Main header (page title) */
    .header {
        background: linear-gradient(90deg, #0052D4, #4364F7, #6FB1FC);
        color: white !important;
        padding: 1.5rem 2rem;
        border-radius: 16px;
        font-weight: 900;
        font-size: 3.5rem;
        text-align: center;
        margin-bottom: 3rem;
        box-shadow: 0 10px 35px rgba(67,100,247,0.6);
        letter-spacing: 2px;
        font-family: 'Poppins', sans-serif;
        text-transform: uppercase;
        text-shadow: 2px 2px 6px rgba(0,0,0,0.3);
    }

    .subheader {
        text-align: center;
        color: #002b5c !important;
        font-weight: 700;
        font-size: 1.8rem;
        margin-bottom: 3rem;
        font-family: 'Poppins', sans-serif;
    }

    /* Section headers (blog/headline style) */
    .section-header {
        background: linear-gradient(90deg, #0052D4, #4364F7, #6FB1FC);
        color: white !important;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        font-weight: 800;
        font-size: 2rem;
        margin-top: 4rem;
        margin-bottom: 2rem;
        box-shadow: 0 5px 20px rgba(0, 43, 92, 0.3);
        font-family: 'Poppins', sans-serif;
        text-transform: uppercase;
        letter-spacing: 1px;
        text-align: center;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .section-header:hover {
        transform: scale(1.02);
        box-shadow: 0 10px 30px rgba(0, 43, 92, 0.4);
    }

    p {
        color: #002b5c !important;
        font-size: 1.1rem;
        line-height: 1.8;
        text-align: justify;
    }

    /* Highlight key points in paragraphs */
    p span.highlight {
        font-weight: 700; /* bold */
        font-size: 1.2rem; /* slightly larger */
        color: #4364F7; /* blue accent color */
    }

    /* Image container with hover zoom & shadow */
    .img-container {
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 10px 35px rgba(0, 43, 92, 0.2);
        margin-bottom: 2rem;
        transition: transform 0.35s ease, box-shadow 0.35s ease;
        width: 4in;
        height: 4in;
        display: flex;
        justify-content: center;
        align-items: center;
        margin-left: auto;
        margin-right: auto;
    }
    .img-container:hover {
        transform: scale(1.1);
        box-shadow: 0 20px 60px rgba(0, 43, 92, 0.5);
    }
    .img-container img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }

    hr.styled-hr {
        border: none;
        height: 3px;
        background: linear-gradient(to right, #4364F7, #6FB1FC);
        margin: 4rem 0 3rem 0;
        border-radius: 12px;
    }

    footer {
        text-align: center;
        color: #002b5c !important;
        font-size: 1rem;
        margin-top: 5rem;
        padding-bottom: 2rem;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Title ---
st.markdown('<div class="header">🏅 One Nation, One Athlete Platform</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subheader">Ensuring Fairness, Access, and Opportunity in Sports Across India 🇮🇳</div>',
    unsafe_allow_html=True,
)

# --- Introduction ---
st.markdown('<div class="section-header">📖 Introduction</div>', unsafe_allow_html=True)
i1, i2 = st.columns([2, 3])
with i1:
    st.markdown("""
    <p>
    India’s sporting landscape is expanding rapidly, with increasing participation across diverse disciplines. 
    However, the path to excellence remains challenging for many athletes, especially those from <span class="highlight">rural regions</span>, <span class="highlight">tribal communities</span>, and <span class="highlight">underprivileged backgrounds</span>. 
    <span class="highlight">Limited access to quality training</span>, <span class="highlight">inadequate mentorship</span>, and a <span class="highlight">lack of structured career planning</span> hinder their growth.
    <br><br>
    The One Nation, One Athlete platform aims to change this by providing a <span class="highlight">unified, technology-driven ecosystem</span> that connects athletes, coaches, institutions, and sponsors. 
    It envisions creating an <span class="highlight">inclusive environment</span> where every athlete receives equal opportunities to develop and succeed on national and international stages.
    </p>
    """, unsafe_allow_html=True)
with i2:
    st.markdown("""
    <div class="img-container">
        <img src="https://images.unsplash.com/photo-1521412644187-c49fa049e84d?auto=format&fit=crop&w=1200&q=80">
    </div>
    """, unsafe_allow_html=True)

# --- Challenges ---
st.markdown('<div class="section-header">⚠️ Current Challenges</div>', unsafe_allow_html=True)
c1, c2 = st.columns([3, 2])
with c1:
    st.markdown("""
    <p>
    Despite major strides in Indian sports, the athlete development ecosystem remains <span class="highlight">fragmented</span>. 
    There is no <span class="highlight">centralized system</span> to track performance, medical data, or training progress. 
    Coaches and organizations often lack <span class="highlight">reliable tools</span> to monitor talent, and promising athletes go unnoticed due to <span class="highlight">limited exposure</span>. 
    <br><br>
    Rural athletes face <span class="highlight">cultural, economic, and infrastructural challenges</span>, while athletes with disabilities struggle to access <span class="highlight">inclusive facilities</span>. 
    These systemic gaps reduce India’s ability to nurture its <span class="highlight">vast talent pool</span>, resulting in missed opportunities on the global stage.
    </p>
    """, unsafe_allow_html=True)
with c2:
    st.markdown("""
    <div class="img-container">
        <img src="https://images.unsplash.com/photo-1504384308090-c894fdcc538d?auto=format&fit=crop&w=1200&q=80">
    </div>
    """, unsafe_allow_html=True)

# --- Vision ---
st.markdown('<div class="section-header">🌟 Vision</div>', unsafe_allow_html=True)
v1, v2 = st.columns([2, 3])
with v1:
    st.markdown("""
    <p>
    The platform envisions a <span class="highlight">unified, data-driven ecosystem</span> where every athlete can flourish. 
    It will integrate <span class="highlight">AI-powered analytics</span>, <span class="highlight">performance dashboards</span>, and <span class="highlight">wellness tracking</span> to offer personalized growth plans.
    <br><br>
    By connecting athletes to <span class="highlight">certified coaches, physiotherapists, nutritionists, and mental health experts</span>, it provides holistic development pathways.
    The platform will also offer <span class="highlight">career counselling</span>, <span class="highlight">sponsorship matching</span>, and <span class="highlight">educational opportunities</span>.
    </p>
    """, unsafe_allow_html=True)
with v2:
    st.markdown("""
    <div class="img-container">
        <img src="https://images.unsplash.com/photo-1517649763962-0c623066013b?auto=format&fit=crop&w=1200&q=80">
    </div>
    """, unsafe_allow_html=True)

# --- Impact ---
st.markdown('<div class="section-header">🚀 Expected Impact</div>', unsafe_allow_html=True)
imp1, imp2 = st.columns([3, 2])
with imp1:
    st.markdown("""
    <p>
    The platform will transform how talent is <span class="highlight">identified, nurtured, and supported</span>. 
    <span class="highlight">Centralized athlete data</span> enables early talent spotting and reduces dropout rates. 
    Coaches get <span class="highlight">real-time performance insights</span> for tailored training.
    <br><br>
    Transparent funding systems encourage <span class="highlight">sponsor investment</span>. 
    Over time, it bridges disparities, increases <span class="highlight">India’s medal prospects</span>, and promotes sports as a <span class="highlight">sustainable profession</span>.
    </p>
    """, unsafe_allow_html=True)
with imp2:
    st.markdown("""
    <div class="img-container">
        <img src="https://images.unsplash.com/photo-1526403229747-0a1a0a7a3f3a?auto=format&fit=crop&w=1200&q=80">
    </div>
    """, unsafe_allow_html=True)

# --- Features ---
st.markdown('<div class="section-header">✨ Key Features & Innovations</div>', unsafe_allow_html=True)
f1, f2 = st.columns([2, 3])
with f1:
    st.markdown("""
    <p>
    The platform offers:  
    <br>• <span class="highlight">Mobile app</span> for athlete management  
    • <span class="highlight">AI-driven analytics</span> for skill development  
    • <span class="highlight">Video-based technique analysis</span> for injury prevention  
    • <span class="highlight">Multilingual interface</span> for inclusivity  
    • <span class="highlight">Secure scholarship and sponsorship portals</span>  
    • <span class="highlight">Mentorship networks</span> with former athletes and experts
    </p>
    """, unsafe_allow_html=True)
with f2:
    st.markdown("""
    <div class="img-container">
        <img src="https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1200&q=80">
    </div>
    """, unsafe_allow_html=True)

# --- Conclusion ---
st.markdown('<div class="section-header">✅ Conclusion</div>', unsafe_allow_html=True)
con1, con2 = st.columns([2, 3])
with con1:
    st.markdown("""
    <p>
    The platform has the potential to redefine India’s approach to sports. 
    By building a <span class="highlight">connected and transparent ecosystem</span>, no athlete is left behind. 
    Through <span class="highlight">data-driven insights, inclusive infrastructure, and equitable access</span>, this initiative unlocks India’s <span class="highlight">true sporting potential</span>.
    <br><br>
    It represents a step towards transforming India from a country of raw talent into a <span class="highlight">nation of world-class champions</span>.
    </p>
    """, unsafe_allow_html=True)
with con2:
    st.markdown("""
    <div class="img-container">
        <img src="https://images.unsplash.com/photo-1517649763962-0c623066013b?auto=format&fit=crop&w=1200&q=80">
    </div>
    """, unsafe_allow_html=True)

# --- Footer ---
st.markdown(
    """
    <footer>
    <hr class="styled-hr">
    © 2024 One Nation, One Athlete Platform | Built with ❤️ using Streamlit
    </footer>
    """,
    unsafe_allow_html=True,
)
