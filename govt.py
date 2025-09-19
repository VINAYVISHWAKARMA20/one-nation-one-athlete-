import streamlit as st
import math

# --- Page Config ---
st.set_page_config(
    page_title="One Nation One Athlete - Schemes Portal",
    layout="wide",
    page_icon="🏅",
    initial_sidebar_state="collapsed"
)

# --- Session State ---
if "favorites" not in st.session_state:
    st.session_state.favorites = []
if "comments" not in st.session_state:
    st.session_state.comments = []

# --- Custom CSS ---
st.markdown("""
<style>
.stApp {
    background: linear-gradient(120deg, #e6f7ff, #ffffff);
    font-family: 'Segoe UI', sans-serif;
}

/* Hero Section */
.hero {
    background: url("https://www.shutterstock.com/image-illustration/sports-day-world-athletics-banner-players-2151597265.jpeg") no-repeat center center;
    background-size: cover;
    padding: 80px 25px;
    border-radius: 20px;
    color: white;
    text-align: center;
    margin-bottom: 40px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.25);
    position: relative;
    overflow: hidden;
}
.hero::after {
    content: "";
    position: absolute;
    top: 0; left: 0;
    right: 0; bottom: 0;
    border-radius: 20px;
    background: rgba(0, 115, 230, 0.6);
}
.hero-content {
    position: relative;
    z-index: 1;
}
.hero h1 {
    font-size: 52px;
    font-weight: 800;
    margin-bottom: 14px;
}
.hero p {
    font-size: 20px;
    opacity: 0.95;
}
.hero-btn, .hero-link-btn {
    margin-top: 20px;
    background: #ffcc00;
    color: black !important;
    padding: 12px 28px;
    border-radius: 30px;
    border: none;
    font-size: 1.1em;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.3s ease;
    z-index: 1;
    text-decoration: none;
    display: inline-block;
}
.hero-btn:hover, .hero-link-btn:hover {
    background: #ffc107;
    transform: scale(1.07);
    color: black !important;
}
.hero-actions {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 20px;
}
.hero-actions .right-btn-container {
    position: absolute;
    top: 20px;
    right: 30px;
}
.hero-actions .right-btn-container .hero-btn {
    margin-top: 0;
}

/* Filters */
.filters {
    background: #f0fff0;
    padding: 20px 28px;
    border-radius: 14px;
    margin-bottom: 35px;
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
}

/* Scheme Card */
.scheme-card {
    background: #ffffff;
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 25px;
    box-shadow: 0 5px 20px rgba(0,0,0,0.1);
    transition: all 0.3s ease-in-out;
}
.scheme-card:hover {
    transform: translateY(-6px) scale(1.02);
    box-shadow: 0 8px 25px rgba(0,0,0,0.18);
}
.scheme-card img {
    width: 100%;
    height: 200px;
    border-radius: 12px;
    object-fit: cover;
    margin-bottom: 14px;
}
.scheme-card h3 { 
    color: #0073e6; 
    margin-bottom: 6px; 
}
.scheme-card .meta { 
    font-size: 14px; 
    color: #555; 
    margin-bottom: 10px; 
}
.scheme-card a {
    display: inline-block;
    margin-top: 10px;
    background: linear-gradient(135deg,#0073e6,#00b894);
    color: white !important;
    padding: 9px 16px;
    border-radius: 8px;
    text-decoration: none;
    font-size: 15px;
    font-weight: 600;
    transition: all 0.3s ease;
}
.scheme-card a:hover { 
    background: linear-gradient(135deg,#00b894,#0073e6); 
    transform: scale(1.05);
}

/* Buttons */
.fav-btn {
    background: #ffcc00;
    padding: 7px 15px;
    border-radius: 18px;
    font-size: 13px;
    cursor: pointer;
    color: black;
    font-weight: bold;
    border: none;
    margin-top: 8px;
}
.fav-btn:hover {
    background: #ffc107;
    transform: scale(1.05);
}

/* Favorites */
.fav-card {
    background: #fff8e1;
    border-left: 6px solid #ffcc00;
    padding: 10px 14px;
    border-radius: 10px;
    margin-bottom: 8px;
    font-weight: 500;
}
.hero .right-btn-container {
    position: absolute;
    top: 20px;
    right: 30px;
}
.hero {
    background: url("https://www.shutterstock.com/shutterstock/photos/2151597265/display_1500/stock-photo-sports-day-or-world-athletics-day-banner-athletics-players-and-sports-men-illustration-2151597265.jpg") no-repeat center center;
    background-size: cover;
    padding: 100px 25px;
    border-radius: 0px; /* full-width header look */
    color: white;
    text-align: center;
    margin-bottom: 40px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.25);
    position: relative;
    overflow: hidden;
}

/* 🔹 dark overlay for readability */
.hero::after {
    content: "";
    position: absolute;
    top: 0; left: 0;
    right: 0; bottom: 0;
    background: rgba(0, 0, 0, 0.55);
}



/* Footer */
.footer {
    background: linear-gradient(135deg,#0073e6,#00b894);
    color: white;
    text-align: center;
    padding: 50px 20px;
    border-radius: 12px;
    margin-top: 40px;
    font-weight: bold;
    font-size: 18px;
    transition: all 0.3s ease;
}
.footer a {
    color: white !important;
    margin: 0 12px;
    font-weight: 600;
    text-decoration: none;
    transition: all 0.3s ease;
}
.footer a:hover {
    color: #ffcc00 !important;
    transform: scale(1.1);
}
.social-icons img {
    width: 32px;
    height: 32px;
    margin: 0 6px;
    transition: all 0.3s ease;
}
.social-icons img:hover {
    transform: scale(1.2);
}
</style>
""", unsafe_allow_html=True)

