import streamlit as st
import pandas as pd
import time

# 1. Page Config
st.set_page_config(page_title="JMMSY Official Portal", layout="wide", page_icon="🏛️")

# 2. Stylish CSS for Deep Blue Theme & Result Cards
st.markdown("""
    <style>
    .stApp {
        background: #f0f4f8;
    }
    /* Header Section */
    .gov-header {
        background: linear-gradient(135deg, #002147 0%, #004080 100%);
        color: white;
        padding: 45px;
        text-align: center;
        border-radius: 0 0 50px 50px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.2);
        margin-bottom: 40px;
        border-bottom: 6px solid #f9a825;
    }
    /* Stat Cards */
    .dashboard-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        border-top: 5px solid #002147;
    }
    /* Result Detail Card */
    .detail-container {
        background: white;
        padding: 40px;
        border-radius: 30px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.1);
        margin-top: 20px;
        border: 1px solid #e1e8ed;
        animation: fadeIn 0.8s ease-in-out;
    }
    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(30px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    .info-label { color: #607d8b; font-size: 0.85rem; font-weight: 700; text-transform: uppercase; margin-bottom: 4px; }
    .info-value { color: #263238; font-size: 1.1rem; font-weight: 700; margin-bottom: 20px; border-left: 4px solid #002147; padding-left: 10px; background: #f9fbe7; border-radius: 0 8px 8px 0; padding-top: 5px; padding-bottom: 5px;}
    
    /* Search Button */
    .stButton>button {
        background: #002147 !important;
        color: white !important;
        border-radius: 12px !important;
        height: 55px !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
        width: 100%;
        transition: 0.4s;
    }
    .stButton>button:hover {
        background: #f9a825 !important;
        box-shadow: 0 8px 20px rgba(0,0,0,0.2);
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Header
st.markdown("""
    <div class='gov-header'>
        <h1 style='margin:0; font-family: sans-serif; letter-spacing: 1px;'>झारखण्ड मुख्यमंत्री मईयां सम्मान योजना (JMMSY)</h1>
        <p style='font-size: 1.3rem; opacity: 0.8;'>ज़िला प्रशासन, चतरा - संपूर्ण लाभार्थी विवरण पोर्टल</p>
    </div>
    """, unsafe_allow_html=True)

# 4. Data Loading
sheet_id = "1fApqqsNEulpVsPH7O0IAMRvQv39DMYkV2PB_kg3qntg"
sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

@st.cache_data(ttl=60)
def fetch_data():
    try:
        df = pd.read_csv(sheet_url)
        df.columns = df.columns.str.strip() # Spaces hatane ke liye
        return df
    except:
        return None

df = fetch_data()

# 5. Top Stats Row
s1, s2, s3, s4 = st.columns(4)
with s1: st.markdown("<div class='dashboard-card'><small>Status</small><h3>Active</h3></div>", unsafe_allow_html=True)
with s2: st.markdown("<div class='dashboard-card'><small>District</small><h3>Chatra</h3></div>", unsafe_allow_html=True)
with s3: st.markdown("<div class='dashboard-card'><small>Category</small><h3>WCD</h3></div>", unsafe_allow_html=True)
with s4: st.markdown("<div class='dashboard-card'><small>Portal</small><h3>Official</h3></div>", unsafe_allow_html=True)

st.write("")

# 6. Search Section
_, search_area, _ = st.columns([1, 2, 1])
with search_area:
    st.markdown("<h3 style='text-align: center; color: #002147;'>🔍 आधार नंबर से विवरण खोजें</h3>", unsafe_allow_html=True)
    user_input = st.text_input("Aadhar", placeholder="Enter 12 digit Aadhaar Number", label_visibility="collapsed")
    clicked = st.button("स्टेटस चेक करें")

# 7. Comprehensive Search & Result Logic
if (clicked or user_input) and user_input:
    if df is not None:
        # Aadhaar Column check
        possible_cols = ['Aadhaar Number', 'Aadhar Number', 'UID', 'Aadhar']
        target_col = next((c for c in possible_cols if c in df.columns), df.columns[0])
        
        # Cleanup
        clean_input = str(user_input).replace(" ", "")
        df['temp_key'] = df[target_col].astype(str).str.replace(" ", "").str.replace(".0", "", regex=False)
        
        match = df[df['temp_key'] == clean_input].copy()
        
        if not match.empty:
            with st.spinner('डेटाबेस से जानकारी निकाली जा रही है...'):
                time.sleep(0.6)
            
            data = match.iloc[0]
            
            # Masking Function
            def mask(val):
                v = str(val).replace('.0', '').strip()
                return f"XXXXXX{v[-4:]}" if len(v) > 4 else v

            # Displaying Result in Professional Card
            st.markdown("<div class='detail-container'>", unsafe_allow_html=True)
            st.markdown("<h2 style='text-align:center; color:#002147; border-bottom: 2px solid #eee; padding-bottom:15px;'>✅ लाभार्थी सत्यापन विवरण</h2>", unsafe_allow_html=True)
            
            # 3-Column Detail Layout
            col_a, col_b, col_c = st.columns(3)
            
            with col_a:
                st.markdown(f"<div class='info-label'>लाभार्थी का नाम</div><div class='info-value'>{data.get('ApplicantName', data.get('Name', 'N/A'))}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='info-label'>ज़िला</div><div class='info-value'>{data.get('DistrictName', 'CHATRA')}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='info-label'>प्रखंड (Block)</div><div class='info-value'>{data.get('BlockName', 'N/A')}</div>", unsafe_allow_html=True)

            with col_b:
                st.markdown(f"<div class='info-label'>पिता/पति का नाम</div><div class='info-value'>{data.get('Father\'s/Husband Name', 'N/A')}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='info-label'>पंचायत</div><div class='info-value'>{data.get('PanchayatName', 'N/A')}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='info-label'>गांव</div><div class='info-value'>{data.get('VillageName', 'N/A')}</div>", unsafe_allow_html=True)

            with col_c:
                # DYNAMIC PAYMENT STATUS FROM SHEET
                raw_status = data.get('Payment Status', data.get('Status', 'Pending'))
                status_clr = "#2e7d32" if "success" in str(raw_status).lower() else "#d32f2f"
                
                st.markdown(f"<div class='info-label'>बैंक का नाम</div><div class='info-value'>{data.get('BankName', 'N/A')}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='info-label'>खाता संख्या</div><div class='info-value'>{mask(data.get('Account Number', 'N/A'))}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='info-label'>भुगतान की स्थिति</div><div class='info-value' style='color:{status_clr}; border-left: 4px solid {status_clr};'>{raw_status}</div>", unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.error("❌ क्षमा करें! यह आधार नंबर रिकॉर्ड में नहीं मिला।")
    else:
        st.error("Google Sheet load nahi ho saki. Permissions check karein.")

# 8. Official Footer
st.markdown("""
    <div style='text-align:center; margin-top:80px; color:#546e7a; border-top: 1px solid #cfd8dc; padding-top:20px;'>
        NIC Jharkhand द्वारा विकसित | ज़िला प्रशासन चतरा <br>
        <b>मुख्यमंत्री मईयां सम्मान योजना - आधिकारिक सूचना पोर्टल</b>
    </div>
    """, unsafe_allow_html=True)
