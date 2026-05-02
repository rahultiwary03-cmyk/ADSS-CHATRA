import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(page_title="JMMMSY Chatra Portal", layout="wide", page_icon="🏛️")

# --- DATA SOURCE ---
SHEET_ID = "15YSpwWFICG6XGXtTRUM6Kn5Cgl6pCfGDL24jWlMb7aI"
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

# Custom CSS for Professional Look
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stTextInput > div > div > input { border-radius: 25px; border: 2px solid #1e40af; padding: 10px 20px; }
    .reportview-container .main .block-container { padding-top: 2rem; }
    .header-style { background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%); color: white; padding: 30px; border-radius: 15px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 25px; }
    .card { background-color: white; padding: 20px; border-radius: 10px; border-left: 5px solid #1e40af; box-shadow: 0 2px 4px rgba(0,0,0,0.05); margin-bottom: 10px; }
    .label { color: #6b7280; font-size: 0.9rem; font-weight: bold; text-transform: uppercase; }
    .value { color: #111827; font-size: 1.1rem; font-weight: 500; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# Header Section
st.markdown("""
    <div class="header-style">
        <h1 style='margin:0;'>झारखण्ड मुख्यमंत्री मईयां सम्मान योजना (JMMMSY)</h1>
        <p style='font-size:1.2rem; opacity:0.9;'>District Administration, Chatra - Payment Status Portal</p>
    </div>
    """, unsafe_allow_html=True)

@st.cache_data(ttl=300)
def load_data():
    try:
        df = pd.read_csv(URL)
        df.columns = df.columns.str.strip()
        return df
    except:
        return None

df = load_data()

if df is not None:
    # Top Stats (Total Records)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Registered", len(df))
    with col2:
        st.metric("District", "Chatra")
    with col3:
        st.metric("Status", "Active")

    st.divider()

    # Search Section
    st.subheader("🔍 लाभार्थी की स्थिति खोजें (Search Beneficiary Status)")
    aadhaar_input = st.text_input("", placeholder="अपना 12 अंकों का आधार नंबर दर्ज करें...")

    if aadhaar_input:
        # Searching across Aadhaar column (CrAadhaar Number as per your image)
        col_name = 'CrAadhaar Number'
        if col_name in df.columns:
            result = df[df[col_name].astype(str).str.contains(aadhaar_input.replace(" ", ""))]
        else:
            result = df[df.astype(str).apply(lambda x: x.str.contains(aadhaar_input)).any(axis=1)]

        if not result.empty:
            st.success(f"कुल {len(result)} रिकॉर्ड मिले।")
            
            for i in range(len(result)):
                row = result.iloc[i]
                # Card Layout for Results
                with st.container():
                    st.markdown(f"""
                    <div class="card">
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                            <div><p class="label">Beneficiary Name</p><p class="value">{row.get('Favoring1', 'N/A')}</p></div>
                            <div><p class="label">Payment Status</p><p class="value" style="color:red;">{row.get('CreditStatus_PB1', 'N/A')}</p></div>
                            <div><p class="label">Reason for Failure</p><p class="value">{row.get('BankReasonDescForFailure1', 'N/A')}</p></div>
                            <div><p class="label">Amount</p><p class="value">₹{row.get('TotalAmount_PB1', '0')}</p></div>
                            <div><p class="label">Aadhaar Number</p><p class="value">{row.get('CrAadhaar Number', 'N/A')}</p></div>
                            <div><p class="label">Credited On</p><p class="value">{row.get('CredittedOn_PB', 'N/A')}</p></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.error("❌ कोई रिकॉर्ड नहीं मिला। कृपया सही आधार नंबर दर्ज करें।")
    else:
        st.info("💡 सूचना: विवरण देखने के लिए ऊपर बॉक्स में आधार नंबर लिखें।")
else:
    st.error("Database से संपर्क नहीं हो पा रहा है।")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: grey;'>Designed for District Administration Chatra | © 2026</p>", unsafe_allow_html=True)
