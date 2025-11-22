import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

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

# Create model with system prompt
model = genai.GenerativeModel(
    "gemini-2.5-flash-lite",
    system_instruction=SYSTEM_PROMPT
)

st.set_page_config(page_title="Posthumanist Privacy Agent", page_icon="🔒")

st.title("🔒 Posthumanist Privacy Risk Analyzer")
st.write("Paste app permissions or privacy-policy text below.")

user_input = st.text_area("Enter the text here:")

if st.button("Analyze"):
    if not user_input.strip():
        st.warning("Please enter some text.")
    else:
        response = model.generate_content(user_input)
        st.markdown("### 🔍 Analysis Result")
        st.write(response.text)
