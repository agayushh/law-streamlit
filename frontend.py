import os
import requests
import streamlit as st
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

# ─── Supabase Setup ─────────────────────────────────
supabase_url = "https://ctrbrlsgdteajwncawzu.supabase.co"
supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImN0cmJybHNnZHRlYWp3bmNhd3p1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDY3ODQwMjksImV4cCI6MjA2MjM2MDAyOX0.0RWo4x5h8D6k_OzLdd6lm8kw1Qpm0vVpGSmJX7DMA3c"

supabase: Client = create_client(supabase_url, supabase_key)

# ─── Initialize Session State ─────────────────────────
if 'user' not in st.session_state:
    st.session_state.user = None
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'show_auth_modal' not in st.session_state:
    st.session_state.show_auth_modal = False
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Home"
if 'history' not in st.session_state:
    st.session_state.history = []

# ─── Page Config & Enhanced Styles ─────────────────────────────
st.set_page_config(
    page_title="Law Vector - Legal AI Assistant",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Inter:wght@300;400;500;600&display=swap');
        
        /* Global Styles */
        .stApp {
            background: linear-gradient(135deg, #0f1419 0%, #1a2332 50%, #2c3e50 100%);
            color: #ffffff;
        }
        
        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stDeployButton {visibility: hidden;}
        
        .navbar {
            background: linear-gradient(90deg, #1a2332 0%, #2c3e50 100%);
            padding: 1rem 2rem;
            margin: -2rem -2rem 0 -2rem;
            border-bottom: 3px solid #d4af37;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
            position: sticky;
            top: 0;
            z-index: 1000;
            
        }

        .nav-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            max-width: 1200px;
            margin: q00 ;
            flex-wrap: wrap;
        }
        
        .logo-section {
            display: flex;
            align-items: center;
            gap: 1rem;
            # margin-top: -90px;
        }
        
        .logo-text {
            font-family: 'Playfair Display', serif;
            font-size: 2.2rem;
            font-weight: 700;
            color: #d4af37;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }
        
        .tagline {
            font-family: 'Inter', sans-serif;
            font-size: 0.8rem;
            color: #b8c5d1;
            font-style: italic;
            margin-top: -3px;
        }
        
        /* Navigation Menu */
        .nav-menu {
            display: flex;
            gap: 2rem;
            align-items: center;
            # margin-top: -90px;
        }
        
        .nav-item {
            font-family: 'Inter', sans-serif;
            font-weight: 500;
            color: #b8c5d1;
            text-decoration: none;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            transition: all 0.3s ease;
            cursor: pointer;
            # margin-top: -90px;
        }
        
        .nav-item:hover, .nav-item.active {
            color: #d4af37;
            background: rgba(212, 175, 55, 0.1);
        }
        
        /* Auth Buttons */
        .auth-buttons {
            display: flex;
            gap: 1rem;
            align-items: center;
        }
        
        .user-profile {
            display: flex;
            align-items: center;
            gap: 1rem;
            color: #d4af37;
            font-family: 'Inter', sans-serif;
            font-weight: 500;
            background: rgba(212, 175, 55, 0.1);
            padding: 0.5rem 1rem;
            border-radius: 20px;
            border: 1px solid rgba(212, 175, 55, 0.3);
        }
        
        /* Modal Styles */
        .modal-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.8);
            backdrop-filter: blur(5px);
            z-index: 2000;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        
        .modal-content {
            background: linear-gradient(135deg, #1a2332, #2c3e50);
            padding: 2rem;
            border-radius: 20px;
            border: 2px solid #d4af37;
            box-shadow: 0 20px 60px rgba(0,0,0,0.5);
            max-width: 400px;
            width: 90%;
            position: relative;
        }
        
        .modal-close {
            position: absolute;
            top: 1rem;
            right: 1rem;
            background: none;
            border: none;
            color: #d4af37;
            font-size: 1.5rem;
            cursor: pointer;
            padding: 0.5rem;
            border-radius: 50%;
            transition: all 0.3s ease;
        }
        
        .modal-close:hover {
            background: rgba(212, 175, 55, 0.1);
        }
        
        button[kind="primary"],
        button[kind="secondary"],
        .stButton > button,
        .stDownloadButton > button {
            background: linear-gradient(45deg, #d4af37, #f4d03f) !important;
            color: #1a2332 !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 0 1rem !important;
            font-weight: 600 !important;
            font-family: 'Inter', sans-serif !important;
            font-size: 1rem !important;
            height: 48px !important;
            width: 140px !important;
            display: inline-flex !important;
            align-items: center !important;
            justify-content: center !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 15px rgba(212, 175, 55, 0.3) !important;
            white-space: nowrap !important;
        }

        /* Hover effect for all buttons */
        button[kind="primary"]:hover,
        button[kind="secondary"]:hover,
        .stButton > button:hover,
        .stDownloadButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(212, 175, 55, 0.4) !important;
        }

        /* Main Content Container */
        .main-container {
            max-width: 1200px;
            margin: 2rem auto;
            padding: 2rem;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 20px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
            min-height: 70vh;
        }
        
        /* Hero Section */
        .hero-section {
            text-align: center;
            padding: 4rem 0;
            background: linear-gradient(135deg, rgba(212, 175, 55, 0.1), rgba(44, 62, 80, 0.1));
            border-radius: 15px;
            margin-bottom: 3rem;
            border: 1px solid rgba(212, 175, 55, 0.2);
        }
        
        .hero-title {
            font-family: 'Playfair Display', serif;
            font-size: 3.5rem;
            font-weight: 700;
            color: #d4af37;
            margin-bottom: 1rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }
        .hero-subtitle {
            font-family: 'Inter', sans-serif;
            font-size: 1.3rem;
            color: #b8c5d1;
            max-width: 700px;
            margin: 0 auto 2rem auto;
            line-height: 1.6;
        }
        /* Form Styling */
        .stTextInput > div > div > input {
            background: rgba(255, 255, 255, 0.1) !important;
            border: 2px solid rgba(212, 175, 55, 0.3) !important;
            border-radius: 10px !important;
            color: #ffffff !important;
            font-family: 'Inter', sans-serif !important;
            padding: 0.8rem !important;
            transition: all 0.3s ease !important;
            margin-bottom: 1.5rem !important; /* space below inputs */
        }

        .stTextInput > div > div > input:focus {
            border-color: #d4af37 !important;
            box-shadow: 0 0 20px rgba(212, 175, 55, 0.3) !important;
        }
        
        .stFileUploader > div {
            background: rgba(255, 255, 255, 0.05) !important;
            border: 2px dashed rgba(212, 175, 55, 0.5) !important;
            border-radius: 15px !important;
            padding: 2rem !important;
            text-align: center !important;
        }
        
        /* Chat Styling */
        .chat-container {
            background: rgba(255, 255, 255, 0.03);
            border-radius: 15px;
            padding: 2rem;
            margin-top: 2rem;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .chat-bubble {
            padding: 1rem 1.5rem;
            margin: 1rem 0;
            border-radius: 20px;
            max-width: 75%;
            line-height: 1.6;
            font-family: 'Inter', sans-serif;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }
        
        .user-message {
            background: linear-gradient(135deg, #d4af37, #f4d03f);
            color: #1a2332;
            margin-left: 25%;
            font-weight: 500;
        }
        
        .bot-message {
            background: rgba(255, 255, 255, 0.1);
            color: #ffffff;
            margin-right: 25%;
            border: 1px solid rgba(212, 175, 55, 0.2);
        }
        
        /* About Section */
        .about-section {
            background: linear-gradient(135deg, rgba(212, 175, 55, 0.1), rgba(255, 255, 255, 0.05));
            padding: 2rem;
            border-radius: 15px;
            margin: 2rem 0;
            border-left: 5px solid #d4af37;
            border: 1px solid rgba(212, 175, 55, 0.2);
        }
        
        .about-title {
            font-family: 'Playfair Display', serif;
            font-size: 1.8rem;
            color: #d4af37;
            margin-bottom: 1rem;
        }
        
        .about-text {
            font-family: 'Inter', sans-serif;
            color: #b8c5d1;
            line-height: 1.6;
        }
        
        /* Footer */
        .footer {
            background: linear-gradient(90deg, #1a2332 0%, #2c3e50 100%);
            padding: 3rem 2rem 2rem 2rem;
            margin: 3rem -1rem -1rem -1rem;
            border-top: 3px solid #d4af37;
            box-shadow: 0 -4px 20px rgba(0,0,0,0.3);
        }
        
        .footer-content {
            max-width: 1200px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: 2fr 1fr 1fr;
            gap: 2rem;
        }
        
        .footer-section h3 {
            font-family: 'Playfair Display', serif;
            color: #d4af37;
            margin-bottom: 1rem;
        }
        
        .footer-section p, .footer-section a {
            font-family: 'Inter', sans-serif;
            color: #b8c5d1;
            line-height: 1.6;
            text-decoration: none;
        }
        
        .footer-section a:hover {
            color: #d4af37;
        }
        
        .social-links {
            display: flex;
            gap: 1rem;
            margin-top: 1rem;
        }
        
        .social-link {
            background: rgba(212, 175, 55, 0.1);
            padding: 0.8rem;
            border-radius: 50%;
            color: #d4af37;
            text-decoration: none;
            transition: all 0.3s ease;
            border: 1px solid rgba(212, 175, 55, 0.3);
        }
        
        .social-link:hover {
            background: rgba(212, 175, 55, 0.2);
            transform: translateY(-2px);
        }
        
        .footer-bottom {
            text-align: center;
            margin-top: 2rem;
            padding-top: 2rem;
            border-top: 1px solid rgba(212, 175, 55, 0.3);
            color: #b8c5d1;
            font-family: 'Inter', sans-serif;
        }
        
        /* Section Headers */
        .section-header {
            font-family: 'Playfair Display', serif;
            font-size: 1.8rem;
            color: #d4af37;
            margin: 2rem 0 1rem 0;
            text-align: center;
        }
        
        /* Success/Error Messages */
        .stSuccess {
            background: rgba(46, 204, 113, 0.2) !important;
            border: 1px solid #2ecc71 !important;
            border-radius: 10px !important;
        }
        
        .stError {
            background: rgba(231, 76, 60, 0.2) !important;
            border: 1px solid #e74c3c !important;
            border-radius: 10px !important;
        }
        
        .stWarning {
            background: rgba(241, 196, 15, 0.2) !important;
            border: 1px solid #f1c40f !important;
            border-radius: 10px !important;
        }
        
        .stInfo {
            background: rgba(52, 152, 219, 0.2) !important;
            border: 1px solid #3498db !important;
            border-radius: 10px !important;
        }
        
        /* Tabs Styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 2rem;
        }
        
        .stTabs [data-baseweb="tab"] {
            background: rgba(212, 175, 55, 0.1);
            border-radius: 10px;
            color: #d4af37;
            border: 1px solid rgba(212, 175, 55, 0.3);
        }
        
        .stTabs [aria-selected="true"] {
            background: rgba(212, 175, 55, 0.2);
        }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            .nav-container {
                flex-direction: column;
                gap: 1rem;
            }
            
            .logo-text {
                font-size: 1.8rem;
            }
            
            .hero-title {
                font-size: 2.5rem;
            }
            
            .main-container {
                padding: 1rem;
            }
            
            .footer-content {
                grid-template-columns: 1fr;
                text-align: center;
            }
        }
    </style>
""", unsafe_allow_html=True)

def login(email, password):
    try:
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })

        if response.user:
            st.session_state.user = response.user
            st.session_state.logged_in = True
            st.session_state.show_auth_modal = False
            st.success(f"Welcome back, {response.user.email}!")
            return response
        else:
            st.error("Login failed - invalid credentials")
            return None

    except Exception as e:
        st.error(f"Login error: {str(e)}")
        return None

def signup(email, password):
    try:
        response = supabase.auth.sign_up({"email": email, "password": password})
        if response.user:
            st.success("Sign-up successful! Check your email for confirmation.")
            return response
        else:
            st.error("Sign-up failed")
            return None
    except Exception as e:
        st.error(f"Sign-up error: {str(e)}")
        return None

# ─── Navigation Bar ────────────────────────────────────────────
def render_navbar():
    # Navigation menu items
    nav_col1, nav_col2, nav_col3, nav_col4, nav_col5 = st.columns([3, 1, 1, 1, 2])
    
    with nav_col1:
        st.markdown("""
            <div class="logo-section">
                <div>
                    <div class="logo-text">Law Vector</div>
                    <div class="tagline">Professional Legal AI Assistant</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with nav_col2:
        if st.button("Home", key="nav_home", help="Go to Home"):
            st.session_state.current_page = "Home"
            st.rerun()
    
    with nav_col3:
        if st.button("About", key="nav_about", help="Learn About Law Vector"):
            st.session_state.current_page = "About"
            st.rerun()
    
    with nav_col4:
        if st.session_state.logged_in:
            if st.button("Dashboard", key="nav_dashboard", help="Your Dashboard"):
                st.session_state.current_page = "Dashboard"
                st.rerun()
    
    with nav_col5:
        if not st.session_state.logged_in:
            auth_col1, auth_col2 = st.columns(2)
            with auth_col1:
                if st.button("Login", key="nav_login"):
                    st.session_state.show_auth_modal = True
                    st.rerun()
            with auth_col2:
                if st.button("Sign Up", key="nav_signup"):
                    st.session_state.show_auth_modal = True
                    st.rerun()
        else:
            # User profile section
            user_email = ""
            if hasattr(st.session_state.user, 'email'):
                user_email = st.session_state.user.email
            elif isinstance(st.session_state.user, dict) and 'email' in st.session_state.user:
                user_email = st.session_state.user['email']
            
            user_col1, user_col2 = st.columns([2, 1])
            with user_col1:
                st.markdown(f'<div class="user-profile">👤 {user_email.split("@")[0] if user_email else "User"}</div>', unsafe_allow_html=True)
            with user_col2:
                if st.button("🚪 Logout", key="nav_logout"):
                    try:
                        supabase.auth.sign_out()
                    except:
                        pass
                    st.session_state.user = None
                    st.session_state.logged_in = False
                    st.session_state.current_page = "Home"
                    st.rerun()

# ─── Authentication Modal ────────────────────────────
def render_auth_modal():
    if st.session_state.show_auth_modal:
        # Create a container for the modal
        with st.container():
            # Use columns to center the modal
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col2:
                # Modal content
                st.markdown("### Access Your Legal Assistant")
                
                tab1, tab2 = st.tabs(["  Sign In  ", "  Sign Up  "])
                
                with tab1:
                    with st.form("modal_login_form"):
                        email_in = st.text_input("Email Address", placeholder="your.email@lawfirm.com", key="modal_email_in")
                        pwd_in = st.text_input("Password", type="password", placeholder="Enter your password", key="modal_pwd_in")
                        
                        col_login1, col_login2 = st.columns([1, 1])
                        with col_login1:
                            login_submitted = st.form_submit_button("Sign In")
                        with col_login2:
                            if st.form_submit_button("Cancel"):
                                st.session_state.show_auth_modal = False
                                st.rerun()
                        
                        if login_submitted:
                            if email_in and pwd_in:
                                res = login(email_in, pwd_in)
                                if res and res.user:
                                    st.rerun()
                            else:
                                st.error("Please enter both email and password")
                
                with tab2:
                    with st.form("modal_signup_form"):
                        email_up = st.text_input("Email Address", placeholder="your.email@lawfirm.com", key="modal_email_up")
                        pwd_up = st.text_input("Password", type="password", placeholder="Create a secure password", key="modal_pwd_up")
                        
                        col_signup1, col_signup2 = st.columns([1, 1])
                        with col_signup1:
                            signup_submitted = st.form_submit_button("Create Account")
                        with col_signup2:
                            if st.form_submit_button("Cancel"):
                                st.session_state.show_auth_modal = False
                                st.rerun()
                        
                        if signup_submitted:
                            if email_up and pwd_up:
                                res = signup(email_up, pwd_up)
                                if res:
                                    st.session_state.show_auth_modal = False
                            else:
                                st.error("Please enter both email and password")

# ─── Footer ────────────────────────────────────────────
def render_footer():
    st.markdown("""
        <div class="footer">
            <div class="footer-content">
                <div class="footer-section">
                    <h3>LawVector Legal AI</h3>
                    <p>Empowering legal professionals with cutting-edge AI. Instant legal insights and document analysis.</p>
                    <div class="social-links">
                        <a href="https://x.com/futurebeast_04" class="social-link" target="_blank" title="Follow us on X">𝕏</a>
                        <a href="https://x.com/idkwhyvi62159" class="social-link" target="_blank" title="Connect on X">𝕏</a>
                    </div>
                </div>
                <div class="footer-section">
                    <h3>Quick Links</h3>
                    <p><a href="#home">Home</a></p>
                    <p><a href="#about">About Us</a></p>
                    <p><a href="#support">Support Center</a></p>
                </div>
                <div class="footer-section">
                    <h3>Contact Us</h3>
                    <p>📧 lawvector09@gmail.com</p>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2024 LawVector Legal AI. All rights reserved.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

# ─── Page Content Functions ────────────────────────────
def render_home_page():
    # Hero Section
    if not st.session_state.logged_in:
        st.markdown("""
            <div class="hero-section">
                <h1 class="hero-title">Advanced Legal Intelligence</h1>
                <p class="hero-subtitle">
                    Harness the power of AI to analyze legal documents, extract key insights, 
                    and get instant answers to your legal questions with professional-grade accuracy.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚀 Get Started Today", key="hero_cta", help="Sign up to access all features"):
            st.session_state.show_auth_modal = True
            st.rerun()
    
    # General Legal Advice Section
    st.markdown('<h2 class="section-header">💡 General Legal Advice</h2>', unsafe_allow_html=True)
    
    user_question = st.text_input(
        "Enter your legal question or concern:", 
        key="general_input", 
        placeholder="e.g., What are my rights as a tenant? How do I file a complaint?"
    )
    
    if st.button("Get AI Legal Advice", key="get_advice"):
        if not user_question.strip():
            st.warning("Please type a question first.")
        else:
            with st.spinner("Analyzing your legal question..."):
                try:
                    api_key = "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"
                    headers = {
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json"
                    }
                    payload = {
                        "model": "sonar-pro",
                        "messages": [
                            {
                                "role": "system",
                                "content": """You are a professional legal AI assistant specializing in Indian law and the Indian Penal Code (IPC). 

                            Provide helpful, accurate legal information while being clear that this is general information and not personalized legal advice. Always recommend consulting with a qualified attorney for specific legal matters.

                            Guidelines:
                            - Focus on Indian law, IPC, and relevant Indian legal procedures
                            - Provide clear, professional responses
                            - Include relevant legal sections or provisions when applicable
                            - Suggest next steps or actions the user might consider
                            - Always include a disclaimer about seeking professional legal counsel
                            - Be respectful and maintain professional tone
                            - If the question is outside Indian law scope, clarify and redirect appropriately"""
                            },
                            {"role": "user", "content": user_question}
                        ],
                        "temperature": 0.2,
                        "max_tokens": 600
                    }

                    response = requests.post(
                        "https://api.perplexity.ai/chat/completions",
                        json=payload,
                        headers=headers
                    )

                    if response.ok:
                        data = response.json()
                        advice = data["choices"][0]["message"]["content"].strip()
                        st.markdown(f'<div class="chat-bubble bot-message">{advice}</div>', unsafe_allow_html=True)

                        # Option to store data
                        if st.checkbox("Allow us to store this for research purposes (helps improve our AI)", key="store_data"):
                            try:
                                record = {"query": user_question, "response": advice}
                                res = supabase.table("legal_queries").insert(record).execute()
                                st.success("✅ Thank you! Your data has been saved for research purposes.")
                            except:
                                st.error("❌ Sorry, we couldn't save your data at this time.")
                    else:
                        st.error(f"❌ API error: {response.status_code} – {response.text}")

                except Exception as e:
                    st.error(f"❌ Error while fetching advice: {e}")
    
    
    # Document Analysis Section (for logged-in users)
    if st.session_state.logged_in:
        st.markdown('<h2 class="section-header">📄 Document Analysis & Legal Consultation</h2>', unsafe_allow_html=True)
        
        # File Upload Section
        st.markdown("### Upload Legal Document")
        pdf = st.file_uploader(
            "Select a PDF document for analysis",
            type="pdf",
            help="Upload contracts, legal briefs, court documents, or any legal PDF for AI-powered analysis"
        )
        
        BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:5000")
        
        if pdf is not None:
            with st.spinner("Uploading and analyzing document..."):
                try:
                    files = {"file": (pdf.name, pdf.getvalue(), "application/pdf")}
                    resp = requests.post(f"{BACKEND_URL}/upload", files=files)
                    
                    if resp.ok:
                        data = resp.json()
                        st.success(data.get("message", "✅ Document uploaded and analyzed successfully!"))
                        if "summary" in data:
                            st.markdown("### 📋 Document Summary")
                            st.markdown(f'<div class="about-section"><p class="about-text">{data["summary"]}</p></div>', unsafe_allow_html=True)
                    else:
                        error_msg = "Upload failed"
                        try:
                            error_data = resp.json()
                            error_msg = error_data.get("error", error_msg)
                        except:
                            pass
                        st.error(f"❌ {error_msg}")
                
                except Exception as e:
                    st.error(f"❌ Upload error: {str(e)}")
        
        # Chat Interface
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        st.markdown('<h3 class="section-header">💬 Legal Consultation Chat</h3>', unsafe_allow_html=True)
        
        # Chat input
        query = st.text_input(
            "Ask your legal question...",
            key="chat_input",
            placeholder="e.g., What are the key terms in this contract? What are my obligations under this agreement?"
        )
        
        col1, col2 = st.columns([1, 4])
        with col1:
            send_clicked = st.button("Send Query", key="send_btn")
        with col2:
            if st.session_state.history:
                clear_clicked = st.button("Clear Conversation", key="clear_chat")
            else:
                clear_clicked = False
        
        if send_clicked and query.strip():
            # Add user message to history
            st.session_state.history.append(("user", query))
            
            with st.spinner("Processing your query..."):
                try:
                    # Send request to backend
                    resp = requests.post(f"{BACKEND_URL}/chat", json={"query": query})
                    
                    if resp.ok:
                        answer = resp.json().get("response", "No response received")
                    else:
                        answer = f"Error: {resp.status_code} - {resp.text}"
                    
                    # Add bot response to history
                    st.session_state.history.append(("bot", answer))
                
                except Exception as e:
                    st.session_state.history.append(("bot", f"Error: {str(e)}"))
                
                # Refresh to show new messages
                st.rerun()
        
        if clear_clicked:
            st.session_state.history = []
            st.rerun()
        
        # Render chat history
        if st.session_state.history:
            st.markdown("### Conversation History")
            for sender, msg in st.session_state.history:
                css_class = "user-message" if sender == "user" else "bot-message"
                st.markdown(f'<div class="chat-bubble {css_class}">{msg}</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    else:
        st.info("🔐 Please sign in to access advanced features including document upload and AI consultation.")

def render_about_page():
    st.markdown('<h1 class="section-header">About Law Vector</h1>', unsafe_allow_html=True)
    
    st.markdown("""
        <div class="about-section">
            <h3 class="about-title">🎯 Our Mission</h3>
            <p class="about-text">
                Law Vector is revolutionizing the legal industry by making professional legal assistance accessible 
                to everyone through cutting-edge artificial intelligence. We believe that legal knowledge should 
                not be a privilege but a right accessible to all, especially in the Indian legal context.
            </p>
        </div>
        
        <div class="about-section">
            <h3 class="about-title">⚡ What We Offer</h3>
            <p class="about-text">
                • <strong>Document Analysis:</strong> Upload legal documents and get instant, comprehensive analysis<br>
                • <strong>Legal Consultation:</strong> Ask questions and receive professional-grade legal advice<br>
                • <strong>IPC Guidance:</strong> Specialized knowledge of Indian Penal Code and Indian law<br>
                • <strong>Contract Review:</strong> Identify key terms, risks, and obligations in contracts<br>
            </p>
        </div>
        
        <div class="about-section">
            <h3 class="about-title">🔬 Our Technology</h3>
            <p class="about-text">
                Law Vector analyzes legal case PDFs using AI to extract key facts, identify relevant laws, and deliver clear summaries. Behind the scenes, it chunks documents, generates embeddings, and performs semantic search using FAISS to find accurate and relevant legal insights. Just upload a PDF—Law Vector does the rest.
            </p>
        </div>
        
        <div class="about-section">
            <h3 class="about-title">🔒 Security & Privacy</h3>
            <p class="about-text">
                We take your privacy seriously. All documents and conversations are encrypted and stored 
                securely using industry-standard protocols. 
            </p>
        </div>
        
        <div class="about-section">
            <h3 class="about-title">👥 Our Team</h3>
            <p class="about-text">
                Law Vector was built by two cracked minds obsessed with law and tech. With no big team or backing—just sheer curiosity and chaos—we created it to make sense of legal stuff and maybe help a few people along the way.
            </p>
        </div>
        
        <div class="about-section">
            <h3 class="about-title">🌟 Why Choose Law Vector?</h3>
            <p class="about-text">
                • <strong>Accuracy:</strong> Trained on verified legal sources and Indian law<br>
                • <strong>Speed:</strong> Get instant responses to complex legal questions<br>
                • <strong>Affordability:</strong> Professional legal guidance at a fraction of traditional costs<br>
                • <strong>Accessibility:</strong> Available 24/7 from anywhere<br>
                • <strong>Specialization:</strong> Deep focus on Indian legal system and IPC<br>
                • <strong>Continuous Learning:</strong> AI improves with every interaction
            </p>
        </div>
    """, unsafe_allow_html=True)

def render_dashboard_page():
    if not st.session_state.logged_in:
        st.error(" Please log in to access your dashboard.")
        return
    
    st.markdown('<h1 class="section-header"> Your Legal Dashboard</h1>', unsafe_allow_html=True)
    
    # Dashboard metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class="about-section">
                <h3 class="about-title">Documents Analyzed</h3>
                <p class="about-text" style="font-size: 2rem; text-align: center; color: #d4af37;">12</p>
                <p class="about-text" style="text-align: center;">Total documents processed</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="about-section">
                <h3 class="about-title"> Consultations</h3>
                <p class="about-text" style="font-size: 2rem; text-align: center; color: #d4af37;">28</p>
                <p class="about-text" style="text-align: center;">Legal questions answered</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="about-section">
                <h3 class="about-title"> Time Saved</h3>
                <p class="about-text" style="font-size: 2rem; text-align: center; color: #d4af37;">45h</p>
                <p class="about-text" style="text-align: center;">Hours of legal research</p>
            </div>
        """, unsafe_allow_html=True)
    
    # Recent activity
    st.markdown("""
        <div class="about-section">
            <h3 class="about-title"> Recent Activity</h3>
            <p class="about-text">
                • <strong>Today:</strong> Contract analysis completed - Employment Agreement<br>
                • <strong>Yesterday:</strong> Legal consultation - Tenant rights inquiry under IPC<br>
                • <strong>2 days ago:</strong> Document upload - Partnership Agreement review<br>
                • <strong>3 days ago:</strong> Case research - Intellectual property dispute<br>
                • <strong>1 week ago:</strong> Legal advice - Consumer protection rights
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Quick actions
    st.markdown('<h2 class="section-header">🚀 Quick Actions</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button(" Upload New Document", key="quick_upload"):
            st.session_state.current_page = "Home"
            st.rerun()
    
    with col2:
        if st.button(" Ask Legal Question", key="quick_question"):
            st.session_state.current_page = "Home"
            st.rerun()
    
    with col3:
        if st.button(" View Analytics", key="quick_analytics"):
            st.info(" Detailed analytics coming soon!")

# ─── Main App Logic ────────────────────────────────────
def main():
    # Render navigation
    render_navbar()
    
    # Render authentication modal if needed
    if st.session_state.show_auth_modal:
        render_auth_modal()
    
    # Main content container
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Route to different pages based on current_page
    if st.session_state.current_page == "Home":
        render_home_page()
    elif st.session_state.current_page == "About":
        render_about_page()
    elif st.session_state.current_page == "Dashboard":
        render_dashboard_page()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Render footer
    render_footer()

# ─── Run the app ────────────────────────────────────
if __name__ == "__main__":
    main()