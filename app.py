import streamlit as st
import pandas as pd
import time

# 1. Page Configuration
st.set_page_config(page_title="JMMSY | Official Portal", layout="wide", page_icon="🏛️")

# 2. Custom Professional CSS (Official Government UI)
st.markdown("""
    <style>
    .stApp { background-color: #f4f7f9; }
    
    /* Header Banner */
    .gov-header {
        background: linear-gradient(135deg, #002e5d 0%, #004a99 100%);
        color: white;
        padding: 40px;
        text-align: center;
        border-radius: 0 0 30px 30px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        margin-bottom: 30px;
        border-bottom: 5px solid #ff9933;
    }
    
    /* Result Container */
    .status-card {
        background: white;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.08);
        border: 1px solid #e1e4e8;
        margin-top: 20px;
        animation: fadeIn 0.6s ease-in-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Labels and Values */
    .detail-label { color: #6c757d; font-size: 0.8rem; font-weight: 700; text-transform: uppercase; margin-bottom: 3px; }
    .detail-value { color: #1a1a1a; font-size: 1.1rem; font-weight: 700; margin-bottom: 15px; background: #f8f9fa; padding: 10px; border-radius: 8px; border-left: 5px solid #002e5d; }
    
    /* Search Button */
    .stButton>button {
        background: #002e5d !important;
        color: white !important;
        border-radius: 10px !important;
        height: 50px !important;
        width: 100%;
        font-weight: bold !important;
        transition: 0.3s;
    }
    .stButton>button:hover { background: #ff9933 !important; box-shadow: 0 5px 15px rgba(0,0,0,0.2); }
    </style>
    """, unsafe_allow_html=True)

# 3. Official Header
st.markdown("""
    <div class='gov-header'>
        <h1 style='margin:0;'>झारखण्ड मुख्यमंत्री मईयां सम्मान योजना (JMMSY)</h1>
        <p style='font-size: 1.2rem; opacity: 0.9;'>ज़िला प्रशासन, चतरा - आधिकारिक लाभार्थी सत्यापन पोर्टल</p>
    </div>
    """, unsafe_allow_html=True)

# 4. Data Loading Logic
SHEET_URL = "https://docs.google.com/spreadsheets/d/1fApqqsNEulpVsPH7O0IAMRvQv39DMYkV2PB_kg3qntg/export?format=csv"

@st.cache_data(ttl=60)
def load_official_data():
    try:
        df = pd.read_csv(SHEET_URL)
        df.columns = df.columns.str.strip() # Clear extra spaces from headers
        return df
    except:
        return None

df = load_official_data()

# 5. Search Area
_, mid_col, _ = st.columns([1, 2, 1])
with mid_col:
    st.markdown("<h3 style='text-align: center; color: #002e5d;'>🔍 आधार नंबर दर्ज करें</h3>", unsafe_allow_html=True)
    user_input = st.text_input("Aadhar", placeholder="12 Digit Aadhaar Number", label_visibility="collapsed")
    search_btn = st.button("स्टेटस चेक करें")

# 6. Result Processing Logic
if (search_btn or user_input) and user_input:
    if df is not None:
        # User input cleanup
        clean_aadhar = str(user_input).replace(" ", "")
        
        # Exact Column from Sheet (Aadhaar Number is usually Col E)
        search_col = 'Aadhaar Number' if 'Aadhaar Number' in df.columns else df.columns[4]
        
        # Handle decimal/space in sheet
        df['temp_key'] = df[search_col].astype(str).str.replace(" ", "").str.replace(".0", "", regex=False)
        
        match = df[df['temp_key'] == clean_aadhar].copy()
        
        if not match.empty:
            with st.spinner('सत्यापन किया जा रहा है...'):
                time.sleep(0.5)
            
            res = match.iloc[0]
            
            # --- Result Card ---
            st.markdown("<div class='status-card'>", unsafe_allow_html=True)
            st.markdown(f"<h2 style='text-align:center; color:#002e5d; margin-bottom:30px;'>✅ सत्यापित लाभार्थी विवरण</h2>", unsafe_allow_html=True)
            
            c1, c2, c3 = st.columns(3)
            
            with c1:
                st.markdown(f"<div class='detail-label'>लाभार्थी का नाम</div><div class='detail-value'>{res.get('Applicant', 'N/A')}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='detail-label'>ज़िला</div><div class='detail-value'>{res.get('District', 'Chatra')}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='detail-label'>प्रखंड (Block)</div><div class='detail-value'>{res.get('Block', 'N/A')}</div>", unsafe_allow_html=True)

            with c2:
                # Use \ for escaping apostrophe in Father's/Husband Name
                f_name = res.get("Father's/Husband Name", 'N/A')
                st.markdown(f"<div class='detail-label'>पिता/पति का नाम</div><div class='detail-value'>{f_name}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='detail-label'>पंचायत / गांव</div><div class='detail-value'>{res.get('Panchayat', 'N/A')} / {res.get('Village', 'N/A')}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='detail-label'>बैंक का नाम</div><div class='detail-value'>{res.get('BankName', 'N/A')}</div>", unsafe_allow_html=True)

            with c3:
                acc_raw = str(res.get('Account Number', 'N/A')).replace('.0', '').strip()
                pds_status = res.get('PDS_Status', 'N/A')
                pay_status = res.get('PAYMENT STATUS', res.get('Payment Status', 'N/A'))
                
                # Dynamic Color
                pay_color = "#28a745" if "success" in str(pay_status).lower() or "paid" in str(pay_status).lower() else "#d32f2f"
                
                st.markdown(f"<div class='detail-label'>खाता संख्या</div><div class='detail-value'>XXXXXX{acc_raw[-4:] if len(acc_raw)>4 else acc_raw}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='detail-label'>PDS STATUS</div><div class='detail-value' style='color:#002e5d;'>{pds_status}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='detail-label'>PAYMENT STATUS</div><div class='detail-value' style='color:{pay_color}; border-left:5px solid {pay_color};'>{pay_status}</div>", unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.error("❌ आधार नंबर रिकॉर्ड में नहीं मिला।")
    else:
        st.error("डेटाबेस लोड नहीं हो सका।")

# 7. Footer
st.markdown("<br><br><center style='color:#777;'>NIC Jharkhand | District Administration Chatra Official Portal</center>", unsafe_allow_html=True)
