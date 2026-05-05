import streamlit as st
import pandas as pd

# 1. पेज कॉन्फ़िगरेशन
st.set_page_config(page_title="JMMMSY Chatra Portal", layout="wide")

# 2. गूगल शीट लिंक
sheet_url = "https://docs.google.com/spreadsheets/d/15YSpwWFICG6XGXtTRUM6Kn5Cgl6pCfGDL24jWlMb7aI/export?format=csv"

@st.cache_data(ttl=60)
def load_data():
    try:
        data = pd.read_csv(sheet_url)
        data.columns = [str(c).strip() for c in data.columns]
        return data
    except:
        return None

df = load_data()

# 3. Colorful Theme और कार्ड्स के लिए CSS
st.markdown("""
    <style>
    .main {
        background-color: #f0f4f8;
    }
    .header-box {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 30px; border-radius: 15px; color: white; text-align: center;
        margin-bottom: 25px; box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .metric-container {
        display: flex; justify-content: space-around; gap: 10px; margin-bottom: 20px;
    }
    .metric-box {
        background: white; padding: 15px; border-radius: 10px; text-align: center;
        flex: 1; box-shadow: 0 2px 5px rgba(0,0,0,0.1); border-bottom: 5px solid #1e3c72;
    }
    .result-card {
        background: white; padding: 30px; border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1); margin-top: 20px;
        border: 1px solid #e0e0e0;
    }
    .status-btn {
        background-color: #2e7d32; color: white; padding: 8px 20px;
        border-radius: 50px; font-weight: bold; font-size: 1.1rem;
        display: inline-block; box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .detail-label { color: #666; font-size: 0.9rem; font-weight: bold; margin-bottom: 2px; }
    .detail-value { color: #1e3c72; font-size: 1.2rem; font-weight: 700; margin-bottom: 15px; }
    </style>
""", unsafe_allow_html=True)

# 4. हेडर
st.markdown("""
    <div class="header-box">
        <h1 style='margin:0; font-size: 2.5rem;'>झारखण्ड मुख्यमंत्री मईयां सम्मान योजना (JMMMSY)</h1>
        <h3 style='margin:0; opacity:0.9;'>सामाजिक सुरक्षा कार्यालय, चतरा</h3>
        <p style='margin:5px 0 0 0;'>ज़िला प्रशासन, चतरा - एकीकृत लाभार्थी डैशबोर्ड</p>
    </div>
""", unsafe_allow_html=True)

# 5. मेट्रिक्स
st.markdown(f"""
    <div class="metric-container">
        <div class="metric-box">
            <div style="color:#1e3c72; font-size:0.9rem;">कुल लाभार्थी</div>
            <div style="font-size:1.5rem; font-weight:bold;">1,89,174</div>
        </div>
        <div class="metric-box" style="border-bottom-color: #2e7d32;">
            <div style="color:#2e7d32; font-size:0.9rem;">सफल भुगतान</div>
            <div style="font-size:1.5rem; font-weight:bold;">1,45,230</div>
        </div>
        <div class="metric-box" style="border-bottom-color: #d32f2f;">
            <div style="color:#d32f2f; font-size:0.9rem;">विफल/लंबित</div>
            <div style="font-size:1.5rem; font-weight:bold;">43,944</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# 6. सर्च इंजन
st.write("### 🔍 लाभार्थी की स्थिति जांचें")
aadhar_input = st.text_input("12 अंकों का आधार नंबर दर्ज करें:", max_chars=12, help="बिना स्पेस के आधार नंबर लिखें").strip()

if st.button("डाटा खोजें (Search)"):
    if aadhar_input and df is not None:
        # आधार कॉलम खोजना
        target_col = 'Aadhaar Number'
        if target_col in df.columns:
            df[target_col] = df[target_col].astype(str).str.replace('.0', '', regex=False).str.strip()
            match = df[df[target_col] == aadhar_input]

            if not match.empty:
                res = match.iloc[0]
                st.success("रिकॉर्ड मिल गया!")
                
                # पेमेंट स्टेटस का रंग तय करना
                status_val = str(res.get('PAYMENT STATUS', 'PENDING'))
                status_bg = "#2e7d32" if "success" in status_val.lower() or "verified" in status_val.lower() else "#d32f2f" if "fail" in status_val.lower() or "block" in status_val.lower() else "#f9a825"

                # रिजल्ट कार्ड रेंडर करना
                st.markdown(f"""
                    <div class="result-card">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 25px; border-bottom: 2px solid #f0f0f0; padding-bottom: 15px;">
                            <h2 style="color: #1e3c72; margin:0;">लाभार्थी विवरण</h2>
                            <div class="status-btn" style="background-color: {status_bg};">STATUS: {status_val}</div>
                        </div>
                        
                        <div style="display: flex; flex-wrap: wrap; gap: 20px;">
                            <div style="flex: 1; min-width: 250px;">
                                <div class="detail-label">लाभार्थी का नाम</div>
                                <div class="detail-value">{res.get('Applicant Name', 'N/A')}</div>
                                
                                <div class="detail-label">पिता/पति का नाम</div>
                                <div class="detail-value">{res.get("Father's/Husband Name", 'N/A')}</div>
                                
                                <div class="detail-label">ज़िला / पंचायत</div>
                                <div class="detail-value">{res.get('District', 'Chatra')} / {res.get('Panchayat', 'N/A')}</div>
                            </div>
                            
                            <div style="flex: 1; min-width: 250px;">
                                <div class="detail-label">बैंक का नाम</div>
                                <div class="detail-value">{res.get('BankName', 'N/A')}</div>
                                
                                <div class="detail-label">भुगतान राशि</div>
                                <div class="detail-value">₹ {res.get('Amount', '0')}</div>
                                
                                <div class="detail-label">स्वीकृति तिथि (Sanction Date)</div>
                                <div class="detail-value">{res.get('SanctionDate', 'N/A')}</div>
                            </div>
                        </div>
                        
                        <div style="margin-top:20px; padding:15px; background-color:#fff3e0; border-radius:10px; border-left: 5px solid #ff9800;">
                            <b style="color: #e65100;">सूचना:</b> यदि विवरण में कोई त्रुटि हो, तो अपने संबंधित ब्लॉक कार्यालय या सामाजिक सुरक्षा कार्यालय, चतरा से संपर्क करें।
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.error("कोई रिकॉर्ड नहीं मिला। कृपया आधार नंबर दोबारा जांचें।")
        else:
            st.error("त्रुटि: गूगल शीट में 'Aadhaar Number' कॉलम नहीं मिला।")
    else:
        st.warning("कृपया सर्च करने के लिए आधार नंबर दर्ज करें।")

# 7. फुटर
st.markdown("<br><hr><p style='text-align:center; color:#777;'>© 2026 <b>सामाजिक सुरक्षा कार्यालय, चतरा</b><br>Data is synced with official JMMMSY records.</p>", unsafe_allow_html=True)
