import streamlit as st
import pandas as pd
import time

# 1. Page Configuration
st.set_page_config(page_title="JMMSY | Official Portal", layout="wide", page_icon="🏛️")

# 2. Advanced Professional CSS (Full Website Look)
st.markdown("""
    <style>
    .stApp { background-color: #f0f2f5; }
    
    /* Official Header Banner */
    .gov-banner {
        background: linear-gradient(135deg, #002e5d 0%, #004a99 100%);
        color: white; padding: 3rem; text-align: center;
        border-radius: 0 0 40px 40px; box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        margin-bottom: 2rem; border-bottom: 6px solid #ff9933;
    }

    /* Dashboard Stats Metric Cards */
    .metric-card {
        background: white; padding: 25px; border-radius: 20px;
        text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border-top: 5px solid #ff9933;
    }

    /* Professional Result Profile Card */
    .profile-container {
        background: white; padding: 40px; border-radius: 30px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.1); margin-top: 30px;
        border: 1px solid #e2e8f0; animation: fadeInUp 0.8s ease-out;
    }
    
    .section-head {
        color: #002e5d; border-bottom: 2px solid #ff9933;
        padding-bottom: 10px; margin: 30px 0 20px 0; font-weight: 800;
        text-transform: uppercase; font-size: 1rem; letter-spacing: 1px;
    }

    .data-tile {
        background: #f8fafc; padding: 18px; border-radius: 12px;
        margin-bottom: 15px; border-left: 5px solid #002e5d;
    }
    .data-label { color: #64748b; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; margin-bottom: 5px; }
    .data-value { color: #1e293b; font-size: 1.1rem; font-weight: 700; }

    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Professional Search Button */
    .stButton>button {
        background: linear-gradient(90deg, #002e5d, #004a99) !important;
        color: white !important; width: 100%; border-radius: 12px !important;
        height: 55px; font-weight: bold; border: none; transition: 0.3s;
    }
    .stButton>button:hover { background: #ff9933 !important; transform: translateY(-2px); }
    </style>
    """, unsafe_allow_html=True)

# 3. Official Banner Header
st.markdown("""
    <div class='gov-banner'>
        <h1 style='margin:0;'>झारखण्ड मुख्यमंत्री मईयां सम्मान योजना (JMMSY)</h1>
        <p style='font-size: 1.3rem; opacity: 0.9; margin-top:10px;'>ज़िला प्रशासन, चतरा - आधिकारिक लाभार्थी डेटा एवं भुगतान सत्यापन पोर्टल</p>
    </div>
    """, unsafe_allow_html=True)

# 4. Data Loading and Live Analytics
SHEET_URL = "https://docs.google.com/spreadsheets/d/1fApqqsNEulpVsPH7O0IAMRvQv39DMYkV2PB_kg3qntg/export?format=csv"

@st.cache_data(ttl=60)
def fetch_portal_data():
    try:
        df = pd.read_csv(SHEET_URL)
        df.columns = df.columns.str.strip()
        total = len(df)
        pay_col = 'PAYMENT STATUS' if 'PAYMENT STATUS' in df.columns else 'Payment Status'
        success = len(df[df[pay_col].astype(str).str.contains('success|paid', case=False, na=False)])
        return df, total, success, (total - success)
    except:
        return None, 0, 0, 0

# Indentation correct hai yahan
df, t_count, s_count, p_count = fetch_portal_data()

# 5. Live Dashboard Metrics
m1, m2, m3, m4 = st.columns(4)
with m1: st.markdown(f"<div class='metric-card'><small>कुल लाभार्थी</small><h2>{t_count:,}</h2></div>", unsafe_allow_html=True)
with m2: st.markdown(f"<div class='metric-card' style='border-top-color:#22c55e'><small>सफल भुगतान</small><h2 style='color:#22c55e'>{s_count:,}</h2></div>", unsafe_allow_html=True)
with m3: st.markdown(f"<div class='metric-card' style='border-top-color:#ef4444'><small>लंबित/विफल</small><h2 style='color:#ef4444'>{p_count:,}</h2></div>", unsafe_allow_html=True)
with m4: st.markdown("<div class='metric-card' style='border-top-color:#002e5d'><small>ज़िला स्थिति</small><h2>चतरा (LIVE)</h2></div>", unsafe_allow_html=True)

st.write("")

