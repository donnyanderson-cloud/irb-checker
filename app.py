import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
import importlib.metadata
import random

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="BCS Research Review Portal", 
    page_icon="🏫", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- SIDEBAR: GLOBAL SETTINGS ---
with st.sidebar:
    st.header("⚙️ Configuration")

    # 1. THE MODE SELECTOR
    st.subheader("👥 Select User Mode")
    user_mode = st.radio(
        "Who are you?",
        ["AP Research Student", "External / Higher Ed Researcher"],
        captions=["For BCS High School Students", "For University/PhD Proposals"]
    )
    
    st.markdown("---")

    # 2. PRIVACY NOTICE
    st.warning("🔒 **Privacy:** Do not upload files containing real participant names or PII.")

    # 3. FILE NAMING GUIDE
    with st.expander("📂 File Naming Standards"):
        if user_mode == "AP Research Student":
            st.markdown("""
            **⚠️ GOOGLE DOCS USERS:**
            Please name your Google Doc using this format **before** downloading as PDF.
            
            **Required Format:**
            `Last name, First name - [Document Type]`
            
            **Copy/Paste Templates:**
            * `Smith, John - Research Proposal`
            * `McCall, Debbie - Survey - Interview Questions`
            * `Wolfe-Miller, LaDonna - Parent Permission Form`
            * `Jones, Tommy - Principal-District Permission Forms`
            """)
        else:
            st.markdown("""
            **For External Review:**
            Please include your Name, Institution, and Year:
            
            * `Lastname_Institution_Proposal_2025.pdf`
            * `Lastname_Institution_Instruments_2025.pdf`
            """)
    
    st.markdown("---")
    
    # 4. KEY MANAGEMENT
    api_key = None
    
    # Check for the list of keys (Primary Method for Classrooms)
    if "DISTRICT_KEYS" in st.secrets:
        key_pool = st.secrets["DISTRICT_KEYS"]
        district_key = random.choice(key_pool)
        api_key = district_key
        
        if user_mode == "AP Research Student":
            st.success(f"✅ District License Active")
            with st.expander("🚀 Performance Boost (Use Your Own Key)"):
                st.info("Classroom blocked? Use your own free key to bypass the wait.")
                st.link_button("1. Get Free API Key ↗️", "https://aistudio.google.com/app/apikey")
                user_key = st.text_input("Paste your personal key:", type="password")
                if user_key:
                    api_key = user_key
                    st.success("✅ Using Personal Key")
        else:
            st.success("✅ District License Active")

    # Fallback for Single Key (Legacy Method)
    elif "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
        if user_mode == "AP Research Student":
            st.success("✅ District License Active")
            with st.expander("🚀 Performance Boost (Use Your Own Key)"):
                st.info("Classroom blocked? Use your own free key.")
                st.link_button("1. Get Free API Key ↗️", "https://aistudio.google.com/app/apikey")
                user_key = st.text_input("Paste your personal key:", type="password")
                if user_key:
                    api_key = user_key
                    st.success("✅ Using Personal Key")
        else:
            st.success("✅ District License Active")

    else:
        st.markdown("### 🔑 Need an API Key?")
        st.info("System requires an API key.")
        st.link_button("1. Get Free API Key ↗️", "https://aistudio.google.com/app/apikey")
        api_key = st.text_input("Enter Google API Key", type="password")

    st.markdown("---")
    
    # 5. DIAGNOSTICS
    if user_mode == "AP Research Student":
        try:
            lib_ver = importlib.metadata.version("google-generativeai")
        except:
            lib_ver = "Unknown"
        st.caption(f"⚙️ System Version: {lib_ver}")

# --- HELPER FUNCTION: PDF TEXT EXTRACTION ---
def extract_text(uploaded_file):
    try:
        reader = PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        return f"Error reading PDF: {e}"

# ==========================================
# MODE A: AP RESEARCH STUDENT
# ==========================================
if user_mode == "AP Research Student":
    
    # --- HEADER WITH CUSTOM LOGO ---
    col_logo, col_text = st.columns([1, 8]) 
    
    with col_logo:
        try:
            st.image("APlogo.png", width=100)
        except:
            st.header("🛡️")
