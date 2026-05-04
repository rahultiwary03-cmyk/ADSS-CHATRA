import streamlit as st
import pandas as pd
import time

# 1. Page Config
st.set_page_config(page_title="JMMSY | Official Status Portal", layout="wide", page_icon="🏛️")

# 2. Stylish Government Dashboard CSS
st.markdown("""
    <style>
    .stApp { background: #f4f7f6; }
    
    /* Elegant Banner */
    .gov-banner {
        background: linear-gradient(135deg, #002e5d 0%, #00509d 100%);
        color: white; padding: 35px; text-align: center;
        border-radius: 0 0 30px 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        margin-bottom: 30px; border-bottom: 6px solid #ff9933;
    }

    /* Result Card */
    .status-container {
        background: white; padding: 35px; border-radius: 25px;
        box-shadow: 0 15px 50px rgba(0,0,0,0.1); margin-top: 20px;
        border-left: 10px solid #002e5d; animation: slideIn 0.6s ease-out;
    }

    @keyframes slideIn {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .info-label { color: #555; font-size: 0.85rem; font-weight: 800; text-transform: uppercase; margin-bottom: 4px; }
    .info-value { color: #111; font-size: 1.15rem; font-weight: 700; margin-bottom: 18px; border-bottom: 1px solid #eee; padding-bottom: 6px; }
    
    /* Search Button */
    .stButton>button {
        background: #002e5d !important; color: white !important;
        width: 100%; border-radius: 12px !important; height: 50px; font-weight: bold; font-size: 1.1rem;
    }
    .stButton>button:hover { background: #ff9933 !important; border-color: #ff9933 !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. Banner
st.markdown("""
    <div class='gov-banner'>
        <h1 style='margin:0;'>झारखण्ड मुख्यमंत्री मईयां सम्मान योजना (JMMSY)</h1>
        <p style='font-size: 1.2rem; opacity: 0.9;'>ज़िला प्रशासन, चतरा - आधिकारिक लाभार्थी डेटा पोर्टल</p>
    </div>
    """, unsafe_allow_html=True)

# 4. Data Loading
sheet_id = "1fApqqsNEulpVsPH7O0IAMRvQv39DMYkV2PB_kg3qntg"
sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

@st.cache_data(ttl=60)
def fetch_portal_data():
    try:
        df = pd.read_csv(sheet_url)
        df.columns = df.columns.str.strip() # Headers saaf karne ke liye
        return df
    except: return None

df = fetch_portal_data()

# 5. Dashboard Stats
col_a, col_b, col_c = st.columns(3)
with col_a: st.markdown("<div style='background:white; padding:15px; border-radius:10px; text-align:center; border-top:4px solid #ff9933;'><b>ज़िला</b><br>चतरा</div>", unsafe_allow_html=True)
with col_b: st.markdown("<div style='background:white; padding:15px; border-radius:10px; text-align:center; border-top:4px solid #002e5d;'><b>कुल लाभार्थी</b><br>1,89,174</div>", unsafe_allow_html=True)
with col_c: st.markdown("<div style='background:white; padding:15px; border-radius:10px; text-align:center; border-top:4px solid #28a745;'><b>स्थिति</b><br>LIVE</div>", unsafe_allow_html=True)

st.write("")

# 6. Search Interface
_, center_search, _ = st.columns([1, 2, 1])
with center_search:
    st.markdown("<h4 style='text-align: center; color: #002e5d;'>🔍 आधार नंबर से स्टेटस चेक करें</h4>", unsafe_allow_html=True)
    aadhar_val = st.text_input("", placeholder="12 अंकों का आधार नंबर यहाँ लिखें...", label_visibility="collapsed")
    search_triggered = st.button("स्टेटस चेक करें")

# 7. Core Search & Result Processing
if (search_triggered or aadhar_val) and aadhar_val:
    if df is not None:
        # User input cleanup
        clean_uid = str(aadhar_val).replace(" ", "")
        
        # Aadhaar Column identify karein
        uid_col = 'Aadhaar Number' if 'Aadhaar Number' in df.columns else 'Aadhar Number'
        
        # Match logic (Space aur .0 ko handle karte huye)
        df['key'] = df[uid_col].astype(str).str.replace(" ", "").str.replace(".0", "", regex=False)
        
        match = df[df['key'] == clean_uid].copy()
        
        if not match.empty:
            with st.spinner('डेटा मिलान किया जा रहा है...'):
                time.sleep(0.5)
            
            res = match.iloc[0]
            
            # Masking Bank A/c
            acc_raw = str(res.get('Account Number', 'N/A')).replace('.0', '').strip()
            masked_acc = f"XXXXXX{acc_raw[-4:]}" if len(acc_raw) > 4 else acc_raw

            # RESULT DISPLAY
            st.markdown("<div class='status-container'>", unsafe_allow_html=True)
            st.markdown("<h2 style='text-align:center; color:#002e5d; margin-bottom:30px;'>✅ सत्यापित लाभार्थी विवरण</h2>", unsafe_allow_html=True)
            
            res_1, res_2, res_3 = st.columns(3)
            
            with res_1:
                st.markdown(f"<div class='info-label'>लाभार्थी का नाम</div><div class='info-value'>{res.get('ApplicantName', res.get('Applicant', 'N/A'))}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='info-label'>पिता/पति का नाम</div><div class='info-value'>{res.get('Father\'s/Husband Name', 'N/A')}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='info-label'>ज़िला</div><div class='info-value'>{res.get('District', 'CHATRA')}</div>", unsafe_allow_html=True)

            with res_2:
                st.markdown(f"<div class='info-label'>पंचायत / गांव</div><div class='info-value'>{res.get('Panchayat', 'N/A')} / {res.get('Village', 'N/A')}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='info-label'>बैंक का नाम</div><div class='info-value'>{res.get('BankName', 'N/A
