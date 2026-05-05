import streamlit as st
import pandas as pd

# 1. पेज कॉन्फ़िगरेशन
st.set_page_config(page_title="JMMMSY Chatra Portal", layout="wide")

# 2. Session State Initialize (ताकि डेटा सुरक्षित रहे और क्रैश न हो)
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
        # सुरक्षा के लिए कॉलम के आगे-पीछे के अदृश्य स्पेस हटाना
        data.columns = data.columns.str.strip()
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
    
    /* 🔥 जादुई CSS: 'View Payment Status' वाले बटन को बहुत बड़ा और रंगीन बनाना */
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

if st.button("डाटा खोजें (Search)"):
    if aadhar_input and df is not None:
        
        # आपकी शीट के सटीक कॉलम का नाम
        target_col = 'AadhaarNumber'
        
        if target_col in df.columns:
            # सर्च मैचिंग
            df['temp_aadhar'] = df[target_col].astype(str).str.replace('.0', '', regex=False).str.strip()
            match = df[df['temp_aadhar'] == aadhar_input]

            if not match.empty:
                st.success("🎉 रिकॉर्ड मिल गया!")
                row = match.iloc[0]
                
                # डेटा को सुरक्षित तरीके से निकालना (जो स्पेस आपने हटाए हैं, उन्हीं नामों का इस्तेमाल)
                st.session_state.search_result = {
                    'name': str(row.get('ApplicantName', 'N/A')),
                    'father': str(row.get("Father's/HusbandName", 'N/A')),
                    'dob': str(row.get('DateOfBirth', 'N/A')),
                    'age': str(row.get('Age', 'N/A')),
                    'category': str(row.get('Category', 'N/A')),
                    'district': str(row.get('District', 'N/A')),
                    'bank': str(row.get('BankName', 'N/A')),
                    'acc': str(row.get('AccountNo', 'N/A')),
                    'ifsc': str(row.get('IfscCode', 'N/A')),
                    'amount': str(row.get('Amount', 'N/A')),
                    'sanction_date': str(row.get('SanctionDate', 'N/A')),
                    'sanction_no': str(row.get('SanctionNo', 'N/A')),
                    'ref_no': str(row.get('MMMSYRefNo', 'N/A')),
                    'status': str(row.get('PAYMENTSTATUS', 'PENDING')).upper()
                }
                st.session_state.show_status = False
            else:
                st.error("कोई रिकॉर्ड नहीं मिला।")
                st.session_state.search_result = None
        else:
            st.error(f"शीट में '{target_col}' कॉलम नहीं मिला। उपलब्ध कॉलम: {', '.join(df.columns)}")
            st.session_state.search_result = None
    else:
        st.warning("कृपया आधार नंबर दर्ज करें।")

# 7. रिजल्ट डिस्प्ले (Strictly Error-Free HTML)
if st.session_state.search_result is not None:
    res = st.session_state.search_result
    
    # HTML स्ट्रिंग को बिना खाली लाइन के बनाना ताकि कोड टेक्स्ट में न बदले और .get() से KeyError न आए
    html_content = (
        f'<div class="result-card">'
        f'<div class="section-title">👤 व्यक्तिगत विवरण (Personal Details)</div>'
        f'<div style="display: flex; flex-wrap: wrap; gap: 40px; margin-bottom: 40px;">'
        f'<div style="flex: 1; min-width: 250px;">'
        f'<div class="detail-label">लाभार्थी का नाम</div><div class="detail-value">{res.get("name", "N/A")}</div>'
        f'<div class="detail-label">पिता/पति का नाम</div><div class="detail-value">{res.get("father", "N/A")}</div>'
        f'<div class="detail-label">ज़िला / श्रेणी</div><div class="detail-value">{res.get("district", "N/A")} / {res.get("category", "N/A")}</div>'
        f'</div>'
        f'<div style="flex: 1; min-width: 250px;">'
        f'<div class="detail-label">जन्म तिथि (DOB)</div><div class="detail-value">{res.get("dob", "N/A")}</div>'
        f'<div class="detail-label">उम्र (Age)</div><div class="detail-value">{res.get("age", "N/A")}</div>'
        f'<div class="detail-label">MMMSY Ref No</div><div class="detail-value">{res.get("ref_no", "N/A")}</div>'
        f'</div>'
        f'</div>'
        f'<div class="section-title">🏦 बैंक एवं स्वीकृति विवरण (Bank Details)</div>'
        f'<div style="display: flex; flex-wrap: wrap; gap: 40px;">'
        f'<div style="flex: 1; min-width: 250px;">'
        f'<div class="detail-label">बैंक का नाम</div><div class="detail-value">{res.get("bank", "N/A")}</div>'
        f'<div class="detail-label">खाता संख्या (Account No)</div><div class="detail-value">{res.get("acc", "N/A")}</div>'
        f'<div class="detail-label">IFSC कोड</div><div class="detail-value">{res.get("ifsc", "N/A")}</div>'
        f'</div>'
        f'<div style="flex: 1; min-width: 250px;">'
        f'<div class="detail-label">भुगतान राशि</div><div class="detail-value">₹ {res.get("amount", "N/A")}</div>'
        f'<div class="detail-label">स्वीकृति तिथि (Sanction Date)</div><div class="detail-value">{res.get("sanction_date", "N/A")}</div>'
        f'<div class="detail-label">Sanction No</div><div class="detail-value">{res.get("sanction_no", "N/A")}</div>'
        f'</div>'
        f'</div>'
        f'</div>'
    )
    
    st.markdown(html_content, unsafe_allow_html=True)
    st.write("<br>", unsafe_allow_html=True)
    
    # 💳 विशाल पेमेंट बटन
    col1, col2, col3 = st.columns([1,3,1])
    with col2:
        if st.button("💳 वर्तमान भुगतान स्थिति देखें (View Payment Status)", type="primary", use_container_width=True):
            st.session_state.show_status = True
            
    # स्टेटस कार्ड
    if st.session_state.show_status:
        status_val = res.get('status', 'PENDING')
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
