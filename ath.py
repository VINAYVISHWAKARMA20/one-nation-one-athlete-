

import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import cv2
import tempfile
import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
import base64

# ---------------------- Config ----------------------
st.set_page_config(page_title="One Nation, One Athlete", layout="wide")

def get_base64_of_bin_file(bin_file):
    with open(bin_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# --- Placeholder for your background image ---
# OPTION 1: Use a publicly accessible image URL
# I have added an example of a high-quality sports image.
# You can replace this URL with your own.
bg_url = "https://www.shutterstock.com/image-photo/sports-woman-running-over-red-background-788274100"
bg_css = f'background-image: url("{bg_url}");'

# For demonstration, we will use a simple, clean look until you provide an image.
bg_css = f"""
    background-image: url("{bg_url}");
    background-size: cover;
    background-attachment: fixed;
    background-position: center;
"""

# ---------------------- Theme Styling ----------------------
st.markdown(
    f"""
    <style>
    .stApp {{
        {bg_css}
    }}
    
    /* General text and header styles */
    h1, h2, h3, h4, .st-emotion-cache-10trblm {{
        color: #1e3a8a; 
        text-align: center;
        font-weight: 900;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.5); /* Stronger shadow for better visibility on a busy background */
    }}
    
    /* Container styling for a professional "card" look */
    .st-emotion-cache-1c7v06k {{
        border-radius: 15px; 
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2); /* Stronger shadow for depth */
        padding: 25px; 
        background-color: rgba(255, 255, 255, 0.95); /* More opaque for better text contrast */
        border: 2px solid #1e3a8a;
    }}
    
    /* Input field borders and focus states */
    .stTextInput>div>div>input, .stNumberInput>div>div>input, .stSelectbox>div>div, .stRadio>div>div {{
        border: 2px solid #ccc; /* A clean, universal border */
        border-radius: 8px;
        padding: 10px;
        font-size: 16px;
        transition: border-color 0.3s ease-in-out;
    }}
    .stTextInput>div>div>input:focus, .stNumberInput>div>div>input:focus {{
        border-color: #1e3a8a; /* Accent color on focus */
        outline: none;
        box-shadow: 0 0 0 2px rgba(30, 58, 138, 0.2);
    }}

    /* Button styles */
    .stButton>button {{
        background: linear-gradient(135deg, #1e3a8a 0%, #10b981 100%);
        color: white; 
        border-radius: 12px; 
        padding: 0.6rem 1.8rem; 
        border: 2px solid white;
        font-weight: bold;
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease-in-out;
    }}
    .stButton>button:hover {{
        background: linear-gradient(135deg, #10b981 0%, #1e3a8a 100%);
        transform: scale(1.05);
        border: 2px solid #f0fdf4;
    }}

    /* Tabs styling */
    .stTabs [role="tab"] {{
        background: #e0f2fe; 
        border-radius: 10px; 
        padding: 10px;
        color: #1e3a8a; 
        font-weight: bold; 
        border: 1px solid #cceeff;
        transition: background 0.2s ease;
    }}
    .stTabs [role="tab"]:hover {{
        background: #d4eafc;
    }}
    .stTabs [aria-selected="true"] {{
        background: #1e3a8a; 
        color: white; 
        border: 1px solid #1e3a8a;
        font-weight: bold;
    }}
    
    /* Achievement card styling */
    .achievement-card {{
        border-radius: 15px;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
        padding: 20px;
        margin-bottom: 20px;
        background: rgba(255,255,255,0.95); /* Opaque background for text clarity */
        border: 2px solid #10b981;
    }}
    
    /* Metric box styling for results */
    .metric-box {{
        background-color: rgba(224,242,254,0.95);
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 15px;
        border-left: 6px solid #1e3a8a;
        font-weight: bold;
    }}

    /* General text improvements for better contrast */
    p, .st-emotion-cache-10trblm p, .st-emotion-cache-18ni7ap, .st-emotion-cache-1c7v06k p {{
        color: #333333; /* Darker text color */
        font-weight: 500;
    }}

    /* Footer styling */
    .footer {{
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: rgba(240, 253, 244, 0.9); /* More opaque background for text */
        color: #555;
        text-align: center;
        padding: 10px;
        font-size: small;
        border-top: 1px solid #e0e0e0;
    }}
    
    /* Table borders */
    .dataframe th, .dataframe td {{
        border: 1px solid #ccc !important;
    }}
    
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------- Session State Init ----------------------
for key in ['logged_in', 'username', 'athlete_profile', 'achievements',
            'image_metrics', 'video_metrics', 'signup_mode']:
    if key not in st.session_state:
        st.session_state[key] = None

# ---------------------- Mediapipe Import ----------------------
try:
    import mediapipe as mp
    MP_AVAILABLE = True
    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils
except Exception:
    MP_AVAILABLE = False

# ---------------------- Helpers ----------------------
def calculate_angle(a, b, c):
    a, b, c = np.array(a), np.array(b), np.array(c)
    ba, bc = a - b, c - b
    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc) + 1e-8)
    angle = np.degrees(np.arccos(np.clip(cosine_angle, -1.0, 1.0)))
    return angle

def get_landmark_coords(landmarks, w, h, idx):
    lm = landmarks.landmark[idx]
    return (lm.x * w, lm.y * h)

def recommendations_from_metrics(metrics, reps=None):
    recs = []
    if "posture_score" in metrics:
        if metrics["posture_score"] > 90:
            recs.append("✅ Excellent posture maintained.")
        elif metrics["posture_score"] > 75:
            recs.append("⚠️ Slight imbalance detected.")
        else:
            recs.append("❌ Needs improvement in posture.")
    if reps is not None:
        if reps < 5:
            recs.append("💪 Increase your repetitions gradually.")
        else:
            recs.append("🔥 Great endurance!")

    while len(recs) < 5:
        recs.append("📌 Keep practicing regularly to improve consistency.")

    return recs

# ---------------------- Pose Analysis ----------------------
def analyze_image_pose(image: np.ndarray):
    h, w, _ = image.shape
    metrics = {}
    with mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5) as pose:
        results = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        annotated = image.copy()
        if not results.pose_landmarks:
            metrics['error'] = 'No pose detected'
            return {'annotated_image': annotated, 'metrics': metrics}

        mp_drawing.draw_landmarks(annotated, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        lm = results.pose_landmarks

        left_knee = calculate_angle(get_landmark_coords(lm, w, h, 23),
                                     get_landmark_coords(lm, w, h, 25),
                                     get_landmark_coords(lm, w, h, 27))
        right_knee = calculate_angle(get_landmark_coords(lm, w, h, 24),
                                      get_landmark_coords(lm, w, h, 26),
                                      get_landmark_coords(lm, w, h, 28))

        metrics['left_knee_deg'] = round(left_knee, 1)
        metrics['right_knee_deg'] = round(right_knee, 1)
        metrics['posture_score'] = round(100 - min(20, abs(left_knee - right_knee)), 1)

        return {'annotated_image': annotated, 'metrics': metrics}

def analyze_video_reps(video_path, exercise='squat'):
    if not MP_AVAILABLE:
        return {'error': 'mediapipe not available'}
    rep_count, prev_state = 0, None
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        cap = cv2.VideoCapture(video_path)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret: break
            h, w, _ = frame.shape
            results = pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            if not results.pose_landmarks: continue
            lm = results.pose_landmarks

            if exercise == 'squat':
                knee_angle = calculate_angle(get_landmark_coords(lm, w, h, 23),
                                             get_landmark_coords(lm, w, h, 25),
                                             get_landmark_coords(lm, w, h, 27))
                state = 'down' if knee_angle < 100 else 'up'
            else:
                elbow_angle = calculate_angle(get_landmark_coords(lm, w, h, 11),
                                              get_landmark_coords(lm, w, h, 13),
                                              get_landmark_coords(lm, w, h, 15))
                state = 'down' if elbow_angle < 100 else 'up'

            if prev_state == 'down' and state == 'up':
                rep_count += 1
            prev_state = state
        cap.release()
    return {'rep_count': rep_count}

# ---------------------- PDF Generator ----------------------
def generate_pdf(filename, profile, achievements, metrics):
    doc = SimpleDocTemplate(filename, pagesize=A4)
    styles = getSampleStyleSheet()
    content = []

    content.append(Paragraph("One Nation, One Athlete - Registration Summary", styles['Title']))
    content.append(Spacer(1, 20))

    # Add Profile
    content.append(Paragraph("<b>Athlete Profile</b>", styles['Heading2']))
    if profile:
        profile_data = [[k, v] for k, v in profile.items()]
        profile_table = Table(profile_data, colWidths=[200, 300])
        profile_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgreen),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BOX', (0, 0), (-1, -1), 1, colors.black)
        ]))
        content.append(profile_table)
    else:
        content.append(Paragraph("No registration found.", styles['Normal']))
    content.append(Spacer(1, 10))

    # Add Achievements
    content.append(Paragraph("<b>Achievements</b>", styles['Heading2']))
    if achievements:
        for ach in achievements:
            content.append(Paragraph(f"- {ach['description']}", styles['Normal']))
            if ach["image"]:
                temp_img = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
                temp_img.write(ach["image"])
                temp_img.close()
                img = RLImage(temp_img.name, width=200, height=150)
                content.append(img)
                os.remove(temp_img.name)
            content.append(Spacer(1, 5))
    else:
        content.append(Paragraph("No achievements recorded.", styles['Normal']))
    content.append(Spacer(1, 10))

    # Add Fitness Metrics
    content.append(Paragraph("<b>Fitness Test Results</b>", styles['Heading2']))
    if metrics:
        metrics_data = [[k, v] for k, v in metrics.items()]
        metrics_table = Table(metrics_data, colWidths=[200, 300])
        metrics_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BOX', (0, 0), (-1, -1), 1, colors.black)
        ]))
        content.append(metrics_table)
    else:
        content.append(Paragraph("No fitness test results found.", styles['Normal']))
    content.append(Spacer(1, 40))
    content.append(Paragraph("<br/>---- End of Report ----", styles['Italic']))
    doc.build(content)

# ---------------------- Login Page ----------------------
if not st.session_state['logged_in']:
    st.image("https://upload.wikimedia.org/wikipedia/en/thumb/9/90/Indian_Olympic_Association_logo.svg/1200px-Indian_Olympic_Association_logo.svg.png", width=150)
    st.title("🔑 Athlete Login")
    st.markdown("### Please log in to access the portal.")
    
    # Center the login form using columns
    col_empty1, col_form, col_empty2 = st.columns([1, 2, 1])
    with col_form:
        st.subheader("Welcome Back!")
        user = st.text_input("Username", placeholder="Enter your username")
        pwd = st.text_input("Password", type="password", placeholder="Enter your password")

        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Login"):
                if user.strip() and pwd.strip():
                    st.session_state['logged_in'] = True
                    st.session_state['username'] = user
                    st.session_state['signup_mode'] = False
                    st.success(f"Welcome back, {user}! Redirecting to dashboard...")
                    st.rerun()
                else:
                    st.error("Please enter valid credentials.")
        with col2:
            st.button("Forgot Password?")
        with col3:
            if st.button("Sign Up"):
                st.session_state['logged_in'] = True
                st.session_state['username'] = user if user else "NewUser"
                st.session_state['signup_mode'] = True
                st.success("Sign-up started. Please complete registration process.")
                st.rerun()
    st.stop()

# ---------------------- Main App ----------------------
st.title("One Nation, One Athlete Portal")
st.markdown(f"### Welcome, **{st.session_state['username']}** 👋")

if st.session_state['signup_mode']:
    tabs = st.tabs(["Registration Form", "Achievements", "Fitness Test", "Dashboard"])
else:
    tabs = st.tabs(["Dashboard"])

# ---------------------- Registration ----------------------
if st.session_state['signup_mode']:
    with tabs[0]:
        st.header("📝 Athlete Registration Form")
        st.markdown("Please fill out your details to get started.")
        
        # Use columns for a more compact form layout
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name")
            age = st.number_input("Age", min_value=10, max_value=100)
            state = st.text_input("State")
            background = st.radio("Background", ["Urban", "Rural"])
            sport = st.text_input("Primary Sport")
        with col2:
            sex = st.selectbox("Gender", ["Male", "Female", "Other"])
            city = st.text_input("City")
            disability = st.selectbox("Disability Status", ["None", "Physical", "Visual", "Hearing", "Other"])
            financial = st.radio("Require financial support?", ["Yes", "No"])

        if st.button("Submit Registration", use_container_width=True):
            st.session_state['athlete_profile'] = {
                "Name": name, "Age": age, "Sex": sex, "State": state,
                "City": city, "Background": background, "Disability": disability,
                "Sport": sport, "FinancialAid": financial
            }
            st.success("✅ Registration submitted successfully!")

# ---------------------- Achievements ----------------------
if st.session_state['signup_mode']:
    with tabs[1]:
        st.header("🏅 Athlete Achievements")
        st.markdown("Showcase your accomplishments by adding them below.")
        if st.session_state['achievements'] is None:
            st.session_state['achievements'] = []

        with st.form("achievements_form", clear_on_submit=True):
            ach_desc = st.text_area("Describe your achievement")
            ach_img = st.file_uploader("Upload Achievement Image", type=["jpg", "jpeg", "png"])
            submitted = st.form_submit_button("➕ Add Achievement")

            if submitted:
                if ach_desc.strip():
                    st.session_state['achievements'].append({
                        "description": ach_desc,
                        "image": ach_img.read() if ach_img else None
                    })
                    st.success("Achievement added!")
                else:
                    st.warning("Please enter a description before adding.")

        if st.session_state['achievements']:
            st.subheader("Your Achievements")
            # Use columns to display achievements as a gallery
            cols = st.columns(3)
            for i, ach in enumerate(st.session_state['achievements']):
                with cols[i % 3]:
                    with st.container(border=True):
                        st.write("🏆", ach["description"])
                        if ach["image"]:
                            st.image(ach["image"], width=200)

# ---------------------- Fitness Test ----------------------
if st.session_state['signup_mode']:
    with tabs[2]:
        st.header("🏃 Fitness Test")
        st.markdown("Upload a photo or video for an AI-powered fitness analysis.")
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Image Analysis")
            img_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"], key='img_uploader')
        with col2:
            st.subheader("Video Analysis")
            vid_file = st.file_uploader("Upload Video", type=["mp4", "avi", "mov"], key='vid_uploader')
            exercise_type = st.selectbox("Exercise Type", ["squat", "pushup"])

        st.markdown("---")
        if img_file and MP_AVAILABLE:
            st.subheader("Image Results")
            image = Image.open(img_file).convert("RGB")
            image_np = np.array(image)[:, :, ::-1]
            with st.spinner("Analyzing image..."):
                res = analyze_image_pose(image_np)
            st.image(res['annotated_image'], caption="Analyzed Image", use_column_width=True)
            st.session_state['image_metrics'] = res['metrics']
            st.markdown(f"**Posture Score:** {res['metrics'].get('posture_score', 'N/A')}")
            recs = recommendations_from_metrics(res['metrics'])
            st.subheader("Recommendations")
            for r in recs:
                st.markdown(f"<div class='metric-box'>{r}</div>", unsafe_allow_html=True)

        if vid_file and MP_AVAILABLE:
            st.subheader("Video Results")
            tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
            tfile.write(vid_file.read()); tfile.close()
            with st.spinner("Analyzing video..."):
                res = analyze_video_reps(tfile.name, exercise=exercise_type)
            st.session_state['video_metrics'] = res
            st.markdown(f"**Reps Detected:** {res.get('rep_count', 'N/A')}")
            recs = recommendations_from_metrics({}, reps=res.get('rep_count'))
            st.subheader("Recommendations")
            for r in recs:
                st.markdown(f"<div class='metric-box'>{r}</div>", unsafe_allow_html=True)
            os.remove(tfile.name)

# ---------------------- Dashboard ----------------------
dash_tab = tabs[-1]
with dash_tab:
    st.header("📊 Athlete Dashboard")
    st.markdown("A summary of your profile, achievements, and fitness data.")
    
    col_profile, col_achievements = st.columns([1, 1])

    with col_profile:
        st.subheader("Personal Profile")
        if st.session_state['athlete_profile']:
            profile_df = pd.DataFrame([st.session_state['athlete_profile']]).T
            profile_df.columns = ["Value"]
            st.dataframe(profile_df, use_container_width=True)
        else:
            st.info("No registration found. Please complete the registration form.")

    with col_achievements:
        st.subheader("Achievements")
        if st.session_state['achievements']:
            for ach in st.session_state['achievements']:
                with st.container(border=True):
                    st.write("🏆", ach["description"])
                    if ach["image"]:
                        st.image(ach["image"], width=150)
        else:
            st.info("No achievements recorded yet.")

    st.markdown("---")
    st.subheader("Fitness Test Results")
    col_img_metrics, col_vid_metrics = st.columns([1, 1])
    
    with col_img_metrics:
        st.markdown("#### Pose Analysis")
        if st.session_state['image_metrics']:
            for k, v in st.session_state['image_metrics'].items():
                st.metric(label=k.replace('_', ' ').title(), value=v)
        else:
            st.info("No image metrics available.")
    
    with col_vid_metrics:
        st.markdown("#### Repetition Count")
        if st.session_state['video_metrics']:
            st.metric(label="Reps Detected", value=st.session_state['video_metrics'].get('rep_count', 'N/A'))
        else:
            st.info("No video metrics available.")

    # PDF Download
    st.markdown("---")
    st.markdown("<div class='center'>", unsafe_allow_html=True)
    if st.button("📄 Download PDF Summary", key='pdf_download_button'):
        filename = f"{st.session_state['username']}_summary.pdf"
        all_metrics = {}
        if st.session_state['image_metrics']: all_metrics.update(st.session_state['image_metrics'])
        if st.session_state['video_metrics']: all_metrics.update(st.session_state['video_metrics'])
        generate_pdf(filename, st.session_state['athlete_profile'], st.session_state['achievements'], all_metrics)
        with open(filename, "rb") as f:
            st.download_button("Click to Download", f, file_name=filename)
        os.remove(filename)
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------- Footer ----------------------
st.markdown("""
<style>
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: rgba(240, 253, 244, 0.9); /* More opaque background for text */
    color: #555;
    text-align: center;
    padding: 10px;
    font-size: small;
    border-top: 1px solid #e0e0e0;
}
</style>
<div class="footer">
    © 2025 One Nation, One Athlete | Powered by Streamlit
</div>
""", unsafe_allow_html=True)
