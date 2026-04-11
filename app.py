"""
DentEdTech™ Evidence Engine
An educational AI platform for medicine, dentistry, and pharmacology students
at Manchester University. Built on the REAL-AI framework principles.

© DentEdTech™ - All Rights Reserved
"""

import streamlit as st
import anthropic
import json
import re
from datetime import datetime

# ─── Page Config ───
st.set_page_config(
    page_title="DentEdTech™ Evidence Engine",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ───
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&display=swap');

:root {
    --primary: #1B4D3E;
    --primary-light: #2D7A5F;
    --accent: #D4A853;
    --accent-light: #E8C97A;
    --bg-dark: #0F1A16;
    --bg-card: #162520;
    --bg-card-hover: #1C3029;
    --text-primary: #E8EDE9;
    --text-secondary: #9BAFA3;
    --text-muted: #6B8577;
    --border: #2D4A3E;
    --danger: #C44B4B;
    --warning: #D4A853;
    --success: #4CAF7D;
    --video-red: #E04040;
    --recall-purple: #9B72CF;
}

.stApp {
    background-color: var(--bg-dark) !important;
    color: var(--text-primary) !important;
    font-family: 'DM Sans', sans-serif !important;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

.main-header {
    text-align: center;
    padding: 2rem 1rem 1.5rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 2rem;
}
.main-header h1 {
    font-family: 'DM Serif Display', serif !important;
    font-size: 2.4rem !important;
    color: var(--text-primary) !important;
    margin: 0 !important;
    letter-spacing: -0.02em;
}
.main-header .tagline {
    font-size: 0.95rem;
    color: var(--text-secondary);
    margin-top: 0.3rem;
    font-style: italic;
}
.brand-accent { color: var(--accent) !important; }

section[data-testid="stSidebar"] {
    background-color: var(--bg-card) !important;
    border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] .stMarkdown p,
section[data-testid="stSidebar"] .stMarkdown li,
section[data-testid="stSidebar"] label {
    color: var(--text-secondary) !important;
    font-family: 'DM Sans', sans-serif !important;
}
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: var(--text-primary) !important;
    font-family: 'DM Serif Display', serif !important;
}

.mode-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    transition: all 0.3s ease;
}
.mode-card:hover {
    border-color: var(--accent);
    background: var(--bg-card-hover);
}
.mode-card h3 {
    font-family: 'DM Serif Display', serif !important;
    color: var(--text-primary) !important;
    margin-top: 0 !important;
    font-size: 1.2rem !important;
}
.mode-card p {
    color: var(--text-secondary) !important;
    font-size: 0.88rem !important;
    line-height: 1.5 !important;
}

