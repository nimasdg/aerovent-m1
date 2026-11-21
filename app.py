import streamlit as st
import base64
import html
import io
import os
import unicodedata

# --- CONFIGURATION ---
st.set_page_config(page_title="Aerivo Medical | Portable Ventilation", layout="wide", initial_sidebar_state="collapsed")

# --- REGIONAL DATASHEET MAPPING ---
PDF_FILES = {
    "EN": "Portable Medical Ventilator Datasheet.pdf",
    "DE": "Technisches Datenblatt Beatmungsgerät.pdf",
    "AR": "البطاقة الفنية لجهاز التنفس الاصطناعي المحمول.pdf",
}

# --- UTILITIES ---
@st.cache_data
def get_base64_of_bin_file(bin_file):
    if os.path.exists(bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return ""

# --- IMAGE HELPERS (PNG/JPG aware, resized + cached so the page stays light) ---
_MIME = {".png": "image/png", ".png": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp"}

def resolve_image_path(path):
    """Return an existing file for `path`; also tries the same name with other image extensions."""
    if os.path.exists(path):
        return path
    stem = os.path.splitext(path)[0]
    for ext in (".png", ".png", ".jpeg", ".webp"):
        if os.path.exists(stem + ext):
            return stem + ext
    return ""

@st.cache_data(show_spinner=False)
def _image_data_uri(real_path, mtime, max_w):
    ext = os.path.splitext(real_path)[1].lower()
    try:
        from PIL import Image
        with Image.open(real_path) as im:
            im.load()
            if im.width > max_w:
                im = im.resize((max_w, round(im.height * max_w / im.width)), Image.LANCZOS)
            has_alpha = im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info)
            buf = io.BytesIO()
            if has_alpha:
                im.convert("RGBA").save(buf, "PNG", optimize=True)
                mime = "image/png"
            else:
                im.convert("RGB").save(buf, "JPEG", quality=86, optimize=True, progressive=True)
                mime = "image/jpeg"
        return f"data:{mime};base64," + base64.b64encode(buf.getvalue()).decode()
    except Exception:
        with open(real_path, "rb") as f:
            raw = f.read()
        return f"data:{_MIME.get(ext, 'image/jpeg')};base64," + base64.b64encode(raw).decode()

def get_image_data_uri(path, max_w=1600):
    real = resolve_image_path(path)
    if not real:
        return ""
    return _image_data_uri(real, os.path.getmtime(real), max_w)

def render_zoom_image(path, caption=""):
    """Click the picture -> it opens full-screen (pure CSS :target, no JavaScript).
    Close with the X button, by clicking the dark backdrop, or any click outside the image."""
    uri = get_image_data_uri(path)
    if not uri:
        return False
    render_zoom_image._n = getattr(render_zoom_image, "_n", 0) + 1
    zid = f"zi-{render_zoom_image._n}"
    alt = html.escape(caption or "Aerivo M1", quote=True)
    cap = f"<figcaption class='zoom-cap'>{html.escape(caption)}</figcaption>" if caption else ""
    st.markdown(
        f"<figure id='{zid}' class='zoom-item'>"
        f"<a class='zoom-open' href='#{zid}' aria-label='Enlarge image'></a>"
        f"<img src='{uri}' alt='{alt}'>"
        f"<span class='zoom-badge'>⤢</span>{cap}"
        f"<a class='zoom-backdrop' href='#_' aria-label='Close image'></a>"
        f"<a class='zoom-close' href='#_' aria-label='Close image' title='Close'>✕</a>"
        f"</figure>",
        unsafe_allow_html=True,
    )
    return True

@st.cache_data
def get_pdf_bytes(filename):
    if os.path.exists(filename):
        with open(filename, "rb") as f:
            return f.read()
    # Fallback with Unicode normalization (handles ä / Arabic filenames across Windows & Linux)
    target_norm = unicodedata.normalize("NFC", filename)
    for entry in os.listdir("."):
        if unicodedata.normalize("NFC", entry) == target_norm:
            with open(entry, "rb") as f:
                return f.read()
    return b""

# --- SESSION STATE INITIALIZATION ---
if 'language' not in st.session_state:
    st.session_state.language = None
if 'cart' not in st.session_state:
    st.session_state.cart = []  # List of dicts: {"name": str, "price": float, "currency": str, "ref": str}
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'show_cart' not in st.session_state:
    st.session_state.show_cart = False
if 'show_account' not in st.session_state:
    st.session_state.show_account = False
if 'show_rfq' not in st.session_state:
    st.session_state.show_rfq = False
if 'show_demo' not in st.session_state:
    st.session_state.show_demo = False
if 'user_prefs' not in st.session_state:
    st.session_state.user_prefs = None
if 'feedback_submitted' not in st.session_state:
    st.session_state.feedback_submitted = False

def add_to_cart(name, price, currency="USD", ref="AERV-M1"):
    st.session_state.cart.append({
        "name": name,
        "price": price,
        "currency": currency,
        "ref": ref
    })
    st.session_state.show_cart = True
    st.session_state.show_account = False
    st.rerun()

# --- CORE CSS (PRESERVED DESIGN + MATCHING STYLES FOR NEW MODULES) ---
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
    h1 { font-size: 2.75rem !important; line-height: 1.12 !important; margin-bottom: .4rem !important; }
    p, li, label, .stMarkdown { color: var(--ink-soft); }
    .hero-subtitle { font-size: 1.2rem; color: var(--ocean); margin: .2rem 0 1.4rem; line-height: 1.55; font-weight: 500; }

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
    .feature-box b, .rtl-feature-box b { color: var(--navy); font-size: 1.05rem; }

    /* Glass Card Grid (for Consumables, Tiers, Team, etc.) */
    .glass-card {
        background: var(--glass); border: 1px solid var(--glass-border); border-radius: 20px;
        padding: 1.35rem; margin-bottom: 1rem; height: 100%;
        backdrop-filter: blur(16px) saturate(160%); -webkit-backdrop-filter: blur(16px) saturate(160%);
        box-shadow: var(--shadow-sm), inset 0 1px 0 rgba(255,255,255,.9);
        transition: transform .3s var(--ease), box-shadow .3s var(--ease), background .3s var(--ease);
    }
    .glass-card:hover { transform: translateY(-4px); background: var(--glass-strong); box-shadow: var(--shadow-md); }
    .glass-card-rtl { direction: rtl; text-align: right; }

    /* Styled Clinical Tables (Specs & TCO) */
    .clinical-table {
        width: 100%; border-collapse: separate; border-spacing: 0;
        background: var(--glass-strong); border-radius: 18px; overflow: hidden;
        border: 1px solid var(--glass-border); box-shadow: var(--shadow-sm);
        margin: 1rem 0 1.5rem; font-size: 0.94rem;
    }
    .clinical-table th {
        background: linear-gradient(135deg, var(--navy), var(--ocean)); color: #FFFFFF;
        padding: 13px 16px; text-align: left; font-weight: 700;
    }
    .clinical-table td {
        padding: 12px 16px; border-bottom: 1px solid rgba(27,111,181,0.12); color: var(--navy);
    }
    .clinical-table tr:last-child td { border-bottom: none; }
    .clinical-table tr:nth-child(even) td { background: rgba(234,244,251,0.45); }
    .clinical-table-rtl th, .clinical-table-rtl td { text-align: right; direction: rtl; }

    /* WhatsApp Action & Floating Button (Iraq Mode) */
    .wa-btn-inline {
        display: inline-flex; align-items: center; justify-content: center; gap: 8px; width: 100%;
        background: linear-gradient(135deg, #25D366 0%, #128C7E 100%); color: #FFFFFF !important;
        font-weight: 800; font-size: 1rem; padding: 0.72rem 1.2rem; border-radius: 14px;
        text-decoration: none !important; box-shadow: 0 10px 24px rgba(18,140,126,0.35);
        transition: transform .25s var(--ease), box-shadow .25s var(--ease);
    }
    .wa-btn-inline:hover { transform: translateY(-3px); box-shadow: 0 14px 30px rgba(18,140,126,0.45); }

    .wa-floating {
        position: fixed; bottom: 24px; left: 24px; z-index: 99999;
        display: inline-flex; align-items: center; gap: 10px;
        background: linear-gradient(135deg, #25D366 0%, #128C7E 100%); color: #FFFFFF !important;
        padding: 13px 22px; border-radius: 999px; font-weight: 800; font-size: 0.95rem;
        text-decoration: none !important; box-shadow: 0 12px 30px rgba(18,140,126,0.45);
        border: 2px solid rgba(255,255,255,0.65); transition: transform .25s var(--ease);
        direction: rtl;
    }
    .wa-floating:hover { transform: translateY(-4px) scale(1.03); }

    .price-tag {
        display: inline-block; font-size: 2.1rem; font-weight: 800; margin: 1rem 0 1.2rem;
        background: linear-gradient(135deg, var(--ocean), var(--teal));
        -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent;
    }
    .cert-badge {
        display: inline-block; background: var(--glass-strong); color: var(--navy);
        padding: 0.38rem 0.85rem; border-radius: 999px; font-weight: 700; font-size: 0.8rem;
        margin: 0 0.45rem 0.45rem 0; border: 1px solid var(--glass-border);
        box-shadow: var(--shadow-sm); backdrop-filter: blur(10px);
        transition: transform .25s var(--ease), box-shadow .25s var(--ease), border-color .25s var(--ease);
    }
    .cert-badge:hover { transform: translateY(-2px); border-color: var(--mint); box-shadow: 0 8px 18px rgba(20,168,155,.2); }
    .ec-rep-bar {
        background: rgba(255,255,255,0.72); border: 1px solid rgba(27,111,181,0.22);
        border-radius: 12px; padding: 10px 14px; font-size: 0.84rem; color: var(--navy);
        margin-bottom: 1.1rem; backdrop-filter: blur(10px);
    }
    .info-chip {
        background: rgba(232,247,238,0.85); color: #1E6B3A; padding: 12px 16px; border-radius: 14px;
        margin-bottom: 15px; font-weight: 700; border: 1px solid rgba(120,200,150,0.55);
        backdrop-filter: blur(10px);
    }
    .section-kicker {
        display: inline-block; font-size: 0.78rem; font-weight: 800; letter-spacing: 0.12em;
        text-transform: uppercase; color: var(--teal-dark); margin-bottom: 0.3rem;
    }
    hr { border: none !important; height: 1px; background: linear-gradient(90deg, transparent, rgba(27,111,181,0.35), transparent) !important; margin: 1.2rem 0 !important; }

    /* ---------- NAVBAR ---------- */
    .brand { display:flex; align-items:center; gap:.7rem; margin: 0; }
    .brand-mark {
        width: 42px; height: 42px; border-radius: 13px; display:flex; align-items:center; justify-content:center;
        background: linear-gradient(135deg, var(--teal), var(--ocean)); color:#fff; font-size: 1.25rem;
        box-shadow: 0 8px 20px rgba(20,168,155,.35), inset 0 1px 0 rgba(255,255,255,.5);
    }
    .brand-name { font-size: 1.55rem; font-weight: 800; color: var(--navy); letter-spacing: -0.03em; }
    .brand-sub { display:block; font-size: .72rem; font-weight: 600; color: var(--ocean); letter-spacing: .02em; margin-top: -3px; }

    /* ---------- PANELS (cart / account / forms) ---------- */
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
    .stTextInput input, .stTextArea textarea, .stSelectbox > div > div {
        background: rgba(255,255,255,0.85) !important; color: var(--navy) !important;
        border: 1px solid rgba(27,111,181,0.25) !important; border-radius: 12px !important;
    }
    [data-testid="stAlert"] { border-radius: 14px; backdrop-filter: blur(10px); }

    /* ---------- TABS ---------- */
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
    [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, var(--teal), var(--ocean)) !important; color: #fff !important;
        box-shadow: 0 6px 16px rgba(20,168,155,.35);
    }
    [data-baseweb="tab-highlight"], [data-baseweb="tab-border"] { display: none !important; }

    /* ---------- IMAGES + CSS-ONLY LIGHTBOX ---------- */
    .zoom-item { position: relative; margin: 0 0 1rem; }
    .zoom-item img {
        display: block; width: 100%; height: auto; border-radius: 22px; box-shadow: var(--shadow-md);
        transition: transform .45s var(--ease), box-shadow .4s var(--ease);
    }
    .zoom-item .zoom-open { position: absolute; inset: 0; z-index: 2; border-radius: 22px; cursor: zoom-in; }
    .zoom-item:hover img { transform: translateY(-4px) scale(1.015); box-shadow: 0 22px 50px rgba(11,42,74,.22); }
    .zoom-item .zoom-open:active + img { transform: scale(.97); }
    .zoom-badge {
        position: absolute; top: 12px; right: 12px; z-index: 3; width: 34px; height: 34px; border-radius: 50%;
        display: flex; align-items: center; justify-content: center; pointer-events: none; font-size: 1rem;
        background: var(--glass-strong); color: var(--navy); border: 1px solid var(--glass-border);
        backdrop-filter: blur(10px); box-shadow: var(--shadow-sm); opacity: 0; transform: scale(.8);
        transition: opacity .25s var(--ease), transform .25s var(--ease);
    }
    .zoom-item:hover .zoom-badge { opacity: 1; transform: none; }
    .zoom-cap { text-align: center; color: var(--ink-soft); font-weight: 600; font-size: .9rem; margin-top: .55rem; }
    .zoom-backdrop, .zoom-close { display: none; }

    /* Opened state: the same figure becomes a full-screen overlay (:target) */
    .zoom-item:target {
        position: fixed; inset: 0; z-index: 999999; margin: 0; padding: 4vh 4vw;
        display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 14px;
        background: rgba(8, 28, 52, 0.78);
        backdrop-filter: blur(14px) saturate(150%); -webkit-backdrop-filter: blur(14px) saturate(150%);
        animation: lb-fade .25s ease-out both;
    }
    .zoom-item:target .zoom-open, .zoom-item:target .zoom-badge { display: none; }
    .zoom-item:target .zoom-backdrop { display: block; position: absolute; inset: 0; z-index: 0; cursor: zoom-out; }
    .zoom-item:target img {
        position: relative; z-index: 1; width: auto; max-width: 92vw; max-height: 80vh; object-fit: contain;
        transform: none !important; border: 1px solid rgba(255,255,255,0.45);
        box-shadow: 0 30px 80px rgba(0,0,0,0.5); animation: lb-pop .35s var(--ease) both;
    }
    .zoom-item:target .zoom-cap { position: relative; z-index: 1; color: #fff; margin: 0; font-size: 1rem; }
    .zoom-item:target .zoom-close {
        display: flex; position: fixed; top: 22px; right: 22px; z-index: 3; width: 54px; height: 54px;
        border-radius: 50%; align-items: center; justify-content: center; text-decoration: none !important;
        font-size: 1.6rem; font-weight: 800; line-height: 1; color: var(--navy) !important;
        background: rgba(255,255,255,0.95); border: 1px solid #fff; box-shadow: 0 10px 28px rgba(0,0,0,0.4);
        transition: transform .25s var(--ease), background .25s var(--ease), color .25s var(--ease);
    }
    .zoom-item:target .zoom-close:hover { background: var(--teal); color: #fff !important; transform: rotate(90deg) scale(1.08); }
    .zoom-item:target .zoom-close:active { transform: rotate(90deg) scale(.9); }
    @keyframes lb-fade { from { opacity: 0; } to { opacity: 1; } }
    @keyframes lb-pop { from { opacity: 0; transform: scale(.92); } to { opacity: 1; } }

    /* ---------- EXPANDER (personalization) ---------- */
    [data-testid="stExpander"] {
        background: var(--glass) !important; border: 1px solid var(--glass-border) !important;
        border-radius: 18px !important; box-shadow: var(--shadow-sm);
        backdrop-filter: blur(14px) saturate(160%); -webkit-backdrop-filter: blur(14px) saturate(160%);
        margin-bottom: 1.2rem; overflow: hidden;
    }
    [data-testid="stExpander"] summary { font-weight: 700; color: var(--navy); transition: background .25s var(--ease); }
    [data-testid="stExpander"] summary:hover { background: rgba(255,255,255,.6); }
    [data-testid="stExpander"] summary:active { background: rgba(20,168,155,.12); }

    /* ---------- CLICK FEEDBACK (restored) ---------- */
    .feature-box:active, .rtl-feature-box:active, .glass-card:active { transform: translateY(-1px) scale(0.985); }
    .cert-badge:active { transform: scale(.94); }
    [data-baseweb="tab"]:active { transform: scale(.94); }
    .scroll-cue:active, .wa-btn-inline:active, .wa-floating:active { transform: scale(.95); }
    .stTextInput input, .stTextArea textarea { transition: box-shadow .25s var(--ease), border-color .25s var(--ease); }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: var(--teal) !important; box-shadow: 0 0 0 4px rgba(20,168,155,0.18) !important;
    }

    /* ---------- SCROLL CUE ---------- */
    @keyframes gentle-bob { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-5px); } }
    .scroll-container { text-align: center; margin: 1.8rem 0 .5rem; }
    .scroll-cue {
        display: inline-flex; align-items: center; gap: .6rem; animation: gentle-bob 3s ease-in-out infinite;
        background: var(--glass-strong); color: var(--navy); font-weight: 700; font-size: 1rem;
        padding: 12px 26px; border-radius: 999px; text-decoration: none !important;
        border: 1px solid var(--glass-border); box-shadow: var(--shadow-sm); backdrop-filter: blur(14px);
        transition: background .3s var(--ease), color .3s var(--ease), box-shadow .3s var(--ease);
    }
    .scroll-cue:hover { background: linear-gradient(135deg, var(--teal), var(--ocean)); color: #fff !important; box-shadow: 0 12px 28px rgba(20,168,155,.35); }

    @keyframes rise { from { opacity: 0; transform: translateY(18px); } to { opacity: 1; transform: none; } }
    h1 { animation: rise .7s var(--ease) both; }
    .hero-subtitle { animation: rise .7s .12s var(--ease) both; }

    @media (max-width: 768px) {
        h1 { font-size: 2rem !important; }
        .price-tag { font-size: 1.7rem; }
        .clinical-table { display: block; overflow-x: auto; }
        .wa-floating { left: 12px; right: 12px; bottom: 12px; justify-content: center; }
        .zoom-item:target .zoom-close { top: 14px; right: 14px; }
    }
    @media (prefers-reduced-motion: reduce) {
        * { animation: none !important; transition: none !important; }
    }
    </style>
""", unsafe_allow_html=True)

# --- NAVBAR & IN-PAGE MENUS ---
def render_navbar(lang="EN"):
    col1, col2, col3, col4 = st.columns([4, 2, 2, 2])
    with col1:
        st.markdown(
            "<div class='brand'><div class='brand-mark'>⚕️</div>"
            "<div><span class='brand-name'>Aerivo</span><span class='brand-sub'>Medical Systems</span></div></div>",
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
            st.session_state.show_rfq = False
            st.session_state.show_demo = False
            st.rerun()
    st.markdown("<hr style='margin-top: 8px;'>", unsafe_allow_html=True)

    # Render Account Dropdown Menu
    if st.session_state.show_account:
        with st.container(border=True):
            if not st.session_state.logged_in:
                t1, t2 = st.tabs(["Login", "Sign Up"])
                with t1:
                    u = st.text_input("Username / Institutional Email", key="login_u")
                    p = st.text_input("Password", type="password", key="login_p")
                    if st.button("Secure Login", type="primary"):
                        if u and p:
                            st.session_state.logged_in = True
                            st.session_state.username = u
                            st.session_state.show_account = False
                            st.rerun()
                        else:
                            st.error("Please enter credentials.")
                with t2:
                    st.text_input("Full Name / Organization", key="reg_name")
                    st.text_input("Email Address", key="reg_email")
                    st.text_input("Choose Password", type="password", key="reg_pwd")
                    if st.button("Create Account", type="primary"):
                        st.success("Account created successfully! You can now login.")
            else:
                st.markdown(f"### Welcome back, {st.session_state.username}")
                st.write("Verified procurement account (ISO 13485 Portal).")
                if st.button("Logout"):
                    st.session_state.logged_in = False
                    st.session_state.username = ""
                    st.rerun()

    # Render Cart Dropdown Menu
    if st.session_state.show_cart:
        with st.container(border=True):
            st.markdown("### 🛒 Your Secure Procurement Cart")
            if len(st.session_state.cart) > 0:
                totals = {}
                for i, item in enumerate(st.session_state.cart):
                    c_item, c_del = st.columns([5, 1])
                    with c_item:
                        sym = "€" if item["currency"] == "EUR" else "$"
                        st.markdown(f"**{i+1}. {item['name']}** (`{item['ref']}`) — **{sym}{item['price']:,.0f}**")
                    with c_del:
                        if st.button("✕", key=f"del_cart_{i}"):
                            st.session_state.cart.pop(i)
                            st.rerun()
                    totals[item["currency"]] = totals.get(item["currency"], 0) + item["price"]
                st.markdown("<hr>", unsafe_allow_html=True)
                labels = {"EUR": "EUR (€)", "USD": "USD ($)"}
                for cur, amount in totals.items():
                    st.markdown(f"**Estimated Total:** {amount:,.2f} {labels.get(cur, cur)}")
                st.write("")
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("Proceed to Checkout / Proforma ➔", use_container_width=True, type="primary"):
                        if st.session_state.logged_in:
                            st.success("Order submitted! Official Proforma Invoice generated.")
                        else:
                            st.warning("Please login via Account to finalize procurement.")
                with c2:
                    if st.button("Clear Cart", use_container_width=True):
                        st.session_state.cart = []
                        st.rerun()
            else:
                st.info("Your cart is empty. Add the Aerivo M1 or consumables to proceed.")

# --- 3-QUESTION PERSONALIZATION MODULE (ANTI-STEREOTYPING) ---
def render_personalization_module(lang="EN"):
    labels = {
        "EN": {
            "exp": "🎯 Personalize Your Experience (3 Quick Questions)",
            "q1": "1. How do you prefer to evaluate medical devices?",
            "o1": ["Technical Datasheets & Standards", "Clinical Video & Visual Walkthrough"],
            "q2": "2. Preferred communication channel?",
            "o2": ["Formal RFQ / Email Documentation", "Direct Live Chat / Phone Consultation"],
            "q3": "3. Primary focus area?",
            "o3": ["Regulatory Compliance & TCO", "Clinical Portability & Rapid Support"],
            "btn": "Apply Personalization",
            "rec_doc": "✅ Tailored for you: We prioritized Technical Specs, Regulatory Compliance, and Formal RFQ below.",
            "rec_vid": "✅ Tailored for you: We prioritized Clinical Demonstrations, Direct Specialist Contact, and Training below."
        },
        "DE": {
            "exp": "🎯 Benutzererfahrung personalisieren (3 kurze Fragen)",
            "q1": "1. Wie bewerten Sie Medizingeräte bevorzugt?",
            "o1": ["Technische Datenblätter & Normen", "Klinisches Video & visuelle Demo"],
            "q2": "2. Bevorzugter Kommunikationskanal?",
            "o2": ["Formelles Angebot (RFQ) / E-Mail", "Direkter Experten-Chat / Telefonat"],
            "q3": "3. Hauptfokus Ihrer Beschaffung?",
            "o3": ["MDR-Konformität & 10-Jahres-TCO", "Klinische Mobilität & schneller Service"],
            "btn": "Einstellungen anwenden",
            "rec_doc": "✅ Personalisiert: Fokus auf EU-MDR-Dokumentation, TCO-Tabelle und offizielles RFQ-Formular aktiviert.",
            "rec_vid": "✅ Personalisiert: Direkter Expertenkontakt, klinische Einsatzbilder und Live-Demo-Optionen hervorgehoben."
        },
        "AR": {
            "exp": "🎯 خصّص تجربتك حسب احتياجك (3 أسئلة سريعة)",
            "q1": "1. كيف تفضل تقييم الأجهزة الطبية؟",
            "o1": ["المواصفات الفنية والوثائق الرسمية", "فيديو سريري وعرض عملي للجهاز"],
            "q2": "2. وسيلة التواصل المفضلة لديك؟",
            "o2": ["عرض سعر رسمي للمناقصات (RFQ)", "محادثة فورية عبر واتساب مع خبير"],
            "q3": "3. ما هي أولويتك الأساسية؟",
            "o3": ["شهادات الجودة والاعتمادات الرسمية", "السعر التنافسي، التدريب والصيانة المحلية"],
            "btn": "تطبيق التخصيص",
            "rec_doc": "✅ تم التخصيص: تم إبراز ملفات المواصفات الفنية ووثائق المناقصات الرسمية (KIMADIA / CFS / ISO) أدناه.",
            "rec_vid": "✅ تم التخصيص: تم إبراز الفيديو السريري، التواصل الفوري عبر واتساب، وبرامج التدريب الميداني أدناه."
        }
    }[lang]

    with st.expander(labels["exp"], expanded=False):
        if lang == "AR":
            st.markdown("<div style='direction: rtl; text-align: right;'>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            a1 = st.radio(labels["q1"], labels["o1"], key=f"p_q1_{lang}")
        with c2:
            a2 = st.radio(labels["q2"], labels["o2"], key=f"p_q2_{lang}")
        with c3:
            a3 = st.radio(labels["q3"], labels["o3"], key=f"p_q3_{lang}")
        if st.button(labels["btn"], key=f"p_btn_{lang}", type="primary"):
            st.session_state.user_prefs = {"eval": a1, "comm": a2, "focus": a3, "lang": lang}
        if lang == "AR":
            st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.user_prefs and st.session_state.user_prefs.get("lang") == lang:
        is_doc = st.session_state.user_prefs["eval"] == labels["o1"][0]
        msg = labels["rec_doc"] if is_doc else labels["rec_vid"]
        if lang == "AR":
            st.markdown(f"<div class='info-chip' style='direction: rtl; text-align: right;'>{msg}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='info-chip'>{msg}</div>", unsafe_allow_html=True)

# --- CONSUMABLES & ACCESSORIES (RECURRING REVENUE MODULE) ---
def render_consumables_accessories(lang="EN"):
    st.markdown("<hr>", unsafe_allow_html=True)
    if lang == "DE":
        st.markdown("<div class='section-kicker'>Wiederkehrende Versorgung & Zubehör</div>", unsafe_allow_html=True)
        st.markdown("<h3>Verbrauchsmaterialien & Zubehör (Recurring Supply)</h3>", unsafe_allow_html=True)
        st.write("Original-Verbrauchsmaterialien sichern die MDR-Konformität und garantieren langfristige Betriebssicherheit.")
        curr, sym = "EUR", "€"
        items_cons = [
            ("Einweg-Beatmungsschlauchsystem (10 Stk.)", "REF: AERV-CIR-01", 240, "Steril, Erwachsene/Pädiatrie, latexfrei"),
            ("Antibakterieller HEPA/HME-Filter (50 Stk.)", "REF: AERV-FLT-02", 185, "99,999% Filtrationseffizienz"),
            ("NIV-Beatmungsmaske (Set S/M/L)", "REF: AERV-MSK-03", 160, "Ergonomische Silikonabdichtung"),
            ("Aktiver Atemgasbefeuchter & Flow-Sensoren", "REF: AERV-HUM-04", 690, "Präzise Durchflussmessung & Kondensationsschutz"),
        ]
        items_acc = [
            ("Hot-Swap Ersatzakku (Li-Ion, +4 Std.)", "REF: AERV-BAT-05", 520, "Verlängert Laufzeit auf bis zu 8+ Stunden"),
            ("Intensiv-Gerätewagen (Trolley) & Tragetasche", "REF: AERV-TRL-06", 1150, "Stoßfest für Klinik- und Rettungstransport"),
        ]
        btn_lbl = "🛒 Hinzufügen"
    elif lang == "AR":
        st.markdown("<div style='direction: rtl; text-align: right;'>", unsafe_allow_html=True)
        st.markdown("<div class='section-kicker'>التوريد المستمر وقطع الغيار</div>", unsafe_allow_html=True)
        st.markdown("<h3 style='direction: rtl; text-align: right;'>المستلزمات الاستهلاكية والملحقات (Consumables & Accessories)</h3>", unsafe_allow_html=True)
        st.markdown("<p style='direction: rtl; text-align: right;'>نوفر إمداداً فورياً ومستمراً لجميع المستهلكات الطبية وقطع الغيار الأصلية لضمان عدم توقف الجهاز في المستشفيات.</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        curr, sym = "USD", "$"
        items_cons = [
            ("دائرة تنفس أحادية الاستخدام (10 قطع)", "REF: AERV-CIR-01", 260, "معقمة ومناسبة للبالغين والأطفال"),
            ("فلتر مضاد للبكتيريا والفيروسات (50 قطعة)", "REF: AERV-FLT-02", 195, "كفاءة ترشيح 99.999% لحماية المريض"),
            ("كمامة تنفس غير جراحي NIV (طقم كامل)", "REF: AERV-MSK-03", 175, "سيليكون طبي مريح لمنع التسرب"),
            ("مرطب هواء نشط ومستشعرات التدفق", "REF: AERV-HUM-04", 740, "حساسات دقيقة لضمان استقرار الأكسجين"),
        ]
        items_acc = [
            ("بطارية احتياطية إضافية (تعمل حتى 8 ساعات)", "REF: AERV-BAT-05", 550, "مثالية لمواجهة انقطاع وتذبذب الكهرباء"),
            ("عربة نقل طبية (Trolley) + حقيبة حمل مبطنة", "REF: AERV-TRL-06", 1200, "جاهزة للنقل داخل المستشفى وسيارات الإسعاف"),
        ]
        btn_lbl = "🛒 أضف للسلة"
    else:
        st.markdown("<div class='section-kicker'>Lifecycle & Recurring Supply</div>", unsafe_allow_html=True)
        st.markdown("<h3>Consumables & Accessories</h3>", unsafe_allow_html=True)
        st.write("Ensure uninterrupted ventilation and hospital lifecycle continuity with certified Aerivo consumables and transport accessories.")
        curr, sym = "USD", "$"
        items_cons = [
            ("Disposable Breathing Circuit (Box of 10)", "REF: AERV-CIR-01", 260, "Sterile, Adult/Pediatric, latex-free"),
            ("Antibacterial/Viral HEPA Filter (Box of 50)", "REF: AERV-FLT-02", 195, "99.999% filtration efficiency"),
            ("NIV Non-Invasive Mask Kit (S/M/L)", "REF: AERV-MSK-03", 175, "Soft silicone cushion, leak-compensated"),
            ("Active Humidifier & Flow Sensor Pack", "REF: AERV-HUM-04", 740, "Proximal flow accuracy & thermal control"),
        ]
        items_acc = [
            ("Hot-Swappable Spare Battery (+4 hrs)", "REF: AERV-BAT-05", 550, "Extends portable runtime up to 8+ hours"),
            ("Clinical Trolley & Rugged Carrying Case", "REF: AERV-TRL-06", 1200, "Shock-resistant mobility for ICU & EMS"),
        ]
        btn_lbl = "🛒 Add to Cart"

    t_cons, t_acc = st.tabs(
        ["Consumables" if lang == "EN" else ("Verbrauchsmaterialien" if lang == "DE" else "المستلزمات الاستهلاكية"),
         "Accessories" if lang == "EN" else ("Zubehör" if lang == "DE" else "الملحقات والبطاريات")]
    )
    rtl_cls = " glass-card-rtl" if lang == "AR" else ""

    with t_cons:
        cols = st.columns(4)
        for idx, (title, ref, price, desc) in enumerate(items_cons):
            with cols[idx]:
                st.markdown(f"""
                <div class='glass-card{rtl_cls}'>
                    <div style='font-size:0.75rem; color:var(--ocean); font-weight:700;'>{ref}</div>
                    <div style='font-weight:800; color:var(--navy); margin:6px 0; min-height:44px;'>{title}</div>
                    <div style='font-size:0.86rem; color:var(--ink-soft); min-height:48px;'>{desc}</div>
                    <div style='font-size:1.25rem; font-weight:800; color:var(--teal-dark); margin-top:8px;'>{sym}{price:,}</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(btn_lbl, key=f"cons_{lang}_{idx}", use_container_width=True):
                    add_to_cart(title, price, curr, ref)

    with t_acc:
        cols = st.columns(2)
        for idx, (title, ref, price, desc) in enumerate(items_acc):
            with cols[idx]:
                st.markdown(f"""
                <div class='glass-card{rtl_cls}'>
                    <div style='font-size:0.75rem; color:var(--ocean); font-weight:700;'>{ref}</div>
                    <div style='font-weight:800; color:var(--navy); margin:6px 0;'>{title}</div>
                    <div style='font-size:0.9rem; color:var(--ink-soft);'>{desc}</div>
                    <div style='font-size:1.35rem; font-weight:800; color:var(--teal-dark); margin-top:10px;'>{sym}{price:,}</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(btn_lbl, key=f"acc_{lang}_{idx}", use_container_width=True):
                    add_to_cart(title, price, curr, ref)

# --- FEEDBACK SECTION ---
def render_feedback_section(lang="EN"):
    st.markdown("<hr>", unsafe_allow_html=True)
    txt = {
        "EN": ("Customer & Evaluator Feedback", "Help us improve our regional catalog and technical documentation.", "Overall Experience (1-5)", "Your comments or missing specifications", "Submit Feedback", "Thank you! Your feedback has been recorded."),
        "DE": ("Feedback & Qualitätsbewertung", "Helfen Sie uns, unsere technische Dokumentation und den Beschaffungsprozess weiter zu optimieren.", "Bewertung der Informationsklarheit (1-5)", "Ihre Anmerkungen oder fehlende Dokumente", "Feedback absenden", "Vielen Dank! Ihr Feedback wurde erfolgreich übermittelt."),
        "AR": ("تقييمك وملاحظاتك (Feedback)", "رأيك يساعدنا على تطوير خدماتنا وتوفير المعلومات التي تحتاجها لمؤسستك الطبية.", "تقييمك للموقع وسهولة الوصول للمعلومات (1-5)", "اكتب ملاحظاتك أو أي استفسار إضافي", "إرسال التقييم", "شكراً لك! تم استلام تقييمك بنجاح.")
    }[lang]

    with st.container(border=True):
        if lang == "AR":
            st.markdown(f"<h4 style='direction:rtl; text-align:right;'>💬 {txt[0]}</h4><p style='direction:rtl; text-align:right;'>{txt[1]}</p>", unsafe_allow_html=True)
        else:
            st.markdown(f"<h4>💬 {txt[0]}</h4><p>{txt[1]}</p>", unsafe_allow_html=True)
        c1, c2 = st.columns([1, 2])
        with c1:
            st.slider(txt[2], 1, 5, 5, key=f"fb_rate_{lang}")
        with c2:
            st.text_input(txt[3], key=f"fb_txt_{lang}")
        if st.button(txt[4], key=f"fb_btn_{lang}"):
            st.success(txt[5])

# --- REUSABLE UI BLOCKS ---
def render_scroll_cue(text):
    st.markdown(f"""
        <div class='scroll-container'>
            <a href="#gallery-section" class='scroll-cue'>{text} ↓</a>
        </div>
    """, unsafe_allow_html=True)

def render_album_gallery(lang="EN"):
    st.markdown("<div id='gallery-section'></div>", unsafe_allow_html=True)
    st.markdown("<br><hr>", unsafe_allow_html=True)
    heading = {
        "EN": "Aerivo M1 Clinical Environments & Hardware Details",
        "DE": "Aerivo M1: Klinische Einsatzbereiche & Gerätedetails",
        "AR": "أيريفو M1 في البيئات السريرية وتفاصيل الجهاز"
    }[lang]
    st.markdown(f"<h3 style='text-align: center; margin-bottom: 1rem;'>{heading}</h3>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["🏥 Clinical Settings", "🚁 Transport & Emergency", "⚙️ Product Details"])
    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            render_zoom_image("Aerivo (8).png", "ICU Clinical Setting")
        with c2:
            render_zoom_image("Aerivo (9).png", "Operating Room Configuration")
    with tab2:
        c1, c2, c3 = st.columns(3)
        with c1:
            render_zoom_image("Aerivo (10).png", "Ambulance Installation")
        with c2:
            render_zoom_image("Aerivo (11).png", "Helicopter Emergency Services")
        with c3:
            render_zoom_image("Aerivo (2).png", "Field & Disaster Care")
    with tab3:
        c1, c2, c3 = st.columns(3)
        with c1:
            render_zoom_image("Aerivo (3).png", "Front Control Panel & UI")
        with c2:
            render_zoom_image("Aerivo (4).png", "Rear View & Connectivity Ports")
        with c3:
            render_zoom_image("Aerivo (5).png", "Accessories & Travel Kit")

def render_tech_specs_button(lang="EN", label="📄 Tech Specs", download_name=None):
    source_file = PDF_FILES.get(lang, PDF_FILES["EN"])
    data = get_pdf_bytes(source_file)
    out_name = download_name or source_file
    if data:
        st.download_button(
            label=label,
            data=data,
            file_name=out_name,
            mime="application/pdf",
            use_container_width=True,
            key=f"dl_pdf_{lang}_{out_name}"
        )
    else:
        st.button(f"{label} (PDF Missing: {source_file})", disabled=True, use_container_width=True)

def render_main_product_image():
    if not render_zoom_image("Aerivo (6).png", "Aerivo M1"):
        st.info("Product Image Loading...")

# ==============================================================================
# 1. GLOBAL / ENGLISH PAGE (Technical Reference)
# ==============================================================================
def page_english_global():
    render_navbar("EN")
    render_personalization_module("EN")

    col_text, col_img = st.columns([1.1, 1], gap="large")
    with col_text:
        st.markdown("<div class='section-kicker'>REF: AERV-M1-GLB | Portable ICU Ventilator</div>", unsafe_allow_html=True)
        st.markdown("<h1>Aerivo M1 Portable Ventilator</h1>", unsafe_allow_html=True)
        st.markdown("<div class='hero-subtitle'>Intelligent ICU-Grade Ventilation, Engineered for Seamless Transport.</div>", unsafe_allow_html=True)
        st.markdown("""
        <div class='feature-box'>
            <b>Compact Turbine Performance (6.5 kg)</b><br>
            High-performance internal turbine independent of wall air supply. Full Adult, Pediatric, and Neonatal ventilation modes.
        </div>
        <div class='feature-box'>
            <b>Extended Battery Autonomy (4 to 8 Hours)</b><br>
            Dual hot-swappable Li-Ion battery architecture ensuring uninterrupted ventilation during intra-hospital and emergency transport.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div class='price-tag'>$15,500.00 USD</div>", unsafe_allow_html=True)

        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("🛒 Add to Cart", use_container_width=True, type="primary"):
                add_to_cart("Aerivo M1 Portable Ventilator (Global)", 15500, "USD", "AERV-M1-GLB")
        with col_btn2:
            render_tech_specs_button("EN", "📄 Download Datasheet (PDF)", "Portable Medical Ventilator Datasheet.pdf")

    with col_img:
        render_main_product_image()

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<h3>Core Technical Specifications</h3>", unsafe_allow_html=True)
    st.markdown("""
    <table class='clinical-table'>
        <thead><tr><th>Parameter</th><th>Specification</th></tr></thead>
        <tbody>
            <tr><td><b>Product Weight</b></td><td>6.5 kg (14.3 lbs) — Ruggedized portable chassis</td></tr>
            <tr><td><b>Air Supply</b></td><td>Integrated high-efficiency internal turbine (up to 260 L/min peak flow)</td></tr>
            <tr><td><b>Battery Runtime</b></td><td>4 hours (single battery) / 8+ hours (dual hot-swappable Li-Ion batteries)</td></tr>
            <tr><td><b>Ventilation Modes</b></td><td>ASV, (S)CMV+, SIMV+, PCV+, PSIMV+, SPONT, APRV, NIV, HiFlowO2</td></tr>
            <tr><td><b>Tidal Volume</b></td><td>Adult/Ped: 20 – 2,000 ml | Neonatal: 2 – 300 ml</td></tr>
            <tr><td><b>Power Supply Options</b></td><td>100–240 VAC, 50/60 Hz (Regional earthed cords: Type F / Type G / Type D) & 12–28 VDC</td></tr>
        </tbody>
    </table>
    """, unsafe_allow_html=True)

    render_consumables_accessories("EN")
    render_scroll_cue("Explore clinical environments below")
    render_album_gallery("EN")
    render_feedback_section("EN")

# ==============================================================================
# 2. GERMANY PAGE (DE) — Low-Context, Authority, TCO/DRG, Formal RFQ, AIDA
# ==============================================================================
def page_german():
    render_navbar("DE")
    render_personalization_module("DE")

    # --- ATTENTION (CE/MDR Authority & Precision) ---
    col_text, col_img = st.columns([1.15, 1], gap="large")
    with col_text:
        st.markdown("<div class='section-kicker'>EU MDR 2017/745 • KLASSE IIb • REF: AERV-M1-DE-01</div>", unsafe_allow_html=True)
        st.markdown("<h1>Aerivo M1: Zertifizierte Präzision für die Intensivmedizin</h1>", unsafe_allow_html=True)
        st.markdown("<div class='hero-subtitle'>Mobiles Turbinen-Beatmungssystem (6,5 kg) — Konform mit EU MDR & deutschen Klinikstandards.</div>", unsafe_allow_html=True)

        # Compliance Badges (Cialdini Authority)
        st.markdown("""
        <div style='margin-bottom: 0.8rem;'>
            <span class='cert-badge'>🇪🇺 CE 0123 (EU MDR 2017/745, Klasse IIb)</span>
            <span class='cert-badge'>📋 ISO 13485:2016</span>
            <span class='cert-badge'>🏥 ISO 80601-2-12</span>
            <span class='cert-badge'>🚑 ISO 80601-2-84</span>
            <span class='cert-badge'>🔖 UDI: (01)04065432109876</span>
        </div>
        <div class='ec-rep-bar'>
            <b>🇪🇺 EC REP (Bevollmächtigter in der EU):</b> Aerivo Europe Regulatory GmbH, Maximilianstraße 35, 80539 München, Deutschland
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class='feature-box'>
            <b>Dokumentierte Ausfallsicherheit & Unabhängigkeit</b><br>
            Integrierte Hochleistungsturbine, 6,5 kg Eigengewicht, 4–8 Std. Akkulaufzeit (Hot-Swap) und Netzanschlusskabel <b>Typ F (Schuko) mit Schutzleiter</b>.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div class='price-tag'>14.200 € <span style='font-size:0.95rem; font-weight:600;'>(zzgl. MwSt., DRG-optimiert)</span></div>", unsafe_allow_html=True)

        # Primary CTAs (Fogg & LIFT: Reduce friction for institutional buyers)
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("📝 Offizielles Angebot (RFQ) anfordern", use_container_width=True, type="primary"):
                st.session_state.show_rfq = not st.session_state.show_rfq
                st.rerun()
        with col_btn2:
            render_tech_specs_button("DE", "📄 Datenblatt & Gebrauchsanweisung (DE)", "Technisches Datenblatt Beatmungsgerät.pdf")

        if st.button("🛒 Direkt in den Beschaffungs-Warenkorb (REF: AERV-M1-DE-01)", use_container_width=True):
            add_to_cart("Aerivo M1 Beatmungssystem (DE-Konfiguration)", 14200, "EUR", "AERV-M1-DE-01")

    with col_img:
        render_main_product_image()

    # Formal RFQ Form (Action)
    if st.session_state.show_rfq:
        st.markdown("<br>", unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown("### 📝 Formelle Angebotsanfrage (RFQ) — Artikel-Nr. `REF: AERV-M1-DE-01`")
            st.write("Für Krankenhaus-Einkaufsabteilungen, TED-Ausschreibungen und Einkaufsgemeinschaften (z. B. Sana, Prospitalia, GDEKK).")
            c1, c2 = st.columns(2)
            with c1:
                st.text_input("Klinik / Einrichtung / Einkaufsgemeinschaft", placeholder="z. B. Universitätsklinikum München")
                st.text_input("Ansprechpartner (Medizintechnik / Einkauf)")
                st.selectbox("Einkaufskanal", ["Direktbeschaffung Klinik", "Einkaufsgemeinschaft (Sana / Prospitalia / GDEKK)", "EU-Ausschreibung (TED)"])
            with c2:
                st.text_input("Geschäftliche E-Mail-Adresse")
                st.number_input("Gewünschte Stückzahl (REF: AERV-M1-DE-01)", min_value=1, value=2)
                st.selectbox("Netzanschlusskabel", ["Typ F (Schuko) mit Schutzleiter — Standard DE", "12-28V DC Fahrzeugadapter + Typ F"])
            if st.button("Verbindliche Angebotsanfrage absenden", type="primary"):
                st.success("✅ Ihre RFQ-Anfrage (REF: AERV-M1-DE-01) wurde registriert. Sie erhalten innerhalb von 24 Werkstunden ein formelles Angebot inkl. Konformitätserklärung.")

    # --- INTEREST (Technical Specs + 5-10 Year TCO Table for DRG) ---
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div class='section-kicker'>Transparente Wirtschaftlichkeit (DRG-System)</div>", unsafe_allow_html=True)
    st.markdown("<h3>Technische Spezifikationen & Total Cost of Ownership (TCO)</h3>", unsafe_allow_html=True)

    tab_tco, tab_specs, tab_sla = st.tabs([
        "📊 5- & 10-Jahres-TCO-Kalkulation",
        "⚙️ Technische Daten & Elektrik (Typ F)",
        "🛡️ Prüfberichte & SLA-Garantie"
    ])

    with tab_tco:
        st.write("Im deutschen DRG-Fallpauschalensystem entscheiden die Gesamtkosten über die Lebensdauer — nicht nur der Anschaffungspreis:")
        st.markdown("""
        <table class='clinical-table'>
            <thead>
                <tr>
                    <th>Kostenposition (pro Gerät)</th>
                    <th>5-Jahres-Horizont</th>
                    <th>10-Jahres-Horizont</th>
                    <th>Leistungsumfang</th>
                </tr>
            </thead>
            <tbody>
                <tr><td><b>Grundgerät Aerivo M1 (REF: AERV-M1-DE-01)</b></td><td>14.200 €</td><td>14.200 €</td><td>Inkl. interner Turbine, Standard-Akku & Typ-F-Kabel</td></tr>
                <tr><td><b>STK / MTK & Periodische Wartung (jährlich)</b></td><td>2.250 €</td><td>4.500 €</td><td>Sicherheitstechnische Kontrolle gem. MPBetreibV</td></tr>
                <tr><td><b>Akkutausch (alle 3 Jahre empfohlen)</b></td><td>520 €</td><td>1.560 €</td><td>Original Li-Ion Hot-Swap-Batteriemodul</td></tr>
                <tr><td><b>Verbrauchsmaterialien (geschätzt/Jahr: 850 €)</b></td><td>4.250 €</td><td>8.500 €</td><td>Einwegschlauchsysteme, HEPA-Filter, Sensoren</td></tr>
                <tr><td><b>Premium SLA-Servicevertrag (48h Ersatzgerät)</b></td><td>1.800 €</td><td>3.600 €</td><td>Garantierte Reaktionszeit & Software-Updates</td></tr>
                <tr><td><b>Gesamt-TCO (Transparent kalkuliert)</b></td><td><b>23.020 €</b></td><td><b>32.360 €</b></td><td><b>Planungssichere Kosten pro Betriebsjahr</b></td></tr>
            </tbody>
        </table>
        """, unsafe_allow_html=True)

    with tab_specs:
        st.markdown("""
        <table class='clinical-table'>
            <thead><tr><th>Merkmal</th><th>Spezifikation (Aerivo M1)</th></tr></thead>
            <tbody>
                <tr><td><b>Gewicht & Bauart</b></td><td>6,5 kg | Kompaktes, stoßfestes Gehäuse (IP24 Spritzwasserschutz)</td></tr>
                <tr><td><b>Drucklufterzeugung</b></td><td>Integrierte Hochleistungsturbine (unabhängig von zentraler Gasversorgung)</td></tr>
                <tr><td><b>Akkulaufzeit</b></td><td>4 Stunden (1 Akku) bis 8+ Stunden (2 Hot-Swap Li-Ion Akkus)</td></tr>
                <tr><td><b>Elektrischer Anschluss</b></td><td>100–240 VAC, 50/60 Hz — <b>Typ F (Schuko) Netzkabel mit Schutzleiter (PE)</b>; 12–28 VDC</td></tr>
                <tr><td><b>Normen & Sicherheit</b></td><td>EU MDR 2017/745 (Kl. IIb), ISO 13485:2016, ISO 80601-2-12, ISO 80601-2-84, IEC 60601-1</td></tr>
                <tr><td><b>Datenschutz</b></td><td>DSGVO-konforme lokale Ereignisprotokollierung ohne externe Cloud-Pflicht</td></tr>
            </tbody>
        </table>
        """, unsafe_allow_html=True)

    # --- DESIRE (Test Reports & SLA) ---
    with tab_sla:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("""
            <div class='glass-card'>
                <h4>🔬 Klinische Validierung & Prüfberichte</h4>
                <ul>
                    <li><b>MTBF (Mean Time Between Failures):</b> &gt; 50.000 Betriebsstunden nachgewiesen.</li>
                    <li><b>EMV & Transportprüfung:</b> Geprüft nach IEC 60601-1-2 und EN 1789 (Rettungsdienst).</li>
                    <li><b>Benannte Stelle (Notified Body):</b> Vollständige technische Dokumentation für Audits jederzeit abrufbar.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown("""
            <div class='glass-card'>
                <h4>📜 Service Level Agreement (SLA)</h4>
                <ul>
                    <li><b>Reaktionszeit:</b> Technischer Support innerhalb von 4 Stunden (Mo–So).</li>
                    <li><b>Austauschgarantie:</b> Leihgerät innerhalb von 24–48 Stunden bundesweit.</li>
                    <li><b>Einweisung:</b> Zertifizierte Geräteeinweisung nach MPBetreibV vor Ort.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

    render_consumables_accessories("DE")
    render_scroll_cue("Klicken Sie hier für klinische Einsatzbilder")
    render_album_gallery("DE")
    render_feedback_section("DE")

# ==============================================================================
# 3. IRAQ PAGE (AR / IQ) — High-Context, WhatsApp/Fogg, Social Proof, 3 Tiers, Tenders
# ==============================================================================
def page_arabic():
    render_navbar("AR")

    # Floating WhatsApp Button (Fogg Behavior Model - Immediate Facilitation)
    st.markdown("""
        <a href="https://wa.me/9647700000000?text=Hello%20Aerivo%20Medical%20Iraq" target="_blank" class="wa-floating">
            💬 تواصل فوري عبر واتساب مع خبير المبيعات
        </a>
    """, unsafe_allow_html=True)

    render_personalization_module("AR")

    # --- ATTENTION (Local Support, Competitive Price, Ready for Transport) ---
    col_img, col_text = st.columns([1, 1.15], gap="large")
    with col_text:
        st.markdown("<div class='section-kicker' style='direction: rtl; text-align: right; display:block;'>دعم محلي في العراق • سعر تنافسي • جاهز للنقل</div>", unsafe_allow_html=True)
        st.markdown("<h1 style='direction: rtl; text-align: right;'>أيريفو M1: دعم محلي موثوق، سعر تنافسي وجاهز للنقل الفوري</h1>", unsafe_allow_html=True)
        st.markdown("<div class='hero-subtitle' style='direction: rtl; text-align: right;'>جهاز تنفس صناعي متنقل بوزن 6.5 كغم وتوربين داخلي — مصمم خصيصاً لظروف العمل في المستشفيات العراقية.</div>", unsafe_allow_html=True)

        st.markdown("<div class='info-chip' style='direction: rtl; text-align: right;'>✔️ جاهز للتسجيل لدى وزارة الصحة العراقية (MOH) ومطابق لمتطلبات مناقصات كيماديا (KIMADIA).</div>", unsafe_allow_html=True)

        # Top Primary CTAs (WhatsApp + Demo/Consultation)
        c_wa, c_demo = st.columns(2)
        with c_wa:
            st.markdown("""
                <a href="https://wa.me/9647700000000?text=Hello%20Aerivo%20Medical%20Iraq" target="_blank" class="wa-btn-inline">
                    💬 محادثة واتساب مع خبير المبيعات
                </a>
            """, unsafe_allow_html=True)
        with c_demo:
            if st.button("📅 طلب عرض عملي (Demo) واستشارة", use_container_width=True, type="primary"):
                st.session_state.show_demo = not st.session_state.show_demo
                st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div class='rtl-feature-box'>
            <b>بطارية احتياطية قوية (حتى 8 ساعات) لمواجهة انقطاع الكهرباء</b><br>
            تعمل بنظام البطاريات المزدوجة القابلة للتبديل السريع مع <b>كابل طاقة مؤرض (Type G / Type D)</b> لحماية الجهاز من تذبذب التيار.
        </div>
        <div class='rtl-feature-box'>
            <b>تركيب مجاني، قطع غيار فورية، وتدريب حضوري باللغة العربية</b><br>
            فريقنا الهندسي ومكتبنا العلمي المعتمد متواجدون في بغداد وأربيل لخدمة كوادركم الطبية على مدار الساعة.
        </div>
        """, unsafe_allow_html=True)

    with col_img:
        render_main_product_image()

    # Demo & Consultation Form (Action)
    if st.session_state.show_demo:
        with st.container(border=True):
            st.markdown("<div style='direction: rtl; text-align: right;'><h3>📅 حجز موعد عرض عملي (Demo) واستشارة مجانية</h3><p>سيقوم مدير المبيعات الإقليمي بالتواصل معكم خلال أقل من ساعتين.</p></div>", unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c2:
                st.text_input("الاسم والمنصب (مثلاً: مدير المستشفى / رئيس قسم العناية)", key="iq_name")
                st.text_input("اسم المستشفى أو المركز الطبي والمحافظة", key="iq_hosp")
            with c1:
                st.text_input("رقم الهاتف / واتساب", key="iq_phone")
                st.selectbox("نوع الكابل الكهربائي المطلوب", ["Type G (المعيار البريطاني المؤرض — الأكثر شيوعاً في العراق)", "Type D (المؤرض)"], key="iq_plug")
            if st.button("تأكيد طلب الاستشارة والعرض العملي", type="primary"):
                st.success("✅ تم استلام طلبكم بنجاح! سيتواصل معكم خبيرنا في بغداد/أربيل قريباً.")

    # --- INTEREST (Clinical Video + 3 Competitive Pricing Tiers) ---
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div style='direction: rtl; text-align: right;'>", unsafe_allow_html=True)
    st.markdown("<div class='section-kicker'>أسعار تنافسية تناسب ميزانيتكم</div>", unsafe_allow_html=True)
    st.markdown("<h3 style='direction: rtl; text-align: right;'>اختر الفئة المناسبة لاحتياج مستشفاك (3 باقات متكاملة)</h3>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    t_eco, t_mid, t_pro = st.columns(3)
    with t_pro:
        st.markdown("""
        <div class='glass-card glass-card-rtl'>
            <span class='cert-badge'>⭐ الأكثر طلباً للعناية المركزة</span>
            <h4>الفئة المتقدمة (ICU Full Spec)</h4>
            <p>مجهزة بالكامل لأقسام العناية المركزة، تشمل جميع أنماط التنفس الذكي (ASV)، مرطب نشط، وبطاريتين (8 ساعات).</p>
            <div class='price-tag' style='font-size:1.75rem; margin:0.6rem 0;'>$15,500 USD</div>
            <div style='font-size:0.82rem; color:var(--ocean);'>REF: AERV-M1-IQ-PRO | كابل Type G/D</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🛒 إضافة الفئة المتقدمة للسلة", key="iq_pro", use_container_width=True, type="primary"):
            add_to_cart("Aerivo M1 - Advanced ICU Tier (IQ)", 15500, "USD", "AERV-M1-IQ-PRO")

    with t_mid:
        st.markdown("""
        <div class='glass-card glass-card-rtl'>
            <span class='cert-badge'>🚑 مثالية للطوارئ والإسعاف</span>
            <h4>الفئة المتوسطة (Emergency & Transport)</h4>
            <p>تشمل حقيبة النقل المقاومة للصدمات، قاعدة التثبيت لسيارات الإسعاف، وبطارية احتياطية ممتدة.</p>
            <div class='price-tag' style='font-size:1.75rem; margin:0.6rem 0;'>$13,800 USD</div>
            <div style='font-size:0.82rem; color:var(--ocean);'>REF: AERV-M1-IQ-MID | كابل Type G/D</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🛒 إضافة الفئة المتوسطة للسلة", key="iq_mid", use_container_width=True):
            add_to_cart("Aerivo M1 - Emergency Mid-Range Tier (IQ)", 13800, "USD", "AERV-M1-IQ-MID")

    with t_eco:
        st.markdown("""
        <div class='glass-card glass-card-rtl'>
            <span class='cert-badge'>🏥 للمستشفيات الخاصة والعيادات</span>
            <h4>الفئة الاقتصادية (Private Hospitals)</h4>
            <p>سعر تنافسي ممتاز مع نفس الكفاءة العالية (وزن 6.5 كغم وتوربين داخلي)، مثالية للمستشفيات الخاصة.</p>
            <div class='price-tag' style='font-size:1.75rem; margin:0.6rem 0;'>$11,900 USD</div>
            <div style='font-size:0.82rem; color:var(--ocean);'>REF: AERV-M1-IQ-ECO | كابل Type G/D</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🛒 إضافة الفئة الاقتصادية للسلة", key="iq_eco", use_container_width=True):
            add_to_cart("Aerivo M1 - Economic Private Tier (IQ)", 11900, "USD", "AERV-M1-IQ-ECO")

    # Clinical Video & Power/Battery Reliability Showcase
    st.markdown("<br>", unsafe_allow_html=True)
    v_col1, v_col2 = st.columns([1.2, 1], gap="large")
    with v_col1:
        st.markdown("""
        <div class='glass-card glass-card-rtl'>
            <h4>🎥 فيديو توضيحي: أداء أيريفو M1 في القسم السريري</h4>
            <p>شاهد سهولة تشغيل الجهاز بواجهة واضحة وسريعة أثناء نقل المرضى وحالات الطوارئ الحرجة.</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class='glass-card' style='text-align:center; padding: 2.2rem 1.5rem; background: linear-gradient(135deg, rgba(11,42,74,0.88), rgba(27,111,181,0.82)); color:#fff;'>
            <div style='font-size:2.8rem; margin-bottom:0.5rem;'>▶️</div>
            <div style='font-size:1.15rem; font-weight:800; color:#fff;'>العرض السريري المباشر لجهاز Aerivo M1</div>
            <div style='font-size:0.9rem; color:rgba(255,255,255,0.85); margin-top:6px; direction:rtl;'>
                استعراض عملي: التشغيل خلال 30 ثانية • اختبار البطارية 8 ساعات • النقل داخل سيارة الإسعاف (باللغة العربية)
            </div>
        </div>
        """, unsafe_allow_html=True)

    with v_col2:
        st.markdown("""
        <div class='glass-card glass-card-rtl'>
            <h4>⚡ المواصفات الكهربائية والميدانية للعراق</h4>
            <table class='clinical-table clinical-table-rtl'>
                <tbody>
                    <tr><td><b>الوزن والتوربين</b></td><td>6.5 كغم مع توربين داخلي مستقل</td></tr>
                    <tr><td><b>زمن عمل البطارية</b></td><td>4 إلى 8+ ساعات (بطاريتان قابلتان للتبديل أثناء العمل)</td></tr>
                    <tr><td><b>قابس الكهرباء</b></td><td>كابل مؤرض قياسي <b>Type G / Type D</b> (220-240V)</td></tr>
                    <tr><td><b>التدريب والدعم</b></td><td>تدريب حضوري شامل للكوادر الطبية باللغة العربية</td></tr>
                </tbody>
            </table>
        </div>
        """, unsafe_allow_html=True)

    # --- DESIRE (Social Proof: Management Team, Regional Exhibitions, Local Scientific Office) ---
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div style='direction: rtl; text-align: right;'><div class='section-kicker'>الثقة والشراكة طويلة الأمد</div><h3 style='direction:rtl; text-align:right;'>فريقنا، حضورنا الإقليمي، والمكتب العلمي المعتمد في العراق</h3></div>", unsafe_allow_html=True)

    d1, d2, d3 = st.columns(3)
    with d3:
        st.markdown("""
        <div class='glass-card glass-card-rtl'>
            <h4>🏢 المكتب العلمي والشريك المحلي</h4>
            <p><b>مكتب الرافدين العلمي للمستلزمات الطبية</b> (وكيل معتمد بوكالة رسمية).</p>
            <p>📍 الفروع: بغداد (الكرادة) وأربيل.<br>🛠️ مركز صيانة محلي ومخزون فوري لقطع الغيار والمستهلكات.</p>
        </div>
        """, unsafe_allow_html=True)
    with d2:
        st.markdown("""
        <div class='glass-card glass-card-rtl'>
            <h4>🌐 الحضور في المعارض الإقليمية</h4>
            <p>مشاركة فاعلة ومستمرة في معرض <b>Iraq Health (بغداد)</b> ومعرض <b>Erbil MedExpo</b> ومعرض الصحة العربي (Arab Health).</p>
            <p><i>"شهادات تقدير من مدراء أقسام العناية المركزة في بغداد والبصرة."</i></p>
        </div>
        """, unsafe_allow_html=True)
    with d1:
        st.markdown("""
        <div class='glass-card glass-card-rtl'>
            <h4>👨‍⚕️ فريق الإدارة والهندسة الطبية</h4>
            <p>يقود الفريق الإقليمي مهندسون طبيون معتمدون بخبرة تزيد عن 12 عاماً في تجهيز المستشفيات الحكومية والخاصة وتدريب الكوادر باللغة العربية.</p>
        </div>
        """, unsafe_allow_html=True)

    # --- DEDICATED TENDER & REGISTRATION DOCUMENTS SECTION (Not Hidden!) ---
    st.markdown("<hr>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("""
        <div style='direction: rtl; text-align: right;'>
            <div class='section-kicker'>الوثائق الرسمية للمناقصات الحكومية والخاصة</div>
            <h3 style='direction: rtl; text-align: right;'>📑 قسم وثائق التسجيل والمناقصات (MOH & KIMADIA)</h3>
            <p style='direction: rtl; text-align: right;'>نضع كافة الوثائق القانونية والجودة بين أيديكم بشفافية تامة لتسهيل إجراءات التسجيل والدخول في مناقصات وزارة الصحة العراقية والشركة العامة لتسويق الأدوية والمستلزمات الطبية (كيماديا) وإقليم كردستان:</p>
            <ul style='direction: rtl; text-align: right;'>
                <li><b>شهادة البيع الحر (CFS - Certificate of Free Sale)</b> مصدقة أصولياً.</li>
                <li><b>شهادات الجودة العالمية:</b> ISO 13485:2016 و ISO 9001 وعلامة CE الأوروبية.</li>
                <li><b>ملف التسجيل الجاهز:</b> ملف تقني كامل للتسجيل في هيئة التسجيل بوزارة الصحة العراقية (MOH) وإجازات الاستيراد.</li>
                <li><b>خطاب التفويض والوكالة الرسمية</b> للمكتب العلمي المحلي لضمان ما بعد البيع والضمان لمدة سنتين.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        c_pdf, c_wa2 = st.columns(2)
        with c_pdf:
            render_tech_specs_button("AR", "📄 تحميل ملف المواصفات الفنية للمناقصات (PDF)", "البطاقة الفنية لجهاز التنفس الاصطناعي المحمول.pdf")
        with c_wa2:
            st.markdown("""
                <a href="https://wa.me/9647700000000?text=Requesting%20KIMADIA%20Tender%20Documents" target="_blank" class="wa-btn-inline">
                    📲 طلب حزمة وثائق المناقصة عبر واتساب
                </a>
            """, unsafe_allow_html=True)

    render_consumables_accessories("AR")
    render_scroll_cue("انقر هنا لاستكشاف البيئات السريرية وتفاصيل الجهاز")
    render_album_gallery("AR")
    render_feedback_section("AR")

# ==============================================================================
# ROUTER & GATEWAY PAGE
# ==============================================================================
if st.session_state.language is None:
    bg_uri = get_image_data_uri("Aerivo (7).png", 1920)

    st.markdown(f"""
        <style>
        .stApp {{
            background:
                linear-gradient(160deg, rgba(11,42,74,0.55) 0%, rgba(20,168,155,0.25) 100%),
                url("{bg_uri}") !important;
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
        .stButton > button {{ padding: 1.1rem 1rem; font-size: 1.05rem; border-radius: 18px; background: rgba(255,255,255,0.82); }}
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class='gate-container'>
            <h1>⚕️ AERIVO MEDICAL</h1>
            <div class='gate-tag'>GLOBAL LIFE SUPPORT SOLUTIONS</div>
            <p class='gate-text'>
                Welcome to the unified Aerivo platform. Please select your region to access localized clinical documentation, regulatory certifications, and dedicated procurement channels.
            </p>
        </div>
        <div class='gate-label'>Select your region & language</div>
    """, unsafe_allow_html=True)

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
    if st.session_state.language == 'EN':
        page_english_global()
    elif st.session_state.language == 'DE':
        page_german()
    elif st.session_state.language == 'AR':
        page_arabic()
