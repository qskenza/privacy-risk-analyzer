import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib import colors
from io import BytesIO
import re
from datetime import datetime
import PyPDF2

# -----------------------
# Setup
# -----------------------
load_dotenv()
api_key = st.secrets["general"]["GOOGLE_API_KEY"]
genai.configure(api_key=api_key)

# -----------------------
# System Prompts
# -----------------------
USER_SYSTEM_PROMPT = """
You are a Posthumanist Privacy Analyst AI.
Your job is to analyze app permissions or excerpts from privacy policies only from the text provided by the user.
Every part of the output needs to be concise and clear.

You are trained exclusively on Zuboff, Floridi, Braidotti, Hayles, and Yuk Hui.
Use concepts like datafication, autonomy erosion, surveillance capitalism, and behavioral surplus.

Privacy Risk Score Model (0–100):
- Data Sensitivity (40 points maximum)
- Autonomy Impact (30 points maximum)
- Surveillance Capitalism (30 points maximum)

IMPORTANT: The three component scores must ADD UP to equal the Overall Score.
For example, if Overall Score is 85/100, the components might be:
• Data Sensitivity: 35/40
• Autonomy Impact: 25/30
• Surveillance Capitalism: 25/30
Total: 35 + 25 + 25 = 85

Output format (use exactly this structure with line breaks):

**SUMMARY**

[Provide a concise summary here]

**POSTHUMANIST INTERPRETATION**

- Key point 1
- Key point 2
- Key point 3

**PRIVACY RISK SCORE**

Overall Score: [total]/100

**Score Breakdown:**

• Data Sensitivity (40%): [score]/40 - [brief explanation]

• Autonomy Impact (30%): [score]/30 - [brief explanation]

• Surveillance Capitalism (30%): [score]/30 - [brief explanation]

Note: Ensure the three component scores add up exactly to the Overall Score.
"""

COMPANY_SYSTEM_PROMPT = """
You are a Posthumanist Privacy Analyst AI.
Your job is to analyze a company's privacy policy or data practices and provide **only actionable recommendations** to improve user experience, privacy transparency, and ethical handling of data.

Use concepts from Zuboff, Floridi, Braidotti, Hayles, and Yuk Hui.
Frame suggestions around:
- Digital autonomy
- Ethical tech design
- User empowerment

Output format (use exactly this structure with line breaks after each title and between bullet points):

**ACTION 1: [Title of recommendation]**

• [First key point or detail]

• [Second key point or detail]

• [Third key point if needed]

**ACTION 2: [Title of recommendation]**

• [First key point or detail]

• [Second key point or detail]

• [Third key point if needed]

**ACTION 3: [Title of recommendation]**

• [First key point or detail]

• [Second key point or detail]

• [Third key point if needed]

[Continue with additional actions as needed, always maintaining line breaks after titles and between bullet points]
"""

# -----------------------
# Create models
# -----------------------
user_model = genai.GenerativeModel(
    "gemini-2.5-flash-lite",
    system_instruction=USER_SYSTEM_PROMPT
)

company_model = genai.GenerativeModel(
    "gemini-2.5-flash-lite",
    system_instruction=COMPANY_SYSTEM_PROMPT
)

# -----------------------
# Streamlit page config
# -----------------------
st.set_page_config(
    page_title="Posthumanist Privacy Agent",
    page_icon="🔒",
    layout="centered",
)

# -----------------------
# Sidebar
# -----------------------
with st.sidebar:
    st.title("📘 About This Agent")
    st.markdown("""
This AI analyzes privacy policies through posthumanist theory:

- **Zuboff** – surveillance capitalism  
- **Floridi** – infosphere ethics  
- **Braidotti** – posthuman subjectivity  
- **Hayles** – human–machine entanglement  
- **Yuk Hui** – technodiversity  

---

### 🔢 Scoring Model (User Mode)
- **Data Sensitivity – 40%**  
- **Autonomy Impact – 30%**  
- **Surveillance Capitalism – 30%**

Privacy Risk Score (0–100)
- **Lower scores indicate safer, more privacy-respecting policies.**
- **Higher scores indicate greater risks and potential privacy concerns.**

---

⚠️ *Philosophical analysis, not legal advice.*  
Version **2.1**
""")

# -----------------------
# Helper functions
# -----------------------
def extract_text_from_pdf(file):
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        st.error(f"Error reading PDF: {str(e)}")
        return None

def process_uploaded_file(uploaded_file):
    if uploaded_file is None:
        return None
    ext = uploaded_file.name.split('.')[-1].lower()
    if ext == 'pdf':
        return extract_text_from_pdf(uploaded_file)
    else:
        st.error(f"Unsupported file type: {ext}. Please upload a PDF.")
        return None