# 6. Search Interface
_, search_area, _ = st.columns([1, 2, 1])
with search_area:
    st.markdown("<h3 style='text-align: center; color: #002e5d;'>🔍 लाभार्थी की स्थिति जांचें</h3>", unsafe_allow_html=True)
    aadhar_in = st.text_input("Aadhar Number", placeholder="अपना 12 अंकों का आधार नंबर यहाँ दर्ज करें...", label_visibility="collapsed")
    
    if st.button("सत्यापन करें") or aadhar_in:
        if aadhar_in and df is not None:
            clean_in = str(aadhar_in).replace(" ", "")
            # Aadhaar Column mapping logic
            uid_col = next((c for c in ['Aadhaar Number', 'Aadhar Number', 'UID'] if c in df.columns), df.columns[0])
            df['key'] = df[uid_col].astype(str).str.replace(" ", "").str.replace(".0", "", regex=False)
            
            match = df[df['key'] == clean_in].copy()
            
            if not match.empty:
                res = match.iloc[0]
                
                # --- START RESULT PROFILE SECTION ---
                st.markdown("<div class='profile-container'>", unsafe_allow_html=True)
                st.markdown(f"<h2 style='text-align:center; color:#002e5d; margin-bottom:40px;'>✅ लाभार्थी प्रोफाइल: {res.get('Applicant', 'N/A')}</h2>", unsafe_allow_html=True)
                
                # Column Grid Layout
                # IDENTITY SECTION
                st.markdown("<div class='section-head'>👤 व्यक्तिगत विवरण (Personal Details)</div>", unsafe_allow_html=True)
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f"<div class='data-tile'><div class='data-label'>आवेदिका का नाम</div><div class='data-value'>{res.get('Applicant', 'N/A')}</div></div>", unsafe_allow_html=True)
                    # Father's/Husband Name handle karne ke liye variable
                    f_name = res.get("Father's/Husband Name", 'N/A')
                    st.markdown(f"<div class='data-tile'><div class='data-label'>पिता/पति का नाम</div><div class='data-value'>{f_name}</div></div>", unsafe_allow_html=True)
                with col2:
                    st.markdown(f"<div class='data-tile'><div class='data-label'>आधार संख्या</div><div class='data-value'>XXXX-XXXX-{clean_in[-4:]}</div></div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='data-tile'><div class='data-label'>उम्र (Age)</div><div class='data-value'>{res.get('Age', 'N/A')} Years</div></div>", unsafe_allow_html=True)
                with col3:
                    st.markdown(f"<div class='data-tile'><div class='data-label'>मोबाइल नंबर</div><div class='data-value'>{res.get('Mobile Number', 'N/A')}</div></div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='data-tile'><div class='data-label'>श्रेणी (Category)</div><div class='data-value'>{res.get('Category', 'N/A')}</div></div>", unsafe_allow_html=True)

                # LOCATION SECTION
                st.markdown("<div class='section-head'>📍 आवासीय पता (Location)</div>", unsafe_allow_html=True)
                loc1, loc2, loc3, loc4 = st.columns(4)
                loc1.markdown(f"<div class='data-tile'><div class='data-label'>ज़िला</div><div class='data-value'>{res.get('District', 'Chatra')}</div></div>", unsafe_allow_html=True)
                loc2.markdown(f"<div class='data-tile'><div class='data-label'>प्रखंड (Block)</div><div class='data-value'>{res.get('Block', 'N/A')}</div></div>", unsafe_allow_html=True)
                loc3.markdown(f"<div class='data-tile'><div class='data-label'>पंचायत</div><div class='data-value'>{res.get('Panchayat', 'N/A')}</div></div>", unsafe_allow_html=True)
                loc4.markdown(f"<div class='data-tile'><div class='data-label'>गांव</div><div class='data-value'>{res.get('Village', 'N/A')}</div></div>", unsafe_allow_html=True)

                # FINANCIAL SECTION
                st.markdown("<div class='section-head'>💰 बैंक एवं भुगतान विवरण (Bank Status)</div>", unsafe_allow_html=True)
                b1, b2, b3 = st.columns(3)
                with b1:
                    st.markdown(f"<div class='data-tile'><div class='data-label'>बैंक का नाम</div><div class='data-value'>{res.get('BankName', 'N/A')}</div></div>", unsafe_allow_html=True)
                    acc_raw = str(res.get('Account Number', 'N/A')).replace('.0', '').strip()
                    st.markdown(f"<div class='data-tile'><div class='data-label'>खाता संख्या</div><div class='data-value'>XXXXXX{acc_raw[-4:] if len(acc_raw)>4 else acc_raw}</div></div>", unsafe_allow_html=True)
                with b2:
                    st.markdown(f"<div class='data-tile'><div class='data-label'>IFSC कोड</div><div class='data-value'>{res.get('IFSC', 'N/A')}</div></div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='data-tile'><div class='data-label'>PDS Status</div><div class='data-value' style='color:#002e5d;'>{res.get('PDS_Status', 'N/A')}</div></div>", unsafe_allow_html=True)
                with b3:
                    p_stat = res.get('PAYMENT STATUS', res.get('Payment Status', 'N/A'))
                    p_clr = "#22c55e" if "success" in str(p_stat).lower() else "#ef4444"
                    st.markdown(f"<div class='data-tile'><div class='data-label'>Payment Status</div><div class='data-value' style='color:{p_clr};'>{p_stat}</div></div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='data-tile'><div class='data-label'>पंजीकरण तिथि</div><div class='data-value'>{res.get('Registration Date', 'N/A')}</div></div>", unsafe_allow_html=True)

                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.error("❌ आधार नंबर रिकॉर्ड में नहीं मिला। कृपया पुनः जाँचें।")

# 7. Official Footer
st.write("---")
st.markdown("<center style='color:#64748b; font-size:0.85rem;'>© 2026 District Administration Chatra | Support: National Informatics Centre (NIC)</center>", unsafe_allow_html=True)
