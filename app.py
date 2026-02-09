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

# ==========================================
# 🛑 ADMIN SECTION: DISTRICT STANDARDS
# ==========================================
# INSTRUCTION: PASTE THE TEXT OF YOUR NEW "REGULATIONS AND PROCEDURES" DOCUMENT
# BETWEEN THE TRIPLE QUOTES BELOW. THE AI WILL USE THIS AS THE SOURCE OF TRUTH.

DISTRICT_STANDARDS_TEXT = """
(PASTE YOUR NEW REGULATION TEXT HERE. DELETE THIS LINE AND PASTE THE CONTENT.
Examples of what should be here:
- The text defining prohibited topics.
- The text defining data destruction requirements.
- The text regarding parental consent.
The AI will read this exact text to make its decisions.)
"""

# ==========================================
# END ADMIN SECTION
# ==========================================

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

    # 3. APP UPDATES
    with st.expander("🆕 App Updates (v3.1)"):
        st.markdown("""
        **Latest Improvements:**
        * 🏆 **Exemplar Library:** Added model proposals to help you start.
        * 💡 **Pro Tips:** Added guidance on explicit policy citation.
        * 📜 **Live Standards Update:** The AI now screens strictly against the **newly revised** District Regulations document.
        * 📂 **Multi-File Uploads:** Support for multiple PDF uploads in the Proposal section.
        * 🎓 **Student-Friendly Tone:** Feedback is clear and encouraging.
        * 🧑‍🤝‍🧑 **Adult Consent Support:** Intelligent triage for Minor vs. Adult participants.
        """)

    # 4. FILE NAMING GUIDE (UPDATED WITH PRO TIP)
    with st.expander("📂 File Naming Standards"):
        st.info("💡 **Pro Tip for a Fast Pass:** The AI looks for *explicit* alignment. Don't just imply you will be safe; clearly state: *'In accordance with Policy 6.4001, I will...'*" )
        
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

    # 5. RESOURCES (UPDATED WITH EXEMPLARS)
    with st.expander("📚 Helpful Resources"):
        st.markdown("""
        **Essential Documents:**
        * [📜 Board Policy 6.4001](https://tsba.net/blount-county-board-of-education-policy-manual/)
        * [🏆 Model Proposal Examples](https://drive.google.com/) *(Ask Mr. Anderson for Link)*
        """)
    
    st.markdown("---")
    
    # 6. KEY MANAGEMENT
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
    
    # 7. DIAGNOSTICS
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
            
    with col_text:
        st.title("AP Research IRB Self-Check Tool")
    
    # --- WORKFLOW GRAPHIC ---
    with st.expander("🗺️ View Research Workflow Map"):
        st.graphviz_chart("""
        digraph {
            rankdir=TB;
            node [shape=box, style="filled,rounded", fontname="Sans-Serif"];
            
            # Colors
            node [fillcolor="#e1f5fe" color="#01579b"]; # Student Blue
            
            # Phase 1
            subgraph cluster_0 {
                label = "Phase 1: Development";
                style=dashed; color=grey;
                Draft [label="📝 Draft Proposal"];
                Inst [label="Create Instruments"];
                Draft -> Inst;
            }

            # Phase 2
            subgraph cluster_1 {
                label = "Phase 2: AI Compliance Check";
                style=filled; color="#e8f5e9";
                
                node [fillcolor="#c8e6c9" color="#2e7d32"]; # AI Green
                Upload [label="🚀 Upload to AI Portal"];
                Check [label="⚠️ AI Review"];
                Pass [label="✅ Clean Bill of Health"];
                Fail [label="❌ Revision Needed"];
                
                Inst -> Upload;
                Upload -> Check;
                Check -> Pass;
                Check -> Fail;
                Fail -> Upload [label="Fix & Re-upload"];
            }

            # Phase 3
            subgraph cluster_2 {
                label = "Phase 3: School IRB Approval";
                style=filled; color="#fff9c4";
                
                node [fillcolor="#fff59d" color="#fbc02d"]; # School Yellow
                Submit [label="📧 Submit to School IRB"];
                Review [label="School Committee Review"];
                Approve [label="📜 Approval Letter"];
                
                Pass -> Submit;
                Submit -> Review;
                Review -> Approve;
                Review -> Fail [label="Denied"];
            }

            # Phase 4
            subgraph cluster_3 {
                label = "Phase 4: Implementation";
                style=filled; color="#f3e5f5";
                
                node [fillcolor="#e1bee7" color="#7b1fa2"]; # School Purple
                Principal [label="📍 Contact Principal"];
                Start [label="📊 Begin Data Collection"];
                
                Approve -> Principal;
                Principal -> Start [label="Site Permission"];
            }
        }
        """)
    
    st.markdown("**For BCS Students:** Screen your research documents against **Policy 6.4001** and **AP Ethics Standards**.&nbsp; Check the sidebar resource to **confirm file-naming standards** for each of your files.")

    document_types = [
        "Research Proposal",
        "Survey / Interview Questions",
        "Participant Consent Forms (Parent or Adult)", 
        "Principal/District Permission Forms"
    ]
    selected_docs = st.multiselect("Select documents to screen:", document_types, default=["Research Proposal"])
    
    student_inputs = {}

    if "Research Proposal" in selected_docs:
        st.markdown("### 1. Research Proposal")
        prop_files = st.file_uploader("Upload Proposal (PDFs)", type="pdf", key="ap_prop", accept_multiple_files=True)
        if prop_files:
            combined_text = ""
            for f in prop_files:
                combined_text += extract_text(f) + "\n\n"
            student_inputs["PROPOSAL"] = combined_text

    if "Survey / Interview Questions" in selected_docs:
        st.markdown("### 2. Survey or Interview Script")
        input_method = st.radio("Input Method:", ["Paste Text", "Upload PDF"], horizontal=True, key="ap_survey_toggle")
        
        if input_method == "Paste Text":
            st.info("💡 Tip: For Google Forms, Ctrl+A -> Copy -> Paste here.")
            text = st.text_area("Paste text here:", height=200, key="ap_survey_text")
            if text: student_inputs["SURVEY"] = text
        else:
            file = st.file_uploader("Upload Survey PDF", type="pdf", key="ap_survey_file")
            if file: student_inputs["SURVEY"] = extract_text(file)

    if "Participant Consent Forms (Parent or Adult)" in selected_docs:
        st.markdown("### 3. Participant Consent Forms")
        st.caption("Upload Parent Permission (for Minors) OR Adult Consent (for 18+).")
        file = st.file_uploader("Upload Consent PDF", type="pdf", key="ap_consent")
        if file: student_inputs["CONSENT_FORMS"] = extract_text(file)

    if "Principal/District Permission Forms" in selected_docs:
        st.markdown("### 4. Principal/District Permission Forms")
        file = st.file_uploader("Upload Permission Form (PDF)", type="pdf", key="ap_perm")
        if file: student_inputs["PERMISSION_FORM"] = extract_text(file)

    # --- SYSTEM PROMPT (STUDENT) ---
    system_prompt = f"""
    ROLE: A helpful, encouraging AP Research Mentor and Compliance Guide.
    
    INSTRUCTION: Review the student proposal for compliance with Policy 6.4001, AP Ethics, and the specific District Standards provided below.
    
    **TONE GUIDE:**
    * Be clear, encouraging, and supportive (like a teacher helper).
    * Avoid robotic or overly legalistic language.
    * Use "We" and "You".
    
    **REVIEW STRATEGY:**
    1. **SUBJECT TRIAGE:** Determine if the participants are **MINORS** (Students <18) or **ADULTS** (Teachers/Community 18+).
       - IF MINORS: Check for "Parent Permission Form".
       - IF ADULTS: Check for "Adult Informed Consent Form" (Do NOT ask for Parent Permission).
    2. **CHECK AGAINST SOURCE:** Compare the student's work specifically against the 'DISTRICT_STANDARDS' text provided below.
    3. **EDUCATIONAL RATIONALE:** Explain the "Why" simply.
    
    **STRICT CONSTRAINTS:** 1. Do NOT rewrite the student's text.
    2. **SCOPE LIMITATION:** Do NOT critique grammar or research quality. Focus ONLY on regulatory compliance.
    
    **SOURCE OF TRUTH (DISTRICT STANDARDS):**
    \"\"\"{DISTRICT_STANDARDS_TEXT}\"\"\"
    
    **OUTPUT FORMAT:**
    - STATUS: [✅ PASS] or [❌ REVISION NEEDED]
    - ACTION PLAN:
      * **[Action Item 1]:** [Clear, simple instruction]
        * *Why is this needed?* "[Simple explanation citing the Policy text above]"
    """

