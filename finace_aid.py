import streamlit as st
import pandas as pd
import numpy as np
import io
from datetime import datetime
import random
from PIL import Image
import requests
import base64

# --------------------------
# One Nation, One Athlete
# Financial Aid module (Streamlit single-file app)
# --------------------------

st.set_page_config(page_title="One Nation, One Athlete — Financial Aid", layout="wide", page_icon="🏆")

# ----- CUSTOM STYLES -----

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap');
    html, body, [class*="st-"] {
        font-family: 'Montserrat', sans-serif;
    }
    .main-header {
        background: linear-gradient(90deg, #1A202C, #2C5282);
        padding: 25px;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        margin-bottom: 25px;
    }
    .main-header h1 {
        font-size: 2.8em;
        margin-bottom: 5px;
        font-weight: 700;
    }
    .main-header .muted {
        font-size: 1.1em;
        opacity: 0.9;
    }
    .card {
        background: linear-gradient(180deg, #ffffff, #f0f4f8);
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 8px 25px rgba(2,6,23,0.1);
        margin-bottom: 20px;
        border: 1px solid #e0e7ff;
    }

    /* Default button styles */
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        padding: 10px 20px;
        border-radius: 10px;
        border: 2px solid #388E3C;
        font-weight: 600;
        transition: all 0.2s ease-in-out;
        box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
    }
    .stButton>button:hover {
        background-color: #388E3C;
        box-shadow: 0 6px 20px rgba(76, 175, 80, 0.4);
        transform: translateY(-2px);
    }

    /* 🚀 Submit My Application */
    .stButton button:has(span:contains("🚀 Submit My Application")) {
        background-color: #FF5722 !important;
        border: 2px solid #E64A19 !important;
        color: white !important;
        border-radius: 12px;
        font-weight: 600;
        padding: 10px 22px;
        box-shadow: 0 4px 15px rgba(255, 87, 34, 0.3);
    }
    .stButton button:has(span:contains("🚀 Submit My Application")):hover {
        background-color: #E64A19 !important;
        box-shadow: 0 6px 20px rgba(255, 87, 34, 0.4);
        transform: translateY(-2px);
    }

    /* 🌐 View All Programs (Demo) */
    .stButton button:has(span:contains("View All Programs (Demo)")) {
        background-color: #3F51B5 !important;
        border: 2px solid #303F9F !important;
        color: white !important;
        border-radius: 12px;
        font-weight: 600;
        padding: 10px 22px;
        box-shadow: 0 4px 15px rgba(63, 81, 181, 0.3);
    }
    .stButton button:has(span:contains("View All Programs (Demo)")):hover {
        background-color: #303F9F !important;
        box-shadow: 0 6px 20px rgba(63, 81, 181, 0.4);
        transform: translateY(-2px);
    }

    /* Existing admin action button styles */
    .stButton[data-testid*="short_"] > button {
        background-color: #2196F3;
        border: 2px solid #1976D2;
        box-shadow: 0 4px 15px rgba(33, 150, 243, 0.3);
    }
    .stButton[data-testid*="short_"] > button:hover {
        background-color: #1976D2;
        box-shadow: 0 6px 20px rgba(33, 150, 243, 0.4);
    }
    .stButton[data-testid*="disp_"] > button {
        background-color: #FFC107;
        border: 2px solid #FFA000;
        color: #333;
        box-shadow: 0 4px 15px rgba(255, 193, 7, 0.3);
    }
    .stButton[data-testid*="disp_"] > button:hover {
        background-color: #FFA000;
        box-shadow: 0 6px 20px rgba(255, 193, 7, 0.4);
    }
    .stButton[data-testid*="rej_"] > button {
        background-color: #F44336;
        border: 2px solid #D32F2F;
        box-shadow: 0 4px 15px rgba(244, 67, 54, 0.3);
    }
    .stButton[data-testid*="rej_"] > button:hover {
        background-color: #D32F2F;
        box-shadow: 0 6px 20px rgba(244, 67, 54, 0.4);
    }
    .stButton[data-testid*="crowdfund_"] > button {
        background-color: #9C27B0;
        border: 2px solid #7B1FA2;
        box-shadow: 0 4px 15px rgba(156, 39, 176, 0.3);
    }
    .stButton[data-testid*="crowdfund_"] > button:hover {
        background-color: #7B1FA2;
        box-shadow: 0 6px 20px rgba(156, 39, 176, 0.4);
    }
    .donor-btn button {
        background-color: #FF5722;
        border: 2px solid #E64A19;
        color: white;
        font-weight: 600;
        border-radius: 10px;
        padding: 10px 20px;
        box-shadow: 0 4px 15px rgba(255, 87, 34, 0.3);
    }
    .donor-btn button:hover {
        background-color: #E64A19;
        box-shadow: 0 6px 20px rgba(255, 87, 34, 0.4);
        transform: translateY(-2px);
    }

    .pill {
        display: inline-block;
        padding: 8px 15px;
        border-radius: 999px;
        background: #e0e7ff;
        color: #3f51b5;
        margin-right: 10px;
        margin-bottom: 8px;
        font-weight: 600;
        font-size: 0.9em;
    }
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size:1.1em;
        font-weight: 600;
    }
    h2, h3, h4 {
        color: #1A202C;
        font-weight: 700;
    }
    .stProgress > div > div > div > div {
        background-color: #2C5282;
    }
    </style>
    """, unsafe_allow_html=True
)

# ----- Helper utilities -----

def load_image_from_url(url):
    try:
        resp = requests.get(url, timeout=8)
        return Image.open(io.BytesIO(resp.content))
    except Exception:
        return None

def generate_reference_id(prefix="AID"):
    return f"{prefix}-{random.randint(10000,99999)}"

def to_bytes_io_pdf(info):
    buffer = io.BytesIO()
    text = "One Nation One Athlete - Financial Aid Summary\n\n"
    for k, v in info.items():
        text += f"{k}: {v}\n"
    buffer.write(text.encode('utf-8'))
    buffer.seek(0)
    return buffer

# ----- Top section -----
with st.container():
    col1, col2 = st.columns([3,1])
    with col1:
        st.markdown('<div class="main-header">', unsafe_allow_html=True)
        st.markdown("<h1>One Nation, One Athlete</h1>")
        st.markdown("<h3>Financial Aid Portal <br> <span class='muted'>Empowering India's sporting talent</span></h3>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        hero_url = "https://images.unsplash.com/photo-1526403224743-8f3f0e1f6e88?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=60" # Athlete with medal
        img = load_image_from_url(hero_url)
        if img:
            st.image(img, use_column_width=True, caption="Championing athletes across India")
        else:
            st.image("https://via.placeholder.com/800x600/2C5282/FFFFFF?text=Athlete+Hero", use_column_width=True, caption="Championing athletes across India")


st.markdown("---")

# ----- Two-column layout: Application form + Dashboard -----
left, right = st.columns([2,3])

# ---- LEFT: Unified Application Form (multi-step in one page) ----
with left:
    st.markdown("## ✍️ Apply for Support")
    st.info("Fill out this simple form to get matched with eligible scholarships and grants. Every field helps us understand your needs better!")
    with st.form('aid_application', clear_on_submit=False): # Keep form data after submission
        st.markdown("#### 👤 Athlete Profile")
        colA, colB = st.columns(2)
        with colA:
            full_name = st.text_input("Full Name", "", placeholder="e.g., Priya Sharma")
            dob = st.date_input("Date of Birth", datetime(2005,1,1))
            sport = st.text_input("Primary Sport", "Athletics", placeholder="e.g., Badminton, Wrestling")
        with colB:
            gender = st.selectbox("Gender", ["Male","Female","Other"], index=1) # Default to female for diversity
            location = st.text_input("Your Location (Village/Town, District, State)", "", placeholder="e.g., Kolar, Kolar, Karnataka")
            mobile = st.text_input("Mobile Number (for verification)", "", placeholder="+91-XXXXXXXXXX")

        st.markdown("---")
        st.markdown("#### 🏡 Socio-economic & Eligibility")
        income_bracket = st.selectbox("Annual Household Income", ["< ₹1 Lakh","₹1-3 Lakh","₹3-6 Lakh","> ₹6 Lakh"])
        is_poc = st.checkbox("Belong to a marginalized community / reserved category?", help="This helps us prioritize and match you with specific inclusive programs.")
        has_disability = st.selectbox("Disability Status", ["No","Yes - minor (e.g., vision impairment)","Yes - major (e.g., mobility impairment)"])

        st.markdown("---")
        st.markdown("#### 📜 Performance & Need (Upload Documents)")
        st.warning("Please upload clear scans of your documents to expedite the verification process.")
        perf_doc = st.file_uploader("Upload Performance Certificate / Scorecard (PDF / image)", type=["pdf","png","jpg","jpeg"], help="Proof of your sporting achievements.")
        income_doc = st.file_uploader("Upload Income Certificate (optional but recommended)", type=["pdf","png","jpg","jpeg"], help="Helps verify your financial need.")
        medical_doc = st.file_uploader("Upload Medical / Disability Certificate (if applicable)", type=["pdf","png","jpg","jpeg"], help="Required for injury, rehab, or disability-specific grants.")

        st.markdown("---")
        st.markdown("#### 🎯 Requested Support")
        support_types = st.multiselect(
            "What types of aid do you need most?",
            ["Stipend / Living allowance", "Training/coaching fees", "Equipment/gear", "Travel to competitions", "Medical/rehab", "Education grant", "Nutrition support"],
            default=["Stipend / Living allowance", "Training/coaching fees"]
        )
        amount_required = st.number_input("Estimated Amount Required (₹)", min_value=0, step=1000, value=25000, help="Provide an estimate for the support you need.")

        st.markdown("---")
        st.markdown("#### ✅ Consent & Declaration")
        consent = st.checkbox("I solemnly declare that the information provided above is true and accurate to the best of my knowledge, and I consent to necessary verification checks by the 'One Nation, One Athlete' team.", value=False)

        st.markdown("<br>", unsafe_allow_html=True) # Add some space before the button
        submit_btn = st.form_submit_button("🚀 Submit My Application")

    if submit_btn:
        if not full_name or not mobile or not perf_doc:
            st.error("🚨 Please fill in your **Full Name**, **Mobile Number**, and upload a **Performance Document** to submit your application.")
        elif not consent:
            st.warning("⚠️ Please check the consent box to proceed with your application.")
        else:
            app_id = generate_reference_id("AID")
            if 'applications' not in st.session_state:
                st.session_state['applications'] = {}
            st.session_state['applications'][app_id] = {
                'name': full_name,
                'dob': str(dob),
                'sport': sport,
                'location': location,
                'mobile': mobile,
                'income_bracket': income_bracket,
                'is_poc': bool(is_poc),
                'has_disability': has_disability,
                'support_types': ", ".join(support_types), # Store as string for display
                'amount_required': amount_required,
                'status': 'Submitted',
                'submitted_at': str(datetime.now().strftime("%Y-%m-%d %H:%M")) # Nicer format
            }
            st.success(f"🎉 **Application Submitted Successfully!** Your Reference ID: **{app_id}**. You can track its status in the Athlete Dashboard.")
            st.balloons() # Visual celebration!

    st.markdown("<br><br>")
    st.markdown("<div class='card'>\n💪 **Pro-Tip:** Make sure your uploaded documents are clear and readable. A strong application with proper documentation increases your chances of faster approval!\n</div>", unsafe_allow_html=True)

# ---- RIGHT: Admin / Athlete Dashboard & Matching ----
with right:
    st.markdown("## 📊 Athlete Dashboard & Ecosystem Overview")
    st.markdown("Track your applications, discover eligible programs, and see the impact of our collective efforts.")

    st.markdown("### Key Metrics")
    # top KPI boxes
    col1, col2, col3 = st.columns(3)
    total_apps = len(st.session_state.get('applications', {}))
    total_disbursed_amount = sum([a.get('amount_required',0) for a in st.session_state.get('applications',{}).values() if a.get('status')=='Disbursed'])
    pending_approvals = len([1 for a in st.session_state.get('applications',{}).values() if a.get('status')=='Submitted' or a.get('status')=='Shortlisted'])
    col1.metric("Total Applications", total_apps, help="Number of applications received.")
    col2.metric("Pending Action", pending_approvals, help="Applications awaiting review or approval.")
    col3.metric("Funds Disbursed (Demo)", f'₹{int(total_disbursed_amount):,}', help="Total estimated funds successfully provided to athletes.")

    st.markdown("---")
    st.markdown("### 🔍 Auto-Match: Discover Your Programs")

    # Simple mock programs dataset
    programs = [
        {"id":"PRG-001","name":"Khelo India Talent Grant","min_income":"< ₹3 Lakh","sport_supported":"All","tier":"State","description":"Supports promising athletes at the state level with training and equipment."},
        {"id":"PRG-002","name":"Grassroots Equipment Subsidy","min_income":"< ₹6 Lakh","sport_supported":"All","tier":"District","description":"Provides essential equipment to athletes from rural and low-income backgrounds."},
        {"id":"PRG-003","name":"Rehab & Recovery Fund","min_income":"Any","sport_supported":"All","tier":"National","description":"Financial assistance for injury treatment and rehabilitation for elite and developing athletes."},
        {"id":"PRG-004","name":"CSR Coaching Scholarship (Private)","min_income":"< ₹1 Lakh","sport_supported":"All","tier":"Private","description":"Corporate-sponsored scholarship covering high-quality coaching fees for underprivileged athletes."},
        {"id":"PRG-005","name":"Para-Athlete Empowerment Grant","min_income":"Any","sport_supported":"All","tier":"National","description":"Dedicated support for athletes with disabilities, covering adaptive equipment and specialized coaching."}
    ]

    st.caption("Select one of your submitted applications to see which financial aid programs you might be eligible for based on your profile.")
    
    # Ensure applications are sorted by latest first for better UX
    sorted_apps_keys = sorted(st.session_state.get('applications',{}).keys(), key=lambda x: st.session_state['applications'][x]['submitted_at'], reverse=True)
    sel_app = st.selectbox("Choose an Application to Match", options=["-- Select an application --"] + sorted_apps_keys, help="Your recently submitted applications will appear here.")
    
    if sel_app and sel_app != "-- Select an application --":
        app = st.session_state['applications'][sel_app]
        st.markdown(f"**Applicant:** {app['name']} (ID: {sel_app})  —  **Sport:** {app['sport']}  —  **Income:** {app['income_bracket']}  —  **Status:** <span class='pill' style='background:#f0f9ff; color:#2563eb;'>{app['status']}</span>", unsafe_allow_html=True)
        
        # Naive matching logic
        matches = []
        for p in programs:
            is_matched = False
            # Income matching
            if app['income_bracket'] == '< ₹1 Lakh' and p['min_income'] in ['< ₹1 Lakh','< ₹3 Lakh','< ₹6 Lakh','Any']:
                is_matched = True
            elif app['income_bracket'] == '₹1-3 Lakh' and p['min_income'] in ['< ₹3 Lakh','< ₹6 Lakh','Any']:
                is_matched = True
            elif app['income_bracket'] == '₹3-6 Lakh' and p['min_income'] in ['< ₹6 Lakh','Any']:
                is_matched = True
            elif app['income_bracket'] == '> ₹6 Lakh' and p['min_income'] == 'Any':
                is_matched = True
            elif p['min_income']=='Any': # Covers all incomes if program doesn't specify
                is_matched = True
            
            # Disability specific program matching
            if 'Para-Athlete Empowerment Grant' in p['name'] and app['has_disability'] == 'No':
                is_matched = False # Exclude if not disabled

            if is_matched:
                matches.append(p)

        st.markdown("#### ✨ Matched Programs for You:")
        if matches:
            for m in matches:
                with st.expander(f"**{m['name']}** - Tier: {m['tier']}"):
                    st.write(f"**Program ID:** {m['id']}")
                    st.write(f"**Eligibility:** Annual income {m['min_income']} or less. Supports {m['sport_supported']} sports.")
                    st.write(f"**Description:** {m['description']}")
                    st.button(f"Apply for {m['name']} (simulated)", key=f"apply_{m['id']}_{sel_app}")
        else:
            st.info("No specific programs matched based on your current profile. We're continuously adding more!")

        st.markdown("---")
        st.markdown("#### ⚙️ Application Actions (Admin / Athlete View)")
        st.caption("As an administrator, you can manage the application status here. Athletes can see their status updates.")
        
        current_status = app['status']
        st.markdown(f"**Current Status:** <span class='pill' style='background:#e0f7fa; color:#00796b;'>{current_status}</span>", unsafe_allow_html=True)

        colA_act, colB_act, colC_act = st.columns(3)
        with colA_act:
            if st.button("👁️‍🗨️ Shortlist", key=f"short_{sel_app}", help="Mark application for further review and verification."):
                st.session_state['applications'][sel_app]['status'] = 'Shortlisted'
                st.success(f"Application {sel_app} has been **shortlisted**.")
                st.experimental_rerun() # Rerun to update status pill
        with colB_act:
            if st.button("✅ Approve & Disburse", key=f"disp_{sel_app}", help="Approve the application and simulate fund disbursement."):
                st.session_state['applications'][sel_app]['status'] = 'Disbursed'
                st.success(f"Application {sel_app} **approved** and funds marked as **disbursed** (demo).")
                st.balloons()
                st.experimental_rerun() # Rerun to update status pill
        with colC_act:
            if st.button("❌ Reject", key=f"rej_{sel_app}", help="Reject the application. Consider providing a reason in a real system."):
                st.session_state['applications'][sel_app]['status'] = 'Rejected'
                st.warning(f"Application {sel_app} has been **rejected**.")
                st.experimental_rerun() # Rerun to update status pill
    else:
        st.info("Select an application from the dropdown above to manage it or see program matches.")

    st.markdown("---")
    st.markdown("### 🤝 Community & Fundraising")
    st.caption("Help us empower more athletes or start a campaign for someone you know!")
    col1_fund, col2_fund = st.columns([2,1])
    with col1_fund:
        st.markdown("**Empower an Athlete with Crowdfunding**")
        st.write("Create a dedicated campaign page for an athlete to gather support from individuals and communities.")
        if st.button("✨ Start New Crowdfund (Demo)", key="crowdfund_btn"):
            st.success("Your crowdfunding page is live (demo)! Share this link: `https://onenationoneathlete.org/crowdfund/{unique_id}`")
    with col2_fund:
        st.markdown("<div class='donor-btn'>", unsafe_allow_html=True)
        if st.button("💖 Quick Donate Now", key="donate_btn"):
            st.balloons()
            st.success("Thank you for your generous contribution to India's athletes! Every Rupee counts. 🙏")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📜 All Applications (Transparency Log)")
    if st.session_state.get('applications'):
        df = pd.DataFrame.from_dict(st.session_state['applications'], orient='index')
        df.index.name = "Application ID" # Add index name
        st.dataframe(df[['name','sport','location','amount_required','status','submitted_at','support_types']].fillna("-"), use_container_width=True)
    else:
        st.info("No applications submitted yet. Be the first to apply!")

# ----- Bottom: Resources, Financial Literacy & Visuals -----
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("## 📚 Resources for Athletes & Organizations")
st.markdown("Beyond financial aid, we provide tools and information to foster holistic growth.")

res1, res2, res3 = st.columns(3)
with res1:
    st.markdown("### 💡 How Our Platform Works")
    st.markdown("""
    1.  **Apply Easily:** Submit your profile and documents through our unified portal.
    2.  **Smart Matching:** Our system intelligently connects you with eligible programs.
    3.  **Transparent Verification:** Applications are reviewed by our dedicated committee.
    4.  **Direct Disbursement:** Funds are securely transferred to your linked account or digital wallet.
    """)
with res2:
    st.markdown("### 🌟 Explore Support Programs")
    st.markdown("""
    *   **Government Schemes:** Direct access to national and state-level sports scholarships.
    *   **CSR & Philanthropy:** Partnered programs from leading corporations and foundations.
    *   **Specialized Grants:** Dedicated funds for injury recovery, equipment, and education.
    *   **Coaching & Training:** Subsidies for high-performance training camps and expert coaching.
    """)
    st.button("View All Programs (Demo)", help="Explore the full list of available financial aid and support programs.", key="view_programs_btn")
with res3:
    st.markdown("### 💰 Financial Literacy for Athletes")
    st.markdown("""
    We believe in empowering athletes beyond the field. Our resources help you manage your finances wisely.
    *   **Budgeting Guides:** Simple templates to track your expenses and savings.
    *   **Investment Basics:** Learn about future planning and securing your financial future.
    *   **Career Transition:** Guidance for life after sports, including skill development.
    """)
    if st.button("Access Financial Guides", key="financial_guides_btn"):
        st.success("Opening a sample financial literacy guide (demo)! Learn to manage your earnings like a pro.")

# ----- Visuals / imagery used (credits) -----
st.markdown("---")
st.markdown("<div class='muted' style='text-align:center; font-size:0.8em;'>Images used in this demo are from Unsplash and public resources — these are illustrative only. For production, ensure proper licensing or use platform-owned assets.</div>", unsafe_allow_html=True)

# ----- Footer -----
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<div style='text-align:center; margin-top:18px; padding:15px; background-color:#f8f9fa; border-top:1px solid #e0e0e0; border-radius:10px;'>Made with ❤️ for <strong>One Nation, One Athlete</strong> — Championing Fairness, Access, and Opportunity in Indian Sports.</div>", unsafe_allow_html=True)