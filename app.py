import streamlit as st
import pandas as pd

# 1. Page Configuration & Styling
st.set_page_config(page_title="JMMSY Chatra Portal", layout="wide", page_icon="🏛️")

st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .main-header {
        background: linear-gradient(90deg, #074799 0%, #001A6E 100%);
        color: white; padding: 25px; text-align: center;
        border-radius: 0 0 20px 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        margin-bottom: 30px;
    }
    .stat-box {
        background: white; padding: 20px; border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08); text-align: center;
        border-bottom: 5px solid #074799;
    }
    .result-card {
        background: white; padding: 20px; border-radius: 10px;
        border-left: 5px solid #28a745; margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Header
st.markdown("""
    <div class='main-header'>
        <h1 style='margin:0; font-family: sans-serif;'>झारखण्ड मुख्यमंत्री मईयां सम्मान योजना (JMMSY)</h1>
        <p style='font-size:1.1rem; opacity:0.8;'>ज़िला प्रशासन, चतरा - भुगतान स्थिति खोजें</p>
    </div>
    """, unsafe_allow_html=True)

# 3. Data Loading (Direct from Google Sheet)
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

# 4. Dashboard Stats
c1, c2, c3 = st.columns(3)
with c1: st.markdown("<div class='stat-box'><small>कुल लाभार्थी</small><h2>1,89,174</h2></div>", unsafe_allow_html=True)
with c2: st.markdown("<div class='stat-box'><small>ज़िला</small><h2>चतरा (CHATRA)</h2></div>", unsafe_allow_html=True)
with c3: st.markdown("<div class='stat-box'><small>पोर्टल स्थिति</small><h2 style='color:green;'>● LIVE</h2></div>", unsafe_allow_html=True)

st.write("")

# 5. Search Interface
st.subheader("🔍 लाभार्थी की स्थिति जांचें")
search_input = st.text_input("आधार नंबर दर्ज करें:", placeholder="12 अंकों का आधार नंबर लिखें...")

# Account Number Masking Function
def mask_acc(val):
    s = str(val).strip().replace('.0', '')
    return f"XXXXXX{s[-4:]}" if len(s) > 4 else s

if st.button("स्टेटas चेक करें") or search_input:
    if search_input and df is not None:
        # Aadhaar Column ki pehchaan (Sheet ke hisab se 'Aadhaar Number' ya 'Aadhar Number')
        col_name = 'Aadhaar Number' if 'Aadhaar Number' in df.columns else 'Aadhar Number'
        
        if col_name in df.columns:
            # --- CRITICAL FIX FOR SPACES ---
            # Input se space hatayein
            clean_input = str(search_input).replace(" ", "")
            
            # Dataframe ke column se bhi temporary space hatakar match karein
            # Hum ek temporary column banayenge matching ke liye
            df['match_key'] = df[col_name].astype(str).str.replace(" ", "").str.replace(".0", "", regex=False)
            
            result = df[df['match_key'] == clean_input].copy()
            
            if not result.empty:
                st.markdown("<div class='result-card'>", unsafe_allow_html=True)
                st.success("✅ लाभार्थी का विवरण मिल गया है")
                
                # Masking columns (Bank A/c details)
                # Agar column ka naam BankName ya Account hai toh mask karein
                for col in result.columns:
                    if 'account' in col.lower() or 'no' in col.lower():
                        if col != 'match_key' and col != col_name:
                             result[col] = result[col].apply(mask_acc)
                
                # Cleanup and Display
                final_display = result.drop(columns=['match_key'])
                st.dataframe(final_display, use_container_width=True, hide_index=True)
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.error("❌ यह आधार नंबर डेटाबेस में नहीं मिला। कृपया नंबर जांचें।")
        else:
            st.error("Sheet Error: Aadhaar column nahi mila.")
    elif df is None:
        st.error("Google Sheet se sampark nahi ho pa raha hai.")

st.markdown("<br><hr><center style='color:grey;'>Digital India Initiative | District Administration Chatra</center>", unsafe_allow_html=True)
