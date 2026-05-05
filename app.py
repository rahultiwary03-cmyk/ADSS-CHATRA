import streamlit as st
import pandas as pd

# पेज सेटअप
st.set_page_config(page_title="JMMMSY Chatra Portal", layout="wide")

# गूगल शीट लिंक
sheet_url = "https://docs.google.com/spreadsheets/d/15YSpwWFICG6XGXtTRUM6Kn5Cgl6pCfGDL24jWlMb7aI/export?format=csv"

@st.cache_data(ttl=60)
def load_data():
    try:
        data = pd.read_csv(sheet_url)
        # कॉलम के नाम से एक्स्ट्रा स्पेस हटाना
        data.columns = [str(col).strip() for col in data.columns]
        return data
    except Exception as e:
        st.error(f"Data Error: {e}")
        return None

df = load_data()

# --- इंटरफेस डिजाइन ---
st.markdown("""
    <style>
    .header-box { background: linear-gradient(90deg, #073b4c 0%, #118ab2 100%); padding: 30px; border-radius: 15px; color: white; text-align: center; margin-bottom: 20px; }
    .metric-card { padding: 15px; border-radius: 10px; color: white; text-align: center; font-weight: bold; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
    .res-card { background: white; padding: 25px; border-radius: 15px; border-left: 10px solid #118ab2; box-shadow: 0 4px 12px rgba(0,0,0,0.1); margin-top: 20px; }
    </style>
""", unsafe_allow_html=True)

st.markdown("""<div class="header-box"><h1>झारखण्ड मुख्यमंत्री मईयां सम्मान योजना (JMMMSY)</h1><h3>सामाजिक सुरक्षा कार्यालय, चतरा</h3></div>""", unsafe_allow_html=True)

# मेट्रिक्स
c1, c2, c3 = st.columns(3)
c1.markdown('<div class="metric-card" style="background:#118ab2;"><h4>कुल लाभार्थी</h4><h2>189,174</h2></div>', unsafe_allow_html=True)
c2.markdown('<div class="metric-card" style="background:#06d6a0;"><h4>सफल भुगतान</h4><h2>145,230</h2></div>', unsafe_allow_html=True)
c3.markdown('<div class="metric-card" style="background:#ef476f;"><h4>विफल (Failed)</h4><h2>12,450</h2></div>', unsafe_allow_html=True)

st.divider()

# --- सर्च सेक्शन ---
st.subheader("🔍 लाभार्थी की स्थिति जांचें")
aadhar_input = st.text_input("अपना 12 अंकों का आधार नंबर दर्ज करें:", max_chars=12).strip()

if st.button("विवरण देखें (View Details)"):
    if aadhar_input and df is not None:
        with st.spinner('डेटा खोजा जा रहा है...'):
            # आपकी इमेज के अनुसार कॉलम का नाम 'Aadhaar Number' है (Double A)
            target_col = 'Aadhaar Number' 
            
            if target_col in df.columns:
                # डेटा क्लीनिंग: .0 हटाना और स्ट्रिंग में बदलना
                df[target_col] = df[target_col].astype(str).str.replace('.0', '', regex=False).str.strip()
                match = df[df[target_col] == aadhar_input]

                if not match.empty:
                    res = match.iloc[0]
                    st.success("रिकॉर्ड मिल गया!")
                    
                    # रिजल्ट डिस्प्ले
                    st.markdown(f"""
                        <div class="res-card">
                            <div style="display: flex; gap: 50px; flex-wrap: wrap;">
                                <div style="flex: 1;">
                                    <p style="color: gray; margin-bottom: 0;">लाभार्थी का नाम</p>
                                    <h2 style="color: #073b4c; margin-top: 0;">{res.get('Applicant Name', 'N/A')}</h2>
                                    
                                    <p style="color: gray; margin-bottom: 0;">पिता/पति का नाम</p>
                                    <h3 style="color: #073b4c; margin-top: 0;">{res.get("Father's/Husband Name", 'N/A')}</h3>
                                </div>
                                <div style="flex: 1;">
                                    <p style="color: gray; margin-bottom: 0;">बैंक का नाम</p>
                                    <h3 style="color: #073b4c; margin-top: 0;">{res.get('BankName', 'N/A')}</h3>
                                    
                                    <p style="color: gray; margin-bottom: 0;">वर्तमान स्थिति</p>
                                    <h2 style="color: #06d6a0; margin-top: 0;">{res.get('PAYMENT STATUS', 'Record Found')}</h2>
                                </div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error(f"आधार नंबर {aadhar_input} के लिए कोई डेटा नहीं मिला।")
            else:
                st.error(f"कॉलम '{target_col}' नहीं मिला। कृपया अपनी शीट चेक करें।")
    else:
        st.warning("कृपया आधार नंबर दर्ज करें।")

st
