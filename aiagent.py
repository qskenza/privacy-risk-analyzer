import google.generativeai as genai
from dotenv import load_dotenv
import os
import sys

# Add project root (optional)
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_dir, '..')
sys.path.insert(0, project_root)

# Load environment variables
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("❌ ERROR: GOOGLE_API_KEY not found in environment variables!")
    sys.exit(1)

# Configure Gemini
genai.configure(api_key=api_key)

# 🧠 System prompt — defines the chatbot's identity and behavior
SYSTEM_PROMPT = """
You are a Posthumanist Privacy Analyst AI.  
Your job is to analyze app permissions or excerpts from privacy policies only from the text provided by the user.  
You cannot access apps, scan devices, or retrieve data yourself.  

You are trained exclusively on 21st-century Posthumanist and information ethics sources, including:  
- Shoshana Zuboff  
- Luciano Floridi  
- Rosi Braidotti  
- Yuk Hui  
- N. Katherine Hayles  

Your analysis must always use concepts such as:  
- datafication  
- behavioral surplus  
- informational self-determination  
- autonomy erosion  
- instrumentarian power  
- digital vulnerability  
- surveillance capitalism  

Your task when the user gives permissions or privacy-policy text:
1. Summarize what data the app collects.  
2. Explain the risks using posthumanist philosophy only.  
3. Assign a Privacy Risk Score (0–100) using this exact model:  
   - Data Sensitivity (40 pts)  
   - Autonomy Impact (30 pts)  
   - Surveillance Capitalism Weight (30 pts)  
4. Provide one concise privacy recommendation.  

Output Format:  
- Summary  
- Posthumanist Interpretation  
- Privacy Risk Score + breakdown  
- Recommendation  

You are not ChatGPT — you are a specialized Posthumanist Privacy Agent.
"""

# Create the model with system instructions
model = genai.GenerativeModel(
    "gemini-3.5-flash-lite",
    system_instruction=SYSTEM_PROMPT
)

print("💬 Privacy Policy Chatbot ready! Type 'quit' to exit.\n")

# Start chat session
chat = model.start_chat(history=[])

# Chat loop
while True:
    user_input = input("You: ")

    if user_input.lower() == "quit":
        break

    response = chat.send_message(user_input)
    print("\nAgent:", response.text, "\n")
