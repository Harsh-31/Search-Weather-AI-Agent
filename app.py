import streamlit as st
import os
from dotenv import load_dotenv

st.set_page_config(
    page_title="Weather Agentic AI",
    page_icon="🌤️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True
if "response" not in st.session_state:
    st.session_state.response = None

dark = st.session_state.dark_mode

if dark:
    BG           = "#0f0d1a"
    BG_CARD      = "rgba(255,255,255,0.05)"
    BG_INPUT     = "#1c1830"
    BORDER       = "rgba(255,255,255,0.10)"
    BORDER_FOCUS = "rgba(139,92,246,0.7)"
    TEXT1        = "#f0eeff"
    TEXT2        = "rgba(240,238,255,0.50)"
    ACCENT       = "#8b5cf6"
    GLOW         = "rgba(139,92,246,0.18)"
    BTN_BG       = "#7c3aed"
    BADGE_BG     = "rgba(139,92,246,0.20)"
    BADGE_TEXT   = "#c4b5fd"
    ANS_BG       = "rgba(139,92,246,0.08)"
    ANS_BORDER   = "rgba(139,92,246,0.28)"
    T_ICON       = "☀️"
    T_LABEL      = "Light mode"
else:
    BG           = "#f5f3ff"
    BG_CARD      = "#ffffff"
    BG_INPUT     = "#ede9fe"
    BORDER       = "rgba(0,0,0,0.09)"
    BORDER_FOCUS = "rgba(109,40,217,0.6)"
    TEXT1        = "#1e1b4b"
    TEXT2        = "#6b7280"
    ACCENT       = "#6d28d9"
    GLOW         = "rgba(109,40,217,0.10)"
    BTN_BG       = "#7c3aed"
    BADGE_BG     = "#ede9fe"
    BADGE_TEXT   = "#5b21b6"
    ANS_BG       = "#f5f3ff"
    ANS_BORDER   = "rgba(109,40,217,0.22)"
    T_ICON       = "🌙"
    T_LABEL      = "Dark mode"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="stMainBlockContainer"] {{
  background: {BG} !important;
  font-family: 'Inter', sans-serif !important;
}}

[data-testid="stHeader"], [data-testid="stToolbar"],
[data-testid="stDecoration"], [data-testid="stStatusWidget"],
footer, #MainMenu, [data-testid="stSidebar"] {{
  display: none !important;
}}

.block-container {{
  max-width: 660px !important;
  padding: 0 1.5rem 4rem !important;
  margin: 0 auto !important;
}}

/* ── Topbar toggle button — override default Streamlit button style ── */
[data-testid="stButton"] button {{
  background: rgba(255,255,255,0.07) !important;
  border: 1px solid {BORDER} !important;
  border-radius: 999px !important;
  padding: 7px 18px !important;
  font-size: 13px !important;
  font-weight: 500 !important;
  color: {TEXT2} !important;
  width: auto !important;
  white-space: nowrap !important;
  transition: background 0.2s, border-color 0.2s, color 0.2s !important;
}}
[data-testid="stButton"] button:hover {{
  background: {GLOW} !important;
  border-color: {ACCENT} !important;
  color: {ACCENT} !important;
}}

