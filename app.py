import streamlit as st
import base64
import os

# --- CONFIGURATION ---
st.set_page_config(page_title="Aerivo Medical | Portable Ventilation", layout="wide", initial_sidebar_state="expanded")

# --- UTILITY: IMAGE TO BASE64 FOR BACKGROUND ---
@st.cache_data
def get_base64_of_bin_file(bin_file):
    if os.path.exists(bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return ""

# --- SESSION STATE INITIALIZATION ---
if 'language' not in st.session_state:
    st.session_state.language = None
if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""

# --- CORE CSS (APPLIED TO ALL PAGES) ---
st.markdown("""
    <style>
    /* Hide Streamlit default white header and adjust top padding */
    header {visibility: hidden !important;}
    #MainMenu {visibility: hidden !important;}
    .block-container {padding-top: 1rem !important; padding-bottom: 2rem !important;}
    
    /* Typography & Colors */
    h1, h2, h3, h4 { color: #1F3B63; font-weight: 700; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .hero-subtitle { font-size: 1.4rem; color: #4F86C6; margin-bottom: 1.5rem; line-height: 1.5;}
    
    /* Premium Buttons */
    .stButton>button { 
        background-color: #5BB3A8; color: #FFFFFF; font-weight: bold; border-radius: 8px; border: none; 
        padding: 0.6rem 1rem; transition: all 0.3s ease; box-shadow: 0 4px 10px rgba(91, 179, 168, 0.3);
    }
    .stButton>button:hover { 
        background-color: #1F3B63; color: #FFFFFF; transform: translateY(-2px); box-shadow: 0 6px 15px rgba(31, 59, 99, 0.4);
    }
    
    /* Content Boxes */
    .feature-box { background-color: #F8FBFF; border-left: 4px solid #5BB3A8; padding: 1.2rem; margin-bottom: 1rem; color: #1F3B63; border-radius: 0 8px 8px 0; box-shadow: 0 2px 5px rgba(0,0,0,0.02);}
    .rtl-feature-box { background-color: #F8FBFF; border-right: 4px solid #5BB3A8; padding: 1.2rem; margin-bottom: 1rem; direction: rtl; text-align: right; color: #1F3B63; border-radius: 8px 0 0 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.02);}
    
    .price-tag { font-size: 2.2rem; color: #4F86C6; font-weight: bold; margin: 1.5rem 0; }
    .cert-badge { display: inline-block; background-color: #DCE9F7; color: #1F3B63; padding: 0.4rem 0.8rem; border-radius: 6px; font-weight: bold; margin-right: 0.5rem; margin-bottom: 0.5rem; font-size: 0.85rem; border: 1px solid #B9D5F0;}
    hr { border-top: 1px solid rgba(79, 134, 198, 0.2); }
    
    /* Animated Scroll Cue */
    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% {transform: translateY(0);}
        40% {transform: translateY(-10px);}
        60% {transform: translateY(-5px);}
    }
    .scroll-cue {
        text-align: center; color: #4F86C6; font-weight: 600; font-size: 1.1rem; 
        animation: bounce 2s infinite; margin-top: 2rem; margin-bottom: 1rem;
        background: #F0F4F8; padding: 10px; border-radius: 20px; display: inline-block;
    }
    .scroll-container { text-align: center; }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR (AUTH & CART) ---
def render_sidebar():
    with st.sidebar:
        st.markdown("<h2 style='text-align: center; color: #4F86C6;'>⚕️ Aerivo Portal</h2>", unsafe_allow_html=True)
        st.divider()
        
        # Authentication Section
        if not st.session_state.logged_in:
            st.markdown("### 👤 User Account")
            tab_login, tab_signup = st.tabs(["Login", "Sign Up"])
            with tab_login:
                usr = st.text_input("Email / Username", key="l_usr")
                pwd = st.text_input("Password", type="password", key="l_pwd")
                if st.button("Secure Login", use_container_width=True):
                    if usr and pwd:
                        st.session_state.logged_in = True
                        st.session_state.username = usr
                        st.rerun()
                    else:
                        st.error("Please enter credentials.")
            with tab_signup:
                st.text_input("Full Name", key="s_name")
                st.text_input("Email", key="s_email")
                st.text_input("Password", type="password", key="s_pwd")
                if st.button("Create Account", use_container_width=True):
                    st.success("Account created! Please login.")
        else:
            st.markdown(f"### 👤 Welcome, {st.session_state.username}")
            if st.button("Logout", use_container_width=True):
                st.session_state.logged_in = False
                st.session_state.username = ""
                st.rerun()
        
        st.divider()
        
        # Cart Section
        st.markdown("### 🛒 Shopping Cart")
        if len(st.session_state.cart) > 0:
            for item in st.session_state.cart:
                st.markdown(f"<div style='background: #DCE9F7; padding: 10px; border-radius: 5px; margin-bottom: 5px; color: #1F3B63; font-weight: bold;'>🏷️ {item}</div>", unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Proceed to Checkout ➔", use_container_width=True):
                if st.session_state.logged_in:
                    st.success("Redirecting to secure payment gateway...")
                else:
                    st.warning("Please login to complete purchase.")
            
            if st.button("Clear Cart", use_container_width=True):
                st.session_state.cart = []
                st.rerun()
        else:
            st.info("Your cart is currently empty.")

# --- COMPONENTS ---
def render_navbar():
    col1, col2, col3 = st.columns([2, 5, 2])
    with col1:
        st.markdown("<h2 style='color: #1F3B63; margin:0;'>⚕️ Aerivo</h2>", unsafe_allow_html=True)
    with col3:
        if st.button("🌐 Change Region / تغيير المنطقة", use_container_width=True):
            st.session_state.language = None
            st.rerun()
    st.markdown("<hr style='margin-top: 5px;'>", unsafe_allow_html=True)

def render_scroll_cue(text="Scroll down for clinical environments & details"):
    st.markdown(f"""
        <div class='scroll-container'>
            <div class='scroll-cue'>👇 {text} 👇</div>
        </div>
    """, unsafe_allow_html=True)

def render_album_gallery():
    st.markdown("<hr>", unsafe_allow_html=True)
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

def render_main_product_image():
    try:
        st.image("Aerivo (6).png", use_container_width=True)
    except:
        st.info("Product Image Loading...")

# --- REGIONAL PAGES ---
def page_english_global():
    render_sidebar()
    render_navbar()
    col_text, col_img = st.columns([1.1, 1], gap="large") # Adjusted ratio to prevent squeezing
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
            if st.button("🛒 Add to Cart", use_container_width=True):
                st.session_state.cart.append("Aerivo M1 (Global)")
                st.rerun()
        with col_btn2:
            st.button("📄 Tech Specs", use_container_width=True)
            
    with col_img:
        render_main_product_image()
        
    render_scroll_cue("Explore clinical environments below")
    render_album_gallery()

def page_german():
    render_sidebar()
    render_navbar()
    col_text, col_img = st.columns([1.1, 1], gap="large")
    with col_text:
        st.markdown("<h1>Aerivo M1: Präzision und Sicherheit</h1>", unsafe_allow_html=True)
        st.markdown("<div class='hero-subtitle'>Mobiles Beatmungssystem für die Intensivmedizin</div>", unsafe_allow_html=True)
        
        st.markdown("""
        <div style='margin-bottom: 1rem;'>
            <span class='cert-badge'>🇪🇺 CE Zertifiziert</span>
            <span class='cert-badge'>📋 EU MDR Konform</span>
            <span class='cert-badge'>⚙️ ISO 13485:2016</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='feature-box'>
            <b>Zuverlässigkeit im Einsatz (MTBF > 50.000h)</b><br>
            Entwickelt für maximale Ausfallsicherheit. Getestet durch unabhängige benannte Stellen.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div class='price-tag'>14.200 €</div>", unsafe_allow_html=True)
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("🛒 In den Warenkorb", use_container_width=True):
                st.session_state.cart.append("Aerivo M1 (DE)")
                st.rerun()
        with col_btn2:
            st.button("📄 Datenblatt (PDF)", use_container_width=True)
            
    with col_img:
        render_main_product_image()

    render_scroll_cue("Scrollen Sie nach unten für weitere Bilder")
    render_album_gallery()

def page_arabic():
    render_sidebar()
    render_navbar()
    st.markdown("<div style='direction: rtl; text-align: right; font-family: Arial;'>", unsafe_allow_html=True)
    
    col_img, col_text = st.columns([1, 1.1], gap="large")
    with col_text:
        st.markdown("<h1 style='direction: rtl; text-align: right;'>أيريفو M1: شريكك الموثوق في العناية المركزة</h1>", unsafe_allow_html=True)
        st.markdown("<div class='hero-subtitle' style='direction: rtl; text-align: right;'>تكنولوجيا التنفس الصناعي المتقدمة، بين يديك.</div>", unsafe_allow_html=True)
        
        st.markdown("<div style='background:#E8F5E9; color:#2E7D32; padding:10px; border-radius:5px; margin-bottom:15px; font-weight:bold; border:1px solid #A5D6A7;'>✔️ مُعتمد ومسجل لدى وزارة الصحة العراقية (MOH) ومطابق لمواصفات (KIMADIA).</div>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class='rtl-feature-box'>
            <b>دعم شامل وتدريب مستمر</b><br>
            نحن لا نبيع جهازاً فقط، بل نبني شراكة طويلة الأمد. نوفر تدريباً حضورياً شاملاً للكوادر الطبية.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div class='price-tag' style='direction: rtl; text-align: right;'>$15,500.00 USD</div>", unsafe_allow_html=True)
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn2:
            if st.button("🛒 إضافة للسلة", use_container_width=True):
                st.session_state.cart.append("Aerivo M1 (AR)")
                st.rerun()
        with col_btn1:
            st.button("💬 تواصل (WhatsApp)", use_container_width=True)
            
    with col_img:
        render_main_product_image()
        
    st.markdown("</div>", unsafe_allow_html=True)
    
    render_scroll_cue("قم بالتمرير لأسفل لرؤية المزيد من الصور")
    render_album_gallery()

# --- ROUTER & CONDITIONAL CSS ---
if st.session_state.language is None:
    # 1. GENERATE BACKGROUND FOR GATEWAY
    bg_base64 = get_base64_of_bin_file("Aerivo (7).png")
    
    # 2. INJECT FULL-SCREEN CSS
    st.markdown(f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(240, 244, 248, 0.7), rgba(225, 235, 245, 0.9)), url("data:image/jpeg;base64,{bg_base64}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        /* Center content vertically without top space */
        .block-container {{
            padding-top: 10vh !important;
            max-width: 850px;
        }}
        /* Gradient box instead of solid white */
        .gate-container {{
            background: linear-gradient(135deg, #F4F9FF 0%, #DDEBFA 100%);
            border-radius: 20px;
            padding: 4rem 3rem;
            box-shadow: 0 20px 50px rgba(31, 59, 99, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.6);
            text-align: center;
            backdrop-filter: blur(10px);
        }}
        [data-testid="collapsedControl"] {{ display: none; }} /* Hide sidebar toggle on gateway */
        </style>
    """, unsafe_allow_html=True)
    
    # 3. RENDER GATEWAY CONTENT
    st.markdown("""
        <div class='gate-container'>
            <h1 style='color: #1F3B63; font-size: 3.5rem; margin-bottom: 0;'>⚕️ AERIVO MEDICAL</h1>
            <p style='color: #4F86C6; font-size: 1.3rem; font-weight: 700; margin-top: 5px; margin-bottom: 2rem; letter-spacing: 2px;'>GLOBAL LIFE SUPPORT SOLUTIONS</p>
            <p style='color: #334E68; font-size: 1.15rem; line-height: 1.7; margin-bottom: 3rem;'>
                Welcome to the unified Aerivo platform. Please select your region to access custom medical specifications, regulatory certifications, and dedicated procurement channels.
            </p>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Global (EN)", use_container_width=True):
            st.session_state.language = 'EN'
            st.rerun()
    with col2:
        if st.button("Deutschland", use_container_width=True):
            st.session_state.language = 'DE'
            st.rerun()
    with col3:
        if st.button("العراق (AR)", use_container_width=True):
            st.session_state.language = 'AR'
            st.rerun()
            
    st.markdown("</div>", unsafe_allow_html=True)

else:
    # INJECT REGULAR BACKGROUND CSS FOR PRODUCT PAGES
    st.markdown("""
        <style>
        .stApp { background: #FFFFFF; }
        .block-container { max-width: 1200px; }
        </style>
    """, unsafe_allow_html=True)
    
    if st.session_state.language == 'EN': page_english_global()
    elif st.session_state.language == 'DE': page_german()
    elif st.session_state.language == 'AR': page_arabic()
