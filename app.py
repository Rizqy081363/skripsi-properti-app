import streamlit as st
import pandas as pd
import numpy as np
import joblib

# ============================================================
# 1. KONFIGURASI HALAMAN
# ============================================================
st.set_page_config(
    page_title="PropVault AI | King County",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# 2. CUSTOM CSS — CINEMATIC DARK LUXURY
# ============================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Inter:wght@300;400;500;600&display=swap');

    /* ── RESET & BASE ── */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #070E1A;
    }
    .stApp {
        background: radial-gradient(ellipse at 20% 10%, #0F2040 0%, #070E1A 55%, #0A0D14 100%);
        min-height: 100vh;
    }

    /* ── HERO SECTION ── */
    .hero-wrap {
        position: relative;
        padding: 3.5rem 0 2rem;
        overflow: hidden;
    }
    .hero-wrap::before {
        content: '';
        position: absolute;
        top: -60px; left: -100px;
        width: 500px; height: 500px;
        background: radial-gradient(circle, rgba(201,168,76,0.10) 0%, transparent 70%);
        pointer-events: none;
    }
    .hero-eyebrow {
        font-family: 'Inter', sans-serif;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 3.5px;
        text-transform: uppercase;
        color: #C9A84C;
        margin-bottom: 0.6rem;
    }
    .hero-title {
        font-family: 'Playfair Display', serif;
        font-size: clamp(2.4rem, 5vw, 3.8rem);
        font-weight: 900;
        color: #F0EDE8;
        line-height: 1.08;
        margin: 0 0 0.8rem;
        letter-spacing: -0.5px;
    }
    .hero-title span {
        color: #C9A84C;
    }
    .hero-subtitle {
        font-size: 0.97rem;
        font-weight: 300;
        color: #7A8FA6;
        max-width: 540px;
        line-height: 1.65;
        margin-bottom: 1.6rem;
    }

    /* ── PILL BADGES ── */
    .badge-row { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 0.5rem; }
    .badge {
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(201,168,76,0.25);
        color: #C9A84C;
        border-radius: 99px;
        padding: 0.3rem 0.85rem;
        font-size: 0.73rem;
        font-weight: 500;
        letter-spacing: 0.3px;
        backdrop-filter: blur(4px);
    }

    /* ── DIVIDER ── */
    .gold-divider {
        height: 1px;
        background: linear-gradient(90deg, #C9A84C33, #C9A84C88, #C9A84C33);
        border: none;
        margin: 1.8rem 0;
    }

    /* ── SECTION LABEL ── */
    .section-label {
        font-family: 'Inter', sans-serif;
        font-size: 0.68rem;
        font-weight: 600;
        letter-spacing: 3px;
        text-transform: uppercase;
        color: #C9A84C;
        margin-bottom: 1.1rem;
        display: flex;
        align-items: center;
        gap: 0.6rem;
    }
    .section-label::after {
        content: '';
        flex: 1;
        height: 1px;
        background: rgba(201,168,76,0.2);
        max-width: 120px;
    }

    /* ── INPUT OVERRIDES ── */
    div[data-testid="stNumberInput"] input,
    div[data-testid="stSelectbox"] div[data-baseweb="select"] {
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid rgba(255,255,255,0.10) !important;
        border-radius: 10px !important;
        color: #F0EDE8 !important;
        font-family: 'Inter', sans-serif !important;
    }
    div[data-testid="stNumberInput"] input:focus,
    div[data-testid="stSelectbox"] div[data-baseweb="select"]:focus-within {
        border-color: rgba(201,168,76,0.5) !important;
        box-shadow: 0 0 0 2px rgba(201,168,76,0.12) !important;
    }
    label[data-testid="stWidgetLabel"] p,
    .stSlider label {
        color: #9EB3C8 !important;
        font-size: 0.80rem !important;
        font-weight: 500 !important;
        letter-spacing: 0.2px;
    }
    /* Slider thumb gold */
    div[data-testid="stSlider"] [role="slider"] {
        background: #C9A84C !important;
        border-color: #C9A84C !important;
    }
    div[data-testid="stSlider"] [data-testid="stSliderThumb"] {
        background: #C9A84C !important;
    }
    .stSlider > div > div > div > div {
        background: #C9A84C !important;
    }

    /* ── METRIC CARDS (top 3) ── */
    .stat-card {
        background: linear-gradient(145deg, rgba(30,58,95,0.6) 0%, rgba(15,32,64,0.8) 100%);
        border: 1px solid rgba(201,168,76,0.18);
        border-radius: 16px;
        padding: 1.4rem 1.6rem;
        text-align: center;
        backdrop-filter: blur(8px);
        transition: border-color 0.3s;
    }
    .stat-card:hover { border-color: rgba(201,168,76,0.45); }
    .stat-card .s-label {
        font-size: 0.68rem;
        font-weight: 600;
        letter-spacing: 2.5px;
        text-transform: uppercase;
        color: #6B88A0;
        margin-bottom: 0.4rem;
    }
    .stat-card .s-value {
        font-family: 'Playfair Display', serif;
        font-size: 2rem;
        font-weight: 700;
        color: #F0EDE8;
        line-height: 1;
    }
    .stat-card .s-unit {
        font-size: 0.75rem;
        color: #C9A84C;
        margin-top: 0.25rem;
        font-weight: 500;
    }

    /* ── RESULT BOX ── */
    .result-box {
        position: relative;
        background: linear-gradient(135deg, rgba(201,168,76,0.08) 0%, rgba(15,32,64,0.95) 60%);
        border: 1px solid rgba(201,168,76,0.45);
        border-radius: 20px;
        padding: 2.8rem 2.4rem 2.4rem;
        text-align: center;
        overflow: hidden;
        animation: fadeSlideUp 0.7s cubic-bezier(0.22, 1, 0.36, 1) both;
    }
    .result-box::before {
        content: '';
        position: absolute;
        top: -80px; left: 50%;
        transform: translateX(-50%);
        width: 300px; height: 300px;
        background: radial-gradient(circle, rgba(201,168,76,0.15) 0%, transparent 70%);
        pointer-events: none;
    }
    .result-eyebrow {
        font-size: 0.70rem;
        font-weight: 600;
        letter-spacing: 3px;
        text-transform: uppercase;
        color: #C9A84C;
        margin-bottom: 0.5rem;
    }
    .result-price {
        font-family: 'Playfair Display', serif;
        font-size: clamp(2.8rem, 6vw, 4.5rem);
        font-weight: 900;
        color: #F0EDE8;
        letter-spacing: -1px;
        line-height: 1;
        margin: 0.3rem 0 0.6rem;
    }
    .result-price .currency {
        font-size: 0.45em;
        color: #C9A84C;
        vertical-align: super;
        font-weight: 700;
    }
    .result-sub {
        font-size: 0.83rem;
        color: #5E7A94;
        font-weight: 400;
        letter-spacing: 0.2px;
    }
    .result-r2 {
        display: inline-block;
        background: rgba(201,168,76,0.12);
        border: 1px solid rgba(201,168,76,0.3);
        border-radius: 99px;
        padding: 0.3rem 1rem;
        font-size: 0.78rem;
        color: #C9A84C;
        font-weight: 600;
        margin-top: 1rem;
        letter-spacing: 0.3px;
    }

    @keyframes fadeSlideUp {
        from { opacity: 0; transform: translateY(30px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    /* ── PREDICT BUTTON ── */
    div[data-testid="stButton"] button[kind="primary"] {
        background: linear-gradient(135deg, #C9A84C 0%, #A8832A 100%) !important;
        color: #0A0D14 !important;
        font-weight: 700 !important;
        font-size: 0.92rem !important;
        letter-spacing: 1.2px !important;
        text-transform: uppercase !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 2rem !important;
        box-shadow: 0 4px 24px rgba(201,168,76,0.30) !important;
        transition: all 0.25s !important;
    }
    div[data-testid="stButton"] button[kind="primary"]:hover {
        box-shadow: 0 6px 32px rgba(201,168,76,0.50) !important;
        transform: translateY(-1px) !important;
    }

    /* ── SIDEBAR ── */
    [data-testid="stSidebar"] {
        background: rgba(7,14,26,0.97) !important;
        border-right: 1px solid rgba(255,255,255,0.05) !important;
    }
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] li,
    [data-testid="stSidebar"] span {
        color: #7A8FA6 !important;
        font-size: 0.85rem !important;
    }
    [data-testid="stSidebar"] h3 {
        color: #F0EDE8 !important;
        font-family: 'Playfair Display', serif !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
    }
    [data-testid="stSidebar"] [data-testid="stMetricValue"] {
        color: #C9A84C !important;
        font-family: 'Playfair Display', serif !important;
        font-size: 1.6rem !important;
    }
    [data-testid="stSidebar"] [data-testid="stMetricLabel"] {
        color: #5E7A94 !important;
        font-size: 0.72rem !important;
        letter-spacing: 1px;
        text-transform: uppercase;
    }
    [data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.07) !important; }

    /* ── EXPANDER ── */
    [data-testid="stExpander"] {
        background: rgba(255,255,255,0.03) !important;
        border: 1px solid rgba(255,255,255,0.07) !important;
        border-radius: 12px !important;
    }
    [data-testid="stExpander"] summary {
        color: #7A8FA6 !important;
        font-size: 0.83rem !important;
    }

    /* ── DATAFRAME ── */
    [data-testid="stDataFrame"] {
        border: 1px solid rgba(255,255,255,0.06) !important;
        border-radius: 10px !important;
        overflow: hidden;
    }

    /* ── FOOTER ── */
    .footer-bar {
        text-align: center;
        padding: 1.5rem 0;
        border-top: 1px solid rgba(255,255,255,0.05);
        margin-top: 3rem;
    }
    .footer-bar p {
        font-size: 0.75rem;
        color: #3A4E62;
        letter-spacing: 0.3px;
    }
    .footer-bar .footer-brand {
        font-family: 'Playfair Display', serif;
        font-size: 1rem;
        color: #C9A84C;
        font-weight: 700;
    }

    /* ── MISC ── */
    footer { visibility: hidden; }
    #MainMenu { visibility: hidden; }
    .stMarkdown p { color: #9EB3C8; }
    .stSpinner > div { border-top-color: #C9A84C !important; }

    /* Caption */
    .stCaption { color: #3A4E62 !important; font-size: 0.75rem !important; }
    .stAlert {
        background: rgba(201,168,76,0.08) !important;
        border: 1px solid rgba(201,168,76,0.3) !important;
        border-radius: 12px !important;
        color: #C9A84C !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# 3. MEMUAT MODEL & ASET
# ============================================================
MODEL_R2   = 0.9457
MODEL_NAME = "Multiple Linear Regression + Spatial & Log-Price Feature Engineering"

@st.cache_resource
def load_assets():
    model    = joblib.load("model_harga_properti.pkl")
    features = joblib.load("daftar_fitur.pkl")
    return model, features

assets_ready = True
try:
    model, features_final = load_assets()
    all_zipcodes = sorted([
        col.replace("ZipCode_", "") for col in features_final if col.startswith("ZipCode_")
    ])
except Exception as e:
    assets_ready = False
    load_error   = e

# ============================================================
# 4. HERO HEADER
# ============================================================
st.markdown("""
<div class="hero-wrap">
    <p class="hero-eyebrow">◆ &nbsp;PropVault Intelligence Platform</p>
    <h1 class="hero-title">Valuation,<br>reimagined by <span>AI</span>.</h1>
    <p class="hero-subtitle">
        Estimasi harga jual properti di King County menggunakan model regresi spasial
        — mempertimbangkan jarak ke taman, sekolah, dan rumah sakit secara real-time.
    </p>
    <div class="badge-row">
        <span class="badge">◈ &nbsp;Linear Regression</span>
        <span class="badge">⌖ &nbsp;Spatial Features</span>
        <span class="badge">◉ &nbsp;R² = 94.57 %</span>
        <span class="badge">📍 &nbsp;King County, WA</span>
    </div>
</div>
""", unsafe_allow_html=True)

if not assets_ready:
    st.error(
        f"⚠️ Gagal memuat sistem: {load_error}\n\n"
        "Pastikan **model_harga_properti.pkl** dan **daftar_fitur.pkl** berada "
        "di direktori yang sama dengan app.py."
    )
    st.stop()

# ============================================================
# 5. SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("### PropVault AI")
    st.write(
        "Model dilatih dari dataset penjualan rumah **King County, Washington (2014–2015)**, "
        "diperkaya data titik fasilitas publik (taman, sekolah, RS) menggunakan algoritma "
        "**KD-Tree** untuk kalkulasi jarak terdekat."
    )
    st.markdown("---")
    st.markdown("**Performa Model**")
    st.metric("R-Squared", f"{MODEL_R2:.2%}")
    st.caption("Diukur pada 20% data uji setelah log-transform harga dan one-hot ZipCode.")
    st.markdown("---")
    st.markdown("**Pipeline Pemodelan**")
    steps = [
        "Integrasi data spasial fasilitas",
        "Kalkulasi jarak via KD-Tree",
        "Log-transform harga target",
        "One-hot encoding ZipCode",
        "Feature engineering Space×Grade",
        "Linear Regression final",
    ]
    for i, s in enumerate(steps, 1):
        st.markdown(f"<span style='color:#C9A84C;font-weight:600'>{i:02d}</span> "
                    f"<span style='color:#5E7A94'>&nbsp;{s}</span>",
                    unsafe_allow_html=True)
    st.markdown("---")
    st.caption("Dibuat sebagai proyek penelitian valuasi properti berbasis machine learning.")

# ============================================================
# 6. FORM INPUT
# ============================================================
st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)
st.markdown('<p class="section-label">🏗 &nbsp;Atribut Fisik Bangunan</p>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3, gap="medium")
with col1:
    sqft      = st.number_input("Luas Ruang Tamu (SqFt)",        min_value=300,  max_value=10000, value=1800, step=50)
    bedrooms  = st.slider("Kamar Tidur",                          min_value=1,    max_value=10,    value=3)
with col2:
    bathrooms = st.slider("Kamar Mandi",                          min_value=1.0,  max_value=8.0,   value=2.0, step=0.25)
    grade     = st.slider("Kualitas Konstruksi (BldgGrade 1–13)", min_value=1,    max_value=13,    value=7)
with col3:
    age       = st.number_input("Umur Bangunan (Tahun)",          min_value=0,    max_value=120,   value=15)
    st.caption("Grade 1 = rendah/sederhana · Grade 13 = ultra premium")

st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)
st.markdown('<p class="section-label">📍 &nbsp;Lokasi & Jarak ke Fasilitas Publik</p>', unsafe_allow_html=True)

col4, col5, col6 = st.columns(3, gap="medium")
with col4:
    park     = st.number_input("Jarak ke Taman (km)",     min_value=0.0, max_value=50.0, value=0.5, step=0.1)
with col5:
    school   = st.number_input("Jarak ke Sekolah (km)",   min_value=0.0, max_value=50.0, value=0.3, step=0.1)
with col6:
    hospital = st.number_input("Jarak ke RS (km)",         min_value=0.0, max_value=50.0, value=1.2, step=0.1)

selected_zip = st.selectbox("Kode Pos (ZipCode)", all_zipcodes,
                             help="Lokasi properti dalam wilayah King County")

st.markdown("<br>", unsafe_allow_html=True)
predict_clicked = st.button(
    "⬡  Hitung Estimasi Harga",
    type="primary",
    use_container_width=True,
)

# ============================================================
# 7. PREDIKSI
# ============================================================
if predict_clicked:
    with st.spinner("Menghitung valuasi properti …"):
        input_data = pd.DataFrame(0, index=[0], columns=features_final)

        mapping = {
            "SqFtTotLiving":   sqft,
            "Bedrooms":        bedrooms,
            "Bathrooms":       bathrooms,
            "BldgGrade":       grade,
            "HouseAge":        age,
            "dist_to_park":    park,
            "dist_to_school":  school,
            "dist_to_hospital":hospital,
            "Space_Quality":   sqft * grade,
        }
        for col, val in mapping.items():
            if col in input_data.columns:
                input_data[col] = val

        defaults = {
            "SqFtLot": 5000, "NbrLivingUnits": 1,
            "LandVal": 150000, "ImpsVal": 200000,
            "zhvi_px": 400000, "AdjSalePrice": 500000,
            "lat": 47.5, "lon": -122.2, "ZIPCODE": int(selected_zip),
        }
        for col, val in defaults.items():
            if col in input_data.columns:
                input_data[col] = val

        target_dummy = f"ZipCode_{selected_zip}"
        if target_dummy in input_data.columns:
            input_data[target_dummy] = 1

        try:
            harga_final = np.exp(model.predict(input_data)[0])

            # ── Stat cards ──
            st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)
            st.markdown('<p class="section-label">◈ &nbsp;Ringkasan Input</p>', unsafe_allow_html=True)

            ca, cb, cc, cd = st.columns(4, gap="medium")
            cards = [
                (ca, f"{sqft:,}",       "SqFt",        "Luas Bangunan"),
                (cb, selected_zip,       "",            "ZipCode"),
                (cc, f"{grade}",         "/ 13",        "BldgGrade"),
                (cd, f"{age}",           "Tahun",       "Umur Bangunan"),
            ]
            for col, val, unit, label in cards:
                with col:
                    st.markdown(
                        f"""<div class="stat-card">
                            <div class="s-label">{label}</div>
                            <div class="s-value">{val}</div>
                            <div class="s-unit">{unit}</div>
                        </div>""",
                        unsafe_allow_html=True,
                    )

            # ── Result box ──
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(
                f"""<div class="result-box">
                    <p class="result-eyebrow">◉ &nbsp;Estimasi Valuasi Properti</p>
                    <p class="result-price">
                        <span class="currency">$</span>{harga_final:,.0f}
                    </p>
                    <p class="result-sub">
                        Kalkulasi berbasis regresi spasial · King County, Washington
                    </p>
                    <span class="result-r2">R² = {MODEL_R2:.2%} &nbsp;·&nbsp; Model akurasi tinggi</span>
                </div>""",
                unsafe_allow_html=True,
            )

            st.markdown("<br>", unsafe_allow_html=True)
            with st.expander("🔍 Inspeksi Fitur Model"):
                cols_to_show = [c for c in [
                    "SqFtTotLiving", "Bedrooms", "Bathrooms", "BldgGrade", "HouseAge",
                    "dist_to_park", "dist_to_school", "dist_to_hospital",
                    "Space_Quality", "ZIPCODE", target_dummy,
                ] if c in input_data.columns]
                st.dataframe(
                    input_data[cols_to_show].T.rename(columns={0: "Nilai"}),
                    use_container_width=True,
                )

            st.caption(
                "⚠ Estimasi bersifat indikatif berdasarkan data historis (2014–2015) "
                "dan tidak menggantikan penilaian appraisal profesional."
            )

        except Exception as pred_err:
            st.error(f"Kesalahan prediksi: {pred_err}")

# ============================================================
# 8. FOOTER
# ============================================================
st.markdown("""
<div class="footer-bar">
    <p class="footer-brand">PropVault AI</p>
    <p>Spatial Valuation Engine · King County Dataset · Multiple Linear Regression</p>
</div>
""", unsafe_allow_html=True)
