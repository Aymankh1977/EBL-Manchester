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

/* Root variables */
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
}

/* Global overrides */
.stApp {
    background-color: var(--bg-dark) !important;
    color: var(--text-primary) !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* Hide Streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Main header */
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
.brand-accent {
    color: var(--accent) !important;
}

/* Sidebar styling */
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

/* Mode selector cards */
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

/* REAL-AI pillar badges */
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

/* Chat message styling */
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

/* EBL phase indicator */
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

/* Phase stepper */
.phase-stepper {
    display: flex;
    justify-content: space-between;
    margin-bottom: 1.5rem;
    padding: 0.8rem 0;
}
.phase-step {
    flex: 1;
    text-align: center;
    position: relative;
    padding: 0 0.5rem;
}
.phase-dot {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 0.75rem;
    font-weight: 700;
    margin-bottom: 0.4rem;
    transition: all 0.3s ease;
}
.phase-dot-active {
    background: var(--accent);
    color: var(--bg-dark);
}
.phase-dot-done {
    background: var(--success);
    color: var(--bg-dark);
}
.phase-dot-pending {
    background: var(--bg-card);
    color: var(--text-muted);
    border: 1px solid var(--border);
}
.phase-label {
    font-size: 0.7rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
.phase-label-active {
    color: var(--accent) !important;
    font-weight: 600;
}

/* Reflection prompt box */
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
.reflection-box p {
    color: var(--text-secondary) !important;
    font-size: 0.85rem !important;
}

/* Source cards */
.source-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 0.9rem 1.1rem;
    margin-bottom: 0.6rem;
    font-size: 0.82rem;
    transition: border-color 0.2s ease;
}
.source-card:hover {
    border-color: var(--primary-light);
}
.source-type {
    font-size: 0.68rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    font-weight: 600;
    margin-bottom: 0.3rem;
}
.source-journal { color: var(--success); }
.source-university { color: #6495ED; }
.source-video { color: var(--danger); }

/* Limitation notice */
.limitation-notice {
    background: rgba(196, 75, 75, 0.08);
    border: 1px solid rgba(196, 75, 75, 0.2);
    border-radius: 8px;
    padding: 0.8rem 1rem;
    margin-top: 1rem;
    font-size: 0.78rem;
    color: var(--text-muted);
}
.limitation-notice strong {
    color: var(--danger);
}

/* Input styling */
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

/* Button styling */
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

/* Selectbox */
.stSelectbox > div > div {
    background-color: var(--bg-card) !important;
    border-color: var(--border) !important;
    color: var(--text-primary) !important;
}

/* Radio buttons */
.stRadio label {
    color: var(--text-secondary) !important;
}

/* Expander */
.streamlit-expanderHeader {
    background-color: var(--bg-card) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
}

/* Divider */
.section-divider {
    border: none;
    border-top: 1px solid var(--border);
    margin: 1.5rem 0;
}

/* Footer */
.app-footer {
    text-align: center;
    padding: 1.5rem;
    border-top: 1px solid var(--border);
    margin-top: 2rem;
    color: var(--text-muted);
    font-size: 0.75rem;
}

/* ─── Video Trust Engine Styles ─── */
.trust-score-ring {
    width: 72px;
    height: 72px;
    border-radius: 50%;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-family: 'DM Serif Display', serif;
    font-size: 1.3rem;
    font-weight: 700;
    margin-right: 1rem;
    flex-shrink: 0;
}
.trust-high {
    background: rgba(76, 175, 125, 0.15);
    border: 3px solid #4CAF7D;
    color: #4CAF7D;
}
.trust-medium {
    background: rgba(212, 168, 83, 0.15);
    border: 3px solid #D4A853;
    color: #D4A853;
}
.trust-low {
    background: rgba(196, 75, 75, 0.15);
    border: 3px solid #C44B4B;
    color: #C44B4B;
}

.video-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    transition: border-color 0.3s ease;
}
.video-card:hover {
    border-color: var(--primary-light);
}
.video-card-header {
    display: flex;
    align-items: center;
    margin-bottom: 1rem;
}
.video-card-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.05rem;
    color: var(--text-primary);
    margin-bottom: 0.2rem;
}
.video-card-channel {
    font-size: 0.8rem;
    color: var(--accent);
    font-weight: 500;
}

