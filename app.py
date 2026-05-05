import streamlit as st
import pandas as pd

# 1. पेज सेटअप और टाइटल
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

# 3. बैकग्राउंड और कार्ड्स के लिए Colorful CSS
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    .header-box {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        padding: 30px; border-radius: 15px; color: white; text-align: center;
        margin-bottom: 25px; box-shadow: 0 10px 20px rgba(0,0,0,0.2);
    }
    .status-card {
        background: white; padding: 25px; border-radius: 15px;
        border-top: 10px solid #1e3c72; box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-top: 20px;
    }
    .payment-badge {
        background: #e8f5e9; color: #2e7d32; padding: 10px 20px;
        border-radius: 30px; font-weight: bold; font-size: 1.2rem;
        display: inline-block; border: 1px solid #2e7d32;
    }
    .detail-row { border-bottom: 1px solid #eee; padding: 10px 0; }
    </style>
""", unsafe_allow_html=True)

# 4. हेडर
st.markdown("""
    <div class="header-box">
        <h1 style='margin:0;'>झारखण्ड मुख्यमंत्री मईयां सम्मान योजना (JMMMSY)</h1>
        <h3 style='margin:0; opacity:0.9;'>सामाजिक सुरक्षा कार्यालय, चतरा</h3>
        <p style='margin:5px 0 0 0;'>ज़िला प्रशासन, चतरा - एकीकृत लाभार्थी डैशबोर्ड</p>
    </div>
""", unsafe_allow_html=True)

# 5. डैशबोर्ड मेट्रिक्स
c1, c2, c3 = st.columns(3)
with c1: st.metric("कुल लाभार्थी", "1,89,174", delta_color="normal")
with c2: st.metric("सफल भुगतान", "145,230")
with c3: st.metric("विफल/लंबित", "43,944")

st.divider()

# 6. सर्च इंजन
st.subheader("🔍 लाभार्थी की विस्तृत स्थिति जांचें")
aadhar_input = st.text_input("12 अंकों का आधार नंबर दर्ज करें:", max_chars=12).strip()

if st.button("डाटा खोजें (Search)"):
    if aadhar_input and df is not None:
        with st.spinner('प्रोसेसिंग...'):
            # आधार कॉलम पहचानना (Aadhaar Number)
            target_col = 'Aadhaar Number'
            if target_col in df.columns:
                df[target_col] = df[target_col].astype(str).str.replace('.0', '', regex=False).str.strip()
                match = df[df[target_col] == aadhar_input]

                if not match.empty:
                    res = match.iloc[0]
                    st.success("रिकॉर्ड मिल गया!")
                    
                    # डेटा डिस्प्ले कार्ड
                    st.markdown(f"""
                        <div class="status-card">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                                <h2 style="color: #1e3c72; margin:0;">लाभार्थी विवरण</h2>
                                <div class="payment-badge">STATUS: {res.get('PAYMENT STATUS', 'PENDING')}</div>
                            </div>
                            
                            <div style="display: flex; gap: 40px; flex-wrap: wrap;">
                                <div style="flex: 1; min-width: 300px;">
                                    <div class="detail-row"><b>लाभार्थी का नाम:</b><br><span style="font-size:1.5rem; color:#1e3c72;">{res.get('Applicant Name', 'N/A')}</span></div>
                                    <div class="detail-row"><b>पिता/पति का नाम:</b><br>{res.get("Father's/Husband Name", 'N/A')}</div>
                                    <div class="detail-row"><b>पंचायत / वार्ड:</b><br>{res.get('Panchayat', 'N/A')}</div>
                                </div>
                                <div style="flex: 1; min-width: 300px;">
                                    <div class="detail-row"><b>बैंक का नाम:</b><br>{res.get('BankName', 'N/A')}</div>
                                    <div class="detail-row"><b>खाता संख्या (अंतिम 4):</b><br>{str(res.get('AccountNo', 'N/A'))[-4:]}</div>
                                    <div class="detail-row"><b>Amount:</b><br>₹ {res.get('Amount', '0')}</div>
                                    <div class="detail-row"><b>Sanction Date:</b><br>{res.get('SanctionDate', 'N/A')}</div>
                                </div>
                            </div>
                            <div style="margin-top:20px; padding:15px; background:#fff3e0; border-radius:10px; color:#e65100;">
                                <b>महत्वपूर्ण नोट:</b> यदि आपका स्टेटस 'A/C Blocked or Frozen' है, तो कृपया अपने बैंक से संपर्क करें।
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error("कोई रिकॉर्ड नहीं मिला। कृपया आधार नंबर दोबारा जांचें।")
            else:
                st.error("Sheet में 'Aadhaar Number' कॉलम नहीं मिल रहा है।")
    else:
        st.warning("कृपया आधार नंबर दर्ज करें।")

# 7. फुटर
st.markdown("<br><br><div style='text-align:center; color:#555;'>© 2026 <b>सामाजिक सुरक्षा कार्यालय, चतरा</b><br>तकनीकी सेल द्वारा संचालित</div>", unsafe_allow_html=True)
