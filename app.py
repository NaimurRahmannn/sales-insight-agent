import streamlit as st
import sys
import os
import json

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from agent.agent import ask

HISTORY_FILE = "chat_history.json"

def load_chat_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_chat_history(messages):
    with open(HISTORY_FILE, "w") as f:
        json.dump(messages, f)

st.set_page_config(
    page_title="Sales Intelligence Agent", 
    page_icon="📈", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium UI Injection
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
    }

    /* Hide default Streamlit noise */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 5rem !important;
        max-width: 1000px !important;
    }

    /* Header styling */
    .hero-container {
        padding: 1.5rem 0 2.5rem 0;
        text-align: center;
        border-bottom: 1px solid #E2E8F0;
        margin-bottom: 2.5rem;
    }
    .hero-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #0F172A;
        margin-bottom: 0.5rem;
    }
    .hero-title span {
        background: linear-gradient(135deg, #2E5BFF 0%, #00C6FF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero-subtitle {
        color: #64748B;
        font-size: 1.1rem;
    }

    /* Chat Messages */
    .stChatMessage {
        border-radius: 12px;
        padding: 1.5rem !important;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.02);
        margin-bottom: 1rem;
        border: 1px solid #F1F5F9;
    }
    
    .stChatMessage[data-testid="stChatMessage"]:nth-child(odd) {
        background-color: #FFFFFF;
    }
    
    .stChatMessage[data-testid="stChatMessage"]:nth-child(even) {
        background-color: #F8FAFC; 
    }

    /* Sidebar Enhancements */
    [data-testid="stSidebar"] {
        background-color: #F8FAFC !important;
        border-right: 1px solid #E2E8F0;
    }
    
    .sidebar-section {
        background: #FFFFFF;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        border: 1px solid #E2E8F0;
        margin-bottom: 1.5rem;
    }
    
    .sidebar-title {
        color: #0F172A;
        font-size: 0.95rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .status-item {
        display: flex;
        align-items: center;
        justify-content: space-between;
        font-size: 0.9rem;
        color: #475569;
        margin-bottom: 0.7rem;
    }
    
    .status-dot {
        height: 8px;
        width: 8px;
        background-color: #10B981;
        border-radius: 50%;
        display: inline-block;
        margin-right: 6px;
    }

    .metric-value {
        font-weight: 600;
        color: #0F172A;
    }

    /* Welcome Cards */
    .welcome-card-container {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1.5rem;
        margin-bottom: 2rem;
    }
    
    .welcome-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .welcome-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 15px rgba(46, 91, 255, 0.08);
        border-color: #2E5BFF;
    }
    
    .welcome-card h3 {
        color: #0F172A;
        font-size: 1.1rem;
        font-weight: 600;
        margin-top: 0;
        margin-bottom: 0.75rem;
    }
    
    .welcome-card p {
        color: #64748B;
        font-size: 0.9rem;
        line-height: 1.5;
        margin: 0;
    }
</style>
""", unsafe_allow_html=True)

# Main Dashboard Header
st.markdown("""
<div class="hero-container">
    <div class="hero-title">Sales Intelligence <span>Platform</span></div>
    <div class="hero-subtitle">Ask questions, generate forecasts, and get business insights instantly.</div>
</div>
""", unsafe_allow_html=True)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = load_chat_history()

# --- Premium Sidebar ---
with st.sidebar:
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Section 1: System Status
    st.markdown("""
    <div class="sidebar-section">
        <div class="sidebar-title">⚡ System Status</div>
        <div class="status-item">
            <span>PostgreSQL DB</span>
            <span><span class="status-dot"></span> <span class="metric-value">Connected</span></span>
        </div>
        <div class="status-item">
            <span>Gemini Flash 3.1</span>
            <span><span class="status-dot"></span> <span class="metric-value">Online</span></span>
        </div>
        <div class="status-item">
            <span>XGBoost Model</span>
            <span><span class="status-dot"></span> <span class="metric-value">Loaded</span></span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Section 2: Data Profile
    st.markdown("""
    <div class="sidebar-section">
        <div class="sidebar-title">📊 Dataset Profile</div>
        <div class="status-item"><span>Total Records</span> <span class="metric-value">9,994</span></div>
        <div class="status-item"><span>Total Customers</span> <span class="metric-value">793</span></div>
        <div class="status-item"><span>Categories</span> <span class="metric-value">3</span></div>
        <div class="status-item"><span>Regions</span> <span class="metric-value">4</span></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Section 3: Example Prompts
    st.markdown("""
    <div class="sidebar-section" style="margin-bottom: 0.5rem;">
        <div class="sidebar-title">💡 Try Asking</div>
        <p style="font-size:0.85rem; color:#64748B;">Click a question below to ask the AI.</p>
    </div>
    """, unsafe_allow_html=True)
    
    example_questions = [
        "What are total sales?",
        "Which region has highest profit?",
        "Why is Furniture underperforming?",
        "What are next 3 months forecast?"
    ]
    
    for i, q in enumerate(example_questions):
        if st.button(q, use_container_width=True, type="primary", key=f"btn_{i}"):
            st.session_state.example_prompt = q
            
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        save_chat_history([])
        st.rerun()
    
# --- Welcome State ---
if not st.session_state.messages:
    st.markdown("<h3 style='text-align: center; color: #1E293B; margin-bottom: 2rem;'>👋 Welcome! Here are some example questions to get you started:</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📊 What are our total sales and profit margins?", use_container_width=True):
            st.session_state.example_prompt = "What are our total sales and profit margins?"
            st.rerun()
            
        if st.button("🌍 Which region has the highest profit?", use_container_width=True):
            st.session_state.example_prompt = "Which region has the highest profit?"
            st.rerun()

    with col2:
        if st.button("⚠️ Why is the Furniture category underperforming?", use_container_width=True):
            st.session_state.example_prompt = "Why is the Furniture category underperforming?"
            st.rerun()
            
        if st.button("📈 What is the sales forecast for the next 3 months?", use_container_width=True):
            st.session_state.example_prompt = "What is the sales forecast for the next 3 months?"
            st.rerun()
    
    st.markdown("<br><br>", unsafe_allow_html=True)

# --- Chat Interface ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
prompt = st.chat_input("Ask about revenue, categories, trends, or forecasts...")

# Check if an example button was clicked
if "example_prompt" in st.session_state and st.session_state.example_prompt:
    prompt = st.session_state.example_prompt
    st.session_state.example_prompt = None

if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    save_chat_history(st.session_state.messages)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing data..."):
            try:
                response = ask(prompt, history=st.session_state.messages[:-1])
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
                save_chat_history(st.session_state.messages)
            except Exception as e:
                error_msg = f"Sorry, I encountered an error while analyzing the data. Please try again. ({str(e)})"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
                save_chat_history(st.session_state.messages)
