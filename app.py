import streamlit as st
import pandas as pd
import numpy as np
import joblib

# ─── PAGE CONFIG ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="PropValAI – Valuasi Properti Cerdas",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── CUSTOM CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Import Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=DM+Serif+Display:ital@0;1&display=swap');

/* ── Root Variables ── */
:root {
    --navy:   #0D1B2A;
    --ink:    #1A2940;
    --slate:  #2E4057;
    --steel:  #3D5A80;
    --sky:    #98C1D9;
    --ice:    #E0ECF4;
    --gold:   #E9A22B;
    --gold-lt:#F5C96A;
    --white:  #FFFFFF;
    --surface:#F7FAFD;
    --muted:  #6B7A8D;
    --border: #D6E4F0;
    --success:#1B9E6E;
    --radius: 12px;
    --shadow: 0 4px 24px rgba(13,27,42,.10);
}

/* ── Global Reset ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    color: var(--ink);
}
.stApp { background: var(--surface); }

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }

/* ── Top Banner ── */
.banner {
    background: linear-gradient(135deg, var(--navy) 0%, var(--slate) 60%, var(--steel) 100%);
    padding: 3rem 2.5rem 2.5rem;
    border-radius: 0 0 24px 24px;
    margin: -1rem -1rem 2rem -1rem;
    position: relative;
    overflow: hidden;
}
.banner::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 320px; height: 320px;
    background: radial-gradient(circle, rgba(152,193,217,.18) 0%, transparent 70%);
    border-radius: 50%;
}
.banner-eyebrow {
    font-size: .72rem;
    font-weight: 600;
    letter-spacing: .18em;
    text-transform: uppercase;
    color: var(--sky);
    margin-bottom: .5rem;
}
.banner-title {
    font-family: 'DM Serif Display', serif;
    font-size: 2.4rem;
    color: var(--white);
    line-height: 1.15;
    margin: 0 0 .75rem 0;
}
.banner-title span { color: var(--gold); }
.banner-sub {
    font-size: .92rem;
    color: var(--sky);
    max-width: 540px;
    line-height: 1.6;
}
.badge-row { display:flex; gap:.75rem; margin-top:1.25rem; flex-wrap:wrap; }
.badge {
    background: rgba(255,255,255,.10);
    border: 1px solid rgba(255,255,255,.18);
    border-radius: 20px;
    padding: .25rem .85rem;
    font-size: .75rem;
    color: var(--ice);
    font-weight: 500;
}

/* ── Section headers ── */
.section-label {
    font-size: .68rem;
    font-weight: 700;
    letter-spacing: .16em;
    text-transform: uppercase;
    color: var(--steel);
    margin-bottom: .75rem;
    display: flex;
    align-items: center;
    gap: .5rem;
}
.section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
}

/* ── Card ── */
.card {
    background: var(--white);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.5rem;
    box-shadow: var(--shadow);
    margin-bottom: 1rem;
}

/* ── Input overrides ── */
div[data-testid="stNumberInput"] input,
div[data-testid="stSelectbox"] select {
    border-radius: 8px !important;
    border-color: var(--border) !important;
    background: var(--surface) !important;
    font-size: .875rem !important;
}
div[data-testid="stSlider"] > div:first-child {
    color: var(--muted);
    font-size: .8rem;
}

