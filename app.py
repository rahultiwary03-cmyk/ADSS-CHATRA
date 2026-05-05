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
        data = pd.read_csv(sheet_url)
        # 💡 सबसे महत्वपूर्ण फिक्स: कॉलम के नाम से हर तरह का स्पेस और लाइन ब्रेक हटाना
        data.columns = data.columns.astype(str).str.replace('\n', ' ', regex=False).str.replace('\r', '', regex=False).str.strip()
        data.columns = [re.sub(r'\s+', ' ', c) for c in data.columns]
        return data
    except Exception as e:
        return None

df = load_data()

# 4. Colourful CSS & Huge Button Style
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }
    .header-box { background: linear-gradient(90deg, #1A2980 0%, #26D0CE 100%); padding: 30px; border-radius: 15px; color: white; text-align: center; margin-bottom: 25px; box-shadow: 0 8px 16px rgba(0,0,0,0.2); }
    .metric-container { display: flex; gap: 20px; margin-bottom: 30px; }
    .metric-card { flex: 1; padding: 25px; border-radius: 15px; color: white; text-align: center; box-shadow: 0 5px 15px rgba(0,0,0,0.2); }
    .bg-blue { background: linear-gradient(135deg, #36D1DC 0%, #5B86E5 100%); }
    .bg-green { background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); }
    .bg-red { background: linear-gradient(135deg, #FF416C 0%, #FF4B2B 100%); }
    
    .result-card { background-color: #ffffff; padding: 35px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.15); margin-top: 20px; border-left: 10px solid #1A2980; }
    .section-title { color: #1A2980; margin: 0 0 20px 0; border-bottom: 2px solid #eee; padding-bottom: 10px; font-size: 1.8rem; font-weight: bold;}
    
    .detail-label { color: #555; font-size: 1.1rem; font-weight: 700; margin-bottom: 2px; margin-top: 15px;}
    .detail-value { color: #000; font-size: 1.4rem; font-weight: 900; border-bottom: 1px dashed #ccc; padding-bottom: 5px;}
    
    .status-card { padding: 30px; border-radius: 15px; text-align: center; margin-top: 25px; color: white; font-size: 2.2rem; font-weight: bold; box-shadow: 0 10px 20px rgba(0,0,0,0.3); border: 4px solid white;}
    
    /* 🔥 जादुई CSS: 'View Payment Status' वाले प्राइमरी बटन को बहुत बड़ा और रंगीन बनाना */
    button[kind="primary"] {
        background: linear-gradient(90deg, #ff416c 0%, #ff4b2b 100%) !important;
        color: white !important;
        border: none !important;
        padding: 20px 40px !important;
        border-radius: 50px !important;
        box-shadow: 0 8px 20px rgba(255, 65, 108, 0.4) !important;
        transition: all 0.3s ease !important;
    }
    button[kind="primary"] p {
        font-size: 24px !important; 
        font-weight: 900 !important;
        margin: 0 !important;
    }
    button[kind="primary"]:hover {
        transform: scale(1.05) !important;
        box-shadow: 0 12px 25px rgba(255, 65, 108, 0.6) !important;
    }
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

# सर्च बटन (Normal / Secondary Button)
if st.button("डाटा खोजें (Search)"):
    if aadhar_input and df is not None:
        
        # कॉलम के नामों को पूरी तरह साफ करना (ताकि मिलान में गलती न हो)
        def clean_col(text): return re.sub(r'[^a-zA-Z0-9]', '', str(text)).lower()
        row_dict_list = []
        
        target_col = next((c for c in df.columns if 'aadhaar' in clean_col(c) or 'aadhar' in clean_col(c)), None)
        
        if target_col:
            df[target_col] = df[target_col].astype(str).str.replace('.0', '', regex=False).str.strip()
            match = df[df[target_col] == aadhar_input]

            if not match.empty:
                st.success("🎉 रिकॉर्ड मिल गया!")
                
                # डेटा को सुरक्षित निकालना
                res_row = match.iloc[0]
                cleaned_row = {clean_col(k): v for k, v in res_row.items()}
                
                def get_val(keys):
                    for k in keys:
                        if k in cleaned_row:
                            val = cleaned_row[k]
                            return str(val).strip() if pd.notna(val) and str(val).strip() != '' else "N/A"
                    return "N/A"

                st.session_state.search_result = {
                    'name': get_val(['applicantname', 'beneficiaryname']),
                    'father': get_val(['fathershusbandname', 'fathername']),
                    'dob': get_val(['dateofbirth', 'dob']),
                    'age': get_val(['age', 'currentage']),
                    'category': get_val(['category']),
                    'district': get_val(['district']),
                    'bank': get_val(['bankname']),
                    'acc': get_val(['accountno', 'accountnumber']),
                    'ifsc': get_val(['ifsccode', 'ifsc']),
                    'amount': get_val(['amount']),
                    'sanction_date': get_val(['sanctiondate']),
                    'sanction_no': get_val(['sanctionno']),
                    'ref_no': get_val(['mmmsyrefno']),
                    'status': get_val(['paymentstatus', 'status']).upper()
                }
                st.session_state.show_status = False # नया सर्च होने पर स्टेटस छुपा दें
            else:
                st.error("कोई रिकॉर्ड नहीं मिला।")
                st.session_state.search_result = None
        else:
            st.error("शीट में आधार कॉलम नहीं मिला।")
    else:
        st.warning("कृपया आधार नंबर दर्ज करें।")

# 7. रिजल्ट और सभी कॉलम का डिस्प्ले
if st.session_state.search_result is not None:
    res = st.session_state.search_result
    
    # 🌟 पूरा डेटा डिस्प्ले
    st.markdown(f"""
    <div class="result-card">
        <div class="section-title">👤 व्यक्तिगत विवरण (Personal Details)</div>
        <div style="display: flex; flex-wrap: wrap; gap: 40px; margin-bottom: 40px;">
            <div style="flex: 1; min-width: 250px;">
                <div class="detail-label">लाभार्थी का नाम</div><div class="detail-value">{res['name']}</div>
                <div class="detail-label">पिता/पति का नाम</div><div class="detail-value">{res['father']}</div>
                <div class="detail-label">ज़िला / श्रेणी</div><div class="detail-value">{res['district']} / {res['category']}</div>
            </div>
            <div style="flex: 1; min-width: 250px;">
                <div class="detail-label">जन्म तिथि (DOB)</div><div class="detail-value">{res['dob']}</div>
                <div class="detail-label">उम्र (Age)</div><div class="detail-value">{res['age']}</div>
                <div class="detail-label">MMMSY Ref No</div><div class="detail-value">{res['ref_no']}</div>
            </div>
        </div>

        <div class="section-title">🏦 बैंक एवं स्वीकृति विवरण (Bank Details)</div>
        <div style="display: flex; flex-wrap: wrap; gap: 40px;">
            <div style="flex: 1; min-width: 250px;">
                <div class="detail-label">बैंक का नाम</div><div class="detail-value">{res['bank']}</div>
                <div class="detail-label">खाता संख्या (Account No)</div><div class="detail-value">{res['acc']}</div>
                <div class="detail-label">IFSC कोड</div><div class="detail-value">{res['ifsc']}</div>
            </div>
            <div style="flex: 1; min-width: 250px;">
                <div class="detail-label">भुगतान राशि</div><div class="detail-value">₹ {res['amount']}</div>
                <div class="detail-label">स्वीकृति तिथि (Sanction Date)</div><div class="detail-value">{res['sanction_date']}</div>
                <div class="detail-label">Sanction No</div><div class="detail-value">{res['sanction_no']}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("<br>", unsafe_allow_html=True)
    
    # 💳 विशाल (Huge) पेमेंट बटन (इसे type="primary" दिया है ताकि CSS इस पर काम करे)
    col1, col2, col3 = st.columns([1,3,1])
    with col2:
        if st.button("💳 वर्तमान भुगतान स्थिति देखें (View Payment Status)", type="primary", use_container_width=True):
            st.session_state.show_status = True
            
    # बटन क्लिक होने के बाद स्टेटस दिखाएं
    if st.session_state.show_status:
        status_val = res['status']
        if "SUCCESS" in status_val or "VERIFIED" in status_val:
            bg_color = "linear-gradient(135deg, #11998e 0%, #38ef7d 100%)"
        elif "FAIL" in status_val or "BLOCK" in status_val or "FROZEN" in status_val:
            bg_color = "linear-gradient(135deg, #FF416C 0%, #FF4B2B 100%)"
        else:
            bg_color = "linear-gradient(135deg, #f12711 0%, #f5af19 100%)"
            
        st.markdown(f"""
        <div class="status-card" style="background: {bg_color};">
            <div style="font-size: 1.5rem; opacity: 0.9;">STATUS</div>
            <div>{status_val}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br><hr><p style='text-align:center; color:#444;'>© 2026 <b>सामाजिक सुरक्षा कार्यालय, चतरा</b></p>", unsafe_allow_html=True)
