import streamlit as st
import openai
import anthropic
from google import genai
import time
import re
from datetime import datetime
import random

st.set_page_config(page_title="AEO Diagnostic — Pixii", page_icon="◈", layout="wide", initial_sidebar_state="collapsed")

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
*{box-sizing:border-box;}
#MainMenu, footer, header, .stDeployButton, [data-testid="stToolbar"]{display:none!important;}
.stApp{
  background:
    radial-gradient(900px 480px at 12% -6%, rgba(99,102,241,0.16), transparent 60%),
    radial-gradient(850px 420px at 92% -10%, rgba(16,185,129,0.08), transparent 58%),
    #0a1020!important;
  color:#e5e7eb;
  font-family:'Inter',sans-serif!important;
}
.block-container{max-width:1120px;padding:0 1.2rem 3.2rem 1.2rem!important;}
section[data-testid="stSidebar"]{display:none!important;}

:root{
  --primary:#6366f1;
  --primary-2:#8b5cf6;
  --success:#10b981;
  --warning:#f59e0b;
  --danger:#ef4444;
  --text:#e2e8f0;
  --muted:#94a3b8;
  --card:#0f172a;
  --card-soft:#111a31;
  --border:rgba(148,163,184,.2);
}

.topnav{
  position:sticky;top:0;z-index:20;height:62px;display:flex;align-items:center;justify-content:space-between;
  padding:0 2px;margin-bottom:18px;background:rgba(10,16,32,.68);backdrop-filter:blur(12px);border-bottom:1px solid rgba(148,163,184,.12);
}
.topnav-left{display:flex;align-items:center;gap:10px;}
.topnav-logo{
  width:28px;height:28px;border-radius:8px;display:flex;align-items:center;justify-content:center;
  font-size:12px;font-weight:900;color:#fff;background:linear-gradient(135deg,var(--primary),var(--primary-2));
  box-shadow:0 8px 22px rgba(99,102,241,.38);
}
.topnav-name{font-size:14px;font-weight:700;color:#f8fafc;letter-spacing:-.02em;}
.topnav-tag{font-size:11px;font-weight:600;color:#94a3b8;letter-spacing:.08em;text-transform:uppercase;}
.live-badge{
  display:inline-flex;align-items:center;gap:7px;padding:5px 10px;border-radius:999px;
  border:1px solid rgba(16,185,129,.32);background:rgba(16,185,129,.1);color:#6ee7b7;font-size:11px;font-weight:700;
}
.live-dot{width:6px;height:6px;border-radius:50%;background:var(--success);animation:pulse 1.8s infinite;}
@keyframes pulse{0%,100%{opacity:1;}50%{opacity:.25;}}

.hero{
  text-align:center;padding:26px 0 30px;margin-bottom:8px;
}
.hero-badge{
  display:inline-flex;align-items:center;gap:7px;padding:6px 13px;border-radius:999px;
  border:1px solid rgba(99,102,241,.38);background:rgba(99,102,241,.12);color:#c7d2fe;font-size:11px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;
}
.hero h1{font-size:clamp(2.2rem,4.6vw,4rem);line-height:1.02;margin:15px 0 14px;letter-spacing:-.045em;color:#f8fafc;}
.hero .grad{
  background:linear-gradient(135deg,#a5b4fc 0%,#c4b5fd 52%,#6ee7b7 100%);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
}
.hero p{max-width:760px;margin:0 auto;color:#9fb0c9;font-size:15px;line-height:1.75;}
.pills{margin-top:18px;display:flex;justify-content:center;gap:8px;flex-wrap:wrap;}
.pill{
  font-size:12px;color:#b8c5dc;background:rgba(148,163,184,.08);border:1px solid rgba(148,163,184,.2);
  border-radius:999px;padding:6px 12px;
}

.card{
  background:linear-gradient(180deg, rgba(17,26,49,.98), rgba(14,23,42,.98));
  border:1px solid var(--border);border-radius:18px;padding:22px 20px;position:relative;overflow:hidden;margin-bottom:14px;
  box-shadow:0 10px 28px rgba(2,6,23,.35);transition:transform .2s ease, border-color .2s ease, box-shadow .2s ease;
}
.card:hover{transform:translateY(-2px);border-color:rgba(129,140,248,.45);box-shadow:0 14px 34px rgba(2,6,23,.48);}
.card:before{
  content:"";position:absolute;inset:0;pointer-events:none;
  background:linear-gradient(120deg, rgba(99,102,241,.09), rgba(16,185,129,.02) 40%, rgba(245,158,11,.03) 80%);
}
.section-label{
  font-size:11px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#a8b8d2;margin-bottom:14px;display:flex;align-items:center;gap:10px;
}
.section-label:after{content:"";height:1px;flex:1;background:rgba(148,163,184,.2);}
.field-label{font-size:11px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#aebfd8;margin-bottom:6px;}
.helper{font-size:12px;color:#8ea1be;margin-top:6px;line-height:1.6;}
.divline{height:1px;background:rgba(148,163,184,.16);margin:18px 0;}

div[data-testid="stTextInput"] label,div[data-testid="stTextInput"] > div > label{display:none!important;}
div[data-testid="stTextInput"] > div > div{background:transparent!important;border:none!important;box-shadow:none!important;}
div[data-testid="stTextInput"] > div > div > input{
  background:#0b1327!important;border:1px solid rgba(148,163,184,.32)!important;color:#e2e8f0!important;
  border-radius:12px!important;padding:11px 12px!important;height:44px!important;font-size:13px!important;transition:.2s!important;
}
div[data-testid="stTextInput"] > div > div > input::placeholder{color:#7087aa!important;}
div[data-testid="stTextInput"] > div > div > input:focus{
  border-color:rgba(129,140,248,.7)!important;box-shadow:0 0 0 3px rgba(99,102,241,.2)!important;
}

div[data-testid="stButton"] > button{
  width:100%!important;height:48px!important;border:none!important;border-radius:12px!important;
  background:linear-gradient(135deg,var(--primary),var(--primary-2))!important;color:#fff!important;
  font-size:14px!important;font-weight:700!important;letter-spacing:-.01em!important;
  box-shadow:0 10px 24px rgba(99,102,241,.35)!important;transition:.2s!important;
}
div[data-testid="stButton"] > button:hover{transform:translateY(-1px)!important;box-shadow:0 14px 28px rgba(99,102,241,.45)!important;}

.kpi{
  display:grid;grid-template-columns:180px 1fr;gap:20px;align-items:center;padding:4px 0;
}
.ring{
  width:160px;height:160px;border-radius:50%;display:flex;align-items:center;justify-content:center;margin:auto;
  background:conic-gradient(var(--ring-color) calc(var(--score)*1%), rgba(148,163,184,.16) 0);
  position:relative;
}
.ring:after{
  content:"";position:absolute;width:126px;height:126px;border-radius:50%;background:#0f172a;border:1px solid rgba(148,163,184,.2);
}
.ring-num{position:relative;z-index:2;font-size:36px;font-weight:800;color:#f8fafc;}
.score-grade{display:inline-flex;padding:6px 12px;border-radius:999px;font-size:12px;font-weight:700;border:1px solid transparent;margin:8px 0;}
.gA{background:rgba(16,185,129,.14);color:#6ee7b7;border-color:rgba(16,185,129,.35);}
.gB{background:rgba(99,102,241,.16);color:#c7d2fe;border-color:rgba(99,102,241,.42);}
.gC{background:rgba(245,158,11,.15);color:#fcd34d;border-color:rgba(245,158,11,.4);}
.gD{background:rgba(249,115,22,.14);color:#fdba74;border-color:rgba(249,115,22,.38);}
.gF{background:rgba(239,68,68,.14);color:#fca5a5;border-color:rgba(239,68,68,.4);}
.score-title{font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:#8fa3c3;font-weight:700;}
.score-desc{color:#9eb0cb;font-size:14px;line-height:1.75;max-width:560px;}

.insight{
  border-radius:14px;padding:14px 14px;border:1px solid transparent;font-size:14px;line-height:1.65;font-weight:600;
}
.ins-low{background:rgba(239,68,68,.12);border-color:rgba(239,68,68,.36);color:#fecaca;}
.ins-mid{background:rgba(245,158,11,.14);border-color:rgba(245,158,11,.36);color:#fde68a;}
.ins-high{background:rgba(16,185,129,.14);border-color:rgba(16,185,129,.36);color:#bbf7d0;}

.engine{
  height:100%;display:flex;flex-direction:column;background:rgba(15,23,42,.72);border:1px solid rgba(148,163,184,.2);border-radius:14px;padding:14px;
}
.engine-head{display:flex;align-items:center;gap:9px;margin-bottom:10px;}
.engine-ico{width:30px;height:30px;border-radius:9px;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:800;color:#fff;}
.ico-g{background:linear-gradient(135deg,#10b981,#34d399);}
.ico-c{background:linear-gradient(135deg,#f59e0b,#fbbf24);}
.ico-m{background:linear-gradient(135deg,#6366f1,#8b5cf6);}
.engine-name{font-size:13px;font-weight:700;color:#e2e8f0;}
.engine-maker{font-size:11px;color:#8fa3c3;}
.engine-resp{
  color:#9eb0cb;font-size:12.8px;line-height:1.74;flex:1;overflow:auto;max-height:180px;padding-right:4px;
}
.engine-found{margin-top:10px;display:inline-flex;padding:4px 9px;border-radius:8px;font-size:11px;font-weight:700;}
.ef-yes{background:rgba(16,185,129,.12);color:#6ee7b7;border:1px solid rgba(16,185,129,.32);}
.ef-no{background:rgba(239,68,68,.12);color:#fca5a5;border:1px solid rgba(239,68,68,.32);}

.bar-row{display:flex;align-items:center;gap:12px;padding:10px 0;border-bottom:1px solid rgba(148,163,184,.12);}
.bar-row:last-child{border-bottom:none;}
.bar-name{width:120px;font-size:13px;color:#bfcee5;font-weight:600;}
.bar-track{height:8px;flex:1;border-radius:999px;background:rgba(148,163,184,.18);overflow:hidden;}
.bar-fill{height:100%;border-radius:999px;background:linear-gradient(90deg,#818cf8,#6ee7b7);}
.bar-value{width:50px;text-align:right;font-size:12px;font-weight:700;color:#cdd9ec;}

.why{font-size:14px;line-height:1.8;color:#9eb0cb;}
.kw-wrap{display:flex;flex-wrap:wrap;gap:7px;}
.kw{
  padding:5px 10px;border:1px solid rgba(148,163,184,.24);border-radius:8px;background:rgba(148,163,184,.08);font-size:12px;color:#cad7ea;
}
.kw.lit{background:rgba(99,102,241,.2);border-color:rgba(129,140,248,.45);color:#dbe3ff;}
.rec{
  display:flex;gap:10px;align-items:flex-start;padding:13px 14px;border-radius:12px;border:1px solid rgba(148,163,184,.2);
  background:rgba(15,23,42,.72);margin-bottom:8px;transition:.2s;
}
.rec:hover{border-color:rgba(129,140,248,.45);transform:translateY(-1px);}
.rec-num{
  width:24px;height:24px;display:flex;align-items:center;justify-content:center;border-radius:7px;font-size:11px;font-weight:800;
  color:#fff;background:linear-gradient(135deg,var(--primary),var(--primary-2));flex-shrink:0;
}
.rec-text{font-size:13.2px;line-height:1.72;color:#9eb0cb;}
.rec-text strong{color:#d2def0;}
.subhead{
  margin:18px 0 10px;font-size:11px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#9cb0cf;display:flex;align-items:center;gap:8px;
}
.subhead:after{content:"";height:1px;flex:1;background:rgba(148,163,184,.2);}
.foot{
  margin-top:16px;text-align:center;color:#7f93b2;font-size:11.5px;padding-top:16px;border-top:1px solid rgba(148,163,184,.14);
}
.demo-banner{
  padding:10px 12px;margin:6px 0 12px;border-radius:10px;
  background:rgba(245,158,11,.12);border:1px solid rgba(245,158,11,.35);
  color:#fde68a;font-size:12px;font-weight:600;
}
.empty{
  margin-top:10px;padding:44px 22px;text-align:center;border:1px dashed rgba(148,163,184,.35);
  border-radius:18px;background:rgba(15,23,42,.45);color:#9db0cc;
}
.empty .icon{font-size:28px;opacity:.7;margin-bottom:10px;}
.empty .title{font-size:16px;font-weight:700;color:#dce6f6;margin-bottom:8px;}
.empty .desc{font-size:13px;line-height:1.7;}

@media (max-width: 900px){
  .kpi{grid-template-columns:1fr;}
  .topnav-tag{display:none;}
}
</style>
""",
    unsafe_allow_html=True,
)

# ── helpers ──────────────────────────────────────────────────────────────────
def grade(s):
    if s>=90: return "A+","gA","Exceptional. You dominate AI-generated answers across all engines."
    if s>=80: return "A","gA","Strong. AI models frequently recommend your brand."
    if s>=70: return "B+","gB","Good. A few targeted optimizations will push you to the top."
    if s>=60: return "B","gB","Moderate. Competitors are likely ranking above you in AI answers."
    if s>=50: return "C","gC","Weak. AI models rarely surface your brand organically."
    if s>=30: return "D","gD","Poor. Immediate action needed before competitors pull further ahead."
    return "F","gF","Invisible. Your product is absent from all AI recommendations."

def hit(text, brand):
    return bool(brand.strip()) and brand.lower() in text.lower()

def keys(q):
    stop = {
        "for", "the", "a", "an", "of", "in", "and", "or", "to", "is", "are",
        "best", "top", "good", "my", "me", "most", "with", "what", "which", "that"
    }
    return [w for w in re.findall(r"\b[a-z]+\b", q.lower()) if w not in stop and len(w) > 2]

def ask_gpt(q, k):
    try:
        r = openai.OpenAI(api_key=k).chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful shopping assistant. Recommend specific named products/brands in 2-3 concise sentences."},
                {"role": "user", "content": f"What is the {q}?"},
            ],
            max_tokens=200,
        )
        return r.choices[0].message.content
    except Exception:
        return None

def ask_claude(q, k):
    try:
        r = anthropic.Anthropic(api_key=k).messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=200,
            messages=[{"role": "user", "content": f"What is the {q}? Name 2-3 specific products or brands concisely."}],
        )
        return r.content[0].text
    except Exception:
        return None

def ask_gemini(q, k):
    try:
        r = genai.Client(api_key=k).models.generate_content(
            model="gemini-2.0-flash",
            contents=f"What is the {q}? Name 2-3 specific products or brands. Be concise.",
        )
        return r.text
    except Exception:
        return None

def action_plan(q, brand, gr, cr, mr, score):
    kw = keys(q)
    out = []
    if score < 70:
        out.append(
            f"<strong>Keyword-optimize your listing</strong> — weave terms like <em>{', '.join(kw[:4])}</em> into your title, bullet points, and A+ content. AI models pull answers directly from indexed product data."
        )
    if not hit(gr, brand):
        out.append("<strong>Build presence on GPT-indexed platforms</strong> — Reddit threads, Quora answers, and niche review sites. GPT learns from public conversation, not just product pages.")
    if not hit(cr, brand):
        out.append("<strong>Get featured in editorial content</strong> — buying guides, comparison articles, and authority blogs. Claude is trained on third-party editorial sources, not listings.")
    if not hit(mr, brand):
        out.append("<strong>Strengthen Google SEO</strong> — Gemini pulls from Google Search. Prioritize structured data markup, Google Shopping optimization, and ranking for category keywords.")
    if score >= 70:
        out.append("<strong>Stay ahead with freshness</strong> — you're ranking well. Continuously add new reviews, update listings with trending keywords, and monitor competitor movements.")
    out.append("<strong>Drive review volume strategically</strong> — prompt buyers to mention their specific use case. AI models identify patterns in review text to assess product relevance.")
    return out[:5]

def simulate_competitors(score):
    return [
        ("Your Brand", score),
        ("Competitor A", max(22, min(95, score - 7))),
        ("Competitor B", max(18, min(92, score - 14))),
        ("Competitor C", max(15, min(90, score - 22))),
    ]


def mock_response(engine_name, query, brand):
    products = [
        "Thorne", "Nature Made", "Garden of Life", "NOW Foods", "Ritual", "Nordic Naturals"
    ]
    brand_candidate = brand.strip() if brand.strip() else random.choice(products)
    if engine_name == "gpt":
        return f"For '{query}', common recommendations include {brand_candidate}, Thorne, and Garden of Life due to quality consistency and customer trust."
    if engine_name == "claude":
        return f"Top options for '{query}' are Nature Made, {brand_candidate}, and NOW Foods. Compare dosage transparency, certifications, and review sentiment."
    return f"Popular choices for '{query}' include {brand_candidate}, Ritual, and Nordic Naturals. Buyers often prioritize verified quality and clear ingredient labeling."


def get_demo_responses(query, brand):
    return (
        mock_response("gpt", query, brand),
        mock_response("claude", query, brand),
        mock_response("gemini", query, brand),
    )


def calculate_score(query, brand, gr, cr, mr):
    gf, cf, mf = hit(gr, brand), hit(cr, brand), hit(mr, brand)
    kw = keys(query)
    combined = f"{gr} {cr} {mr}".lower()
    kw_hits = sum(1 for w in kw if w in combined)
    kw_bonus = min(12, kw_hits * 2)
    brand_weight = min(10, (gf + cf + mf) * 3 + (4 if brand.strip() else 0))
    engine_points = (gf + cf + mf) * 30
    score = max(0, min(100, engine_points + kw_bonus + brand_weight))
    return score, gf, cf, mf, kw


def key_insight(score, brand):
    b = brand.strip() if brand.strip() else "your brand"
    if score < 45:
        return "ins-low", f"{b} is mostly invisible in AI answers right now. You are losing high-intent demand to better-optimized competitors."
    if score < 75:
        return "ins-mid", f"{b} has partial visibility, but recommendation consistency is weak. A focused optimization sprint can materially improve conversion share."
    return "ins-high", f"{b} is showing strong AI discoverability. Keep momentum by refreshing content and defending against competitor gains."


def loading_experience():
    steps = [
        "Analyzing across AI engines...",
        "Comparing responses...",
        "Calculating AEO score...",
        "Preparing your strategy brief...",
    ]
    status = st.empty()
    bar = st.progress(0)
    for idx, step in enumerate(steps, start=1):
        status.info(step)
        bar.progress(int((idx / len(steps)) * 100))
        time.sleep(0.45)
    status.empty()
    bar.empty()


def set_example_query(value):
    # Safe state update via callback before widget re-render.
    st.session_state["q"] = value


def header():
    st.markdown(
        """
        <div class="topnav">
          <div class="topnav-left">
            <div class="topnav-logo">◈</div>
            <span class="topnav-name">Pixii AEO</span>
          </div>
          <div style="display:flex;align-items:center;gap:14px;">
            <span class="topnav-tag">Answer Engine Optimization Intelligence</span>
            <div class="live-badge"><div class="live-dot"></div>Live</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def hero():
    st.markdown(
        """
        <div class="hero">
          <div class="hero-badge">AI Visibility Diagnostic</div>
          <h1>Is Your Product <span class="grad">Winning AI Answers?</span></h1>
          <p>Evaluate how GPT-4o, Claude, and Gemini recommend your brand, then get an investor-grade action brief to improve discoverability and revenue impact.</p>
          <div class="pills">
            <div class="pill">⚡ Fast multi-model analysis</div>
            <div class="pill">🤖 GPT + Claude + Gemini</div>
            <div class="pill">📊 100-point visibility score</div>
            <div class="pill">🚀 Tactical action plan</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def input_form():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">API Credentials</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="field-label">OpenAI Key</div>', unsafe_allow_html=True)
        ok = st.text_input("ok", label_visibility="collapsed", type="password", placeholder="sk-...", key="ok")
        st.markdown('<div class="helper">Used for GPT-4o mini diagnostic response.</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="field-label">Anthropic Key</div>', unsafe_allow_html=True)
        ak = st.text_input("ak", label_visibility="collapsed", type="password", placeholder="sk-ant-...", key="ak")
        st.markdown('<div class="helper">Used for Claude 3 Haiku response.</div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="field-label">Gemini Key</div>', unsafe_allow_html=True)
        gk = st.text_input("gk", label_visibility="collapsed", type="password", placeholder="AIza...", key="gk")
        st.markdown('<div class="helper">Used for Gemini 2.0 Flash response.</div>', unsafe_allow_html=True)

    st.markdown('<div class="divline"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Product Context</div>', unsafe_allow_html=True)
    q1, q2 = st.columns([3, 2])
    with q1:
        st.markdown('<div class="field-label">Product Query</div>', unsafe_allow_html=True)
        query = st.text_input("q", label_visibility="collapsed", placeholder='e.g. "best magnesium supplement for seniors"', key="q")
        st.markdown('<div class="helper">Describe the exact customer search intent you want to rank for.</div>', unsafe_allow_html=True)
    with q2:
        st.markdown('<div class="field-label">Brand Name</div>', unsafe_allow_html=True)
        brand = st.text_input("b", label_visibility="collapsed", placeholder='e.g. "Nature Made"', key="b")
        st.markdown('<div class="helper">We detect whether this brand appears in each model output.</div>', unsafe_allow_html=True)

    st.markdown('<div style="height:4px"></div>', unsafe_allow_html=True)
    st.markdown('<div class="field-label">Try an example query</div>', unsafe_allow_html=True)
    eq1, eq2, eq3 = st.columns(3)
    eq1.button(
        "Best CRM for startups",
        key="ex_q1",
        on_click=set_example_query,
        args=("best CRM for startups",),
        use_container_width=True,
    )
    eq2.button(
        "Best magnesium supplement for seniors",
        key="ex_q2",
        on_click=set_example_query,
        args=("best magnesium supplement for seniors",),
        use_container_width=True,
    )
    eq3.button(
        "Best project management tool for teams",
        key="ex_q3",
        on_click=set_example_query,
        args=("best project management tool for teams",),
        use_container_width=True,
    )

    st.markdown('<div style="height:6px"></div>', unsafe_allow_html=True)
    go = st.button("Analyze My AEO Score", key="go")
    st.markdown('</div>', unsafe_allow_html=True)
    return ok, ak, gk, query, brand, go


def render_results(query, brand, gr, cr, mr, elapsed, demo_mode=False):
    sc, gf, cf, mf, kw = calculate_score(query, brand, gr, cr, mr)
    g, gcls, gdesc = grade(sc)
    ring_color = "#10b981" if sc >= 75 else "#f59e0b" if sc >= 45 else "#ef4444"
    ins_class, insight = key_insight(sc, brand)

    if demo_mode:
        st.markdown('<div class="demo-banner">Demo mode active (API fallback)</div>', unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="card">
          <div class="kpi">
            <div class="ring" style="--score:{sc};--ring-color:{ring_color};">
              <div class="ring-num">{sc}</div>
            </div>
            <div>
              <div class="score-title">Your AEO Score</div>
              <div class="helper" title="Score = 30 points per engine match + keyword relevance bonus + brand presence weight (clamped to 100).">How score works: engine match + relevance + brand weight</div>
              <div class="score-grade {gcls}">Grade {g}</div>
              <div class="score-desc">{gdesc}</div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="subhead">Key Insight</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="insight {ins_class}">{insight}</div>', unsafe_allow_html=True)

    st.markdown('<div class="subhead">AI Engine Responses</div>', unsafe_allow_html=True)
    e1, e2, e3 = st.columns(3)
    engines = [
        (e1, "ico-g", "G", "GPT-4o", "OpenAI", gr, gf),
        (e2, "ico-c", "C", "Claude 3", "Anthropic", cr, cf),
        (e3, "ico-m", "◈", "Gemini", "Google", mr, mf),
    ]
    for col, ico_class, icon, name, maker, resp, found in engines:
        with col:
            brand_badge = (
                f'<div class="engine-found ef-yes">✓ {brand} detected</div>'
                if found and brand
                else f'<div class="engine-found ef-no">✗ {brand or "Brand"} not detected</div>'
            )
            st.markdown(
                f"""
                <div class="engine">
                  <div class="engine-head">
                    <div class="engine-ico {ico_class}">{icon}</div>
                    <div>
                      <div class="engine-name">{name}</div>
                      <div class="engine-maker">{maker}</div>
                    </div>
                  </div>
                  <div class="engine-resp">{resp}</div>
                  {brand_badge}
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown('<div class="subhead">Visibility by Engine</div>', unsafe_allow_html=True)
    visibility_rows = ""
    for label, found in [("GPT-4o", gf), ("Claude 3", cf), ("Gemini", mf)]:
        visibility_rows += (
            f'<div class="bar-row"><div class="bar-name">{label}</div>'
            f'<div class="bar-track"><div class="bar-fill" style="width:{"100%" if found else "8%"}"></div></div>'
            f'<div class="bar-value">{"Found" if found else "Low"}</div></div>'
        )
    st.markdown(f'<div class="card">{visibility_rows}</div>', unsafe_allow_html=True)

    st.markdown('<div class="subhead">Competitor Comparison</div>', unsafe_allow_html=True)
    comp_rows = ""
    for name, val in simulate_competitors(sc):
        comp_rows += (
            f'<div class="bar-row"><div class="bar-name">{name}</div>'
            f'<div class="bar-track"><div class="bar-fill" style="width:{val}%"></div></div>'
            f'<div class="bar-value">{val}</div></div>'
        )
    st.markdown(f'<div class="card">{comp_rows}</div>', unsafe_allow_html=True)

    st.markdown('<div class="subhead">Why This Matters</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="card">
          <div class="why">
            AI assistants are becoming a top-of-funnel acquisition channel for high-intent buyers.
            Strong AEO performance increases brand mentions, protects category share, and improves conversion from recommendation to purchase.
            Improving visibility now compounds over time as models repeatedly reference trusted sources.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if kw:
        st.markdown('<div class="subhead">Keywords Detected</div>', unsafe_allow_html=True)
        all_responses = (gr + cr + mr).lower()
        chips = "".join(f'<span class="kw{" lit" if w in all_responses else ""}">{w}</span>' for w in kw)
        st.markdown(f'<div class="card"><div class="kw-wrap">{chips}</div></div>', unsafe_allow_html=True)
        st.caption("Highlighted keywords are present in at least one AI response.")

    st.markdown('<div class="subhead">Action Plan</div>', unsafe_allow_html=True)
    for idx, rec in enumerate(action_plan(query, brand, gr, cr, mr, sc), start=1):
        st.markdown(f'<div class="rec"><div class="rec-num">{idx}</div><div class="rec-text">{rec}</div></div>', unsafe_allow_html=True)

    st.button("Improve My Ranking", key="cta_improve")

    st.markdown(
        f'<div class="foot">Completed in {elapsed}s · {datetime.now().strftime("%b %d, %Y %H:%M")} · GPT-4o · Claude 3 Haiku · Gemini 2.0 Flash<br/>Built by Sunil Nagarkoti</div>',
        unsafe_allow_html=True,
    )


def render_empty_state():
    st.markdown(
        """
        <div class="empty">
          <div class="icon">◈</div>
          <div class="title">Ready for your AEO diagnostic</div>
          <div class="desc">
            Add your API keys and product context above, then run analysis to generate a premium visibility report with score, insights, competitor benchmark, and action plan.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def run():
    header()
    hero()
    ok, ak, gk, query, brand, go = input_form()

    if not go:
        render_empty_state()
        return

    if not query.strip():
        st.warning("Enter a product query to continue.")
        return

    loading_experience()
    demo_mode = False
    t0 = time.time()

    # Fail-safe mode: always deliver a report, even when keys or APIs fail.
    if not all([ok, ak, gk]):
        demo_mode = True
        gr, cr, mr = get_demo_responses(query, brand)
    else:
        gr = ask_gpt(query, ok)
        cr = ask_claude(query, ak)
        mr = ask_gemini(query, gk)
        if not all([gr, cr, mr]):
            demo_mode = True
            gr, cr, mr = get_demo_responses(query, brand)
        else:
            gr = gr.strip() if isinstance(gr, str) else str(gr)
            cr = cr.strip() if isinstance(cr, str) else str(cr)
            mr = mr.strip() if isinstance(mr, str) else str(mr)

    elapsed = round(time.time() - t0, 1)
    render_results(query, brand, gr, cr, mr, elapsed, demo_mode=demo_mode)


run()