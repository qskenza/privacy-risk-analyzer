import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.units import cm, inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib import colors
from io import BytesIO
import re
from datetime import datetime

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
# Enhanced PDF Download Function
# -----------------------
def generate_pdf(text):
    """Generate a beautifully formatted PDF with proper styling"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=A4,
        rightMargin=2*cm, 
        leftMargin=2*cm,
        topMargin=2.5*cm, 
        bottomMargin=2.5*cm
    )
    
    # Create custom styles
    styles = getSampleStyleSheet()
    
    # Title style
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    # Heading style
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#2c5aa0'),
        spaceAfter=12,
        spaceBefore=20,
        fontName='Helvetica-Bold',
        borderPadding=5,
        leftIndent=0
    )
    
    # Body text style
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=11,
        leading=16,
        textColor=colors.HexColor('#333333'),
        alignment=TA_JUSTIFY,
        fontName='Helvetica',
        spaceAfter=10
    )
    
    # Bullet point style
    bullet_style = ParagraphStyle(
        'CustomBullet',
        parent=body_style,
        leftIndent=20,
        bulletIndent=10,
        fontSize=10,
        leading=14
    )
    
    # Score style (highlighted)
    score_style = ParagraphStyle(
        'ScoreStyle',
        parent=body_style,
        fontSize=12,
        textColor=colors.HexColor('#c41e3a'),
        fontName='Helvetica-Bold',
        spaceAfter=15
    )
    
    elements = []
    
    # Add header
    elements.append(Paragraph("🔒 Posthumanist Privacy Risk Analysis", title_style))
    elements.append(Spacer(1, 0.3*cm))
    
    # Add date
    date_text = f"<i>Generated on {datetime.now().strftime('%B %d, %Y at %H:%M')}</i>"
    date_style = ParagraphStyle('DateStyle', parent=body_style, fontSize=9, textColor=colors.grey, alignment=TA_CENTER)
    elements.append(Paragraph(date_text, date_style))
    elements.append(Spacer(1, 0.8*cm))
    
    # Add decorative line
    line_table = Table([['']], colWidths=[doc.width])
    line_table.setStyle(TableStyle([
        ('LINEABOVE', (0, 0), (-1, 0), 2, colors.HexColor('#2c5aa0')),
    ]))
    elements.append(line_table)
    elements.append(Spacer(1, 0.5*cm))
    
    # Parse and format the analysis text
    lines = text.split('\n')
    
    for line in lines:
        line = line.strip()
        
        if not line:
            elements.append(Spacer(1, 0.2*cm))
            continue
        
        # Detect headings (lines with certain keywords or markdown-style headers)
        if any(keyword in line.lower() for keyword in ['summary', 'interpretation', 'score', 'recommendation', 'breakdown']):
            # Remove markdown symbols if present
            clean_line = re.sub(r'^#+\s*', '', line)
            clean_line = re.sub(r'\*\*', '', clean_line)
            elements.append(Paragraph(clean_line, heading_style))
        
        # Detect score values (lines with numbers and /)
        elif re.search(r'\d+/\d+|\d+\s*out of\s*\d+', line):
            elements.append(Paragraph(line, score_style))
        
        # Detect bullet points
        elif line.startswith(('-', '•', '*')):
            clean_line = re.sub(r'^[-•*]\s*', '• ', line)
            elements.append(Paragraph(clean_line, bullet_style))
        
        # Regular paragraph
        else:
            # Clean up markdown bold
            clean_line = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', line)
            elements.append(Paragraph(clean_line, body_style))
    
    # Add footer space
    elements.append(Spacer(1, 1*cm))
    
    # Add footer note
    footer_text = "<i>Note: This is a philosophical analysis based on posthumanist theory and not legal advice.</i>"
    footer_style = ParagraphStyle('FooterStyle', parent=body_style, fontSize=8, textColor=colors.grey, alignment=TA_CENTER)
    elements.append(Paragraph(footer_text, footer_style))
    
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer

# -----------------------
# Show download button if analysis exists
# -----------------------
if analysis_output:
    pdf_buffer = generate_pdf(analysis_output)

    st.download_button(
        label="📄 Download Analysis as PDF",
        data=pdf_buffer,
        file_name="privacy_analysis.pdf",
        mime="application/pdf",
        use_container_width=True
    )