.pillar-badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    margin-right: 6px;
    margin-bottom: 4px;
}
.pillar-r { background: rgba(76, 175, 125, 0.15); color: #4CAF7D; border: 1px solid rgba(76, 175, 125, 0.3); }
.pillar-e { background: rgba(212, 168, 83, 0.15); color: #D4A853; border: 1px solid rgba(212, 168, 83, 0.3); }
.pillar-a { background: rgba(100, 149, 237, 0.15); color: #6495ED; border: 1px solid rgba(100, 149, 237, 0.3); }
.pillar-l { background: rgba(196, 75, 75, 0.15); color: #E07070; border: 1px solid rgba(196, 75, 75, 0.3); }

.chat-msg {
    padding: 1.2rem 1.5rem;
    border-radius: 12px;
    margin-bottom: 1rem;
    line-height: 1.7;
    font-size: 0.92rem;
}
.chat-msg-user {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-left: 3px solid var(--accent);
}
.chat-msg-assistant {
    background: rgba(27, 77, 62, 0.15);
    border: 1px solid rgba(45, 122, 95, 0.25);
    border-left: 3px solid var(--primary-light);
}
.chat-msg-system {
    background: rgba(212, 168, 83, 0.08);
    border: 1px solid rgba(212, 168, 83, 0.2);
    border-left: 3px solid var(--accent);
    font-style: italic;
}

.ebl-phase {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 1.5rem;
}
.ebl-phase-title {
    font-family: 'DM Serif Display', serif !important;
    font-size: 1.1rem !important;
    color: var(--accent) !important;
    margin-bottom: 0.5rem !important;
}
.ebl-phase-desc {
    color: var(--text-secondary) !important;
    font-size: 0.85rem !important;
    line-height: 1.5 !important;
}

.phase-stepper {
    display: flex;
    justify-content: space-between;
    margin-bottom: 1.5rem;
    padding: 0.8rem 0;
}
.phase-step { flex: 1; text-align: center; position: relative; padding: 0 0.5rem; }
.phase-dot {
    width: 32px; height: 32px; border-radius: 50%;
    display: inline-flex; align-items: center; justify-content: center;
    font-size: 0.75rem; font-weight: 700; margin-bottom: 0.4rem;
    transition: all 0.3s ease;
}
.phase-dot-active { background: var(--accent); color: var(--bg-dark); }
.phase-dot-done { background: var(--success); color: var(--bg-dark); }
.phase-dot-pending { background: var(--bg-card); color: var(--text-muted); border: 1px solid var(--border); }
.phase-label { font-size: 0.7rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em; }
.phase-label-active { color: var(--accent) !important; font-weight: 600; }

.reflection-box {
    background: rgba(212, 168, 83, 0.06);
    border: 1px dashed rgba(212, 168, 83, 0.35);
    border-radius: 10px;
    padding: 1.2rem 1.5rem;
    margin: 1rem 0;
}
.reflection-box h4 {
    color: var(--accent) !important;
    font-family: 'DM Serif Display', serif !important;
    font-size: 0.95rem !important;
    margin-bottom: 0.5rem !important;
}
.reflection-box p { color: var(--text-secondary) !important; font-size: 0.85rem !important; }

.limitation-notice {
    background: rgba(196, 75, 75, 0.08);
    border: 1px solid rgba(196, 75, 75, 0.2);
    border-radius: 8px;
    padding: 0.8rem 1rem;
    margin-top: 1rem;
    font-size: 0.78rem;
    color: var(--text-muted);
}
.limitation-notice strong { color: var(--danger); }

.stTextArea textarea, .stTextInput input {
    background-color: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    color: var(--text-primary) !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stTextArea textarea:focus, .stTextInput input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 1px var(--accent) !important;
}

.stButton > button {
    background-color: var(--primary) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--primary-light) !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    padding: 0.5rem 1.5rem !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    background-color: var(--primary-light) !important;
    border-color: var(--accent) !important;
}

.stSelectbox > div > div {
    background-color: var(--bg-card) !important;
    border-color: var(--border) !important;
    color: var(--text-primary) !important;
}

.section-divider { border: none; border-top: 1px solid var(--border); margin: 1.5rem 0; }

.app-footer {
    text-align: center; padding: 1.5rem;
    border-top: 1px solid var(--border); margin-top: 2rem;
    color: var(--text-muted); font-size: 0.75rem;
}

/* ─── Active Recall Styles ─── */
.recall-phase-box {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 1.5rem;
}
.recall-phase-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.1rem;
    color: var(--recall-purple);
    margin-bottom: 0.5rem;
}

.knowledge-bar-container { margin: 0.4rem 0; }
.knowledge-bar-label {
    font-size: 0.78rem; color: var(--text-muted);
    margin-bottom: 0.2rem; display: flex;
    justify-content: space-between;
}
.knowledge-bar-bg {
    height: 10px; background: rgba(255,255,255,0.06);
    border-radius: 5px; overflow: hidden;
}
.knowledge-bar-fill {
    height: 100%; border-radius: 5px;
    transition: width 0.6s ease;
}

.gap-missed { background: var(--danger); }
.gap-misunderstood { background: var(--warning); }
.gap-understood { background: var(--success); }

.idk-button {
    background: rgba(196, 75, 75, 0.12) !important;
    border: 1px solid rgba(196, 75, 75, 0.3) !important;
    color: #E07070 !important;
}

.recall-round-badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    background: rgba(155, 114, 207, 0.15);
    color: var(--recall-purple);
    border: 1px solid rgba(155, 114, 207, 0.3);
}
</style>
""", unsafe_allow_html=True)


# ─── System Prompts ───

EVIDENCE_SYSTEM_PROMPT = """You are the DentEdTech™ Evidence Engine, an educational AI assistant for medicine, dentistry, and pharmacology students at the University of Manchester. You operate under the REAL-AI framework principles.

## YOUR STRICT SOURCE CONSTRAINTS
You may ONLY provide information from these source types:
1. **Scientific journals** (PubMed-indexed, peer-reviewed)
2. **University websites** (.ac.uk, .edu domains)
3. **Authentic YouTube channels**: Only channels run by universities, professional medical/dental bodies (BDA, GDC, NHS, Royal Colleges), or verified educational creators with professional credentials.

You must NEVER cite Wikipedia, blogs, commercial health sites, social media, or unverified sources.

## REAL-AI FRAMEWORK INTEGRATION
### Pillar 1 — Reflective Integration
Before providing evidence, ALWAYS ask the student what they already know first. Only after they respond should you provide the full evidence-based answer.

### Pillar 3 — Authentic Clinical Alignment
Always include a **⚠️ Limitations** section. Be transparent: "This AI response is a learning aid, not clinical advice"

### Pillar 4 — Learning-Centred Partnership
Encourage the student to discuss findings with faculty. End with a reflective question.

## RESPONSE FORMAT
📋 Pre-Reflection Prompt → 🔬 Evidence Summary → 📚 Key Sources → 🎓 University Resources → 🎥 Recommended Video → ⚠️ Limitations → 🤔 Post-Learning Reflection

## CRITICAL RULES
- Never fabricate references
- Always distinguish levels of evidence
- If you cannot find strong evidence, say so honestly"""


EBL_SYSTEM_PROMPT = """You are the DentEdTech™ Enquiry-Based Learning (EBL) Facilitator. You guide students through structured inquiry WITHOUT giving direct answers. You operate under the REAL-AI framework.

## THE HYBRID EBL MODEL — 5 Phases:
1. FORMING: Encounter the problem, activate prior knowledge
2. STORMING: Generate multiple perspectives and hypotheses
3. QUESTIONING: Transform uncertainty into structured research questions (PICO/PEO)
4. SEEKING: Learn WHERE and HOW to find evidence (without providing it)
5. SYNTHESISING: Connect findings back to the original problem

## CRITICAL RULES
- NEVER provide direct evidence, citations, or links
- NEVER answer clinical questions directly
- Always respond with guiding questions
- Use "What makes you think that?" before "Have you considered...?"
- Normalise uncertainty: "Not knowing is the starting point of inquiry, not a failure"
- Always indicate current phase: 📍 **Phase [N]: [PHASE NAME]**"""


VIDEO_SEARCH_SYSTEM_PROMPT = """You are the DentEdTech™ Clinical Video Trust Engine. You find and evaluate clinical skills videos against the Video Trust Authentication Framework (VTAF) — 7 dimensions:

1. Author Credentials (25%): Degrees, postgrad, academic appointment, GDC/GMC, publications
2. Institutional Backing (20%): University/Royal College vs personal channel
3. Production Quality (10%): Multi-angle, audio, HD
4. Educational Structure (15%): Learning objectives, narration, terminology, error discussion
5. Professional Engagement (5%): Weighted LOW — niche content gets few views
6. Skill Transfer Potential (15%): Can you practise after watching?
7. Currency & Evidence (10%): Guideline alignment, publication date

Trust Levels: ≥80% ✅ TRUSTED | 60-79% ⚠️ CAUTION | <60% ❌ NOT RECOMMENDED

For each video provide: Title, URL, Channel, Author Profile (qualifications, position, registration), full 7-dimension breakdown, skill transfer assessment, and limitations.
Maximum 3 videos per query. Include direct YouTube URLs."""


ACTIVE_RECALL_ANALYSIS_PROMPT = """You are the DentEdTech™ Active Recall Analyser. You are an expert at comparing a student's recalled knowledge against their original study material to identify precise knowledge gaps.

## YOUR TASK
You will receive:
1. The ORIGINAL STUDY MATERIAL the student uploaded
2. The student's FREE RECALL attempt (what they wrote from memory) OR their ANSWERS to questions

## YOUR ANALYSIS
Compare the recall/answers against the original material and categorise EVERY key concept/fact into exactly one of three categories:

### ✅ UNDERSTOOD — Student got this right
Concepts the student recalled correctly, with accurate details and relationships.

### ⚠️ MISUNDERSTOOD — Student got this partially right or wrong
Concepts the student attempted but got details wrong, confused relationships, mixed up terminology, or had incomplete understanding. Explain exactly what they got wrong and what the correct information is.

### ❌ MISSED — Student forgot or didn't mention this
Important concepts from the study material that the student did not mention at all, or said "I don't know" to. These are complete gaps.

## RESPONSE FORMAT
You MUST respond in valid JSON with this exact structure:
```json
{
    "summary": "Brief overall assessment of the student's recall",
    "round_score": 65,
    "understood": [
        {"concept": "Name of concept", "detail": "What they got right"},
        ...
    ],
    "misunderstood": [
        {"concept": "Name of concept", "student_said": "What the student said", "correct": "What the correct information is"},
        ...
    ],
    "missed": [
        {"concept": "Name of concept", "correct": "What the student needs to learn"},
        ...
    ],
    "total_concepts": 20,
    "understood_count": 8,
    "misunderstood_count": 5,
    "missed_count": 7
}
```

## CRITICAL RULES
- Be thorough: extract EVERY important concept from the study material, not just main headings
- Include specific facts, relationships, mechanisms, definitions, clinical significance
- Be fair: if the student conveyed the right idea in different words, count it as understood
- Be precise about misunderstandings: quote what they said vs what's correct
- Do NOT include any text outside the JSON block
- round_score should be a percentage: (understood / total_concepts) × 100"""


ACTIVE_RECALL_QUESTIONS_PROMPT = """You are the DentEdTech™ Active Recall Question Generator. You generate targeted questions to test a student's knowledge, prioritising their weakest areas.

## YOUR TASK
You will receive:
1. The ORIGINAL STUDY MATERIAL
2. The student's KNOWLEDGE GAP ANALYSIS (what they understood, misunderstood, and missed)
3. The current ROUND number

## QUESTION GENERATION RULES

### Priority Order (MANDATORY):
1. FIRST: Ask about concepts the student MISSED completely (❌) — these are the biggest gaps
2. SECOND: Ask about concepts the student MISUNDERSTOOD (⚠️) — test if they now understand correctly
3. LAST: Ask about concepts they UNDERSTOOD (✅) — brief verification only

### Question Design:
- Generate 5-8 questions per round
- Questions should be specific, not vague
- Mix question types: definition, mechanism, clinical application, comparison, case-based
- For misunderstood concepts: frame questions that specifically target the misconception
- For missed concepts: start with foundational questions before complex ones

## RESPONSE FORMAT
You MUST respond in valid JSON:
```json
{
    "questions": [
        {
            "id": 1,
            "question": "The question text",
            "concept": "Which concept this tests",
            "gap_type": "missed",
            "difficulty": "foundation"
        },
        ...
    ],
    "focus_message": "Brief message to the student about what this round focuses on"
}
```

gap_type must be one of: "missed", "misunderstood", "understood"
difficulty must be one of: "foundation", "application", "integration"

## CRITICAL RULES
- At least 60% of questions should target missed or misunderstood concepts
- Never provide answers in the questions
- Each question should test ONE concept clearly
- Include "I don't know" as a valid response option — tell the student this in focus_message
- Do NOT include any text outside the JSON block"""


ACTIVE_RECALL_RELEARN_PROMPT = """You are the DentEdTech™ Active Recall Re-Learning Presenter. You re-present study material in a prioritised order based on the student's knowledge gaps.

## YOUR TASK
You will receive:
1. The ORIGINAL STUDY MATERIAL
2. The student's KNOWLEDGE GAP ANALYSIS

## RE-PRESENTATION ORDER (MANDATORY):
Present the material in this EXACT priority order:

### 1. ❌ MISSED CONCEPTS — Present FIRST
These are concepts the student completely forgot or never learned. Present each one with:
- Clear definition/explanation
- Why it matters clinically
- Memory hook or mnemonic if helpful
- Connection to concepts they already understand

### 2. ⚠️ MISUNDERSTOOD CONCEPTS — Present SECOND
These are concepts the student got wrong. For each:
- State what they incorrectly believed
- Explain why that's wrong
- Present the correct information clearly
- Highlight the specific distinction they missed

### 3. ✅ UNDERSTOOD CONCEPTS — Present LAST (brief)
These concepts the student already knows. Present briefly as confirmation/reinforcement.
- Brief summary only
- Any nuances they might deepen

## FORMAT
Use clear headings and structure. Make it scannable. Use clinical examples from the original material.
Start with: "Here's your study material, reorganised based on your recall performance. We're starting with what needs the most attention."

End with: "When you're ready, we'll test you again on the areas you struggled with. Take your time reading through — especially the ❌ sections."

## CRITICAL RULES
- Use the EXACT content from the original study material — don't invent new information
- Be encouraging, not punitive
- Emphasise that forgetting is normal and part of the learning process
- Keep the re-presentation focused and scannable"""


# ─── Trusted Channel Registry ───
TRUSTED_CHANNELS = {
    "university": [
        {"channel": "University of Manchester", "url": "https://www.youtube.com/@OfficialUoM", "category": "University", "trust_floor": 85, "notes": "Home institution."},
        {"channel": "King's College London Dentistry", "url": "https://www.youtube.com/@KCLDentistry", "category": "University", "trust_floor": 90, "notes": "Leading UK dental school."},
        {"channel": "Harvard School of Dental Medicine", "url": "https://www.youtube.com/@HarvardDentalMedicine", "category": "University", "trust_floor": 90, "notes": "International leader."},
        {"channel": "University of Michigan School of Dentistry", "url": "https://www.youtube.com/@umichdent", "category": "University", "trust_floor": 88, "notes": "Extensive clinical skills library."},
    ],
    "professional_bodies": [
        {"channel": "British Dental Association (BDA)", "url": "https://www.youtube.com/@TheBDA", "category": "Professional Body", "trust_floor": 90, "notes": "UK professional body."},
        {"channel": "General Dental Council (GDC)", "url": "https://www.youtube.com/@TheGDCUK", "category": "Regulator", "trust_floor": 85, "notes": "UK dental regulator."},
        {"channel": "Royal College of Surgeons of England", "url": "https://www.youtube.com/@RCSEngland", "category": "Royal College", "trust_floor": 92, "notes": "FDSRCS, surgical technique."},
        {"channel": "Royal Pharmaceutical Society", "url": "https://www.youtube.com/@royalpharmaceuticalsociety", "category": "Professional Body", "trust_floor": 88, "notes": "Pharmacology content."},
    ],
    "nhs": [
        {"channel": "NHS England", "url": "https://www.youtube.com/@NHSEngland", "category": "NHS", "trust_floor": 85, "notes": "Official NHS channel."},
    ],
}


# ─── Session State ───
def init_session():
    defaults = {
        "mode": None,
        "evidence_messages": [],
        "ebl_messages": [],
        "ebl_phase": 1,
        "ebl_case": None,
        "reflection_given": False,
        "discipline": "Dentistry",
        "year_of_study": "Year 3",
        "video_messages": [],
        # Active Recall state
        "ar_phase": "upload",  # upload → free_recall → analysis → questions → relearn → repeat
        "ar_study_material": None,
        "ar_file_name": None,
        "ar_free_recall": None,
        "ar_analysis": None,
        "ar_questions": None,
        "ar_answers": {},
        "ar_round": 1,
        "ar_history": [],
        "ar_messages": [],
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_session()


# ─── Helper Functions ───

def get_api_key():
    try:
        return st.secrets["ANTHROPIC_API_KEY"]
    except (KeyError, FileNotFoundError):
        return None


def call_claude(messages, system_prompt, use_search=False):
    api_key = get_api_key()
    if not api_key:
        return "⚠️ API key not found. Please add ANTHROPIC_API_KEY to your Streamlit secrets."

    client = anthropic.Anthropic(api_key=api_key)
    kwargs = {
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 4096,
        "system": system_prompt,
        "messages": messages,
    }
    if use_search:
        kwargs["tools"] = [{"type": "web_search_20250305", "name": "web_search"}]

    try:
        response = client.messages.create(**kwargs)
        text_parts = []
        for block in response.content:
            if hasattr(block, "text"):
                text_parts.append(block.text)
        return "\n".join(text_parts) if text_parts else "I wasn't able to generate a response. Please try again."
    except anthropic.AuthenticationError:
        return "⚠️ Invalid API key."
    except anthropic.RateLimitError:
        return "⚠️ Rate limit reached. Please wait."
    except Exception as e:
        return f"⚠️ An error occurred: {str(e)}"


def call_claude_json(messages, system_prompt):
    """Call Claude and parse JSON from response."""
    raw = call_claude(messages, system_prompt, use_search=False)
    # Extract JSON from response (handle markdown code blocks)
    json_match = re.search(r'```(?:json)?\s*([\s\S]*?)```', raw)
    if json_match:
        raw = json_match.group(1)
    # Try to find JSON object or array
    json_match = re.search(r'(\{[\s\S]*\})', raw)
    if json_match:
        try:
            return json.loads(json_match.group(1))
        except json.JSONDecodeError:
            return None
    return None


def render_phase_stepper(current_phase):
    phases = [("1", "Forming"), ("2", "Storming"), ("3", "Questioning"), ("4", "Seeking"), ("5", "Synthesising")]
    html = '<div class="phase-stepper">'
    for num, label in phases:
        phase_num = int(num)
        if phase_num < current_phase:
            dot_class, label_class, dot_content = "phase-dot phase-dot-done", "phase-label", "✓"
        elif phase_num == current_phase:
            dot_class, label_class, dot_content = "phase-dot phase-dot-active", "phase-label phase-label-active", num
        else:
            dot_class, label_class, dot_content = "phase-dot phase-dot-pending", "phase-label", num
        html += f'<div class="phase-step"><div class="{dot_class}">{dot_content}</div><div class="{label_class}">{label}</div></div>'
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


def render_message(role, content):
    if role == "user":
        css_class, icon = "chat-msg chat-msg-user", "🧑‍🎓"
    elif role == "system":
        css_class, icon = "chat-msg chat-msg-system", "🔔"
    else:
        css_class, icon = "chat-msg chat-msg-assistant", "🔬"
    st.markdown(f'<div class="{css_class}">{icon} {content}</div>', unsafe_allow_html=True)


def render_real_ai_badges(pillars):
    badge_map = {
        "R": ("pillar-r", "Reflective Integration"), "E": ("pillar-e", "Equity by Design"),
        "A": ("pillar-a", "Authentic Alignment"), "L": ("pillar-l", "Learning Partnership"),
    }
    return "".join(f'<span class="pillar-badge {badge_map[p][0]}">{badge_map[p][1]}</span>' for p in pillars)


def render_youtube_embed(video_id):
    return f"""<div style="position:relative;padding-bottom:56.25%;height:0;overflow:hidden;border-radius:10px;margin:1rem 0;">
        <iframe src="https://www.youtube.com/embed/{video_id}" style="position:absolute;top:0;left:0;width:100%;height:100%;border:none;border-radius:10px;"
        allow="accelerometer;autoplay;clipboard-write;encrypted-media;gyroscope;picture-in-picture" allowfullscreen></iframe></div>"""


def render_knowledge_bar(label, count, total, color_class):
    pct = (count / total * 100) if total > 0 else 0
    return f"""<div class="knowledge-bar-container">
        <div class="knowledge-bar-label"><span>{label}</span><span>{count}/{total} ({pct:.0f}%)</span></div>
        <div class="knowledge-bar-bg"><div class="knowledge-bar-fill {color_class}" style="width:{pct}%"></div></div></div>"""


def render_recall_phase_stepper(current_phase):
    phases = [("upload", "📄 Upload"), ("free_recall", "✍️ Recall"), ("analysis", "📊 Analysis"),
              ("questions", "❓ Questions"), ("relearn", "📖 Re-learn")]
    html = '<div class="phase-stepper">'
    phase_order = ["upload", "free_recall", "analysis", "questions", "relearn"]
    current_idx = phase_order.index(current_phase) if current_phase in phase_order else 0
    for i, (key, label) in enumerate(phases):
        if i < current_idx:
            dot_class, label_class = "phase-dot phase-dot-done", "phase-label"
            dot_content = "✓"
        elif i == current_idx:
            dot_class, label_class = "phase-dot phase-dot-active", "phase-label phase-label-active"
            dot_content = str(i + 1)
        else:
            dot_class, label_class = "phase-dot phase-dot-pending", "phase-label"
            dot_content = str(i + 1)
        html += f'<div class="phase-step"><div class="{dot_class}">{dot_content}</div><div class="{label_class}">{label}</div></div>'
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


def read_uploaded_file(uploaded_file):
    """Extract text from uploaded file."""
    if uploaded_file is None:
        return None
    name = uploaded_file.name.lower()
    try:
        if name.endswith('.txt') or name.endswith('.md'):
            return uploaded_file.read().decode('utf-8')
        elif name.endswith('.pdf'):
            import pypdf
            reader = pypdf.PdfReader(uploaded_file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
        elif name.endswith('.docx'):
            import docx
            doc = docx.Document(uploaded_file)
            return "\n".join([para.text for para in doc.paragraphs])
        elif name.endswith('.pptx'):
            from pptx import Presentation
            prs = Presentation(uploaded_file)
            text = ""
            for slide in prs.slides:
                for shape in slide.shapes:
                    if shape.has_text_frame:
                        text += shape.text + "\n"
            return text
        else:
            return uploaded_file.read().decode('utf-8', errors='ignore')
    except Exception as e:
        return f"Error reading file: {str(e)}"


# ─── Sidebar ───
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 1rem 0 0.5rem;">
        <span style="font-family: 'DM Serif Display', serif; font-size: 1.5rem; color: #E8EDE9;">
            Dent<span style="color: #D4A853;">Ed</span>Tech™
        </span>
        <div style="font-size: 0.72rem; color: #6B8577; margin-top: 0.2rem; letter-spacing: 0.08em; text-transform: uppercase;">
            Evidence Engine
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    st.markdown("##### 🎓 Your Profile")
    st.session_state.discipline = st.selectbox("Discipline", ["Dentistry", "Medicine", "Pharmacology"], index=0)
    st.session_state.year_of_study = st.selectbox("Year of Study", ["Year 1", "Year 2", "Year 3", "Year 4", "Year 5", "Postgraduate"], index=2)

    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    with st.expander("📐 About the REAL-AI Framework"):
        st.markdown("""
        **R** — Reflective Integration · **E** — Equity by Design
        **A** — Authentic Clinical Alignment · **L** — Learning-Centred Partnership
        *Framework: Beyond the Algorithm (2026)*
        """)

    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    if st.session_state.mode is not None:
        if st.button("← Back to Mode Selection", use_container_width=True):
            st.session_state.mode = None
            st.rerun()
        if st.button("🔄 Reset Conversation", use_container_width=True):
            if st.session_state.mode == "evidence":
                st.session_state.evidence_messages = []
            elif st.session_state.mode == "ebl":
                st.session_state.ebl_messages = []
                st.session_state.ebl_phase = 1
            elif st.session_state.mode == "video":
                st.session_state.video_messages = []
            elif st.session_state.mode == "recall":
                for k in ["ar_phase", "ar_study_material", "ar_file_name", "ar_free_recall",
                           "ar_analysis", "ar_questions", "ar_answers", "ar_round", "ar_history", "ar_messages"]:
                    del st.session_state[k]
                init_session()
            st.rerun()

    st.markdown("""<div class="app-footer">© 2026 DentEdTech™<br>University of Manchester<br><em>Not a substitute for clinical judgement</em></div>""", unsafe_allow_html=True)


# ─── Main Content ───
st.markdown("""
<div class="main-header">
    <h1>Dent<span class="brand-accent">Ed</span>Tech™ Evidence Engine</h1>
    <div class="tagline">Theory-informed AI for health professions learning — built on the REAL-AI framework</div>
</div>
""", unsafe_allow_html=True)


# ─── Mode Selection ───
if st.session_state.mode is None:
    st.markdown(f"""<div style="text-align:center;margin-bottom:2rem;">
        <span style="color:var(--text-secondary);font-size:0.9rem;">Welcome, {st.session_state.discipline} student · {st.session_state.year_of_study} · University of Manchester</span></div>""", unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="medium")
    col3, col4 = st.columns(2, gap="medium")

    with col1:
        st.markdown(f"""<div class="mode-card"><h3>🔬 Evidence-Based Knowledge</h3>
            <p>Ask clinical or scientific questions and receive evidence-based answers sourced exclusively from peer-reviewed journals, university resources, and verified educational videos.</p>
            <div style="margin-top:0.8rem;">{render_real_ai_badges(["R", "A"])}</div></div>""", unsafe_allow_html=True)
        if st.button("Enter Evidence Mode →", key="btn_evidence", use_container_width=True):
            st.session_state.mode = "evidence"
            st.rerun()

    with col2:
        st.markdown(f"""<div class="mode-card"><h3>🧭 Enquiry-Based Learning</h3>
            <p>Develop your inquiry skills through a guided 5-phase cycle: Forming, Storming, Questioning, Seeking, and Synthesising. The AI guides you to discover answers yourself.</p>
            <div style="margin-top:0.8rem;">{render_real_ai_badges(["R", "E", "A", "L"])}</div></div>""", unsafe_allow_html=True)
        if st.button("Enter EBL Mode →", key="btn_ebl", use_container_width=True):
            st.session_state.mode = "ebl"
            st.session_state.ebl_messages = [{"role": "assistant", "content": "📍 **Phase 1: FORMING**\n\nWelcome to Enquiry-Based Learning.\n\nYou can either:\n- **Bring your own case** — describe a clinical scenario or problem\n- **Ask me for a case** — tell me the subject area\n\n*What topic are you most curious about right now?*"}]
            st.rerun()

    with col3:
        st.markdown(f"""<div class="mode-card"><h3>🎥 Clinical Video Trust Engine</h3>
            <p>Find the most trustworthy clinical skills videos on YouTube, scored against a 7-dimension trust framework. Videos play directly in the platform with full trust breakdowns.</p>
            <div style="margin-top:0.8rem;">{render_real_ai_badges(["R", "A", "L"])}</div></div>""", unsafe_allow_html=True)
        if st.button("Enter Video Mode →", key="btn_video", use_container_width=True):
            st.session_state.mode = "video"
            st.rerun()

    with col4:
        st.markdown(f"""<div class="mode-card"><h3>🧠 Active Recall</h3>
            <p>Upload your study material, write everything you remember, then let AI identify what you understood, misunderstood, and missed completely. Material is re-presented starting with your biggest gaps. Repeat until mastery.</p>
            <div style="margin-top:0.8rem;">{render_real_ai_badges(["R", "L"])}</div></div>""", unsafe_allow_html=True)
        if st.button("Enter Active Recall →", key="btn_recall", use_container_width=True):
            st.session_state.mode = "recall"
            st.rerun()


# ─── Evidence-Based Mode ───
elif st.session_state.mode == "evidence":
    st.markdown(f"""<div style="margin-bottom:1.5rem;"><span style="font-family:'DM Serif Display',serif;font-size:1.4rem;color:var(--text-primary);">🔬 Evidence-Based Knowledge</span>
        <span style="margin-left:1rem;">{render_real_ai_badges(["R", "A"])}</span></div>""", unsafe_allow_html=True)
    st.markdown("""<div class="limitation-notice"><strong>⚠️ Pillar 3 — Transparency:</strong> This AI searches peer-reviewed sources. Always verify against primary sources and discuss with supervisors.</div>""", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    for msg in st.session_state.evidence_messages:
        render_message(msg["role"], msg["content"])
    user_input = st.chat_input("Ask a clinical or scientific question...", key="evidence_input")
    if user_input:
        st.session_state.evidence_messages.append({"role": "user", "content": user_input})
        context = f"[Student: {st.session_state.discipline}, {st.session_state.year_of_study}, University of Manchester]"
        api_msgs = [{"role": m["role"], "content": (f"{context}\n\n{m['content']}" if i == 0 and m["role"] == "user" else m["content"])} for i, m in enumerate(st.session_state.evidence_messages)]
        with st.spinner("Searching evidence-based sources..."):
            response = call_claude(api_msgs, EVIDENCE_SYSTEM_PROMPT, use_search=True)
        st.session_state.evidence_messages.append({"role": "assistant", "content": response})
        st.rerun()


# ─── EBL Mode ───
elif st.session_state.mode == "ebl":
    st.markdown(f"""<div style="margin-bottom:1rem;"><span style="font-family:'DM Serif Display',serif;font-size:1.4rem;color:var(--text-primary);">🧭 Enquiry-Based Learning</span>
        <span style="margin-left:1rem;">{render_real_ai_badges(["R", "E", "A", "L"])}</span></div>""", unsafe_allow_html=True)
    render_phase_stepper(st.session_state.ebl_phase)
    phase_info = {1: ("Forming", "Encounter the problem. Activate what you already know."), 2: ("Storming", "Generate hypotheses freely. Challenge assumptions."),
                  3: ("Questioning", "Transform uncertainty into structured research questions."), 4: ("Seeking", "Plan your evidence search strategy."), 5: ("Synthesising", "Connect findings back to the case.")}
    pn, pd = phase_info[st.session_state.ebl_phase]
    st.markdown(f'<div class="ebl-phase"><div class="ebl-phase-title">📍 Phase {st.session_state.ebl_phase}: {pn}</div><div class="ebl-phase-desc">{pd}</div></div>', unsafe_allow_html=True)
    st.markdown("""<div class="limitation-notice"><strong>⚠️ EBL Commitment:</strong> This mode will NOT give you direct answers. The struggle of finding answers yourself is where deep learning happens.</div>""", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    for msg in st.session_state.ebl_messages:
        render_message(msg["role"], msg["content"])
    nc1, nc2, nc3 = st.columns([1, 2, 1])
    with nc1:
        if st.session_state.ebl_phase > 1 and st.button("← Previous Phase"):
            st.session_state.ebl_phase -= 1
            st.session_state.ebl_messages.append({"role": "assistant", "content": f"📍 Moving back to **Phase {st.session_state.ebl_phase}: {phase_info[st.session_state.ebl_phase][0]}**"})
            st.rerun()
    with nc3:
        if st.session_state.ebl_phase < 5 and st.button("Next Phase →"):
            st.session_state.ebl_phase += 1
            st.session_state.ebl_messages.append({"role": "assistant", "content": f"📍 Progressing to **Phase {st.session_state.ebl_phase}: {phase_info[st.session_state.ebl_phase][0]}**\n\n{phase_info[st.session_state.ebl_phase][1]}"})
            st.rerun()
    user_input = st.chat_input("Share your thinking...", key="ebl_input")
    if user_input:
        st.session_state.ebl_messages.append({"role": "user", "content": user_input})
        ctx = f"[Student: {st.session_state.discipline}, {st.session_state.year_of_study}]\n[Phase: {st.session_state.ebl_phase} — {phase_info[st.session_state.ebl_phase][0]}]"
        api_msgs = []
        for i, m in enumerate(st.session_state.ebl_messages):
            if m["role"] == "user" and i == len(st.session_state.ebl_messages) - 1:
                api_msgs.append({"role": "user", "content": f"{ctx}\n\n{m['content']}"})
            else:
                api_msgs.append(m)
        with st.spinner("Reflecting on your inquiry..."):
            response = call_claude(api_msgs, EBL_SYSTEM_PROMPT, use_search=False)
        if st.session_state.ebl_phase < 5:
            trans = {1: ["phase 2", "move to storming"], 2: ["phase 3", "move to questioning"], 3: ["phase 4", "move to seeking"], 4: ["phase 5", "move to synthesising"]}
            if any(kw in response.lower() for kw in trans.get(st.session_state.ebl_phase, [])):
                st.session_state.ebl_phase += 1
        st.session_state.ebl_messages.append({"role": "assistant", "content": response})
        st.rerun()


# ─── Video Trust Engine ───
elif st.session_state.mode == "video":
    st.markdown(f"""<div style="margin-bottom:1rem;"><span style="font-family:'DM Serif Display',serif;font-size:1.4rem;color:var(--text-primary);">🎥 Clinical Video Trust Engine</span>
        <span style="margin-left:1rem;">{render_real_ai_badges(["R", "A", "L"])}</span></div>""", unsafe_allow_html=True)
    st.markdown("""<div class="ebl-phase"><div class="ebl-phase-title">📐 Video Trust Authentication Framework (VTAF)</div>
        <div class="ebl-phase-desc">7 dimensions: Author Credentials (25%), Institutional Backing (20%), Educational Structure (15%), Skill Transfer (15%), Production Quality (10%), Currency (10%), Engagement (5%). Only ≥60% recommended.</div></div>""", unsafe_allow_html=True)
    st.markdown("""<div class="limitation-notice"><strong>⚠️ Transparency:</strong> Trust scores are AI-assessed. Verify author credentials independently. Watching does not replace supervised practice.</div>""", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    if not st.session_state.video_messages:
        st.markdown("""<div class="reflection-box"><h4>🤔 Before You Search (Pillar 1)</h4><p>What do you already know about this procedure? What specific aspect are you uncertain about?</p></div>""", unsafe_allow_html=True)
    for msg in st.session_state.video_messages:
        render_message(msg["role"], msg["content"])
        if msg["role"] == "assistant":
            for vid_id in dict.fromkeys(re.findall(r'(?:youtube\.com/watch\?v=|youtu\.be/)([\w-]+)', msg["content"])):
                st.markdown(render_youtube_embed(vid_id), unsafe_allow_html=True)
    user_input = st.chat_input("Search for a clinical skill or procedure...", key="video_input")
    if user_input:
        st.session_state.video_messages.append({"role": "user", "content": user_input})
        trusted_ctx = "\n\n## PRE-VERIFIED CHANNELS\n" + "".join(f"- {ch['channel']} ({ch['category']}) — Floor: {ch['trust_floor']}%\n" for cat in TRUSTED_CHANNELS.values() for ch in cat)
        ctx = f"[Student: {st.session_state.discipline}, {st.session_state.year_of_study}]\n[Search YouTube. Evaluate against VTAF. Provide direct URLs.]"
        api_msgs = [{"role": m["role"], "content": (f"{ctx}\n\n{m['content']}" if m["role"] == "user" and i == len(st.session_state.video_messages) - 1 else m["content"])} for i, m in enumerate(st.session_state.video_messages)]
        with st.spinner("Searching and evaluating clinical videos..."):
            response = call_claude(api_msgs, VIDEO_SEARCH_SYSTEM_PROMPT + trusted_ctx, use_search=True)
        st.session_state.video_messages.append({"role": "assistant", "content": response})
        st.rerun()


# ─── Active Recall Mode ───
elif st.session_state.mode == "recall":

    st.markdown(f"""<div style="margin-bottom:1rem;"><span style="font-family:'DM Serif Display',serif;font-size:1.4rem;color:var(--text-primary);">
        🧠 Active Recall</span><span style="margin-left:1rem;">{render_real_ai_badges(["R", "L"])}</span></div>""", unsafe_allow_html=True)

    # Round indicator
    st.markdown(f'<span class="recall-round-badge">Round {st.session_state.ar_round}</span>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # Phase stepper
    render_recall_phase_stepper(st.session_state.ar_phase)

    # ── PHASE 1: Upload ──
    if st.session_state.ar_phase == "upload":
        st.markdown("""<div class="recall-phase-box"><div class="recall-phase-title">📄 Step 1: Upload Your Study Material</div>
            <div class="ebl-phase-desc">Upload the material you've been studying. This can be lecture notes, a textbook chapter, a PDF, Word document, PowerPoint, or plain text file. The AI will use this as the source of truth to assess your recall.</div></div>""", unsafe_allow_html=True)

        st.markdown("""<div class="reflection-box"><h4>🤔 Pillar 1: Reflective Integration</h4>
            <p>Before you begin, close your notes. The power of active recall comes from retrieving information without looking. After uploading, you'll write everything you remember — no peeking.</p></div>""", unsafe_allow_html=True)

        uploaded_file = st.file_uploader(
            "Upload your study material",
            type=["txt", "md", "pdf", "docx", "pptx"],
            help="Supported: PDF, Word, PowerPoint, Text files",
        )

        if uploaded_file is not None:
            with st.spinner("Reading your study material..."):
                content = read_uploaded_file(uploaded_file)
            if content and not content.startswith("Error"):
                st.session_state.ar_study_material = content
                st.session_state.ar_file_name = uploaded_file.name
                st.success(f"✅ Loaded: **{uploaded_file.name}** ({len(content.split())} words)")
                if st.button("I've read this material — let's test my recall →", use_container_width=True):
                    st.session_state.ar_phase = "free_recall"
                    st.rerun()
            else:
                st.error(f"Could not read file: {content}")

    # ── PHASE 2: Free Recall ──
    elif st.session_state.ar_phase == "free_recall":
        if st.session_state.ar_round == 1:
            st.markdown("""<div class="recall-phase-box"><div class="recall-phase-title">✍️ Step 2: Write Everything You Remember</div>
                <div class="ebl-phase-desc">Without looking at your notes, write down everything you can remember from your study material.
                Don't worry about order or completeness — just get everything out of your head. This is the most important step: retrieval is where learning happens.</div></div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""<div class="recall-phase-box"><div class="recall-phase-title">✍️ Round {st.session_state.ar_round}: Write What You Remember Now</div>
                <div class="ebl-phase-desc">You've just reviewed the material with your gaps highlighted. Now, without looking, write everything you remember — especially the concepts you missed or misunderstood in the previous round.</div></div>""", unsafe_allow_html=True)

        st.markdown(f"""<div class="limitation-notice"><strong>📄 Studying:</strong> {st.session_state.ar_file_name}</div>""", unsafe_allow_html=True)

        free_recall = st.text_area(
            "Write everything you remember (no peeking!):",
            height=300,
            placeholder="Start writing everything you can recall from the material...\n\nDon't worry about perfect wording — just get the concepts, facts, mechanisms, and relationships down.",
            key=f"recall_input_round_{st.session_state.ar_round}",
        )

        if st.button("Submit my recall →", use_container_width=True, disabled=not free_recall):
            st.session_state.ar_free_recall = free_recall
            st.session_state.ar_phase = "analysis"
            st.rerun()

    # ── PHASE 3: Analysis ──
    elif st.session_state.ar_phase == "analysis":
        st.markdown("""<div class="recall-phase-box"><div class="recall-phase-title">📊 Step 3: Knowledge Gap Analysis</div>
            <div class="ebl-phase-desc">The AI is comparing your recall against the original material to identify what you understood, misunderstood, and missed completely.</div></div>""", unsafe_allow_html=True)

        if st.session_state.ar_analysis is None:
            with st.spinner("Analysing your recall against the study material..."):
                analysis_messages = [{"role": "user", "content": f"""## ORIGINAL STUDY MATERIAL:
{st.session_state.ar_study_material[:8000]}

## STUDENT'S FREE RECALL (Round {st.session_state.ar_round}):
{st.session_state.ar_free_recall}

Analyse this recall attempt against the original material. Respond ONLY with valid JSON."""}]
                result = call_claude_json(analysis_messages, ACTIVE_RECALL_ANALYSIS_PROMPT)
                if result:
                    st.session_state.ar_analysis = result
                    st.session_state.ar_history.append({"round": st.session_state.ar_round, "score": result.get("round_score", 0)})
                    st.rerun()
                else:
                    st.error("Analysis failed. Please try again.")
                    if st.button("Retry Analysis"):
                        st.rerun()

        if st.session_state.ar_analysis:
            a = st.session_state.ar_analysis
            total = a.get("total_concepts", 0)
            understood = a.get("understood_count", 0)
            misunderstood = a.get("misunderstood_count", 0)
            missed = a.get("missed_count", 0)
            score = a.get("round_score", 0)

            # Score display
            if score >= 80:
                score_color = "#4CAF7D"
            elif score >= 60:
                score_color = "#D4A853"
            else:
                score_color = "#C44B4B"

            st.markdown(f"""<div style="text-align:center;margin:1.5rem 0;">
                <div style="display:inline-block;width:90px;height:90px;border-radius:50%;border:4px solid {score_color};
                background:rgba({','.join(str(int(score_color.lstrip('#')[i:i+2], 16)) for i in (0,2,4))},0.12);
                display:inline-flex;align-items:center;justify-content:center;font-family:'DM Serif Display',serif;font-size:1.6rem;color:{score_color};">
                {score}%</div>
                <div style="color:var(--text-secondary);margin-top:0.5rem;font-size:0.88rem;">{a.get('summary', '')}</div></div>""", unsafe_allow_html=True)

            # Knowledge bars
            st.markdown(render_knowledge_bar("✅ Understood", understood, total, "gap-understood"), unsafe_allow_html=True)
            st.markdown(render_knowledge_bar("⚠️ Misunderstood", misunderstood, total, "gap-misunderstood"), unsafe_allow_html=True)
            st.markdown(render_knowledge_bar("❌ Missed", missed, total, "gap-missed"), unsafe_allow_html=True)

            # Detailed breakdown
            with st.expander("✅ Understood Concepts", expanded=False):
                for item in a.get("understood", []):
                    st.markdown(f"**{item['concept']}** — {item['detail']}")

            with st.expander("⚠️ Misunderstood Concepts", expanded=True):
                for item in a.get("misunderstood", []):
                    st.markdown(f"**{item['concept']}**")
                    st.markdown(f"You said: *\"{item['student_said']}\"*")
                    st.markdown(f"Correct: **{item['correct']}**")
                    st.markdown("---")

            with st.expander("❌ Missed Concepts", expanded=True):
                for item in a.get("missed", []):
                    st.markdown(f"**{item['concept']}** — {item['correct']}")

            # Score history
            if len(st.session_state.ar_history) > 1:
                st.markdown("**📈 Progress Across Rounds:**")
                for h in st.session_state.ar_history:
                    bar_w = h['score']
                    bar_c = "#4CAF7D" if h['score'] >= 80 else "#D4A853" if h['score'] >= 60 else "#C44B4B"
                    st.markdown(f"""<div style="display:flex;align-items:center;margin:0.3rem 0;font-size:0.82rem;">
                        <span style="width:70px;color:var(--text-muted);">Round {h['round']}</span>
                        <div style="flex:1;height:8px;background:rgba(255,255,255,0.06);border-radius:4px;overflow:hidden;">
                        <div style="width:{bar_w}%;height:100%;background:{bar_c};border-radius:4px;"></div></div>
                        <span style="width:40px;text-align:right;color:var(--text-secondary);font-weight:600;">{h['score']}%</span></div>""", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            if score >= 95:
                st.markdown("""<div class="reflection-box"><h4>🎉 Outstanding!</h4>
                    <p>You've demonstrated comprehensive recall of this material. Consider discussing the concepts you found trickiest with your tutor to deepen your understanding even further.</p></div>""", unsafe_allow_html=True)
            else:
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("❓ Test me with questions →", use_container_width=True):
                        st.session_state.ar_phase = "questions"
                        st.session_state.ar_questions = None
                        st.session_state.ar_answers = {}
                        st.rerun()
                with c2:
                    if st.button("📖 Show me what I missed →", use_container_width=True):
                        st.session_state.ar_phase = "relearn"
                        st.rerun()

    # ── PHASE 4: Questions ──
    elif st.session_state.ar_phase == "questions":
        st.markdown(f"""<div class="recall-phase-box"><div class="recall-phase-title">❓ Step 4: Targeted Questions</div>
            <div class="ebl-phase-desc">These questions focus on your weakest areas first. If you don't know an answer, select "I don't know" — honest gaps are more useful than guesses.</div></div>""", unsafe_allow_html=True)

        # Generate questions if not yet generated
        if st.session_state.ar_questions is None:
            with st.spinner("Generating targeted questions based on your gaps..."):
                q_messages = [{"role": "user", "content": f"""## ORIGINAL STUDY MATERIAL:
{st.session_state.ar_study_material[:6000]}

## KNOWLEDGE GAP ANALYSIS:
{json.dumps(st.session_state.ar_analysis, indent=2)}

## ROUND: {st.session_state.ar_round}

Generate targeted questions prioritising missed and misunderstood concepts. Respond ONLY with valid JSON."""}]
                result = call_claude_json(q_messages, ACTIVE_RECALL_QUESTIONS_PROMPT)
                if result:
                    st.session_state.ar_questions = result
                    st.rerun()
                else:
                    st.error("Question generation failed.")
                    if st.button("Retry"):
                        st.rerun()

        if st.session_state.ar_questions:
            qs = st.session_state.ar_questions
            st.markdown(f"""<div class="reflection-box"><h4>📋 Focus for this round</h4><p>{qs.get('focus_message', 'Answer honestly. Select "I don\'t know" if unsure.')}</p></div>""", unsafe_allow_html=True)

            questions = qs.get("questions", [])

            with st.form("questions_form"):
                for q in questions:
                    qid = str(q.get("id", ""))
                    gap = q.get("gap_type", "")
                    gap_icon = {"missed": "❌", "misunderstood": "⚠️", "understood": "✅"}.get(gap, "")

                    st.markdown(f"**{gap_icon} Q{qid}: {q['question']}**")
                    st.markdown(f"<span style='font-size:0.72rem;color:var(--text-muted);'>Testing: {q.get('concept', '')} · {q.get('difficulty', '')}</span>", unsafe_allow_html=True)

                    answer = st.text_area(
                        "Your answer:",
                        key=f"q_answer_{st.session_state.ar_round}_{qid}",
                        height=80,
                        placeholder="Type your answer here, or leave blank and tick 'I don't know' below",
                    )
                    idk = st.checkbox("🚫 I don't know", key=f"q_idk_{st.session_state.ar_round}_{qid}")

                    st.session_state.ar_answers[qid] = "I DON'T KNOW" if idk else answer
                    st.markdown("---")

                submitted = st.form_submit_button("Submit all answers →", use_container_width=True)

            if submitted:
                # Build answers summary for re-analysis
                answers_text = ""
                for q in questions:
                    qid = str(q.get("id", ""))
                    ans = st.session_state.ar_answers.get(qid, "")
                    answers_text += f"Q: {q['question']}\nA: {ans}\n\n"

                # Combine free recall + question answers for new analysis
                combined_recall = f"{st.session_state.ar_free_recall}\n\n--- QUESTION ANSWERS ---\n{answers_text}"
                st.session_state.ar_free_recall = combined_recall
                st.session_state.ar_analysis = None
                st.session_state.ar_phase = "analysis"
                st.rerun()

    # ── PHASE 5: Re-learn ──
    elif st.session_state.ar_phase == "relearn":
        st.markdown(f"""<div class="recall-phase-box"><div class="recall-phase-title">📖 Step 5: Prioritised Re-Learning</div>
            <div class="ebl-phase-desc">Your study material is re-presented below, reorganised by priority: missed concepts first, then misunderstood, then what you already know. Read carefully, especially the ❌ sections.</div></div>""", unsafe_allow_html=True)

        # Generate re-learning presentation
        if "ar_relearn_content" not in st.session_state or st.session_state.ar_relearn_content is None:
            with st.spinner("Reorganising material based on your knowledge gaps..."):
                relearn_messages = [{"role": "user", "content": f"""## ORIGINAL STUDY MATERIAL:
{st.session_state.ar_study_material[:8000]}

## KNOWLEDGE GAP ANALYSIS:
{json.dumps(st.session_state.ar_analysis, indent=2)}

Re-present the study material prioritised by the student's gaps."""}]
                result = call_claude(relearn_messages, ACTIVE_RECALL_RELEARN_PROMPT, use_search=False)
                st.session_state.ar_relearn_content = result
                st.rerun()

        if st.session_state.get("ar_relearn_content"):
            render_message("assistant", st.session_state.ar_relearn_content)

            st.markdown("<br>", unsafe_allow_html=True)

            st.markdown("""<div class="reflection-box"><h4>🤔 Ready for another round?</h4>
                <p>When you've finished reading through the material above — especially the ❌ missed sections — you can test yourself again. Each round should show improvement as your brain strengthens the recall pathways.</p></div>""", unsafe_allow_html=True)

            if st.button("🔄 Test myself again →", use_container_width=True):
                st.session_state.ar_round += 1
                st.session_state.ar_phase = "free_recall"
                st.session_state.ar_free_recall = None
                st.session_state.ar_analysis = None
                st.session_state.ar_questions = None
                st.session_state.ar_answers = {}
                st.session_state.ar_relearn_content = None
                st.rerun()
