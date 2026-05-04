import streamlit as st
import pandas as pd
import time
from datetime import datetime

# ==========================================
# 1. PAGE CONFIGURATION & PREMIUM CSS
# ==========================================
st.set_page_config(page_title="JMMSY | Official Portal", layout="wide", page_icon="🏛️")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #f8fafc; }
    
    /* Official Header Banner */
    .gov-banner {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: white; padding: 2.5rem; text-align: center;
        border-radius: 0 0 20px 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        margin-bottom: 2rem; border-bottom: 4px solid #eab308;
    }
    
    /* Dashboard Cards */
    .dash-card {
        background: white; padding: 20px; border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); text-align: center;
        border-top: 4px solid #3b82f6;
    }
    
    /* Profile Sections */
    .section-title {
        color: #0f172a; border-bottom: 2px solid #e2e8f0;
        padding-bottom: 8px; margin: 25px 0 15px 0; font-weight: 700;
        text-transform: uppercase; font-size: 1rem;
    }
    
    .data-grid { display: flex; flex-wrap: wrap; gap: 15px; }
    
    .data-box {
        background: #ffffff; padding: 12px 15px; border-radius: 8px;
        border: 1px solid #e2e8f0; flex: 1 1 calc(25% - 15px);
        min-width: 200px; border-left: 4px solid #3b82f6;
    }
    
    .lbl { color: #64748b; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; margin-bottom: 4px; }
    .val { color: #0f172a; font-size: 1.05rem; font-weight: 700; word-wrap: break-word; }
    
    /* Status Tags */
    .tag-success { color: #166534; background: #dcfce7; padding: 4px 10px; border-radius: 6px; font-size: 0.9rem; }
    .tag-danger { color: #991b1b; background: #fee2e2; padding: 4px 10px; border-radius: 6px; font-size: 0.9rem; }
    .tag-warning { color: #854d0e; background: #fef08a; padding: 4px 10px; border-radius: 6px; font-size: 0.9rem; }
    
    /* Search Button */
    .stButton>button {
        background: #1e293b !important; color: white !important;
        width: 100%; border-radius: 8px !important; height: 50px;
        font-weight: 600; border: none; font-size: 1.1rem; transition: 0.2s;
    }
    .stButton>button:hover { background: #eab308 !important; color: #0f172a !important; }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] { justify-content: center; gap: 20px; }
    .stTabs [data-baseweb="tab"] { font-size: 1.1rem; font-weight: 600; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. HEADER
# ==========================================
st.markdown("""
    <div class='gov-banner'>
        <h1 style='margin:0; letter-spacing: 0.5px;'>झारखण्ड मुख्यमंत्री मईयां सम्मान योजना (JMMSY)</h1>
        <p style='font-size: 1.1rem; opacity: 0.8; margin-top:8px;'>ज़िला प्रशासन, चतरा - एकीकृत लाभार्थी डैशबोर्ड</p>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 3. ROBUST DATA ENGINE (Failsafe Loading)
# ==========================================
SHEET_URL = "https://docs.google.com/spreadsheets/d/1fApqqsNEulpVsPH7O0IAMRvQv39DMYkV2PB_kg3qntg/export?format=csv"

@st.cache_data(ttl=60)
def load_and_clean_data():
    try:
        df = pd.read_csv(SHEET_URL)
        # Clean all column headers to uppercase for foolproof matching
        df.columns = df.columns.str.strip().str.upper()
        
        # Smart Aadhar Extractor (Removes all spaces, letters, decimals)
        uid_cols = [c for c in df.columns if 'AADHAAR' in c or 'AADHAR' in c or 'UID' in c]
        if uid_cols:
            main_uid_col = uid_cols[0]
            df['SEARCH_KEY'] = df[main_uid_col].astype(str).str.replace(r'\D', '', regex=True)
        else:
            df['SEARCH_KEY'] = ""
            
        return df
    except Exception as e:
        return None

df = load_and_clean_data()

# Helper function to safely fetch data regardless of exact spelling in Excel
def get_val(row, possible_cols, default="N/A"):
    for col in possible_cols:
        col_upper = col.upper()
        if col_upper in row.index and pd.notna(row[col_upper]):
            val = str(row[col_upper]).strip()
            # Remove .0 from numbers
            if val.endswith('.0'): val = val[:-2]
            return val if val else default
    return default

# ==========================================
# 4. PORTAL TABS
# ==========================================
tab1, tab2, tab3 = st.tabs(["🔍 लाभार्थी खोजें", "📊 लाइव डैशबोर्ड", "📞 सहायता एवं संपर्क"])

# ------------------------------------------
# TAB 1: ADVANCED PROFILE SEARCH
# ------------------------------------------
with tab1:
    st.write("")
    _, search_col, _ = st.columns([1, 2, 1])
    with search_col:
        search_input = st.text_input("Aadhar", placeholder="यहाँ 12 अंकों का आधार संख्या दर्ज करें...", label_visibility="collapsed")
        search_btn = st.button("सत्यापन प्रारंभ करें")

    if search_btn or search_input:
        if df is not None:
            clean_input = ''.join(filter(str.isdigit, str(search_input)))
            
            if len(clean_input) > 0:
                match = df[df['SEARCH_KEY'] == clean_input]
                
                if not match.empty:
                    st.toast('लाभार्थी का डेटा प्राप्त हुआ!', icon='✅')
                    row = match.iloc[0]
                    
                    # Fetching all 18+ Columns Safely
                    name = get_val(row, ['APPLICANT', 'APPLICANTNAME', 'NAME'])
                    fname = get_val(row, ["FATHER'S/HUSBAND NAME", "FATHER NAME", "HUSBAND NAME"])
                    dob = get_val(row, ['DATEOFBIRTH', 'DOB'])
                    age = get_val(row, ['AGE', 'CURRENTAGE'])
                    cat = get_val(row, ['CATEGORY'])
                    
                    dist = get_val(row, ['DISTRICT', 'DISTRICTNAME'], "CHATRA")
                    block = get_val(row, ['BLOCK', 'BLOCKNAME'])
                    panchayat = get_val(row, ['PANCHAYAT', 'PANCHAYATNAME'])
                    village = get_val(row, ['VILLAGE', 'VILLAGENAME'])
                    
                    bank = get_val(row, ['BANKNAME', 'BANK'])
                    acc = get_val(row, ['ACCOUNT NUMBER', 'ACCOUNTNO', 'ACCOUNT'])
                    acc_masked = f"XXXXXX{acc[-4:]}" if len(acc) > 4 else acc
                    ifsc = get_val(row, ['IFSC', 'IFSCCODE'])
                    
                    ref_no = get_val(row, ['MMMSYREFNO', 'REFNO'])
                    sanc_no = get_val(row, ['SANCTIONNO'])
                    amount = get_val(row, ['AMOUNT'])
                    
                    pds = get_val(row, ['PDS_STATUS', 'PDS STATUS'])
                    pay = get_val(row, ['PAYMENT STATUS', 'STATUS'])

                    # UI Render - Professional Grid
                    st.markdown("<div style='background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); border: 1px solid #e2e8f0; margin-top: 20px;'>", unsafe_allow_html=True)
                    st.markdown(f"<h2 style='text-align:center; color:#0f172a; margin-bottom: 30px;'>✅ सत्यापित लाभार्थी: {name}</h2>", unsafe_allow_html=True)
                    
                    # 1. Identity Details
                    st.markdown("<div class='section-title'>👤 व्यक्तिगत विवरण (Identity)</div>", unsafe_allow_html=True)
                    st.markdown(f"""
                        <div class='data-grid'>
                            <div class='data-box'><div class='lbl'>आवेदिका का नाम</div><div class='val'>{name}</div></div>
                            <div class='data-box'><div class='lbl'>पिता/पति का नाम</div><div class='val'>{fname}</div></div>
                            <div class='data-box'><div class='lbl'>आधार संख्या</div><div class='val'>XXXX-XXXX-{clean_input[-4:]}</div></div>
                            <div class='data-box'><div class='lbl'>जन्म तिथि / उम्र</div><div class='val'>{dob} ({age} वर्ष)</div></div>
                            <div class='data-box'><div class='lbl'>श्रेणी (Category)</div><div class='val'>{cat}</div></div>
                        </div>
                    """, unsafe_allow_html=True)

                    # 2. Location Details
                    st.markdown("<div class='section-title'>📍 आवासीय पता (Location)</div>", unsafe_allow_html=True)
                    st.markdown(f"""
                        <div class='data-grid'>
                            <div class='data-box'><div class='lbl'>ज़िला</div><div class='val'>{dist}</div></div>
                            <div class='data-box'><div class='lbl'>प्रखंड (Block)</div><div class='val'>{block}</div></div>
                            <div class='data-box'><div class='lbl'>पंचायत</div><div class='val'>{panchayat}</div></div>
                            <div class='data-box'><div class='lbl'>गांव</div><div class='val'>{village}</div></div>
                        </div>
                    """, unsafe_allow_html=True)

                    # 3. Scheme & Bank Details
                    st.markdown("<div class='section-title'>🏦 योजना एवं बैंक विवरण (Scheme & Financials)</div>", unsafe_allow_html=True)
                    st.markdown(f"""
                        <div class='data-grid'>
                            <div class='data-box'><div class='lbl'>आवेदन क्र. (Ref No)</div><div class='val'>{ref_no}</div></div>
                            <div class='data-box'><div class='lbl'>स्वीकृति क्र. (Sanction No)</div><div class='val'>{sanc_no}</div></div>
                            <div class='data-box'><div class='lbl'>स्वीकृत राशि</div><div class='val'>₹{amount}</div></div>
                            <div class='data-box'><div class='lbl'>बैंक का नाम</div><div class='val'>{bank}</div></div>
                            <div class='data-box'><div class='lbl'>खाता संख्या</div><div class='val'>{acc_masked}</div></div>
                            <div class='data-box'><div class='lbl'>IFSC कोड</div><div class='val'>{ifsc}</div></div>
                        </div>
                    """, unsafe_allow_html=True)

                    # 4. Status Details
                    st.markdown("<div class='section-title'>📊 वर्तमान स्थिति (Current Status)</div>", unsafe_allow_html=True)
                    
                    pay_class = "tag-success" if "success" in pay.lower() or "paid" in pay.lower() else ("tag-warning" if "pending" in pay.lower() else "tag-danger")
                    
                    st.markdown(f"""
                        <div class='data-grid'>
                            <div class='data-box' style='border-left-color: #eab308;'><div class='lbl'>PDS Status</div><div class='val'>{pds}</div></div>
                            <div class='data-box' style='border-left-color: #3b82f6;'><div class='lbl'>Payment Status</div><div class='val'><span class='{pay_class}'>{pay}</span></div></div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Live Progress
                    st.write("")
                    st.caption("भुगतान प्रक्रिया (Payment Progress)")
                    st.progress(100 if "success" in pay.lower() else (50 if "pending" in pay.lower() else 20))

                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.error("❌ यह आधार नंबर डेटाबेस में उपलब्ध नहीं है। कृपया संख्या जाँचें।")
        else:
            st.warning("⚠️ डेटाबेस सर्वर से संपर्क नहीं हो पा रहा है।")

# ------------------------------------------
# TAB 2: LIVE ANALYTICS DASHBOARD
# ------------------------------------------
with tab2:
    if df is not None:
        st.markdown("<h3 style='color:#0f172a; margin-bottom: 20px;'>📊 ज़िला स्तरीय आँकड़े (Chatra)</h3>", unsafe_allow_html=True)
        
        # Real-time calculations from Excel
        tot = len(df)
        pay_cols = [c for c in df.columns if 'PAYMENT' in c or 'STATUS' in c]
        if pay_cols:
            status_series = df[pay_cols[0]].astype(str).str.lower()
            succ = len(status_series[status_series.str.contains('success|paid')])
            fail = len(status_series[status_series.str.contains('fail|reject|blocked')])
            pend = tot - (succ + fail)
            
            c1, c2, c3, c4 = st.columns(4)
            c1.markdown(f"<div class='dash-card' style='border-color:#3b82f6;'><div class='lbl'>कुल लाभार्थी</div><div class='val' style='font-size:2rem;'>{tot:,}</div></div>", unsafe_allow_html=True)
            c2.markdown(f"<div class='dash-card' style='border-color:#22c55e;'><div class='lbl'>सफल भुगतान</div><div class='val' style='font-size:2rem; color:#166534;'>{succ:,}</div></div>", unsafe_allow_html=True)
            c3.markdown(f"<div class='dash-card' style='border-color:#eab308;'><div class='lbl'>लंबित (Pending)</div><div class='val' style='font-size:2rem; color:#854d0e;'>{pend:,}</div></div>", unsafe_allow_html=True)
            c4.markdown(f"<div class='dash-card' style='border-color:#ef4444;'><div class='lbl'>विफल (Failed)</div><div class='val' style='font-size:2rem; color:#991b1b;'>{fail:,}</div></div>", unsafe_allow_html=True)
            
            st.info("💡 **नोट:** यह डेटा सीधे Excel शीट से रीयल-टाइम में सिंक किया जा रहा है।")
    else:
        st.error("डेटा लोड हो रहा है...")

# ------------------------------------------
# TAB 3: HELPDESK (UPDATED)
# ------------------------------------------
with tab3:
    st.markdown("""
        <div style='background: white; padding: 40px; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); border: 1px solid #e2e8f0; text-align: center;'>
            <h2 style='color: #0f172a; margin-bottom: 20px;'>📞 सहायता एवं संपर्क</h2>
            <img src="https://cdn-icons-png.flaticon.com/512/4144/4144781.png" width="80" style="margin-bottom:20px;">
            <h4 style='color: #3b82f6; margin-bottom: 10px;'>किसी भी प्रकार की तकनीकी सहायता या भुगतान विफलता की स्थिति में:</h4>
            <h3 style='color: #ef4444; background: #fee2e2; padding: 15px; border-radius: 8px; display: inline-block;'>
                "कार्यालय सामाजिक सुरक्षा कोषांग, चतरा से संपर्क करें"<br>
                <span style='font-size: 1rem; color: #991b1b;'>(Office social security office chatra se sampark kren)</span>
            </h3>
            <p style='margin-top: 20px; color: #64748b;'>यदि आपका भुगतान लंबित है, तो अपनी बैंक शाखा में जाकर अपना <b>Aadhaar NPCI Link</b> (DBT) सुनिश्चित करें।</p>
        </div>
    """, unsafe_allow_html=True)

# ==========================================
# 5. OFFICIAL FOOTER
# ==========================================
st.markdown("<br><br><hr><center style='color:#94a3b8; font-size:0.85rem;'><b>Digital India Initiative</b> | © 2026 District Administration Chatra | Powered by National Informatics Centre (NIC)</center>", unsafe_allow_html=True)
