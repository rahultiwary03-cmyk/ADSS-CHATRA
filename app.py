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
        # कॉलम के नामों से एक्स्ट्रा स्पेस हटाना
        data.columns = [str(col).strip() for col in data.columns]
        return data
    except Exception as e:
        st.error(f"Data Load Error: {e}")
        return None

df = load_data()

# --- CSS Styling ---
st.markdown("""
    <style>
    .header-box { background: linear-gradient(90deg, #073b4c 0%, #118ab2 100%); padding: 30px; border-radius: 15px; color: white; text-align: center; margin-bottom: 20px; }
    .res-card { background: white; padding: 25px; border-radius: 15px; border-left: 10px solid #118ab2; box-shadow: 0 4px 12px rgba(0,0,0,0.1); margin-top: 20px; }
    </style>
""", unsafe_allow_html=True)

st.markdown("""<div class="header-box"><h1>झारखण्ड मुख्यमंत्री मईयां सम्मान योजना (JMMMSY)</h1><h3>सामाजिक सुरक्षा कार्यालय, चतरा</h3></div>""", unsafe_allow_html=True)

# --- Search Section ---
st.subheader("🔍 लाभार्थी की स्थिति जांचें")
aadhar_input = st.text_input("अपना 12 अंकों का आधार नंबर दर्ज करें:", max_chars=12).strip()

if st.button("विवरण देखें (View Details)"):
    if aadhar_input and df is not None:
        with st.spinner('खोज जारी है...'):
            # 1. आधार कॉलम को डायनामिक तरीके से ढूंढना
            aadhar_col = next((c for c in df.columns if 'aadhar' in c.lower() or 'adhar' in c.lower()), None)
            
            if aadhar_col:
                # डेटा क्लीन करना
                df[aadhar_col] = df[aadhar_col].astype(str).str.replace('.0', '', regex=False).str.strip()
                match = df[df[aadhar_col] == aadhar_input]

                if not match.empty:
                    res = match.iloc[0]
                    st.success("रिकॉर्ड मिल गया!")
                    
                    # 2. अन्य कॉलमों को डायनामिक तरीके से ढूंढना (ताकि N/A न आए)
                    name = res.get('Applicant Name') or res.get('Beneficiary Name') or "उपलब्ध नहीं"
                    father = res.get("Father's/Husband Name") or res.get("Father Husband Name") or "उपलब्ध नहीं"
                    bank = res.get('BankName') or res.get('Bank Name') or "उपलब्ध नहीं"
                    status = res.get('PAYMENT STATUS') or res.get('Payment Status') or "Record Found"

                    st.markdown(f"""
                        <div class="res-card">
                            <div style="display: flex; gap: 50px; flex-wrap: wrap;">
                                <div style="flex: 1; min-width: 250px;">
                                    <p style="color: gray; margin-bottom: 0;"><b>लाभार्थी का नाम</b></p>
                                    <h2 style="color: #073b4c; margin-top: 0;">{name}</h2>
                                    
                                    <p style="color: gray; margin-bottom: 5px; margin-top: 15px;"><b>पिता/पति का नाम</b></p>
                                    <h3 style="color: #073b4c; margin-top: 0;">{father}</h3>
                                </div>
                                <div style="flex: 1; min-width: 250px;">
                                    <p style="color: gray; margin-bottom: 0;"><b>बैंक का नाम</b></p>
                                    <h3 style="color: #073b4c; margin-top: 0;">{bank}</h3>
                                    
                                    <p style="color: gray; margin-bottom: 5px; margin-top: 15px;"><b>वर्तमान स्थिति</b></p>
                                    <h2 style="color: #06d6a0; margin-top: 0; font-size: 1.5rem;">{status}</h2>
                                </div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error(f"आधार नंबर {aadhar_input} के लिए कोई रिकॉर्ड नहीं मिला।")
            else:
                st.error("Sheet में आधार का कॉलम नहीं मिला। कृपया कॉलम का नाम 'Aadhaar Number' रखें।")
    else:
        st.warning("कृपया आधार नंबर दर्ज करें।")
