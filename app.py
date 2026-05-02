import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(page_title="JMMMSY Portal - Chatra", layout="wide")

# Ye aapki sheet ka direct CSV link hai
SHEET_ID = "https://docs.google.com/spreadsheets/d/15YSpwWFICG6XGXtTRUM6Kn5Cgl6pCfGDL24jWlMb7aI/edit?usp=sharing"
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv"

# Header Design
st.markdown("""
    <style>
    .header-box { background-color: #004a99; padding: 20px; border-radius: 10px; color: white; text-align: center; border-bottom: 5px solid #ff9933; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="header-box"><h1>झारखण्ड मुख्यमंत्री मइयां सम्मान योजना (JMMMSY)</h1><h3>District Administration - Chatra</h3></div>', unsafe_allow_html=True)

@st.cache_data(ttl=60)
def fetch_data():
    try:
        # Direct hit to Google Visualization API (Sabse fast aur reliable)
        data = pd.read_csv(URL)
        return data
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None

df = fetch_data()

if df is not None:
    # Column names cleaning
    df.columns = df.columns.str.strip()
    
    # Aadhaar column dhoondhna
    target_col = next((col for col in df.columns if 'Aadhaar' in col or 'Aadhar' in col or 'CrAadhaar' in col), None)
    
    if target_col:
        # Aadhaar numbers clean karna
        df[target_col] = df[target_col].astype(str).str.replace(r'\s+|\.0$', '', regex=True)
        
        st.subheader("Beneficiary Search")
        search_input = st.text_input("12-digit Aadhaar Number enter karein:")

        if st.button("Check Status"):
            if search_input:
                query = search_input.strip()
                result = df[df[target_col].str.contains(query, na=False)]
                
                if not result.empty:
                    st.success("Record Found!")
                    st.dataframe(result, use_container_width=True, hide_index=True)
                else:
                    st.error(f"Aadhaar '{query}' ke liye koi record nahi mila.")
            else:
                st.info("Kripya Aadhaar number enter karein.")
    else:
        st.error("Sheet mein 'Aadhaar Number' ka column nahi mil raha. Heading check karein.")
else:
    st.error("Google Sheet se connect nahi ho pa raha. Kripya link check karein.")

st.markdown("---")
st.caption("© 2026 District Administration, Chatra | Direct Cloud Sync Enabled")
