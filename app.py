import streamlit as st
import hashlib

# 1. Configuration & Theming (White, Navy, Turquoise, Blue)
st.set_page_config(page_title="AeroVent M1 Medical", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; }
    h1, h2, h3 { color: #000080; font-family: 'Arial', sans-serif; } /* Navy Blue */
    .stButton>button { background-color: #40E0D0; color: #000080; font-weight: bold; border-radius: 8px; border: none; padding: 10px 24px; } /* Turquoise */
    .stButton>button:hover { background-color: #0000FF; color: white; } /* Pure Blue */
    .product-price { font-size: 24px; color: #0000FF; font-weight: bold; }
    .rtl-text { direction: rtl; text-align: right; font-family: 'Tahoma', sans-serif; }
    </style>
""", unsafe_allow_html=True)

# 2. Session State Initialization
if 'language' not in st.session_state:
    st.session_state.language = None
if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'

# --- SECURITY & AUTHENTICATION MODULE ---
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Mock Database for Users (In a real scenario, connects to SQL Server)
USER_DB = {"admin": hash_password("admin123"), "user1": hash_password("pass123")}

def login_page():
    st.subheader("User Login / Admin Panel")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in USER_DB and USER_DB[username] == hash_password(password):
            st.session_state.logged_in = True
            st.success("Logged in successfully!")
            st.rerun()
        else:
            st.error("Invalid credentials. Security logged.")

def cart_widget():
    st.sidebar.markdown(f"### 🛒 Cart ({len(st.session_state.cart)} items)")
    if st.session_state.cart:
        st.sidebar.write("AeroVent M1 Portable Ventilator")
        st.sidebar.markdown("<p class='product-price'>$15,500.00</p>", unsafe_allow_html=True)
        if st.sidebar.button("Checkout"):
            if st.session_state.logged_in:
                st.sidebar.success("Proceeding to secure payment gateway...")
            else:
                st.sidebar.warning("Please login to checkout.")
    
    if not st.session_state.logged_in:
        st.sidebar.markdown("---")
        if st.sidebar.button("Login / Register"):
            st.session_state.current_page = 'login'
            st.rerun()

# --- CULTURAL PAGES BASED ON HOFSTEDE & HALL ---

def english_page():
    st.title("AeroVent M1 Portable Ventilator")
    st.image("https://via.placeholder.com/800x400.png?text=AeroVent+M1+Image", use_container_width=True) # جایگزین با عکس ادیت شده همیلتون
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        ### Intelligent Ventilation Anywhere
        The AeroVent M1 provides high-end ventilation performance in a compact, rugged design. 
        Suitable for all patient groups from neonates to adults.
        - **Battery Life:** 9 hours hot-swappable
        - **Modes:** NIV, CPAP, ASV
        - **Weight:** 6.5 kg
        """)
    with col2:
        st.markdown("<p class='product-price'>Price: $15,500.00</p>", unsafe_allow_html=True)
        if st.button("Add to Cart", key="eng_add"):
            st.session_state.cart.append("AeroVent M1")
            st.success("Added to cart!")

def german_page():
    # Low-Context, High Uncertainty Avoidance
    st.title("AeroVent M1: Präzision und Sicherheit")
    st.info("Zertifiziert nach EU MDR | ISO 13485:2016 konform | DSGVO-konforme Datenverarbeitung")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        ### Technische Spezifikationen & Zuverlässigkeit
        Entwickelt für maximale Ausfallsicherheit im klinischen und präklinischen Einsatz.
        
        * **MTBF (Mean Time Between Failures):** > 50,000 Stunden
        * **Klinische Validierung:** Getestet in über 12 unabhängigen Studien in der DACH-Region.
        * **Datenschutz:** Integrierte Ende-zu-Ende-Verschlüsselung für Patientendaten.
        """)
        
        with st.expander("📄 Technisches Datenblatt herunterladen (PDF)"):
            st.write("Detaillierte Spezifikationen, Wartungszyklen und OEE-Metriken.")
            st.button("Download PDF")
            
    with col2:
        st.markdown("<p class='product-price'>Preis: 14.200 €</p>", unsafe_allow_html=True)
        if st.button("In den Warenkorb", key="ger_add"):
            st.session_state.cart.append("AeroVent M1")
            st.success("Zum Warenkorb hinzugefügt!")

def arabic_page():
    # High-Context, High Power Distance (Relationships, Authority, Visuals)
    st.markdown("<div class='rtl-text'>", unsafe_allow_html=True)
    st.title("أيروڤينت M1: شريكك الموثوق في العناية المركزة")
    
    st.error("مُعتمد رسمياً من قبل وزارة الصحة العراقية (MOH) ومطابق لمواصفات كيماديا (Kimadia)")
    
    st.image("https://via.placeholder.com/800x300.png?text=Doctors+Using+AeroVent", use_container_width=True)
    
    col1, col2 = st.columns([1, 2])
    with col2:
        st.markdown("""
        <div class='rtl-text'>
        <h3>دعم شامل وتدريب مستمر</h3>
        نحن لا نبيع جهازاً فقط، بل نبني شراكة طويلة الأمد مع مؤسستكم الطبية.
        <ul>
            <li><b>الصيانة والضمان:</b> فريق صيانة متواجد في بغداد وأربيل لضمان عدم توقف الجهاز.</li>
            <li><b>التدريب:</b> تدريب حضوري شامل للكوادر الطبية والتمريضية.</li>
        </ul>
        <i>"لقد أحدث جهاز أيروڤينت نقلة نوعية في قسم الطوارئ لدينا." - د. أحمد، مدير مستشفى الطوارئ</i>
        </div>
        """, unsafe_allow_html=True)
    with col1:
        st.markdown("<p class='product-price'>السعر: $15,500.00</p>", unsafe_allow_html=True)
        if st.button("إضافة إلى السلة", key="ar_add"):
            st.session_state.cart.append("AeroVent M1")
            st.success("تمت الإضافة!")
    st.markdown("</div>", unsafe_allow_html=True)

# --- ROUTING LOGIC ---
if st.session_state.current_page == 'login':
    login_page()
    if st.button("Back to Store"):
        st.session_state.current_page = 'home'
        st.rerun()
else:
    if st.session_state.language is None:
        # Language Selection Gateway
        st.markdown("<h1 style='text-align: center;'>Select Your Region / Language</h1>", unsafe_allow_html=True)
        st.write("")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Global (English)", use_container_width=True):
                st.session_state.language = 'EN'
                st.rerun()
        with col2:
            if st.button("Deutschland (Deutsch)", use_container_width=True):
                st.session_state.language = 'DE'
                st.rerun()
        with col3:
            if st.button("العراق (العربية)", use_container_width=True):
                st.session_state.language = 'AR'
                st.rerun()
    else:
        # Top Navigation
        colA, colB = st.columns([4, 1])
        with colA:
            if st.button("🌍 Change Language / تغییر زبان"):
                st.session_state.language = None
                st.rerun()
        
        cart_widget()
        
        st.markdown("---")
        
        # Render Page based on selection
        if st.session_state.language == 'EN':
            english_page()
        elif st.session_state.language == 'DE':
            german_page()
        elif st.session_state.language == 'AR':
            arabic_page()