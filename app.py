import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# Page Configuration
st.set_page_config(page_title="JMMMSY Portal - Chatra", layout="wide")

# Google Sheet Link (Yahan apna link paste karein)
sheet_url = "https://docs.google.com/spreadsheets/d/15YSpwWFICG6XGXtTRUM6Kn5Cgl6pCfGDL24jWlMb7aI/edit?usp=sharing"

# Header Design
st.markdown("""
    <style>
    .header-box { background-color: #004a99; padding: 20px; border-radius: 10px; color: white; text-align: center; border-bottom: 5px solid #ff9933; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="header-box"><h1>झारखण्ड मुख्यमंत्री मइयां सम्मान योजना (JMMMSY)</h1><h3>District Administration - Chatra</h3></div>', unsafe_allow_html=True)

try:
    # Database Connection
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(spreadsheet=sheet_url, ttl="5m") # 5 min cache
    
    # Cleaning Column Names
    df.columns = df.columns.str.strip()
    
    # Aapke sheet ke hisaab se Aadhaar column ka naam (CrAadhaarNumber)
    target_col = 'CrAadhaarNumber' 
    
    if target_col in df.columns:
        # Aadhaar numbers ko clean karna
        df[target_col] = df[target_col].astype(str).str.replace(r'\s+|\.0$', '', regex=True)
        
        st.subheader("Beneficiary Search")
        search_query = st.text_input("12-digit Aadhaar Number enter karein:")

        if st.button("Check Status"):
            if search_query:
                clean_query = search_query.strip()
                result = df[df[target_col].str.contains(clean_query, na=False)]
                
                if not result.empty:
                    st.success("Record Found!")
                    st.dataframe(result, use_container_width=True, hide_index=True)
                else:
                    st.error("Is Aadhaar Number ka koi record nahi mila.")
            else:
                st.info("Kripya search karne ke liye Aadhaar number likhein.")
    else:
        st.error(f"Sheet mein '{target_col}' column nahi mila. Column ka naam check karein.")

except Exception as e:
    st.error(f"Error: Database connection failed. Link check karein.")

st.markdown("---")
st.caption("© 2026 District Administration, Chatra | Google Sheets Live Portal")
