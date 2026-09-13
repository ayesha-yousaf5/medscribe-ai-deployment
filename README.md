# 🩺 MedScribe AI

An agentic radiology assistant that reads chest X-rays, detects abnormalities,
explains its reasoning with heatmaps, writes a structured clinical report, and
produces a plain-language patient summary in the patient's own language.

---

## ✨ Features

- 🖼️ Chest X-ray analysis using a fine-tuned ResNet18 (NORMAL / PNEUMONIA)
- 🔥 Grad-CAM heatmap showing where the AI looked
- 🧠 Agentic workflow — the LLM decides which tools to call, in what order
- 📋 Structured clinical report (findings → impression → recommendation → urgency)
- 🚨 Urgency triage (routine / urgent / critical) with auto-escalation
- 💬 Patient-friendly summary in English, Urdu, Spanish, Arabic, or Hindi
- 🧭 Multi-tab UI — Doctor View, Agent Trace, Patient View, About

---

## 🏗️ Architecture

User uploads X-ray + picks language
        ↓
AGENT (LangGraph ReAct + `openai/gpt-oss-120b` via Groq)
        ↓
  decides to call:
    1. detect_findings        → ResNet18 classifies NORMAL / PNEUMONIA
    2. write_clinical_report  → structured report
    3. assess_urgency         → routine / urgent / critical
    4. escalate_to_doctor     → only if critical
    5. write_patient_summary  → plain language + translation
        ↓
Streamlit UI:
    🩺 Diagnosis  |  🧠 Agent Trace  |  💬 Patient View  |  ℹ️ About

---

## 🧰 Tech Stack

| Layer | Tool |
|---|---|
| Frontend | Streamlit (tabbed UI) |
| CV Model | Fine-tuned ResNet18 checkpoint |
| Explainability | Grad-CAM |
| Agent Framework | LangGraph (ReAct) |
| LLM | `openai/gpt-oss-120b` via Groq |
| Language | Python 3.11 |
| Deployment | Streamlit Community Cloud |
| Model hosting | Hugging Face (`TabasumDev/medscribe-resnet18`) |

---

## 📁 Project Structure

    medscribe-ai/
    ├── app.py              # Streamlit UI (tabbed)
    ├── orchestrator.py     # LangGraph ReAct agent
    ├── tools.py            # Agent tools
    ├── vision.py           # ResNet18 + Grad-CAM
    ├── agent.py            # LLM report generation
    ├── report.py           # Output formatting
    ├── prompts.py          # LLM prompts
    ├── settings.py         # Config + env loading
    ├── requirements.txt
    ├── fonts/              # Bundled Urdu-capable Noto font
    ├── packages.txt        # Streamlit Cloud system packages
    └── outputs/            # Generated results + traces

---

## 🚀 Setup

### 1. Clone & enter
    git clone <your-repo-url>
    cd medscribe-ai

### 2. Create virtual environment (Python 3.11)
    py -3.11 -m venv venv
    venv\Scripts\activate      # Windows
    source venv/bin/activate   # macOS/Linux

### 3. Install dependencies
    pip install -r requirements.txt

### 4. Add your Groq API key
Create a `.env` file:

    GROQ_API_KEY=your_groq_key_here

Get a free key at https://console.groq.com/keys

### 5. Run the app
    streamlit run app.py

Open http://localhost:8501

### Streamlit Community Cloud

Deploy `ayesha-yousaf5/medscribe-ai-deployment` with `app.py` as the main
file. Add this secret under the app settings:

    GROQ_API_KEY = "your_groq_key_here"

The ResNet checkpoint is not committed to GitHub. If the local
`models/medscribe_model_a_resnet18.pth` file is unavailable, `vision.py`
downloads it automatically from the public Hugging Face repository
`TabasumDev/medscribe-resnet18`.

The Urdu-capable font is bundled at `fonts/NotoNaskhArabic.ttf`, so Urdu PDF
export does not depend on a platform-specific font installation.

---

## 🧪 Usage

1. Upload a chest X-ray (JPG/PNG)
2. Select the patient's language
3. Click **Analyze**
4. Explore the tabs:
   - **🩺 Diagnosis** — scan, heatmap, urgency, clinical report
   - **🧠 Agent Trace** — every tool the agent decided to call
   - **💬 Patient View** — plain-language summary in the chosen language
   - **ℹ️ About** — tech details and disclaimer

---

## 🧠 How the Agent Works

The agent is a **ReAct loop** built with LangGraph. Given a scan, it:

1. Calls `detect_findings` to run the ResNet18 model on the image
2. Calls `write_clinical_report` with the findings
3. Calls `assess_urgency` on the report
4. If urgency is **critical**, calls `escalate_to_doctor`
5. Calls `write_patient_summary` for the translated summary

The **order isn't hardcoded** — the LLM decides. The **Agent Trace** tab shows
exactly what it chose to do, in order, with inputs.

---

## ⚠️ Disclaimer

This project is a **proof of concept** built for a hackathon.
It is **not a medical device** and must **not** be used for real clinical diagnosis.
Always consult a qualified radiologist.

---

## 📜 License

MIT