import streamlit as st
import pandas as pd

# Page setup
st.set_page_config(page_title="JMMMSY Chatra", layout="wide")

# --- UPDATE SHEET ID HERE ---
SHEET_ID = "15YSpwWFICG6XGXtTRUM6Kn5Cgl6pCfGDL24jWlMb7aI"
# ----------------------------

# CSV URL format
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

st.title("झारखण्ड मुख्यमंत्री मईयां सम्मान योजना - चतरा")

# Data fetch karne ka function
@st.cache_data(ttl=60)
def load_my_data():
    try:
        df = pd.read_csv(URL)
        return df
    except Exception as e:
        st.error("Data load nahi ho pa raha hai. Sheet ki 'Sharing' check karein.")
        return None

data = load_my_data()

if data is not None:
    st.success("Data successfully loaded!")
    # Search bar
    search = st.text_input("Search (Block/Panchayat)...")
    if search:
        data = data[data.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]
    
    st.dataframe(data, use_container_width=True)
