import streamlit as st
import pandas as pd
import re

# 1. पेज कॉन्फ़िगरेशन
st.set_page_config(page_title="JMMMSY Chatra Portal", layout="wide")

# 2. Session State Initialize (ताकि बटन क्लिक करने पर पेज रिफ्रेश न हो)
if "search_result" not in st.session_state:
    st.session_state.search_result = None
if "show_status" not in st.session_state:
    st.session_state.show_status = False

# 3. गूगल शीट लिंक
sheet_url = "https://docs.google.com/spreadsheets/d/15YSpwWFICG6XGXtTRUM6Kn5Cgl6pCfGDL24jWlMb7aI/export?format=csv"

@st.cache_data(ttl=60)
def load_data():
    try:
        return pd.read_csv(sheet_url)
    except:
        return None

df = load_data()

# 4. Colourful CSS (Large Fonts & Beautiful UI)
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }
    .header-box { background: linear-gradient(90deg, #1A2980 0%, #26D0CE 100%); padding: 30px; border-radius: 15px; color: white; text-align: center; margin-bottom: 25px; box-shadow: 0 8px 16px rgba(0,0,0,0.2); }
    .metric-container { display: flex; gap: 20px; margin-bottom: 30px; }
    .metric-card { flex: 1; padding: 25px; border-radius: 15px; color: white; text-align: center; box-shadow: 0 5px 15px rgba(0,0,0,0.2); }
    .bg-blue { background: linear-gradient(135deg, #36D1DC 0%, #5B86E5 100%); }
    .bg-green { background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); }
    .bg-red { background: linear-gradient(135deg, #FF416C 0%, #FF4B2B 100%); }
    .result-card { background-color: #ffffff; padding: 35px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.15); margin-top: 20px; border-left: 12px solid #26D0CE; }
    .detail-label { color: #666; font-size: 1.1rem; font-weight: 700; margin-bottom: 5px; margin-top: 15px;}
    .detail-value { color: #1A2980; font-size: 1.5rem; font-weight: 900; border-bottom: 1px dashed #ccc; padding-bottom: 5px;}
    .status-card { padding: 30px; border-radius: 15px; text-align: center; margin-top: 20px; color: white; font-size: 2rem; font-weight: bold; box-shadow: 0 10px 20px rgba(0,0,0,0.2); }
    </style>
""", unsafe_allow_html=True)

# 5. हेडर और मेट्रिक्स
st.markdown("""
    <div class="header-box">
        <h1 style='margin:0; font-size: 3rem;'>झारखण्ड मुख्यमंत्री मईयां सम्मान योजना (JMMMSY)</h1>
        <h2 style='margin:0; opacity:0.9; font-size: 1.8rem;'>सामाजिक सुरक्षा कार्यालय, चतरा</h2>
    </div>
    <div class="metric-container">
        <div class="metric-card bg-blue"><div style="font-size:1.2rem;">कुल लाभार्थी</div><div style="font-size:2.2rem; font-weight:bold;">1,89,174</div></div>
        <div class="metric-card bg-green"><div style="font-size:1.2rem;">सफल भुगतान</div><div style="font-size:2.2rem; font-weight:bold;">1,45,230</div></div>
        <div class="metric-card bg-red"><div style="font-size:1.2rem;">विफल/लंबित</div><div style="font-size:2.2rem; font-weight:bold;">43,944</div></div>
    </div>
""", unsafe_allow_html=True)

# 6. सर्च इंजन
st.markdown("<h2 style='color:#1A2980;'>🔍 लाभार्थी की स्थिति जांचें</h2>", unsafe_allow_html=True)
aadhar_input = st.text_input("12 अंकों का आधार नंबर दर्ज करें:", max_chars=12).strip()

if st.button("डाटा खोजें (Search)", type="primary"):
    if aadhar_input and df is not None:
        # 💡 N/A फिक्स: कॉलम के नाम से हर तरह का स्पेस और एंटर हटाना
        def clean_text(text): return re.sub(r'[^a-zA-Z0-9]', '', str(text)).lower()
        col_map = {clean_text(c): c for c in df.columns}
        
        target_col = col_map.get('aadhaarnumber') or col_map.get('aadharnumber')
        
        if target_col:
            df[target_col] = df[target_col].astype(str).str.replace('.0', '', regex=False).str.strip()
            match = df[df[target_col] == aadhar_input]

            if not match.empty:
                st.success("🎉 रिकॉर्ड मिल गया!")
                
                # डेटा को Session State में सुरक्षित करना
                res_dict = {}
                for clean_k, orig_k in col_map.items():
                    val = match.iloc[0][orig_k]
                    res_dict[clean_k] = str(val).strip() if pd.notna(val) else "N/A"
                
                st.session_state.search_result = res_dict
                st.session_state.show_status = False # नया सर्च होने पर स्टेटस छुपा दें
            else:
                st.error("कोई रिकॉर्ड नहीं मिला।")
                st.session_state.search_result = None
        else:
            st.error("शीट में आधार कॉलम नहीं मिला।")
    else:
        st.warning("कृपया आधार नंबर दर्ज करें।")

# 7. रिजल्ट और अलग पेमेंट बटन डिस्प्ले
if st.session_state.search_result is not None:
    res = st.session_state.search_result
    
    # सुरक्षित डेटा मैपिंग
    name = res.get('applicantname', 'N/A')
    father = res.get('fathershusbandname', 'N/A')
    district = res.get('district', 'N/A')
    category = res.get('category', 'N/A')
    bank = res.get('bankname', 'N/A')
    acc = res.get('accountno', 'N/A')
    ifsc = res.get('ifsccode', 'N/A')
    amount = res.get('amount', 'N/A')
    date = res.get('sanctiondate', 'N/A')
    status_val = res.get('paymentstatus', 'PENDING').upper()

    # लाभार्थी का कार्ड
    st.markdown(f"""
    <div class="result-card">
        <h2 style="color: #1A2980; margin:0 0 20px 0; border-bottom: 2px solid #eee; padding-bottom: 10px;">👤 व्यक्तिगत विवरण (Personal Details)</h2>
        <div style="display: flex; flex-wrap: wrap; gap: 40px;">
            <div style="flex: 1; min-width: 300px;">
                <div class="detail-label">लाभार्थी का नाम</div><div class="detail-value">{name}</div>
                <div class="detail-label">पिता/पति का नाम</div><div class="detail-value">{father}</div>
                <div class="detail-label">ज़िला / श्रेणी</div><div class="detail-value">{district} / {category}</div>
            </div>
            <div style="flex: 1; min-width: 300px;">
                <div class="detail-label">बैंक का नाम</div><div class="detail-value">{bank}</div>
                <div class="detail-label">खाता संख्या (Account No)</div><div class="detail-value">{acc}</div>
                <div class="detail-label">IFSC कोड</div><div class="detail-value">{ifsc}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("---")
    
    # 💳 पेमेंट स्टेटस देखने के लिए अलग बटन
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("💳 पेमेंट स्टेटस देखें (View Payment Status)", use_container_width=True):
            st.session_state.show_status = True
            
    # बटन क्लिक होने के बाद स्टेटस दिखाएं
    if st.session_state.show_status:
        if "SUCCESS" in status_val or "VERIFIED" in status_val:
            bg_color = "linear-gradient(135deg, #11998e 0%, #38ef7d 100%)"
        elif "FAIL" in status_val or "BLOCK" in status_val or "FROZEN" in status_val:
            bg_color = "linear-gradient(135deg, #FF416C 0%, #FF4B2B 100%)"
        else:
            bg_color = "linear-gradient(135deg, #f12711 0%, #f5af19 100%)"
            
        st.markdown(f"""
        <div class="status-card" style="background: {bg_color};">
            <div style="font-size: 1.5rem; opacity: 0.9;">वर्तमान भुगतान स्थिति</div>
            <div>{status_val}</div>
            <hr style="opacity: 0.3; margin: 15px 0;">
            <div style="font-size: 1.2rem;">स्वीकृति तिथि (Sanction Date): {date} | राशि: ₹ {amount}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br><hr><p style='text-align:center; color:#444;'>© 2026 <b>सामाजिक सुरक्षा कार्यालय, चतरा</b></p>", unsafe_allow_html=True)
