import streamlit as st
import pandas as pd
import numpy as np
import joblib

# ============================================================
# 1. KONFIGURASI HALAMAN
# ============================================================
st.set_page_config(
    page_title="Valuasi Properti AI | King County",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# 2. CUSTOM CSS — TAMPILAN PROFESIONAL
# ============================================================
st.markdown("""
<style>
    /* Font & warna dasar */
    html, body, [class*="css"] {
        font-family: 'Segoe UI', 'Inter', sans-serif;
    }

    /* Header utama */
    .main-header {
        font-size: 2.3rem;
        font-weight: 800;
        color: #1B3A57;
        margin-bottom: 0;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #5A6B7B;
        margin-top: 0.2rem;
        margin-bottom: 1.5rem;
    }

    /* Kartu metrik */
    .metric-card {
        background: linear-gradient(135deg, #1B3A57 0%, #2C5F7C 100%);
        padding: 1.2rem 1.5rem;
        border-radius: 14px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 14px rgba(0,0,0,0.12);
    }
    .metric-card h2 {
        margin: 0;
        font-size: 2.1rem;
        font-weight: 800;
    }
    .metric-card p {
        margin: 0;
        font-size: 0.85rem;
        opacity: 0.85;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }

    /* Kartu hasil prediksi */
    .result-box {
        background: linear-gradient(135deg, #e9f7ef 0%, #d4f1de 100%);
        border: 1px solid #8fd9b6;
        border-radius: 16px;
        padding: 1.8rem 2rem;
        text-align: center;
        margin-top: 1rem;
    }
    .result-box h1 {
        color: #1B5E3C;
        font-size: 2.6rem;
        margin: 0.3rem 0;
    }
    .result-box p {
        color: #2E4F3E;
        margin: 0;
        font-size: 0.95rem;
    }

    /* Badge kecil */
    .badge {
        display: inline-block;
        background-color: #EEF3F8;
        color: #1B3A57;
        border-radius: 20px;
        padding: 0.25rem 0.9rem;
        font-size: 0.78rem;
        font-weight: 600;
        margin-right: 0.4rem;
        border: 1px solid #d6e2ec;
    }

    /* Section divider */
    .section-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #1B3A57;
        margin-top: 1.6rem;
        margin-bottom: 0.4rem;
        border-left: 4px solid #2C5F7C;
        padding-left: 0.6rem;
    }

    div[data-testid="stMetricValue"] {
        color: #1B3A57;
    }

    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ============================================================
# 3. MEMUAT MODEL & ASET
# ============================================================
MODEL_R2 = 0.9457  # R-Squared model final (lihat tahap evaluasi di notebook)
MODEL_NAME = "Multiple Linear Regression + Spatial & Log-Price Feature Engineering"

@st.cache_resource
def load_assets():
    model = joblib.load("model_harga_properti.pkl")
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
    load_error = e

# ============================================================
# 4. HEADER
# ============================================================
col_logo, col_title = st.columns([0.08, 0.92])
with col_logo:
    st.markdown("<div style='font-size:3rem;'>🏠</div>", unsafe_allow_html=True)
with col_title:
    st.markdown('<p class="main-header">Sistem Valuasi Properti Berbasis AI</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="sub-header">Estimasi harga jual rumah di King County menggunakan model regresi '
        'spasial dengan fitur jarak ke fasilitas publik</p>',
        unsafe_allow_html=True,
    )

st.markdown(
    f"""
    <span class="badge">📊 Model: Linear Regression</span>
    <span class="badge">🌍 Fitur Spasial: Taman, Sekolah, RS</span>
    <span class="badge">📈 R² = {MODEL_R2:.2%}</span>
    """,
    unsafe_allow_html=True,
)
st.markdown("<br>", unsafe_allow_html=True)

if not assets_ready:
    st.error(
        f"⚠️ Gagal memuat sistem: {load_error}\n\n"
        "Pastikan file **model_harga_properti.pkl** dan **daftar_fitur.pkl** berada "
        "di folder yang sama dengan app.py, atau cek kembali proses export dari Colab."
    )
    st.stop()

# ============================================================
# 5. SIDEBAR — INFORMASI MODEL
# ============================================================
with st.sidebar:
    st.markdown("### ℹ️ Tentang Model")
    st.write(
        "Model ini dilatih menggunakan dataset penjualan rumah **King County, "
        "Washington (2014–2015)**, dipadukan dengan data **titik fasilitas publik** "
        "(taman, sekolah, rumah sakit) untuk menghitung jarak terdekat sebagai fitur tambahan."
    )
    st.markdown("---")
    st.markdown("**Ringkasan performa model**")
    st.metric("R-Squared (Akurasi)", f"{MODEL_R2:.2%}")
    st.caption(
        "R² diukur pada data uji (20% hold-out) setelah transformasi log harga "
        "dan one-hot encoding ZipCode."
    )
    st.markdown("---")
    st.markdown("**Tahapan pemodelan**")
    st.markdown(
        "- Pembersihan & penggabungan data spasial\n"
        "- Perhitungan jarak ke fasilitas (KD-Tree)\n"
        "- Log-transform target harga\n"
        "- One-hot encoding ZipCode\n"
        "- Linear Regression final"
    )
    st.markdown("---")
    st.caption("Dibuat sebagai bagian dari proyek skripsi/penelitian valuasi properti — King County dataset.")

# ============================================================
# 6. FORM INPUT
# ============================================================
st.markdown('<p class="section-title">📋 Atribut Fisik Bangunan</p>', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    sqft = st.number_input("Luas Ruang Tamu (SqFt)", min_value=300, max_value=10000, value=1800, step=50)
    bedrooms = st.slider("Jumlah Kamar Tidur", min_value=1, max_value=10, value=3)
with col2:
    bathrooms = st.slider("Jumlah Kamar Mandi", min_value=1.0, max_value=8.0, value=2.0, step=0.25)
    grade = st.slider("Skor Kualitas Konstruksi (BldgGrade)", min_value=1, max_value=13, value=7)
with col3:
    age = st.number_input("Umur Bangunan (Tahun)", min_value=0, max_value=120, value=15)
    st.caption("Skala BldgGrade: 1 (rendah) – 13 (mewah/premium)")

st.markdown('<p class="section-title">📍 Lokasi & Jarak ke Fasilitas Publik</p>', unsafe_allow_html=True)
col4, col5, col6 = st.columns(3)
with col4:
    park = st.number_input("Jarak ke Taman Terdekat (Km)", min_value=0.0, max_value=50.0, value=0.5, step=0.1)
with col5:
    school = st.number_input("Jarak ke Sekolah Terdekat (Km)", min_value=0.0, max_value=50.0, value=0.3, step=0.1)
with col6:
    hospital = st.number_input("Jarak ke RS Terdekat (Km)", min_value=0.0, max_value=50.0, value=1.2, step=0.1)

selected_zip = st.selectbox("Pilih Kode Pos (ZipCode)", all_zipcodes)

st.markdown("<br>", unsafe_allow_html=True)
predict_clicked = st.button("🚀 Hitung Estimasi Harga Rumah", type="primary", use_container_width=True)

# ============================================================
# 7. PROSES PREDIKSI
# ============================================================
if predict_clicked:
    with st.spinner("Menghitung estimasi harga..."):
        # Template baris fitur, default 0
        input_data = pd.DataFrame(0, index=[0], columns=features_final)

        # Fitur inti yang memang dipakai untuk melatih model (lihat notebook)
        if "SqFtTotLiving" in input_data.columns:
            input_data["SqFtTotLiving"] = sqft
        if "Bedrooms" in input_data.columns:
            input_data["Bedrooms"] = bedrooms
        if "Bathrooms" in input_data.columns:
            input_data["Bathrooms"] = bathrooms
        if "BldgGrade" in input_data.columns:
            input_data["BldgGrade"] = grade
        if "HouseAge" in input_data.columns:
            input_data["HouseAge"] = age
        if "dist_to_park" in input_data.columns:
            input_data["dist_to_park"] = park
        if "dist_to_school" in input_data.columns:
            input_data["dist_to_school"] = school
        if "dist_to_hospital" in input_data.columns:
            input_data["dist_to_hospital"] = hospital
        if "Space_Quality" in input_data.columns:
            input_data["Space_Quality"] = sqft * grade

        # Nilai default/rata-rata untuk kolom administratif yang tidak diisi lewat form
        # namun tetap ada di daftar fitur model (agar dimensi matriks cocok)
        default_values = {
            "SqFtLot": 5000,
            "NbrLivingUnits": 1,
            "LandVal": 150000,
            "ImpsVal": 200000,
            "zhvi_px": 400000,
            "AdjSalePrice": 500000,
            "lat": 47.5,
            "lon": -122.2,
            "ZIPCODE": None,  # diisi di bawah dari selected_zip
        }
        for col, val in default_values.items():
            if col in input_data.columns:
                input_data[col] = int(selected_zip) if col == "ZIPCODE" else val

        # Aktifkan kolom dummy ZipCode yang sesuai
        target_dummy_col = f"ZipCode_{selected_zip}"
        if target_dummy_col in input_data.columns:
            input_data[target_dummy_col] = 1

        try:
            prediksi_log = model.predict(input_data)
            harga_final = np.exp(prediksi_log[0])

            st.markdown("---")
            colA, colB, colC = st.columns(3)
            with colA:
                st.markdown(
                    f"<div class='metric-card'><p>Luas Bangunan</p><h2>{sqft:,} SqFt</h2></div>",
                    unsafe_allow_html=True,
                )
            with colB:
                st.markdown(
                    f"<div class='metric-card'><p>ZipCode</p><h2>{selected_zip}</h2></div>",
                    unsafe_allow_html=True,
                )
            with colC:
                st.markdown(
                    f"<div class='metric-card'><p>Grade Konstruksi</p><h2>{grade}/13</h2></div>",
                    unsafe_allow_html=True,
                )

            st.markdown(
                f"""
                <div class="result-box">
                    <p>🎉 Estimasi Harga Properti</p>
                    <h1>${harga_final:,.2f}</h1>
                    <p>Dihitung dengan model regresi spasial — R² ≈ {MODEL_R2:.2%} pada data uji</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            with st.expander("🔍 Lihat detail fitur yang dikirim ke model"):
                tampil_kolom = [c for c in [
                    "SqFtTotLiving", "Bedrooms", "Bathrooms", "BldgGrade", "HouseAge",
                    "dist_to_park", "dist_to_school", "dist_to_hospital", "Space_Quality",
                    "ZIPCODE", target_dummy_col,
                ] if c in input_data.columns]
                st.dataframe(input_data[tampil_kolom].T.rename(columns={0: "Nilai"}))

            st.caption(
                "⚠️ Estimasi ini bersifat indikatif berdasarkan data historis King County "
                "(2014–2015) dan tidak menggantikan penilaian profesional (appraisal) resmi."
            )

        except Exception as pred_err:
            st.error(f"Terjadi kesalahan saat melakukan prediksi: {pred_err}")

# ============================================================
# 8. FOOTER
# ============================================================
st.markdown("---")
st.markdown(
    f"<p style='text-align:center; color:#9AA7B2; font-size:0.85rem;'>"
    f"Sistem Valuasi Properti AI · Model: {MODEL_NAME} · Dataset: King County House Sales"
    f"</p>",
    unsafe_allow_html=True,
)
