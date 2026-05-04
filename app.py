import streamlit as st
import pandas as pd
import time

# 1. Page Configuration
st.set_page_config(page_title="JMMSY Official Portal", layout="wide", page_icon="🏛️")

# 2. Advanced Premium CSS (Professional Gov Dashboard)
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #eef2f3 0%, #8e9eab 100%);
    }
    /* Banner Header */
    .banner {
        background: linear-gradient(90deg, #002e5d 0%, #00509d 100%);
        color: white;
        padding: 40px;
        text-align: center;
        border-radius: 0 0 40px 40px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        margin-bottom: 40px;
        border-bottom: 6px solid #ff9933;
    }
    /* Stats Cards */
    .stat-box {
        background: rgba(255, 255, 255, 0.9);
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border-top: 5px solid #002e5d;
    }
    /* Result Card Detail Styling */
    .card-container {
        background: white;
        padding: 35px;
        border-radius: 25px;
        box-shadow: 0 15px 45px rgba(0,0,0,0.12);
        margin-top: 20px;
        border: 1px solid #ddd;
        animation: fadeInUp 0.8s ease-in-out;
    }
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .label { color: #555; font-size: 0.85rem; font-weight: 700; text-transform: uppercase; margin-bottom: 5px; }
    .data-val { color: #002e5d; font-size: 1.15rem; font-weight: 700; margin-bottom: 20px; background: #f9f9f9; padding: 10px; border-radius: 8px; border-left: 5px solid #ff9933; }
    
    /* Search Button */
    .stButton>button {
        background: linear-gradient(to right, #002e5d, #00509d) !important;
        color: white !important;
        border-radius: 12px !important;
        height: 55px !important;
        font-weight: bold !important;
        width: 100%;
        font-size: 1.1rem !important;
        border: none !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Official Banner
st.markdown("""
    <div class='banner'>
        <h1 style='margin:0;'>झारखण्ड मुख्यमंत्री मईयां सम्मान योजना (JMMSY)</h1>
        <p style='font-size: 1.3rem; opacity: 0.9;'>ज़िला प्रशासन, चतरा - आधिकारिक लाभार्थी सत्यापन एवं भुगतान पोर्टल</p>
    </div>
    """, unsafe_allow_html=True)

# 4. Data Retrieval
SHEET_URL = "https://docs.google.com/spreadsheets/d/1fApqqsNEulpVsPH7O0IAMRvQv39DMYkV2PB_kg3qntg/export?format=csv"

@st.cache_data(ttl=60)
def get_data():
    try:
        df = pd.read_csv(SHEET_URL)
        df.columns = df.columns.str.strip()
        return df
    except Exception:
        return None

df = get_data()

# 5. Dashboard Stats Row
s1, s2, s3, s4 = st.columns(4)
with s1: st.markdown("<div class='stat-box'><small>District</small><h3>चतरा</h3></div>", unsafe_allow_html=True)
with s2: st.markdown("<div class='stat-box'><small>Status</small><h3>LIVE</h3></div>", unsafe_allow_html=True)
with s3: st.markdown("<div class='stat-box'><small>WCD</small><h3>Jharkhand</h3></div>", unsafe_allow_html=True)
with s4: st.markdown("<div class='stat-box'><small>Update</small><h3>Real-time</h3></div>", unsafe_allow_html=True)

st.write("")

# 6. Search Interface
_, search_area, _ = st.columns([1, 2, 1])
with search_area:
    st.markdown("<h3 style='text-align: center; color: #002e5d;'>🔍 लाभार्थी की स्थिति जांचें</h3>", unsafe_allow_html=True)
    user_input = st.text_input("Aadhar", placeholder="अपना 12 अंकों का आधार नंबर यहाँ दर्ज करें...", label_visibility="collapsed")
    search_click = st.button("सत्यापन करें")

# 7. Search Logic & Detailed Card
if (search_click or user_input) and user_input:
    if df is not None:
        # User input cleanup
        uid_input = str(user_input).replace(" ", "")
        
        # Mapping Column E (Aadhaar Number)
        target_col = 'Aadhaar Number' if 'Aadhaar Number' in df.columns else df.columns[4]
        
        # Flexible match (Removing spaces from sheet data too)
        df['temp_match'] = df[target_col].astype(str).str.replace(" ", "").str.replace(".0", "", regex=False)
        
        match = df[df['temp_match'] == uid_input].copy()
        
        if not match.empty:
            with st.spinner('डेटाबेस से जानकारी मिलान की जा रही है...'):
                time.sleep(0.5)
            
            row = match.iloc[0]
            
            # Formatting Masked Data
            def mask_acc(val):
                v = str(val).replace('.0', '').strip()
                return f"XXXXXX{v[-4:]}" if len(v) > 4 else v

            # --- Result Card Display ---
            st.markdown("<div class='card-container'>", unsafe_allow_html=True)
            st.markdown("<h2 style='text-align:center; color:#002e5d; border-bottom:2px solid #eee; padding-bottom:15px;'>✅ सत्यापित लाभार्थी विवरण</h2>", unsafe_allow_html=True)
            
            res_c1, res_c2, res_c3 = st.columns(3)
            
            with res_c1:
                st.markdown(f"<div class='label'>लाभार्थी का नाम</div><div class='data-val'>{row.get('Applicant', 'N/A')}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='label'>ज़िला / प्रखंड</div><div class='data-val'>{row.get('District', 'Chatra')} / {row.get('Block', 'N/A')}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='label'>आधार संख्या</div><div class='data-val'>XXXX-XXXX-{uid_input[-4:]}</div>", unsafe_allow_html=True)

            with res_c2:
                st.markdown(f"<div class='label'>पिता/पति का नाम</div><div class='data-val'>{row.get(\"Father's/Husband Name\", 'N/A')}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='label'>पंचायत / गांव</div><div class='data-val'>{row.get('Panchayat', 'N/A')} / {row.get('Village', 'N/A')}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='label'>PDS STATUS</div><div class='data-val' style='color:#002e5d;'>{row.get('PDS_Status', 'N/A')}</div>", unsafe_allow_html=True)

            with res_c3:
                # PAYMENT STATUS Logic from Column R/S
                p_status = row.get('PAYMENT STATUS', row.get('Payment Status', 'N/A'))
                clr = "#28a745" if "success" in str(p_status).lower() or "paid" in str(p_status).lower() else "#d32f2f"
                
                st.markdown(f"<div class='label'>बैंक का नाम</div><div class='data-val'>{row.get('BankName', 'N/A')}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='label'>खाता संख्या</div><div class='data-val'>{mask_acc(row.get('Account Number', 'N/A'))}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='label'>भुगतान की स्थिति</div><div class='data-val' style='color:{clr}; border-left: 5px solid {clr};'>{p_status}</div>", unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.error("❌ आधार नंबर रिकॉर्ड में नहीं मिला। कृपया पुनः जाँचें।")
    else:
        st.error("डेटाबेस लोड नहीं हो सका। कृपया इंटरनेट या लिंक जाँचें।")

# 8. Official Footer
st.markdown("<br><br><center style='color:#666; font-size:0.8rem;'>NIC Jharkhand | District Administration Chatra Official Portal</center>", unsafe_allow_html=True)
