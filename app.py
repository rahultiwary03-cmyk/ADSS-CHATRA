import streamlit as st
import pandas as pd

# 1. पेज कॉन्फ़िगरेशन (Wide Mode)
st.set_page_config(page_title="JMMMSY Chatra Portal", layout="wide")

# 2. गूगल शीट लिंक
sheet_url = "https://docs.google.com/spreadsheets/d/15YSpwWFICG6XGXtTRUM6Kn5Cgl6pCfGDL24jWlMb7aI/export?format=csv"

@st.cache_data(ttl=60)
def load_data():
    try:
        data = pd.read_csv(sheet_url)
        # कॉलम के नामों से स्पेस हटाना
        data.columns = [str(c).strip() for c in data.columns]
        return data
    except:
        return None

df = load_data()

# 3. Colourful Theme, Large Fonts और CSS
st.markdown("""
    <style>
    /* पूरे ऐप का कलरफुल बैकग्राउंड */
    .stApp {
        background: linear-gradient(135deg, #e0eafc 0%, #cfdef3 100%);
    }
    
    /* हेडर बॉक्स */
    .header-box {
        background: linear-gradient(90deg, #1A2980 0%, #26D0CE 100%);
        padding: 30px; border-radius: 15px; color: white; text-align: center;
        margin-bottom: 25px; box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    }
    
    /* मेट्रिक्स कार्ड्स */
    .metric-container {
        display: flex; justify-content: space-between; gap: 20px; margin-bottom: 30px;
    }
    .metric-card {
        flex: 1; padding: 25px; border-radius: 15px; color: white; text-align: center;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    .bg-blue { background: linear-gradient(135deg, #36D1DC 0%, #5B86E5 100%); }
    .bg-green { background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); }
    .bg-red { background: linear-gradient(135deg, #FF416C 0%, #FF4B2B 100%); }
    
    /* रिज़ल्ट कार्ड */
    .result-card {
        background-color: #ffffff; padding: 35px; border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.15); margin-top: 20px;
        border-left: 12px solid #26D0CE;
    }
    
    /* बड़ा और स्पष्ट फ़ॉन्ट */
    .detail-label { color: #666; font-size: 1.2rem; font-weight: 700; margin-bottom: 5px; margin-top: 20px;}
    .detail-value { color: #1A2980; font-size: 1.6rem; font-weight: 900; border-bottom: 2px dashed #ddd; padding-bottom: 5px;}
    
    /* स्टेटस बटन */
    .status-btn {
        color: white; padding: 12px 30px; border-radius: 50px;
        font-weight: 900; font-size: 1.3rem; display: inline-block;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2); text-transform: uppercase;
    }
    </style>
""", unsafe_allow_html=True)

# 4. हेडर
st.markdown("""
    <div class="header-box">
        <h1 style='margin:0; font-size: 3rem;'>झारखण्ड मुख्यमंत्री मईयां सम्मान योजना (JMMMSY)</h1>
        <h2 style='margin:0; opacity:0.9; font-size: 1.8rem;'>सामाजिक सुरक्षा कार्यालय, चतरा</h2>
        <p style='margin:10px 0 0 0; font-size:1.3rem;'>ज़िला प्रशासन, चतरा - एकीकृत लाभार्थी डैशबोर्ड</p>
    </div>
""", unsafe_allow_html=True)

