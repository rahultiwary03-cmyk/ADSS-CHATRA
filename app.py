import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(page_title="JMMMSY Chatra Portal", layout="wide")

# Google Sheet CSV Link
sheet_url = "https://docs.google.com/spreadsheets/d/15YSpwWFICG6XGXtTRUM6Kn5Cgl6pCfGDL24jWlMb7aI/export?format=csv"

@st.cache_data(ttl=60)
def load_data():
    try:
        data = pd.read_csv(sheet_url)
        data.columns = [str(col).strip() for col in data.columns]
        return data
    except Exception as e:
        st.error(f"डेटा लोड एरर: {e}")
        return None

df = load_data()

# --- Custom Styling ---
st.markdown("""
    <style>
    .header-container { background: linear-gradient(90deg, #073b4c 0%, #118ab2 100%); padding: 30px; border-radius: 15px; color: white; text-align: center; margin-bottom: 20px; }
    .metric-card { padding: 15px; border-radius: 12px; color: white; text-align: center; font-weight: bold; }
    .total-card { background: #118ab2; }
    .success-card { background: #06d6a0; }
    .failed-card { background: #ef476f; }
    .result-box { background-color: white; padding: 25px; border-radius: 15px; border: 2px solid #118ab2; margin-top: 20px; }
    </style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("""
    <div class="header-container">
        <h1 style='margin-bottom:0;'>झारखण्ड मुख्यमंत्री मईयां सम्मान योजना (JMMMSY)</h1>
        <h3 style='margin-top:0;'>सामाजिक सुरक्षा कार्यालय, चतरा</h3>
        <p>ज़िला प्रशासन, चतरा - एकीकृत लाभार्थी डैशबोर्ड</p>
    </div>
""", unsafe_allow_html=True)

# --- Metrics ---
c1, c2, c3 = st.columns(3)
c1.markdown('<div class="metric-card total-card"><h4>कुल लाभार्थी</h4><h2>189,174</h2></div>', unsafe_allow_html=True)
c2.markdown('<div class="metric-card success-card"><h4>सफल भुगतान</h4><h2>145,230</h2></div>', unsafe_allow_html=True)
c3.markdown('<div class="metric-card failed-card"><h4>विफल (Failed)</h4><h2>12,450</h2></div>', unsafe_allow_html=True)

st.divider()

# --- Search Section ---
st.subheader("🔍 लाभार्थी की स्थिति जांचें")
aadhar_input = st.text_input("अपना 12 अंकों का आधार नंबर दर्ज करें:", max_chars=12).strip()

if st.button("विवरण देखें (View Details)"):
    if aadhar_input and df is not None:
        with st.spinner('खोज जारी है...'):
            # सुधार: 'Aadhar' शब्द वाले किसी भी कॉलम को ढूंढना
            target_col = None
            for col in df.columns:
                if 'aadhar' in col.lower() or 'adhar' in col.lower():
                    target_col = col
                    break
            
            if target_col:
                # डेटा को स्ट्रिंग में बदलकर मैच करना
                df[target_col] = df[target_col].astype(str).str.replace('.0', '', regex=False).str.strip()
                match = df[df[target_col] == aadhar_input]

                if not match.empty:
                    res = match.iloc[0]
                    st.success("विवरण मिल गया!")
                    st.markdown(f"""
                        <div class="result-box">
                            <div style="display: flex; gap: 30px; flex-wrap: wrap;">
                                <div style="flex: 1;">
                                    <p style="color: gray; margin-bottom: 0;">लाभार्थी का नाम</p>
                                    <h3 style="color: #073b4c; margin-top: 0;">{res.get('Beneficiary Name', 'N/A')}</h3>
                                    <p style="color: gray; margin-bottom: 0;">पिता/पति का नाम</p>
                                    <h3 style="color: #073b4c; margin-top: 0;">{res.get("Father's/Husband Name", 'N/A')}</h3>
                                </div>
                                <div style="flex: 1;">
                                    <p style="color: gray; margin-bottom: 0;">पंचायत / ब्लॉक</p>
                                    <h3 style="color: #073b4c; margin-top: 0;">{res.get('Panchayat', 'N/A')}</h3>
                                    <p style="color: gray; margin-bottom: 0;">वर्तमान स्थिति</p>
                                    <h2 style="color: #06d6a0;">{res.get('Payment Status', 'Record Found')}</h2>
                                </div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error(f"आधार नंबर {aadhar_input} के लिए कोई रिकॉर्ड नहीं मिला।")
            else:
                # अगर कॉलम नहीं मिला, तो सारे कॉलम के नाम दिखा दें ताकि यूजर को पता चले गलती कहाँ है
                st.error(f"शीट में आधार कॉलम नहीं मिला। उपलब्ध कॉलम: {list(df.columns)}")
    else:
        st.warning("कृपया 12 अंकों का आधार नंबर दर्ज करें।")
