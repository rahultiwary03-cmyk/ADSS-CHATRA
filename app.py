import streamlit as st
import pandas as pd

# Page Config
st.set_page_config(page_title="JMMMSY Portal - Chatra", layout="wide")

# Direct Sheet Link
sheet_url = "https://docs.google.com/spreadsheets/d/15YSpwWFlCG6XGXtTRUM6Kn5Cgl6pCFGDL24jWIMb7aI/export?format=csv"

# Header Design
st.markdown("""
    <style>
    .header-box { background-color: #004a99; padding: 20px; border-radius: 10px; color: white; text-align: center; border-bottom: 5px solid #ff9933; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="header-box"><h1>झारखण्ड मुख्यमंत्री मइयां सम्मान योजना (JMMMSY)</h1><h3>District Administration - Chatra</h3></div>', unsafe_allow_html=True)

@st.cache_data(ttl=60)
def load_data():
    try:
        # User-agent bypass karne ke liye (security ke liye)
        return pd.read_csv(sheet_url)
    except Exception as e:
        return None

df = load_data()

if df is not None:
    df.columns = df.columns.str.strip()
    # Aadhaar column search logic
    target_col = next((col for col in df.columns if 'Aadhaar' in col or 'Aadhar' in col or 'CrAadhaar' in col), None)
    
    if target_col:
        df[target_col] = df[target_col].astype(str).str.replace(r'\s+|\.0$', '', regex=True)
        
        st.subheader("Beneficiary Search")
        search_query = st.text_input("12-digit Aadhaar Number enter karein:")

        if st.button("Check Status"):
            if search_query:
                result = df[df[target_col].str.contains(search_query.strip(), na=False)]
                if not result.empty:
                    st.success("Record Found!")
                    st.dataframe(result, use_container_width=True, hide_index=True)
                else:
                    st.error("Record nahi mila. Aadhaar number check karein.")
            else:
                st.info("Kripya Aadhaar number likhein.")
    else:
        st.error("Aadhaar column nahi mila. Sheet check karein.")
else:
    st.error("Google Sheet se connection fail ho gaya. Sheet ki 'Share' setting check karein.")
