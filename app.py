import streamlit as st
import pandas as pd

# पेज की पूरी सेटिंग
st.set_page_config(page_title="JMMMSY Chatra", layout="wide", page_icon="📝")

# गूगल शीट का CSV लिंक
# ध्यान दें: अपनी शीट के लिंक को 'export?format=csv' के साथ ही इस्तेमाल करें
sheet_url = "https://docs.google.com/spreadsheets/d/15YSpwWFICG6XGXtTRUM6Kn5Cgl6pCfGDL24jWlMb7aI/export?format=csv"

@st.cache_data(ttl=300)
def load_data():
    data = pd.read_csv(sheet_url)
    # कॉलम के नामों से एक्स्ट्रा स्पेस हटाना
    data.columns = [col.strip() for col in data.columns]
    return data

# डेटा लोड करना
try:
    df = load_data()
except Exception as e:
    st.error("डेटा लोड करने में त्रुटि हुई। कृपया लिंक चेक करें।")

# --- कस्टम स्टाइलिंग (UI) ---
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .header-box {
        background-color: #004085;
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin-bottom: 30px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .result-card {
        background-color: white;
        padding: 25px;
        border-radius: 12px;
        border-left: 8px solid #28a745;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-top: 20px;
    }
    .stat-text { font-size: 1.1rem; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- हेडर ---
st.markdown("""
    <div class="header-box">
        <h1 style='margin:0;'>झारखण्ड मुख्यमंत्री मईयां सम्मान योजना (JMMMSY)</h1>
        <p style='font-size:1.3rem; opacity:0.9;'>ज़िला प्रशासन, चतरा - भुगतान स्थिति पोर्टल</p>
    </div>
    """, unsafe_allow_html=True)

# --- मेट्रिक्स ---
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("कुल लाभार्थी", "1,89,174")
with col2:
    st.metric("ज़िला", "चतरा (CHATRA)")
with col3:
    st.metric("पोर्टल स्थिति", "सक्रिय (Live)")

st.write("---")

# --- सर्च सेक्शन ---
st.subheader("🔍 लाभार्थी खोजें (Beneficiary Search)")
aadhar_input = st.text_input("आधार नंबर दर्ज करें (12 अंक):", placeholder="यहाँ अपना आधार नंबर लिखें...", max_chars=12)

if st.button("स्टेटस चेक करें"):
    if aadhar_input:
        with st.spinner('डेटा खोजा जा रहा है...'):
            # आधार कॉलम को स्ट्रिंग में बदलकर मैच करना
            # सुनिश्चित करें कि आपकी शीट में कॉलम का नाम 'Aadhar Number' ही है
            search_col = 'Aadhar Number' 
            
            # डेटा सर्च
            result = df[df[search_col].astype(str).str.contains(aadhar_input, na=False)]

            if not result.empty:
                st.success("विवरण मिल गया!")
                res = result.iloc[0]
                
                # परिणाम कार्ड
                st.markdown(f"""
                    <div class="result-card">
                        <h3 style='color: #004085; margin-top:0;'>लाभार्थी का विवरण</h3>
                        <div style="display: flex; flex-wrap: wrap; gap: 40px;">
                            <div class="stat-text">
                                <b>नाम:</b> {res.get('Beneficiary Name', 'N/A')}<br>
                                <b>पिता/पति का नाम:</b> {res.get("Father's/Husband Name", 'N/A')}<br>
                                <b>श्रेणी (Category):</b> {res.get('Category', 'N/A')}
                            </div>
                            <div class="stat-text">
                                <b>पंचायत:</b> {res.get('Panchayat', 'N/A')}<br>
                                <b>ज़िला:</b> {res.get('District', 'N/A')}<br>
                                <b style='color: #28a745;'>भुगतान की स्थिति:</b> {res.get('Payment Status', 'Record Found')}
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.error("कोई रिकॉर्ड नहीं मिला। कृपया सही आधार नंबर दर्ज करें।")
    else:
        st.warning("कृपया सर्च करने के लिए आधार नंबर दर्ज करें।")

# --- फुटर ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
    <div style='text-align: center; color: gray; font-size: 0.9rem; border-top: 1px solid #ddd; padding-top: 20px;'>
        © 2026 ज़िला प्रशासन चतरा | तकनीकी सेल द्वारा विकसित<br>
        डेटा आधिकारिक रिकॉर्ड के साथ सिंक किया गया है।
    </div>
    """, unsafe_allow_html=True)