# ==========================================
# MODE B: EXTERNAL / HIGHER ED RESEARCHER
# ==========================================
else:
    st.title("🏛️ External Research Proposal Review")
    st.info("### 📋 Criteria for External Proposals")
    
    st.markdown("All research requests involving Blount County Schools (BCS) are critiqued against District Standards (Policy 6.4001).&nbsp; Check the sidebar resource to **confirm file-naming standards** for each of your files.")
    
    st.info("You may upload multiple PDF files for each section.")

    external_inputs = {}
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 1. Main Proposal Packet")
        st.caption("Purpose, Methodology, Benefit, Logistics.")
        prop_files = st.file_uploader("Upload Full Proposal (PDFs)", type="pdf", key="ext_prop", accept_multiple_files=True)
        if prop_files:
            combined_text = ""
            for f in prop_files:
                combined_text += extract_text(f) + "\n\n"
            external_inputs["FULL_PROPOSAL"] = combined_text

    with col2:
        st.markdown("### 2. Instruments & Consents")
        st.caption("Surveys, Protocols, Consent Forms.")
        inst_files = st.file_uploader("Upload Instruments (PDFs)", type="pdf", key="ext_inst", accept_multiple_files=True)
        if inst_files:
            combined_text = ""
            for f in inst_files:
                combined_text += extract_text(f) + "\n\n"
            external_inputs["INSTRUMENTS"] = combined_text

    # --- SYSTEM PROMPT (EXTERNAL) ---
    system_prompt = f"""
    ROLE: Research Committee Reviewer for Blount County Schools (BCS).
    TASK: Analyze the external research proposal against Board Policy 6.4001 and the updated Regulations provided below.

    **REVIEW STRATEGY:**
    1. **SUBJECT TRIAGE:** Determine if the participants are **MINORS** (Students <18) or **ADULTS** (Teachers/Staff).
       - IF MINORS: Check for "Parent Permission Form".
       - IF ADULTS: Check for "Adult Informed Consent Form".
    2. **CHECK AGAINST SOURCE:** Compare the proposal specifically against the 'DISTRICT_STANDARDS' text provided below.
    3. **EDUCATIONAL RATIONALE:** Explain **WHY** the revision is needed by citing the standards below.

    **STRICT CONSTRAINTS:**
    1. Do not provide specific rewrite examples or sample verbiage. 
    2. **SCOPE LIMITATION:** Do NOT critique grammar or research quality. Focus ONLY on regulatory compliance.

    **SOURCE OF TRUTH (DISTRICT STANDARDS):**
    \"\"\"{DISTRICT_STANDARDS_TEXT}\"\"\"

    OUTPUT FORMAT:
    - STATUS: [✅ RECOMMEND FOR REVIEW] or [❌ REVISION NEEDED]
    - ACTION PLAN & RATIONALE:
      * **[Action Step 1]:** [Clear instruction to fix missing items]
        * *Rationale:* "[Brief explanation citing the Standard text]"
    """
    
    student_inputs = external_inputs

