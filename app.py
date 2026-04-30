import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# Page Config
st.set_page_config(page_title="JMMMSY Portal - Chatra", layout="wide")

# Google Sheet Link
sheet_url = "https://docs.google.com/spreadsheets/d/15YSpwWFlCG6XGXtTRUM6Kn5Cgl6pCFGDL24jWIMb7aI/edit?usp=sharing"

# Header Design
st.markdown("""
    <style>
    .header-box { background-color: #004a99; padding: 20px; border-radius: 10px; color: white; text-align: center; border-bottom: 5px solid #ff9933; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="header-box"><h1>झारखण्ड मुख्यमंत्री मइयां सम्मान योजना (JMMMSY)</h1><h3>District Administration - Chatra</h3></div>', unsafe_allow_html=True)

try:
    # Database Connection (Cache 2 min rakha hai taaki jaldi update ho)
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(spreadsheet=sheet_url, ttl="2m")
    
    # Cleaning Column Names
    df.columns = df.columns.str.strip()
    
    # Smart Column Finder (Ye line Aadhaar wala column apne aap dhoondh legi)
    target_col = next((col for col in df.columns if 'Aadhaar' in col or 'Aadhar' in col), None)
    
    if target_col:
        # Aadhaar numbers clean karna
        df[target_col] = df[target_col].astype(str).str.replace(r'\s+|\.0$', '', regex=True).str.replace("'", "", regex=False)
        
        st.subheader("Beneficiary Status Search")
        search_query = st.text_input("12-digit Aadhaar Number enter karein:")

        if st.button("Check Status"):
            if search_query:
                clean_query = search_query.strip()
                # Search Logic
                result = df[df[target_col].str.contains(clean_query, na=False)]
                
                if not result.empty:
                    st.success(f"Record Found!")
                    st.dataframe(result, use_container_width=True, hide_index=True)
                else:
                    st.error(f"Aadhaar '{clean_query}' ke liye koi record nahi mila.")
            else:
                st.warning("Kripya search karne ke liye number enter karein.")
    else:
        st.error("Sheet mein 'Aadhaar Number' wala column nahi mila. Kripya heading check karein.")

except Exception as e:
    st.error("Database Connection Error. Kripya Sheet ki privacy 'Anyone with link' check karein.")

st.markdown("---")
st.caption("© 2026 District Administration, Chatra | Google Sheets Live Portal")
