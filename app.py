import streamlit as st
import pandas as pd

# 1. पेज सेटअप (Fast Loading)
st.set_page_config(page_title="JMMMSY Chatra", layout="wide")

# 2. गूगल शीट लिंक
sheet_url = "https://docs.google.com/spreadsheets/d/15YSpwWFICG6XGXtTRUM6Kn5Cgl6pCfGDL24jWlMb7aI/export?format=csv"

# 3. डेटा लोड करने का सबसे तेज़ तरीका
@st.cache_data(ttl=300) # 5 मिनट का कैश ताकि बार-बार लोड न हो
def get_data():
    try:
        # सिर्फ जरूरी कॉलम लोड करना (Memory बचाने के लिए)
        data = pd.read_csv(sheet_url)
        data.columns = [str(c).strip() for c in data.columns]
        return data
    except:
        return None

df = get_data()

# 4. क्लीन UI (बिना भारी ग्राफिक्स के)
st.markdown("""
    <style>
    .header { background: #073b4c; padding: 20px; border-radius: 10px; color: white; text-align: center; }
    .card { background: white; padding: 20px; border-radius: 10px; border-left: 8px solid #118ab2; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
    </style>
    <div class="header">
        <h1>झारखण्ड मुख्यमंत्री मईयां सम्मान योजना</h1>
        <h3>सामाजिक सुरक्षा कार्यालय, चतरा</h3>
    </div>
""", unsafe_allow_html=True)

# 5. मेट्रिक्स (सिंपल और फास्ट)
st.write("")
c1, c2, c3 = st.columns(3)
c1.metric("कुल लाभार्थी", "1,89,174")
c2.metric("सफल भुगतान", "145,230")
c3.metric("विफल/लंबित", "43,944")

st.divider()

# 6. सर्च इंजन (Optimized)
st.subheader("🔍 आधार नंबर से स्थिति जांचें")
input_num = st.text_input("12 अंकों का आधार नंबर लिखें:", max_chars=12).strip()

if st.button("सर्च करें"):
    if input_num and df is not None:
        # Aadhaar Number कॉलम को टारगेट करना
        target = 'Aadhaar Number'
        if target in df.columns:
            # तेज सर्च के लिए स्ट्रिंग कन्वर्जन
            df[target] = df[target].astype(str).str.replace('.0', '', regex=False).str.strip()
            res = df[df[target] == input_num]

            if not res.empty:
                val = res.iloc[0]
                st.success("डेटा मिल गया!")
                st.markdown(f"""
                    <div class="card">
                        <p style="margin:0; color:gray;">नाम:</p>
                        <h2 style="margin:0; color:#073b4c;">{val.get('Applicant Name', 'N/A')}</h2>
                        <hr>
                        <p style="margin:0; color:gray;">पिता/पति:</p>
                        <h3 style="margin:0; color:#073b4c;">{val.get("Father's/Husband Name", 'N/A')}</h3>
                        <br>
                        <p style="margin:0; color:gray;">स्टेटस:</p>
                        <h2 style="margin:0; color:#06d6a0;">{val.get('PAYMENT STATUS', 'PENDING')}</h2>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.error("कोई रिकॉर्ड नहीं मिला।")
    else:
        st.warning("कृपया आधार नंबर दर्ज करें।")

st.markdown("<br><p style='text-align:center; color:silver;'>© 2026 सामाजिक सुरक्षा कार्यालय, चतरा</p>", unsafe_allow_html=True)
