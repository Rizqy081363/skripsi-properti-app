import streamlit as st
import pandas as pd
import numpy as np
import joblib

# ─── PAGE CONFIG ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="PropVal AI · Valuasi Properti",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── CUSTOM CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
  /* ── Google Fonts ── */
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@700&display=swap');

  /* ── Base Reset ── */
  html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
  }

  /* ── App background ── */
  .stApp {
    background: #0a0e1a;
  }

  /* ── Hide default Streamlit chrome ── */
  #MainMenu, footer, header { visibility: hidden; }
  .block-container { padding: 0 !important; max-width: 100% !important; }

  /* ── Hero banner ── */
  .hero {
    background: linear-gradient(135deg, #0d1b2a 0%, #112240 60%, #0a3d62 100%);
    padding: 56px 64px 48px;
    border-bottom: 1px solid rgba(100,220,255,0.08);
    position: relative;
    overflow: hidden;
  }
  .hero::before {
    content: '';
    position: absolute;
    top: -80px; right: -80px;
    width: 400px; height: 400px;
    background: radial-gradient(circle, rgba(0,180,255,0.12) 0%, transparent 70%);
    pointer-events: none;
  }
  .hero-eyebrow {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 3px;
    color: #64d2ff;
    text-transform: uppercase;
    margin-bottom: 12px;
  }
  .hero-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(32px, 4vw, 52px);
    font-weight: 700;
    color: #f0f4ff;
    line-height: 1.15;
    margin-bottom: 12px;
  }
  .hero-title span { color: #64d2ff; }
  .hero-sub {
    font-size: 15px;
    color: #8899bb;
    max-width: 540px;
    line-height: 1.65;
  }
  .hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    margin-top: 20px;
    background: rgba(100,210,255,0.1);
    border: 1px solid rgba(100,210,255,0.25);
    border-radius: 100px;
    padding: 6px 14px;
    font-size: 12px;
    font-weight: 500;
    color: #64d2ff;
  }
  .hero-badge .dot {
    width: 7px; height: 7px;
    background: #30d158;
    border-radius: 50%;
    animation: pulse 2s infinite;
  }
  @keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
  }

  /* ── Stat bar ── */
  .stat-bar {
    background: #0d1520;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    padding: 18px 64px;
    display: flex;
    gap: 48px;
  }
  .stat-item { text-align: left; }
  .stat-value {
    font-size: 22px;
    font-weight: 700;
    color: #f0f4ff;
    letter-spacing: -0.5px;
  }
  .stat-label {
    font-size: 11px;
    color: #5a6a8a;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-top: 2px;
  }

  /* ── Main content wrapper ── */
  .main-content {
    padding: 40px 64px 80px;
    max-width: 1200px;
  }

  /* ── Section headers ── */
  .section-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 24px;
    margin-top: 40px;
  }
  .section-header .icon {
    width: 36px; height: 36px;
    background: rgba(100,210,255,0.1);
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 16px;
  }
  .section-header h3 {
    font-size: 17px;
    font-weight: 600;
    color: #d0d8ef;
    margin: 0;
  }
  .section-header p {
    font-size: 12px;
    color: #5a6a8a;
    margin: 0;
    letter-spacing: 0.3px;
  }

  /* ── Card panels ── */
  .card {
    background: #111827;
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 16px;
    padding: 28px;
    margin-bottom: 20px;
  }

  /* ── Streamlit widget overrides ── */
  div[data-baseweb="input"] input,
  div[data-baseweb="select"] div,
  div[data-baseweb="slider"] {
    background: #1a2236 !important;
    border-color: rgba(100,210,255,0.15) !important;
    color: #d0d8ef !important;
    border-radius: 10px !important;
  }

  .stSlider [data-baseweb="slider"] {
    padding: 0 !important;
  }
  .stSlider .StyledThumb {
    background: #64d2ff !important;
    border-color: #64d2ff !important;
  }
  .stSlider .StyledTrack[data-testid="stSliderTrackFill"] {
    background: #64d2ff !important;
  }

  label, .stSlider label, .stNumberInput label, .stSelectbox label {
    color: #8899bb !important;
    font-size: 12px !important;
    font-weight: 500 !important;
    letter-spacing: 0.5px !important;
    text-transform: uppercase !important;
  }

  /* ── Primary button ── */
  .stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #0077cc, #0099ee) !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 14px 32px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 15px !important;
    color: #fff !important;
    width: 100%;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 20px rgba(0,150,255,0.35) !important;
    letter-spacing: 0.3px !important;
  }
  .stButton > button[kind="primary"]:hover {
    box-shadow: 0 6px 28px rgba(0,150,255,0.55) !important;
    transform: translateY(-1px) !important;
  }

  /* ── Result card ── */
  .result-card {
    background: linear-gradient(135deg, #0d2040 0%, #0a3060 100%);
    border: 1px solid rgba(100,210,255,0.25);
    border-radius: 20px;
    padding: 40px;
    text-align: center;
    margin-top: 32px;
    position: relative;
    overflow: hidden;
  }
  .result-card::before {
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(ellipse at 50% 0%, rgba(100,210,255,0.08) 0%, transparent 60%);
    pointer-events: none;
  }
  .result-label {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 3px;
    color: #64d2ff;
    text-transform: uppercase;
    margin-bottom: 8px;
  }
  .result-price {
    font-family: 'Playfair Display', serif;
    font-size: clamp(40px, 6vw, 64px);
    font-weight: 700;
    color: #f0f4ff;
    letter-spacing: -2px;
    line-height: 1.1;
  }
  .result-meta {
    font-size: 13px;
    color: #5a7aaa;
    margin-top: 10px;
  }
  .result-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(48,209,88,0.12);
    border: 1px solid rgba(48,209,88,0.3);
    border-radius: 100px;
    padding: 6px 16px;
    font-size: 12px;
    color: #30d158;
    font-weight: 600;
    margin-top: 16px;
  }

  /* ── Grade legend ── */
  .grade-bar {
    display: flex;
    gap: 3px;
    margin-top: 6px;
    margin-bottom: 4px;
  }
  .grade-cell {
    flex: 1;
    height: 6px;
    border-radius: 3px;
    background: rgba(255,255,255,0.07);
  }
  .grade-cell.active {
    background: #64d2ff;
  }

  /* ── Divider ── */
  .divider {
    border: none;
    border-top: 1px solid rgba(255,255,255,0.05);
    margin: 32px 0;
  }

  /* ── Info tooltip chip ── */
  .info-chip {
    font-size: 11px;
    color: #5a7aaa;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 6px;
    padding: 4px 10px;
    margin-bottom: 16px;
    display: inline-block;
  }

  /* ── Error card ── */
  .error-card {
    background: rgba(255,60,60,0.08);
    border: 1px solid rgba(255,60,60,0.2);
    border-radius: 14px;
    padding: 24px 28px;
    color: #ff6b6b;
    font-size: 14px;
    line-height: 1.6;
  }
  .error-card strong { color: #ff4d4d; }

  /* ── Streamlit number input ── */
  .stNumberInput > div > div > input {
    background: #1a2236 !important;
    color: #d0d8ef !important;
    border-radius: 10px !important;
    border: 1px solid rgba(100,210,255,0.15) !important;
    font-size: 15px !important;
  }
  .stSelectbox > div > div {
    background: #1a2236 !important;
    border: 1px solid rgba(100,210,255,0.15) !important;
    border-radius: 10px !important;
    color: #d0d8ef !important;
  }
</style>
""", unsafe_allow_html=True)

# ─── HERO ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-eyebrow">AI · Machine Learning · Real Estate</div>
  <div class="hero-title">Sistem Valuasi Properti<br><span>berbasis Kecerdasan Buatan</span></div>
  <div class="hero-sub">
    Estimasi harga pasar properti secara instan menggunakan
    Multiple Linear Regression dengan fitur spasial—jarak ke taman,
    sekolah, dan rumah sakit terdekat.
  </div>
  <div class="hero-badge">
    <span class="dot"></span>
    Model Aktif · Akurasi R² 94.56%
  </div>
</div>
""", unsafe_allow_html=True)

