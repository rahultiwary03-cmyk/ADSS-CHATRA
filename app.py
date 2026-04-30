import streamlit as st
import pandas as pd

# 1. Page Configuration (Professional Look)
st.set_page_config(page_title="JMMMSY Payment Status Portal", page_icon="🏦", layout="wide")

# 2. Custom CSS for Government Blue Theme
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { width: 100%; background-color: #004a99; color: white; border-radius: 5px; font-weight: bold; }
    .header-box { background-color: #004a99; padding: 25px; border-radius: 10px; color: white; text-align: center; margin-bottom: 30px; border-bottom: 5px solid #ff9933; }
    .metric-card { background-color: white; padding: 15px; border-radius: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# 3. Header Section
st.markdown('<div class="header-box"><h1>झारखण्ड मुख्यमंत्री मइयां सम्मान योजना (JMMMSY)</h1><h3>District Administration - Official Payment Status Portal</h3></div>', unsafe_allow_html=True)

# 4. Sidebar for Admin Access
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/b/bb/Emblem_of_Jharkhand.svg/1200px-Emblem_of_Jharkhand.svg.png", width=100)
    st.title("Admin Panel")
    st.write("---")
    admin_password = st.text_input("Office Password Enter Karein", type="password")
    
    # Password check to show upload option
    if admin_password == "Admin@JPSC": 
        st.success("Access Granted!")
        uploaded_file = st.file_uploader("Upload Master Database (Excel)", type=["xlsx", "xls"])
        if uploaded_file:
            try:
                data = pd.read_excel(uploaded_file)
                # Clean column names immediately
                data.columns = data.columns.str.strip()
                st.session_state['master_data'] = data
                st.success("Database Updated Successfully!")
            except Exception as e:
                st.error(f"Error: {e}")
    elif admin_password != "":
        st.error("Incorrect Password")

# 5. Main Search Logic
if 'master_data' in st.session_state:
    df = st.session_state['master_data']
    
    # Target Column Name (As per your Excel screenshot)
    target_col = 'Aadhaar Number'
    
    if target_col not in df.columns:
        st.error(f"Excel mein '{target_col}' naam ka column nahi mila!")
    else:
        # Pre-cleaning the data for better search
        df[target_col] = (
            df[target_col]
            .astype(str)
            .str.replace("'", "", regex=False)
            .str.replace(r'\s+', '', regex=True)
            .str.replace(r'\.0$', '', regex=True)
            .str.strip()
        )

        col1, col2 = st.columns([2, 1])

        with col1:
            st.subheader("Beneficiary Search")
            search_query = st.text_input("12-digit Aadhaar Number enter karein:", placeholder="Example: 552387299348")
            
            if st.button("Check Status"):
                if search_query:
                    clean_query = search_query.strip().replace(" ", "")
                    # Search using contains to be safe
                    result = df[df[target_col].str.contains(clean_query, na=False)]
                    
                    if not result.empty:
                        st.balloons()
                        res = result.iloc[0]
                        
                        # Result Dashboard
                        st.markdown("---")
                        r_col1, r_col2, r_col3 = st.columns(3)
                        with r_col1:
                            st.info(f"*Beneficiary Name*\n\n{res.get('ApplicantName', 'N/A')}")
                        with r_col2:
                            st.info(f"*Payment Status*\n\n{res.get('PDS_Status', 'In Progress')}")
                        with r_col3:
                            st.info(f"*Amount*\n\n₹ {res.get('Amount', '1000')}")
                        
                        st.write("### Complete Details:")
                        st.dataframe(result, use_container_width=True, hide_index=True)
                    else:
                        st.warning(f"Aadhaar '{clean_query}' ke liye koi record nahi mila.")
                else:
                    st.info("Kripya search karne ke liye Aadhaar Number likhein.")
        
        with col2:
            st.write("### Instructions")
            st.markdown("""
            1. *Search:* Beneficiary ka 12-digit Aadhaar bina space ke enter karein.
            2. *Verification:* Details verify karne ke baad payment status block ko report karein.
            3. *Print:* Record milne par aap result ka screenshot le sakte hain.
            """)
else:
    # Information for users when no data is loaded
    st.warning("⚠️ *Database Not Found:* Kripya pehle Sidebar mein Admin Password dalkar Master Excel file upload karein.")
    st.info("Note: Ye portal Block aur Panchayat officers ke liye payment status check karne ke liye banaya gaya hai.")

# 6. Footer
st.markdown("---")
st.caption("© 2026 District Administration - Chatra, Jharkhand | Designed for JMMMSY Operations")