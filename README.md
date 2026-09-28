# Privacy Risk Analyzer

An AI agent that reads app permissions or privacy policies and explains what they really mean for users. It combines Google Gemini with a structured scoring model grounded in information ethics, turning long legal text into a clear risk score, an explanation, and concrete recommendations.

## What it does

The app has two modes:

**User mode** helps people decide whether to trust an app. Paste a privacy policy or permission list, or upload a PDF, and get:
- A plain-language summary of the data being collected
- An interpretation of the risks through information-ethics theory
- A **Privacy Risk Score (0–100)** with a breakdown
- One concrete recommendation

**Company mode** helps organizations improve their practices. It returns prioritized, actionable recommendations for transparency, user autonomy, and ethical data handling.

Every analysis can be downloaded as a formatted **PDF report**.

## Scoring model

| Dimension | Weight | What it measures |
|---|---|---|
| Data Sensitivity | 40 pts | How personal or sensitive the collected data is |
| Autonomy Impact | 30 pts | How much the practices shape or limit user choices |
| Surveillance Capitalism | 30 pts | How much user data is turned into profit or behavioral prediction |

Lower scores mean a more privacy-respecting policy. The model is prompted to keep the three sub-scores consistent with the total.

## Theoretical grounding

The agent's analysis is constrained to concepts from contemporary information ethics and posthumanist thinkers: Shoshana Zuboff (surveillance capitalism), Luciano Floridi (infosphere ethics), Rosi Braidotti (posthuman subjectivity), N. Katherine Hayles (human–machine entanglement), and Yuk Hui (technodiversity).

## Tech stack

| Component | Technology |
|---|---|
| Interface | Streamlit |
| LLM | Google Gemini (`gemini-2.5-flash-lite`) with role-specific system prompts |
| PDF input | PyPDF2 |
| PDF reports | ReportLab |
| Config | python-dotenv, Streamlit secrets |

## Getting started

```bash
git clone https://github.com/qskenza/privacy-risk-analyzer.git
cd privacy-risk-analyzer
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Add your Gemini API key (get one at https://aistudio.google.com/apikey) in `.streamlit/secrets.toml`:

```toml
[general]
GOOGLE_API_KEY = "your-gemini-api-key"
```

Then run:

```bash
streamlit run app.py
```

A terminal version of the agent is also included. It reads the key from a `.env` file (`GOOGLE_API_KEY=...`):

```bash
python aiagent.py
```

## Limitations

This tool gives an AI-generated, philosophically framed analysis. It is **not legal advice**, and scores can vary between runs because they come from a language model.
