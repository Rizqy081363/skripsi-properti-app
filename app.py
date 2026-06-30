import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go

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
    /* Harga: flex layout supaya simbol $ dan angka tidak dempet */
    .result-price {
        font-family: 'Playfair Display', serif;
        font-size: clamp(2.6rem, 5.4vw, 4.2rem);
        font-weight: 900;
        color: #F0EDE8;
        letter-spacing: 0px;
        line-height: 1;
        margin: 0.5rem 0 0.7rem;
        display: flex;
        align-items: baseline;
        justify-content: center;
        gap: 0.35rem;
        flex-wrap: wrap;
        word-break: keep-all;
    }
    .result-price .currency {
        font-size: 0.42em;
        color: #C9A84C;
        font-weight: 700;
    }
    .result-price .amount {
        white-space: nowrap;
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

    /* ── DRIVER PANEL ── */
    .driver-panel {
        background: linear-gradient(145deg, rgba(20,30,48,0.75) 0%, rgba(10,16,28,0.9) 100%);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 18px;
        padding: 1.4rem 1.6rem 0.6rem;
    }
    .driver-panel-up { border-color: rgba(46,196,141,0.25); }
    .driver-panel-down { border-color: rgba(224,90,90,0.25); }
    .driver-title {
        font-family: 'Inter', sans-serif;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 0.2rem;
    }
    .driver-title-up { color: #2EC48D; }
    .driver-title-down { color: #E05A5A; }
    .driver-sub {
        font-size: 0.75rem;
        color: #5E7A94;
        margin-bottom: 0.6rem;
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

# Mapping nama fitur teknis -> label yang enak dibaca di grafik
FEATURE_LABELS = {
    "SqFtTotLiving":    "Luas Ruang Tamu (SqFt)",
    "Bedrooms":         "Jumlah Kamar Tidur",
    "Bathrooms":        "Jumlah Kamar Mandi",
    "BldgGrade":        "Kualitas Konstruksi (Grade)",
    "HouseAge":         "Umur Bangunan",
    "dist_to_park":     "Jarak ke Taman",
    "dist_to_school":   "Jarak ke Sekolah",
    "dist_to_hospital": "Jarak ke Rumah Sakit",
    "Space_Quality":    "Interaksi Luas × Grade",
    "SqFtLot":          "Luas Lahan",
    "NbrLivingUnits":   "Jumlah Unit Hunian",
    "LandVal":          "Nilai Tanah",
    "ImpsVal":          "Nilai Bangunan",
    "zhvi_px":          "Indeks Harga Zona (ZHVI)",
    "AdjSalePrice":     "Harga Jual Acuan",
    "lat":              "Latitude",
    "lon":              "Longitude",
    "ZIPCODE":          "Kode Pos",
}

def pretty_feature_name(col: str) -> str:
    if col in FEATURE_LABELS:
        return FEATURE_LABELS[col]
    if col.startswith("ZipCode_"):
        return f"Wilayah ZipCode {col.replace('ZipCode_', '')}"
    return col.replace("_", " ").title()

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
            log_pred    = model.predict(input_data)[0]
            harga_final = np.exp(log_pred)

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

            # ── Result box (harga jelas, tidak dempet) ──
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(
                f"""<div class="result-box">
                    <p class="result-eyebrow">◉ &nbsp;Estimasi Valuasi Properti</p>
                    <p class="result-price">
                        <span class="currency">$</span><span class="amount">{harga_final:,.0f}</span>
                    </p>
                    <p class="result-sub">
                        Kalkulasi berbasis regresi spasial · King County, Washington
                    </p>
                    <span class="result-r2">R² = {MODEL_R2:.2%} &nbsp;·&nbsp; Model akurasi tinggi</span>
                </div>""",
                unsafe_allow_html=True,
            )

            # ============================================================
            # 7b. GRAFIK PENDORONG HARGA (Top 10 Naik vs Top 10 Turun)
            # ============================================================
            if hasattr(model, "coef_"):
                coefs = np.asarray(model.coef_).ravel()
                x_vals = input_data.iloc[0].values.astype(float)

                # Kontribusi setiap fitur terhadap log(harga): coef * nilai input
                contrib = coefs * x_vals
                contrib_df = pd.DataFrame({
                    "feature": features_final,
                    "contribution": contrib,
                }).query("feature != @target_dummy or feature == @target_dummy")  # keep all
                # Buang fitur ZipCode_ lain yang nilainya 0 (tidak relevan utk properti ini)
                contrib_df = contrib_df[
                    (~contrib_df["feature"].str.startswith("ZipCode_")) |
                    (contrib_df["feature"] == target_dummy)
                ]
                contrib_df = contrib_df[contrib_df["contribution"] != 0]
                contrib_df["label"] = contrib_df["feature"].apply(pretty_feature_name)
                contrib_df["pct_impact"] = (np.exp(contrib_df["contribution"]) - 1) * 100

                top_up   = contrib_df.sort_values("contribution", ascending=False).head(10)
                top_down = contrib_df.sort_values("contribution", ascending=True).head(10)

                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)
                st.markdown('<p class="section-label">⚡ &nbsp;Faktor Pendorong Harga</p>', unsafe_allow_html=True)
                st.caption(
                    "Estimasi dampak tiap fitur terhadap harga akhir, dihitung dari kontribusinya "
                    "pada model (koefisien × nilai input pada skala log-harga)."
                )

                gcol1, gcol2 = st.columns(2, gap="large")

                with gcol1:
                    st.markdown(
                        '<div class="driver-panel driver-panel-up">'
                        '<p class="driver-title driver-title-up">▲ &nbsp;Top 10 Pendorong Harga Naik</p>'
                        '<p class="driver-sub">Fitur dengan kontribusi positif terbesar</p>'
                        '</div>', unsafe_allow_html=True
                    )
                    fig_up = go.Figure(go.Bar(
                        x=top_up["pct_impact"][::-1],
                        y=top_up["label"][::-1],
                        orientation="h",
                        marker=dict(
                            color=top_up["pct_impact"][::-1],
                            colorscale=[[0, "#1B6B4F"], [1, "#2EC48D"]],
                        ),
                        text=[f"+{v:.1f}%" for v in top_up["pct_impact"][::-1]],
                        textposition="outside",
                        textfont=dict(color="#2EC48D", size=12),
                        hovertemplate="%{y}<br>Dampak: +%{x:.2f}%<extra></extra>",
                    ))
                    fig_up.update_layout(
                        plot_bgcolor="rgba(0,0,0,0)",
                        paper_bgcolor="rgba(0,0,0,0)",
                        font=dict(family="Inter, sans-serif", color="#9EB3C8", size=12),
                        margin=dict(l=10, r=40, t=10, b=10),
                        height=420,
                        xaxis=dict(title="Dampak terhadap harga (%)", gridcolor="rgba(255,255,255,0.06)", zeroline=False),
                        yaxis=dict(gridcolor="rgba(255,255,255,0.03)"),
                        showlegend=False,
                    )
                    st.plotly_chart(fig_up, use_container_width=True, config={"displayModeBar": False})

                with gcol2:
                    st.markdown(
                        '<div class="driver-panel driver-panel-down">'
                        '<p class="driver-title driver-title-down">▼ &nbsp;Top 10 Pendorong Harga Turun</p>'
                        '<p class="driver-sub">Fitur dengan kontribusi negatif terbesar</p>'
                        '</div>', unsafe_allow_html=True
                    )
                    fig_down = go.Figure(go.Bar(
                        x=top_down["pct_impact"][::-1],
                        y=top_down["label"][::-1],
                        orientation="h",
                        marker=dict(
                            color=top_down["pct_impact"][::-1],
                            colorscale=[[0, "#E05A5A"], [1, "#7A2424"]],
                        ),
                        text=[f"{v:.1f}%" for v in top_down["pct_impact"][::-1]],
                        textposition="outside",
                        textfont=dict(color="#E05A5A", size=12),
                        hovertemplate="%{y}<br>Dampak: %{x:.2f}%<extra></extra>",
                    ))
                    fig_down.update_layout(
                        plot_bgcolor="rgba(0,0,0,0)",
                        paper_bgcolor="rgba(0,0,0,0)",
                        font=dict(family="Inter, sans-serif", color="#9EB3C8", size=12),
                        margin=dict(l=10, r=40, t=10, b=10),
                        height=420,
                        xaxis=dict(title="Dampak terhadap harga (%)", gridcolor="rgba(255,255,255,0.06)", zeroline=False),
                        yaxis=dict(gridcolor="rgba(255,255,255,0.03)"),
                        showlegend=False,
                    )
                    st.plotly_chart(fig_down, use_container_width=True, config={"displayModeBar": False})

                st.caption(
                    "ℹ Persentase dampak dihitung relatif terhadap model dalam skala log-harga "
                    "(exp(koefisien × nilai) − 1) × 100%, bukan kontribusi nominal langsung dalam Dolar."
                )
            else:
                st.info("Model tidak menyediakan koefisien (coef_), grafik pendorong harga tidak dapat ditampilkan.")

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