# ─── STAT BAR ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="stat-bar">
  <div class="stat-item">
    <div class="stat-value">94.56%</div>
    <div class="stat-label">Akurasi Model (R²)</div>
  </div>
  <div class="stat-item">
    <div class="stat-value">MLR + Spatial</div>
    <div class="stat-label">Algoritma</div>
  </div>
  <div class="stat-item">
    <div class="stat-value">King County</div>
    <div class="stat-label">Dataset Wilayah</div>
  </div>
  <div class="stat-item">
    <div class="stat-value">8 Fitur</div>
    <div class="stat-label">Parameter Input</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─── LOAD MODEL ──────────────────────────────────────────────────────────────
@st.cache_resource
def load_assets():
    model = joblib.load('model_harga_properti.pkl')
    features = joblib.load('daftar_fitur.pkl')
    return model, features

# ─── MAIN LAYOUT ─────────────────────────────────────────────────────────────
with st.container():
    st.markdown('<div class="main-content">', unsafe_allow_html=True)

    try:
        model, features_final = load_assets()
        all_zipcodes = sorted([
            col.replace('ZipCode_', '')
            for col in features_final
            if col.startswith('ZipCode_')
        ])

        # ── Section 1: Physical Attributes ──────────────────────────────────
        st.markdown("""
        <div class="section-header">
          <div class="icon">🏗️</div>
          <div>
            <h3>Atribut Fisik Bangunan</h3>
            <p>Spesifikasi teknis properti yang akan divaluasi</p>
          </div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4, gap="medium")
        with col1:
            sqft = st.number_input(
                "Luas Ruang Tamu (SqFt)",
                min_value=300, max_value=10000, value=1800, step=50,
                help="Luas total ruang tamu dalam satuan square feet"
            )
        with col2:
            bedrooms = st.number_input(
                "Kamar Tidur",
                min_value=1, max_value=10, value=3,
                help="Jumlah kamar tidur"
            )
        with col3:
            bathrooms = st.number_input(
                "Kamar Mandi",
                min_value=1.0, max_value=8.0, value=2.0, step=0.25,
                help="Jumlah kamar mandi (0.25 = hanya toilet)"
            )
        with col4:
            age = st.number_input(
                "Umur Bangunan (Tahun)",
                min_value=0, max_value=120, value=15,
                help="Selisih antara tahun sekarang dan tahun dibangun"
            )

        st.markdown("<br>", unsafe_allow_html=True)

        # Building grade with visual bar
        st.markdown('<p style="font-size:12px;color:#8899bb;font-weight:500;letter-spacing:0.5px;text-transform:uppercase;margin-bottom:4px;">Skor Kualitas Konstruksi (BldgGrade)</p>', unsafe_allow_html=True)
        grade = st.slider("", min_value=1, max_value=13, value=7, label_visibility="collapsed")

        grade_desc = {
            range(1, 4): ("Rendah", "#ff6b6b"),
            range(4, 7): ("Di Bawah Rata-rata", "#ffa500"),
            range(7, 10): ("Rata-rata hingga Baik", "#64d2ff"),
            range(10, 12): ("Sangat Baik", "#30d158"),
            range(12, 14): ("Mewah", "#c678dd"),
        }
        grade_label, grade_color = "Standar", "#64d2ff"
        for r, (lbl, col) in grade_desc.items():
            if grade in r:
                grade_label, grade_color = lbl, col
                break

        cells = "".join([
            f'<div class="grade-cell {"active" if i < grade else ""}"></div>'
            for i in range(1, 14)
        ])
        st.markdown(f"""
        <div class="grade-bar">{cells}</div>
        <span style="font-size:12px;color:{grade_color};font-weight:600;">{grade}/13 — {grade_label}</span>
        """, unsafe_allow_html=True)

        st.markdown('<hr class="divider">', unsafe_allow_html=True)

        # ── Section 2: Spatial Features ─────────────────────────────────────
        st.markdown("""
        <div class="section-header">
          <div class="icon">📍</div>
          <div>
            <h3>Fitur Spasial & Lokasi</h3>
            <p>Jarak ke fasilitas publik terdekat dalam kilometer</p>
          </div>
        </div>
        """, unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3, gap="medium")
        with c1:
            park = st.number_input(
                "🌳 Jarak ke Taman (Km)",
                min_value=0.0, max_value=50.0, value=0.5, step=0.1,
                format="%.1f"
            )
        with c2:
            school = st.number_input(
                "🏫 Jarak ke Sekolah (Km)",
                min_value=0.0, max_value=50.0, value=0.3, step=0.1,
                format="%.1f"
            )
        with c3:
            hospital = st.number_input(
                "🏥 Jarak ke Rumah Sakit (Km)",
                min_value=0.0, max_value=50.0, value=1.2, step=0.1,
                format="%.1f"
            )

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div class="section-header">
          <div class="icon">🗺️</div>
          <div>
            <h3>Kode Pos Kawasan</h3>
            <p>Lokasi administratif yang memengaruhi nilai properti</p>
          </div>
        </div>
        """, unsafe_allow_html=True)

        selected_zip = st.selectbox(
            "Pilih Kode Pos (ZipCode)",
            options=all_zipcodes,
            label_visibility="collapsed"
        )
        st.markdown(
            f'<span class="info-chip">📌 {len(all_zipcodes)} zona kode pos tersedia dalam dataset King County</span>',
            unsafe_allow_html=True
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # ── CTA Button ──────────────────────────────────────────────────────
        _, btn_col, _ = st.columns([1, 2, 1])
        with btn_col:
            run = st.button("🚀  Hitung Estimasi Harga Properti", type="primary")

        # ── Prediction ──────────────────────────────────────────────────────
        if run:
            input_data = pd.DataFrame(0, index=[0], columns=features_final)
            input_data['SqFtTotLiving'] = sqft
            input_data['Bedrooms'] = bedrooms
            input_data['Bathrooms'] = bathrooms
            input_data['BldgGrade'] = grade
            input_data['HouseAge'] = age
            input_data['dist_to_park'] = park
            input_data['dist_to_school'] = school
            input_data['dist_to_hospital'] = hospital

            target_dummy_col = f"ZipCode_{selected_zip}"
            if target_dummy_col in input_data.columns:
                input_data[target_dummy_col] = 1

            with st.spinner("Menghitung valuasi dengan model AI..."):
                prediksi_log = model.predict(input_data)
                harga_final = np.exp(prediksi_log[0])

            # Breakdown estimates
            harga_low = harga_final * 0.92
            harga_high = harga_final * 1.08

            st.markdown(f"""
            <div class="result-card">
              <div class="result-label">Estimasi Nilai Pasar Properti</div>
              <div class="result-price">${harga_final:,.0f}</div>
              <div class="result-meta">
                Rentang kepercayaan: ${harga_low:,.0f} — ${harga_high:,.0f}
              </div>
              <div class="result-pill">
                ✓ Akurasi Model R² = 94.56%
              </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # Summary breakdown
            d1, d2, d3, d4 = st.columns(4)
            metrics = [
                ("Luas Bangunan", f"{sqft:,} SqFt", d1),
                ("Kualitas Konstruksi", f"Grade {grade}/13", d2),
                ("Umur Properti", f"{age} Tahun", d3),
                ("Zona Lokasi", f"ZIP {selected_zip}", d4),
            ]
            for label, value, col in metrics:
                with col:
                    st.markdown(f"""
                    <div style="background:#111827;border:1px solid rgba(255,255,255,0.06);
                                border-radius:12px;padding:16px;text-align:center;">
                      <div style="font-size:11px;color:#5a6a8a;text-transform:uppercase;
                                  letter-spacing:1px;margin-bottom:6px;">{label}</div>
                      <div style="font-size:16px;font-weight:600;color:#d0d8ef;">{value}</div>
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown("""
            <div style="margin-top:24px;padding:16px 20px;background:rgba(100,210,255,0.04);
                        border:1px solid rgba(100,210,255,0.1);border-radius:12px;">
              <span style="font-size:12px;color:#5a7aaa;line-height:1.7;">
                ⚠️ <strong style="color:#7a9acc;">Catatan:</strong>
                Estimasi ini dihasilkan oleh model statistik berbasis data historis King County
                dan bersifat indikatif. Harga aktual dapat berbeda karena kondisi pasar, renovasi,
                atau faktor mikro-lokasi yang tidak tertangkap dalam model.
              </span>
            </div>
            """, unsafe_allow_html=True)

    except FileNotFoundError:
        st.markdown("""
        <div class="error-card">
          <strong>⚠️ Model tidak ditemukan</strong><br><br>
          File <code>model_harga_properti.pkl</code> dan <code>daftar_fitur.pkl</code> belum ada
          di direktori yang sama dengan <code>app.py</code> ini.<br><br>
          Pastikan kamu sudah menjalankan notebook Colab hingga selesai dan mengunduh kedua file tersebut,
          lalu letakkan di folder yang sama sebelum menjalankan <code>streamlit run app.py</code>.
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ─── FOOTER ──────────────────────────────────────────────────────────────────
st.markdown("""
<div style="border-top:1px solid rgba(255,255,255,0.05);padding:24px 64px;
            display:flex;justify-content:space-between;align-items:center;">
  <span style="font-size:12px;color:#2a3a5a;">
    PropVal AI · Multiple Linear Regression & Spatial Features
  </span>
  <span style="font-size:12px;color:#2a3a5a;">
    Dataset: King County Housing · Model R² 94.56%
  </span>
</div>
""", unsafe_allow_html=True)
