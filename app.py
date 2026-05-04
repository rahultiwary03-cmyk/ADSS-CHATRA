import streamlit as st
import pandas as pd
import time

# 1. Page Config
st.set_page_config(page_title="JMMSY Official Verification Portal", layout="wide", page_icon="🏛️")

# 2. Advanced Professional Styling (Premium Government Look)
st.markdown("""
    <style>
    .stApp { background: #f4f7f9; }
    
    /* Elegant Header */
    .gov-header {
        background: linear-gradient(135deg, #002147 0%, #004080 100%);
        color: white; padding: 40px; text-align: center;
        border-radius: 0 0 40px 40px; box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        margin-bottom: 30px; border-bottom: 5px solid #f9a825;
    }

    /* Professional Card for Details */
    .status-card {
        background: white; padding: 35px; border-radius: 25px;
        box-shadow: 0 15px 45px rgba(0,0,0,0.1); margin-top: 20px;
        border: 1px solid #dee2e6; animation: fadeIn 0.8s ease-in-out;
    }

    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(20px); }
        100% { opacity: 1; transform: translateY(0); }
    }

    /* Text Styling */
    .field-label { color: #6c757d; font-size: 0.8rem; font-weight: 700; text-transform: uppercase; margin-bottom: 2px; }
    .field-value { color: #1a1a1a; font-size: 1.1rem; font-weight: 700; margin-bottom: 18px; border-bottom: 1.5px solid #f1f3f5; padding-bottom: 5px; }
    
    .status-success { color: #28a745; font-weight: 900; background: #e8f5e9; padding: 5px 15px; border-radius: 10px; }
    .status-other { color: #d32f2f; font-weight: 900; background: #ffebee; padding: 5px 15px; border-radius: 10px; }

    /* Search Button */
    .stButton>button {
        background: #002147 !important; color: white !important;
        border-radius: 12px !important; height: 55px !important;
        font-weight: bold !important; width: 100%; transition: 0.3s;
    }
    .stButton>button:hover { background: #f9a825 !important; border-color: #f9a825 !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. Header Section
st.markdown("""
    <div class='gov-header'>
        <h1 style='margin:0;'>झारखण्ड मुख्यमंत्री मईयां सम्मान योजना (JMMSY)</h1>
        <p style='font-size: 1.2rem; opacity: 0.8;'>ज़िला प्रशासन, चतरा - आधिकारिक लाभार्थी डेटा पोर्टल</p>
    </div>
    """, unsafe_allow_html=True)

# 4. Data Loading Logic
sheet_id = "1fApqqsNEulpVsPH7O0IAMRvQv39DMYkV2PB_kg3qntg"
sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

@st.cache_data(ttl=60)
def get_data():
    try:
        df = pd.read_csv(sheet_url)
        df.columns = df.columns.str.strip() # Remove spaces from headers
        return df
    except: return None

df = get_data()

# 5. Search Area
_, mid_col, _ = st.columns([1, 2, 1])
with mid_col:
    st.markdown("<h3 style='text-align: center; color: #002147;'>🔍 आधार नंबर दर्ज करें</h3>", unsafe_allow_html=True)
    input_val = st.text_input("", placeholder="12-digit Aadhaar Number", label_visibility="collapsed")
    search_now = st.button("स्टेटस चेक करें")

# 6. Detailed Logic
if (search_now or input_val) and input_val:
    if df is not None:
        # 12-digit Aadhaar Cleaning
        clean_input = str(input_val).replace(" ", "")
        
        # Finding Aadhaar Column (Checking multiple possible names)
        id_col = next((c for c in ['Aadhaar Number', 'Aadhar Number', 'UID', 'Aadhar'] if c in df.columns), df.columns[0])
        
        # Prepare match key
        df['match_key'] = df[id_col].astype(str).str.replace(" ", "").str.replace(".0", "", regex=False)
        
        match_data = df[df['match_key'] == clean_input].copy()
        
        if not match_data.empty:
            with st.spinner('डेटाबेस से जानकारी मिलान की जा रही है...'):
                time.sleep(0.6)
            
            row = match_data.iloc[0]
            
            # --- Dynamic Column Mapping ---
            # Hum Excel ke har column ko check karke dikhayenge
            name = row.get('ApplicantName', row.get('Name', 'N/A'))
            fname = row.get("Father's/Husband Name", 'N/A')
            dist = row.get('DistrictName', 'CHATRA')
            block = row.get('BlockName', 'N/A')
            panchayat = row.get('PanchayatName', 'N/A')
            village = row.get('VillageName', 'N/A')
            bank = row.get('BankName', 'N/A')
            acc_raw = str(row.get('Account Number', row.get('AccountNo', 'N/A'))).replace('.0', '')
            acc_masked = f"XXXXXX{acc_raw[-4:]}" if len(acc_raw) > 4 else acc_raw
            
            # Asli Payment Status jo Excel mein hai
            pay_status = row.get('Payment Status', row.get('Status', 'Pending'))
            status_style = "status-success" if "success" in str(pay_status).lower() else "status-other"

            # --- Professional Result Display ---
            st.markdown("<div class='status-card'>", unsafe_allow_html=True)
            st.markdown(f"<h2 style='text-align:center; color:#002147; margin-bottom:30px;'>सत्यापित लाभार्थी विवरण</h2>", unsafe_allow_html=True)
            
            c1, c2, c3 = st.columns(3)
            
            with c1:
                st.markdown(f"<div class='field-label'>लाभार्थी का नाम</div><div class='field-value'>{name}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='field-label'>ज़िला</div><div class='field-value'>{dist}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='field-label'>बैंक का नाम</div><div class='field-value'>{bank}</div>", unsafe_allow_html=True)

            with c2:
                st.markdown(f"<div class='field-label'>पिता/पति का नाम</div><div class='field-value'>{fname}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='field-label'>प्रखंड (Block)</div><div class='field-value'>{block}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='field-label'>खाता संख्या</div><div class='field-value'>{acc_masked}</div>", unsafe_allow_html=True)

            with c3:
                st.markdown(f"<div class='field-label'>पंचायत / गांव</div><div class='field-value'>{panchayat} / {village}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='field-label'>आधार संख्या</div><div class='field-value'>XXXX-XXXX-{clean_input[-4:]}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='field-label'>भुगतान स्थिति (As per Sheet)</div><div class='field-value'><span class='{status_style}'>{pay_status}</span></div>", unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.error("❌ रिकॉर्ड नहीं मिला। कृपया आधार नंबर की जांच करें।")
    else:
        st.error("Google Sheet load nahi ho saki. Internet connection ya sheet link check karein.")

# 7. Footer
st.markdown("<br><br><center style='color:#666;'>NIC Jharkhand | District Administration Chatra Official Portal</center>", unsafe_allow_html=True)
