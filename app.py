import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(page_title="JMMMSY Chatra Portal", layout="wide")

# Custom CSS for Professional Look
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .header-box {
        background-color: #003399;
        color: white;
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stat-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
    }
    .result-card {
        background-color: #ffffff;
        padding: 20px;
        border-left: 5px solid #003399;
        border-radius: 5px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-top: 20px;
    }
    .stTextInput>div>div>input {
        border-radius: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# Google Sheet Connection (Direct CSV Link)
SHEET_ID = "15YSpwWFICG6XGXtTRUM6Kn5Cgl6pCfGDL24jWlMb7aI"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

@st.cache_data(ttl=600) # 10 minute tak data cache rahega
def load_data():
    try:
        df = pd.read_csv(SHEET_URL)
        # Data Cleaning: Column names se extra spaces hatana
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"Error connecting to Google Sheets: {e}")
        return None

df = load_data()

# App Header
st.markdown("""
    <div class="header-box">
        <h1>झारखण्ड मुख्यमंत्री मईयां सम्मान योजना (JMMMSY)</h1>
        <p style='font-size: 1.2rem;'>District Administration, Chatra - Payment Status Portal</p>
    </div>
    """, unsafe_allow_html=True)

if df is not None:
    # Top Stats Row
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="stat-card"><h3>Total Registered</h3><h2 style="color:#003399;">{len(df)}</h2></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="stat-card"><h3>District</h3><h2 style="color:#003399;">Chatra</h2></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="stat-card"><h3>Status</h3><h2 style="color:green;">Active</h2></div>', unsafe_allow_html=True)

    st.divider()

    # Search Section
    st.subheader("🔍 लाभार्थी की स्थिति खोजें (Search Beneficiary Status)")
    search_query = st.text_input("Enter Aadhaar Number / आधार नंबर दर्ज करें", placeholder="12 digit Aadhaar Number...")

    if search_query:
        # Aadhaar column ka naam wahi rakha hai jo aapki sheet mein dikh raha hai
        # Search logic (matches as string to avoid formatting issues)
        search_query = str(search_query).strip()
        result = df[df['Aadhaar Numbe'].astype(str).str.contains(search_query, na=False)]

        if not result.empty:
            st.success(f"कुल {len(result)} रिकॉर्ड मिले।")
            
            for index, row in result.iterrows():
                with st.container():
                    st.markdown('<div class="result-card">', unsafe_allow_html=True)
                    c1, c2 = st.columns(2)
                    
                    with c1:
                        st.write(f"*BENEFICIARY NAME:* {row.get('ApplicantName', 'N/A')}")
                        st.write(f"*FATHER/HUSBAND NAME:* {row.get('FatherHusbandN', 'N/A')}")
                        st.write(f"*AADHAAR NUMBER:* {row.get('Aadhaar Numbe', 'N/A')}")
                        st.write(f"*BANK NAME:* {row.get('BankName', 'N/A')}")

                    with c2:
                        st.write(f"*PAYMENT STATUS:* :green[SUCCESS]" if row.get('Amount', 0) > 0 else ":red[PENDING]")
                        st.write(f"*AMOUNT:* ₹{row.get('Amount', 0)}")
                        st.write(f"*REF NO:* {row.get('MMMSYRefNo', 'N/A')}")
                        st.write(f"*CATEGORY:* {row.get('Category', 'N/A')}")
                    
                    st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("कोई रिकॉर्ड नहीं मिला। कृपया आधार नंबर चेक करें।")

else:
    st.info("Database load ho raha hai, kripya pratiksha karein...")

# Footer
st.markdown("<br><hr><center><p style='color: grey;'>© 2026 District Administration Chatra | Technical Cell</p></center>", unsafe_allow_html=True)
