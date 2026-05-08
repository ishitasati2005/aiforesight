import streamlit as st
import requests
import google.generativeai as genai

#PAGE CONFIG
st.set_page_config(
    page_title="AgroPredict AI",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

#LOAD CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style.css")

#SESSION STATE
if "crop" not in st.session_state:
    st.session_state.crop = None

#GEMINI SETUP
GEMINI_API_KEY = "AIzaSyAQ68o_efsIqSJUW-muqjHYDTLS6e4BLsA"
genai.configure(api_key=GEMINI_API_KEY)
gemini = genai.GenerativeModel(model_name="gemini-3.1-flash-lite")

#HERO
st.markdown("""
<div class="hero-wrap">
    <div class="hero-badge">🌾 AI-Powered Crop Intelligence</div>
    <h1 class="hero-title">Agro<span>Predict</span></h1>
    <p class="hero-sub">
        Feed your soil data, harvest the right crop.<br>
        Precision agriculture powered by machine learning.
    </p>
</div>

<div class="vine-divider">⸻ 🌿 ⸻</div>

<div class="stat-row">
    <span class="stat-chip">🪱 Soil NPK Analysis</span>
    <span class="stat-chip">🌡 Climate-Aware</span>
    <span class="stat-chip">💧 Moisture Tracking</span>
    <span class="stat-chip">⚗️ pH Calibrated</span>
    <span class="stat-chip">🤖 Gemini AI Assistant</span>
</div>
""", unsafe_allow_html=True)

#MAIN LAYOUT
left, right = st.columns([1.4, 1], gap="large")

#LEFT: SOIL INPUTS
with left:

    st.markdown("""
    <div class="card">
      <div class="section-label">Step 01</div>
      <div class="section-title">🪱 Soil Composition</div>
      <div class="npk-grid">
        <div class="npk-block">
          <div class="npk-letter n">N</div>
          <div class="npk-name">Nitrogen</div>
        </div>
        <div class="npk-block">
          <div class="npk-letter p">P</div>
          <div class="npk-name">Phosphorus</div>
        </div>
        <div class="npk-block">
          <div class="npk-letter k">K</div>
          <div class="npk-name">Potassium</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        n = st.number_input("N – Nitrogen (kg/ha)", min_value=0.0, max_value=150.0, value=50.0)
    with c2:
        p = st.number_input("P – Phosphorus (kg/ha)", min_value=0.0, max_value=150.0, value=50.0)
    with c3:
        k = st.number_input("K – Potassium (kg/ha)", min_value=0.0, max_value=150.0, value=50.0)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
      <div class="section-label">Step 02</div>
      <div class="section-title">🌦 Environmental Conditions</div>
    </div>
    """, unsafe_allow_html=True)

    c4, c5 = st.columns(2)
    with c4:
        st.markdown('<div class="slider-label">🌡 Temperature (°C)</div>', unsafe_allow_html=True)
        temp = st.slider("Temperature", -10.0, 50.0, 25.0, label_visibility="collapsed")
        st.markdown('<div class="slider-label">⚗️ Soil pH Level</div>', unsafe_allow_html=True)
        ph = st.slider("pH", 0.0, 14.0, 6.5, label_visibility="collapsed")
    with c5:
        st.markdown('<div class="slider-label">💧 Humidity (%)</div>', unsafe_allow_html=True)
        humidity = st.slider("Humidity", 0.0, 100.0, 50.0, label_visibility="collapsed")
        st.markdown('<div class="slider-label">🌧 Rainfall (mm)</div>', unsafe_allow_html=True)
        rainfall = st.slider("Rainfall", 0.0, 500.0, 100.0, label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)

    # Live soil meters
    def bar_color(pct):
        if pct < 0.3:   return "#c0392b"
        elif pct < 0.6: return "#e67e22"
        else:            return "#3E6B3E"

    st.markdown(f"""
    <div class="soil-meter-wrap">
      <div class="meter-title">📊 Live Soil Health Overview</div>
      <div class="meter-row">
        <span class="meter-icon">🟢</span><span class="meter-label">Nitrogen</span>
        <div class="meter-bar-bg"><div class="meter-bar-fill" style="width:{n/150*100:.0f}%;background:{bar_color(n/150)};"></div></div>
        <span class="meter-val">{n:.0f}</span>
      </div>
      <div class="meter-row">
        <span class="meter-icon">🟤</span><span class="meter-label">Phosphorus</span>
        <div class="meter-bar-bg"><div class="meter-bar-fill" style="width:{p/150*100:.0f}%;background:{bar_color(p/150)};"></div></div>
        <span class="meter-val">{p:.0f}</span>
      </div>
      <div class="meter-row">
        <span class="meter-icon">🟡</span><span class="meter-label">Potassium</span>
        <div class="meter-bar-bg"><div class="meter-bar-fill" style="width:{k/150*100:.0f}%;background:{bar_color(k/150)};"></div></div>
        <span class="meter-val">{k:.0f}</span>
      </div>
      <div class="meter-row">
        <span class="meter-icon">⚗️</span><span class="meter-label">pH Level</span>
        <div class="meter-bar-bg"><div class="meter-bar-fill" style="width:{ph/14*100:.0f}%;background:#5a7a3a;"></div></div>
        <span class="meter-val">{ph:.1f}</span>
      </div>
      <div class="meter-row">
        <span class="meter-icon">💧</span><span class="meter-label">Humidity</span>
        <div class="meter-bar-bg"><div class="meter-bar-fill" style="width:{humidity:.0f}%;background:#2e86c1;"></div></div>
        <span class="meter-val">{humidity:.0f}%</span>
      </div>
      <div class="meter-row">
        <span class="meter-icon">🌧</span><span class="meter-label">Rainfall</span>
        <div class="meter-bar-bg"><div class="meter-bar-fill" style="width:{rainfall/500*100:.0f}%;background:#1a5276;"></div></div>
        <span class="meter-val">{rainfall:.0f}</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    predict_btn = st.button("🌾 Analyse & Recommend Crop")

#RIGHT: INFO PANEL
with right:

    st.markdown("""
    <div class="about-card">
      <div class="about-title">From soil to harvest —<br>smarter decisions, every season.</div>
      <div class="about-item"><span class="about-icon">🌱</span>
        <span>Analyzes <b>7 key soil &amp; climate factors</b> to match the ideal crop for your land.</span></div>
      <div class="about-item"><span class="about-icon">🧬</span>
        <span>Trained on thousands of real agricultural data points across diverse terrains.</span></div>
      <div class="about-item"><span class="about-icon">💡</span>
        <span>Reduces guesswork, improves yield, and promotes sustainable farming practices.</span></div>
      <div class="about-item"><span class="about-icon">🤖</span>
        <span>Ask our <b>Gemini AI Assistant</b> anything about your crop, fertilizer &amp; irrigation.</span></div>
    </div>
    """, unsafe_allow_html=True)

    st.image(
        "https://images.unsplash.com/photo-1500651230702-0e2d8a49d4ad?q=80&w=1200&auto=format&fit=crop",
        use_container_width=True,
        caption="Every field tells a story. We help you read it."
    )

    st.markdown("""
    <div class="almanac-box">
      <div class="almanac-title">🌾 Farmer's Almanac Tip</div>
      <div class="almanac-body">
        Soil pH between <b>6.0–7.0</b> suits most crops. Nitrogen boosts
        leaf growth; phosphorus strengthens roots; potassium improves
        drought &amp; disease resistance.<br><br>
        <i>"Healthy soil is the foundation of all agriculture."</i>
      </div>
    </div>
    """, unsafe_allow_html=True)

#PREDICTION API CALL
if predict_btn:
    payload = {"n": n, "p": p, "k": k, "temp": temp, "humidity": humidity, "ph": ph, "rainfall": rainfall}
    try:
        with st.spinner("🌱 Reading your soil profile and running the model..."):
            resp = requests.post("http://127.0.0.1:8000/predict", json=payload, timeout=10)
        if resp.status_code == 200:
            prediction = resp.json().get("prediction", resp.text)
            st.session_state.crop = prediction
            st.balloons()
            st.markdown(f"""
            <div class="result-wrap">
              <div class="result-card">
                <div class="result-eyebrow">✦ AI Recommendation ✦</div>
                <div class="result-crop">🌾 {prediction}</div>
                <div class="result-tip">
                  <b>💡 Why this crop?</b><br>
                  Based on your soil NPK ratio (N:{n:.0f} P:{p:.0f} K:{k:.0f}),
                  pH {ph:.1f}, {temp:.0f}°C temperature, {humidity:.0f}% humidity
                  and {rainfall:.0f}mm rainfall — <b>{prediction}</b> is the optimal
                  match for maximum yield on your land.
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error(f"⚠️ API returned status {resp.status_code}. Check your FastAPI server.")
    except requests.exceptions.ConnectionError:
        st.error("⚠️ Cannot reach FastAPI server at http://127.0.0.1:8000 — make sure it's running.")
    except requests.exceptions.Timeout:
        st.error("⏱ The server took too long to respond. Please try again.")

#CHATBOT
st.markdown("""
<div class="chat-section-header">
    <div class="chat-badge">🌿 Powered by Gemini AI</div>
    <div class="chat-heading">Ask the <span>Field Assistant</span></div>
    <div class="chat-subheading">Get expert advice on fertilizers, irrigation, diseases, and more.</div>
</div>
""", unsafe_allow_html=True)

#Suggestion pills
st.markdown("""
<div class="suggestion-row">
    <span class="suggestion-pill">💧 Best irrigation schedule?</span>
    <span class="suggestion-pill">🌿 Which fertilizer to use?</span>
    <span class="suggestion-pill">🐛 How to prevent pests?</span>
    <span class="suggestion-pill">🌱 When to sow?</span>
    <span class="suggestion-pill">☀️ Sun &amp; shade tips</span>
</div>
""", unsafe_allow_html=True)

#Crop context
if st.session_state.crop:
    st.markdown(f"""
    <div class="context-pill">
        <span class="context-dot"></span>
        Active crop context: <b>{st.session_state.crop}</b> — AI will tailor advice to this crop
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="no-crop-note">
        🌾 <span>Run the crop prediction above first for crop-specific AI advice — or ask a general farming question below.</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

#Input + Ask button
st.markdown('<div class="chat-input-wrap"><div class="chat-input-label">✍️ Your Question</div>', unsafe_allow_html=True)
user_question = st.text_input(
    "Ask about fertilizers, irrigation, diseases, etc.",
    placeholder="e.g. What fertilizer should I use for my crop? How often should I irrigate?",
    label_visibility="collapsed"
)
ask_btn = st.button("🌿 Ask Field Assistant")
st.markdown('</div>', unsafe_allow_html=True)

if ask_btn:
    if user_question.strip():
        context = (
            f"The farmer's ML model has recommended growing '{st.session_state.crop}' "
            f"based on their soil data (N:{n:.0f}, P:{p:.0f}, K:{k:.0f}, pH:{ph:.1f}, "
            f"Temp:{temp:.0f}°C, Humidity:{humidity:.0f}%, Rainfall:{rainfall:.0f}mm). "
            if st.session_state.crop else
            "The farmer has not yet run a crop prediction. "
        )
        full_prompt = (
            f"{context}"
            f"Question: {user_question}. "
            f"You are an expert agricultural advisor. Give practical, concise, farmer-friendly advice. "
            f"Use simple language. Structure your answer clearly with key points."
        )
        try:
            with st.spinner("🌿 Consulting the field assistant..."):
                ai_resp = gemini.generate_content(full_prompt)
                answer  = ai_resp.text

            crop_label = f"for {st.session_state.crop}" if st.session_state.crop else "General farming"

            st.markdown(f"""
            <div class="ai-response-card">
              <div class="ai-response-header">
                <div class="ai-avatar">🌿</div>
                <div>
                  <div class="ai-name">Field Assistant</div>
                  <div class="ai-role">Gemini AI · {crop_label}</div>
                </div>
              </div>
              <div class="ai-body">{answer.replace(chr(10), '<br>')}</div>
              <div class="ai-footer-note">⚡ Powered by Google Gemini · Always verify with a local agronomist</div>
            </div>
            """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"🌾 Gemini error: {e}")
    else:
        st.warning("🌱 Please type a question before asking the assistant.")

#  FOOTER 
st.markdown("""
<div class="footer">
    <div class="footer-brand">🌿 AgroPredict AI</div>
    Built with care for farmers, fields &amp; the future of sustainable agriculture.<br>
    Powered by Machine Learning &amp; Google Gemini · Grounded in Nature
</div>
""", unsafe_allow_html=True)