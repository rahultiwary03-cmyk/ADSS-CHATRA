import streamlit as st
import pandas as pd

# 1. Page Configuration & Professional Styling
st.set_page_config(page_title="JMMSY Chatra Portal", layout="wide", page_icon="🏛️")

# Custom CSS for a professional "Dashboard" look
st.markdown("""
    <style>
    /* Background color */
    .stApp {
        background-color: #f4f7f9;
    }
    /* Main Header */
    .main-header {
        background: linear-gradient(90deg, #1c49a6 0%, #2a5fc1 100%);
        color: white;
        padding: 30px;
        text-align: center;
        border-radius: 0px 0px 15px 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        margin-bottom: 25px;
    }
    /* Statistics Card */
    .stat-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        text-align: center;
        border-top: 4px solid #1c49a6;
    }
    /* Data Table Styling */
    .stDataFrame {
        border: 1px solid #e6e9ef;
        border-radius: 10px;
    }
    /* Footer */
    .footer {
        text-align: center;
        color: #888;
        padding: 20px;
        font-size: 12px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Top Banner Header
st.markdown("""
    <div class='main-header'>
        <h1 style='margin:0;'>झारखण्ड मुख्यमंत्री मईयां सम्मान योजना (JMMSY)</h1>
        <p style='font-size:1.2rem; opacity:0.9;'>ज़िला प्रशासन, चतरा - भुगतान स्थिति पोर्टल</p>
    </div>
    """, unsafe_allow_html=True)

# 3. Google Sheet Data Loading Logic
sheet_id = "1fApqqsNEulpVsPH7O0IAMRvQv39DMYkV2PB_kg3qntg"
sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

@st.cache_data(ttl=300)
def load_data():
    try:
        df = pd.read_csv(sheet_url)
        df.columns = df.columns.str.strip() # Headers saaf karne ke liye
        return df
    except Exception as e:
        return None

df = load_data()

# 4. Statistics Row (Professional Cards)
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("<div class='stat-card'><small>कुल लाभार्थी</small><h3>1,89,174</h3></div>", unsafe_allow_html=True)
with c2:
    st.markdown("<div class='stat-card'><small>ज़िला</small><h3>चतरा (CHATRA)</h3></div>", unsafe_allow_html=True)
with c3:
    st.markdown("<div class='stat-card'><small>पोर्टल स्थिति</small><h3 style='color:green;'>● सक्रिय (Live)</h3></div>", unsafe_allow_html=True)

st.write("---")

# 5. Search Section
st.subheader("🔍 लाभार्थी खोजें (Beneficiary Search)")
col_left, col_right = st.columns([2, 1])

with col_left:
    aadhar_input = st.text_input("आधार नंबर दर्ज करें (12 अंक):", placeholder="XXXXXXXX8724")

# Masking Function (Account Number chupane ke liye)
def mask_account(acc_no):
    acc_str = str(acc_no).strip()
    if len(acc_str) > 4:
        return "XXXXXX" + acc_str[-4:]
    return acc_str

# Search Logic
if st.button("स्टेटस चेक करें") or aadhar_input:
    if aadhar_input:
        if df is not None:
            # Column identification (Aadhar search ke liye)
            search_col = 'Aadhar Number' if 'Aadhar Number' in df.columns else df.columns[2] # Fallback to 3rd column
            
            # Cleaning data for search
            df[search_col] = df[search_col].astype(str).str.replace('.0', '', regex=False).str.strip()
            
            result = df[df[search_col] == aadhar_input.strip()].copy()
            
            if not result.empty:
                st.success("✅ Record Mil Gaya!")
                
                # --- ACCOUNT NUMBER MASKING ---
                # Check karein ki aapki sheet mein 'IfscCode' ya 'Account' column kahan hai
                # Maan lete hain column ka naam 'IfscCode' ke paas wala hai ya niche image ke hisab se:
                if 'IfscCode' in result.columns:
                    # Agar account number kisi specific column mein hai (e.g., 'AccountNo')
                    # Yahan main sirf display ke liye result ko modify kar raha hoon
                    for col in result.columns:
                        if 'account' in col.lower() or 'no' in col.lower():
                            result[col] = result[col].apply(mask_account)
                
                # Result ko display karna
                st.dataframe(result, use_container_width=True, hide_index=True)
            else:
                st.error("❌ Maafi chahte hain, ye Aadhaar number record mein nahi mila.")
        else:
            st.error("Data load nahi ho paya. Kripya connection check karein.")
    else:
        st.info("Kripya search karne ke liye Aadhaar number upar box mein likhein.")

# 6. Footer
st.markdown("""
    <div class='footer'>
        <hr>
        © 2024 District Administration, Chatra. Designed for Secure Beneficiary Verification.<br>
        Digital India Initiative | Government of Jharkhand
    </div>
    """, unsafe_allow_html=True)
