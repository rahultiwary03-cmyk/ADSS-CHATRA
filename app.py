import streamlit as st
import pandas as pd
import time

# 1. Page Configuration
st.set_page_config(page_title="JMMSY | Chatra Official Portal", layout="wide", page_icon="🏛️")

# 2. Advanced Premium CSS
st.markdown("""
    <style>
    .stApp { background-color: #f1f5f9; }
    
    /* Official Header */
    .gov-header {
        background: linear-gradient(135deg, #002e5d 0%, #004a99 100%);
        color: white; padding: 3rem; text-align: center;
        border-radius: 0 0 40px 40px; box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        margin-bottom: 2rem; border-bottom: 6px solid #ff9933;
    }

    /* Stats Section */
    .stat-card {
        background: white; padding: 20px; border-radius: 15px;
        text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border-top: 5px solid #ff9933;
    }

    /* Result Layout Styling */
    .result-container {
        background: white; padding: 40px; border-radius: 25px;
        box-shadow: 0 20px 50px rgba(0,0,0,0.1); margin-top: 20px;
        border: 1px solid #e2e8f0; animation: fadeInUp 0.7s ease-out;
    }
    
    .section-title {
        color: #002e5d; border-bottom: 2px solid #ff9933;
        padding-bottom: 10px; margin-bottom: 25px; font-weight: 800;
        text-transform: uppercase; letter-spacing: 1px;
    }

    .info-tile {
        background: #f8fafc; padding: 15px; border-radius: 10px;
        margin-bottom: 15px; border-left: 4px solid #002e5d;
    }
    .info-label { color: #64748b; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; }
    .info-value { color: #1e293b; font-size: 1rem; font-weight: 700; }

    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Custom Search Button */
    .stButton>button {
        background: #002e5d !important; color: white !important;
        width: 100%; border-radius: 12px !important; height: 55px;
        font-weight: bold; font-size: 1.1rem; border: none;
    }
    .stButton>button:hover { background: #ff9933 !important; color: white !important; transform: translateY(-2px); }
    </style>
    """, unsafe_allow_html=True)

# 3. Official Header Banner
st.markdown("""
    <div class='gov-header'>
        <h1 style='margin:0;'>झारखण्ड मुख्यमंत्री मईयां सम्मान योजना (JMMSY)</h1>
        <p style='font-size: 1.3rem; opacity: 0.9; margin-top:10px;'>ज़िला प्रशासन, चतरा - लाभार्थी डेटा एवं भुगतान सत्यापन प्रणाली</p>
    </div>
    """, unsafe_allow_html=True)

# 4. Data Fetching and Live Stats
SHEET_URL = "https://docs.google.com/spreadsheets/d/1fApqqsNEulpVsPH7O0IAMRvQv39DMYkV2PB_kg3qntg/export?format=csv"

@st.cache_data(ttl=60)
def get_live_data():
    try:
        df = pd.read_csv(SHEET_URL)
        df.columns = df.columns.str.strip()
        total = len(df)
        # Payment Status counting
        pay_col = 'PAYMENT STATUS' if 'PAYMENT STATUS' in df.columns else 'Payment Status'
        success = len(df[df[pay_col].astype(str).str.contains('success|paid', case=False, na=False)])
        pending = total - success
        return df, total, success, pending
    except:
        return None, 0, 0, 0

df, total_count, success_count, pending_count = get_live_data()

# 5. Dashboard Summary Stats
s1, s2, s3, s4 = st.columns(4)
with s1: st.markdown(f"<div class='stat-card'><small>कुल लाभार्थी</small><h2>{total_count:,}</h2></div>", unsafe_allow_html=True)
with s2: st.markdown(f"<div class='stat-card' style='border-top-color:#22c55e'><small>सफल भुगतान</small><h2 style='color:#22c55e'>{success_count:,}</h2></div>", unsafe_allow_html=True)
with s3: st.markdown(f"<div class='stat-card' style='border-top-color:#ef4444'><small>लंबित भुगतान</small><h2 style='color:#ef4444'>{pending_count:,}</h2></div>", unsafe_allow_html=True)
with s4: st.markdown(f"<div class='stat-card' style='border-top-color:#002e5d'><small>ज़िला</small><h2>चतरा</h2></div>", unsafe_allow_html=True)

st.write("")

# 6. Search Section
_, search_box, _ = st.columns([1, 2, 1])
with search_box:
    st.markdown("<h3 style='text-align: center; color: #002e5d;'>🔍 लाभार्थी की स्थिति जांचें</h3>", unsafe_allow_html=True)
    aadhar_in = st.text_input("Aadhar", placeholder="अपना 12 अंकों का आधार नंबर दर्ज करें...", label_visibility="collapsed")
    find_btn = st.button("स्टेटस चेक करें")