# 5. कलरफुल मेट्रिक्स
st.markdown("""
    <div class="metric-container">
        <div class="metric-card bg-blue">
            <div style="font-size:1.3rem; opacity:0.9;">कुल लाभार्थी</div>
            <div style="font-size:2.5rem; font-weight:bold;">1,89,174</div>
        </div>
        <div class="metric-card bg-green">
            <div style="font-size:1.3rem; opacity:0.9;">सफल भुगतान</div>
            <div style="font-size:2.5rem; font-weight:bold;">1,45,230</div>
        </div>
        <div class="metric-card bg-red">
            <div style="font-size:1.3rem; opacity:0.9;">विफल/लंबित</div>
            <div style="font-size:2.5rem; font-weight:bold;">43,944</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# 6. सर्च इंजन
st.markdown("<h2 style='color:#1A2980; font-size: 2rem;'>🔍 लाभार्थी की स्थिति जांचें</h2>", unsafe_allow_html=True)
aadhar_input = st.text_input("12 अंकों का आधार नंबर दर्ज करें:", max_chars=12).strip()

if st.button("डाटा खोजें (Search)", type="primary"):
    if aadhar_input and df is not None:
        target_col = 'Aadhaar Number'
        if target_col in df.columns:
            # सर्च के लिए तैयार करना
            df[target_col] = df[target_col].astype(str).str.replace('.0', '', regex=False).str.strip()
            match = df[df[target_col] == aadhar_input]

            if not match.empty:
                res = match.iloc[0]
                st.success("🎉 रिकॉर्ड सफलतापूर्वक मिल गया!")

                # स्टेटस के अनुसार बटन का रंग तय करना
                status_val = str(res.get('PAYMENT STATUS', 'PENDING'))
                if "success" in status_val.lower() or "verified" in status_val.lower():
                    status_bg = "linear-gradient(135deg, #11998e 0%, #38ef7d 100%)" # Green
                elif "fail" in status_val.lower() or "block" in status_val.lower():
                    status_bg = "linear-gradient(135deg, #FF416C 0%, #FF4B2B 100%)" # Red
                else:
                    status_bg = "linear-gradient(135deg, #f12711 0%, #f5af19 100%)" # Orange

                # डेटा वेरिएबल्स
                name = res.get('Applicant Name', 'N/A')
                father = res.get("Father's/Husband Name", 'N/A')
                district = res.get('District', 'Chatra')
                panchayat = res.get('Panchayat', 'N/A')
                bank = res.get('BankName', 'N/A')
                amount = res.get('Amount', '0')
                date = res.get('SanctionDate', 'N/A')

                # HTML कोड (बिना किसी खाली लाइन के, ताकि कोड टेक्स्ट में न बदले)
                html_content = f"""
                <div class="result-card">
                    <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 3px solid #eee; padding-bottom: 20px; margin-bottom: 20px;">
                        <h2 style="color: #1A2980; margin:0; font-size: 2.2rem;">लाभार्थी विवरण</h2>
                        <div class="status-btn" style="background: {status_bg};">STATUS: {status_val}</div>
                    </div>
                    <div style="display: flex; flex-wrap: wrap; gap: 40px;">
                        <div style="flex: 1; min-width: 300px;">
                            <div class="detail-label">👤 लाभार्थी का नाम</div>
                            <div class="detail-value">{name}</div>
                            <div class="detail-label">👨‍👩‍👦 पिता/पति का नाम</div>
                            <div class="detail-value">{father}</div>
                            <div class="detail-label">📍 ज़िला / पंचायत</div>
                            <div class="detail-value">{district} / {panchayat}</div>
                        </div>
                        <div style="flex: 1; min-width: 300px;">
                            <div class="detail-label">🏦 बैंक का नाम</div>
                            <div class="detail-value">{bank}</div>
                            <div class="detail-label">💰 भुगतान राशि</div>
                            <div class="detail-value">₹ {amount}</div>
                            <div class="detail-label">📅 स्वीकृति तिथि (Sanction Date)</div>
                            <div class="detail-value">{date}</div>
                        </div>
                    </div>
                </div>
                """
                st.markdown(html_content, unsafe_allow_html=True)
            else:
                st.error("कोई रिकॉर्ड नहीं मिला। कृपया आधार नंबर दोबारा जांचें।")
        else:
            st.error("त्रुटि: गूगल शीट में 'Aadhaar Number' कॉलम नहीं मिला।")
    else:
        st.warning("कृपया सर्च करने के लिए आधार नंबर दर्ज करें।")

# 7. फुटर
st.markdown("<br><br><hr><p style='text-align:center; color:#444; font-size:1.2rem;'>© 2026 <b>सामाजिक सुरक्षा कार्यालय, चतरा</b> | JMMMSY Dashboard</p>", unsafe_allow_html=True)
