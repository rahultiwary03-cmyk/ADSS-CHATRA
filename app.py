import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(page_title="JMMMSY Chatra Portal", layout="wide", page_icon="📊")

# Google Sheet CSV Link
sheet_url = "https://docs.google.com/spreadsheets/d/15YSpwWFICG6XGXtTRUM6Kn5Cgl6pCfGDL24jWlMb7aI/export?format=csv"

@st.cache_data(ttl=60) # TTL को कम किया ताकि अपडेट जल्दी दिखे
def load_data():
    try:
        data = pd.read_csv(sheet_url)
        data.columns = [col.strip() for col in data.columns] # कॉलम क्लीनिंग
        return data
    except Exception as e:
        st.error(f"Data लोड नहीं हो रहा: {e}")
        return None

df = load_data()

# --- Custom CSS ---
st.markdown("""
    <style>
    .main { background: #f8f9fa; }
    .header-container {
        background: linear-gradient(90deg, #073b4c 0%, #118ab2 100%);
        padding: 35px; border-radius: 15px; color: white; text-align: center; margin-bottom: 25px;
    }
    .metric-card { padding: 20px; border-radius: 12px; color: white; text-align: center; font-weight: bold; }
    .total-card { background: #118ab2; }
    .success-card { background: #06d6a0; }
    .failed-card { background: #ef476f; }
    .result-box { background-color: white; padding: 25px; border-radius: 15px; border: 2px solid #118ab2; }
    </style>
    """, unsafe_allow_html=True)

# --- Header ---
st.markdown("""
    <div class="header-container">
        <h1 style='font-size: 2.5rem; margin-bottom: 5px;'>झारखण्ड मुख्यमंत्री मईयां सम्मान योजना (JMMMSY)</h1>
        <h3 style='margin-top: 0;'>सामाजिक सुरक्षा कार्यालय, चतरा</h3>
        <p>ज़िला प्रशासन, चतरा - एकीकृत लाभार्थी डैशबोर्ड</p>
    </div>
    """, unsafe_allow_html=True)

# --- Metrics ---
col1, col2, col3 = st.columns(3)
with col1: st.markdown('<div class="metric-card total-card"><h4>कुल लाभार्थी</h4><h2>189,174</h2></div>', unsafe_allow_html=True)
with col2: st.markdown('<div class="metric-card success-card"><h4>सफल भुगतान</h4><h2>145,230</h2></div>', unsafe_allow_html=True)
with col3: st.markdown('<div class="metric-card failed-card"><h4>विफल (Failed)</h4><h2>12,450</h2></div>', unsafe_allow_html=True)

st.write("---")

# --- Improved Search Section ---
st.markdown("<h2 style='color: #073b4c;'>🔍 लाभार्थी की स्थिति जांचें</h2>", unsafe_allow_html=True)
aadhar_input = st.text_input("अपना 12 अंकों का आधार नंबर दर्ज करें:", placeholder="यहाँ लिखें...", max_chars=12).strip()

if st.button("विवरण देखें (View Details)"):
    if aadhar_input and df is not None:
        with st.spinner('खोज जारी है...'):
            # सही आधार कॉलम ढूंढना
            aadhar_col = next((col for col in df.columns if 'aadhar' in col.lower()), None)
            
            if aadhar_col:
                # सर्च को मजबूत बनाना: दोनों तरफ से स्ट्रिंग में बदल कर और स्पेस हटाकर मैच करना
                df[aadhar_col] = df[aadhar_col].astype(str).str.strip()
                result = df[df[aadhar_col] == aadhar_input]

                if not result.empty:
                    res = result.iloc[0]
                    status = str(res.get('Payment Status', 'Record Found'))
                    color = "#06d6a0" if "success" in status.lower() else "#ef476f"
                    
                    st.markdown(f"""
                        <div class="result-box">
                            <div style="display: flex; gap: 40px; flex-wrap: wrap;">
                                <div style="flex: 1;">
                                    <p style="color: gray; margin-bottom: 2px;">लाभार्थी का नाम</p>
                                    <h3 style="color: #073b4c; margin-top: 0;">{res.get('Beneficiary Name', 'N/A')}</h3>
                                    <p style="color: gray; margin-bottom: 2px;">पिता/पति का नाम</p>
                                    <h3 style="color: #073b4c; margin-top: 0;">{res.get("Father's/Husband Name", 'N/A')}</h3>
                                </div>
                                <div style="flex: 1;">
                                    <p style="color: gray; margin-bottom: 2px;">पंचायत / ब्लॉक</p>
                                    <h3 style="color: #073b4c; margin-top: 0;">{res.get('Panchayat', 'N/A')}</h3>
                                    <p style="color: gray; margin-bottom: 2px;">वर्तमान स्थिति</p>
                                    <h2 style="color: {color}; margin-top: 0;">{status}</h2>
                                </div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error(f"आधार नंबर {aadhar_input} के लिए कोई रिकॉर्ड नहीं मिला।")
            else:
                st.error("Sheet में आधार कॉलम नहीं मिला।")
    else:
        st.warning("कृपया आधार नंबर दर्ज करें।")

# Footer
st.markdown("<br><div style='text-align: center; color: #666; border-top: 1px solid #ddd; padding-top: 20px;'><p>© 2026 <b>सामाजिक सुरक्षा कार्यालय, चतरा</b></p></div>", unsafe_allow_html=True)