# 7. Comprehensive Result Display (Showing ALL columns)
if (find_btn or aadhar_in) and aadhar_in:
    if df is not None:
        clean_in = str(aadhar_in).replace(" ", "")
        # Aadhaar matching logic
        df['match_key'] = df['Aadhaar Number'].astype(str).str.replace(" ", "").str.replace(".0", "", regex=False)
        match = df[df['match_key'] == clean_in].copy()
        
        if not match.empty:
            res = match.iloc[0]
            st.markdown("<div class='result-container'>", unsafe_allow_html=True)
            st.markdown(f"<h2 style='text-align:center; color:#002e5d;'>✅ लाभार्थी विवरण: {res.get('Applicant', 'N/A')}</h2>", unsafe_allow_html=True)
            
            # --- SECTION 1: Personal Details ---
            st.markdown("<h4 class='section-title'>👤 व्यक्तिगत जानकारी</h4>", unsafe_allow_html=True)
            p1, p2, p3 = st.columns(3)
            with p1:
                st.markdown(f"<div class='info-tile'><div class='info-label'>लाभार्थी का नाम</div><div class='info-value'>{res.get('Applicant', 'N/A')}</div></div>", unsafe_allow_html=True)
                st.markdown(f"<div class='info-tile'><div class='info-label'>पिता/पति का नाम</div><div class='info-value'>{res.get(\"Father's/Husband Name\", 'N/A')}</div></div>", unsafe_allow_html=True)
            with p2:
                st.markdown(f"<div class='info-tile'><div class='info-label'>मोबाइल नंबर</div><div class='info-value'>{res.get('Mobile Number', 'N/A')}</div></div>", unsafe_allow_html=True)
                st.markdown(f"<div class='info-tile'><div class='info-label'>आधार नंबर</div><div class='info-value'>XXXX-XXXX-{clean_in[-4:]}</div></div>", unsafe_allow_html=True)
            with p3:
                st.markdown(f"<div class='info-tile'><div class='info-label'>उम्र</div><div class='info-value'>{res.get('Age', 'N/A')}</div></div>", unsafe_allow_html=True)
                st.markdown(f"<div class='info-tile'><div class='info-label'>श्रेणी (Category)</div><div class='info-value'>{res.get('Category', 'N/A')}</div></div>", unsafe_allow_html=True)

            # --- SECTION 2: Address Details ---
            st.markdown("<h4 class='section-title'>📍 पता विवरण</h4>", unsafe_allow_html=True)
            a1, a2, a3, a4 = st.columns(4)
            with a1: st.markdown(f"<div class='info-tile'><div class='info-label'>ज़िला</div><div class='info-value'>{res.get('District', 'Chatra')}</div></div>", unsafe_allow_html=True)
            with a2: st.markdown(f"<div class='info-tile'><div class='info-label'>प्रखंड (Block)</div><div class='info-value'>{res.get('Block', 'N/A')}</div></div>", unsafe_allow_html=True)
            with a3: st.markdown(f"<div class='info-tile'><div class='info-label'>पंचायत</div><div class='info-value'>{res.get('Panchayat', 'N/A')}</div></div>", unsafe_allow_html=True)
            with a4: st.markdown(f"<div class='info-tile'><div class='info-label'>गांव</div><div class='info-value'>{res.get('Village', 'N/A')}</div></div>", unsafe_allow_html=True)

            # --- SECTION 3: Bank & Status ---
            st.markdown("<h4 class='section-title'>💰 बैंक एवं भुगतान की स्थिति</h4>", unsafe_allow_html=True)
            b1, b2, b3 = st.columns(3)
            with b1:
                st.markdown(f"<div class='info-tile'><div class='info-label'>बैंक का नाम</div><div class='info-value'>{res.get('BankName', 'N/A')}</div></div>", unsafe_allow_html=True)
                acc = str(res.get('Account Number', 'N/A')).replace('.0', '').strip()
                st.markdown(f"<div class='info-tile'><div class='info-label'>खाता संख्या</div><div class='info-value'>XXXXXX{acc[-4:]}</div></div>", unsafe_allow_html=True)
            with b2:
                st.markdown(f"<div class='info-tile'><div class='info-label'>IFSC कोड</div><div class='info-value'>{res.get('IFSC', 'N/A')}</div></div>", unsafe_allow_html=True)
                st.markdown(f"<div class='info-tile'><div class='info-label'>PDS Status</div><div class='info-value' style='color:#002e5d;'>{res.get('PDS_Status', 'N/A')}</div></div>", unsafe_allow_html=True)
            with b3:
                p_status = res.get('PAYMENT STATUS', res.get('Payment Status', 'N/A'))
                p_color = "#22c55e" if "success" in str(p_status).lower() else "#ef4444"
                st.markdown(f"<div class='info-tile'><div class='info-label'>Payment Status</div><div class='info-value' style='color:{p_color}; border-left-color:{p_color};'>{p_status}</div></div>", unsafe_allow_html=True)
                st.markdown(f"<div class='info-tile'><div class='info-label'>Registration Date</div><div class='info-value'>{res.get('Registration Date', 'N/A')}</div></div>", unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.error("❌ यह आधार नंबर हमारे डेटाबेस में उपलब्ध नहीं है। कृपया सही आधार दर्ज करें।")
    else:
        st.error("⚠️ डेटाबेस लोड करने में त्रुटि। कृपया इंटरनेट कनेक्शन जाँचें।")

# 8. Modern Footer
st.write("---")
f1, f2 = st.columns(2)
with f1:
    st.info("💡 **सुझाव:** यदि आपका 'Payment Status' विफल है, तो कृपया बैंक जाकर आधार सीडिंग (NPCI) चेक करवाएं।")
with f2:
    st.markdown("🔗 **उपयोगी लिंक:** [District Chatra](https://chatra.nic.in) | [JMMSY Portal](https://mmmsy.jharkhand.gov.in)")

st.markdown("<br><center style='color:#64748b; font-size:0.8rem;'>© 2026 District Administration Chatra | Powered by National Informatics Centre (NIC)</center>", unsafe_allow_html=True)
