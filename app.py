import streamlit as st
import pandas as pd

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="JMMMSY Chatra - Payment Status", page_icon="🏛️", layout="wide")

# 2. CUSTOM CSS
custom_css = """
<style>
    .stApp { background-color: #f0f4f8; }
    .main-header {
        background: linear-gradient(135deg, #0d47a1 0%, #1976d2 100%);
        color: white; padding: 2.5rem 1rem; border-radius: 12px;
        text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.15); margin-bottom: 2rem;
    }
    .main-header h1 { margin: 0; font-size: 2.6rem; font-weight: 700; text-shadow: 1px 2px 3px rgba(0,0,0,0.3); }
    .main-header p { margin-top: 10px; font-size: 1.2rem; opacity: 0.95; }
    .beneficiary-card {
        background-color: white; padding: 25px; border-radius: 12px;
        box-shadow: 0 6px 12px rgba(0,0,0,0.1); margin-top: 20px; border-top: 5px solid #1976d2;
    }
    .section-title {
        color: #0d47a1; border-bottom: 2px solid #e0e0e0; padding-bottom: 8px;
        margin-bottom: 15px; font-size: 1.3rem; font-weight: 600;
    }
    .detail-row { margin-bottom: 12px; font-size: 1.05rem; color: #333; }
    .detail-label { font-weight: 600; color: #555; display: inline-block; width: 150px; }
    .success-text { color: #1b5e20; background-color: #e8f5e9; padding: 4px 10px; border-radius: 5px; font-weight: bold; border: 1px solid #c8e6c9; }
    .error-text { color: #b71c1c; background-color: #ffebee; padding: 4px 10px; border-radius: 5px; font-weight: bold; border: 1px solid #ffcdd2; }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# 3. DATABASE CONNECTION
SHEET_ID = "15YSpwWFICG6XGXtTRUM6Kn5Cgl6pCfGDL24jWlMb7aI"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

@st.cache_data(ttl=120)
def load_database():
    try:
        df = pd.read_csv(SHEET_URL)
        df.columns = df.columns.str.strip()
        df = df.fillna("N/A")
        return df
    except Exception as e:
        return None

df = load_database()

# 4. HEADER UI
header_html = """
<div class="main-header">
    <h1>झारखण्ड मुख्यमंत्री मईयां सम्मान योजना (JMMMSY)</h1>
    <p>District Administration, Chatra - Payment Status Portal</p>
</div>
"""
st.markdown(header_html, unsafe_allow_html=True)

# 5. MAIN LOGIC
if df is not None:
    # Top Stats
    col1, col2, col3 = st.columns(3)
    col1.metric(label="📊 Total Beneficiaries", value=f"{len(df):,}")
    col2.metric(label="📍 District", value="Chatra")
    col3.metric(label="🟢 Portal Status", value="Live / Active")

    st.write("---")

    # Search Bar
    st.markdown("### 🔍 लाभार्थी खोजें (Beneficiary Search)")
    search_query = st.text_input("Aadhaar Number (आधार नंबर) दर्ज करें:", placeholder="Enter 12-digit Aadhaar Number here...")

    if search_query:
        search_query = str(search_query).strip()
        aadhaar_col = "Aadhaar Number" if "Aadhaar Number" in df.columns else next((c for c in df.columns if 'aadhaar' in c.lower()), None)
        
        if not aadhaar_col:
            st.error("❌ Database mein 'Aadhaar Number' column nahi mila.")
        else:
            df[aadhaar_col] = df[aadhaar_col].astype(str).str.replace('.0', '', regex=False)
            result = df[df[aadhaar_col].str.contains(search_query, na=False, case=False)]

            if not result.empty:
                st.success(f"✅ {len(result)} रिकॉर्ड सफलतापूर्वक प्राप्त हुआ।")
                
                for index, row in result.iterrows():
                    name = row.get("ApplicantName", "N/A")
                    guardian = row.get("FatherHusbandN", "N/A")
                    aadhaar = str(row.get(aadhaar_col, "N/A")).replace("N/A", "")
                    dob = row.get("DateOfBirth", "N/A")
                    age = row.get("CurrentAge", "N/A")
                    bank = row.get("BankName", "N/A")
                    amount = row.get("Amount", "N/A")
                    ref_no = row.get("MMMSYRefNo", "N/A")
                    cpsms_id = row.get("CpsmsId", "N/A")
                    sanc_date = row.get("SanctionDate", "N/A")
                    category = row.get("Category", "N/A")
                    
                    raw_status = str(row.get("PAYMENT STATUS", "Pending")).strip()
                    if raw_status.lower() in ["success", "paid", "credited", "approved"]:
                        status_html = f"<span class='success-text'>{raw_status}</span>"
                    else:
                        status_html = f"<span class='error-text'>{raw_status}</span>"

                    masked_aadhaar = f"XXXXXXXX{aadhaar[-4:]}" if len(aadhaar) >= 4 else aadhaar

                    # Result Card UI built safely
                    card_html = f"""
                    <div class="beneficiary-card">
                        <div class="section-title">👤 Beneficiary Details (लाभार्थी का विवरण)</div>
                        <div style='display: flex; flex-wrap: wrap; gap: 30px;'>
                            <div style='flex: 1; min-width: 300px;'>
                                <div class="detail-row"><span class="detail-label">Name:</span> {name}</div>
                                <div class="detail-row"><span class="detail-label">Father/Husband:</span> {guardian}</div>
                                <div class="detail-row"><span class="detail-label">Aadhaar No:</span> {masked_aadhaar}</div>
                                <div class="detail-row"><span class="detail-label">Date of Birth:</span> {dob}</div>
                                <div class="detail-row"><span class="detail-label">Current Age:</span> {age}</div>
                                <div class="detail-row"><span class="detail-label">Category:</span> {category}</div>
                            </div>
                            <div style='flex: 1; min-width: 300px; background-color: #f9fbff; padding: 15px; border-radius: 8px; border: 1px solid #e3ebf6;'>
                                <div class="detail-row"><span class="detail-label">Payment Status:</span> {status_html}</div>
                                <div class="detail-row"><span class="detail-label">Amount:</span> ₹{amount}</div>
                                <div class="detail-row"><span class="detail-label">Bank Name:</span> {bank}</div>
                                <div class="detail-row"><span class="detail-label">CPSMS ID:</span> {cpsms_id}</div>
                                <div class="detail-row"><span class="detail-label">Ref Number:</span> {ref_no}</div>
                                <div class="detail-row"><span class="detail-label">Sanction Date:</span> {sanc_date}</div>
                            </div>
                        </div>
                    </div>
                    """
                    st.markdown(card_html, unsafe_allow_html=True)
            else:
                st.warning("⚠️ कोई रिकॉर्ड नहीं मिला। कृपया आधार नंबर दोबारा जाँचे।")
else:
    st.error("Database load karne mein error aa raha hai. Kripya apna Google Sheet link aur internet check karein.")

# 6. FOOTER
footer_html = """
<br><hr>
<div style='text-align: center; color: #7f8c8d; font-size: 0.9rem;'>
    © 2026 District Administration Chatra | Technical Cell<br>
    <i>Data is synced directly with official records</i>
</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)
