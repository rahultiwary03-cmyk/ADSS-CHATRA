import streamlit as st
import pandas as pd
import time

# 1. Page Configuration
st.set_page_config(page_title="JMMSY Payment Portal | Chatra", layout="wide", page_icon="🏛️")

# 2. Modern & Stylish Government Theme CSS
st.markdown("""
    <style>
    /* Background Gradient */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Glossy Header */
    .main-header {
        background: rgba(0, 51, 102, 0.95);
        color: white;
        padding: 40px;
        text-align: center;
        border-radius: 0 0 40px 40px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        margin-bottom: 40px;
        border-bottom: 5px solid #ff9933;
    }

    /* Glassmorphism Effect for Cards */
    .stat-card {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px);
        padding: 25px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.18);
    }

    /* Result Animation & Design */
    .result-card {
        background: white;
        padding: 35px;
        border-radius: 25px;
        box-shadow: 0 20px 50px rgba(0,0,0,0.1);
        margin-top: 30px;
        border-top: 10px solid #003366;
        animation: fadeInScale 0.7s ease-out;
    }

    @keyframes fadeInScale {
        0% { opacity: 0; transform: scale(0.9); }
        100% { opacity: 1; transform: scale(1); }
    }

    .label-box { color: #555; font-size: 0.9rem; font-weight: bold; text-transform: uppercase; letter-spacing: 1px; }
    .value-box { color: #003366; font-size: 1.2rem; font-weight: 800; margin-bottom: 20px; padding: 10px; background: #f8f9fa; border-radius: 10px; }
    
    /* Search Button Style */
    .stButton>button {
        background: linear-gradient(90deg, #003366 0%, #00509d 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 15px !important;
        height: 55px !important;
        font-size: 1.2rem !important;
        font-weight: bold !important;
        transition: all 0.3s ease !important;
    }
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 5px 15px rgba(0,80,157,0.4);
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Official Header
st.markdown("""
    <div class='main-header'>
        <h1 style='margin:0; font-family: "Segoe UI", Arial;'>झारखण्ड मुख्यमंत्री मईयां सम्मान योजना (JMMSY)</h1>
        <p style='font-size: 1.3rem; opacity: 0.9;'>ज़िला प्रशासन, चतरा - डिजिटल भुगतान सत्यापन पोर्टल</p>
    </div>
    """, unsafe_allow_html=True)

# 4. Data Connection
sheet_id = "1fApqqsNEulpVsPH7O0IAMRvQv39DMYkV2PB_kg3qntg"
sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

@st.cache_data(ttl=60)
def load_data():
    try:
        df = pd.read_csv(sheet_url)
        df.columns = df.columns.str.strip()
        return df
    except:
        return None

df = load_data()

# 5. Quick Stats
c1, c2, c3 = st.columns(3)
with c1: st.markdown("<div class='stat-card'><small>Status</small><h3>Active</h3></div>", unsafe_allow_html=True)
with c2: st.markdown("<div class='stat-card'><small>District</small><h3>Chatra</h3></div>", unsafe_allow_html=True)
with c3: st.markdown("<div class='stat-card'><small>Updated</small><h3>Live</h3></div>", unsafe_allow_html=True)

st.write("")

# 6. Search Interface
_, mid, _ = st.columns([1, 2, 1])
with mid:
    st.markdown("<h3 style='text-align: center; color: #003366;'>लाभार्थी की स्थिति खोजें</h3>", unsafe_allow_html=True)
    aadhar_in = st.text_input("Aadhar Number", placeholder="12-digit Aadhaar Number", label_visibility="collapsed")
    search_btn = st.button("स्टेटस चेक करें")

# 7. Logic and Dynamic Result Display
if (search_btn or aadhar_in) and aadhar_in:
    if df is not None:
        # Aadhaar Column identification
        target = 'Aadhaar Number' if 'Aadhaar Number' in df.columns else 'Aadhar Number'
        
        # Space cleanup
        clean_search = str(aadhar_in).replace(" ", "")
        df['key'] = df[target].astype(str).str.replace(" ", "").str.replace(".0", "", regex=False)
        
        match = df[df['key'] == clean_search].copy()
        
        if not match.empty:
            with st.spinner('डेटा प्राप्त किया जा रहा है...'):
                time.sleep(0.5)
            
            res = match.iloc[0]
            
            # --- Dynamic Payment Status ---
            # Hum sheet ke 'Payment Status' ya 'Status' column se data utha rahe hain
            p_status = res.get('Payment Status', res.get('Status', 'N/A'))
            status_color = "#28a745" if "success" in str(p_status).lower() else "#dc3545"

            # Masking Bank Details
            def secure_mask(val):
                v = str(val).replace('.0', '').strip()
                return f"XXXXXX{v[-4:]}" if len(v) > 4 else v

            # Stylish Result UI
            st.markdown("<div class='result-card'>", unsafe_allow_html=True)
            st.markdown(f"<h2 style='text-align:center; color:#003366;'>विवरण मिल गया है</h2>", unsafe_allow_html=True)
            st.write("---")
            
            res_col1, res_col2 = st.columns(2)
            with res_col1:
                st.markdown(f"<div class='label-box'>लाभार्थी का नाम</div><div class='value-box'>{res.get('Name', res.get('ApplicantName', 'N/A'))}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='label-text'>आधार संख्या</div><div class='value-box'>XXXX-XXXX-{clean_search[-4:]}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='label-text'>पिता/पति का नाम</div><div class='value-box'>{res.get('Father\'s/Husband Name', 'N/A')}</div>", unsafe_allow_html=True)

            with res_col2:
                st.markdown(f"<div class='label-box'>बैंक का नाम</div><div class='value-box'>{res.get('BankName', 'N/A')}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='label-box'>खाता संख्या</div><div class='value-box'>{secure_mask(res.get('Account Number', 'N/A'))}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='label-box'>भुगतान की स्थिति</div><div class='value-box' style='color:{status_color}; background:#f0fff4;'>{p_status}</div>", unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.error("❌ रिकॉर्ड नहीं मिला। कृपया आधार नंबर चेक करें।")
    else:
        st.error("डेटाबेस से संपर्क नहीं हो पाया।")

# 8. Professional Footer
st.markdown("""
    <div style='text-align:center; margin-top:80px; color:#666; font-size:0.8rem;'>
        <hr>
        Supported by National Informatics Centre | District Administration, Chatra<br>
        <b>Digital Jharkhand Initiative</b>
    </div>
    """, unsafe_allow_html=True)
