import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="JMMSY Chatra Portal", layout="wide", page_icon="📝")

# Custom Styling
st.markdown("""
    <style>
    .main-header {
        background-color: #1c49a6;
        color: white;
        padding: 15px;
        text-align: center;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .stButton>button {
        width: 100%;
        background-color: #1c49a6;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Header
st.markdown("<div class='main-header'><h1>झारखण्ड मुख्यमंत्री मईयां सम्मान योजना (JMMSY)</h1><p>ज़िला प्रशासन, चतरा - भुगतान स्थिति पोर्टल</p></div>", unsafe_allow_html=True)

# 3. Google Sheet Data Loading
# Aapki sheet ka ID: 1fApqqsNEulpVsPH7O0IAMRvQv39DMYkV2PB_kg3qntg
sheet_id = "1fApqqsNEulpVsPH7O0IAMRvQv39DMYkV2PB_kg3qntg"
sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

@st.cache_data(ttl=600) # Har 10 minute mein data refresh hoga
def load_data():
    try:
        df = pd.read_csv(sheet_url)
        # Column names ke extra spaces hatane ke liye
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

df = load_data()

# 4. Top Statistics (Manual as per image)
col1, col2, col3 = st.columns(3)
col1.metric("कुल लाभार्थी", "1,89,174")
col2.metric("ज़िला", "चतरा (CHATRA)")
col3.metric("पोर्टल स्थिति", "सक्रिय (Live)")

st.divider()

# 5. Search Section
st.subheader("🔍 लाभार्थी खोजें (Beneficiary Search)")

# Input field
aadhar_input = st.text_input("आधार नंबर दर्ज करें (12 अंक):", placeholder="Yahan 12-digit Aadhaar Number likhein...")

if st.button("स्टेटस चेक करें"):
    if aadhar_input:
        if df is not None:
            # SEARCH COLUMN IDENTIFICATION
            # Hum check kar rahe hain ki column ka naam 'Aadhar Number' hai ya 'Aadhaar'
            possible_cols = ['Aadhar Number', 'Aadhaar Number', 'AADHAR', 'Aadhar']
            search_col = None
            
            for col in possible_cols:
                if col in df.columns:
                    search_col = col
                    break
            
            if search_col:
                # Data ko string mein convert karke search karna taaki KeyError na aaye
                df[search_col] = df[search_col].astype(str).str.replace('.0', '', regex=False).str.strip()
                
                # Filter results
                result = df[df[search_col] == aadhar_input.strip()]
                
                if not result.empty:
                    st.success(f"Record Mil Gaya!")
                    st.dataframe(result, use_container_width=True)
                else:
                    st.error("Maafi chahte hain, is Aadhaar number ka koi record nahi mila.")
            else:
                st.error(f"Error: Sheet mein Aadhaar ka column nahi mila. Sheet headers: {list(df.columns)}")
        else:
            st.error("Google Sheet load nahi ho saki.")
    else:
        st.warning("Kripya search karne ke liye Aadhaar number enter karein.")

# Footer
st.markdown("---")
st.caption("© 2024 District Administration, Chatra. All Rights Reserved.")