def generate_pdf(text):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            rightMargin=2*cm, leftMargin=2*cm,
                            topMargin=2.5*cm, bottomMargin=2.5*cm)
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=24,
                                 textColor=colors.HexColor('#1a1a1a'), alignment=TA_CENTER)
    body_style = ParagraphStyle('CustomBody', parent=styles['Normal'], fontSize=11,
                                leading=16, textColor=colors.HexColor('#333333'), alignment=TA_JUSTIFY)
    bullet_style = ParagraphStyle('CustomBullet', parent=body_style, leftIndent=20, bulletIndent=10, fontSize=10)
    
    elements = [Paragraph("🔒 Posthumanist Privacy Analysis", title_style), Spacer(1, 0.3*cm)]
    
    lines = text.split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            elements.append(Spacer(1, 0.2*cm))
            continue
        # For company mode, start each line with Action N: if missing
        if line.startswith("Action") or line.startswith(("-", "•", "*")):
            elements.append(Paragraph(line, bullet_style))
        else:
            elements.append(Paragraph(line, body_style))
    
    doc.build(elements)
    buffer.seek(0)
    return buffer

# -----------------------
# Main UI
# -----------------------
st.markdown("""
<h1 style='text-align: center; font-size: 36px;'>🔒 Posthumanist Privacy Risk Analyzer</h1>
<p style='text-align: center; font-size: 18px;'>Paste text or upload a PDF for analysis.</p>
""", unsafe_allow_html=True)

mode = st.radio("Select Mode:", ["USER", "COMPANY"])

tab1, tab2 = st.tabs(["📝 Paste Text", "📁 Upload File"])
user_text = None

with tab1:
    user_input = st.text_area("Enter privacy policy or app permissions:", height=250)
    if user_input.strip():
        user_text = user_input

with tab2:
    uploaded_file = st.file_uploader("Upload a PDF privacy policy", type=['pdf'])
    if uploaded_file:
        st.success(f"✅ Uploaded: {uploaded_file.name}")
        with st.spinner("Extracting text..."):
            extracted_text = process_uploaded_file(uploaded_file)
            if extracted_text:
                user_text = extracted_text
                with st.expander("Preview extracted text"):
                    st.text(extracted_text[:500] + ("..." if len(extracted_text) > 500 else ""))

analysis_output = None

def format_output(text, mode):
    """Format the output with larger, bold titles"""
    if mode == "USER":
        # Replace section headers with larger HTML styled headers
        text = text.replace("**SUMMARY**", '<h2 style="font-size: 28px; font-weight: bold; margin-top: 20px; margin-bottom: 10px;">📋 SUMMARY</h2>')
        text = text.replace("**POSTHUMANIST INTERPRETATION**", '<h2 style="font-size: 28px; font-weight: bold; margin-top: 30px; margin-bottom: 10px;">🔍 POSTHUMANIST INTERPRETATION</h2>')
        text = text.replace("**PRIVACY RISK SCORE**", '<h2 style="font-size: 28px; font-weight: bold; margin-top: 30px; margin-bottom: 10px;">⚠️ PRIVACY RISK SCORE</h2>')
        text = text.replace("**Score Breakdown:**", '<h3 style="font-size: 22px; font-weight: bold; margin-top: 15px; margin-bottom: 10px;">Score Breakdown:</h3>')
    else:
        # Replace ACTION headers with larger HTML styled headers
        import re
        text = re.sub(r'\*\*ACTION (\d+): ([^*]+)\*\*', 
                     r'<h2 style="font-size: 26px; font-weight: bold; margin-top: 30px; margin-bottom: 10px;">🎯 ACTION \1: \2</h2>', 
                     text)
    return text

if st.button("Analyze", use_container_width=True):
    if not user_text or not user_text.strip():
        st.warning("⚠️ Please provide text or upload a PDF.")
    else:
        with st.spinner("Processing with AI..."):
            if mode == "USER":
                response = user_model.generate_content(user_text)
                analysis_output = response.text
                output_title = "## 🔍 Analysis Result"
            else:
                response = company_model.generate_content(user_text)
                analysis_output = response.text
                output_title = "## 📌 Actionable Recommendations"
        
        st.markdown(output_title)
        # Format and display with larger titles
        formatted_output = format_output(analysis_output, mode)
        st.markdown(formatted_output, unsafe_allow_html=True)
        # Store the original for PDF generation
        analysis_output = analysis_output

if analysis_output:
    pdf_buffer = generate_pdf(analysis_output)
    st.download_button(
        label="📄 Download Analysis as PDF",
        data=pdf_buffer,
        file_name="privacy_analysis.pdf",
        mime="application/pdf",
        use_container_width=True
    )