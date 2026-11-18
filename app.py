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
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=Noto+Sans+Arabic:wght@400;600;700&display=swap');

    :root {
        --navy: #0B2A4A;
        --ocean: #1B6FB5;
        --teal: #14A89B;
        --teal-dark: #0E8479;
        --mint: #7FD8CC;
        --ice: #EAF4FB;
        --ink-soft: #3E5A78;
        --glass: rgba(255, 255, 255, 0.55);
        --glass-strong: rgba(255, 255, 255, 0.78);
        --glass-border: rgba(255, 255, 255, 0.85);
        --shadow-sm: 0 4px 16px rgba(11, 42, 74, 0.08);
        --shadow-md: 0 14px 40px rgba(11, 42, 74, 0.14);
        --ease: cubic-bezier(.22, .8, .24, 1);
    }

    html { scroll-behavior: smooth; }
    html, body, [class*="css"], .stApp, .stMarkdown, button, input, textarea {
        font-family: 'Manrope', 'Noto Sans Arabic', 'Segoe UI', Tahoma, sans-serif !important;
    }

    /* Hide Streamlit defaults */
    header {visibility: hidden !important;}
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    [data-testid="collapsedControl"] { display: none; }
    .block-container {padding-top: 1.5rem !important; padding-bottom: 3rem !important; max-width: 1150px;}

    /* Background: soft clinical gradient with light "glow" orbs behind the glass */
    .stApp {
        background:
            radial-gradient(900px 500px at 8% -5%, rgba(20,168,155,0.22), transparent 60%),
            radial-gradient(800px 520px at 100% 10%, rgba(27,111,181,0.22), transparent 60%),
            radial-gradient(700px 500px at 50% 110%, rgba(127,216,204,0.28), transparent 60%),
            linear-gradient(160deg, #F6FAFD 0%, #E4F0FA 100%) !important;
        background-attachment: fixed !important;
        color: var(--navy);
    }

    /* Typography */
    h1, h2, h3, h4 { color: var(--navy); font-weight: 800; letter-spacing: -0.02em; }
    h1 { font-size: 2.9rem !important; line-height: 1.08 !important; margin-bottom: .4rem !important; }
    p, li, label, .stMarkdown { color: var(--ink-soft); }
    .hero-subtitle { font-size: 1.25rem; color: var(--ocean); margin: .2rem 0 1.6rem; line-height: 1.55; font-weight: 500; }

    /* ---------- BUTTONS ---------- */
    .stButton > button, .stDownloadButton > button {
        position: relative; overflow: hidden;
        background: var(--glass-strong); color: var(--navy);
        font-weight: 700; font-size: 0.95rem;
        border: 1px solid var(--glass-border); border-radius: 14px;
        padding: 0.65rem 1.1rem;
        backdrop-filter: blur(14px) saturate(160%); -webkit-backdrop-filter: blur(14px) saturate(160%);
        box-shadow: var(--shadow-sm), inset 0 1px 0 rgba(255,255,255,.9);
        transition: transform .25s var(--ease), box-shadow .25s var(--ease), background .25s var(--ease), color .25s var(--ease), border-color .25s var(--ease);
    }
    .stButton > button:hover, .stDownloadButton > button:hover {
        background: #FFFFFF; color: var(--teal-dark); border-color: var(--mint);
        transform: translateY(-3px); box-shadow: 0 12px 28px rgba(20,168,155,0.22);
    }
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, var(--teal) 0%, var(--ocean) 100%);
        color: #FFFFFF; border: 1px solid rgba(255,255,255,.35);
        box-shadow: 0 10px 26px rgba(20,168,155,0.38), inset 0 1px 0 rgba(255,255,255,.45);
    }
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, var(--teal-dark) 0%, var(--navy) 100%);
        color: #FFFFFF; box-shadow: 0 16px 34px rgba(11,42,74,0.35);
    }
    .stButton > button::before, .stDownloadButton > button::before {
        content: ""; position: absolute; top: 0; left: -80%; width: 50%; height: 100%;
        background: linear-gradient(100deg, transparent, rgba(255,255,255,.55), transparent);
        transform: skewX(-20deg); transition: left .6s var(--ease); pointer-events: none;
    }
    .stButton > button:hover::before, .stDownloadButton > button:hover::before { left: 130%; }

    @keyframes click-ring {
        0%   { box-shadow: 0 0 0 0 rgba(20,168,155,0.55); }
        100% { box-shadow: 0 0 0 16px rgba(20,168,155,0); }
    }
    .stButton > button:active, .stDownloadButton > button:active {
        transform: translateY(0) scale(0.95) !important;
        animation: click-ring .5s ease-out;
        filter: brightness(0.96);
        transition-duration: .08s;
    }
    .stButton > button:focus-visible, .stDownloadButton > button:focus-visible, a:focus-visible {
        outline: 3px solid rgba(20,168,155,.55) !important; outline-offset: 2px;
    }
    .stButton > button:disabled { opacity: .55; transform: none; box-shadow: none; }

    /* ---------- GLASS CARDS ---------- */
    .feature-box, .rtl-feature-box {
        background: var(--glass); color: var(--navy);
        padding: 1.2rem 1.4rem; margin-bottom: 1rem; border-radius: 18px;
        border: 1px solid var(--glass-border);
        backdrop-filter: blur(16px) saturate(160%); -webkit-backdrop-filter: blur(16px) saturate(160%);
        box-shadow: var(--shadow-sm), inset 0 1px 0 rgba(255,255,255,.9);
        position: relative; overflow: hidden;
        transition: transform .3s var(--ease), box-shadow .3s var(--ease), background .3s var(--ease);
    }
    .feature-box::before, .rtl-feature-box::before {
        content: ""; position: absolute; top: 14px; bottom: 14px; width: 4px; border-radius: 4px;
        background: linear-gradient(180deg, var(--teal), var(--ocean));
    }
    .feature-box::before { left: 0; }
    .rtl-feature-box::before { right: 0; }
    .feature-box { padding-left: 1.6rem; }
    .rtl-feature-box { direction: rtl; text-align: right; padding-right: 1.6rem; }
    .feature-box:hover, .rtl-feature-box:hover {
        transform: translateY(-4px); background: var(--glass-strong); box-shadow: var(--shadow-md);
    }
    .feature-box:active, .rtl-feature-box:active { transform: translateY(-1px) scale(0.985); }
    .feature-box b, .rtl-feature-box b { color: var(--navy); font-size: 1.05rem; }

    .price-tag {
        display: inline-block; font-size: 2.2rem; font-weight: 800; margin: 1.2rem 0 1.4rem;
        background: linear-gradient(135deg, var(--ocean), var(--teal));
        -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent;
    }
    .cert-badge {
        display: inline-block; background: var(--glass-strong); color: var(--navy);
        padding: 0.4rem 0.9rem; border-radius: 999px; font-weight: 700; font-size: 0.82rem;
        margin: 0 0.5rem 0.5rem 0; border: 1px solid var(--glass-border);
        box-shadow: var(--shadow-sm); backdrop-filter: blur(10px);
        transition: transform .25s var(--ease), box-shadow .25s var(--ease), border-color .25s var(--ease);
    }
    .cert-badge:hover { transform: translateY(-2px); border-color: var(--mint); box-shadow: 0 8px 18px rgba(20,168,155,.2); }
    .cert-badge:active { transform: scale(.94); }
    .info-chip {
        background: rgba(232,247,238,0.85); color: #1E6B3A; padding: 12px 16px; border-radius: 14px;
        margin-bottom: 15px; font-weight: 700; border: 1px solid rgba(120,200,150,0.55);
        backdrop-filter: blur(10px);
    }
    hr { border: none !important; height: 1px; background: linear-gradient(90deg, transparent, rgba(27,111,181,0.35), transparent) !important; margin: 1rem 0 !important; }

    /* ---------- NAVBAR ---------- */
    .brand { display:flex; align-items:center; gap:.7rem; margin: 0; }
    .brand-mark {
        width: 42px; height: 42px; border-radius: 13px; display:flex; align-items:center; justify-content:center;
        background: linear-gradient(135deg, var(--teal), var(--ocean)); color:#fff; font-size: 1.25rem;
        box-shadow: 0 8px 20px rgba(20,168,155,.35), inset 0 1px 0 rgba(255,255,255,.5);
    }
    .brand-name { font-size: 1.55rem; font-weight: 800; color: var(--navy); letter-spacing: -0.03em; }
    .brand-sub { display:block; font-size: .72rem; font-weight: 600; color: var(--ocean); letter-spacing: .02em; margin-top: -3px; }

    /* ---------- PANELS (cart / account) ---------- */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background: var(--glass-strong) !important;
        border: 1px solid var(--glass-border) !important; border-radius: 22px !important;
        backdrop-filter: blur(20px) saturate(170%); -webkit-backdrop-filter: blur(20px) saturate(170%);
        box-shadow: var(--shadow-md), inset 0 1px 0 rgba(255,255,255,.9);
        padding: .6rem .9rem;
        animation: panel-in .35s var(--ease);
    }
    @keyframes panel-in { from { opacity: 0; transform: translateY(-8px) scale(.99); } to { opacity: 1; transform: none; } }

    /* ---------- INPUTS ---------- */
    .stTextInput input {
        background: rgba(255,255,255,0.8) !important; color: var(--navy) !important;
        border: 1px solid rgba(27,111,181,0.25) !important; border-radius: 12px !important;
        transition: box-shadow .25s var(--ease), border-color .25s var(--ease);
    }
    .stTextInput input:focus { border-color: var(--teal) !important; box-shadow: 0 0 0 4px rgba(20,168,155,0.18) !important; }
    [data-testid="stAlert"] { border-radius: 14px; backdrop-filter: blur(10px); }

    /* ---------- TABS (segmented glass control) ---------- */
    [data-baseweb="tab-list"] {
        gap: 6px; background: var(--glass); padding: 6px; border-radius: 16px; width: fit-content;
        border: 1px solid var(--glass-border); backdrop-filter: blur(14px); box-shadow: var(--shadow-sm);
        margin: 0 auto 1rem;
    }
    [data-baseweb="tab"] {
        border-radius: 11px !important; padding: 8px 18px !important; background: transparent !important;
        color: var(--ink-soft) !important; font-weight: 700 !important;
        transition: background .25s var(--ease), color .25s var(--ease), transform .15s var(--ease);
    }
    [data-baseweb="tab"]:hover { background: rgba(255,255,255,.7) !important; color: var(--teal-dark) !important; }
    [data-baseweb="tab"]:active { transform: scale(.94); }
    [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, var(--teal), var(--ocean)) !important; color: #fff !important;
        box-shadow: 0 6px 16px rgba(20,168,155,.35);
    }
    [data-baseweb="tab-highlight"], [data-baseweb="tab-border"] { display: none !important; }

    /* ---------- IMAGES (FIXED FOR FULLSCREEN CLICK) ---------- */
    [data-testid="stImage"] { 
        border-radius: 22px; 
        overflow: hidden; 
        box-shadow: var(--shadow-md); 
        transition: transform .4s var(--ease), box-shadow .4s var(--ease); 
        position: relative !important; 
        display: block !important;
    }
    [data-testid="stImage"] img { 
        border-radius: 22px; 
        transition: transform .6s var(--ease); 
    }
    [data-testid="stImage"]:hover { 
        transform: translateY(-4px); 
        box-shadow: 0 22px 50px rgba(11,42,74,.2); 
    }
    [data-testid="stImage"]:hover img { 
        transform: scale(1.04); 
    }
    [data-testid="stImageCaption"] { color: var(--ink-soft); font-weight: 600; text-align: center; }

    /* STRETCH THE FULLSCREEN BUTTON */
    [data-testid="StyledFullScreenButton"] {
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        width: 100% !important;
        height: 100% !important;
        opacity: 0 !important; /* Make invisible but clickable */
        z-index: 999 !important; /* Place it on top of the image */
    }
    [data-testid="StyledFullScreenButton"] button {
        width: 100% !important;
        height: 100% !important;
        cursor: zoom-in !important; /* Cursor indicates zoom capability */
        border: none !important;
        background: transparent !important;
    }

    /* ---------- SCROLL CUE ---------- */
    @keyframes gentle-bob { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-5px); } }
    .scroll-container { text-align: center; margin: 2rem 0 .5rem; }
    .scroll-cue {
        display: inline-flex; align-items: center; gap: .6rem; animation: gentle-bob 3s ease-in-out infinite;
        background: var(--glass-strong); color: var(--navy); font-weight: 700; font-size: 1rem;
        padding: 12px 26px; border-radius: 999px; text-decoration: none !important;
        border: 1px solid var(--glass-border); box-shadow: var(--shadow-sm); backdrop-filter: blur(14px);
        transition: background .3s var(--ease), color .3s var(--ease), box-shadow .3s var(--ease);
    }
    .scroll-cue:hover { background: linear-gradient(135deg, var(--teal), var(--ocean)); color: #fff !important; box-shadow: 0 12px 28px rgba(20,168,155,.35); }
    .scroll-cue:active { transform: scale(.94); }

    /* Hero entrance (the single orchestrated moment) */
    @keyframes rise { from { opacity: 0; transform: translateY(18px); } to { opacity: 1; transform: none; } }
    h1 { animation: rise .7s var(--ease) both; }
    .hero-subtitle { animation: rise .7s .12s var(--ease) both; }

    @media (max-width: 768px) {
        h1 { font-size: 2.1rem !important; }
        .price-tag { font-size: 1.8rem; }
    }
    @media (prefers-reduced-motion: reduce) {
        * { animation: none !important; transition: none !important; }
    }
    </style>
""", unsafe_allow_html=True)

# --- NAVBAR & IN-PAGE MENUS ---
def render_navbar():
    col1, col2, col3, col4 = st.columns([4, 2, 2, 2])
    with col1:
        st.markdown(
            "<div class='brand'><div class='brand-mark'>⚕️</div>"
            "<div><span class='brand-name'>Aerivo</span><span class='brand-sub'>Medical</span></div></div>",
            unsafe_allow_html=True,
        )
    with col2:
        if st.button(f"🛒 Cart ({len(st.session_state.cart)})", use_container_width=True):
            st.session_state.show_cart = not st.session_state.show_cart
            st.session_state.show_account = False
            st.rerun()
    with col3:
        if st.button("👤 Account", use_container_width=True):
            st.session_state.show_account = not st.session_state.show_account
            st.session_state.show_cart = False
            st.rerun()
    with col4:
        if st.button("🌐 Change Region", use_container_width=True):
            st.session_state.language = None
            st.session_state.show_cart = False
            st.session_state.show_account = False
            st.rerun()
    st.markdown("<hr style='margin-top: 8px;'>", unsafe_allow_html=True)

    # Render Account Dropdown Menu
    if st.session_state.show_account:
        with st.container(border=True):
            if not st.session_state.logged_in:
                t1, t2 = st.tabs(["Login", "Sign Up"])
                with t1:
                    u = st.text_input("Username")
                    p = st.text_input("Password", type="password")
                    if st.button("Secure Login", type="primary"):
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
                    if st.button("Create Account", type="primary"):
                        st.success("Account created successfully! You can now login.")
            else:
                st.markdown(f"### Welcome back, {st.session_state.username}!")
                st.write("Your account is verified for medical procurement.")
                if st.button("Logout"):
                    st.session_state.logged_in = False
                    st.session_state.username = ""
                    st.rerun()

    # Render Cart Dropdown Menu
    if st.session_state.show_cart:
        with st.container(border=True):
            st.markdown("### 🛒 Your Secure Shopping Cart")
            if len(st.session_state.cart) > 0:
                for i, item in enumerate(st.session_state.cart):
                    st.markdown(f"**{i+1}. {item}** - $15,500.00")
                st.markdown("<hr>", unsafe_allow_html=True)
                st.markdown(f"**Total Estimated:** ${len(st.session_state.cart) * 15500:,.2f} USD")
                st.write("")
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("Proceed to Checkout ➔", use_container_width=True, type="primary"):
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

# --- REUSABLE UI BLOCKS ---
def render_scroll_cue(text):
    st.markdown(f"""
        <div class='scroll-container'>
            <a href="#gallery-section" class='scroll-cue'>{text} ↓</a>
        </div>
    """, unsafe_allow_html=True)

def render_album_gallery():
    st.markdown("<div id='gallery-section'></div>", unsafe_allow_html=True)
    st.markdown("<br><hr>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; margin-bottom: 1rem;'>Aerivo M1 Environments & Details</h3>", unsafe_allow_html=True)

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
            if st.button("🛒 Add to Cart", use_container_width=True, type="primary"):
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
            if st.button("🛒 In den Warenkorb", use_container_width=True, type="primary"):
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
    st.markdown("<div style='direction: rtl; text-align: right;'>", unsafe_allow_html=True)

    col_img, col_text = st.columns([1, 1.1], gap="large")
    with col_text:
        st.markdown("<h1 style='direction: rtl; text-align: right;'>أيريفو M1: شريكك الموثوق في العناية المركزة</h1>", unsafe_allow_html=True)
        st.markdown("<div class='hero-subtitle' style='direction: rtl; text-align: right;'>تكنولوجيا التنفس الصناعي المتقدمة، بين يديك.</div>", unsafe_allow_html=True)

        st.markdown("<div class='info-chip' style='direction: rtl; text-align: right;'>✔️ مُعتمد ومسجل لدى وزارة الصحة العراقية (MOH) ومطابق لمواصفات (KIMADIA).</div>", unsafe_allow_html=True)

        st.markdown("""
        <div class='rtl-feature-box'>
            <b>دعم شامل وتدريب مستمر</b><br>
            نحن لا نبيع جهازاً فقط، بل نبني شراكة طويلة الأمد. نوفر تدريباً حضورياً شاملاً للكوادر الطبية.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div class='price-tag' style='direction: rtl; text-align: right;'>$15,500.00 USD</div>", unsafe_allow_html=True)

        col_btn1, col_btn2 = st.columns(2)
        with col_btn2:
            if st.button("🛒 إضافة للسلة", use_container_width=True, type="primary"):
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
            background:
                linear-gradient(160deg, rgba(11,42,74,0.55) 0%, rgba(20,168,155,0.25) 100%),
                url("data:image/jpeg;base64,{bg_base64}") !important;
            background-size: cover !important;
            background-position: center !important;
            background-attachment: fixed !important;
        }}
        .block-container {{ padding-top: 12vh !important; max-width: 880px; }}
        .gate-container {{
            background: rgba(255,255,255,0.18);
            border-radius: 28px; padding: 3.5rem 3rem 3rem; text-align: center;
            border: 1px solid rgba(255,255,255,0.45);
            box-shadow: 0 30px 70px rgba(5,20,40,0.35), inset 0 1px 0 rgba(255,255,255,0.6);
            backdrop-filter: blur(22px) saturate(170%); -webkit-backdrop-filter: blur(22px) saturate(170%);
            margin-bottom: 1.4rem;
            animation: rise .8s var(--ease) both;
        }}
        .gate-container h1 {{ color: #FFFFFF !important; font-size: 3.2rem !important; margin-bottom: 0 !important; text-shadow: 0 2px 20px rgba(0,0,0,.25); }}
        .gate-tag {{ color: var(--mint); font-size: 1.05rem; font-weight: 800; margin: 6px 0 1.6rem; letter-spacing: 0.18em; }}
        .gate-text {{ color: rgba(255,255,255,0.92); font-size: 1.1rem; line-height: 1.75; margin: 0 auto; max-width: 640px; }}
        .gate-label {{ text-align: center; color: rgba(255,255,255,0.9); font-weight: 700; margin-bottom: .6rem; }}
        /* Region buttons on the dark photo: bigger glass cards */
        .stButton > button {{ padding: 1.1rem 1rem; font-size: 1.05rem; border-radius: 18px; background: rgba(255,255,255,0.82); }}
        </style>
    """, unsafe_allow_html=True)

    # 3. RENDER GATEWAY CONTENT
    st.markdown("""
        <div class='gate-container'>
            <h1>⚕️ AERIVO MEDICAL</h1>
            <div class='gate-tag'>GLOBAL LIFE SUPPORT SOLUTIONS</div>
            <p class='gate-text'>
                Welcome to the unified Aerivo platform. Please select your region to access custom medical specifications, regulatory certifications, and dedicated procurement channels.
            </p>
        </div>
        <div class='gate-label'>Select your region</div>
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

else:
    if st.session_state.language == 'EN': page_english_global()
    elif st.session_state.language == 'DE': page_german()
    elif st.session_state.language == 'AR': page_arabic()