.credential-tag {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 0.68rem;
    font-weight: 600;
    margin-right: 4px;
    margin-bottom: 4px;
    letter-spacing: 0.03em;
}
.cred-degree { background: rgba(100, 149, 237, 0.15); color: #6495ED; border: 1px solid rgba(100, 149, 237, 0.25); }
.cred-postgrad { background: rgba(76, 175, 125, 0.15); color: #4CAF7D; border: 1px solid rgba(76, 175, 125, 0.25); }
.cred-academic { background: rgba(212, 168, 83, 0.15); color: #D4A853; border: 1px solid rgba(212, 168, 83, 0.25); }
.cred-reg { background: rgba(196, 130, 200, 0.15); color: #C882C8; border: 1px solid rgba(196, 130, 200, 0.25); }
.cred-institution { background: rgba(224, 64, 64, 0.12); color: #E07070; border: 1px solid rgba(224, 64, 64, 0.2); }
</style>
""", unsafe_allow_html=True)


# ─── System Prompts ───

EVIDENCE_SYSTEM_PROMPT = """You are the DentEdTech™ Evidence Engine, an educational AI assistant for medicine, dentistry, and pharmacology students at the University of Manchester. You operate under the REAL-AI framework principles.

## YOUR STRICT SOURCE CONSTRAINTS
You may ONLY provide information from these source types:
1. **Scientific journals** (PubMed-indexed, peer-reviewed): e.g., Journal of Dental Research, The Lancet, BMJ, NEJM, Journal of Dental Education, European Journal of Dental Education, British Dental Journal, Journal of Clinical Pharmacology, etc.
2. **University websites** (.ac.uk, .edu domains): e.g., University of Manchester, NHS education resources, university course materials.
3. **Authentic YouTube channels**: Only channels run by universities, professional medical/dental bodies (BDA, GDC, NHS, Royal Colleges), or verified educational creators with professional credentials.

You must NEVER cite Wikipedia, blogs, commercial health sites, social media, or unverified sources.

## REAL-AI FRAMEWORK INTEGRATION

### Pillar 1 — Reflective Integration
Before providing evidence, ALWAYS ask the student:
- "What do you already know about this topic?"
- "What do you expect the evidence might show?"
Only after they respond should you provide the full evidence-based answer. If they insist on a direct answer, gently explain why reflection first produces deeper learning, then provide the answer with a post-reflection prompt.

### Pillar 2 — Equity by Design
- Present diverse perspectives and global evidence where relevant
- Note when evidence may be limited to specific populations
- Use inclusive language and consider accessibility

### Pillar 3 — Authentic Clinical Alignment
- Always state the clinical relevance of evidence
- Include a **⚠️ Limitations** section noting what the evidence does NOT cover
- Flag when simulated/in-vitro evidence may not transfer to clinical settings
- Be transparent: "This AI response is a learning aid, not clinical advice"

### Pillar 4 — Learning-Centred Partnership
- Encourage the student to discuss findings with faculty
- Suggest how they might verify or extend the information
- Prompt: "How might you apply this in your next clinical session?"

## RESPONSE FORMAT
Structure your evidence-based responses as follows:

**📋 Pre-Reflection Prompt** (always first, unless student has already reflected)

Then after reflection:

**🔬 Evidence Summary**
Synthesise the key findings in clear, accessible language.

**📚 Key Sources**
List 3-5 specific references with:
- Author(s), Year, Title
- Journal name
- DOI or URL where available
- Brief note on evidence quality (RCT, systematic review, cohort study, etc.)

**🎓 University Resources**
Link to relevant Manchester or other university learning materials if applicable.

**🎥 Recommended Video**
Suggest 1-2 authentic YouTube videos from verified channels (university lectures, Royal College presentations, BDA/GDC content, etc.). Include channel name and why it's trustworthy.

**⚠️ Limitations & Transparency**
- What this evidence does NOT tell us
- Any biases or gaps in the literature
- "This AI-generated summary should be verified against primary sources"

**🤔 Post-Learning Reflection**
End with a reflective question: "Now that you've seen this evidence, how does it change or confirm your initial thinking?"

## CRITICAL RULES
- If you cannot find strong evidence from approved sources, say so honestly and suggest the most relevant authentic YouTube video as a starting point
- Never fabricate references — if unsure, say "I recommend searching PubMed for [specific terms]"
- Always distinguish between levels of evidence (systematic review > RCT > cohort > case report > expert opinion)
- When using web search, prioritise PubMed, university repositories, and professional body websites"""


EBL_SYSTEM_PROMPT = """You are the DentEdTech™ Enquiry-Based Learning (EBL) Facilitator. You guide medicine, dentistry, and pharmacology students through structured inquiry WITHOUT giving them direct answers or direct evidence. You operate under the REAL-AI framework.

## YOUR ROLE
You are a Socratic facilitator. Your job is to help students develop the PROCESS of inquiry, not to hand them conclusions. You must resist every temptation to provide direct answers, even when asked.

## THE HYBRID EBL MODEL
You guide students through a 5-phase inquiry cycle that combines a forming-storming-questioning model with Kolb's experiential learning:

### Phase 1: FORMING (Concrete Experience → Orientation)
Purpose: Encounter the problem and activate prior knowledge
Your prompts should:
- Present or help frame the clinical scenario/problem
- Ask: "What is your first reaction to this case?"
- Ask: "What do you already know that might be relevant?"
- Ask: "What feels familiar here, and what feels new or confusing?"
- Help students identify the BOUNDARIES of their current knowledge
DO NOT: Provide background information or context they haven't asked about

### Phase 2: STORMING (Reflective Observation → Divergent Thinking)
Purpose: Generate multiple perspectives and hypotheses
Your prompts should:
- Ask: "What are ALL the possible explanations? Don't filter yet."
- Ask: "What would a [periodontist/pharmacologist/radiologist] notice here that you might miss?"
- Ask: "What assumptions are you making? Can you name them?"
- Challenge groupthink: "You've all agreed quickly — what's the counterargument?"
- Encourage: "What if the opposite of your hypothesis were true?"
DO NOT: Validate or invalidate their hypotheses. Let ambiguity sit.

### Phase 3: QUESTIONING (Abstract Conceptualisation → Inquiry Design)
Purpose: Transform uncertainty into structured research questions
Your prompts should:
- Ask: "What specific questions do you need answered to move forward?"
- Help refine vague questions into searchable, answerable ones
- Ask: "Is this a question about mechanism, prevalence, treatment efficacy, or prognosis?"
- Guide PICO/PEO framework: "Who is the patient? What's the intervention? What are you comparing to? What outcome matters?"
- Ask: "How would you rank these questions by importance to the case?"
DO NOT: Provide the questions. Help them BUILD the questions themselves.

### Phase 4: SEEKING (Active Experimentation → Evidence Navigation)
Purpose: Learn WHERE and HOW to find evidence
Your prompts should:
- Ask: "Where would you look first? Why that source?"
- Guide search strategy: "What search terms would you use? How might you combine them?"
- Ask: "What type of evidence would best answer your question — a systematic review? An RCT? Clinical guidelines?"
- Prompt critical appraisal: "If you find a study, what would you check first to judge its quality?"
- Suggest databases WITHOUT searching for them: "PubMed, Cochrane Library, NICE guidelines — which fits your question type?"
- If stuck: "What if you searched [broader/narrower term]? What Boolean operators might help?"
DO NOT: Search for evidence, provide links, or summarise findings. Guide them to the water; don't pour it.

### Phase 5: SYNTHESISING (Reflection → Integration)
Purpose: Connect evidence back to the original problem
Your prompts should:
- Ask: "What did you find? How does it relate to the original case?"
- Ask: "Did the evidence confirm or challenge your initial thinking?"
- Ask: "What would you do differently next time you approach a similar case?"
- Ask: "What gaps remain? What would you want to investigate further?"
- Ask: "How would you explain your findings to the patient?"
- Prompt Kolb closure: "What's one principle you'll carry forward from this inquiry?"
DO NOT: Provide a summary. The student must synthesise.

## REAL-AI INTEGRATION

### Pillar 1 — Reflective Integration
- Every phase transition includes a reflection checkpoint
- Never provide terminal answers — always respond with a guiding question
- Use "What makes you think that?" before "Have you considered...?"

### Pillar 2 — Equity by Design
- In Phase 2, prompt consideration of diverse patient populations
- Ask: "Would this case unfold differently for a patient from a different background?"
- Encourage consideration of health inequalities and social determinants

### Pillar 3 — Authentic Clinical Alignment
- Ground all scenarios in realistic clinical contexts
- Ask: "In a real clinic, what constraints would you face that this scenario doesn't capture?"
- Remind students of the gap between textbook cases and clinical reality

### Pillar 4 — Learning-Centred Partnership
- Explicitly name when you're holding back an answer and why
- Encourage them to bring findings to their tutor/supervisor
- Normalise uncertainty: "Not knowing is the starting point of inquiry, not a failure"

## PHASE TRACKING
Always indicate which phase the student is in and when it's time to progress.
Use this format at the start of each response:
📍 **Phase [N]: [PHASE NAME]**

When transitioning, explain why: "You've generated strong questions — let's move to thinking about where to find answers."

## CRITICAL RULES
- NEVER provide direct evidence, citations, or links in EBL mode
- NEVER answer their clinical questions directly
- If they demand answers, explain: "In EBL, the process of finding the answer IS the learning. I can guide your search strategy, but the discovery needs to be yours."
- If they're truly stuck, offer a HINT (not an answer): "Consider looking at the mechanism of action..." not "The mechanism is..."
- You may provide a case scenario if the student asks for one to practise with
- Always maintain warmth and encouragement — inquiry is hard, and struggle is productive"""


VIDEO_SEARCH_SYSTEM_PROMPT = """You are the DentEdTech™ Clinical Video Trust Engine. You help students find the MOST trustworthy clinical skills videos on YouTube for dentistry, medicine, and pharmacology.

## YOUR ROLE
When a student asks about a clinical skill or procedure, you search for YouTube videos and evaluate them against the DentEdTech™ Video Trust Authentication Framework (VTAF). You return ONLY videos that meet the trust criteria, with full transparency about why each video is or is not trustworthy.

## VIDEO TRUST AUTHENTICATION FRAMEWORK (VTAF) — 7 DIMENSIONS

You must evaluate every video candidate against ALL seven dimensions and provide a score for each (1-5):

### Dimension 1: Author Credentials (Weight: 25%)
Score 5: Verified dental/medical degree + postgraduate specialty qualification + current academic appointment + professional registration (GDC/GMC/GPhC) + published researcher
Score 4: Verified degree + postgraduate qualification + academic or hospital appointment
Score 3: Verified degree + clinical practice (no academic appointment)
Score 2: Claims credentials but not independently verifiable
Score 1: No credentials stated or unverifiable

Look for: BDS, DDS, MBChB, MBBS, MPharm, MFDS, MJDF, FDSRCS, MSc, PhD, FRCS, consultant title, professor/lecturer title, GDC/GMC number displayed.

### Dimension 2: Institutional Backing (Weight: 20%)
Score 5: Official university channel or Royal College/professional body channel
Score 4: NHS Trust or teaching hospital channel
Score 3: Professional association channel (BDA, ADA, FDI) or accredited CPD provider
Score 2: Personal channel but author has verified institutional affiliation
Score 1: Personal channel with no institutional connection

### Dimension 3: Production Quality (Weight: 10%)
Score 5: Professional multi-angle filming, clear audio, HD/4K, proper lighting of clinical field
Score 4: Good quality single-camera with clear clinical visibility
Score 3: Adequate quality, some limitations in angles or audio
Score 2: Poor quality but content still discernible
Score 1: Unwatchable quality that impedes learning

### Dimension 4: Educational Script & Structure (Weight: 15%)
Score 5: States learning objectives + step-by-step narration with anatomical terminology + evidence citations + summary/key takeaways + addresses common errors
Score 4: Clear narration with terminology + structured steps + summary
Score 3: Narrated procedure with some structure but missing objectives or summary
Score 2: Minimal narration, mostly demonstration
Score 1: No narration or educational structure

### Dimension 5: View Count & Professional Engagement (Weight: 5%)
This dimension is weighted LOW deliberately. Dental professionals watch niche content; low views do NOT mean low quality. Evaluate:
- Like-to-dislike ratio (if visible) matters more than raw count
- Comments from verified professionals indicating accuracy
- Whether the channel has a consistent professional audience
Score 5: Strong professional engagement regardless of view count
Score 4: Moderate professional engagement
Score 3: General engagement, some professional comments
Score 2: Low engagement overall
Score 1: No engagement or predominantly non-professional audience

### Dimension 6: Skill Transfer Potential (Weight: 15%)
Score 5: Teaches transferable technique + shows common errors + addresses patient variations + complications discussed + suitable for simulation practice afterwards
Score 4: Teaches technique + addresses some variations + mentions complications
Score 3: Demonstrates technique clearly but doesn't address variations or errors
Score 2: Shows end result but technique is hard to replicate from watching
Score 1: Entertainment/demonstration only, no transfer value

### Dimension 7: Currency & Evidence Alignment (Weight: 10%)
Score 5: Published within 2 years + references current guidelines (NICE, SDCEP, BSP, BNF) + technique consistent with current evidence
Score 4: Published within 3 years + technique consistent with current practice
Score 3: Published within 5 years + still largely current
Score 2: Older than 5 years but fundamentals unchanged
Score 1: Outdated techniques or contradicts current guidelines

## TRUST SCORE CALCULATION
Weighted score = (D1×0.25) + (D2×0.20) + (D3×0.10) + (D4×0.15) + (D5×0.05) + (D6×0.15) + (D7×0.10)
Convert to percentage: (weighted score / 5) × 100

Trust Levels:
- 80-100%: ✅ TRUSTED — Recommended for learning
- 60-79%: ⚠️ USE WITH CAUTION — Some limitations noted
- Below 60%: ❌ NOT RECOMMENDED — Significant trust concerns

## RESPONSE FORMAT
For each video you find and evaluate, provide this EXACT structure:

### 🎥 Video [N]: [Title]
**Channel:** [Name]
**URL:** [Full YouTube URL]
**Published:** [Date/Year]

**👤 Author Profile:**
- Name: [Full name]
- Qualifications: [List all verified qualifications e.g., BDS, MFDS RCS, PhD]
- Current Position: [Title and institution]
- Registration: [GDC/GMC number if available, or "Not displayed"]
- Publications: [If known, or "Not verified"]

**📊 VTAF Trust Score: [X]%** [✅ TRUSTED / ⚠️ USE WITH CAUTION / ❌ NOT RECOMMENDED]

**Dimension Breakdown:**
1. Author Credentials: [X]/5 — [Brief justification]
2. Institutional Backing: [X]/5 — [Brief justification]
3. Production Quality: [X]/5 — [Brief justification]
4. Educational Structure: [X]/5 — [Brief justification]
5. Professional Engagement: [X]/5 — [Brief justification]
6. Skill Transfer Potential: [X]/5 — [Brief justification]
7. Currency & Evidence: [X]/5 — [Brief justification]

**🎯 Skill Transfer Assessment:**
- Can you practise this after watching? [Yes/Partially/No]
- What you'll need: [Equipment/simulation requirements]
- What this video does NOT teach: [Gaps and limitations]

**⚠️ Limitations:** [What this video cannot replicate — e.g., haptic feedback, patient anxiety, real tissue feel]

---

Then at the end:

**🤔 Post-Viewing Reflection (Pillar 1):**
After watching, ask yourself: What was new? What confirmed your existing knowledge? What would you do differently in clinic? Discuss with your supervisor before attempting the procedure.

## CRITICAL RULES
- Search YouTube specifically for the clinical skill requested
- ALWAYS provide the full 7-dimension trust breakdown — never skip dimensions
- If you cannot verify author credentials, say so explicitly — do NOT assume
- If no trusted videos exist for a topic, say so honestly and suggest the student consult faculty or a specific textbook
- Recommend a MAXIMUM of 3 videos per query, ranked by trust score
- For each video, state what it does NOT teach (Pillar 3: Authentic Alignment)
- Include the direct YouTube URL so the student can watch within the platform
- Weight your recommendations toward videos from UK/European dental practice where relevant for Manchester students, but include international sources when they are higher quality
- When author backgrounds are available on university websites or professional registers, include that information"""


# ─── Trusted Channel Registry ───
TRUSTED_CHANNELS = {
    "university": [
        {
            "channel": "University of Manchester",
            "url": "https://www.youtube.com/@OfficialUoM",
            "category": "University",
            "trust_floor": 85,
            "notes": "Home institution. Dental school lectures, clinical demonstrations.",
        },
        {
            "channel": "King's College London Dentistry",
            "url": "https://www.youtube.com/@KCLDentistry",
            "category": "University",
            "trust_floor": 90,
            "notes": "Leading UK dental school. Faculty-led procedural and didactic content.",
        },
        {
            "channel": "University of Sheffield School of Clinical Dentistry",
            "url": "https://www.youtube.com/@shikitagawa",
            "category": "University",
            "trust_floor": 85,
            "notes": "UK dental school with strong simulation teaching.",
        },
        {
            "channel": "Harvard School of Dental Medicine",
            "url": "https://www.youtube.com/@HarvardDentalMedicine",
            "category": "University",
            "trust_floor": 90,
            "notes": "International leader in dental education and research.",
        },
        {
            "channel": "University of Michigan School of Dentistry",
            "url": "https://www.youtube.com/@umichdent",
            "category": "University",
            "trust_floor": 88,
            "notes": "Extensive clinical skills video library.",
        },
    ],
    "professional_bodies": [
        {
            "channel": "British Dental Association (BDA)",
            "url": "https://www.youtube.com/@TheBDA",
            "category": "Professional Body",
            "trust_floor": 90,
            "notes": "UK professional body. Clinical guidance, CPD content.",
        },
        {
            "channel": "General Dental Council (GDC)",
            "url": "https://www.youtube.com/@TheGDCUK",
            "category": "Regulator",
            "trust_floor": 85,
            "notes": "UK dental regulator. Standards, fitness to practise, professionalism.",
        },
        {
            "channel": "Royal College of Surgeons of England",
            "url": "https://www.youtube.com/@RCSEngland",
            "category": "Royal College",
            "trust_floor": 92,
            "notes": "FDSRCS examinations, surgical technique, CPD.",
        },
        {
            "channel": "FDI World Dental Federation",
            "url": "https://www.youtube.com/@FDIWorldDentalFederation",
            "category": "International Body",
            "trust_floor": 85,
            "notes": "Global dental federation. International perspectives and guidelines.",
        },
        {
            "channel": "British Medical Association (BMA)",
            "url": "https://www.youtube.com/@TheBMA",
            "category": "Professional Body",
            "trust_floor": 88,
            "notes": "UK medical professional body. Relevant for medical students.",
        },
        {
            "channel": "Royal Pharmaceutical Society",
            "url": "https://www.youtube.com/@royalpharmaceuticalsociety",
            "category": "Professional Body",
            "trust_floor": 88,
            "notes": "UK pharmacy professional body. Pharmacology content.",
        },
    ],
    "nhs": [
        {
            "channel": "NHS Health Education England",
            "url": "https://www.youtube.com/@NHSHEE",
            "category": "NHS",
            "trust_floor": 87,
            "notes": "NHS training and education content.",
        },
        {
            "channel": "NHS England",
            "url": "https://www.youtube.com/@NHSEngland",
            "category": "NHS",
            "trust_floor": 85,
            "notes": "Official NHS channel. Clinical pathways, public health.",
        },
    ],
}


# ─── Session State Initialization ───
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
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_session()


# ─── Helper Functions ───

def get_api_key():
    """Get API key from Streamlit secrets."""
    try:
        return st.secrets["ANTHROPIC_API_KEY"]
    except (KeyError, FileNotFoundError):
        return None


def call_claude(messages, system_prompt, use_search=False):
    """Call Claude API with optional web search."""
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
        kwargs["tools"] = [
            {
                "type": "web_search_20250305",
                "name": "web_search",
            }
        ]

    try:
        response = client.messages.create(**kwargs)

        text_parts = []
        for block in response.content:
            if hasattr(block, "text"):
                text_parts.append(block.text)
        return "\n".join(text_parts) if text_parts else "I wasn't able to generate a response. Please try again."

    except anthropic.AuthenticationError:
        return "⚠️ Invalid API key. Please check your Anthropic API key."
    except anthropic.RateLimitError:
        return "⚠️ Rate limit reached. Please wait a moment and try again."
    except Exception as e:
        return f"⚠️ An error occurred: {str(e)}"


def render_phase_stepper(current_phase):
    """Render the EBL phase progress stepper."""
    phases = [
        ("1", "Forming"),
        ("2", "Storming"),
        ("3", "Questioning"),
        ("4", "Seeking"),
        ("5", "Synthesising"),
    ]

    html = '<div class="phase-stepper">'
    for num, label in phases:
        phase_num = int(num)
        if phase_num < current_phase:
            dot_class = "phase-dot phase-dot-done"
            label_class = "phase-label"
            dot_content = "✓"
        elif phase_num == current_phase:
            dot_class = "phase-dot phase-dot-active"
            label_class = "phase-label phase-label-active"
            dot_content = num
        else:
            dot_class = "phase-dot phase-dot-pending"
            label_class = "phase-label"
            dot_content = num

        html += f"""
        <div class="phase-step">
            <div class="{dot_class}">{dot_content}</div>
            <div class="{label_class}">{label}</div>
        </div>"""

    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


def render_message(role, content):
    """Render a chat message with styling."""
    if role == "user":
        css_class = "chat-msg chat-msg-user"
        icon = "🧑‍🎓"
    elif role == "system":
        css_class = "chat-msg chat-msg-system"
        icon = "🔔"
    else:
        css_class = "chat-msg chat-msg-assistant"
        icon = "🔬"

    st.markdown(
        f'<div class="{css_class}">{icon} {content}</div>',
        unsafe_allow_html=True,
    )


def render_real_ai_badges(pillars):
    """Render REAL-AI pillar badges."""
    badge_map = {
        "R": ("pillar-r", "Reflective Integration"),
        "E": ("pillar-e", "Equity by Design"),
        "A": ("pillar-a", "Authentic Alignment"),
        "L": ("pillar-l", "Learning Partnership"),
    }
    html = ""
    for p in pillars:
        cls, label = badge_map[p]
        html += f'<span class="pillar-badge {cls}">{label}</span>'
    return html


def render_youtube_embed(video_id):
    """Render an embedded YouTube player."""
    return f"""
    <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; border-radius: 10px; margin: 1rem 0;">
        <iframe
            src="https://www.youtube.com/embed/{video_id}"
            style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none; border-radius: 10px;"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowfullscreen>
        </iframe>
    </div>"""


def render_trusted_channels_sidebar():
    """Render the trusted channel registry in sidebar."""
    with st.expander("📋 Trusted Channel Registry"):
        st.markdown("**Pre-verified channels:**")
        for category, channels in TRUSTED_CHANNELS.items():
            cat_label = category.replace("_", " ").title()
            st.markdown(f"**{cat_label}**")
            for ch in channels:
                st.markdown(
                    f"<span style='font-size:0.78rem; color: var(--text-secondary);'>"
                    f"• {ch['channel']}<br>"
                    f"<span style='color: var(--text-muted); font-size:0.7rem;'>"
                    f"Trust floor: {ch['trust_floor']}% · {ch['category']}</span></span>",
                    unsafe_allow_html=True,
                )
            st.markdown("")


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

    # Student context
    st.markdown("##### 🎓 Your Profile")
    st.session_state.discipline = st.selectbox(
        "Discipline",
        ["Dentistry", "Medicine", "Pharmacology"],
        index=0,
    )
    st.session_state.year_of_study = st.selectbox(
        "Year of Study",
        ["Year 1", "Year 2", "Year 3", "Year 4", "Year 5", "Postgraduate"],
        index=2,
    )

    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    # REAL-AI Info
    with st.expander("📐 About the REAL-AI Framework"):
        st.markdown("""
        This platform is built on the **REAL-AI** framework for principled AI integration in health professions education:

        **R** — Reflective Integration
        *AI promotes critical thinking, not dependency*

        **E** — Equity by Design
        *Inclusive, unbiased, accessible learning*

        **A** — Authentic Clinical Alignment
        *Transparent about what AI can and cannot do*

        **L** — Learning-Centred Partnership
        *AI augments faculty, never replaces them*

        *Framework: Beyond the Algorithm (2026)*
        """)

    # Trusted Channels (show only in video mode)
    if st.session_state.mode == "video":
        render_trusted_channels_sidebar()

    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    # Mode switch / Reset
    if st.session_state.mode is not None:
        if st.button("← Back to Mode Selection", use_container_width=True):
            st.session_state.mode = None
            st.rerun()

        if st.button("🔄 Reset Conversation", use_container_width=True):
            if st.session_state.mode == "evidence":
                st.session_state.evidence_messages = []
                st.session_state.reflection_given = False
            elif st.session_state.mode == "ebl":
                st.session_state.ebl_messages = []
                st.session_state.ebl_phase = 1
                st.session_state.ebl_case = None
            elif st.session_state.mode == "video":
                st.session_state.video_messages = []
            st.rerun()

    st.markdown("""
    <div class="app-footer">
        © 2026 DentEdTech™<br>
        University of Manchester<br>
        <em>Not a substitute for clinical judgement</em>
    </div>
    """, unsafe_allow_html=True)


# ─── Main Content ───

# Header
st.markdown("""
<div class="main-header">
    <h1>Dent<span class="brand-accent">Ed</span>Tech™ Evidence Engine</h1>
    <div class="tagline">Theory-informed AI for health professions learning — built on the REAL-AI framework</div>
</div>
""", unsafe_allow_html=True)


# ─── Mode Selection ───
if st.session_state.mode is None:

    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 2rem;">
        <span style="color: var(--text-secondary); font-size: 0.9rem;">
            Welcome, {st.session_state.discipline} student · {st.session_state.year_of_study} · University of Manchester
        </span>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3, gap="medium")

    with col1:
        st.markdown(f"""
        <div class="mode-card">
            <h3>🔬 Evidence-Based Knowledge</h3>
            <p>
                Ask clinical or scientific questions and receive evidence-based answers sourced
                exclusively from peer-reviewed journals, university resources, and verified
                educational videos.
            </p>
            <p>
                The engine will first prompt you to reflect on what you already know — building
                deeper learning through the Reflective Integration pillar.
            </p>
            <div style="margin-top: 0.8rem;">
                {render_real_ai_badges(["R", "A"])}
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Enter Evidence Mode →", key="btn_evidence", use_container_width=True):
            st.session_state.mode = "evidence"
            st.rerun()

    with col2:
        st.markdown(f"""
        <div class="mode-card">
            <h3>🧭 Enquiry-Based Learning</h3>
            <p>
                Develop your inquiry skills through a guided 5-phase cycle: Forming, Storming,
                Questioning, Seeking, and Synthesising. The AI will never give you direct
                answers — it guides you to discover them yourself.
            </p>
            <p>
                Combines problem-based learning with Kolb's experiential cycle for
                deep, transferable clinical reasoning.
            </p>
            <div style="margin-top: 0.8rem;">
                {render_real_ai_badges(["R", "E", "A", "L"])}
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Enter EBL Mode →", key="btn_ebl", use_container_width=True):
            st.session_state.mode = "ebl"
            welcome = (
                "📍 **Phase 1: FORMING**\n\n"
                "Welcome to Enquiry-Based Learning. This is where your inquiry journey begins.\n\n"
                "You can either:\n"
                "- **Bring your own case** — describe a clinical scenario, lecture topic, or problem you're working through\n"
                "- **Ask me for a case** — tell me the subject area and I'll present a scenario for you to explore\n\n"
                "Before we begin, take a moment: *What topic or clinical area are you most curious about right now?*"
            )
            st.session_state.ebl_messages = [{"role": "assistant", "content": welcome}]
            st.rerun()

    with col3:
        st.markdown(f"""
        <div class="mode-card">
            <h3>🎥 Clinical Video Trust Engine</h3>
            <p>
                Find the most trustworthy clinical skills videos on YouTube, scored against
                a 7-dimension trust framework: author credentials, institutional backing,
                production quality, educational structure, engagement, skill transfer potential,
                and currency.
            </p>
            <p>
                Videos play directly in the platform. Every recommendation shows
                the full trust breakdown so you know exactly why it's reliable.
            </p>
            <div style="margin-top: 0.8rem;">
                {render_real_ai_badges(["R", "A", "L"])}
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Enter Video Mode →", key="btn_video", use_container_width=True):
            st.session_state.mode = "video"
            st.rerun()

    # Framework overview
    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align: center; margin: 1rem 0 1.5rem;">
        <span style="font-family: 'DM Serif Display', serif; font-size: 1.1rem; color: var(--text-primary);">
            How the REAL-AI Framework Guides This Platform
        </span>
    </div>
    """, unsafe_allow_html=True)

    p1, p2, p3, p4 = st.columns(4, gap="medium")

    with p1:
        st.markdown("""
        <div class="mode-card" style="min-height: 180px;">
            <span class="pillar-badge pillar-r">R</span>
            <h3 style="font-size: 1rem !important;">Reflective Integration</h3>
            <p>AI pauses and prompts you to think before revealing answers. Your reasoning comes first.</p>
        </div>
        """, unsafe_allow_html=True)

    with p2:
        st.markdown("""
        <div class="mode-card" style="min-height: 180px;">
            <span class="pillar-badge pillar-e">E</span>
            <h3 style="font-size: 1rem !important;">Equity by Design</h3>
            <p>Diverse evidence, inclusive scenarios, and accessible design for all learners.</p>
        </div>
        """, unsafe_allow_html=True)

    with p3:
        st.markdown("""
        <div class="mode-card" style="min-height: 180px;">
            <span class="pillar-badge pillar-a">A</span>
            <h3 style="font-size: 1rem !important;">Authentic Alignment</h3>
            <p>Every response declares its limitations. Evidence is sourced, graded, and clinically contextualised.</p>
        </div>
        """, unsafe_allow_html=True)

    with p4:
        st.markdown("""
        <div class="mode-card" style="min-height: 180px;">
            <span class="pillar-badge pillar-l">L</span>
            <h3 style="font-size: 1rem !important;">Learning Partnership</h3>
            <p>AI supports your faculty, never replaces them. You're guided to grow, not to depend.</p>
        </div>
        """, unsafe_allow_html=True)


# ─── Evidence-Based Mode ───
elif st.session_state.mode == "evidence":

    st.markdown(f"""
    <div style="margin-bottom: 1.5rem;">
        <span style="font-family: 'DM Serif Display', serif; font-size: 1.4rem; color: var(--text-primary);">
            🔬 Evidence-Based Knowledge
        </span>
        <span style="margin-left: 1rem;">
            {render_real_ai_badges(["R", "A"])}
        </span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="limitation-notice">
        <strong>⚠️ Pillar 3 — Transparency Statement:</strong>
        This AI searches peer-reviewed journals, university websites, and verified educational videos.
        It may not capture all available evidence. Always verify findings against primary sources
        and discuss with your supervisors. This tool does not replicate clinical reasoning under real-world conditions.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    for msg in st.session_state.evidence_messages:
        render_message(msg["role"], msg["content"])

    user_input = st.chat_input(
        "Ask a clinical or scientific question...",
        key="evidence_input",
    )

    if user_input:
        st.session_state.evidence_messages.append(
            {"role": "user", "content": user_input}
        )
        render_message("user", user_input)

        context_note = f"[Student context: {st.session_state.discipline}, {st.session_state.year_of_study}, University of Manchester]"
        api_messages = []
        for msg in st.session_state.evidence_messages:
            if msg["role"] == "user" and msg == st.session_state.evidence_messages[0]:
                api_messages.append({
                    "role": "user",
                    "content": f"{context_note}\n\n{msg['content']}"
                })
            else:
                api_messages.append({
                    "role": msg["role"],
                    "content": msg["content"],
                })

        with st.spinner("Searching evidence-based sources..."):
            response = call_claude(
                api_messages,
                EVIDENCE_SYSTEM_PROMPT,
                use_search=True,
            )

        st.session_state.evidence_messages.append(
            {"role": "assistant", "content": response}
        )
        st.rerun()


# ─── EBL Mode ───
elif st.session_state.mode == "ebl":

    st.markdown(f"""
    <div style="margin-bottom: 1rem;">
        <span style="font-family: 'DM Serif Display', serif; font-size: 1.4rem; color: var(--text-primary);">
            🧭 Enquiry-Based Learning
        </span>
        <span style="margin-left: 1rem;">
            {render_real_ai_badges(["R", "E", "A", "L"])}
        </span>
    </div>
    """, unsafe_allow_html=True)

    render_phase_stepper(st.session_state.ebl_phase)

    phase_info = {
        1: ("Forming", "Encounter the problem. Activate what you already know. Identify the edges of your understanding."),
        2: ("Storming", "Generate hypotheses freely. Challenge assumptions. Explore multiple perspectives without filtering."),
        3: ("Questioning", "Transform your uncertainty into structured, searchable research questions."),
        4: ("Seeking", "Plan your evidence search strategy. Learn where and how to find reliable sources."),
        5: ("Synthesising", "Connect your findings back to the case. Reflect on what changed in your thinking."),
    }

    phase_name, phase_desc = phase_info[st.session_state.ebl_phase]
    st.markdown(f"""
    <div class="ebl-phase">
        <div class="ebl-phase-title">📍 Phase {st.session_state.ebl_phase}: {phase_name}</div>
        <div class="ebl-phase-desc">{phase_desc}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="limitation-notice">
        <strong>⚠️ EBL Commitment:</strong>
        This mode will NOT give you direct answers or evidence. It guides your inquiry process.
        The struggle of finding answers yourself is where deep learning happens.
        Bring your findings to your tutor for validation.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    for msg in st.session_state.ebl_messages:
        render_message(msg["role"], msg["content"])

    nav_col1, nav_col2, nav_col3 = st.columns([1, 2, 1])
    with nav_col1:
        if st.session_state.ebl_phase > 1:
            if st.button("← Previous Phase"):
                st.session_state.ebl_phase -= 1
                transition_msg = f"📍 Moving back to **Phase {st.session_state.ebl_phase}: {phase_info[st.session_state.ebl_phase][0]}**\n\n{phase_info[st.session_state.ebl_phase][1]}"
                st.session_state.ebl_messages.append(
                    {"role": "assistant", "content": transition_msg}
                )
                st.rerun()
    with nav_col3:
        if st.session_state.ebl_phase < 5:
            if st.button("Next Phase →"):
                st.session_state.ebl_phase += 1
                transition_msg = f"📍 Progressing to **Phase {st.session_state.ebl_phase}: {phase_info[st.session_state.ebl_phase][0]}**\n\n{phase_info[st.session_state.ebl_phase][1]}\n\nLet's continue your inquiry."
                st.session_state.ebl_messages.append(
                    {"role": "assistant", "content": transition_msg}
                )
                st.rerun()

    user_input = st.chat_input(
        "Share your thinking...",
        key="ebl_input",
    )

    if user_input:
        st.session_state.ebl_messages.append(
            {"role": "user", "content": user_input}
        )
        render_message("user", user_input)

        context_note = (
            f"[Student context: {st.session_state.discipline}, {st.session_state.year_of_study}, "
            f"University of Manchester]\n"
            f"[Current EBL Phase: {st.session_state.ebl_phase} — {phase_info[st.session_state.ebl_phase][0]}]\n"
            f"[Facilitate according to Phase {st.session_state.ebl_phase} guidelines. "
            f"If the student seems ready to progress, suggest moving to the next phase.]"
        )

        api_messages = []
        for i, msg in enumerate(st.session_state.ebl_messages):
            if i == 0 and msg["role"] == "assistant":
                api_messages.append(msg)
            elif msg["role"] == "user" and i == len(st.session_state.ebl_messages) - 1:
                api_messages.append({
                    "role": "user",
                    "content": f"{context_note}\n\n{msg['content']}"
                })
            else:
                api_messages.append(msg)

        with st.spinner("Reflecting on your inquiry..."):
            response = call_claude(
                api_messages,
                EBL_SYSTEM_PROMPT,
                use_search=False,
            )

        if st.session_state.ebl_phase < 5:
            transition_keywords = {
                1: ["move to storming", "phase 2", "ready to storm", "let's storm"],
                2: ["move to questioning", "phase 3", "ready to question", "form your questions"],
                3: ["move to seeking", "phase 4", "ready to seek", "where to look"],
                4: ["move to synthesising", "phase 5", "ready to synthesise", "bring it together"],
            }
            check_keys = transition_keywords.get(st.session_state.ebl_phase, [])
            if any(kw in response.lower() for kw in check_keys):
                st.session_state.ebl_phase += 1

        st.session_state.ebl_messages.append(
            {"role": "assistant", "content": response}
        )
        st.rerun()


# ─── Clinical Video Trust Engine ───
elif st.session_state.mode == "video":

    st.markdown(f"""
    <div style="margin-bottom: 1rem;">
        <span style="font-family: 'DM Serif Display', serif; font-size: 1.4rem; color: var(--text-primary);">
            🎥 Clinical Video Trust Engine
        </span>
        <span style="margin-left: 1rem;">
            {render_real_ai_badges(["R", "A", "L"])}
        </span>
    </div>
    """, unsafe_allow_html=True)

    # VTAF Overview
    st.markdown("""
    <div class="ebl-phase">
        <div class="ebl-phase-title">📐 Video Trust Authentication Framework (VTAF)</div>
        <div class="ebl-phase-desc">
            Every video is evaluated against 7 trust dimensions: Author Credentials (25%),
            Institutional Backing (20%), Educational Structure (15%), Skill Transfer Potential (15%),
            Production Quality (10%), Currency & Evidence Alignment (10%), and Professional Engagement (5%).
            Only videos scoring ≥60% are recommended. Full transparency on every score.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Transparency notice
    st.markdown("""
    <div class="limitation-notice">
        <strong>⚠️ Pillar 3 — Transparency Statement:</strong>
        Trust scores are AI-assessed based on available information and may not capture all factors.
        Author credentials are verified where possible but should be independently confirmed.
        Watching a video does not replace supervised clinical practice.
        Always discuss techniques with your clinical supervisors before applying them.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Pre-reflection prompt (REAL-AI Pillar 1)
    if not st.session_state.video_messages:
        st.markdown("""
        <div class="reflection-box">
            <h4>🤔 Before You Search (Pillar 1: Reflective Integration)</h4>
            <p>
                Before watching a clinical video, take a moment to consider:
                What do you already know about this procedure? What specific aspect are you
                uncertain about? This primes your brain to learn actively rather than passively watch.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Display conversation history with embedded videos
    for msg in st.session_state.video_messages:
        if msg["role"] == "user":
            render_message("user", msg["content"])
        else:
            render_message("assistant", msg["content"])

            # Extract and embed any YouTube URLs found in the response
            youtube_ids = re.findall(
                r'https?://(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)([\w-]+)',
                msg["content"]
            )
            # Deduplicate while preserving order
            seen = set()
            unique_ids = []
            for vid_id in youtube_ids:
                if vid_id not in seen:
                    seen.add(vid_id)
                    unique_ids.append(vid_id)

            for vid_id in unique_ids:
                st.markdown(
                    render_youtube_embed(vid_id),
                    unsafe_allow_html=True,
                )

    # Input
    user_input = st.chat_input(
        "Search for a clinical skill or procedure (e.g., 'Class II composite restoration', 'inferior alveolar nerve block')...",
        key="video_input",
    )

    if user_input:
        st.session_state.video_messages.append(
            {"role": "user", "content": user_input}
        )
        render_message("user", user_input)

        # Build trusted channels context
        trusted_context = "\n\n## PRE-VERIFIED TRUSTED CHANNELS\nThe following channels have been pre-verified by DentEdTech™. If you find videos from these channels, their trust floor is already established:\n"
        for category, channels in TRUSTED_CHANNELS.items():
            for ch in channels:
                trusted_context += f"- {ch['channel']} ({ch['category']}) — Trust floor: {ch['trust_floor']}% — {ch['notes']}\n"

        full_system_prompt = VIDEO_SEARCH_SYSTEM_PROMPT + trusted_context

        context_note = (
            f"[Student context: {st.session_state.discipline}, {st.session_state.year_of_study}, "
            f"University of Manchester]\n"
            f"[Search YouTube for clinical skills videos matching this query. Evaluate against VTAF. "
            f"Provide direct YouTube URLs. Prioritise UK dental education where relevant.]"
        )

        api_messages = []
        for i, msg in enumerate(st.session_state.video_messages):
            if msg["role"] == "user" and i == len(st.session_state.video_messages) - 1:
                api_messages.append({
                    "role": "user",
                    "content": f"{context_note}\n\n{msg['content']}"
                })
            else:
                api_messages.append(msg)

        with st.spinner("Searching and evaluating clinical videos against VTAF..."):
            response = call_claude(
                api_messages,
                full_system_prompt,
                use_search=True,
            )

        st.session_state.video_messages.append(
            {"role": "assistant", "content": response}
        )
        st.rerun()