# --- Hero Section ---
st.markdown("""
<div class="hero">
    <div class="hero-actions right-btn-container">
        <a href="https://your-financial-aid-app-url.streamlit.app" target="_blank" class="footer-link-btn">Financial Aid</a>
    </div>
    <div class="hero-content">
        <h1>🇮🇳 One Nation — One Athlete</h1>
        <p>Explore 20+ official government schemes for Athletes, Coaches & Institutions — from College to International levels.</p>
        <div class="hero-actions">
            <button class="footer-btn">🚀 Explore Schemes</button>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
st.markdown("""<style>
.footer-link-btn, .footer-btn {
    margin-top: 20px;
    background: linear-gradient(135deg,#0073e6,#00b894);
    color: white !important;
    padding: 12px 28px;
    border-radius: 30px;
    border: none;
    font-size: 1.1em;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.3s ease;
    z-index: 1;
    text-decoration: none;
    display: inline-block;
}
.footer-link-btn:hover, .footer-btn:hover {
    transform: scale(1.07);
    background: linear-gradient(135deg,#00b894,#0073e6); /* Optional: reverse gradient on hover */
    color: white !important;
}
""", unsafe_allow_html=True)           
# --- Schemes Dataset (20+) ---
schemes = [
    {
        "name": "College Sports Development Scheme",
        "category": "College",
        "description": "Provides infrastructure and funding for sports activities at college level.",
        "eligibility": "Open to students enrolled in recognized colleges.",
        "who_can_apply": "College students, sports coordinators.",
        "link": "https://yas.nic.in/",
        "image": "https://images.pexels.com/photos/3757375/pexels-photo-3757375.jpeg"
    },
    {
        "name": "University Sports Excellence Programme",
        "category": "University",
        "description": "Supports advanced training facilities and sports scholarships in universities.",
        "eligibility": "University students across India.",
        "who_can_apply": "Students, university sports departments.",
        "link": "https://www.education.gov.in/",
        "image": "https://images.pexels.com/photos/256369/pexels-photo-256369.jpeg"
    },
    # ... add more schemes here (20+) ...
]

# Extend to 8 schemes for demo
# --- Schemes Dataset (20+) ---
schemes = [
    {
        "name": "College Sports Development Scheme",
        "category": "College",
        "description": "Provides infrastructure and funding for sports activities at college level.",
        "eligibility": "Open to students enrolled in recognized colleges.",
        "who_can_apply": "College students, sports coordinators.",
        "link": "https://yas.nic.in/",
        "image": "https://images.pexels.com/photos/3757375/pexels-photo-3757375.jpeg"
    },
    {
        "name": "University Sports Excellence Programme",
        "category": "University",
        "description": "Supports advanced training facilities and sports scholarships in universities.",
        "eligibility": "University students across India.",
        "who_can_apply": "Students, university sports departments.",
        "link": "https://www.education.gov.in/",
        "image": "https://images.pexels.com/photos/256369/pexels-photo-256369.jpeg"
    },
    # ... add more schemes here (20+) ...
]

# A list of the 8 new image URLs you provided
new_images = [
    "https://encrypted-tbn1.gstatic.com/licensed-image?q=tbn:ANd9GcTo4oRzXK4VipcoKgWgtiTxKJBVXnO7dlRg3A9k6131Zt93VqEc79uolyqu06DJTsyDoM7XtcDHKSqsmyhtaaAnifob7GhkHw-eUxirznqW6dJnsdE",
    "https://encrypted-tbn3.gstatic.com/licensed-image?q=tbn:ANd9GcSbesmCLMaGHs25fsw-N_3WizhT3AI48J19SCwsjuBmi4G3Tgjn8tYhBYYP-7yyvMzD7ucKeHUmY_NHzvMAdvK7MzrCs1XVvpBUjG3z1-uLWxuPH2s",
    "https://encrypted-tbn3.gstatic.com/licensed-image?q=tbn:ANd9GcT5t2QOKTRTyJqkaBLroWUgEOcD7748A99wMqWxvpcJNLXjXKS9Ad0h7SsTL5KMnISIui4nbCQxG1AQQYEfedOAYNEnkCPwGCY_8dwX6k7xZv6rNCM",
    "https://encrypted-tbn0.gstatic.com/licensed-image?q=tbn:ANd9GcTHlXu3My8Q4mneGgZL9BnYyR3MbQgoFh4PHZLDzYESvkXqFWAGwT_azKxn_E6zJOxdP45UdlmeU2VVCM8MfGBfm8bqH_brsggjr_tBE2bdbhJ59U8",
    "https://encrypted-tbn1.gstatic.com/licensed-image?q=tbn:ANd9GcR241A8juutvBe8XJQOhByGFCk9YwziKli3JV409DwrVgtlhJk6ajCeopb1eQ4qSeu9clBymqg6KQZUkB59vXjToTJLm9SDMgCS5_8XhR8OieJZ5V4",
    "https://encrypted-tbn0.gstatic.com/licensed-image?q=tbn:ANd9GcQAUBZm6xNDZV-PbrixD_7ljED4XQNa647fcCubHf_cvQX--STx6M1UQnhl47p0eJgqc_X07Wg0Yle_ZduggbXmJu-bQY8Ne8-0mVRRrDyndWYk9kQ",
    "https://encrypted-tbn3.gstatic.com/licensed-image?q=tbn:ANd9GcRsiR_0qirbcKVODVl1-5XvF9CVMhcfAn0xn1tOQLkl5e3qAi0xPqUYTLg_DMpHNWaQugoHY7cUY2XzccUHW93cgGwPxehyfwdIgt8qD9cU0RWChS4",
    "https://encrypted-tbn1.gstatic.com/licensed-image?q=tbn:ANd9GcR0dBTKk4iJ97ET6GEL_XA46Lv829EAfCJqDFRu_2XJT9y-XOlC62qQ6V5ns5DfI8QLYha6JKt4EEEUQPZcJVn66hbAMLk6BcAtNQkuOUPg7-_TyjU"
]

# Extend to 8 schemes for demo, each with a different image
for i in range(8):
    schemes.append({
        "name": f"Special Sports Initiative {i+1}",
        "category": ["College", "University", "District", "State", "National", "International"][i % 6],
        "description": "Government initiative to boost athlete participation and development.",
        "eligibility": "Eligible athletes based on category.",
        "who_can_apply": "Students, athletes, federations.",
        "link": "https://yas.nic.in/",
        "image": new_images[i]  # Use the new image list
    })

categories = ["All", "College", "University", "District", "State", "National", "International"]
categories = ["All", "College", "University", "District", "State", "National", "International"]

# --- Filters ---
with st.container():
    st.markdown('<div class="filters">', unsafe_allow_html=True)
    selected_category = st.selectbox("📍 Filter by Category", categories)
    st.markdown('</div>', unsafe_allow_html=True)

# --- Filter Schemes ---
filtered_schemes = [s for s in schemes if selected_category == "All" or s["category"] == selected_category]

# --- Display Schemes in Multiple Columns ---
num_cols = 2  # You can change to 3 for wider display
num_rows = math.ceil(len(filtered_schemes)/num_cols)

for row in range(num_rows):
    cols = st.columns(num_cols)
    for col_idx in range(num_cols):
        idx = row*num_cols + col_idx
        if idx < len(filtered_schemes):
            scheme = filtered_schemes[idx]
            with cols[col_idx]:
                st.markdown(f"""
                <div class="scheme-card">
                    <img src="{scheme['image']}" alt="{scheme['name']}"/>
                    <h3>{scheme['name']}</h3>
                    <p class="meta"><b>Category:</b> {scheme['category']}</p>
                    <p>{scheme['description']}</p>
                    <p><b>Eligibility:</b> {scheme['eligibility']}</p>
                    <p><b>Who Can Apply:</b> {scheme['who_can_apply']}</p>
                    <a href="{scheme['link']}" target="_blank">🔗 Apply / Register</a>
                </div>
                """, unsafe_allow_html=True)

                # Interactive features
                if st.button("⭐ Add to Favorites", key=f"fav-{scheme['name']}"):
                    if scheme["name"] not in st.session_state.favorites:
                        st.session_state.favorites.append(scheme["name"])
                        st.success(f"Added {scheme['name']} to Favorites!")

                comment = st.text_input(f"💬 Comment on {scheme['name']}", key=f"cmt-{scheme['name']}")
                if st.button(f"Post Comment - {scheme['name']}", key=f"post-{scheme['name']}"):
                    if comment:
                        st.session_state.comments.append((scheme["name"], comment))
                        st.info(f"Comment added for {scheme['name']}!")

# --- Favorites Section ---
if st.session_state.favorites:
    st.subheader("⭐ Your Favorites")
    for fav in st.session_state.favorites:
        st.markdown(f"<div class='fav-card'>{fav}</div>", unsafe_allow_html=True)

# --- Comments Section ---
if st.session_state.comments:
    st.subheader("💬 User Comments")
    for scheme_name, cmt in st.session_state.comments:
        st.write(f"**{scheme_name}:** {cmt}")

# --- Footer ---
st.markdown("""
<style>
.footer {
    background: linear-gradient(135deg,#0073e6,#00b894);
    color: white;
    text-align: center;
    padding: 50px 20px;
    border-radius: 12px;
    margin-top: 40px;
    font-weight: bold;
    font-size: 18px;
    transition: all 0.3s ease;
}
.footer a {
    color: white !important;
    margin: 0 12px;
    font-weight: 600;
    text-decoration: none;
    transition: all 0.3s ease;
}
.footer a:hover {
    color: #ffcc00 !important;
    transform: scale(1.1);
}
.social-icons img {
    width: 32px;
    height: 32px;
    margin: 0 6px;
    transition: all 0.3s ease;
}
.social-icons img:hover {
    transform: scale(1.2);
}
</style>

<div class="footer">
    <h2>One Nation One Athlete 🇮🇳</h2>
    <p>Championing Fairness, Access, and Opportunity in Indian Sports</p>
    <div>
        <a href="#">Home</a> |
        <a href="#">Schemes</a> |
        <a href="#">About</a> |
        <a href="#">Contact</a>
    </div>
    <p style="margin-top:15px;">&copy; 2025 One Nation One Athlete | Government of India | All Rights Reserved</p>
</div>
""", unsafe_allow_html=True)