# ==========================================
# EXECUTION LOGIC
# ==========================================
if st.button("Run Compliance Check"):
    if not api_key:
        st.error("⚠️ Please enter a Google API Key in the sidebar.")
    elif not student_inputs:
        st.warning("Please upload at least one document.")
    else:
        # 1. SETUP
        status = st.empty() 
        status.info("🔌 Connecting to AI Services...")
        genai.configure(api_key=api_key)
        
        # 2. CONFIGURATION
        generation_config = {
            "temperature": 0.3, 
            "top_p": 0.95, 
            "top_k": 40, 
            "max_output_tokens": 8192
        }
        
        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_ONLY_HIGH"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_ONLY_HIGH"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_ONLY_HIGH"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_ONLY_HIGH"},
        ]

        # 3. PREPARING TEXT
        status.info("📄 Reading your PDF files...")
        user_message = f"{system_prompt}\n\nAnalyze the following documents:\n"
        
        total_chars = 0
        for doc_type, content in student_inputs.items():
            clean_content = str(content)[:40000]
            total_chars += len(clean_content)
            user_message += f"\n--- {doc_type} ---\n{clean_content}\n" 
        
        status.info(f"📤 Sending {total_chars} characters to Gemini AI...")

        # 4. MODEL SELECTOR
        target_models = [
            "gemini-2.5-flash-lite",      # 🥇 Confirmed in your list
            "gemini-flash-lite-latest",   # 🥈 Alias for the above
            "gemini-2.0-flash-lite",      # 🥉 Fallback Lite model
            "gemini-2.5-flash"            # 🚨 LAST RESORT (Low 20/day limit)
        ]

        response = None
        success = False
        connected_model = ""

        with st.spinner("🤖 Connecting..."):
            for model_name in target_models:
                try:
                    model = genai.GenerativeModel(
                        model_name=model_name, 
                        generation_config=generation_config, 
                        safety_settings=safety_settings
                    )
                    response = model.generate_content(user_message)
                    success = True
                    connected_model = model_name
                    break 
                except Exception as e:
                    continue

        # 5. DISPLAY RESULTS
        if success and response:
            st.toast(f"✅ Connected to: {connected_model}", icon="⚡")
            status.success("✅ Analysis Complete!")
            st.markdown("---")
            st.markdown(response.text)
            
            # --- CONDITIONAL NEXT STEPS ---
            st.markdown("---")
            st.subheader("📬 Next Steps")
            
            if user_mode == "AP Research Student":
                st.success("""
                **✅ If all of your artifacts have passed:**
                1. Submit your screened files to your **AP Research Teacher / School IRB** for final approval.
                2. Ensure all file naming conventions are correct before submission.
                """)
                st.error("""
                **❌ If your Status is REVISION NEEDED:**
                * Review the "Action Plan" above.
                * Edit your documents to address the missing policy requirements.
                * **Re-run this check** until you get a PASS status.
                """)
            else: 
                # External Researchers usually still need District Approval
                st.success("""
                **✅ If all of your artifacts have passed:**
                Please email your screened files to Blount County Schools (**research@blountk12.org**) for final approval. 
                *⚠️ Make sure that all file sharing options have been addressed prior to your email submission.*
                """)
                st.error("""
                **❌ If the Analysis says "REVISION NEEDED":**
                Please correct the items listed in the checklist above before emailing the district. 
                **Non-compliant proposals will be automatically returned.**
                """)
        else:
            status.error("❌ Connection Failed")
            st.error("""
            **All models failed.** Please check your Quota usage at https://ai.google.dev/usage. 
            You may need to create a new API Key if your daily limit is reached.
            """)
