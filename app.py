import streamlit as st
import pandas as pd
import time

# 1. Page Configuration
st.set_page_config(page_title="JMMSY | Official District Portal", layout="wide", page_icon="🏛️")

# 2. Premium Professional CSS (Government Official Theme)
st.markdown("""
    <style>
    /* Background and Font */
    .stApp {
        background-color: #f0f4f7;
    }
    
    /* Elegant Header Banner */
    .header-banner {
        background: linear-gradient(135deg, #002e5d 0%, #00509d 100%);
        color: #ffffff;
        padding: 45px;
        text-align: center;
        border-radius: 0 0 35px 35px;
        box-shadow: 0 12px 25px rgba(0,0,0,0.15);
        margin-bottom: 35px;
        border-bottom: 6px solid #ff9933;
    }

    /* Professional Card for Result */
    .result-card {
        background: white;
        padding: 40px;
        border-radius: 25px;
        box-shadow: 0 15px 40px rgba(0,0,0,0.08);
        border: 1px solid #dee2e6;
        animation: slideInUp 0.8s ease-in-out;
        margin-top: 20px;
    }

    @keyframes slideInUp {
        from { opacity: 0; transform: translateY(40px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Detail Boxes */
    .info-box {
        background: #fdfdfd;
        padding: 12px 15px;
        border-radius: 10px;
        border-left: 4px solid #002e5d;
        margin-bottom: 15px;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.02);
    }
    .info-label { color: #666; font-size: 0.8rem; font-weight: 700; text-transform: uppercase; margin-bottom: 4px; }
    .info-value { color: #111; font-size: 1.1rem; font-weight: 700; }
    
    /* Search Button Style */
    .stButton>button {
        background: linear-gradient(90deg, #002e5d 0%, #00509d 100%) !important;
        color: white !important;
        border-radius: 12px !important;
        height: 55px !important;
        width: 100%;
        font-weight: bold !important;
        font-size: 1.1rem !important;
        transition: 0.3s !important;
        border: none !important;
    }
    .stButton>button:hover {
        background: #ff9933 !important;
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Official Banner
st.markdown("""
    <div class='header-banner'>
        <h1 style='margin:0; font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;'>झारखण्ड मुख्यमंत्री मईयां सम्मान योजना (JMMSY)</h1>
        <p style='font-size: 1.3rem; opacity: 0.9; margin-top: 10px;'>ज़िला प्रशासन, चतरा - डिजिटल भुगतान एवं PDS सत्यापन पोर्टल</p>
    </div>
    """, unsafe_allow_html=True)

# 4. Data Loading Logic
SHEET_ID = "1fApqqsNEulpVsPH7O0IAMRvQv39DMYkV2PB_kg3qntg"
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

@st.cache_data(ttl=60)
def load_data():
    try:
        df = pd.read_csv(URL)
        df.columns = df.columns.str.strip() # Headers saaf karne ke liye
        return df
    except Exception as e:
        return None

df = load_data()

# 5. Quick Stats
c1, c2, c3 = st.columns(3)
with c1: st.markdown("<div style='background:white; padding:15px; border-radius:12px; text-align:center; border-top:4px solid #ff9933;'><b>ज़िला</b><br>चतरा</div>", unsafe_allow_html=True)
with c2: st.markdown("<div style='background:white; padding:15px; border-radius:12px; text-align:center; border-top:4px solid #002e5d;'><b>कुल लाभार्थी</b><br>1,89,174</div>", unsafe_allow_html=True)
with c3: st.markdown("<div style='background:white; padding:15px; border-radius:12px; text-align:center; border-top:4px solid #28a745;'><b>स्थिति</b><br>सक्रिय (LIVE)</div>", unsafe_allow_html=True)

st.write("")

# 6. Search Interface
_, search_col, _ = st.columns([1, 2, 1])
with search_col:
    st.markdown("<h4 style='text-align: center; color: #002e5d;'>🔍 लाभार्थी स्थिति की जाँच करें</h4>", unsafe_allow_html=True)
    aadhar_input = st.text_input("Aadhar Number", placeholder="अपना 12 अंकों का आधार नंबर यहाँ लिखें...", label_visibility="collapsed")
    submit_btn = st.button("स्टेटस चेक करें")

# 7. Core Search & Result Processing
if (submit_btn or aadhar_input) and aadhar_input:
    if df is not None:
        # Aadhaar Input cleanup
        clean_uid = str(aadhar_input).replace(" ", "")
        
        # Exact Column Identification from your Spreadsheet
        id_header = 'Aadhaar Number' if 'Aadhaar Number' in df.columns else 'Aadhar Number'
        
        # Matching Logic (Space and Decimal handle karte huye)
        df['match_key'] = df[id_header].astype(str).str.replace(" ", "").str.replace(".0", "", regex=False)
        
        match = df[df['match_key'] == clean_uid].copy()
        
        if not match.empty:
            with st.spinner('डेटाबेस से जानकारी मिलान की जा रही है...'):
                time.sleep(0.6)
            
            res = match.iloc[0]
            
            # Masking Bank Account
            raw_acc = str(res.get('Account Number', 'N/A')).replace('.0', '').strip()
            masked_acc = f"XXXXXX{raw_acc[-4:]}" if len(raw_acc) > 4 else raw_acc

            # --- Professional Result Display ---
            st.markdown("<div class='result-card'>", unsafe_allow_html=True)
            st.markdown(f"<h2 style='text-align:center; color:#002e5d; margin-bottom:35px;'>✅ लाभार्थी विवरण सफलतापूर्वक मिला</h2>", unsafe_allow_html=True)
            
            r1, r2, r3 = st.columns(3)
            
            with r1:
                st.markdown(f"<div class='info-box'><div class='info-label'>लाभार्थी का नाम</div><div class='info-value'>{res.get('Applicant', res.get('ApplicantName', 'N/A'))}</div></div>", unsafe_allow_html=True)
                st.markdown(f"<div class='info-box'><div class='info-label'>ज़िला</div><div class='info-value'>{res.get('District', 'CHATRA')}</div></div>", unsafe_allow_html=True)
                st.markdown(f"<div class='info-box'><div class='info-label'>प्रखंड (Block)</div><div class='info-value'>{res.get('Block', 'N/A')}</div></div>", unsafe_allow_html=True)

            with r2:
                st.markdown(f"<div class='info-box'><div class='info-label'>पिता/पति का नाम</div><div class='info-value'>{res.get(\"Father's/Husband Name\", 'N/A')}</div></div>", unsafe_allow_html=True)
                st.markdown(f"<div class='info-box'><div class='info-label'>पंचायत / गांव</div><div class='info-value'>{res.get('Panchayat', 'N/A')} / {res.get('Village', 'N/A')}</div></div>", unsafe_allow_html=True)
                st.markdown(f"<div class='info-box'><div class='info-label'>बैंक का नाम</div><div class='info-value'>{res.get('BankName', 'N/A')}</div></div>", unsafe_allow_html=True)

            with
