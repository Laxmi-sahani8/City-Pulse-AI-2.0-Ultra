import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime
from fpdf import FPDF
import json
import os
import datetime


# --- 1. PAGE SETUP & STYLING ---
st.set_page_config(page_title="City-Pulse AI 2.0 Ultra", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }
    .high-alert { padding: 10px; background-color: #ff4b4b; color: white; border-radius: 10px; text-align: center; font-weight: bold; animation: blinker 1.5s linear infinite; }
    @keyframes blinker { 50% { opacity: 0; } }
    </style>
    """, unsafe_allow_html=True)

# --- 2. AUTHENTICATION SYSTEM ---

USER_DB = "users.json"
def load_users():
    if os.path.exists(USER_DB):
        with open(USER_DB, "r") as f: return json.load(f)
    return {"admin": "password123"}

def save_user(u, p):
    users = load_users()
    if u in users: return False
    users[u] = p
    with open(USER_DB, "w") as f: json.dump(users, f)
    return True

if "logged_in" not in st.session_state: st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    st.title("🔐 Secure Access Portal")
    t1, t2 = st.tabs(["Login", "Register"])
    with t1:
        with st.form("l"):
            u = st.text_input("Username"); p = st.text_input("Password", type="password")
            if st.form_submit_button("Login"):
                db = load_users()
                if u in db and db[u] == p:
                    st.session_state["logged_in"] = True; st.session_state["user"] = u; st.rerun()
                else: st.error("Wrong details!")
    with t2:
        with st.form("r"):
            nu = st.text_input("New Username"); np_ = st.text_input("New Password", type="password")
            if st.form_submit_button("Create"):
                if save_user(nu, np_): st.success("Created! Now Login.")
                else: st.error("User exists.")
    st.stop()

# --- 3. DASHBOARD ENGINE ---
@st.cache_data
def get_data():
    df = pd.read_csv('data.csv', encoding='unicode_escape')
    loc_col = df.columns[1] 
    val_col = 'Total - Total_18 years & Above'
    df_clean = df[~df[loc_col].str.contains('Total|All India', case=False, na=False)].copy()
    df_clean['Safety_Score'] = 100 - (df_clean[val_col] / df_clean[val_col].max() * 100)
    return df_clean, loc_col, val_col

df_final, loc_col, val_col = get_data()

# --- SIDEBAR & TOP HEADER (MODERN LOOK + TITLE FIX) ---
with st.sidebar:
    # 1. Admin Profile Section
    st.markdown(f"""
        <div style='text-align: center; padding: 10px; background-color: #ffffff; border-radius: 15px; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
            <img src='https://cdn-icons-png.flaticon.com/512/3135/3135715.png' width='70' style='border-radius: 50%;'>
            <h3 style='margin: 10px 0 0 0; color: #1f1f1f;'>{st.session_state['user']}</h3>
            <p style='color: #28a745; font-size: 13px; font-weight: bold;'>🟢 System Admin</p>
        </div>
    """, unsafe_allow_html=True)

    # 2. Modern Navigation
    st.markdown("### 🛠️ Navigation")
    menu = st.radio(
        label="Select Module:",
        options=["Predictive Dashboard", "Battle Mode", "AI Assistant"],
        label_visibility="collapsed"
    )

    st.markdown("---")

    # 3. System Health (Extra feature for Ultra look)
    st.markdown("### 🛰️ Engine Status")
    st.info("AI Model: Llama-3.1-8b-instant")
    st.progress(98)
    st.caption("Neural Engine Efficiency: 98%")

    st.markdown("---")

    # 4. Logout Button
    if st.button("🚪 Logout Account", use_container_width=True):
        st.session_state["logged_in"] = False
        st.rerun()

# --- MAIN HEADER (ONE LINE TITLE FIX) ---
# Yahan st.title ko hata kar hum custom HTML use kar rahe hain
st.markdown("""
    <div style='
        display: flex;
        align-items: center;
        width: 100%;
        font-family: sans-serif;
    '>
        <span style='font-size: 3rem; margin-right: 15px;'>🛡️</span>
        <h1 style='
            margin: 0;
            white-space: nowrap; /* Forces text to ONE line */
            font-size: 2.8rem;   /* Adjusted size to fit wide screens */
            font-weight: 700;
            width: 100%;
        '>
          City-Pulse AI 2.0: Predictive Safety Analytics
        </h1>
    </div>
""", unsafe_allow_html=True)

# --- FEATURE 1: PREDICTIVE DASHBOARD ---
if menu == "Predictive Dashboard":
    # This line forces the app to refresh every 1 second
    st_autorefresh(interval=1000, key="clock_refresh") 

    # Calculate live Indian Standard Time (IST)
    now = datetime.datetime.now() + datetime.timedelta(hours=5, minutes=30)
    current_time = now.strftime("%H:%M:%S")
    current_date = now.strftime("%Y-%m-%d")

    # Display the modern Live Status Header
    st.markdown(f"""
        <div style="background-color: #f0f2f6; padding: 15px; border-radius: 10px; border-left: 5px solid #007bff; margin-bottom: 20px;">
            <span style="font-size: 18px; font-weight: bold;">🛰️ Live Engine Status: </span>
            <span style="color: green; font-weight: bold;">Online</span> | 
            <span style="font-size: 18px; font-weight: bold;">🕒 Time: </span> {current_time} | 
            <span style="font-size: 18px; font-weight: bold;">📅 Date: </span> {current_date}
        </div>
    """, unsafe_allow_html=True)
    state_list = ["All India"] + sorted(list(df_final[loc_col].unique()))
    target = st.selectbox("🎯Target Location Selection:", state_list)
    
    df_sel = df_final if target == "All India" else df_final[df_final[loc_col] == target]
    
    max_val = df_sel[val_col].max()
    if max_val > 5000:
        st.markdown(f"<div class='high-alert'>🚨 HIGH ALERT: Unusual activity detected in {target}! Immediate monitoring required.</div>", unsafe_allow_html=True)
        st.write("")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Total Historical Cases (Past)", f"{int(df_sel[val_col].sum()):,}")
    with c2:
        
        day_of_year = datetime.datetime.now().timetuple().tm_yday
        present_est = int((df_sel[val_col].mean() / 365) * day_of_year)
        st.metric("Estimated Cases 2026 (Present)", f"{present_est:,}", delta="Live Tracking")
    with c3:
        future_proj = int(df_sel[val_col].mean() * 1.05)
        st.metric("AI Projection 2027 (Future)", f"{future_proj:,}", delta="Predicted Trend")
    with c4:
        st.metric("Safety Index Score", f"{round(df_sel['Safety_Score'].mean(), 1)}/100")

    st.divider()
    col_left, col_right = st.columns(2)
    with col_left:
        st.subheader("Regional Risk Distribution")
        st.plotly_chart(px.bar(df_sel.head(10), x=loc_col, y=val_col, color='Safety_Score', color_continuous_scale='RdYlGn'), use_container_width=True)
    with col_right:
        st.subheader("National Heatmap")
        
        fig_map = px.choropleth(df_final, geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d1a7df9754632c31478/raw/229a4a79649175373801f440536c4983a4216893/india_states.geojson",
                                featureidkey='properties.ST_NM', locations=loc_col, color='Safety_Score', color_continuous_scale="RdYlGn")
        fig_map.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig_map, use_container_width=True)
# 4. PDF REPORT GENERATOR
    st.markdown("### 📥 Official Documentation")
    if st.button("Generate Professional Safety Report (PDF)"):
        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(200, 10, txt="City-Pulse AI 2.0: Official Analytics Report", ln=True, align='C')
            pdf.ln(10)
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt=f"Location Analyzed: {target}", ln=True)
            pdf.cell(200, 10, txt=f"Safety Score: {round(safety_val, 1)}/100", ln=True)
            pdf.cell(200, 10, txt=f"Date: {datetime.now().strftime('%Y-%m-%d')}", ln=True)
            pdf.ln(10)
            pdf.multi_cell(0, 10, txt="This report is generated by City-Pulse AI 2.0 using predictive analytics. The data indicates the need for focused monitoring in the identified regions to ensure public safety.")
            
            report_name = "safety_analytics.pdf"
            pdf.output(report_name)
            
            with open(report_name, "rb") as f:
                st.download_button(label="Click to Download PDF", data=f, file_name=f"{target}_Report.pdf", mime="application/pdf")
        except Exception as e:
            st.error(f"PDF Error: {e}")
# --- FEATURE 2: BATTLE MODE ---
elif menu == "Battle Mode":
    st.title("⚔️ Comparative Analysis")
    b1, b2 = st.columns(2)
    s1 = b1.selectbox("State A", df_final[loc_col].unique(), key="a")
    s2 = b2.selectbox("State B", df_final[loc_col].unique(), key="b")
    st.plotly_chart(px.bar(df_final[df_final[loc_col].isin([s1, s2])], x=loc_col, y=val_col, color=loc_col, barmode='group'), use_container_width=True)
# --- FEATURE 3: SMART AI ASSISTANT (JUHI) ---
elif menu == "AI Assistant":
    from groq import Groq
    from gtts import gTTS
    import base64
    import os

    st.title("🤖 AI Smart Assistant (JUHI)")
    st.info("Juhi is now even smarter! She remembers your entire conversation context.")

    # 1. INITIALIZE MEMORY (Using Streamlit Session State)
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Initialize the Groq Client
    # Best practice: client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])

    def juhi_speaks(text):
        """Converts AI text response to speech."""
        try:
            # Limit voice output length for faster processing
            short_text = text[:200] + "..." if len(text) > 200 else text
            tts = gTTS(text=short_text, lang='en')
            tts.save("voice_temp.mp3")
            with open("voice_temp.mp3", "rb") as f:
                data = f.read()
                b64 = base64.b64encode(data).decode()
                st.markdown(f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)
        except Exception as e:
            pass

    # 2. DISPLAY CONVERSATION HISTORY
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 3. CHAT INPUT LOGIC
    if q := st.chat_input("Ask JUHI about city safety or analytics..."):
        # Save and display user message
        st.session_state.messages.append({"role": "user", "content": q})
        with st.chat_message("user"):
            st.markdown(q)

        # Generate and display Assistant Response
        with st.chat_message("assistant"):
            try:
                # Setting up the AI Persona (System Prompt)
                system_prompt = {
                    "role": "system", 
                    "content": f"You are JUHI, an elite safety AI for City-Pulse 2.0. You analyze urban safety data professionally. Remember context from this conversation. The current user is {st.session_state.get('user', 'Guest')}."
                }
                
                # Combine System Prompt + Full History to provide "Memory"
                messages_to_send = [system_prompt] + st.session_state.messages

                # Call the AI Model
                chat_completion = client.chat.completions.create(
                    messages=messages_to_send,
                    model="llama-3.1-8b-instant",
                )
                
                response = chat_completion.choices[0].message.content
                st.markdown(response)
                
                # Play audio and save assistant message to history
                juhi_speaks(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
                
            except Exception as e:
                st.error("The AI engine is currently busy. Please try again in a moment.")

    # 4. MEMORY MANAGEMENT
    st.divider()
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()
