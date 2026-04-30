import streamlit as st
import pandas as pd

# Page Config
st.set_page_config(page_title="JMMMSY Portal - Chatra", layout="wide")

# Google Sheet CSV Link (Ye link hamesha kaam karta hai)
# Maine aapki sheet ID use ki hai jo screenshots mein dikh rahi thi
sheet_id = "15YSpwWFlCG6XGXtTRUM6Kn5Cgl6pCFGDL24jWIMb7aI"
csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

# Header Design
st.markdown("""
    <style>
    .header-box { background-color: #004a99; padding: 20px; border-radius: 10px; color: white; text-align: center; border-bottom: 5px solid #ff9933; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="header-box"><h1>झारखण्ड मुख्यमंत्री मइयां सम्मान योजना (JMMMSY)</h1><h3>District Administration - Chatra</h3></div>', unsafe_allow_html=True)

@st.cache_data(ttl=300) # 5 minute tak data yaad rakhega
def load_data(url):
    try:
        # Seedha CSV format mein read karein (Isme koi extra library nahi chahiye)
        data = pd.read_csv(url)
        return data
    except Exception as e:
        return None

df = load_data(csv_url)

if df is not None:
    # Column names saaf karein
    df.columns = df.columns.str.strip()
    
    # Aadhaar column dhoondhein
    target_col = next((col for col in df.columns if 'Aadhaar' in col or 'Aadhar' in col or 'CrAadhaar' in col), None)
    
    if target_col:
        # Data clean karein
        df[target_col] = df[target_col].astype(str).str.replace(r'\s+|\.0$', '', regex=True)
        
        st.subheader("Beneficiary Search")
        search_query = st.text_input("12-digit Aadhaar Number enter karein:", placeholder="Yahan Aadhaar likhein...")

        if st.button("Check Status"):
            if search_query:
                clean_query = search_query.strip()
                result = df[df[target_col].str.contains(clean_query, na=False)]
                
                if not result.empty:
                    st.success("Record Found!")
                    st.dataframe(result, use_container_width=True, hide_index=True)
                else:
                    st.error(f"Record nahi mila. Kripya check karein.")
            else:
                st.info("Search karne ke liye Aadhaar number enter karein.")
    else:
        st.error("Google Sheet mein 'Aadhaar Number' wala column nahi mil raha.")
else:
    st.error("Google Sheet se connect nahi ho pa raha. Kripya check karein ki Sheet 'Anyone with the link' par set hai.")

st.markdown("---")
st.caption("© 2026 District Administration, Chatra | Live Database Portal")
