import streamlit as st
import base64
import os

# --- CONFIGURATION ---
st.set_page_config(page_title="Aerivo Medical | Portable Ventilation", layout="wide", initial_sidebar_state="collapsed")

# --- UTILITIES ---
@st.cache_data
def get_base64_of_bin_file(bin_file):
    if os.path.exists(bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return ""

def get_pdf_bytes(filename):
    if os.path.exists(filename):
        with open(filename, "rb") as f:
            return f.read()
    return b""

# Load Tech Specs PDF
pdf_data = get_pdf_bytes("Tech Specs.pdf")

# --- SESSION STATE INITIALIZATION ---
if 'language' not in st.session_state:
    st.session_state.language = None
if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'show_cart' not in st.session_state:
    st.session_state.show_cart = False
if 'show_account' not in st.session_state:
    st.session_state.show_account = False

# --- CORE CSS (APPLIED TO ALL PAGES) ---
st.markdown("""
    <style>
    /* Smooth Scrolling for the Anchor Link */
    html { scroll-behavior: smooth; }
    
    /* Hide Streamlit defaults */
    header {visibility: hidden !important;}
    #MainMenu {visibility: hidden !important;}
    .block-container {padding-top: 2rem !important; padding-bottom: 2rem !important; max-width: 1100px;}
    [data-testid="collapsedControl"] { display: none; }
    
    /* Global Gradient Background for ALL Pages */
    .stApp {
        background: linear-gradient(135deg, #F0F4F8 0%, #DDEBFA 100%) !important;
        background-attachment: fixed !important;
    }
    
    /* Typography & Colors */
    h1, h2, h3, h4 { color: #1F3B63; font-weight: 700; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .hero-subtitle { font-size: 1.4rem; color: #4F86C6; margin-bottom: 1.5rem; line-height: 1.5;}
    
    /* Premium Buttons */
    .stButton>button, .stDownloadButton>button { 
        background-color: #5BB3A8; color: #FFFFFF; font-weight: bold; border-radius: 8px; border: none; 
        padding: 0.6rem 1rem; transition: all 0.3s ease; box-shadow: 0 4px 10px rgba(91, 179, 168, 0.3);
    }
    .stButton>button:hover, .stDownloadButton>button:hover { 
        background-color: #1F3B63; color: #FFFFFF; transform: translateY(-2px); box-shadow: 0 6px 15px rgba(31, 59, 99, 0.4);
    }
    
    /* Secondary Nav Buttons (Cart, Account, Region) */
    .nav-btn>button { background-color: #FFFFFF; color: #1F3B63; border: 1px solid #4F86C6; box-shadow: none; }
    .nav-btn>button:hover { background-color: #4F86C6; color: #FFFFFF; }
    
    /* Content Boxes */
    .feature-box { background-color: rgba(255,255,255,0.8); border-left: 4px solid #5BB3A8; padding: 1.2rem; margin-bottom: 1rem; color: #1F3B63; border-radius: 0 8px 8px 0; backdrop-filter: blur(5px);}
    .rtl-feature-box { background-color: rgba(255,255,255,0.8); border-right: 4px solid #5BB3A8; padding: 1.2rem; margin-bottom: 1rem; direction: rtl; text-align: right; color: #1F3B63; border-radius: 8px 0 0 8px; backdrop-filter: blur(5px);}
    .price-tag { font-size: 2.2rem; color: #4F86C6; font-weight: bold; margin: 1.5rem 0; }
    .cert-badge { display: inline-block; background-color: #FFFFFF; color: #1F3B63; padding: 0.4rem 0.8rem; border-radius: 6px; font-weight: bold; margin-right: 0.5rem; margin-bottom: 0.5rem; font-size: 0.85rem; border: 1px solid #B9D5F0;}
    hr { border-top: 1px solid rgba(79, 134, 198, 0.3); }
    
    /* Animated Scroll Cue Link */
    @keyframes bounce { 0%, 20%, 50%, 80%, 100% {transform: translateY(0);} 40% {transform: translateY(-10px);} 60% {transform: translateY(-5px);} }
    .scroll-cue {
        text-align: center; color: #1F3B63; font-weight: bold; font-size: 1.1rem; 
        animation: bounce 2s infinite; margin-top: 2rem; margin-bottom: 1rem;
        background: #FFFFFF; padding: 12px 25px; border-radius: 30px; display: inline-block;
        text-decoration: none; box-shadow: 0 4px 10px rgba(0,0,0,0.05); border: 1px solid #DCE9F7; transition: all 0.3s ease;
    }
    .scroll-cue:hover { background: #5BB3A8; color: #FFFFFF; text-decoration: none; }
    .scroll-container { text-align: center; }
    </style>
""", unsafe_allow_html=True)

# --- NAVBAR & IN-PAGE MENUS ---
def render_navbar():
    col1, col2, col3, col4 = st.columns([4, 2, 2, 2])
    with col1:
        st.markdown("<h2 style='color: #1F3B63; margin:0;'>⚕️ Aerivo</h2>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='nav-btn'>", unsafe_allow_html=True)
        if st.button(f"🛒 Cart ({len(st.session_state.cart)})", use_container_width=True):
            st.session_state.show_cart = not st.session_state.show_cart
            st.session_state.show_account = False
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='nav-btn'>", unsafe_allow_html=True)
        if st.button("👤 Account", use_container_width=True):
            st.session_state.show_account = not st.session_state.show_account
            st.session_state.show_cart = False
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    with col4:
        st.markdown("<div class='nav-btn'>", unsafe_allow_html=True)
        if st.button("🌐 Change Region", use_container_width=True):
            st.session_state.language = None
            st.session_state.show_cart = False
            st.session_state.show_account = False
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<hr style='margin-top: 5px;'>", unsafe_allow_html=True)

    # Render Account Dropdown Menu
    if st.session_state.show_account:
        with st.container():
            st.markdown("<div style='background: rgba(255,255,255,0.9); padding: 25px; border-radius: 12px; border: 2px solid #5BB3A8; margin-bottom: 20px;'>", unsafe_allow_html=True)
            if not st.session_state.logged_in:
                t1, t2 = st.tabs(["Login", "Sign Up"])
                with t1:
                    u = st.text_input("Username")
                    p = st.text_input("Password", type="password")
                    if st.button("Secure Login"):
                        if u and p:
                            st.session_state.logged_in = True
                            st.session_state.username = u
                            st.session_state.show_account = False
                            st.rerun()
                        else:
                            st.error("Please enter credentials")
                with t2:
                    st.text_input("Full Name")
                    st.text_input("Email Address")
                    st.text_input("Choose Password", type="password")
                    if st.button("Create Account"):
                        st.success("Account created successfully! You can now login.")
            else:
                st.markdown(f"### Welcome back, {st.session_state.username}!")
                st.write("Your account is verified for medical procurement.")
                if st.button("Logout"):
                    st.session_state.logged_in = False
                    st.session_state.username = ""
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

    # Render Cart Dropdown Menu
    if st.session_state.show_cart:
        with st.container():
            st.markdown("<div style='background: rgba(255,255,255,0.9); padding: 25px; border-radius: 12px; border: 2px solid #4F86C6; margin-bottom: 20px;'>", unsafe_allow_html=True)
            st.markdown("### 🛒 Your Secure Shopping Cart")
            if len(st.session_state.cart) > 0:
                for i, item in enumerate(st.session_state.cart):
                    st.markdown(f"**{i+1}. {item}** - $15,500.00")
                st.markdown("<hr>", unsafe_allow_html=True)
                st.markdown(f"**Total Estimated:** ${len(st.session_state.cart) * 15500:,.2f} USD")
                st.write("")
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("Proceed to Checkout ➔", use_container_width=True):
                        if st.session_state.logged_in:
                            st.success("Transferring to encrypted payment gateway...")
                        else:
                            st.warning("Please login to complete your order.")
                with c2:
                    if st.button("Clear Cart", use_container_width=True):
                        st.session_state.cart = []
                        st.rerun()
            else:
                st.info("Your cart is empty. Add products to proceed.")
            st.markdown("</div>", unsafe_allow_html=True)

# --- REUSABLE UI BLOCKS ---
def render_scroll_cue(text):
    # Clickable link that scrolls to the #gallery-section ID
    st.markdown(f"""
        <div class='scroll-container'>
            <a href="#gallery-section" class='scroll-cue'>👇 {text} 👇</a>
        </div>
    """, unsafe_allow_html=True)

def render_album_gallery():
    # ID target for smooth scrolling
    st.markdown("<div id='gallery-section'></div>", unsafe_allow_html=True)
    st.markdown("<br><hr>", unsafe_allow_html=True)
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

def render_tech_specs_button(label="📄 Tech Specs"):
    if pdf_data:
        st.download_button(label=label, data=pdf_data, file_name="Tech_Specs.pdf", mime="application/pdf", use_container_width=True)
    else:
        st.button(f"{label} (File Missing)", disabled=True, use_container_width=True)

def render_main_product_image():
    try:
        st.image("Aerivo (6).png", use_container_width=True)
    except:
        st.info("Product Image Loading...")

# --- REGIONAL PAGES ---
def page_english_global():
    render_navbar()
    col_text, col_img = st.columns([1.1, 1], gap="large")
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
                st.session_state.show_cart = True
                st.rerun()
        with col_btn2:
            render_tech_specs_button("📄 Download Specs")
            
    with col_img:
        render_main_product_image()
        
    render_scroll_cue("Explore clinical environments below")
    render_album_gallery()

def page_german():
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
                st.session_state.show_cart = True
                st.rerun()
        with col_btn2:
            render_tech_specs_button("📄 Datenblatt (PDF)")
            
    with col_img:
        render_main_product_image()

    render_scroll_cue("Klicken Sie hier für weitere Bilder")
    render_album_gallery()

def page_arabic():
    render_navbar()
    st.markdown("<div style='direction: rtl; text-align: right; font-family: Arial;'>", unsafe_allow_html=True)
    
    col_img, col_text = st.columns([1, 1.1], gap="large")
    with col_text:
        st.markdown("<h1 style='direction: rtl; text-align: right;'>أيريفو M1: شريكك الموثوق في العناية المركزة</h1>", unsafe_allow_html=True)
        st.markdown("<div class='hero-subtitle' style='direction: rtl; text-align: right;'>تكنولوجيا التنفس الصناعي المتقدمة، بين يديك.</div>", unsafe_allow_html=True)
        
        st.markdown("<div style='background:rgba(255,255,255,0.9); color:#2E7D32; padding:10px; border-radius:5px; margin-bottom:15px; font-weight:bold; border:1px solid #A5D6A7;'>✔️ مُعتمد ومسجل لدى وزارة الصحة العراقية (MOH) ومطابق لمواصفات (KIMADIA).</div>", unsafe_allow_html=True)
        
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
                st.session_state.show_cart = True
                st.rerun()
        with col_btn1:
            render_tech_specs_button("📄 تحميل المواصفات")
            
    with col_img:
        render_main_product_image()
        
    st.markdown("</div>", unsafe_allow_html=True)
    
    render_scroll_cue("انقر هنا لاستكشاف البيئات السريرية")
    render_album_gallery()

# --- ROUTER & CONDITIONAL CSS ---
if st.session_state.language is None:
    # 1. GENERATE BACKGROUND FOR GATEWAY
    bg_base64 = get_base64_of_bin_file("Aerivo (7).png")
    
    # 2. INJECT FULL-SCREEN CSS FOR GATEWAY
    st.markdown(f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(240, 244, 248, 0.6), rgba(225, 235, 245, 0.85)), url("data:image/jpeg;base64,{bg_base64}") !important;
            background-size: cover !important;
            background-position: center !important;
        }}
        .block-container {{ padding-top: 15vh !important; max-width: 850px; }}
        .gate-container {{
            background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(240,248,255,0.9) 100%);
            border-radius: 20px; padding: 4rem 3rem; text-align: center;
            box-shadow: 0 20px 50px rgba(31, 59, 99, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.8);
            backdrop-filter: blur(8px);
        }}
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
        if st.button("العراق", use_container_width=True):
            st.session_state.language = 'AR'
            st.rerun()
            
    st.markdown("</div>", unsafe_allow_html=True)

else:
    if st.session_state.language == 'EN': page_english_global()
    elif st.session_state.language == 'DE': page_german()
    elif st.session_state.language == 'AR': page_arabic()
