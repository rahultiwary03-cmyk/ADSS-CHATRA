import streamlit as st
import pandas as pd
import time

# 1. Page Configuration
st.set_page_config(page_title="JMMSY | Chatra Portal", layout="wide", page_icon="🏛️")

# 2. Advanced Professional Styling (Government Theme)
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background-color: #f4f7f6;
    }
    
    /* Elegant Gov Header */
    .gov-banner {
        background: linear-gradient(135deg, #002e5d 0%, #00509d 100%);
        color: white;
        padding: 35px;
        text-align: center;
        border-radius: 0 0 25px 25px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        margin-bottom: 30px;
    }

    /* Stat Cards */
    .stat-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border-bottom: 4px solid #ff9933;
    }

    /* Result Card Styling */
    .result-card {
        background: white;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        border-left: 10px solid #28a745;
        margin-top: 25px;
        animation: slideUp 0.6s ease-out;
    }

    @keyframes slideUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .label-text { color: #555; font-size: 0.85rem; font-weight: 600; text-transform: uppercase; margin-bottom: 2px; }
    .value-text { color: #111; font-size: 1.15rem; font-weight: 700; margin-bottom: 15px; border-bottom: 1px solid #eee; padding-bottom: 5px; }
    
    /* Buttons */
    .stButton>button {
        background-color: #002e5d !important;
        color: white !important;
        width: 100%;
        border-radius: 10px;
        height: 50px;
        font-weight: bold;
        font-size: 1.1rem;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Header
st.markdown("""
    <div class='gov-banner'>
        <h1 style='margin:0; font-size: 2.5rem;'>झारखण्ड मुख्यमंत्री मईयां सम्मान योजना (JMMSY)</h1>
        <p style='font-size: 1.2rem; opacity: 0.9; font-weight: 300;'>ज़िला प्रशासन, चतरा - भुगतान स्थिति खोजें</p>
    </div>
    """, unsafe_allow_html=True)

# 4. Data Loading (Google Sheets)
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

# 5. Dashboard Stats
col1, col2, col3 = st.columns(3)
with col1: st.markdown("<div class='stat-card'><small>कुल लाभार्थी</small><h2>1,89,174</h2></div>", unsafe_allow_html=True)
with col2: st.markdown("<div class='stat-card'><small>ज़िला</small><h2>चतरा (CHATRA)</h2></div>", unsafe_allow_html=True)
with col3: st.markdown("<div class='stat-card'><small>स्थिति</small><h2 style='color:#28a745;'>● सक्रिय</h2></div>", unsafe_allow_html=True)

st.write("")

# 6. Search Interface
_, center_col, _ = st.columns([1, 2, 1])
with center_col:
    st.markdown("<h4 style='text-align: center; color: #002e5d;'>🔍 लाभार्थी की स्थिति जांचें</h4>", unsafe_allow_html=True)
    aadhar_input = st.text_input("Aadhaar Number", placeholder="अपना आधार नंबर दर्ज करें...", label_visibility="collapsed")
    search_clicked = st.button("स्टेटस चेक करें")

# 7. Search Logic & Result Display
if (search_clicked or aadhar_input) and aadhar_input:
    if df is not None:
        # Aadhaar Column cleaning for spaces
        target_col = 'Aadhaar Number' if 'Aadhaar Number' in df.columns else 'Aadhar Number'
        
        # User input cleanup
        clean_input = str(aadhar_input).replace(" ", "")
        
        # DataFrame cleaning (Temporary key for matching)
        df['match_key'] = df[target_col].astype(str).str.replace(" ", "").str.replace(".0", "", regex=False)
        
        match = df[df['match_key'] == clean_input].copy()
        
        if not match.empty:
            with st.spinner('कृपया प्रतीक्षा करें...'):
                time.sleep(0.7)
            
            res = match.iloc[0]
            
            # Formatting Masked Data
            masked_aadhar = f"XXXX-XXXX-{clean_input[-4:]}"
            
            # Masking Bank Account (detecting column)
            acc_val = "N/A"
            for c in ['AccountNo', 'Account Number', 'Account']:
                if c in res:
                    raw_acc = str(res[c]).replace('.0', '').strip()
                    acc_val = f"XXXXXX{raw_acc[-4:]}" if len(raw_acc) > 4 else raw_acc

            # --- STYLISH RESULT CARD ---
            st.markdown("<div class='result-card'>", unsafe_allow_html=True)
            st.success("✅ लाभार्थी का विवरण मिल गया है")
            
            r_col1, r_col2 = st.columns(2)
            with r_col1:
                st.markdown(f"<div class='label-text'>लाभार्थी का नाम</div><div class='value-text'>{res.get('ApplicantName', res.get('Name', 'N/A'))}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='label-text'>आधार संख्या</div><div class='value-text'>{masked_aadhar}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='label-text'>पिता/पति का नाम</div><div class='value-text'>{res.get('Father\'s/Husband Name', 'N/A')}</div>", unsafe_allow_html=True)
            
            with r_col2:
                st.markdown(f"<div class='label-text'>बैंक का नाम</div><div class='value-text'>{res.get('BankName', 'N/A')}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='label-text'>खाता संख्या</div><div class='value-text'>{acc_val}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='label-text'>भुगतान स्थिति</div><div class='value-text' style='color:#28a745;'>सफल (Success)</div>", unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.error("❌ यह आधार नंबर रिकॉर्ड में नहीं मिला। कृपया पुनः जाँचें।")
    else:
        st.error("डेटा लोड करने में समस्या आ रही है।")

# 8. Footer
st.markdown("""
    <div style='text-align: center; margin-top: 50px; padding: 20px; color: #888; font-size: 0.9rem;'>
        <hr>
        © 2024 District Administration, Chatra | Digital India | NIC Jharkhand
    </div>
    """, unsafe_allow_html=True)
