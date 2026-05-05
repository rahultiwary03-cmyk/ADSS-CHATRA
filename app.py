import streamlit as st
import pandas as pd

# 1. पेज कॉन्फ़िगरेशन
st.set_page_config(page_title="JMMMSY Chatra Portal", layout="wide", page_icon="📊")

# 2. गूगल शीट का लिंक (CSV फॉर्मेट)
sheet_url = "https://docs.google.com/spreadsheets/d/15YSpwWFICG6XGXtTRUM6Kn5Cgl6pCfGDL24jWlMb7aI/export?format=csv"

@st.cache_data(ttl=60)
def load_data():
    try:
        data = pd.read_csv(sheet_url)
        # कॉलम के नामों से एक्स्ट्रा स्पेस हटाना ताकि KeyError न आए
        data.columns = [str(col).strip() for col in data.columns]
        return data
    except Exception as e:
        st.error(f"डेटा लोड करने में समस्या: {e}")
        return None

df = load_data()

# 3. प्रोफेशनल लुक के लिए CSS
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .header-box {
        background: linear-gradient(90deg, #073b4c 0%, #118ab2 100%);
        padding: 40px; border-radius: 20px; color: white; text-align: center;
        margin-bottom: 30px; box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }
    .metric-card {
        padding: 20px; border-radius: 15px; color: white; text-align: center;
        font-weight: bold; box-shadow: 0 4px 8px rgba(0,0,0,0.1); margin-bottom: 15px;
    }
    .result-card {
        background-color: #ffffff; padding: 30px; border-radius: 20px;
        border-left: 12px solid #118ab2; box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# 4. हेडर सेक्शन
st.markdown("""
    <div class="header-box">
        <h1 style='font-size: 2.5rem; margin-bottom: 5px;'>झारखण्ड मुख्यमंत्री मईयां सम्मान योजना (JMMMSY)</h1>
        <h2 style='font-weight: normal; margin-top: 0; opacity: 0.9;'>सामाजिक सुरक्षा कार्यालय, चतरा</h2>
        <p style='font-size: 1.1rem;'>ज़िला प्रशासन, चतरा - भुगतान स्थिति पोर्टल</p>
    </div>
""", unsafe_allow_html=True)

# 5. डैशबोर्ड मेट्रिक्स (Colorful Cards)
col1, col2, col3, col4 = st.columns(4)
with col1: st.markdown('<div class="metric-card" style="background:#118ab2;"><h4>कुल लाभार्थी</h4><h2>189,174</h2></div>', unsafe_allow_html=True)
with col2: st.markdown('<div class="metric-card" style="background:#06d6a0;"><h4>सफल भुगतान</h4><h2>145,230</h2></div>', unsafe_allow_html=True)
with col3: st.markdown('<div class="metric-card" style="background:#ef476f;"><h4>विफल (Failed)</h4><h2>12,450</h2></div>', unsafe_allow_html=True)
with col4: st.markdown('<div class="metric-card" style="background:#ffd166; color:#073b4c;"><h4>लंबित (Pending)</h4><h2>31,494</h2></div>', unsafe_allow_html=True)

st.divider()

# 6. सर्च इंजन
st.markdown("<h2 style='color: #073b4c;'>🔍 लाभार्थी की स्थिति जांचें</h2>", unsafe_allow_html=True)
aadhar_input = st.text_input("अपना 12 अंकों का आधार नंबर दर्ज करें:", placeholder="91XXXXXXXXXX", max_chars=12).strip()

if st.button("विवरण देखें (View Details)"):
    if aadhar_input and df is not None:
        with st.spinner('डेटा खोजा जा रहा है...'):
            # आपकी शीट के अनुसार कॉलम का नाम
            aadhar_col = 'Aadhaar Number'
            
            if aadhar_col in df.columns:
                # डेटा को साफ करना (Numbers से String में बदलना)
                df[aadhar_col] = df[aadhar_col].astype(str).str.replace('.0', '', regex=False).str.strip()
                match = df[df[aadhar_col] == aadhar_input]

                if not match.empty:
                    res = match.iloc[0]
                    
                    # डेटा निकालना (सटीक कॉलम मैपिंग)
                    name = res.get('Applicant Name', 'विवरण उपलब्ध नहीं')
                    father = res.get("Father's/Husband Name", 'विवरण उपलब्ध नहीं')
                    bank = res.get('BankName', 'N/A')
                    raw_status = str(res.get('PAYMENT STATUS', 'PENDING')).upper()
                    
                    # स्टेटस और रंग का लॉजिक
                    if "SUCCESS" in raw_status:
                        display_status = "सफल भुगतान (SUCCESS)"
                        status_color = "#06d6a0" # हरा
                    elif "FAIL" in raw_status:
                        display_status = "भुगतान विफल (FAILED)"
                        status_color = "#ef476f" # लाल
                    else:
                        display_status = f"प्रक्रिया में / लंबित ({raw_status})"
                        status_color = "#ffd166" # पीला

                    # परिणाम डिस्प्ले कार्ड
                    st.markdown(f"""
                        <div class="result-card">
                            <h3 style="color: #073b4c; border-bottom: 2px solid #eee; padding-bottom: 10px;">लाभार्थी का विवरण</h3>
                            <div style="display: flex; gap: 50px; flex-wrap: wrap; margin-top: 20px;">
                                <div style="flex: 1; min-width: 280px;">
                                    <p style="color: gray; margin-bottom: 0;"><b>लाभार्थी का नाम:</b></p>
                                    <h2 style="color: #073b4c; margin-top: 0;">{name}</h2>
                                    
                                    <p style="color: gray; margin-bottom: 0; margin-top: 20px;"><b>पिता/पति का नाम:</b></p>
                                    <h3 style="color: #073b4c; margin-top: 0;">{father}</h3>
                                </div>
                                <div style="flex: 1; min-width: 280px;">
                                    <p style="color: gray; margin-bottom: 0;"><b>बैंक का नाम:</b></p>
                                    <h3 style="color: #073b4c; margin-top: 0;">{bank}</h3>
                                    
                                    <p style="color: gray; margin-bottom: 0; margin-top: 20px;"><b>वर्तमान भुगतान स्थिति:</b></p>
                                    <h2 style="color: {status_color}; margin-top: 0; font-size: 1.8rem;">{display_status}</h2>
                                </div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error(f"आधार नंबर '{aadhar_input}' के लिए कोई रिकॉर्ड नहीं मिला।")
            else:
                st.error(f"Error: शीट में '{aadhar_col}' कॉलम नहीं मिला।")
    else:
        st.warning("कृपया 12 अंकों का आधार नंबर सही से दर्ज करें।")

# 7. फुटर
st.markdown("<br><br><div style='text-align: center; color: #666; border-top: 1px solid #ddd; padding-top: 20px;'><p>© 2026 <b>सामाजिक सुरक्षा कार्यालय, चतरा</b> | NIC चतरा द्वारा संचालित</p></div>", unsafe_allow_html=True)