/* ── Grade pills ── */
.grade-pills { display:flex; flex-wrap:wrap; gap:.4rem; margin-top:.4rem; }
.grade-pill {
    padding: .2rem .6rem;
    border-radius: 20px;
    font-size: .72rem;
    font-weight: 600;
}
.grade-low  { background:#FEF3C7; color:#92400E; }
.grade-mid  { background:#DBEAFE; color:#1E40AF; }
.grade-high { background:#D1FAE5; color:#065F46; }
.grade-lux  { background:#EDE9FE; color:#5B21B6; }

/* ── CTA Button ── */
div[data-testid="stButton"] > button[kind="primary"] {
    background: linear-gradient(135deg, var(--steel) 0%, var(--navy) 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: .85rem 2rem !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    letter-spacing: .02em !important;
    width: 100% !important;
    box-shadow: 0 6px 20px rgba(61,90,128,.35) !important;
    transition: all .2s !important;
}
div[data-testid="stButton"] > button[kind="primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 28px rgba(61,90,128,.45) !important;
}

/* ── Result card ── */
.result-card {
    background: linear-gradient(135deg, var(--navy) 0%, var(--slate) 100%);
    border-radius: 16px;
    padding: 2rem 2.5rem;
    text-align: center;
    color: white;
    box-shadow: 0 8px 32px rgba(13,27,42,.25);
    margin: 1.5rem 0;
    position: relative;
    overflow: hidden;
}
.result-card::before {
    content: '';
    position: absolute;
    bottom: -40px; right: -40px;
    width: 180px; height: 180px;
    background: radial-gradient(circle, rgba(233,162,43,.2), transparent 70%);
    border-radius: 50%;
}
.result-label {
    font-size: .75rem;
    font-weight: 600;
    letter-spacing: .15em;
    text-transform: uppercase;
    color: var(--sky);
    margin-bottom: .5rem;
}
.result-price {
    font-family: 'DM Serif Display', serif;
    font-size: 3rem;
    color: var(--gold);
    line-height: 1.1;
    margin: .25rem 0;
}
.result-note { font-size: .8rem; color: var(--sky); margin-top: .75rem; }

/* ── Metric mini cards ── */
.mini-metrics { display:flex; gap:.75rem; flex-wrap:wrap; margin-top:1rem; }
.mini-metric {
    flex: 1 1 160px;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: .75rem 1rem;
    text-align: center;
}
.mini-metric .mm-val {
    font-size: 1.4rem;
    font-weight: 700;
    color: var(--steel);
}
.mini-metric .mm-lbl {
    font-size: .72rem;
    color: var(--muted);
    margin-top: .2rem;
}

/* ── Tooltip caption ── */
.tip { font-size: .72rem; color: var(--muted); margin-top: .2rem; }

/* ── Divider ── */
.hr { border: none; border-top: 1px solid var(--border); margin: 1.5rem 0; }

/* ── Footer ── */
.footer {
    text-align: center;
    font-size: .72rem;
    color: var(--muted);
    padding: 1.5rem 0 .5rem;
}
</style>
""", unsafe_allow_html=True)

# ─── BANNER ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="banner">
  <div class="banner-eyebrow">🏙️ PropValAI · Sistem Valuasi Properti</div>
  <div class="banner-title">Estimasi Harga Rumah<br>berbasis <span>Kecerdasan Buatan</span></div>
  <div class="banner-sub">
    Masukkan atribut fisik dan lokasi properti untuk mendapatkan estimasi harga
    secara instan menggunakan model <em>Multiple Linear Regression</em> dengan fitur spasial.
  </div>
  <div class="badge-row">
    <span class="badge">📐 Multiple Linear Regression</span>
    <span class="badge">🗺️ Spatial Features</span>
    <span class="badge">✅ Akurasi 94.56%</span>
    <span class="badge">🏠 King County Dataset</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ─── LOAD MODEL ─────────────────────────────────────────────────────────────────
@st.cache_resource
def load_assets():
    model = joblib.load('model_harga_properti.pkl')
    features = joblib.load('daftar_fitur.pkl')
    return model, features

try:
    model, features_final = load_assets()
    all_zipcodes = sorted([col.replace('ZipCode_', '') for col in features_final if col.startswith('ZipCode_')])
    model_loaded = True
except FileNotFoundError:
    model_loaded = False

# ─── MAIN LAYOUT ────────────────────────────────────────────────────────────────
col_form, col_info = st.columns([3, 1], gap="large")

with col_form:
    # ── Section 1: Fisik Bangunan ──
    st.markdown('<div class="section-label">📐 Atribut Fisik Bangunan</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        sqft = st.number_input(
            "Luas Ruang Tamu (sq ft)",
            min_value=300, max_value=10000, value=1800, step=50,
            help="Total area ruang hidup dalam satuan kaki persegi"
        )
        st.markdown('<div class="tip">Rata-rata: 1.500 – 2.500 sq ft</div>', unsafe_allow_html=True)

        bedrooms = st.slider("Kamar Tidur", min_value=1, max_value=10, value=3)

        bathrooms = st.slider("Kamar Mandi", min_value=1.0, max_value=8.0, value=2.0, step=0.25)

    with c2:
        grade = st.slider(
            "Skor Kualitas Konstruksi (BldgGrade)",
            min_value=1, max_value=13, value=7,
            help="1-3: Rendah · 4-6: Standar · 7-10: Baik · 11-13: Mewah"
        )
        # Grade hint pills
        if grade <= 3:
            label, css = "Konstruksi Rendah", "grade-low"
        elif grade <= 6:
            label, css = "Standar", "grade-mid"
        elif grade <= 10:
            label, css = "Kualitas Baik", "grade-high"
        else:
            label, css = "Mewah / Premium", "grade-lux"
        st.markdown(f'<div class="grade-pills"><span class="grade-pill {css}">{label} (Grade {grade})</span></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        age = st.number_input(
            "Umur Bangunan (Tahun)",
            min_value=0, max_value=120, value=15, step=1,
            help="Tahun sejak bangunan pertama kali dibangun"
        )

    st.markdown('<div class="hr"></div>', unsafe_allow_html=True)

    # ── Section 2: Jarak Fasilitas ──
    st.markdown('<div class="section-label">🗺️ Kedekatan Fasilitas Publik</div>', unsafe_allow_html=True)

    c3, c4, c5 = st.columns(3)
    with c3:
        park = st.number_input("🌳 Jarak ke Taman (km)", min_value=0.0, max_value=50.0, value=0.5, step=0.1)
    with c4:
        school = st.number_input("🏫 Jarak ke Sekolah (km)", min_value=0.0, max_value=50.0, value=0.3, step=0.1)
    with c5:
        hospital = st.number_input("🏥 Jarak ke RS (km)", min_value=0.0, max_value=50.0, value=1.2, step=0.1)

    st.markdown('<div class="tip">Semakin dekat ke fasilitas umum, nilai properti cenderung lebih tinggi.</div>', unsafe_allow_html=True)

    st.markdown('<div class="hr"></div>', unsafe_allow_html=True)

    # ── Section 3: Lokasi ──
    st.markdown('<div class="section-label">📍 Lokasi & Kode Pos</div>', unsafe_allow_html=True)

    if model_loaded:
        selected_zip = st.selectbox(
            "Kode Pos Kawasan (ZipCode)",
            options=all_zipcodes,
            help="Lokasi berpengaruh signifikan terhadap harga berdasarkan prestige kawasan"
        )
    else:
        st.selectbox("Kode Pos Kawasan (ZipCode)", options=["98001"], disabled=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── CTA ──
    if model_loaded:
        predict_btn = st.button("🚀  Hitung Estimasi Harga", type="primary", use_container_width=True)
    else:
        st.button("🚀  Hitung Estimasi Harga", type="primary", use_container_width=True, disabled=True)
        st.error(
            "⚠️ **Model tidak ditemukan.** Pastikan file `model_harga_properti.pkl` dan "
            "`daftar_fitur.pkl` berada di folder yang sama dengan `app.py`.",
            icon="🚫"
        )
        predict_btn = False

    # ── RESULT ──
    if model_loaded and predict_btn:
        with st.spinner("Menjalankan model AI…"):
            input_data = pd.DataFrame(0, index=[0], columns=features_final)
            input_data['SqFtTotLiving'] = sqft
            input_data['Bedrooms']      = bedrooms
            input_data['Bathrooms']     = bathrooms
            input_data['BldgGrade']     = grade
            input_data['HouseAge']      = age
            input_data['dist_to_park']     = park
            input_data['dist_to_school']   = school
            input_data['dist_to_hospital'] = hospital

            target_col = f"ZipCode_{selected_zip}"
            if target_col in input_data.columns:
                input_data[target_col] = 1

            pred_log  = model.predict(input_data)
            harga     = np.exp(pred_log[0])

        st.markdown(f"""
        <div class="result-card">
          <div class="result-label">Estimasi Valuasi AI</div>
          <div class="result-price">${harga:,.0f}</div>
          <div class="result-note">
            ✅ Dihitung menggunakan model MLR dengan akurasi <strong>94.56% (R²)</strong>
            berdasarkan data King County, Washington.
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Mini summary metrics
        harga_per_sqft = harga / sqft if sqft else 0
        st.markdown(f"""
        <div class="mini-metrics">
          <div class="mini-metric">
            <div class="mm-val">${harga_per_sqft:,.0f}</div>
            <div class="mm-lbl">Harga per sq ft</div>
          </div>
          <div class="mini-metric">
            <div class="mm-val">{bedrooms} KT / {bathrooms:.2g} KM</div>
            <div class="mm-lbl">Komposisi Kamar</div>
          </div>
          <div class="mini-metric">
            <div class="mm-val">Grade {grade}</div>
            <div class="mm-lbl">Kualitas Konstruksi</div>
          </div>
          <div class="mini-metric">
            <div class="mm-val">{age} thn</div>
            <div class="mm-lbl">Umur Bangunan</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

with col_info:
    # ── Info Cards ──
    st.markdown('<div class="section-label">ℹ️ Panduan</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
      <strong style="font-size:.9rem;">🎯 Cara Pakai</strong>
      <ol style="font-size:.8rem;color:#4A5568;margin-top:.75rem;padding-left:1.2rem;line-height:1.8;">
        <li>Isi atribut fisik bangunan</li>
        <li>Masukkan jarak ke fasilitas terdekat</li>
        <li>Pilih kode pos kawasan</li>
        <li>Tekan tombol <em>Hitung Estimasi</em></li>
      </ol>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
      <strong style="font-size:.9rem;">📊 Tentang Model</strong>
      <p style="font-size:.78rem;color:#4A5568;margin-top:.6rem;line-height:1.7;">
        Model dilatih menggunakan dataset King County, WA dengan fitur spasial tambahan
        seperti jarak ke taman, sekolah, dan rumah sakit berbasis algoritma K-D Tree.
        Target menggunakan transformasi logaritmik untuk mengurangi skewness.
      </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
      <strong style="font-size:.9rem;">⚠️ Disclaimer</strong>
      <p style="font-size:.78rem;color:#4A5568;margin-top:.6rem;line-height:1.7;">
        Hasil estimasi bersifat indikatif dan tidak menggantikan penilaian properti
        profesional. Gunakan sebagai referensi awal saja.
      </p>
    </div>
    """, unsafe_allow_html=True)

    # BldgGrade legend
    st.markdown("""
    <div class="card">
      <strong style="font-size:.9rem;">🏗️ Skala BldgGrade</strong>
      <div style="margin-top:.7rem;">
        <div class="grade-pills" style="flex-direction:column;gap:.35rem;">
          <span class="grade-pill grade-low" style="width:fit-content">1–3 &nbsp;Rendah / Darurat</span>
          <span class="grade-pill grade-mid" style="width:fit-content">4–6 &nbsp;Standar</span>
          <span class="grade-pill grade-high" style="width:fit-content">7–10  Baik</span>
          <span class="grade-pill grade-lux" style="width:fit-content">11–13 Mewah</span>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ─── FOOTER ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
  PropValAI · Proyek TPDB · Multiple Linear Regression &amp; Spatial Features
  · Data: King County, WA · Model akurasi 94.56%
</div>
""", unsafe_allow_html=True)
