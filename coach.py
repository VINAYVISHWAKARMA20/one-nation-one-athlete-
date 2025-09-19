import streamlit as st
import json
from firebase_admin import credentials, initialize_app, firestore
import firebase_admin.firestore
import firebase_admin.auth
from firebase_admin.auth import sign_in_with_custom_token, sign_in_anonymously, get_user
import base64
import os

# Custom CSS for styling
st.markdown("""
<style>
    .stButton>button {
        color: white;
        background-color: #007bff;
        border: 2px solid #007bff;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #0056b3;
        border-color: #0056b3;
    }
    .stButton>button.blue {
        background-color: #007bff;
        border-color: #007bff;
    }
    .stButton>button.green {
        background-color: #28a745;
        border-color: #28a745;
    }
    .stTextInput>div>div>input {
        border: 2px solid #007bff;
        border-radius: 8px;
    }
    .stTextArea>div>div>textarea {
        border: 2px solid #007bff;
        border-radius: 8px;
    }
    .stFileUploader>div>div {
        border: 2px dashed #007bff;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)


# Initialize Firebase and Firestore
if 'db' not in st.session_state:
    try:
        # These variables are injected by the Canvas environment
        firebase_config = json.loads(os.environ.get('__firebase_config', '{}'))
        app_id = os.environ.get('__app_id', 'default-app-id')
        initial_auth_token = os.environ.get('__initial_auth_token', None)

        if not firebase_admin._apps:
            cred = credentials.Certificate(firebase_config)
            initialize_app(cred)
        
        db = firestore.client()
        st.session_state.db = db
        st.session_state.app_id = app_id
        st.session_state.auth = firebase_admin.auth
        st.session_state.user_uid = None
        st.session_state.auth_ready = False
        
        if initial_auth_token:
            auth_user = st.session_state.auth.sign_in_with_custom_token(initial_auth_token)
            st.session_state.user_uid = auth_user.uid
        else:
            auth_user = st.session_state.auth.sign_in_anonymously()
            st.session_state.user_uid = auth_user.uid
            
        st.session_state.auth_ready = True
        
    except Exception as e:
        st.error(f"Error initializing Firebase: {e}")
        st.stop()

# Set up the main session state for the app flow
if 'page' not in st.session_state:
    st.session_state.page = 'login'

# Helper functions
def get_user_doc_ref():
    if not st.session_state.user_uid:
        return None
    app_id = st.session_state.app_id
    user_id = st.session_state.user_uid
    return st.session_state.db.collection(f'artifacts/{app_id}/users/{user_id}/coach_profiles').document(user_id)

def add_experience():
    st.session_state.experiences.append({
        'where': '',
        'why': '',
        'proof_image': None
    })

def add_achievement():
    st.session_state.achievements.append({
        'what': '',
        'proof_image': None
    })

def save_profile_data(data):
    doc_ref = get_user_doc_ref()
    if doc_ref:
        try:
            doc_ref.set(data)
            st.success("Profile saved successfully!")
            st.session_state.profile_data = data
            st.session_state.page = 'dashboard'
            st.rerun()
        except Exception as e:
            st.error(f"Error saving profile: {e}")
    else:
        st.error("User not authenticated.")

def update_profile_data(data):
    doc_ref = get_user_doc_ref()
    if doc_ref:
        try:
            doc_ref.update(data)
            st.success("Profile updated successfully!")
            st.session_state.profile_data = data
            st.session_state.page = 'dashboard'
            st.rerun()
        except Exception as e:
            st.error(f"Error updating profile: {e}")
    else:
        st.error("User not authenticated.")

def load_profile_data():
    doc_ref = get_user_doc_ref()
    if doc_ref:
        doc = doc_ref.get()
        if doc.exists:
            st.session_state.profile_data = doc.to_dict()
            st.session_state.page = 'dashboard'
        else:
            st.session_state.page = 'signup_step_1'

def show_dashboard():
    st.title("👨‍💼 Coach Profile Dashboard")
    st.info(f"**Your User ID:** {st.session_state.user_uid}")

    if st.session_state.profile_data:
        data = st.session_state.profile_data
        
        st.subheader("Basic Information")
        st.write(f"**Name:** {data.get('name', '')}")
        st.write(f"**Email:** {data.get('email', '')}")
        st.write(f"**Phone Number:** {data.get('phone_number', '')}")
        st.write(f"**Years of Experience:** {data.get('years_of_experience', '')}")

        if 'photo_base64' in data and data['photo_base64']:
            st.image(base64.b64decode(data['photo_base64']), caption="Coach Photo")

        st.subheader("Experience")
        for i, exp in enumerate(data.get('experiences', [])):
            with st.expander(f"Experience #{i+1}"):
                st.write(f"**Where:** {exp.get('where', '')}")
                st.write(f"**Why:** {exp.get('why', '')}")
                if 'proof_base64' in exp and exp['proof_base64']:
                    st.image(base64.b64decode(exp['proof_base64']), caption="Proof Image")

        st.subheader("Achievements")
        for i, ach in enumerate(data.get('achievements', [])):
            with st.expander(f"Achievement #{i+1}"):
                st.write(f"**What:** {ach.get('what', '')}")
                if 'proof_base64' in ach and ach['proof_base64']:
                    st.image(base64.b64decode(ach['proof_base64']), caption="Proof Image")
        
        st.subheader("Planning & Execution Task")
        st.write(data.get('planning_task', ''))

    if st.button("Edit Profile", help="Click to edit your profile", type="primary"):
        st.session_state.page = 'edit_form'
        st.rerun()

    if st.button("Logout", help="Click to logout", type="secondary"):
        st.session_state.page = 'login'
        st.rerun()


def show_login_signup():
    st.title("Welcome")
    st.header("Coach Registration Portal")
    
    st.info(f"**Your User ID:** {st.session_state.user_uid}")

    st.write("Please select an option to continue.")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Sign Up", help="Create a new profile", type="primary"):
            st.session_state.page = 'signup_step_1'
            st.session_state.form_data = {}
            st.session_state.experiences = []
            st.session_state.achievements = []
            st.rerun()
    with col2:
        if st.button("Login", help="Login to edit an existing profile", type="secondary"):
            load_profile_data()


def show_signup_form():
    st.title("📝 Coach Registration")
    st.markdown("---")

    form = st.form("coach_registration_form")
    
    if st.session_state.page == 'signup_step_1':
        form.subheader("1. Basic Information")
        name = form.text_input("Full Name", value=st.session_state.form_data.get('name', ''))
        email = form.text_input("Email", value=st.session_state.form_data.get('email', ''))
        phone_number = form.text_input("Phone Number", value=st.session_state.form_data.get('phone_number', ''))
        years_of_experience = form.number_input("Years of Experience", min_value=0, max_value=100, value=st.session_state.form_data.get('years_of_experience', 0))
        
        if form.form_submit_button("Next: Experience", type="primary"):
            st.session_state.form_data.update({
                'name': name, 'email': email, 'phone_number': phone_number, 'years_of_experience': years_of_experience
            })
            st.session_state.page = 'signup_step_2'
            st.rerun()

    elif st.session_state.page == 'signup_step_2':
        form.subheader("2. Experience with Proof")
        st.info("Provide details of your experience. Click 'Add More' to add another entry.")
        
        for i, exp in enumerate(st.session_state.experiences):
            with form.container():
                form.write(f"**Experience #{i+1}**")
                exp['where'] = form.text_input("Where?", value=exp.get('where', ''), key=f"exp_where_{i}")
                exp['why'] = form.text_area("Why?", value=exp.get('why', ''), key=f"exp_why_{i}")
                exp['proof_image'] = form.file_uploader("Upload Journal Proof (Image)", type=['jpg', 'jpeg', 'png'], key=f"exp_proof_{i}")
                if exp['proof_image']:
                    exp['proof_base64'] = base64.b64encode(exp['proof_image'].read()).decode('utf-8')

        if form.form_submit_button("Add More Experience", help="Click to add another experience entry", type="secondary"):
            add_experience()
            st.rerun()
        
        if form.form_submit_button("Next: Achievements", type="primary"):
            st.session_state.page = 'signup_step_3'
            st.rerun()

    elif st.session_state.page == 'signup_step_3':
        form.subheader("3. Achievements with Proof")
        st.info("Share your key achievements. Click 'Add More' to add another entry.")
        
        for i, ach in enumerate(st.session_state.achievements):
            with form.container():
                form.write(f"**Achievement #{i+1}**")
                ach['what'] = form.text_area("What was the achievement?", value=ach.get('what', ''), key=f"ach_what_{i}")
                ach['proof_image'] = form.file_uploader("Upload Proof (Image)", type=['jpg', 'jpeg', 'png'], key=f"ach_proof_{i}")
                if ach['proof_image']:
                    ach['proof_base64'] = base64.b64encode(ach['proof_image'].read()).decode('utf-8')
        
        if form.form_submit_button("Add More Achievements", help="Click to add another achievement entry", type="secondary"):
            add_achievement()
            st.rerun()
            
        if form.form_submit_button("Next: Photo", type="primary"):
            st.session_state.page = 'signup_step_4'
            st.rerun()

    elif st.session_state.page == 'signup_step_4':
        form.subheader("4. Coach Photo")
        photo = form.file_uploader("Upload Your Profile Photo", type=['jpg', 'jpeg', 'png'])
        if photo:
            st.session_state.form_data['photo'] = photo
            st.session_state.form_data['photo_base64'] = base64.b64encode(photo.read()).decode('utf-8')
            form.image(photo, caption="Your Photo", width=200)

        if form.form_submit_button("Next: Planning Task", type="primary"):
            st.session_state.page = 'signup_step_5'
            st.rerun()

    elif st.session_state.page == 'signup_step_5':
        form.subheader("5. Planning & Execution Task")
        planning_task = form.text_area(
            "Describe a planning and execution task you handled:",
            value=st.session_state.form_data.get('planning_task', ''),
            height=200
        )
        st.session_state.form_data['planning_task'] = planning_task
        
        if form.form_submit_button("Submit Registration", type="primary"):
            final_data = {
                'name': st.session_state.form_data.get('name', ''),
                'email': st.session_state.form_data.get('email', ''),
                'phone_number': st.session_state.form_data.get('phone_number', ''),
                'years_of_experience': st.session_state.form_data.get('years_of_experience', 0),
                'photo_base64': st.session_state.form_data.get('photo_base64', ''),
                'planning_task': st.session_state.form_data.get('planning_task', ''),
                'experiences': [
                    {'where': exp['where'], 'why': exp['why'], 'proof_base64': exp.get('proof_base64', '')}
                    for exp in st.session_state.experiences
                ],
                'achievements': [
                    {'what': ach['what'], 'proof_base64': ach.get('proof_base64', '')}
                    for ach in st.session_state.achievements
                ]
            }
            save_profile_data(final_data)


def show_edit_form():
    st.title("📝 Edit Profile")
    st.markdown("---")
    
    if 'profile_data' not in st.session_state:
        st.warning("No profile data found. Please login first.")
        st.session_state.page = 'login'
        st.rerun()
        
    data = st.session_state.profile_data
    
    with st.form("edit_form"):
        st.subheader("Basic Information")
        name = st.text_input("Full Name", value=data.get('name', ''))
        email = st.text_input("Email", value=data.get('email', ''))
        phone_number = st.text_input("Phone Number", value=data.get('phone_number', ''))
        years_of_experience = st.number_input("Years of Experience", min_value=0, max_value=100, value=data.get('years_of_experience', 0))
        
        st.subheader("Experience")
        experiences_to_update = data.get('experiences', [])
        
        for i, exp in enumerate(experiences_to_update):
            with st.expander(f"Experience #{i+1}"):
                exp['where'] = st.text_input("Where?", value=exp.get('where', ''), key=f"edit_exp_where_{i}")
                exp['why'] = st.text_area("Why?", value=exp.get('why', ''), key=f"edit_exp_why_{i}")
                
        if st.form_submit_button("Save Changes", type="primary"):
            updated_data = {
                'name': name,
                'email': email,
                'phone_number': phone_number,
                'years_of_experience': years_of_experience,
                'experiences': experiences_to_update
            }
            update_profile_data(updated_data)

# Main app logic based on page state
if st.session_state.auth_ready:
    if st.session_state.page == 'login':
        show_login_signup()
    elif st.session_state.page.startswith('signup'):
        show_signup_form()
    elif st.session_state.page == 'dashboard':
        show_dashboard()
    elif st.session_state.page == 'edit_form':
        show_edit_form()
else:
    st.info("Connecting to Firebase...")
