import streamlit as st
import pandas as pd

# Page setup
st.set_page_config(page_title="JMMMSY Chatra - Search", layout="centered")

# --- SHEET ID ---
SHEET_ID = "15YSpwWFICG6XGXtTRUM6Kn5Cgl6pCfGDL24jWlMb7aI"
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

# Header
st.markdown("<h2 style='text-align: center; color: #1e40af;'>झारखण्ड मुख्यमंत्री मईयां सम्मान योजना</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>District Administration - Chatra</p>", unsafe_allow_html=True)

# Data load karne ka function (Hidden from UI)
@st.cache_data(ttl=60)
def load_data():
    try:
        df = pd.read_csv(URL)
        # Columns ke naam se extra space hatane ke liye
        df.columns = df.columns.str.strip()
        return df
    except:
        return None

df = load_data()

# Search Box UI
st.write("---")
aadhaar_input = st.text_input("अपना 12 अंकों का आधार नंबर दर्ज करें (Enter Aadhaar Number):", placeholder="0000 0000 0000")

if aadhaar_input:
    if df is not None:
        # Yahan 'Aadhaar' ki jagah wahi naam likhein jo aapki excel sheet ke column ka hai
        # Hum maan kar chal rahe hain column ka naam 'Aadhaar Number' ya 'Aadhaar' hoga
        column_name = 'Aadhaar Number' # Agar aapki sheet mein sirf 'Aadhaar' hai toh ise badal dein
        
        if column_name not in df.columns:
            # Agar column name match nahi hua toh search as string karega
            result = df[df.astype(str).apply(lambda x: x.str.contains(aadhaar_input)).any(axis=1)]
        else:
            result = df[df[column_name].astype(str).str.contains(aadhaar_input)]

        if not result.empty:
            st.success("Record Mil Gaya!")
            # Detail ko Card format mein dikhane ke liye
            for i in range(len(result)):
                st.write(result.iloc[i])
                st.write("---")
        else:
            st.error("Is Aadhaar number se koi record nahi mila. Kripya check karein.")
    else:
        st.warning("Data fetch karne mein dikkat ho rahi hai. Sheet link check karein.")
else:
    st.info("Kripya search karne ke liye Aadhaar number upar box mein likhein.")

# Hide Streamlit Menu and Footer
hide_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_style, unsafe_allow_html=True)
