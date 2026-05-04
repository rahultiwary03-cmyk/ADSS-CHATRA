import streamlit as st
import pandas as pd
import time

# 1. Page Configuration
st.set_page_config(page_title="JMMSY Official Portal | Chatra", layout="wide", page_icon="🏛️")

# 2. Premium Professional CSS
st.markdown("""
    <style>
    .stApp { background-color: #f8fafc; }
    
    .main-header {
        background: linear-gradient(135deg, #002e5d 0%, #00509d 100%);
        color: white; padding: 40px; text-align: center;
        border-radius: 0 0 30px 30px; box-shadow: 0 10px 25px rgba(0,0,0,0.15);
        margin-bottom: 30px; border-bottom: 6px solid #ff9933;
    }
    
    .stat-card {
        background: white; padding: 20px; border-radius: 15px;
        text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border-top: 5px solid #ff9933;
    }

    .result-card {
        background: white; padding: 35px; border-radius: 20px;
        box-shadow: 0 15px 40px rgba(0,0,0,0.1);
        border-left: 10px solid #002e5d; margin-top: 25px;
        animation: fadeIn 0.7s ease-in-out;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .label-text { color: #64748b; font-size: 0.8rem; font-weight: 700; text-transform: uppercase; }
    .value-text { color: #1e293b; font-size: 1.1rem; font-weight: 700; margin-bottom: 15px; background: #f1f5f9; padding: 10px; border-radius: 8px; }
    
    .stButton>button {
        background: #002e5d !important; color: white !important;
        width: 100%; border-radius: 12px !important; height: 50px; font-weight: bold;
    }
    .stButton>button:hover { background: #ff9933 !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. Header
st.markdown("""
    <div class='main-header'>
        <h1 style='margin:0;'>झारखण्ड मुख्यमंत्री मईयां सम्मान योजना (JMMSY)</h1>
        <p style='font-size: 1.2rem; opacity: 0.9;'>ज़िला प्रशासन, चतरा - लाभार्थी सत्यापन एवं डैशबोर्ड</p>
    </div>
    """, unsafe_allow_html=True)

# 4. Data Fetching & Calculations
SHEET_URL = "https://docs.google.com/spreadsheets/d/1fApqqsNEulpVsPH7O0IAMRvQv39DMYkV2PB_kg3qntg/export?format=csv"

@st.cache_data(ttl=60)
def load_and_stats():
    try:
        df = pd.read_csv(SHEET_URL)
        df.columns = df.columns.str.strip()
        
        # Live Stats Calculation
        total = len(df)
        # Payment Status column R ya S se success count nikalna
        pay_col = 'PAYMENT STATUS' if 'PAYMENT STATUS' in df.columns else 'Payment Status'
        success = len(df[df[pay_col].astype(str).str.contains('success|paid', case=False, na=False)])
        pending = total - success
        
        return df, total, success, pending
    except:
        return None, 0, 0, 0

df, total_b, success_b, pending_b = load_and_stats()

# 5. Live Dashboard Stats
c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown(f"<div class='stat-card'><small>कुल लाभार्थी</small><h2>{total_b:,}</h2></div>", unsafe_allow_html=True)
with c2: st.markdown(f"<div class='stat-card' style='border-top-color:#28a745'><small>सफल भुगतान</small><h2 style='color:#28a745'>{success_b:,}</h2></div>", unsafe_allow_html=True)
with c3: st.markdown(f"<div class='stat-card' style='border-top-color:#dc3545'><small>लंबित/विफल</small><h2 style='color:#dc3545'>{pending_b:,}</h2></div>", unsafe_allow_html=True)
with c4: st.markdown(f"<div class='stat-card' style='border-top-color:#002e5d'><small>ज़िला</small><h2>चतरा</h2></div>", unsafe_allow_html=True)

st.write("")

# 6. Search Interface
_, search_box, _ = st.columns([1, 2, 1])
with search_box:
    st.markdown("<h3 style='text-align: center; color: #002e5d;'>🔍 स्टेटस चेक करें</h3>", unsafe_allow_html=True)
    input_uid = st.text_input("Aadhar", placeholder="आधार नंबर दर्ज करें...", label_visibility="collapsed")
    btn = st.button("सत्यापन करें")

# 7. Result Logic
if (btn or input_uid) and input_uid:
    if df is not None:
        clean_uid = str(input_uid).replace(" ", "")
        # Aadhaar Column match
        df['temp_key'] = df['Aadhaar Number'].astype(str).str.replace(" ", "").str.replace(".0", "", regex=False)
        match = df[df['temp_key'] == clean_uid].copy()
        
        if not match.empty:
            res = match.iloc[0]
            st.markdown("<div class='result-card'>", unsafe_allow_html=True)
            st.markdown("<h2 style='text-align:center; color:#002e5d; margin-bottom:30px;'>✅ लाभार्थी जानकारी</h2>", unsafe_allow_html=True)
            
            r1, r2, r3 = st.columns(3)
            with r1:
                st.markdown(f"<div class='label-text'>नाम</div><div class='value-text'>{res.get('Applicant', 'N/A')}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='label-text'>प्रखंड (Block)</div><div class='value-text'>{res.get('Block', 'N/A')}</div>", unsafe_allow_html=True)
            
            with r2:
                f_name = res.get("Father's/Husband Name", 'N/A')
                st.markdown(f"<div class='label-text'>पिता/पति</div><div class='value-text'>{f_name}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='label-text'>बैंक</div><div class='value-text'>{res.get('BankName', 'N/A')}</div>", unsafe_allow_html=True)

            with r3:
                p_status = res.get('PAYMENT STATUS', res.get('Payment Status', 'N/A'))
                p_color = "#28a745" if "success" in str(p_status).lower() else "#dc3545"
                st.markdown(f"<div class='label-text'>PDS STATUS</div><div class='value-text'>{res.get('PDS_Status', 'N/A')}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='label-text'>PAYMENT STATUS</div><div class='value-text' style='color:{p_color}'>{p_status}</div>", unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.error("❌ रिकॉर्ड नहीं मिला।")

# 8. Extra Features (Website looks complete)
st.write("---")
l_col, r_col = st.columns(2)
with l_col:
    st.subheader("📢 महत्वपूर्ण सूचना")
    st.info("यदि आपका भुगतान लंबित है, तो कृपया अपने आधार बैंक लिंकिंग (NPCI) की जाँच करें।")
with r_col:
    st.subheader("🔗 उपयोगी लिंक")
    st.markdown("- [Official JMMSY Portal](https://mmmsy.jharkhand.gov.in/)")
    st.markdown("- [District Chatra Official](https://chatra.nic.in/)")

st.markdown("<br><center style='color:#666;'>© 2026 District Administration Chatra | Support: NIC Chatra</center>", unsafe_allow_html=True)
