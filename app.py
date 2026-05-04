import streamlit as st
import pandas as pd
import time

# 1. Page Configuration
st.set_page_config(page_title="JMMSY | Chatra Verification Portal", layout="wide", page_icon="🏛️")

# 2. Premium Official Theme CSS
st.markdown("""
    <style>
    .stApp { background-color: #f8fafc; }
    .main-banner {
        background: linear-gradient(135deg, #002e5d 0%, #00509d 100%);
        color: white; padding: 3rem; text-align: center;
        border-radius: 0 0 40px 40px; box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        margin-bottom: 2rem; border-bottom: 6px solid #ff9933;
    }
    .stat-card {
        background: white; padding: 20px; border-radius: 15px;
        text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border-top: 5px solid #ff9933;
    }
    .result-container {
        background: white; padding: 40px; border-radius: 25px;
        box-shadow: 0 20px 50px rgba(0,0,0,0.1); margin-top: 20px;
        border: 1px solid #e2e8f0; animation: fadeInUp 0.7s ease-out;
    }
    .section-header {
        color: #002e5d; border-bottom: 2px solid #ff9933;
        padding-bottom: 8px; margin: 25px 0 15px 0; font-weight: 800;
        text-transform: uppercase; font-size: 0.9rem;
    }
    .info-tile {
        background: #f1f5f9; padding: 12px 15px; border-radius: 10px;
        margin-bottom: 10px; border-left: 4px solid #002e5d;
    }
    .info-label { color: #64748b; font-size: 0.7rem; font-weight: 700; text-transform: uppercase; }
    .info-value { color: #1e293b; font-size: 1rem; font-weight: 700; }
    
    .stButton>button {
        background: #002e5d !important; color: white !important;
        width: 100%; border-radius: 12px !important; height: 55px;
        font-weight: bold; border: none;
    }
    .stButton>button:hover { background: #ff9933 !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. Header
st.markdown("""
    <div class='main-banner'>
        <h1 style='margin:0;'>झारखण्ड मुख्यमंत्री मईयां सम्मान योजना (JMMSY)</h1>
        <p style='font-size: 1.2rem; opacity: 0.9; margin-top:10px;'>ज़िला प्रशासन, चतरा - संपूर्ण लाभार्थी विवरण पोर्टल</p>
    </div>
    """, unsafe_allow_html=True)

# 4. Data Loading & Live Calculations
SHEET_URL = "https://docs.google.com/spreadsheets/d/1fApqqsNEulpVsPH7O0IAMRvQv39DMYkV2PB_kg3qntg/export?format=csv"

@st.cache_data(ttl=60)
def load_data():
    try:
        df = pd.read_csv(SHEET_URL)
        df.columns = df.columns.str.strip()
        total = len(df)
        pay_col = 'PAYMENT STATUS' if 'PAYMENT STATUS' in df.columns else 'Payment Status'
        success = len(df[df[pay_col].astype(str).str.contains('success|paid', case=False, na=False)])
        return df, total, success, (total - success)
    except:
        return None, 0, 0, 0

df, total_b, success_b, pending_b = load_data()

# 5. Dashboard Stats
s1, s2, s3, s4 = st.columns(4)
with s1: st.markdown(f"<div class='stat-card'><small>कुल लाभार्थी</small><h2>{total_b:,}</h2></div>", unsafe_allow_html=True)
with s2: st.markdown(f"<div class='stat-card' style='border-top-color:#22c55e'><small>सफल भुगतान</small><h2 style='color:#22c55e'>{success_b:,}</h2></div>", unsafe_allow_html=True)
with s3: st.markdown(f"<div class='stat-card' style='border-top-color:#ef4444'><small>लंबित/विफल</small><h2 style='color:#ef4444'>{pending_b:,}</h2></div>", unsafe_allow_html=True)
with s4: st.markdown("<div class='stat-card'><small>ज़िला</small><h2>चतरा</h2></div>", unsafe_allow_html=True)

# 6. Search Area
_, mid, _ = st.columns([1, 2, 1])
with mid:
    st.write("")
    aadhar_input = st.text_input("Aadhar Number", placeholder="अपना 12 अंकों का आधार नंबर यहाँ लिखें...", label_visibility="collapsed")
    if st.button("सत्यापन करें") or aadhar_input:
        if aadhar_input and df is not None:
            clean_uid = str(aadhar_input).replace(" ", "")
            # Flexible Aadhar Column Match
            aadhar_col = next((c for c in ['Aadhaar Number', 'Aadhar Number', 'UID'] if c in df.columns), df.columns[0])
            df['temp_match'] = df[aadhar_col].astype(str).str.replace(" ", "").str.replace(".0", "", regex=False)
            
            match = df[df['temp_match'] == clean_uid].copy()
            
            if not match.empty:
                res = match.iloc[0]
                st.markdown("<div class='result-container'>", unsafe_allow_html=True)
                st.markdown(f"<h2 style='text-align:center; color:#002e5d;'>✅ लाभार्थी विवरण: {res.get('Applicant', 'N/A')}</h2>", unsafe_allow_html=True)
                
                # --- Detail Grid (Displaying ALL columns) ---
                # Section 1: Identity
                st.markdown("<div class='section-header'>👤 व्यक्तिगत विवरण (Identity)</div>", unsafe_allow_html=True)
                i1, i2, i3 = st.columns(3)
                i1.markdown(f"<div class='info-tile'><div class='info-label'>आवेदिका का नाम</div><div class='info-value'>{res.get('Applicant', 'N/A')}</div></div>", unsafe_allow_html=True)
                # Fix for Father's Name quote error
                father_val = res.get("Father's/Husband Name", 'N/A')
                i2.markdown(f"<div class='info-tile'><div class='info-label'>पिता/पति का नाम</div><div class='info-value'>{father_val}</div></div>", unsafe_allow_html=True)
                i3.markdown(f"<div class='info-tile'><div class='info-label'>आधार संख्या</div><div class='info-value'>XXXX-XXXX-{clean_uid[-4:]}</div></div>", unsafe_allow_html=True)

                # Section 2: Address
                st.markdown("<div class='section-header'>📍 आवासीय पता (Address)</div>", unsafe_allow_html=True)
                a1, a2, a3, a4 = st.columns(4)
                a1.markdown(f"<div class='info-tile'><div class='info-label'>ज़िला</div><div class='info-value'>{res.get('District', 'Chatra')}</div></div>", unsafe_allow_html=True)
                a2.markdown(f"<div class='info-tile'><div class='info-label'>प्रखंड (Block)</div><div class='info-value'>{res.get('Block', 'N/A')}</div></div>", unsafe_allow_html=True)
                a3.markdown(f"<div class='info-tile'><div class='info-label'>पंचायत</div><div class='info-value'>{res.get('Panchayat', 'N/A')}</div></div>", unsafe_allow_html=True)
                a4.markdown(f"<div class='info-tile'><div class='info-label'>गांव</div><div class='info-value'>{res.get('Village', 'N/A')}</div></div>", unsafe_allow_html=True)

                # Section 3: Bank & Payment (All status columns)
                st.markdown("<div class='section-header'>💰 बैंक एवं भुगतान विवरण (Bank & Payment)</div>", unsafe_allow_html=True)
                b1, b2, b3 = st.columns(3)
                b1.markdown(f"<div class='info-tile'><div class='info-label'>बैंक का नाम</div><div class='info-value'>{res.get('BankName', 'N/A')}</div></div>", unsafe_allow_html=True)
                acc = str(res.get('Account Number', 'N/A')).replace('.0', '').strip()
                b1.markdown(f"<div class='info-tile'><div class='info-label'>खाता संख्या</div><div class='info-value'>XXXXXX{acc[-4:] if len(acc)>4 else acc}</div></div>", unsafe_allow_html=True)
                
                b2.markdown(f"<div class='info-tile'><div class='info-label'>IFSC कोड</div><div class='info-value'>{res.get('IFSC', 'N/A')}</div></div>", unsafe_allow_html=True)
                b2.markdown(f"<div class='info-tile'><div class='info-label'>PDS Status</div><div class='info-value' style='color:#002e5d;'>{res.get('PDS_Status', 'N/A')}</div></div>
