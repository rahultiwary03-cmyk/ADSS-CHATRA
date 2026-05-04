import streamlit as st
import pandas as pd
import time

# 1. Page Configuration
st.set_page_config(page_title="JMMSY | Official Portal", layout="wide", page_icon="🏛️")

# 2. Advanced Professional CSS (Full Website Look)
st.markdown("""
    <style>
    .stApp { background-color: #f0f2f5; }
    
    /* Official Header */
    .gov-banner {
        background: linear-gradient(135deg, #002e5d 0%, #004a99 100%);
        color: white; padding: 3rem; text-align: center;
        border-radius: 0 0 40px 40px; box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        margin-bottom: 2rem; border-bottom: 6px solid #ff9933;
    }

    /* Dashboard Stats */
    .metric-card {
        background: white; padding: 25px; border-radius: 20px;
        text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border-top: 5px solid #ff9933;
    }

    /* Professional Result Card */
    .profile-container {
        background: white; padding: 40px; border-radius: 30px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.1); margin-top: 30px;
        border: 1px solid #e2e8f0; animation: fadeInUp 0.8s ease-out;
    }
    
    .section-head {
        color: #002e5d; border-bottom: 2px solid #ff9933;
        padding-bottom: 10px; margin: 30px 0 20px 0; font-weight: 800;
        text-transform: uppercase; font-size: 1rem; letter-spacing: 1px;
    }

    .data-tile {
        background: #f8fafc; padding: 18px; border-radius: 12px;
        margin-bottom: 15px; border-left: 5px solid #002e5d;
    }
    .data-label { color: #64748b; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; margin-bottom: 5px; }
    .data-value { color: #1e293b; font-size: 1.1rem; font-weight: 700; }

    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .stButton>button {
        background: linear-gradient(90deg, #002e5d, #004a99) !important;
        color: white !important; width: 100%; border-radius: 12px !important;
        height: 55px; font-weight: bold; border: none; transition: 0.3s;
    }
    .stButton>button:hover { background: #ff9933 !important; transform: translateY(-2px); }
    </style>
    """, unsafe_allow_html=True)

# 3. Official Banner
st.markdown("""
    <div class='gov-banner'>
        <h1 style='margin:0;'>झारखण्ड मुख्यमंत्री मईयां सम्मान योजना (JMMSY)</h1>
        <p style='font-size: 1.3rem; opacity: 0.9; margin-top:10px;'>ज़िला प्रशासन, चतरा - आधिकारिक लाभार्थी डेटा एवं भुगतान सत्यापन पोर्टल</p>
    </div>
    """, unsafe_allow_html=True)

# 4. Data Connection & Analytics
SHEET_URL = "https://docs.google.com/spreadsheets/d/1fApqqsNEulpVsPH7O0IAMRvQv39DMYkV2PB_kg3qntg/export?format=csv"

@st.cache_data(ttl=60)
def fetch_portal_data():
