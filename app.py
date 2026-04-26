import streamlit as st
import pandas as pd
from datetime import datetime, date
import time
import plotly.graph_objects as go
import plotly.express as px

# --- 1. PRO SYSTEM CONFIGURATION ---
st.set_page_config(
    page_title="Smart Study Planner | Vishwas Jha",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. ELITE CSS ENGINE ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;600;800&display=swap');

    .stApp {
        background: radial-gradient(circle at top left, #ffffff 0%, #f8fafc 100%);
        color: #1e293b;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    section[data-testid="stSidebar"] {
        width: 420px !important;
        background-color: #f8fafc !important;
        border-right: 1px solid #e2e8f0;
    }

    .hero-title {
        font-size: 6.5rem !important;
        font-weight: 800 !important;
        text-align: center;
        background: linear-gradient(to right, #2563eb, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -4px;
        margin-top: -60px;
    }

    h1 { font-size: 4.5rem !important; font-weight: 800 !important; }
    h2 { font-size: 3.5rem !important; font-weight: 700 !important; }
    p, label, li { font-size: 1.6rem !important; color: #475569; }
    
    [data-testid="stMetricValue"] { 
        font-size: 5.5rem !important; 
        font-weight: 800 !important; 
        color: #2563eb !important; 
    }

    .planner-box {
        background: white;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #e2e8f0;
        min-height: 400px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }

    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: white;
        color: #0f172a;
        text-align: center;
        padding: 15px;
        font-weight: 800;
        font-size: 1.5rem;
        border-top: 4px solid #2563eb;
        z-index: 1000;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSION STATE INITIALIZATION ---
if 'onboarded' not in st.session_state:
    st.session_state.onboarded = False
if 'planner_tasks' not in st.session_state:
    st.session_state.planner_tasks = {day: "" for day in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]}

# --- PHASE 1: ACADEMIC SETUP ---
if not st.session_state.onboarded:
    st.markdown("<h1 class='hero-title'>SMART STUDY</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 2.2rem; font-weight: 600;'>Design Thinking Semester Project</p>", unsafe_allow_html=True)
    
    with st.form("academic_setup"):
        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input("Full Name", placeholder="Vishwas Jha")
            course = st.selectbox("Course", ["B.Tech Data Science & AI", "Computer Science", "Engineering"])
        with c2:
            year = st.selectbox("Year", ["1st Year", "2nd Year", "3rd Year", "4th Year"])
            sem = st.selectbox("Semester", [f"{i} Semester" for i in range(1,9)])
        
        subs = st.multiselect("Select Subjects", ["Python", "Machine Learning", "AI Ethics", "Data Structures", "DBMS"])
        target = st.slider("Daily Study Goal (Hours)", 1, 15, 8)
        
        if st.form_submit_button("DEPLOY PLANNER 🚀"):
            if not name or not subs:
                st.error("⚠️ Please enter your name and select subjects.")
            else:
                st.session_state.user_data = {"name": name, "course": course, "year": year, "sem": sem, "subs": subs, "hours": target}
                st.session_state.onboarded = True
                st.rerun()

# --- PHASE 2: DASHBOARD & FEATURES ---
else:
    with st.sidebar:
        st.markdown(f"## {st.session_state.user_data['name']}")
        st.write(f"🎓 {st.session_state.user_data['course']}")
        st.write(f"📅 {st.session_state.user_data['year']} | {st.session_state.user_data['sem']}")
        st.markdown("---")
        menu = st.radio("CORE FEATURES", ["📊 Dashboard", "📅 Weekly Planner", "⏱️ Focus Timer", "🎯 Goal Tracker", "🧠 Mood Tracker"])
        if st.button("Reset Session"):
            st.session_state.onboarded = False
            st.rerun()

    # 1. DASHBOARD
    if menu == "📊 Dashboard":
        st.title("Performance Hub")
        m1, m2, m3 = st.columns(3)
        m1.metric("Goal", f"{st.session_state.user_data['hours']}h")
        m2.metric("Modules", len(st.session_state.user_data['subs']))
        m3.metric("Streak", "14 Days", "🔥")
        st.markdown("---")
        
        c_left, c_right = st.columns(2)
        with c_left:
            st.subheader("Mastery Analysis")
            cols = st.columns(len(st.session_state.user_data['subs']))
            for i, sub in enumerate(st.session_state.user_data['subs']):
                with cols[i]:
                    fig = go.Figure(go.Pie(values=[75, 25], hole=.8, marker_colors=['#2563eb', '#f1f5f9']))
                    fig.update_layout(showlegend=False, height=150, margin=dict(t=0,b=0,l=0,r=0), paper_bgcolor='rgba(0,0,0,0)')
                    st.plotly_chart(fig, use_container_width=True)
                    st.markdown(f"<p style='text-align: center; font-size: 0.9rem !important;'>{sub}</p>", unsafe_allow_html=True)
        with c_right:
            st.subheader("Time Allocation")
            df = pd.DataFrame({"Day": ["Mon", "Tue", "Wed", "Thu", "Fri"], "Hours": [4, 6, 5, 8, 7]})
            fig_bar = px.bar(df, x='Day', y='Hours', color='Hours', color_continuous_scale='Blues')
            st.plotly_chart(fig_bar, use_container_width=True)

    # 2. FIXED WEEKLY PLANNER (FUNCTIONAL)
    elif menu == "📅 Weekly Planner":
        st.title("Strategic Weekly Roadmap")
        st.write("Plan your subjects for the entire week. Your changes are saved automatically.")
        
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        cols = st.columns(7)
        
        for i, day in enumerate(days):
            with cols[i]:
                st.markdown(f"### {day}")
                # Using text_area for each day so user can actually type tasks
                st.session_state.planner_tasks[day] = st.text_area(
                    "Tasks:", 
                    value=st.session_state.planner_tasks[day], 
                    height=300, 
                    key=f"plan_{day}"
                )

    # 3. FOCUS TIMER (REVERSE CLOCK)
    elif menu == "⏱️ Focus Timer":
        st.title("Focus Engine")
        c1, c2 = st.columns(2)
        with c1: duration = st.number_input("Minutes", value=25)
        with c2: interval = st.selectbox("Motivation Gap", [5, 10, 15])
        
        placeholder = st.empty()
        if st.button("START REVERSE COUNTDOWN"):
            total_sec = duration * 60
            for sec in range(total_sec, -1, -1):
                mins, secs = divmod(sec, 60)
                placeholder.markdown(f"<h1 style='font-size: 200px !important; color: #2563eb; text-align: center;'>{mins:02d}:{secs:02d}</h1>", unsafe_allow_html=True)
                
                # Motivation pop-up logic
                elapsed_min = (total_sec - sec) // 60
                if elapsed_min > 0 and elapsed_min % interval == 0 and sec % 60 == 0:
                    st.toast("🚀 Keep going! You're making progress!", icon="🔥")
                
                time.sleep(1)
            st.balloons()

    # 4. GOAL TRACKER
    elif menu == "🎯 Goal Tracker":
        st.title("Hour-Target Matrix")
        for sub in st.session_state.user_data['subs']:
            st.slider(f"Weekly Hours for {sub}", 1, 50, 10)
            st.progress(0.6)

    # 5. MOOD TRACKER
    elif menu == "🧠 Mood Tracker":
        st.title("Neural State Log")
        mood = st.radio("Mood:", ["😫 Exhausted", "😰 Stressed", "😐 Neutral", "🤩 Motivated", "🔥 Peak Focus"], horizontal=True)
        if st.button("GET STRATEGY"):
            if "Exhausted" in mood: st.warning("AI Tip: Energy low. Try passive learning (videos).")
            elif "Peak" in mood: st.success("AI Tip: Prime focus! Start complex coding/projects.")

# --- FOOTER ---
st.markdown(f"""<div class="footer">Design and Thinking project by Vishwas Jha</div>""", unsafe_allow_html=True)