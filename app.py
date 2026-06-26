import streamlit as st
import pandas as pd
import numpy as np
import joblib

# 1. Mengatur konfigurasi halaman Web
st.set_page_config(page_title="Valuasi Properti AI", layout="centered")

st.title("🏠 Sistem Prediksi Harga Properti berbasis AI")
st.write("Aplikasi valas massal menggunakan algoritma Multiple Linear Regression & Spatial Features")
st.markdown("---")

# 2. Memuat Model dan Daftar Fitur dari Colab
@st.cache_resource
def load_assets():
    model = joblib.load('model_harga_properti.pkl')
    features = joblib.load('daftar_fitur.pkl')
    return model, features

try:
    model, features_final = load_assets()
    
    # Memisahkan fitur inti dan fitur dummy ZipCode
    base_features = ['SqFtTotLiving', 'Bedrooms', 'Bathrooms', 'BldgGrade', 'HouseAge', 'dist_to_park', 'dist_to_school', 'dist_to_hospital']
    all_zipcodes = [col.replace('ZipCode_', '') for col in features_final if col.startswith('ZipCode_')]
    
    # 3. Membuat Input Form di Antarmuka Web
    st.subheader("📋 Atribut Fisik & Spasial Bangunan")
    
    col1, col2 = st.columns(2)
    with col1:
        sqft = st.number_input("Luas Ruang Tamu (SqFt)", min_value=300, max_value=10000, value=1800)
        bedrooms = st.slider("Jumlah Kamar Tidur", min_value=1, max_value=10, value=3)
        bathrooms = st.slider("Jumlah Kamar Mandi", min_value=1.0, max_value=8.0, value=2.0, step=0.25)
        grade = st.slider("Skor Kualitas Konstruksi (BldgGrade)", min_value=1, max_value=13, value=7)
    
    with col2:
        age = st.number_input("Umur Bangunan (Tahun)", min_value=0, max_value=120, value=15)
        park = st.number_input("Jarak ke Taman Terdekat (Km)", min_value=0.0, max_value=50.0, value=0.5)
        school = st.number_input("Jarak ke Sekolah Terdekat (Km)", min_value=0.0, max_value=50.0, value=0.3)
        hospital = st.number_input("Jarak ke Rumah Sakit Terdekat (Km)", min_value=0.0, max_value=50.0, value=1.2)
        
    st.subheader("📍 Lokasi Kawasan Properti")
    selected_zip = st.selectbox("Pilih Kode Pos (ZipCode Prestise)", sorted(all_zipcodes))
    
    # 4. Memproses Input Menjadi Matriks DataFrame Sesuai Model Training
    if st.button("🚀 Hitung Estimasi Harga Rumah", type="primary"):
        # Buat template data berisi angka 0 untuk seluruh fitur final
        input_data = pd.DataFrame(0, index=[0], columns=features_final)
        
        # Isi nilai fitur dasar
        input_data['SqFtTotLiving'] = sqft
        input_data['Bedrooms'] = bedrooms
        input_data['Bathrooms'] = bathrooms
        input_data['BldgGrade'] = grade
        input_data['HouseAge'] = age
        input_data['dist_to_park'] = park
        input_data['dist_to_school'] = school
        input_data['dist_to_hospital'] = hospital
        
        # Aktifkan kolom dummy ZipCode yang dipilih menjadi angka 1
        target_dummy_col = f"ZipCode_{selected_zip}"
        if target_dummy_col in input_data.columns:
            input_data[target_dummy_col] = 1
            
        # 5. Eksekusi Prediksi AI
        prediksi_log = model.predict(input_data)
        
        # KUNCI UTAMA: Balikkan nilai logaritma ke mata uang asli memakai np.exp()
        harga_final = np.exp(prediksi_log[0])
        
        # 6. Tampilkan Hasil Ke Layar
        st.markdown("---")
        st.success(f"### 🎉 Hasil Valuasi AI: **${harga_final:,.2f}**")
        st.caption("Catatan: Prediksi ini dihitung menggunakan akurasi model final sebesar 94.56% berdasarkan parameter spasial.")

except FileNotFoundError:
    st.error("Gagal memuat sistem. Pastikan file 'model_harga_properti.pkl' dan 'daftar_fitur.pkl' sudah diletakkan di folder yang sama.")