/* ── Submit button — target by key via aria-label trick ── */
button[kind="primary"],
[data-testid="stButton"]:has(button p:first-child) {{
  width: 100% !important;
}}
.submit-btn [data-testid="stButton"] button {{
  width: 100% !important;
  background: linear-gradient(135deg, #7c3aed, #5b21b6) !important;
  color: #fff !important;
  font-weight: 600 !important;
  font-size: 15px !important;
  border: none !important;
  border-radius: 14px !important;
  padding: 0.85rem 1.5rem !important;
  margin-top: 0 !important;
}}
.submit-btn [data-testid="stButton"] button:hover {{
  opacity: 0.88 !important;
  background: linear-gradient(135deg, #7c3aed, #5b21b6) !important;
  border-color: transparent !important;
  color: #fff !important;
}}

/* ── Textarea ── */
.stTextArea label,
.stTextArea [data-testid="InputInstructions"] {{ display: none !important; }}
.stTextArea > div {{ background: transparent !important; border: none !important; padding: 0 !important; }}
[data-baseweb="textarea"] {{ background: transparent !important; border: none !important; padding: 0 !important; }}
.stTextArea textarea {{
  background: {BG_INPUT} !important;
  border: 1.5px solid {BORDER} !important;
  border-radius: 16px !important;
  color: {TEXT1} !important;
  font-size: 15px !important;
  font-family: 'Inter', sans-serif !important;
  padding: 14px 16px !important;
  resize: none !important;
  box-shadow: none !important;
  transition: border-color 0.2s, box-shadow 0.2s !important;
}}
.stTextArea textarea:focus {{
  border-color: {BORDER_FOCUS} !important;
  box-shadow: 0 0 0 4px {GLOW} !important;
  outline: none !important;
}}
.stTextArea textarea::placeholder {{ color: {TEXT2} !important; opacity: 1 !important; }}

/* ── Answer card ── */
.acard {{
  background: {ANS_BG}; border: 1.5px solid {ANS_BORDER};
  border-radius: 20px; padding: 1.6rem 1.75rem;
  position: relative; overflow: hidden;
}}
.acard::before {{
  content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px;
  background: linear-gradient(90deg, {ACCENT}, #a78bfa, {ACCENT});
}}
.ahead {{ display: flex; align-items: center; gap: 10px; margin-bottom: 1rem; }}
.aicon {{
  width: 34px; height: 34px; border-radius: 10px; background: {BADGE_BG};
  display: flex; align-items: center; justify-content: center;
  font-size: 17px; flex-shrink: 0;
}}
.atitle {{ font-size: 11px; font-weight: 600; color: {BADGE_TEXT}; letter-spacing: 0.09em; text-transform: uppercase; }}
.abody {{ font-size: 15px; line-height: 1.78; color: {TEXT1}; white-space: pre-wrap; word-break: break-word; }}

[data-testid="stSpinner"] p {{ color: {TEXT2} !important; font-size: 14px !important; }}

::-webkit-scrollbar {{ width: 4px; }}
::-webkit-scrollbar-thumb {{ background: rgba(139,92,246,0.3); border-radius: 4px; }}
</style>
""", unsafe_allow_html=True)

# ── TOPBAR ────────────────────────────────────────────────────────────────────
c1, c2 = st.columns([5, 2])
with c1:
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:9px;padding:1.4rem 0 1rem;">
      <span style="width:8px;height:8px;border-radius:50%;background:{ACCENT};
        display:inline-block;flex-shrink:0;"></span>
      <span style="font-size:15px;font-weight:600;color:{TEXT1};
        letter-spacing:-0.01em;">Weather AI</span>
    </div>
    """, unsafe_allow_html=True)
with c2:
    st.markdown(f"<div style='padding-top:1rem;display:flex;justify-content:flex-end;'>", unsafe_allow_html=True)
    if st.button(f"{T_ICON} {T_LABEL}", key="theme_btn"):
        st.session_state.dark_mode = not dark
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown(f'<hr style="border:none;border-top:1px solid {BORDER};margin:0;">', unsafe_allow_html=True)

# ── HERO — full width, properly centered ──────────────────────────────────────
st.markdown(f"""
<div style="text-align:center;padding:2.75rem 0 2rem;width:100%;">
  <div style="display:inline-flex;align-items:center;gap:6px;
    background:{BADGE_BG};color:{BADGE_TEXT};font-size:12px;font-weight:500;
    padding:5px 14px;border-radius:999px;margin-bottom:1.25rem;
    border:1px solid {BORDER};">
    ✦ Powered by GPT-3.5 + ReAct Agent
  </div>
  <div style="font-size:clamp(1.8rem,5vw,2.4rem);font-weight:700;color:{TEXT1};
    letter-spacing:-0.03em;line-height:1.2;margin-bottom:1rem;">
    Hello, Welcome to<br>
    <span style="color:{ACCENT};">Weather Agentic AI</span> App
  </div>
  <p style="font-size:15px;color:{TEXT2};line-height:1.65;
    max-width:430px;margin:0 auto;">
    Ask about weather, current events, or anything else — the agent
    thinks, searches, and answers in real time.
  </p>
</div>
""", unsafe_allow_html=True)

# ── QUICK PROMPTS ─────────────────────────────────────────────────────────────
pills_data = ["🌤 Weather in Tokyo","🌧 Weather in London","🌡 Hottest city today","❄️ Weather in Iceland","🌊 Hurricane updates"]
html = f"""
<div style="margin-bottom:2rem;">
  <span style="display:block;font-size:11px;font-weight:600;color:{TEXT2};
    letter-spacing:0.09em;text-transform:uppercase;margin-bottom:12px;">
    Quick prompts
  </span>
  <div style="display:flex;flex-wrap:wrap;gap:8px;">
"""
for p in pills_data:
    html += f"""<span style="background:{BG_CARD};border:1px solid {BORDER};
      border-radius:999px;padding:7px 15px;font-size:13px;color:{TEXT2};
      font-family:'Inter',sans-serif;">{p}</span>"""
html += "</div></div>"
st.markdown(html, unsafe_allow_html=True)

# ── YOUR QUESTION label ───────────────────────────────────────────────────────
st.markdown(f"""
<span style="display:block;font-size:11px;font-weight:600;color:{TEXT2};
  letter-spacing:0.09em;text-transform:uppercase;margin-bottom:8px;">
  Your question
</span>
""", unsafe_allow_html=True)

# ── TEXTAREA (no wrapper div — placed naked) ──────────────────────────────────
user_query = st.text_area(
    label="q", label_visibility="collapsed",
    placeholder="e.g. What is the current weather in Paris, and any recent news about it?",
    height=130, key="user_query",
)

# ── GAP then SUBMIT ───────────────────────────────────────────────────────────
st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
st.markdown('<div class="submit-btn">', unsafe_allow_html=True)
submit = st.button("✦  Ask the Agent  →", key="submit_btn")
st.markdown('</div>', unsafe_allow_html=True)

# ── AGENT ─────────────────────────────────────────────────────────────────────
def run_agent(query: str):
    import requests as req_lib
    from langchain_openai import ChatOpenAI
    from langchain_community.tools.tavily_search import TavilySearchResults
    from langchain import hub
    from langchain.tools import tool
    from langchain.agents import create_react_agent, AgentExecutor

    load_dotenv()
    OPENAI_API_KEY       = os.getenv("OPENAI_API_KEY")
    WEATHERSTACK_API_KEY = os.getenv("WEATHER_STACK_API")
    search_tool = TavilySearchResults(max_results=2)

    @tool
    def get_weather_data(city: str) -> str:
        """Fetch current weather information for a given city using WeatherStack API."""
        url = f"https://api.weatherstack.com/current?access_key={WEATHERSTACK_API_KEY}&query={city}"
        data = req_lib.get(url).json()
        if "current" not in data:
            return f"Could not fetch weather data for {city}"
        return (
            f"City: {city}\n"
            f"Temperature: {data['current']['temperature']} °C\n"
            f"Weather: {data['current']['weather_descriptions'][0]}\n"
            f"Humidity: {data['current']['humidity']}%"
        )

    llm      = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.9, openai_api_key=OPENAI_API_KEY)
    prompt   = hub.pull("hwchase17/react")
    tools    = [search_tool, get_weather_data]
    agent    = create_react_agent(llm=llm, tools=tools, prompt=prompt)
    executor = AgentExecutor(agent=agent, tools=tools, verbose=False)
    return executor.invoke({"input": query})["output"]

if submit and user_query.strip():
    with st.spinner("Agent is thinking…"):
        try:
            st.session_state.response = run_agent(user_query.strip())
        except Exception as e:
            st.session_state.response = f"⚠️ Error: {str(e)}"
elif submit:
    st.markdown("""
    <div style="padding:12px 16px;background:rgba(234,88,12,0.1);
    border:1px solid rgba(234,88,12,0.3);border-radius:12px;
    color:#fb923c;font-size:14px;margin-top:0.75rem;">
      Please enter a question first.
    </div>""", unsafe_allow_html=True)

# ── ANSWER ────────────────────────────────────────────────────────────────────
if st.session_state.response:
    st.markdown(f"""
    <div style="height:1rem"></div>
    <div class="acard">
      <div class="ahead">
        <div class="aicon">🤖</div>
        <div class="atitle">Agent Response</div>
      </div>
      <div class="abody">{st.session_state.response}</div>
    </div>""", unsafe_allow_html=True)

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="text-align:center;margin-top:3rem;padding-top:1.5rem;
  border-top:1px solid {BORDER};">
  <span style="font-size:12px;color:{TEXT2};">
    Built with LangChain · OpenAI GPT-3.5 · WeatherStack · Tavily Search
  </span>
</div>""", unsafe_allow_html=True)