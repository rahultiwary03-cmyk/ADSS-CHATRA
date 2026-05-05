import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(page_title="JMMMSY Chatra Portal", layout="wide", page_icon="📊")

# Google Sheet CSV Link
sheet_url = "https://docs.google.com/spreadsheets/d/15YSpwWFICG6XGXtTRUM6Kn5Cgl6pCfGDL24jWlMb7aI/export?format=csv"

@st.cache_data(ttl=300)
def load_data():
    data = pd.read_csv(sheet_url)
    # सभी कॉलम के नाम से एक्स्ट्रा स्पेस हटाना
    data.columns = [col.strip() for col in data.columns]
    return data

try:
    df = load_data()
except Exception as e:
    st.error("Data load nahi ho pa raha hai.")

# --- Custom CSS ---
st.markdown("""
    <style>
    .main { background: #f8f9fa; }
    .header-container {
        background: linear-gradient(90deg, #073b4c 0%, #118ab2 100%);
        padding: 35px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.15);
    }
    .metric-card {
        padding: 20px; border-radius: 12px; color: white;
        text-align: center; font-weight: bold; box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .total-card { background: #118ab2; }
    .success-card { background: #06d6a0; }
    .failed-card { background: #ef476f; }
    .result-box {
        background-color: white; padding: 25px; border-radius: 15px;
        border: 1.5px solid #118ab2; box-shadow: 0 5px 10px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# --- Header ---
st.markdown("""
    <div class="header-container">
        <h1 style='font-size: 2.8rem; margin-bottom: 5px;'>झारखण्ड मुख्यमंत्री मईयां सम्मान योजना (JMMMSY)</h1>
        <h3 style='font-weight: normal; margin-top: 0; opacity: 0.9;'>सामाजिक सुरक्षा कार्यालय, चतरा</h3>
        <p style='font-size: 1.1rem; margin-top: 5px;'>ज़िला प्रशासन, चतरा - एकीकृत लाभार्थी डैशबोर्ड</p>
    </div>
    """, unsafe_allow_html=True)

# --- Metrics ---
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<div class="metric-card total-card"><h4>कुल लाभार्थी</h4><h2>189,174</h2></div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="metric-card success-card"><h4>सफल भुगतान</h4><h2>145,230</h2></div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="metric-card failed-card"><h4>विफल (Failed)</h4><h2>12,450</h2></div>', unsafe_allow_html=True)

st.write("---")

# --- Search Section ---
st.markdown("<h2 style='color: #073b4c;'>🔍 लाभार्थी की स्थिति जांचें</h2>", unsafe_allow_html=True)
aadhar_input = st.text_input("अपना 12 अंकों का आधार नंबर दर्ज करें:", placeholder="यहाँ आधार नंबर लिखें...", max_chars=12)
