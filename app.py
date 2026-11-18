import streamlit as st

# --- CONFIGURATION & THEMING ---
st.set_page_config(page_title="Aerivo Medical | Portable Ventilation", layout="wide", initial_sidebar_state="collapsed")

# Enhanced CSS for a premium medical-grade UI with light blue background
st.markdown("""
    <style>
    /* Gradient Light Blue Background & Visual Enhancements */
    .stApp { 
        background: linear-gradient(135deg, #F0F4F8 0%, #E1EBF5 100%); 
        color: #1F3B63; 
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
    }
    
    /* Gate Page Graphic & Box */
    .gate-container {
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 16px;
        padding: 3rem;
        box-shadow: 0 10px 30px rgba(31, 59, 99, 0.08);
        border: 1px solid rgba(79, 134, 198, 0.2);
        margin-top: 2rem;
    }
    
    h1, h2, h3, h4 { color: #1F3B63; font-weight: 700; }
    .hero-subtitle { font-size: 1.5rem; color: #4F86C6; margin-bottom: 2rem; }
    
    /* Premium Buttons */
    .stButton>button { 
        background-color: #5BB3A8; 
        color: #FFFFFF; 
        font-weight: bold; 
        border-radius: 8px; 
        border: none; 
        padding: 0.8rem 2rem; 
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(91, 179, 168, 0.2);
    }
    .stButton>button:hover { 
        background-color: #1F3B63; 
        color: #FFFFFF; 
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(31, 59, 99, 0.3);
    }
    
    /* Gallery Styling */
    .gallery-card {
        background-color: #FFFFFF;
        border-radius: 8px;
        padding: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 1.5rem;
    }
    
    .price-tag { font-size: 2rem; color: #4F86C6; font-weight: bold; margin: 1rem 0; }
    .cert-badge { display: inline-block; background-color: #DCE9F7; color: #1F3B63; padding: 0.5rem 1rem; border-radius: 4px; font-weight: bold; margin-right: 1rem; font-size: 0.9rem;}
    .rtl-text { direction: rtl; text-align: right; font-family: 'Arial', sans-serif; }
    .feature-box { border-left: 4px solid #5BB3A8; padding-left: 1rem; margin-bottom: 1.5rem; }
    .rtl-feature-box { border-right: 4px solid #5BB3A8; padding-right: 1rem; margin-bottom: 1.5rem; direction: rtl; text-align: right; }
    hr { border-top: 1px solid rgba(79, 134, 198, 0.2); }
    </style>
""", unsafe_allow_html=True)

# --- SESSION STATE ---
if 'language' not in st.session_state:
    st.session_state.language = None
if 'cart' not in st.session_state:
    st.session_state.cart = []

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

# Function to render gallery section at the bottom of the page
def render_multiscreen_gallery():
    st.markdown("<br><hr><br>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Aerivo M1 in Field & Clinical Environments</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #4F86C6; margin-bottom: 2rem;'>Explore how the Aerivo M1 adapts to various medical and rescue environments globally.</p>", unsafe_allow_html=True)
    
    # Grid for the 10 custom environment images
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='gallery-card'>", unsafe_allow_html=True)
        st.image("image_7.png", caption="Aerivo M1 Multi-Environment Operations", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='gallery-card'>", unsafe_allow_html=True)
        st.image("image_6.png", caption="The Portable Kit (Standard Package)", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# --- REGIONAL PAGES ---

def page_english_global():
    render_navbar()
    
    # HERO SECTION
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
        st.image("image_6.png", use_container_width=True)
        
    st.markdown("<br><hr><br>", unsafe_allow_html=True)
    
    # SPECS SECTION
    st.markdown("<h3>Technical Specifications</h3>", unsafe_allow_html=True)
    spec_col1, spec_col2 = st.columns(2)
    with spec_col1:
        st.markdown("""
        * **Patient Types:** Adult, Pediatric, Neonatal (with optional upgrade)
        * **Ventilation Modes:** ASV, (S)CMV, SIMV, PCV+, PSIMV+, SPONT, APRV, NIV
        * **Weight:** 6.5 kg (14.3 lbs)
        """)
    with spec_col2:
        st.markdown("""
        * **Dimensions:** 280 x 210 x 310 mm
        * **Display:** 8.4 inch touchscreen
        * **Interfaces:** USB, Ethernet, RS-232
        """)
    
    render_multiscreen_gallery()

def page_german():
    render_navbar()
    
    # HERO SECTION
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
            Entwickelt für maximale Ausfallsicherheit im klinischen und präklinischen Einsatz. Getestet durch unabhängige benannte Stellen (Notified Bodies).
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div class='price-tag'>14.200 €</div>", unsafe_allow_html=True)
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            st.button("Offizielles Angebot anfordern", use_container_width=True)
        with col_btn2:
            st.button("📄 Datenblatt (PDF)", use_container_width=True)
            
    with col_img:
        st.image("image_6.png", use_container_width=True)

    st.markdown("<br><hr><br>", unsafe_allow_html=True)
    
    # STRUCTURAL DATA SECTION
    st.markdown("<h3>Klinische Spezifikationen & Rahmenverträge</h3>", unsafe_allow_html=True)
    st.info("Zugelassen für die Beschaffung über Prospitalia, Sana und GDEKK Einkaufsverbünde. Vollständige Integration in DRG-Abrechnungssysteme.")
    
    tab1, tab2 = st.tabs(["Technische Daten", "Qualitätsmanagement"])
    with tab1:
        st.markdown("""
        * **Atemzugvolumen:** 20 ml - 2000 ml
        * **Akkulaufzeit:** 9 Stunden (Hot-Swap fähig)
        * **Schutzklasse:** IP24 (Spritzwassergeschützt)
        """)
    with tab2:
        st.markdown("""
        * Datenspeicherung gemäß **DSGVO** Richtlinien.
        * Erfüllt **ISO 80601-2-12:2020** (Intensivpflege) und **ISO 80601-2-84:2020** (Notfall/Transport).
        """)
        
    render_multiscreen_gallery()

def page_arabic():
    render_navbar()
    
    # HERO SECTION
    st.markdown("<div class='rtl-text'>", unsafe_allow_html=True)
    
    col_img, col_text = st.columns([1, 1], gap="large")
    with col_text:
        st.markdown("<h1 style='direction: rtl; text-align: right;'>أيريفو M1: شريكك الموثوق في العناية المركزة</h1>", unsafe_allow_html=True)
        st.markdown("<div class='hero-subtitle' style='direction: rtl; text-align: right;'>تكنولوجيا التنفس الصناعي المتقدمة، بين يديك.</div>", unsafe_allow_html=True)
        
        st.
