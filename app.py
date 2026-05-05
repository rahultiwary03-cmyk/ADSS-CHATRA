import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(page_title="JMMMSY Chatra Portal", layout="wide", page_icon="📊")

# Google Sheet CSV Link
sheet_url = "https://docs.google.com/spreadsheets/d/15YSpwWFICG6XGXtTRUM6Kn5Cgl6pCfGDL24jWlMb7aI/export?format=csv"

@st.cache_data(ttl=300)
def load_data():
    data = pd.read_csv(sheet_url)
    data.columns = [col.strip() for col in data.columns]
    return data

try:
    df = load_data()
except Exception as e:
    st.error("Data load nahi ho pa raha hai.")

# --- Custom Colorful CSS ---
st.markdown("""
    <style>
    .main { background: linear-gradient(to bottom, #e3f2fd, #ffffff); }
    .header-container {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        padding: 40px;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
    }
    /* Metric Cards Styling */
    .metric-card {
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        font-weight: bold;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .total-card { background: linear-gradient(45deg, #2196F3, #00BCD4); }
    .success-card { background: linear-gradient(45deg, #4CAF50, #8BC34A); }
    .failed-card { background: linear-gradient(45deg, #F44336, #E91E63); }
    .pending-card { background: linear-gradient(45deg, #FF9800, #FFC107); }
    
    /* Result Box */
    .result-box {
        background-color: #ffffff;
        padding: 30px;
        border-radius: 20px;
        border: 2px solid #2a5298;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# --- Header Section ---
st.markdown("""
    <div class="header-container">
        <h1 style='font-size: 3rem; margin-bottom: 0;'>झारखण्ड मुख्यमंत्री मईयां सम्मान योजना (JMMMSY)</h1>
        <h3 style='font-weight: normal; opacity: 0.9;'>ज़िला प्रशासन, चतरा - एकीकृत लाभार्थी डैशबोर्ड</h3>
    </div>
    """, unsafe_allow_html=True)

# --- Colorful Metrics Dashboard ---
# Note: In numbers ko aap apne logic se calculate kar sakte hain: df[df['Status'] == 'Success'].count()
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<div class="metric-card total-card"><h4>कुल लाभार्थी</h4><h2>189,174</h2></div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="metric-card success-card"><h4>सफल भुगतान</h4><h2>145,230</h2></div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="metric-card failed-card"><h4>विफल (Failed)</h4><h2>12,450</h2></div>', unsafe_allow_html=True)
with col4:
    st.markdown('<div class="metric-card pending-card"><h4>लंबित (Pending)</h4><h2>31,494</h2></div>', unsafe_allow_html=True)

st.write("---")

# --- Search Section ---
st.markdown("<h2 style='color: #1e3c72;'>🔍 लाभार्थी की स्थिति जांचें</h2>", unsafe_allow_html=True)
aadhar_input = st.text_input("अपना 12 अंकों का आधार नंबर दर्ज करें:", placeholder="98XXXXXXXXXX", max_chars=12)

if st.button("विवरण देखें (View Details)"):
    if aadhar_input:
        with st.spinner('डेटा खोजा जा रहा है...'):
            # Sheet ke column names ke anusar filter (Aadhar Number)
            result = df[df['Aadhar Number'].astype(str).str.contains(aadhar_input, na=False)]

            if not result.empty:
                res = result.iloc[0]
                status = res.get('Payment Status', 'N/A')
                
                # Status ke hisaab se color chunna
                status_color = "#4CAF50" if "Success" in status else "#F44336" if "Fail" in status else "#FF9800"
                status_hindi = "सफल भुगतान" if "Success" in status else "भुगतान विफल" if "Fail" in status else "भुगतान लंबित"

                st.markdown(f"""
                    <div class="result-box">
                        <div style="display: flex; justify-content:建设; gap: 50px; flex-wrap: wrap;">
                            <div style="flex: 1; min-width: 250px;">
                                <p style="color: gray; margin-bottom: 0;">लाभार्थी का नाम</p>
                                <h3 style="color: #1e3c72; margin-top: 0;">{res.get('Beneficiary Name', 'N/A')}</h3>
                                
                                <p style="color: gray; margin-bottom: 0;">पिता/पति का नाम</p>
                                <h3 style="color: #1e3c72; margin-top: 0;">{res.get("Father's/Husband Name", 'N/A')}</h3>
                            </div>
                            <div style="flex: 1; min-width: 250px;">
                                <p style="color: gray; margin-bottom: 0;">पंचायत / ब्लॉक</p>
                                <h3 style="color: #1e3c72; margin-top: 0;">{res.get('Panchayat', 'N/A')}</h3>
                                
                                <p style="color: gray; margin-bottom: 0;">वर्तमान स्थिति</p>
                                <h2 style="color: {status_color}; margin-top: 0;">{status_hindi}</h2>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.error("कोई रिकॉर्ड नहीं मिला। कृपया आधार नंबर फिर से जांचें।")
    else:
        st.warning("कृपया आधार नंबर दर्ज करें।")

# --- Footer ---
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown("""
    <div style='text-align: center; background-color: #f8f9fa; padding: 20px; border-radius: 10px;'>
        <p style='color: #666;'>💡 नोट: यह डेटा सीधे आधिकारिक एक्सेल शीट से रियल-टाइम में सिंक किया जा रहा है।</p>
        <p style='font-weight: bold; color: #1e3c72;'>© 2026 ज़िला प्रशासन चतरा | Technical Cell</p>
    </div>
    """, unsafe_allow_html=True)
