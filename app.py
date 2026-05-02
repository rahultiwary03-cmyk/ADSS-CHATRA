import streamlit as st
import pandas as pd

# ==========================================
# 1. PAGE CONFIGURATION & PROFESSIONAL UI CSS
# ==========================================
st.set_page_config(page_title="JMMMSY Chatra Portal", page_icon="🏛️", layout="wide")

st.markdown("""
    <style>
    /* Background and General Fonts */
    .stApp {
        background-color: #f4f6f9;
    }
    
    /* Modern Header */
    .main-header {
        background: linear-gradient(135deg, #003399 0%, #0055ff 100%);
        color: white;
        padding: 2.5rem 1rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
    }
    .main-header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
    }
    .main-header p {
        margin-top: 10px;
        font-size: 1.2rem;
        opacity: 0.9;
    }

    /* Metric Cards (Stats) */
    div[data-testid="metric-container"] {
        background-color: white;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        border-left: 5px solid #003399;
    }

    /* Search Result Card */
    .beneficiary-card {
        background-color: white;
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.08);
        margin-top: 15px;
        border-top: 4px solid #28a745;
    }
    
    /* Details inside card */
    .detail-row {
        margin-bottom: 10px;
        font-size: 1.05rem;
    }
    .detail-label {
        font-weight: 600;
        color: #555;
    }
    .success-text {
        color: #28a745;
        font-weight: bold;
    }
    .pending-text {
        color: #dc3545;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. DATABASE CONNECTION (GOOGLE SHEETS)
# ==========================================
# Aapka provided Google Sheet link (Direct CSV export link for pandas)
SHEET_ID = "15YSpwWFICG6XGXtTRUM6Kn5Cgl6pCfGDL24jWlMb7aI"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

@st.cache_data(ttl=300) # Data har 5 minute mein refresh hoga
def load_database():
    try:
        df = pd.read_csv(SHEET_URL)
        # Columns ke aage-peeche ke extra spaces hatana (To prevent KeyError)
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error("⚠️ Database se connect karne mein samasya aa rahi hai. Kripya internet connection check karein.")
        return None

df = load_database()

# ==========================================
# 3. WEBSITE LAYOUT & LOGIC
# ==========================================

# Custom Header
st.markdown("""
    <div class="main-header">
        <h1>झारखण्ड मुख्यमंत्री मईयां सम्मान योजना (JMMMSY)</h1>
        <p>District Administration, Chatra - Official Payment Status Portal</p>
    </div>
""", unsafe_allow_html=True)

if df is not None:
    # Top Statistics Row
    col1, col2, col3 = st.columns(3)
    col1.metric(label="📊 Total Registered Beneficiaries", value=f"{len(df):,}")
    col2.metric(label="📍 District", value="Chatra")
    col3.metric(label="🟢 Portal Status", value="Active / Live")

    st.write("---")

    # Search Section
    st.markdown("### 🔍 लाभार्थी की स्थिति खोजें (Beneficiary Search)")
    
    # User Input
    search_query = st.text_input("Aadhaar Number (आधार नंबर) दर्ज करें:", placeholder="Enter 12-digit Aadhaar Number here...")

    if search_query:
        search_query = str(search_query).strip()

        # ---------------------------------------------------------
        # SMART COLUMN DETECTION (Taaki KeyError na aaye)
        # ---------------------------------------------------------
        aadhaar_col = next((col for col in df.columns if 'aadhaar' in col.lower() or 'aadhar' in col.lower()), None)
        
        if not aadhaar_col:
            st.error(f"Database mein 'Aadhaar' naam ka koi column nahi mila. Yeh columns available hain: {', '.join(df.columns)}")
        else:
            # Search execution
            result = df[df[aadhaar_col].astype(str).str.contains(search_query, na=False)]

            if not result.empty:
                st.success(f"✅ कुल {len(result)} रिकॉर्ड सफलतापूर्वक मिले।")
                
                # Display Results
                for index, row in result.iterrows():
                    # Smart variables: Jo available hai wahi uthayega, nahi toh "N/A"
                    name = row.get("ApplicantName", row.get("Name", "N/A"))
                    guardian = row.get("FatherHusbandN", row.get("GuardianName", "N/A"))
                    aadhaar = row.get(aadhaar_col, "N/A")
                    bank = row.get("BankName", "N/A")
                    amount = row.get("Amount", 0)
                    ref_no = row.get("MMMSYRefNo", "N/A")
                    category = row.get("Category", "N/A")
                    
                    status_html = "<span class='success-text'>SUCCESS</span>" if pd.to_numeric(amount, errors='coerce') > 0 else "<span class='pending-text'>PENDING</span>"

                    # Beautiful Result Card HTML
                    st.markdown(f"""
                        <div class="beneficiary-card">
                            <h4 style='color: #003399; border-bottom: 1px solid #eee; padding-bottom: 10px; margin-bottom: 15px;'>
                                👤 Beneficiary Details
                            </h4>
                            <div style='display: flex; flex-wrap: wrap; gap: 20px;'>
                                <div style='flex: 1; min-width: 250px;'>
                                    <div class="detail-row"><span class="detail-label">Name:</span> {name}</div>
                                    <div class="detail-row"><span class="detail-label">Father/Husband:</span> {guardian}</div>
                                    <div class="detail-row"><span class="detail-label">Aadhaar No:</span> XXXXXXXX{str(aadhaar)[-4:] if len(str(aadhaar)) >= 4 else aadhaar}</div>
                                    <div class="detail-row"><span class="detail-label">Category:</span> {category}</div>
                                </div>
                                <div style='flex: 1; min-width: 250px;'>
                                    <div class="detail-row"><span class="detail-label">Bank Name:</span> {bank}</div>
                                    <div class="detail-row"><span class="detail-label">Payment Status:</span> {status_html}</div>
                                    <div class="detail-row"><span class="detail-label">Amount:</span> ₹{amount}</div>
                                    <div class="detail-row"><span class="detail-label">Ref Number:</span> {ref_no}</div>
                                </div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("⚠️ कोई रिकॉर्ड नहीं मिला। कृपया अपना आधार नंबर दोबारा जाँचे।")

else:
    st.info("⏳ Database Load ho raha hai, kripya pratiksha karein...")

# Footer
st.markdown("""
    <br><br>
    <div style='text-align: center; color: #888; font-size: 0.9rem;'>
        © 2026 District Administration Chatra | Developed for Block Office Operations<br>
        <i>Data automatically synced with Google Sheets Permanent Database</i>
    </div>
""", unsafe_allow_html=True)
