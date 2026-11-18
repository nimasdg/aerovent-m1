import streamlit as st
import base64
import os

# --- CONFIGURATION ---
st.set_page_config(page_title="Aerivo Medical | Portable Ventilation", layout="wide", initial_sidebar_state="collapsed")

# --- UTILITY: IMAGE TO BASE64 FOR BACKGROUND ---
@st.cache_data
def get_base64_of_bin_file(bin_file):
    if os.path.exists(bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return ""

# --- SESSION STATE ---
if 'language' not in st.session_state:
    st.session_state.language = None
if 'cart' not in st.session_state:
    st.session_state.cart = []

# --- CORE CSS (APPLIED TO ALL PAGES) ---
st.markdown("""
    <style>
    h1, h2, h3, h4 { color: #1F3B63; font-weight: 700; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .hero-subtitle { font-size: 1.5rem; color: #4F86C6; margin-bottom: 2rem; }
    
    /* Premium Buttons */
    .stButton>button { 
        background-color: #5BB3A8; color: #FFFFFF; font-weight: bold; border-radius: 8px; border: none; 
        padding: 0.8rem 2rem; transition: all 0.3s ease; box-shadow: 0 4px 12px rgba(91, 179, 168, 0.2);
    }
    .stButton>button:hover { 
        background-color: #1F3B63; color: #FFFFFF; transform: translateY(-2px); box-shadow: 0 6px 15px rgba(31, 59, 99, 0.3);
    }
    
    .price-tag { font-size: 2rem; color: #4F86C6; font-weight: bold; margin: 1rem 0; }
    .cert-badge { display: inline-block; background-color: #DCE9F7; color: #1F3B63; padding: 0.5rem 1rem; border-radius: 4px; font-weight: bold; margin-right: 1rem; font-size: 0.9rem;}
    .feature-box { border-left: 4px solid #5BB3A8; padding-left: 1rem; margin-bottom: 1.5rem; color: #1F3B63; }
    .rtl-feature-box { border-right: 4px solid #5BB3A8; padding-right: 1rem; margin-bottom: 1.5rem; direction: rtl; text-align: right; color: #1F3B63; }
    hr { border-top: 1px solid rgba(79, 134, 198, 0.2); }
    </style>
""", unsafe_allow_html=True)

# --- COMPONENTS ---
def render_navbar():
    col1, col2, col3 = st.columns([1, 4, 1])
    with col1:
        st.markdown("<h3 style='color: #4F86C6; margin:0;'>⚕️ Aerivo Medical</h3>", unsafe_allow_html=True)
    with col3:
        if st.button("🌐 Change Region"):
            st.session_state.language = None
            st.rerun()
    st.markdown("<hr>", unsafe_allow_html=True)

def render_album_gallery():
    st.markdown("<br><hr><br>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Aerivo M1 Environments & Details</h3>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["🏥 Clinical Settings", "🚁 Transport & Emergency", "⚙️ Product Details"])
    
    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            try: st.image("Aerivo (8).png", caption="ICU Clinical Setting", use_container_width=True)
            except: pass
        with c2:
            try: st.image("Aerivo (9).png", caption="Operating Room Configuration", use_container_width=True)
            except: pass
            
    with tab2:
        c1, c2, c3 = st.columns(3)
        with c1:
            try: st.image("Aerivo (10).png", caption="Ambulance Installation", use_container_width=True)
            except: pass
        with c2:
            try: st.image("Aerivo (11).png", caption="Helicopter Emergency Services", use_container_width=True)
            except: pass
        with c3:
            try: st.image("Aerivo (2).png", caption="Field & Disaster Care", use_container_width=True)
            except: pass
            
    with tab3:
        c1, c2, c3 = st.columns(3)
        with c1:
            try: st.image("Aerivo (3).png", caption="Front Control Panel & UI", use_container_width=True)
            except: pass
        with c2:
            try: st.image("Aerivo (4).png", caption="Rear View & Connectivity Ports", use_container_width=True)
            except: pass
        with c3:
            try: st.image("Aerivo (5).png", caption="Accessories & Travel Kit", use_container_width=True)
            except: pass

# --- REGIONAL PAGES ---
def render_main_product_image():
    try:
        st.image("Aerivo (6).png", use_container_width=True)
    except:
        st.info("Please upload 'Aerivo (6).png' to GitHub.")

def page_english_global():
    render_navbar()
    col_text, col_img = st.columns([1, 1], gap="large")
    with col_text:
        st.markdown("<h1>Aerivo M1 Portable Ventilator</h1>", unsafe_allow_html=True)
        st.markdown("<div class='hero-subtitle'>Intelligent Ventilation, Anywhere You Need It.</div>", unsafe_allow_html=True)
        st.markdown("""
        <div class='feature-box'>
            <b>Uncompromising Performance</b><br>
            Delivering ICU-level ventilation in a compact, ruggedized transport housing. Suitable for neonates to adults.
        </div>
        <div class='feature-box'>
            <b>Continuous Operation</b><br>
            Up to 9 hours of battery life with hot-swappable dual battery technology.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div class='price-tag'>$15,500.00 USD</div>", unsafe_allow_html=True)
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("Add to Cart", use_container_width=True):
                st.session_state.cart.append("Aerivo M1")
                st.success("Added to secure cart.")
        with col_btn2:
            st.button("View Technical Specs", use_container_width=True)
            
    with col_img:
        render_main_product_image()
        
    render_album_gallery()

def page_german():
    render_navbar()
    col_text, col_img = st.columns([1, 1], gap="large")
    with col_text:
        st.markdown("<h1>Aerivo M1: Präzision und Sicherheit</h1>", unsafe_allow_html=True)
        st.markdown("<div class='hero-subtitle'>Mobiles Beatmungssystem für die Intensivmedizin</div>", unsafe_allow_html=True)
        
        st.markdown("""
        <div style='margin-bottom: 1.5rem;'>
            <span class='cert-badge'>🇪🇺 CE Zertifiziert</span>
            <span class='cert-badge'>📋 EU MDR Konform</span>
            <span class='cert-badge'>⚙️ ISO 13485:2016</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='feature-box'>
            <b>Zuverlässigkeit im Einsatz (MTBF > 50.000h)</b><br>
            Entwickelt für maximale Ausfallsicherheit im klinischen und präklinischen Einsatz. Getestet durch unabhängige benannte Stellen.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div class='price-tag'>14.200 €</div>", unsafe_allow_html=True)
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            st.button("Offizielles Angebot anfordern", use_container_width=True)
        with col_btn2:
            st.button("📄 Datenblatt (PDF)", use_container_width=True)
            
    with col_img:
        render_main_product_image()

    st.markdown("<br><hr>", unsafe_allow_html=True)
    st.markdown("<h3>Klinische Spezifikationen & Rahmenverträge</h3>", unsafe_allow_html=True)
    st.info("Zugelassen für die Beschaffung über Prospitalia, Sana und GDEKK Einkaufsverbünde. Vollständige Integration in DRG-Abrechnungssysteme.")
        
    render_album_gallery()

def page_arabic():
    render_navbar()
    st.markdown("<div style='direction: rtl; text-align: right; font-family: Arial;'>", unsafe_allow_html=True)
    
    col_img, col_text = st.columns([1, 1], gap="large")
    with col_text:
        st.markdown("<h1 style='direction: rtl; text-align: right;'>أيريفو M1: شريكك الموثوق في العناية المركزة</h1>", unsafe_allow_html=True)
        st.markdown("<div class='hero-subtitle' style='direction: rtl; text-align: right;'>تكنولوجيا التنفس الصناعي المتقدمة، بين يديك.</div>", unsafe_allow_html=True)
        
        st.success("مُعتمد رسمياً ومسجل لدى وزارة الصحة العراقية (MOH) ومطابق لمواصفات الشركة العامة لتسويق الأدوية والمستلزمات الطبية (KIMADIA).")
        
        st.markdown("""
        <div class='rtl-feature-box'>
            <b>دعم شامل وتدريب مستمر</b><br>
            نحن لا نبيع جهازاً فقط، بل نبني شراكة طويلة الأمد. نوفر تدريباً حضورياً شاملاً للكوادر الطبية لضمان الاستخدام الأمثل.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div class='price-tag' style='direction: rtl; text-align: right;'>$15,500.00 USD</div>", unsafe_allow_html=True)
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn2:
            st.button("تحدث مع خبير المبيعات (WhatsApp) 💬", use_container_width=True)
        with col_btn1:
            st.button("طلب عرض سعر للمناقصات", use_container_width=True)
            
    with col_img:
        render_main_product_image()
        
    st.markdown("</div>", unsafe_allow_html=True)
    
    render_album_gallery()

# --- ROUTER & CONDITIONAL CSS ---
if st.session_state.language is None:
    # 1. GENERATE BACKGROUND FOR GATEWAY
    bg_base64 = get_base64_of_bin_file("Aerivo (7).png")
    
    # 2. INJECT FULL-SCREEN CSS
    st.markdown(f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(240, 244, 248, 0.8), rgba(225, 235, 245, 0.95)), url("data:image/jpeg;base64,{bg_base64}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        /* Center content vertically */
        .block-container {{
            padding-top: 15vh;
            max-width: 800px;
        }}
        .gate-container {{
            background-color: rgba(255, 255, 255, 0.95);
            border-radius: 16px;
            padding: 4rem 3rem;
            box-shadow: 0 15px 40px rgba(31, 59, 99, 0.15);
            border: 1px solid rgba(79, 134, 198, 0.3);
            text-align: center;
        }}
        </style>
    """, unsafe_allow_html=True)
    
    # 3. RENDER GATEWAY CONTENT
    st.markdown("""
        <div class='gate-container'>
            <h1 style='color: #1F3B63; font-size: 3.2rem; margin-bottom: 0;'>⚕️ AERIVO MEDICAL</h1>
            <p style='color: #4F86C6; font-size: 1.4rem; font-weight: 600; margin-top: 5px; margin-bottom: 2rem;'>GLOBAL LIFE SUPPORT SOLUTIONS</p>
            <p style='color: #1F3B63; font-size: 1.1rem; line-height: 1.6; margin-bottom: 3rem;'>
                Welcome to the unified Aerivo platform. Please select your region to access custom medical specifications, regulatory certifications, and dedicated procurement channels.
            </p>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🌍 Global (EN)", use_container_width=True):
            st.session_state.language = 'EN'
            st.rerun()
    with col2:
        if st.button("🇩🇪 Deutschland (DE)", use_container_width=True):
            st.session_state.language = 'DE'
            st.rerun()
    with col3:
        if st.button("🇮🇶 العراق (AR)", use_container_width=True):
            st.session_state.language = 'AR'
            st.rerun()
            
    st.markdown("</div>", unsafe_allow_html=True)

else:
    # INJECT REGULAR BACKGROUND CSS FOR PRODUCT PAGES
    st.markdown("""
        <style>
        .stApp { background: #FFFFFF; }
        .block-container { padding-top: 3rem; max-width: 1200px; }
        </style>
    """, unsafe_allow_html=True)
    
    if st.session_state.language == 'EN': page_english_global()
    elif st.session_state.language == 'DE': page_german()
    elif st.session_state.language == 'AR': page_arabic()
