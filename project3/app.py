import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from fpdf import FPDF

# -----------------------
# Setup
# -----------------------
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

SYSTEM_PROMPT = """
You are a Posthumanist Privacy Analyst AI.
Your job is to analyze app permissions or excerpts from privacy policies only from the text provided by the user.

You are trained exclusively on Zuboff, Floridi, Braidotti, Hayles, and Yuk Hui.
Use concepts like datafication, autonomy erosion, surveillance capitalism, and behavioral surplus.

Privacy Risk Score Model (0–100):
- Data Sensitivity (40)
- Autonomy Impact (30)
- Surveillance Capitalism Weight (30)

Output:
1. Summary
2. Posthumanist Interpretation
3. Privacy Risk Score + breakdown
4. Recommendation
"""

model = genai.GenerativeModel(
    "gemini-2.5-flash-lite",
    system_instruction=SYSTEM_PROMPT
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
# Sidebar content
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

### 🔢 Scoring Model  
- **Data Sensitivity – 40%**  
- **Autonomy Impact – 30%**  
- **Surveillance Capitalism – 30%**

---

⚠️ *Philosophical analysis, not legal advice.*

Version **1.0**
""")

# -----------------------
# Main UI
# -----------------------
st.markdown(
    """
    <h1 style='text-align: center; font-size: 36px;'>
        🔒 Posthumanist Privacy Risk Analyzer
    </h1>
    <p style='text-align: center; font-size: 18px;'>
        Paste any privacy-policy text or app permissions for analysis.
    </p>
    """,
    unsafe_allow_html=True
)

user_input = st.text_area("Enter your text here:", height=200)

# Placeholder for the analysis result
analysis_output = None

# -----------------------
# Analyze button
# -----------------------
if st.button("Analyze", use_container_width=True):
    if not user_input.strip():
        st.warning("Please enter some text.")
    else:
        response = model.generate_content(user_input)
        analysis_output = response.text

        st.markdown("### 🔍 Analysis Result")
        st.write(analysis_output)

# -----------------------
# PDF Download Function
# -----------------------
def generate_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    for line in text.split("\n"):
        pdf.multi_cell(0, 10, line)

    filename = "privacy_analysis.pdf"
    pdf.output(filename)
    return filename

# -----------------------
# Show download button if analysis exists
# -----------------------
if "analysis_output" in locals() and analysis_output:
    pdf_file = generate_pdf(analysis_output)

    with open(pdf_file, "rb") as f:
        st.download_button(
            label="📄 Download Analysis as PDF",
            data=f,
            file_name="privacy_analysis.pdf",
            mime="application/pdf",
        )
