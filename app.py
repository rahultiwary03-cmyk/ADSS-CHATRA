import streamlit as st
import pandas as pd
import time

# 1. Page Config & Professional Theme
st.set_page_config(page_title="JMMSY | District Administration Chatra", layout="wide", page_icon="🏛️")

# Custom CSS for Government Branding and Animations
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Roboto', sans-serif;
        background-color: #f0f2f5;
    }

    /* Government Header */
    .gov-header {
        background: linear-gradient(135deg, #003366 0%, #004080 100%);
        color: white;
        padding: 40px;
        text-align: center;
        border-radius: 0 0 30px 30px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.15);
        margin-bottom: 40px;
    }

    /* Professional Stat Cards */
    .stat-card {
        background: white;
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border-top: 5px solid #ff9933; /* Saffron touch */
    }

    /* Stylish Result Card Animation */
    .result-container {
        background: white;
        padding: 30px;
        border-radius: 20px;
        border-left: 8px solid #28a745;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        animation: fadeIn 0.8s ease-in-out;
    }

    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(20px); }
        100% { opacity: 1; transform: translateY(0); }
    }

    .label { color: #666; font-size: 0.9rem; font-weight: bold; margin-bottom: 5px; }
    .value { color: #1a1a1a; font-size: 1.1rem; font-weight: bold; margin-bottom: 15px; }
    
    /* Search Button Style */
    .stButton>button {
        background: #003366;
        color: white;
        border-radius: 8px;
        padding: 10px 25px;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background: #ff9933;
        border-color: #ff9933;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Top Header Section
st.markdown("""
    <div class='gov-header'>
        <h1 style='margin:0; letter-spacing: 1px;'>झारखण्ड मुख्यमंत्री मईयां सम्मान योजना (JMMSY)</h1>
        <h3 style='margin:10px 0 0 0; opacity:0.8; font-weight:300;'>ज़िला प्रशासन, चतरा - आधिकारिक लाभार्थी पोर्टल</h3>
    </div>
    """, unsafe_allow_html=True)

# 3. Data Loading
sheet_id = "1fApqqsNEulpVsPH7O0IAMRvQv39DMYkV2PB_kg3qntg"
sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

@st.cache_data(ttl=300)
def load_data():
    try:
        df = pd.read_csv(sheet_url)
        df.columns = df.columns.str.strip()
        return df
    except:
        return None

df = load_data()

# 4. Dashboard Stats Row
c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown("<div class='stat-card'><small>कुल पंजीकृत</small><h2>1,89,174</h2></div>", unsafe_allow_html=True)
with c2: st.markdown("<div class='stat-card'><small>ज़िला</small><h2>चतरा</h2></div>", unsafe_allow_html=True)
with c3: st.markdown("<div class='stat-card'><small>विभाग</small><h2>WCD Jharkhand</h2></div>", unsafe_allow_html=True)
with c4: st.markdown("<div class='stat-card'><small>सर्वर स्थिति</small><h2 style='color:#28a745;'>ONLINE</h2></div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 5. Search Interface
with st.container():
    st.markdown("<h3 style='text-align: center; color: #003366;'>🔍 लाभार्थी स्थिति की जाँच करें</h3>", unsafe_allow_html=True)
    
    # UI Design for search box
    _, search_col, _ = st.columns([1, 2, 1])
    with search_col:
        aadhar_input = st.text_input("", placeholder="अपना 12 अंकों का आधार नंबर यहाँ लिखें...", label_visibility="collapsed")
        search_btn = st.button("स्टेटस चेक करें")

# 6. Result Processing Logic
if search_btn and aadhar_input:
    if df is not None:
        # Aadhaar Column detection and cleaning
        col_name = 'Aadhaar Number' if 'Aadhaar Number' in df.columns else 'Aadhar Number'
        
        # Creating a match key by removing all spaces from input and data
        clean_input = str(aadhar_input).replace(" ", "")
        df['match_key'] = df[col_name].astype(str).str.replace(" ", "").str.replace(".0", "", regex=False)
        
        result = df[df['match_key'] == clean_input].copy()
        
        if not result.empty:
            # Animation effect
            with st.spinner('डेटाबेस से जानकारी प्राप्त की जा रही है...'):
                time.sleep(1)
            
            row = result.iloc[0] # Get first match record
            
            # Masking logic
            def mask_val(v):
                v_str = str(v).replace('.0', '').strip()
                return f"XXXXXXX{v_str[-4
